import os
from PySide6.QtCore import QObject, Signal
from pynput import keyboard as pynput_keyboard


class ShutdownBus(QObject):
    shutdown_requested = Signal()


class GlobalHotkeyManager:
    def __init__(self, bus: ShutdownBus):
        self.bus = bus
        self._listener = None
        self._pressed = set()
        self._fired = False

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
        self._fired = False

    def force_kill(self) -> None:
        os._exit(0)

    def _on_press(self, key) -> None:
        self._pressed.add(key)
        ctrl_down = pynput_keyboard.Key.ctrl_l in self._pressed or pynput_keyboard.Key.ctrl_r in self._pressed
        alt_down = (
            pynput_keyboard.Key.alt_l in self._pressed
            or pynput_keyboard.Key.alt_r in self._pressed
            or pynput_keyboard.Key.alt_gr in self._pressed
        )
        end_down = key == pynput_keyboard.Key.end
        if ctrl_down and alt_down and end_down and not self._fired:
            self._fired = True
            self.bus.shutdown_requested.emit()

    def _on_release(self, key) -> None:
        self._pressed.discard(key)
        if key in (
            pynput_keyboard.Key.end,
            pynput_keyboard.Key.ctrl_l,
            pynput_keyboard.Key.ctrl_r,
            pynput_keyboard.Key.alt_l,
            pynput_keyboard.Key.alt_r,
            pynput_keyboard.Key.alt_gr,
        ):
            self._fired = False
