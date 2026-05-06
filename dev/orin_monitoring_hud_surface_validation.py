"""Validate the FAM-006 Monitoring HUD visual baseline contract.

This helper is intentionally static for SLC-016. It proves the desktop-only
visual surface, source-truth markers, and slice-boundary copy without sampling
telemetry, changing settings, modeling fail-safe states, or touching voice/audio.
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

    hud_section = _html_section(html)
    _require(bool(hud_section), "orin_core.html is missing the monitoring-hud section", failures)
    for needle in (
        'data-package="PKG-006"',
        'data-slice="SLC-016"',
        'aria-label="Monitoring HUD visual baseline"',
        'aria-hidden="true"',
        "FAM-006 Monitoring HUD",
        "System surface baseline",
        "Visual layer online",
        "Pending SLC-025",
        "Pending SLC-026",
        "Pending SLC-027",
        "Pending SLC-028",
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
        "window.setDesktopSurfaceMode(false)",
    ):
        _require_contains(js, needle, "monitoring HUD JavaScript", failures)

    for needle in (
        "def _apply_desktop_surface_mode(self):",
        "window.setDesktopSurfaceMode(true)",
        "MONITORING_HUD_BASELINE_READY",
        'package="PKG-006"',
        'slice="SLC-016"',
        'baseline="visual_only"',
        "self._apply_desktop_surface_mode()",
    ):
        _require_contains(renderer, needle, "desktop renderer HUD hook", failures)

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

    print("PASS: FAM-006 SLC-016 HUD visual baseline is visible, bounded, and marker-backed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
