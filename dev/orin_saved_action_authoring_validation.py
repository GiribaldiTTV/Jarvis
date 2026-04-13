import json
import os
import sys
import tempfile
from pathlib import Path


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import desktop.saved_action_source as saved_action_source_mod
from desktop.saved_action_authoring import (
    SavedActionDraft,
    SavedActionDraftValidationError,
    SavedActionUnsafeSourceError,
    create_saved_action_from_draft,
    load_saved_action_draft_for_edit,
    prepare_saved_action_record_for_create,
    update_saved_action_from_draft,
)
from desktop.saved_action_source import DEFAULT_SAVED_ACTION_TEMPLATE


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


def _write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _test_create_persists_saved_action_and_preserves_template_fields():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        result = create_saved_action_from_draft(
            SavedActionDraft(
                title="Open Reports",
                target_kind="folder",
                target=r"C:\Reports",
                aliases=("show reports", "view reports"),
            ),
            source_path,
        )

        payload = json.loads(source_path.read_text(encoding="utf-8"))
        actions = payload.get("actions") or []

        _assert(source_path.is_file(), "successful authoring should persist the saved-action source file")
        _assert(payload.get("schema_version") == 1, "successful authoring should preserve schema version 1")
        _assert(
            payload.get("examples") == DEFAULT_SAVED_ACTION_TEMPLATE["examples"],
            "successful authoring should preserve starter examples in the saved-action source",
        )
        _assert(len(actions) == 1, "successful authoring should write one saved action")
        _assert(actions[0]["id"] == "open_reports", "successful authoring should generate a stable id from the title")
        _assert(
            len(result.catalog.saved_action_inventory.actions) == 1,
            "successful authoring should return a reloaded catalog that includes the new saved action",
        )
        _assert(
            result.catalog.actions[-1].id == "open_reports",
            "successful authoring should append the new saved action to the effective shared catalog",
        )


def _test_id_generation_avoids_existing_saved_ids():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _write_json(
            source_path,
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "open_reports",
                        "title": "Show Reports Hub",
                        "target_kind": "folder",
                        "target": r"C:\Reports\Hub",
                        "aliases": ["show reports hub"],
                    }
                ],
            },
        )

        record = prepare_saved_action_record_for_create(
            SavedActionDraft(
                title="Open Reports",
                target_kind="folder",
                target=r"C:\Reports",
                aliases=("view reports",),
            ),
            source_path,
        )

        _assert(
            record["id"] == "open_reports_2",
            "id generation should avoid collisions with existing saved-action ids",
        )


def _test_create_supports_all_persisted_target_kinds():
    with tempfile.TemporaryDirectory() as temp_dir:
        cases = [
            ("Open Notepad", "app", "notepad.exe"),
            ("Open Reports Folder", "folder", r"C:\Reports"),
            ("Open Reports File", "file", r"C:\Reports\weekly.txt"),
            ("Open Docs Site", "url", "https://example.com/docs"),
        ]

        for index, (title, target_kind, target) in enumerate(cases, start=1):
            source_path = Path(temp_dir) / f"saved_actions_{index}.json"
            result = create_saved_action_from_draft(
                SavedActionDraft(
                    title=title,
                    target_kind=target_kind,
                    target=target,
                    aliases=(f"alias {index}",),
                ),
                source_path,
            )

            payload = json.loads(source_path.read_text(encoding="utf-8"))
            action = (payload.get("actions") or [])[0]
            _assert(
                action["target_kind"] == target_kind,
                "authoring foundation should preserve supported persisted target kinds on write",
            )
            _assert(
                action["target"] == target,
                "authoring foundation should preserve the provided target on write",
            )
            _assert(
                result.catalog.actions[-1].target_kind == target_kind,
                "authoring foundation should reload the saved action into the catalog with the same target kind",
            )


def _test_invalid_inputs_are_rejected_before_write():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"

        try:
            create_saved_action_from_draft(
                SavedActionDraft(
                    title="Open Docs URL",
                    target_kind="url",
                    target="example.com/docs",
                    aliases=("view docs url",),
                ),
                source_path,
            )
        except SavedActionDraftValidationError:
            pass
        else:
            raise AssertionError("invalid url targets should be rejected before write")

        _assert(
            not source_path.exists(),
            "rejecting invalid input should not create or modify the saved-action source file",
        )


def _test_builtin_collisions_are_rejected_before_write():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"

        try:
            create_saved_action_from_draft(
                SavedActionDraft(
                    title="Open Windows Explorer",
                    target_kind="app",
                    target="explorer.exe",
                    aliases=("open explorer again",),
                ),
                source_path,
            )
        except SavedActionDraftValidationError:
            pass
        else:
            raise AssertionError("built-in collisions should be rejected before write")

        _assert(
            not source_path.exists(),
            "rejecting a built-in collision should not create or modify the saved-action source file",
        )


def _test_existing_saved_action_phrase_collisions_are_rejected_before_write():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _write_json(
            source_path,
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "show_reports_hub",
                        "title": "Show Reports Hub",
                        "target_kind": "folder",
                        "target": r"C:\Reports\Hub",
                        "aliases": ["open reports hub"],
                    }
                ],
            },
        )
        original_text = source_path.read_text(encoding="utf-8")

        try:
            create_saved_action_from_draft(
                SavedActionDraft(
                    title="Open Reports Hub",
                    target_kind="folder",
                    target=r"C:\Reports",
                    aliases=("view reports",),
                ),
                source_path,
            )
        except SavedActionDraftValidationError:
            pass
        else:
            raise AssertionError("existing saved-action phrase collisions should be rejected before write")

        _assert(
            source_path.read_text(encoding="utf-8") == original_text,
            "rejecting an existing saved-action collision should leave the source untouched",
        )


def _test_invalid_existing_saved_actions_block_write_completely():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        original_text = json.dumps(
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "open_reports",
                        "title": "Open Reports",
                        "target_kind": "folder",
                        "target": r"C:\Reports",
                        "aliases": ["show reports"],
                    },
                    {
                        "id": "open_reports_archive",
                        "title": "Open Reports Archive",
                        "target_kind": "folder",
                        "target": r"C:\Reports\Archive",
                        "aliases": ["show reports"],
                    },
                ],
            },
            indent=2,
        ) + "\n"
        source_path.write_text(original_text, encoding="utf-8")

        try:
            create_saved_action_from_draft(
                SavedActionDraft(
                    title="Open Tools",
                    target_kind="folder",
                    target=r"C:\Tools",
                    aliases=("view tools",),
                ),
                source_path,
            )
        except SavedActionUnsafeSourceError:
            pass
        else:
            raise AssertionError("invalid existing saved-action states should block writes completely")

        _assert(
            source_path.read_text(encoding="utf-8") == original_text,
            "blocking an unsafe source should leave the original saved-action source untouched",
        )


def _test_atomic_write_failure_preserves_existing_source():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        original_payload = {
            "schema_version": 1,
            "actions": [
                {
                    "id": "show_reports_hub",
                    "title": "Show Reports Hub",
                    "target_kind": "folder",
                    "target": r"C:\Reports\Hub",
                    "aliases": ["show reports hub"],
                }
            ],
        }
        _write_json(source_path, original_payload)
        original_text = source_path.read_text(encoding="utf-8")

        original_replace = saved_action_source_mod.os.replace
        saved_action_source_mod.os.replace = lambda *_args, **_kwargs: (_ for _ in ()).throw(
            OSError("replace failed")
        )
        try:
            try:
                create_saved_action_from_draft(
                    SavedActionDraft(
                        title="Open Reports",
                        target_kind="folder",
                        target=r"C:\Reports",
                        aliases=("view reports",),
                    ),
                    source_path,
                )
            except saved_action_source_mod.SavedActionSourceWriteBlocked:
                pass
            else:
                raise AssertionError("atomic replace failure should raise a safe write-blocked error")
        finally:
            saved_action_source_mod.os.replace = original_replace

        _assert(
            source_path.read_text(encoding="utf-8") == original_text,
            "atomic replace failure should preserve the original saved-action source contents",
        )
        _assert(
            not any(path.suffix == ".tmp" for path in source_path.parent.iterdir()),
            "atomic replace failure should not leave orphaned temp files behind",
        )


def _test_edit_loads_existing_saved_action_draft():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _write_json(
            source_path,
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "open_reports",
                        "title": "Open Reports",
                        "target_kind": "folder",
                        "target": r"C:\Reports",
                        "aliases": ["show reports", "view reports"],
                    }
                ],
            },
        )

        draft = load_saved_action_draft_for_edit("open_reports", source_path)

        _assert(draft.title == "Open Reports", "edit loading should preload the existing title")
        _assert(draft.target_kind == "folder", "edit loading should preload the existing target kind")
        _assert(draft.target == r"C:\Reports", "edit loading should preload the existing target")
        _assert(
            draft.aliases == ("show reports", "view reports"),
            "edit loading should preload the existing aliases",
        )


def _test_valid_edit_updates_existing_record_and_preserves_id():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _write_json(
            source_path,
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "open_reports",
                        "title": "Open Reports",
                        "target_kind": "folder",
                        "target": r"C:\Reports",
                        "aliases": ["show reports"],
                    }
                ],
            },
        )

        result = update_saved_action_from_draft(
            "open_reports",
            SavedActionDraft(
                title="Open Weekly Reports",
                target_kind="file",
                target=r"C:\Reports\weekly.txt",
                aliases=("weekly reports",),
            ),
            source_path,
        )

        payload = json.loads(source_path.read_text(encoding="utf-8"))
        actions = payload.get("actions") or []

        _assert(len(actions) == 1, "valid edit should preserve the number of saved actions")
        _assert(actions[0]["id"] == "open_reports", "valid edit should preserve the existing saved-action id")
        _assert(actions[0]["title"] == "Open Weekly Reports", "valid edit should update the title in place")
        _assert(actions[0]["target_kind"] == "file", "valid edit should update the target kind in place")
        _assert(
            actions[0]["target"] == r"C:\Reports\weekly.txt",
            "valid edit should update the target in place",
        )
        _assert(
            actions[0]["aliases"] == ["weekly reports"],
            "valid edit should replace aliases safely in place",
        )
        _assert(
            result.catalog.saved_action_inventory.actions[0].id == "open_reports",
            "valid edit should reload the updated action without changing its identity",
        )


def _test_edit_rejects_builtin_collisions_without_writing():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _write_json(
            source_path,
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "open_reports",
                        "title": "Open Reports",
                        "target_kind": "folder",
                        "target": r"C:\Reports",
                        "aliases": ["show reports"],
                    }
                ],
            },
        )
        original_text = source_path.read_text(encoding="utf-8")

        try:
            update_saved_action_from_draft(
                "open_reports",
                SavedActionDraft(
                    title="Open Windows Explorer",
                    target_kind="app",
                    target="explorer.exe",
                    aliases=("show explorer",),
                ),
                source_path,
            )
        except SavedActionDraftValidationError:
            pass
        else:
            raise AssertionError("editing into a built-in collision should be rejected")

        _assert(
            source_path.read_text(encoding="utf-8") == original_text,
            "rejecting a built-in collision during edit should leave the source untouched",
        )


def _test_edit_rejects_other_saved_action_collisions_without_self_collision():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _write_json(
            source_path,
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "open_reports",
                        "title": "Open Reports",
                        "target_kind": "folder",
                        "target": r"C:\Reports",
                        "aliases": ["show reports"],
                    },
                    {
                        "id": "open_docs",
                        "title": "Open Knowledge Base",
                        "target_kind": "url",
                        "target": "https://example.com/knowledge",
                        "aliases": ["show knowledge base"],
                    },
                ],
            },
        )
        original_text = source_path.read_text(encoding="utf-8")

        result = update_saved_action_from_draft(
            "open_reports",
            SavedActionDraft(
                title="Open Reports",
                target_kind="folder",
                target=r"C:\Reports\Archive",
                aliases=("show reports",),
            ),
            source_path,
        )
        _assert(
            result.record["id"] == "open_reports",
            "editing a record without changing its phrases should not self-collide",
        )

        try:
            update_saved_action_from_draft(
                "open_reports",
                SavedActionDraft(
                    title="Open Knowledge Base",
                    target_kind="folder",
                    target=r"C:\Reports",
                    aliases=("view reports",),
                ),
                source_path,
            )
        except SavedActionDraftValidationError:
            pass
        else:
            raise AssertionError("editing into another saved-action phrase should be rejected")

        _assert(
            json.loads(source_path.read_text(encoding="utf-8"))["actions"][0]["id"] == "open_reports",
            "edit collisions should not change the saved-action identity",
        )
        _assert(
            json.loads(source_path.read_text(encoding="utf-8"))["actions"][1]["id"] == "open_docs",
            "edit collisions should not disturb other saved actions",
        )


def _test_invalid_edit_input_is_rejected_before_write():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _write_json(
            source_path,
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "open_docs",
                        "title": "Open Knowledge Base",
                        "target_kind": "url",
                        "target": "https://example.com/knowledge",
                        "aliases": ["show knowledge base"],
                    }
                ],
            },
        )
        original_text = source_path.read_text(encoding="utf-8")

        try:
            update_saved_action_from_draft(
                "open_docs",
                SavedActionDraft(
                    title="Open Knowledge Base",
                    target_kind="url",
                    target="example.com/docs",
                    aliases=("show knowledge base",),
                ),
                source_path,
            )
        except SavedActionDraftValidationError:
            pass
        else:
            raise AssertionError("invalid edit inputs should be rejected before write")

        _assert(
            source_path.read_text(encoding="utf-8") == original_text,
            "rejecting invalid edit input should leave the saved-action source untouched",
        )


def _test_invalid_existing_saved_actions_block_edit_completely():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        original_text = json.dumps(
            {
                "schema_version": 1,
                "actions": [
                    {
                        "id": "open_reports",
                        "title": "Open Reports",
                        "target_kind": "folder",
                        "target": r"C:\Reports",
                        "aliases": ["show reports"],
                    },
                    {
                        "id": "open_reports_archive",
                        "title": "Open Reports Archive",
                        "target_kind": "folder",
                        "target": r"C:\Reports\Archive",
                        "aliases": ["show reports"],
                    },
                ],
            },
            indent=2,
        ) + "\n"
        source_path.write_text(original_text, encoding="utf-8")

        try:
            update_saved_action_from_draft(
                "open_reports",
                SavedActionDraft(
                    title="Open Reports Folder",
                    target_kind="folder",
                    target=r"C:\Reports",
                    aliases=("view reports",),
                ),
                source_path,
            )
        except SavedActionUnsafeSourceError:
            pass
        else:
            raise AssertionError("invalid existing saved-action states should block edits completely")

        _assert(
            source_path.read_text(encoding="utf-8") == original_text,
            "blocking unsafe edit sources should leave the original saved-action source untouched",
        )


def main():
    tests = [
        ("create persists saved action and preserves template fields", _test_create_persists_saved_action_and_preserves_template_fields),
        ("id generation avoids existing saved ids", _test_id_generation_avoids_existing_saved_ids),
        ("create supports all persisted target kinds", _test_create_supports_all_persisted_target_kinds),
        ("invalid inputs rejected before write", _test_invalid_inputs_are_rejected_before_write),
        ("built-in collisions rejected before write", _test_builtin_collisions_are_rejected_before_write),
        ("existing saved-action collisions rejected before write", _test_existing_saved_action_phrase_collisions_are_rejected_before_write),
        ("invalid existing saved actions block write", _test_invalid_existing_saved_actions_block_write_completely),
        ("atomic write failure preserves existing source", _test_atomic_write_failure_preserves_existing_source),
        ("edit loads existing saved action draft", _test_edit_loads_existing_saved_action_draft),
        ("valid edit updates existing record and preserves id", _test_valid_edit_updates_existing_record_and_preserves_id),
        ("edit rejects built-in collisions without write", _test_edit_rejects_builtin_collisions_without_writing),
        ("edit rejects other saved-action collisions without self-collision", _test_edit_rejects_other_saved_action_collisions_without_self_collision),
        ("invalid edit input is rejected before write", _test_invalid_edit_input_is_rejected_before_write),
        ("invalid existing saved actions block edit", _test_invalid_existing_saved_actions_block_edit_completely),
    ]

    for name, fn in tests:
        fn()
        print(f"PASS: {name}")

    print("SAVED ACTION AUTHORING VALIDATION: PASS")


if __name__ == "__main__":
    raise SystemExit(main())
