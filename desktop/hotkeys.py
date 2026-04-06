import os
from PySide6.QtCore import QObject, Signal
from pynput import keyboard as pynput_keyboard


class ShutdownBus(QObject):
    shutdown_requested = Signal()
    command_overlay_toggle_requested = Signal()


class GlobalHotkeyManager:
    def __init__(self, bus: ShutdownBus):
        self.bus = bus
        self._listener = None
        self._pressed = set()
        self._shutdown_fired = False
        self._overlay_toggle_fired = False
        self._overlay_digit_chars = {"1"}
        self._overlay_digit_vks = {49}
        self._shutdown_digit_chars = {"2"}
        self._shutdown_digit_vks = {50}

    def start(self) -> None:
        if self._listener is not None:
            return
        self._listener = pynput_keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self._listener.start()

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
            self._listener = None
        self._pressed.clear()
        self._shutdown_fired = False
        self._overlay_toggle_fired = False

    def force_kill(self) -> None:
        os._exit(0)

    def _ctrl_down(self) -> bool:
        return pynput_keyboard.Key.ctrl_l in self._pressed or pynput_keyboard.Key.ctrl_r in self._pressed

    def _alt_down(self) -> bool:
        return (
            pynput_keyboard.Key.alt_l in self._pressed
            or pynput_keyboard.Key.alt_r in self._pressed
            or pynput_keyboard.Key.alt_gr in self._pressed
        )

    def _key_char(self, key):
        char = getattr(key, "char", None)
        if isinstance(char, str):
            return char.lower()
        return None

    def _key_vk(self, key):
        return getattr(key, "vk", None)

    def _key_matches_overlay_trigger(self, key) -> bool:
        if key == pynput_keyboard.Key.home:
            return True
        return self._key_char(key) in self._overlay_digit_chars or self._key_vk(key) in self._overlay_digit_vks

    def _key_matches_shutdown_trigger(self, key) -> bool:
        if key == pynput_keyboard.Key.end:
            return True
        return self._key_char(key) in self._shutdown_digit_chars or self._key_vk(key) in self._shutdown_digit_vks

    def _overlay_key_down(self) -> bool:
        return any(self._key_matches_overlay_trigger(key) for key in self._pressed)

    def _shutdown_key_down(self) -> bool:
        return any(self._key_matches_shutdown_trigger(key) for key in self._pressed)

    def _on_press(self, key) -> None:
        self._pressed.add(key)
        ctrl_down = self._ctrl_down()
        alt_down = self._alt_down()
        shutdown_down = self._key_matches_shutdown_trigger(key)
        overlay_down = self._key_matches_overlay_trigger(key)

        if ctrl_down and alt_down and shutdown_down and not self._shutdown_fired:
            self._shutdown_fired = True
            self.bus.shutdown_requested.emit()
            return

        if ctrl_down and alt_down and overlay_down and not self._overlay_toggle_fired:
            self._overlay_toggle_fired = True
            self.bus.command_overlay_toggle_requested.emit()
            return

    def _on_release(self, key) -> None:
        self._pressed.discard(key)
        if (
            self._key_matches_shutdown_trigger(key)
            or self._key_matches_overlay_trigger(key)
            or key in (
                pynput_keyboard.Key.ctrl_l,
                pynput_keyboard.Key.ctrl_r,
                pynput_keyboard.Key.alt_l,
                pynput_keyboard.Key.alt_r,
                pynput_keyboard.Key.alt_gr,
            )
        ):
            if not (self._ctrl_down() and self._alt_down() and self._shutdown_key_down()):
                self._shutdown_fired = False
            if not (self._ctrl_down() and self._alt_down() and self._overlay_key_down()):
                self._overlay_toggle_fired = False
