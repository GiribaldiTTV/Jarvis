"""Validate the FAM-006 Monitoring HUD product visibility baseline.

This helper is intentionally static. It proves the WS7 visible HUD panel,
card-model, provider-contract truth, anchored click-through posture, toggle /
task-tray posture, no-data/degraded copy, and live-proof helper markers without
polling hardware, inventing metric values, persisting settings, or widening
into deferred product lanes.
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


def _require_no_collection_imports(text: str, label: str, failures: list[str]) -> None:
    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "win32", "powershell"):
        _require(
            forbidden not in text.casefold(),
            f"{label} must not perform {forbidden} collection in the WS7 product baseline",
            failures,
        )


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
        'data-product-surface="nexus-monitoring-hud"',
        'data-interaction-mode="anchored-click-through"',
        'data-provider-state="setup-required"',
        'data-warning-mode="visual-non-invasive"',
        'data-live-values="provider-required"',
        'data-keybind-policy="none"',
        'aria-label="Nexus Desktop AI Monitoring HUD product visibility baseline"',
        'aria-label="Configurable sensor card model"',
        'aria-hidden="true"',
        "Nexus Desktop AI",
        "Monitoring HUD",
        "HUD enabled",
        "Provider setup required",
        "Hardware values stay hidden until a safe provider and validation route exist.",
        "Movable panel",
        "Snap-ready",
        "Anchored click-through",
        "Task tray unanchor path",
        "No default keybinds",
        'data-sensor-card="cpu-thermal"',
        'data-sensor-card="gpu-thermal"',
        'data-sensor-card="cpu-load"',
        'data-sensor-card="gpu-load"',
        'data-live-value="blocked-until-provider"',
        "CPU Thermal",
        "GPU Thermal",
        "CPU Load",
        "GPU Load",
        "Provider required",
        "Unavailable",
        "No live value",
        "No polling yet",
        "No polling until provider selection",
        "Provider-contract-first",
        "Movable top-right snap rail",
        "Resizable card grid",
        "Optional HUD layer",
        "On/off represented",
        "Show unavailable; no fake values",
        "Name reconnect/setup gap",
        "Visual badge only",
        "Full desktop required",
        "Pending acceptance",
        "PKG-006 in progress",
    ):
        _require_contains(hud_section, needle, "monitoring HUD HTML", failures)

    retired_product_name = "".join(chr(code) for code in (74, 97, 114, 118, 105, 115)).casefold()
    for forbidden in ("voice", "audio", "spoken", "microphone", retired_product_name):
        _require(
            forbidden not in hud_section.casefold(),
            f"monitoring HUD HTML must not introduce {forbidden} behavior in WS7",
            failures,
        )

    fake_metric_pattern = re.compile(
        r"\b\d+(?:\.\d+)?\s?(?:°|c\b|%|rpm\b|mhz\b|ghz\b|w\b)",
        flags=re.IGNORECASE,
    )
    _require(
        fake_metric_pattern.search(hud_section) is None,
        "monitoring HUD HTML must not present numeric hardware values before provider proof exists",
        failures,
    )

    for needle in (
        "#monitoring-hud {",
        "display: none;",
        "body.desktop-mode #monitoring-hud",
        "width: min(560px, calc(100vw - 36px));",
        'font-family: "Bahnschrift", "Rajdhani", "Segoe UI", sans-serif;',
        "pointer-events: none",
        ".monitoring-hud__chrome",
        ".monitoring-hud__anchor-rail",
        ".monitoring-hud__card-grid",
        ".monitoring-hud-card",
        ".monitoring-hud-card--setup",
        ".monitoring-hud-card--unavailable",
        ".monitoring-hud-card--warning",
        "resize: both;",
        ".monitoring-hud__resize-corner",
        "@media (max-width: 760px), (max-height: 620px)",
        "@keyframes monitoringHudSettle",
    ):
        _require_contains(css, needle, "monitoring HUD CSS", failures)

    for needle in (
        'const monitoringHud = document.getElementById("monitoring-hud")',
        'const monitoringHudProviderState = document.getElementById("monitoring-hud-provider-state")',
        'const monitoringHudWarningPosture = document.getElementById("monitoring-hud-warning-posture")',
        'const monitoringHudTrayPath = document.getElementById("monitoring-hud-tray-path")',
        "window.setDesktopSurfaceMode = function(enabled)",
        'monitoringHud.dataset.renderState = isEnabled ? "product-visibility-baseline" : "hidden"',
        'monitoringHud.dataset.productSurfaceState = isEnabled ? "visible-user-facing" : "hidden"',
        "window.setMonitoringHudTelemetry = function(snapshot)",
        'monitoringHud.dataset.providerState = "setup-required"',
        'monitoringHud.dataset.liveValues = "provider-required"',
        'monitoringHudProviderState.textContent = "Provider setup required"',
        "window.setMonitoringHudPlacementOwnership = function(contract)",
        'monitoringHud.dataset.interactionMode = "anchored-click-through"',
        'monitoringHudPlacementAnchor.textContent = monitoringHudPlacement.anchor || "Movable top-right snap rail"',
        'monitoringHudPlacementPointer.textContent = monitoringHudPlacement.pointerModel || "Anchored click-through"',
        'monitoringHudResizePosture.textContent = monitoringHudPlacement.resizePosture || "Resizable card grid"',
        "window.setMonitoringHudControlsVisibility = function(contract)",
        'monitoringHud.dataset.controlsState = "toggle-posture-visible"',
        'monitoringHud.dataset.keybindPolicy = "none"',
        'monitoringHudControlsVisibility.textContent = monitoringHudControls.visibilityState || "Optional HUD layer"',
        'monitoringHudTrayPath.textContent = "Task tray unanchor path"',
        "window.setMonitoringHudStatusBehavior = function(snapshot)",
        'monitoringHud.dataset.warningMode = "visual-non-invasive"',
        'monitoringHudWarningPosture.textContent = "Visual badge only"',
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
        'monitoringHud.dataset.renderState = "product-visibility-baseline"',
        'monitoringHud.dataset.productSurfaceState = "visible-user-facing"',
        "MONITORING_HUD_BASELINE_READY",
        'baseline="product_visibility_baseline"',
        "MONITORING_HUD_PRODUCT_VISIBILITY_READY",
        'seam="WS7"',
        'proof="visible_hud_card_panel"',
        "MONITORING_HUD_VISIBLE_OVERLAY_READY",
        'pointer_model="click_through_no_focus"',
        "DESKTOP_VISIBLE_OVERLAY_RESULT|success=true",
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
        'owner="DesktopRuntimeWindow"',
        'placement="desktop-renderer-top-right"',
        'controls="hud-controls-visibility"',
        'persistence="not_persisted"',
        'status="hud-local-readiness-status"',
        'source_truth="renderer_local"',
    ):
        _require_contains(renderer, needle, "desktop renderer HUD hook", failures)

    desktop_mode_method = re.search(
        r"def _apply_desktop_surface_mode\(self\):.*?def _monitoring_hud_telemetry_snapshot",
        renderer,
        flags=re.DOTALL,
    )
    method_text = desktop_mode_method.group(0).casefold() if desktop_mode_method else ""
    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "settings"):
        _require(
            forbidden not in method_text,
            f"desktop renderer HUD product hook must not implement {forbidden} behavior",
            failures,
        )

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-025"',
        'ADAPTER_ID = "desktop-runtime-boundary"',
        "provider-contract-first posture",
        'adapter_status="Provider contract boundary ready"',
        'source_scope="Provider-contract-first local runtime readiness"',
        'hardware_polling="No polling until provider selection"',
    ):
        _require_contains(telemetry, needle, "monitoring HUD telemetry adapter", failures)
    _require_no_collection_imports(telemetry, "monitoring HUD telemetry adapter", failures)

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-026"',
        'PLACEMENT_ID = "desktop-renderer-top-right"',
        'renderer_owner="DesktopRuntimeWindow"',
        'anchor="Movable top-right snap rail"',
        'pointer_model="Anchored click-through/no-focus-steal"',
        'z_index="18"',
    ):
        _require_contains(placement, needle, "monitoring HUD placement contract", failures)
    _require_no_collection_imports(placement, "monitoring HUD placement contract", failures)

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-027"',
        'CONTROLS_ID = "hud-controls-visibility"',
        'visibility_state="Optional HUD layer visible in desktop mode" if desktop_mode else "Waiting for desktop mode"',
        'control_surface="Toggle/on-off and task-tray unanchor posture represented"',
        'persistence="Not persisted"',
        'operator_action="No default keybinds"',
    ):
        _require_contains(controls, needle, "monitoring HUD controls visibility contract", failures)
    _require_no_collection_imports(controls, "monitoring HUD controls visibility contract", failures)

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-028"',
        'STATUS_ID = "hud-local-readiness-status"',
        'status_kind = "no-data"',
        'status_kind = "degraded"',
        'status_kind = "ready"',
        'status_label = "Provider setup required"',
        'status_label = "Reconnect/setup route unavailable"',
        'no_data_behavior="Show setup/unavailable state; do not invent hardware values"',
        'degraded_behavior="Name reconnect/setup gap with visual warning only"',
        'source_truth="Provider-contract-first local readiness only"',
    ):
        _require_contains(status, needle, "monitoring HUD status behavior contract", failures)
    _require_no_collection_imports(status, "monitoring HUD status behavior contract", failures)

    for needle in (
        "SLC-029",
        "WS7 - Monitoring HUD Product Visibility And Acceptance Baseline",
        "MONITORING_HUD_BASELINE_READY",
        "MONITORING_HUD_PRODUCT_VISIBILITY_READY",
        "MONITORING_HUD_VISIBLE_OVERLAY_READY",
        "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
        "MONITORING_HUD_PLACEMENT_OWNERSHIP_READY",
        "MONITORING_HUD_CONTROLS_VISIBILITY_READY",
        "MONITORING_HUD_STATUS_BEHAVIOR_READY",
        "DESKTOP_VISIBLE_OVERLAY_RESULT|success=true",
        "DESKTOP_OUTCOME|SETTLED|state=dormant",
        "settling visible overlay before full-desktop screenshot",
        "monitoring_hud_desktop.png",
        "manifest.json",
        "Stop-Process -Id $script:RuntimeProcess.Id -Force",
        "No-progress watchdog exceeded",
    ):
        _require_contains(live_validation, needle, "monitoring HUD live validation helper", failures)

    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("FAIL: FAM-006 Monitoring/HUD product visibility validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: FAM-006 HUD product visibility baseline is bounded, visible, provider-truthful, and marker-backed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
