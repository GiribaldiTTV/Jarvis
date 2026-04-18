import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace


CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import desktop.desktop_renderer as renderer_mod
from desktop.interaction_overlay_model import CommandOverlayModel
from desktop.saved_action_authoring import (
    CallableGroupDraft,
    SavedActionDraft,
    create_callable_group_from_draft,
    create_saved_action_from_draft,
)
from desktop.shared_action_model import (
    CommandGroup,
    build_default_command_action_catalog,
    execute_command_group,
)


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


def _make_group(source_path: Path):
    create_saved_action_from_draft(
        SavedActionDraft(
            title="Open Reports",
            target_kind="folder",
            target=r"C:\Reports",
            aliases=("show reports",),
        ),
        source_path,
    )
    create_saved_action_from_draft(
        SavedActionDraft(
            title="Open Notes",
            target_kind="app",
            target="notepad.exe",
            aliases=("notes",),
        ),
        source_path,
    )
    create_callable_group_from_draft(
        CallableGroupDraft(
            title="Workspace Tools",
            aliases=("workspace tools",),
            member_action_ids=("open_reports", "open_saved_actions_folder", "open_notes"),
        ),
        source_path,
    )
    catalog = build_default_command_action_catalog(source_path)
    group = catalog.resolve_group("workspace tools")
    _assert(group is not None, "callable-group execution validation should resolve the created group")
    return group


def _make_window():
    window = SimpleNamespace(_events=[])
    window._log_event = lambda event: window._events.append(event)
    window._emit_group_execution_marker = lambda marker_name, fields: renderer_mod.DesktopRuntimeWindow._emit_group_execution_marker(
        window,
        marker_name,
        fields,
    )
    return window


def _make_dispatch_window(source_path: Path):
    window = SimpleNamespace(_events=[], _shown_results=[], _cleared_launch_failure_action_ids=[])
    window._command_model = CommandOverlayModel(action_catalog=build_default_command_action_catalog(source_path))
    window._command_model.open(arm_input=True)
    window._overlay_local_input_engaged = False
    window._foreground_window_snapshot = lambda: {"hwnd": 0, "class_name": "", "title": ""}
    window._trace_overlay = lambda *_args, **_kwargs: None
    window._apply_command_overlay_state = lambda: None
    window._refresh_overlay_input_capture = lambda *_args, **_kwargs: None
    window._log_event = lambda event: window._events.append(event)
    window._prepare_recoverable_launch_failure_report = lambda _action: None

    def _show_command_result(status_kind: str, status_text: str, close_delay_ms: int = 1200):
        del close_delay_ms
        window._shown_results.append((status_kind, status_text))
        window._command_model.show_result(status_kind, status_text)

    def _clear_launch_failure_tracking(action_id: str):
        window._cleared_launch_failure_action_ids.append(action_id)

    window._show_command_result = _show_command_result
    window._clear_launch_failure_tracking = _clear_launch_failure_tracking
    window._emit_group_execution_marker = lambda marker_name, fields: renderer_mod.DesktopRuntimeWindow._emit_group_execution_marker(
        window,
        marker_name,
        fields,
    )
    window._execute_callable_group = lambda group: renderer_mod.DesktopRuntimeWindow._execute_callable_group(window, group)
    return window


def _group_events(window):
    return [event for event in window._events if event.startswith("RENDERER_MAIN|GROUP_EXECUTION_")]


def _parse_group_event(event: str):
    parts = event.split("|")
    marker_name = parts[1] if len(parts) > 1 else ""
    fields = {}
    for part in parts[2:]:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        fields[key] = value
    return marker_name, fields


def _test_group_execution_runs_in_persisted_order_with_gap_free_markers():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        group = _make_group(source_path)
        window = _make_window()

        original_launch = renderer_mod.launch_command_action
        launched_action_ids = []
        renderer_mod.launch_command_action = lambda action: launched_action_ids.append(action.id)
        try:
            result = renderer_mod.DesktopRuntimeWindow._execute_callable_group(window, group)
        finally:
            renderer_mod.launch_command_action = original_launch

        _assert(result.succeeded, "group execution should succeed when every step launcher succeeds")
        _assert(
            result.completed_action_ids == group.member_action_ids,
            "successful group execution should report every completed action id in persisted stored order",
        )
        _assert(
            launched_action_ids == list(group.member_action_ids),
            "group execution should launch member actions exactly in persisted stored order",
        )

        parsed_events = [_parse_group_event(event) for event in _group_events(window)]
        marker_names = [marker_name for marker_name, _fields in parsed_events]
        _assert(
            marker_names
            == [
                "GROUP_EXECUTION_STARTED",
                "GROUP_EXECUTION_STEP_STARTED",
                "GROUP_EXECUTION_STEP_SUCCEEDED",
                "GROUP_EXECUTION_STEP_STARTED",
                "GROUP_EXECUTION_STEP_SUCCEEDED",
                "GROUP_EXECUTION_STEP_STARTED",
                "GROUP_EXECUTION_STEP_SUCCEEDED",
                "GROUP_EXECUTION_COMPLETED",
            ],
            "group execution should emit deterministic start, per-step, and completion markers",
        )

        started_steps = [fields for marker_name, fields in parsed_events if marker_name == "GROUP_EXECUTION_STEP_STARTED"]
        completed_steps = [fields for marker_name, fields in parsed_events if marker_name == "GROUP_EXECUTION_STEP_SUCCEEDED"]
        _assert(
            [int(fields["step_index"]) for fields in started_steps] == [1, 2, 3],
            "step-start markers should advance monotonically without gaps",
        )
        _assert(
            [fields["action_id"] for fields in started_steps] == list(group.member_action_ids),
            "step-start markers should reflect persisted member ids in order",
        )
        _assert(
            [int(fields["step_index"]) for fields in completed_steps] == [1, 2, 3],
            "step-success markers should advance monotonically without gaps",
        )


def _test_group_execution_stops_on_first_failure_and_reports_terminal_failure():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        group = _make_group(source_path)
        window = _make_window()

        original_launch = renderer_mod.launch_command_action
        launched_action_ids = []

        def _failing_launcher(action):
            launched_action_ids.append(action.id)
            if action.id == "open_saved_actions_folder":
                raise RuntimeError("expected failure")

        renderer_mod.launch_command_action = _failing_launcher
        try:
            result = renderer_mod.DesktopRuntimeWindow._execute_callable_group(window, group)
        finally:
            renderer_mod.launch_command_action = original_launch

        _assert(not result.succeeded, "group execution should fail when a member launcher raises")
        _assert(
            result.completed_action_ids == ("open_reports",),
            "group execution should report only the successfully completed prefix before failure",
        )
        _assert(
            result.failed_action_id == "open_saved_actions_folder" and result.failed_step_index == 2,
            "group execution should surface the exact failed member id and step index",
        )
        _assert(
            launched_action_ids == ["open_reports", "open_saved_actions_folder"],
            "group execution should stop immediately after the first failed member",
        )

        parsed_events = [_parse_group_event(event) for event in _group_events(window)]
        marker_names = [marker_name for marker_name, _fields in parsed_events]
        _assert(
            marker_names
            == [
                "GROUP_EXECUTION_STARTED",
                "GROUP_EXECUTION_STEP_STARTED",
                "GROUP_EXECUTION_STEP_SUCCEEDED",
                "GROUP_EXECUTION_STEP_STARTED",
                "GROUP_EXECUTION_STEP_FAILED",
                "GROUP_EXECUTION_FAILED",
            ],
            "group execution should emit a terminal failure marker immediately after the failed step",
        )
        started_steps = [fields for marker_name, fields in parsed_events if marker_name == "GROUP_EXECUTION_STEP_STARTED"]
        _assert(
            [int(fields["step_index"]) for fields in started_steps] == [1, 2],
            "group execution should not emit later step markers after the first failure",
        )


def _test_group_execution_rejects_ambiguous_member_order():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        group = _make_group(source_path)
        ambiguous_group = CommandGroup(
            id="ambiguous_workspace_tools",
            title="Ambiguous Workspace Tools",
            aliases=("ambiguous workspace tools",),
            member_action_ids=("open_saved_actions_folder", "open_reports"),
            member_actions=(
                group.member_actions[0],
                group.member_actions[1],
            ),
        )

        try:
            execute_command_group(
                ambiguous_group,
                action_launcher=lambda _action: None,
            )
        except ValueError as exc:
            _assert(
                "ambiguous" in str(exc).casefold(),
                "ambiguous member ordering should fail with an explicit ambiguity error",
            )
        else:
            raise AssertionError("group execution should reject ambiguous member ordering before any launch")


def _test_dispatch_routes_group_execution_without_double_launch():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        group = _make_group(source_path)
        window = _make_dispatch_window(source_path)

        original_launch = renderer_mod.launch_command_action
        launched_action_ids = []
        renderer_mod.launch_command_action = lambda action: launched_action_ids.append(action.id)
        try:
            window._command_model.set_input_text("workspace tools")
            renderer_mod.DesktopRuntimeWindow.handle_command_submit(window)
            match_ids = [match.get("id") for match in window._command_model.view_payload().get("ambiguous_matches") or []]
            selected_index = match_ids.index("open_saved_actions_folder")
            renderer_mod.DesktopRuntimeWindow.handle_ambiguous_match_selected(window, selected_index)
            renderer_mod.DesktopRuntimeWindow.handle_command_submit(window)
        finally:
            renderer_mod.launch_command_action = original_launch

        _assert(
            launched_action_ids == list(group.member_action_ids),
            "dispatch integration should route group execution through the deterministic helper in persisted order",
        )
        _assert(
            window._shown_results[-1][0] == "launch_requested",
            "successful group dispatch should preserve the existing launch-requested result surface",
        )
        _assert(
            any("COMMAND_GROUP_EXECUTION_COMPLETED|group_id=workspace_tools|step_count=3" in event for event in window._events),
            "dispatch integration should log explicit group completion after deterministic execution",
        )
        _assert(
            not any("COMMAND_LAUNCH_REQUEST_SENT|action_id=open_saved_actions_folder" in event for event in window._events),
            "group dispatch should not fall back into the single-action launch path after helper execution",
        )
        parsed_group_events = [_parse_group_event(event) for event in _group_events(window)]
        _assert(
            [marker_name for marker_name, _fields in parsed_group_events][-1] == "GROUP_EXECUTION_COMPLETED",
            "group dispatch should emit terminal group markers only through the deterministic helper",
        )


def _test_dispatch_preserves_single_action_execution_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _make_group(source_path)
        window = _make_dispatch_window(source_path)

        original_launch = renderer_mod.launch_command_action
        launched_action_ids = []
        renderer_mod.launch_command_action = lambda action: launched_action_ids.append(action.id)
        try:
            window._command_model.set_input_text("show reports")
            renderer_mod.DesktopRuntimeWindow.handle_command_submit(window)
            renderer_mod.DesktopRuntimeWindow.handle_command_submit(window)
        finally:
            renderer_mod.launch_command_action = original_launch

        _assert(
            launched_action_ids == ["open_reports"],
            "single-action dispatch should still execute through the original launch path only once",
        )
        _assert(
            any("COMMAND_LAUNCH_REQUEST_SENT|action_id=open_reports" in event for event in window._events),
            "single-action dispatch should preserve the existing launch-request marker",
        )
        _assert(
            not _group_events(window),
            "single-action dispatch should not emit group execution markers",
        )


def _test_dispatch_group_failure_stops_without_later_execution():
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / "saved_actions.json"
        _make_group(source_path)
        window = _make_dispatch_window(source_path)

        original_launch = renderer_mod.launch_command_action
        launched_action_ids = []

        def _failing_launcher(action):
            launched_action_ids.append(action.id)
            if action.id == "open_saved_actions_folder":
                raise RuntimeError("expected failure")

        renderer_mod.launch_command_action = _failing_launcher
        try:
            window._command_model.set_input_text("workspace tools")
            renderer_mod.DesktopRuntimeWindow.handle_command_submit(window)
            renderer_mod.DesktopRuntimeWindow.handle_ambiguous_match_selected(window, 0)
            renderer_mod.DesktopRuntimeWindow.handle_command_submit(window)
        finally:
            renderer_mod.launch_command_action = original_launch

        _assert(
            launched_action_ids == ["open_reports", "open_saved_actions_folder"],
            "group dispatch should stop immediately after the first failed member and never launch later steps",
        )
        _assert(
            window._shown_results[-1][0] == "launch_failed",
            "group dispatch failure should preserve the existing launch-failed result surface",
        )
        _assert(
            any("GROUP_EXECUTION_STEP_FAILED" in event for event in _group_events(window))
            and any("GROUP_EXECUTION_FAILED" in event for event in _group_events(window)),
            "group dispatch failure should emit deterministic step-failure and terminal-failure markers",
        )
        _assert(
            not any("COMMAND_LAUNCH_REQUEST_SENT|action_id=" in event for event in window._events),
            "failed group dispatch should not emit single-action launch success markers",
        )


def main():
    tests = [
        (
            "group execution runs in persisted order with gap-free markers",
            _test_group_execution_runs_in_persisted_order_with_gap_free_markers,
        ),
        (
            "group execution stops on first failure",
            _test_group_execution_stops_on_first_failure_and_reports_terminal_failure,
        ),
        (
            "group execution rejects ambiguous member order",
            _test_group_execution_rejects_ambiguous_member_order,
        ),
        (
            "dispatch routes group execution without double launch",
            _test_dispatch_routes_group_execution_without_double_launch,
        ),
        (
            "dispatch preserves single-action execution path",
            _test_dispatch_preserves_single_action_execution_path,
        ),
        (
            "dispatch group failure stops without later execution",
            _test_dispatch_group_failure_stops_without_later_execution,
        ),
    ]

    for name, fn in tests:
        fn()
        print(f"PASS: {name}")

    print("CALLABLE GROUP EXECUTION VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
