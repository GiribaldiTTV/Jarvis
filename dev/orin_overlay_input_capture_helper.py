import os
import sys
import time
from types import SimpleNamespace

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import desktop.desktop_renderer as renderer_mod
import desktop.hotkeys as hotkeys_mod
from desktop.interaction_overlay_model import CommandOverlayModel
from pynput import keyboard as pynput_keyboard


class _FakeRect:
    def __init__(self, x=0, y=0, width=1280, height=720):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def x(self):
        return self._x

    def y(self):
        return self._y

    def width(self):
        return self._width

    def height(self):
        return self._height


class _FakeTimer:
    def __init__(self):
        self.started_with = None

    def stop(self):
        self.started_with = None

    def start(self, duration_ms):
        self.started_with = duration_ms


class _FakeInputLine:
    def __init__(self):
        self.focused = False

    def hasFocus(self):
        return self.focused


class _FakePanel:
    def __init__(self):
        self.input_line = _FakeInputLine()
        self.active = False
        self.visible = False
        self.last_payload = None
        self.focus_after_show_calls = 0

    def render_payload(self, payload):
        self.last_payload = payload

    def show_for_geometry(self, *_args, **_kwargs):
        self.visible = True

    def focus_input_after_show(self):
        self.focus_after_show_calls += 1

    def focus_input(self, *_args, **_kwargs):
        self.active = True
        self.input_line.focused = True

    def isActiveWindow(self):
        return self.active

    def hide(self):
        self.visible = False

    def setFocus(self, *_args, **_kwargs):
        self.active = True


def _make_window():
    window = renderer_mod.DesktopRuntimeWindow.__new__(renderer_mod.DesktopRuntimeWindow)
    window.screen_ref = SimpleNamespace(availableGeometry=lambda: _FakeRect())
    window.compute_compact_geometry = lambda: _FakeRect()
    window._is_shutting_down = False
    window._command_model = CommandOverlayModel()
    window._command_panel = _FakePanel()
    window._result_close_timer = _FakeTimer()
    window._overlay_input_capture_until = 0.0
    window._overlay_local_input_engaged = False
    window._log_event = lambda *_args, **_kwargs: None
    window._apply_command_overlay_state = lambda: window._command_panel.render_payload(
        window._command_model.view_payload()
    )
    window._show_command_result = lambda kind, text: (
        window._command_model.show_result(kind, text),
        window._apply_command_overlay_state(),
    )
    return window


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


class _RecorderSignal:
    def __init__(self, sink, label):
        self._sink = sink
        self._label = label

    def emit(self, *args):
        self._sink.append((self._label, args))


class _FakeBus:
    def __init__(self):
        self.events = []
        self.shutdown_requested = _RecorderSignal(self.events, "shutdown")
        self.command_overlay_toggle_requested = _RecorderSignal(self.events, "toggle")
        self.command_overlay_text_requested = _RecorderSignal(self.events, "text")
        self.command_overlay_backspace_requested = _RecorderSignal(self.events, "backspace")
        self.command_overlay_submit_requested = _RecorderSignal(self.events, "submit")
        self.command_overlay_escape_requested = _RecorderSignal(self.events, "escape")


def _test_first_open_capture_allows_typing():
    window = _make_window()
    window.open_command_overlay()
    _assert(window._command_panel.focus_after_show_calls == 1, "open should request local input focus after show")
    _assert(window.overlay_needs_global_input_capture(), "capture should arm on first open")
    window.handle_overlay_text_requested("o")
    _assert(window._command_model.input_text == "o", "first typed character should reach the overlay")


def _test_active_panel_without_input_focus_still_uses_capture():
    window = _make_window()
    window.open_command_overlay()
    window._command_panel.active = True
    window._command_panel.input_line.focused = False
    _assert(
        window.overlay_needs_global_input_capture(),
        "entry capture should stay on when the panel is active but the input line still lacks focus",
    )


def _test_local_focus_clears_capture_and_stops_mirroring():
    window = _make_window()
    window.open_command_overlay()
    window._command_panel.active = True
    window._command_panel.input_line.focused = True
    window.handle_command_input_focus_acquired()
    _assert(
        not window.overlay_needs_global_input_capture(),
        "capture should stand down once the panel really owns active focused input",
    )
    window._command_panel.active = False
    window._command_panel.input_line.focused = False
    _assert(
        not window.overlay_needs_global_input_capture(),
        "capture should stay off after focus leaves a real local-input session",
    )
    before = window._command_model.input_text
    window.handle_overlay_text_requested("x")
    _assert(
        window._command_model.input_text == before,
        "typing elsewhere should no longer mirror into the overlay after focus loss",
    )


def _test_reopen_rearms_capture():
    window = _make_window()
    window.open_command_overlay()
    window._command_panel.active = True
    window._command_panel.input_line.focused = True
    window.handle_command_input_focus_acquired()
    window._command_panel.active = False
    window._command_panel.input_line.focused = False
    window.close_command_overlay()
    window.open_command_overlay()
    _assert(window.overlay_needs_global_input_capture(), "reopen should arm a fresh capture session")


def _test_ambiguous_choose_confirm_execute_path():
    window = _make_window()
    launches = []
    original_launch = renderer_mod.launch_command_action
    renderer_mod.launch_command_action = lambda action: launches.append((action.id, action.target))
    try:
        window.open_command_overlay()
        for char in "open nexus folder":
            window.handle_overlay_text_requested(char)
        window.handle_overlay_submit_requested()
        _assert(window._command_model.phase == "choose", "open nexus folder should enter choose state")
        window.handle_overlay_text_requested("2")
        _assert(window._command_model.phase == "confirm", "digit choice should enter confirm state")
        window.handle_overlay_submit_requested()
        _assert(
            launches and launches[0][0] == "open_jarvis_docs",
            "confirm path should launch the selected docs action",
        )
    finally:
        renderer_mod.launch_command_action = original_launch


def _test_capture_expiry_stands_down_fallback():
    window = _make_window()
    window.open_command_overlay()
    window._overlay_input_capture_until = time.monotonic() - 0.01
    _assert(not window.overlay_needs_global_input_capture(), "expired capture session should not keep forwarding keys")


def _test_line_edit_focus_methods_present():
    _assert(
        "focusInEvent" in renderer_mod.CommandInputLineEdit.__dict__,
        "the input line edit must override focusInEvent so local-focus engagement is tracked",
    )
    _assert(
        "focusOutEvent" in renderer_mod.CommandInputLineEdit.__dict__,
        "the input line edit must override focusOutEvent so local-focus loss can be observed",
    )


def _test_hotkey_launch_grace_bridges_open_gap():
    bus = _FakeBus()
    manager = hotkeys_mod.GlobalHotkeyManager(bus)
    manager.set_overlay_input_enabled_provider(lambda: False)

    manager._on_press(pynput_keyboard.Key.ctrl_l)
    manager._on_press(pynput_keyboard.Key.alt_l)
    manager._on_press(pynput_keyboard.Key.home)
    manager._on_release(pynput_keyboard.Key.home)
    manager._on_release(pynput_keyboard.Key.alt_l)
    manager._on_release(pynput_keyboard.Key.ctrl_l)
    manager._on_press(pynput_keyboard.KeyCode.from_char("o"))

    _assert(bus.events[0][0] == "toggle", "overlay hotkey should toggle first")
    _assert(
        ("text", ("o",)) in bus.events,
        "launch grace should forward immediate typing even before the provider is ready",
    )


def _test_hotkey_grace_expires_cleanly():
    bus = _FakeBus()
    manager = hotkeys_mod.GlobalHotkeyManager(bus)
    manager.set_overlay_input_enabled_provider(lambda: False)
    manager._overlay_launch_grace_until = time.monotonic() - 0.01
    manager._on_press(pynput_keyboard.KeyCode.from_char("x"))
    _assert(not bus.events, "expired hotkey grace should not keep forwarding stray typing")


def main():
    tests = [
        ("first-open capture", _test_first_open_capture_allows_typing),
        ("entry capture while input lacks focus", _test_active_panel_without_input_focus_still_uses_capture),
        ("local focus clears mirroring", _test_local_focus_clears_capture_and_stops_mirroring),
        ("reopen rearms capture", _test_reopen_rearms_capture),
        ("choose-confirm execute path", _test_ambiguous_choose_confirm_execute_path),
        ("capture expiry", _test_capture_expiry_stands_down_fallback),
        ("line edit focus methods", _test_line_edit_focus_methods_present),
        ("hotkey launch grace", _test_hotkey_launch_grace_bridges_open_gap),
        ("hotkey grace expiry", _test_hotkey_grace_expires_cleanly),
    ]

    for name, fn in tests:
        fn()
        print(f"PASS: {name}")

    print("OVERLAY INPUT HELPER: PASS")


if __name__ == "__main__":
    raise SystemExit(main())
