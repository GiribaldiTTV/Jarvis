"""Monitoring/HUD controls visibility contract for FAM-006.

This module defines the SLC-027 settings and user-controls visibility boundary.
It exposes the optional HUD layer, toggle posture, task-tray unanchor path,
snap posture, and bounded polling choices without adding broad provider
platform work or cross-family behavior.
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
    anchor_state: str
    tray_path: str
    snap_state: str
    polling_rate_ms: str

    def as_dict(self) -> dict[str, str]:
        return {
            "packageId": self.package_id,
            "sliceId": self.slice_id,
            "controlsId": self.controls_id,
            "visibilityState": self.visibility_state,
            "controlSurface": self.control_surface,
            "persistence": self.persistence,
            "operatorAction": self.operator_action,
            "anchorState": self.anchor_state,
            "trayPath": self.tray_path,
            "snapState": self.snap_state,
            "pollingRateMs": self.polling_rate_ms,
        }


def build_monitoring_hud_controls_visibility_contract(
    *,
    desktop_mode: bool,
    visible: bool = True,
    anchored: bool = True,
    snap_enabled: bool = True,
    polling_rate_ms: int = 1000,
) -> MonitoringHudControlsVisibilityContract:
    """Build the HUD controls visibility contract from renderer state."""

    return MonitoringHudControlsVisibilityContract(
        package_id=PACKAGE_ID,
        slice_id=SLICE_ID,
        controls_id=CONTROLS_ID,
        visibility_state=(
            "Optional HUD layer visible in desktop mode"
            if desktop_mode and visible
            else "Optional HUD layer hidden"
            if desktop_mode
            else "Waiting for desktop mode"
        ),
        control_surface="Toggle/on-off, task-tray unanchor, snap, and polling controls represented",
        persistence="Local browser layout state",
        operator_action="No default keybinds",
        anchor_state="anchored-click-through" if anchored else "unanchored-edit-mode",
        tray_path="Task tray can unanchor or restore the HUD",
        snap_state="enabled" if snap_enabled else "disabled",
        polling_rate_ms=str(max(1000, int(polling_rate_ms or 1000))),
    )
