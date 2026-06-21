"""FAM-003 resident access and quick-action route contract.

This module keeps the tray doorway model local and deterministic. It does not
load providers, call models, probe hardware, or implement owner-FAM surfaces.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


RESIDENT_ACCESS_SETTINGS_SCHEMA_VERSION = "resident-access-settings.v1"
TRAY_IDENTITY_LABEL = "Nexus Desktop AI"
TRAY_ORIN_MARK_LABEL = "ORIN"
RESIDENT_STATUS_LOCAL_NO_PROVIDER = "AI local/no provider; Provider-visible data: none"
TRAY_TOOLTIP_TEXT = f"{TRAY_IDENTITY_LABEL} - {RESIDENT_STATUS_LOCAL_NO_PROVIDER}"
TRAY_DISCOVERY_DURATION_MS = 4500
WINDOWS_TRAY_VISIBILITY_LIMITATION = (
    "Windows controls whether app notification icons stay pinned or move under hidden icons. "
    "Nexus can show the icon and a discovery cue, but it cannot force permanent tray placement."
)
TRAY_DISCOVERY_MESSAGE = (
    "Nexus Desktop AI is running in the Windows notification area. "
    "If you do not see the icon, open hidden icons (^). "
    + WINDOWS_TRAY_VISIBILITY_LIMITATION
)
DEFAULT_QUICK_SLOT_ROUTE_IDS = (
    "command_overlay",
    "create_custom_task",
    "open_saved_actions_folder",
)
MAX_QUICK_SLOT_COUNT = 5
DEFAULT_QUICK_SLOT_COUNT = 3
IMMUTABLE_ROUTE_IDS = (
    "hud_dashboard",
    "global_settings",
    "ai_status_command_center",
    "privacy_lockdown",
    "exit_nexus",
)


@dataclass(frozen=True)
class ResidentAccessRoute:
    route_id: str
    label: str
    owner_family: str
    availability: str
    route_kind: str
    description: str
    immutable: bool = False
    quick_slot_candidate: bool = False
    enabled: bool = True

    def as_dict(self) -> dict[str, object]:
        return {
            "routeId": self.route_id,
            "label": self.label,
            "ownerFamily": self.owner_family,
            "availability": self.availability,
            "routeKind": self.route_kind,
            "description": self.description,
            "immutable": self.immutable,
            "quickSlotCandidate": self.quick_slot_candidate,
            "enabled": self.enabled,
        }


@dataclass(frozen=True)
class ResidentAccessSettings:
    quick_slot_ids: tuple[str, ...] = DEFAULT_QUICK_SLOT_ROUTE_IDS
    menu_budget: int = MAX_QUICK_SLOT_COUNT
    show_ai_privacy_status: bool = True
    schema_version: str = RESIDENT_ACCESS_SETTINGS_SCHEMA_VERSION

    def as_dict(self) -> dict[str, object]:
        return {
            "schemaVersion": self.schema_version,
            "quickSlotIds": list(self.quick_slot_ids),
            "menuBudget": self.menu_budget,
            "showAiPrivacyStatus": self.show_ai_privacy_status,
        }


ROUTE_CATALOG: tuple[ResidentAccessRoute, ...] = (
    ResidentAccessRoute(
        "hud_dashboard",
        "HUD Dashboard",
        "FAM-006",
        "available-through-existing-hud-route",
        "owner-surface",
        "Routes to the FAM-006 HUD Dashboard without taking ownership of HUD internals.",
        immutable=True,
    ),
    ResidentAccessRoute(
        "global_settings",
        "Global Settings",
        "FAM-003",
        "available-minimal-shell",
        "local-shell",
        "Opens the minimal Resident Access / Quick Access settings shell.",
        immutable=True,
    ),
    ResidentAccessRoute(
        "ai_status_command_center",
        "AI Status / Command Center",
        "FAM-007",
        "route-only-status-summary",
        "owner-bounded-route",
        "Shows FAM-007 no-provider/status copy and defers AI Command Center internals.",
        immutable=True,
    ),
    ResidentAccessRoute(
        "privacy_lockdown",
        "Privacy Lockdown",
        "FAM-007",
        "route-only-feedback",
        "owner-bounded-route",
        "Shows privacy route feedback only; provider/runtime privacy enforcement remains FAM-007.",
        immutable=True,
    ),
    ResidentAccessRoute(
        "exit_nexus",
        "Exit Nexus",
        "SHARED-DESKTOP-CORE",
        "available-confirmed-exit",
        "runtime-command",
        "Requests the existing fail-safe shutdown confirmation path.",
        immutable=True,
    ),
    ResidentAccessRoute(
        "command_overlay",
        "Open Command Overlay",
        "FAM-003",
        "available",
        "runtime-command",
        "Opens or closes the existing command overlay.",
        quick_slot_candidate=True,
    ),
    ResidentAccessRoute(
        "create_custom_task",
        "Create Custom Task",
        "FAM-003",
        "available",
        "runtime-command",
        "Routes to the existing tray-origin custom task authoring path.",
        quick_slot_candidate=True,
    ),
    ResidentAccessRoute(
        "open_saved_actions_folder",
        "Open Saved Actions Folder",
        "FAM-003",
        "available",
        "runtime-command",
        "Opens the local saved-actions folder through the shared action launcher.",
        quick_slot_candidate=True,
    ),
    ResidentAccessRoute(
        "recording_studio",
        "Recording Studio",
        "FAM-006",
        "future-gated-owner-surface",
        "owner-bounded-route",
        "Reserved quick slot for the FAM-006 Recording Studio when its surface is available.",
        quick_slot_candidate=True,
        enabled=False,
    ),
    ResidentAccessRoute(
        "log_viewer",
        "Log Viewer",
        "FAM-006",
        "future-gated-owner-surface",
        "owner-bounded-route",
        "Reserved quick slot for the FAM-006 Log Viewer when its surface is available.",
        quick_slot_candidate=True,
        enabled=False,
    ),
    ResidentAccessRoute(
        "tray_visibility_education",
        "Tray Visibility Help",
        "FAM-008",
        "route-only-copy",
        "owner-bounded-route",
        "Shows honest Windows tray visibility limitation copy without FAM-008 startup/package work.",
        quick_slot_candidate=True,
    ),
)

ROUTE_BY_ID = {route.route_id: route for route in ROUTE_CATALOG}


def default_resident_access_settings_path() -> Path:
    override = (os.environ.get("NEXUS_RESIDENT_ACCESS_SETTINGS_PATH") or "").strip()
    if override:
        return Path(override)
    local_app_data = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(local_app_data) / "Nexus Desktop AI" / "resident_access_settings.json"


def quick_slot_candidate_routes() -> tuple[ResidentAccessRoute, ...]:
    return tuple(route for route in ROUTE_CATALOG if route.quick_slot_candidate)


def immutable_routes() -> tuple[ResidentAccessRoute, ...]:
    return tuple(ROUTE_BY_ID[route_id] for route_id in IMMUTABLE_ROUTE_IDS)


def normalize_quick_slot_ids(slot_ids: Iterable[str] | None) -> tuple[str, ...]:
    candidate_ids = {route.route_id for route in quick_slot_candidate_routes()}
    normalized: list[str] = []
    for raw_id in tuple(slot_ids or ()):
        route_id = str(raw_id or "").strip()
        if route_id not in candidate_ids or route_id in normalized:
            continue
        normalized.append(route_id)
        if len(normalized) >= MAX_QUICK_SLOT_COUNT:
            break
    if not normalized:
        normalized.extend(DEFAULT_QUICK_SLOT_ROUTE_IDS)
    return tuple(normalized[:MAX_QUICK_SLOT_COUNT])


def normalize_resident_access_settings(raw: dict[str, object] | None = None) -> ResidentAccessSettings:
    raw = raw if isinstance(raw, dict) else {}
    quick_slot_ids = normalize_quick_slot_ids(raw.get("quickSlotIds"))
    try:
        menu_budget = int(raw.get("menuBudget", MAX_QUICK_SLOT_COUNT))
    except (TypeError, ValueError):
        menu_budget = MAX_QUICK_SLOT_COUNT
    menu_budget = min(MAX_QUICK_SLOT_COUNT, max(DEFAULT_QUICK_SLOT_COUNT, menu_budget))
    show_status = raw.get("showAiPrivacyStatus", True)
    return ResidentAccessSettings(
        quick_slot_ids=quick_slot_ids,
        menu_budget=menu_budget,
        show_ai_privacy_status=bool(show_status),
    )


def load_resident_access_settings(path: str | os.PathLike[str] | None = None) -> ResidentAccessSettings:
    settings_path = Path(path) if path else default_resident_access_settings_path()
    try:
        raw = json.loads(settings_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ResidentAccessSettings()
    except Exception:
        return ResidentAccessSettings()
    return normalize_resident_access_settings(raw)


def save_resident_access_settings(
    settings: ResidentAccessSettings,
    path: str | os.PathLike[str] | None = None,
) -> Path:
    normalized = normalize_resident_access_settings(settings.as_dict())
    settings_path = Path(path) if path else default_resident_access_settings_path()
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(
        json.dumps(normalized.as_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return settings_path


def route_for_id(route_id: str) -> ResidentAccessRoute | None:
    return ROUTE_BY_ID.get(str(route_id or "").strip())


def configured_quick_slot_routes(settings: ResidentAccessSettings | None = None) -> tuple[ResidentAccessRoute, ...]:
    settings = settings or load_resident_access_settings()
    routes: list[ResidentAccessRoute] = []
    for route_id in normalize_quick_slot_ids(settings.quick_slot_ids):
        route = route_for_id(route_id)
        if route is not None:
            routes.append(route)
    return tuple(routes[: settings.menu_budget])


def _payload_value(payload: dict[str, object] | None, *keys: str, default: str = "") -> str:
    if not isinstance(payload, dict):
        return default
    for key in keys:
        value = payload.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return default


def build_ai_privacy_summary(ai_provider_state: dict[str, object] | None = None) -> dict[str, str]:
    provider_label = _payload_value(
        ai_provider_state,
        "providerLabel",
        "provider_label",
        default="No AI provider",
    )
    status_label = _payload_value(
        ai_provider_state,
        "statusLabel",
        "status_label",
        default="AI local/no provider",
    )
    visible_data_label = _payload_value(
        ai_provider_state,
        "providerVisibleDataLabel",
        "provider_visible_data_label",
        default="Provider-visible data: none",
    )
    privacy_label = _payload_value(
        ai_provider_state,
        "privacyLabel",
        "privacy_label",
        default="Local shell only; nothing is sent",
    )
    compact = f"{status_label}; {visible_data_label}"
    if len(compact) > 96:
        compact = RESIDENT_STATUS_LOCAL_NO_PROVIDER
    return {
        "providerLabel": provider_label,
        "statusLabel": status_label,
        "providerVisibleDataLabel": visible_data_label,
        "privacyLabel": privacy_label,
        "compactLabel": compact,
    }


def build_tray_tooltip_text(ai_summary: dict[str, str] | None = None) -> str:
    ai_summary = ai_summary if isinstance(ai_summary, dict) else {}
    compact_status = str(ai_summary.get("compactLabel") or RESIDENT_STATUS_LOCAL_NO_PROVIDER).strip()
    compact_status = compact_status.rstrip(".")
    return f"{TRAY_IDENTITY_LABEL} - {compact_status}"


def build_resident_access_menu_plan(
    *,
    settings: ResidentAccessSettings | None = None,
    ai_provider_state: dict[str, object] | None = None,
    monitoring_hud_state: dict[str, object] | None = None,
    command_overlay_state: dict[str, object] | None = None,
) -> dict[str, object]:
    settings = settings or load_resident_access_settings()
    ai_summary = build_ai_privacy_summary(ai_provider_state)
    quick_slots = configured_quick_slot_routes(settings)
    hud_state = monitoring_hud_state if isinstance(monitoring_hud_state, dict) else {}
    overlay_state = command_overlay_state if isinstance(command_overlay_state, dict) else {}
    return {
        "schemaVersion": RESIDENT_ACCESS_SETTINGS_SCHEMA_VERSION,
        "identityLabel": TRAY_IDENTITY_LABEL,
        "orinMarkLabel": TRAY_ORIN_MARK_LABEL,
        "tooltipText": build_tray_tooltip_text(ai_summary),
        "statusLabel": ai_summary["compactLabel"],
        "windowsTrayVisibilityLimitation": WINDOWS_TRAY_VISIBILITY_LIMITATION,
        "menuBudget": {
            "defaultQuickSlots": DEFAULT_QUICK_SLOT_COUNT,
            "maximumQuickSlots": MAX_QUICK_SLOT_COUNT,
            "currentQuickSlots": len(quick_slots),
        },
        "aiPrivacy": ai_summary,
        "hudState": {
            "featureEnabled": bool(hud_state.get("feature_enabled")),
            "dashboardVisible": bool(hud_state.get("dashboard_visible")),
            "overlayDeferred": hud_state.get("overlay_deferred", True) is not False,
        },
        "commandOverlay": {
            "visible": bool(overlay_state.get("visible")),
            "phase": str(overlay_state.get("phase") or "closed"),
        },
        "immutableRoutes": [route.as_dict() for route in immutable_routes()],
        "quickSlots": [route.as_dict() for route in quick_slots],
        "candidateRoutes": [route.as_dict() for route in quick_slot_candidate_routes()],
        "settings": settings.as_dict(),
        "singleTrayIconContract": (
            "FAM-003 owns the resident doorway identity and menu routing; FAM-007 status appears inside "
            "the same single tray icon/menu instead of creating a second tray icon."
        ),
    }
