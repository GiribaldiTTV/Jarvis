"""Monitoring/HUD controls visibility contract for FAM-006.

This module defines the SLC-027 settings and user-controls visibility boundary.
It exposes the current Dashboard-first HUD feature toggle posture while keeping
the deferred Overlay anchor/unanchor path non-gating until a later interface
release admits it.
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
    monitor_management: str
    overlay_mode_controls: str
    warning_controls: str

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
            "monitorManagement": self.monitor_management,
            "overlayModeControls": self.overlay_mode_controls,
            "warningControls": self.warning_controls,
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
            "Enable or disable HUD feature from dashboard/tray"
            if desktop_mode and visible
            else "HUD feature disabled from dashboard/tray"
            if desktop_mode
            else "Waiting for desktop mode"
        ),
        control_surface="Dashboard controls HUD feature state; Overlay controls remain deferred",
        persistence="Store group/layout posture locally",
        operator_action="No default keybinds",
        anchor_state="overlay-deferred",
        tray_path="Task tray enables/disables HUD feature; Overlay anchor controls deferred",
        snap_state="enabled" if snap_enabled else "disabled",
        polling_rate_ms=str(max(1000, int(polling_rate_ms or 1000))),
        monitor_management="Dashboard creates, edits, enables, disables, and sets polling for monitor groups",
        overlay_mode_controls="Overlay display and anchor/unanchor controls are deferred/non-gating",
        warning_controls="Visual badge, text label, and color state only; no audio or screen flash",
    )
