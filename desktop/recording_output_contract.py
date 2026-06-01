"""In-memory output contract for future active-overlay recording logs.

The contract is graph/plot-ready proof only. It does not write files, start
recording, stop recording, export, share, or implement Native Log Loader.
"""

from __future__ import annotations

import csv
import io
import json
from copy import deepcopy
from typing import Any


RECORDING_OUTPUT_CONTRACT_VERSION = 1
RECORDING_OUTPUT_CONTRACT_ID = "slc-054-active-overlay-recording-output-contract"
RECORDING_OUTPUT_FORMAT = "csv-with-json-metadata-manifest"
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
        "recordingExecutionState": "blocked",
        "fileWritingState": "blocked",
        "startStopState": "future-gated",
        "nativeLogLoaderState": "future-separate-viewer",
        "exportShareState": "future-gated",
    }


def build_recording_output_manifest(
    *,
    active_overlay_profile_id: str,
    active_overlay_profile_name: str,
    target_monitor_ids: list[str],
    target_state: str,
    snapshot_mode: str = "snapshot-at-recording-start",
) -> dict[str, Any]:
    monitor_ids = [str(monitor_id) for monitor_id in target_monitor_ids if str(monitor_id).strip()]
    return {
        "contractId": RECORDING_OUTPUT_CONTRACT_ID,
        "schemaVersion": RECORDING_OUTPUT_CONTRACT_VERSION,
        "format": RECORDING_OUTPUT_FORMAT,
        "activeOverlayProfileId": str(active_overlay_profile_id or ""),
        "activeOverlayProfileName": str(active_overlay_profile_name or ""),
        "targetMonitorIds": monitor_ids,
        "targetMonitorCount": len(monitor_ids),
        "targetState": str(target_state or "unknown"),
        "snapshotMode": snapshot_mode,
        "recordingExecutionState": "blocked",
        "fileWritingState": "blocked",
        "nativeLogLoaderState": "future-separate-viewer",
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


def validate_recording_output_contract() -> dict[str, Any]:
    contract = recording_output_contract()
    manifest = build_recording_output_manifest(
        active_overlay_profile_id="default-overlay-profile",
        active_overlay_profile_name="Default Overlay Profile",
        target_monitor_ids=["cpu", "gpu"],
        target_state="ready",
    )
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
    manifest_round_trip = json.loads(json.dumps(manifest, sort_keys=True))
    proof = {
        "passed": False,
        "contract": contract,
        "manifest": manifest,
        "headerDeterministic": csv_text.splitlines()[0].split(",") == list(RECORDING_OUTPUT_HEADERS),
        "rowDeterministic": normalized[0]["monitor_id"] == "cpu" and normalized[1]["monitor_id"] == "gpu",
        "parseReadback": parsed == normalized,
        "manifestSerializable": manifest_round_trip == manifest,
        "nullNoDataBehavior": parsed[1]["value"] == "" and parsed[1]["quality"] == "unavailable",
        "graphPlotReady": contract["graphPlotReady"] is True,
        "fileWritingBlocked": contract["fileWritingState"] == "blocked",
        "recordingExecutionBlocked": contract["recordingExecutionState"] == "blocked",
        "nativeLogLoaderFutureBoundary": contract["nativeLogLoaderState"] == "future-separate-viewer",
        "exportShareBlocked": contract["exportShareState"] == "future-gated",
    }
    proof["passed"] = all(
        bool(proof[key])
        for key in (
            "headerDeterministic",
            "rowDeterministic",
            "parseReadback",
            "manifestSerializable",
            "nullNoDataBehavior",
            "graphPlotReady",
            "fileWritingBlocked",
            "recordingExecutionBlocked",
            "nativeLogLoaderFutureBoundary",
            "exportShareBlocked",
        )
    )
    return deepcopy(proof)
