"""Monitoring/HUD controls visibility contract for FAM-006.

This module defines the SLC-027 settings and user-controls visibility boundary.
It exposes the optional HUD layer, toggle posture, and task-tray unanchor path
without persisting preferences, implementing provider polling, or adding
cross-family behavior.
"""

from __future__ import annotations

from dataclasses import dataclass


PACKAGE_ID = "PKG-006"
SLICE_ID = "SLC-027"
CONTROLS_ID = "hud-controls-visibility"


@dataclass(frozen=True)
class MonitoringHudControlsVisibilityContract:
    package_id: str
    slice_id: str
    controls_id: str
    visibility_state: str
    control_surface: str
    persistence: str
    operator_action: str

    def as_dict(self) -> dict[str, str]:
        return {
            "packageId": self.package_id,
            "sliceId": self.slice_id,
            "controlsId": self.controls_id,
            "visibilityState": self.visibility_state,
            "controlSurface": self.control_surface,
            "persistence": self.persistence,
            "operatorAction": self.operator_action,
        }


def build_monitoring_hud_controls_visibility_contract(
    *,
    desktop_mode: bool,
) -> MonitoringHudControlsVisibilityContract:
    """Build the HUD controls visibility contract without changing preferences."""

    return MonitoringHudControlsVisibilityContract(
        package_id=PACKAGE_ID,
        slice_id=SLICE_ID,
        controls_id=CONTROLS_ID,
        visibility_state="Optional HUD layer visible in desktop mode" if desktop_mode else "Waiting for desktop mode",
        control_surface="Toggle/on-off and task-tray unanchor posture represented",
        persistence="Not persisted",
        operator_action="No default keybinds",
    )
