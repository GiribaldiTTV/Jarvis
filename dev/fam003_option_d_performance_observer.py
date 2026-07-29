"""External process observer for FAM-003 Option D performance proof."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import psutil


METHODOLOGY_VERSION = "fam003-option-g-owner-attribution-v5"
DEFAULT_TIMEOUT_SECONDS = 420
USS_SAMPLE_EVERY_N_INTERVALS = 8
PROCESS_TREE_REFRESH_EVERY_N_INTERVALS = 4


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _cpu_seconds(process: psutil.Process) -> float:
    values = process.cpu_times()
    return float(values.user + values.system)


def _memory(process: psutil.Process, *, include_uss: bool) -> dict[str, int | str | None]:
    basic = process.memory_info()
    rss = int(getattr(basic, "rss", 0))
    basic_private = getattr(basic, "private", None)
    full = process.memory_full_info() if include_uss or basic_private is None else None
    private_commit = int((basic_private if basic_private is not None else getattr(full, "private", 0)) or 0)
    uss_value = getattr(full, "uss", None) if full is not None else None
    uss = int(uss_value) if uss_value is not None else None
    shared_estimate = max(0, rss - uss) if uss is not None else None
    return {
        "rssBytes": rss,
        "workingSetBytes": int(getattr(basic, "wset", rss) or rss),
        "privateCommitBytes": private_commit,
        "ussBytes": uss,
        "sharedWorkingSetEstimateBytes": shared_estimate,
        "privateMetricSource": "psutil.memory_info.private",
        "ussMetricSource": "psutil.memory_full_info.uss" if include_uss else "NOT_SAMPLED_THIS_INTERVAL",
        "sharedMetricDisposition": "DERIVED_RSS_MINUS_USS_ESTIMATE" if uss is not None else "UNAVAILABLE",
    }


def _command_line(process: psutil.Process) -> str:
    try:
        return " ".join(process.cmdline())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return ""


def _role(process: psutil.Process, root_pid: int) -> str:
    if process.pid == root_pid:
        return "desktop-python-parent"
    command = _command_line(process).casefold()
    if "qtwebengineprocess" in command:
        if "--type=renderer" in command:
            return "webengine-renderer"
        if "--type=gpu-process" in command:
            return "webengine-gpu-process"
        if "--type=utility" in command and "network" in command:
            return "webengine-network-utility"
        if "--type=utility" in command and "audio" in command:
            return "webengine-audio-utility"
        if "--type=utility" in command:
            return "webengine-utility"
        return "webengine-other"
    return "desktop-child-other"


def _product_tree(root_pid: int) -> list[psutil.Process]:
    try:
        root = psutil.Process(root_pid)
        return [root, *root.children(recursive=True)]
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return []


def _launcher_ancestors(root_pid: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        ancestors = psutil.Process(root_pid).parents()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return rows
    for process in ancestors:
        command = _command_line(process)
        if "orin_desktop_launcher.pyw" not in command.casefold():
            continue
        try:
            rows.append(
                {
                    "pid": process.pid,
                    "parentPid": process.ppid(),
                    "executable": process.exe(),
                    "commandLine": command,
                    "role": "normal-desktop-launcher",
                    "creationTimeEpoch": process.create_time(),
                    **_memory(process, include_uss=True),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return rows


def _process_snapshot(
    process: psutil.Process,
    root_pid: int,
    *,
    include_uss: bool,
    metadata_cache: dict[int, dict[str, Any]],
) -> dict[str, Any] | None:
    try:
        metadata = metadata_cache.get(process.pid)
        if metadata is None:
            metadata = {
                "pid": process.pid,
                "parentPid": process.ppid(),
                "executable": process.exe(),
                "name": process.name(),
                "commandLine": _command_line(process),
                "role": _role(process, root_pid),
                "creationTimeEpoch": process.create_time(),
            }
            metadata_cache[process.pid] = metadata
        return {
            **metadata,
            "cpuTimeSeconds": _cpu_seconds(process),
            **_memory(process, include_uss=include_uss),
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def _summary(values: list[int]) -> dict[str, float | int | None]:
    if not values:
        return {"median": None, "max": None, "final": None}
    return {
        "median": round(statistics.median(values) / (1024 * 1024), 3),
        "max": round(max(values) / (1024 * 1024), 3),
        "final": round(values[-1] / (1024 * 1024), 3),
    }


def _observe(request: dict[str, Any], observer: psutil.Process) -> dict[str, Any]:
    root_pid = int(request["rootPid"])
    duration_ms = int(request["sampleDurationMs"])
    interval_ms = int(request["sampleIntervalMs"])
    logical_cpu_count = max(1, int(psutil.cpu_count(logical=True) or 1))
    observer_cpu_start = _cpu_seconds(observer)
    observer_memory_samples: list[dict[str, int | str | None]] = []
    process_accumulator: dict[int, dict[str, Any]] = {}
    raw_samples: list[dict[str, Any]] = []
    cached_processes = {process.pid: process for process in _product_tree(root_pid)}
    initial_pids = set(cached_processes)
    started = time.perf_counter()
    previous_cpu: dict[int, float] = {}
    metadata_cache: dict[int, dict[str, Any]] = {}
    surface_renderer_map = list(request.get("surfaceRendererMap") or [])
    surface_rows_by_pid: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for surface_row in surface_renderer_map:
        renderer_pid = int(surface_row.get("rendererPid") or 0)
        if renderer_pid > 0:
            surface_rows_by_pid[renderer_pid].append(surface_row)
    for process in cached_processes.values():
        try:
            previous_cpu[process.pid] = _cpu_seconds(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    sample_index = 0
    while (time.perf_counter() - started) * 1000.0 < duration_ms:
        interval_started = time.perf_counter()
        remaining = duration_ms - int((interval_started - started) * 1000.0)
        time.sleep(max(0.001, min(interval_ms, remaining) / 1000.0))
        interval_duration = max(0.001, time.perf_counter() - interval_started)
        include_uss = sample_index % USS_SAMPLE_EVERY_N_INTERVALS == 0 or remaining <= interval_ms
        rows: list[dict[str, Any]] = []
        if sample_index % PROCESS_TREE_REFRESH_EVERY_N_INTERVALS == 0:
            cached_processes = {
                process.pid: process for process in _product_tree(root_pid)
            }
        current_processes = list(cached_processes.values())
        for process in current_processes:
            snapshot = _process_snapshot(
                process,
                root_pid,
                include_uss=include_uss,
                metadata_cache=metadata_cache,
            )
            if snapshot is None:
                continue
            end_cpu = float(snapshot.pop("cpuTimeSeconds"))
            cpu_delta = max(0.0, end_cpu - previous_cpu.get(process.pid, end_cpu))
            previous_cpu[process.pid] = end_cpu
            core_equivalent = (cpu_delta / interval_duration) * 100.0
            row = {
                **snapshot,
                "cpuTimeSeconds": round(cpu_delta, 6),
                "cpuCoreEquivalentPercent": round(core_equivalent, 3),
                "cpuWholeMachinePercent": round(core_equivalent / logical_cpu_count, 3),
                "persistedFromIntervalStart": process.pid in initial_pids,
                "attributedSurfaceIds": sorted(
                    row["surfaceId"] for row in surface_rows_by_pid.get(process.pid, [])
                ),
                "attributedOwnerClassifications": sorted(
                    {
                        row["ownerClassification"]
                        for row in surface_rows_by_pid.get(process.pid, [])
                    }
                ),
                "surfaceAttributionBasis": (
                    "DIRECT_QWEBENGINEPAGE_RENDER_PROCESS_PID"
                    if surface_rows_by_pid.get(process.pid)
                    else "NO_DIRECT_SURFACE_PID_MATCH"
                ),
            }
            rows.append(row)
            aggregate = process_accumulator.setdefault(
                process.pid,
                {
                    **{key: value for key, value in snapshot.items() if not key.endswith("Bytes")},
                    "attributedSurfaceIds": row["attributedSurfaceIds"],
                    "attributedOwnerClassifications": row[
                        "attributedOwnerClassifications"
                    ],
                    "surfaceAttributionBasis": row["surfaceAttributionBasis"],
                    "cpuTimeSeconds": 0.0,
                    "rssBytes": [],
                    "workingSetBytes": [],
                    "privateCommitBytes": [],
                    "ussBytes": [],
                    "sharedWorkingSetEstimateBytes": [],
                    "persistedFromIntervalStart": process.pid in initial_pids,
                },
            )
            aggregate["cpuTimeSeconds"] += cpu_delta
            for field in (
                "rssBytes",
                "workingSetBytes",
                "privateCommitBytes",
                "ussBytes",
                "sharedWorkingSetEstimateBytes",
            ):
                value = row.get(field)
                if value is not None:
                    aggregate[field].append(int(value))
        current_pids = {int(row["pid"]) for row in rows}
        observer_memory_samples.append(_memory(observer, include_uss=include_uss))
        raw_samples.append(
            {
                "sampleIndex": sample_index,
                "offsetMs": round((interval_started - started) * 1000.0, 3),
                "durationMs": round(interval_duration * 1000.0, 3),
                "productProcesses": rows,
                "productProcessCount": len(current_pids),
                "ussSampledThisInterval": include_uss,
            }
        )
        sample_index += 1

    duration_seconds = max(0.001, time.perf_counter() - started)
    per_process: list[dict[str, Any]] = []
    for aggregate in sorted(process_accumulator.values(), key=lambda row: (row["role"], row["pid"])):
        cpu_seconds = float(aggregate.pop("cpuTimeSeconds"))
        memory_fields = {
            field: _summary(list(aggregate.pop(field)))
            for field in (
                "rssBytes",
                "workingSetBytes",
                "privateCommitBytes",
                "ussBytes",
                "sharedWorkingSetEstimateBytes",
            )
        }
        core_equivalent = (cpu_seconds / duration_seconds) * 100.0
        per_process.append(
            {
                **aggregate,
                "cpuTimeSeconds": round(cpu_seconds, 6),
                "cpuCoreEquivalentPercent": round(core_equivalent, 3),
                "cpuWholeMachinePercent": round(core_equivalent / logical_cpu_count, 3),
                "memoryMiB": memory_fields,
                "presentAtEnd": any(
                    row["pid"] == aggregate["pid"]
                    for row in (raw_samples[-1]["productProcesses"] if raw_samples else [])
                ),
            }
        )

    role_rows: list[dict[str, Any]] = []
    by_role: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in per_process:
        by_role[str(row["role"])].append(row)
    for role, rows in sorted(by_role.items()):
        role_rows.append(
            {
                "role": role,
                "processCount": len(rows),
                "cpuCoreEquivalentPercent": round(sum(float(row["cpuCoreEquivalentPercent"]) for row in rows), 3),
                "cpuWholeMachinePercent": round(sum(float(row["cpuWholeMachinePercent"]) for row in rows), 3),
                "rssMedianMiBSum": round(sum(float(row["memoryMiB"]["rssBytes"]["median"] or 0) for row in rows), 3),
                "ussMedianMiBSum": round(sum(float(row["memoryMiB"]["ussBytes"]["median"] or 0) for row in rows), 3),
                "privateCommitMedianMiBSum": round(sum(float(row["memoryMiB"]["privateCommitBytes"]["median"] or 0) for row in rows), 3),
            }
        )

    observer_cpu_seconds = max(0.0, _cpu_seconds(observer) - observer_cpu_start)
    observer_core_equivalent = (observer_cpu_seconds / duration_seconds) * 100.0
    observer_rss = [int(row["rssBytes"]) for row in observer_memory_samples]
    observer_uss = [int(row["ussBytes"]) for row in observer_memory_samples if row.get("ussBytes") is not None]
    total_cpu_seconds = sum(float(row["cpuTimeSeconds"]) for row in per_process)
    return {
        "schema": "fam003-option-d-external-observation-v1",
        "methodologyVersion": METHODOLOGY_VERSION,
        "requestId": request["requestId"],
        "state": request["state"],
        "cycleIndex": request.get("cycleIndex", 0),
        "attributionCondition": request.get("attributionCondition", "resident-baseline"),
        "rootPid": root_pid,
        "sampleDurationMs": round(duration_seconds * 1000.0, 3),
        "requiredMinimumDurationMs": duration_ms,
        "sampleIntervalMs": interval_ms,
        "ussSampleIntervalMs": interval_ms * USS_SAMPLE_EVERY_N_INTERVALS,
        "rawSampleCount": len(raw_samples),
        "invalidSampleCount": 0,
        "droppedSampleCount": 0,
        "logicalProcessorCount": logical_cpu_count,
        "cpuNormalization": {
            "coreEquivalentPercent": "100 percent equals one logical processor occupied for the measured wall interval",
            "wholeMachinePercent": "core-equivalent percent divided by logical processor count",
        },
        "memoryMethodology": {
            "rss": "Windows resident working set; may include shared Chromium pages",
            "privateCommit": "Windows process private committed bytes",
            "uss": "psutil unique set size; closest available private resident measure",
            "ussSamplingCadence": f"every {USS_SAMPLE_EVERY_N_INTERVALS} raw intervals plus the final interval",
            "sharedWorkingSetEstimate": "derived RSS minus USS; labeled estimate and not summed as private memory",
        },
        "surfaceInventoryBefore": request["surfaceInventoryBefore"],
        "surfaceRendererMap": surface_renderer_map,
        "controllerMemoryBeforeObservation": request.get(
            "controllerMemoryBeforeObservation", {}
        ),
        "workload": request["workload"],
        "rawSamples": raw_samples,
        "perProcess": per_process,
        "perRole": role_rows,
        "launcherAncestors": _launcher_ancestors(root_pid),
        "totalProductTree": {
            "processCount": len(per_process),
            "cpuTimeSeconds": round(total_cpu_seconds, 6),
            "cpuCoreEquivalentPercent": round((total_cpu_seconds / duration_seconds) * 100.0, 3),
            "cpuWholeMachinePercent": round((total_cpu_seconds / duration_seconds) * 100.0 / logical_cpu_count, 3),
            "rssMedianMiBSum": round(sum(float(row["memoryMiB"]["rssBytes"]["median"] or 0) for row in per_process), 3),
            "ussMedianMiBSum": round(sum(float(row["memoryMiB"]["ussBytes"]["median"] or 0) for row in per_process), 3),
            "privateCommitMedianMiBSum": round(sum(float(row["memoryMiB"]["privateCommitBytes"]["median"] or 0) for row in per_process), 3),
        },
        "observerOverhead": {
            "pid": observer.pid,
            "role": "external-performance-observer",
            "runsInProductProcess": False,
            "touchesGuiThread": False,
            "injectsInput": False,
            "performsScreenshots": False,
            "performsDomQueries": False,
            "samplingFrequencyHz": round(1000.0 / interval_ms, 3),
            "cpuTimeSeconds": round(observer_cpu_seconds, 6),
            "cpuCoreEquivalentPercent": round(observer_core_equivalent, 3),
            "cpuWholeMachinePercent": round(observer_core_equivalent / logical_cpu_count, 3),
            "rssMiB": _summary(observer_rss),
            "ussMiB": _summary(observer_uss),
            "includedInProductTotals": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-root", type=Path, required=True)
    parser.add_argument("--expected-source-head", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    args = parser.parse_args()

    root = args.session_root.resolve()
    requests = root / "observer_requests"
    results = root / "observer_results"
    requests.mkdir(parents=True, exist_ok=True)
    results.mkdir(parents=True, exist_ok=True)
    observer = psutil.Process(os.getpid())
    ready_path = root / "observer_ready.json"
    _atomic_json(
        ready_path,
        {
            "schema": "fam003-option-d-external-observer-ready-v1",
            "methodologyVersion": METHODOLOGY_VERSION,
            "observerPid": observer.pid,
            "sourceHead": args.expected_source_head,
            "readyAtEpoch": time.time(),
        },
    )

    processed: list[str] = []
    deadline = time.time() + args.timeout_seconds
    while time.time() < deadline:
        for request_path in sorted(requests.glob("*.json")):
            if request_path.name in processed:
                continue
            request = json.loads(request_path.read_text(encoding="utf-8-sig"))
            if request.get("sourceHead") != args.expected_source_head:
                raise RuntimeError(f"observer request source HEAD mismatch: {request_path}")
            result = _observe(request, observer)
            _atomic_json(results / request_path.name, result)
            processed.append(request_path.name)
        stop_path = root / "observer_stop.json"
        if stop_path.exists():
            stop = json.loads(stop_path.read_text(encoding="utf-8-sig"))
            expected = int(stop.get("expectedRequestCount", -1))
            if expected == len(processed):
                _atomic_json(
                    root / "observer_manifest.json",
                    {
                        "schema": "fam003-option-d-external-observer-manifest-v1",
                        "status": "PASS",
                        "methodologyVersion": METHODOLOGY_VERSION,
                        "observerPid": observer.pid,
                        "sourceHead": args.expected_source_head,
                        "processedRequestCount": len(processed),
                        "processedRequests": processed,
                        "productSamplingUsesNestedEventLoop": False,
                        "observerIncludedInProductTotals": False,
                        "finishedAtEpoch": time.time(),
                    },
                )
                return 0
        time.sleep(0.05)

    raise RuntimeError(f"external observer timed out after {args.timeout_seconds}s; processed={processed}")


if __name__ == "__main__":
    raise SystemExit(main())
