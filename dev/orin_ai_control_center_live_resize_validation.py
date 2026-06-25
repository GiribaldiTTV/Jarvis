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
import sys
import time
from pathlib import Path

from PySide6.QtCore import QPoint, QRect, Qt
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
              const hub = document.getElementById("ai-control-center-card-hub");
              const firstCard = document.querySelector("[data-dashboard-hub-card]");
              const thirdCard = document.querySelector('[data-dashboard-hub-card="capabilities-maintenance"]');
              const chromeStyle = chrome ? getComputedStyle(chrome) : null;
              const hubStyle = hub ? getComputedStyle(hub) : null;
              const rowMetrics = [...document.querySelectorAll(".ai-control-center-card-rows .monitoring-hud__state-row")].map((row) => {
                const rect = row.getBoundingClientRect();
                const style = getComputedStyle(row);
                return {
                  height: Math.round(rect.height),
                  paddingTop: style.paddingTop,
                  paddingBottom: style.paddingBottom
                };
              });
              return JSON.stringify({
                title: document.querySelector(".monitoring-hud__title")?.textContent.trim() || "",
                subtitle: document.querySelector(".monitoring-hud__subtitle")?.textContent.trim() || "",
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
                  topGutter: firstCard && hub ? Math.round(firstCard.getBoundingClientRect().top - hub.getBoundingClientRect().top) : 0,
                  scrollbarVisible: surface?.dataset.customScrollbarVisible || "false",
                  rowMetrics
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
            and min(row_heights or [0]) >= 29
            and all(int(button.get("height") or 0) >= 34 for button in deferred_buttons)
            and all(int(button.get("width") or 0) >= 120 for button in deferred_buttons)
            and all(str(button.get("fontWeight") or "").isdigit() and int(button.get("fontWeight")) >= 800 for button in deferred_buttons)
            and int(layout_metrics.get("headerWidth") or 0) >= int(layout_metrics.get("surfaceWidth") or 0) - 32
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
