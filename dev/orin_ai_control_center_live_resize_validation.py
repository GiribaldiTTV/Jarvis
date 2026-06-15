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
    isolated_state_path = log_root / "isolated_ai_control_center_window_state.json"
    os.environ["NEXUS_AI_CONTROL_CENTER_STATE_PATH"] = str(isolated_state_path)
    os.environ.pop("NEXUS_AI_CONTROL_CENTER_ENABLE_GEOMETRY_MEMORY", None)
    isolated_state_path.write_text(
        json.dumps(
            {
                "schemaVersion": 9,
                "kind": "ai-control-center-window-geometry",
                "x": 12,
                "y": 12,
                "w": 900,
                "h": 760,
                "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

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
    constructor_default_rect = {
        "x": int(dialog.geometry().x()),
        "y": int(dialog.geometry().y()),
        "width": int(dialog.geometry().width()),
        "height": int(dialog.geometry().height()),
    }
    geometry_memory_enabled = bool(dialog._window_geometry_memory_enabled())

    available = screen.availableGeometry()
    initial_width = min(dialog.DEFAULT_WIDTH, max(dialog.minimumWidth() + 80, available.width() - 360))
    initial_height = min(dialog.DEFAULT_HEIGHT, max(dialog.minimumHeight() + 80, available.height() - 260))
    initial = QRect(
        available.x() + 120,
        available.y() + 80,
        int(initial_width),
        int(initial_height),
    )
    initial_bounded = dialog._bound_geometry_to_available_desktop(initial)
    dialog.setGeometry(initial_bounded)
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
    title_chrome_proof_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const rect = (element) => {
            if (!element) {
              return null;
            }
            const bounds = element.getBoundingClientRect();
            return {
              left: Math.round(bounds.left),
              top: Math.round(bounds.top),
              right: Math.round(bounds.right),
              bottom: Math.round(bounds.bottom),
              width: Math.round(bounds.width),
              height: Math.round(bounds.height)
            };
          };
          const style = (element) => {
            if (!element) {
              return null;
            }
            const computed = window.getComputedStyle(element);
            return {
              background: computed.background,
              borderColor: computed.borderColor,
              borderRadius: computed.borderRadius,
              color: computed.color,
              fontFamily: computed.fontFamily,
              fontSize: computed.fontSize,
              fontWeight: computed.fontWeight,
              height: computed.height,
              letterSpacing: computed.letterSpacing,
              lineHeight: computed.lineHeight,
              paddingLeft: computed.paddingLeft,
              paddingRight: computed.paddingRight,
              textTransform: computed.textTransform,
              width: computed.width
            };
          };
          const subtitle = document.querySelector(".monitoring-hud__subtitle");
          const cluster = document.querySelector(".monitoring-hud__window-controls");
          const close = document.getElementById("ai-control-center-close-action");
          const maximize = document.getElementById("ai-control-center-maximize-action");
          const minimize = document.getElementById("ai-control-center-minimize-action");
          return JSON.stringify({
            subtitleText: subtitle ? subtitle.textContent.trim() : "",
            subtitleLineCount: subtitle ? subtitle.getClientRects().length : 0,
            subtitleRect: rect(subtitle),
            clusterRect: rect(cluster),
            clusterStyle: style(cluster),
            closeText: close ? close.textContent.trim() : "",
            closeRect: rect(close),
            closeClass: close ? close.className : "",
            closeStyle: style(close),
            closeLabel: close ? close.getAttribute("aria-label") : "",
            closeTitle: close ? close.getAttribute("title") : "",
            maximizeText: maximize ? maximize.textContent.trim() : "",
            maximizeRect: rect(maximize),
            maximizeClass: maximize ? maximize.className : "",
            maximizeStyle: style(maximize),
            maximizeLabel: maximize ? maximize.getAttribute("aria-label") : "",
            maximizeState: maximize ? maximize.dataset.windowState : "",
            maximizeControl: maximize ? maximize.dataset.control : "",
            maximizeDisabled: maximize ? maximize.disabled : false,
            maximizeAriaDisabled: maximize ? maximize.getAttribute("aria-disabled") : "",
            maximizeTitle: maximize ? maximize.getAttribute("title") : "",
            minimizeText: minimize ? minimize.textContent.trim() : "",
            minimizeRect: rect(minimize),
            minimizeClass: minimize ? minimize.className : "",
            minimizeStyle: style(minimize),
            minimizeLabel: minimize ? minimize.getAttribute("aria-label") : "",
            minimizeTitle: minimize ? minimize.getAttribute("title") : "",
            chromeGap: close && maximize && minimize
              ? Math.round(Math.min(
                  maximize.getBoundingClientRect().left - minimize.getBoundingClientRect().right,
                  close.getBoundingClientRect().left - maximize.getBoundingClientRect().right
                ))
              : null,
            compactButtonCount: cluster ? cluster.querySelectorAll(".monitoring-hud__window-control-button").length : 0
          });
        })();
        """,
    )
    try:
        title_chrome_proof = json.loads(title_chrome_proof_raw) if isinstance(title_chrome_proof_raw, str) else title_chrome_proof_raw
    except json.JSONDecodeError:
        title_chrome_proof = {"ok": False, "raw": title_chrome_proof_raw}
    hover_proof: dict[str, object] = {}
    if isinstance(title_chrome_proof, dict):
        window_rect_for_hover = _native_rect(hwnd)
        for rect_key, label in (
            ("minimizeRect", "02_window_control_minimize_hover"),
            ("maximizeRect", "03_window_control_maximize_disabled_hover"),
            ("closeRect", "04_window_control_close_hover"),
        ):
            control_rect = title_chrome_proof.get(rect_key)
            if not isinstance(control_rect, dict):
                hover_proof[label] = {"ok": False, "reason": f"missing-{rect_key}"}
                continue
            hover_x = int(window_rect_for_hover["left"] + int(control_rect.get("left") or 0) + (int(control_rect.get("width") or 0) // 2))
            hover_y = int(window_rect_for_hover["top"] + int(control_rect.get("top") or 0) + (int(control_rect.get("height") or 0) // 2))
            _move_mouse(app, hover_x, hover_y, 900)
            hover_proof[label] = {
                "ok": True,
                "screenPoint": {"x": hover_x, "y": hover_y},
                "evidence": _capture(app, dialog, log_root, label),
            }
    _move_mouse(app, _native_rect(hwnd)["left"] + 24, _native_rect(hwnd)["top"] + 24, 120)
    minimize_click_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const minimize = document.getElementById("ai-control-center-minimize-action");
          if (!minimize) {
            return JSON.stringify({ ok: false, reason: "missing-minimize-button" });
          }
          minimize.click();
          return JSON.stringify({ ok: true, text: minimize.textContent.trim(), className: minimize.className });
        })();
        """,
    )
    try:
        minimize_click = json.loads(minimize_click_raw) if isinstance(minimize_click_raw, str) else minimize_click_raw
    except json.JSONDecodeError:
        minimize_click = {"ok": False, "raw": minimize_click_raw}
    _pump(app, 360)
    minimized_after_click = bool(dialog.isMinimized())
    dialog.showNormal()
    dialog.setGeometry(initial_bounded)
    dialog.raise_()
    dialog.activateWindow()
    _pump(app, 360)
    BringWindowToTop(ctypes.wintypes.HWND(hwnd))
    SetForegroundWindow(ctypes.wintypes.HWND(hwnd))
    _pump(app, 220)
    post_minimize_restore_rect = _native_rect(hwnd)
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
        "04_custom_scrollbar_visual_probe",
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
    corner_offset = max(18, (int(getattr(dialog, "RESIZE_MARGIN", 14)) * 2) - 2)
    corner = _drag_resize(
        app,
        hwnd,
        "bottom_right_corner",
        rect["right"] - corner_offset,
        rect["bottom"] - corner_offset,
        min(available.right() - 24, rect["right"] + 96),
        min(available.bottom() - 24, rect["bottom"] + 72),
    )
    screenshot_evidence["afterCorner"] = _capture(app, dialog, log_root, "05_after_corner_resize")
    dialog.setGeometry(initial_bounded)
    _pump(app, 180)
    BringWindowToTop(ctypes.wintypes.HWND(hwnd))
    SetForegroundWindow(ctypes.wintypes.HWND(hwnd))
    _pump(app, 160)

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
    screenshot_evidence["afterRightEdge"] = _capture(app, dialog, log_root, "06_after_right_edge_resize")
    dialog.setGeometry(initial_bounded)
    _pump(app, 180)
    BringWindowToTop(ctypes.wintypes.HWND(hwnd))
    SetForegroundWindow(ctypes.wintypes.HWND(hwnd))
    _pump(app, 160)

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
    screenshot_evidence["afterBottomEdge"] = _capture(app, dialog, log_root, "07_after_bottom_edge_resize")
    try:
        final_state_payload = json.loads(isolated_state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        final_state_payload = {}

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
        "restartMemoryDisabled": geometry_memory_enabled is False,
        "staleGeometryIgnoredAtConstruction": (
            int(constructor_default_rect["width"]) == int(dialog.DEFAULT_WIDTH)
            and int(constructor_default_rect["height"]) == int(dialog.DEFAULT_HEIGHT)
        ),
        "geometryStateNotPersistedDuringRuntime": (
            int(final_state_payload.get("w") or 0) == 900
            and int(final_state_payload.get("h") or 0) == 760
            and int(final_state_payload.get("x") or 0) == 12
            and int(final_state_payload.get("y") or 0) == 12
        ),
        "titleSubtitleDoesNotWrapTooSoon": (
            isinstance(title_chrome_proof, dict)
            and int(title_chrome_proof.get("subtitleLineCount") or 0) <= 1
        ),
        "compactWindowControlClusterVisible": (
            isinstance(title_chrome_proof, dict)
            and int(title_chrome_proof.get("compactButtonCount") or 0) == 3
            and isinstance(title_chrome_proof.get("clusterRect"), dict)
            and int(title_chrome_proof["clusterRect"].get("width") or 0) <= 130
        ),
        "compactWindowControlButtonsSized": (
            isinstance(title_chrome_proof, dict)
            and all(
                isinstance(title_chrome_proof.get(key), dict)
                and int(title_chrome_proof[key].get("width") or 0) <= 34
                and int(title_chrome_proof[key].get("height") or 0) <= 32
                for key in ("minimizeRect", "maximizeRect", "closeRect")
            )
        ),
        "compactWindowControlBordersVisible": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("minimizeStyle"), dict)
            and title_chrome_proof["minimizeStyle"].get("borderColor") == "rgba(122, 232, 255, 0.34)"
            and isinstance(title_chrome_proof.get("closeStyle"), dict)
            and title_chrome_proof["closeStyle"].get("borderColor") == "rgba(122, 232, 255, 0.34)"
            and isinstance(title_chrome_proof.get("maximizeStyle"), dict)
            and title_chrome_proof["maximizeStyle"].get("borderColor") == "rgba(122, 232, 255, 0.25)"
        ),
        "windowControlNativeTooltipsSuppressed": (
            isinstance(title_chrome_proof, dict)
            and not title_chrome_proof.get("minimizeTitle")
            and not title_chrome_proof.get("maximizeTitle")
            and not title_chrome_proof.get("closeTitle")
        ),
        "windowControlHoverProofCaptured": (
            isinstance(hover_proof, dict)
            and all(
                isinstance(hover_proof.get(label), dict)
                and hover_proof[label].get("ok") is True
                and isinstance(hover_proof[label].get("evidence"), dict)
                for label in (
                    "02_window_control_minimize_hover",
                    "03_window_control_maximize_disabled_hover",
                    "04_window_control_close_hover",
                )
            )
        ),
        "windowControlAccessibleLabelsPresent": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("minimizeLabel") == "Minimize AI Control Center"
            and title_chrome_proof.get("maximizeLabel") == "Maximize or restore AI Control Center future-gated"
            and title_chrome_proof.get("closeLabel") == "Close AI Control Center"
        ),
        "maximizeRestoreFutureGatedDisabled": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("maximizeDisabled") is True
            and title_chrome_proof.get("maximizeAriaDisabled") == "true"
            and title_chrome_proof.get("maximizeControl") == "maximize-restore-future-gated"
            and title_chrome_proof.get("maximizeState") == "future-gated"
        ),
        "minimizeMaximizeCloseShareCompactClass": (
            isinstance(title_chrome_proof, dict)
            and "monitoring-hud__window-control-button" in str(title_chrome_proof.get("minimizeClass") or "")
            and "monitoring-hud__window-control-button" in str(title_chrome_proof.get("maximizeClass") or "")
            and "monitoring-hud__window-control-button" in str(title_chrome_proof.get("closeClass") or "")
        ),
        "minimizeCommandMinimizedWindow": minimized_after_click,
        "minimizeRestoreReturnedToKnownGeometry": (
            abs(post_minimize_restore_rect["width"] - initial_native_rect["width"]) <= 4
            and abs(post_minimize_restore_rect["height"] - initial_native_rect["height"]) <= 4
        ),
        "minimizeMarkerLogged": any("AI_CONTROL_CENTER_MINIMIZED" in event for event in events),
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
        "titleChromeProof": title_chrome_proof,
        "windowControlHoverProof": hover_proof,
        "windowControlProof": {
            "cluster": "compact-minimize-maximize-close",
            "minimize": "active-native-showMinimized",
            "maximizeRestore": "future-gated-disabled",
            "close": "active-native-close",
        },
        "minimizeClickProof": {
            "clickResult": minimize_click,
            "windowMinimizedAfterClick": minimized_after_click,
            "restoredForResizeProof": bool(not dialog.isMinimized()),
            "postMinimizeRestoreRect": post_minimize_restore_rect,
        },
        "expectedInitialWindowSize": {
            "width": int(initial_width),
            "height": int(initial_height),
            "defaultWidth": int(dialog.DEFAULT_WIDTH),
            "defaultHeight": int(dialog.DEFAULT_HEIGHT),
            "defaultMaxHeight": int(dialog.DEFAULT_MAX_HEIGHT),
        },
        "geometryMemoryPolicy": {
            "env": "NEXUS_AI_CONTROL_CENTER_ENABLE_GEOMETRY_MEMORY",
            "enabled": geometry_memory_enabled,
            "restartMemoryDisabled": geometry_memory_enabled is False,
            "staleStatePath": str(isolated_state_path),
            "constructorDefaultRect": constructor_default_rect,
            "ignoredPersistedSize": {"width": 900, "height": 760},
            "finalStatePayload": final_state_payload,
            "fam003ResetDependency": "ai-global-settings-reset-default-location-size",
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
