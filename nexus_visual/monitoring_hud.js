const body = document.body;
const monitoringHud = document.getElementById("monitoring-hud");
const monitoringHudMinimal = document.getElementById("monitoring-hud-minimal");
const monitoringHudOverlayDisplay = document.getElementById("monitoring-hud-overlay-display");
const monitoringHudOverlayCanvas = document.getElementById("monitoring-hud-overlay-canvas");
const monitoringHudMinimalRuntimeStatus = document.getElementById("monitoring-hud-minimal-runtime-status");
const monitoringHudMinimalProviderState = document.getElementById("monitoring-hud-minimal-provider-state");
const monitoringHudMinimalAnchor = document.getElementById("monitoring-hud-minimal-anchor");
const monitoringHudMinimalWarning = document.getElementById("monitoring-hud-minimal-warning");
const monitoringHudRuntimeStatus = document.getElementById("monitoring-hud-runtime-status");
const monitoringHudProviderState = document.getElementById("monitoring-hud-provider-state");
const monitoringHudAdapterStatus = document.getElementById("monitoring-hud-adapter-status");
const monitoringHudSourceScope = document.getElementById("monitoring-hud-source-scope");
const monitoringHudHardwarePolling = document.getElementById("monitoring-hud-hardware-polling");
const monitoringHudProviderStateMatrix = document.getElementById("monitoring-hud-provider-state-matrix");
const monitoringHudPlacementOwner = document.getElementById("monitoring-hud-placement-owner");
const monitoringHudPlacementAnchor = document.getElementById("monitoring-hud-placement-anchor");
const monitoringHudPlacementPointer = document.getElementById("monitoring-hud-placement-pointer");
const monitoringHudResizePosture = document.getElementById("monitoring-hud-resize-posture");
const monitoringHudControlsVisibility = document.getElementById("monitoring-hud-controls-visibility");
const monitoringHudControlsSurface = document.getElementById("monitoring-hud-controls-surface");
const monitoringHudControlsPersistence = document.getElementById("monitoring-hud-controls-persistence");
const monitoringHudStatusLabel = document.getElementById("monitoring-hud-status-label");
const monitoringHudNoDataBehavior = document.getElementById("monitoring-hud-no-data-behavior");
const monitoringHudDegradedBehavior = document.getElementById("monitoring-hud-degraded-behavior");
const monitoringHudWarningPosture = document.getElementById("monitoring-hud-warning-posture");
const monitoringHudTrayPath = document.getElementById("monitoring-hud-tray-path");
const monitoringHudAnchorStatus = document.getElementById("monitoring-hud-anchor-status");
const monitoringHudDragHandle = document.getElementById("monitoring-hud-drag-handle");
const monitoringHudToggle = document.getElementById("monitoring-hud-toggle");
const monitoringHudAnchorToggle = document.getElementById("monitoring-hud-anchor-toggle");
const monitoringHudCreateMonitor = document.getElementById("monitoring-hud-create-monitor");
const monitoringHudEditMonitor = document.getElementById("monitoring-hud-edit-monitor");
const monitoringHudSnapToggle = document.getElementById("monitoring-hud-snap-toggle");
const monitoringHudWarningToggle = document.getElementById("monitoring-hud-warning-toggle");
const monitoringHudSnapLabel = document.getElementById("monitoring-hud-snap-label");
const monitoringHudPollingRate = document.getElementById("monitoring-hud-polling-rate");
const monitoringHudWarningModeControl = document.getElementById("monitoring-hud-warning-mode-control");
const monitoringHudMonitorList = document.getElementById("monitoring-hud-monitor-list");
const monitoringHudMonitorSelector = document.getElementById("monitoring-hud-monitor-selector");
const monitoringHudMonitorListSummary = document.getElementById("monitoring-hud-monitor-list-summary");
const monitoringHudMonitorEditorTitle = document.getElementById("monitoring-hud-monitor-editor-title");
const monitoringHudMonitorEnabled = document.getElementById("monitoring-hud-monitor-enabled");
const monitoringHudMonitorPollingRate = document.getElementById("monitoring-hud-monitor-polling-rate");
const monitoringHudMonitorEditorScope = document.getElementById("monitoring-hud-monitor-editor-scope");

let monitoringHudTelemetry = {
  packageId: "PKG-006",
  sliceId: "SLC-025",
  adapterStatus: "Waiting for safe provider",
  sourceScope: "Provider-first; no fake values",
  hardwarePolling: "1s after provider proof",
  sources: []
};
let monitoringHudPlacement = {
  packageId: "PKG-006",
  sliceId: "SLC-026",
  placementId: "standalone-native-hud-window",
  rendererOwner: "Future HUD display is deferred. The Dashboard can store settings now without asking for Overlay acceptance.",
  anchor: "Deferred / non-gating",
  pointerModel: "Dashboard controls future HUD display",
  resizePosture: "Prepared for future HUD display branch"
};
let monitoringHudControls = {
  packageId: "PKG-006",
  sliceId: "SLC-027",
  controlsId: "hud-controls-visibility",
  visibilityState: "HUD feature disabled from dashboard/tray",
  controlSurface: "Tray controls HUD feature state; Dashboard open/close is separate; HUD display remains deferred",
  persistence: "Store group/layout posture locally",
  operatorAction: "No default keybinds",
  trayPath: "Task tray enables/disables HUD feature and opens/closes Dashboard; Overlay controls deferred"
};
let monitoringHudStatus = {
  packageId: "PKG-006",
  sliceId: "SLC-028",
  statusId: "hud-local-readiness-status",
  statusKind: "no-data",
  statusLabel: "Provider setup required",
  noDataBehavior: "Show unavailable; no fake values",
  degradedBehavior: "Name reconnect/setup gap; visual warning only"
};
let monitoringHudControlState = {
  featureEnabled: false,
  overlayDeferred: true,
  visible: false,
  anchored: true,
  snapEnabled: true,
  pollingRateMs: 1000,
  warningMode: "badge-text-color",
  warningNotificationsMuted: false,
  panelPosition: null,
  selectedMonitorId: "cpu",
  monitorSequence: 2,
  cards: {
    cpu: { x: 0, y: 0, w: 600, h: 280, title: "CPU Group", enabled: true, pollingRateMs: 1000 },
    gpu: { x: 0, y: 300, w: 600, h: 280, title: "GPU Group", enabled: true, pollingRateMs: 1000 }
  },
  changedAt: Date.now()
};
const monitoringHudStorageKey = "nexusMonitoringHudLayoutV3";
const monitoringHudLegacyStorageKeys = ["nexusMonitoringHudLayoutV1", "nexusMonitoringHudLayoutV2"];
const monitoringHudSnapSize = 20;
let monitoringHudDragInProgress = false;
let monitoringHudPanelPositionFrame = 0;
let monitoringHudQueuedPanelPosition = null;

function monitoringHudSnap(value) {
  if (!monitoringHudControlState.snapEnabled) return Math.round(value);
  return Math.round(value / monitoringHudSnapSize) * monitoringHudSnapSize;
}

function monitoringHudBound(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function monitoringHudLoadStoredState() {
  try {
    if (window.localStorage) {
      monitoringHudLegacyStorageKeys.forEach((key) => window.localStorage.removeItem(key));
    }
    const raw = window.localStorage ? window.localStorage.getItem(monitoringHudStorageKey) : "";
    if (!raw) return;
    const stored = JSON.parse(raw);
    monitoringHudControlState = Object.assign({}, monitoringHudControlState, stored || {});
    monitoringHudControlState.cards = Object.assign(
      {},
      monitoringHudControlState.cards,
      (stored && stored.cards) || {}
    );
  } catch (_err) {
    monitoringHudControlState.changedAt = Date.now();
  }
}

function monitoringHudSaveStoredState() {
  try {
    if (!window.localStorage) return;
    window.localStorage.setItem(monitoringHudStorageKey, JSON.stringify(monitoringHudControlState));
  } catch (_err) {}
}

function monitoringHudMarkChanged() {
  monitoringHudControlState.changedAt = Date.now();
  monitoringHudSaveStoredState();
}

function monitoringHudCardDefaults(cardId) {
  return {
    x: 0,
    y: Object.keys(monitoringHudControlState.cards || {}).length * 300,
    w: 600,
    h: 280,
    title: cardId === "cpu" ? "CPU Group" : cardId === "gpu" ? "GPU Group" : "Monitor Group",
    enabled: true,
    pollingRateMs: 1000
  };
}

function monitoringHudSelectedMonitor() {
  const cards = monitoringHudControlState.cards || {};
  const selectedId = monitoringHudControlState.selectedMonitorId;
  if (selectedId && cards[selectedId]) return { id: selectedId, layout: cards[selectedId] };
  const firstId = Object.keys(cards)[0] || "cpu";
  monitoringHudControlState.selectedMonitorId = firstId;
  return { id: firstId, layout: cards[firstId] || monitoringHudCardDefaults(firstId) };
}

function monitoringHudNormalizeMonitorGroupTitle(cardId, layout) {
  if (!layout) return;
  const oldCpuTitle = ["CPU", "Monitor"].join(" ");
  const oldGpuTitle = ["GPU", "Monitor"].join(" ");
  if (cardId === "cpu" && (!layout.title || layout.title === oldCpuTitle)) {
    layout.title = "CPU Group";
  } else if (cardId === "gpu" && (!layout.title || layout.title === oldGpuTitle)) {
    layout.title = "GPU Group";
  } else if (/^Monitor\s+\d+$/i.test(String(layout.title || ""))) {
    layout.title = String(layout.title).replace(/^Monitor/i, "Monitor Group");
  } else if (!layout.title) {
    layout.title = "Monitor Group";
  }
}

function monitoringHudCreateCardNode(cardId, layout) {
  if (!monitoringHudMonitorSelector || monitoringHudMonitorSelector.querySelector(`[data-monitor-config-option="${cardId}"]`)) return;
  const title = layout.title || "Monitor Group";
  const option = document.createElement("option");
  option.value = cardId;
  option.dataset.monitorConfigOption = cardId;
  option.textContent = title;
  monitoringHudMonitorSelector.appendChild(option);
}

function monitoringHudEnsureCardNodes() {
  if (!monitoringHudMonitorList) return;
  Object.keys(monitoringHudControlState.cards || {}).forEach((cardId) => {
    const layout = Object.assign(monitoringHudCardDefaults(cardId), monitoringHudControlState.cards[cardId] || {});
    monitoringHudNormalizeMonitorGroupTitle(cardId, layout);
    monitoringHudControlState.cards[cardId] = layout;
    monitoringHudCreateCardNode(cardId, layout);
  });
}

function monitoringHudRenderMonitorManagement() {
  const selected = monitoringHudSelectedMonitor();
  if (monitoringHud) {
    monitoringHud.dataset.dashboardControlPanel = "hud-display-monitor-management";
    monitoringHud.dataset.monitorManagement = "create-edit-enable-polling";
    monitoringHud.dataset.overlayModeControls = "enable-disable-anchor-unanchor";
    monitoringHud.dataset.primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel";
    monitoringHud.dataset.interfaceAcceptancePolicy = "dashboard-only-current-branch";
    monitoringHud.dataset.dashboardAcceptanceBaseline = "ws31-dashboard-control-panel";
    monitoringHud.dataset.dashboardProofPath = "dashboard-specific-static-live-uts";
    monitoringHud.dataset.dashboardStandaloneProof = "ws32-dashboard-window-travel";
    monitoringHud.dataset.dashboardClippingProof = "within-virtual-desktop";
    monitoringHud.dataset.dashboardDecouplingProof = "core-overlay-independent";
    monitoringHud.dataset.dashboardContentPolish = "ws40-control-hub-ia";
    monitoringHud.dataset.dashboardHomeModel = "control-hub-cards-no-inline-editor";
    monitoringHud.dataset.dashboardPollingPlacement = "monitor-group-editor-only";
    monitoringHud.dataset.dashboardProofContentPolicy = "validator-artifacts-not-home-surface";
    monitoringHud.dataset.dashboardChildWindowScope = "ws41-if-admitted";
    monitoringHud.dataset.dashboardSettingsModel = "hud-capability-monitor-groups-provider-warning";
    monitoringHud.dataset.monitorGroupModel = "organizational-groups-settings-only";
    monitoringHud.dataset.dashboardMonitorCardPolicy = "overlay-display-owns-monitor-cards";
    monitoringHud.dataset.overlayAcceptancePolicy = "deferred-non-gating";
    monitoringHud.dataset.interfaceBundleApproval = "not-granted";
    monitoringHud.dataset.coreRepairClassification = "dependency-repair-only";
    monitoringHud.dataset.monitorCount = String(Object.keys(monitoringHudControlState.cards || {}).length);
    monitoringHud.dataset.selectedMonitor = selected.id || "";
  }
  Object.keys(monitoringHudControlState.cards || {}).forEach((cardId) => {
    const layout = Object.assign(monitoringHudCardDefaults(cardId), monitoringHudControlState.cards[cardId] || {});
    monitoringHudNormalizeMonitorGroupTitle(cardId, layout);
    const cardNode = monitoringHudMonitorSelector
      ? monitoringHudMonitorSelector.querySelector(`[data-monitor-config-option="${cardId}"]`)
      : null;
    if (!cardNode) return;
    cardNode.dataset.monitorEnabled = layout.enabled === false ? "false" : "true";
    cardNode.dataset.monitorPollingMs = String(Math.max(1000, Number(layout.pollingRateMs) || 1000));
    cardNode.textContent = layout.title || "Monitor";
  });
  if (monitoringHudMonitorSelector) {
    monitoringHudMonitorSelector.value = selected.id || "cpu";
  }
  if (monitoringHudMonitorListSummary) {
    monitoringHudMonitorListSummary.textContent = `${Object.keys(monitoringHudControlState.cards || {}).length} Monitor Groups configured. Polling defaults to 1s inside Create/Edit, not on the Dashboard home.`;
  }
  if (monitoringHudMonitorEditorTitle) {
    monitoringHudMonitorEditorTitle.textContent = selected.layout.title || "Monitor Group";
  }
  if (monitoringHudMonitorEnabled) {
    monitoringHudMonitorEnabled.checked = selected.layout.enabled !== false;
  }
  if (monitoringHudMonitorPollingRate) {
    monitoringHudMonitorPollingRate.value = String(Math.max(1000, Number(selected.layout.pollingRateMs) || 1000));
  }
  if (monitoringHudMonitorEditorScope) {
    monitoringHudMonitorEditorScope.textContent = "Monitor Groups organize what the future HUD displays; the Dashboard does not render display cards or fake values.";
  }
}

function monitoringHudCreateOverlayCardNode(cardId, layout) {
  if (!monitoringHudOverlayCanvas || monitoringHudOverlayCanvas.querySelector(`[data-overlay-monitor-card="${cardId}"]`)) return;
  const article = document.createElement("article");
  article.className = "monitoring-hud-overlay-card monitoring-hud-overlay-card--unavailable";
  article.dataset.overlayMonitorCard = cardId;
  article.dataset.overlayMonitorEnabled = layout.enabled === false ? "false" : "true";
  article.dataset.overlayMonitorPollingMs = String(layout.pollingRateMs || 1000);
  article.style.setProperty("--overlay-card-x", `${Math.round(layout.x || 0)}px`);
  article.style.setProperty("--overlay-card-y", `${Math.round(layout.y || 0)}px`);
  article.style.setProperty("--overlay-card-w", `${Math.round(Math.max(220, Math.min(layout.w || 300, 420)))}px`);
  article.style.setProperty("--overlay-card-h", `${Math.round(Math.max(108, Math.min(layout.h || 132, 180)))}px`);
  article.innerHTML = `
    <div class="monitoring-hud-overlay-card__topline">
      <strong data-overlay-monitor-title="${cardId}"></strong>
      <span data-overlay-monitor-state="${cardId}">No data</span>
    </div>
    <p data-overlay-monitor-summary="${cardId}">Provider required</p>
    <div class="monitoring-hud-overlay-card__quick-actions" data-overlay-monitor-quick-actions="${cardId}">
      <button type="button" data-overlay-monitor-edit="${cardId}">Edit</button>
    </div>
  `;
  monitoringHudOverlayCanvas.appendChild(article);
}

function monitoringHudRenderOverlayDisplay() {
  if (!monitoringHudOverlayDisplay || !monitoringHudOverlayCanvas) return;
  const cards = monitoringHudControlState.cards || {};
  const overlayDeferred = monitoringHudControlState.overlayDeferred !== false;
  monitoringHudOverlayDisplay.dataset.anchorState = monitoringHudControlState.anchored ? "anchored" : "unanchored";
  monitoringHudOverlayDisplay.dataset.visibilityState = overlayDeferred ? "hidden-deferred" : (monitoringHudControlState.visible ? "visible" : "hidden");
  monitoringHudOverlayDisplay.dataset.overlayEditMode = "unanchored-focusable-resizable-scrollable";
  monitoringHudOverlayDisplay.dataset.overlayAnchorMode = "anchored-uninteractable-click-through";
  monitoringHudOverlayDisplay.dataset.overlayCanvas = "edge-to-edge-snipping-tool-style";
  monitoringHudOverlayDisplay.dataset.monitorLayout = "movable-resizable-monitor-cards";
  monitoringHudOverlayDisplay.dataset.edgeToEdgePosture = "landscape-portrait-monitor-fit";
  monitoringHudOverlayDisplay.dataset.interfaceAcceptancePolicy = "deferred-non-gating";
  monitoringHudOverlayDisplay.dataset.dashboardAcceptanceRole = "supporting-future-interface-evidence";
  monitoringHudOverlayDisplay.dataset.currentBranchReleaseGate = "false";
  monitoringHudOverlayDisplay.dataset.monitorCount = String(Object.keys(cards).length);
  Object.keys(cards).forEach((cardId) => {
    const layout = Object.assign(monitoringHudCardDefaults(cardId), cards[cardId] || {});
    const overlayLayout = Object.assign({}, layout, {
      x: monitoringHudSnap(layout.x || 0) + 28,
      y: monitoringHudSnap(layout.y || 0) + 34,
      w: Math.max(220, Math.min(layout.w || 300, 420)),
      h: Math.max(108, Math.min(layout.h || 132, 180))
    });
    monitoringHudCreateOverlayCardNode(cardId, overlayLayout);
    const cardNode = monitoringHudOverlayCanvas.querySelector(`[data-overlay-monitor-card="${cardId}"]`);
    if (!cardNode) return;
    cardNode.dataset.overlayMonitorEnabled = layout.enabled === false ? "false" : "true";
    cardNode.dataset.overlayMonitorPollingMs = String(Math.max(1000, Number(layout.pollingRateMs) || 1000));
    cardNode.style.setProperty("--overlay-card-x", `${Math.round(overlayLayout.x)}px`);
    cardNode.style.setProperty("--overlay-card-y", `${Math.round(overlayLayout.y)}px`);
    cardNode.style.setProperty("--overlay-card-w", `${Math.round(overlayLayout.w)}px`);
    cardNode.style.setProperty("--overlay-card-h", `${Math.round(overlayLayout.h)}px`);
    cardNode.classList.toggle("monitoring-hud-overlay-card--setup", cardId === "cpu");
    cardNode.classList.toggle("monitoring-hud-overlay-card--unavailable", cardId !== "cpu");
    const titleNode = cardNode.querySelector(`[data-overlay-monitor-title="${cardId}"]`);
    if (titleNode) titleNode.textContent = layout.title || "Monitor";
    const stateNode = cardNode.querySelector(`[data-overlay-monitor-state="${cardId}"]`);
    if (stateNode) stateNode.textContent = layout.enabled === false ? "Hidden" : (cardId === "cpu" ? "Setup" : "No data");
    const summaryNode = cardNode.querySelector(`[data-overlay-monitor-summary="${cardId}"]`);
    if (summaryNode) {
      summaryNode.textContent = layout.enabled === false
        ? "Disabled in overlay"
        : (cardId === "cpu" ? "Provider warming" : cardId === "gpu" ? "Provider required" : "Provider route pending");
    }
  });
}

function monitoringHudUpdateSurfaceSplit() {
  if (monitoringHud) {
    monitoringHud.dataset.productSurfaceRole = "dashboard-configuration-surface";
    monitoringHud.dataset.dashboardSurface = "monitoring-hud-dashboard";
    monitoringHud.dataset.configuresSurface = "monitoring-hud-minimal";
    monitoringHud.dataset.splitContract = "dashboard-configures-minimal-overlay";
    monitoringHud.dataset.nativeDashboardOwner = "DesktopRuntimeWindow";
    monitoringHud.dataset.standaloneWindowContract = "dashboard-overlay-core-independent-native-surfaces";
    monitoringHud.dataset.dragSmoothing = "native-os-window-move";
    monitoringHud.dataset.nativeResizeModel = "os-edge-corner-resize";
    monitoringHud.dataset.scrollbarStyle = "nexus-thin-glow";
    monitoringHud.dataset.primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel";
    monitoringHud.dataset.interfaceAcceptancePolicy = "dashboard-only-current-branch";
    monitoringHud.dataset.dashboardAcceptanceBaseline = "ws31-dashboard-control-panel";
    monitoringHud.dataset.dashboardProofPath = "dashboard-specific-static-live-uts";
    monitoringHud.dataset.overlayAcceptancePolicy = "deferred-non-gating";
    monitoringHud.dataset.interfaceBundleApproval = "not-granted";
    monitoringHud.dataset.coreRepairClassification = "dependency-repair-only";
    monitoringHud.dataset.dashboardContentPolish = "ws33-settings-control-clarity";
    monitoringHud.dataset.dashboardSettingsModel = "hud-capability-monitor-groups-provider-warning";
    monitoringHud.dataset.monitorGroupModel = "organizational-groups-settings-only";
    monitoringHud.dataset.dashboardMonitorCardPolicy = "overlay-display-owns-monitor-cards";
  }
  if (!monitoringHudMinimal) return;
  monitoringHudMinimal.dataset.visibilityState = monitoringHudControlState.overlayDeferred !== false ? "hidden-deferred" : (monitoringHudControlState.visible ? "visible" : "hidden");
  monitoringHudMinimal.dataset.anchorState = monitoringHudControlState.anchored ? "anchored" : "unanchored";
  monitoringHudMinimal.dataset.interactionMode = monitoringHudControlState.anchored
    ? "anchored-click-through"
    : "unanchored-edit-preview";
  monitoringHudMinimal.dataset.configuredBy = "monitoring-hud";
  monitoringHudMinimal.dataset.dashboardOwner = "monitoring-hud";
  monitoringHudMinimal.dataset.splitContract = "dashboard-configures-minimal-overlay";
  monitoringHudMinimal.dataset.nativeOverlayOwner = "MonitoringHudOverlayDisplayWindow";
  monitoringHudMinimal.dataset.nativeWindowSplitProof = "ready-ws26";
  monitoringHudMinimal.dataset.providerState = monitoringHudTelemetry.providerState || "setup-required";
  monitoringHudMinimal.dataset.liveValues = monitoringHudTelemetry.liveValues || "provider-required";
  monitoringHudMinimal.dataset.warningMode = "visual-non-invasive";
  monitoringHudMinimal.dataset.clickThroughProof = monitoringHudControlState.anchored
    ? "native-transparent-input"
    : "edit-mode-preview";
  monitoringHudMinimal.dataset.focusProof = monitoringHudControlState.anchored
    ? "native-no-focus-noactivate"
    : "edit-mode-preview";
  monitoringHudMinimal.dataset.interfaceAcceptancePolicy = "deferred-non-gating";
  monitoringHudMinimal.dataset.dashboardAcceptanceRole = "supporting-future-interface-evidence";
  monitoringHudMinimal.dataset.currentBranchReleaseGate = "false";
  if (monitoringHudMinimalRuntimeStatus) {
    monitoringHudMinimalRuntimeStatus.textContent = monitoringHudControlState.visible ? "Minimal HUD enabled" : "Minimal HUD hidden";
  }
  if (monitoringHudMinimalAnchor) {
    monitoringHudMinimalAnchor.textContent = monitoringHudControlState.anchored ? "Anchored" : "Edit";
  }
  if (monitoringHudMinimalProviderState) {
    monitoringHudMinimalProviderState.textContent = monitoringHudTelemetry.providerLabel || "Provider setup required";
  }
  if (monitoringHudMinimalWarning) {
    monitoringHudMinimalWarning.textContent = monitoringHudStatus.warningPosture || "Visual warning baseline only";
  }
  monitoringHudRenderOverlayDisplay();
}

function monitoringHudApplyCardLayout() {
  monitoringHudEnsureCardNodes();
  Object.keys(monitoringHudControlState.cards).forEach((cardId) => {
    const layout = Object.assign(monitoringHudCardDefaults(cardId), monitoringHudControlState.cards[cardId] || {});
    monitoringHudNormalizeMonitorGroupTitle(cardId, layout);
    monitoringHudControlState.cards[cardId] = layout;
  });
  monitoringHudRenderMonitorManagement();
  monitoringHudRenderOverlayDisplay();
}

function monitoringHudRenderControls() {
  if (!monitoringHud) return;
  const featureEnabled = Boolean(monitoringHudControlState.featureEnabled);
  const dashboardVisible = Boolean(featureEnabled && monitoringHudControlState.visible);
  const overlayDeferred = monitoringHudControlState.overlayDeferred !== false;
  monitoringHudControlState.visible = dashboardVisible;
  monitoringHud.dataset.visibilityState = dashboardVisible ? "visible" : "hidden";
  monitoringHud.dataset.featureEnabled = featureEnabled ? "true" : "false";
  monitoringHud.dataset.overlayDeferred = overlayDeferred ? "true" : "false";
  monitoringHud.dataset.anchorState = monitoringHudControlState.anchored ? "overlay-anchored" : "overlay-unanchored";
  monitoringHud.dataset.interactionMode = "standalone-dashboard-window";
  monitoringHud.dataset.controlsState = featureEnabled
    ? (dashboardVisible ? "feature-enabled-dashboard-open" : "feature-enabled-dashboard-closed")
    : "feature-disabled-dashboard-closed";
  monitoringHud.dataset.snapState = monitoringHudControlState.snapEnabled ? "enabled" : "disabled";
  monitoringHud.dataset.pollingRateMs = String(monitoringHudControlState.pollingRateMs);
  monitoringHud.dataset.warningControlPosture = monitoringHudControlState.warningNotificationsMuted
    ? "global-muted"
    : "visual-notifications-enabled";
  monitoringHud.dataset.dashboardProviderTruth = "provider-contract-first";
  monitoringHud.dataset.dashboardStateModel = "setup-no-data-degraded-warning";
  monitoringHud.dataset.dashboardWarningControls = "visual-non-invasive-only";
  monitoringHud.dataset.dashboardFakeTelemetryPolicy = "blocked";
  if (monitoringHudRuntimeStatus) {
    monitoringHudRuntimeStatus.textContent = featureEnabled ? "HUD feature enabled" : "HUD feature disabled";
  }
  if (monitoringHudAnchorStatus) {
    monitoringHudAnchorStatus.textContent = overlayDeferred ? "HUD display deferred" : (monitoringHudControlState.anchored ? "HUD display anchored" : "HUD display unanchored");
  }
  if (monitoringHudToggle) {
    monitoringHudToggle.textContent = featureEnabled ? "Disable HUD feature" : "Enable HUD feature";
  }
  if (monitoringHudAnchorToggle) {
    monitoringHudAnchorToggle.textContent = overlayDeferred ? "HUD display deferred" : (monitoringHudControlState.anchored ? "Unanchor HUD display" : "Anchor HUD display");
    monitoringHudAnchorToggle.disabled = overlayDeferred;
  }
  if (monitoringHudEditMonitor) {
    monitoringHudEditMonitor.textContent = "Edit Monitor Group";
  }
  if (monitoringHudSnapToggle) {
    monitoringHudSnapToggle.textContent = "HUD display settings";
    monitoringHudSnapToggle.disabled = overlayDeferred;
  }
  if (monitoringHudWarningToggle) {
    monitoringHudWarningToggle.textContent = monitoringHudControlState.warningNotificationsMuted
      ? "Warning Notifications Muted"
      : "Warning Notifications On";
  }
  if (monitoringHudSnapLabel) {
    monitoringHudSnapLabel.textContent = "HUD display deferred";
  }
  if (monitoringHudPollingRate) {
    monitoringHudPollingRate.value = String(monitoringHudControlState.pollingRateMs);
  }
  if (monitoringHudWarningModeControl) {
    monitoringHudWarningModeControl.value = monitoringHudControlState.warningMode || "badge-text-color";
  }
  if (monitoringHudWarningPosture) {
    monitoringHudWarningPosture.textContent = monitoringHudControlState.warningNotificationsMuted
      ? "Globally muted; Monitor Group settings preserved"
      : "Visual notifications enabled";
  }
  if (monitoringHudPlacementPointer) {
    monitoringHudPlacementPointer.textContent = "Dashboard controls future HUD display";
  }
  monitoringHudUpdateSurfaceSplit();
  monitoringHudRenderMonitorManagement();
  monitoringHudRenderOverlayDisplay();
}

function monitoringHudApplyPanelPosition(position) {
  if (!monitoringHud || !position) return;
  monitoringHud.style.left = `${position.left}px`;
  monitoringHud.style.top = `${position.top}px`;
  monitoringHud.style.right = "auto";
  monitoringHud.style.transformOrigin = "top left";
}

function monitoringHudSetPanelPosition(left, top, persist = true) {
  if (!monitoringHud) return;
  const minVisibleWidth = Math.min(monitoringHud.offsetWidth, 520);
  const minVisibleHeight = Math.min(monitoringHud.offsetHeight, 420);
  const maxLeft = Math.max(0, window.innerWidth - minVisibleWidth);
  const maxTop = Math.max(0, window.innerHeight - minVisibleHeight);
  const boundedLeft = monitoringHudBound(monitoringHudSnap(left), 0, maxLeft);
  const boundedTop = monitoringHudBound(monitoringHudSnap(top), 0, maxTop);
  monitoringHudControlState.panelPosition = { left: boundedLeft, top: boundedTop };
  monitoringHudQueuedPanelPosition = { left: boundedLeft, top: boundedTop };
  if (typeof window.requestAnimationFrame === "function") {
    if (!monitoringHudPanelPositionFrame) {
      monitoringHudPanelPositionFrame = window.requestAnimationFrame(() => {
        monitoringHudPanelPositionFrame = 0;
        monitoringHudApplyPanelPosition(monitoringHudQueuedPanelPosition);
      });
    }
  } else {
    monitoringHudApplyPanelPosition(monitoringHudQueuedPanelPosition);
  }
  if (persist && !monitoringHudDragInProgress) {
    monitoringHudMarkChanged();
  } else {
    monitoringHudControlState.changedAt = Date.now();
  }
}

function monitoringHudClearPanelPosition() {
  if (!monitoringHud) return;
  monitoringHud.style.left = "";
  monitoringHud.style.top = "";
  monitoringHud.style.right = "";
  monitoringHud.style.transformOrigin = "top right";
  monitoringHudControlState.panelPosition = null;
}

function monitoringHudRenderSensorCards(cards) {
  if (!Array.isArray(cards)) return;
  cards.forEach((card) => {
    if (!card || !card.id) return;
    const cardNode = monitoringHudMonitorList
      ? monitoringHudMonitorList.querySelector(`[data-monitor-config-option="${card.id}"]`)
      : null;
    if (cardNode) {
      if (card.state) cardNode.dataset.monitorProviderState = card.state;
      const statusNode = cardNode.querySelector(`[data-monitor-config-status="${card.id}"]`);
      if (statusNode) statusNode.textContent = card.summary || (card.state === "warning" ? "Warning in future overlay" : "Enabled for future overlay");
    }
    const minimalCardNode = monitoringHudMinimal
      ? monitoringHudMinimal.querySelector(`[data-minimal-card="${card.id}"]`)
      : null;
    if (minimalCardNode && card.state) {
      minimalCardNode.classList.toggle("monitoring-hud-minimal-card--setup", card.state === "setup");
      minimalCardNode.classList.toggle("monitoring-hud-minimal-card--unavailable", card.state === "no-data" || card.state === "degraded");
      minimalCardNode.classList.toggle("monitoring-hud-minimal-card--warning", card.state === "warning");
      minimalCardNode.dataset.cardState = card.state;
    }
    const minimalSummaryNode = monitoringHudMinimal
      ? monitoringHudMinimal.querySelector(`[data-minimal-card-summary="${card.id}"]`)
      : null;
    if (minimalSummaryNode && card.summary) minimalSummaryNode.textContent = card.summary;
    if (!Array.isArray(card.sensors)) return;
    card.sensors.forEach((sensor) => {
      if (!sensor || !sensor.id) return;
      const row = cardNode ? cardNode.querySelector(`[data-sensor-row="${sensor.id}"]`) : null;
      const valueNode = cardNode ? cardNode.querySelector(`[data-sensor-value="${sensor.id}"]`) : null;
      const sourceNode = cardNode ? cardNode.querySelector(`[data-sensor-source="${sensor.id}"]`) : null;
      if (row && sensor.state) row.dataset.liveValue = sensor.state;
      if (valueNode && sensor.value) valueNode.textContent = sensor.value;
      if (sourceNode && sensor.source) sourceNode.textContent = sensor.source;
    });
  });
}

function monitoringHudStartPointerDrag(event, target, onMove) {
  if (!monitoringHud || !monitoringHudControlState.visible) return;
  if (monitoringHudDragInProgress) return;
  if (event.button !== undefined && event.button !== 0) return;
  if (event.target && event.target.closest && event.target.closest("button,input,select,label")) return;
  event.preventDefault();
  monitoringHudDragInProgress = true;
  monitoringHudControlState.lastDragEvent = {
    target: target && target.id ? target.id : (target && target.dataset ? JSON.stringify(target.dataset) : "unknown"),
    phase: "started",
    type: event.type || "unknown",
    startX: event.clientX,
    startY: event.clientY
  };
  const startX = event.clientX;
  const startY = event.clientY;
  const isPointerEvent = String(event.type || "").indexOf("pointer") === 0;
  const moveEventName = isPointerEvent ? "pointermove" : "mousemove";
  const upEventName = isPointerEvent ? "pointerup" : "mouseup";
  const cancelEventName = isPointerEvent ? "pointercancel" : "";
  if (isPointerEvent && typeof target.setPointerCapture === "function" && event.pointerId !== undefined) {
    target.setPointerCapture(event.pointerId);
  }
  function move(moveEvent) {
    monitoringHudControlState.lastDragEvent = Object.assign({}, monitoringHudControlState.lastDragEvent || {}, {
      phase: "moving",
      dx: moveEvent.clientX - startX,
      dy: moveEvent.clientY - startY
    });
    onMove(moveEvent.clientX - startX, moveEvent.clientY - startY);
  }
  function end() {
    monitoringHudControlState.lastDragEvent = Object.assign({}, monitoringHudControlState.lastDragEvent || {}, {
      phase: "ended"
    });
    monitoringHudDragInProgress = false;
    monitoringHudMarkChanged();
    document.removeEventListener(moveEventName, move);
    document.removeEventListener(upEventName, end);
    if (cancelEventName) document.removeEventListener(cancelEventName, end);
  }
  document.addEventListener(moveEventName, move);
  document.addEventListener(upEventName, end);
  if (cancelEventName) document.addEventListener(cancelEventName, end);
}

function monitoringHudWirePanelDrag() {
  if (!monitoringHud || !monitoringHudDragHandle) return;
  const startPanelDrag = (event) => {
    if (document.body && document.body.classList.contains("desktop-mode")) {
      return;
    }
    const rect = monitoringHud.getBoundingClientRect();
    monitoringHudStartPointerDrag(event, monitoringHudDragHandle, (dx, dy) => {
      monitoringHudSetPanelPosition(rect.left + dx, rect.top + dy, false);
    });
  };
  monitoringHudDragHandle.addEventListener("pointerdown", startPanelDrag);
  monitoringHudDragHandle.addEventListener("mousedown", startPanelDrag);
}

function monitoringHudWireCardInteractions() {
  // Monitor card movement/resizing belongs to the standalone overlay window.
  // The dashboard only edits monitor settings and never renders monitor cards.
}

function monitoringHudWireControls() {
  if (monitoringHudToggle) {
    monitoringHudToggle.addEventListener("click", () => {
      monitoringHudControlState.featureEnabled = !monitoringHudControlState.featureEnabled;
      monitoringHudControlState.visible = monitoringHudControlState.featureEnabled;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudAnchorToggle) {
    monitoringHudAnchorToggle.addEventListener("click", () => {
      if (monitoringHudControlState.overlayDeferred !== false) {
        monitoringHudControlState.lastDeferredAnchorRequest = Date.now();
        monitoringHudRenderControls();
        monitoringHudMarkChanged();
        return;
      }
      monitoringHudControlState.anchored = !monitoringHudControlState.anchored;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  function createMonitorGroup() {
    const nextNumber = Math.max(3, Number(monitoringHudControlState.monitorSequence || 2) + 1);
    monitoringHudControlState.monitorSequence = nextNumber;
    const cardId = `monitor-${nextNumber}`;
    monitoringHudControlState.cards[cardId] = {
      x: 0,
      y: (nextNumber - 1) * 300,
      w: 600,
      h: 280,
      title: `Monitor Group ${nextNumber}`,
      enabled: true,
      pollingRateMs: 1000
    };
    monitoringHudControlState.selectedMonitorId = cardId;
    monitoringHudApplyCardLayout();
    monitoringHudWireCardInteractions();
    monitoringHudRenderControls();
    monitoringHudMarkChanged();
  }
  if (monitoringHudCreateMonitor) {
    monitoringHudCreateMonitor.addEventListener("click", () => {
      createMonitorGroup();
    });
  }
  document.querySelectorAll('[data-control="create-monitor"]').forEach((button) => {
    if (button === monitoringHudCreateMonitor) return;
    button.addEventListener("click", createMonitorGroup);
  });
  if (monitoringHudSnapToggle) {
    monitoringHudSnapToggle.addEventListener("click", () => {
      monitoringHudControlState.snapEnabled = !monitoringHudControlState.snapEnabled;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudPollingRate) {
    monitoringHudPollingRate.addEventListener("change", () => {
      const value = Number(monitoringHudPollingRate.value) || 1000;
      monitoringHudControlState.pollingRateMs = Math.max(1000, value);
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudWarningModeControl) {
    monitoringHudWarningModeControl.addEventListener("change", () => {
      const allowedModes = new Set(["badge-text-color", "badge-only", "text-color"]);
      const value = String(monitoringHudWarningModeControl.value || "badge-text-color");
      monitoringHudControlState.warningMode = allowedModes.has(value) ? value : "badge-text-color";
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  document.querySelectorAll('[data-control="warning-notifications"]').forEach((button) => {
    button.addEventListener("click", () => {
      monitoringHudControlState.warningNotificationsMuted = !monitoringHudControlState.warningNotificationsMuted;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  });
  if (monitoringHudMonitorEnabled) {
    monitoringHudMonitorEnabled.addEventListener("change", () => {
      const selected = monitoringHudSelectedMonitor();
      if (selected.layout) selected.layout.enabled = Boolean(monitoringHudMonitorEnabled.checked);
      monitoringHudRenderMonitorManagement();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudMonitorPollingRate) {
    monitoringHudMonitorPollingRate.addEventListener("change", () => {
      const selected = monitoringHudSelectedMonitor();
      if (selected.layout) selected.layout.pollingRateMs = Math.max(1000, Number(monitoringHudMonitorPollingRate.value) || 1000);
      monitoringHudRenderMonitorManagement();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudMonitorSelector) {
    monitoringHudMonitorSelector.addEventListener("change", () => {
      const cardId = monitoringHudMonitorSelector.value;
      if (!cardId || !monitoringHudControlState.cards[cardId]) return;
      monitoringHudControlState.selectedMonitorId = cardId;
      monitoringHudRenderMonitorManagement();
      monitoringHudMarkChanged();
    });
  }
}

function monitoringHudInitializeControls() {
  monitoringHudLoadStoredState();
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudWirePanelDrag();
  monitoringHudWireCardInteractions();
  monitoringHudWireControls();
  document.addEventListener("mousedown", (event) => {
    const target = event.target && event.target.id
      ? event.target.id
      : (event.target && event.target.dataset ? JSON.stringify(event.target.dataset) : String(event.target && event.target.tagName || "unknown"));
    monitoringHudControlState.lastMouseEvent = {
      type: "mousedown",
      target,
      x: event.clientX,
      y: event.clientY
    };
  }, true);
  document.addEventListener("mousemove", (event) => {
    if (event.buttons !== 1) return;
    monitoringHudControlState.lastMouseEvent = {
      type: "mousemove",
      target: event.target && event.target.id ? event.target.id : String(event.target && event.target.tagName || "unknown"),
      x: event.clientX,
      y: event.clientY,
      buttons: event.buttons
    };
  }, true);
}

window.getMonitoringHudControlState = function() {
  return Object.assign({}, monitoringHudControlState, {
    cards: Object.assign({}, monitoringHudControlState.cards)
  });
};

window.getMonitoringHudLiveClientGeometry = function() {
  function rectFor(selector) {
    const node = document.querySelector(selector);
    if (!node) return null;
    const rect = node.getBoundingClientRect();
    return {
      left: rect.left,
      top: rect.top,
      width: rect.width,
      height: rect.height,
      right: rect.right,
      bottom: rect.bottom,
      centerX: rect.left + rect.width / 2,
      centerY: rect.top + rect.height / 2
    };
  }
  return {
    hud: rectFor("#monitoring-hud"),
    dashboard: rectFor("#monitoring-hud"),
    minimalHud: rectFor("#monitoring-hud-minimal"),
    overlayDisplay: rectFor("#monitoring-hud-overlay-display"),
    overlayCanvas: rectFor("#monitoring-hud-overlay-canvas"),
    coreWrap: null,
    anchorToggle: rectFor("#monitoring-hud-anchor-toggle"),
    createMonitor: rectFor("#monitoring-hud-create-monitor"),
    editMonitor: rectFor("#monitoring-hud-edit-monitor"),
    visibilityToggle: rectFor("#monitoring-hud-toggle"),
    snapToggle: rectFor("#monitoring-hud-snap-toggle"),
    warningToggle: rectFor("#monitoring-hud-warning-toggle"),
    pollingRate: rectFor("#monitoring-hud-polling-rate"),
    warningModeControl: rectFor("#monitoring-hud-warning-mode-control"),
    panelDragHandle: rectFor("#monitoring-hud-drag-handle"),
    monitorList: rectFor("#monitoring-hud-monitor-list"),
    monitorSelector: rectFor("#monitoring-hud-monitor-selector"),
    dataSourcesAction: rectFor('[data-control="open-data-sources"]'),
    hudDisplaySettingsAction: rectFor('[data-control="hud-display-settings"]'),
    monitorEnabled: rectFor("#monitoring-hud-monitor-enabled"),
    monitorPollingRate: rectFor("#monitoring-hud-monitor-polling-rate"),
    monitorListSummary: rectFor("#monitoring-hud-monitor-list-summary")
  };
};

window.getMonitoringHudSurfaceSplitState = function() {
  const dashboardRect = monitoringHud ? monitoringHud.getBoundingClientRect() : null;
  const minimalRect = monitoringHudMinimal ? monitoringHudMinimal.getBoundingClientRect() : null;
  const overlayRect = monitoringHudOverlayDisplay ? monitoringHudOverlayDisplay.getBoundingClientRect() : null;
  return {
    dashboardPresent: Boolean(monitoringHud),
    minimalHudPresent: Boolean(monitoringHudMinimal),
    overlayDisplayPresent: Boolean(monitoringHudOverlayDisplay),
    dashboardSurfaceRole: monitoringHud ? monitoringHud.dataset.productSurfaceRole || "" : "",
    minimalHudSurfaceRole: monitoringHudMinimal ? monitoringHudMinimal.dataset.productSurfaceRole || "" : "",
    overlayDisplaySurfaceRole: monitoringHudOverlayDisplay ? monitoringHudOverlayDisplay.dataset.productSurfaceRole || "" : "",
    overlayCanvas: monitoringHudOverlayDisplay ? monitoringHudOverlayDisplay.dataset.overlayCanvas || "" : "",
    overlayMonitorLayout: monitoringHudOverlayDisplay ? monitoringHudOverlayDisplay.dataset.monitorLayout || "" : "",
    overlayEdgeToEdgePosture: monitoringHudOverlayDisplay ? monitoringHudOverlayDisplay.dataset.edgeToEdgePosture || "" : "",
    dashboardConfigures: monitoringHud ? monitoringHud.dataset.configuresSurface || "" : "",
    minimalConfiguredBy: monitoringHudMinimal ? monitoringHudMinimal.dataset.configuredBy || "" : "",
    splitContract: monitoringHudMinimal ? monitoringHudMinimal.dataset.splitContract || "" : "",
    dashboardVisible: Boolean(dashboardRect && dashboardRect.width > 100 && dashboardRect.height > 100),
    minimalHudVisible: Boolean(minimalRect && minimalRect.width > 180 && minimalRect.height > 80),
    overlayDisplayVisible: Boolean(overlayRect && overlayRect.width > 640 && overlayRect.height > 420),
    overlayDisplayEdgeToEdge: Boolean(
      overlayRect
      && overlayRect.width >= Math.max(640, window.innerWidth - 24)
      && overlayRect.height >= Math.max(360, window.innerHeight - 24)
    ),
    primaryInterfaceReleaseSurface: monitoringHud ? monitoringHud.dataset.primaryInterfaceReleaseSurface || "" : "",
    dashboardAcceptanceBaseline: monitoringHud ? monitoringHud.dataset.dashboardAcceptanceBaseline || "" : "",
    dashboardProofPath: monitoringHud ? monitoringHud.dataset.dashboardProofPath || "" : "",
    dashboardStandaloneProof: monitoringHud ? monitoringHud.dataset.dashboardStandaloneProof || "" : "",
    dashboardClippingProof: monitoringHud ? monitoringHud.dataset.dashboardClippingProof || "" : "",
    dashboardDecouplingProof: monitoringHud ? monitoringHud.dataset.dashboardDecouplingProof || "" : "",
    dashboardContentPolish: monitoringHud ? monitoringHud.dataset.dashboardContentPolish || "" : "",
    dashboardSettingsModel: monitoringHud ? monitoringHud.dataset.dashboardSettingsModel || "" : "",
    monitorGroupModel: monitoringHud ? monitoringHud.dataset.monitorGroupModel || "" : "",
    dashboardMonitorCardPolicy: monitoringHud ? monitoringHud.dataset.dashboardMonitorCardPolicy || "" : "",
    dashboardProviderTruth: monitoringHud ? monitoringHud.dataset.dashboardProviderTruth || "" : "",
    dashboardStateModel: monitoringHud ? monitoringHud.dataset.dashboardStateModel || "" : "",
    dashboardWarningControls: monitoringHud ? monitoringHud.dataset.dashboardWarningControls || "" : "",
    dashboardFakeTelemetryPolicy: monitoringHud ? monitoringHud.dataset.dashboardFakeTelemetryPolicy || "" : "",
    warningControlPosture: monitoringHud ? monitoringHud.dataset.warningControlPosture || "" : "",
    interfaceAcceptancePolicy: monitoringHud ? monitoringHud.dataset.interfaceAcceptancePolicy || "" : "",
    overlayAcceptancePolicy: monitoringHud ? monitoringHud.dataset.overlayAcceptancePolicy || "" : "",
    interfaceBundleApproval: monitoringHud ? monitoringHud.dataset.interfaceBundleApproval || "" : "",
    coreRepairClassification: monitoringHud ? monitoringHud.dataset.coreRepairClassification || "" : "",
    minimalHudAcceptancePolicy: monitoringHudMinimal ? monitoringHudMinimal.dataset.interfaceAcceptancePolicy || "" : "",
    overlayDisplayAcceptancePolicy: monitoringHudOverlayDisplay ? monitoringHudOverlayDisplay.dataset.interfaceAcceptancePolicy || "" : "",
    sharedRendererOwner: monitoringHudMinimal ? monitoringHudMinimal.dataset.rendererOwner || "" : "",
    nativeOverlayOwner: monitoringHudMinimal ? monitoringHudMinimal.dataset.nativeOverlayOwner || "" : "",
    nativeWindowSplitProof: monitoringHudMinimal ? monitoringHudMinimal.dataset.nativeWindowSplitProof || "" : ""
  };
};

window.getMonitoringHudDashboardAcceptanceState = function() {
  const split = window.getMonitoringHudSurfaceSplitState ? window.getMonitoringHudSurfaceSplitState() : {};
  return {
    primaryInterfaceReleaseSurface: split.primaryInterfaceReleaseSurface || "",
    dashboardAcceptanceBaseline: split.dashboardAcceptanceBaseline || "",
    dashboardProofPath: split.dashboardProofPath || "",
    dashboardStandaloneProof: split.dashboardStandaloneProof || "",
    dashboardClippingProof: split.dashboardClippingProof || "",
    dashboardDecouplingProof: split.dashboardDecouplingProof || "",
    interfaceAcceptancePolicy: split.interfaceAcceptancePolicy || "",
    overlayAcceptancePolicy: split.overlayAcceptancePolicy || "",
    interfaceBundleApproval: split.interfaceBundleApproval || "",
    coreRepairClassification: split.coreRepairClassification || "",
    overlayAcceptanceNonGating: Boolean(
      split.overlayAcceptancePolicy === "deferred-non-gating"
      && split.minimalHudAcceptancePolicy === "deferred-non-gating"
      && split.overlayDisplayAcceptancePolicy === "deferred-non-gating"
    ),
    dashboardAcceptanceBaselineReady: Boolean(
      split.primaryInterfaceReleaseSurface === "monitoring-hud-dashboard-control-panel"
      && split.dashboardAcceptanceBaseline === "ws31-dashboard-control-panel"
      && split.interfaceAcceptancePolicy === "dashboard-only-current-branch"
      && split.interfaceBundleApproval === "not-granted"
    ),
    dashboardStandaloneMovementReady: Boolean(
      split.dashboardStandaloneProof === "ws32-dashboard-window-travel"
      && split.dashboardClippingProof === "within-virtual-desktop"
      && split.dashboardDecouplingProof === "core-overlay-independent"
    ),
    dashboardSettingsContentReady: Boolean(
      split.dashboardContentPolish === "ws33-settings-control-clarity"
      && split.dashboardSettingsModel === "hud-capability-monitor-groups-provider-warning"
      && split.monitorGroupModel === "organizational-groups-settings-only"
      && split.dashboardMonitorCardPolicy === "overlay-display-owns-monitor-cards"
    ),
    dashboardProviderTruthReady: Boolean(
      split.dashboardProviderTruth === "provider-contract-first"
      && split.dashboardStateModel === "setup-no-data-degraded-warning"
      && split.dashboardWarningControls === "visual-non-invasive-only"
      && split.dashboardFakeTelemetryPolicy === "blocked"
    )
  };
};

window.getMonitoringHudIsolationState = function() {
  const hudRect = monitoringHud ? monitoringHud.getBoundingClientRect() : null;
  const minimalRect = monitoringHudMinimal ? monitoringHudMinimal.getBoundingClientRect() : null;
  const overlayRect = monitoringHudOverlayDisplay ? monitoringHudOverlayDisplay.getBoundingClientRect() : null;
  const split = window.getMonitoringHudSurfaceSplitState ? window.getMonitoringHudSurfaceSplitState() : {};
  const hudWindowMode = body.classList.contains("hud-window-mode");
  return {
    hudWindowMode,
    coreWindowMode: false,
    standaloneHudWindow: Boolean(hudWindowMode && monitoringHud && !document.getElementById("scene")),
    coreSceneHiddenInHudWindow: Boolean(hudWindowMode && !document.getElementById("scene")),
    coreWrapPresent: false,
    coreWrapVisible: false,
    coreWrapVisuallyReadable: false,
    hudPresent: Boolean(monitoringHud),
    hudVisible: Boolean(hudRect && hudRect.width > 100 && hudRect.height > 100),
    dashboardSurfacePresent: Boolean(monitoringHud),
    minimalHudSurfacePresent: Boolean(monitoringHudMinimal),
    overlayDisplaySurfacePresent: Boolean(monitoringHudOverlayDisplay),
    minimalHudVisible: Boolean(minimalRect && minimalRect.width > 180 && minimalRect.height > 80),
    overlayDisplayVisible: Boolean(overlayRect && overlayRect.width > 640 && overlayRect.height > 420),
    overlayDisplayEdgeToEdge: split.overlayDisplayEdgeToEdge === true,
    dashboardMinimalSplitReady: Boolean(
      split.dashboardSurfaceRole === "dashboard-configuration-surface"
      && split.minimalHudSurfaceRole === "minimal-anchored-hud-overlay"
      && split.dashboardConfigures === "monitoring-hud-minimal"
      && split.minimalConfiguredBy === "monitoring-hud"
    ),
    dashboardAcceptanceBaselineReady: Boolean(
      split.primaryInterfaceReleaseSurface === "monitoring-hud-dashboard-control-panel"
      && split.dashboardAcceptanceBaseline === "ws31-dashboard-control-panel"
      && split.interfaceAcceptancePolicy === "dashboard-only-current-branch"
      && split.overlayAcceptancePolicy === "deferred-non-gating"
      && split.interfaceBundleApproval === "not-granted"
    ),
    overlayAcceptanceNonGating: Boolean(
      split.overlayAcceptancePolicy === "deferred-non-gating"
      && split.minimalHudAcceptancePolicy === "deferred-non-gating"
      && split.overlayDisplayAcceptancePolicy === "deferred-non-gating"
    ),
    primaryInterfaceReleaseSurface: split.primaryInterfaceReleaseSurface || "",
    interfaceAcceptancePolicy: split.interfaceAcceptancePolicy || "",
    overlayAcceptancePolicy: split.overlayAcceptancePolicy || "",
    interfaceBundleApproval: split.interfaceBundleApproval || "",
    dashboardSurfaceRole: split.dashboardSurfaceRole || "",
    minimalHudSurfaceRole: split.minimalHudSurfaceRole || "",
    hudOutsideCoreScene: Boolean(monitoringHud && !document.getElementById("scene")),
    coreHudOverlap: false,
    coreHudGap: 999,
    coreHudSeparated: true,
    isolationBoundary: monitoringHud ? monitoringHud.dataset.isolationBoundary || "" : "",
    coreFailureIsolation: monitoringHud ? monitoringHud.dataset.coreFailureIsolation || "" : "",
    validationFault: monitoringHud ? monitoringHud.dataset.validationFault || "" : "",
    desktopMode: body.classList.contains("desktop-mode")
  };
};

window.simulateMonitoringHudFaultForValidation = function(enabled) {
  if (monitoringHud) {
    monitoringHud.dataset.validationFault = enabled ? "simulated-hud-module-fault" : "";
    monitoringHud.classList.toggle("monitoring-hud--validation-fault", Boolean(enabled));
  }
  return window.getMonitoringHudIsolationState();
};

window.setMonitoringHudControlState = function(state) {
  monitoringHudControlState = Object.assign({}, monitoringHudControlState, state || {});
  monitoringHudControlState.featureEnabled = Boolean(monitoringHudControlState.featureEnabled);
  monitoringHudControlState.overlayDeferred = monitoringHudControlState.overlayDeferred !== false;
  monitoringHudControlState.visible = Boolean(monitoringHudControlState.featureEnabled && monitoringHudControlState.visible);
  monitoringHudControlState.warningMode = monitoringHudControlState.warningMode || "badge-text-color";
  monitoringHudControlState.cards = Object.assign({}, {
    cpu: { x: 0, y: 0, w: 600, h: 280, title: "CPU Group", enabled: true, pollingRateMs: 1000 },
    gpu: { x: 0, y: 300, w: 600, h: 280, title: "GPU Group", enabled: true, pollingRateMs: 1000 }
  }, monitoringHudControlState.cards || {});
  Object.keys(monitoringHudControlState.cards).forEach((cardId) => {
    monitoringHudControlState.cards[cardId] = Object.assign(
      monitoringHudCardDefaults(cardId),
      monitoringHudControlState.cards[cardId] || {}
    );
  });
  if (!monitoringHudControlState.selectedMonitorId || !monitoringHudControlState.cards[monitoringHudControlState.selectedMonitorId]) {
    monitoringHudControlState.selectedMonitorId = Object.keys(monitoringHudControlState.cards)[0] || "cpu";
  }
  monitoringHudControlState.monitorSequence = Math.max(
    Number(monitoringHudControlState.monitorSequence || 2),
    Object.keys(monitoringHudControlState.cards).length
  );
  if (monitoringHudControlState.panelPosition) {
    monitoringHudSetPanelPosition(
      monitoringHudControlState.panelPosition.left || 0,
      monitoringHudControlState.panelPosition.top || 0
    );
  } else if (monitoringHud) {
    monitoringHudClearPanelPosition();
  }
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudMarkChanged();
};

window.setDesktopSurfaceMode = function(enabled) {
  const isEnabled = Boolean(enabled);
  body.classList.toggle("desktop-mode", isEnabled);
  body.classList.add("hud-window-mode");
  if (monitoringHud) {
    monitoringHud.setAttribute("aria-hidden", isEnabled ? "false" : "true");
    monitoringHud.dataset.renderState = isEnabled ? "product-visibility-baseline" : "hidden";
    monitoringHud.dataset.productSurfaceState = (isEnabled && monitoringHudControlState.visible) ? "visible-user-facing" : "hidden";
  }
  if (monitoringHudMinimal) {
    monitoringHudMinimal.setAttribute("aria-hidden", isEnabled ? "false" : "true");
    monitoringHudMinimal.dataset.renderState = isEnabled ? "minimal-overlay-ready" : "hidden";
    monitoringHudMinimal.dataset.productSurfaceState = "hidden-deferred";
  }
  if (monitoringHudOverlayDisplay) {
    monitoringHudOverlayDisplay.setAttribute("aria-hidden", isEnabled ? "false" : "true");
    monitoringHudOverlayDisplay.dataset.renderState = isEnabled ? "edgeless-overlay-display-ready" : "hidden";
    monitoringHudOverlayDisplay.dataset.productSurfaceState = "hidden-deferred";
  }
  monitoringHudRenderControls();
};

window.setMonitoringHudTelemetry = function(snapshot) {
  monitoringHudTelemetry = Object.assign({}, monitoringHudTelemetry, snapshot || {});
  if (monitoringHud) {
    monitoringHud.dataset.telemetryPackage = monitoringHudTelemetry.packageId || "PKG-006";
    monitoringHud.dataset.telemetrySlice = monitoringHudTelemetry.sliceId || "SLC-025";
    monitoringHud.dataset.telemetryAdapter = monitoringHudTelemetry.adapterId || "desktop-runtime-boundary";
    monitoringHud.dataset.providerState = monitoringHudTelemetry.providerState || "setup-required";
    monitoringHud.dataset.liveValues = monitoringHudTelemetry.liveValues || "provider-required";
    monitoringHud.dataset.pollingRateMs = String(monitoringHudTelemetry.pollingRateMs || monitoringHudControlState.pollingRateMs || 1000);
  }
  if (monitoringHudRuntimeStatus) {
    monitoringHudRuntimeStatus.textContent = monitoringHudControlState.visible ? "HUD capability enabled" : "HUD capability disabled";
  }
  if (monitoringHudProviderState) {
    monitoringHudProviderState.textContent = monitoringHudTelemetry.providerLabel || "Provider setup required";
  }
  if (monitoringHudAdapterStatus) {
    monitoringHudAdapterStatus.textContent = monitoringHudTelemetry.adapterStatus || "Waiting for safe provider";
  }
  if (monitoringHudSourceScope) {
    monitoringHudSourceScope.textContent = monitoringHudTelemetry.sourceScope || "Provider-first; no fake values";
  }
  if (monitoringHudHardwarePolling) {
    monitoringHudHardwarePolling.textContent = monitoringHudTelemetry.hardwarePolling || "1s after provider proof";
  }
  if (monitoringHudProviderStateMatrix) {
    monitoringHudProviderStateMatrix.textContent = "Setup / no data / degraded / ready";
  }
  monitoringHudRenderSensorCards(monitoringHudTelemetry.sensorCards);
  monitoringHudUpdateSurfaceSplit();
};

window.setMonitoringHudPlacementOwnership = function(contract) {
  monitoringHudPlacement = Object.assign({}, monitoringHudPlacement, contract || {});
  if (monitoringHud) {
    monitoringHud.dataset.placementPackage = monitoringHudPlacement.packageId || "PKG-006";
    monitoringHud.dataset.placementSlice = monitoringHudPlacement.sliceId || "SLC-026";
    monitoringHud.dataset.placementId = monitoringHudPlacement.placementId || "standalone-native-hud-window";
    monitoringHud.dataset.placementState = "desktop-renderer-owned";
    monitoringHud.dataset.interactionMode = "standalone-dashboard-window";
  }
  if (monitoringHudPlacementOwner) {
    monitoringHudPlacementOwner.textContent = monitoringHudPlacement.rendererOwner || "Future HUD display is deferred. The Dashboard can store settings now without asking for Overlay acceptance.";
  }
  if (monitoringHudPlacementAnchor) {
    monitoringHudPlacementAnchor.textContent = monitoringHudPlacement.anchor || "Deferred / non-gating";
  }
  if (monitoringHudPlacementPointer) {
    monitoringHudPlacementPointer.textContent = monitoringHudPlacement.pointerModel || "Dashboard controls future HUD display";
  }
  if (monitoringHudResizePosture) {
    monitoringHudResizePosture.textContent = monitoringHudPlacement.resizePosture || "Prepared for future HUD display branch";
  }
  monitoringHudUpdateSurfaceSplit();
};

window.setMonitoringHudControlsVisibility = function(contract) {
  monitoringHudControls = Object.assign({}, monitoringHudControls, contract || {});
  if (monitoringHud) {
    monitoringHud.dataset.controlsPackage = monitoringHudControls.packageId || "PKG-006";
    monitoringHud.dataset.controlsSlice = monitoringHudControls.sliceId || "SLC-027";
    monitoringHud.dataset.controlsId = monitoringHudControls.controlsId || "hud-controls-visibility";
    monitoringHud.dataset.controlsState = monitoringHudControlState.featureEnabled
      ? (monitoringHudControlState.visible ? "feature-enabled-dashboard-open" : "feature-enabled-dashboard-closed")
      : "feature-disabled-dashboard-closed";
    monitoringHud.dataset.keybindPolicy = "none";
    monitoringHud.dataset.monitorManagement = "create-edit-enable-polling";
    monitoringHud.dataset.overlayModeControls = "enable-disable-anchor-unanchor";
  }
  if (monitoringHudControlsVisibility) {
    monitoringHudControlsVisibility.textContent = monitoringHudControls.visibilityState || "HUD feature disabled from dashboard/tray";
  }
  if (monitoringHudControlsSurface) {
    monitoringHudControlsSurface.textContent = monitoringHudControls.controlSurface || "Tray controls HUD feature state; Dashboard open/close is separate; HUD display remains deferred";
  }
  if (monitoringHudControlsPersistence) {
    monitoringHudControlsPersistence.textContent = monitoringHudControls.persistence || "Store group/layout posture locally";
  }
  if (monitoringHudWarningPosture && monitoringHudControls.warningControls) {
    monitoringHudWarningPosture.textContent = monitoringHudControls.warningControls;
  }
  if (monitoringHudTrayPath) {
    monitoringHudTrayPath.textContent = monitoringHudControls.trayPath || "Task tray enables/disables HUD feature and opens/closes Dashboard; Overlay controls deferred";
  }
  monitoringHudRenderControls();
  monitoringHudUpdateSurfaceSplit();
};

window.setMonitoringHudStatusBehavior = function(snapshot) {
  monitoringHudStatus = Object.assign({}, monitoringHudStatus, snapshot || {});
  if (monitoringHud) {
    monitoringHud.dataset.statusPackage = monitoringHudStatus.packageId || "PKG-006";
    monitoringHud.dataset.statusSlice = monitoringHudStatus.sliceId || "SLC-028";
    monitoringHud.dataset.statusId = monitoringHudStatus.statusId || "hud-local-readiness-status";
    monitoringHud.dataset.statusKind = monitoringHudStatus.statusKind || "no-data";
    monitoringHud.dataset.warningMode = "visual-non-invasive";
    monitoringHud.dataset.warningState = monitoringHudStatus.warningState || "advisory";
    monitoringHud.dataset.dashboardProviderTruth = "provider-contract-first";
    monitoringHud.dataset.dashboardStateModel = "setup-no-data-degraded-warning";
    monitoringHud.dataset.dashboardWarningControls = "visual-non-invasive-only";
    monitoringHud.dataset.dashboardFakeTelemetryPolicy = "blocked";
  }
  if (monitoringHudStatusLabel) {
    monitoringHudStatusLabel.textContent = monitoringHudStatus.statusLabel || "Provider setup required";
  }
  if (monitoringHudNoDataBehavior) {
    monitoringHudNoDataBehavior.textContent = monitoringHudStatus.noDataBehavior || "Show unavailable; no fake values";
  }
  if (monitoringHudDegradedBehavior) {
    monitoringHudDegradedBehavior.textContent = monitoringHudStatus.degradedBehavior || "Name reconnect/setup gap";
  }
  if (monitoringHudWarningPosture) {
    monitoringHudWarningPosture.textContent = monitoringHudStatus.warningPosture || "Visual notifications enabled";
  }
  monitoringHudUpdateSurfaceSplit();
};

monitoringHudInitializeControls();
window.setDesktopSurfaceMode(false);
window.setMonitoringHudTelemetry({});
window.setMonitoringHudPlacementOwnership({});
window.setMonitoringHudControlsVisibility({});
window.setMonitoringHudStatusBehavior({});
