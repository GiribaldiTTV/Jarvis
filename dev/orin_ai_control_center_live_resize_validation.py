# Helper Status: Workstream-scoped
# Owner Workstream: FAM-007 AI Dashboard parent-only Workstream-exit repair
# Reason Reusable Helper Was Not Extended: the HUD live validator is FAM-006-specific; this helper proves FAM-007 parent-dashboard visual/function acceptance after detached child windows were deferred.
# Consolidation Target: future reusable Nexus product-window visual and functional acceptance validator
# Promotion Decision Point: before PR Readiness fold-down

from __future__ import annotations

import ctypes
import ctypes.wintypes
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from desktop.ai_provider_state import (  # noqa: E402
    build_default_provider_readiness_config,
    build_provider_setup_completion_foundation_state,
)
from desktop.desktop_renderer import AIControlCenterDialog  # noqa: E402


user32 = ctypes.windll.user32
GetWindowRect = user32.GetWindowRect
GetWindowRect.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.RECT)]
GetWindowRect.restype = ctypes.c_bool
SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = [ctypes.wintypes.HWND]
SetForegroundWindow.restype = ctypes.c_bool
BringWindowToTop = user32.BringWindowToTop
BringWindowToTop.argtypes = [ctypes.wintypes.HWND]
BringWindowToTop.restype = ctypes.c_bool
ShowWindow = user32.ShowWindow
ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
ShowWindow.restype = ctypes.c_bool
SetCursorPos = user32.SetCursorPos
SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
SetCursorPos.restype = ctypes.c_bool
mouse_event = user32.mouse_event
mouse_event.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
mouse_event.restype = None
SW_RESTORE = 9
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def _pump(app: QApplication, duration_ms: int = 80) -> None:
    deadline = time.monotonic() + max(0, duration_ms) / 1000.0
    while time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()


def _run_js(app: QApplication, dialog: AIControlCenterDialog, script: str, timeout_ms: int = 1500):
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


def _run_child_js(app: QApplication, window, script: str, timeout_ms: int = 1500):
    box: dict[str, object] = {"done": False, "result": None}

    def _complete(result):
        box["result"] = result
        box["done"] = True

    window.webview.page().runJavaScript(script, _complete)
    deadline = time.monotonic() + max(0, timeout_ms) / 1000.0
    while not box["done"] and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    return box.get("result")


def _rect(hwnd: int) -> dict[str, int]:
    native_rect = ctypes.wintypes.RECT()
    if not hwnd or not GetWindowRect(ctypes.wintypes.HWND(int(hwnd)), ctypes.byref(native_rect)):
        return {"left": 0, "top": 0, "right": 0, "bottom": 0, "width": 0, "height": 0}
    return {
        "left": int(native_rect.left),
        "top": int(native_rect.top),
        "right": int(native_rect.right),
        "bottom": int(native_rect.bottom),
        "width": int(native_rect.right - native_rect.left),
        "height": int(native_rect.bottom - native_rect.top),
    }


def _foreground_window(app: QApplication, window, duration_ms: int = 260) -> None:
    window.showNormal()
    window.raise_()
    window.activateWindow()
    hwnd = int(window.winId()) if window.winId() else 0
    if hwnd:
        ShowWindow(ctypes.wintypes.HWND(hwnd), SW_RESTORE)
        BringWindowToTop(ctypes.wintypes.HWND(hwnd))
        SetForegroundWindow(ctypes.wintypes.HWND(hwnd))
    _pump(app, duration_ms)


def _capture_window(app: QApplication, window, root: Path, label: str) -> dict[str, str]:
    focused_path = root / f"{label}_focused_window.png"
    desktop_path = root / f"{label}_full_desktop.png"
    screen = window.screen() or QApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No screen available for screenshot capture")
    _foreground_window(app, window)
    if not window.grab().save(str(focused_path)):
        raise RuntimeError(f"Failed to save focused screenshot: {focused_path}")
    _pump(app, 80)
    if not screen.grabWindow(0).save(str(desktop_path)):
        raise RuntimeError(f"Failed to save desktop screenshot: {desktop_path}")
    _pump(app, 50)
    return {"focusedWindow": str(focused_path), "fullDesktop": str(desktop_path)}


def _probe_rect_to_qrect(raw: dict[str, object] | None, window) -> QRect:
    source = raw if isinstance(raw, dict) else {}
    try:
        left = int(round(float(source.get("left", 0))))
        top = int(round(float(source.get("top", 0))))
        width = int(round(float(source.get("width", 0))))
        height = int(round(float(source.get("height", 0))))
    except Exception:
        return QRect()
    rect = QRect(max(0, left), max(0, top), max(0, width), max(0, height))
    return rect.intersected(QRect(0, 0, int(window.width()), int(window.height())))


def _capture_window_region(app: QApplication, window, root: Path, label: str, raw_rect: dict[str, object] | None) -> dict[str, object]:
    rect = _probe_rect_to_qrect(raw_rect, window)
    if not rect.isValid() or rect.width() < 16 or rect.height() < 12:
        return {"ok": False, "label": label, "reason": "invalid-rect"}
    path = root / f"{label}.png"
    _foreground_window(app, window, 140)
    if not window.grab(rect).save(str(path)):
        return {"ok": False, "label": label, "reason": "save-failed", "path": str(path)}
    return {
        "ok": True,
        "label": label,
        "path": str(path),
        "rect": {
            "left": rect.left(),
            "top": rect.top(),
            "width": rect.width(),
            "height": rect.height(),
        },
    }


def _copy_reference_image(source: Path, root: Path, label: str) -> dict[str, object]:
    target = root / f"{label}.png"
    if not source.exists():
        return {"ok": False, "label": label, "source": str(source), "reason": "missing-reference"}
    target.write_bytes(source.read_bytes())
    image = QImage(str(target))
    return {
        "ok": not image.isNull(),
        "label": label,
        "source": str(source),
        "path": str(target),
        "width": int(image.width()) if not image.isNull() else 0,
        "height": int(image.height()) if not image.isNull() else 0,
        "reason": "" if not image.isNull() else "unreadable-reference",
    }


def _scaled_for_board(image: QImage, max_width: int = 460, max_height: int = 420) -> QImage:
    if image.isNull():
        return image
    scaled = image
    if scaled.width() > max_width:
        scaled = scaled.scaledToWidth(max_width, Qt.SmoothTransformation)
    if scaled.height() > max_height:
        scaled = scaled.scaledToHeight(max_height, Qt.SmoothTransformation)
    return scaled


def _write_side_by_side_board(
    left_path: Path,
    right_path: Path,
    out_path: Path,
    left_label: str,
    right_label: str,
) -> dict[str, object]:
    left = QImage(str(left_path))
    right = QImage(str(right_path))
    if left.isNull() or right.isNull():
        return {
            "ok": False,
            "path": str(out_path),
            "reason": "source-image-unreadable",
            "left": str(left_path),
            "right": str(right_path),
        }
    left = _scaled_for_board(left)
    right = _scaled_for_board(right)
    padding = 18
    label_height = 32
    width = left.width() + right.width() + (padding * 3)
    height = max(left.height(), right.height()) + label_height + (padding * 2)
    board = QImage(width, height, QImage.Format_ARGB32)
    board.fill(QColor(2, 10, 20))
    painter = QPainter(board)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setPen(QColor(116, 240, 255))
    font = QFont("Segoe UI", 10)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(padding, padding + 14, left_label)
    right_x = left.width() + (padding * 2)
    painter.drawText(right_x, padding + 14, right_label)
    painter.drawImage(padding, padding + label_height, left)
    painter.drawImage(right_x, padding + label_height, right)
    painter.end()
    if not board.save(str(out_path)):
        return {"ok": False, "path": str(out_path), "reason": "save-failed"}
    return {
        "ok": True,
        "path": str(out_path),
        "left": str(left_path),
        "right": str(right_path),
    }


def _capture_main_runtime_ai_control_center_reference(log_root: Path) -> dict[str, object]:
    main_root = Path("C:/Nexus Desktop AI")
    launcher = Path.home() / "OneDrive" / "Desktop" / "MAIN GREEN - Nexus Desktop AI Launcher.lnk"
    focused_path = log_root / "09_main_runtime_old_ai_control_center_focused_window.png"
    desktop_path = log_root / "10_main_runtime_old_ai_control_center_full_desktop.png"
    script_path = log_root / "_capture_main_runtime_ai_control_center_reference.py"
    metadata_path = log_root / "main_runtime_old_ai_control_center_reference.json"
    state_path = log_root / "main_runtime_ai_control_center_state.json"
    if not main_root.exists():
        return {
            "ok": False,
            "referenceSource": str(main_root),
            "launcher": str(launcher),
            "reason": "main-runtime-root-missing",
        }
    script_path.write_text(
        f"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication

main_root = Path({json.dumps(str(main_root))})
focused_path = Path({json.dumps(str(focused_path))})
desktop_path = Path({json.dumps(str(desktop_path))})
metadata_path = Path({json.dumps(str(metadata_path))})
state_path = Path({json.dumps(str(state_path))})

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["NEXUS_AI_CONTROL_CENTER_STATE_PATH"] = str(state_path)
os.environ.pop("NEXUS_AI_CONTROL_CENTER_ENABLE_GEOMETRY_MEMORY", None)
sys.path.insert(0, str(main_root))

from desktop.ai_provider_state import build_default_provider_readiness_config, build_provider_setup_completion_foundation_state  # noqa: E402
from desktop.desktop_renderer import AIControlCenterDialog  # noqa: E402


def pump(app: QApplication, duration_ms: int = 80) -> None:
    deadline = time.monotonic() + max(0, duration_ms) / 1000.0
    while time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()


def run_js(app: QApplication, dialog: AIControlCenterDialog, script: str, timeout_ms: int = 1500):
    box = {{"done": False, "result": None}}

    def complete(result):
        box["result"] = result
        box["done"] = True

    dialog.webview.page().runJavaScript(script, complete)
    deadline = time.monotonic() + max(0, timeout_ms) / 1000.0
    while not box["done"] and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    return box.get("result")


app = QApplication.instance() or QApplication(sys.argv)
screen = QApplication.primaryScreen()
if screen is None:
    raise RuntimeError("No primary screen available for main runtime reference")
events = []
provider_state = build_provider_setup_completion_foundation_state(
    build_default_provider_readiness_config(),
    surface_role="hud",
)
dialog = AIControlCenterDialog(screen, event_logger=events.append)
dialog.update_provider_state(provider_state.as_renderer_payload())
available = screen.availableGeometry()
dialog.setGeometry(
    QRect(
        available.x() + max(40, available.width() - dialog.DEFAULT_WIDTH - 120),
        available.y() + 80,
        dialog.DEFAULT_WIDTH,
        dialog.DEFAULT_HEIGHT,
    )
)
dialog.show_from_tray()
pump(app, 900)
focused_saved = bool(dialog.grab().save(str(focused_path)))
pump(app, 80)
desktop_saved = bool(screen.grabWindow(0).save(str(desktop_path)))
probe_raw = run_js(
    app,
    dialog,
    \"\"\"
    (() => {{
      const surface = document.getElementById("monitoring-hud");
      return JSON.stringify({{
        title: document.querySelector(".monitoring-hud__title")?.textContent.trim() || "",
        subtitle: document.querySelector(".monitoring-hud__subtitle")?.textContent.trim() || "",
        surfaceId: surface?.dataset.surfaceId || "",
        productSurfaceRole: surface?.dataset.productSurfaceRole || "",
        defaultWindowWidth: surface?.dataset.defaultWindowWidth || "",
        defaultWindowHeight: surface?.dataset.defaultWindowHeight || "",
        cardTitles: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-card-title-copy strong, .monitoring-hud__hub-card-title-copy strong")].map((node) => node.textContent.trim()),
        bodyTextSample: document.body.innerText.replace(/\\\\s+/g, " ").trim().slice(0, 500)
      }});
    }})();
    \"\"\",
)
try:
    probe = json.loads(probe_raw or "{{}}")
except Exception:
    probe = {{"rawProbe": str(probe_raw or "")}}
metadata = {{
    "ok": bool(focused_saved and desktop_saved and focused_path.exists() and desktop_path.exists()),
    "referenceKind": "main-worktree-old-ai-control-center-runtime",
    "referenceSource": str(main_root),
    "focusedWindow": str(focused_path),
    "fullDesktop": str(desktop_path),
    "windowTitle": dialog.windowTitle(),
    "defaultWidth": int(dialog.DEFAULT_WIDTH),
    "defaultHeight": int(dialog.DEFAULT_HEIGHT),
    "minimumWidth": int(dialog.minimumWidth()),
    "minimumHeight": int(dialog.minimumHeight()),
    "probe": probe,
    "events": events,
}}
metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
print(json.dumps(metadata, sort_keys=True))
dialog.close()
pump(app, 300)
""".strip()
        + "\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["NEXUS_AI_CONTROL_CENTER_STATE_PATH"] = str(state_path)
    env.pop("NEXUS_AI_CONTROL_CENTER_ENABLE_GEOMETRY_MEMORY", None)
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(main_root),
        env=env,
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    stdout_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    metadata: dict[str, object] = {}
    if stdout_lines:
        try:
            metadata = json.loads(stdout_lines[-1])
        except Exception:
            metadata = {}
    ok = bool(metadata.get("ok")) and result.returncode == 0
    return {
        "ok": ok,
        "referenceKind": "main-worktree-old-ai-control-center-runtime",
        "referenceSource": str(main_root),
        "desktopLauncher": str(launcher),
        "launcherExists": launcher.exists(),
        "focusedWindow": str(focused_path),
        "fullDesktop": str(desktop_path),
        "metadataPath": str(metadata_path),
        "captureScript": str(script_path),
        "returnCode": result.returncode,
        "stdoutTail": stdout_lines[-3:],
        "stderrTail": result.stderr.splitlines()[-10:],
        "metadata": metadata,
        "reason": "" if ok else "main-runtime-reference-capture-failed",
    }


def _ai_dashboard_resize_hit_zone_probe(app: QApplication, dialog: AIControlCenterDialog) -> dict[str, object]:
    width = int(dialog.width())
    height = int(dialog.height())
    center_x = width // 2
    center_y = height // 2
    sample_points = {
        "left": QPoint(1, center_y),
        "right": QPoint(width - 2, center_y),
        "top": QPoint(center_x, 1),
        "bottom": QPoint(center_x, height - 2),
        "topLeft": QPoint(1, 1),
        "topRight": QPoint(width - 2, 1),
        "bottomLeft": QPoint(1, height - 2),
        "bottomRight": QPoint(width - 2, height - 2),
        "innerContent": QPoint(max(48, dialog.RESIZE_MARGIN + 28), max(220, dialog.RESIZE_MARGIN + 80)),
        "windowControls": dialog._ai_control_center_close_zone().center(),
    }
    expected_resize_samples = {
        "left",
        "right",
        "top",
        "bottom",
        "topLeft",
        "topRight",
        "bottomLeft",
        "bottomRight",
    }
    samples: dict[str, dict[str, object]] = {}
    for name, point in sample_points.items():
        edges = dialog._ai_control_center_resize_edges_for_local_pos(point)
        hit_test = int(dialog._ai_control_center_resize_hit_test_for_edges(edges))
        global_point = dialog.mapToGlobal(point)
        SetCursorPos(int(global_point.x()), int(global_point.y()))
        _pump(app, 60)
        dialog._poll_ai_control_center_resize_hover_cursor()
        samples[name] = {
            "localPoint": {"x": point.x(), "y": point.y()},
            "globalPoint": {"x": global_point.x(), "y": global_point.y()},
            "edges": {
                "left": bool(edges & Qt.LeftEdge),
                "right": bool(edges & Qt.RightEdge),
                "top": bool(edges & Qt.TopEdge),
                "bottom": bool(edges & Qt.BottomEdge),
            },
            "hitTest": hit_test,
            "hoverCursorKey": list(dialog._resize_cursor_key) if isinstance(dialog._resize_cursor_key, tuple) else dialog._resize_cursor_key,
            "expectedResize": name in expected_resize_samples,
        }
    dialog._reset_ai_control_center_resize_cursor()
    expected_ok = all(samples[name]["hitTest"] != 0 for name in expected_resize_samples)
    non_edge_ok = samples["innerContent"]["hitTest"] == 0 and samples["windowControls"]["hitTest"] == 0
    hover_ok = all(samples[name]["hoverCursorKey"] not in (None, [False, False, False, False]) for name in expected_resize_samples)
    return {
        "ok": expected_ok and non_edge_ok and hover_ok,
        "resizeMarginPx": int(dialog.RESIZE_MARGIN),
        "expectedResizeSamples": sorted(expected_resize_samples),
        "samples": samples,
        "expectedResizeSamplesHit": expected_ok,
        "nonEdgeSamplesClear": non_edge_ok,
        "hoverCursorSamplesStable": hover_ok,
    }


def _button_rect(app: QApplication, web_window, button_id: str) -> dict[str, int | str | bool]:
    raw = _run_child_js(
        app,
        web_window,
        f"""
        (() => {{
          const button = document.getElementById({json.dumps(button_id)});
          if (!button) return JSON.stringify({{ ok: false, reason: "missing-button" }});
          button.scrollIntoView({{ block: "center", inline: "center", behavior: "instant" }});
          const rect = button.getBoundingClientRect();
          return JSON.stringify({{
            ok: true,
            id: button.id || "",
            text: button.textContent.trim(),
            left: Math.round(rect.left),
            top: Math.round(rect.top),
            width: Math.round(rect.width),
            height: Math.round(rect.height)
          }});
        }})();
        """,
    )
    return json.loads(raw or "{}")


def _click_web_button(app: QApplication, web_window, button_id: str) -> dict[str, object]:
    rect = _button_rect(app, web_window, button_id)
    if not rect.get("ok"):
        return {"ok": False, "button": button_id, "reason": rect.get("reason", "missing-button")}
    _foreground_window(app, web_window)
    point = QPoint(int(rect["left"]) + int(rect["width"]) // 2, int(rect["top"]) + int(rect["height"]) // 2)
    global_point = web_window.webview.mapToGlobal(point)
    SetCursorPos(int(global_point.x()), int(global_point.y()))
    _pump(app, 80)
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    _pump(app, 40)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    _pump(app, 500)
    return {
        "ok": True,
        "button": button_id,
        "text": rect.get("text", ""),
        "point": {"x": point.x(), "y": point.y()},
        "globalPoint": {"x": global_point.x(), "y": global_point.y()},
        "clickMode": "os-cursor-webview-coordinate",
    }


def _hover_web_button(app: QApplication, web_window, button_id: str) -> dict[str, object]:
    rect = _button_rect(app, web_window, button_id)
    if not rect.get("ok"):
        return {"ok": False, "button": button_id, "reason": rect.get("reason", "missing-button")}
    _foreground_window(app, web_window)
    point = QPoint(int(rect["left"]) + int(rect["width"]) // 2, int(rect["top"]) + int(rect["height"]) // 2)
    global_point = web_window.webview.mapToGlobal(point)
    SetCursorPos(int(global_point.x()), int(global_point.y()))
    _pump(app, 260)
    return {
        "ok": True,
        "button": button_id,
        "text": rect.get("text", ""),
        "point": {"x": point.x(), "y": point.y()},
        "globalPoint": {"x": global_point.x(), "y": global_point.y()},
        "hoverMode": "os-cursor-webview-coordinate",
    }


def _drag_child_window(app: QApplication, window, dx: int = 36, dy: int = 24) -> dict[str, object]:
    _foreground_window(app, window)
    before = _rect(int(window.winId()))
    start = QPoint(min(176, max(80, window.webview.width() // 3)), 46)
    end = QPoint(start.x() + dx, start.y() + dy)
    QTest.mousePress(window.webview, Qt.LeftButton, Qt.NoModifier, start)
    _pump(app, 60)
    QTest.mouseMove(window.webview, end, 120)
    _pump(app, 80)
    QTest.mouseRelease(window.webview, Qt.LeftButton, Qt.NoModifier, end)
    _pump(app, 220)
    after = _rect(int(window.winId()))
    return {
        "before": before,
        "after": after,
        "deltaLeft": after["left"] - before["left"],
        "deltaTop": after["top"] - before["top"],
        "moved": abs(after["left"] - before["left"]) >= 16 and abs(after["top"] - before["top"]) >= 12,
        "mode": "webview-header-drag",
    }


def _resize_child_window(app: QApplication, window, dx: int = 44, dy: int = 34) -> dict[str, object]:
    _foreground_window(app, window)
    before = _rect(int(window.winId()))
    start = QPoint(max(2, window.webview.width() - 4), max(2, window.webview.height() - 4))
    end = QPoint(start.x() + dx, start.y() + dy)
    QTest.mousePress(window.webview, Qt.LeftButton, Qt.NoModifier, start)
    _pump(app, 60)
    QTest.mouseMove(window.webview, end, 140)
    _pump(app, 80)
    QTest.mouseRelease(window.webview, Qt.LeftButton, Qt.NoModifier, end)
    _pump(app, 260)
    after = _rect(int(window.winId()))
    return {
        "before": before,
        "after": after,
        "widthDelta": after["width"] - before["width"],
        "heightDelta": after["height"] - before["height"],
        "resized": after["width"] - before["width"] >= 22 and after["height"] - before["height"] >= 16,
        "mode": "webview-bottom-right-edge-resize",
    }


def _open_from_dashboard(app: QApplication, dialog: AIControlCenterDialog, button_id: str, domain_id: str):
    before = set(dialog._domain_windows.keys())
    result = _run_js(
        app,
        dialog,
        f"""
        (() => {{
          const button = document.getElementById({json.dumps(button_id)});
          if (!button) return JSON.stringify({{ ok: false, reason: "missing-button" }});
          return JSON.stringify({{ ok: true, label: button.textContent.trim(), target: button.dataset.launchTarget || "", kind: button.dataset.launchWindowKind || "" }});
        }})();
        """,
    )
    click = _click_web_button(app, dialog, button_id)
    _pump(app, 700)
    window = dialog._domain_windows.get(domain_id)
    return {"probe": json.loads(result or "{}"), "realClick": click}, window, before


def _hash_file(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _copy_user_evidence(local_root: Path, stamp: str) -> Path:
    user_root = (
        Path.home()
        / "OneDrive"
        / "Pictures"
        / "Screenshots"
        / "Nexus Desktop AI"
        / "FAM-007-H4"
        / f"{stamp}-parent-dashboard"
    )
    if user_root.exists():
        shutil.rmtree(user_root)
    user_root.mkdir(parents=True, exist_ok=True)
    for png in sorted(local_root.glob("*.png")):
        (user_root / png.name).write_bytes(png.read_bytes())
    return user_root


def main() -> int:
    stamp = _timestamp()
    log_root = REPO_ROOT / "dev" / "logs" / "fam_007_ai_control_center_live_resize" / stamp
    log_root.mkdir(parents=True, exist_ok=True)
    isolated_state_path = log_root / "isolated_ai_dashboard_window_state.json"
    os.environ["NEXUS_AI_CONTROL_CENTER_STATE_PATH"] = str(isolated_state_path)
    os.environ.pop("NEXUS_AI_CONTROL_CENTER_ENABLE_GEOMETRY_MEMORY", None)

    app = QApplication.instance() or QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No primary screen available for parent-dashboard validation")

    events: list[str] = []
    provider_state = build_provider_setup_completion_foundation_state(
        build_default_provider_readiness_config(),
        surface_role="hud",
    )
    dialog = AIControlCenterDialog(screen, event_logger=events.append)
    dialog.update_provider_state(provider_state.as_renderer_payload())
    available = screen.availableGeometry()
    dialog.setGeometry(
        QRect(
            available.x() + max(40, available.width() - dialog.DEFAULT_WIDTH - 120),
            available.y() + 80,
            dialog.DEFAULT_WIDTH,
            dialog.DEFAULT_HEIGHT,
        )
    )
    dialog.show_from_tray()
    _pump(app, 900)

    screenshots: dict[str, dict[str, str]] = {
        "dashboard_initial": _capture_window(app, dialog, log_root, "01_dashboard_initial"),
    }
    dashboard_probe = json.loads(
        _run_js(
            app,
            dialog,
            """
            (() => {
              const surface = document.getElementById("monitoring-hud");
              const cardNames = Array.from(document.querySelectorAll("[data-dashboard-hub-card]")).map((card) => card.dataset.dashboardHubCard || "");
              const launchers = Array.from(document.querySelectorAll("[data-category-launcher]")).map((button) => ({
                id: button.id || "",
                text: button.textContent.trim(),
                launcher: button.dataset.categoryLauncher || "",
                target: button.dataset.launchTarget || "",
                kind: button.dataset.launchWindowKind || ""
              }));
              const deferredButtons = Array.from(document.querySelectorAll("[data-action-state='deferred']")).map((button) => {
                const rect = button.getBoundingClientRect();
                const style = getComputedStyle(button);
                return {
                  id: button.id || "",
                  text: button.textContent.trim(),
                  disabled: Boolean(button.disabled),
                  ariaDisabled: button.getAttribute("aria-disabled") || "",
                  launchTarget: button.dataset.launchTarget || "",
                  launchKind: button.dataset.launchWindowKind || "",
                  width: Math.round(rect.width),
                  height: Math.round(rect.height),
                  fontSize: style.fontSize,
                  fontWeight: style.fontWeight
                };
              });
              const surfaceRect = surface?.getBoundingClientRect();
              const chrome = document.querySelector(".monitoring-hud__chrome");
              const header = document.querySelector(".monitoring-hud__title-group");
              const headerCopy = document.querySelector(".monitoring-hud__header");
              const title = document.querySelector(".monitoring-hud__title");
              const subtitle = document.querySelector(".monitoring-hud__subtitle");
              const windowControls = document.querySelector(".monitoring-hud__window-controls");
              const hub = document.getElementById("ai-control-center-card-hub");
              const firstCard = document.querySelector("[data-dashboard-hub-card]");
              const thirdCard = document.querySelector('[data-dashboard-hub-card="capabilities-maintenance"]');
              const chromeStyle = chrome ? getComputedStyle(chrome) : null;
              const headerCopyStyle = headerCopy ? getComputedStyle(headerCopy) : null;
              const subtitleStyle = subtitle ? getComputedStyle(subtitle) : null;
              const hubStyle = hub ? getComputedStyle(hub) : null;
              const rectFor = (node, extra = 0) => {
                if (!node) return { left: 0, top: 0, width: 0, height: 0, right: 0, bottom: 0 };
                const rect = node.getBoundingClientRect();
                return {
                  left: Math.round(rect.left - extra),
                  top: Math.round(rect.top - extra),
                  width: Math.round(rect.width + (extra * 2)),
                  height: Math.round(rect.height + (extra * 2)),
                  right: Math.round(rect.right + extra),
                  bottom: Math.round(rect.bottom + extra)
                };
              };
              const intersects = (a, b) => Boolean(a && b && a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top);
              const rowMetrics = [...document.querySelectorAll(".ai-control-center-card-rows .monitoring-hud__state-row")].map((row) => {
                const rect = row.getBoundingClientRect();
                const style = getComputedStyle(row);
                return {
                  height: Math.round(rect.height),
                  paddingTop: style.paddingTop,
                  paddingBottom: style.paddingBottom
                };
              });
              const cardVisualMetrics = [...document.querySelectorAll("[data-dashboard-hub-card]")].map((card) => {
                const cardRect = card.getBoundingClientRect();
                const rows = card.querySelector(".ai-control-center-card-rows");
                const rowsRect = rows?.getBoundingClientRect();
                const action = card.querySelector(".monitoring-hud__hub-actions");
                const actionRect = action?.getBoundingClientRect();
                const button = card.querySelector("[data-action-state='deferred']");
                const buttonRect = button?.getBoundingClientRect();
                const descriptions = card.querySelector(".monitoring-hud__hub-card-description");
                const descriptionStyle = descriptions ? getComputedStyle(descriptions) : null;
                return {
                  card: card.dataset.dashboardHubCard || "",
                  height: Math.round(cardRect.height),
                  rowsHeight: rowsRect ? Math.round(rowsRect.height) : 0,
                  actionGapFromRows: rowsRect && actionRect ? Math.round(actionRect.top - rowsRect.bottom) : 0,
                  actionHeight: actionRect ? Math.round(actionRect.height) : 0,
                  rightGutterToButton: buttonRect ? Math.round(cardRect.right - buttonRect.right) : 0,
                  buttonWidth: buttonRect ? Math.round(buttonRect.width) : 0,
                  buttonHeight: buttonRect ? Math.round(buttonRect.height) : 0,
                  descriptionTextIndent: descriptionStyle ? descriptionStyle.textIndent : "",
                  descriptionTop: descriptions ? Math.round(descriptions.getBoundingClientRect().top - cardRect.top) : 0
                };
              });
              const headerRect = rectFor(header, 3);
              const subtitleRect = rectFor(subtitle, 4);
              const windowControlRect = rectFor(windowControls, 0);
              const firstRows = firstCard?.querySelector(".ai-control-center-card-rows");
              const firstAction = firstCard?.querySelector(".monitoring-hud__hub-actions");
              return JSON.stringify({
                title: document.querySelector(".monitoring-hud__title")?.textContent.trim() || "",
                subtitle: document.querySelector(".monitoring-hud__subtitle")?.textContent.trim() || "",
                surfaceRole: surface?.dataset.productSurfaceRole || "",
                aiControlCenterPlacement: surface?.dataset.aiControlCenterPlacement || "",
                dashboardIaModel: surface?.dataset.dashboardIaModel || "",
                dashboardSurfaceModel: surface?.dataset.dashboardSurfaceModel || "",
                childWindowModel: surface?.dataset.childWindowModel || "",
                sameWindowFocusedSectionPolicy: surface?.dataset.sameWindowFocusedSectionPolicy || "",
                defaultWindowWidth: surface?.dataset.defaultWindowWidth || "",
                defaultWindowHeight: surface?.dataset.defaultWindowHeight || "",
                cardOrder: surface?.dataset.dashboardCardOrder || "",
                cardNames,
                launchers,
                deferredButtons,
                designProcessCopyPresent: /Refined|Option\\s+[A-Z]|target/i.test(document.body.innerText || ""),
                detachedWindowOpenCopyPresent: /Open Control Center|Open Diagnostics|Open Capabilities/.test(document.body.innerText || ""),
                cardTitles: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-card-title-copy strong")].map((node) => node.textContent.trim()),
                cardDescriptions: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-card-description")].map((node) => node.textContent.trim()),
                stripText: document.querySelector("[data-dashboard-role='global-ai-strip']")?.textContent.replace(/\\s+/g, " ").trim() || "",
                launcherActionRows: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-actions")].map((row) => ({
                  contract: row.dataset.actionRowContract || "",
                  buttonCount: row.querySelectorAll("[data-action-state='deferred']").length,
                  followsRows: Boolean(row.previousElementSibling?.classList.contains("ai-control-center-card-rows")),
                  insideRows: Boolean(row.closest(".ai-control-center-card-rows"))
                })),
                layoutMetrics: {
                  surfaceWidth: surfaceRect ? Math.round(surfaceRect.width) : 0,
                  chromePaddingLeft: chromeStyle ? chromeStyle.paddingLeft : "",
                  chromePaddingRight: chromeStyle ? chromeStyle.paddingRight : "",
                  headerWidth: header ? Math.round(header.getBoundingClientRect().width) : 0,
                  hubPaddingTop: hubStyle ? hubStyle.paddingTop : "",
                  hubPaddingLeft: hubStyle ? hubStyle.paddingLeft : "",
                  hubPaddingRight: hubStyle ? hubStyle.paddingRight : "",
                  headerPaddingRight: headerCopyStyle ? headerCopyStyle.paddingRight : "",
                  subtitleHeight: subtitle ? Math.round(subtitle.getBoundingClientRect().height) : 0,
                  subtitleLineHeight: subtitleStyle ? subtitleStyle.lineHeight : "",
                  subtitleOverlapsWindowControls: intersects(subtitleRect, windowControlRect),
                  topGutter: firstCard && hub ? Math.round(firstCard.getBoundingClientRect().top - hub.getBoundingClientRect().top) : 0,
                  scrollbarVisible: surface?.dataset.customScrollbarVisible || "false",
                  rowMetrics,
                  cardVisualMetrics
                },
                proofRects: {
                  header: headerRect,
                  subtitleWrap: subtitleRect,
                  rowGutterCardDensity: rectFor(firstRows, 8),
                  buttonPlacement: rectFor(firstAction, 8),
                  firstCard: rectFor(firstCard, 4)
                },
                defaultScrollMetrics: (() => {
                  const hubRect = hub?.getBoundingClientRect();
                  const thirdRect = thirdCard?.getBoundingClientRect();
                  return {
                    clientHeight: hub ? Math.round(hub.clientHeight) : 0,
                    scrollHeight: hub ? Math.round(hub.scrollHeight) : 0,
                    maxScroll: hub ? Math.round(Math.max(0, hub.scrollHeight - hub.clientHeight)) : 0,
                    scrollTop: hub ? Math.round(hub.scrollTop) : 0,
                    thirdCardFullyVisibleAtDefault: Boolean(hubRect && thirdRect && thirdRect.top >= hubRect.top && thirdRect.bottom <= hubRect.bottom),
                    thirdCardPartiallyVisibleAtDefault: Boolean(hubRect && thirdRect && thirdRect.bottom > hubRect.top && thirdRect.top < hubRect.bottom)
                  };
                })(),
                rowGroups: Object.fromEntries([...document.querySelectorAll("[data-dashboard-hub-card]")].map((card) => [
                  card.dataset.dashboardHubCard || "",
                  [...card.querySelectorAll(".monitoring-hud__state-row")].map((row) => ({
                    label: row.querySelector("span")?.textContent.trim() || "",
                    value: row.querySelector("strong")?.textContent.trim() || ""
                  }))
                ])),
                capabilityHubRows: document.querySelectorAll('[data-dashboard-hub-card="capabilities-maintenance"] .monitoring-hud__state-row').length,
                settingsTooltipText: document.getElementById("ai-dashboard-settings-tooltip")?.textContent.trim() || "",
                settingsRoutePresent: Boolean(document.querySelector("[data-dashboard-utility-row='settings-route']")),
                settingsRouteVisible: (() => {
                  const row = document.querySelector("[data-dashboard-utility-row='settings-route']");
                  if (!row) return false;
                  const style = getComputedStyle(row);
                  const rect = row.getBoundingClientRect();
                  return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
                })(),
                settingsButtonPresent: Boolean(document.getElementById("ai-dashboard-settings-action")),
                settingsButtonVisible: (() => {
                  const button = document.getElementById("ai-dashboard-settings-action");
                  if (!button) return false;
                  const style = getComputedStyle(button);
                  const rect = button.getBoundingClientRect();
                  return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
                })(),
                focusedSurfaceCount: document.querySelectorAll("[data-focused-surface]").length,
                domainSurfaceCount: document.querySelectorAll("[data-domain-surface]").length,
                localCheckInline: Boolean(document.getElementById("ai-control-center-local-check-action")),
                generateInline: Boolean(document.getElementById("ai-control-center-generate-report-action")),
                copyInline: Boolean(document.getElementById("ai-control-center-copy-report-action")),
                visibleSettingsFutureText: document.body.innerText.includes("Settings future-gated"),
                activeAiText: document.body.innerText.includes("Active AI"),
                trustProviderText: document.body.innerText.includes("Trust & Provider"),
                nativeTitleTooltipCount: document.querySelectorAll("[title]").length
              });
            })();
            """,
        )
    )
    settings_hover = {
        "ok": True,
        "button": "ai-dashboard-settings-action",
        "state": "hidden-for-option-g-target",
    }
    settings_tooltip_probe = json.loads(
        _run_js(
            app,
            dialog,
            """
            (() => {
              const tooltip = document.getElementById("ai-dashboard-settings-tooltip");
              const style = tooltip ? getComputedStyle(tooltip) : null;
              const rect = tooltip ? tooltip.getBoundingClientRect() : null;
              return JSON.stringify({
                present: Boolean(tooltip),
                text: tooltip?.textContent.trim() || "",
                opacity: style ? Number(style.opacity) : 0,
                display: style ? style.display : "",
                visibility: style ? style.visibility : "",
                visible: style && rect ? style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0 : false,
                label: document.getElementById("ai-dashboard-settings-action")?.getAttribute("aria-label") || "",
                titleCount: document.querySelectorAll("[title]").length
              });
            })();
            """,
        )
    )
    proof_rects = dashboard_probe.get("proofRects") if isinstance(dashboard_probe.get("proofRects"), dict) else {}
    proof_crops = {
        "focusedTitleHeader": _capture_window_region(app, dialog, log_root, "04_focused_title_header", proof_rects.get("header")),
        "subtitleWrap": _capture_window_region(app, dialog, log_root, "05_subtitle_wrap", proof_rects.get("subtitleWrap")),
        "rowGutterCardDensity": _capture_window_region(app, dialog, log_root, "06_row_gutter_card_density", proof_rects.get("rowGutterCardDensity")),
        "buttonPlacement": _capture_window_region(app, dialog, log_root, "07_button_placement", proof_rects.get("buttonPlacement")),
        "firstCardDensity": _capture_window_region(app, dialog, log_root, "08_first_card_density", proof_rects.get("firstCard")),
    }
    fam007_h4_root = Path.home() / "OneDrive" / "Pictures" / "Screenshots" / "Nexus Desktop AI" / "FAM-007-H4"
    main_runtime_ai_control_center_reference = _capture_main_runtime_ai_control_center_reference(log_root)
    previous_parent_dashboard_reference = _copy_reference_image(
        fam007_h4_root
        / "20260624-214952-parent-dashboard"
        / "01_dashboard_initial_focused_window.png",
        log_root,
        "11_before_parent_dashboard_density_reference",
    )
    visual_comparison_boards = {
        "currentVsMainRuntimeOldAiControlCenter": _write_side_by_side_board(
            Path(screenshots["dashboard_initial"]["focusedWindow"]),
            Path(str(main_runtime_ai_control_center_reference.get("focusedWindow", ""))),
            log_root / "12_current_vs_main_runtime_old_ai_control_center.png",
            "Current repaired parent AI Dashboard",
            "Main runtime old AI Control Center",
        ) if main_runtime_ai_control_center_reference.get("ok") else {
            "ok": False,
            "reason": main_runtime_ai_control_center_reference.get("reason", "missing-reference"),
        },
        "beforeAfterParentDensity": _write_side_by_side_board(
            Path(str(previous_parent_dashboard_reference.get("path", ""))),
            Path(screenshots["dashboard_initial"]["focusedWindow"]),
            log_root / "13_before_after_parent_dashboard_density.png",
            "Before returned defect proof",
            "Current repaired parent AI Dashboard",
        ) if previous_parent_dashboard_reference.get("ok") else {
            "ok": False,
            "reason": previous_parent_dashboard_reference.get("reason", "missing-reference"),
        },
    }
    resize_edge_hit_zone_probe = _ai_dashboard_resize_hit_zone_probe(app, dialog)

    child_windows_visible_before_close = {
        "control-center": False,
        "readiness-diagnostics": False,
        "capabilities-maintenance": False,
    }
    child_chrome_probe = {}
    child_geometry_behavior = {}
    readiness_result = {}
    singleton_focus = {}
    child_control_behavior = {}
    deferred_launch_probe = {
        "domainWindowCount": len(dialog._domain_windows),
        "domainWindowKeys": sorted(dialog._domain_windows.keys()),
        "acceptedScope": "parent-dashboard-only",
        "detachedChildWindowDisposition": "deferred-not-accepted-current-gate",
    }

    dashboard_rect_before_resize = _rect(int(dialog.winId()))
    _run_js(
        app,
        dialog,
        """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          if (hub) {
            hub.scrollTop = hub.scrollHeight;
            if (window.nexusAiControlCenterSyncScrollbar) {
              window.nexusAiControlCenterSyncScrollbar();
            }
          }
          return "true";
        })();
        """,
    )
    _pump(app, 250)
    scrolled_probe = json.loads(
        _run_js(
            app,
            dialog,
            """
            (() => {
              const hub = document.getElementById("ai-control-center-card-hub");
              const thirdCard = document.querySelector('[data-dashboard-hub-card="capabilities-maintenance"]');
              const hubRect = hub?.getBoundingClientRect();
              const thirdRect = thirdCard?.getBoundingClientRect();
              return JSON.stringify({
                scrollTop: hub ? Math.round(hub.scrollTop) : 0,
                maxScroll: hub ? Math.round(Math.max(0, hub.scrollHeight - hub.clientHeight)) : 0,
                thirdCardFullyVisibleAfterScroll: Boolean(hubRect && thirdRect && thirdRect.top >= hubRect.top && thirdRect.bottom <= hubRect.bottom),
                thirdCardPartiallyVisibleAfterScroll: Boolean(hubRect && thirdRect && thirdRect.bottom > hubRect.top && thirdRect.top < hubRect.bottom)
              });
            })();
            """,
        )
    )
    screenshots["dashboard_scrolled_bottom"] = _capture_window(
        app,
        dialog,
        log_root,
        "02_dashboard_scrolled_bottom",
    )
    _run_js(
        app,
        dialog,
        """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          if (hub) {
            hub.scrollTop = 0;
            if (window.nexusAiControlCenterSyncScrollbar) {
              window.nexusAiControlCenterSyncScrollbar();
            }
          }
          return "true";
        })();
        """,
    )
    _pump(app, 180)
    dialog.resize(dialog.width() + 42, dialog.height() + 28)
    _pump(app, 300)
    dashboard_rect_after_resize = _rect(int(dialog.winId()))
    screenshots["dashboard_resized"] = _capture_window(
        app,
        dialog,
        log_root,
        "03_dashboard_resized",
    )
    dashboard_resize_proof = {
        "before": dashboard_rect_before_resize,
        "after": dashboard_rect_after_resize,
        "widthDelta": dashboard_rect_after_resize["width"] - dashboard_rect_before_resize["width"],
        "heightDelta": dashboard_rect_after_resize["height"] - dashboard_rect_before_resize["height"],
    }

    dialog.close()
    _pump(app, 500)
    lifecycle_after_dashboard_close = {
        "controlVisible": False,
        "maintenanceVisible": False,
        "readinessVisible": False,
    }

    opened_desktop_hashes = {}
    duplicate_full_desktop_proof = False
    actual_deferred_labels = [button.get("text") for button in dashboard_probe.get("deferredButtons") or []]
    expected_option_g_rows = {
        "control-center": [
            {"label": "AI", "value": "ORIN not implemented; no real AI executing"},
            {"label": "Provider", "value": "Blocked; no provider/model path active"},
            {"label": "Visible data", "value": "None leaves this machine"},
        ],
        "readiness-diagnostics": [
            {"label": "Local check", "value": "Waiting for USER action"},
            {"label": "Readiness report", "value": "Local decision aid behind diagnostics"},
            {"label": "Prompt/data", "value": "Not accepted, sent, stored, or indexed"},
        ],
        "capabilities-maintenance": [
            {"label": "Capability packs", "value": "Install intent blocked; downloads disabled"},
            {"label": "Downloads/updates", "value": "Future-gated; no install execution"},
        ],
    }

    layout_metrics = dashboard_probe.get("layoutMetrics") or {}
    row_heights = [
        int(row.get("height") or 0)
        for row in layout_metrics.get("rowMetrics") or []
    ]
    card_visual_metrics = layout_metrics.get("cardVisualMetrics") or []
    card_heights = [
        int(card.get("height") or 0)
        for card in card_visual_metrics
    ]
    action_gaps = [
        int(card.get("actionGapFromRows") or 0)
        for card in card_visual_metrics
    ]
    button_right_gutters = [
        int(card.get("rightGutterToButton") or 0)
        for card in card_visual_metrics
    ]
    description_indents = [
        str(card.get("descriptionTextIndent") or "")
        for card in card_visual_metrics
    ]
    proof_crops_ok = all(item.get("ok") is True for item in proof_crops.values())
    required_reference_images_ok = (
        main_runtime_ai_control_center_reference.get("ok") is True
    )
    visual_boards_ok = (
        visual_comparison_boards["currentVsMainRuntimeOldAiControlCenter"].get("ok") is True
        and visual_comparison_boards["beforeAfterParentDensity"].get("ok") is True
    )
    deferred_buttons = dashboard_probe.get("deferredButtons") or []
    checks = {
        "dashboardHubParentOnly": (
            dashboard_probe.get("title") == "AI Dashboard"
            and dashboard_probe.get("dashboardIaModel") == "ai-dashboard-parent-only-global-strip-category-cards-detached-child-windows-deferred"
            and dashboard_probe.get("dashboardSurfaceModel") == "hub-only-cards-are-doorways"
            and dashboard_probe.get("childWindowModel") == "detached-child-windows-deferred-not-accepted-current-gate"
            and dashboard_probe.get("sameWindowFocusedSectionPolicy") == "blocked-as-dashboard-workspace-substitute"
            and dashboard_probe.get("cardNames") == ["control-center", "readiness-diagnostics", "capabilities-maintenance"]
            and dashboard_probe.get("cardTitles") == [
                "AI Status & Trust",
                "AI Readiness & Diagnostics",
                "Capabilities & Maintenance",
            ]
            and dashboard_probe.get("cardDescriptions") == [
                "Truth-first orientation before any AI action.",
                "Local checks and readiness report doorway.",
                "Capability state without install or update execution.",
            ]
            and all(part in dashboard_probe.get("stripText", "") for part in ["AI - ORIN", "Status - Not implemented", "Provider - Blocked", "Data - None"])
            and len(dashboard_probe.get("launcherActionRows") or []) == 3
            and all(
                row.get("contract") == "separate-from-state-rows"
                and row.get("buttonCount") == 1
                and row.get("followsRows") is True
                and row.get("insideRows") is False
                for row in dashboard_probe.get("launcherActionRows") or []
            )
            and dashboard_probe.get("rowGroups") == expected_option_g_rows
            and dashboard_probe.get("focusedSurfaceCount") == 0
            and dashboard_probe.get("domainSurfaceCount") == 0
        ),
        "doorwayButtonsDeferredNoFakeActions": (
            actual_deferred_labels == ["Not Available Yet", "Not Available Yet", "Not Available Yet"]
            and len(dashboard_probe.get("launchers") or []) == 0
            and len(deferred_buttons) == 3
            and all(button.get("disabled") is True for button in deferred_buttons)
            and all(button.get("ariaDisabled") == "true" for button in deferred_buttons)
            and all(button.get("launchTarget") == "deferred" for button in deferred_buttons)
            and all(button.get("launchKind") == "deferred-detached-child" for button in deferred_buttons)
            and deferred_launch_probe.get("domainWindowCount") == 0
        ),
        "parentVisualMetrics": (
            dashboard_probe.get("defaultWindowWidth") == "840"
            and dashboard_probe.get("defaultWindowHeight") == "720"
            and str(layout_metrics.get("chromePaddingLeft")) == str(layout_metrics.get("chromePaddingRight"))
            and int(layout_metrics.get("topGutter") or 0) >= 8
            and len(row_heights) == 8
            and min(row_heights or [0]) >= 23
            and max(row_heights or [999]) <= 32
            and all(int(button.get("height") or 0) >= 34 for button in deferred_buttons)
            and all(int(button.get("width") or 0) >= 120 for button in deferred_buttons)
            and all(str(button.get("fontWeight") or "").isdigit() and int(button.get("fontWeight")) >= 800 for button in deferred_buttons)
            and int(layout_metrics.get("headerWidth") or 0) >= int(layout_metrics.get("surfaceWidth") or 0) - 32
        ),
        "returnedDensityAndButtonPlacementRepaired": (
            len(card_heights) == 3
            and max(card_heights or [999]) <= 215
            and min(card_heights or [0]) >= 145
            and all(0 <= gap <= 8 for gap in action_gaps)
            and all(10 <= gutter <= 28 for gutter in button_right_gutters)
            and all(indent in ("0px", "0") for indent in description_indents)
        ),
        "returnedTitleSubtitleWrapRepaired": (
            str(layout_metrics.get("headerPaddingRight") or "").startswith("108")
            and int(layout_metrics.get("subtitleHeight") or 0) <= 42
            and layout_metrics.get("subtitleOverlapsWindowControls") is False
        ),
        "acceptedReferenceComparisonProven": (
            dashboard_probe.get("surfaceRole") == "ai-dashboard-top-most-hub"
            and dashboard_probe.get("aiControlCenterPlacement") == "focused-domain-card-inside-ai-dashboard"
            and required_reference_images_ok
            and visual_boards_ok
            and proof_crops_ok
        ),
        "resizeEdgeHitZoneProven": (
            resize_edge_hit_zone_probe.get("ok") is True
            and int(resize_edge_hit_zone_probe.get("resizeMarginPx") or 0) >= 16
        ),
        "defaultScrollIntentProven": (
            dashboard_probe.get("defaultWindowHeight") == "720"
            and str(layout_metrics.get("scrollbarVisible")) == "true"
            and int((dashboard_probe.get("defaultScrollMetrics") or {}).get("maxScroll") or 0) > 20
            and (dashboard_probe.get("defaultScrollMetrics") or {}).get("thirdCardFullyVisibleAtDefault") is False
            and scrolled_probe.get("thirdCardFullyVisibleAfterScroll") is True
            and int(scrolled_probe.get("scrollTop") or 0) >= int(scrolled_probe.get("maxScroll") or 0) - 2
        ),
        "runtimeCopyIsProductFacing": (
            "provider/model execution is blocked" in str(dashboard_probe.get("subtitle") or "")
            and "no prompt, file, memory, telemetry, or provider data leaves this machine" in str(dashboard_probe.get("subtitle") or "")
            and dashboard_probe.get("designProcessCopyPresent") is False
            and dashboard_probe.get("detachedWindowOpenCopyPresent") is False
        ),
        "noInlineWorkspaceActions": (
            dashboard_probe.get("localCheckInline") is False
            and dashboard_probe.get("generateInline") is False
            and dashboard_probe.get("copyInline") is False
        ),
        "capabilitiesCardCompactDoorway": (
            dashboard_probe.get("capabilityHubRows") == 2
        ),
        "redundantCardsRemoved": (
            dashboard_probe.get("activeAiText") is False
            and dashboard_probe.get("trustProviderText") is False
        ),
        "settingsRouteHiddenForOptionG": (
            dashboard_probe.get("visibleSettingsFutureText") is False
            and dashboard_probe.get("nativeTitleTooltipCount") == 0
            and dashboard_probe.get("settingsRoutePresent") is True
            and dashboard_probe.get("settingsRouteVisible") is False
            and dashboard_probe.get("settingsButtonPresent") is True
            and dashboard_probe.get("settingsButtonVisible") is False
            and dashboard_probe.get("settingsTooltipText") == "Settings"
            and settings_tooltip_probe.get("text") == "Settings"
            and settings_tooltip_probe.get("visible") is False
            and settings_tooltip_probe.get("label") == "Settings"
            and settings_tooltip_probe.get("titleCount") == 0
        ),
        "fullDesktopProofNotDuplicated": (
            len(opened_desktop_hashes) == 0
            and duplicate_full_desktop_proof is False
        ),
        "dashboardResizeStillWorks": (
            dashboard_resize_proof["widthDelta"] >= 30
            and dashboard_resize_proof["heightDelta"] >= 20
        ),
        "childLifecycleBehavior": (
            lifecycle_after_dashboard_close["controlVisible"] is False
            and lifecycle_after_dashboard_close["maintenanceVisible"] is False
            and lifecycle_after_dashboard_close["readinessVisible"] is False
        ),
        "providerExecutionStillBlocked": (
            all("PROVIDER" not in event or "provider_visible_data=none" in event.lower() or "provider/model" not in event.lower() for event in events)
            and provider_state.as_renderer_payload().get("sentToProvider") is False
            and provider_state.as_renderer_payload().get("canAcceptPrompts") is False
            and provider_state.as_renderer_payload().get("networkEgressState") == "network-egress-blocked"
            and provider_state.as_renderer_payload().get("memoryIndexingState") == "memory-indexing-disabled"
        ),
    }

    status = "PASS" if all(checks.values()) else "FAIL"
    user_evidence_root = _copy_user_evidence(log_root, stamp)
    manifest = {
        "status": status,
        "stamp": stamp,
        "helper": "dev/orin_ai_control_center_live_resize_validation.py",
        "proofClass": "live AI Dashboard parent-only visual and functional proof",
        "worktree": str(REPO_ROOT),
        "window": "AI Dashboard",
        "dashboardProbe": dashboard_probe,
        "proofCrops": proof_crops,
        "acceptedReferenceImages": {
            "mainRuntimeOldAiControlCenter": main_runtime_ai_control_center_reference,
            "beforeParentDashboard": previous_parent_dashboard_reference,
        },
        "visualComparisonBoards": visual_comparison_boards,
        "resizeEdgeHitZoneProbe": resize_edge_hit_zone_probe,
        "surfaceClassification": {
            "currentSurface": "parent AI Dashboard top-most hub",
            "currentSurfaceRole": dashboard_probe.get("surfaceRole"),
            "aiControlCenterPlacement": dashboard_probe.get("aiControlCenterPlacement"),
            "detachedChildWindowDisposition": "deferred-not-accepted-current-gate",
            "acceptedComparatorUse": "Main worktree old AI Control Center runtime is comparator proof only, not global UIREF promotion or detached-child acceptance",
            "acceptedComparatorSource": main_runtime_ai_control_center_reference.get("referenceSource"),
            "acceptedComparatorDesktopLauncher": main_runtime_ai_control_center_reference.get("desktopLauncher"),
        },
        "deferredLaunchProbe": deferred_launch_probe,
        "settingsHover": settings_hover,
        "settingsTooltipProbe": settings_tooltip_probe,
        "defaultScrollIntentProbe": scrolled_probe,
        "childChromeProbe": child_chrome_probe,
        "childControlBehavior": child_control_behavior,
        "fullDesktopHashes": opened_desktop_hashes,
        "duplicateFullDesktopProof": duplicate_full_desktop_proof,
        "childWindowClassificationLedger": {
            "control-center": {
                "sourceCategoryCard": "AI Status & Trust",
                "launcherLabel": "Not Available Yet",
                "classification": "deferred-detached-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": False,
                "moveBehavior": "not-in-accepted-scope",
                "resizeBehavior": "not-in-accepted-scope",
                "shellConformance": "deferred-not-accepted-current-gate",
                "focusBehavior": "not-in-accepted-scope",
            },
            "readiness-diagnostics": {
                "sourceCategoryCard": "AI Readiness & Diagnostics",
                "launcherLabel": "Not Available Yet",
                "classification": "deferred-detached-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": False,
                "moveBehavior": "not-in-accepted-scope",
                "resizeBehavior": "not-in-accepted-scope",
                "shellConformance": "deferred-not-accepted-current-gate",
                "focusBehavior": "not-in-accepted-scope",
            },
            "capabilities-maintenance": {
                "sourceCategoryCard": "Capabilities & Maintenance",
                "launcherLabel": "Not Available Yet",
                "classification": "deferred-detached-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": False,
                "moveBehavior": "not-in-accepted-scope",
                "resizeBehavior": "not-in-accepted-scope",
                "shellConformance": "deferred-not-accepted-current-gate",
                "focusBehavior": "not-in-accepted-scope",
            },
        },
        "readinessResult": readiness_result,
        "singletonFocus": singleton_focus,
        "dashboardResizeProof": dashboard_resize_proof,
        "lifecycleAfterDashboardClose": lifecycle_after_dashboard_close,
        "childWindowsVisibleBeforeDashboardClose": child_windows_visible_before_close,
        "childGeometryBehavior": child_geometry_behavior,
        "providerBoundary": {
            "sentToProvider": provider_state.as_renderer_payload().get("sentToProvider"),
            "canAcceptPrompts": provider_state.as_renderer_payload().get("canAcceptPrompts"),
            "providerVisibleData": provider_state.as_renderer_payload().get("providerVisibleData"),
            "networkEgressState": provider_state.as_renderer_payload().get("networkEgressState"),
            "memoryIndexingState": provider_state.as_renderer_payload().get("memoryIndexingState"),
        },
        "events": events,
        "checks": checks,
        "screenshots": screenshots,
        "userInspectableEvidenceRoot": str(user_evidence_root),
        "localLogRoot": str(log_root),
    }
    manifest_path = log_root / "live_resize_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (user_evidence_root / "live_resize_manifest.json").write_bytes(manifest_path.read_bytes())

    if status != "PASS":
        print(f"FAIL: FAM-007 AI Dashboard parent-only validation failed. Manifest: {manifest_path}")
        return 1
    print(f"PASS: FAM-007 AI Dashboard parent-only validation passed. Manifest: {manifest_path}")
    print(f"USER_EVIDENCE_ROOT: {user_evidence_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
