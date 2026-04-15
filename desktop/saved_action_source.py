from copy import deepcopy
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_SAVED_ACTION_FILENAME = "saved_actions.json"
DEFAULT_SAVED_ACTION_TEMPLATE = {
    "schema_version": 1,
    "actions": [],
    "groups": [],
    "examples": [
        {
            "id": "open_notepad",
            "title": "Open Notepad",
            "target_kind": "app",
            "target": "notepad.exe",
            "aliases": ["open notepad"],
        },
        {
            "id": "open_downloads",
            "title": "Open Downloads",
            "target_kind": "folder",
            "target": r"C:\Users\YourName\Downloads",
            "aliases": ["open downloads", "show downloads"],
        },
        {
            "id": "open_nexus_docs_site",
            "title": "Open Nexus Docs Site",
            "target_kind": "url",
            "target": "https://example.com/docs",
            "aliases": ["open nexus docs site", "open docs site"],
        },
    ],
}

_GROUPS_UNSET = object()


@dataclass(frozen=True)
class SavedActionSourcePayload:
    path: Path
    actions: tuple[dict[str, Any], ...]
    groups: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class SavedActionSourceInspection:
    path: Path
    status: str
    actions: tuple[dict[str, Any], ...] = ()
    groups: tuple[dict[str, Any], ...] = ()


class SavedActionSourceError(ValueError):
    pass


class SavedActionSourceWriteBlocked(SavedActionSourceError):
    pass


def resolve_default_saved_action_source_path() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
    if local_app_data:
        return Path(local_app_data) / "Nexus Desktop AI" / DEFAULT_SAVED_ACTION_FILENAME

    return Path.home() / "AppData" / "Local" / "Nexus Desktop AI" / DEFAULT_SAVED_ACTION_FILENAME


def _resolve_saved_action_source_path(
    source_path: str | os.PathLike[str] | None = None,
) -> Path:
    return (
        Path(source_path)
        if source_path is not None
        else resolve_default_saved_action_source_path()
    )


def _default_saved_action_source_text() -> str:
    return json.dumps(DEFAULT_SAVED_ACTION_TEMPLATE, indent=2) + "\n"


def _load_saved_action_source_document_from_path(path: Path) -> dict[str, Any]:
    try:
        raw_text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise SavedActionSourceWriteBlocked(
            "Saved actions source is unavailable because the source file could not be read cleanly."
        ) from exc

    if not raw_text.strip():
        raise SavedActionSourceWriteBlocked(
            "Saved actions source is unavailable because the source file could not be read cleanly."
        )

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise SavedActionSourceWriteBlocked(
            "Saved actions source is unavailable because the source file could not be read cleanly."
        ) from exc

    if not isinstance(payload, dict):
        raise SavedActionSourceWriteBlocked(
            "Saved actions source is unavailable because the source file could not be read cleanly."
        )

    actions = payload.get("actions")
    if not isinstance(actions, list):
        raise SavedActionSourceWriteBlocked(
            "Saved actions source is unavailable because the source file could not be read cleanly."
        )

    groups = payload.get("groups", [])
    if not isinstance(groups, list):
        raise SavedActionSourceWriteBlocked(
            "Saved actions source is unavailable because the source file could not be read cleanly."
        )

    return payload


def _coerce_saved_action_source_actions_for_write(
    actions: Any,
) -> tuple[dict[str, Any], ...]:
    if not isinstance(actions, (list, tuple)):
        raise SavedActionSourceError("Saved action source writes require a list of action objects.")

    normalized_actions: list[dict[str, Any]] = []
    for action in actions:
        if not isinstance(action, dict):
            raise SavedActionSourceError("Saved action source writes require action objects.")
        normalized_actions.append(deepcopy(action))

    return tuple(normalized_actions)


def _coerce_saved_action_source_groups_for_write(
    groups: Any,
) -> tuple[dict[str, Any], ...]:
    if not isinstance(groups, (list, tuple)):
        raise SavedActionSourceError("Saved action source writes require a list of group objects.")

    normalized_groups: list[dict[str, Any]] = []
    for group in groups:
        if not isinstance(group, dict):
            raise SavedActionSourceError("Saved action source writes require group objects.")
        normalized_groups.append(deepcopy(group))

    return tuple(normalized_groups)


def prepare_saved_action_source_document_for_write(
    actions: Any,
    source_path: str | os.PathLike[str] | None = None,
    *,
    groups: Any = _GROUPS_UNSET,
) -> tuple[Path, dict[str, Any]]:
    path = _resolve_saved_action_source_path(source_path)
    normalized_actions = _coerce_saved_action_source_actions_for_write(actions)
    normalized_groups = (
        _coerce_saved_action_source_groups_for_write(groups)
        if groups is not _GROUPS_UNSET
        else _GROUPS_UNSET
    )

    try:
        exists = path.exists()
        is_file = path.is_file() if exists else False
    except OSError as exc:
        raise SavedActionSourceWriteBlocked(
            "Saved actions source is unavailable because the source file could not be read cleanly."
        ) from exc

    if exists and not is_file:
        raise SavedActionSourceWriteBlocked(
            "Saved actions source is unavailable because the source path is not a file."
        )

    if exists:
        payload = _load_saved_action_source_document_from_path(path)
    else:
        payload = deepcopy(DEFAULT_SAVED_ACTION_TEMPLATE)

    payload["actions"] = list(normalized_actions)
    if normalized_groups is not _GROUPS_UNSET:
        payload["groups"] = list(normalized_groups)
    elif "groups" not in payload:
        payload["groups"] = []
    if "schema_version" not in payload:
        payload["schema_version"] = DEFAULT_SAVED_ACTION_TEMPLATE["schema_version"]

    try:
        json.dumps(payload, indent=2)
    except (TypeError, ValueError) as exc:
        raise SavedActionSourceError(
            "Saved action source writes require JSON-serializable action and group objects."
        ) from exc

    return path, payload


def write_saved_action_source(
    actions: Any,
    source_path: str | os.PathLike[str] | None = None,
    *,
    groups: Any = _GROUPS_UNSET,
) -> SavedActionSourcePayload:
    path, payload = prepare_saved_action_source_document_for_write(
        actions,
        source_path,
        groups=groups,
    )
    serialized = json.dumps(payload, indent=2) + "\n"

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SavedActionSourceWriteBlocked(
            "Saved actions source could not be prepared for writing."
        ) from exc

    temp_fd = None
    temp_path = None
    try:
        temp_fd, temp_name = tempfile.mkstemp(
            prefix=f".{path.stem}_",
            suffix=".tmp",
            dir=str(path.parent),
        )
        temp_path = Path(temp_name)
        with os.fdopen(temp_fd, "w", encoding="utf-8", newline="\n") as handle:
            temp_fd = None
            handle.write(serialized)
            handle.flush()
        os.replace(temp_path, path)
    except OSError as exc:
        raise SavedActionSourceWriteBlocked(
            "Saved actions source could not be written safely."
        ) from exc
    finally:
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except OSError:
                pass
        if temp_path is not None and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass

    return SavedActionSourcePayload(
        path=path,
        actions=tuple(payload.get("actions", ())),
        groups=tuple(payload.get("groups", ())),
    )


def ensure_saved_action_source_bootstrap(
    source_path: str | os.PathLike[str] | None = None,
) -> Path | None:
    path = _resolve_saved_action_source_path(source_path)

    try:
        if path.exists():
            return path if path.is_file() else None
    except OSError:
        return None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_default_saved_action_source_text(), encoding="utf-8")
    except OSError:
        return None

    return path


def load_saved_action_source(
    source_path: str | os.PathLike[str] | None = None,
) -> SavedActionSourcePayload | None:
    inspection = inspect_saved_action_source(source_path)
    if inspection.status != "loaded":
        return None

    return SavedActionSourcePayload(
        path=inspection.path,
        actions=inspection.actions,
        groups=inspection.groups,
    )


def inspect_saved_action_source(
    source_path: str | os.PathLike[str] | None = None,
) -> SavedActionSourceInspection:
    path = _resolve_saved_action_source_path(source_path)

    # Bootstrap only the default runtime source so users get an explicit starter
    # file without widening fallback behavior for custom or validation-only paths.
    if source_path is None:
        bootstrapped_path = ensure_saved_action_source_bootstrap()
        if bootstrapped_path is not None:
            path = bootstrapped_path

    try:
        if not path.exists() or not path.is_file():
            return SavedActionSourceInspection(path=path, status="missing")
    except OSError:
        return SavedActionSourceInspection(path=path, status="missing")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return SavedActionSourceInspection(path=path, status="invalid_source")

    if not raw_text.strip():
        return SavedActionSourceInspection(path=path, status="invalid_source")

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return SavedActionSourceInspection(path=path, status="invalid_source")

    if not isinstance(payload, dict):
        return SavedActionSourceInspection(path=path, status="invalid_source")

    actions = payload.get("actions")
    if not isinstance(actions, list):
        return SavedActionSourceInspection(path=path, status="invalid_source")

    groups = payload.get("groups", [])
    if not isinstance(groups, list):
        return SavedActionSourceInspection(path=path, status="invalid_source")

    if not actions and not groups:
        return SavedActionSourceInspection(path=path, status="template_only")

    return SavedActionSourceInspection(
        path=path,
        status="loaded",
        actions=tuple(actions),
        groups=tuple(groups),
    )
