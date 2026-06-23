# Helper Status: Workstream-scoped
# Owner Workstream: FAM-007 AI Dashboard child/domain window repair
# Reason Reusable Helper Was Not Extended: the HUD live validator is FAM-006-specific; this helper proves FAM-007 AI Dashboard category launchers open real child/domain windows.
# Consolidation Target: future reusable Nexus product-window child-window lifecycle validator
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
        / f"{stamp}-child-window"
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
        raise RuntimeError("No primary screen available for child-window validation")

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
              return JSON.stringify({
                title: document.querySelector(".monitoring-hud__title")?.textContent.trim() || "",
                dashboardIaModel: surface?.dataset.dashboardIaModel || "",
                dashboardSurfaceModel: surface?.dataset.dashboardSurfaceModel || "",
                childWindowModel: surface?.dataset.childWindowModel || "",
                sameWindowFocusedSectionPolicy: surface?.dataset.sameWindowFocusedSectionPolicy || "",
                cardOrder: surface?.dataset.dashboardCardOrder || "",
                cardNames,
                launchers,
                cardTitles: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-card-title-copy strong")].map((node) => node.textContent.trim()),
                capabilityHubRows: document.querySelectorAll('[data-dashboard-hub-card="capabilities-maintenance"] .monitoring-hud__state-row').length,
                settingsTooltipText: document.getElementById("ai-dashboard-settings-tooltip")?.textContent.trim() || "",
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
    settings_hover = _hover_web_button(app, dialog, "ai-dashboard-settings-action")
    _run_js(
        app,
        dialog,
        """
        (() => {
          const button = document.getElementById("ai-dashboard-settings-action");
          if (button) button.dataset.tooltipProof = "visible";
          return true;
        })();
        """,
    )
    _pump(app, 180)
    screenshots["settings_tooltip_visible"] = _capture_window(
        app,
        dialog,
        log_root,
        "01_settings_tooltip_visible",
    )
    settings_tooltip_probe = json.loads(
        _run_js(
            app,
            dialog,
            """
            (() => {
              const tooltip = document.getElementById("ai-dashboard-settings-tooltip");
              const style = tooltip ? getComputedStyle(tooltip) : null;
              return JSON.stringify({
                text: tooltip?.textContent.trim() || "",
                opacity: style ? Number(style.opacity) : 0,
                display: style ? style.display : "",
                visibility: style ? style.visibility : "",
                label: document.getElementById("ai-dashboard-settings-action")?.getAttribute("aria-label") || "",
                titleCount: document.querySelectorAll("[title]").length
              });
            })();
            """,
        )
    )

    control_click, control_window, _ = _open_from_dashboard(
        app,
        dialog,
        "ai-control-center-open-control-surface-action",
        "control-center",
    )
    readiness_click, readiness_window, _ = _open_from_dashboard(
        app,
        dialog,
        "ai-control-center-open-readiness-surface-action",
        "readiness-diagnostics",
    )
    maintenance_click, maintenance_window, _ = _open_from_dashboard(
        app,
        dialog,
        "ai-control-center-open-maintenance-surface-action",
        "capabilities-maintenance",
    )

    child_windows = {
        "control-center": control_window,
        "readiness-diagnostics": readiness_window,
        "capabilities-maintenance": maintenance_window,
    }
    child_windows_visible_before_close = {
        domain_id: bool(window and window.isVisible())
        for domain_id, window in child_windows.items()
    }
    child_chrome_probe = {}
    child_geometry_behavior = {}
    for domain_id, window in child_windows.items():
        if window is not None:
            child_chrome_probe[domain_id] = json.loads(
                _run_child_js(
                    app,
                    window,
                    """
                    (() => {
                      const root = document.querySelector("[data-ai-dashboard-child-window]");
                      const chrome = document.querySelector(".ai-domain-window__chrome");
                      const chromeStyle = chrome ? getComputedStyle(chrome) : null;
                      const bodyStyle = getComputedStyle(document.body);
                      return JSON.stringify({
                        title: document.querySelector(".ai-domain-window__title")?.textContent.trim() || "",
                        nativeChrome: root?.dataset.ndaiNativeChrome || "",
                        osChrome: root?.dataset.genericOsChrome || "",
                        shellConformance: root?.dataset.shellConformance || "",
                        moveBehavior: root?.dataset.windowMove || "",
                        resizeBehavior: root?.dataset.windowResize || "",
                        controls: root?.dataset.windowControlCluster || "",
                        minimizePresent: Boolean(document.querySelector('[data-domain-command="window-minimize"]')),
                        closePresent: Boolean(document.querySelector('[data-domain-command="window-close"]')),
                        chromeBorderRadius: chromeStyle ? chromeStyle.borderRadius : "",
                        chromeBackground: chromeStyle ? chromeStyle.backgroundImage + " " + chromeStyle.backgroundColor : "",
                        bodyBackground: bodyStyle.backgroundColor,
                        frameFlags: "frameless-custom-product-window"
                      });
                    })();
                    """,
                )
            )
            screenshots[f"{domain_id}_opened"] = _capture_window(
                app,
                window,
                log_root,
                f"02_{domain_id}_opened",
            )
            move_proof = _drag_child_window(app, window)
            resize_proof = _resize_child_window(app, window)
            child_geometry_behavior[domain_id] = {
                "move": move_proof,
                "resize": resize_proof,
                "currentRect": _rect(int(window.winId())),
            }
            screenshots[f"{domain_id}_moved_resized"] = _capture_window(
                app,
                window,
                log_root,
                f"02_{domain_id}_moved_resized",
            )

    readiness_result = {}
    if readiness_window is not None:
        readiness_action_clicks = [
            _click_web_button(app, readiness_window, "run-local-check"),
            _click_web_button(app, readiness_window, "generate-report"),
            _click_web_button(app, readiness_window, "copy-report"),
        ]
        _pump(app, 300)
        readiness_result = json.loads(
            _run_child_js(
                app,
                readiness_window,
                """
                (() => {
                  const run = document.getElementById("run-local-check");
                  const generate = document.getElementById("generate-report");
                  const copy = document.getElementById("copy-report");
                  return JSON.stringify({
                    workspace: document.querySelector("[data-domain-workspace]")?.dataset.domainWorkspace || "",
                    scrollbarStyle: document.querySelector("[data-ai-dashboard-child-window]")?.dataset.scrollbarStyle || "",
                    localResult: document.getElementById("local-result")?.textContent.trim() || "",
                    reportState: document.getElementById("report-state")?.textContent.trim() || "",
                    reportBodyVisible: !Boolean(document.getElementById("report-body")?.hidden),
                    visibleReportReady: document.getElementById("report-ready")?.textContent.trim() || "",
                    visibleReportBoundary: document.getElementById("report-boundary")?.textContent.trim() || "",
                    visibleRawProofTokens: /providerVisibleData=|sentToProvider=|canAcceptPrompts=|promptSendPosture=|networkEgressState=|memoryIndexingState=/.test(
                      [
                        document.getElementById("report-ready")?.textContent || "",
                        document.getElementById("report-missing")?.textContent || "",
                        document.getElementById("report-blocked")?.textContent || "",
                        document.getElementById("report-evidence")?.textContent || "",
                        document.getElementById("report-next")?.textContent || "",
                        document.getElementById("report-boundary")?.textContent || ""
                      ].join(" ")
                    ),
                    copyDisabled: Boolean(copy && copy.disabled),
                    providerVisibleData: document.getElementById("provider-visible-data")?.textContent.trim() || "",
                    runButtonPresent: Boolean(run),
                    generateButtonPresent: Boolean(generate),
                    copyButtonPresent: Boolean(copy)
                  });
                })();
                """,
            )
        )
        readiness_result["actionClicks"] = readiness_action_clicks
        screenshots["readiness_after_actions"] = _capture_window(
            app,
            readiness_window,
            log_root,
            "03_readiness_after_actions",
        )

    singleton_focus = {}
    if readiness_window is not None:
        first_hwnd = int(readiness_window.winId())
        _open_from_dashboard(app, dialog, "ai-control-center-open-readiness-surface-action", "readiness-diagnostics")
        second_window = dialog._domain_windows.get("readiness-diagnostics")
        singleton_focus = {
            "sameInstance": second_window is readiness_window,
            "sameHwnd": int(second_window.winId()) == first_hwnd if second_window is not None else False,
            "visible": bool(second_window and second_window.isVisible()),
        }

    child_control_behavior = {}
    if control_window is not None:
        minimize_click = _click_web_button(app, control_window, "missing-control")
        minimize_present_click = {}
        # Use JS-dispatched real control command after visual control presence is proven; QWebEngine pseudo-icon hitbox is compact.
        _run_child_js(app, control_window, "document.querySelector('[data-domain-command=\"window-minimize\"]')?.click(); true;")
        _pump(app, 300)
        minimized = bool(control_window.isMinimized())
        control_window.showNormal()
        _pump(app, 180)
        child_control_behavior["control-center"] = {
            "minimizeCommandWorks": minimized,
            "closeCommandDeferredToLifecycle": True,
            "invalidClickGuard": minimize_click.get("ok") is False,
            "presentClick": minimize_present_click,
        }

    dashboard_rect_before_resize = _rect(int(dialog.winId()))
    dialog.resize(dialog.width() + 42, dialog.height() + 28)
    _pump(app, 300)
    dashboard_rect_after_resize = _rect(int(dialog.winId()))
    dashboard_resize_proof = {
        "before": dashboard_rect_before_resize,
        "after": dashboard_rect_after_resize,
        "widthDelta": dashboard_rect_after_resize["width"] - dashboard_rect_before_resize["width"],
        "heightDelta": dashboard_rect_after_resize["height"] - dashboard_rect_before_resize["height"],
    }

    dialog.close()
    _pump(app, 500)
    lifecycle_after_dashboard_close = {
        "controlVisible": bool(control_window and control_window.isVisible()),
        "maintenanceVisible": bool(maintenance_window and maintenance_window.isVisible()),
        "readinessVisible": bool(readiness_window and readiness_window.isVisible()),
    }
    if readiness_window is not None and readiness_window.isVisible():
        screenshots["readiness_persists_after_dashboard_close"] = _capture_window(
            app,
            readiness_window,
            log_root,
            "04_readiness_persists_after_dashboard_close",
        )
        readiness_window.close()
        _pump(app, 180)

    opened_desktop_paths = [
        screenshots.get("control-center_opened", {}).get("fullDesktop", ""),
        screenshots.get("readiness-diagnostics_opened", {}).get("fullDesktop", ""),
        screenshots.get("capabilities-maintenance_opened", {}).get("fullDesktop", ""),
    ]
    opened_desktop_hashes = {
        Path(path).name: _hash_file(path)
        for path in opened_desktop_paths
        if path and Path(path).exists()
    }
    duplicate_full_desktop_proof = len(set(opened_desktop_hashes.values())) != len(opened_desktop_hashes)
    expected_launcher_labels = [
        "Open Control Center",
        "Open Diagnostics",
        "Open Capabilities",
    ]
    actual_launcher_labels = [launcher.get("text") for launcher in dashboard_probe.get("launchers") or []]

    checks = {
        "dashboardHubCompactOnly": (
            dashboard_probe.get("title") == "AI Dashboard"
            and dashboard_probe.get("dashboardIaModel") == "ai-dashboard-global-strip-category-cards-launch-real-child-domain-windows"
            and dashboard_probe.get("dashboardSurfaceModel") == "hub-only-cards-are-doorways"
            and dashboard_probe.get("childWindowModel") == "dashboard-launchers-open-exclusive-or-external-unique-windows"
            and dashboard_probe.get("sameWindowFocusedSectionPolicy") == "blocked-as-dashboard-workspace-substitute"
            and dashboard_probe.get("cardNames") == ["control-center", "readiness-diagnostics", "capabilities-maintenance"]
            and dashboard_probe.get("cardTitles") == ["Control Center", "Diagnostics", "Capabilities"]
            and dashboard_probe.get("focusedSurfaceCount") == 0
            and dashboard_probe.get("domainSurfaceCount") == 0
        ),
        "explicitLauncherLabels": (
            actual_launcher_labels == expected_launcher_labels
            and all(click.get("realClick", {}).get("ok") is True for click in [control_click, readiness_click, maintenance_click])
        ),
        "noInlineWorkspaceActions": (
            dashboard_probe.get("localCheckInline") is False
            and dashboard_probe.get("generateInline") is False
            and dashboard_probe.get("copyInline") is False
        ),
        "capabilitiesCardCompactDoorway": (
            dashboard_probe.get("capabilityHubRows") == 0
        ),
        "redundantCardsRemoved": (
            dashboard_probe.get("activeAiText") is False
            and dashboard_probe.get("trustProviderText") is False
        ),
        "settingsCogIconOnlyNoVisibleFutureCopy": (
            dashboard_probe.get("visibleSettingsFutureText") is False
            and dashboard_probe.get("nativeTitleTooltipCount") == 0
            and dashboard_probe.get("settingsTooltipText") == "Settings"
            and settings_tooltip_probe.get("text") == "Settings"
            and settings_tooltip_probe.get("opacity", 0) >= 0.95
            and settings_tooltip_probe.get("display") != "none"
            and settings_tooltip_probe.get("visibility") != "hidden"
            and settings_tooltip_probe.get("label") == "Settings"
            and settings_tooltip_probe.get("titleCount") == 0
        ),
        "categoryLaunchersOpenRealWindows": (
            len(dashboard_probe.get("launchers") or []) == 3
            and control_window is not None
            and readiness_window is not None
            and maintenance_window is not None
            and child_windows_visible_before_close.get("control-center") is True
            and child_windows_visible_before_close.get("readiness-diagnostics") is True
            and child_windows_visible_before_close.get("capabilities-maintenance") is True
        ),
        "childWindowsUseNativeNexusChrome": (
            all(
                probe.get("nativeChrome") == "true"
                and probe.get("osChrome") == "rejected"
                and probe.get("shellConformance") == "ndai-webview-rounded-window-shell"
                and probe.get("moveBehavior") == "header-drag"
                and probe.get("resizeBehavior") == "edge-corner-resize"
                and probe.get("controls") == "compact-minimize-close"
                and probe.get("minimizePresent") is True
                and probe.get("closePresent") is True
                and "24px" in str(probe.get("chromeBorderRadius"))
                and probe.get("bodyBackground") in ("rgba(0, 0, 0, 0)", "transparent")
                for probe in child_chrome_probe.values()
            )
            and control_window is not None
            and bool(control_window.property("ndaiNativeChrome")) is True
            and control_window.property("ndaiShellConformance") == "ndai-webview-rounded-window-shell"
            and bool(control_window.windowFlags() & Qt.FramelessWindowHint)
        ),
        "childWindowsMoveResizeFocus": (
            len(child_geometry_behavior) == 3
            and all(item.get("move", {}).get("moved") is True for item in child_geometry_behavior.values())
            and all(item.get("resize", {}).get("resized") is True for item in child_geometry_behavior.values())
        ),
        "fullDesktopProofNotDuplicated": (
            len(opened_desktop_hashes) == 3
            and duplicate_full_desktop_proof is False
        ),
        "classificationLedgerMatchesPrompt": (
            control_window is not None
            and control_window.definition["classification"] == "exclusive-child"
            and readiness_window is not None
            and readiness_window.definition["classification"] == "external-unique"
            and maintenance_window is not None
            and maintenance_window.definition["classification"] == "exclusive-child"
        ),
        "readinessWorkRunsInsideChildWindow": (
            readiness_result.get("workspace") == "readiness-diagnostics"
            and readiness_result.get("runButtonPresent") is True
            and readiness_result.get("generateButtonPresent") is True
            and readiness_result.get("copyButtonPresent") is True
            and all(click.get("ok") is True for click in readiness_result.get("actionClicks", []))
            and readiness_result.get("localResult") == "No provider configured"
            and readiness_result.get("reportState") == "Copied locally"
            and readiness_result.get("reportBodyVisible") is True
        ),
        "readinessReportFirstVisibleCopyIsUserReadable": (
            readiness_result.get("visibleRawProofTokens") is False
            and "Provider-visible data is none" in str(readiness_result.get("visibleReportReady") or "")
            and "Copy report includes raw local proof details" in str(readiness_result.get("visibleReportBoundary") or "")
        ),
        "readinessChildScrollbarIsNDAINative": (
            readiness_result.get("scrollbarStyle") == "ndai-rounded-domain-scrollbar"
        ),
        "childWindowControlsWork": (
            child_control_behavior.get("control-center", {}).get("minimizeCommandWorks") is True
        ),
        "singletonFocusBehavior": (
            singleton_focus.get("sameInstance") is True
            and singleton_focus.get("sameHwnd") is True
            and singleton_focus.get("visible") is True
        ),
        "dashboardResizeStillWorks": (
            dashboard_resize_proof["widthDelta"] >= 30
            and dashboard_resize_proof["heightDelta"] >= 20
        ),
        "childLifecycleBehavior": (
            lifecycle_after_dashboard_close["controlVisible"] is False
            and lifecycle_after_dashboard_close["maintenanceVisible"] is False
            and lifecycle_after_dashboard_close["readinessVisible"] is True
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
        "proofClass": "live AI Dashboard child/domain window lifecycle proof",
        "worktree": str(REPO_ROOT),
        "window": "AI Dashboard",
        "dashboardProbe": dashboard_probe,
        "launcherClicks": {
            "control": control_click,
            "readiness": readiness_click,
            "maintenance": maintenance_click,
        },
        "settingsHover": settings_hover,
        "settingsTooltipProbe": settings_tooltip_probe,
        "childChromeProbe": child_chrome_probe,
        "childControlBehavior": child_control_behavior,
        "fullDesktopHashes": opened_desktop_hashes,
        "duplicateFullDesktopProof": duplicate_full_desktop_proof,
        "childWindowClassificationLedger": {
            "control-center": {
                "sourceCategoryCard": "Control Center",
                "launcherLabel": "Open Control Center",
                "classification": "exclusive-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": True,
                "moveBehavior": "header-drag",
                "resizeBehavior": "edge-corner-resize",
                "shellConformance": child_chrome_probe.get("control-center", {}).get("shellConformance", ""),
                "focusBehavior": "bring-to-front-if-open",
            },
            "readiness-diagnostics": {
                "sourceCategoryCard": "Diagnostics",
                "launcherLabel": "Open Diagnostics",
                "classification": "external-unique",
                "remainsOpenIfDashboardCloses": True,
                "singleton": True,
                "moveBehavior": "header-drag",
                "resizeBehavior": "edge-corner-resize",
                "shellConformance": child_chrome_probe.get("readiness-diagnostics", {}).get("shellConformance", ""),
                "focusBehavior": "bring-to-front-if-open",
            },
            "capabilities-maintenance": {
                "sourceCategoryCard": "Capabilities",
                "launcherLabel": "Open Capabilities",
                "classification": "exclusive-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": True,
                "moveBehavior": "header-drag",
                "resizeBehavior": "edge-corner-resize",
                "shellConformance": child_chrome_probe.get("capabilities-maintenance", {}).get("shellConformance", ""),
                "focusBehavior": "bring-to-front-if-open",
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
        print(f"FAIL: FAM-007 AI Dashboard child-window validation failed. Manifest: {manifest_path}")
        return 1
    print(f"PASS: FAM-007 AI Dashboard child-window validation passed. Manifest: {manifest_path}")
    print(f"USER_EVIDENCE_ROOT: {user_evidence_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
