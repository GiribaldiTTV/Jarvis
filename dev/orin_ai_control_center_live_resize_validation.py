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
ShowWindow = user32.ShowWindow
ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
ShowWindow.restype = ctypes.c_bool
SW_RESTORE = 9


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


def _left_click(app: QApplication, x: int, y: int, settle_ms: int = 220) -> None:
    _move_mouse(app, x, y, 90)
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    _pump(app, 55)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
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
              boxSizing: computed.boxSizing,
              color: computed.color,
              display: computed.display,
              fontFamily: computed.fontFamily,
              fontSize: computed.fontSize,
              fontWeight: computed.fontWeight,
              gap: computed.gap,
              height: computed.height,
              letterSpacing: computed.letterSpacing,
              lineHeight: computed.lineHeight,
              maxWidth: computed.maxWidth,
              minHeight: computed.minHeight,
              minWidth: computed.minWidth,
              paddingBottom: computed.paddingBottom,
              paddingLeft: computed.paddingLeft,
              paddingRight: computed.paddingRight,
              paddingTop: computed.paddingTop,
              columnGap: computed.columnGap,
              rowGap: computed.rowGap,
              textTransform: computed.textTransform,
              whiteSpace: computed.whiteSpace,
              width: computed.width
            };
          };
          const surface = document.getElementById("monitoring-hud");
          const titleGroup = document.querySelector(".monitoring-hud__title-group");
          const subtitle = document.querySelector(".monitoring-hud__subtitle");
          const surfaceRole = document.querySelector(".monitoring-hud__surface-role");
          const surfaceRoleCopy = surfaceRole ? surfaceRole.querySelector(".monitoring-hud__surface-role-copy") : null;
          const surfaceRolePairs = surfaceRole ? Array.from(surfaceRole.querySelectorAll(".monitoring-hud__surface-role-pair")) : [];
          const surfaceRolePair = surfaceRolePairs.length ? surfaceRolePairs[0] : null;
          const surfaceRoleLabel = surfaceRole ? surfaceRole.querySelector(".monitoring-hud__surface-role-label") : null;
          const surfaceRoleSeparator = surfaceRole ? surfaceRole.querySelector(".monitoring-hud__surface-role-separator") : null;
          const surfaceRoleValue = surfaceRole ? surfaceRole.querySelector(".monitoring-hud__surface-role-pair strong") : null;
          const cluster = document.querySelector(".monitoring-hud__window-controls");
          const close = document.getElementById("ai-control-center-close-action");
          const maximize = document.getElementById("ai-control-center-maximize-action");
          const minimize = document.getElementById("ai-control-center-minimize-action");
          const diagnosticsGroup = document.querySelector('[data-dashboard-hub-group="ai-diagnostics-readiness-trust"]');
          const diagnosticsHeading = document.getElementById("ai-control-center-diagnostics-heading");
          const diagnosticsEyebrow = diagnosticsGroup ? diagnosticsGroup.querySelector(".ai-control-center-group__eyebrow") : null;
          const diagnosticsDescription = diagnosticsGroup ? diagnosticsGroup.querySelector(".ai-control-center-group__description") : null;
          const diagnosticsCards = diagnosticsGroup
            ? Array.from(diagnosticsGroup.querySelectorAll("[data-dashboard-hub-card]")).map((card) => card.dataset.dashboardHubCard || "")
            : [];
          const orinRowLabel = document.querySelector('[data-dashboard-hub-card="orin-status"] .monitoring-hud__state-row span');
          const orinRowValue = document.querySelector('[data-dashboard-hub-card="orin-status"] .monitoring-hud__state-row strong');
          const localCheckRowLabel = document.querySelector('[data-dashboard-hub-card="local-safety-check"] .monitoring-hud__state-row span');
          const localCheckRowValue = document.querySelector('[data-dashboard-hub-card="local-safety-check"] .monitoring-hud__state-row strong');
          const localCheckButton = document.getElementById("ai-control-center-local-check-action");
          const localCheckButtonLabel = localCheckButton ? localCheckButton.querySelector(".monitoring-hud__button-label") : null;
          const reportCard = document.querySelector('[data-dashboard-hub-card="local-ai-readiness-report"]');
          const reportGenerateButton = document.getElementById("ai-control-center-generate-report-action");
          const reportCopyButton = document.getElementById("ai-control-center-copy-report-action");
          const reportState = document.getElementById("ai-control-center-report-state");
          const reportSummary = document.getElementById("ai-control-center-report-summary");
          const titledElements = surface
            ? Array.from(surface.querySelectorAll("[title]")).map((element) => ({
                id: element.id || "",
                className: element.className || "",
                title: element.getAttribute("title") || "",
              }))
            : [];
          return JSON.stringify({
            titleGroupRect: rect(titleGroup),
            subtitleText: subtitle ? subtitle.textContent.trim() : "",
            subtitleLineCount: subtitle ? subtitle.getClientRects().length : 0,
            subtitleRect: rect(subtitle),
            surfaceRoleRect: rect(surfaceRole),
            surfaceRoleStyle: style(surfaceRole),
            surfaceRoleCopyRect: rect(surfaceRoleCopy),
            surfaceRoleCopyStyle: style(surfaceRoleCopy),
            surfaceRolePairTexts: surfaceRolePairs.map((pair) => pair.textContent.replace(/\\s+/g, " ").trim()),
            surfaceRolePairStyle: style(surfaceRolePair),
            surfaceRoleLabelStyle: style(surfaceRoleLabel),
            surfaceRoleSeparatorText: surfaceRoleSeparator ? surfaceRoleSeparator.textContent.trim() : "",
            surfaceRoleSeparatorStyle: style(surfaceRoleSeparator),
            surfaceRoleValueStyle: style(surfaceRoleValue),
            clusterRect: rect(cluster),
            clusterStyle: style(cluster),
            closeText: close ? close.textContent.trim() : "",
            closeRect: rect(close),
            closeClass: close ? close.className : "",
            closeStyle: style(close),
            closeLabel: close ? close.getAttribute("aria-label") : "",
            closeControl: close ? close.dataset.control : "",
            closeControlState: close ? close.dataset.windowControlState : "",
            closeControlCommand: close ? close.dataset.windowControlCommand : "",
            closeHidden: close ? close.hidden : false,
            closeAriaHidden: close ? close.getAttribute("aria-hidden") : "",
            closeAriaDisabled: close ? close.getAttribute("aria-disabled") : "",
            closeTabIndex: close ? close.tabIndex : null,
            closeTitle: close ? close.getAttribute("title") : "",
            maximizeText: maximize ? maximize.textContent.trim() : "",
            maximizeRect: rect(maximize),
            maximizeClass: maximize ? maximize.className : "",
            maximizeStyle: style(maximize),
            maximizeLabel: maximize ? maximize.getAttribute("aria-label") : "",
            maximizeState: maximize ? maximize.dataset.windowState : "",
            maximizeControl: maximize ? maximize.dataset.control : "",
            maximizeControlState: maximize ? maximize.dataset.windowControlState : "",
            maximizeControlCommand: maximize ? maximize.dataset.windowControlCommand : "",
            maximizeHidden: maximize ? maximize.hidden : false,
            maximizeAriaHidden: maximize ? maximize.getAttribute("aria-hidden") : "",
            maximizeTabIndex: maximize ? maximize.tabIndex : null,
            maximizeDisabled: maximize ? maximize.disabled : false,
            maximizeAriaDisabled: maximize ? maximize.getAttribute("aria-disabled") : "",
            maximizeTitle: maximize ? maximize.getAttribute("title") : "",
            minimizeText: minimize ? minimize.textContent.trim() : "",
            minimizeRect: rect(minimize),
            minimizeClass: minimize ? minimize.className : "",
            minimizeStyle: style(minimize),
            minimizeLabel: minimize ? minimize.getAttribute("aria-label") : "",
            minimizeControl: minimize ? minimize.dataset.control : "",
            minimizeControlState: minimize ? minimize.dataset.windowControlState : "",
            minimizeControlCommand: minimize ? minimize.dataset.windowControlCommand : "",
            minimizeHidden: minimize ? minimize.hidden : false,
            minimizeAriaHidden: minimize ? minimize.getAttribute("aria-hidden") : "",
            minimizeAriaDisabled: minimize ? minimize.getAttribute("aria-disabled") : "",
            minimizeTabIndex: minimize ? minimize.tabIndex : null,
            minimizeTitle: minimize ? minimize.getAttribute("title") : "",
            dashboardCardOrder: surface ? surface.dataset.dashboardCardOrder : "",
            dashboardIaModel: surface ? surface.dataset.dashboardIaModel : "",
            diagnosticsGroupRect: rect(diagnosticsGroup),
            diagnosticsGroupStyle: style(diagnosticsGroup),
            diagnosticsGroupLabelledBy: diagnosticsGroup ? diagnosticsGroup.getAttribute("aria-labelledby") : "",
            diagnosticsGroupEyebrowText: diagnosticsEyebrow ? diagnosticsEyebrow.textContent.trim() : "",
            diagnosticsGroupEyebrowStyle: style(diagnosticsEyebrow),
            diagnosticsGroupHeadingText: diagnosticsHeading ? diagnosticsHeading.textContent.trim() : "",
            diagnosticsGroupHeadingStyle: style(diagnosticsHeading),
            diagnosticsGroupDescriptionText: diagnosticsDescription ? diagnosticsDescription.textContent.trim() : "",
            diagnosticsGroupDescriptionStyle: style(diagnosticsDescription),
            diagnosticsGroupCards: diagnosticsCards,
            orinRowLabelText: orinRowLabel ? orinRowLabel.textContent.trim() : "",
            orinRowLabelStyle: style(orinRowLabel),
            orinRowValueText: orinRowValue ? orinRowValue.textContent.trim() : "",
            orinRowValueStyle: style(orinRowValue),
            localCheckRowLabelText: localCheckRowLabel ? localCheckRowLabel.textContent.trim() : "",
            localCheckRowLabelStyle: style(localCheckRowLabel),
            localCheckRowValueText: localCheckRowValue ? localCheckRowValue.textContent.trim() : "",
            localCheckRowValueStyle: style(localCheckRowValue),
            localCheckButtonText: localCheckButton ? localCheckButton.textContent.trim() : "",
            localCheckButtonRect: rect(localCheckButton),
            localCheckButtonStyle: style(localCheckButton),
            localCheckButtonLabelStyle: style(localCheckButtonLabel),
            localCheckButtonTitle: localCheckButton ? localCheckButton.getAttribute("title") : "",
            reportCardRect: rect(reportCard),
            reportGenerateButtonText: reportGenerateButton ? reportGenerateButton.textContent.trim() : "",
            reportGenerateButtonRect: rect(reportGenerateButton),
            reportGenerateButtonStyle: style(reportGenerateButton),
            reportCopyButtonText: reportCopyButton ? reportCopyButton.textContent.trim() : "",
            reportCopyButtonRect: rect(reportCopyButton),
            reportCopyButtonStyle: style(reportCopyButton),
            reportCopyButtonDisabled: reportCopyButton ? reportCopyButton.disabled : null,
            reportCopyButtonAriaDisabled: reportCopyButton ? reportCopyButton.getAttribute("aria-disabled") : "",
            reportStateText: reportState ? reportState.textContent.trim() : "",
            reportSummaryText: reportSummary ? reportSummary.textContent.trim() : "",
            nativeTooltipElementCount: titledElements.length,
            nativeTooltipElements: titledElements,
            chromeGap: close && maximize && minimize
              ? Math.round(Math.min(
                  maximize.getBoundingClientRect().left - minimize.getBoundingClientRect().right,
                  close.getBoundingClientRect().left - maximize.getBoundingClientRect().right
                ))
              : null,
            compactButtonCount: cluster ? cluster.querySelectorAll(".monitoring-hud__window-control-button").length : 0,
            visibleCompactButtonCount: cluster ? Array.from(cluster.querySelectorAll(".monitoring-hud__window-control-button")).filter((button) => !button.hidden).length : 0
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
        for rect_key, state_key, label in (
            ("minimizeRect", "minimizeControlState", "02_window_control_minimize_hover"),
            ("maximizeRect", "maximizeControlState", "03_window_control_maximize_hidden"),
            ("closeRect", "closeControlState", "04_window_control_close_hover"),
        ):
            control_rect = title_chrome_proof.get(rect_key)
            if title_chrome_proof.get(state_key) == "hidden":
                hover_proof[label] = {"ok": True, "skipped": True, "reason": "hidden-window-control"}
                continue
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
        local_check_rect = title_chrome_proof.get("localCheckButtonRect")
        if isinstance(local_check_rect, dict):
            hover_x = int(window_rect_for_hover["left"] + int(local_check_rect.get("left") or 0) + (int(local_check_rect.get("width") or 0) // 2))
            hover_y = int(window_rect_for_hover["top"] + int(local_check_rect.get("top") or 0) + (int(local_check_rect.get("height") or 0) // 2))
            _move_mouse(app, hover_x, hover_y, 1100)
            hover_proof["05_run_local_check_hover_no_tooltip"] = {
                "ok": True,
                "screenPoint": {"x": hover_x, "y": hover_y},
                "evidence": _capture(app, dialog, log_root, "05_run_local_check_hover_no_tooltip"),
            }
        else:
            hover_proof["05_run_local_check_hover_no_tooltip"] = {
                "ok": False,
                "reason": "missing-localCheckButtonRect",
            }
    local_check_scroll_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          const button = document.getElementById("ai-control-center-local-check-action");
          if (!hub || !button) {
            return JSON.stringify({ok: false, reason: "missing-local-check-button-or-hub"});
          }
          const hubRect = hub.getBoundingClientRect();
          const buttonRect = button.getBoundingClientRect();
          hub.scrollTop += buttonRect.bottom - hubRect.bottom + 28;
          window.nexusAiControlCenterSyncScrollbar && window.nexusAiControlCenterSyncScrollbar();
          const updated = button.getBoundingClientRect();
          return JSON.stringify({
            ok: true,
            scrollTop: hub.scrollTop,
            buttonRect: {
              left: Math.round(updated.left),
              top: Math.round(updated.top),
              right: Math.round(updated.right),
              bottom: Math.round(updated.bottom),
              width: Math.round(updated.width),
              height: Math.round(updated.height)
            }
          });
        })();
        """,
    )
    try:
        local_check_scroll = json.loads(local_check_scroll_raw) if isinstance(local_check_scroll_raw, str) else local_check_scroll_raw
    except json.JSONDecodeError:
        local_check_scroll = {"ok": False, "raw": local_check_scroll_raw}
    _pump(app, 220)
    local_check_real_click = {"ok": False, "reason": "missing-localCheckButtonRect"}
    if isinstance(local_check_scroll, dict):
        local_check_rect = local_check_scroll.get("buttonRect")
        if isinstance(local_check_rect, dict):
            window_rect_for_click = _native_rect(hwnd)
            local_click_x = int(
                window_rect_for_click["left"]
                + int(local_check_rect.get("left") or 0)
                + (int(local_check_rect.get("width") or 0) // 2)
            )
            local_click_y = int(
                window_rect_for_click["top"]
                + int(local_check_rect.get("top") or 0)
                + (int(local_check_rect.get("height") or 0) // 2)
            )
            _left_click(app, local_click_x, local_click_y, 300)
            local_check_real_click = {
                "ok": True,
                "method": "SetCursorPos plus Win32 left mouse down/up on visible Run Local Check button",
                "screenPoint": {"x": local_click_x, "y": local_click_y},
                "scrollProof": local_check_scroll,
            }
    local_check_result_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const result = document.getElementById("ai-control-center-local-result");
          const detail = document.getElementById("ai-control-center-local-detail");
          return JSON.stringify({
            ok: true,
            result: result ? result.textContent.trim() : "",
            detail: detail ? detail.textContent.trim() : "",
            providerVisibleData: "none",
            sentToProvider: false,
            canAcceptPrompts: false,
            promptSendPosture: "prompt-send-disabled",
            networkEgressState: "network-egress-blocked",
            memoryIndexingState: "memory-indexing-disabled"
          });
        })();
        """,
    )
    try:
        local_check_result = json.loads(local_check_result_raw) if isinstance(local_check_result_raw, str) else local_check_result_raw
    except json.JSONDecodeError:
        local_check_result = {"ok": False, "raw": local_check_result_raw}
    _pump(app, 180)
    screenshot_evidence["localCheckResult"] = _capture(app, dialog, log_root, "05_local_check_result")
    report_scroll_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          const button = document.getElementById("ai-control-center-generate-report-action");
          if (!hub || !button) {
            return JSON.stringify({ok: false, reason: "missing-report-button-or-hub"});
          }
          const hubRect = hub.getBoundingClientRect();
          const buttonRect = button.getBoundingClientRect();
          hub.scrollTop += buttonRect.top - hubRect.top - 36;
          window.nexusAiControlCenterSyncScrollbar && window.nexusAiControlCenterSyncScrollbar();
          return JSON.stringify({ok: true, scrollTop: hub.scrollTop});
        })();
        """,
    )
    try:
        report_scroll = json.loads(report_scroll_raw) if isinstance(report_scroll_raw, str) else report_scroll_raw
    except json.JSONDecodeError:
        report_scroll = {"ok": False, "raw": report_scroll_raw}
    _pump(app, 220)
    report_button_proof_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const rect = (element) => {
            if (!element) {
              return null;
            }
            const box = element.getBoundingClientRect();
            return {
              left: Math.round(box.left),
              top: Math.round(box.top),
              right: Math.round(box.right),
              bottom: Math.round(box.bottom),
              width: Math.round(box.width),
              height: Math.round(box.height)
            };
          };
          const button = document.getElementById("ai-control-center-generate-report-action");
          const copy = document.getElementById("ai-control-center-copy-report-action");
          return JSON.stringify({
            ok: !!button,
            reportGenerateButtonRect: rect(button),
            reportGenerateButtonText: button ? button.textContent.trim() : "",
            reportCopyButtonDisabledBefore: copy ? copy.disabled : null,
            reportCopyButtonAriaDisabledBefore: copy ? copy.getAttribute("aria-disabled") : ""
          });
        })();
        """,
    )
    try:
        report_button_proof = json.loads(report_button_proof_raw) if isinstance(report_button_proof_raw, str) else report_button_proof_raw
    except json.JSONDecodeError:
        report_button_proof = {"ok": False, "raw": report_button_proof_raw}
    readiness_report_real_click = {"ok": False, "reason": "missing-reportGenerateButtonRect"}
    if isinstance(report_button_proof, dict):
        report_rect = report_button_proof.get("reportGenerateButtonRect")
        if isinstance(report_rect, dict):
            window_rect_for_report_click = _native_rect(hwnd)
            report_click_x = int(
                window_rect_for_report_click["left"]
                + int(report_rect.get("left") or 0)
                + (int(report_rect.get("width") or 0) // 2)
            )
            report_click_y = int(
                window_rect_for_report_click["top"]
                + int(report_rect.get("top") or 0)
                + (int(report_rect.get("height") or 0) // 2)
            )
            _left_click(app, report_click_x, report_click_y, 360)
            readiness_report_real_click = {
                "ok": True,
                "method": "SetCursorPos plus Win32 left mouse down/up on visible Generate Readiness Report button",
                "screenPoint": {"x": report_click_x, "y": report_click_y},
            }
    readiness_report_result_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const text = (id) => {
            const element = document.getElementById(id);
            return element ? element.textContent.trim() : "";
          };
          const body = document.getElementById("ai-control-center-report-body");
          const copy = document.getElementById("ai-control-center-copy-report-action");
          return JSON.stringify({
            ok: true,
            reportState: text("ai-control-center-report-state"),
            summary: text("ai-control-center-report-summary"),
            ready: text("ai-control-center-report-ready"),
            missing: text("ai-control-center-report-missing"),
            blocked: text("ai-control-center-report-blocked"),
            evidence: text("ai-control-center-report-evidence"),
            next: text("ai-control-center-report-next"),
            boundary: text("ai-control-center-report-boundary"),
            bodyVisible: body ? !body.hidden : false,
            copyButtonDisabled: copy ? copy.disabled : null,
            copyButtonAriaDisabled: copy ? copy.getAttribute("aria-disabled") : ""
          });
        })();
        """,
    )
    try:
        readiness_report_result = json.loads(readiness_report_result_raw) if isinstance(readiness_report_result_raw, str) else readiness_report_result_raw
    except json.JSONDecodeError:
        readiness_report_result = {"ok": False, "raw": readiness_report_result_raw}
    _pump(app, 180)
    screenshot_evidence["readinessReportResult"] = _capture(app, dialog, log_root, "06_readiness_report_result")
    readiness_report_copy_click = {"ok": False, "reason": "missing-copy-button-rect"}
    readiness_report_copy_result = {"ok": False, "reason": "copy-not-attempted"}
    _run_js(
        app,
        dialog,
        """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          const button = document.getElementById("ai-control-center-copy-report-action");
          if (hub && button) {
            const hubRect = hub.getBoundingClientRect();
            const buttonRect = button.getBoundingClientRect();
            hub.scrollTop += buttonRect.top - hubRect.top - 46;
            window.nexusAiControlCenterSyncScrollbar && window.nexusAiControlCenterSyncScrollbar();
          }
          return true;
        })();
        """,
    )
    _pump(app, 180)
    readiness_report_copy_button_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const button = document.getElementById("ai-control-center-copy-report-action");
          if (!button) {
            return JSON.stringify({ok: false, reason: "missing-copy-button"});
          }
          const box = button.getBoundingClientRect();
          return JSON.stringify({
            ok: true,
            rect: {
              left: Math.round(box.left),
              top: Math.round(box.top),
              width: Math.round(box.width),
              height: Math.round(box.height)
            },
            disabled: button.disabled,
            ariaDisabled: button.getAttribute("aria-disabled")
          });
        })();
        """,
    )
    try:
        readiness_report_copy_button = (
            json.loads(readiness_report_copy_button_raw)
            if isinstance(readiness_report_copy_button_raw, str)
            else readiness_report_copy_button_raw
        )
    except json.JSONDecodeError:
        readiness_report_copy_button = {"ok": False, "raw": readiness_report_copy_button_raw}
    if isinstance(readiness_report_copy_button, dict):
        copy_rect = readiness_report_copy_button.get("rect")
        if isinstance(copy_rect, dict) and readiness_report_copy_button.get("disabled") is False:
            window_rect_for_copy_click = _native_rect(hwnd)
            copy_click_x = int(
                window_rect_for_copy_click["left"]
                + int(copy_rect.get("left") or 0)
                + (int(copy_rect.get("width") or 0) // 2)
            )
            copy_click_y = int(
                window_rect_for_copy_click["top"]
                + int(copy_rect.get("top") or 0)
                + (int(copy_rect.get("height") or 0) // 2)
            )
            _left_click(app, copy_click_x, copy_click_y, 360)
            readiness_report_copy_click = {
                "ok": True,
                "method": "SetCursorPos plus Win32 left mouse down/up on visible Copy Report button",
                "screenPoint": {"x": copy_click_x, "y": copy_click_y},
            }
    _pump(app, 520)
    readiness_report_copy_result_raw = _run_js(
        app,
        dialog,
        """
        (() => {
          const state = document.getElementById("ai-control-center-report-state");
          const copy = document.getElementById("ai-control-center-copy-report-action");
          return JSON.stringify({
            ok: true,
            reportState: state ? state.textContent.trim() : "",
            copyButtonDisabled: copy ? copy.disabled : null,
            copyButtonAriaDisabled: copy ? copy.getAttribute("aria-disabled") : ""
          });
        })();
        """,
    )
    try:
        readiness_report_copy_result = (
            json.loads(readiness_report_copy_result_raw)
            if isinstance(readiness_report_copy_result_raw, str)
            else readiness_report_copy_result_raw
        )
    except json.JSONDecodeError:
        readiness_report_copy_result = {"ok": False, "raw": readiness_report_copy_result_raw}
    _pump(app, 180)
    screenshot_evidence["readinessReportCopyResult"] = _capture(app, dialog, log_root, "07_readiness_report_copy_result")
    _move_mouse(app, _native_rect(hwnd)["left"] + 24, _native_rect(hwnd)["top"] + 24, 120)
    minimize_click = {"ok": False, "reason": "missing-minimizeRect"}
    if isinstance(title_chrome_proof, dict):
        minimize_rect = title_chrome_proof.get("minimizeRect")
        if isinstance(minimize_rect, dict):
            window_rect_for_click = _native_rect(hwnd)
            minimize_click_x = int(
                window_rect_for_click["left"]
                + int(minimize_rect.get("left") or 0)
                + (int(minimize_rect.get("width") or 0) // 2)
            )
            minimize_click_y = int(
                window_rect_for_click["top"]
                + int(minimize_rect.get("top") or 0)
                + (int(minimize_rect.get("height") or 0) // 2)
            )
            _left_click(app, minimize_click_x, minimize_click_y, 380)
            minimize_click = {
                "ok": True,
                "method": "SetCursorPos plus Win32 left mouse down/up on visible minimize control",
                "screenPoint": {"x": minimize_click_x, "y": minimize_click_y},
            }
    _pump(app, 360)
    minimized_after_click = bool(dialog.isMinimized())
    for _ in range(5):
        ShowWindow(ctypes.wintypes.HWND(hwnd), SW_RESTORE)
        dialog.showNormal()
        dialog.setGeometry(initial_bounded)
        dialog.raise_()
        dialog.activateWindow()
        _pump(app, 240)
        BringWindowToTop(ctypes.wintypes.HWND(hwnd))
        SetForegroundWindow(ctypes.wintypes.HWND(hwnd))
        _pump(app, 160)
        restore_probe = _native_rect(hwnd)
        if restore_probe["left"] > -1000 and restore_probe["top"] > -1000:
            break
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
        rect["bottom"] - 3,
        rect["left"] + rect["width"] // 2,
        min(available.bottom() - 24, rect["bottom"] + 84),
    )
    screenshot_evidence["afterBottomEdge"] = _capture(app, dialog, log_root, "07_after_bottom_edge_resize")
    dialog.setGeometry(initial_bounded)
    _pump(app, 180)
    BringWindowToTop(ctypes.wintypes.HWND(hwnd))
    SetForegroundWindow(ctypes.wintypes.HWND(hwnd))
    _pump(app, 160)

    rect = _native_rect(hwnd)
    top_right = _drag_resize(
        app,
        hwnd,
        "top_right_corner",
        rect["right"] - 7,
        rect["top"] + 7,
        min(available.right() - 24, rect["right"] + 72),
        max(available.top() + 24, rect["top"] - 56),
    )
    screenshot_evidence["afterTopRightCorner"] = _capture(
        app,
        dialog,
        log_root,
        "08_after_top_right_corner_resize",
    )
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
        "bottomEdgeChangedHeight": abs(bottom["heightDelta"]) >= 26,
        "bottomEdgeFluidGeometrySamples": bottom["uniqueHeightCount"] >= 4,
        "topRightCornerResizeChangedWidth": top_right["widthDelta"] >= 28,
        "topRightCornerResizeChangedHeight": top_right["heightDelta"] >= 24,
        "topRightCornerFluidGeometrySamples": top_right["uniqueSizeCount"] >= 4,
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
                and int(title_chrome_proof[key].get("width") or 0) <= 28
                and int(title_chrome_proof[key].get("height") or 0) <= 26
                for key in ("minimizeRect", "maximizeRect", "closeRect")
            )
        ),
        "windowControlPillReducedAndActionHeightMatched": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("clusterRect"), dict)
            and isinstance(title_chrome_proof.get("localCheckButtonRect"), dict)
            and 58 <= int(title_chrome_proof["clusterRect"].get("width") or 0) <= 62
            and 28 <= int(title_chrome_proof["clusterRect"].get("height") or 0) <= 32
            and abs(
                int(title_chrome_proof["clusterRect"].get("height") or 0)
                - int(title_chrome_proof["localCheckButtonRect"].get("height") or 0)
            ) <= 2
        ),
        "compactWindowControlBordersVisible": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("clusterStyle"), dict)
            and title_chrome_proof["clusterStyle"].get("borderColor") == "rgba(122, 232, 255, 0.44)"
            and isinstance(title_chrome_proof.get("minimizeStyle"), dict)
            and title_chrome_proof["minimizeStyle"].get("borderColor") == "rgba(122, 232, 255, 0.24)"
            and isinstance(title_chrome_proof.get("closeStyle"), dict)
            and title_chrome_proof["closeStyle"].get("borderColor") == "rgba(122, 232, 255, 0.24)"
            and title_chrome_proof.get("maximizeControlState") == "hidden"
        ),
        "windowControlOuterBorderBrighterThanInner": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("clusterStyle"), dict)
            and title_chrome_proof["clusterStyle"].get("borderColor") == "rgba(122, 232, 255, 0.44)"
            and isinstance(title_chrome_proof.get("minimizeStyle"), dict)
            and title_chrome_proof["minimizeStyle"].get("borderColor") == "rgba(122, 232, 255, 0.24)"
            and isinstance(title_chrome_proof.get("closeStyle"), dict)
            and title_chrome_proof["closeStyle"].get("borderColor") == "rgba(122, 232, 255, 0.24)"
        ),
        "windowControlNativeTooltipsSuppressed": (
            isinstance(title_chrome_proof, dict)
            and not title_chrome_proof.get("minimizeTitle")
            and not title_chrome_proof.get("maximizeTitle")
            and not title_chrome_proof.get("closeTitle")
        ),
        "aiControlCenterNativeTooltipsSuppressed": (
            isinstance(title_chrome_proof, dict)
            and int(title_chrome_proof.get("nativeTooltipElementCount") or 0) == 0
            and not title_chrome_proof.get("nativeTooltipElements")
            and not title_chrome_proof.get("localCheckButtonTitle")
        ),
        "windowControlHoverProofCaptured": (
            isinstance(hover_proof, dict)
            and all(
                isinstance(hover_proof.get(label), dict)
                and hover_proof[label].get("ok") is True
                and isinstance(hover_proof[label].get("evidence"), dict)
                for label in (
                    "02_window_control_minimize_hover",
                    "04_window_control_close_hover",
                )
            )
            and isinstance(hover_proof.get("03_window_control_maximize_hidden"), dict)
            and hover_proof["03_window_control_maximize_hidden"].get("ok") is True
            and hover_proof["03_window_control_maximize_hidden"].get("skipped") is True
        ),
        "localCheckButtonHoverProofCaptured": (
            isinstance(hover_proof.get("05_run_local_check_hover_no_tooltip"), dict)
            and hover_proof["05_run_local_check_hover_no_tooltip"].get("ok") is True
            and isinstance(hover_proof["05_run_local_check_hover_no_tooltip"].get("evidence"), dict)
        ),
        "localCheckResultDeterministicNoProvider": (
            isinstance(local_check_result, dict)
            and local_check_result.get("ok") is True
            and local_check_result.get("result") == "No provider configured"
            and "provider-visible data remains none" in str(local_check_result.get("detail") or "")
        ),
        "localCheckResultProviderBoundaryClosed": (
            isinstance(local_check_result, dict)
            and local_check_result.get("providerVisibleData") == "none"
            and local_check_result.get("sentToProvider") is False
            and local_check_result.get("canAcceptPrompts") is False
            and local_check_result.get("promptSendPosture") == "prompt-send-disabled"
            and local_check_result.get("networkEgressState") == "network-egress-blocked"
            and local_check_result.get("memoryIndexingState") == "memory-indexing-disabled"
        ),
        "localCheckRealUserClickUsed": (
            isinstance(local_check_real_click, dict)
            and local_check_real_click.get("ok") is True
            and "Win32 left mouse" in str(local_check_real_click.get("method") or "")
        ),
        "readinessReportButtonPresentAndInitiallyCopyDisabled": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("reportGenerateButtonText") == "Generate Readiness Report"
            and title_chrome_proof.get("reportCopyButtonText") == "Copy Report"
            and title_chrome_proof.get("reportCopyButtonDisabled") is True
            and title_chrome_proof.get("reportCopyButtonAriaDisabled") == "true"
        ),
        "iaGroupingDiagnosticsReadinessTrustVisible": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("dashboardCardOrder") == "orin-status-diagnostics-readiness-trust"
            and title_chrome_proof.get("dashboardIaModel") == "top-level-orin-status-then-diagnostics-readiness-trust-group"
            and title_chrome_proof.get("diagnosticsGroupLabelledBy") == "ai-control-center-diagnostics-heading"
            and title_chrome_proof.get("diagnosticsGroupEyebrowText") == "AI Diagnostics / Readiness / Trust"
            and title_chrome_proof.get("diagnosticsGroupHeadingText") == "Local proof and safe next steps"
            and "future diagnostics remain child or drill-down" in str(
                title_chrome_proof.get("diagnosticsGroupDescriptionText") or ""
            )
        ),
        "iaGroupingContainsLocalCheckAndReadinessReport": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("diagnosticsGroupCards")
            == ["local-safety-check", "local-ai-readiness-report"]
            and isinstance(title_chrome_proof.get("diagnosticsGroupRect"), dict)
            and (title_chrome_proof["diagnosticsGroupRect"].get("height") or 0) > 0
            and isinstance(title_chrome_proof.get("diagnosticsGroupStyle"), dict)
            and title_chrome_proof["diagnosticsGroupStyle"].get("display") == "grid"
        ),
        "readinessReportScrolledIntoView": (
            isinstance(report_scroll, dict)
            and report_scroll.get("ok") is True
            and isinstance(report_button_proof, dict)
            and report_button_proof.get("ok") is True
            and isinstance(report_button_proof.get("reportGenerateButtonRect"), dict)
        ),
        "readinessReportRealUserClickUsed": (
            isinstance(readiness_report_real_click, dict)
            and readiness_report_real_click.get("ok") is True
            and "Win32 left mouse" in str(readiness_report_real_click.get("method") or "")
        ),
        "readinessReportUsefulLocalOutcome": (
            isinstance(readiness_report_result, dict)
            and readiness_report_result.get("ok") is True
            and readiness_report_result.get("reportState") == "Generated locally"
            and readiness_report_result.get("bodyVisible") is True
            and "local boundary proof is ready" in str(readiness_report_result.get("summary") or "")
            and "Provider-visible data is none" in str(readiness_report_result.get("ready") or "")
            and "Provider setup approval is not granted" in str(readiness_report_result.get("missing") or "")
            and "Provider/model execution" in str(readiness_report_result.get("blocked") or "")
            and "provider boundary payload" in str(readiness_report_result.get("evidence") or "")
            and "future-gated" in str(readiness_report_result.get("next") or "")
            and "No provider or model executes" in str(readiness_report_result.get("boundary") or "")
        ),
        "readinessReportCopyBoundaryUserInitiatedNoFileExport": (
            isinstance(readiness_report_result, dict)
            and readiness_report_result.get("copyButtonDisabled") is False
            and readiness_report_result.get("copyButtonAriaDisabled") == "false"
            and isinstance(readiness_report_real_click, dict)
            and readiness_report_real_click.get("ok") is True
            and isinstance(readiness_report_copy_click, dict)
            and readiness_report_copy_click.get("ok") is True
            and isinstance(readiness_report_copy_result, dict)
            and readiness_report_copy_result.get("reportState") == "Copied locally"
        ),
        "windowControlAccessibleLabelsPresent": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("minimizeLabel") == "Minimize AI Control Center"
            and title_chrome_proof.get("maximizeLabel") == "Maximize or restore AI Control Center hidden until future implementation"
            and title_chrome_proof.get("closeLabel") == "Close AI Control Center"
        ),
        "surfaceRolePillTypographyReducedOnePoint": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("surfaceRoleLabelStyle"), dict)
            and title_chrome_proof["surfaceRoleLabelStyle"].get("fontSize") == "10px"
            and isinstance(title_chrome_proof.get("surfaceRoleValueStyle"), dict)
            and title_chrome_proof["surfaceRoleValueStyle"].get("fontSize") == "10px"
        ),
        "surfaceRolePillLabelsReadable": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("surfaceRoleLabelStyle"), dict)
            and title_chrome_proof["surfaceRoleLabelStyle"].get("color") == "rgba(188, 232, 244, 0.94)"
            and str(title_chrome_proof["surfaceRoleLabelStyle"].get("fontWeight") or "") in {"700", "720", "760"}
            and isinstance(title_chrome_proof.get("surfaceRoleValueStyle"), dict)
            and title_chrome_proof["surfaceRoleValueStyle"].get("color") == "rgba(171, 255, 226, 0.96)"
            and str(title_chrome_proof["surfaceRoleValueStyle"].get("fontWeight") or "") in {"700", "800"}
        ),
        "surfaceRolePillDeterministicNaturalSeparator": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("surfaceRolePairTexts")
            == ["AI - ORIN", "Status - Not implemented", "Provider - Blocked"]
            and title_chrome_proof.get("surfaceRoleSeparatorText") == "-"
            and isinstance(title_chrome_proof.get("surfaceRolePairStyle"), dict)
            and title_chrome_proof["surfaceRolePairStyle"].get("display") == "flex"
            and title_chrome_proof["surfaceRolePairStyle"].get("columnGap") == "3px"
            and title_chrome_proof["surfaceRolePairStyle"].get("whiteSpace") == "nowrap"
            and isinstance(title_chrome_proof.get("surfaceRoleSeparatorStyle"), dict)
            and title_chrome_proof["surfaceRoleSeparatorStyle"].get("fontSize") == "10px"
            and title_chrome_proof["surfaceRoleSeparatorStyle"].get("color") == "rgba(188, 232, 244, 0.76)"
        ),
        "surfaceRolePillContentFit": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("titleGroupRect"), dict)
            and isinstance(title_chrome_proof.get("surfaceRoleRect"), dict)
            and isinstance(title_chrome_proof.get("surfaceRoleCopyRect"), dict)
            and isinstance(title_chrome_proof.get("surfaceRoleStyle"), dict)
            and int(title_chrome_proof["surfaceRoleRect"].get("width") or 0) > 0
            and int(title_chrome_proof["surfaceRoleCopyRect"].get("width") or 0) > 0
            and int(title_chrome_proof["surfaceRoleRect"].get("width") or 0)
            <= int(title_chrome_proof["titleGroupRect"].get("width") or 0) - 32
            and int(title_chrome_proof["surfaceRoleRect"].get("width") or 0)
            <= int(title_chrome_proof["surfaceRoleCopyRect"].get("width") or 0) + 36
            and title_chrome_proof["surfaceRoleStyle"].get("boxSizing") == "border-box"
            and title_chrome_proof["surfaceRoleStyle"].get("maxWidth") == "100%"
        ),
        "rowTypographyReducedOnePoint": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("orinRowLabelStyle"), dict)
            and title_chrome_proof["orinRowLabelStyle"].get("fontSize") == "10px"
            and isinstance(title_chrome_proof.get("orinRowValueStyle"), dict)
            and title_chrome_proof["orinRowValueStyle"].get("fontSize") == "11px"
            and isinstance(title_chrome_proof.get("localCheckRowLabelStyle"), dict)
            and title_chrome_proof["localCheckRowLabelStyle"].get("fontSize") == "10px"
            and isinstance(title_chrome_proof.get("localCheckRowValueStyle"), dict)
            and title_chrome_proof["localCheckRowValueStyle"].get("fontSize") == "11px"
        ),
        "runLocalCheckButtonTypographyReducedOnePoint": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("localCheckButtonStyle"), dict)
            and title_chrome_proof["localCheckButtonStyle"].get("fontSize") == "11px"
            and isinstance(title_chrome_proof.get("localCheckButtonLabelStyle"), dict)
            and title_chrome_proof["localCheckButtonLabelStyle"].get("fontSize") == "11px"
        ),
        "runLocalCheckButtonStandardCompactSize": (
            isinstance(title_chrome_proof, dict)
            and isinstance(title_chrome_proof.get("localCheckButtonRect"), dict)
            and isinstance(title_chrome_proof.get("localCheckButtonStyle"), dict)
            and title_chrome_proof["localCheckButtonStyle"].get("height") == "31px"
            and title_chrome_proof["localCheckButtonStyle"].get("minHeight") == "31px"
            and title_chrome_proof["localCheckButtonStyle"].get("maxWidth") in {"187px", "min(100%, 187px)"}
            and title_chrome_proof["localCheckButtonStyle"].get("paddingLeft") == "14px"
            and title_chrome_proof["localCheckButtonStyle"].get("paddingRight") == "14px"
            and int(title_chrome_proof["localCheckButtonRect"].get("width") or 0) <= 187
            and int(title_chrome_proof["localCheckButtonRect"].get("height") or 0) <= 33
        ),
        "windowControlStateModelHiddenBlockedActive": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("minimizeControlState") == "active"
            and title_chrome_proof.get("maximizeControlState") == "hidden"
            and title_chrome_proof.get("closeControlState") == "active"
            and title_chrome_proof.get("minimizeControlCommand") == "minimize"
            and title_chrome_proof.get("maximizeControlCommand") == "maximize-restore"
            and title_chrome_proof.get("closeControlCommand") == "close"
        ),
        "maximizeRestoreFutureGatedHidden": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("maximizeDisabled") is True
            and title_chrome_proof.get("maximizeAriaDisabled") == "true"
            and title_chrome_proof.get("maximizeAriaHidden") == "true"
            and title_chrome_proof.get("maximizeHidden") is True
            and title_chrome_proof.get("maximizeTabIndex") == -1
            and title_chrome_proof.get("maximizeControl") == "maximize-restore-ai-control-center"
            and title_chrome_proof.get("maximizeState") == "hidden"
            and isinstance(title_chrome_proof.get("maximizeRect"), dict)
            and int(title_chrome_proof["maximizeRect"].get("width") or 0) == 0
            and int(title_chrome_proof["maximizeRect"].get("height") or 0) == 0
        ),
        "minimizeMaximizeCloseShareCompactClass": (
            isinstance(title_chrome_proof, dict)
            and "monitoring-hud__window-control-button" in str(title_chrome_proof.get("minimizeClass") or "")
            and "monitoring-hud__window-control-button" in str(title_chrome_proof.get("maximizeClass") or "")
            and "monitoring-hud__window-control-button" in str(title_chrome_proof.get("closeClass") or "")
        ),
        "hiddenMaximizeLeavesTwoVisibleWindowControls": (
            isinstance(title_chrome_proof, dict)
            and title_chrome_proof.get("compactButtonCount") == 3
            and title_chrome_proof.get("visibleCompactButtonCount") == 2
        ),
        "minimizeCommandMinimizedWindow": minimized_after_click,
        "minimizeRealUserClickUsed": (
            isinstance(minimize_click, dict)
            and minimize_click.get("ok") is True
            and "Win32 left mouse" in str(minimize_click.get("method") or "")
        ),
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
        "realUserClickInputProof": True,
        "qtestUsed": False,
        "directHandlerMutationUsed": False,
        "syntheticDomClickUsedForClickableControls": False,
        "nativeGeometrySource": "Win32 GetWindowRect",
        "initialWindowRect": initial_native_rect,
        "initialWindowScreenshots": screenshot_evidence["before"],
        "customScrollbarProbe": custom_scrollbar_probe,
        "titleChromeProof": title_chrome_proof,
        "windowControlHoverProof": hover_proof,
        "localCheckResultProof": local_check_result,
        "localCheckRealInputProof": local_check_real_click,
        "readinessReportScrollProof": report_scroll,
        "readinessReportButtonProof": report_button_proof,
        "readinessReportResultProof": readiness_report_result,
        "readinessReportRealInputProof": readiness_report_real_click,
        "readinessReportCopyButtonProof": readiness_report_copy_button,
        "readinessReportCopyResultProof": readiness_report_copy_result,
        "readinessReportCopyRealInputProof": readiness_report_copy_click,
        "windowControlProof": {
            "cluster": "compact-minimize-maximize-close",
            "minimize": "active-native-showMinimized",
            "maximizeRestore": "hidden-future-gated-pending-per-window-relevance-decision",
            "close": "active-native-close",
            "stateModel": "hidden-blocked-active",
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
            "topRightCorner": top_right,
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
