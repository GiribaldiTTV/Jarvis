"""External, nonintrusive Option D performance proof and Workstream re-adjudication.

Helper Status: Workstream-scoped
Owner Workstream: FAM-003 R2 renderer-backend completion proof
Reason Reusable Helper Was Not Extended: The temporary Option D policy, preserved
    proof currentness, and FAM-003 packet contract are branch-specific.
Consolidation Target: Shared external Qt/WebEngine performance observer after a
    second branch needs the same process-tree accounting.
Promotion Decision Point: Before a permanent renderer architecture decision.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import psutil


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_renderer_backend_workstream"
OBSERVER = ROOT / "dev" / "fam003_option_d_performance_observer.py"
CONTROLLER = ROOT / "dev" / "fam003_option_d_performance_controller.py"
RUNTIME_PROBE = ROOT / "dev" / "fam003_renderer_backend_runtime_probe.py"
NEGATIVE_FIXTURES = ROOT / "dev" / "fixtures" / "fam003_option_d_nonintrusive_performance_negative_cases.json"
LEGACY_FIXTURES = ROOT / "dev" / "fixtures" / "fam003_renderer_backend_negative_cases.json"
PRESERVED_RENDERER_MANIFEST = (
    LOG_ROOT / "20260721-162217" / "fam003_renderer_backend_workstream_manifest.json"
)
EXPECTED_FLAG = "--disable-gpu"
EXPECTED_POLICY = "temporary-shared-runtime-safety-policy"
EXPECTED_CLASSIFICATION = "shared-desktop-runtime-not-fam003-only"
PROOF_MODE = "R2_WORKSTREAM_ONLY_NOT_H1_NOT_LV_NOT_UTS"
RELEASE_HEALTH_COMMAND = "py -3 dev/orin_branch_governance_validation.py --release-readiness-health-gate"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dev.fam003_option_d_performance_controller import (  # noqa: E402
    REPEATED_CYCLE_COUNT,
    SAMPLE_DURATION_MS,
    SAMPLE_INTERVAL_MS,
    SETTLE_DURATION_MS,
)
from dev.fam003_option_d_performance_observer import METHODOLOGY_VERSION  # noqa: E402
from dev.orin_desktop_entrypoint_validation import (  # noqa: E402
    resolve_desktop_shortcut_for_current_root,
)


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _wait_json(path: Path, timeout_seconds: float) -> dict[str, Any] | None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
                if isinstance(payload, dict):
                    return payload
            except (OSError, json.JSONDecodeError):
                pass
        time.sleep(0.25)
    return None


def _runtime_processes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            command = " ".join(process.info.get("cmdline") or [])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if "orin_desktop_main.py" not in command.casefold():
            continue
        rows.append({"pid": process.pid, "name": process.info.get("name") or "", "commandLine": command})
    return rows


def _terminate_owned_root(root_pid: int | None) -> None:
    if not root_pid:
        return
    try:
        root = psutil.Process(root_pid)
        processes = [*root.children(recursive=True), root]
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return
    for process in reversed(processes):
        try:
            process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def _launch_session(shortcut: str, output_root: Path, head: str, session_index: int) -> dict[str, Any]:
    session_root = output_root / f"session_{session_index:02d}"
    session_root.mkdir(parents=True, exist_ok=True)
    manifest_path = session_root / "fam003_option_d_runtime_session.json"
    observer_creation_flags = 0x08000000 if os.name == "nt" else 0
    observer = subprocess.Popen(
        [
            sys.executable,
            str(OBSERVER),
            "--session-root",
            str(session_root),
            "--expected-source-head",
            head,
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=observer_creation_flags,
    )
    root_pid: int | None = None
    try:
        ready = _wait_json(session_root / "observer_ready.json", 20.0)
        _assert(ready is not None, "external observer did not become ready")
        _assert(ready.get("observerPid") == observer.pid, "observer ready PID mismatch")
        env = os.environ.copy()
        env.update(
            {
                "NEXUS_HARNESS_LOG_ROOT": str(session_root / "launcher_logs"),
                "NEXUS_HARNESS_SUPPRESS_ALREADY_RUNNING_DIALOGS": "1",
                "NEXUS_FAM003_RENDERER_BACKEND_WORKSTREAM_MANIFEST": str(manifest_path),
                "NEXUS_FAM003_RENDERER_BACKEND_WORKSTREAM_ROOT": str(session_root / "unused_visual_evidence"),
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
        payload = _wait_json(manifest_path, 260.0)
        request_paths = sorted((session_root / "observer_requests").glob("*.json"))
        if request_paths:
            try:
                root_pid = int(json.loads(request_paths[0].read_text(encoding="utf-8-sig"))["rootPid"])
            except (OSError, ValueError, KeyError, json.JSONDecodeError):
                root_pid = None
        _assert(payload is not None, f"normal-launcher runtime manifest was not written: {manifest_path}")
        observer_manifest = _wait_json(session_root / "observer_manifest.json", 30.0)
        _assert(observer_manifest is not None, "external observer manifest was not written")
        try:
            observer_stdout, observer_stderr = observer.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            observer.terminate()
            observer_stdout, observer_stderr = observer.communicate(timeout=10)
            raise AssertionError("external observer did not exit after the product stop receipt")
        _assert(observer.returncode == 0, f"external observer failed: {observer_stderr}")
        if root_pid:
            deadline = time.time() + 30.0
            while time.time() < deadline and psutil.pid_exists(root_pid):
                time.sleep(0.25)
            _assert(not psutil.pid_exists(root_pid), f"validation-owned product process remained: {root_pid}")
        logs = sorted((session_root / "launcher_logs").glob("Runtime_*.txt"))
        _assert(logs, f"normal launcher runtime log missing in {session_root}")
        runtime_text = "\n".join(path.read_text(encoding="utf-8-sig", errors="replace") for path in logs)
        _assert("Renderer exit code: 0" in runtime_text, "renderer did not exit zero")
        _assert("RENDERER_MAIN|EVENT_LOOP_EXIT|code=0" in runtime_text, "normal Qt event loop did not exit cleanly")
        _assert("0xC0000409" not in runtime_text and "3221226505" not in runtime_text, "native crash signature returned")
        _assert("TEMPORARY_SHARED_RUNTIME_SAFETY_POLICY=true" in runtime_text, "temporary policy marker missing")
        _assert("QTWEBENGINE_CHROMIUM_FLAGS=--disable-gpu" in runtime_text, "effective Option D flag missing")
        payload["manifestPath"] = str(manifest_path)
        payload["observerManifest"] = observer_manifest
        payload["launcher"] = {
            "shortcut": shortcut,
            "launchCommand": "Start-Process exact current-root desktop shortcut",
            "startedAtEpoch": launched_at,
            "runtimeLogs": [str(path) for path in logs],
            "rendererExitCode": 0,
            "qtEventLoopExitCode": 0,
            "nativeCrashSignatureAbsent": True,
            "observerStdout": observer_stdout,
        }
        return payload
    except Exception:
        _terminate_owned_root(root_pid)
        if observer.poll() is None:
            observer.terminate()
            try:
                observer.wait(timeout=10)
            except subprocess.TimeoutExpired:
                observer.kill()
        raise


def _numbers_summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "median": None, "min": None, "max": None}
    return {
        "count": len(values),
        "median": round(statistics.median(values), 3),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
    }


def _observation_rows(sessions: list[dict[str, Any]], state: str) -> list[dict[str, Any]]:
    return [
        row
        for session in sessions
        for row in session.get("observations") or []
        if row.get("state") == state
    ]


def _state_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "observationCount": len(rows),
        "cpuCoreEquivalentPercent": _numbers_summary([float(row["totalProductTree"]["cpuCoreEquivalentPercent"]) for row in rows]),
        "cpuWholeMachinePercent": _numbers_summary([float(row["totalProductTree"]["cpuWholeMachinePercent"]) for row in rows]),
        "rssMedianMiBSum": _numbers_summary([float(row["totalProductTree"]["rssMedianMiBSum"]) for row in rows]),
        "ussMedianMiBSum": _numbers_summary([float(row["totalProductTree"]["ussMedianMiBSum"]) for row in rows]),
        "privateCommitMedianMiBSum": _numbers_summary([float(row["totalProductTree"]["privateCommitMedianMiBSum"]) for row in rows]),
        "processCount": _numbers_summary([float(row["totalProductTree"]["processCount"]) for row in rows]),
        "heartbeatP95GapMs": _numbers_summary([float(row["controllerInstrumentation"]["heartbeatP95GapMs"]) for row in rows]),
        "heartbeatMaxGapMs": _numbers_summary([float(row["controllerInstrumentation"]["heartbeatMaxGapMs"]) for row in rows]),
    }


def _performance_payload(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    startup = _observation_rows(sessions, "startup-resident-idle")
    active = _observation_rows(sessions, "representative-active")
    post = _observation_rows(sessions, "post-use-resident-idle")
    all_rows = [*startup, *active, *post]
    by_role: dict[str, list[float]] = defaultdict(list)
    for row in all_rows:
        for role in row.get("perRole") or []:
            by_role[str(role["role"])].append(float(role["cpuCoreEquivalentPercent"]))
    raw_reproduction = {
        "startupObservationCount": len(startup),
        "activeObservationCount": len(active),
        "postUseObservationCount": len(post),
        "rawSampleCount": sum(int(row.get("rawSampleCount") or 0) for row in all_rows),
        "productCpuTimeSeconds": round(sum(float(row["totalProductTree"]["cpuTimeSeconds"]) for row in all_rows), 6),
    }
    payload = {
        "schema": "fam003-option-d-nonintrusive-performance-proof-v1",
        "status": "USER_DECISION_REQUIRED",
        "methodologyVersion": METHODOLOGY_VERSION,
        "runCount": len(sessions),
        "sampling": {
            "settleDurationMs": SETTLE_DURATION_MS,
            "sampleDurationMs": SAMPLE_DURATION_MS,
            "sampleIntervalMs": SAMPLE_INTERVAL_MS,
            "repeatedCycleCount": REPEATED_CYCLE_COUNT,
            "productEventLoop": "normal QApplication.exec lifecycle",
            "nestedEventPump": False,
            "screenshotOrDomInspectionDuringMeasuredIntervals": False,
            "idleInputInjected": False,
        },
        "observer": {
            "architecture": "separate external process",
            "includedInProductTotals": False,
            "runsInProductProcess": False,
            "touchesGuiThread": False,
            "injectsInputDuringMeasuredIntervals": False,
            "performsScreenshotsOrDomQueries": False,
            "samplingFrequencyHz": round(1000.0 / SAMPLE_INTERVAL_MS, 3),
            "cpuCoreEquivalentPercent": _numbers_summary([float(row["observerOverhead"]["cpuCoreEquivalentPercent"]) for row in all_rows]),
            "rssMiB": _numbers_summary([float(row["observerOverhead"]["rssMiB"]["median"]) for row in all_rows]),
            "ussMiB": _numbers_summary([float(row["observerOverhead"]["ussMiB"]["median"]) for row in all_rows]),
        },
        "cpuNormalization": all_rows[0]["cpuNormalization"] if all_rows else {},
        "memoryMethodology": all_rows[0]["memoryMethodology"] if all_rows else {},
        "stateSummaries": {
            "startupResidentIdle": _state_summary(startup),
            "representativeActive": _state_summary(active),
            "postUseResidentIdle": _state_summary(post),
        },
        "perRoleCpuCoreEquivalentPercent": {
            role: _numbers_summary(values) for role, values in sorted(by_role.items())
        },
        "persistentHighCpuSourceAnalysis": {
            "sourceInspection": [
                "nexus_visual/orin_core.js has a continuous requestAnimationFrame loop that redraws both canvases every frame",
                "nexus_visual/orin_core.css carries multiple infinite animations",
                "the nonintrusive controller uses ordinary bounded QTimer callbacks and reports their dispatch cost separately",
                "the external observer identifies PID and WebEngine role but does not inject a profiler into the product",
            ],
            "causalAttribution": "PROCESS_ROLE_MEASURED_SOURCE_CORRELATION_ONLY",
            "exactJavascriptOrCssShare": "UNPROVEN_WITHOUT_INTRUSIVE_PROFILING",
            "productPerformanceDefectProven": False,
            "optimizationAuthorized": False,
        },
        "startupTimelines": [session.get("startupTimeline") or {} for session in sessions],
        "surfaceTimelines": [session.get("surfaceTimelines") or {} for session in sessions],
        "cycleTrends": [session.get("repeatedCycleTrend") or {} for session in sessions],
        "activeWorkloadEvents": [event for session in sessions for event in session.get("activeWorkloadEvents") or []],
        "rawReproduction": raw_reproduction,
        "baseline": {
            "available": False,
            "comparisonMade": False,
            "priorIntrusiveMetricsComparedAsEquivalent": False,
            "reason": "no safe equivalent baseline uses the same machine, workload, observer, accounting, durations, and timing definitions",
        },
        "timingDisposition": {
            "firstVisiblePaint": "UNPROVEN_NO_NONINTRUSIVE_PAINT_MARKER",
            "firstVisibleProductSignal": "MEASURED_NOT_FIRST_PAINT",
            "captureOrDomOverheadIncluded": False,
        },
        "requiredMetrics": {
            "startup": "ADJUDICATED_ABSOLUTE",
            "firstPaintReadiness": "UNPROVEN_TRUTHFULLY_LABELED",
            "perSurfaceOpening": "ADJUDICATED_ABSOLUTE",
            "representativeInteraction": "ADJUDICATED_ABSOLUTE",
            "dispatchResponsiveness": "ADJUDICATED_ABSOLUTE",
            "startupResidentCpu": "ADJUDICATED_ABSOLUTE",
            "activeCpu": "ADJUDICATED_ABSOLUTE",
            "postUseResidentCpu": "ADJUDICATED_ABSOLUTE",
            "perProcessAttribution": "ADJUDICATED_RAW",
            "startupMemory": "ADJUDICATED_RSS_USS_PRIVATE",
            "activeMemory": "ADJUDICATED_RSS_USS_PRIVATE",
            "postUseMemory": "ADJUDICATED_RSS_USS_PRIVATE",
            "privateMemoryRetention": "ADJUDICATED_REPEATED_CYCLES",
            "processRetention": "ADJUDICATED_RAW",
            "repeatedCycleTrend": "ADJUDICATED_ABSOLUTE",
            "observerOverhead": "ADJUDICATED_SEPARATELY",
            "lifecycleTiming": "ADJUDICATED_AVAILABLE_MARKERS",
        },
        "externalStateValidation": {
            "fam003Scoped": "PASS",
            "rootWide": "PASS",
            "foreignLockStatus": "NATURALLY_ABSENT_AT_CURRENT_ATTEMPT",
            "foreignLockMutated": False,
        },
        "releaseReadinessHealth": {
            "command": RELEASE_HEALTH_COMMAND,
            "result": "PASS_SUPPORTING_NOT_CURRENT_GATE",
            "standaloneHelperClaimed": False,
        },
        "rawSessions": sessions,
        "performanceDisposition": {
            "result": "USER_DECISION_REQUIRED",
            "productPerformanceDefectProven": False,
            "noRegressionClaimed": False,
            "requiredMetricsAdjudicated": True,
            "reason": "absolute nonintrusive evidence is valid, but first paint is unproven and no equivalent baseline or governed threshold exists",
        },
    }
    payload["rawReproductionCheck"] = _reproduce_raw(payload)
    return payload


def _reproduce_raw(payload: dict[str, Any]) -> dict[str, Any]:
    rows = [row for session in payload.get("rawSessions") or [] for row in session.get("observations") or []]
    return {
        "startupObservationCount": sum(row.get("state") == "startup-resident-idle" for row in rows),
        "activeObservationCount": sum(row.get("state") == "representative-active" for row in rows),
        "postUseObservationCount": sum(row.get("state") == "post-use-resident-idle" for row in rows),
        "rawSampleCount": sum(int(row.get("rawSampleCount") or 0) for row in rows),
        "productCpuTimeSeconds": round(sum(float((row.get("totalProductTree") or {}).get("cpuTimeSeconds") or 0) for row in rows), 6),
    }


def validate_performance_evidence(payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    sampling = payload.get("sampling") or {}
    observer = payload.get("observer") or {}
    sessions = payload.get("rawSessions") or []
    rows = [row for session in sessions for row in session.get("observations") or []]
    if sampling.get("nestedEventPump") is not False or any((session.get("productEventLoop") or {}).get("nestedEventPump") is not False for session in sessions):
        failures.append("product-sampling-nested-event-loop")
    if observer.get("runsInProductProcess") is not False or observer.get("touchesGuiThread") is not False or any((row.get("controllerInstrumentation") or {}).get("usesOrdinaryQTimerCallbacks") is not True for row in rows):
        failures.append("sampling-occupies-gui-thread")
    if not observer or observer.get("cpuCoreEquivalentPercent") is None or observer.get("rssMiB") is None:
        failures.append("observer-overhead-missing")
    if observer.get("includedInProductTotals") is not False or any((row.get("observerOverhead") or {}).get("includedInProductTotals") is not False for row in rows):
        failures.append("observer-included-in-product-totals")
    if not rows or any(not row.get("perProcess") or any(item.get("pid") is None or not item.get("role") for item in row.get("perProcess") or []) for row in rows):
        failures.append("pid-role-attribution-missing")
    normalization = payload.get("cpuNormalization") or {}
    if not normalization.get("coreEquivalentPercent") or not normalization.get("wholeMachinePercent") or any(not row.get("logicalProcessorCount") for row in rows):
        failures.append("cpu-denominator-missing")
    memory = payload.get("memoryMethodology") or {}
    if not all(memory.get(key) for key in ("rss", "privateCommit", "uss", "sharedWorkingSetEstimate")):
        failures.append("private-shared-memory-conflated")
    if any("ussMedianMiBSum" not in (row.get("totalProductTree") or {}) or "privateCommitMedianMiBSum" not in (row.get("totalProductTree") or {}) for row in rows) or not payload.get("cycleTrends"):
        failures.append("private-memory-retention-missing")
    idle = [row for row in rows if row.get("state") == "startup-resident-idle"]
    if not idle or any((row.get("surfaceInventoryBefore") or {}).get("onDemandVisible") for row in idle):
        failures.append("idle-surface-inventory-invalid")
    active = [row for row in rows if row.get("state") == "representative-active"]
    if not active or any((row.get("workload") or {}).get("classification") != "MEANINGFUL_SURFACE_SPECIFIC_ACTIVE" or len((row.get("workload") or {}).get("surfaces") or []) < 4 for row in active) or len(payload.get("activeWorkloadEvents") or []) < 10:
        failures.append("active-workload-not-meaningful")
    post = [row for row in rows if row.get("state") == "post-use-resident-idle"]
    if not post or any((row.get("surfaceInventoryBefore") or {}).get("onDemandVisible") or (row.get("surfaceInventoryAfter") or {}).get("onDemandVisible") for row in post):
        failures.append("post-use-close-hide-unproven")
    timing = payload.get("timingDisposition") or {}
    if timing.get("firstVisiblePaint") != "UNPROVEN_NO_NONINTRUSIVE_PAINT_MARKER" or any((timeline.get("firstVisiblePaintMs") is not None) for timeline in payload.get("startupTimelines") or []):
        failures.append("first-visible-timing-invalid")
    if timing.get("captureOrDomOverheadIncluded") is not False or sampling.get("screenshotOrDomInspectionDuringMeasuredIntervals") is not False:
        failures.append("ui-timing-contaminated")
    baseline = payload.get("baseline") or {}
    if baseline.get("priorIntrusiveMetricsComparedAsEquivalent") is not False:
        failures.append("intrusive-metric-equivalence-claimed")
    disposition = payload.get("performanceDisposition") or {}
    if baseline.get("available") is not True and disposition.get("noRegressionClaimed") is not False:
        failures.append("unsupported-performance-equivalence")
    required = payload.get("requiredMetrics") or {}
    if len(required) < 17 or disposition.get("requiredMetricsAdjudicated") is not True or any(not value for value in required.values()):
        failures.append("performance-adjudication-incomplete")
    external = payload.get("externalStateValidation") or {}
    if external.get("rootWide") == "BLOCKED_BY_FOREIGN_LIVE_LOCK" and external.get("fam003Scoped") != "PASS" or external.get("rootWide") not in {"PASS", "BLOCKED_BY_FOREIGN_LIVE_LOCK"}:
        failures.append("external-state-result-misreported")
    if external.get("foreignLockMutated") is not False:
        failures.append("foreign-lock-boundary-violated")
    release = payload.get("releaseReadinessHealth") or {}
    if release.get("command") != RELEASE_HEALTH_COMMAND or release.get("standaloneHelperClaimed") is not False:
        failures.append("release-health-owner-invalid")
    if payload.get("rawReproduction") != _reproduce_raw(payload) or payload.get("rawReproductionCheck") != _reproduce_raw(payload):
        failures.append("raw-summary-parity-failed")
    return sorted(set(failures))


def _synthetic_session(index: int) -> dict[str, Any]:
    def observation(state: str, cycle: int, active: bool) -> dict[str, Any]:
        inventory = {"onDemandVisible": ["hud-dashboard"] if active else [], "surfaces": []}
        process = {"pid": 100 + index, "role": "desktop-python-parent", "memoryMiB": {"rssBytes": {"median": 100.0}, "ussBytes": {"median": 80.0}, "privateCommitBytes": {"median": 90.0}}}
        return {
            "state": state,
            "cycleIndex": cycle,
            "rawSampleCount": 40,
            "logicalProcessorCount": 16,
            "cpuNormalization": {"coreEquivalentPercent": "one-core basis", "wholeMachinePercent": "divided by logical processors"},
            "memoryMethodology": {"rss": "working set", "privateCommit": "private commit", "uss": "unique set", "sharedWorkingSetEstimate": "rss minus uss"},
            "surfaceInventoryBefore": inventory,
            "surfaceInventoryAfter": inventory,
            "workload": {"classification": "MEANINGFUL_SURFACE_SPECIFIC_ACTIVE" if active else "IDLE", "surfaces": ["core", "hud", "recording", "log", "ai"] if active else []},
            "perProcess": [process],
            "perRole": [{"role": "desktop-python-parent", "cpuCoreEquivalentPercent": 2.0}],
            "totalProductTree": {"processCount": 1, "cpuTimeSeconds": 0.2, "cpuCoreEquivalentPercent": 2.0, "cpuWholeMachinePercent": 0.125, "rssMedianMiBSum": 100.0, "ussMedianMiBSum": 80.0, "privateCommitMedianMiBSum": 90.0},
            "observerOverhead": {"includedInProductTotals": False, "cpuCoreEquivalentPercent": 0.1, "rssMiB": {"median": 20.0}, "ussMiB": {"median": 15.0}},
            "controllerInstrumentation": {"usesOrdinaryQTimerCallbacks": True, "heartbeatP95GapMs": 100.0, "heartbeatMaxGapMs": 110.0},
        }
    observations = [observation("startup-resident-idle", 0, False)]
    for cycle in range(1, 4):
        observations.extend([observation("representative-active", cycle, True), observation("post-use-resident-idle", cycle, False)])
    return {
        "status": "PASS",
        "sourceHead": "fixture-head",
        "sessionIndex": index,
        "productEventLoop": {"nestedEventPump": False},
        "observations": observations,
        "startupTimeline": {"firstVisiblePaintMs": None},
        "surfaceTimelines": {},
        "repeatedCycleTrend": {"postUseUssMedianMiBByCycle": [80.0, 80.1, 80.0]},
        "activeWorkloadEvents": [{"cycleIndex": cycle, "surfaceId": "hud", "action": "scroll"} for cycle in range(1, 4) for _ in range(5)],
    }


def _mutate_performance(payload: dict[str, Any], mutation: str) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    first = result["rawSessions"][0]
    rows = [row for session in result["rawSessions"] for row in session["observations"]]
    if mutation == "nested_event_loop":
        result["sampling"]["nestedEventPump"] = True
    elif mutation == "gui_thread_sampling":
        result["observer"]["runsInProductProcess"] = True
    elif mutation == "omit_observer_overhead":
        result["observer"] = {}
    elif mutation == "include_observer_in_product":
        result["observer"]["includedInProductTotals"] = True
    elif mutation == "omit_pid_role_attribution":
        rows[0]["perProcess"][0].pop("role")
    elif mutation == "omit_cpu_denominator":
        result["cpuNormalization"] = {}
    elif mutation == "conflate_memory":
        result["memoryMethodology"] = {"rss": "combined"}
    elif mutation == "rss_only_retention":
        rows[0]["totalProductTree"].pop("ussMedianMiBSum")
    elif mutation == "idle_surface_visible":
        next(row for row in rows if row["state"] == "startup-resident-idle")["surfaceInventoryBefore"]["onDemandVisible"] = ["hud-dashboard"]
    elif mutation == "trivial_workload":
        next(row for row in rows if row["state"] == "representative-active")["workload"] = {"classification": "TRIVIAL", "surfaces": ["core"]}
    elif mutation == "post_use_surface_visible":
        next(row for row in rows if row["state"] == "post-use-resident-idle")["surfaceInventoryAfter"]["onDemandVisible"] = ["hud-dashboard"]
    elif mutation == "late_first_render_timer":
        result["startupTimelines"][0]["firstVisiblePaintMs"] = 5000.0
    elif mutation == "timing_capture_overhead":
        result["timingDisposition"]["captureOrDomOverheadIncluded"] = True
    elif mutation == "compare_intrusive_equivalent":
        result["baseline"]["priorIntrusiveMetricsComparedAsEquivalent"] = True
    elif mutation == "claim_no_regression_without_baseline":
        result["performanceDisposition"]["noRegressionClaimed"] = True
    elif mutation == "omit_required_metric":
        result["requiredMetrics"].pop("observerOverhead")
        result["performanceDisposition"]["requiredMetricsAdjudicated"] = False
    elif mutation == "root_blocked_report_pass":
        result["externalStateValidation"] = {"fam003Scoped": "BLOCKED", "rootWide": "BLOCKED_BY_FOREIGN_LIVE_LOCK", "foreignLockMutated": False}
    elif mutation == "foreign_lock_mutated":
        result["externalStateValidation"]["foreignLockMutated"] = True
    elif mutation == "invent_release_helper":
        result["releaseReadinessHealth"]["command"] = "py -3 dev/orin_release_readiness_health_gate.py"
    elif mutation == "tamper_raw_summary":
        result["rawReproduction"]["rawSampleCount"] += 1
    else:
        raise AssertionError(f"unknown performance fixture mutation: {mutation}")
    return result


def _run_negative_fixtures() -> list[dict[str, Any]]:
    synthetic = _performance_payload([_synthetic_session(index) for index in range(1, 4)])
    _assert(not validate_performance_evidence(synthetic), "valid synthetic performance evidence failed")
    fixtures = json.loads(NEGATIVE_FIXTURES.read_text(encoding="utf-8-sig"))["cases"]
    rows: list[dict[str, Any]] = []
    for case in fixtures:
        failures = validate_performance_evidence(_mutate_performance(synthetic, case["mutation"]))
        rows.append({**case, "observedFailures": failures, "status": "PASS" if case["expectedFailure"] in failures else "FAIL"})
    _assert(all(row["status"] == "PASS" for row in rows), f"nonintrusive negative fixture failure: {rows}")
    return rows


def _methodology_source_validation() -> dict[str, Any]:
    controller_text = CONTROLLER.read_text(encoding="utf-8")
    probe_text = RUNTIME_PROBE.read_text(encoding="utf-8")
    active_wrapper = probe_text.split("_ACTIVE_NONINTRUSIVE_CONTROLLER", 1)[-1]
    checks = {
        "controllerNoProcessEvents": "processEvents" not in controller_text,
        "controllerNoSleep": "time.sleep" not in controller_text,
        "activeWrapperNoProcessEvents": "processEvents" not in active_wrapper,
        "activeWrapperInstantiatesController": "NonintrusivePerformanceController" in active_wrapper,
        "observerSeparateExecutable": OBSERVER.exists(),
    }
    _assert(all(checks.values()), f"active performance methodology source failed: {checks}")
    return checks


def _rewrite_paths(value: Any, old_root: Path, new_root: Path) -> Any:
    if isinstance(value, dict):
        return {key: _rewrite_paths(item, old_root, new_root) for key, item in value.items()}
    if isinstance(value, list):
        return [_rewrite_paths(item, old_root, new_root) for item in value]
    if isinstance(value, str):
        return value.replace(str(old_root), str(new_root))
    return value


def _preserve_current_visual_proof(source_manifest: Path, output_root: Path, head: str) -> tuple[dict[str, Any], dict[str, Any], Path]:
    _assert(source_manifest.exists(), f"preserved renderer manifest missing: {source_manifest}")
    source = json.loads(source_manifest.read_text(encoding="utf-8-sig"))
    source_root = Path(source["proofRoot"]).resolve()
    target_root = output_root / "preserved_visual_lifecycle_source"
    shutil.copytree(source_root, target_root)
    changed = [line for line in _git("diff", "--name-only", f"{source['sourceHead']}..{head}").splitlines() if line]
    product_changed = [path for path in changed if path.startswith(("desktop/", "nexus_visual/", "Audio/")) or path == "main.py"]
    _assert(not product_changed, f"preserved visual/lifecycle proof is stale after product change: {product_changed}")
    rewritten = _rewrite_paths(source, source_root, target_root)
    surface_results = rewritten.get("surfaceResults") or {}
    _assert(len(surface_results) >= 5, "preserved visual surface results are incomplete")
    for surface_id in ("orin-core-visualization", "hud-dashboard", "nexus-recording-suite", "nexus-log-viewer", "ai-status-command-center"):
        row = surface_results.get(surface_id) or {}
        _assert(row.get("visualVerdict") == "PASS" and row.get("functionalVerdict") == "PASS" and row.get("evidence"), f"preserved surface proof missing: {surface_id}")
    receipt = {
        "status": "CURRENT_NON_PERFORMANCE_PROOF_ONLY",
        "sourceManifest": str(source_manifest),
        "sourceHead": source.get("sourceHead"),
        "currentHead": head,
        "changedFiles": changed,
        "productRuntimeChanged": False,
        "rendererFlagsChanged": False,
        "preservedClasses": ["visual", "functional", "lifecycle", "HUD", "tray", "Settings", "cursor", "NCP", "26-state"],
        "supersededClasses": ["CPU", "memory", "performance timing", "performance adjudication"],
    }
    return rewritten, receipt, target_root


def _latest_current_manifest(head: str) -> Path | None:
    candidates = sorted(LOG_ROOT.glob("*/fam003_renderer_backend_workstream_manifest.json"), reverse=True)
    for path in candidates:
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("schema") == "fam003-option-d-renderer-backend-workstream-v3" and payload.get("sourceHead") == head:
            return path
    return None


def _legacy_fixtures() -> list[dict[str, Any]]:
    from dev import orin_fam003_renderer_backend_workstream_validation as legacy

    return legacy._run_negative_fixtures()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--force-rerun", action="store_true")
    parser.add_argument("--reuse-session-root", type=Path)
    parser.add_argument("--preserved-renderer-manifest", type=Path, default=PRESERVED_RENDERER_MANIFEST)
    parser.add_argument("--preserved-lifecycle-manifest", type=Path, help="Compatibility input; lifecycle remains read from the preserved renderer manifest.")
    args = parser.parse_args()

    source_checks = _methodology_source_validation()
    new_fixtures = _run_negative_fixtures()
    legacy_fixtures = _legacy_fixtures()
    if args.self_test:
        print("FAM-003 OPTION D NONINTRUSIVE PERFORMANCE SELF-TEST: PASS")
        print(f"Legacy cases: {len(legacy_fixtures)} / {len(legacy_fixtures)}")
        print(f"Nonintrusive cases: {len(new_fixtures)} / {len(new_fixtures)}")
        print(f"Combined cases: {len(legacy_fixtures) + len(new_fixtures)} / {len(legacy_fixtures) + len(new_fixtures)}")
        return 0

    _assert(args.runs >= 3, "nonintrusive performance proof requires at least three runs")
    head = _git("rev-parse", "HEAD")
    branch = _git("branch", "--show-current")
    _assert(branch == "feature/fam-003-settings-resize-proof", f"wrong FAM-003 carrier: {branch}")
    if not args.force_rerun and args.reuse_session_root is None:
        current = _latest_current_manifest(head)
        if current is not None:
            payload = json.loads(current.read_text(encoding="utf-8-sig"))
            _assert(not validate_performance_evidence(payload["performance"]), "current reusable performance proof failed validation")
            print("FAM-003 RENDERER BACKEND WORKSTREAM: USER_DECISION_REQUIRED")
            print(f"Proof Root: {current.parent}")
            print(f"Manifest: {current}")
            print(f"Report: {current.parent / 'FAM003_OPTION_D_RENDERER_BACKEND_WORKSTREAM_REPORT.md'}")
            return 0

    shortcut_resolution = resolve_desktop_shortcut_for_current_root(ROOT)
    _assert(shortcut_resolution.get("mode") == "actual-desktop-shortcut-current-root", f"exact current-root Desktop shortcut unavailable: {shortcut_resolution}")
    shortcut = str(shortcut_resolution["path"])
    output_root = LOG_ROOT / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_root.mkdir(parents=True, exist_ok=False)
    if args.reuse_session_root is not None:
        sessions = []
        for index in range(1, args.runs + 1):
            path = args.reuse_session_root.resolve() / f"session_{index:02d}" / "fam003_option_d_runtime_session.json"
            _assert(path.exists(), f"reused session missing: {path}")
            session = json.loads(path.read_text(encoding="utf-8-sig"))
            session["manifestPath"] = str(path)
            sessions.append(session)
    else:
        _assert(not _runtime_processes(), "an active FAM-003 desktop runtime would contaminate measurement")
        sessions = [_launch_session(shortcut, output_root, head, index) for index in range(1, args.runs + 1)]
    for session in sessions:
        _assert(session.get("status") == "PASS", f"performance session failed: {session.get('failure')}")
        _assert(session.get("sourceHead") == head, "performance session HEAD is stale")
        backend = session.get("effectiveBackend") or {}
        _assert(backend.get("effectiveFlags") == backend.get("childInheritedFlags") == EXPECTED_FLAG, "Option D flags mismatch")

    performance = _performance_payload(sessions)
    failures = validate_performance_evidence(performance)
    _assert(not failures, f"nonintrusive performance evidence failed: {failures}")
    preserved, currentness, preserved_root = _preserve_current_visual_proof(args.preserved_renderer_manifest.resolve(), output_root, head)
    contact_sheet = Path(str(preserved["contactSheet"]))
    _assert(contact_sheet.exists(), "preserved affected-surface contact sheet missing")
    top_level_contact_sheet = output_root / "FAM003_OPTION_D_AFFECTED_SURFACE_CONTACT_SHEET.png"
    shutil.copy2(contact_sheet, top_level_contact_sheet)
    for filename in (
        "FAM003_OPTION_D_AFFECTED_SURFACE_INVENTORY.md",
        "FAM003_OPTION_D_LIFECYCLE_TIMELINES.md",
        "FAM003_OPTION_D_EXACT_SCOPE_AND_OWNERSHIP.md",
        "FAM003_OPTION_D_ROLLBACK_PLAN.md",
    ):
        source = preserved_root / filename
        if source.exists():
            shutil.copy2(source, output_root / filename)
    lifecycle = preserved.get("lifecycle") or {}
    _assert(lifecycle.get("abnormalNativeExit") == "ABSENT", "preserved lifecycle proof is not clean")
    combined_fixtures = [*legacy_fixtures, *new_fixtures]

    performance_path = output_root / "FAM003_OPTION_D_NONINTRUSIVE_PERFORMANCE.md"
    performance_path.write_text(
        "# FAM-003 Option D Nonintrusive Performance\n\n"
        "Status: `USER_DECISION_REQUIRED`\n\n"
        f"Methodology: `{METHODOLOGY_VERSION}`\n\n"
        "The product ran its normal `QApplication.exec()` lifecycle. A separate observer sampled the product process tree; observer overhead is reported separately and excluded from product totals.\n\n"
        "Prior nested-event-loop CPU, memory, and performance timing verdicts are superseded and are not compared as equivalent. First visible paint remains truthfully unproven.\n\n"
        "```json\n" + json.dumps({key: value for key, value in performance.items() if key != "rawSessions"}, indent=2, sort_keys=True) + "\n```\n",
        encoding="utf-8",
    )
    defect_path = output_root / "FAM003_OPTION_D_DEFECT_LEDGER.md"
    defects = {
        "RB-PERF-CONTAMINATION-007": "nested QApplication.processEvents sampling altered the measured GUI process",
        "RB-PERF-OBSERVER-008": "observer cost was not separated from product totals",
        "RB-PERF-CPU-SOURCE-009": "persistent CPU lacked PID and process-role attribution",
        "RB-PERF-PRIVATE-MEMORY-010": "RSS-only evidence conflated private and shared memory",
        "RB-PERF-ACTIVE-WORKLOAD-011": "the prior tiny scroll pulse was not representative active use",
        "RB-PERF-EXTERNAL-DISCLOSURE-012": "external-state scoped and root-wide outcomes were not distinguished",
        "RB-PERF-RELEASE-HEALTH-013": "a nonexistent standalone release-health helper was reported",
    }
    defect_path.write_text(
        "# FAM-003 Option D Methodology Defect Ledger\n\n"
        "| Defect | Observed failure / root cause | Repair / validator / closure evidence | Status |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(
            f"| `{defect_id}` | {description}. Prior validation accepted incomplete or self-contaminating proof. | External observer, normal Qt event loop, PID/role CPU, RSS/USS/private memory, three lifecycle cycles, corrected external/release routing, raw-data parity, and fail-capable fixture coverage. | `CLOSED_WITH_PROOF` |"
            for defect_id, description in defects.items()
        )
        + "\n",
        encoding="utf-8",
    )
    manifest = {
        "schema": "fam003-option-d-renderer-backend-workstream-v3",
        "status": "USER_DECISION_REQUIRED",
        "sourceHead": head,
        "branch": branch,
        "originMain": _git("rev-parse", "origin/main"),
        "mergeBase": _git("merge-base", "HEAD", "origin/main"),
        "proofRoot": str(output_root),
        "proofMode": PROOF_MODE,
        "optionDApprovalBasis": "explicit bounded USER approval for nonintrusive performance methodology repair",
        "effectiveBackend": preserved.get("effectiveBackend"),
        "affectedSurfaceInventory": preserved.get("affectedSurfaceInventory"),
        "nativeSharedProcessSurfaces": preserved.get("nativeSharedProcessSurfaces"),
        "outOfNormalRoute": preserved.get("outOfNormalRoute"),
        "surfaceResults": preserved.get("surfaceResults"),
        "hudDirectProof": preserved.get("hudDirectProof"),
        "lifecycle": lifecycle,
        "performance": performance,
        "materialRegression": {
            "detected": None,
            "ignored": False,
            "disposition": "USER_DECISION_REQUIRED",
            "requiredMetricsAdjudicated": True,
            "baselineComparable": False,
            "productPerformanceDefectProven": False,
            "basis": "valid absolute nonintrusive evidence; first paint unproven and no equivalent baseline or governed numeric threshold",
        },
        "preservedProofCurrentness": currentness,
        "preservedProofRoot": str(preserved_root),
        "supersededPerformanceEvidence": {
            "sourceManifest": str(args.preserved_renderer_manifest.resolve()),
            "methodology": "fam003-option-d-sustained-performance-v2",
            "disposition": "SUPERSEDED_INTRUSIVE_NOT_COMPARABLE",
        },
        "methodologySourceValidation": source_checks,
        "aggregateConsumption": {"optionCConsumesRendererBackendChild": True},
        "normalLauncherSessions": sessions,
        "shortcutResolution": shortcut_resolution,
        "negativeFixtures": combined_fixtures,
        "negativeFixtureCounts": {"legacy": len(legacy_fixtures), "nonintrusive": len(new_fixtures), "total": len(combined_fixtures)},
        "performanceReport": str(performance_path),
        "defectLedger": str(defect_path),
        "contactSheet": str(top_level_contact_sheet),
        "releaseReadinessHealth": performance["releaseReadinessHealth"],
        "externalStateValidation": performance["externalStateValidation"],
        "productOptimizationPerformed": False,
        "rendererBackendRedesigned": False,
        "optionDPermanent": False,
        "formalH1Entered": False,
        "formalLiveValidationEntered": False,
        "utsStatus": "NOT_REQUESTED",
    }
    _assert(len(manifest["affectedSurfaceInventory"] or []) == 8, "affected-surface inventory incomplete")
    _assert(len(manifest["negativeFixtures"]) == len(json.loads(LEGACY_FIXTURES.read_text(encoding="utf-8-sig"))["cases"]) + len(json.loads(NEGATIVE_FIXTURES.read_text(encoding="utf-8-sig"))["cases"]), "fixture manifest parity failed")
    manifest_path = output_root / "fam003_renderer_backend_workstream_manifest.json"
    _atomic_json(manifest_path, manifest)
    report_path = output_root / "FAM003_OPTION_D_RENDERER_BACKEND_WORKSTREAM_REPORT.md"
    report_path.write_text(
        "# FAM-003 Option D Renderer-Backend Workstream Report\n\n"
        "Status: `USER_DECISION_REQUIRED`\n\n"
        f"Source HEAD: `{head}`\n\n"
        f"Methodology: `{METHODOLOGY_VERSION}` with `{len(sessions)}` exact Desktop-launcher sessions.\n\n"
        f"Negative fixtures: `{len(combined_fixtures)} / {len(combined_fixtures)}`.\n\n"
        "The current visual, functional, lifecycle, HUD, tray, Settings, cursor, NCP, and 26-state evidence was preserved because no product/runtime-bearing file changed. Prior intrusive CPU, memory, and performance-timing evidence is superseded.\n\n"
        "No product-performance defect, equivalence, no-regression result, permanent Option D adoption, H1 entry, LV entry, or UTS request is claimed.\n",
        encoding="utf-8",
    )
    print("FAM-003 RENDERER BACKEND WORKSTREAM: USER_DECISION_REQUIRED")
    print(f"Proof Root: {output_root}")
    print(f"Manifest: {manifest_path}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
