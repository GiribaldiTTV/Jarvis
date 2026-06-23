# Helper Status: Workstream-scoped
# Owner Workstream: FAM-007 AI Dashboard child/domain window repair
# Reason Reusable Helper Was Not Extended: the HUD live validator is FAM-006-specific; this helper proves FAM-007 AI Dashboard category launchers open real child/domain windows.
# Consolidation Target: future reusable Nexus product-window child-window lifecycle validator
# Promotion Decision Point: before PR Readiness fold-down

from __future__ import annotations

import ctypes
import ctypes.wintypes
import datetime
import json
import os
import shutil
import sys
import time
from pathlib import Path

from PySide6.QtCore import QRect
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
SW_RESTORE = 9


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


def _capture_window(app: QApplication, window, root: Path, label: str) -> dict[str, str]:
    focused_path = root / f"{label}_focused_window.png"
    desktop_path = root / f"{label}_full_desktop.png"
    screen = window.screen() or QApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No screen available for screenshot capture")
    if not window.grab().save(str(focused_path)):
        raise RuntimeError(f"Failed to save focused screenshot: {focused_path}")
    if not screen.grabWindow(0).save(str(desktop_path)):
        raise RuntimeError(f"Failed to save desktop screenshot: {desktop_path}")
    _pump(app, 50)
    return {"focusedWindow": str(focused_path), "fullDesktop": str(desktop_path)}


def _open_from_dashboard(app: QApplication, dialog: AIControlCenterDialog, button_id: str, domain_id: str):
    before = set(dialog._domain_windows.keys())
    result = _run_js(
        app,
        dialog,
        f"""
        (() => {{
          const button = document.getElementById({json.dumps(button_id)});
          if (!button) return JSON.stringify({{ ok: false, reason: "missing-button" }});
          button.click();
          return JSON.stringify({{ ok: true, label: button.textContent.trim(), target: button.dataset.launchTarget || "", kind: button.dataset.launchWindowKind || "" }});
        }})();
        """,
    )
    _pump(app, 700)
    window = dialog._domain_windows.get(domain_id)
    return result, window, before


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
    for domain_id, window in child_windows.items():
        if window is not None:
            screenshots[f"{domain_id}_opened"] = _capture_window(
                app,
                window,
                log_root,
                f"02_{domain_id}_opened",
            )

    readiness_result = {}
    if readiness_window is not None:
        _run_child_js(
            app,
            readiness_window,
            """
            (() => {
              const run = document.getElementById("run-local-check");
              const generate = document.getElementById("generate-report");
              const copy = document.getElementById("copy-report");
              if (run) run.click();
              if (generate) generate.click();
              if (copy) copy.click();
              return true;
            })();
            """,
        )
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
                    localResult: document.getElementById("local-result")?.textContent.trim() || "",
                    reportState: document.getElementById("report-state")?.textContent.trim() || "",
                    reportBodyVisible: !Boolean(document.getElementById("report-body")?.hidden),
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

    checks = {
        "dashboardHubCompactOnly": (
            dashboard_probe.get("title") == "AI Dashboard"
            and dashboard_probe.get("dashboardIaModel") == "ai-dashboard-global-strip-category-cards-launch-real-child-domain-windows"
            and dashboard_probe.get("dashboardSurfaceModel") == "hub-only-cards-are-doorways"
            and dashboard_probe.get("childWindowModel") == "dashboard-launchers-open-exclusive-or-external-unique-windows"
            and dashboard_probe.get("sameWindowFocusedSectionPolicy") == "blocked-as-dashboard-workspace-substitute"
            and dashboard_probe.get("cardNames") == ["control-center", "readiness-diagnostics", "capabilities-maintenance"]
            and dashboard_probe.get("focusedSurfaceCount") == 0
            and dashboard_probe.get("domainSurfaceCount") == 0
        ),
        "noInlineWorkspaceActions": (
            dashboard_probe.get("localCheckInline") is False
            and dashboard_probe.get("generateInline") is False
            and dashboard_probe.get("copyInline") is False
        ),
        "redundantCardsRemoved": (
            dashboard_probe.get("activeAiText") is False
            and dashboard_probe.get("trustProviderText") is False
        ),
        "settingsCogIconOnlyNoVisibleFutureCopy": (
            dashboard_probe.get("visibleSettingsFutureText") is False
            and dashboard_probe.get("nativeTitleTooltipCount") == 0
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
            and readiness_result.get("localResult") == "No provider configured"
            and readiness_result.get("reportState") == "Copied locally"
            and readiness_result.get("reportBodyVisible") is True
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
        "childWindowClassificationLedger": {
            "control-center": {
                "classification": "exclusive-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": True,
                "focusBehavior": "bring-to-front-if-open",
            },
            "readiness-diagnostics": {
                "classification": "external-unique",
                "remainsOpenIfDashboardCloses": True,
                "singleton": True,
                "focusBehavior": "bring-to-front-if-open",
            },
            "capabilities-maintenance": {
                "classification": "exclusive-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": True,
                "focusBehavior": "bring-to-front-if-open",
            },
        },
        "readinessResult": readiness_result,
        "singletonFocus": singleton_focus,
        "dashboardResizeProof": dashboard_resize_proof,
        "lifecycleAfterDashboardClose": lifecycle_after_dashboard_close,
        "childWindowsVisibleBeforeDashboardClose": child_windows_visible_before_close,
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
