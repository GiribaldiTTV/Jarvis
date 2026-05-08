"""Validate the FAM-006 Monitoring HUD product surface baseline.

This helper is intentionally static. It proves the Dashboard-first HUD
Workstream handoff posture, current dashboard/control-panel markers,
provider-contract truth, no-data/degraded copy, warning posture, and
live/internal proof helper markers without inventing metric values or widening
into deferred product lanes.
Overlay/display markers remain supporting evidence unless source truth later
admits that interface as the active release surface.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _require_contains(text: str, needle: str, label: str, failures: list[str]) -> None:
    _require(needle in text, f"{label} is missing {needle!r}", failures)


def _html_section(text: str) -> str:
    match = re.search(
        r'<section\s+id="monitoring-hud".*?</section>',
        text,
        flags=re.DOTALL,
    )
    return match.group(0) if match else ""


def _html_section_by_id(text: str, section_id: str) -> str:
    pattern = rf'<section\s+id="{re.escape(section_id)}".*?</section>'
    match = re.search(pattern, text, flags=re.DOTALL)
    return match.group(0) if match else ""


def _require_no_collection_imports(text: str, label: str, failures: list[str]) -> None:
    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "win32", "powershell"):
        _require(
            forbidden not in text.casefold(),
            f"{label} must not perform {forbidden} collection in the WS7 product baseline",
            failures,
        )


def validate() -> list[str]:
    failures: list[str] = []

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
    telemetry = _read("desktop/monitoring_hud_telemetry.py")
    placement = _read("desktop/monitoring_hud_placement.py")
    controls = _read("desktop/monitoring_hud_controls.py")
    status = _read("desktop/monitoring_hud_status.py")
    live_validation = _read("dev/orin_monitoring_hud_live_validation.ps1")
    branch_record = _read("Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md")
    helper_registry = _read("Docs/validation_helper_registry.md")
    phase_governance = _read("Docs/phase_governance.md")

    for needle in (
        "Primary Interface Release Surface: `Monitoring HUD Dashboard / control panel`",
        "Interface Bundle User Approval: `Not granted",
        "Dashboard Acceptance Pending",
        "Overlay Scope Deferred",
        "Core Repair Dependency Only",
        "Branch Readiness Interface Planning Incomplete: `Cleared by Stage 2-R13",
        "Stage 1-R10 PASS Recording:",
        "Workstream WS31 - Dashboard Control Panel Acceptance Baseline And Overlay Deferral Enforcement",
        "Workstream WS31 Dashboard Control Panel Acceptance Baseline And Overlay Deferral Enforcement",
        "WS31 Result: `Green - Dashboard-first acceptance baseline recorded",
        "Next Active Seam: Workstream WS32 - Dashboard Standalone Window Movement Clipping And Core Overlay Decoupling Proof",
    ):
        _require_contains(branch_record, needle, "FAM-006 Dashboard-first branch source truth", failures)
    for needle in (
        "Interface Release Boundary",
        "Primary Interface Release Surface:",
        "Interface Bundle User Approval:",
        "Multiple Interface Release Drift",
    ):
        _require_contains(phase_governance, needle, "interface release boundary governance", failures)
    for needle in (
        "Stage 2-R13 Dashboard-first Workstream handoff source-truth markers",
        "Dashboard-first Interface Release Boundary source-truth markers",
        "Overlay/display deferred/non-gating proof classification",
        "future Overlay/display proof only when that interface is re-admitted",
    ):
        _require_contains(helper_registry, needle, "monitoring HUD helper registry", failures)

    for label, text in (
        ("ORIN Core HTML", core_html),
        ("ORIN Core CSS", core_css),
        ("ORIN Core desktop HTML", core_desktop_html),
        ("ORIN Core desktop CSS", core_desktop_css),
        ("ORIN Core JavaScript", core_js),
    ):
        _require(
            "monitoring-hud" not in text and "Monitoring HUD" not in text,
            f"{label} must not contain Monitoring HUD surface markup, styles, or behavior",
            failures,
        )

    for needle in (
        '<div id="scene">',
        '<div id="core-wrap">',
        '<script src="orin_core.js"></script>',
    ):
        _require_contains(core_html, needle, "ORIN Core restored visual surface", failures)

    for needle in (
        '<body class="desktop-mode">',
        '<link rel="stylesheet" href="orin_core_desktop.css" />',
        '<script src="orin_core.js"></script>',
    ):
        _require_contains(core_desktop_html, needle, "ORIN Core desktop visual surface", failures)

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
        _require_contains(core_desktop_css, needle, "ORIN Core desktop transparent visual CSS", failures)

    hud_section = _html_section(html)
    minimal_hud_section = _html_section_by_id(html, "monitoring-hud-minimal")
    overlay_display_section = _html_section_by_id(html, "monitoring-hud-overlay-display")
    _require(bool(hud_section), "orin_core.html is missing the monitoring-hud section", failures)
    _require(bool(minimal_hud_section), "monitoring_hud.html is missing the monitoring-hud-minimal section", failures)
    _require(bool(overlay_display_section), "monitoring_hud.html is missing the monitoring-hud-overlay-display section", failures)
    for needle in (
        'data-package="PKG-006"',
        'data-slice="SLC-016"',
        'data-product-surface-role="dashboard-configuration-surface"',
        'data-configures-surface="monitoring-hud-minimal"',
        'data-native-dashboard-owner="DesktopRuntimeWindow"',
        'data-standalone-window-contract="dashboard-overlay-core-independent-native-surfaces"',
        'data-split-contract="dashboard-configures-minimal-overlay"',
        'data-slice="SLC-025"',
        'data-slice="SLC-026"',
        'data-slice="SLC-027"',
        'data-slice="SLC-028"',
        'data-hud-module="monitoring-hud-shell-module"',
        'data-product-surface="nexus-monitoring-hud"',
        'data-isolation-boundary="standalone-hud-layer"',
        'data-core-failure-isolation="hud-fail-does-not-hide-core"',
        'data-interaction-mode="anchored-click-through"',
        'data-anchor-state="anchored"',
        'data-visibility-state="visible"',
        'data-snap-state="enabled"',
        'data-card-model="category-sensor-cards"',
        'data-provider-state="setup-required"',
        'data-warning-mode="visual-non-invasive"',
        'data-live-values="provider-required"',
        'data-polling-default-ms="1000"',
        'data-polling-options-ms="1000,2000,5000,10000"',
        'data-keybind-policy="none"',
        'data-drag-smoothing="raf-local-persist-on-release"',
        'data-scrollbar-style="nexus-thin-glow"',
        'data-sandbox-state-matrix="setup,no-data,degraded,ready,warning"',
        'data-dashboard-control-panel="hud-display-monitor-management"',
        'data-monitor-management="create-edit-enable-polling"',
        'data-overlay-mode-controls="enable-disable-anchor-unanchor"',
        'data-primary-interface-release-surface="monitoring-hud-dashboard-control-panel"',
        'data-interface-acceptance-policy="dashboard-only-current-branch"',
        'data-dashboard-acceptance-baseline="ws31-dashboard-control-panel"',
        'data-dashboard-proof-path="dashboard-specific-static-live-uts"',
        'data-overlay-acceptance-policy="deferred-non-gating"',
        'data-interface-bundle-approval="not-granted"',
        'data-core-repair-classification="dependency-repair-only"',
        'aria-label="Nexus Desktop AI Monitoring HUD product surface"',
        'aria-label="Dashboard monitor selector and configuration entry point"',
        'aria-hidden="true"',
        "Nexus Desktop AI",
        "Monitoring HUD",
        "Monitoring Dashboard",
        "Configures the minimal anchored Monitoring HUD overlay.",
        "Dashboard surface",
        "Configuration/settings window",
        "Separate anchored overlay configured here",
        "Dashboard acceptance only",
        "HUD enabled",
        "Anchored",
        "Provider setup required",
        "Hardware values stay hidden until a safe provider and validation route exist.",
        'id="monitoring-hud-toggle"',
        'id="monitoring-hud-anchor-toggle"',
        'id="monitoring-hud-create-monitor"',
        'id="monitoring-hud-snap-toggle"',
        'id="monitoring-hud-polling-rate"',
        "Movable panel",
        "Snap-ready",
        "Anchored click-through",
        "Task tray unanchor path",
        "No default keybinds",
        'id="monitoring-hud-monitor-list"',
        'id="monitoring-hud-monitor-selector"',
        'data-dashboard-monitor-display-policy="settings-only-no-monitor-cards"',
        'data-monitor-config-option="cpu"',
        'data-monitor-config-option="gpu"',
        "Overlay owns monitor cards; dashboard edits their settings.",
        "CPU Monitor",
        "GPU Monitor",
        "Provider setup required",
        "Enabled in overlay",
        "Overlay owns monitor cards; dashboard edits their settings.",
        'data-dashboard-content="sensor-setup"',
        'data-dashboard-content="minimal-hud-output"',
        'data-dashboard-content="user-controls"',
        'data-dashboard-content="readiness-states"',
        'data-dashboard-content="next-actions"',
        "Sensor setup",
        "Tell me what can be trusted",
        "Waiting for safe provider",
        "Provider-first; no fake values",
        "1s after provider proof",
        "Minimal HUD output",
        "Configure the small overlay",
        "Separate minimal HUD overlay",
        "Anchor anywhere after OS proof",
        "Cards resize and snap in overlay edit mode",
        "Controls",
        "Adjust without cluttering the HUD",
        "Show or hide from dashboard/tray",
        "Unanchor to edit; anchor to observe",
        "Snap cards; save local layout",
        "Readiness states",
        "Be clear when data is not ready",
        "Show unavailable; no fake values",
        "Name reconnect/setup gap",
        "Next actions",
        "What the user can trust now",
        "Visual badge only",
        "Full desktop and UTS later",
        "Provider setup before live values",
        "PKG-006 in progress",
        'data-dashboard-content="monitor-management"',
        "Monitor editor",
        "Dashboard-owned control panel",
        "Enabled in overlay",
        "Monitor polling",
        "Monitors group sensors; they do not fake hardware values.",
    ):
        _require_contains(hud_section, needle, "monitoring HUD HTML", failures)

    for forbidden_dashboard_card in (
        'data-category-card="',
        'data-monitor-card="',
        'data-card-handle="',
        'data-card-resize="',
        "monitoring-hud-card",
    ):
        _require(
            forbidden_dashboard_card not in hud_section,
            "dashboard HTML must not render monitor cards; cards belong to the overlay display",
            failures,
        )

    retired_product_name = "".join(chr(code) for code in (74, 97, 114, 118, 105, 115)).casefold()
    for forbidden in ("voice", "audio", "spoken", "microphone", retired_product_name):
        _require(
            forbidden not in hud_section.casefold(),
            f"monitoring HUD HTML must not introduce {forbidden} behavior in WS7",
            failures,
        )

    for needle in (
        'data-package="PKG-006"',
        'data-slice="SLC-016"',
        'data-placement-slice="SLC-026"',
        'data-status-slice="SLC-028"',
        'data-proof-slice="SLC-029"',
        'data-product-surface="nexus-monitoring-hud-minimal"',
        'data-product-surface-role="minimal-anchored-hud-overlay"',
        'data-renderer-owner="MonitoringHudWindow"',
        'data-configured-by="monitoring-hud"',
        'data-dashboard-owner="monitoring-hud"',
        'data-split-contract="dashboard-configures-minimal-overlay"',
        'data-native-overlay-owner="MonitoringHudOverlayDisplayWindow"',
        'data-native-window-split-proof="ready-ws26"',
        'data-click-through-proof="native-transparent-input"',
        'data-focus-proof="native-no-focus-noactivate"',
        'data-interface-acceptance-policy="deferred-non-gating"',
        'data-dashboard-acceptance-role="supporting-future-interface-evidence"',
        'data-current-branch-release-gate="false"',
        'aria-label="Nexus Desktop AI minimal anchored Monitoring HUD overlay"',
        "Minimal HUD enabled",
        "Provider setup required",
        "Provider warming",
        "Provider required",
        "Visual warning baseline only",
    ):
        _require_contains(minimal_hud_section, needle, "minimal monitoring HUD HTML", failures)
    for forbidden in ("voice", "audio", "spoken", "microphone", retired_product_name):
        _require(
            forbidden not in minimal_hud_section.casefold(),
            f"minimal monitoring HUD HTML must not introduce {forbidden} behavior in WS19",
            failures,
        )

    for needle in (
        'id="monitoring-hud-overlay-display"',
        'data-product-surface="nexus-monitoring-hud-overlay-display"',
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
        "Nexus Desktop AI / ORIN",
    ):
        _require_contains(overlay_display_section, needle, "edgeless overlay display HTML", failures)
    for forbidden in ("voice", "audio", "spoken", "microphone", retired_product_name):
        _require(
            forbidden not in overlay_display_section.casefold(),
            f"edgeless overlay display HTML must not introduce {forbidden} behavior in WS25",
            failures,
        )

    fake_metric_pattern = re.compile(
        r"\b\d+(?:\.\d+)?\s?(?:°|c\b|%|rpm\b|mhz\b|ghz\b|w\b)",
        flags=re.IGNORECASE,
    )
    _require(
        fake_metric_pattern.search(hud_section) is None,
        "monitoring HUD HTML must not present numeric hardware values before provider proof exists",
        failures,
    )

    for needle in (
        "#monitoring-hud {",
        "#monitoring-hud-minimal {",
        "#monitoring-hud-overlay-display {",
        "display: none;",
        "body.desktop-mode #monitoring-hud",
        "body.desktop-mode #monitoring-hud-minimal",
        "body.desktop-mode #monitoring-hud-overlay-display",
        'body.desktop-mode #monitoring-hud-overlay-display[data-anchor-state="unanchored"]',
        "width: min(780px, calc(100vw - 24px));",
        "scrollbar-width: thin;",
        "scrollbar-color: rgba(108, 232, 255, 0.52) rgba(5, 18, 31, 0.34);",
        "body.desktop-mode #monitoring-hud::-webkit-scrollbar",
        "body.desktop-mode #monitoring-hud::-webkit-scrollbar-thumb",
        'body.desktop-mode #monitoring-hud[data-drag-smoothing="raf-local-persist-on-release"]',
        'font-family: "Bahnschrift", "Rajdhani", "Segoe UI", sans-serif;',
        "pointer-events: auto",
        'body.desktop-mode #monitoring-hud[data-anchor-state="unanchored"]',
        ".monitoring-hud__chrome",
        ".monitoring-hud__toolbar",
        ".monitoring-hud__surface-role",
        ".monitoring-hud__config-heading",
        ".monitoring-hud__anchor-rail",
        ".monitoring-hud__monitor-selector",
        ".monitoring-hud__selector-control",
        "#monitoring-hud-monitor-list-summary",
        ".monitoring-hud__monitor-editor",
        ".monitoring-hud__inline-control",
        '.monitoring-hud__inline-control input[type="checkbox"]',
        ".monitoring-hud-minimal__frame",
        ".monitoring-hud-minimal__topline",
        ".monitoring-hud-minimal__cards",
        ".monitoring-hud-minimal-card",
        ".monitoring-hud-minimal__warning",
        ".monitoring-hud-overlay-display__frame",
        ".monitoring-hud-overlay-display__canvas",
        ".monitoring-hud-overlay-display__watermark",
        ".monitoring-hud-overlay-card",
        ".monitoring-hud-overlay-card__quick-actions",
        ".monitoring-hud-overlay-card__topline",
        "cursor: nwse-resize",
        ".monitoring-hud__resize-corner",
        ".monitoring-hud--validation-fault",
        "@media (max-width: 760px), (max-height: 620px)",
        "@keyframes monitoringHudSettle",
    ):
        _require_contains(css, needle, "monitoring HUD CSS", failures)

    for needle in (
        'const monitoringHud = document.getElementById("monitoring-hud")',
        'const monitoringHudMinimal = document.getElementById("monitoring-hud-minimal")',
        'const monitoringHudOverlayDisplay = document.getElementById("monitoring-hud-overlay-display")',
        'const monitoringHudOverlayCanvas = document.getElementById("monitoring-hud-overlay-canvas")',
        'const monitoringHudProviderState = document.getElementById("monitoring-hud-provider-state")',
        'const monitoringHudMinimalProviderState = document.getElementById("monitoring-hud-minimal-provider-state")',
        'const monitoringHudWarningPosture = document.getElementById("monitoring-hud-warning-posture")',
        'const monitoringHudTrayPath = document.getElementById("monitoring-hud-tray-path")',
        'const monitoringHudAnchorToggle = document.getElementById("monitoring-hud-anchor-toggle")',
        'const monitoringHudCreateMonitor = document.getElementById("monitoring-hud-create-monitor")',
        'const monitoringHudMonitorList = document.getElementById("monitoring-hud-monitor-list")',
        'const monitoringHudMonitorSelector = document.getElementById("monitoring-hud-monitor-selector")',
        'const monitoringHudPollingRate = document.getElementById("monitoring-hud-polling-rate")',
        'const monitoringHudMonitorEnabled = document.getElementById("monitoring-hud-monitor-enabled")',
        'const monitoringHudMonitorPollingRate = document.getElementById("monitoring-hud-monitor-polling-rate")',
        "window.getMonitoringHudControlState = function()",
        "window.getMonitoringHudLiveClientGeometry = function()",
        "minimalHud: rectFor(\"#monitoring-hud-minimal\")",
        "window.getMonitoringHudSurfaceSplitState = function()",
        "window.getMonitoringHudDashboardAcceptanceState = function()",
        "window.getMonitoringHudIsolationState = function()",
        "primaryInterfaceReleaseSurface",
        "dashboardAcceptanceBaseline",
        "dashboardProofPath",
        "interfaceAcceptancePolicy",
        "overlayAcceptancePolicy",
        "interfaceBundleApproval",
        "dashboardAcceptanceBaselineReady",
        "overlayAcceptanceNonGating",
        "dashboardMinimalSplitReady",
        "minimal-anchored-hud-overlay",
        "dashboard-configuration-surface",
        "dashboard-configures-minimal-overlay",
        "MonitoringHudOverlayDisplayWindow",
        'monitoringHudMinimal.dataset.nativeWindowSplitProof = "ready-ws26"',
        'monitoringHudMinimal.dataset.clickThroughProof = monitoringHudControlState.anchored',
        'monitoringHudMinimal.dataset.focusProof = monitoringHudControlState.anchored',
        "monitoringHudPanelPositionFrame",
        "monitoringHudQueuedPanelPosition",
        "monitoringHudApplyPanelPosition",
        "window.requestAnimationFrame",
        "monitoringHudSetPanelPosition(rect.left + dx, rect.top + dy, false)",
        'monitoringHud.dataset.dragSmoothing = "raf-local-persist-on-release"',
        'monitoringHud.dataset.scrollbarStyle = "nexus-thin-glow"',
        'monitoringHud.dataset.primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel"',
        'monitoringHud.dataset.dashboardAcceptanceBaseline = "ws31-dashboard-control-panel"',
        'monitoringHud.dataset.interfaceAcceptancePolicy = "dashboard-only-current-branch"',
        'monitoringHud.dataset.overlayAcceptancePolicy = "deferred-non-gating"',
        "standaloneHudWindow",
        "coreSceneHiddenInHudWindow",
        "hudWindowMode",
        "window.simulateMonitoringHudFaultForValidation = function(enabled)",
        "window.setMonitoringHudControlState = function(state)",
        "monitoringHudWirePanelDrag",
        "monitoringHudWireCardInteractions",
        "monitoringHudWireControls",
        "monitoringHudRenderMonitorManagement",
        "monitoringHudCreateCardNode",
        "monitoringHudRenderOverlayDisplay",
        "monitoringHudCreateOverlayCardNode",
        "monitoringHudClearPanelPosition",
        "monitoringHudRenderSensorCards",
        "window.setDesktopSurfaceMode = function(enabled)",
        'monitoringHud.dataset.renderState = isEnabled ? "product-visibility-baseline" : "hidden"',
        'monitoringHud.dataset.productSurfaceState = isEnabled ? "visible-user-facing" : "hidden"',
        'monitoringHudMinimal.dataset.productSurfaceState = isEnabled ? "visible-minimal-anchored-hud" : "hidden"',
        "window.setMonitoringHudTelemetry = function(snapshot)",
        'monitoringHud.dataset.providerState = monitoringHudTelemetry.providerState || "setup-required"',
        'monitoringHud.dataset.liveValues = monitoringHudTelemetry.liveValues || "provider-required"',
        'monitoringHudProviderState.textContent = monitoringHudTelemetry.providerLabel || "Provider setup required"',
        "window.setMonitoringHudPlacementOwnership = function(contract)",
        'monitoringHud.dataset.interactionMode = monitoringHudControlState.anchored ? "anchored-click-through" : "unanchored-edit-mode"',
        'monitoringHudPlacementAnchor.textContent = monitoringHudPlacement.anchor || "Anchor anywhere after OS proof"',
        'monitoringHudResizePosture.textContent = monitoringHudPlacement.resizePosture || "Cards resize and snap in overlay edit mode"',
        "window.setMonitoringHudControlsVisibility = function(contract)",
        'monitoringHud.dataset.controlsState = monitoringHudControlState.visible ? "toggle-posture-visible" : "toggle-posture-hidden"',
        'monitoringHud.dataset.keybindPolicy = "none"',
        'monitoringHud.dataset.monitorManagement = "create-edit-enable-polling"',
        'monitoringHud.dataset.overlayModeControls = "enable-disable-anchor-unanchor"',
        'monitoringHudControlsVisibility.textContent = monitoringHudControls.visibilityState || "Show or hide from dashboard/tray"',
        'monitoringHudControlsSurface.textContent = monitoringHudControls.controlSurface || "Unanchor to edit; anchor to observe"',
        'monitoringHudControlsPersistence.textContent = monitoringHudControls.persistence || "Snap cards; save local layout"',
        'monitoringHudTrayPath.textContent = monitoringHudControls.trayPath || "Task tray unanchor path"',
        "window.setMonitoringHudStatusBehavior = function(snapshot)",
        'monitoringHud.dataset.warningMode = "visual-non-invasive"',
        'monitoringHudWarningPosture.textContent = monitoringHudStatus.warningPosture || "Visual badge only"',
        "monitoringHudInitializeControls();",
        "window.setDesktopSurfaceMode(false)",
        "window.setMonitoringHudTelemetry({})",
        "window.setMonitoringHudPlacementOwnership({})",
        "window.setMonitoringHudControlsVisibility({})",
        "window.setMonitoringHudStatusBehavior({})",
    ):
        _require_contains(js, needle, "monitoring HUD JavaScript", failures)

    for needle in (
        "from .monitoring_hud_controls import build_monitoring_hud_controls_visibility_contract",
        "from .monitoring_hud_placement import build_monitoring_hud_placement_contract",
        "from .monitoring_hud_status import build_monitoring_hud_status_snapshot",
        "from .monitoring_hud_telemetry import build_monitoring_hud_telemetry_snapshot",
        'surface_role: str = "hud"',
        "def _apply_desktop_surface_mode(self):",
        "hud-window-mode",
        "core-window-mode",
        'monitoringHud.dataset.renderState = "product-visibility-baseline"',
        'monitoringHud.dataset.productSurfaceState = "visible-user-facing"',
        "MONITORING_HUD_BASELINE_READY",
        'baseline="product_visibility_baseline"',
        "MONITORING_HUD_PRODUCT_VISIBILITY_READY",
        'seam="WS7"',
        'proof="visible_hud_card_panel"',
        "MONITORING_HUD_DASHBOARD_SURFACE_READY",
        "MONITORING_HUD_DASHBOARD_ACCEPTANCE_BASELINE_READY",
        "MONITORING_HUD_OVERLAY_DEFERRAL_ENFORCED_READY",
        'seam="WS31"',
        'acceptance_policy="dashboard_only_current_branch"',
        'overlay_acceptance="deferred_non_gating"',
        'surface="dashboard_configuration_surface"',
        "MONITORING_HUD_MINIMAL_OVERLAY_READY",
        'surface="minimal_anchored_hud_overlay"',
        "MONITORING_HUD_DASHBOARD_MINIMAL_SPLIT_READY",
        'native_window_split_proof="ready_ws26"',
        "MONITORING_HUD_DASHBOARD_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MOTION_POLISH_READY",
        "MONITORING_HUD_DASHBOARD_SCROLLBAR_STYLE_READY",
        "MONITORING_HUD_EDGELESS_OVERLAY_CANVAS_READY",
        "class MonitoringHudOverlayDisplayWindow(QWidget):",
        "MONITORING_HUD_STANDALONE_OVERLAY_DISPLAY_WINDOW_READY",
        "MONITORING_HUD_ANCHORED_OVERLAY_UNINTERACTABLE_READY",
        "MONITORING_HUD_OVERLAY_POSITION_PRESERVED_READY",
        "MONITORING_HUD_STANDALONE_DASHBOARD_WINDOW_READY",
        "MONITORING_HUD_SURFACE_NATIVE_INDEPENDENCE_READY",
        "MONITORING_HUD_SURFACE_VIRTUAL_DESKTOP_TRAVEL_READY",
        "CORE_VISUALIZATION_HUD_SURFACE_SEPARATION_READY",
        "surfaceSeparationOk",
        "MONITORING_HUD_MINIMAL_NATIVE_OVERLAY_READY",
        "MONITORING_HUD_MINIMAL_ANCHORED_CLICK_THROUGH_READY",
        "MONITORING_HUD_MINIMAL_NON_FOCUS_READY",
        "WindowFromPoint",
        "native_overlay_center_click_through",
        "standalone overlay display proves anchored uninteractable/no-focus",
        "emit_status: bool = True",
        "emit_status=False",
        "MONITORING_HUD_VISIBLE_OVERLAY_READY",
        'pointer_model="click_through_no_focus"',
        "MONITORING_HUD_INTERACTION_MODE_READY",
        "MONITORING_HUD_CONTROL_STATE_READY",
        "MONITORING_HUD_MONITOR_MANAGEMENT_READY",
        "MONITORING_HUD_WINDOW_STATUS_READY",
        "MONITORING_HUD_TRAY_UNANCHOR_READY",
        "MONITORING_HUD_TRAY_TOGGLE_READY",
        "configure_monitoring_hud_live_client_self_qa",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_CONFIGURED",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_STEP",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_INTERACTION_READY",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_READY",
        "MONITORING_HUD_NATIVE_PANEL_DRAG_READY",
        "MONITORING_HUD_NATIVE_WINDOW_MOVE_READY",
        "MONITORING_HUD_NATIVE_CARD_DRAG_READY",
        "MONITORING_HUD_NATIVE_CARD_RESIZE_READY",
        "initial visible HUD identity/provider/no-fake-state",
        "dashboard and minimal HUD surfaces are split",
        "HUD standalone window preserves Core isolation contract",
        "real mouse hit targets are visible and large enough",
        "real mouse click on HUD Unanchor control sent",
        "real mouse unanchor reaches editable HUD",
        "active live-client pointer drag moves HUD panel without disappearing",
        "dashboard and overlay move independently across virtual desktop without clipping",
        "independent_user_selected_monitor_scoped",
        "attachedToHudDashboardOrNcp",
        "active live-client hide control and tray toggle route sent",
        "visible toggle hides HUD in live client",
        "active live-client drag overlay monitor card sent",
        "active live-client resize overlay monitor card sent",
        "draggable/resizable card layout and snap posture",
        "real mouse click on HUD Anchor control sent",
        "anchored click-through/no-focus posture",
        "DESKTOP_VISIBLE_OVERLAY_RESULT|success=true",
        "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
        "MONITORING_HUD_PLACEMENT_OWNERSHIP_READY",
        "MONITORING_HUD_CONTROLS_VISIBILITY_READY",
        "MONITORING_HUD_STATUS_BEHAVIOR_READY",
        'package="PKG-006"',
        'slice="SLC-016"',
        'slice="SLC-025"',
        'slice="SLC-026"',
        'slice="SLC-027"',
        'slice="SLC-028"',
        'adapter="desktop-runtime-boundary"',
        'hardware_polling="native_cpu_load_bounded"',
        'owner="DesktopRuntimeWindow"',
        'placement="standalone-native-hud-window"',
        'controls="hud-controls-visibility"',
        'persistence="local_layout_state"',
        'status="hud-local-readiness-status"',
        'source_truth="renderer_local"',
    ):
        _require_contains(renderer, needle, "desktop renderer HUD hook", failures)

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
        "CORE_VISUALIZATION_WINDOW_VISIBLE|surface=separate_persona_core",
        "CORE_VISUALIZATION_INDEPENDENT_PRESET_MONITOR_READY",
        "surface=separate_persona_core",
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

    desktop_mode_method = re.search(
        r"def _apply_desktop_surface_mode\(self\):.*?def _monitoring_hud_telemetry_snapshot",
        renderer,
        flags=re.DOTALL,
    )
    method_text = desktop_mode_method.group(0).casefold() if desktop_mode_method else ""
    for forbidden in ("psutil", "subprocess", "wmi", "pynvml", "settings"):
        _require(
            forbidden not in method_text,
            f"desktop renderer HUD product hook must not implement {forbidden} behavior",
            failures,
        )

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-025"',
        'ADAPTER_ID = "desktop-runtime-boundary"',
        "provider route is admitted",
        'DEFAULT_POLLING_RATE_MS = 1000',
        "NativeCpuLoadProbe",
        "GetSystemTimes",
        '"Waiting for safe provider"',
        '"Provider-first; no fake values"',
        '"1s after provider proof; CPU load warming"',
        '"sensorCards": [card.as_dict() for card in self.sensor_cards]',
        'MonitoringHudSensor(',
        'sensor_id="cpu-load"',
        'sensor_id="gpu-load"',
        'value="Unavailable"',
    ):
        _require_contains(telemetry, needle, "monitoring HUD telemetry adapter", failures)
    _require_no_collection_imports(telemetry, "monitoring HUD telemetry adapter", failures)

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-026"',
        'PLACEMENT_ID = "standalone-native-hud-window"',
        'renderer_owner="Separate minimal HUD overlay"',
        'surface_owner="Standalone Qt WebEngine HUD overlay window"',
        'anchor="Anchor anywhere after OS proof"',
        'pointer_model="Anchored click-through/no-focus-steal"',
        'snap_model="20px snap grid with snap-disable posture"',
        'card_layout_model="cards resize and snap in overlay edit mode"',
        'z_index="native-topmost"',
    ):
        _require_contains(placement, needle, "monitoring HUD placement contract", failures)
    _require_no_collection_imports(placement, "monitoring HUD placement contract", failures)

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-027"',
        'CONTROLS_ID = "hud-controls-visibility"',
        'visible: bool = True',
        'anchored: bool = True',
        'snap_enabled: bool = True',
        'polling_rate_ms: int = 1000',
        'control_surface="Unanchor to edit; anchor to observe"',
        'persistence="Snap cards; save local layout"',
        'operator_action="No default keybinds"',
        'anchor_state="anchored-click-through" if anchored else "unanchored-edit-mode"',
        'tray_path="Task tray can unanchor or restore the HUD"',
        'snap_state="enabled" if snap_enabled else "disabled"',
        'monitor_management="Dashboard creates, edits, enables, disables, and sets polling for monitors"',
        'overlay_mode_controls="Dashboard controls HUD display enablement plus anchor/unanchor mode"',
    ):
        _require_contains(controls, needle, "monitoring HUD controls visibility contract", failures)
    _require_no_collection_imports(controls, "monitoring HUD controls visibility contract", failures)

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-028"',
        'STATUS_ID = "hud-local-readiness-status"',
        'status_kind = "no-data"',
        'status_kind = "degraded"',
        'status_kind = "ready"',
        'status_label = "Provider setup required"',
        'status_label = "Reconnect/setup route unavailable"',
        'no_data_behavior="Show unavailable; no fake values"',
        'degraded_behavior="Name reconnect/setup gap with visual warning only"',
        'warning_posture="Visual badge, color state, and text label only"',
        'source_truth="Provider-contract-first local readiness only"',
    ):
        _require_contains(status, needle, "monitoring HUD status behavior contract", failures)
    _require_no_collection_imports(status, "monitoring HUD status behavior contract", failures)

    for needle in (
        "SLC-029",
        "Live Validation LV1 - Monitoring HUD Product Surface Live Validation",
        "proofStandard",
        "WS30 active-client before-after desktop proof plus fixed Core/HUD surface separation",
        "primaryInterfaceReleaseSurface",
        "monitoring-hud-dashboard-control-panel",
        "dashboardFirstWorkstreamHandoff",
        "ws31-dashboard-control-panel-acceptance-baseline",
        "dashboardOnlyAcceptanceBaseline",
        "currentInterfaceReleaseGate",
        "dashboard-only-current-branch",
        "overlayAcceptanceGate",
        "deferred-non-gating-supporting-evidence",
        "interfaceBundleUserApproval",
        "overlayDisplayAcceptance",
        "deferred-non-gating",
        "coreRepairClassification",
        "dependency-repair-only",
        "dashboardFirstProofPath",
        "revisedOverlayProof",
        "fullVirtualDesktopScreenshot",
        "userInspectableScreenshot",
        "standaloneDashboardWindowReady",
        "surfaceNativeIndependenceReady",
        "overlayCardsMovableReady",
        "surfaceVirtualDesktopTravelReady",
        "coreIndependentPresetMonitorReady",
        "coreHudSurfaceSeparationReady",
        "coreWorkerwCoordinateRebaseReady",
        "standaloneOverlayDisplayWindowReady",
        "anchoredOverlayUninteractableReady",
        "overlayPositionPreservedReady",
        "providerContractReady",
        "noFakeTelemetryPosture",
        "RunInteractionSelfQA",
        "VisibleClient",
        "ActiveUserFacingClient",
        "InteractionStepDelayMilliseconds",
        "FinalClientHoldSeconds",
        "InteractionManifest",
        "InteractionEvidenceRoot",
        "activeUserFacingClient",
        "interactionSelfQARequested",
        "interactionStepDelayMs",
        "finalClientHoldMs",
        "interactionManifestStatus",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_INTERACTION_READY",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_READY",
        "CORE_VISUALIZATION_PRESET_MONITOR_SELECTION_READY",
        "CORE_VISUALIZATION_WINDOW_READY|surface=separate_persona_core",
        "CORE_VISUALIZATION_DESKTOP_LAYER_READY|surface=separate_persona_core",
        "CORE_VISUALIZATION_WINDOW_GEOMETRY_READY",
        "CORE_VISUALIZATION_WORKERW_COORDINATE_REBASE_READY",
        "CORE_VISUALIZATION_FIXED_PRESET_MONITOR_READY",
        "CORE_VISUALIZATION_WINDOW_VISIBLE|surface=separate_persona_core",
        "CORE_VISUALIZATION_INDEPENDENT_PRESET_MONITOR_READY",
        "CORE_VISUALIZATION_HUD_SURFACE_SEPARATION_READY",
        "MONITORING_HUD_WINDOW_STATUS_READY",
        "interaction self-QA manifest PASS",
        "MONITORING_HUD_BASELINE_READY",
        "MONITORING_HUD_PRODUCT_VISIBILITY_READY",
        "MONITORING_HUD_DASHBOARD_SURFACE_READY",
        "MONITORING_HUD_MINIMAL_OVERLAY_READY",
        "MONITORING_HUD_DASHBOARD_MINIMAL_SPLIT_READY",
        "MONITORING_HUD_DASHBOARD_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MOTION_POLISH_READY",
        "MONITORING_HUD_DASHBOARD_SCROLLBAR_STYLE_READY",
        "MONITORING_HUD_EDGELESS_OVERLAY_CANVAS_READY",
        "MONITORING_HUD_STANDALONE_OVERLAY_DISPLAY_WINDOW_READY",
        "MONITORING_HUD_ANCHORED_OVERLAY_UNINTERACTABLE_READY",
        "MONITORING_HUD_OVERLAY_POSITION_PRESERVED_READY",
        "MONITORING_HUD_VISIBLE_OVERLAY_READY",
        "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
        "MONITORING_HUD_PLACEMENT_OWNERSHIP_READY",
        "MONITORING_HUD_CONTROLS_VISIBILITY_READY",
        "MONITORING_HUD_STATUS_BEHAVIOR_READY",
        "MONITORING_HUD_INTERACTION_MODE_READY",
        "MONITORING_HUD_CONTROL_STATE_READY",
        "DESKTOP_VISIBLE_OVERLAY_RESULT|success=true",
        "DESKTOP_OUTCOME|SETTLED|state=dormant",
        "settling visible overlay before full-desktop screenshot",
        "beforeLaunchScreenshot",
        "afterLaunchScreenshot",
        "monitoring_hud_desktop_before_launch.png",
        "monitoring_hud_desktop_after_launch.png",
        "beforeAfterDesktopComparisonReady",
        "manifest.json",
        "Stop-Process -Id $script:RuntimeProcess.Id -Force",
        "No-progress watchdog exceeded",
    ):
        _require_contains(live_validation, needle, "monitoring HUD live validation helper", failures)

    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("FAIL: FAM-006 Monitoring/HUD product visibility validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: FAM-006 HUD Dashboard-first source truth is bounded, provider-truthful, and marker-backed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
