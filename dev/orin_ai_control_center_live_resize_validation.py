# Helper Status: Workstream-scoped
# Owner Workstream: FAM-007 H4 AI Control Center live resize repair
# Reason Reusable Helper Was Not Extended: the HUD live validator is FAM-006-specific and exercises the Dashboard launch/tray flow; this helper proves the FAM-007 AI Control Center resize path directly with real OS mouse input.
# Consolidation Target: future reusable Nexus product-window live resize validator
# Promotion Decision Point: before PR Readiness fold-down

from __future__ import annotations

import ctypes
import ctypes.wintypes
import datetime
import json
import os
import sys
import time
from pathlib import Path

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from desktop.desktop_renderer import AIControlCenterDialog
from desktop.ai_provider_state import (
    build_default_provider_readiness_config,
    build_provider_setup_completion_foundation_state,
)


MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

user32 = ctypes.windll.user32
SetCursorPos = user32.SetCursorPos
SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
SetCursorPos.restype = ctypes.c_bool
mouse_event = user32.mouse_event
mouse_event.argtypes = [
    ctypes.wintypes.DWORD,
    ctypes.c_long,
    ctypes.c_long,
    ctypes.wintypes.DWORD,
    ctypes.c_ulong,
]
mouse_event.restype = None
GetWindowRect = user32.GetWindowRect
GetWindowRect.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.RECT)]
GetWindowRect.restype = ctypes.c_bool
SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = [ctypes.wintypes.HWND]
SetForegroundWindow.restype = ctypes.c_bool
BringWindowToTop = user32.BringWindowToTop
BringWindowToTop.argtypes = [ctypes.wintypes.HWND]
BringWindowToTop.restype = ctypes.c_bool


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def _rect_to_dict(rect: ctypes.wintypes.RECT) -> dict[str, int]:
    return {
        "left": int(rect.left),
        "top": int(rect.top),
        "right": int(rect.right),
        "bottom": int(rect.bottom),
        "width": int(rect.right - rect.left),
        "height": int(rect.bottom - rect.top),
    }


def _native_rect(hwnd: int) -> dict[str, int]:
    rect = ctypes.wintypes.RECT()
    if not GetWindowRect(ctypes.wintypes.HWND(int(hwnd)), ctypes.byref(rect)):
        raise RuntimeError("GetWindowRect failed for AI Control Center")
    return _rect_to_dict(rect)


def _pump(app: QApplication, duration_ms: int = 80) -> None:
    deadline = time.monotonic() + max(0, duration_ms) / 1000.0
    while time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()


def _run_js(app: QApplication, dialog: AIControlCenterDialog, script: str, timeout_ms: int = 1200):
    box: dict[str, object] = {"done": False, "result": None}

    def _complete(result):
        box["result"] = result
        box["done"] = True

    dialog.webview.page().runJavaScript(script, _complete)
    deadline = time.monotonic() + max(0, timeout_ms) / 1000.0
    while not box["done"] and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    return box.get("result")


def _move_mouse(app: QApplication, x: int, y: int, settle_ms: int = 18) -> None:
    SetCursorPos(int(x), int(y))
    mouse_event(MOUSEEVENTF_MOVE, 0, 0, 0, 0)
    _pump(app, settle_ms)


def _capture(app: QApplication, dialog: AIControlCenterDialog, root: Path, label: str) -> dict[str, str]:
    full_path = root / f"{label}_full_desktop.png"
    focused_path = root / f"{label}_focused_window.png"
    screen = dialog.screen() or QApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No screen available for screenshot capture")
    full = screen.grabWindow(0)
    if not full.save(str(full_path)):
        raise RuntimeError(f"Failed to save full desktop screenshot: {full_path}")
    focused = dialog.grab()
    if not focused.save(str(focused_path)):
        raise RuntimeError(f"Failed to save focused screenshot: {focused_path}")
    _pump(app, 40)
    return {
        "fullDesktop": str(full_path),
        "focusedWindow": str(focused_path),
    }


def _drag_resize(
    app: QApplication,
    hwnd: int,
    label: str,
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    *,
    steps: int = 42,
) -> dict[str, object]:
    before = _native_rect(hwnd)
    samples = [before]
    _move_mouse(app, start_x, start_y, 140)
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    _pump(app, 80)
    for index in range(1, steps + 1):
        t = index / steps
        x = round(start_x + ((end_x - start_x) * t))
        y = round(start_y + ((end_y - start_y) * t))
        _move_mouse(app, x, y, 10)
        samples.append(_native_rect(hwnd))
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    _pump(app, 260)
    after = _native_rect(hwnd)
    samples.append(after)
    unique_sizes = sorted({(item["width"], item["height"]) for item in samples})
    unique_widths = sorted({item["width"] for item in samples})
    unique_heights = sorted({item["height"] for item in samples})
    return {
        "label": label,
        "method": "SetCursorPos plus held Win32 left mouse button against visible AI Control Center resize rail",
        "start": {"x": int(start_x), "y": int(start_y)},
        "end": {"x": int(end_x), "y": int(end_y)},
        "before": before,
        "after": after,
        "widthDelta": int(after["width"] - before["width"]),
        "heightDelta": int(after["height"] - before["height"]),
        "sampleCount": len(samples),
        "uniqueSizeCount": len(unique_sizes),
        "uniqueWidthCount": len(unique_widths),
        "uniqueHeightCount": len(unique_heights),
        "samples": samples,
    }


def _copy_user_evidence(local_root: Path, stamp: str) -> Path:
    user_root = (
        Path.home()
        / "OneDrive"
        / "Pictures"
        / "Screenshots"
        / "Nexus Desktop AI"
        / "FAM-007-H4"
        / f"{stamp}-live-resize"
    )
    user_root.mkdir(parents=True, exist_ok=True)
    for png in sorted(local_root.glob("*.png")):
        (user_root / png.name).write_bytes(png.read_bytes())
    return user_root


def main() -> int:
    stamp = _timestamp()
    repo_root = Path(__file__).resolve().parents[1]
    log_root = repo_root / "dev" / "logs" / "fam_007_ai_control_center_live_resize" / stamp
    log_root.mkdir(parents=True, exist_ok=True)
    os.environ["NEXUS_AI_CONTROL_CENTER_STATE_PATH"] = str(log_root / "isolated_ai_control_center_window_state.json")

    app = QApplication.instance() or QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No primary screen available for live resize validation")

    events: list[str] = []
    provider_state = build_provider_setup_completion_foundation_state(
        build_default_provider_readiness_config(),
        surface_role="hud",
    )
    dialog = AIControlCenterDialog(screen, event_logger=events.append)
    dialog.update_provider_state(provider_state.as_renderer_payload())

    available = screen.availableGeometry()
    initial_width = min(dialog.DEFAULT_WIDTH, max(dialog.minimumWidth() + 80, available.width() - 360))
    initial_height = min(dialog.DEFAULT_HEIGHT, max(dialog.minimumHeight() + 80, available.height() - 260))
    initial = QRect(
        available.x() + 120,
        available.y() + 80,
        int(initial_width),
        int(initial_height),
    )
    dialog.setGeometry(dialog._bound_geometry_to_available_desktop(initial))
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()
    _pump(app, 900)
    hwnd = int(dialog.winId())
    BringWindowToTop(ctypes.wintypes.HWND(hwnd))
    SetForegroundWindow(ctypes.wintypes.HWND(hwnd))
    _pump(app, 300)

    screenshot_evidence: dict[str, dict[str, str]] = {}
    initial_native_rect = _native_rect(hwnd)
    screenshot_evidence["before"] = _capture(app, dialog, log_root, "01_before_resize")
    custom_scrollbar_probe_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const surface = document.getElementById("monitoring-hud");
          const hub = document.getElementById("ai-control-center-card-hub");
          if (!surface || !hub || !window.nexusAiControlCenterSyncScrollbar) {
            return { ok: false, reason: "missing-scrollbar-elements" };
          }
          hub.dataset.scrollbarVisualProbe = "temporary-overflow-proof";
          hub.style.setProperty("padding-bottom", "220px", "important");
          void hub.offsetHeight;
          window.nexusAiControlCenterSyncScrollbar();
          const thumb = document.getElementById("ai-control-center-scrollbar-thumb");
          const thumbStyle = thumb ? window.getComputedStyle(thumb) : null;
          return JSON.stringify({
            ok: surface.dataset.customScrollbarVisible === "true",
            style: surface.dataset.scrollbarStyle || "",
            visible: surface.dataset.customScrollbarVisible || "",
            thumbBorderRadius: thumbStyle ? thumbStyle.borderRadius : "",
            thumbBackground: thumbStyle ? thumbStyle.backgroundColor : ""
          });
        })();
        """,
    )
    try:
        custom_scrollbar_probe = json.loads(custom_scrollbar_probe_raw) if isinstance(custom_scrollbar_probe_raw, str) else custom_scrollbar_probe_raw
    except json.JSONDecodeError:
        custom_scrollbar_probe = {"ok": False, "raw": custom_scrollbar_probe_raw}
    _pump(app, 200)
    screenshot_evidence["customScrollbarProbe"] = _capture(
        app,
        dialog,
        log_root,
        "02_custom_scrollbar_visual_probe",
    )
    _run_js(
        app,
        dialog,
        """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          if (hub) {
            hub.style.removeProperty("padding-bottom");
            delete hub.dataset.scrollbarVisualProbe;
          }
          window.nexusAiControlCenterSyncScrollbar && window.nexusAiControlCenterSyncScrollbar();
          return true;
        })();
        """,
    )
    _pump(app, 200)

    rect = _native_rect(hwnd)
    corner = _drag_resize(
        app,
        hwnd,
        "bottom_right_corner",
        rect["right"] - 8,
        rect["bottom"] - 8,
        min(available.right() - 24, rect["right"] + 96),
        min(available.bottom() - 24, rect["bottom"] + 72),
    )
    screenshot_evidence["afterCorner"] = _capture(app, dialog, log_root, "02_after_corner_resize")

    rect = _native_rect(hwnd)
    right = _drag_resize(
        app,
        hwnd,
        "right_edge",
        rect["right"] - 8,
        rect["top"] + max(220, rect["height"] // 2),
        min(available.right() - 24, rect["right"] + 84),
        rect["top"] + max(220, rect["height"] // 2),
    )
    screenshot_evidence["afterRightEdge"] = _capture(app, dialog, log_root, "03_after_right_edge_resize")

    rect = _native_rect(hwnd)
    bottom = _drag_resize(
        app,
        hwnd,
        "bottom_edge",
        rect["left"] + rect["width"] // 2,
        rect["bottom"] - 8,
        rect["left"] + rect["width"] // 2,
        min(available.bottom() - 24, rect["bottom"] + 66),
    )
    screenshot_evidence["afterBottomEdge"] = _capture(app, dialog, log_root, "04_after_bottom_edge_resize")

    checks = {
        "defaultOpenUsesContentFitHeight": abs(initial_native_rect["height"] - int(initial_height)) <= 4,
        "defaultOpenRespectsMaxHeight": initial_native_rect["height"] <= dialog.DEFAULT_MAX_HEIGHT,
        "customScrollbarProbeVisible": bool(
            isinstance(custom_scrollbar_probe, dict)
            and custom_scrollbar_probe.get("ok") is True
            and custom_scrollbar_probe.get("style") == "nexus-rounded-custom-overlay"
        ),
        "cornerResizeChangedWidth": corner["widthDelta"] >= 36,
        "cornerResizeChangedHeight": corner["heightDelta"] >= 28,
        "cornerFluidGeometrySamples": corner["uniqueSizeCount"] >= 6,
        "rightEdgeChangedWidth": right["widthDelta"] >= 32,
        "rightEdgeFluidGeometrySamples": right["uniqueWidthCount"] >= 4,
        "bottomEdgeChangedHeight": bottom["heightDelta"] >= 26,
        "bottomEdgeFluidGeometrySamples": bottom["uniqueHeightCount"] >= 4,
        "fallbackStartedMarker": any("AI_CONTROL_CENTER_WINDOW_RESIZE_FALLBACK_STARTED" in event for event in events),
        "resizeReadyMarker": any("AI_CONTROL_CENTER_WINDOW_RESIZE_READY" in event for event in events),
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    user_evidence_root = _copy_user_evidence(log_root, stamp)

    manifest = {
        "status": status,
        "stamp": stamp,
        "helper": "dev/orin_ai_control_center_live_resize_validation.py",
        "proofClass": "live OS mouse resize proof",
        "worktree": str(repo_root),
        "window": "AI Control Center",
        "realOsMouseInputProof": True,
        "qtestUsed": False,
        "directHandlerMutationUsed": False,
        "nativeGeometrySource": "Win32 GetWindowRect",
        "initialWindowRect": initial_native_rect,
        "initialWindowScreenshots": screenshot_evidence["before"],
        "customScrollbarProbe": custom_scrollbar_probe,
        "expectedInitialWindowSize": {
            "width": int(initial_width),
            "height": int(initial_height),
            "defaultWidth": int(dialog.DEFAULT_WIDTH),
            "defaultHeight": int(dialog.DEFAULT_HEIGHT),
            "defaultMaxHeight": int(dialog.DEFAULT_MAX_HEIGHT),
        },
        "scrollbarStyle": "nexus-rounded-custom-overlay",
        "checks": checks,
        "drags": {
            "bottomRightCorner": corner,
            "rightEdge": right,
            "bottomEdge": bottom,
        },
        "events": events,
        "screenshots": screenshot_evidence,
        "userInspectableEvidenceRoot": str(user_evidence_root),
        "localLogRoot": str(log_root),
    }
    manifest_path = log_root / "live_resize_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (user_evidence_root / "live_resize_manifest.json").write_bytes(manifest_path.read_bytes())

    dialog.close()
    _pump(app, 160)

    if status != "PASS":
        print(f"FAIL: FAM-007 AI Control Center live resize validation failed. Manifest: {manifest_path}")
        return 1
    print(f"PASS: FAM-007 AI Control Center live resize validation passed. Manifest: {manifest_path}")
    print(f"USER_EVIDENCE_ROOT: {user_evidence_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
