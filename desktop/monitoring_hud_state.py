import datetime
import json
import os
from pathlib import Path


MONITORING_HUD_STATE_ENV = "NEXUS_MONITORING_HUD_STATE_PATH"
MONITORING_HUD_STATE_FILENAME = "monitoring_hud_state.json"
OVERLAY_PROFILE_SCHEMA_VERSION = 1
DEFAULT_OVERLAY_PROFILE_ID = "default-overlay-profile"
RECORDING_PROFILE_SCHEMA_VERSION = 1
DEFAULT_RECORDING_PROFILE_ID = "default-recording-profile"


def _emit(event_logger, event: str) -> None:
    if callable(event_logger):
        try:
            event_logger(event)
        except Exception:
            pass


def monitoring_hud_state_path() -> Path:
    override = os.environ.get(MONITORING_HUD_STATE_ENV, "").strip()
    if override:
        return Path(override)
    local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
    if local_app_data:
        return Path(local_app_data) / "Nexus Desktop AI" / MONITORING_HUD_STATE_FILENAME
    return Path.home() / "AppData" / "Local" / "Nexus Desktop AI" / MONITORING_HUD_STATE_FILENAME


def _stable_monitor_ids(values) -> list[str]:
    seen: set[str] = set()
    monitor_ids: list[str] = []
    if not isinstance(values, list):
        return monitor_ids
    for value in values:
        monitor_id = str(value or "").strip()
        if not monitor_id or monitor_id in seen:
            continue
        seen.add(monitor_id)
        monitor_ids.append(monitor_id)
    return monitor_ids


def _stable_string_ids(values) -> list[str]:
    seen: set[str] = set()
    string_ids: list[str] = []
    if not isinstance(values, list):
        return string_ids
    for value in values:
        string_id = str(value or "").strip()
        if not string_id or string_id in seen:
            continue
        seen.add(string_id)
        string_ids.append(string_id)
    return string_ids


def default_overlay_profile_state(monitor_ids=None, previous_profile=None) -> dict[str, object]:
    previous = previous_profile if isinstance(previous_profile, dict) else {}
    allowed_monitor_ids = _stable_monitor_ids(monitor_ids or [])
    allowed_monitor_id_set = set(allowed_monitor_ids)
    previous_monitor_ids = (
        [
            monitor_id
            for monitor_id in _stable_monitor_ids(previous.get("monitorIds"))
            if not allowed_monitor_id_set or monitor_id in allowed_monitor_id_set
        ]
        if isinstance(previous.get("monitorIds"), list)
        else None
    )
    return {
        "id": DEFAULT_OVERLAY_PROFILE_ID,
        "schemaVersion": OVERLAY_PROFILE_SCHEMA_VERSION,
        "kind": "overlay-profile",
        "scope": "overlay-visible-monitor-membership",
        "name": str(previous.get("name") or "Default Overlay Profile"),
        "monitorIds": previous_monitor_ids if previous_monitor_ids is not None else allowed_monitor_ids,
        "displayMode": str(previous.get("displayMode") or "monitor-cards"),
        "source": str(previous.get("source") or "legacy-monitor-card-migration"),
        "dirty": False,
    }


def normalize_monitoring_hud_overlay_profiles(payload=None, monitor_ids=None) -> dict[str, object]:
    source_payload = payload if isinstance(payload, dict) else {}
    allowed_monitor_ids = _stable_monitor_ids(monitor_ids or source_payload.get("monitorIds") or [])
    allowed_monitor_id_set = set(allowed_monitor_ids)
    has_overlay_profiles_payload = "overlayProfiles" in source_payload
    default_profile_deleted_by_user = bool(source_payload.get("overlayProfileDefaultDeletedByUser"))
    raw_profiles = source_payload.get("overlayProfiles")
    if not isinstance(raw_profiles, dict):
        raw_profiles = {}
    profiles: dict[str, dict[str, object]] = {}
    for profile_key, raw_profile in raw_profiles.items():
        if not isinstance(raw_profile, dict):
            continue
        profile_id = str(raw_profile.get("id") or profile_key or "").strip()
        if not profile_id:
            continue
        raw_monitor_ids = _stable_monitor_ids(raw_profile.get("monitorIds") or [])
        monitor_members = [
            monitor_id
            for monitor_id in raw_monitor_ids
            if not allowed_monitor_id_set or monitor_id in allowed_monitor_id_set
        ]
        profiles[profile_id] = {
            "id": profile_id,
            "schemaVersion": OVERLAY_PROFILE_SCHEMA_VERSION,
            "kind": "overlay-profile",
            "scope": "overlay-visible-monitor-membership",
            "name": str(raw_profile.get("name") or "Overlay Profile"),
            "monitorIds": monitor_members,
            "displayMode": str(raw_profile.get("displayMode") or "monitor-cards"),
            "source": str(raw_profile.get("source") or "persisted-overlay-profile-state"),
            "dirty": bool(raw_profile.get("dirty")),
        }
    active_profile_id = str(source_payload.get("activeOverlayProfileId") or "").strip()
    should_ensure_default_profile = (
        not has_overlay_profiles_payload
        or DEFAULT_OVERLAY_PROFILE_ID in raw_profiles
        or (
            not default_profile_deleted_by_user
            and (
                not profiles
                or active_profile_id == DEFAULT_OVERLAY_PROFILE_ID
                or active_profile_id not in profiles
            )
        )
    )
    if should_ensure_default_profile:
        profiles[DEFAULT_OVERLAY_PROFILE_ID] = default_overlay_profile_state(
            allowed_monitor_ids,
            profiles.get(DEFAULT_OVERLAY_PROFILE_ID) or raw_profiles.get(DEFAULT_OVERLAY_PROFILE_ID),
        )
    if active_profile_id not in profiles:
        active_profile_id = DEFAULT_OVERLAY_PROFILE_ID if DEFAULT_OVERLAY_PROFILE_ID in profiles else next(iter(profiles), "")
    default_profile = profiles.get(DEFAULT_OVERLAY_PROFILE_ID)
    return {
        "overlayProfileSchemaVersion": OVERLAY_PROFILE_SCHEMA_VERSION,
        "activeOverlayProfileId": active_profile_id,
        "overlayProfileDefaultDeletedByUser": default_profile_deleted_by_user
        and DEFAULT_OVERLAY_PROFILE_ID not in profiles,
        "overlayProfiles": profiles,
        "overlayProfileStateProof": {
            "schemaVersion": OVERLAY_PROFILE_SCHEMA_VERSION,
            "activeProfileId": active_profile_id,
            "defaultProfileId": DEFAULT_OVERLAY_PROFILE_ID,
            "defaultProfileMonitorIds": list(default_profile.get("monitorIds", []))
            if isinstance(default_profile, dict)
            else [],
            "defaultProfileDeletedByUser": default_profile_deleted_by_user
            and DEFAULT_OVERLAY_PROFILE_ID not in profiles,
            "profileCount": len(profiles),
            "monitorGroupBoundary": "monitor-groups-organize-configuration-only",
            "recordingProfileBoundary": "recording-profile-state-absent-future-gated",
            "visibleEditorUi": "slc-039-membership-editor",
        },
    }


def default_recording_profile_state(previous_profile=None, monitor_ids=None) -> dict[str, object]:
    previous = previous_profile if isinstance(previous_profile, dict) else {}
    allowed_monitor_ids = _stable_monitor_ids(monitor_ids or [])
    allowed_monitor_id_set = set(allowed_monitor_ids)
    previous_monitor_ids = [
        monitor_id
        for monitor_id in _stable_monitor_ids(previous.get("monitorIds"))
        if not allowed_monitor_id_set or monitor_id in allowed_monitor_id_set
    ]
    return {
        "id": DEFAULT_RECORDING_PROFILE_ID,
        "schemaVersion": RECORDING_PROFILE_SCHEMA_VERSION,
        "kind": "recording-profile",
        "scope": "recording-profile-state-foundation",
        "name": str(previous.get("name") or "Default Recording Profile"),
        "monitorIds": previous_monitor_ids,
        "sourceIds": _stable_string_ids(previous.get("sourceIds")),
        "recordingMode": str(previous.get("recordingMode") or "manual-future-gated"),
        "storagePolicy": str(previous.get("storagePolicy") or "local-metadata-only"),
        "source": str(previous.get("source") or "recording-profile-state-foundation"),
        "dirty": False,
    }


def normalize_monitoring_hud_recording_profiles(payload=None, monitor_ids=None) -> dict[str, object]:
    source_payload = payload if isinstance(payload, dict) else {}
    allowed_monitor_ids = _stable_monitor_ids(monitor_ids or source_payload.get("monitorIds") or [])
    allowed_monitor_id_set = set(allowed_monitor_ids)
    has_recording_profiles_payload = "recordingProfiles" in source_payload
    raw_profiles = source_payload.get("recordingProfiles")
    if not isinstance(raw_profiles, dict):
        raw_profiles = {}
    profiles: dict[str, dict[str, object]] = {}
    for profile_key, raw_profile in raw_profiles.items():
        if not isinstance(raw_profile, dict):
            continue
        profile_id = str(raw_profile.get("id") or profile_key or "").strip()
        if not profile_id:
            continue
        raw_monitor_ids = _stable_monitor_ids(raw_profile.get("monitorIds") or [])
        monitor_members = [
            monitor_id
            for monitor_id in raw_monitor_ids
            if not allowed_monitor_id_set or monitor_id in allowed_monitor_id_set
        ]
        profiles[profile_id] = {
            "id": profile_id,
            "schemaVersion": RECORDING_PROFILE_SCHEMA_VERSION,
            "kind": "recording-profile",
            "scope": "recording-profile-state-foundation",
            "name": str(raw_profile.get("name") or "Recording Profile"),
            "monitorIds": monitor_members,
            "sourceIds": _stable_string_ids(raw_profile.get("sourceIds") or []),
            "recordingMode": str(raw_profile.get("recordingMode") or "manual-future-gated"),
            "storagePolicy": str(raw_profile.get("storagePolicy") or "local-metadata-only"),
            "source": str(raw_profile.get("source") or "persisted-recording-profile-state"),
            "dirty": bool(raw_profile.get("dirty")),
        }
    if not profiles or not has_recording_profiles_payload or DEFAULT_RECORDING_PROFILE_ID in raw_profiles:
        profiles[DEFAULT_RECORDING_PROFILE_ID] = default_recording_profile_state(
            profiles.get(DEFAULT_RECORDING_PROFILE_ID) or raw_profiles.get(DEFAULT_RECORDING_PROFILE_ID),
            allowed_monitor_ids,
        )
    active_profile_id = str(source_payload.get("activeRecordingProfileId") or "").strip()
    if active_profile_id not in profiles:
        active_profile_id = DEFAULT_RECORDING_PROFILE_ID if DEFAULT_RECORDING_PROFILE_ID in profiles else next(iter(profiles), "")
    default_profile = profiles.get(DEFAULT_RECORDING_PROFILE_ID)
    return {
        "recordingProfileSchemaVersion": RECORDING_PROFILE_SCHEMA_VERSION,
        "activeRecordingProfileId": active_profile_id,
        "recordingProfiles": profiles,
        "recordingProfileStateProof": {
            "schemaVersion": RECORDING_PROFILE_SCHEMA_VERSION,
            "activeProfileId": active_profile_id,
            "defaultProfileId": DEFAULT_RECORDING_PROFILE_ID,
            "defaultProfileMonitorIds": list(default_profile.get("monitorIds", []))
            if isinstance(default_profile, dict)
            else [],
            "defaultProfileSourceIds": list(default_profile.get("sourceIds", []))
            if isinstance(default_profile, dict)
            else [],
            "profileCount": len(profiles),
            "legacyMonitorCardsAutoRecorded": False,
            "monitorGroupBoundary": "monitor-groups-organize-configuration-only",
            "overlayProfileBoundary": "overlay-profiles-control-display-only",
            "trayRecordingBoundary": "tray-recording-controls-future-gated",
            "exportShareBoundary": "export-share-future-gated",
        },
    }


def default_monitoring_hud_state(source: str = "default") -> dict[str, object]:
    state = {
        "schemaVersion": 1,
        "featureEnabled": False,
        "dashboardVisible": False,
        "overlayDeferred": True,
        "source": source,
    }
    state.update(normalize_monitoring_hud_overlay_profiles({}))
    state.update(normalize_monitoring_hud_recording_profiles({}))
    return state


def load_monitoring_hud_state(event_logger=None) -> dict[str, object]:
    path = monitoring_hud_state_path()
    if not path.exists():
        state = default_monitoring_hud_state("missing")
        _emit(
            event_logger,
            "MONITORING_HUD_STATE_LOAD_READY|source=missing"
            f"|path={str(path)}|feature_enabled=false|dashboard_visible=false",
        )
        return state
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        state = default_monitoring_hud_state("invalid")
        _emit(
            event_logger,
            "MONITORING_HUD_STATE_LOAD_READY|source=invalid"
            f"|path={str(path)}|reason={type(exc).__name__}|feature_enabled=false|dashboard_visible=false",
        )
        return state
    if not isinstance(payload, dict):
        state = default_monitoring_hud_state("invalid_shape")
        _emit(
            event_logger,
            "MONITORING_HUD_STATE_LOAD_READY|source=invalid_shape"
            f"|path={str(path)}|feature_enabled=false|dashboard_visible=false",
        )
        return state
    state = default_monitoring_hud_state("persisted")
    state["featureEnabled"] = bool(payload.get("featureEnabled"))
    state["dashboardVisible"] = bool(payload.get("dashboardVisible"))
    state["overlayDeferred"] = payload.get("overlayDeferred", True) is not False
    state["updatedAt"] = str(payload.get("updatedAt") or "")
    state.update(normalize_monitoring_hud_overlay_profiles(payload, payload.get("monitorIds")))
    state.update(normalize_monitoring_hud_recording_profiles(payload, payload.get("monitorIds")))
    _emit(
        event_logger,
        "MONITORING_HUD_STATE_LOAD_READY|source=persisted"
        f"|path={str(path)}"
        f"|feature_enabled={str(bool(state['featureEnabled'])).lower()}"
        f"|dashboard_visible={str(bool(state['dashboardVisible'])).lower()}",
    )
    return state


def save_monitoring_hud_state(
    *,
    feature_enabled: bool,
    dashboard_visible: bool,
    event_logger=None,
    source: str = "runtime",
    monitor_ids=None,
    overlay_profiles=None,
    active_overlay_profile_id: str = DEFAULT_OVERLAY_PROFILE_ID,
    overlay_profile_default_deleted_by_user: bool = False,
    recording_profiles=None,
    active_recording_profile_id: str = DEFAULT_RECORDING_PROFILE_ID,
) -> bool:
    path = monitoring_hud_state_path()
    payload = {
        "schemaVersion": 1,
        "featureEnabled": bool(feature_enabled),
        "dashboardVisible": bool(dashboard_visible),
        "overlayDeferred": True,
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    overlay_payload = {
        "monitorIds": _stable_monitor_ids(monitor_ids or []),
        "overlayProfiles": overlay_profiles if isinstance(overlay_profiles, dict) else {},
        "activeOverlayProfileId": active_overlay_profile_id,
        "overlayProfileDefaultDeletedByUser": bool(overlay_profile_default_deleted_by_user),
    }
    payload.update(overlay_payload)
    payload.update(normalize_monitoring_hud_overlay_profiles(overlay_payload, overlay_payload["monitorIds"]))
    recording_payload = {
        "monitorIds": overlay_payload["monitorIds"],
        "recordingProfiles": recording_profiles if isinstance(recording_profiles, dict) else {},
        "activeRecordingProfileId": active_recording_profile_id,
    }
    payload.update(recording_payload)
    payload.update(normalize_monitoring_hud_recording_profiles(recording_payload, recording_payload["monitorIds"]))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_name(f"{path.name}.tmp")
        temp_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temp_path, path)
    except Exception as exc:
        _emit(
            event_logger,
            "MONITORING_HUD_STATE_SAVE_READY|status=fail"
            f"|source={source}|path={str(path)}|reason={type(exc).__name__}",
        )
        return False
    _emit(
        event_logger,
        "MONITORING_HUD_STATE_SAVE_READY|status=pass"
        f"|source={source}|path={str(path)}"
        f"|feature_enabled={str(bool(feature_enabled)).lower()}"
        f"|dashboard_visible={str(bool(dashboard_visible)).lower()}",
    )
    return True
