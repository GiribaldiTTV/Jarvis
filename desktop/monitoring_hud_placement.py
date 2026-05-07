"""Renderer-owned Monitoring/HUD placement contract for FAM-006.

This module defines the SLC-026 desktop placement and renderer ownership
boundary. It describes where the visible HUD is owned, movable/anchorable, and
click-through when anchored without adding provider-platform, live proof, or
cross-family behavior.
"""

from __future__ import annotations

from dataclasses import dataclass


PACKAGE_ID = "PKG-006"
SLICE_ID = "SLC-026"
PLACEMENT_ID = "desktop-renderer-top-right"


@dataclass(frozen=True)
class MonitoringHudPlacementContract:
    package_id: str
    slice_id: str
    placement_id: str
    renderer_owner: str
    surface_owner: str
    anchor: str
    pointer_model: str
    z_index: str
    desktop_mode: str
    window_geometry: dict[str, int]

    def as_dict(self) -> dict[str, object]:
        return {
            "packageId": self.package_id,
            "sliceId": self.slice_id,
            "placementId": self.placement_id,
            "rendererOwner": self.renderer_owner,
            "surfaceOwner": self.surface_owner,
            "anchor": self.anchor,
            "pointerModel": self.pointer_model,
            "zIndex": self.z_index,
            "desktopMode": self.desktop_mode,
            "windowGeometry": dict(self.window_geometry),
        }


def build_monitoring_hud_placement_contract(
    *,
    desktop_mode: bool,
    x: int,
    y: int,
    width: int,
    height: int,
) -> MonitoringHudPlacementContract:
    """Build the HUD placement contract owned by the desktop renderer."""

    return MonitoringHudPlacementContract(
        package_id=PACKAGE_ID,
        slice_id=SLICE_ID,
        placement_id=PLACEMENT_ID,
        renderer_owner="DesktopRuntimeWindow",
        surface_owner="Qt WebEngine desktop child surface",
        anchor="Movable top-right snap rail",
        pointer_model="Anchored click-through/no-focus-steal",
        z_index="18",
        desktop_mode="enabled" if desktop_mode else "pending",
        window_geometry={
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height),
        },
    )
