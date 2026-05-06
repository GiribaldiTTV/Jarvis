"""Validate the FAM-006 Monitoring HUD visual, telemetry, placement, controls, and status contract.

This helper is intentionally static for SLC-016/SLC-025. It proves the
desktop-only visual surface, runtime telemetry adapter boundary, renderer-owned
placement contract, controls visibility contract, source-truth markers, and
slice-boundary copy without polling hardware, persisting settings, inventing
hardware values, expanding retired legacy product identity, inventing
recovery behavior, or touching voice/audio.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _require_contains(text: str, needle: str, label: str, failures: list[str]) -> None:
    _require(needle in text, f"{label} is missing {needle!r}", failures)


def _html_section(text: str) -> str:
    match = re.search(
        r'<section\s+id="monitoring-hud".*?</section>',
        text,
        flags=re.DOTALL,
    )
    return match.group(0) if match else ""


def validate() -> list[str]:
    failures: list[str] = []

    html = _read("nexus_visual/orin_core.html")
    css = _read("nexus_visual/orin_core.css")
    js = _read("nexus_visual/orin_core.js")
    renderer = _read("desktop/desktop_renderer.py")
    telemetry = _read("desktop/monitoring_hud_telemetry.py")
    placement = _read("desktop/monitoring_hud_placement.py")
    controls = _read("desktop/monitoring_hud_controls.py")
    status = _read("desktop/monitoring_hud_status.py")
    live_validation = _read("dev/orin_monitoring_hud_live_validation.ps1")

    hud_section = _html_section(html)
    _require(bool(hud_section), "orin_core.html is missing the monitoring-hud section", failures)
    for needle in (
        'data-package="PKG-006"',
        'data-slice="SLC-016"',
        'data-slice="SLC-025"',
        'data-slice="SLC-026"',
        'data-slice="SLC-027"',
        'data-slice="SLC-028"',
        'aria-label="Monitoring HUD visual baseline"',
        'aria-label="Runtime telemetry adapter boundary"',
        'aria-label="Desktop placement and renderer ownership"',
        'aria-label="Settings and user controls visibility"',
        'aria-label="Fail-safe no-data and degraded-status behavior"',
        'aria-hidden="true"',
        "FAM-006 Monitoring HUD",
        "System surface baseline",
        "Visual layer online",
        "Active SLC-025",
        "Active SLC-026",
        "Active SLC-027",
        "Active SLC-028",
        "Adapter boundary",
        "Local runtime only",
        "Not performed",
        "Renderer owner",
        "DesktopRuntimeWindow",
        "Desktop anchor",
        "Top-right",
        "Pointer model",
        "Non-interactive",
        "HUD visibility",
        "Desktop mode visible",
        "Control surface",
        "Read-only preview",
        "Persistence",
        "Not persisted",
        "Fail-safe state",
        "Waiting for source truth",
        "No-data behavior",
        "Do not imply telemetry",
        "Degraded behavior",
        "Name local readiness gap",
    ):
        _require_contains(hud_section, needle, "monitoring HUD HTML", failures)

    retired_product_name = "".join(chr(code) for code in (74, 97, 114, 118, 105, 115)).casefold()
    for forbidden in ("voice", "audio", "spoken", "microphone", retired_product_name):
        _require(
            forbidden not in hud_section.casefold(),
            f"monitoring HUD HTML must not introduce {forbidden} behavior in SLC-016",
            failures,
        )

    for forbidden_metric in ("cpu temp", "gpu temp", "thermal value", "fake metric", "mock metric"):
        _require(
            forbidden_metric not in hud_section.casefold(),
            (
                "monitoring HUD HTML must not present hardware metric values before "
                f"provider-contract proof exists: {forbidden_metric}"
            ),
            failures,
        )

    for needle in (
        "#monitoring-hud {",
        "display: none;",
        "body.desktop-mode #monitoring-hud",
        ".monitoring-hud__placement",
        ".monitoring-hud__controls",
        ".monitoring-hud__status-model",
        "pointer-events: none",
        "@media (max-width: 760px), (max-height: 620px)",
        "@keyframes monitoringHudSettle",
    ):
        _require_contains(css, needle, "monitoring HUD CSS", failures)

    for needle in (
        'const monitoringHud = document.getElementById("monitoring-hud")',
        "window.setDesktopSurfaceMode = function(enabled)",
        'body.classList.toggle("desktop-mode", isEnabled)',
        'monitoringHud.setAttribute("aria-hidden", isEnabled ? "false" : "true")',
        'monitoringHud.dataset.renderState = isEnabled ? "visual-baseline" : "hidden"',
        "window.setMonitoringHudTelemetry = function(snapshot)",
        'monitoringHud.dataset.telemetrySlice = monitoringHudTelemetry.sliceId || "SLC-025"',
        'monitoringHudRuntimeStatus.textContent = "Runtime boundary online"',
        "window.setMonitoringHudPlacementOwnership = function(contract)",
        'monitoringHud.dataset.placementSlice = monitoringHudPlacement.sliceId || "SLC-026"',
        'monitoringHud.dataset.placementId = monitoringHudPlacement.placementId || "desktop-renderer-top-right"',
        'monitoringHud.dataset.placementState = "desktop-renderer-owned"',
        "window.setMonitoringHudControlsVisibility = function(contract)",
        'monitoringHud.dataset.controlsSlice = monitoringHudControls.sliceId || "SLC-027"',
        'monitoringHud.dataset.controlsId = monitoringHudControls.controlsId || "hud-controls-visibility"',
        'monitoringHud.dataset.controlsState = "visible-read-only"',
        "window.setMonitoringHudStatusBehavior = function(snapshot)",
        'monitoringHud.dataset.statusSlice = monitoringHudStatus.sliceId || "SLC-028"',
        'monitoringHud.dataset.statusId = monitoringHudStatus.statusId || "hud-local-readiness-status"',
        'monitoringHud.dataset.statusKind = monitoringHudStatus.statusKind || "no-data"',
        "window.setDesktopSurfaceMode(false)",
        "window.setMonitoringHudTelemetry({})",
        "window.setMonitoringHudPlacementOwnership({})",
        "window.setMonitoringHudControlsVisibility({})",
        "window.setMonitoringHudStatusBehavior({})",
    ):
        _require_contains(js, needle, "monitoring HUD JavaScript", failures)

    for needle in (
        "from .monitoring_hud_controls import build_monitoring_hud_controls_visibility_contract",
        "from .monitoring_hud_placement import build_monitoring_hud_placement_contract",
        "from .monitoring_hud_status import build_monitoring_hud_status_snapshot",
        "from .monitoring_hud_telemetry import build_monitoring_hud_telemetry_snapshot",
        "def _apply_desktop_surface_mode(self):",
        "def _monitoring_hud_telemetry_snapshot(self) -> dict[str, object]:",
        "def _publish_monitoring_hud_telemetry_boundary(self):",
        "def _monitoring_hud_placement_contract(self) -> dict[str, object]:",
        "def _publish_monitoring_hud_placement_ownership(self):",
        "def _monitoring_hud_controls_visibility_contract(self) -> dict[str, str]:",
        "def _publish_monitoring_hud_controls_visibility(self):",
        "def _monitoring_hud_status_snapshot(self) -> dict[str, str]:",
        "def _publish_monitoring_hud_status_behavior(self):",
        "build_monitoring_hud_telemetry_snapshot(",
        "build_monitoring_hud_placement_contract(",
        "build_monitoring_hud_controls_visibility_contract(",
        "build_monitoring_hud_status_snapshot(",
        "window.setDesktopSurfaceMode(true)",
        "window.setMonitoringHudTelemetry",
        "window.setMonitoringHudPlacementOwnership",
        "window.setMonitoringHudControlsVisibility",
        "window.setMonitoringHudStatusBehavior",
        "MONITORING_HUD_BASELINE_READY",
        "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
        "MONITORING_HUD_PLACEMENT_OWNERSHIP_READY",
        "MONITORING_HUD_CONTROLS_VISIBILITY_READY",
        "MONITORING_HUD_STATUS_BEHAVIOR_READY",
        'package="PKG-006"',
        'slice="SLC-016"',
        'slice="SLC-025"',
        'slice="SLC-026"',
        'slice="SLC-027"',
        'slice="SLC-028"',
        'adapter="desktop-runtime-boundary"',
        'hardware_polling="not_performed"',
        'baseline="visual_only"',
        'owner="DesktopRuntimeWindow"',
        'placement="desktop-renderer-top-right"',
        'anchor="top_right"',
        'controls="hud-controls-visibility"',
        'persistence="not_persisted"',
        'status="hud-local-readiness-status"',
        'source_truth="renderer_local"',
        "self._apply_desktop_surface_mode()",
        "self._publish_monitoring_hud_telemetry_boundary()",
        "self._publish_monitoring_hud_placement_ownership()",
        "self._publish_monitoring_hud_controls_visibility()",
        "self._publish_monitoring_hud_status_behavior()",
    ):
        _require_contains(renderer, needle, "desktop renderer HUD hook", failures)

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-025"',
        'ADAPTER_ID = "desktop-runtime-boundary"',
        "class MonitoringHudTelemetrySnapshot",
        "def build_monitoring_hud_telemetry_snapshot(",
        'adapter_status="Boundary ready"',
        'source_scope="Local runtime readiness"',
        'hardware_polling="Not performed"',
        'MonitoringHudSource("Visual page"',
        'MonitoringHudSource("Desktop surface"',
        'MonitoringHudSource("Runtime log"',
        'MonitoringHudSource("Event route"',
    ):
        _require_contains(telemetry, needle, "monitoring HUD telemetry adapter", failures)

    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "win32", "powershell"):
        _require(
            forbidden not in telemetry.casefold(),
            f"monitoring HUD telemetry adapter must not perform {forbidden} collection in SLC-025",
            failures,
        )

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-026"',
        'PLACEMENT_ID = "desktop-renderer-top-right"',
        "class MonitoringHudPlacementContract",
        "def build_monitoring_hud_placement_contract(",
        'renderer_owner="DesktopRuntimeWindow"',
        'surface_owner="Qt WebEngine desktop child surface"',
        'anchor="Top-right inside desktop visual surface"',
        'pointer_model="Non-interactive pass-through"',
        'z_index="18"',
    ):
        _require_contains(placement, needle, "monitoring HUD placement contract", failures)

    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "win32", "powershell"):
        _require(
            forbidden not in placement.casefold(),
            f"monitoring HUD placement contract must not perform {forbidden} collection in SLC-026",
            failures,
        )

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-027"',
        'CONTROLS_ID = "hud-controls-visibility"',
        "class MonitoringHudControlsVisibilityContract",
        "def build_monitoring_hud_controls_visibility_contract(",
        'control_surface="Read-only HUD controls preview"',
        'persistence="Not persisted"',
        'operator_action="No toggle in this slice"',
    ):
        _require_contains(controls, needle, "monitoring HUD controls visibility contract", failures)

    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "win32", "powershell"):
        _require(
            forbidden not in controls.casefold(),
            f"monitoring HUD controls visibility contract must not perform {forbidden} collection in SLC-027",
            failures,
        )

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-028"',
        'STATUS_ID = "hud-local-readiness-status"',
        "class MonitoringHudStatusSnapshot",
        "def build_monitoring_hud_status_snapshot(",
        'status_kind = "no-data"',
        'status_kind = "degraded"',
        'status_kind = "ready"',
        'no_data_behavior="Show waiting state; do not imply unavailable telemetry exists"',
        'degraded_behavior="Name the local readiness gap without recovery claims"',
        'source_truth="Renderer-owned local readiness only"',
    ):
        _require_contains(status, needle, "monitoring HUD status behavior contract", failures)

    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "win32", "powershell"):
        _require(
            forbidden not in status.casefold(),
            f"monitoring HUD status behavior contract must not perform {forbidden} collection in SLC-028",
            failures,
        )

    for needle in (
        "SLC-029",
        "WS6 - Validation And Live Desktop Proof",
        "MONITORING_HUD_BASELINE_READY",
        "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
        "MONITORING_HUD_PLACEMENT_OWNERSHIP_READY",
        "MONITORING_HUD_CONTROLS_VISIBILITY_READY",
        "MONITORING_HUD_STATUS_BEHAVIOR_READY",
        "DESKTOP_OUTCOME|SETTLED|state=dormant",
        "monitoring_hud_desktop.png",
        "manifest.json",
        "Stop-Process -Id $script:RuntimeProcess.Id -Force",
        "No-progress watchdog exceeded",
    ):
        _require_contains(live_validation, needle, "monitoring HUD live validation helper", failures)

    desktop_mode_method = re.search(
        r"def _apply_desktop_surface_mode\(self\):.*?def _on_load_finished",
        renderer,
        flags=re.DOTALL,
    )
    method_text = desktop_mode_method.group(0).casefold() if desktop_mode_method else ""
    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "settings", "voice", "audio"):
        _require(
            forbidden not in method_text,
            f"desktop renderer HUD baseline hook must not implement {forbidden} behavior",
            failures,
        )

    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("FAIL: FAM-006 Monitoring/HUD surface validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: FAM-006 HUD visual, telemetry, placement, controls, and status boundaries are bounded and marker-backed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
