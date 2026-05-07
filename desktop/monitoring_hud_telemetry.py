"""Local Monitoring/HUD telemetry boundary helpers for FAM-006.

This module defines the SLC-025 adapter shape. It reports only local runtime
readiness facts that the desktop renderer already owns; it does not poll
hardware sensors, read vendor APIs, model degraded states, or change settings.
WS7 uses this provider-contract-first posture so the visible HUD can show
setup/unavailable states without inventing hardware values.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


PACKAGE_ID = "PKG-006"
SLICE_ID = "SLC-025"
ADAPTER_ID = "desktop-runtime-boundary"


@dataclass(frozen=True)
class MonitoringHudSource:
    label: str
    value: str
    source: str

    def as_dict(self) -> dict[str, str]:
        return {
            "label": self.label,
            "value": self.value,
            "source": self.source,
        }


@dataclass(frozen=True)
class MonitoringHudTelemetrySnapshot:
    package_id: str
    slice_id: str
    adapter_id: str
    adapter_status: str
    source_scope: str
    hardware_polling: str
    sources: tuple[MonitoringHudSource, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "packageId": self.package_id,
            "sliceId": self.slice_id,
            "adapterId": self.adapter_id,
            "adapterStatus": self.adapter_status,
            "sourceScope": self.source_scope,
            "hardwarePolling": self.hardware_polling,
            "sources": [source.as_dict() for source in self.sources],
        }


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def build_monitoring_hud_telemetry_snapshot(
    *,
    page_ready: bool,
    desktop_mode: bool,
    runtime_log_path: str = "",
    event_route_present: bool = False,
) -> MonitoringHudTelemetrySnapshot:
    """Build a HUD-ready local runtime snapshot without collecting telemetry."""

    runtime_log = os.path.abspath(runtime_log_path) if runtime_log_path else ""
    runtime_log_label = "runtime log route present" if runtime_log else "runtime log route not supplied"
    event_route_label = "event route present" if event_route_present else "event route not supplied"

    return MonitoringHudTelemetrySnapshot(
        package_id=PACKAGE_ID,
        slice_id=SLICE_ID,
        adapter_id=ADAPTER_ID,
        adapter_status="Provider contract boundary ready",
        source_scope="Provider-contract-first local runtime readiness",
        hardware_polling="No polling until provider selection",
        sources=(
            MonitoringHudSource("Visual page", "ready" if page_ready else "loading", "renderer page state"),
            MonitoringHudSource("Desktop surface", "enabled" if desktop_mode else "pending", "desktop mode flag"),
            MonitoringHudSource("Runtime log", runtime_log_label, "runtime log path"),
            MonitoringHudSource("Event route", event_route_label, "renderer event logger"),
        ),
    )
