"""Internal sandbox validation for the FAM-006 Monitoring HUD Workstream.

This helper proves the current-branch HUD product baseline without asking the
USER for a User Test Summary during Workstream. It validates the bounded
runtime seams for the HUD shell, controls, card model, provider-truthful
telemetry, no-data/degraded states, visual warnings, and naming sterilization.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.monitoring_hud_controls import build_monitoring_hud_controls_visibility_contract
from desktop.monitoring_hud_placement import build_monitoring_hud_placement_contract
from desktop.monitoring_hud_status import build_monitoring_hud_status_snapshot
from desktop.monitoring_hud_telemetry import build_monitoring_hud_telemetry_snapshot


LOG_ROOT = ROOT / "dev" / "logs" / "fam_006_monitoring_hud_internal_sandbox"


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _require_contains(text: str, needle: str, label: str, failures: list[str]) -> None:
    _require(needle in text, f"{label} is missing {needle!r}", failures)


def _retired_name() -> str:
    return "".join(chr(code) for code in (74, 97, 114, 118, 105, 115))


def _tracked_text_files() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        parts = set(relative.parts)
        if ".git" in parts or "__pycache__" in parts:
            continue
        if len(relative.parts) >= 2 and relative.parts[0] == "dev" and relative.parts[1] == "logs":
            continue
        if parts & {"dev", "desktop", "nexus_visual", "Docs", "Audio"} or path.name == "main.py":
            if path.suffix.lower() in {".py", ".pyw", ".ps1", ".md", ".txt", ".html", ".css", ".js", ".json"}:
                result.append(path)
    return result


def _validate_naming_sterilization(failures: list[str]) -> None:
    retired = _retired_name().casefold()
    for path in _tracked_text_files():
        relative = path.relative_to(ROOT)
        _require(retired not in str(relative).casefold(), f"{relative}: path contains retired product name", failures)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if retired in line.casefold():
                failures.append(f"{relative}:{line_number}: content contains retired product name")


def _validate_static_surface(failures: list[str]) -> None:
    html = _read("nexus_visual/orin_core.html")
    css = _read("nexus_visual/orin_core.css")
    js = _read("nexus_visual/orin_core.js")
    renderer = _read("desktop/desktop_renderer.py")
    tray = _read("desktop/orin_desktop_main.py")

    for needle in (
        'data-hud-module="monitoring-hud-shell-module"',
        'data-anchor-state="anchored"',
        'data-visibility-state="visible"',
        'data-snap-state="enabled"',
        'data-card-model="category-sensor-cards"',
        'data-polling-default-ms="1000"',
        'data-sandbox-state-matrix="setup,no-data,degraded,ready,warning"',
        'id="monitoring-hud-toggle"',
        'id="monitoring-hud-anchor-toggle"',
        'id="monitoring-hud-snap-toggle"',
        'id="monitoring-hud-polling-rate"',
        'data-category-card="cpu"',
        'data-category-card="gpu"',
        'data-sensor-row="cpu-load"',
        'data-sensor-row="cpu-thermal"',
        'data-sensor-row="gpu-load"',
        'data-sensor-row="gpu-thermal"',
        "Sandbox state matrix required",
    ):
        _require_contains(html, needle, "HUD HTML product surface", failures)

    for needle in (
        'body.desktop-mode #monitoring-hud[data-anchor-state="unanchored"]',
        ".monitoring-hud__toolbar",
        ".monitoring-hud__card-board",
        ".monitoring-hud-card__drag-handle",
        ".monitoring-hud-sensor-row",
        ".monitoring-hud-card__resize-handle",
        "cursor: nwse-resize",
    ):
        _require_contains(css, needle, "HUD CSS interaction surface", failures)

    for needle in (
        "window.getMonitoringHudControlState = function()",
        "window.setMonitoringHudControlState = function(state)",
        "monitoringHudWirePanelDrag",
        "monitoringHudWireCardInteractions",
        "monitoringHudWireControls",
        "monitoringHudRenderSensorCards",
        "monitoringHudStorageKey",
        "monitoringHudPollingRate.addEventListener",
        "monitoringHudControlState.snapEnabled",
        'monitoringHud.dataset.interactionMode = monitoringHudControlState.anchored ? "anchored-click-through" : "unanchored-edit-mode"',
    ):
        _require_contains(js, needle, "HUD JavaScript controls", failures)

    for needle in (
        "request_monitoring_hud_unanchor_from_tray",
        "request_monitoring_hud_toggle_from_tray",
        "MONITORING_HUD_INTERACTION_MODE_READY",
        "MONITORING_HUD_CONTROL_STATE_READY",
        "MONITORING_HUD_TRAY_UNANCHOR_READY",
        "MONITORING_HUD_TRAY_TOGGLE_READY",
        "native_cpu_load_bounded",
    ):
        _require_contains(renderer, needle, "desktop renderer HUD runtime", failures)

    for needle in (
        "Show / Hide Monitoring HUD",
        "Unanchor Monitoring HUD",
        "TRAY_MONITORING_HUD_TOGGLE_REQUESTED",
        "TRAY_MONITORING_HUD_UNANCHOR_REQUESTED",
    ):
        _require_contains(tray, needle, "desktop tray HUD controls", failures)


def _validate_contracts(failures: list[str]) -> dict[str, object]:
    first = build_monitoring_hud_telemetry_snapshot(
        page_ready=True,
        desktop_mode=True,
        runtime_log_path=str(LOG_ROOT / "runtime_log.txt"),
        event_route_present=True,
        polling_rate_ms=1000,
    ).as_dict()
    time.sleep(0.05)
    second = build_monitoring_hud_telemetry_snapshot(
        page_ready=True,
        desktop_mode=True,
        runtime_log_path=str(LOG_ROOT / "runtime_log.txt"),
        event_route_present=True,
        polling_rate_ms=1000,
    ).as_dict()
    placement = build_monitoring_hud_placement_contract(
        desktop_mode=True,
        x=100,
        y=120,
        width=900,
        height=700,
    ).as_dict()
    controls = build_monitoring_hud_controls_visibility_contract(
        desktop_mode=True,
        visible=True,
        anchored=False,
        snap_enabled=True,
        polling_rate_ms=1000,
    ).as_dict()
    status = build_monitoring_hud_status_snapshot(
        page_ready=True,
        desktop_mode=True,
        event_route_present=True,
    ).as_dict()

    cards = second.get("sensorCards") or []
    sensors = {
        sensor.get("id"): sensor
        for card in cards
        for sensor in card.get("sensors", [])
        if isinstance(sensor, dict)
    }
    _require(second.get("pollingRateMs") == 1000, "telemetry contract must use 1s default polling", failures)
    _require(second.get("liveValues") in {"native-cpu-load-only", "provider-required"}, "telemetry contract has invalid live value state", failures)
    _require("cpu-load" in sensors, "telemetry contract is missing CPU load sensor", failures)
    _require(sensors.get("gpu-load", {}).get("value") == "Unavailable", "GPU load must remain provider-unavailable", failures)
    _require(sensors.get("gpu-thermal", {}).get("value") == "Unavailable", "GPU thermal must remain provider-unavailable", failures)
    _require(sensors.get("cpu-thermal", {}).get("value") == "Provider required", "CPU thermal must remain provider-required", failures)
    _require(placement.get("snapModel") == "20px snap grid with snap-disable posture", "placement contract must describe snap posture", failures)
    _require(placement.get("cardLayoutModel") == "draggable/resizable category cards", "placement contract must describe card layout", failures)
    _require(controls.get("anchorState") == "unanchored-edit-mode", "controls contract must support unanchored edit mode", failures)
    _require(controls.get("pollingRateMs") == "1000", "controls contract must preserve 1s default polling", failures)
    _require(status.get("warningPosture") == "Visual badge, color state, and text label only", "status contract must preserve visual warning posture", failures)

    return {
        "firstTelemetry": first,
        "secondTelemetry": second,
        "placement": placement,
        "controls": controls,
        "status": status,
    }


def _write_manifest(status: str, failures: list[str], contracts: dict[str, object]) -> Path:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    manifest_path = LOG_ROOT / f"{stamp}_manifest.json"
    payload = {
        "status": status,
        "package": "PKG-006",
        "phase": "Workstream",
        "seam": "WS8-WS17 internal sandbox consolidation",
        "contracts": contracts,
        "failures": failures,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return manifest_path


def validate() -> tuple[list[str], Path]:
    failures: list[str] = []
    _validate_naming_sterilization(failures)
    _validate_static_surface(failures)
    contracts = _validate_contracts(failures)
    status = "PASS" if not failures else "FAIL"
    manifest_path = _write_manifest(status, failures, contracts)
    return failures, manifest_path


def main() -> int:
    failures, manifest_path = validate()
    if failures:
        print("FAIL: FAM-006 Monitoring HUD internal sandbox validation failed")
        for failure in failures:
            print(f"- {failure}")
        print(f"manifest: {manifest_path}")
        return 1

    print("PASS: FAM-006 Monitoring HUD internal sandbox validation is green")
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
