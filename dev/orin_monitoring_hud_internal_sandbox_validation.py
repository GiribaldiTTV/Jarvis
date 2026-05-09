"""Internal sandbox validation for the FAM-006 Monitoring HUD Workstream.

This helper proves the current-branch Dashboard-first Workstream handoff without
asking the USER for a User Test Summary during Workstream or Branch Readiness.
It validates the bounded runtime seams for the HUD shell, controls,
provider-truthful telemetry, no-data/degraded states, visual warnings, source
truth, and naming sterilization. Overlay/display proof remains supporting
evidence unless that interface is later re-admitted.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.monitoring_hud_controls import build_monitoring_hud_controls_visibility_contract
from desktop.monitoring_hud_placement import build_monitoring_hud_placement_contract
from desktop.monitoring_hud_status import build_monitoring_hud_status_snapshot
from desktop.monitoring_hud_telemetry import build_monitoring_hud_telemetry_snapshot


LOG_ROOT = ROOT / "dev" / "logs" / "fam_006_monitoring_hud_internal_sandbox"


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _require_contains(text: str, needle: str, label: str, failures: list[str]) -> None:
    _require(needle in text, f"{label} is missing {needle!r}", failures)


def _retired_name() -> str:
    return "".join(chr(code) for code in (74, 97, 114, 118, 105, 115))


def _tracked_text_files() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        parts = set(relative.parts)
        if ".git" in parts or "__pycache__" in parts:
            continue
        if len(relative.parts) >= 2 and relative.parts[0] == "dev" and relative.parts[1] == "logs":
            continue
        if parts & {"dev", "desktop", "nexus_visual", "Docs", "Audio"} or path.name == "main.py":
            if path.suffix.lower() in {".py", ".pyw", ".ps1", ".md", ".txt", ".html", ".css", ".js", ".json"}:
                result.append(path)
    return result


def _validate_naming_sterilization(failures: list[str]) -> None:
    retired = _retired_name().casefold()
    for path in _tracked_text_files():
        relative = path.relative_to(ROOT)
        _require(retired not in str(relative).casefold(), f"{relative}: path contains retired product name", failures)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if retired in line.casefold():
                failures.append(f"{relative}:{line_number}: content contains retired product name")


def _validate_static_surface(failures: list[str]) -> None:
    branch_record = _read("Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md")
    helper_registry = _read("Docs/validation_helper_registry.md")
    phase_governance = _read("Docs/phase_governance.md")
    core_html = _read("nexus_visual/orin_core.html")
    core_css = _read("nexus_visual/orin_core.css")
    core_desktop_html = _read("nexus_visual/orin_core_desktop.html")
    core_desktop_css = _read("nexus_visual/orin_core_desktop.css")
    core_js = _read("nexus_visual/orin_core.js")
    html = _read("nexus_visual/monitoring_hud.html")
    css = _read("nexus_visual/monitoring_hud.css")
    js = _read("nexus_visual/monitoring_hud.js")
    renderer = _read("desktop/desktop_renderer.py")
    core_renderer = _read("desktop/core_visualization_renderer.py")
    tray = _read("desktop/orin_desktop_main.py")

    for needle in (
        "Primary Interface Release Surface: `Monitoring HUD Dashboard / control panel`",
        "Interface Bundle User Approval: `Not granted",
        "Dashboard Acceptance Pending",
        "Overlay Scope Deferred",
        "Core Repair Dependency Only",
        "Branch Readiness Interface Planning Incomplete: `Cleared by Stage 2-R13",
        "Workstream WS31 - Dashboard Control Panel Acceptance Baseline And Overlay Deferral Enforcement",
        "Workstream WS31 Dashboard Control Panel Acceptance Baseline And Overlay Deferral Enforcement",
        "WS31 Result: `Green - Dashboard-first acceptance baseline recorded",
        "Workstream WS32 Dashboard Standalone Window Movement Clipping And Core Overlay Decoupling Proof",
        "WS32 Result: `Green - Dashboard standalone window movement, clipping boundary, and Core/Overlay decoupling proof recorded",
        "Workstream WS33 Dashboard Settings Control Content Polish And Monitor Management Clarity",
        "WS33 Result: `Green - Dashboard settings/control content polish and monitor-management clarity recorded",
        "Workstream WS34 Dashboard Provider Setup No-Data Degraded Truth And Warning Posture Controls",
        "WS34 Result: `Green - Dashboard provider/setup/no-data/degraded truth and visual warning posture controls recorded",
        "Workstream WS35 Dashboard Specific Static Live Proof Screenshots And Live Validation UTS Boundary",
        "WS35 Result: `Green - Dashboard-specific static/live proof, screenshots, and Live Validation UTS boundary recorded",
        "Workstream WS36 Workstream Completion Review And Hardening Handoff Reconciliation",
        "WS36 Result: `Green - Dashboard-focused Workstream completion review passed and Hardening handoff recorded",
        "Next Active Seam: Hardening H1 - Monitoring HUD Product Surface Hardening Rerun",
    ):
        _require_contains(branch_record, needle, "FAM-006 Dashboard-first branch source truth", failures)
    for needle in (
        "Interface Release Boundary",
        "Primary Interface Release Surface:",
        "Interface Bundle User Approval:",
        "Branch Readiness Interface Planning Incomplete",
    ):
        _require_contains(phase_governance, needle, "interface release boundary governance", failures)
    for needle in (
        "Dashboard-first Workstream handoff posture",
        "Overlay/display deferred/non-gating classification",
        "WS35 dashboard-specific proof refresh and Live Validation UTS boundary",
        "Historical WS18-WS30 markers remain supporting repair evidence",
    ):
        _require_contains(helper_registry, needle, "monitoring HUD helper registry", failures)

    for label, text in (
        ("ORIN Core HTML", core_html),
        ("ORIN Core CSS", core_css),
        ("ORIN Core desktop HTML", core_desktop_html),
        ("ORIN Core desktop CSS", core_desktop_css),
        ("ORIN Core JavaScript", core_js),
    ):
        for forbidden in (
            "monitoring-hud",
            "Monitoring HUD",
            "monitoringHud",
            "MONITORING_HUD_",
        ):
            _require(
                forbidden not in text,
                f"{label} must remain HUD-free after standalone HUD split; found {forbidden!r}",
                failures,
            )

    for needle in (
        '<div id="scene">',
        '<div id="core-wrap">',
        '<script src="orin_core.js"></script>',
    ):
        _require_contains(core_html, needle, "ORIN Core restored visual markup", failures)

    for needle in (
        '<body class="desktop-mode">',
        '<link rel="stylesheet" href="orin_core_desktop.css" />',
        '<script src="orin_core.js"></script>',
    ):
        _require_contains(core_desktop_html, needle, "ORIN Core desktop visual markup", failures)

    for needle in (
        "background: #000;",
        "radial-gradient(circle at center, #03070d",
        "rgba(0,0,0,0.58) 100%",
    ):
        _require_contains(core_css, needle, "ORIN Core restored visual CSS", failures)

    for needle in (
        "background: transparent !important;",
        "body.desktop-mode #scene",
        "pointer-events: none;",
    ):
        _require_contains(core_desktop_css, needle, "ORIN Core desktop transparent CSS", failures)

    for needle in (
        'data-hud-module="monitoring-hud-shell-module"',
        'data-product-surface-role="dashboard-configuration-surface"',
        'data-configures-surface="monitoring-hud-minimal"',
        'data-split-contract="dashboard-configures-minimal-overlay"',
        'id="monitoring-hud-minimal"',
        'data-product-surface-role="minimal-anchored-hud-overlay"',
        'data-configured-by="monitoring-hud"',
        'data-native-overlay-owner="MonitoringHudOverlayDisplayWindow"',
        'data-native-window-split-proof="ready-ws26"',
        'data-click-through-proof="native-transparent-input"',
        'data-focus-proof="native-no-focus-noactivate"',
        'id="monitoring-hud-overlay-display"',
        'data-product-surface-role="edgeless-overlay-display"',
        'data-overlay-canvas="edge-to-edge-snipping-tool-style"',
        'data-overlay-edit-mode="unanchored-focusable-resizable-scrollable"',
        'data-overlay-anchor-mode="anchored-uninteractable-click-through"',
        'data-monitor-layout="movable-resizable-monitor-cards"',
        'data-watermark-identity="edge-safe-nexus-orin-watermark"',
        'data-edge-to-edge-posture="landscape-portrait-monitor-fit"',
        'data-interface-acceptance-policy="deferred-non-gating"',
        'data-dashboard-acceptance-role="supporting-future-interface-evidence"',
        'data-current-branch-release-gate="false"',
        'id="monitoring-hud-overlay-canvas"',
        'data-overlay-monitor-card="cpu"',
        'data-overlay-monitor-card="gpu"',
        "HUD Dashboard",
        'data-native-resize-model="os-edge-corner-resize"',
        "HUD Dashboard ready",
        'data-anchor-state="anchored"',
        'data-visibility-state="hidden-deferred"',
        'data-snap-state="enabled"',
        'data-card-model="category-sensor-cards"',
        'data-polling-default-ms="1000"',
        'data-drag-smoothing="native-os-window-move"',
        'data-scrollbar-style="nexus-thin-glow"',
        'data-frame-ownership="single-rounded-dashboard-chrome"',
        'data-scroll-owner="monitoring-hud-chrome"',
        'data-grid-scope="control-hub-cards-only"',
        'data-deadzone-policy="auto-height-content-no-empty-hit-zones"',
        'data-sticky-header-mask="opaque-scroll-mask"',
        'data-native-resize-hit-zone="all-edges-and-corners"',
        'data-sandbox-state-matrix="setup,no-data,degraded,ready,warning"',
        'data-dashboard-control-panel="hud-overlay-monitor-management"',
        'data-monitor-management="create-edit-enable-polling"',
        'data-overlay-mode-controls="overlay-deferred-tray-owned"',
        'data-primary-interface-release-surface="monitoring-hud-dashboard-control-panel"',
        'data-interface-acceptance-policy="dashboard-only-current-branch"',
        'data-dashboard-acceptance-baseline="ws31-dashboard-control-panel"',
        'data-dashboard-proof-path="dashboard-specific-static-live"',
        'data-dashboard-standalone-proof="ws32-dashboard-window-travel"',
        'data-dashboard-clipping-proof="within-virtual-desktop"',
        'data-dashboard-decoupling-proof="core-overlay-independent"',
        'data-dashboard-content-polish="ws45-clean-control-hub-ia"',
        'data-dashboard-settings-model="hud-overlay-monitor-groups-provider-warning"',
        'data-dashboard-ia-model="ws45-hub-actions-current-scope"',
        'data-dashboard-quick-access="warning-notifications-only"',
        'data-dashboard-global-feature-control="tray-owned"',
        'data-dashboard-deferred-action-policy="disabled-labeled-not-clickable"',
        'data-dashboard-card-order="hud-overlay-monitor-groups-data-sources-readiness"',
        'data-monitor-group-model="organizational-groups-settings-only"',
        'data-dashboard-monitor-card-policy="overlay-display-owns-monitor-cards"',
        'data-dashboard-provider-truth="provider-contract-first"',
        'data-dashboard-state-model="setup-no-data-degraded-warning"',
        'data-dashboard-warning-controls="visual-non-invasive-only"',
        'data-dashboard-fake-telemetry-policy="blocked"',
        'data-overlay-acceptance-policy="deferred-non-gating"',
        'data-interface-bundle-approval="not-granted"',
        'data-core-repair-classification="dependency-repair-only"',
        'id="monitoring-hud-warning-toggle"',
        'id="monitoring-hud-create-monitor-action"',
        'id="monitoring-hud-edit-monitor-action"',
        'id="monitoring-hud-monitor-list"',
        'id="monitoring-hud-monitor-selector"',
        'data-dashboard-monitor-display-policy="settings-only-no-monitor-cards"',
        'data-dashboard-content="control-hub-cards"',
        'data-child-window-model="hub-actions-standalone-child-windows-next"',
        'data-dashboard-hub-card="hud-overlay"',
        'data-dashboard-hub-card="monitor-groups"',
        'data-dashboard-hub-card="data-sources"',
        'data-dashboard-hub-card="readiness"',
        'data-monitor-config-option="cpu"',
        'data-monitor-config-option="gpu"',
        "CPU Group",
        "GPU Group",
        "2 Monitor Groups configured. Polling defaults to 1s inside Create/Edit, not on the Dashboard home.",
        "Monitor Groups",
        "Data Sources",
        "HUD Overlay",
        "Warning Notifications",
        "Readiness",
        "Waiting for safe provider",
        "Provider-first; no fake values",
        "HUD Overlay release acceptance is deferred.",
        "Deferred / non-gating",
        "Overlay settings are future branch scope",
        "Data Sources Window Deferred",
        "Show unavailable; no fake values",
        "Dashboard configures overlay behavior",
        "Monitor Groups organize what the future HUD Overlay shows; the Dashboard does not render display cards or fake values.",
    ):
        _require_contains(html, needle, "HUD HTML product surface", failures)
    for forbidden_home_copy in (
        "Default polling",
        "Warning posture",
        "Monitor group to edit",
        "Monitor group editor",
        "Dashboard proof",
        "Full desktop now; UTS only in Live Validation Stage 1",
    ):
        _require(
            forbidden_home_copy not in html,
            f"dashboard home must not include stale proof/inline-editor copy: {forbidden_home_copy}",
            failures,
        )
    for forbidden_dashboard_card in (
        'data-category-card="',
        'data-monitor-card="',
        'data-card-handle="',
        'data-card-resize="',
        "monitoring-hud-card",
    ):
        _require(forbidden_dashboard_card not in html, "dashboard must not render monitor cards outside overlay/minimal surfaces", failures)

    for needle in (
        'body.desktop-mode #monitoring-hud[data-anchor-state="unanchored"]',
        "body.desktop-mode #monitoring-hud-minimal",
        "body.desktop-mode #monitoring-hud-overlay-display",
        'body.desktop-mode #monitoring-hud-overlay-display[data-anchor-state="unanchored"]',
        ".monitoring-hud__toolbar",
        ".monitoring-hud__surface-role",
        ".monitoring-hud__config-heading",
        ".monitoring-hud__control-hub",
        ".monitoring-hud__hub-card",
        ".monitoring-hud__hub-card-topline",
        ".monitoring-hud__hub-action",
        ".monitoring-hud__state-row",
        ".monitoring-hud__selector-control",
        "#monitoring-hud-monitor-list-summary",
        ".monitoring-hud-minimal__frame",
        ".monitoring-hud-minimal-card",
        ".monitoring-hud-overlay-display__frame",
        ".monitoring-hud-overlay-display__canvas",
        ".monitoring-hud-overlay-display__watermark",
        ".monitoring-hud-overlay-card",
        ".monitoring-hud-overlay-card__quick-actions",
        ".monitoring-hud-overlay-card__topline",
        "scrollbar-width: thin",
        "body.desktop-mode .monitoring-hud__chrome::-webkit-scrollbar",
        'body.desktop-mode #monitoring-hud[data-drag-smoothing="native-os-window-move"]',
        "scrollbar-gutter: stable;",
    ):
        _require_contains(css, needle, "HUD CSS interaction surface", failures)

    for needle in (
        "window.getMonitoringHudControlState = function()",
        "window.getMonitoringHudSurfaceSplitState = function()",
        "window.getMonitoringHudDashboardAcceptanceState = function()",
        "window.setMonitoringHudControlState = function(state)",
        "monitoringHudUpdateSurfaceSplit",
        "primaryInterfaceReleaseSurface",
        "dashboardAcceptanceBaseline",
        "dashboardStandaloneProof",
        "dashboardClippingProof",
        "dashboardDecouplingProof",
        "dashboardContentPolish",
        "dashboardSettingsModel",
        "monitorGroupModel",
        "dashboardMonitorCardPolicy",
        "dashboardStandaloneMovementReady",
        "dashboardSettingsContentReady",
        "dashboardAcceptanceBaselineReady",
        "overlayAcceptanceNonGating",
        "monitoringHudPanelPositionFrame",
        "monitoringHudQueuedPanelPosition",
        "monitoringHudApplyPanelPosition",
        "window.requestAnimationFrame",
        'monitoringHud.dataset.scrollbarStyle = "nexus-thin-glow"',
        'monitoringHud.dataset.primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel"',
        'monitoringHud.dataset.dashboardAcceptanceBaseline = "ws31-dashboard-control-panel"',
        'monitoringHud.dataset.interfaceAcceptancePolicy = "dashboard-only-current-branch"',
        'monitoringHud.dataset.dashboardStandaloneProof = "ws32-dashboard-window-travel"',
        'monitoringHud.dataset.dashboardClippingProof = "within-virtual-desktop"',
        'monitoringHud.dataset.dashboardDecouplingProof = "core-overlay-independent"',
        'monitoringHud.dataset.dashboardContentPolish = "ws45-clean-control-hub-ia"',
        'monitoringHud.dataset.dashboardHomeModel = "control-hub-cards-no-inline-editor"',
        'monitoringHud.dataset.dashboardPollingPlacement = "monitor-group-editor-only"',
        'monitoringHud.dataset.dashboardProofContentPolicy = "validator-artifacts-not-home-surface"',
        'monitoringHud.dataset.dashboardChildWindowScope = "ws41-if-admitted"',
        'monitoringHud.dataset.dashboardSettingsModel = "hud-overlay-monitor-groups-provider-warning"',
        'monitoringHud.dataset.dashboardIaModel = "ws45-hub-actions-current-scope"',
        'monitoringHud.dataset.dashboardQuickAccess = "warning-notifications-only"',
        'monitoringHud.dataset.dashboardGlobalFeatureControl = "tray-owned"',
        'monitoringHud.dataset.dashboardDeferredActionPolicy = "disabled-labeled-not-clickable"',
        'monitoringHud.dataset.dashboardCardOrder = "hud-overlay-monitor-groups-data-sources-readiness"',
        'monitoringHud.dataset.monitorGroupModel = "organizational-groups-settings-only"',
        'monitoringHud.dataset.dashboardMonitorCardPolicy = "overlay-display-owns-monitor-cards"',
        'monitoringHud.dataset.dashboardProviderTruth = "provider-contract-first"',
        'monitoringHud.dataset.dashboardStateModel = "setup-no-data-degraded-warning"',
        'monitoringHud.dataset.dashboardWarningControls = "visual-non-invasive-only"',
        'monitoringHud.dataset.dashboardFakeTelemetryPolicy = "blocked"',
        "monitoringHud.dataset.warningControlPosture = monitoringHudControlState.warningNotificationsMuted",
        'monitoringHud.dataset.overlayAcceptancePolicy = "deferred-non-gating"',
        "MonitoringHudOverlayDisplayWindow",
        'monitoringHudMinimal.dataset.nativeWindowSplitProof = "ready-ws26"',
        'monitoringHudMinimal.dataset.clickThroughProof = monitoringHudControlState.anchored',
        'monitoringHudMinimal.dataset.focusProof = monitoringHudControlState.anchored',
        "monitoringHudRenderOverlayDisplay",
        "monitoringHudCreateOverlayCardNode",
        "minimal-anchored-hud-overlay",
        "dashboard-configuration-surface",
        "monitoringHudWirePanelDrag",
        'monitoringHud.dataset.nativeResizeModel = "os-edge-corner-resize"',
        'monitoringHud.dataset.frameOwnership = "single-rounded-dashboard-chrome"',
        'monitoringHud.dataset.scrollOwner = "monitoring-hud-chrome"',
        'monitoringHud.dataset.gridScope = "control-hub-cards-only"',
        'monitoringHud.dataset.deadzonePolicy = "auto-height-content-no-empty-hit-zones"',
        'monitoringHud.dataset.stickyHeaderMask = "opaque-scroll-mask"',
        'monitoringHud.dataset.nativeResizeHitZone = "all-edges-and-corners"',
        'document.body.classList.contains("desktop-mode")',
        "monitoringHudWireCardInteractions",
        "monitoringHudWireControls",
        "monitoringHudRenderMonitorManagement",
        "monitoringHudCreateCardNode",
        "monitoringHudRenderSensorCards",
        "monitoringHudStorageKey",
        "monitoringHudPollingRate.addEventListener",
        "monitoringHudControlState.snapEnabled",
        'monitoringHud.dataset.interactionMode = "standalone-dashboard-window"',
    ):
        _require_contains(js, needle, "HUD JavaScript controls", failures)

    for needle in (
        "MONITORING_HUD_WINDOW_STATUS_READY",
        "MONITORING_HUD_DASHBOARD_SURFACE_READY",
        "MONITORING_HUD_DASHBOARD_ACCEPTANCE_BASELINE_READY",
        "MONITORING_HUD_OVERLAY_DEFERRAL_ENFORCED_READY",
        "MONITORING_HUD_MINIMAL_OVERLAY_READY",
        "MONITORING_HUD_DASHBOARD_MINIMAL_SPLIT_READY",
        "MONITORING_HUD_DASHBOARD_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MOTION_POLISH_READY",
        "MONITORING_HUD_DASHBOARD_SCROLLBAR_STYLE_READY",
        "MONITORING_HUD_DASHBOARD_SETTINGS_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MONITOR_GROUP_CLARITY_READY",
        "MONITORING_HUD_DASHBOARD_OVERLAY_NON_GATING_COPY_READY",
        "MONITORING_HUD_EDGELESS_OVERLAY_CANVAS_READY",
        "MONITORING_HUD_STANDALONE_OVERLAY_DISPLAY_WINDOW_READY",
        "MONITORING_HUD_ANCHORED_OVERLAY_UNINTERACTABLE_READY",
        "MONITORING_HUD_OVERLAY_POSITION_PRESERVED_READY",
        "MONITORING_HUD_MINIMAL_NATIVE_OVERLAY_READY",
        "MONITORING_HUD_MINIMAL_ANCHORED_CLICK_THROUGH_READY",
        "MONITORING_HUD_MINIMAL_NON_FOCUS_READY",
        "standalone overlay display proves anchored uninteractable/no-focus",
        "emit_status=False",
        "MONITORING_HUD_WINDOW_OWNERSHIP_FOCUS_READY",
        "MONITORING_HUD_NATIVE_SYSTEM_MOVE_STARTED",
        "MONITORING_HUD_NATIVE_WINDOW_MOVE_READY",
        "MONITORING_HUD_NATIVE_WINDOW_RESIZE_READY",
        "MONITORING_HUD_NATIVE_SYSTEM_RESIZE_STARTED",
        "MONITORING_HUD_NATIVE_WINDOW_RESIZE_FALLBACK_STARTED",
        "MONITORING_HUD_DASHBOARD_SHELL_LAYOUT_READY",
        "MONITORING_HUD_DASHBOARD_VISUAL_SHELL_READY",
        "os-system-move-no-snap",
        "os-edge-corner-resize",
        "fallback-edge-corner-resize",
        "all-edges-and-corners",
        "fallback-direct-move-no-snap",
        "startSystemMove",
        "startSystemResize",
        "WS_EX_APPWINDOW",
        "WS_EX_TOOLWINDOW",
        "self.setWindowFlag(Qt.Window, True)",
        "MONITORING_HUD_DASHBOARD_STANDALONE_WINDOW_TRAVEL_READY",
        "MONITORING_HUD_DASHBOARD_CLIPPING_BOUNDARY_READY",
        "MONITORING_HUD_DASHBOARD_CORE_OVERLAY_DECOUPLING_READY",
        "request_monitoring_hud_unanchor_from_tray",
        "request_monitoring_hud_toggle_from_tray",
        "request_monitoring_hud_dashboard_from_tray",
        "MONITORING_HUD_INTERACTION_MODE_READY",
        "MONITORING_HUD_CONTROL_STATE_READY",
        "MONITORING_HUD_TRAY_ENABLE_RENDER_STABLE_READY",
        "MONITORING_HUD_TRAY_ENABLE_DISABLE_ROUNDTRIP_READY",
        "MONITORING_HUD_TRAY_DASHBOARD_OPEN_CLOSE_READY",
        "MONITORING_HUD_DISABLE_RECOVERY_READY",
        "MONITORING_HUD_MONITOR_MANAGEMENT_READY",
        "MONITORING_HUD_TRAY_UNANCHOR_DEFERRED",
        "MONITORING_HUD_TRAY_TOGGLE_READY",
        "CORE_VISUALIZATION_HUD_SURFACE_SEPARATION_READY",
        "surfaceSeparationOk",
        "native_cpu_load_bounded",
    ):
        _require_contains(renderer, needle, "desktop renderer HUD runtime", failures)

    for needle in (
        "from desktop.core_visualization_renderer import CoreVisualizationWindow",
        "DesktopRuntimeUnavailable",
        "DESKTOP_RUNTIME_UNAVAILABLE",
        'visual_html_path = os.path.join(ROOT_DIR, "nexus_visual", "orin_core_desktop.html")',
        "resolve_core_visualization_screen",
        "CORE_VISUALIZATION_PRESET_MONITOR_SELECTION_READY",
    ):
        _require_contains(tray, needle, "desktop launcher Core/HUD failure isolation", failures)

    for needle in (
        "class CoreVisualizationWindow(QWidget):",
        "CORE_VISUALIZATION_WINDOW_READY|surface=separate_persona_core",
        "CORE_VISUALIZATION_DESKTOP_LAYER_READY",
        "CORE_VISUALIZATION_WINDOW_GEOMETRY_READY",
        "CORE_VISUALIZATION_WORKERW_COORDINATE_REBASE_READY",
        "CORE_VISUALIZATION_FIXED_PRESET_MONITOR_READY",
        "CORE_VISUALIZATION_INDEPENDENT_PRESET_MONITOR_READY",
        "background-color: transparent",
        "setFixedSize",
        "compute_core_parent_geometry",
        "coordinate_space=\"parent\"",
        "desktop_screen_geometry",
        "desktop_layer=workerw",
        "hud_attachment=none",
        "ncp_attachment=none",
        "position_desktop_child",
    ):
        _require_contains(core_renderer, needle, "independent ORIN Core renderer", failures)
    _require(
        "WindowStaysOnTopHint" not in core_renderer,
        "independent ORIN Core renderer must not request topmost foreground ownership",
        failures,
    )

    for needle in (
        "monitoring_hud_html_path",
        'surface_role="hud"',
        "Enable HUD Feature",
        "Open HUD Dashboard",
        "Unanchor Monitoring HUD",
        "TRAY_MONITORING_HUD_TOGGLE_REQUESTED",
        "TRAY_MONITORING_HUD_DASHBOARD_REQUESTED",
        "TRAY_MONITORING_HUD_UNANCHOR_REQUESTED",
    ):
        _require_contains(tray, needle, "desktop tray HUD controls", failures)


def _validate_contracts(failures: list[str]) -> dict[str, object]:
    first = build_monitoring_hud_telemetry_snapshot(
        page_ready=True,
        desktop_mode=True,
        runtime_log_path=str(LOG_ROOT / "runtime_log.txt"),
        event_route_present=True,
        polling_rate_ms=1000,
    ).as_dict()
    time.sleep(0.05)
    second = build_monitoring_hud_telemetry_snapshot(
        page_ready=True,
        desktop_mode=True,
        runtime_log_path=str(LOG_ROOT / "runtime_log.txt"),
        event_route_present=True,
        polling_rate_ms=1000,
    ).as_dict()
    placement = build_monitoring_hud_placement_contract(
        desktop_mode=True,
        x=100,
        y=120,
        width=900,
        height=700,
    ).as_dict()
    controls = build_monitoring_hud_controls_visibility_contract(
        desktop_mode=True,
        visible=True,
        anchored=False,
        snap_enabled=True,
        polling_rate_ms=1000,
    ).as_dict()
    status = build_monitoring_hud_status_snapshot(
        page_ready=True,
        desktop_mode=True,
        event_route_present=True,
    ).as_dict()

    cards = second.get("sensorCards") or []
    sensors = {
        sensor.get("id"): sensor
        for card in cards
        for sensor in card.get("sensors", [])
        if isinstance(sensor, dict)
    }
    _require(second.get("pollingRateMs") == 1000, "telemetry contract must use 1s default polling", failures)
    _require(second.get("liveValues") in {"native-cpu-load-only", "provider-required"}, "telemetry contract has invalid live value state", failures)
    _require("cpu-load" in sensors, "telemetry contract is missing CPU load sensor", failures)
    _require(sensors.get("gpu-load", {}).get("value") == "Unavailable", "GPU load must remain provider-unavailable", failures)
    _require(sensors.get("gpu-thermal", {}).get("value") == "Unavailable", "GPU thermal must remain provider-unavailable", failures)
    _require(sensors.get("cpu-thermal", {}).get("value") == "Provider required", "CPU thermal must remain provider-required", failures)
    _require(
        placement.get("snapModel") == "Dashboard window movement is unsnapped; Overlay layout snap remains deferred",
        "placement contract must describe Dashboard unsnapped movement posture",
        failures,
    )
    _require(placement.get("cardLayoutModel") == "cards resize and snap in overlay edit mode", "placement contract must describe card layout", failures)
    _require(controls.get("anchorState") == "overlay-deferred", "controls contract must keep overlay anchor controls deferred", failures)
    _require(controls.get("pollingRateMs") == "1000", "controls contract must preserve 1s default polling", failures)
    _require(
        controls.get("monitorManagement") == "Dashboard creates, edits, enables, disables, and sets polling for monitor groups",
        "controls contract must describe dashboard monitor management",
        failures,
    )
    _require(
        controls.get("overlayModeControls") == "Overlay display and anchor/unanchor controls are deferred/non-gating",
        "controls contract must describe overlay mode controls",
        failures,
    )
    _require(
        controls.get("warningControls") == "Visual badge, text label, and color state only; no audio or screen flash",
        "controls contract must preserve visual/non-invasive warning controls",
        failures,
    )
    _require(status.get("warningPosture") == "Visual badge, color state, and text label only", "status contract must preserve visual warning posture", failures)

    return {
        "firstTelemetry": first,
        "secondTelemetry": second,
        "placement": placement,
        "controls": controls,
        "status": status,
    }


def _write_manifest(status: str, failures: list[str], contracts: dict[str, object]) -> Path:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    manifest_path = LOG_ROOT / f"{stamp}_manifest.json"
    payload = {
        "status": status,
        "package": "PKG-006",
        "phase": "Workstream",
        "seam": "WS33 dashboard settings content and monitor-management clarity sandbox consolidation",
        "contracts": contracts,
        "failures": failures,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return manifest_path


def validate() -> tuple[list[str], Path]:
    failures: list[str] = []
    _validate_naming_sterilization(failures)
    _validate_static_surface(failures)
    contracts = _validate_contracts(failures)
    status = "PASS" if not failures else "FAIL"
    manifest_path = _write_manifest(status, failures, contracts)
    return failures, manifest_path


def main() -> int:
    failures, manifest_path = validate()
    if failures:
        print("FAIL: FAM-006 Monitoring HUD internal sandbox validation failed")
        for failure in failures:
            print(f"- {failure}")
        print(f"manifest: {manifest_path}")
        return 1

    print("PASS: FAM-006 Monitoring HUD internal sandbox validation is green")
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
