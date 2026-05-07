const body = document.body;
const monitoringHud = document.getElementById("monitoring-hud");
const monitoringHudMinimal = document.getElementById("monitoring-hud-minimal");
const monitoringHudMinimalRuntimeStatus = document.getElementById("monitoring-hud-minimal-runtime-status");
const monitoringHudMinimalProviderState = document.getElementById("monitoring-hud-minimal-provider-state");
const monitoringHudMinimalAnchor = document.getElementById("monitoring-hud-minimal-anchor");
const monitoringHudMinimalWarning = document.getElementById("monitoring-hud-minimal-warning");
const monitoringHudRuntimeStatus = document.getElementById("monitoring-hud-runtime-status");
const monitoringHudProviderState = document.getElementById("monitoring-hud-provider-state");
const monitoringHudAdapterStatus = document.getElementById("monitoring-hud-adapter-status");
const monitoringHudSourceScope = document.getElementById("monitoring-hud-source-scope");
const monitoringHudHardwarePolling = document.getElementById("monitoring-hud-hardware-polling");
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
const monitoringHudSnapToggle = document.getElementById("monitoring-hud-snap-toggle");
const monitoringHudSnapLabel = document.getElementById("monitoring-hud-snap-label");
const monitoringHudPollingRate = document.getElementById("monitoring-hud-polling-rate");
const monitoringHudCardBoard = document.getElementById("monitoring-hud-card-board");

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
  rendererOwner: "Separate minimal HUD overlay",
  anchor: "Anchor anywhere after OS proof",
  pointerModel: "Anchored click-through/no-focus-steal",
  resizePosture: "Cards resize and snap from dashboard"
};
let monitoringHudControls = {
  packageId: "PKG-006",
  sliceId: "SLC-027",
  controlsId: "hud-controls-visibility",
  visibilityState: "Show or hide from dashboard/tray",
  controlSurface: "Unanchor to edit; anchor to observe",
  persistence: "Snap cards; save local layout",
  operatorAction: "No default keybinds"
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
  visible: true,
  anchored: true,
  snapEnabled: true,
  pollingRateMs: 1000,
  panelPosition: null,
  cards: {
    cpu: { x: 0, y: 0, w: 600, h: 280 },
    gpu: { x: 0, y: 300, w: 600, h: 280 }
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

function monitoringHudUpdateSurfaceSplit() {
  if (monitoringHud) {
    monitoringHud.dataset.productSurfaceRole = "dashboard-configuration-surface";
    monitoringHud.dataset.dashboardSurface = "monitoring-hud-dashboard";
    monitoringHud.dataset.configuresSurface = "monitoring-hud-minimal";
    monitoringHud.dataset.splitContract = "dashboard-configures-minimal-overlay";
    monitoringHud.dataset.dragSmoothing = "raf-local-persist-on-release";
    monitoringHud.dataset.scrollbarStyle = "nexus-thin-glow";
  }
  if (!monitoringHudMinimal) return;
  monitoringHudMinimal.dataset.visibilityState = monitoringHudControlState.visible ? "visible" : "hidden";
  monitoringHudMinimal.dataset.anchorState = monitoringHudControlState.anchored ? "anchored" : "unanchored";
  monitoringHudMinimal.dataset.interactionMode = monitoringHudControlState.anchored
    ? "anchored-click-through-pending-ws22"
    : "unanchored-edit-preview";
  monitoringHudMinimal.dataset.configuredBy = "monitoring-hud";
  monitoringHudMinimal.dataset.dashboardOwner = "monitoring-hud";
  monitoringHudMinimal.dataset.splitContract = "dashboard-configures-minimal-overlay";
  monitoringHudMinimal.dataset.providerState = monitoringHudTelemetry.providerState || "setup-required";
  monitoringHudMinimal.dataset.liveValues = monitoringHudTelemetry.liveValues || "provider-required";
  monitoringHudMinimal.dataset.warningMode = "visual-non-invasive";
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
}

function monitoringHudApplyCardLayout() {
  if (!monitoringHudCardBoard) return;
  Object.keys(monitoringHudControlState.cards).forEach((cardId) => {
    const card = monitoringHudCardBoard.querySelector(`[data-category-card="${cardId}"]`);
    const layout = monitoringHudControlState.cards[cardId];
    if (!card || !layout) return;
    card.style.setProperty("--card-x", `${Math.round(layout.x)}px`);
    card.style.setProperty("--card-y", `${Math.round(layout.y)}px`);
    card.style.setProperty("--card-w", `${Math.round(layout.w)}px`);
    card.style.setProperty("--card-h", `${Math.round(layout.h)}px`);
  });
}

function monitoringHudRenderControls() {
  if (!monitoringHud) return;
  monitoringHud.dataset.visibilityState = monitoringHudControlState.visible ? "visible" : "hidden";
  monitoringHud.dataset.anchorState = monitoringHudControlState.anchored ? "anchored" : "unanchored";
  monitoringHud.dataset.interactionMode = monitoringHudControlState.anchored
    ? "anchored-click-through"
    : "unanchored-edit-mode";
  monitoringHud.dataset.controlsState = monitoringHudControlState.visible
    ? "toggle-posture-visible"
    : "toggle-posture-hidden";
  monitoringHud.dataset.snapState = monitoringHudControlState.snapEnabled ? "enabled" : "disabled";
  monitoringHud.dataset.pollingRateMs = String(monitoringHudControlState.pollingRateMs);
  if (monitoringHudRuntimeStatus) {
    monitoringHudRuntimeStatus.textContent = monitoringHudControlState.visible ? "HUD enabled" : "HUD hidden";
  }
  if (monitoringHudAnchorStatus) {
    monitoringHudAnchorStatus.textContent = monitoringHudControlState.anchored ? "Anchored" : "Unanchored";
  }
  if (monitoringHudToggle) {
    monitoringHudToggle.textContent = monitoringHudControlState.visible ? "Hide HUD" : "Show HUD";
  }
  if (monitoringHudAnchorToggle) {
    monitoringHudAnchorToggle.textContent = monitoringHudControlState.anchored ? "Unanchor" : "Anchor";
  }
  if (monitoringHudSnapToggle) {
    monitoringHudSnapToggle.textContent = monitoringHudControlState.snapEnabled ? "Snap on" : "Snap off";
  }
  if (monitoringHudSnapLabel) {
    monitoringHudSnapLabel.textContent = monitoringHudControlState.snapEnabled ? "Snap-ready" : "Snap disabled";
  }
  if (monitoringHudPollingRate) {
    monitoringHudPollingRate.value = String(monitoringHudControlState.pollingRateMs);
  }
  if (monitoringHudPlacementPointer) {
    monitoringHudPlacementPointer.textContent = monitoringHudControlState.anchored
      ? "Anchored click-through"
      : "Unanchored edit mode";
  }
  monitoringHudUpdateSurfaceSplit();
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
    const cardNode = monitoringHudCardBoard
      ? monitoringHudCardBoard.querySelector(`[data-category-card="${card.id}"]`)
      : null;
    if (!cardNode) return;
    if (card.state) cardNode.dataset.cardState = card.state;
    cardNode.classList.toggle("monitoring-hud-card--warning", card.state === "warning");
    cardNode.classList.toggle("monitoring-hud-card--setup", card.state === "setup");
    cardNode.classList.toggle("monitoring-hud-card--unavailable", card.state === "no-data" || card.state === "degraded");
    const summaryNode = cardNode.querySelector(`[data-card-summary="${card.id}"]`);
    if (summaryNode && card.summary) summaryNode.textContent = card.summary;
    const badgeNode = cardNode.querySelector(`[data-card-badge="${card.id}"]`);
    if (badgeNode && card.badge) badgeNode.textContent = card.badge;
    const metaNode = cardNode.querySelector(`[data-card-meta="${card.id}"]`);
    if (metaNode && card.meta) metaNode.textContent = card.meta;
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
      const row = cardNode.querySelector(`[data-sensor-row="${sensor.id}"]`);
      const valueNode = cardNode.querySelector(`[data-sensor-value="${sensor.id}"]`);
      const sourceNode = cardNode.querySelector(`[data-sensor-source="${sensor.id}"]`);
      if (row && sensor.state) row.dataset.liveValue = sensor.state;
      if (valueNode && sensor.value) valueNode.textContent = sensor.value;
      if (sourceNode && sensor.source) sourceNode.textContent = sensor.source;
    });
  });
}

function monitoringHudStartPointerDrag(event, target, onMove) {
  if (!monitoringHud || monitoringHudControlState.anchored) return;
  if (monitoringHudDragInProgress) return;
  if (event.button !== undefined && event.button !== 0) return;
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
    const rect = monitoringHud.getBoundingClientRect();
    monitoringHudStartPointerDrag(event, monitoringHudDragHandle, (dx, dy) => {
      monitoringHudSetPanelPosition(rect.left + dx, rect.top + dy, false);
    });
  };
  monitoringHudDragHandle.addEventListener("pointerdown", startPanelDrag);
  monitoringHudDragHandle.addEventListener("mousedown", startPanelDrag);
}

function monitoringHudWireCardInteractions() {
  if (!monitoringHudCardBoard) return;
  monitoringHudCardBoard.querySelectorAll("[data-card-handle]").forEach((handle) => {
    const startCardDrag = (event) => {
      const card = handle.closest("[data-category-card]");
      if (!card) return;
      const cardId = card.dataset.categoryCard;
      const start = Object.assign({ x: 0, y: 0, w: 600, h: 280 }, monitoringHudControlState.cards[cardId]);
      monitoringHudStartPointerDrag(event, handle, (dx, dy) => {
        const boardWidth = monitoringHudCardBoard.clientWidth || 720;
        const boardHeight = monitoringHudCardBoard.clientHeight || 600;
        const next = Object.assign({}, start, {
          x: monitoringHudBound(monitoringHudSnap(start.x + dx), 0, Math.max(0, boardWidth - start.w)),
          y: monitoringHudBound(monitoringHudSnap(start.y + dy), 0, Math.max(0, boardHeight - start.h))
        });
        monitoringHudControlState.cards[cardId] = next;
        monitoringHudApplyCardLayout();
      });
    };
    handle.addEventListener("pointerdown", startCardDrag);
    handle.addEventListener("mousedown", startCardDrag);
  });
  monitoringHudCardBoard.querySelectorAll("[data-card-resize]").forEach((handle) => {
    const startCardResize = (event) => {
      const card = handle.closest("[data-category-card]");
      if (!card) return;
      const cardId = card.dataset.categoryCard;
      const start = Object.assign({ x: 0, y: 0, w: 600, h: 280 }, monitoringHudControlState.cards[cardId]);
      monitoringHudStartPointerDrag(event, handle, (dx, dy) => {
        const next = Object.assign({}, start, {
          w: monitoringHudBound(
            monitoringHudSnap(start.w + dx),
            340,
            Math.max(340, monitoringHudSnap((monitoringHudCardBoard.clientWidth || 720) - start.x))
          ),
          h: monitoringHudBound(
            monitoringHudSnap(start.h + dy),
            260,
            Math.max(260, monitoringHudSnap((monitoringHudCardBoard.clientHeight || 600) - start.y))
          )
        });
        monitoringHudControlState.cards[cardId] = next;
        monitoringHudApplyCardLayout();
      });
    };
    handle.addEventListener("pointerdown", startCardResize);
    handle.addEventListener("mousedown", startCardResize);
  });
}

function monitoringHudWireControls() {
  if (monitoringHudToggle) {
    monitoringHudToggle.addEventListener("click", () => {
      monitoringHudControlState.visible = !monitoringHudControlState.visible;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudAnchorToggle) {
    monitoringHudAnchorToggle.addEventListener("click", () => {
      monitoringHudControlState.anchored = !monitoringHudControlState.anchored;
      if (monitoringHudControlState.anchored) {
        monitoringHudClearPanelPosition();
      }
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
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
    coreWrap: null,
    anchorToggle: rectFor("#monitoring-hud-anchor-toggle"),
    visibilityToggle: rectFor("#monitoring-hud-toggle"),
    snapToggle: rectFor("#monitoring-hud-snap-toggle"),
    pollingRate: rectFor("#monitoring-hud-polling-rate"),
    panelDragHandle: rectFor("#monitoring-hud-drag-handle"),
    cardBoard: rectFor("#monitoring-hud-card-board"),
    cpuCard: rectFor('[data-category-card="cpu"]'),
    cpuDragHandle: rectFor('[data-card-handle="cpu"]'),
    cpuResizeHandle: rectFor('[data-card-resize="cpu"]'),
    gpuCard: rectFor('[data-category-card="gpu"]'),
    gpuDragHandle: rectFor('[data-card-handle="gpu"]'),
    gpuResizeHandle: rectFor('[data-card-resize="gpu"]')
  };
};

window.getMonitoringHudSurfaceSplitState = function() {
  const dashboardRect = monitoringHud ? monitoringHud.getBoundingClientRect() : null;
  const minimalRect = monitoringHudMinimal ? monitoringHudMinimal.getBoundingClientRect() : null;
  return {
    dashboardPresent: Boolean(monitoringHud),
    minimalHudPresent: Boolean(monitoringHudMinimal),
    dashboardSurfaceRole: monitoringHud ? monitoringHud.dataset.productSurfaceRole || "" : "",
    minimalHudSurfaceRole: monitoringHudMinimal ? monitoringHudMinimal.dataset.productSurfaceRole || "" : "",
    dashboardConfigures: monitoringHud ? monitoringHud.dataset.configuresSurface || "" : "",
    minimalConfiguredBy: monitoringHudMinimal ? monitoringHudMinimal.dataset.configuredBy || "" : "",
    splitContract: monitoringHudMinimal ? monitoringHudMinimal.dataset.splitContract || "" : "",
    dashboardVisible: Boolean(dashboardRect && dashboardRect.width > 100 && dashboardRect.height > 100),
    minimalHudVisible: Boolean(minimalRect && minimalRect.width > 180 && minimalRect.height > 80),
    sharedRendererOwner: monitoringHudMinimal ? monitoringHudMinimal.dataset.rendererOwner || "" : "",
    nativeWindowSplitProof: "pending-ws22"
  };
};

window.getMonitoringHudIsolationState = function() {
  const hudRect = monitoringHud ? monitoringHud.getBoundingClientRect() : null;
  const minimalRect = monitoringHudMinimal ? monitoringHudMinimal.getBoundingClientRect() : null;
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
    minimalHudVisible: Boolean(minimalRect && minimalRect.width > 180 && minimalRect.height > 80),
    dashboardMinimalSplitReady: Boolean(
      split.dashboardSurfaceRole === "dashboard-configuration-surface"
      && split.minimalHudSurfaceRole === "minimal-anchored-hud-overlay"
      && split.dashboardConfigures === "monitoring-hud-minimal"
      && split.minimalConfiguredBy === "monitoring-hud"
    ),
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
  monitoringHudControlState.cards = Object.assign({}, {
    cpu: { x: 0, y: 0, w: 600, h: 280 },
    gpu: { x: 0, y: 300, w: 600, h: 280 }
  }, monitoringHudControlState.cards || {});
  if (monitoringHudControlState.anchored) {
    monitoringHudClearPanelPosition();
  } else if (monitoringHudControlState.panelPosition) {
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
    monitoringHud.dataset.productSurfaceState = isEnabled ? "visible-user-facing" : "hidden";
  }
  if (monitoringHudMinimal) {
    monitoringHudMinimal.setAttribute("aria-hidden", isEnabled ? "false" : "true");
    monitoringHudMinimal.dataset.renderState = isEnabled ? "minimal-overlay-ready" : "hidden";
    monitoringHudMinimal.dataset.productSurfaceState = isEnabled ? "visible-minimal-anchored-hud" : "hidden";
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
    monitoringHudRuntimeStatus.textContent = monitoringHudControlState.visible ? "HUD enabled" : "HUD hidden";
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
    monitoringHud.dataset.interactionMode = monitoringHudControlState.anchored ? "anchored-click-through" : "unanchored-edit-mode";
  }
  if (monitoringHudPlacementOwner) {
    monitoringHudPlacementOwner.textContent = monitoringHudPlacement.rendererOwner || "Separate minimal HUD overlay";
  }
  if (monitoringHudPlacementAnchor) {
    monitoringHudPlacementAnchor.textContent = monitoringHudPlacement.anchor || "Anchor anywhere after OS proof";
  }
  if (monitoringHudPlacementPointer) {
    monitoringHudPlacementPointer.textContent = monitoringHudControlState.anchored
      ? (monitoringHudPlacement.pointerModel || "Anchored click-through")
      : "Unanchored edit mode";
  }
  if (monitoringHudResizePosture) {
    monitoringHudResizePosture.textContent = monitoringHudPlacement.resizePosture || "Cards resize and snap from dashboard";
  }
  monitoringHudUpdateSurfaceSplit();
};

window.setMonitoringHudControlsVisibility = function(contract) {
  monitoringHudControls = Object.assign({}, monitoringHudControls, contract || {});
  if (monitoringHud) {
    monitoringHud.dataset.controlsPackage = monitoringHudControls.packageId || "PKG-006";
    monitoringHud.dataset.controlsSlice = monitoringHudControls.sliceId || "SLC-027";
    monitoringHud.dataset.controlsId = monitoringHudControls.controlsId || "hud-controls-visibility";
    monitoringHud.dataset.controlsState = monitoringHudControlState.visible ? "toggle-posture-visible" : "toggle-posture-hidden";
    monitoringHud.dataset.keybindPolicy = "none";
  }
  if (monitoringHudControlsVisibility) {
    monitoringHudControlsVisibility.textContent = monitoringHudControls.visibilityState || "Show or hide from dashboard/tray";
  }
  if (monitoringHudControlsSurface) {
    monitoringHudControlsSurface.textContent = monitoringHudControls.controlSurface || "Unanchor to edit; anchor to observe";
  }
  if (monitoringHudControlsPersistence) {
    monitoringHudControlsPersistence.textContent = monitoringHudControls.persistence || "Snap cards; save local layout";
  }
  if (monitoringHudTrayPath) {
    monitoringHudTrayPath.textContent = monitoringHudControls.trayPath || "Task tray unanchor path";
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
    monitoringHudWarningPosture.textContent = monitoringHudStatus.warningPosture || "Visual badge only";
  }
  monitoringHudUpdateSurfaceSplit();
};

monitoringHudInitializeControls();
window.setDesktopSurfaceMode(false);
window.setMonitoringHudTelemetry({});
window.setMonitoringHudPlacementOwnership({});
window.setMonitoringHudControlsVisibility({});
window.setMonitoringHudStatusBehavior({});
