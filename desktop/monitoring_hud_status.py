"""Monitoring/HUD fail-safe status contract for FAM-006.

This module defines the SLC-028 no-data and degraded-status behavior for the
HUD. It uses only renderer-owned readiness facts and does not poll hardware,
perform live proof, persist preferences, or touch voice/audio behavior.
"""

from __future__ import annotations

from dataclasses import dataclass


PACKAGE_ID = "PKG-006"
SLICE_ID = "SLC-028"
STATUS_ID = "hud-local-readiness-status"


@dataclass(frozen=True)
class MonitoringHudStatusSnapshot:
    package_id: str
    slice_id: str
    status_id: str
    status_kind: str
    status_label: str
    no_data_behavior: str
    degraded_behavior: str
    source_truth: str

    def as_dict(self) -> dict[str, str]:
        return {
            "packageId": self.package_id,
            "sliceId": self.slice_id,
            "statusId": self.status_id,
            "statusKind": self.status_kind,
            "statusLabel": self.status_label,
            "noDataBehavior": self.no_data_behavior,
            "degradedBehavior": self.degraded_behavior,
            "sourceTruth": self.source_truth,
        }


def build_monitoring_hud_status_snapshot(
    *,
    page_ready: bool,
    desktop_mode: bool,
    event_route_present: bool,
) -> MonitoringHudStatusSnapshot:
    """Build truthful no-data/degraded HUD status from local renderer facts."""

    if not page_ready:
        status_kind = "no-data"
        status_label = "Waiting for visual source"
    elif not desktop_mode:
        status_kind = "degraded"
        status_label = "Desktop surface pending"
    elif not event_route_present:
        status_kind = "degraded"
        status_label = "Event route unavailable"
    else:
        status_kind = "ready"
        status_label = "Local readiness available"

    return MonitoringHudStatusSnapshot(
        package_id=PACKAGE_ID,
        slice_id=SLICE_ID,
        status_id=STATUS_ID,
        status_kind=status_kind,
        status_label=status_label,
        no_data_behavior="Show waiting state; do not imply unavailable telemetry exists",
        degraded_behavior="Name the local readiness gap without recovery claims",
        source_truth="Renderer-owned local readiness only",
    )
