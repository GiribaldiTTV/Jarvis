"""Live proof helper for the FAM-006 Dashboard rounded native window mask.

The human-client validator launches the real FAM-006 shortcut and then calls
this helper with the live Dashboard HWND. This helper places a white backdrop
behind that window, samples the native window's rounded-corner exterior pixels,
and fails if the old opaque rectangular black corner is still present.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
import tkinter as tk

import win32api
import win32con
import win32gui
import win32ui


LIGHT_THRESHOLD = 210
DASHBOARD_VISIBLE_THRESHOLD = 190
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79


def _screen_bounds() -> tuple[int, int, int, int]:
    left = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
    width = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
    return left, top, left + width, top + height


def _sample_color(screen_dc: int, x: int, y: int) -> dict[str, object]:
    colorref = win32gui.GetPixel(screen_dc, x, y)
    r = colorref & 0xFF
    g = (colorref >> 8) & 0xFF
    b = (colorref >> 16) & 0xFF
    brightness = round((r + g + b) / 3.0, 2)
    return {"x": x, "y": y, "r": r, "g": g, "b": b, "brightness": brightness}


def _is_light_backdrop(sample: dict[str, object]) -> bool:
    return (
        int(sample["r"]) >= LIGHT_THRESHOLD
        and int(sample["g"]) >= LIGHT_THRESHOLD
        and int(sample["b"]) >= LIGHT_THRESHOLD
        and float(sample["brightness"]) >= LIGHT_THRESHOLD
    )


def _is_visible_dashboard(sample: dict[str, object]) -> bool:
    return float(sample["brightness"]) <= DASHBOARD_VISIBLE_THRESHOLD


def _capture_virtual_desktop(output_dir: Path) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%H%M%S_%f")[:-3]
    path = output_dir / f"{stamp}_dashboard_rounded_corner_mask_light_backdrop.bmp"
    left, top, right, bottom = _screen_bounds()
    width = right - left
    height = bottom - top

    desktop_hwnd = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(desktop_hwnd)
    src_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = src_dc.CreateCompatibleDC()
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(src_dc, width, height)
    previous = mem_dc.SelectObject(bitmap)
    try:
        mem_dc.BitBlt((0, 0), (width, height), src_dc, (left, top), win32con.SRCCOPY)
        bitmap.SaveBitmapFile(mem_dc, str(path))
    finally:
        mem_dc.SelectObject(previous)
        win32gui.DeleteObject(bitmap.GetHandle())
        mem_dc.DeleteDC()
        src_dc.DeleteDC()
        win32gui.ReleaseDC(desktop_hwnd, desktop_dc)
    return str(path)


def _bring_dashboard_front(hwnd: int) -> None:
    flags = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, flags)
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flags)
    win32gui.BringWindowToTop(hwnd)


def run_probe(hwnd: int, output_dir: Path) -> dict[str, object]:
    if not hwnd or not win32gui.IsWindow(hwnd):
        raise RuntimeError(f"Dashboard HWND is not valid: {hwnd}")

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    if right <= left or bottom <= top:
        raise RuntimeError(f"Dashboard HWND has invalid rect: {(left, top, right, bottom)}")

    width = right - left
    height = bottom - top
    backdrop = tk.Tk()
    backdrop.title("NDAI rounded corner validation backdrop")
    backdrop.overrideredirect(True)
    backdrop.configure(bg="white")
    backdrop.geometry(f"{width + 72}x{height + 72}+{left - 36}+{top - 36}")
    backdrop.update_idletasks()
    backdrop.update()
    time.sleep(0.2)
    _bring_dashboard_front(hwnd)
    time.sleep(0.3)

    screen_hwnd = win32gui.GetDesktopWindow()
    screen_dc = win32gui.GetWindowDC(screen_hwnd)
    try:
        corner_points = [
            (left + 6, top + 6),
            (right - 7, top + 6),
            (left + 6, bottom - 7),
            (right - 7, bottom - 7),
        ]
        visible_points = [
            (left + min(64, max(16, width // 4)), top + min(64, max(16, height // 5))),
            (left + width // 2, top + min(92, max(18, height // 4))),
        ]
        corner_samples = [_sample_color(screen_dc, x, y) for x, y in corner_points]
        visible_samples = [_sample_color(screen_dc, x, y) for x, y in visible_points]
        screenshot = _capture_virtual_desktop(output_dir)
    finally:
        win32gui.ReleaseDC(screen_hwnd, screen_dc)
        backdrop.destroy()

    corner_pass = all(_is_light_backdrop(sample) for sample in corner_samples)
    visible_pass = all(_is_visible_dashboard(sample) for sample in visible_samples)
    return {
        "pass": bool(corner_pass and visible_pass),
        "screenshot": screenshot,
        "windowRect": [left, top, right, bottom],
        "backdropRect": [left - 36, top - 36, right + 36, bottom + 36],
        "cornerPass": bool(corner_pass),
        "visibleDashboardPass": bool(visible_pass),
        "cornerSamples": corner_samples,
        "visibleSamples": visible_samples,
        "policy": "rounded corner exterior samples must show the white validation backdrop while interior samples still show Dashboard chrome",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--window-handle", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run_probe(args.window_handle, args.output_dir)
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
