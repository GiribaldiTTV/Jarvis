"""Validate the FAM-006 Monitoring HUD visual and telemetry boundary contract.

This helper is intentionally static for SLC-016/SLC-025. It proves the
desktop-only visual surface, runtime telemetry adapter boundary, source-truth
markers, and slice-boundary copy without polling hardware, changing settings,
modeling fail-safe states, or touching voice/audio.
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

    html = _read("jarvis_visual/orin_core.html")
    css = _read("jarvis_visual/orin_core.css")
    js = _read("jarvis_visual/orin_core.js")
    renderer = _read("desktop/desktop_renderer.py")
    telemetry = _read("desktop/monitoring_hud_telemetry.py")

    hud_section = _html_section(html)
    _require(bool(hud_section), "orin_core.html is missing the monitoring-hud section", failures)
    for needle in (
        'data-package="PKG-006"',
        'data-slice="SLC-016"',
        'data-slice="SLC-025"',
        'aria-label="Monitoring HUD visual baseline"',
        'aria-label="Runtime telemetry adapter boundary"',
        'aria-hidden="true"',
        "FAM-006 Monitoring HUD",
        "System surface baseline",
        "Visual layer online",
        "Active SLC-025",
        "Pending SLC-026",
        "Pending SLC-027",
        "Pending SLC-028",
        "Adapter boundary",
        "Local runtime only",
        "Not performed",
    ):
        _require_contains(hud_section, needle, "monitoring HUD HTML", failures)

    for forbidden in ("voice", "audio", "spoken", "microphone"):
        _require(
            forbidden not in hud_section.casefold(),
            f"monitoring HUD HTML must not introduce {forbidden} behavior in SLC-016",
            failures,
        )

    for needle in (
        "#monitoring-hud {",
        "display: none;",
        "body.desktop-mode #monitoring-hud",
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
        "window.setDesktopSurfaceMode(false)",
        "window.setMonitoringHudTelemetry({})",
    ):
        _require_contains(js, needle, "monitoring HUD JavaScript", failures)

    for needle in (
        "from .monitoring_hud_telemetry import build_monitoring_hud_telemetry_snapshot",
        "def _apply_desktop_surface_mode(self):",
        "def _monitoring_hud_telemetry_snapshot(self) -> dict[str, object]:",
        "def _publish_monitoring_hud_telemetry_boundary(self):",
        "build_monitoring_hud_telemetry_snapshot(",
        "window.setDesktopSurfaceMode(true)",
        "window.setMonitoringHudTelemetry",
        "MONITORING_HUD_BASELINE_READY",
        "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
        'package="PKG-006"',
        'slice="SLC-016"',
        'slice="SLC-025"',
        'adapter="desktop-runtime-boundary"',
        'hardware_polling="not_performed"',
        'baseline="visual_only"',
        "self._apply_desktop_surface_mode()",
        "self._publish_monitoring_hud_telemetry_boundary()",
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
        print("FAIL: FAM-006 SLC-016 HUD visual baseline validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: FAM-006 HUD visual baseline and telemetry boundary are bounded and marker-backed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
