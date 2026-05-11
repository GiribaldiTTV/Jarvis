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
    hud_state = _read("desktop/monitoring_hud_state.py")
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
        "Multiple Interface Release Drift",
    ):
        _require_contains(phase_governance, needle, "interface release boundary governance", failures)
    for needle in (
        "Stage 2-R13 Dashboard-first Workstream handoff source-truth markers",
        "Dashboard-first Interface Release Boundary source-truth markers",
        "WS35 dashboard-specific proof refresh and Live Validation UTS boundary",
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
        'data-interaction-mode="standalone-dashboard-window"',
        'data-anchor-state="overlay-anchored"',
        'data-feature-enabled="false"',
        'data-overlay-deferred="true"',
        'data-visibility-state="hidden"',
        'data-snap-state="enabled"',
        'data-card-model="category-sensor-cards"',
        'data-provider-state="setup-required"',
        'data-warning-mode="visual-non-invasive"',
        'data-live-values="provider-required"',
        'data-polling-default-ms="1000"',
        'data-polling-options-ms="1000,2000,5000,10000"',
        'data-keybind-policy="none"',
        'data-drag-smoothing="native-os-window-move"',
        'data-scrollbar-style="nexus-thin-glow"',
        'data-frame-ownership="single-rounded-dashboard-chrome"',
        'data-scroll-owner="monitoring-hud-chrome"',
        'data-scrollbar-boundary="rounded-window-clipped"',
        'data-outer-frame-haze="removed-no-square-layer"',
        'data-grid-scope="control-hub-cards-only"',
        'data-deadzone-policy="auto-height-content-no-empty-hit-zones"',
        'data-sticky-header-mask="opaque-scroll-mask"',
        'data-native-resize-hit-zone="cursor-aligned-12px-all-edges-and-corners"',
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
        'aria-label="Nexus Desktop AI Monitoring HUD product surface"',
        'aria-label="HUD Dashboard control hub cards"',
        'aria-hidden="true"',
        "Nexus Desktop AI",
        "Monitoring HUD",
        "HUD Dashboard",
        'data-native-resize-model="os-edge-corner-resize"',
        "Configure HUD access, monitor groups, data sources, warning notifications, and future display behavior.",
        "Dashboard",
        "Settings and control hub",
        "HUD Overlay",
        "Deferred future overlay",
        "Dashboard configures overlay behavior",
        "HUD Dashboard ready",
        "HUD Overlay deferred",
        "Quick Access",
        "Tray owns HUD feature enablement; Dashboard stays focused on settings.",
        'id="monitoring-hud-warning-toggle"',
        'id="monitoring-hud-create-monitor-action"',
        'id="monitoring-hud-edit-monitor-action"',
        "Warning Notifications",
        "Monitor Groups",
        "Data Sources",
        'id="monitoring-hud-monitor-list"',
        'id="monitoring-hud-monitor-selector"',
        'data-dashboard-monitor-display-policy="settings-only-no-monitor-cards"',
        'data-dashboard-content="control-hub-cards"',
        'data-child-window-model="hub-actions-standalone-child-windows-next"',
        'data-dashboard-monitor-model="organizational-groups-settings-only"',
        'data-dashboard-hub-card="hud-overlay"',
        'data-dashboard-hub-card="monitor-groups"',
        'data-dashboard-hub-card="data-sources"',
        'data-dashboard-hub-card="readiness"',
        'data-monitor-config-option="cpu"',
        'data-monitor-config-option="gpu"',
        "2 Monitor Groups configured. Polling defaults to 1s inside Create/Edit, not on the Dashboard home.",
        "CPU Group",
        "GPU Group",
        "Monitor Groups organize what the future HUD Overlay shows; the Dashboard does not render display cards or fake values.",
        "Waiting for safe provider",
        "Provider-first; no fake values",
        "HUD Overlay release acceptance is deferred.",
        "Deferred / non-gating",
        "Overlay settings are future branch scope",
        "Data Sources Window Deferred",
        "Provider setup required",
        "Show unavailable; no fake values",
        "Name reconnect/setup gap",
    ):
        _require_contains(hud_section, needle, "monitoring HUD HTML", failures)

    for forbidden_home_copy in (
        "Default polling",
        "Warning posture",
        "Monitor group to edit",
        "Monitor group editor",
        "Dashboard proof",
        "Full desktop now; UTS only in Live Validation Stage 1",
        'data-dashboard-content="dashboard-proof-next-actions"',
        'data-dashboard-content="monitor-group-management"',
    ):
        _require(
            forbidden_home_copy not in hud_section,
            f"monitoring HUD home surface must not include stale proof/inline-editor copy: {forbidden_home_copy}",
            failures,
        )

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
        "inset: 0;",
        "width: 100vw;",
        "overflow: hidden;",
        "clip-path: inset(0 round 28px);",
        "scrollbar-width: thin;",
        "scrollbar-color: rgba(108, 232, 255, 0.58) transparent;",
        "width: 6px;",
        "margin: 52px 0;",
        "border: 1px solid rgba(4, 17, 32, 0.72);",
        "background-clip: padding-box;",
        "contain: paint;",
        "body.desktop-mode .monitoring-hud__chrome::-webkit-scrollbar",
        "body.desktop-mode .monitoring-hud__chrome::-webkit-scrollbar-thumb",
        "body.desktop-mode .monitoring-hud__chrome::-webkit-scrollbar-corner",
        'body.desktop-mode #monitoring-hud[data-drag-smoothing="native-os-window-move"]',
        'font-family: "Bahnschrift", "Rajdhani", "Segoe UI", sans-serif;',
        "pointer-events: auto",
        'body.desktop-mode #monitoring-hud[data-anchor-state="unanchored"]',
        ".monitoring-hud__chrome",
        ".monitoring-hud__toolbar",
        ".monitoring-hud__surface-role",
        ".monitoring-hud__config-heading",
        ".monitoring-hud__anchor-rail",
        ".monitoring-hud__control-hub",
        ".monitoring-hud__hub-card",
        ".monitoring-hud__hub-card-topline",
        ".monitoring-hud__hub-action",
        ".monitoring-hud__state-row",
        ".monitoring-hud__selector-control",
        "#monitoring-hud-monitor-list-summary",
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
        ".monitoring-hud__title-group",
        "position: sticky;",
        "scrollbar-gutter: stable;",
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
        'const monitoringHudCreateMonitor = document.getElementById("monitoring-hud-create-monitor-action")',
        'const monitoringHudEditMonitor = document.getElementById("monitoring-hud-edit-monitor-action")',
        'const monitoringHudWarningToggle = document.getElementById("monitoring-hud-warning-toggle")',
        'const monitoringHudMonitorList = document.getElementById("monitoring-hud-monitor-list")',
        'const monitoringHudMonitorSelector = document.getElementById("monitoring-hud-monitor-selector")',
        "warningNotificationsMuted",
        "window.getMonitoringHudControlState = function()",
        "window.getMonitoringHudLiveClientGeometry = function()",
        "minimalHud: rectFor(\"#monitoring-hud-minimal\")",
        "window.getMonitoringHudSurfaceSplitState = function()",
        "window.getMonitoringHudDashboardAcceptanceState = function()",
        "window.getMonitoringHudIsolationState = function()",
        "primaryInterfaceReleaseSurface",
        "dashboardAcceptanceBaseline",
        "dashboardProofPath",
        "dashboardStandaloneProof",
        "dashboardClippingProof",
        "dashboardDecouplingProof",
        "dashboardContentPolish",
        "dashboardSettingsModel",
        "monitorGroupModel",
        "dashboardMonitorCardPolicy",
        "dashboardStandaloneMovementReady",
        "dashboardSettingsContentReady",
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
        'monitoringHud.dataset.dragSmoothing = "native-os-window-move"',
        'monitoringHud.dataset.nativeResizeModel = "os-edge-corner-resize"',
        'document.body.classList.contains("desktop-mode")',
        'monitoringHud.dataset.scrollbarStyle = "nexus-thin-glow"',
        'monitoringHud.dataset.frameOwnership = "single-rounded-dashboard-chrome"',
        'monitoringHud.dataset.scrollOwner = "monitoring-hud-chrome"',
        'monitoringHud.dataset.scrollbarBoundary = "rounded-window-clipped"',
        'monitoringHud.dataset.outerFrameHaze = "removed-no-square-layer"',
        'monitoringHud.dataset.gridScope = "control-hub-cards-only"',
        'monitoringHud.dataset.deadzonePolicy = "auto-height-content-no-empty-hit-zones"',
        'monitoringHud.dataset.stickyHeaderMask = "opaque-scroll-mask"',
        'monitoringHud.dataset.nativeResizeHitZone = "all-edges-and-corners"',
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
        'monitoringHud.dataset.productSurfaceState = (isEnabled && monitoringHudControlState.visible) ? "visible-user-facing" : "hidden"',
        'monitoringHudMinimal.dataset.productSurfaceState = "hidden-deferred"',
        "window.setMonitoringHudTelemetry = function(snapshot)",
        'monitoringHud.dataset.providerState = monitoringHudTelemetry.providerState || "setup-required"',
        'monitoringHud.dataset.liveValues = monitoringHudTelemetry.liveValues || "provider-required"',
        'monitoringHudProviderState.textContent = monitoringHudTelemetry.providerLabel || "Provider setup required"',
        "window.setMonitoringHudPlacementOwnership = function(contract)",
        'monitoringHud.dataset.interactionMode = "standalone-dashboard-window"',
        'monitoringHudPlacementAnchor.textContent = monitoringHudPlacement.anchor || "Deferred / non-gating"',
        'monitoringHudResizePosture.textContent = monitoringHudPlacement.resizePosture || "Overlay settings are future branch scope"',
        "window.setMonitoringHudControlsVisibility = function(contract)",
        '"feature-enabled-dashboard-open"',
        '"feature-enabled-dashboard-closed"',
        '"feature-disabled-dashboard-closed"',
        'monitoringHud.dataset.keybindPolicy = "none"',
        'monitoringHud.dataset.monitorManagement = "create-edit-enable-polling"',
        'monitoringHud.dataset.overlayModeControls = "overlay-deferred-tray-owned"',
        'monitoringHudControlsVisibility.textContent = monitoringHudControls.visibilityState || "HUD feature disabled from dashboard/tray"',
        'monitoringHudControlsSurface.textContent = monitoringHudControls.controlSurface || "Tray controls HUD feature state; Dashboard open/close is separate; HUD Overlay remains deferred"',
        'monitoringHudControlsPersistence.textContent = monitoringHudControls.persistence || "Store group/layout posture locally"',
        'monitoringHudTrayPath.textContent = monitoringHudControls.trayPath || "Task tray enables/disables HUD feature and opens/closes Dashboard; HUD Overlay controls deferred"',
        "window.setMonitoringHudStatusBehavior = function(snapshot)",
        'monitoringHud.dataset.warningMode = "visual-non-invasive"',
        'monitoringHudWarningPosture.textContent = monitoringHudStatus.warningPosture || "Visual notifications enabled"',
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
        "MONITORING_HUD_DASHBOARD_SETTINGS_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MONITOR_GROUP_CLARITY_READY",
        "MONITORING_HUD_DASHBOARD_OVERLAY_NON_GATING_COPY_READY",
        "MONITORING_HUD_DASHBOARD_PROVIDER_TRUTH_READY",
        "MONITORING_HUD_DASHBOARD_STATE_MODEL_READY",
        "MONITORING_HUD_DASHBOARD_WARNING_CONTROLS_READY",
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
        "MONITORING_HUD_TRAY_ENABLE_RENDER_STABLE_READY",
        "MONITORING_HUD_TRAY_ENABLE_DISABLE_ROUNDTRIP_READY",
        "MONITORING_HUD_TRAY_DASHBOARD_OPEN_CLOSE_READY",
        "MONITORING_HUD_DISABLE_RECOVERY_READY",
        "MONITORING_HUD_REAL_CLIENT_DASHBOARD_VISIBILITY_REQUESTED",
        "_ensure_monitoring_hud_desktop_mode_for_visible_dashboard",
        "MONITORING_HUD_MONITOR_MANAGEMENT_READY",
        "MONITORING_HUD_WINDOW_STATUS_READY",
        "MONITORING_HUD_WINDOW_OWNERSHIP_FOCUS_READY",
        "MONITORING_HUD_NATIVE_SYSTEM_MOVE_STARTED",
        "MONITORING_HUD_TRAY_UNANCHOR_DEFERRED",
        "MONITORING_HUD_TRAY_TOGGLE_READY",
        "request_monitoring_hud_dashboard_from_tray",
        "configure_monitoring_hud_live_client_self_qa",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_CONFIGURED",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_STEP",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_INTERACTION_READY",
        "MONITORING_HUD_LIVE_CLIENT_SELF_QA_READY",
        "MONITORING_HUD_NATIVE_PANEL_DRAG_READY",
        "MONITORING_HUD_NATIVE_WINDOW_MOVE_READY",
        "MONITORING_HUD_NATIVE_WINDOW_RESIZE_READY",
        "MONITORING_HUD_NATIVE_SYSTEM_RESIZE_STARTED",
        "MONITORING_HUD_NATIVE_WINDOW_RESIZE_FALLBACK_STARTED",
        "_monitoring_hud_window_resize_interaction_available",
        "_monitoring_hud_resize_hit_zone_px",
        "findChildren(QWidget)",
        "_finish_monitoring_hud_fallback_window_resize",
        "Returning a real non-client edge lets Windows own the visible",
        "_monitoring_hud_windows_resize_cursor_id_for_edges",
        "cursor-aligned-12px-all-edges-and-corners",
        "setMouseTracking(True)",
        "MONITORING_HUD_DASHBOARD_SHELL_LAYOUT_READY",
        "MONITORING_HUD_DASHBOARD_VISUAL_SHELL_READY",
        "WM_NCHITTEST",
        "HTBOTTOMRIGHT",
        "ctypes.wintypes.MSG.from_address",
        "return 12",
        "save_monitoring_hud_state",
        "_persist_monitoring_hud_feature_state",
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
        "initial visible HUD identity/provider/no-fake-state",
        "dashboard and minimal HUD surfaces are split",
        "HUD standalone window preserves Core isolation contract",
        "real mouse hit targets are visible and large enough",
        "dashboard standalone window moves across virtual desktop without clipping while Core and Overlay remain decoupled",
        "independent_user_selected_monitor_scoped",
        "attachedToHudDashboardOrNcp",
        "active live-client tray Dashboard close route sent",
        "tray Dashboard close hides only the Dashboard",
        "dashboard monitor management create/edit/enable/polling state",
        "dashboard monitor editor control mutation sent",
        "cleanup route available",
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
        "app.setQuitOnLastWindowClosed(False)",
        "SHUTDOWN_CONFIRMATION_DIALOG_VISIBLE",
        "REAL_CLIENT_TRAY_PRECHECK_MANIFEST_ENV",
        "REAL_CLIENT_TRAY_PRECHECK_STARTED",
        "from desktop.monitoring_hud_state import load_monitoring_hud_state",
        "MONITORING_HUD_STARTUP_STATE_READY",
        "monitoring_hud_feature_enabled_at_startup",
        "monitoring_hud_dashboard_visible_at_startup",
    ):
        _require_contains(tray, needle, "desktop launcher Core/HUD failure isolation", failures)

    for needle in (
        'MONITORING_HUD_STATE_ENV = "NEXUS_MONITORING_HUD_STATE_PATH"',
        "monitoring_hud_state_path",
        "load_monitoring_hud_state",
        "save_monitoring_hud_state",
        "MONITORING_HUD_STATE_LOAD_READY",
        "MONITORING_HUD_STATE_SAVE_READY",
        '"featureEnabled"',
        '"dashboardVisible"',
        "os.replace",
    ):
        _require_contains(hud_state, needle, "Monitoring HUD persisted state helper", failures)

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
    for forbidden in ("psutil", "subprocess", "wmi", "pynvml"):
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
        'renderer_owner="Dashboard-first runtime window"',
        'surface_owner="Standalone Qt WebEngine Dashboard window"',
        'anchor="Overlay anchor deferred until future interface release"',
        'pointer_model="Normal dashboard window; OS-native move; no topmost/no focus steal"',
        'snap_model="Dashboard window movement is unsnapped; Overlay layout snap remains deferred"',
        'card_layout_model="cards resize and snap in overlay edit mode"',
        'z_index="normal-window-no-topmost"',
    ):
        _require_contains(placement, needle, "monitoring HUD placement contract", failures)
    _require_no_collection_imports(placement, "monitoring HUD placement contract", failures)

    for needle in (
        'PACKAGE_ID = "PKG-006"',
        'SLICE_ID = "SLC-027"',
        'CONTROLS_ID = "hud-controls-visibility"',
        "feature_enabled: bool | None = None",
        'visible: bool = True',
        'anchored: bool = True',
        'snap_enabled: bool = True',
        'polling_rate_ms: int = 1000',
        'control_surface="Tray controls HUD feature state; Dashboard open/close is separate; Overlay controls remain deferred"',
        'persistence="Store group/layout posture locally"',
        'operator_action="No default keybinds"',
        'anchor_state="overlay-deferred"',
        'tray_path="Task tray enables/disables HUD feature and opens/closes Dashboard; Overlay anchor controls deferred"',
        'snap_state="enabled" if snap_enabled else "disabled"',
        'monitor_management="Dashboard creates, edits, enables, disables, and sets polling for monitor groups"',
        'overlay_mode_controls="Overlay display and anchor/unanchor controls are deferred/non-gating"',
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
        "Dashboard-specific active-client proof - no UTS export",
        "ProofSeam",
        "proofStandard",
        "Dashboard-specific static/live proof screenshots; ledger-aligned User Test Summary export is Live Validation Stage 1 only",
        "elementValidationLedger",
        "feature_fam_006_monitoring_hud_product_surface_element_ledger.md",
        "elementLedgerAlignedUserTestSummary",
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
        "dashboardSpecificProofRefreshReady",
        "dashboardSpecificStaticLiveProofReady",
        "dashboardUserTestSummaryExportRefreshed",
        "dashboardUserTestSummaryExportPath",
        "dashboardUserTestSummaryReturnedResults",
        "live-validation-stage-1-only",
        "dashboardSpecificProof",
        "dashboardOnlyCurrentInterfaceGate",
        "overlayAcceptanceDeferredNonGating",
        "coreRepairDependencyOnly",
        "userTestSummaryExportRefreshed",
        "userTestSummaryPhaseBoundary",
        "returnedUserTestSummaryDigestReserved",
        "revisedOverlayProof",
        "fullVirtualDesktopScreenshot",
        "userInspectableScreenshot",
        "standaloneDashboardWindowReady",
        "surfaceNativeIndependenceReady",
        "dashboardStandaloneWindowTravelReady",
        "dashboardClippingBoundaryReady",
        "dashboardCoreOverlayDecouplingReady",
        "dashboardSettingsContentReady",
        "dashboardMonitorGroupClarityReady",
        "dashboardOverlayNonGatingCopyReady",
        "dashboardProviderTruthReady",
        "dashboardStateModelReady",
        "dashboardWarningControlsReady",
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
        "MONITORING_HUD_DASHBOARD_STANDALONE_WINDOW_TRAVEL_READY",
        "MONITORING_HUD_DASHBOARD_CLIPPING_BOUNDARY_READY",
        "MONITORING_HUD_DASHBOARD_CORE_OVERLAY_DECOUPLING_READY",
        "MONITORING_HUD_DASHBOARD_SETTINGS_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MONITOR_GROUP_CLARITY_READY",
        "MONITORING_HUD_DASHBOARD_OVERLAY_NON_GATING_COPY_READY",
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
        "MONITORING_HUD_DASHBOARD_SETTINGS_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MONITOR_GROUP_CLARITY_READY",
        "MONITORING_HUD_DASHBOARD_OVERLAY_NON_GATING_COPY_READY",
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
        "MONITORING_HUD_TRAY_ENABLE_RENDER_STABLE_READY",
        "MONITORING_HUD_TRAY_ENABLE_DISABLE_ROUNDTRIP_READY",
        "MONITORING_HUD_TRAY_DASHBOARD_OPEN_CLOSE_READY",
        "MONITORING_HUD_DISABLE_RECOVERY_READY",
        "DESKTOP_VISIBLE_OVERLAY_RESULT|success=true",
        "DESKTOP_OUTCOME|SETTLED|state=dormant",
        "settling Dashboard-first client before full-desktop screenshot",
        "beforeLaunchScreenshot",
        "afterLaunchScreenshot",
        "monitoring_hud_desktop_before_launch.png",
        "monitoring_hud_desktop_after_launch.png",
        "beforeAfterDesktopComparisonReady",
        "PrepareLiveValidationUserTestSummary",
        "skipped User Test Summary export: UTS is Live Validation Stage 1 only",
        "Overlay/display release acceptance is deferred and non-gating",
        "Current Phase: Live Validation Stage 1 User Test Summary handoff",
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
