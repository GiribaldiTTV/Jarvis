"""Runtime output contract for active-overlay recording logs.

The contract owns the local file shape, safe runtime output root, atomic write,
and readback proof for Dashboard Recording Start/Stop. Tray controls,
export/share, provider/model work, and Native Log Loader remain outside this
branch.
"""

from __future__ import annotations

import csv
import datetime as _dt
import io
import json
import os
import re
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any


RECORDING_OUTPUT_CONTRACT_VERSION = 2
RECORDING_OUTPUT_CONTRACT_ID = "slc-054-active-overlay-recording-output-contract"
RECORDING_OUTPUT_FORMAT = "csv-with-json-metadata-manifest"
RECORDING_OUTPUT_ENV = "NEXUS_MONITORING_HUD_RECORDING_OUTPUT_DIR"
RECORDING_OUTPUT_DIR_NAME = "Recordings"
RECORDING_OUTPUT_FAMILY_DIR_NAME = "FAM-006"
RECORDING_OUTPUT_HEADERS = (
    "timestamp_utc",
    "elapsed_ms",
    "overlay_profile_id",
    "overlay_profile_name",
    "monitor_id",
    "monitor_name",
    "sensor_id",
    "sensor_label",
    "value",
    "unit",
    "quality",
    "source_state",
)


def _utc_now_iso() -> str:
    return _dt.datetime.now(_dt.UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _safe_token(value: Any, fallback: str = "recording") -> str:
    token = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value or "").strip()).strip("-._")
    return token[:80] or fallback


def recording_output_dir() -> Path:
    override = os.environ.get(RECORDING_OUTPUT_ENV, "").strip()
    if override:
        return Path(override)
    local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
    if local_app_data:
        return Path(local_app_data) / "Nexus Desktop AI" / RECORDING_OUTPUT_DIR_NAME / RECORDING_OUTPUT_FAMILY_DIR_NAME
    return Path.home() / "AppData" / "Local" / "Nexus Desktop AI" / RECORDING_OUTPUT_DIR_NAME / RECORDING_OUTPUT_FAMILY_DIR_NAME


def recording_output_contract() -> dict[str, Any]:
    return {
        "contractId": RECORDING_OUTPUT_CONTRACT_ID,
        "schemaVersion": RECORDING_OUTPUT_CONTRACT_VERSION,
        "format": RECORDING_OUTPUT_FORMAT,
        "headers": list(RECORDING_OUTPUT_HEADERS),
        "timestampColumn": "timestamp_utc",
        "xAxisCandidates": ["timestamp_utc", "elapsed_ms"],
        "seriesIdentityColumns": ["monitor_id", "sensor_id"],
        "valueColumn": "value",
        "unitColumn": "unit",
        "qualityColumn": "quality",
        "graphPlotReady": True,
        "recordingExecutionState": "enabled",
        "fileWritingState": "enabled",
        "startStopState": "dashboard-card-enabled",
        "outputRootOwner": "runtime-local-app-data",
        "outputRoot": str(recording_output_dir()),
        "nativeLogLoaderState": "future-separate-viewer",
        "exportShareState": "future-gated",
    }


def build_recording_output_manifest(
    *,
    active_overlay_profile_id: str,
    active_overlay_profile_name: str,
    target_monitor_ids: list[str],
    target_state: str,
    session_id: str = "",
    started_at_utc: str = "",
    stopped_at_utc: str = "",
    snapshot_mode: str = "snapshot-at-recording-start",
) -> dict[str, Any]:
    monitor_ids = [str(monitor_id) for monitor_id in target_monitor_ids if str(monitor_id).strip()]
    return {
        "contractId": RECORDING_OUTPUT_CONTRACT_ID,
        "schemaVersion": RECORDING_OUTPUT_CONTRACT_VERSION,
        "format": RECORDING_OUTPUT_FORMAT,
        "sessionId": str(session_id or ""),
        "activeOverlayProfileId": str(active_overlay_profile_id or ""),
        "activeOverlayProfileName": str(active_overlay_profile_name or ""),
        "targetMonitorIds": monitor_ids,
        "targetMonitorCount": len(monitor_ids),
        "targetState": str(target_state or "unknown"),
        "snapshotMode": snapshot_mode,
        "startedAtUtc": str(started_at_utc or ""),
        "stoppedAtUtc": str(stopped_at_utc or ""),
        "finalizedAtUtc": _utc_now_iso(),
        "recordingExecutionState": "saved-complete",
        "fileWritingState": "saved-complete",
        "nativeLogLoaderState": "future-separate-viewer",
        "exportShareState": "future-gated",
    }


def normalize_recording_output_row(row: dict[str, Any]) -> dict[str, str]:
    normalized = {header: "" for header in RECORDING_OUTPUT_HEADERS}
    for header in RECORDING_OUTPUT_HEADERS:
        value = row.get(header, "")
        normalized[header] = "" if value is None else str(value)
    return normalized


def build_recording_output_rows(samples: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows = [normalize_recording_output_row(sample) for sample in samples]
    rows.sort(
        key=lambda row: (
            row["timestamp_utc"],
            row["elapsed_ms"].zfill(16),
            row["monitor_id"],
            row["sensor_id"],
        )
    )
    return rows


def render_recording_output_csv(rows: list[dict[str, Any]]) -> str:
    normalized_rows = build_recording_output_rows(rows)
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(RECORDING_OUTPUT_HEADERS), lineterminator="\n")
    writer.writeheader()
    writer.writerows(normalized_rows)
    return buffer.getvalue()


def parse_recording_output_csv(csv_text: str) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(csv_text or ""))
    if tuple(reader.fieldnames or ()) != RECORDING_OUTPUT_HEADERS:
        raise ValueError("Recording output CSV headers do not match the SLC-054 contract")
    return [normalize_recording_output_row(row) for row in reader]


def readback_recording_output_files(csv_path: str | Path, manifest_path: str | Path) -> dict[str, Any]:
    csv_text = Path(csv_path).read_text(encoding="utf-8")
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    rows = parse_recording_output_csv(csv_text)
    return {
        "passed": bool(rows) and manifest.get("contractId") == RECORDING_OUTPUT_CONTRACT_ID,
        "rowCount": len(rows),
        "manifest": manifest,
        "rows": rows,
    }


def write_recording_output_files(
    *,
    session_id: str,
    active_overlay_profile_id: str,
    active_overlay_profile_name: str,
    target_monitor_ids: list[str],
    target_state: str,
    samples: list[dict[str, Any]],
    started_at_utc: str = "",
    stopped_at_utc: str = "",
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    rows = build_recording_output_rows(samples)
    if not rows:
        raise ValueError("Recording output requires at least one usable sample row")
    output_root = Path(output_dir) if output_dir is not None else recording_output_dir()
    output_root.mkdir(parents=True, exist_ok=True)
    safe_session = _safe_token(session_id, "recording-session")
    safe_profile = _safe_token(active_overlay_profile_name or active_overlay_profile_id, "overlay-profile")
    stem = f"{_safe_token(stopped_at_utc or _utc_now_iso(), 'recording-time')}_{safe_profile}_{safe_session}"
    csv_path = output_root / f"{stem}.csv"
    manifest_path = output_root / f"{stem}.manifest.json"
    manifest = build_recording_output_manifest(
        active_overlay_profile_id=active_overlay_profile_id,
        active_overlay_profile_name=active_overlay_profile_name,
        target_monitor_ids=target_monitor_ids,
        target_state=target_state,
        session_id=session_id,
        started_at_utc=started_at_utc,
        stopped_at_utc=stopped_at_utc,
    )
    manifest["csvPath"] = str(csv_path)
    manifest["manifestPath"] = str(manifest_path)
    manifest["rowCount"] = len(rows)
    csv_text = render_recording_output_csv(rows)
    csv_tmp = csv_path.with_suffix(csv_path.suffix + ".tmp")
    manifest_tmp = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    csv_tmp.write_text(csv_text, encoding="utf-8", newline="")
    manifest_tmp.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(csv_tmp, csv_path)
    os.replace(manifest_tmp, manifest_path)
    readback = readback_recording_output_files(csv_path, manifest_path)
    return {
        "passed": bool(readback.get("passed")),
        "sessionId": str(session_id or ""),
        "csvPath": str(csv_path),
        "manifestPath": str(manifest_path),
        "rowCount": len(rows),
        "readbackPassed": bool(readback.get("passed")),
        "fileWritingState": "saved-complete",
        "recordingExecutionState": "saved-complete",
        "outputRootOwner": "runtime-local-app-data",
    }


def validate_recording_output_contract() -> dict[str, Any]:
    contract = recording_output_contract()
    samples = [
        {
            "timestamp_utc": "2026-06-01T19:00:00.000Z",
            "elapsed_ms": 1000,
            "overlay_profile_id": "default-overlay-profile",
            "overlay_profile_name": "Default Overlay Profile",
            "monitor_id": "gpu",
            "monitor_name": "GPU Group",
            "sensor_id": "gpu-load",
            "sensor_label": "GPU Load",
            "value": "",
            "unit": "%",
            "quality": "unavailable",
            "source_state": "provider-required",
        },
        {
            "timestamp_utc": "2026-06-01T19:00:00.000Z",
            "elapsed_ms": 0,
            "overlay_profile_id": "default-overlay-profile",
            "overlay_profile_name": "Default Overlay Profile",
            "monitor_id": "cpu",
            "monitor_name": "CPU Group",
            "sensor_id": "cpu-load",
            "sensor_label": "CPU Load",
            "value": "12.5",
            "unit": "%",
            "quality": "ok",
            "source_state": "sample",
        },
    ]
    normalized = build_recording_output_rows(samples)
    csv_text = render_recording_output_csv(samples)
    parsed = parse_recording_output_csv(csv_text)
    with tempfile.TemporaryDirectory(prefix="nexus-fam006-recording-") as temp_dir:
        write_result = write_recording_output_files(
            session_id="validation-session",
            active_overlay_profile_id="default-overlay-profile",
            active_overlay_profile_name="Default Overlay Profile",
            target_monitor_ids=["cpu", "gpu"],
            target_state="ready",
            samples=samples,
            started_at_utc="2026-06-01T18:59:59.000Z",
            stopped_at_utc="2026-06-01T19:00:01.000Z",
            output_dir=temp_dir,
        )
        readback = readback_recording_output_files(write_result["csvPath"], write_result["manifestPath"])
    proof = {
        "passed": False,
        "contract": contract,
        "headerDeterministic": csv_text.splitlines()[0].split(",") == list(RECORDING_OUTPUT_HEADERS),
        "rowDeterministic": normalized[0]["monitor_id"] == "cpu" and normalized[1]["monitor_id"] == "gpu",
        "parseReadback": parsed == normalized,
        "nullNoDataBehavior": parsed[1]["value"] == "" and parsed[1]["quality"] == "unavailable",
        "graphPlotReady": contract["graphPlotReady"] is True,
        "fileWritingEnabled": contract["fileWritingState"] == "enabled",
        "recordingExecutionEnabled": contract["recordingExecutionState"] == "enabled",
        "dashboardStartStopEnabled": contract["startStopState"] == "dashboard-card-enabled",
        "writeReadbackPassed": bool(write_result.get("passed") and readback.get("passed")),
        "nativeLogLoaderFutureBoundary": contract["nativeLogLoaderState"] == "future-separate-viewer",
        "exportShareBlocked": contract["exportShareState"] == "future-gated",
    }
    proof["passed"] = all(
        bool(proof[key])
        for key in (
            "headerDeterministic",
            "rowDeterministic",
            "parseReadback",
            "nullNoDataBehavior",
            "graphPlotReady",
            "fileWritingEnabled",
            "recordingExecutionEnabled",
            "dashboardStartStopEnabled",
            "writeReadbackPassed",
            "nativeLogLoaderFutureBoundary",
            "exportShareBlocked",
        )
    )
    return deepcopy(proof)
