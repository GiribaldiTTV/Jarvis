import datetime
import json
import os
from pathlib import Path


MONITORING_HUD_STATE_ENV = "NEXUS_MONITORING_HUD_STATE_PATH"
MONITORING_HUD_STATE_FILENAME = "monitoring_hud_state.json"


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


def default_monitoring_hud_state(source: str = "default") -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "featureEnabled": False,
        "dashboardVisible": False,
        "overlayDeferred": True,
        "source": source,
    }


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
) -> bool:
    path = monitoring_hud_state_path()
    payload = {
        "schemaVersion": 1,
        "featureEnabled": bool(feature_enabled),
        "dashboardVisible": bool(dashboard_visible),
        "overlayDeferred": True,
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
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
