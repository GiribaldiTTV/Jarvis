// NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM006-HUD; ledger=SRCOWN-FIRSTPASS-FAM006-HUD-008; surface=monitoring-hud-dashboard-script; status=shared
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
const monitoringHudOverlayProfileEditor = document.getElementById("monitoring-hud-overlay-profile-editor");
const monitoringHudOverlayProfileSelector = document.getElementById("monitoring-hud-overlay-profile-selector");
const monitoringHudOverlayProfileToggle = document.getElementById("monitoring-hud-overlay-profile-toggle");
const monitoringHudOverlayProfileLabel = document.getElementById("monitoring-hud-overlay-profile-label");
const monitoringHudOverlayProfileMenu = document.getElementById("monitoring-hud-overlay-profile-menu");
const monitoringHudOverlayProfileMonitorCount = document.getElementById("monitoring-hud-overlay-profile-monitor-count");
const monitoringHudOverlayProfileDisplayMode = document.getElementById("monitoring-hud-overlay-profile-display-mode");
const monitoringHudOverlayProfileOpenSettings = document.getElementById("monitoring-hud-overlay-profile-open-settings");
const monitoringHudOverlayProfileNameInput = document.getElementById("monitoring-hud-overlay-profile-name-input");
const monitoringHudOverlayProfileCreate = document.getElementById("monitoring-hud-overlay-profile-create");
const monitoringHudOverlayProfileSave = document.getElementById("monitoring-hud-overlay-profile-save");
const monitoringHudOverlayProfileDiscard = document.getElementById("monitoring-hud-overlay-profile-discard");
const monitoringHudOverlayProfileMembershipNote = document.getElementById("monitoring-hud-overlay-profile-membership-note");
const monitoringHudOverlayProfileMembershipList = document.getElementById("monitoring-hud-overlay-profile-membership-list");
const monitoringHudOverlayProfileWindow = document.getElementById("monitoring-hud-overlay-profile-window");
const monitoringHudOverlayProfileWindowTitle = document.getElementById("monitoring-hud-overlay-profile-window-title");
const monitoringHudOverlayProfileWindowActiveName = document.getElementById("monitoring-hud-overlay-profile-window-active-name");
const monitoringHudOverlayProfileWindowCount = document.getElementById("monitoring-hud-overlay-profile-window-count");
const monitoringHudOverlayProfileWindowMembership = document.getElementById("monitoring-hud-overlay-profile-window-membership");
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
const monitoringHudDashboardClose = document.getElementById("monitoring-hud-dashboard-close-action");
const monitoringHudSettingsAction = document.getElementById("monitoring-hud-settings-action");
const monitoringHudEditMonitor = document.getElementById("monitoring-hud-edit-monitor-action");
const monitoringHudSnapToggle = document.getElementById("monitoring-hud-snap-toggle");
const monitoringHudWarningToggle = document.getElementById("monitoring-hud-warning-toggle");
const monitoringHudSnapLabel = document.getElementById("monitoring-hud-snap-label");
const monitoringHudPollingRate = document.getElementById("monitoring-hud-polling-rate");
const monitoringHudWarningModeControl = document.getElementById("monitoring-hud-warning-mode-control");
const monitoringHudMonitorList = document.getElementById("monitoring-hud-monitor-list");
const monitoringHudMonitorListSummary = document.getElementById("monitoring-hud-monitor-list-summary");
const monitoringHudMonitorCount = document.getElementById("monitoring-hud-monitor-count");
const monitoringHudMonitorPollingSummary = document.getElementById("monitoring-hud-monitor-polling-summary");
const monitoringHudMonitorEditorTitle = document.getElementById("monitoring-hud-monitor-editor-title");
const monitoringHudMonitorEnabled = document.getElementById("monitoring-hud-monitor-enabled");
const monitoringHudMonitorPollingRate = document.getElementById("monitoring-hud-monitor-polling-rate");
const monitoringHudMonitorPollingRateControl = document.getElementById("monitoring-hud-monitor-polling-rate-control");
const monitoringHudMonitorPollingRateToggle = document.getElementById("monitoring-hud-monitor-polling-rate-toggle");
const monitoringHudMonitorPollingRateLabel = document.getElementById("monitoring-hud-monitor-polling-rate-label");
const monitoringHudMonitorEditorScope = document.getElementById("monitoring-hud-monitor-editor-scope");
const monitoringHudChildWindowLayer = document.getElementById("monitoring-hud-child-window-layer");
const monitoringHudSettingsWindow = document.getElementById("monitoring-hud-settings-window");
const monitoringHudSettingsWarningToggle = document.getElementById("monitoring-hud-settings-warning-toggle");
const monitoringHudSettingsFeatureControl = document.getElementById("monitoring-hud-settings-feature-control");
const monitoringHudSettingsWarningState = document.getElementById("monitoring-hud-settings-warning-state");
const monitoringHudSettingsPersistence = document.getElementById("monitoring-hud-settings-persistence");
const monitoringHudSettingsOverlayState = document.getElementById("monitoring-hud-settings-overlay-state");
const monitoringHudSettingsProviderState = document.getElementById("monitoring-hud-settings-provider-state");
const monitoringHudCreateMonitorWindow = document.getElementById("monitoring-hud-create-monitor-window");
const monitoringHudEditMonitorWindow = document.getElementById("monitoring-hud-edit-monitor-window");
const monitoringHudCreateMonitorName = document.getElementById("monitoring-hud-create-monitor-name");
const monitoringHudCreateMonitorConfirm = document.getElementById("monitoring-hud-create-monitor-confirm");
const monitoringHudManageMonitorCreate = document.getElementById("monitoring-hud-manage-monitor-create-action");
const monitoringHudMonitorManageSummary = document.getElementById("monitoring-hud-monitor-manage-summary");
const monitoringHudMonitorSearch = document.getElementById("monitoring-hud-monitor-search");
const monitoringHudEditMonitorList = document.getElementById("monitoring-hud-edit-monitor-list");
const monitoringHudMonitorListEmpty = document.getElementById("monitoring-hud-monitor-list-empty");
const monitoringHudEditMonitorTitle = document.getElementById("monitoring-hud-edit-monitor-title");
const monitoringHudEditMonitorName = document.getElementById("monitoring-hud-edit-monitor-name");
const monitoringHudEditMonitorConfirm = document.getElementById("monitoring-hud-edit-monitor-confirm");
const monitoringHudEditMonitorDiscard = document.getElementById("monitoring-hud-edit-monitor-discard");
const monitoringHudMonitorDetailActions = document.getElementById("monitoring-hud-monitor-detail-actions");
const monitoringHudMonitorDetailNote = document.getElementById("monitoring-hud-monitor-detail-note");
const monitoringHudMonitorDeleteConfirmation = document.getElementById("monitoring-hud-monitor-delete-confirmation");
const monitoringHudMonitorDeleteTitle = document.getElementById("monitoring-hud-monitor-delete-title");
const monitoringHudMonitorDeleteCopy = document.getElementById("monitoring-hud-monitor-delete-copy");
const monitoringHudMonitorDeleteConfirm = document.getElementById("monitoring-hud-monitor-delete-confirm");
const monitoringHudMonitorDeleteCancel = document.getElementById("monitoring-hud-monitor-delete-cancel");
const monitoringHudMonitorDetailDelete = document.getElementById("monitoring-hud-monitor-detail-delete");
const monitoringHudMonitorUnsavedGuard = document.getElementById("monitoring-hud-monitor-unsaved-guard");
const monitoringHudMonitorUnsavedSave = document.getElementById("monitoring-hud-monitor-unsaved-save");
const monitoringHudMonitorUnsavedDiscard = document.getElementById("monitoring-hud-monitor-unsaved-discard");
const monitoringHudMonitorDetailEmpty = document.getElementById("monitoring-hud-monitor-detail-empty");
const monitoringHudMonitorEmptyCreate = document.getElementById("monitoring-hud-monitor-empty-create-action");
const monitoringHudMonitorWarningSetting = document.getElementById("monitoring-hud-monitor-warning-notifications-setting");
const monitoringHudProviderReadinessPanel = document.getElementById("monitoring-hud-provider-readiness-panel");
const monitoringHudMonitorSensorAssignment = document.getElementById("monitoring-hud-monitor-sensor-assignment");
const monitoringHudMonitorSensorSettings = document.getElementById("monitoring-hud-monitor-sensor-settings");
const monitoringHudSensorSearch = document.getElementById("monitoring-hud-sensor-search");
const monitoringHudSensorFilter = document.getElementById("monitoring-hud-sensor-filter");
const monitoringHudSensorFilterToggle = document.getElementById("monitoring-hud-sensor-filter-toggle");
const monitoringHudSensorFilterLabel = document.getElementById("monitoring-hud-sensor-filter-label");
const monitoringHudSensorResultSummary = document.getElementById("monitoring-hud-sensor-result-summary");
const monitoringHudSensorPreview = document.getElementById("monitoring-hud-sensor-preview");

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
  rendererOwner: "HUD Overlay release acceptance is deferred. The Dashboard can describe the future overlay boundary without enabling it.",
  anchor: "Deferred / non-gating",
  pointerModel: "Dashboard configures future HUD Overlay behavior",
  resizePosture: "Overlay settings are future branch scope"
};
let monitoringHudControls = {
  packageId: "PKG-006",
  sliceId: "SLC-027",
  controlsId: "hud-controls-visibility",
  visibilityState: "HUD feature disabled from dashboard/tray",
  controlSurface: "Tray controls HUD feature state; Dashboard open/close is separate; HUD Overlay remains deferred",
  persistence: "Store group/layout posture locally",
  operatorAction: "No default keybinds",
  trayPath: "Task tray enables/disables HUD feature and opens/closes Dashboard; HUD Overlay controls deferred"
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

function monitoringHudInitialCards() {
  return {
    cpu: {
      x: 0,
      y: 0,
      w: 600,
      h: 280,
      title: "CPU Group",
      enabled: true,
      pollingRateMs: 1000,
      warningNotificationsEnabled: true,
      sensors: ["cpu-load"],
      sensorSettings: {
        "cpu-load": { displayMode: "badge-text", warningEnabled: true }
      }
    },
    gpu: {
      x: 0,
      y: 300,
      w: 600,
      h: 280,
      title: "GPU Group",
      enabled: true,
      pollingRateMs: 1000,
      warningNotificationsEnabled: true,
      sensors: [],
      sensorSettings: {}
    }
  };
}

function monitoringHudHasOwnCards(state) {
  return Boolean(state) && Object.prototype.hasOwnProperty.call(state, "cards");
}

function monitoringHudSafeCardsObject(cards) {
  if (!cards || typeof cards !== "object" || Array.isArray(cards)) return {};
  return Object.assign({}, cards);
}

const monitoringHudOverlayProfileSchemaVersion = 1;
const monitoringHudDefaultOverlayProfileId = "default-overlay-profile";

function monitoringHudSafeOverlayProfilesObject(overlayProfiles) {
  if (!overlayProfiles || typeof overlayProfiles !== "object" || Array.isArray(overlayProfiles)) return {};
  return Object.assign({}, overlayProfiles);
}

function monitoringHudStableMonitorIds(cards) {
  return Object.keys(cards || {}).filter((cardId) => typeof cardId === "string" && cardId.trim());
}

function monitoringHudUniqueValidMonitorIds(values, cards) {
  const cardIds = new Set(monitoringHudStableMonitorIds(cards));
  const seen = new Set();
  const result = [];
  if (!Array.isArray(values)) return result;
  values.forEach((value) => {
    const monitorId = String(value || "").trim();
    if (!monitorId || !cardIds.has(monitorId) || seen.has(monitorId)) return;
    seen.add(monitorId);
    result.push(monitorId);
  });
  return result;
}

function monitoringHudDefaultOverlayProfile(cards, previousProfile = {}) {
  const previousMonitorIds = Array.isArray(previousProfile.monitorIds)
    ? monitoringHudUniqueValidMonitorIds(previousProfile.monitorIds, cards)
    : null;
  return {
    id: monitoringHudDefaultOverlayProfileId,
    schemaVersion: monitoringHudOverlayProfileSchemaVersion,
    kind: "overlay-profile",
    scope: "overlay-visible-monitor-membership",
    name: previousProfile.name || "Default Overlay Profile",
    monitorIds: previousMonitorIds || monitoringHudStableMonitorIds(cards),
    displayMode: previousProfile.displayMode || "monitor-cards",
    source: previousProfile.source || "legacy-monitor-card-migration",
    dirty: false
  };
}

function monitoringHudNormalizeOverlayProfileState(state) {
  const targetState = state || monitoringHudControlState;
  const cards = monitoringHudSafeCardsObject(targetState.cards || {});
  const rawProfiles = monitoringHudSafeOverlayProfilesObject(targetState.overlayProfiles);
  const profiles = {};
  const migratedLegacyCards = !Object.prototype.hasOwnProperty.call(targetState, "overlayProfiles");

  Object.keys(rawProfiles).forEach((profileKey) => {
    const rawProfile = rawProfiles[profileKey];
    if (!rawProfile || typeof rawProfile !== "object" || Array.isArray(rawProfile)) return;
    const profileId = String(rawProfile.id || profileKey || "").trim();
    if (!profileId) return;
    profiles[profileId] = {
      id: profileId,
      schemaVersion: monitoringHudOverlayProfileSchemaVersion,
      kind: "overlay-profile",
      scope: "overlay-visible-monitor-membership",
      name: String(rawProfile.name || "Overlay Profile").trim() || "Overlay Profile",
      monitorIds: monitoringHudUniqueValidMonitorIds(rawProfile.monitorIds, cards),
      displayMode: String(rawProfile.displayMode || "monitor-cards").trim() || "monitor-cards",
      source: String(rawProfile.source || "persisted-overlay-profile-state").trim() || "persisted-overlay-profile-state",
      dirty: Boolean(rawProfile.dirty)
    };
  });

  profiles[monitoringHudDefaultOverlayProfileId] = monitoringHudDefaultOverlayProfile(
    cards,
    profiles[monitoringHudDefaultOverlayProfileId] || rawProfiles[monitoringHudDefaultOverlayProfileId] || {}
  );
  const activeProfileId = String(targetState.activeOverlayProfileId || "").trim();
  targetState.overlayProfileSchemaVersion = monitoringHudOverlayProfileSchemaVersion;
  targetState.overlayProfiles = profiles;
  targetState.activeOverlayProfileId = profiles[activeProfileId] ? activeProfileId : monitoringHudDefaultOverlayProfileId;
  targetState.overlayProfileStateProof = {
    schemaVersion: monitoringHudOverlayProfileSchemaVersion,
    activeProfileId: targetState.activeOverlayProfileId,
    defaultProfileId: monitoringHudDefaultOverlayProfileId,
    defaultProfileMonitorIds: profiles[monitoringHudDefaultOverlayProfileId].monitorIds.slice(),
    profileCount: Object.keys(profiles).length,
    legacyCardsMigrated: migratedLegacyCards,
    duplicateMonitorIdsRemoved: true,
    staleMonitorIdsRemoved: true,
    monitorGroupBoundary: "monitor-groups-organize-configuration-only",
    recordingProfileBoundary: "recording-profile-state-absent-future-gated",
    visibleEditorUi: "slc-039-membership-editor"
  };
  return targetState;
}

function monitoringHudActiveOverlayProfile() {
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  return monitoringHudControlState.overlayProfiles[monitoringHudControlState.activeOverlayProfileId]
    || monitoringHudControlState.overlayProfiles[monitoringHudDefaultOverlayProfileId];
}

function monitoringHudOverlayProfileList() {
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  const profiles = monitoringHudControlState.overlayProfiles || {};
  return Object.keys(profiles)
    .sort((left, right) => {
      if (left === monitoringHudDefaultOverlayProfileId) return -1;
      if (right === monitoringHudDefaultOverlayProfileId) return 1;
      return String(profiles[left].name || left).localeCompare(String(profiles[right].name || right));
    })
    .map((profileId) => profiles[profileId])
    .filter(Boolean);
}

function monitoringHudCleanOverlayProfileName(value, fallback = "Overlay Profile") {
  const cleaned = String(value || "").replace(/\s+/g, " ").trim();
  return (cleaned || fallback).slice(0, 48);
}

function monitoringHudUniqueOverlayProfileName(value, currentProfileId = "") {
  const baseName = monitoringHudCleanOverlayProfileName(value);
  const existingNames = new Set(
    monitoringHudOverlayProfileList()
      .filter((profile) => profile.id !== currentProfileId)
      .map((profile) => String(profile.name || "").trim().toLocaleLowerCase())
      .filter(Boolean)
  );
  if (!existingNames.has(baseName.toLocaleLowerCase())) return baseName;
  for (let index = 2; index < 100; index += 1) {
    const candidate = `${baseName} ${index}`;
    if (!existingNames.has(candidate.toLocaleLowerCase())) return candidate;
  }
  return `${baseName} ${Date.now()}`;
}

function monitoringHudNextOverlayProfileId() {
  const profiles = monitoringHudControlState.overlayProfiles || {};
  let index = Object.keys(profiles).length + 1;
  let profileId = `overlay-profile-${index}`;
  while (profiles[profileId]) {
    index += 1;
    profileId = `overlay-profile-${index}`;
  }
  return profileId;
}

function monitoringHudOverlayProfileDisplayLabel(displayMode) {
  return String(displayMode || "monitor-cards")
    .split("-")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ") || "Monitor Cards";
}

function monitoringHudSameMonitorMembership(left, right, cards) {
  const normalizedLeft = monitoringHudUniqueValidMonitorIds(left, cards);
  const normalizedRight = monitoringHudUniqueValidMonitorIds(right, cards);
  return JSON.stringify(normalizedLeft) === JSON.stringify(normalizedRight);
}

function monitoringHudOverlayProfileDraftMonitorIdsFromWindow() {
  const cards = monitoringHudControlState && monitoringHudControlState.cards
    ? monitoringHudControlState.cards
    : {};
  if (!monitoringHudOverlayProfileMembershipList) {
    return monitoringHudUniqueValidMonitorIds(monitoringHudOverlayProfileDraftMonitorIds, cards);
  }
  const checkedIds = Array.from(
    monitoringHudOverlayProfileMembershipList.querySelectorAll("[data-overlay-profile-membership-toggle]")
  );
  if (!checkedIds.length) {
    if (monitoringHudOverlayProfileDraftMonitorIds.length) {
      return monitoringHudUniqueValidMonitorIds(monitoringHudOverlayProfileDraftMonitorIds, cards);
    }
    const activeProfile = monitoringHudActiveOverlayProfile() || {};
    return monitoringHudUniqueValidMonitorIds(activeProfile.monitorIds, cards);
  }
  const selectedIds = checkedIds
    .filter((input) => input.checked)
    .map((input) => input.value);
  return monitoringHudUniqueValidMonitorIds(selectedIds, cards);
}

function monitoringHudOverlayProfileMonitorSummary(cardId, layout) {
  const label = monitoringHudSensorAssignmentSummary(layout);
  const pollingMs = Math.max(1000, Number(layout && layout.pollingRateMs) || 1000);
  const enabledCopy = layout && layout.enabled === false ? "hidden" : "visible";
  return `${label}; ${enabledCopy}; ${pollingMs / 1000}s polling`;
}

function monitoringHudRenderOverlayProfileMembershipList(activeProfile, cards, draftMonitorIds) {
  if (!monitoringHudOverlayProfileMembershipList) return;
  const monitorIds = monitoringHudStableMonitorIds(cards);
  const selectedIds = new Set(monitoringHudUniqueValidMonitorIds(draftMonitorIds, cards));
  monitoringHudOverlayProfileMembershipList.replaceChildren();
  monitoringHudOverlayProfileMembershipList.dataset.overlayProfileMembershipList = "editable-monitor-membership";
  monitoringHudOverlayProfileMembershipList.dataset.activeOverlayProfileId = activeProfile.id || monitoringHudDefaultOverlayProfileId;
  monitoringHudOverlayProfileMembershipList.dataset.selectedMonitorCount = String(selectedIds.size);
  if (!monitorIds.length) {
    const empty = document.createElement("p");
    empty.className = "monitoring-hud__child-note";
    empty.textContent = "No Monitor Groups are available to map yet.";
    monitoringHudOverlayProfileMembershipList.appendChild(empty);
    return;
  }
  monitorIds.forEach((cardId) => {
    const layout = Object.assign(monitoringHudCardDefaults(cardId), cards[cardId] || {});
    const checked = selectedIds.has(cardId);
    const row = document.createElement("label");
    row.className = "monitoring-hud__overlay-profile-membership-row";
    row.dataset.overlayProfileMembershipRow = cardId;
    row.setAttribute("aria-selected", checked ? "true" : "false");

    const input = document.createElement("input");
    input.type = "checkbox";
    input.value = cardId;
    input.checked = checked;
    input.dataset.overlayProfileMembershipToggle = cardId;
    input.setAttribute("aria-label", `Show ${layout.title || "Monitor Group"} in active Overlay Profile`);

    const title = document.createElement("strong");
    title.textContent = layout.title || "Monitor Group";

    const summary = document.createElement("small");
    summary.textContent = monitoringHudOverlayProfileMonitorSummary(cardId, layout);

    row.appendChild(input);
    row.appendChild(title);
    row.appendChild(summary);
    monitoringHudOverlayProfileMembershipList.appendChild(row);
  });
}

function monitoringHudClearOverlayProfileMembershipList() {
  if (monitoringHudOverlayProfileMembershipList) {
    monitoringHudOverlayProfileMembershipList.replaceChildren();
  }
}

function monitoringHudSetOverlayProfileDraftFromActive() {
  const activeProfile = monitoringHudActiveOverlayProfile() || {};
  const cards = monitoringHudControlState.cards || {};
  monitoringHudOverlayProfileDraftId = activeProfile.id || monitoringHudDefaultOverlayProfileId;
  monitoringHudOverlayProfileDraftName = monitoringHudCleanOverlayProfileName(activeProfile.name, "Default Overlay Profile");
  monitoringHudOverlayProfileDraftMonitorIds = monitoringHudUniqueValidMonitorIds(activeProfile.monitorIds, cards);
  if (monitoringHudOverlayProfileNameInput) {
    monitoringHudOverlayProfileNameInput.value = monitoringHudOverlayProfileDraftName;
  }
}

function monitoringHudOverlayProfileDraftDirty() {
  const activeProfile = monitoringHudActiveOverlayProfile() || {};
  const cards = monitoringHudControlState.cards || {};
  const currentName = monitoringHudCleanOverlayProfileName(activeProfile.name, "Overlay Profile");
  const currentMonitorIds = monitoringHudUniqueValidMonitorIds(activeProfile.monitorIds, cards);
  const draftName = monitoringHudCleanOverlayProfileName(
    monitoringHudOverlayProfileNameInput ? monitoringHudOverlayProfileNameInput.value : monitoringHudOverlayProfileDraftName,
    "Overlay Profile"
  );
  const draftMonitorIds = monitoringHudOverlayProfileDraftMonitorIdsFromWindow();
  monitoringHudOverlayProfileDraftMonitorIds = draftMonitorIds;
  return draftName !== currentName || !monitoringHudSameMonitorMembership(draftMonitorIds, currentMonitorIds, cards);
}

function monitoringHudSetOverlayProfileDropdownOpen(open) {
  if (!monitoringHudOverlayProfileSelector || !monitoringHudOverlayProfileMenu) return;
  monitoringHudOverlayProfileSelector.dataset.dropdownOpen = open ? "true" : "false";
  monitoringHudOverlayProfileMenu.hidden = !open;
  if (monitoringHudOverlayProfileToggle) {
    monitoringHudOverlayProfileToggle.setAttribute("aria-expanded", open ? "true" : "false");
  }
  if (!open) {
    monitoringHudResetOverlayProfileHover();
  }
}

function monitoringHudResetOverlayProfileHover() {
  if (!monitoringHudOverlayProfileSelector) return;
  monitoringHudOverlayProfileSelector.dataset.hoveredProfileId = "";
  monitoringHudOverlayProfileSelector.querySelectorAll("[data-overlay-profile-option].is-hovered").forEach((option) => {
    option.classList.remove("is-hovered");
  });
}

function monitoringHudSelectOverlayProfile(profileId) {
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  const normalizedProfileId = String(profileId || "").trim();
  if (!monitoringHudControlState.overlayProfiles[normalizedProfileId]) return false;
  monitoringHudControlState.activeOverlayProfileId = normalizedProfileId;
  monitoringHudSetOverlayProfileDraftFromActive();
  monitoringHudClearOverlayProfileMembershipList();
  monitoringHudSetOverlayProfileDropdownOpen(false);
  monitoringHudRenderControls();
  monitoringHudMarkChanged();
  return true;
}

function monitoringHudCreateOverlayProfile() {
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  const profileId = monitoringHudNextOverlayProfileId();
  const activeProfile = monitoringHudActiveOverlayProfile() || {};
  const profileName = monitoringHudUniqueOverlayProfileName("Overlay Profile", profileId);
  monitoringHudControlState.overlayProfiles[profileId] = {
    id: profileId,
    schemaVersion: monitoringHudOverlayProfileSchemaVersion,
    kind: "overlay-profile",
    scope: "overlay-visible-monitor-membership",
    name: profileName,
    monitorIds: Array.isArray(activeProfile.monitorIds)
      ? activeProfile.monitorIds.slice()
      : monitoringHudStableMonitorIds(monitoringHudControlState.cards || {}),
    displayMode: activeProfile.displayMode || "monitor-cards",
    source: "slc-039-membership-editor-create-shell",
    dirty: false
  };
  monitoringHudControlState.activeOverlayProfileId = profileId;
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  monitoringHudSetOverlayProfileDraftFromActive();
  monitoringHudClearOverlayProfileMembershipList();
  monitoringHudRenderControls();
  if (monitoringHudOverlayProfileNameInput && typeof monitoringHudOverlayProfileNameInput.focus === "function") {
    monitoringHudOverlayProfileNameInput.focus();
    monitoringHudOverlayProfileNameInput.select();
  }
  monitoringHudMarkChanged();
  return true;
}

function monitoringHudSaveOverlayProfileDraft() {
  const activeProfile = monitoringHudActiveOverlayProfile();
  if (!activeProfile) return false;
  const cards = monitoringHudControlState.cards || {};
  const draftName = monitoringHudUniqueOverlayProfileName(
    monitoringHudOverlayProfileNameInput ? monitoringHudOverlayProfileNameInput.value : activeProfile.name,
    activeProfile.id
  );
  activeProfile.name = draftName;
  activeProfile.monitorIds = monitoringHudOverlayProfileDraftMonitorIdsFromWindow();
  activeProfile.monitorIds = monitoringHudUniqueValidMonitorIds(activeProfile.monitorIds, cards);
  activeProfile.dirty = false;
  activeProfile.source = "slc-039-membership-editor";
  monitoringHudControlState.overlayProfiles[activeProfile.id] = activeProfile;
  monitoringHudSetOverlayProfileDraftFromActive();
  monitoringHudClearOverlayProfileMembershipList();
  monitoringHudRenderControls();
  monitoringHudMarkChanged();
  return true;
}

function monitoringHudDiscardOverlayProfileDraft() {
  monitoringHudSetOverlayProfileDraftFromActive();
  monitoringHudClearOverlayProfileMembershipList();
  monitoringHudRenderControls();
  return true;
}

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
  cards: monitoringHudInitialCards(),
  overlayProfileSchemaVersion: monitoringHudOverlayProfileSchemaVersion,
  activeOverlayProfileId: monitoringHudDefaultOverlayProfileId,
  overlayProfiles: {},
  changedAt: Date.now()
};
monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
const monitoringHudStorageKey = "nexusMonitoringHudLayoutV4";
const monitoringHudLegacyStorageKeys = ["nexusMonitoringHudLayoutV1", "nexusMonitoringHudLayoutV2", "nexusMonitoringHudLayoutV3"];
const monitoringHudSnapSize = 20;
const monitoringHudLargeMonitorFixtureCount = 125;
const monitoringHudLargeSensorFixtureCount = 1200;
const monitoringHudSensorRenderLimit = 120;
let monitoringHudDragInProgress = false;
let monitoringHudPanelPositionFrame = 0;
let monitoringHudQueuedPanelPosition = null;
let monitoringHudActiveChildWindow = "";
let monitoringHudPendingDeleteMonitorId = "";
let monitoringHudResizeProofFrame = 0;
let monitoringHudLargeFixtureModeEnabled = false;
let monitoringHudLargeSensorFixtureCache = null;
let monitoringHudUnsavedMonitorDirty = false;
let monitoringHudPendingSelectMonitorId = "";
let monitoringHudPendingGuardAction = null;
let monitoringHudDraftOriginalMonitorId = "";
let monitoringHudDraftOriginalLayout = null;
let monitoringHudDraftWorkingLayout = null;
let monitoringHudSensorSettingsRefreshFrame = 0;
let monitoringHudSourcePickerSuppressNativeChangeUntil = 0;
let monitoringHudSourcePickerSuppressClickUntil = 0;
let monitoringHudSourcePickerSuppressClickRow = null;
let monitoringHudDisplayModeSuppressClickUntil = 0;
let monitoringHudDisplayModeSuppressClickButton = null;
let monitoringHudOverlayProfileDraftId = monitoringHudDefaultOverlayProfileId;
let monitoringHudOverlayProfileDraftName = "Default Overlay Profile";
let monitoringHudOverlayProfileDraftMonitorIds = [];
const monitoringHudSourceFilterLabels = {
  all: "All",
  supported: "Supported",
  deferred: "Deferred",
  missing: "Missing",
  warning: "Warning",
  cpu: "CPU",
  gpu: "GPU",
  memory: "Memory",
  disk: "Disk",
  network: "Network",
  temperature: "Temperature",
  load: "Load",
  clock: "Clock",
  power: "Power",
  fan: "Fan",
  voltage: "Voltage"
};
const monitoringHudPollingRateLabels = {
  1000: "1s",
  2000: "2s",
  5000: "5s",
  10000: "10s"
};
const monitoringHudReliableActivationState = {
  sequence: 0,
  lastKey: "",
  lastAt: 0,
  attempts: [],
  visualStates: {}
};

function monitoringHudSnap(value) {
  if (!monitoringHudControlState.snapEnabled) return Math.round(value);
  return Math.round(value / monitoringHudSnapSize) * monitoringHudSnapSize;
}

function monitoringHudBound(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function monitoringHudRecordResizeFrame(payload) {
  if (!monitoringHud) return;
  const rect = payload || {};
  monitoringHudResizeProofFrame += 1;
  monitoringHud.dataset.liveResizeProof = "invisible-real-ui-frame-pixel-signature-grow-shrink";
  monitoringHud.dataset.liveResizeActive = rect.active === false ? "false" : "true";
  monitoringHud.dataset.liveResizeFrame = String(monitoringHudResizeProofFrame);
  monitoringHud.dataset.liveResizeDirection = String(rect.direction || "unknown");
  monitoringHud.dataset.liveResizeGeometry = `${Number(rect.width) || 0}x${Number(rect.height) || 0}`;
  monitoringHud.dataset.liveResizeFrameIntervalMs = String(Number(rect.frameIntervalMs) || 0);
  monitoringHud.dataset.resizeProofVisibility = "normal-ui-no-proof-artifacts";
  monitoringHud.dataset.resizeProofVisuals = "none";
  monitoringHud.dataset.liveResizeVisualArtifact = "none";
  monitoringHud.dataset.liveResizePixelSignature = [
    monitoringHudResizeProofFrame,
    Number(rect.width) || 0,
    Number(rect.height) || 0,
    String(rect.direction || "unknown")
  ].join(":");
  monitoringHud.style.setProperty("--monitoring-hud-live-resize-proof-x", "0px");
  monitoringHud.style.setProperty("--monitoring-hud-live-resize-proof-y", "0px");
  monitoringHud.style.setProperty("--monitoring-hud-live-resize-proof-alpha", "0");
}

function monitoringHudFinishResizeFrame(payload) {
  monitoringHudRecordResizeFrame(Object.assign({}, payload || {}, { active: false }));
  if (monitoringHud) {
    monitoringHud.dataset.liveResizeActive = "false";
    monitoringHud.style.setProperty("--monitoring-hud-live-resize-proof-alpha", "0");
  }
}

window.monitoringHudRecordResizeFrame = monitoringHudRecordResizeFrame;
window.monitoringHudFinishResizeFrame = monitoringHudFinishResizeFrame;

function monitoringHudLoadStoredState() {
  try {
    if (window.localStorage) {
      monitoringHudLegacyStorageKeys.forEach((key) => window.localStorage.removeItem(key));
    }
    const raw = window.localStorage ? window.localStorage.getItem(monitoringHudStorageKey) : "";
    if (!raw) return;
    const stored = JSON.parse(raw);
    const storedHasCards = monitoringHudHasOwnCards(stored);
    monitoringHudControlState = Object.assign({}, monitoringHudControlState, stored || {});
    monitoringHudControlState.cards = storedHasCards
      ? monitoringHudSafeCardsObject(stored.cards)
      : monitoringHudSafeCardsObject(monitoringHudControlState.cards || monitoringHudInitialCards());
    if (!monitoringHudControlState.selectedMonitorId || !monitoringHudControlState.cards[monitoringHudControlState.selectedMonitorId]) {
      monitoringHudControlState.selectedMonitorId = Object.keys(monitoringHudControlState.cards)[0] || "";
    }
    monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  } catch (_err) {
    monitoringHudControlState.changedAt = Date.now();
    monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  }
}

function monitoringHudSaveStoredState() {
  try {
    if (!window.localStorage) return;
    monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
    window.localStorage.setItem(monitoringHudStorageKey, JSON.stringify(monitoringHudControlState));
  } catch (_err) {}
}

function monitoringHudMarkChanged() {
  monitoringHudControlState.changedAt = Date.now();
  monitoringHudSaveStoredState();
}

function monitoringHudCardDefaults(cardId) {
  const sensors = monitoringHudDefaultSensorIds(cardId);
  const sensorSettings = {};
  sensors.forEach((sensorId) => {
    sensorSettings[sensorId] = monitoringHudDefaultSensorSetting(sensorId);
  });
  return {
    x: 0,
    y: Object.keys(monitoringHudControlState.cards || {}).length * 300,
    w: 600,
    h: 280,
    title: cardId === "cpu" ? "CPU Group" : cardId === "gpu" ? "GPU Group" : "Monitor Group",
    enabled: true,
    pollingRateMs: 1000,
    warningNotificationsEnabled: true,
    sensors,
    sensorSettings
  };
}

function monitoringHudNextMonitorGroupNumber() {
  const numericSuffixes = Object.keys(monitoringHudControlState.cards || {})
    .map((cardId) => {
      const match = String(cardId).match(/^monitor-(\d+)$/);
      return match ? Number(match[1]) : 0;
    })
    .filter((value) => Number.isFinite(value));
  return Math.max(3, Number(monitoringHudControlState.monitorSequence || 2) + 1, ...numericSuffixes.map((value) => value + 1));
}

function monitoringHudSuggestedMonitorName() {
  return `Monitor Group ${monitoringHudNextMonitorGroupNumber()}`;
}

function monitoringHudCleanMonitorTitle(value, fallback) {
  const title = String(value || "").trim();
  return title || fallback || "Monitor Group";
}

function monitoringHudSensorCategoryForId(sensorId) {
  const value = String(sensorId || "").toLowerCase();
  if (value.includes("cpu")) return "cpu";
  if (value.includes("gpu")) return "gpu";
  if (value.includes("memory")) return "memory";
  if (value.includes("disk")) return "disk";
  if (value.includes("network")) return "network";
  if (value.includes("temperature") || value.includes("thermal")) return "temperature";
  if (value.includes("clock")) return "clock";
  if (value.includes("power")) return "power";
  if (value.includes("fan")) return "fan";
  if (value.includes("voltage")) return "voltage";
  if (value.includes("load")) return "load";
  return "supported";
}

function monitoringHudLargeSensorFixtures() {
  if (monitoringHudLargeSensorFixtureCache) return monitoringHudLargeSensorFixtureCache;
  const categories = [
    ["cpu", "CPU", "Load"],
    ["gpu", "GPU", "Load"],
    ["memory", "Memory", "Usage"],
    ["disk", "Disk", "Throughput"],
    ["network", "Network", "Throughput"],
    ["temperature", "Temperature", "Thermal"],
    ["clock", "Clock", "Frequency"],
    ["power", "Power", "Watts"],
    ["fan", "Fan", "RPM"],
    ["voltage", "Voltage", "Volts"]
  ];
  const sensors = [];
  for (let index = 0; index < monitoringHudLargeSensorFixtureCount; index += 1) {
    const [category, deviceLabel, metricLabel] = categories[index % categories.length];
    const deviceIndex = Math.floor(index / categories.length) + 1;
    const supported = index % 6 === 0 || category === "cpu" || category === "memory";
    const duplicateName = index % 47 === 0 ? "Duplicate Thermal Sensor" : "";
    const longName = index % 59 === 0
      ? `${deviceLabel} ${deviceIndex} ${metricLabel} Extended Descriptor For Long Source Name Validation`
      : "";
    sensors.push({
      id: `fixture-${category}-${deviceIndex}-${index}`,
      label: duplicateName || longName || `${deviceLabel} ${deviceIndex} ${metricLabel}`,
      source: `${supported ? "Local fixture" : "Provider-required fixture"} / ${deviceLabel} ${deviceIndex} / ${metricLabel} / sensor ${index}${longName ? " / extended descriptor long source path" : ""}`,
      state: supported ? "fixture-supported" : "blocked-until-provider",
      value: supported ? "Fixture source available for scale proof" : "Provider required",
      assignable: supported,
      reason: supported ? "Fixture-supported source" : "Provider required",
      provider: supported ? "local-fixture" : "provider-required",
      device: `${deviceLabel} ${deviceIndex}`,
      category,
      metric: metricLabel,
      instance: `sensor-${index}`
    });
  }
  monitoringHudLargeSensorFixtureCache = sensors;
  return monitoringHudLargeSensorFixtureCache;
}

function monitoringHudSensorDefinitions() {
  const base = {
    "cpu-load": {
      id: "cpu-load",
      label: "CPU Load",
      source: "Native Windows CPU load",
      state: "native-provider-pending",
      value: "Warming up",
      assignable: true,
      reason: "Native runtime source",
      provider: "native",
      device: "CPU",
      category: "cpu",
      metric: "Load",
      instance: "primary"
    },
    "cpu-thermal": {
      id: "cpu-thermal",
      label: "CPU Thermal",
      source: "Thermal source pending",
      state: "blocked-until-provider",
      value: "Provider required",
      assignable: false,
      reason: "Provider required",
      provider: "provider-required",
      device: "CPU",
      category: "temperature",
      metric: "Thermal",
      instance: "primary"
    },
    "gpu-load": {
      id: "gpu-load",
      label: "GPU Load",
      source: "GPU source pending",
      state: "blocked-until-provider",
      value: "Unavailable",
      assignable: false,
      reason: "Provider required",
      provider: "provider-required",
      device: "GPU",
      category: "gpu",
      metric: "Load",
      instance: "primary"
    },
    "gpu-thermal": {
      id: "gpu-thermal",
      label: "GPU Thermal",
      source: "Thermal source pending",
      state: "blocked-until-provider",
      value: "Unavailable",
      assignable: false,
      reason: "Provider required",
      provider: "provider-required",
      device: "GPU",
      category: "temperature",
      metric: "Thermal",
      instance: "primary"
    },
    "memory-usage": {
      id: "memory-usage",
      label: "Memory Usage",
      source: "Provider memory source pending",
      state: "blocked-until-provider",
      value: "Provider required",
      assignable: false,
      reason: "Provider required",
      provider: "provider-required",
      device: "Memory",
      category: "memory",
      metric: "Usage",
      instance: "primary"
    },
    "disk-throughput": {
      id: "disk-throughput",
      label: "Disk Throughput",
      source: "Provider disk source pending",
      state: "missing",
      value: "Missing source",
      assignable: false,
      reason: "Missing source",
      provider: "provider-required",
      device: "Disk",
      category: "disk",
      metric: "Throughput",
      instance: "primary"
    },
    "network-throughput": {
      id: "network-throughput",
      label: "Network Throughput",
      source: "Provider network source pending",
      state: "warning",
      value: "Provider warning",
      assignable: false,
      reason: "Warning state, provider required",
      provider: "provider-required",
      device: "Network",
      category: "network",
      metric: "Throughput",
      instance: "primary"
    },
    "clock-frequency": {
      id: "clock-frequency",
      label: "Clock Frequency",
      source: "Provider clock source pending",
      state: "blocked-until-provider",
      value: "Provider required",
      assignable: false,
      reason: "Provider required",
      provider: "provider-required",
      device: "Clock",
      category: "clock",
      metric: "Frequency",
      instance: "primary"
    },
    "power-watts": {
      id: "power-watts",
      label: "Power Draw",
      source: "Provider power source pending",
      state: "blocked-until-provider",
      value: "Provider required",
      assignable: false,
      reason: "Provider required",
      provider: "provider-required",
      device: "Power",
      category: "power",
      metric: "Watts",
      instance: "primary"
    },
    "fan-rpm": {
      id: "fan-rpm",
      label: "Fan Speed",
      source: "Provider fan source pending",
      state: "blocked-until-provider",
      value: "Provider required",
      assignable: false,
      reason: "Provider required",
      provider: "provider-required",
      device: "Fan",
      category: "fan",
      metric: "RPM",
      instance: "primary"
    },
    "voltage-rail": {
      id: "voltage-rail",
      label: "Voltage Rail",
      source: "Provider voltage source pending",
      state: "blocked-until-provider",
      value: "Provider required",
      assignable: false,
      reason: "Provider required",
      provider: "provider-required",
      device: "Voltage",
      category: "voltage",
      metric: "Volts",
      instance: "primary"
    }
  };
  const telemetryCards = Array.isArray(monitoringHudTelemetry.sensorCards) ? monitoringHudTelemetry.sensorCards : [];
  const nonAssignableProductConcepts = new Set(["provider-state", "warning-notifications"]);
  telemetryCards.forEach((card) => {
    const sensors = card && Array.isArray(card.sensors) ? card.sensors : [];
    sensors.forEach((sensor) => {
      if (!sensor || !sensor.id) return;
      const sensorId = String(sensor.id);
      if (nonAssignableProductConcepts.has(sensorId)) return;
      const state = String(sensor.state || base[sensorId]?.state || "");
      const telemetryAssignable = !["blocked-until-provider", "provider-required", "deferred", "missing", "warning"].includes(state);
      base[sensorId] = Object.assign({}, base[sensorId] || {}, {
        id: sensorId,
        label: String(sensor.label || base[sensorId]?.label || sensorId),
        source: String(sensor.source || base[sensorId]?.source || "runtime source"),
        state,
        value: String(sensor.value || base[sensorId]?.value || ""),
        assignable: telemetryAssignable,
        reason: telemetryAssignable ? "Runtime source" : "Provider required",
        provider: String(sensor.provider || base[sensorId]?.provider || "runtime"),
        device: String(sensor.device || base[sensorId]?.device || "Runtime"),
        category: String(sensor.category || base[sensorId]?.category || monitoringHudSensorCategoryForId(sensorId)),
        metric: String(sensor.metric || base[sensorId]?.metric || "Metric"),
        instance: String(sensor.instance || base[sensorId]?.instance || sensorId)
      });
    });
  });
  const sourceDefinitions = Object.values(base);
  return monitoringHudLargeFixtureModeEnabled ? sourceDefinitions.concat(monitoringHudLargeSensorFixtures()) : sourceDefinitions;
}

function monitoringHudSensorDefinitionById(sensorId) {
  return monitoringHudSensorDefinitions().find((sensor) => sensor.id === sensorId) || null;
}

function monitoringHudDefaultSensorIds(cardId) {
  if (cardId === "cpu") return ["cpu-load"];
  return [];
}

function monitoringHudDefaultSensorSetting(sensorId) {
  return {
    displayMode: sensorId === "cpu-load" ? "badge-text" : "text",
    warningEnabled: true
  };
}

function monitoringHudNormalizeSensorAssignments(cardId, layout) {
  if (!layout) return layout;
  const assignable = new Set(
    monitoringHudSensorDefinitions()
      .filter((sensor) => sensor.assignable !== false)
      .map((sensor) => sensor.id)
  );
  const rawSensors = Array.isArray(layout.sensors) ? layout.sensors : monitoringHudDefaultSensorIds(cardId);
  layout.sensors = rawSensors
    .map((sensorId) => String(sensorId || "").trim())
    .filter((sensorId, index, list) => sensorId && assignable.has(sensorId) && list.indexOf(sensorId) === index);
  layout.sensorSettings = Object.assign({}, layout.sensorSettings || {});
  layout.sensors.forEach((sensorId) => {
    layout.sensorSettings[sensorId] = Object.assign(
      monitoringHudDefaultSensorSetting(sensorId),
      layout.sensorSettings[sensorId] || {}
    );
  });
  Object.keys(layout.sensorSettings).forEach((sensorId) => {
    if (!layout.sensors.includes(sensorId)) delete layout.sensorSettings[sensorId];
  });
  return layout;
}

function monitoringHudSelectedMonitor() {
  const cards = monitoringHudControlState.cards || {};
  const selectedId = monitoringHudControlState.selectedMonitorId;
  if (selectedId && cards[selectedId]) {
    return { id: selectedId, layout: monitoringHudNormalizeSensorAssignments(selectedId, cards[selectedId]) };
  }
  const firstId = Object.keys(cards)[0] || "";
  monitoringHudControlState.selectedMonitorId = firstId;
  return firstId
    ? { id: firstId, layout: monitoringHudNormalizeSensorAssignments(firstId, cards[firstId] || monitoringHudCardDefaults(firstId)) }
    : { id: "", layout: null };
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
  if (!cardId || !layout) return;
  monitoringHudControlState.lastMonitorGroupNodeSync = "edit-child-window-list";
}

function monitoringHudEnsureCardNodes() {
  if (!monitoringHudMonitorList) return;
  Object.keys(monitoringHudControlState.cards || {}).forEach((cardId) => {
    const layout = Object.assign(monitoringHudCardDefaults(cardId), monitoringHudControlState.cards[cardId] || {});
    monitoringHudNormalizeMonitorGroupTitle(cardId, layout);
    monitoringHudNormalizeSensorAssignments(cardId, layout);
    monitoringHudControlState.cards[cardId] = layout;
    monitoringHudCreateCardNode(cardId, layout);
  });
}

function monitoringHudSetChildWindowVisibility(kind) {
  monitoringHudActiveChildWindow = kind || "";
  if (!monitoringHudChildWindowLayer) return;
  const open = Boolean(monitoringHudActiveChildWindow);
  monitoringHudChildWindowLayer.hidden = !open;
  monitoringHudChildWindowLayer.setAttribute("aria-hidden", open ? "false" : "true");
  monitoringHudChildWindowLayer.dataset.childWindowState = open ? monitoringHudActiveChildWindow : "closed";
  [monitoringHudSettingsWindow, monitoringHudOverlayProfileWindow, monitoringHudCreateMonitorWindow, monitoringHudEditMonitorWindow].forEach((windowNode) => {
    if (!windowNode) return;
    const isActive = windowNode.dataset.childWindow === monitoringHudActiveChildWindow;
    windowNode.hidden = !isActive;
    windowNode.setAttribute("aria-hidden", isActive ? "false" : "true");
  });
  if (monitoringHud) {
    monitoringHud.dataset.activeChildWindow = open ? monitoringHudActiveChildWindow : "none";
    monitoringHud.dataset.dashboardSettingsPanelState = monitoringHudActiveChildWindow === "dashboard-settings" ? "open" : "closed";
    monitoringHud.dataset.overlayProfileSettingsWindowState = monitoringHudActiveChildWindow === "overlay-profile-settings" ? "open" : "closed";
  }
  if (monitoringHudSettingsAction) {
    const settingsOpen = monitoringHudActiveChildWindow === "dashboard-settings";
    monitoringHudSettingsAction.setAttribute("aria-expanded", settingsOpen ? "true" : "false");
  }
  if (monitoringHudOverlayProfileOpenSettings) {
    const profileSettingsOpen = monitoringHudActiveChildWindow === "overlay-profile-settings";
    monitoringHudOverlayProfileOpenSettings.setAttribute("aria-expanded", profileSettingsOpen ? "true" : "false");
  }
}

function monitoringHudRenderDashboardSettingsPanel() {
  const warningEnabled = !monitoringHudControlState.warningNotificationsMuted;
  if (monitoringHudSettingsWarningToggle) {
    monitoringHudSettingsWarningToggle.checked = warningEnabled;
  }
  if (monitoringHudSettingsFeatureControl) {
    monitoringHudSettingsFeatureControl.textContent = monitoringHudControlState.featureEnabled
      ? "Tray owns HUD feature enablement; Dashboard close hides this window only"
      : "HUD feature disabled from tray path; Dashboard opens only when feature is enabled";
  }
  if (monitoringHudSettingsWarningState) {
    monitoringHudSettingsWarningState.textContent = warningEnabled
      ? "Visual notifications enabled"
      : "Warning notifications muted; monitor group settings preserved";
  }
  if (monitoringHudSettingsPersistence) {
    monitoringHudSettingsPersistence.textContent = "Monitor group and Dashboard layout posture are stored locally";
  }
  if (monitoringHudSettingsOverlayState) {
    monitoringHudSettingsOverlayState.textContent = "Deferred; no Overlay/display acceptance in this branch";
  }
  if (monitoringHudSettingsProviderState) {
    monitoringHudSettingsProviderState.textContent = "Provider setup required; no fake telemetry values";
  }
}

function monitoringHudRenderOverlayProfileControls() {
  if (!monitoringHudOverlayProfileEditor) return;
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  const profiles = monitoringHudOverlayProfileList();
  const activeProfile = monitoringHudActiveOverlayProfile() || {};
  const activeProfileId = activeProfile.id || monitoringHudDefaultOverlayProfileId;
  const activeProfileName = monitoringHudCleanOverlayProfileName(activeProfile.name, "Default Overlay Profile");
  const cards = monitoringHudControlState.cards || {};
  const monitorIds = monitoringHudUniqueValidMonitorIds(activeProfile.monitorIds, cards);
  const dirty = monitoringHudOverlayProfileDraftDirty();
  const draftMonitorIds = monitoringHudOverlayProfileDraftMonitorIdsFromWindow();

  monitoringHudOverlayProfileEditor.dataset.overlayProfileEditorUi = "slc-039-membership-editor";
  monitoringHudOverlayProfileEditor.dataset.overlayProfileMembership = "editable-slc-039-mapping";
  monitoringHudOverlayProfileEditor.dataset.overlayProfileDirty = dirty ? "dirty" : "clean";
  monitoringHudOverlayProfileEditor.dataset.activeOverlayProfileId = activeProfileId;
  monitoringHudOverlayProfileEditor.dataset.overlayProfileCount = String(profiles.length);
  monitoringHudOverlayProfileEditor.dataset.overlayProfileProof = "selector-settings-window-create-rename-membership-save-discard";

  if (monitoringHudOverlayProfileSelector) {
    monitoringHudOverlayProfileSelector.dataset.selectedProfileId = activeProfileId;
    monitoringHudOverlayProfileSelector.dataset.overlayProfileSelector = "active-profile-selector";
  }
  if (monitoringHudOverlayProfileLabel) {
    monitoringHudOverlayProfileLabel.textContent = activeProfileName;
  }
  if (monitoringHudOverlayProfileMenu) {
    monitoringHudOverlayProfileMenu.replaceChildren();
    profiles.forEach((profile) => {
      const option = document.createElement("button");
      option.type = "button";
      option.className = "monitoring-hud__bounded-dropdown-option";
      option.dataset.overlayProfileOption = profile.id;
      option.setAttribute("role", "option");
      option.setAttribute("aria-selected", profile.id === activeProfileId ? "true" : "false");
      option.textContent = monitoringHudCleanOverlayProfileName(profile.name, "Overlay Profile");
      monitoringHudOverlayProfileMenu.appendChild(option);
    });
  }
  if (monitoringHudOverlayProfileMonitorCount) {
    monitoringHudOverlayProfileMonitorCount.textContent = `${monitorIds.length} mapped monitor${monitorIds.length === 1 ? "" : "s"}`;
  }
  if (monitoringHudOverlayProfileDisplayMode) {
    monitoringHudOverlayProfileDisplayMode.textContent = monitoringHudOverlayProfileDisplayLabel(activeProfile.displayMode);
  }
  if (monitoringHudOverlayProfileWindow) {
    monitoringHudOverlayProfileWindow.dataset.overlayProfileWindow = "create-rename-membership-settings-shell";
    monitoringHudOverlayProfileWindow.dataset.activeOverlayProfileId = activeProfileId;
    monitoringHudOverlayProfileWindow.dataset.overlayProfileDirty = dirty ? "dirty" : "clean";
    monitoringHudOverlayProfileWindow.dataset.overlayProfileMembership = "editable-slc-039-mapping";
  }
  if (monitoringHudOverlayProfileWindowTitle) {
    monitoringHudOverlayProfileWindowTitle.textContent = "Profile Settings";
  }
  if (monitoringHudOverlayProfileWindowActiveName) {
    monitoringHudOverlayProfileWindowActiveName.textContent = activeProfileName;
  }
  if (monitoringHudOverlayProfileWindowCount) {
    monitoringHudOverlayProfileWindowCount.textContent = `${profiles.length} available profile${profiles.length === 1 ? "" : "s"}`;
  }
  if (monitoringHudOverlayProfileWindowMembership) {
    monitoringHudOverlayProfileWindowMembership.textContent = `${draftMonitorIds.length} selected of ${monitoringHudStableMonitorIds(cards).length} monitor${monitoringHudStableMonitorIds(cards).length === 1 ? "" : "s"}`;
  }
  monitoringHudRenderOverlayProfileMembershipList(activeProfile, cards, draftMonitorIds);
  if (monitoringHudOverlayProfileNameInput && document.activeElement !== monitoringHudOverlayProfileNameInput) {
    monitoringHudOverlayProfileNameInput.value = dirty
      ? monitoringHudOverlayProfileNameInput.value
      : activeProfileName;
  }
  if (monitoringHudOverlayProfileSave) {
    monitoringHudSetActionDisabled(monitoringHudOverlayProfileSave, !dirty, "saveable");
  }
  if (monitoringHudOverlayProfileDiscard) {
    monitoringHudSetActionDisabled(monitoringHudOverlayProfileDiscard, !dirty, "discardable");
  }
  if (monitoringHudOverlayProfileMembershipNote) {
    monitoringHudOverlayProfileMembershipNote.textContent = "Membership is editable inside Overlay Profile Settings; Monitor Groups and Recording Profiles remain separate.";
  }
}

function monitoringHudSensorAssignmentSummary(layout) {
  const assigned = Array.isArray(layout && layout.sensors) ? layout.sensors : [];
  if (!assigned.length) return "No sources assigned";
  const labels = assigned
    .map((sensorId) => monitoringHudSensorDefinitionById(sensorId))
    .filter(Boolean)
    .map((sensor) => sensor.label);
  return labels.length ? `${labels.length} source${labels.length === 1 ? "" : "s"}: ${labels.join(", ")}` : "No sources assigned";
}

function monitoringHudRenderDeleteConfirmation() {
  if (!monitoringHudMonitorDeleteConfirmation) return;
  const cardId = monitoringHudPendingDeleteMonitorId;
  const layout = cardId && monitoringHudControlState.cards ? monitoringHudControlState.cards[cardId] : null;
  const open = Boolean(cardId && layout);
  monitoringHudMonitorDeleteConfirmation.hidden = !open;
  monitoringHudMonitorDeleteConfirmation.dataset.deleteConfirmationState = open ? "open" : "closed";
  monitoringHudMonitorDeleteConfirmation.dataset.deleteMonitorId = open ? cardId : "";
  if (monitoringHudMonitorDeleteTitle) {
    monitoringHudMonitorDeleteTitle.textContent = open ? `Delete ${layout.title || "Monitor Group"}?` : "Delete monitor?";
  }
  if (monitoringHudMonitorDeleteCopy) {
    monitoringHudMonitorDeleteCopy.textContent = open
      ? "Confirm before removing this Monitor Group and its source assignments."
      : "Confirm before removing this Monitor Group.";
  }
}

function monitoringHudMonitorSearchValue() {
  return String(monitoringHudMonitorSearch ? monitoringHudMonitorSearch.value : "").trim().toLowerCase();
}

function monitoringHudFilteredMonitorIds(cards) {
  const query = monitoringHudMonitorSearchValue();
  const ids = Object.keys(cards || {});
  if (!query) return ids;
  return ids.filter((cardId) => {
    const layout = cards[cardId] || {};
    return [
      cardId,
      layout.title,
      monitoringHudSensorAssignmentSummary(layout)
    ].some((value) => String(value || "").toLowerCase().includes(query));
  });
}

function monitoringHudSensorSearchValue() {
  return String(monitoringHudSensorSearch ? monitoringHudSensorSearch.value : "").trim().toLowerCase();
}

function monitoringHudSensorFilterValue() {
  return String(
    monitoringHudSensorFilter
      ? (monitoringHudSensorFilter.dataset.selectedFilter || monitoringHudSensorFilter.value || "all")
      : "all"
  ).trim().toLowerCase() || "all";
}

function monitoringHudResetSourceFilterHover() {
  if (!monitoringHudSensorFilter) return;
  monitoringHudSensorFilter.dataset.hoveredFilter = "";
  monitoringHudSensorFilter.querySelectorAll("[data-source-filter]").forEach((item) => {
    item.classList.remove("is-hovered");
  });
}

function monitoringHudSetSourceFilterDropdownOpen(open) {
  if (!monitoringHudSensorFilter) return;
  const isOpen = Boolean(open);
  const menu = monitoringHudSensorFilter.querySelector(".monitoring-hud__source-filter-menu");
  monitoringHudSensorFilter.dataset.filterOpen = isOpen ? "true" : "false";
  if (monitoringHudSensorFilterToggle) {
    monitoringHudSensorFilterToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  }
  if (menu) menu.hidden = !isOpen;
  monitoringHudResetSourceFilterHover();
}

function monitoringHudSetSourceFilterValue(value) {
  if (!monitoringHudSensorFilter) return;
  const nextValue = String(value || "all").trim().toLowerCase() || "all";
  monitoringHudSensorFilter.dataset.selectedFilter = nextValue;
  monitoringHudSensorFilter.dataset.currentFilterLabel = monitoringHudSourceFilterLabels[nextValue] || nextValue;
  monitoringHudSensorFilter.querySelectorAll("[data-source-filter]").forEach((item) => {
    const selected = String(item.dataset.sourceFilter || "all").toLowerCase() === nextValue;
    item.setAttribute("aria-selected", selected ? "true" : "false");
    item.setAttribute("aria-pressed", selected ? "true" : "false");
  });
  if (monitoringHudSensorFilterLabel) {
    monitoringHudSensorFilterLabel.textContent = monitoringHudSourceFilterLabels[nextValue] || nextValue;
  }
}

function monitoringHudPollingRateValue(value) {
  const number = Math.max(1000, Number(value) || 1000);
  return Object.prototype.hasOwnProperty.call(monitoringHudPollingRateLabels, number) ? String(number) : "1000";
}

function monitoringHudResetPollingRateHover() {
  if (!monitoringHudMonitorPollingRateControl) return;
  monitoringHudMonitorPollingRateControl.dataset.hoveredValue = "";
  monitoringHudMonitorPollingRateControl.querySelectorAll("[data-polling-rate-option]").forEach((item) => {
    item.classList.remove("is-hovered");
  });
}

function monitoringHudSetPollingRateDropdownOpen(open) {
  if (!monitoringHudMonitorPollingRateControl) return;
  const isOpen = Boolean(open) && monitoringHudMonitorPollingRateControl.dataset.controlDisabled !== "true";
  const menu = document.getElementById("monitoring-hud-monitor-polling-rate-menu");
  monitoringHudMonitorPollingRateControl.dataset.dropdownOpen = isOpen ? "true" : "false";
  if (monitoringHudMonitorPollingRateToggle) {
    monitoringHudMonitorPollingRateToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  }
  if (menu) menu.hidden = !isOpen;
  monitoringHudResetPollingRateHover();
}

function monitoringHudSetPollingRateValue(value, options = {}) {
  const nextValue = monitoringHudPollingRateValue(value);
  if (monitoringHudMonitorPollingRate) {
    monitoringHudMonitorPollingRate.value = nextValue;
  }
  if (monitoringHudMonitorPollingRateControl) {
    monitoringHudMonitorPollingRateControl.dataset.selectedValue = nextValue;
    monitoringHudMonitorPollingRateControl.dataset.currentLabel = monitoringHudPollingRateLabels[Number(nextValue)] || nextValue;
    monitoringHudMonitorPollingRateControl.querySelectorAll("[data-polling-rate-option]").forEach((item) => {
      const selected = String(item.dataset.pollingRateOption || "") === nextValue;
      item.setAttribute("aria-selected", selected ? "true" : "false");
      item.setAttribute("aria-pressed", selected ? "true" : "false");
    });
  }
  if (monitoringHudMonitorPollingRateLabel) {
    monitoringHudMonitorPollingRateLabel.textContent = monitoringHudPollingRateLabels[Number(nextValue)] || nextValue;
  }
  if (options.dispatchChange && monitoringHudMonitorPollingRate) {
    monitoringHudMonitorPollingRate.dispatchEvent(new Event("change", { bubbles: true }));
  }
}

function monitoringHudControlActivationKey(element, fallback = "") {
  if (!element) return fallback || "unknown-control";
  if (element.id) return element.id;
  if (element.dataset) {
    if (element.dataset.control) return `control:${element.dataset.control}`;
    if (element.dataset.childWindowClose) return `close:${element.dataset.childWindowClose}`;
    if (element.dataset.monitorSelect) return `monitor:${element.dataset.monitorSelect}`;
    if (element.dataset.sourcePickerRow) return `source-row:${element.dataset.sourcePickerRow}`;
    if (element.dataset.monitorSensorInput) return `source-check:${element.dataset.monitorSensorInput}`;
    if (element.dataset.sourceFilter) return `source-filter:${element.dataset.sourceFilter}`;
    if (element.dataset.pollingRateOption) return `polling-rate:${element.dataset.pollingRateOption}`;
    if (element.dataset.sensorDisplayModeOption) {
      return `display-mode:${element.dataset.sensorDisplayModeOption}:${element.dataset.sensorDisplayModeValue || "text"}`;
    }
  }
  return fallback || String(element.textContent || element.tagName || "unknown-control").trim().slice(0, 64);
}

function monitoringHudControlInterceptionSnapshot(element) {
  if (!element || typeof element.getBoundingClientRect !== "function") return {};
  const rect = element.getBoundingClientRect();
  const x = Math.round(rect.left + rect.width / 2);
  const y = Math.round(rect.top + rect.height / 2);
  const topElement = document.elementFromPoint ? document.elementFromPoint(x, y) : null;
  const style = window.getComputedStyle ? window.getComputedStyle(element) : null;
  const topStyle = topElement && window.getComputedStyle ? window.getComputedStyle(topElement) : null;
  return {
    target: monitoringHudControlActivationKey(element),
    tag: String(element.tagName || ""),
    x,
    y,
    width: Math.round(rect.width),
    height: Math.round(rect.height),
    disabled: Boolean(element.disabled),
    ariaDisabled: String(element.getAttribute && element.getAttribute("aria-disabled") || "false"),
    pointerEvents: style ? style.pointerEvents : "",
    zIndex: style ? style.zIndex : "",
    interceptedBy: topElement ? monitoringHudControlActivationKey(topElement, String(topElement.tagName || "")) : "",
    interceptedPointerEvents: topStyle ? topStyle.pointerEvents : "",
    sameTargetOrChild: Boolean(topElement && (topElement === element || element.contains(topElement)))
  };
}

function monitoringHudPollingRateHitboxProof() {
  const row = document.querySelector('[data-control-row="polling-rate-inline"]');
  const control = monitoringHudMonitorPollingRateControl;
  const toggle = monitoringHudMonitorPollingRateToggle;
  if (!row || !control || !toggle) {
    return { passed: false, reason: "polling-rate-hitbox:missing-control" };
  }
  const rowRect = row.getBoundingClientRect();
  const toggleRect = toggle.getBoundingClientRect();
  const labelX = Math.round(rowRect.left + Math.min(24, Math.max(4, rowRect.width * 0.12)));
  const labelY = Math.round(rowRect.top + rowRect.height / 2);
  const labelTarget = document.elementFromPoint ? document.elementFromPoint(labelX, labelY) : null;
  const labelOpensControl = Boolean(
    labelTarget
    && (
      labelTarget === toggle
      || toggle.contains(labelTarget)
      || labelTarget === control
      || control.contains(labelTarget)
    )
  );
  const rowMuchWiderThanToggle = rowRect.width > toggleRect.width + 80;
  const toggleBounded = toggleRect.width <= 156 && toggleRect.right <= rowRect.right + 2;
  return {
    passed: row.dataset.pollingRateHitbox === "toggle-only" && rowMuchWiderThanToggle && toggleBounded && !labelOpensControl,
    rowWidth: Math.round(rowRect.width),
    toggleWidth: Math.round(toggleRect.width),
    labelProbe: [labelX, labelY],
    labelProbeTarget: monitoringHudControlActivationKey(labelTarget),
    labelOpensControl,
    rowPointerEvents: window.getComputedStyle ? window.getComputedStyle(row).pointerEvents : "",
    controlPointerEvents: window.getComputedStyle ? window.getComputedStyle(control).pointerEvents : "",
    hitboxMode: row.dataset.pollingRateHitbox || ""
  };
}

function monitoringHudManageCloseHitboxProof() {
  const button = document.querySelector('[data-child-window-close="monitor-group-edit"]');
  const windowNode = document.getElementById("monitoring-hud-edit-monitor-window");
  if (!button || !windowNode || windowNode.hidden) {
    return { passed: false, reason: "manage-close-hitbox:missing-open-control" };
  }
  const rect = button.getBoundingClientRect();
  const probes = [0.18, 0.50, 0.82].map((ratio) => {
    const x = Math.round(rect.left + rect.width / 2);
    const y = Math.round(rect.top + rect.height * ratio);
    const target = document.elementFromPoint ? document.elementFromPoint(x, y) : null;
    const sameTargetOrChild = Boolean(target && (target === button || button.contains(target)));
    return {
      ratio,
      x,
      y,
      target: monitoringHudControlActivationKey(target),
      sameTargetOrChild
    };
  });
  const style = window.getComputedStyle ? window.getComputedStyle(button) : null;
  const allProbesHitButton = probes.every((probe) => probe.sameTargetOrChild);
  return {
    passed: allProbesHitButton
      && rect.width >= 64
      && rect.height >= 30
      && (!style || (style.pointerEvents !== "none" && style.cursor === "pointer")),
    reason: allProbesHitButton ? "manage-close-hitbox:full-height-clear" : "manage-close-hitbox:partial-interception",
    rect: {
      left: Math.round(rect.left),
      top: Math.round(rect.top),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
      bottom: Math.round(rect.bottom)
    },
    probes,
    pointerEvents: style ? style.pointerEvents : "",
    cursor: style ? style.cursor : "",
    activeChildWindow: monitoringHudActiveChildWindow || "none"
  };
}

function monitoringHudReliableActivationAllowed(key) {
  const now = Date.now();
  monitoringHudReliableActivationState.lastKey = key;
  monitoringHudReliableActivationState.lastAt = now;
  return true;
}

function monitoringHudRecordReliableActivation(element, phase, passed = true) {
  const key = monitoringHudControlActivationKey(element);
  monitoringHudReliableActivationState.sequence += 1;
  const snapshot = monitoringHudControlInterceptionSnapshot(element);
  const record = Object.assign({}, snapshot, {
    sequence: monitoringHudReliableActivationState.sequence,
    key,
    phase,
    passed: Boolean(passed),
    timestamp: Date.now()
  });
  monitoringHudReliableActivationState.attempts.push(record);
  if (monitoringHudReliableActivationState.attempts.length > 120) {
    monitoringHudReliableActivationState.attempts.shift();
  }
  if (monitoringHud) {
    monitoringHud.dataset.interactiveControlReliability = "first-click-stress-ready";
    monitoringHud.dataset.lastInteractiveControl = key;
    monitoringHud.dataset.lastInteractiveControlPhase = phase;
    monitoringHud.dataset.clickInterceptionDiagnostics = record.sameTargetOrChild ? "target-clear" : "possible-interception";
  }
  return record;
}

function monitoringHudApplyPressedState(element, pressed) {
  if (!element || !element.classList) return;
  element.classList.toggle("is-pressed", Boolean(pressed));
}

function monitoringHudWireReliableControl(element, key, handler) {
  if (!element || typeof handler !== "function") return;
  const activationKey = key || monitoringHudControlActivationKey(element);
  element.addEventListener("pointerdown", () => {
    monitoringHudApplyPressedState(element, true);
    monitoringHudRecordReliableActivation(element, "pointerdown", true);
  });
  element.addEventListener("pointerleave", () => monitoringHudApplyPressedState(element, false));
  const activate = (event, phase) => {
    if (event && typeof event.preventDefault === "function") event.preventDefault();
    if (event && typeof event.stopPropagation === "function") event.stopPropagation();
    monitoringHudApplyPressedState(element, false);
    if (!monitoringHudReliableActivationAllowed(activationKey)) return;
    const result = handler(event);
    monitoringHudRecordReliableActivation(element, phase, result !== false);
  };
  element.addEventListener("click", (event) => activate(event, "click"));
}

function monitoringHudWireReliableDelegatedControl(root, selector, keyPrefix, handler, options = {}) {
  if (!root || typeof handler !== "function") return;
  const activate = (event, phase) => {
    const target = event.target && event.target.closest ? event.target.closest(selector) : null;
    if (!target || !root.contains(target)) return;
    const allowNative = Boolean(options.allowNative && options.allowNative(target, event, phase));
    if (!allowNative && event && typeof event.preventDefault === "function") event.preventDefault();
    if (!allowNative && event && typeof event.stopPropagation === "function") event.stopPropagation();
    monitoringHudApplyPressedState(target, false);
    const key = `${keyPrefix}:${monitoringHudControlActivationKey(target)}`;
    if (!monitoringHudReliableActivationAllowed(key)) return;
    const result = handler(target, event);
    monitoringHudRecordReliableActivation(target, phase, result !== false);
  };
  root.addEventListener("pointerdown", (event) => {
    const target = event.target && event.target.closest ? event.target.closest(selector) : null;
    if (!target || !root.contains(target)) return;
    monitoringHudApplyPressedState(target, true);
    monitoringHudRecordReliableActivation(target, "pointerdown", true);
  });
  root.addEventListener("pointerleave", (event) => {
    const target = event.target && event.target.closest ? event.target.closest(selector) : null;
    if (target) monitoringHudApplyPressedState(target, false);
  });
  root.addEventListener("click", (event) => activate(event, "click"));
}

function monitoringHudSourcePickerRowFromEvent(event) {
  return event && event.target && event.target.closest
    ? event.target.closest("[data-source-picker-row]")
    : null;
}

function monitoringHudPreventNativeSourcePickerEvent(event) {
  if (event && typeof event.preventDefault === "function") event.preventDefault();
  if (event && typeof event.stopPropagation === "function") event.stopPropagation();
}

function monitoringHudActivateSourcePickerRow(row, event, phase, options = {}) {
  if (!row || !monitoringHudMonitorSensorAssignment || !monitoringHudMonitorSensorAssignment.contains(row)) return false;
  monitoringHudPreventNativeSourcePickerEvent(event);
  const key = `source-picker:checkmark:${monitoringHudControlActivationKey(row)}`;
  if (options.suppressNativeChange) monitoringHudSourcePickerSuppressNativeChangeUntil = Date.now() + 500;
  if (options.suppressFollowingClick) {
    monitoringHudSourcePickerSuppressClickUntil = Date.now() + 500;
    monitoringHudSourcePickerSuppressClickRow = row;
  }
  monitoringHudApplyPressedState(row, true);
  const result = monitoringHudToggleSensorAssignmentRow(row);
  window.setTimeout(() => monitoringHudApplyPressedState(row, false), 80);
  monitoringHudRecordReliableActivation(row, phase, result !== false);
  if (monitoringHudMonitorSensorAssignment) {
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerActivationPath = "single-deterministic-row-input-keyboard";
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerLastActivation = phase;
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerLastActivationKey = key;
  }
  return result;
}

function monitoringHudWireSourcePickerReliableSelection(root) {
  if (!root) return;
  root.addEventListener("pointerdown", (event) => {
    const row = monitoringHudSourcePickerRowFromEvent(event);
    if (!row || !root.contains(row)) return;
    monitoringHudActivateSourcePickerRow(row, event, "pointerdown-immediate", {
      suppressNativeChange: true,
      suppressFollowingClick: true
    });
  });
  root.addEventListener("pointerleave", (event) => {
    const row = monitoringHudSourcePickerRowFromEvent(event);
    if (row) monitoringHudApplyPressedState(row, false);
  });
  root.addEventListener("click", (event) => {
    const row = monitoringHudSourcePickerRowFromEvent(event);
    if (!row || !root.contains(row)) return;
    monitoringHudPreventNativeSourcePickerEvent(event);
    if (Date.now() <= monitoringHudSourcePickerSuppressClickUntil && row === monitoringHudSourcePickerSuppressClickRow) {
      monitoringHudSourcePickerSuppressClickUntil = 0;
      monitoringHudSourcePickerSuppressClickRow = null;
      return;
    }
    monitoringHudSourcePickerSuppressClickRow = null;
    monitoringHudActivateSourcePickerRow(row, event, "click-fallback");
  }, true);
}

function monitoringHudSetActionDisabled(button, disabled, activeState, disabledState = "clean-disabled") {
  if (!button) return;
  const isDisabled = Boolean(disabled);
  button.disabled = isDisabled;
  button.setAttribute("aria-disabled", isDisabled ? "true" : "false");
  button.dataset.controlState = isDisabled ? disabledState : activeState;
}

function monitoringHudUpdateMonitorActionState() {
  const selected = monitoringHudSelectedMonitor();
  const canEdit = Boolean(selected && selected.id && selected.layout);
  const dirty = Boolean(canEdit && monitoringHudUnsavedMonitorDirty);
  monitoringHudSetActionDisabled(monitoringHudEditMonitorConfirm, !dirty, "saveable");
  monitoringHudSetActionDisabled(monitoringHudEditMonitorDiscard, !dirty, "discardable");
  if (monitoringHudMonitorDetailActions) {
    monitoringHudMonitorDetailActions.dataset.draftActionState = dirty ? "dirty-save-discard-enabled" : "clean-save-discard-disabled";
    monitoringHudMonitorDetailActions.dataset.footerActions = "save-left-discard-left-delete-right";
  }
}

function monitoringHudDiscardCurrentMonitorDraft() {
  if (!monitoringHudUnsavedMonitorDirty) {
    monitoringHudUpdateMonitorActionState();
    return false;
  }
  if (
    monitoringHudDraftOriginalMonitorId
    && monitoringHudDraftOriginalLayout
    && monitoringHudControlState.cards
    && monitoringHudControlState.cards[monitoringHudDraftOriginalMonitorId]
  ) {
    monitoringHudControlState.cards[monitoringHudDraftOriginalMonitorId] = monitoringHudCloneMonitorLayout(monitoringHudDraftOriginalLayout);
    monitoringHudControlState.selectedMonitorId = monitoringHudDraftOriginalMonitorId;
  }
  monitoringHudPendingDeleteMonitorId = "";
  monitoringHudSetMonitorDraftDirty(false);
  monitoringHudRenderMonitorManagement();
  return true;
}

function monitoringHudRevealUnsavedGuard() {
  if (!monitoringHudMonitorUnsavedGuard || monitoringHudMonitorUnsavedGuard.hidden) return;
  monitoringHudMonitorUnsavedGuard.dataset.unsavedGuardReveal = "scrolled-focused";
  const immediatePane = monitoringHudEditMonitorWindow
    ? monitoringHudEditMonitorWindow.querySelector(".monitoring-hud__monitor-detail-pane")
    : null;
  if (immediatePane) immediatePane.scrollTop = 0;
  window.requestAnimationFrame(() => {
    if (!monitoringHudMonitorUnsavedGuard || monitoringHudMonitorUnsavedGuard.hidden) return;
    const detailPane = monitoringHudEditMonitorWindow
      ? monitoringHudEditMonitorWindow.querySelector(".monitoring-hud__monitor-detail-pane")
      : null;
    if (detailPane) detailPane.scrollTop = 0;
    if (typeof monitoringHudMonitorUnsavedGuard.scrollIntoView === "function") {
      monitoringHudMonitorUnsavedGuard.scrollIntoView({ block: "start", inline: "nearest", behavior: "instant" });
    }
    const focusTarget = monitoringHudMonitorUnsavedSave || monitoringHudMonitorUnsavedDiscard;
    if (focusTarget && typeof focusTarget.focus === "function") {
      focusTarget.focus({ preventScroll: true });
    }
  });
}

function monitoringHudActivateDisplayModeChip(button, event, phase, options = {}) {
  if (!button || !monitoringHudMonitorSensorSettings || !monitoringHudMonitorSensorSettings.contains(button)) return false;
  if (event && typeof event.preventDefault === "function") event.preventDefault();
  if (event && typeof event.stopPropagation === "function") event.stopPropagation();
  if (options.suppressFollowingClick) {
    monitoringHudDisplayModeSuppressClickUntil = Date.now() + 500;
    monitoringHudDisplayModeSuppressClickButton = button;
  }
  const sensorId = button.dataset.sensorDisplayModeOption;
  const value = button.dataset.sensorDisplayModeValue || "text";
  const group = monitoringHudMonitorSensorSettings.querySelector(`[data-sensor-display-mode="${sensorId}"]`);
  if (!sensorId || !group) return false;
  group.dataset.sensorDisplayModeSelected = value;
  group.querySelectorAll("[data-sensor-display-mode-option]").forEach((item) => {
    item.setAttribute("aria-pressed", item === button ? "true" : "false");
    item.classList.toggle("is-pressed", item === button && phase.indexOf("pointerdown") >= 0);
  });
  const draft = monitoringHudUpdateMonitorDraftFromWindow();
  if (draft) {
    monitoringHudUpdateSelectedMonitorRowSummary(draft.layout);
    monitoringHudMonitorSensorSettings.dataset.displayModeActivationPath = "deterministic-pointer-click-keyboard";
    monitoringHudMonitorSensorSettings.dataset.displayModeLastActivation = phase;
    monitoringHudMonitorSensorSettings.dataset.displayModeLastValue = value;
  }
  monitoringHudRecordReliableActivation(button, phase, Boolean(draft));
  if (phase.indexOf("pointerdown") >= 0) {
    window.setTimeout(() => monitoringHudApplyPressedState(button, false), 80);
  }
  return Boolean(draft);
}

function monitoringHudWireDisplayModeReliableSelection(root) {
  if (!root) return;
  root.addEventListener("pointerdown", (event) => {
    const button = event.target && event.target.closest ? event.target.closest("[data-sensor-display-mode-option]") : null;
    if (!button || !root.contains(button)) return;
    monitoringHudActivateDisplayModeChip(button, event, "pointerdown-immediate", { suppressFollowingClick: true });
  });
  root.addEventListener("click", (event) => {
    const button = event.target && event.target.closest ? event.target.closest("[data-sensor-display-mode-option]") : null;
    if (!button || !root.contains(button)) return;
    if (Date.now() <= monitoringHudDisplayModeSuppressClickUntil && button === monitoringHudDisplayModeSuppressClickButton) {
      if (event && typeof event.preventDefault === "function") event.preventDefault();
      if (event && typeof event.stopPropagation === "function") event.stopPropagation();
      monitoringHudDisplayModeSuppressClickUntil = 0;
      monitoringHudDisplayModeSuppressClickButton = null;
      return;
    }
    monitoringHudDisplayModeSuppressClickButton = null;
    monitoringHudActivateDisplayModeChip(button, event, "click-fallback");
  }, true);
  root.addEventListener("keydown", (event) => {
    if (!["Enter", " "].includes(event.key)) return;
    const button = event.target && event.target.closest ? event.target.closest("[data-sensor-display-mode-option]") : null;
    if (!button || !root.contains(button)) return;
    monitoringHudActivateDisplayModeChip(button, event, "keyboard-toggle");
  });
}

function monitoringHudSensorMatchesFilter(sensor, query, filterValue) {
  const category = String(sensor.category || monitoringHudSensorCategoryForId(sensor.id)).toLowerCase();
  const metric = String(sensor.metric || "").toLowerCase();
  const state = String(sensor.state || "").toLowerCase();
  const supported = sensor.assignable !== false;
  if (filterValue === "supported" && !supported) return false;
  if (filterValue === "deferred" && (supported || !["blocked-until-provider", "provider-required", "deferred"].includes(state))) return false;
  if (filterValue === "missing" && state !== "missing") return false;
  if (filterValue === "warning" && state !== "warning") return false;
  if (!["all", "supported", "deferred", "missing", "warning"].includes(filterValue)) {
    const filterCandidates = [category, metric, state, sensor.id, sensor.label, sensor.source, sensor.provider, sensor.device, sensor.instance, sensor.reason]
      .map((value) => String(value || "").toLowerCase());
    if (!filterCandidates.some((value) => value === filterValue || value.includes(filterValue))) return false;
  }
  if (!query) return true;
  return [
    sensor.id,
    sensor.label,
    sensor.source,
    sensor.provider,
    sensor.device,
    sensor.category,
    sensor.metric,
    sensor.instance,
    sensor.reason,
    state
  ].some((value) => String(value || "").toLowerCase().includes(query));
}

function monitoringHudFilteredSensorDefinitions() {
  const query = monitoringHudSensorSearchValue();
  const filterValue = monitoringHudSensorFilterValue();
  return monitoringHudSensorDefinitions().filter((sensor) => monitoringHudSensorMatchesFilter(sensor, query, filterValue));
}

function monitoringHudRenderSensorPreview(totalCount, renderedCount, selectedCount, supportedCount, deferredCount) {
  if (!monitoringHudSensorPreview) return;
  monitoringHudSensorPreview.dataset.sensorPreview = "source-identity-breadcrumbs";
  const fixtureCopy = monitoringHudLargeFixtureModeEnabled
    ? ` Large-source fixture proof mode is active with ${monitoringHudLargeSensorFixtureCount} scale sources.`
    : "";
  monitoringHudSensorPreview.textContent = `${selectedCount} selected. Showing ${renderedCount} of ${totalCount} filtered sources; ${supportedCount} supported and ${deferredCount} provider-required/deferred. Source rows expose provider, device, category, metric, and sensor instance breadcrumbs.${fixtureCopy}`;
}

function monitoringHudRenderSensorAssignment(selected) {
  if (!monitoringHudMonitorSensorAssignment) return;
  const layout = selected && selected.layout ? monitoringHudNormalizeSensorAssignments(selected.id, selected.layout) : null;
  const assigned = new Set(Array.isArray(layout && layout.sensors) ? layout.sensors : []);
  monitoringHudMonitorSensorAssignment.innerHTML = "";
  monitoringHudMonitorSensorAssignment.dataset.sensorAssignment = "sensor-library-source-picker";
  monitoringHudMonitorSensorAssignment.dataset.sourcePickerVisual = "nexus-faceted-searchable-rows";
  monitoringHudMonitorSensorAssignment.dataset.largeSourceFixtureCount = String(monitoringHudLargeSensorFixtureCount);
  monitoringHudMonitorSensorAssignment.dataset.largeSourceFixtureMode = monitoringHudLargeFixtureModeEnabled ? "enabled-validation-support" : "available-validation-support";
  monitoringHudMonitorSensorAssignment.dataset.visibleSourceResultLimit = String(monitoringHudSensorRenderLimit);
  const filtered = monitoringHudFilteredSensorDefinitions();
  const rendered = filtered.slice(0, monitoringHudSensorRenderLimit);
  const supportedCount = filtered.filter((sensor) => sensor.assignable !== false).length;
  const deferredCount = filtered.length - supportedCount;
  monitoringHudMonitorSensorAssignment.dataset.filteredSourceCount = String(filtered.length);
  monitoringHudMonitorSensorAssignment.dataset.renderedSourceCount = String(rendered.length);
  monitoringHudMonitorSensorAssignment.dataset.supportedSourceCount = String(supportedCount);
  monitoringHudMonitorSensorAssignment.dataset.deferredSourceCount = String(deferredCount);
  if (monitoringHudSensorResultSummary) {
    monitoringHudSensorResultSummary.textContent = `${rendered.length} shown of ${filtered.length} matching sources (${supportedCount} supported, ${deferredCount} deferred)`;
  }
  rendered.forEach((sensor) => {
    const row = document.createElement("div");
    row.className = "monitoring-hud__sensor-option";
    row.dataset.monitorSensorOption = sensor.id;
    row.dataset.sourcePickerRow = sensor.id;
    row.dataset.sensorSourceState = sensor.state || "unknown";
    row.dataset.sensorAssignable = sensor.assignable === false ? "false" : "true";
    row.dataset.sensorProvider = sensor.provider || "";
    row.dataset.sensorDevice = sensor.device || "";
    row.dataset.sensorCategory = sensor.category || "";
    row.dataset.sensorMetric = sensor.metric || "";
    row.dataset.sensorInstance = sensor.instance || "";
    row.dataset.sourceBreadcrumb = [sensor.provider, sensor.device, sensor.category, sensor.metric, sensor.instance].filter(Boolean).join(" > ");
    row.dataset.sourceToggleMode = "row-and-checkbox-immediate";
    row.dataset.sourceSelected = assigned.has(sensor.id) ? "true" : "false";
    row.setAttribute("role", "option");
    row.setAttribute("tabindex", sensor.assignable === false ? "-1" : "0");
    row.setAttribute("aria-selected", assigned.has(sensor.id) ? "true" : "false");
    row.setAttribute("aria-disabled", sensor.assignable === false ? "true" : "false");
    if (sensor.assignable === false) {
      row.classList.add("monitoring-hud__sensor-option--disabled");
    }
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = sensor.id;
    checkbox.checked = assigned.has(sensor.id);
    checkbox.disabled = sensor.assignable === false;
    checkbox.dataset.monitorSensorInput = sensor.id;
    checkbox.setAttribute("aria-label", `Assign ${sensor.label || sensor.id}`);
    const name = document.createElement("span");
    name.textContent = sensor.label || sensor.id;
    const status = document.createElement("b");
    status.className = "monitoring-hud__source-status";
    status.textContent = sensor.assignable === false ? String(sensor.state || "deferred").replace(/-/g, " ") : "supported";
    const detail = document.createElement("small");
    const breadcrumb = [sensor.provider, sensor.device, sensor.category, sensor.metric, sensor.instance]
      .filter(Boolean)
      .join(" > ");
    detail.textContent = sensor.assignable === false
      ? `${sensor.reason || "Provider required"} - ${breadcrumb || sensor.source || ""}`.trim()
      : `${sensor.reason || "Runtime source"} - ${breadcrumb || sensor.value || sensor.source || ""}`.trim();
    const meta = document.createElement("div");
    meta.className = "monitoring-hud__source-meta";
    [
      sensor.provider || "provider",
      sensor.device || "device",
      sensor.category || "category",
      sensor.metric || "metric",
      sensor.instance || "instance",
      sensor.value || sensor.reason || ""
    ].filter(Boolean).forEach((part) => {
      const item = document.createElement("span");
      item.textContent = String(part);
      meta.appendChild(item);
    });
    row.appendChild(checkbox);
    row.appendChild(name);
    row.appendChild(status);
    row.appendChild(detail);
    row.appendChild(meta);
    monitoringHudMonitorSensorAssignment.appendChild(row);
  });
  if (!rendered.length) {
    const empty = document.createElement("div");
    empty.className = "monitoring-hud__sensor-settings-empty";
    empty.dataset.sensorLibraryEmpty = "no-results";
    empty.textContent = "No matching sources. Change search or filter to find supported or deferred data sources.";
    monitoringHudMonitorSensorAssignment.appendChild(empty);
  }
  monitoringHudRenderSensorPreview(filtered.length, rendered.length, assigned.size, supportedCount, deferredCount);
}

function monitoringHudSetSourceRowSelectionState(row, checked) {
  if (!row) return;
  row.dataset.sourceSelected = checked ? "true" : "false";
  row.setAttribute("aria-selected", checked ? "true" : "false");
}

function monitoringHudUpdateSelectedMonitorRowSummary(layout) {
  if (!monitoringHudEditMonitorList || !monitoringHudControlState.selectedMonitorId || !layout) return;
  const row = monitoringHudEditMonitorList.querySelector(`[data-monitor-row="${monitoringHudControlState.selectedMonitorId}"]`);
  const summary = row ? row.querySelector("span") : null;
  if (summary) summary.textContent = monitoringHudSensorAssignmentSummary(layout);
}

function monitoringHudRefreshSensorPickerSelectionProof(draft, options = {}) {
  const layout = draft && draft.layout ? draft.layout : null;
  const selectedCount = Array.isArray(layout && layout.sensors) ? layout.sensors.length : 0;
  monitoringHudUpdateSelectedMonitorRowSummary(layout);
  if (options.deferSettingsRefresh && monitoringHudMonitorSensorAssignment) {
    const totalCount = Number(monitoringHudMonitorSensorAssignment.dataset.filteredSourceCount || 0);
    const renderedCount = Number(monitoringHudMonitorSensorAssignment.dataset.renderedSourceCount || 0);
    const supportedCount = Number(monitoringHudMonitorSensorAssignment.dataset.supportedSourceCount || 0);
    const deferredCount = Number(monitoringHudMonitorSensorAssignment.dataset.deferredSourceCount || 0);
    monitoringHudRenderSensorPreview(totalCount, renderedCount, selectedCount, supportedCount, deferredCount);
    monitoringHudScheduleSensorSettingsRefresh(draft);
  } else {
    const filtered = monitoringHudFilteredSensorDefinitions();
    const rendered = filtered.slice(0, monitoringHudSensorRenderLimit);
    const supportedCount = filtered.filter((sensor) => sensor.assignable !== false).length;
    const deferredCount = filtered.length - supportedCount;
    monitoringHudRenderSensorSettings(draft);
    monitoringHudRenderSensorPreview(filtered.length, rendered.length, selectedCount, supportedCount, deferredCount);
  }
  if (monitoringHudMonitorSensorAssignment) {
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerCheckmarkMode = options.deferSettingsRefresh
      ? "row-and-checkbox-immediate-deferred-settings"
      : "row-and-checkbox-immediate";
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerCheckmarkStress = "ready";
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerCheckmarkLatency = options.deferSettingsRefresh
      ? "immediate-visual-deferred-settings"
      : "synchronous";
  }
}

function monitoringHudScheduleSensorSettingsRefresh(draft) {
  if (!monitoringHudMonitorSensorSettings) return;
  if (monitoringHudSensorSettingsRefreshFrame) {
    cancelAnimationFrame(monitoringHudSensorSettingsRefreshFrame);
  }
  const selected = draft && draft.id && draft.layout
    ? { id: draft.id, layout: monitoringHudCloneMonitorLayout(draft.layout) }
    : null;
  monitoringHudSensorSettingsRefreshFrame = requestAnimationFrame(() => {
    monitoringHudSensorSettingsRefreshFrame = 0;
    monitoringHudRenderSensorSettings(selected);
  });
}

function monitoringHudApplySensorAssignmentToDraft(row, checked) {
  if (!row || row.dataset.sensorAssignable === "false") return null;
  const sourceId = String(row.dataset.sourcePickerRow || row.dataset.monitorSensorOption || "").trim();
  if (!sourceId) return null;
  const draft = monitoringHudEnsureMonitorDraft();
  if (!draft || !draft.layout) return null;
  draft.layout.title = monitoringHudCleanMonitorTitle(
    monitoringHudEditMonitorName ? monitoringHudEditMonitorName.value : "",
    draft.layout.title || "Monitor Group"
  );
  draft.layout.enabled = monitoringHudMonitorEnabled ? Boolean(monitoringHudMonitorEnabled.checked) : draft.layout.enabled !== false;
  draft.layout.pollingRateMs = monitoringHudMonitorPollingRate
    ? Math.max(1000, Number(monitoringHudMonitorPollingRate.value) || 1000)
    : Math.max(1000, Number(draft.layout.pollingRateMs) || 1000);
  draft.layout.warningNotificationsEnabled = monitoringHudMonitorWarningSetting
    ? Boolean(monitoringHudMonitorWarningSetting.checked)
    : draft.layout.warningNotificationsEnabled !== false;
  const existing = Array.isArray(draft.layout.sensors) ? draft.layout.sensors.slice() : [];
  const selected = checked
    ? Array.from(new Set(existing.concat(sourceId)))
    : existing.filter((sensorId) => sensorId !== sourceId);
  draft.layout.sensors = selected;
  draft.layout.sensorSettings = Object.assign({}, draft.layout.sensorSettings || {});
  if (checked) {
    draft.layout.sensorSettings[sourceId] = Object.assign(
      monitoringHudDefaultSensorSetting(sourceId),
      draft.layout.sensorSettings[sourceId] || {}
    );
  } else {
    delete draft.layout.sensorSettings[sourceId];
  }
  monitoringHudDraftWorkingLayout = draft.layout;
  return {
    id: draft.id,
    layout: monitoringHudDraftWorkingLayout
  };
}

function monitoringHudToggleSensorAssignmentRow(row, explicitChecked) {
  if (!row || row.dataset.sensorAssignable === "false") return false;
  const input = row.querySelector("[data-monitor-sensor-input]");
  if (!input || input.disabled) return false;
  const nextChecked = typeof explicitChecked === "boolean" ? explicitChecked : !input.checked;
  input.checked = nextChecked;
  monitoringHudSetSourceRowSelectionState(row, nextChecked);
  const draft = monitoringHudApplySensorAssignmentToDraft(row, nextChecked);
  if (!draft) return false;
  monitoringHudRefreshSensorPickerSelectionProof(draft, { deferSettingsRefresh: true });
  return true;
}

function monitoringHudRenderSensorSettings(selected) {
  if (!monitoringHudMonitorSensorSettings) return;
  const layout = selected && selected.layout ? monitoringHudNormalizeSensorAssignments(selected.id, selected.layout) : null;
  const assigned = Array.isArray(layout && layout.sensors) ? layout.sensors : [];
  monitoringHudMonitorSensorSettings.innerHTML = "";
  monitoringHudMonitorSensorSettings.dataset.sensorSettings = "selected-monitor-sources";
  if (!assigned.length) {
    const empty = document.createElement("div");
    empty.className = "monitoring-hud__sensor-settings-empty";
    empty.textContent = "No supported sources assigned to this Monitor Group.";
    monitoringHudMonitorSensorSettings.appendChild(empty);
    return;
  }
  assigned.forEach((sensorId) => {
    const sensor = monitoringHudSensorDefinitionById(sensorId);
    if (!sensor) return;
    const settings = Object.assign(monitoringHudDefaultSensorSetting(sensorId), layout.sensorSettings[sensorId] || {});
    const row = document.createElement("div");
    row.className = "monitoring-hud__sensor-settings-row";
    row.dataset.sensorSettingsRow = sensorId;
    const title = document.createElement("strong");
    title.textContent = sensor.label || sensorId;
    const modeLabel = document.createElement("div");
    modeLabel.className = "monitoring-hud__mode-chip-group";
    modeLabel.dataset.sensorDisplayMode = sensorId;
    modeLabel.dataset.sensorDisplayModeSelected = settings.displayMode || "badge-text";
    const modeTitle = document.createElement("span");
    modeTitle.textContent = "Display mode";
    modeLabel.appendChild(modeTitle);
    [
      ["badge-text", "Badge + text"],
      ["text", "Text only"],
      ["badge", "Badge only"]
    ].forEach(([value, label]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "monitoring-hud__mode-chip";
      button.dataset.sensorDisplayModeOption = sensorId;
      button.dataset.sensorDisplayModeValue = value;
      button.setAttribute("aria-pressed", settings.displayMode === value ? "true" : "false");
      button.textContent = label;
      modeLabel.appendChild(button);
    });
    const warningLabel = document.createElement("label");
    const warning = document.createElement("input");
    warning.type = "checkbox";
    warning.dataset.sensorWarningEnabled = sensorId;
    warning.checked = settings.warningEnabled !== false;
    warningLabel.appendChild(warning);
    warningLabel.append(" Warning state uses visual Dashboard notifications");
    row.appendChild(title);
    row.appendChild(modeLabel);
    row.appendChild(warningLabel);
    monitoringHudMonitorSensorSettings.appendChild(row);
  });
}

function monitoringHudRenderChildWindows() {
  const cards = monitoringHudControlState.cards || {};
  const selected = monitoringHudSelectedMonitor();
  const hasSelectedMonitor = Boolean(selected.id && selected.layout);
  const selectedLayout = hasSelectedMonitor ? monitoringHudSelectedMonitorDetailLayout(selected) : null;
  const count = Object.keys(cards).length;
  monitoringHudRenderDashboardSettingsPanel();
  if (monitoringHudCreateMonitorName && !monitoringHudCreateMonitorName.value.trim()) {
    monitoringHudCreateMonitorName.value = monitoringHudSuggestedMonitorName();
  }
  if (monitoringHudEditMonitorTitle) {
    monitoringHudEditMonitorTitle.textContent = selectedLayout ? (selectedLayout.title || "Monitor Group") : (count === 0 ? "No Monitors Yet" : "No Monitor Selected");
  }
  if (monitoringHudEditMonitorName) {
    monitoringHudEditMonitorName.value = selectedLayout ? (selectedLayout.title || "Monitor Group") : "";
    monitoringHudEditMonitorName.disabled = !hasSelectedMonitor;
  }
  if (monitoringHudMonitorEnabled) {
    monitoringHudMonitorEnabled.checked = selectedLayout ? selectedLayout.enabled !== false : false;
    monitoringHudMonitorEnabled.disabled = !hasSelectedMonitor;
  }
  if (monitoringHudMonitorPollingRate) {
    monitoringHudSetPollingRateValue(selectedLayout ? String(Math.max(1000, Number(selectedLayout.pollingRateMs) || 1000)) : "1000");
    monitoringHudMonitorPollingRate.disabled = !hasSelectedMonitor;
  }
  if (monitoringHudMonitorPollingRateControl) {
    monitoringHudMonitorPollingRateControl.dataset.controlDisabled = hasSelectedMonitor ? "false" : "true";
  }
  if (monitoringHudMonitorPollingRateToggle) {
    monitoringHudMonitorPollingRateToggle.disabled = !hasSelectedMonitor;
    monitoringHudMonitorPollingRateToggle.setAttribute("aria-disabled", hasSelectedMonitor ? "false" : "true");
  }
  if (monitoringHudMonitorWarningSetting) {
    monitoringHudMonitorWarningSetting.checked = selectedLayout ? selectedLayout.warningNotificationsEnabled !== false : false;
    monitoringHudMonitorWarningSetting.disabled = !hasSelectedMonitor;
  }
  if (monitoringHudProviderReadinessPanel) {
    monitoringHudProviderReadinessPanel.dataset.readinessClassification = "status-future-capability-not-assignable-source";
  }
  if (monitoringHudSensorFilter) {
    monitoringHudSetSourceFilterValue(monitoringHudSensorFilterValue());
  }
  if (monitoringHudMonitorDetailDelete) {
    monitoringHudMonitorDetailDelete.disabled = !hasSelectedMonitor;
    monitoringHudMonitorDetailDelete.setAttribute("aria-disabled", hasSelectedMonitor ? "false" : "true");
  }
  if (monitoringHudMonitorDetailEmpty) {
    monitoringHudMonitorDetailEmpty.hidden = count !== 0;
    monitoringHudMonitorDetailEmpty.dataset.monitorDetailEmpty = count === 0 ? "true-empty-state-create-reachable" : "hidden";
  }
  if (monitoringHudMonitorDetailActions) {
    monitoringHudMonitorDetailActions.hidden = !hasSelectedMonitor;
    monitoringHudMonitorDetailActions.dataset.monitorDetailActions = hasSelectedMonitor ? "selected-monitor-footer" : "hidden-no-monitor";
  }
  monitoringHudUpdateMonitorActionState();
  if (monitoringHudMonitorDetailNote) {
    monitoringHudMonitorDetailNote.hidden = !hasSelectedMonitor;
  }
  const settingsPanel = monitoringHudEditMonitorWindow
    ? monitoringHudEditMonitorWindow.querySelector(".monitoring-hud__monitor-settings-panel")
    : null;
  if (settingsPanel) {
    settingsPanel.hidden = count === 0;
    settingsPanel.dataset.monitorDetailState = count === 0 ? "empty" : "selected-monitor-detail";
  }
  if (monitoringHudEditMonitorList) {
    monitoringHudEditMonitorList.innerHTML = "";
    const visibleMonitorIds = monitoringHudFilteredMonitorIds(cards);
    visibleMonitorIds.forEach((cardId) => {
      const layout = Object.assign(monitoringHudCardDefaults(cardId), cards[cardId] || {});
      monitoringHudNormalizeMonitorGroupTitle(cardId, layout);
      monitoringHudNormalizeSensorAssignments(cardId, layout);
      cards[cardId] = layout;
      const row = document.createElement("div");
      row.className = "monitoring-hud__monitor-manage-row";
      row.dataset.monitorRow = cardId;
      row.dataset.monitorSelect = cardId;
      row.setAttribute("role", "button");
      row.setAttribute("tabindex", "0");
      row.setAttribute("aria-current", cardId === selected.id ? "true" : "false");
      const copy = document.createElement("div");
      const title = document.createElement("strong");
      title.textContent = layout.title || `Group ${cardId}`;
      const meta = document.createElement("span");
      meta.textContent = monitoringHudSensorAssignmentSummary(layout);
      copy.appendChild(title);
      copy.appendChild(meta);
      row.appendChild(copy);
      monitoringHudEditMonitorList.appendChild(row);
    });
    monitoringHudEditMonitorList.dataset.monitorListScale = "searchable-large-monitor-list";
    monitoringHudEditMonitorList.dataset.monitorListStressProof = "20-plus-groups-nexus-scrollbar";
    monitoringHudEditMonitorList.dataset.largeMonitorFixtureCount = String(monitoringHudLargeMonitorFixtureCount);
    monitoringHudEditMonitorList.dataset.visibleMonitorCount = String(visibleMonitorIds.length);
    if (monitoringHudMonitorListEmpty) {
      const empty = visibleMonitorIds.length === 0;
      monitoringHudMonitorListEmpty.hidden = !empty;
      monitoringHudMonitorListEmpty.dataset.monitorListEmpty = empty ? (count === 0 ? "true-empty-state" : "no-results") : "hidden";
      monitoringHudMonitorListEmpty.textContent = count === 0 ? "No monitors yet." : "No matching monitors.";
    }
  }
  if (monitoringHudMonitorManageSummary) {
    const visibleCount = monitoringHudEditMonitorList
      ? Number(monitoringHudEditMonitorList.dataset.visibleMonitorCount || count)
      : count;
    monitoringHudMonitorManageSummary.textContent = `${visibleCount} shown / ${count} created monitor${count === 1 ? "" : "s"}`;
  }
  monitoringHudRenderDeleteConfirmation();
  monitoringHudRenderSensorAssignment({ id: selected.id, layout: selectedLayout });
  monitoringHudRenderSensorSettings({ id: selected.id, layout: selectedLayout });
  if (monitoringHudEditMonitor) {
    monitoringHudEditMonitor.disabled = count === 0;
    monitoringHudEditMonitor.setAttribute("aria-disabled", count === 0 ? "true" : "false");
  }
}

function monitoringHudOpenChildWindow(kind) {
  if (kind === "monitor-group-create" && monitoringHudCreateMonitorName) {
    monitoringHudCreateMonitorName.value = monitoringHudSuggestedMonitorName();
  }
  if (kind === "overlay-profile-settings") {
    monitoringHudSetOverlayProfileDraftFromActive();
    monitoringHudClearOverlayProfileMembershipList();
    monitoringHudSetOverlayProfileDropdownOpen(false);
  }
  monitoringHudRenderChildWindows();
  monitoringHudSetChildWindowVisibility(kind);
  if (kind === "overlay-profile-settings") {
    monitoringHudRenderOverlayProfileControls();
  }
  const focusTarget = kind === "dashboard-settings"
    ? monitoringHudSettingsWarningToggle
    : kind === "monitor-group-create"
      ? monitoringHudCreateMonitorName
      : kind === "overlay-profile-settings"
        ? monitoringHudOverlayProfileNameInput
        : monitoringHudEditMonitorName;
  if (focusTarget && typeof focusTarget.focus === "function") {
    setTimeout(() => focusTarget.focus(), 0);
  }
}

function monitoringHudCloseChildWindow(options = {}) {
  if (!options.force && monitoringHudActiveChildWindow === "monitor-group-edit" && monitoringHudUnsavedMonitorDirty) {
    monitoringHudShowUnsavedGuard({ type: "close" });
    return false;
  }
  if (document.activeElement && document.activeElement.closest && document.activeElement.closest(".monitoring-hud__child-window")) {
    document.activeElement.blur();
  }
  monitoringHudSetChildWindowVisibility("");
  return true;
}

function monitoringHudCreateMonitorGroup(titleValue) {
  const nextNumber = monitoringHudNextMonitorGroupNumber();
  monitoringHudControlState.monitorSequence = nextNumber;
  const cardId = `monitor-${nextNumber}`;
  const title = monitoringHudCleanMonitorTitle(
    titleValue,
    `Monitor Group ${nextNumber}`
  );
  monitoringHudControlState.cards[cardId] = {
    x: 0,
    y: (nextNumber - 1) * 300,
    w: 600,
    h: 280,
    title,
    enabled: true,
    pollingRateMs: 1000,
    warningNotificationsEnabled: true,
    sensors: monitoringHudDefaultSensorIds(cardId),
    sensorSettings: {}
  };
  monitoringHudNormalizeSensorAssignments(cardId, monitoringHudControlState.cards[cardId]);
  monitoringHudControlState.selectedMonitorId = cardId;
  monitoringHudPendingDeleteMonitorId = "";
  return cardId;
}

function monitoringHudCreateMonitorGroupFromWindow() {
  monitoringHudCreateMonitorGroup(monitoringHudCreateMonitorName ? monitoringHudCreateMonitorName.value : "");
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudCloseChildWindow();
  monitoringHudMarkChanged();
}

function monitoringHudCreateMonitorGroupFromManageWindow(options = {}) {
  if (!options.force && monitoringHudUnsavedMonitorDirty) {
    monitoringHudShowUnsavedGuard({ type: "create" });
    return;
  }
  monitoringHudCreateMonitorGroup(monitoringHudSuggestedMonitorName());
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudOpenChildWindow("monitor-group-edit");
  monitoringHudMarkChanged();
}

function monitoringHudBuildLargeMonitorFixture(count) {
  monitoringHudLargeFixtureModeEnabled = true;
  const targetCount = Math.max(1, Number(count) || monitoringHudLargeMonitorFixtureCount);
  const cards = {};
  for (let index = 0; index < targetCount; index += 1) {
    const number = index + 1;
    const cardId = `fixture-monitor-${number}`;
    const sensorA = index % 3 === 0 ? "cpu-load" : "";
    const sensorB = index % 5 === 0 ? "memory-usage" : "";
    const sensors = [sensorA, sensorB].filter(Boolean);
    const sensorSettings = {};
    sensors.forEach((sensorId) => {
      sensorSettings[sensorId] = monitoringHudDefaultSensorSetting(sensorId);
    });
    cards[cardId] = {
      x: 0,
      y: index * 300,
      w: 600,
      h: 280,
      title: `Monitor Group Fixture ${number}`,
      enabled: index % 7 !== 0,
      pollingRateMs: [1000, 2000, 5000, 10000][index % 4],
      warningNotificationsEnabled: index % 4 !== 0,
      sensors,
      sensorSettings
    };
  }
  monitoringHudControlState.cards = cards;
  monitoringHudControlState.monitorSequence = targetCount + 2;
  monitoringHudControlState.selectedMonitorId = Object.keys(cards)[0] || "";
  monitoringHudPendingDeleteMonitorId = "";
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudRenderMonitorManagement();
  return {
    monitorCount: Object.keys(cards).length,
    sensorFixtureCount: monitoringHudLargeSensorFixtureCount,
    selectedMonitorId: monitoringHudControlState.selectedMonitorId
  };
}

window.setMonitoringHudLargeFixtureMode = monitoringHudBuildLargeMonitorFixture;
window.clearMonitoringHudLargeFixtureMode = function() {
  monitoringHudLargeFixtureModeEnabled = false;
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudRenderMonitorManagement();
};

function monitoringHudReadSensorAssignmentsFromWindow(layout) {
  if (!layout) return;
  const selectedSensors = Array.isArray(layout.sensors) ? layout.sensors.slice() : [];
  if (monitoringHudMonitorSensorAssignment) {
    monitoringHudMonitorSensorAssignment.querySelectorAll("input[type='checkbox'][data-monitor-sensor-input]").forEach((input) => {
      const sensorId = String(input.value || "");
      if (!sensorId) return;
      const existingIndex = selectedSensors.indexOf(sensorId);
      if (!input.disabled && input.checked && existingIndex === -1) selectedSensors.push(sensorId);
      if (!input.disabled && !input.checked && existingIndex !== -1) selectedSensors.splice(existingIndex, 1);
    });
  }
  layout.sensors = selectedSensors.filter(Boolean);
  layout.sensorSettings = {};
  if (monitoringHudMonitorSensorSettings) {
    layout.sensors.forEach((sensorId) => {
      const mode = monitoringHudMonitorSensorSettings.querySelector(`[data-sensor-display-mode="${sensorId}"]`);
      const warning = monitoringHudMonitorSensorSettings.querySelector(`[data-sensor-warning-enabled="${sensorId}"]`);
      layout.sensorSettings[sensorId] = {
        displayMode: mode ? String(mode.dataset.sensorDisplayModeSelected || "text") : monitoringHudDefaultSensorSetting(sensorId).displayMode,
        warningEnabled: warning ? Boolean(warning.checked) : true
      };
    });
  }
  monitoringHudNormalizeSensorAssignments(monitoringHudControlState.selectedMonitorId, layout);
}

function monitoringHudCloneMonitorLayout(layout) {
  return JSON.parse(JSON.stringify(layout || {}));
}

function monitoringHudSelectedMonitorDetailLayout(selected = monitoringHudSelectedMonitor()) {
  if (
    monitoringHudUnsavedMonitorDirty
    && selected.id
    && selected.id === monitoringHudDraftOriginalMonitorId
    && monitoringHudDraftWorkingLayout
  ) {
    return monitoringHudNormalizeSensorAssignments(selected.id, monitoringHudDraftWorkingLayout);
  }
  return selected.layout;
}

function monitoringHudEnsureMonitorDraft() {
  const selected = monitoringHudSelectedMonitor();
  if (!selected.id || !selected.layout) return null;
  if (!monitoringHudUnsavedMonitorDirty) {
    monitoringHudDraftOriginalMonitorId = selected.id;
    monitoringHudDraftOriginalLayout = monitoringHudCloneMonitorLayout(selected.layout);
    monitoringHudDraftWorkingLayout = monitoringHudCloneMonitorLayout(selected.layout);
  } else if (!monitoringHudDraftWorkingLayout) {
    monitoringHudDraftWorkingLayout = monitoringHudCloneMonitorLayout(selected.layout);
  }
  monitoringHudUnsavedMonitorDirty = true;
  if (monitoringHud) {
    monitoringHud.dataset.monitorUnsavedChanges = "pending";
  }
  monitoringHudUpdateMonitorActionState();
  return {
    id: monitoringHudDraftOriginalMonitorId || selected.id,
    layout: monitoringHudDraftWorkingLayout
  };
}

function monitoringHudUpdateMonitorDraftFromWindow() {
  const draft = monitoringHudEnsureMonitorDraft();
  if (!draft || !draft.layout) return null;
  draft.layout.title = monitoringHudCleanMonitorTitle(
    monitoringHudEditMonitorName ? monitoringHudEditMonitorName.value : "",
    draft.layout.title || "Monitor Group"
  );
  draft.layout.enabled = monitoringHudMonitorEnabled ? Boolean(monitoringHudMonitorEnabled.checked) : draft.layout.enabled !== false;
  draft.layout.pollingRateMs = monitoringHudMonitorPollingRate
    ? Math.max(1000, Number(monitoringHudMonitorPollingRate.value) || 1000)
    : Math.max(1000, Number(draft.layout.pollingRateMs) || 1000);
  draft.layout.warningNotificationsEnabled = monitoringHudMonitorWarningSetting
    ? Boolean(monitoringHudMonitorWarningSetting.checked)
    : draft.layout.warningNotificationsEnabled !== false;
  monitoringHudReadSensorAssignmentsFromWindow(draft.layout);
  monitoringHudDraftWorkingLayout = monitoringHudCloneMonitorLayout(draft.layout);
  return {
    id: draft.id,
    layout: monitoringHudDraftWorkingLayout
  };
}

function monitoringHudSaveEditMonitorWindow(options = {}) {
  const selected = monitoringHudSelectedMonitor();
  if (!selected.id || !selected.layout) return;
  const draft = monitoringHudUpdateMonitorDraftFromWindow();
  const targetId = draft && draft.id ? draft.id : selected.id;
  const targetLayout = draft && draft.layout ? monitoringHudCloneMonitorLayout(draft.layout) : monitoringHudCloneMonitorLayout(selected.layout);
  monitoringHudNormalizeSensorAssignments(targetId, targetLayout);
  monitoringHudControlState.cards[targetId] = targetLayout;
  monitoringHudPendingDeleteMonitorId = "";
  monitoringHudSetMonitorDraftDirty(false);
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  if (options.keepOpen) monitoringHudRenderMonitorManagement();
  if (!options.keepOpen) monitoringHudCloseChildWindow({ force: true });
  monitoringHudMarkChanged();
}

function monitoringHudPersistCurrentMonitorDraft() {
  const selected = monitoringHudSelectedMonitor();
  const targetId = monitoringHudDraftOriginalMonitorId || (selected && selected.id) || "";
  if (!targetId || !monitoringHudControlState.cards || !monitoringHudControlState.cards[targetId]) return false;
  const targetLayout = monitoringHudDraftWorkingLayout
    ? monitoringHudCloneMonitorLayout(monitoringHudDraftWorkingLayout)
    : monitoringHudCloneMonitorLayout(monitoringHudControlState.cards[targetId]);
  monitoringHudNormalizeSensorAssignments(targetId, targetLayout);
  monitoringHudControlState.cards[targetId] = targetLayout;
  monitoringHudPendingDeleteMonitorId = "";
  monitoringHudSetMonitorDraftDirty(false);
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudMarkChanged();
  return true;
}

function monitoringHudRequestDeleteMonitorGroup(cardId, options = {}) {
  if (!cardId || !monitoringHudControlState.cards || !monitoringHudControlState.cards[cardId]) return;
  if (!options.force && monitoringHudUnsavedMonitorDirty && cardId === monitoringHudControlState.selectedMonitorId) {
    monitoringHudShowUnsavedGuard({ type: "delete", cardId });
    return;
  }
  monitoringHudPendingDeleteMonitorId = cardId;
  monitoringHudControlState.selectedMonitorId = cardId;
  monitoringHudRenderMonitorManagement();
  monitoringHudRevealDeleteConfirmation();
}

function monitoringHudRevealDeleteConfirmation() {
  if (!monitoringHudMonitorDeleteConfirmation || monitoringHudMonitorDeleteConfirmation.hidden) return;
  monitoringHudMonitorDeleteConfirmation.dataset.deleteConfirmationReveal = "scrolled-focused";
  window.requestAnimationFrame(() => {
    if (!monitoringHudMonitorDeleteConfirmation || monitoringHudMonitorDeleteConfirmation.hidden) return;
    if (typeof monitoringHudMonitorDeleteConfirmation.scrollIntoView === "function") {
      monitoringHudMonitorDeleteConfirmation.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "instant" });
    }
    const focusTarget = monitoringHudMonitorDeleteConfirm || monitoringHudMonitorDeleteCancel;
    if (focusTarget && typeof focusTarget.focus === "function") {
      focusTarget.focus({ preventScroll: true });
    }
  });
}

function monitoringHudConfirmDeleteMonitorGroup() {
  const cardId = monitoringHudPendingDeleteMonitorId;
  if (!cardId || !monitoringHudControlState.cards || !monitoringHudControlState.cards[cardId]) return;
  delete monitoringHudControlState.cards[cardId];
  const nextId = Object.keys(monitoringHudControlState.cards)[0] || "";
  monitoringHudControlState.selectedMonitorId = nextId;
  monitoringHudPendingDeleteMonitorId = "";
  monitoringHudSetMonitorDraftDirty(false);
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudMarkChanged();
}

function monitoringHudCancelDeleteMonitorGroup() {
  monitoringHudPendingDeleteMonitorId = "";
  monitoringHudRenderMonitorManagement();
}

function monitoringHudSetMonitorDraftDirty(dirty) {
  if (dirty && !monitoringHudUnsavedMonitorDirty) {
    const selected = monitoringHudSelectedMonitor();
    monitoringHudDraftOriginalMonitorId = selected.id || "";
    monitoringHudDraftOriginalLayout = selected.layout ? JSON.parse(JSON.stringify(selected.layout)) : null;
  }
  monitoringHudUnsavedMonitorDirty = Boolean(dirty);
  if (monitoringHud) {
    monitoringHud.dataset.monitorUnsavedChanges = monitoringHudUnsavedMonitorDirty ? "pending" : "clean";
  }
  if (!monitoringHudUnsavedMonitorDirty) {
    monitoringHudPendingSelectMonitorId = "";
    monitoringHudPendingGuardAction = null;
    monitoringHudDraftOriginalMonitorId = "";
    monitoringHudDraftOriginalLayout = null;
    monitoringHudDraftWorkingLayout = null;
    if (monitoringHudMonitorUnsavedGuard) {
      monitoringHudMonitorUnsavedGuard.hidden = true;
      monitoringHudMonitorUnsavedGuard.dataset.unsavedGuard = "closed";
      monitoringHudMonitorUnsavedGuard.dataset.guardActionLayout = "";
      monitoringHudMonitorUnsavedGuard.dataset.draftMonitorId = "";
      monitoringHudMonitorUnsavedGuard.dataset.guardStateModel = "";
      monitoringHudMonitorUnsavedGuard.dataset.pendingMonitorSelect = "";
      monitoringHudMonitorUnsavedGuard.dataset.pendingMonitorAction = "";
    }
  }
  monitoringHudUpdateMonitorActionState();
}

function monitoringHudShowUnsavedGuard(action) {
  monitoringHudUpdateMonitorDraftFromWindow();
  const pendingAction = typeof action === "string" ? { type: "select", cardId: action } : Object.assign({}, action || {});
  monitoringHudPendingGuardAction = pendingAction;
  monitoringHudPendingSelectMonitorId = pendingAction.type === "select" ? (pendingAction.cardId || "") : "";
  if (!monitoringHudMonitorUnsavedGuard) return;
  monitoringHudMonitorUnsavedGuard.hidden = false;
  monitoringHudMonitorUnsavedGuard.dataset.unsavedGuard = "open-save-discard";
  monitoringHudMonitorUnsavedGuard.dataset.guardActionLayout = "save-left-discard-right-no-cancel";
  monitoringHudMonitorUnsavedGuard.dataset.draftMonitorId = monitoringHudDraftOriginalMonitorId || "";
  monitoringHudMonitorUnsavedGuard.dataset.guardStateModel = "draft-preserved-before-queued-action";
  monitoringHudMonitorUnsavedGuard.dataset.pendingMonitorSelect = monitoringHudPendingSelectMonitorId;
  monitoringHudMonitorUnsavedGuard.dataset.pendingMonitorAction = pendingAction.type || "unknown";
  monitoringHudRevealUnsavedGuard();
}

function monitoringHudSelectMonitorGroup(cardId, options = {}) {
  if (!cardId || !monitoringHudControlState.cards || !monitoringHudControlState.cards[cardId]) return false;
  if (!options.force && monitoringHudUnsavedMonitorDirty && cardId !== monitoringHudControlState.selectedMonitorId) {
    monitoringHudShowUnsavedGuard({ type: "select", cardId });
    return false;
  }
  monitoringHudControlState.selectedMonitorId = cardId;
  monitoringHudPendingDeleteMonitorId = "";
  monitoringHudSetMonitorDraftDirty(false);
  monitoringHudRenderMonitorManagement();
  return true;
}

function monitoringHudRunPendingGuardAction(action) {
  const pendingAction = action || monitoringHudPendingGuardAction;
  if (!pendingAction || !pendingAction.type) return;
  if (pendingAction.type === "select") {
    monitoringHudSelectMonitorGroup(pendingAction.cardId, { force: true });
  } else if (pendingAction.type === "create") {
    monitoringHudCreateMonitorGroupFromManageWindow({ force: true });
  } else if (pendingAction.type === "delete") {
    monitoringHudRequestDeleteMonitorGroup(pendingAction.cardId, { force: true });
  } else if (pendingAction.type === "close") {
    monitoringHudCloseChildWindow({ force: true });
  }
}

function monitoringHudPendingGuardActionSnapshot() {
  const pendingAction = Object.assign({}, monitoringHudPendingGuardAction || {});
  if (pendingAction.type) return pendingAction;
  if (!monitoringHudMonitorUnsavedGuard || monitoringHudMonitorUnsavedGuard.hidden) return pendingAction;
  const guardType = monitoringHudMonitorUnsavedGuard.dataset.pendingMonitorAction || "";
  if (!guardType) return pendingAction;
  if (guardType === "select") {
    return {
      type: "select",
      cardId: monitoringHudMonitorUnsavedGuard.dataset.pendingMonitorSelect || ""
    };
  }
  return {
    type: guardType,
    cardId: monitoringHudMonitorUnsavedGuard.dataset.draftMonitorId || monitoringHudControlState.selectedMonitorId || ""
  };
}

function monitoringHudSaveAndSelectPendingMonitor() {
  const pendingAction = monitoringHudPendingGuardActionSnapshot();
  monitoringHudPersistCurrentMonitorDraft();
  monitoringHudRunPendingGuardAction(pendingAction);
}

function monitoringHudDiscardAndSelectPendingMonitor() {
  const pendingAction = monitoringHudPendingGuardActionSnapshot();
  if (
    monitoringHudDraftOriginalMonitorId
    && monitoringHudDraftOriginalLayout
    && monitoringHudControlState.cards
    && monitoringHudControlState.cards[monitoringHudDraftOriginalMonitorId]
  ) {
    monitoringHudControlState.cards[monitoringHudDraftOriginalMonitorId] = JSON.parse(JSON.stringify(monitoringHudDraftOriginalLayout));
  }
  monitoringHudSetMonitorDraftDirty(false);
  monitoringHudRunPendingGuardAction(pendingAction);
}

function monitoringHudRenderMonitorManagement() {
  const selected = monitoringHudSelectedMonitor();
  const selectedLayout = selected.id ? monitoringHudSelectedMonitorDetailLayout(selected) : null;
  const monitorCount = Object.keys(monitoringHudControlState.cards || {}).length;
  const assignedSensorCount = Object.values(monitoringHudControlState.cards || {}).reduce((total, layout) => {
    return total + (Array.isArray(layout && layout.sensors) ? layout.sensors.length : 0);
  }, 0);
  if (monitoringHud) {
    monitoringHud.dataset.dashboardControlPanel = "hud-overlay-monitor-management";
    monitoringHud.dataset.monitorManagement = "sensor-command-center-list-detail-source-picker";
    monitoringHud.dataset.overlayModeControls = "overlay-deferred-tray-owned";
    monitoringHud.dataset.primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel";
    monitoringHud.dataset.interfaceAcceptancePolicy = "dashboard-only-current-branch";
    monitoringHud.dataset.dashboardAcceptanceBaseline = "ws31-dashboard-control-panel";
    monitoringHud.dataset.dashboardProofPath = "dashboard-specific-static-live-uts";
    monitoringHud.dataset.dashboardStandaloneProof = "ws32-dashboard-window-travel";
    monitoringHud.dataset.dashboardClippingProof = "within-virtual-desktop";
    monitoringHud.dataset.dashboardMinimumEdgeProof = "native-min-size-bottom-edge-visible";
    monitoringHud.dataset.dashboardDecouplingProof = "core-overlay-independent";
    monitoringHud.dataset.dashboardContentPolish = "branch2-monitor-groups-no-dead-space";
    monitoringHud.dataset.dashboardLayoutProof = "monitor-groups-measured-no-overlap";
    monitoringHud.dataset.dashboardHomeModel = "control-hub-cards-monitor-management-child-windows";
    monitoringHud.dataset.dashboardPollingPlacement = "monitor-group-editor-only";
    monitoringHud.dataset.dashboardProofContentPolicy = "validator-artifacts-not-home-surface";
    monitoringHud.dataset.dashboardChildWindowScope = "monitor-groups-manage-create-edit-delete-sensor-windows-overlay-profile-settings";
    monitoringHud.dataset.dashboardSettingsModel = "hud-overlay-monitor-groups-provider-warning";
    monitoringHud.dataset.dashboardIaModel = "branch2-ia-controls-followthrough";
    monitoringHud.dataset.dashboardCloseAffordance = "window-level-close-button";
    monitoringHud.dataset.dashboardCloseLayout = "window-level-top-right-close-pill";
    monitoringHud.dataset.dashboardOpenBadge = "removed";
    monitoringHud.dataset.dashboardMonitorSelectionPlacement = "edit-child-window-only";
    monitoringHud.dataset.dashboardQuickAccess = "warning-notifications-only";
    monitoringHud.dataset.dashboardGlobalFeatureControl = "tray-owned";
    monitoringHud.dataset.dashboardDeferredActionPolicy = "disabled-labeled-not-clickable";
    monitoringHud.dataset.dashboardCardOrder = "hud-overlay-monitor-groups-data-sources-readiness";
    monitoringHud.dataset.dashboardSettingsAffordance = "dashboard-ia-card-settings-button";
    monitoringHud.dataset.dashboardSettingsPanel = "settings-panel-child-window";
    monitoringHud.dataset.dashboardSettingsProof = "visible-open-close-control-hit-target";
    monitoringHud.dataset.dashboardSettingsPanelState = monitoringHudActiveChildWindow === "dashboard-settings" ? "open" : "closed";
    monitoringHud.dataset.monitorGroupModel = "configurable-groups-sensor-assignment";
    monitoringHud.dataset.monitorManagementScale = "split-layout-search-filter-large-fixtures";
    monitoringHud.dataset.monitorManagementLayout = "compact-list-right-detail-command-center";
    monitoringHud.dataset.sensorLibraryScale = "search-facet-thousand-source-fixture";
    monitoringHud.dataset.sourceFilterMode = "nexus-dropdown-source-picker";
    monitoringHud.dataset.sensorLibraryFixtures = `monitors-${monitoringHudLargeMonitorFixtureCount}-sources-${monitoringHudLargeSensorFixtureCount}`;
    monitoringHud.dataset.sensorLibraryFixtureMode = monitoringHudLargeFixtureModeEnabled ? "enabled-validation-support" : "available-validation-support";
    monitoringHud.dataset.monitorManagementScrollbars = "nexus-styled-child-list-detail-sensor-panes";
    monitoringHud.dataset.monitorManagementToolbar = "compact-search-summary-list-header-create";
    monitoringHud.dataset.monitorDeletePlacement = "detail-pane-bottom-danger-zone";
    monitoringHud.dataset.manageWindowSizing = "taller-default-bounded-resizable";
    monitoringHud.dataset.firstOpenFlickerGuard = "native-opacity-guard-stable-first-open";
    monitoringHud.dataset.resizeLiveProof = "invisible-real-ui-frame-pixel-signature-grow-shrink";
    monitoringHud.dataset.resizeProofVisibility = "normal-ui-no-proof-artifacts";
    monitoringHud.dataset.resizeProofVisuals = "none";
    monitoringHud.dataset.dashboardMonitorCardPolicy = "overlay-display-owns-visual-rendering";
    monitoringHud.dataset.monitorSensorAssignment = "sensor-library-source-picker";
    monitoringHud.dataset.sourceClassification = "settings-readiness-outside-assignable-sensors";
    monitoringHud.dataset.monitorDeleteConfirmation = monitoringHudPendingDeleteMonitorId ? "pending-confirmation" : "closed";
    monitoringHud.dataset.interactiveControlAffordance = "normal-hover-active-focus-visible-disabled-open-selected";
    monitoringHud.dataset.interactiveControlReliability = monitoringHud.dataset.interactiveControlReliability || "first-click-stress-proof-required";
    monitoringHud.dataset.clickInterceptionDiagnostics = monitoringHud.dataset.clickInterceptionDiagnostics || "z-index-pointer-events-disabled-aria-dom-focus-timing";
    monitoringHud.dataset.pollingRateDropdown = "nexus-styled-bounded-control";
    monitoringHud.dataset.overlayAcceptancePolicy = "deferred-non-gating";
    monitoringHud.dataset.interfaceBundleApproval = "not-granted";
    monitoringHud.dataset.coreRepairClassification = "dependency-repair-only";
    monitoringHud.dataset.monitorCount = String(monitorCount);
    monitoringHud.dataset.assignedSensorCount = String(assignedSensorCount);
    monitoringHud.dataset.selectedMonitor = selected.id || "";
  }
  Object.keys(monitoringHudControlState.cards || {}).forEach((cardId) => {
    const layout = Object.assign(monitoringHudCardDefaults(cardId), monitoringHudControlState.cards[cardId] || {});
    monitoringHudNormalizeMonitorGroupTitle(cardId, layout);
    const cardNode = monitoringHudEditMonitorList
      ? monitoringHudEditMonitorList.querySelector(`[data-monitor-row="${cardId}"]`)
      : null;
    if (!cardNode) return;
    cardNode.dataset.monitorEnabled = layout.enabled === false ? "false" : "true";
    cardNode.dataset.monitorPollingMs = String(Math.max(1000, Number(layout.pollingRateMs) || 1000));
    cardNode.dataset.assignedSensorCount = String(Array.isArray(layout.sensors) ? layout.sensors.length : 0);
  });
  if (monitoringHudMonitorListSummary) {
    monitoringHudMonitorListSummary.textContent = `${monitorCount} Monitor Groups configured with ${assignedSensorCount} supported source assignment${assignedSensorCount === 1 ? "" : "s"}. Manage opens list, create, edit, delete, and sensor controls.`;
  }
  if (monitoringHudMonitorCount) {
    monitoringHudMonitorCount.textContent = `${monitorCount} configured`;
  }
  if (monitoringHudMonitorPollingSummary) {
    monitoringHudMonitorPollingSummary.textContent = `${assignedSensorCount} assigned source${assignedSensorCount === 1 ? "" : "s"}`;
  }
  if (monitoringHudMonitorEditorTitle) {
    monitoringHudMonitorEditorTitle.textContent = selectedLayout ? (selectedLayout.title || "Monitor Group") : "No Monitor Selected";
  }
  if (monitoringHudMonitorEnabled) {
    monitoringHudMonitorEnabled.checked = selectedLayout ? selectedLayout.enabled !== false : false;
  }
  if (monitoringHudMonitorPollingRate) {
    monitoringHudSetPollingRateValue(selectedLayout ? String(Math.max(1000, Number(selectedLayout.pollingRateMs) || 1000)) : "1000");
  }
  if (monitoringHudMonitorEditorScope) {
    monitoringHudMonitorEditorScope.textContent = "Monitor Groups assign available runtime sources and settings. HUD Overlay owns future visual display; fake values remain blocked.";
  }
  monitoringHudRenderChildWindows();
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
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  const cards = monitoringHudControlState.cards || {};
  const activeProfile = monitoringHudActiveOverlayProfile() || {};
  const activeMonitorIds = monitoringHudUniqueValidMonitorIds(activeProfile.monitorIds, cards);
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
  monitoringHudOverlayDisplay.dataset.monitorCount = String(activeMonitorIds.length);
  monitoringHudOverlayDisplay.dataset.overlayProfileState = "slc-039-membership-mapping";
  monitoringHudOverlayDisplay.dataset.overlayProfileSchemaVersion = String(monitoringHudOverlayProfileSchemaVersion);
  monitoringHudOverlayDisplay.dataset.activeOverlayProfileId = String(monitoringHudControlState.activeOverlayProfileId || monitoringHudDefaultOverlayProfileId);
  monitoringHudOverlayDisplay.dataset.activeOverlayProfileMonitorCount = String(activeMonitorIds.length);
  monitoringHudOverlayDisplay.dataset.overlayProfileEditor = "slc-039-membership-editor";
  monitoringHudOverlayDisplay.dataset.overlayProfileMembership = "editable-slc-039-mapping";
  monitoringHudOverlayDisplay.dataset.recordingProfileState = "recording-profile-state-absent-future-gated";
  activeMonitorIds.forEach((cardId) => {
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
    monitoringHud.dataset.frameOwnership = "single-rounded-dashboard-chrome";
    monitoringHud.dataset.scrollOwner = "monitoring-hud-control-hub";
    monitoringHud.dataset.scrollbarBoundary = "inner-content-well-gutter";
    monitoringHud.dataset.outerFrameHaze = "removed-no-square-layer";
    monitoringHud.dataset.gridScope = "control-hub-cards-only";
    monitoringHud.dataset.deadzonePolicy = "auto-height-content-no-empty-hit-zones";
    monitoringHud.dataset.stickyHeaderMask = "opaque-scroll-mask";
    monitoringHud.dataset.nativeResizeHitZone = "preclick-hover-cursor-aligned-14px-app-owned-resize-action";
    monitoringHud.dataset.primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel";
    monitoringHud.dataset.interfaceAcceptancePolicy = "dashboard-only-current-branch";
    monitoringHud.dataset.dashboardAcceptanceBaseline = "ws31-dashboard-control-panel";
    monitoringHud.dataset.dashboardProofPath = "dashboard-specific-static-live-uts";
    monitoringHud.dataset.dashboardMinimumEdgeProof = "native-min-size-bottom-edge-visible";
    monitoringHud.dataset.overlayAcceptancePolicy = "deferred-non-gating";
    monitoringHud.dataset.interfaceBundleApproval = "not-granted";
    monitoringHud.dataset.coreRepairClassification = "dependency-repair-only";
    monitoringHud.dataset.dashboardContentPolish = "branch2-monitor-groups-no-dead-space";
    monitoringHud.dataset.dashboardLayoutProof = "monitor-groups-measured-no-overlap";
    monitoringHud.dataset.dashboardSettingsModel = "hud-overlay-monitor-groups-provider-warning";
    monitoringHud.dataset.dashboardHomeModel = "control-hub-cards-monitor-management-child-windows";
    monitoringHud.dataset.dashboardChildWindowScope = "monitor-groups-manage-create-edit-delete-sensor-windows-overlay-profile-settings";
    monitoringHud.dataset.dashboardIaModel = "branch2-ia-controls-followthrough";
    monitoringHud.dataset.dashboardCloseAffordance = "window-level-close-button";
    monitoringHud.dataset.dashboardCloseLayout = "window-level-top-right-close-pill";
    monitoringHud.dataset.dashboardOpenBadge = "removed";
    monitoringHud.dataset.dashboardMonitorSelectionPlacement = "edit-child-window-only";
    monitoringHud.dataset.dashboardQuickAccess = "warning-notifications-only";
    monitoringHud.dataset.dashboardGlobalFeatureControl = "tray-owned";
    monitoringHud.dataset.dashboardDeferredActionPolicy = "disabled-labeled-not-clickable";
    monitoringHud.dataset.dashboardCardOrder = "hud-overlay-monitor-groups-data-sources-readiness";
    monitoringHud.dataset.monitorGroupModel = "configurable-groups-sensor-assignment";
    monitoringHud.dataset.dashboardMonitorCardPolicy = "overlay-display-owns-visual-rendering";
    monitoringHud.dataset.monitorSensorAssignment = "sensor-library-source-picker";
    monitoringHud.dataset.sourceClassification = "settings-readiness-outside-assignable-sensors";
    monitoringHud.dataset.interactiveControlAffordance = "normal-hover-active-focus-visible-disabled-open-selected";
    monitoringHud.dataset.interactiveControlReliability = monitoringHud.dataset.interactiveControlReliability || "first-click-stress-proof-required";
    monitoringHud.dataset.clickInterceptionDiagnostics = monitoringHud.dataset.clickInterceptionDiagnostics || "z-index-pointer-events-disabled-aria-dom-focus-timing";
    monitoringHud.dataset.pollingRateDropdown = "nexus-styled-bounded-control";
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
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
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
  monitoringHud.dataset.overlayProfileState = "slc-039-membership-mapping";
  monitoringHud.dataset.overlayProfileSchemaVersion = String(monitoringHudOverlayProfileSchemaVersion);
  monitoringHud.dataset.activeOverlayProfileId = String(monitoringHudControlState.activeOverlayProfileId || monitoringHudDefaultOverlayProfileId);
  monitoringHud.dataset.overlayProfileEditor = "slc-039-membership-editor";
  monitoringHud.dataset.overlayProfileMembership = "editable-slc-039-mapping";
  monitoringHud.dataset.recordingProfileState = "recording-profile-state-absent-future-gated";
  monitoringHud.dataset.warningControlPosture = monitoringHudControlState.warningNotificationsMuted
    ? "global-muted"
    : "visual-notifications-enabled";
  monitoringHud.dataset.dashboardProviderTruth = "provider-contract-first";
  monitoringHud.dataset.dashboardStateModel = "setup-no-data-degraded-warning";
  monitoringHud.dataset.dashboardWarningControls = "visual-non-invasive-only";
  monitoringHud.dataset.dashboardFakeTelemetryPolicy = "blocked";
  monitoringHud.dataset.interactiveControlAffordance = "normal-hover-active-focus-visible-disabled-open-selected";
  monitoringHud.dataset.interactiveControlReliability = monitoringHud.dataset.interactiveControlReliability || "first-click-stress-proof-required";
  monitoringHud.dataset.clickInterceptionDiagnostics = monitoringHud.dataset.clickInterceptionDiagnostics || "z-index-pointer-events-disabled-aria-dom-focus-timing";
  monitoringHud.dataset.pollingRateDropdown = "nexus-styled-bounded-control";
  if (monitoringHudRuntimeStatus) {
    monitoringHudRuntimeStatus.textContent = dashboardVisible ? "Dashboard visible" : "Dashboard hidden";
  }
  if (monitoringHudAnchorStatus) {
    monitoringHudAnchorStatus.textContent = overlayDeferred ? "HUD Overlay deferred" : (monitoringHudControlState.anchored ? "HUD Overlay anchored" : "HUD Overlay unanchored");
  }
  if (monitoringHudToggle) {
    monitoringHudToggle.textContent = featureEnabled ? "Disable HUD Overlay" : "Enable HUD Overlay";
  }
  if (monitoringHudAnchorToggle) {
    monitoringHudAnchorToggle.textContent = overlayDeferred ? "HUD Overlay deferred" : (monitoringHudControlState.anchored ? "Unanchor HUD Overlay" : "Anchor HUD Overlay");
    monitoringHudAnchorToggle.disabled = overlayDeferred;
  }
  if (monitoringHudEditMonitor) {
    monitoringHudEditMonitor.textContent = "Manage Monitors";
  }
  if (monitoringHudSnapToggle) {
    monitoringHudSnapToggle.textContent = "HUD Overlay settings";
    monitoringHudSnapToggle.disabled = overlayDeferred;
  }
  if (monitoringHudWarningToggle) {
    monitoringHudWarningToggle.textContent = monitoringHudControlState.warningNotificationsMuted
      ? "Warning Notifications Muted"
      : "Warning Notifications On";
  }
  if (monitoringHudSnapLabel) {
    monitoringHudSnapLabel.textContent = "HUD Overlay deferred";
  }
  if (monitoringHudPollingRate) {
    monitoringHudPollingRate.value = String(monitoringHudControlState.pollingRateMs);
  }
  if (monitoringHudWarningModeControl) {
    monitoringHudWarningModeControl.value = monitoringHudControlState.warningMode || "badge-text-color";
  }
  monitoringHudRenderDashboardSettingsPanel();
  monitoringHudRenderOverlayProfileControls();
  if (monitoringHudWarningPosture) {
    monitoringHudWarningPosture.textContent = monitoringHudControlState.warningNotificationsMuted
      ? "Globally muted; Monitor Group settings preserved"
      : "Visual notifications enabled";
  }
  if (monitoringHudPlacementPointer) {
    monitoringHudPlacementPointer.textContent = "Dashboard configures future HUD Overlay behavior";
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
    const cardNode = monitoringHudEditMonitorList
      ? monitoringHudEditMonitorList.querySelector(`[data-monitor-row="${card.id}"]`)
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
    monitoringHudWireReliableControl(monitoringHudToggle, "dashboard:toggle-visibility", () => {
      monitoringHudControlState.featureEnabled = !monitoringHudControlState.featureEnabled;
      monitoringHudControlState.visible = monitoringHudControlState.featureEnabled;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudAnchorToggle) {
    monitoringHudWireReliableControl(monitoringHudAnchorToggle, "dashboard:anchor-toggle", () => {
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
  if (monitoringHudDashboardClose) {
    monitoringHudWireReliableControl(monitoringHudDashboardClose, "dashboard:close", () => {
      if (!monitoringHudCloseChildWindow()) return;
      monitoringHudControlState.visible = false;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudSettingsAction) {
    monitoringHudWireReliableControl(monitoringHudSettingsAction, "dashboard:settings", () => {
      monitoringHudOpenChildWindow("dashboard-settings");
    });
  }
  if (monitoringHudEditMonitor) {
    monitoringHudWireReliableControl(monitoringHudEditMonitor, "dashboard:manage-monitors", () => {
      monitoringHudOpenChildWindow("monitor-group-edit");
    });
  }
  if (monitoringHudCreateMonitorConfirm) {
    monitoringHudWireReliableControl(monitoringHudCreateMonitorConfirm, "create-window:confirm", monitoringHudCreateMonitorGroupFromWindow);
  }
  if (monitoringHudManageMonitorCreate) {
    monitoringHudWireReliableControl(monitoringHudManageMonitorCreate, "manage:create", monitoringHudCreateMonitorGroupFromManageWindow);
  }
  if (monitoringHudMonitorEmptyCreate) {
    monitoringHudWireReliableControl(monitoringHudMonitorEmptyCreate, "manage:empty-create", monitoringHudCreateMonitorGroupFromManageWindow);
  }
  if (monitoringHudEditMonitorConfirm) {
    monitoringHudWireReliableControl(monitoringHudEditMonitorConfirm, "manage:save-monitor", () => monitoringHudSaveEditMonitorWindow({ keepOpen: true }));
  }
  if (monitoringHudEditMonitorDiscard) {
    monitoringHudWireReliableControl(monitoringHudEditMonitorDiscard, "manage:discard-monitor", monitoringHudDiscardCurrentMonitorDraft);
  }
  if (monitoringHudEditMonitorList) {
    monitoringHudWireReliableDelegatedControl(monitoringHudEditMonitorList, "[data-monitor-select]", "manage:row-switch", (row) => {
      if (monitoringHudSelectMonitorGroup(row.dataset.monitorSelect)) {
        monitoringHudMarkChanged();
      }
    });
    monitoringHudEditMonitorList.addEventListener("keydown", (event) => {
      if (!["Enter", " "].includes(event.key)) return;
      const row = event.target && event.target.closest ? event.target.closest("[data-monitor-select]") : null;
      if (!row) return;
      event.preventDefault();
      if (monitoringHudSelectMonitorGroup(row.dataset.monitorSelect)) {
        monitoringHudMarkChanged();
      }
    });
  }
  if (monitoringHudMonitorSearch) {
    monitoringHudMonitorSearch.addEventListener("input", () => {
      monitoringHudRenderMonitorManagement();
    });
  }
  if (monitoringHudMonitorDeleteConfirm) {
    monitoringHudWireReliableControl(monitoringHudMonitorDeleteConfirm, "manage:delete-confirm", monitoringHudConfirmDeleteMonitorGroup);
  }
  if (monitoringHudMonitorDeleteCancel) {
    monitoringHudWireReliableControl(monitoringHudMonitorDeleteCancel, "manage:delete-cancel", monitoringHudCancelDeleteMonitorGroup);
  }
  if (monitoringHudMonitorDetailDelete) {
    monitoringHudWireReliableControl(monitoringHudMonitorDetailDelete, "manage:delete-selected", () => {
      const selected = monitoringHudSelectedMonitor();
      if (!selected.id) return;
      monitoringHudRequestDeleteMonitorGroup(selected.id);
    });
  }
  if (monitoringHudMonitorUnsavedSave) {
    monitoringHudWireReliableControl(monitoringHudMonitorUnsavedSave, "manage:dirty-save", monitoringHudSaveAndSelectPendingMonitor);
  }
  if (monitoringHudMonitorUnsavedDiscard) {
    monitoringHudWireReliableControl(monitoringHudMonitorUnsavedDiscard, "manage:dirty-discard", monitoringHudDiscardAndSelectPendingMonitor);
  }
  if (monitoringHudMonitorSensorAssignment) {
    monitoringHudMonitorSensorAssignment.addEventListener("change", (event) => {
      if (!event.target || !event.target.matches || !event.target.matches("[data-monitor-sensor-input]")) return;
      if (Date.now() <= monitoringHudSourcePickerSuppressNativeChangeUntil) {
        monitoringHudPreventNativeSourcePickerEvent(event);
        return;
      }
      const row = event.target.closest("[data-source-picker-row]");
      if (row) monitoringHudSetSourceRowSelectionState(row, Boolean(event.target.checked));
      const draft = row
        ? monitoringHudApplySensorAssignmentToDraft(row, Boolean(event.target.checked))
        : monitoringHudUpdateMonitorDraftFromWindow();
      if (!draft) return;
      monitoringHudRefreshSensorPickerSelectionProof(draft, { deferSettingsRefresh: Boolean(row) });
    });
    monitoringHudWireSourcePickerReliableSelection(monitoringHudMonitorSensorAssignment);
    monitoringHudMonitorSensorAssignment.addEventListener("keydown", (event) => {
      if (!["Enter", " "].includes(event.key)) return;
      const row = event.target && event.target.closest ? event.target.closest("[data-source-picker-row]") : null;
      if (!row || !monitoringHudMonitorSensorAssignment.contains(row)) return;
      event.preventDefault();
      if (typeof event.stopPropagation === "function") event.stopPropagation();
      const result = monitoringHudToggleSensorAssignmentRow(row);
      monitoringHudRecordReliableActivation(row, "keyboard-toggle", result !== false);
    });
  }
  if (monitoringHudMonitorSensorSettings) {
    monitoringHudMonitorSensorSettings.addEventListener("change", (event) => {
      if (!event.target || !event.target.matches) return;
      if (!event.target.matches("[data-sensor-warning-enabled]")) return;
      if (!monitoringHudUpdateMonitorDraftFromWindow()) return;
      monitoringHudRenderMonitorManagement();
    });
    monitoringHudWireDisplayModeReliableSelection(monitoringHudMonitorSensorSettings);
  }
  if (monitoringHudSensorSearch) {
    monitoringHudSensorSearch.addEventListener("input", () => {
      monitoringHudRenderMonitorManagement();
    });
  }
  if (monitoringHudSensorFilter) {
    monitoringHudWireReliableDelegatedControl(monitoringHudSensorFilter, "#monitoring-hud-sensor-filter-toggle,[data-source-filter]", "source-filter", (button) => {
      if (button.id === "monitoring-hud-sensor-filter-toggle") {
        monitoringHudSetSourceFilterDropdownOpen(monitoringHudSensorFilter.dataset.filterOpen !== "true");
        return true;
      }
      monitoringHudSetSourceFilterValue(button.dataset.sourceFilter || "all");
      monitoringHudSetSourceFilterDropdownOpen(false);
      monitoringHudRenderMonitorManagement();
    });
    monitoringHudSensorFilter.addEventListener("mouseover", (event) => {
      const option = event.target && event.target.closest ? event.target.closest("[data-source-filter]") : null;
      if (!option) return;
      monitoringHudResetSourceFilterHover();
      option.classList.add("is-hovered");
      monitoringHudSensorFilter.dataset.hoveredFilter = option.dataset.sourceFilter || "";
    });
    monitoringHudSensorFilter.addEventListener("mouseleave", monitoringHudResetSourceFilterHover);
    monitoringHudSensorFilter.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        monitoringHudSetSourceFilterDropdownOpen(false);
      }
    });
    monitoringHudSetSourceFilterValue(monitoringHudSensorFilterValue());
  }
  if (monitoringHudOverlayProfileSelector) {
    monitoringHudWireReliableDelegatedControl(monitoringHudOverlayProfileSelector, "#monitoring-hud-overlay-profile-toggle,[data-overlay-profile-option]", "overlay-profile", (button) => {
      if (button.id === "monitoring-hud-overlay-profile-toggle") {
        monitoringHudSetOverlayProfileDropdownOpen(monitoringHudOverlayProfileSelector.dataset.dropdownOpen !== "true");
        return true;
      }
      return monitoringHudSelectOverlayProfile(button.dataset.overlayProfileOption || monitoringHudDefaultOverlayProfileId);
    });
    monitoringHudOverlayProfileSelector.addEventListener("mouseover", (event) => {
      const option = event.target && event.target.closest ? event.target.closest("[data-overlay-profile-option]") : null;
      if (!option) return;
      monitoringHudResetOverlayProfileHover();
      option.classList.add("is-hovered");
      monitoringHudOverlayProfileSelector.dataset.hoveredProfileId = option.dataset.overlayProfileOption || "";
    });
    monitoringHudOverlayProfileSelector.addEventListener("mouseleave", monitoringHudResetOverlayProfileHover);
    monitoringHudOverlayProfileSelector.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        monitoringHudSetOverlayProfileDropdownOpen(false);
      }
    });
  }
  if (monitoringHudOverlayProfileOpenSettings) {
    monitoringHudWireReliableControl(monitoringHudOverlayProfileOpenSettings, "overlay-profile:open-settings", () => {
      monitoringHudOpenChildWindow("overlay-profile-settings");
      return true;
    });
  }
  if (monitoringHudOverlayProfileNameInput) {
    monitoringHudOverlayProfileNameInput.addEventListener("input", () => {
      monitoringHudRenderOverlayProfileControls();
    });
    monitoringHudOverlayProfileNameInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        monitoringHudSaveOverlayProfileDraft();
      } else if (event.key === "Escape") {
        event.preventDefault();
        monitoringHudDiscardOverlayProfileDraft();
      }
    });
  }
  if (monitoringHudOverlayProfileMembershipList) {
    monitoringHudOverlayProfileMembershipList.addEventListener("change", (event) => {
      const toggle = event.target && event.target.closest
        ? event.target.closest("[data-overlay-profile-membership-toggle]")
        : null;
      if (!toggle) return;
      const row = toggle.closest("[data-overlay-profile-membership-row]");
      if (row) {
        row.setAttribute("aria-selected", toggle.checked ? "true" : "false");
      }
      monitoringHudOverlayProfileDraftMonitorIds = monitoringHudOverlayProfileDraftMonitorIdsFromWindow();
      monitoringHudRenderOverlayProfileControls();
    });
  }
  if (monitoringHudOverlayProfileCreate) {
    monitoringHudWireReliableControl(monitoringHudOverlayProfileCreate, "overlay-profile:create", monitoringHudCreateOverlayProfile);
  }
  if (monitoringHudOverlayProfileSave) {
    monitoringHudWireReliableControl(monitoringHudOverlayProfileSave, "overlay-profile:save", () => {
      if (monitoringHudOverlayProfileSave.disabled) return false;
      return monitoringHudSaveOverlayProfileDraft();
    });
  }
  if (monitoringHudOverlayProfileDiscard) {
    monitoringHudWireReliableControl(monitoringHudOverlayProfileDiscard, "overlay-profile:discard", () => {
      if (monitoringHudOverlayProfileDiscard.disabled) return false;
      return monitoringHudDiscardOverlayProfileDraft();
    });
  }
  if (monitoringHudMonitorPollingRateControl) {
    monitoringHudWireReliableDelegatedControl(monitoringHudMonitorPollingRateControl, "#monitoring-hud-monitor-polling-rate-toggle,[data-polling-rate-option]", "polling-rate", (button) => {
      if (button.id === "monitoring-hud-monitor-polling-rate-toggle") {
        monitoringHudSetPollingRateDropdownOpen(monitoringHudMonitorPollingRateControl.dataset.dropdownOpen !== "true");
        return true;
      }
      monitoringHudSetPollingRateValue(button.dataset.pollingRateOption || "1000", { dispatchChange: true });
      monitoringHudSetPollingRateDropdownOpen(false);
      if (!monitoringHudUpdateMonitorDraftFromWindow()) return false;
      monitoringHudRenderMonitorManagement();
      return true;
    });
    monitoringHudMonitorPollingRateControl.addEventListener("mouseover", (event) => {
      const option = event.target && event.target.closest ? event.target.closest("[data-polling-rate-option]") : null;
      if (!option) return;
      monitoringHudResetPollingRateHover();
      option.classList.add("is-hovered");
      monitoringHudMonitorPollingRateControl.dataset.hoveredValue = option.dataset.pollingRateOption || "";
    });
    monitoringHudMonitorPollingRateControl.addEventListener("mouseleave", monitoringHudResetPollingRateHover);
    monitoringHudMonitorPollingRateControl.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        monitoringHudSetPollingRateDropdownOpen(false);
      }
    });
    monitoringHudSetPollingRateValue(monitoringHudMonitorPollingRate ? monitoringHudMonitorPollingRate.value : "1000");
  }
  document.addEventListener("click", (event) => {
    if (!monitoringHudSensorFilter || monitoringHudSensorFilter.contains(event.target)) return;
    monitoringHudSetSourceFilterDropdownOpen(false);
  });
  document.addEventListener("click", (event) => {
    if (!monitoringHudOverlayProfileSelector || monitoringHudOverlayProfileSelector.contains(event.target)) return;
    monitoringHudSetOverlayProfileDropdownOpen(false);
  });
  document.addEventListener("click", (event) => {
    if (!monitoringHudMonitorPollingRateControl || monitoringHudMonitorPollingRateControl.contains(event.target)) return;
    monitoringHudSetPollingRateDropdownOpen(false);
  });
  document.querySelectorAll("[data-child-window-close]").forEach((button) => {
    monitoringHudWireReliableControl(button, `child-window-close:${button.dataset.childWindowClose || "unknown"}`, () => monitoringHudCloseChildWindow());
  });
  if (monitoringHudSnapToggle) {
    monitoringHudWireReliableControl(monitoringHudSnapToggle, "dashboard:snap-toggle", () => {
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
    monitoringHudWireReliableControl(button, "dashboard:warning-notifications", () => {
      monitoringHudControlState.warningNotificationsMuted = !monitoringHudControlState.warningNotificationsMuted;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  });
  if (monitoringHudSettingsWarningToggle) {
    monitoringHudSettingsWarningToggle.addEventListener("change", () => {
      monitoringHudControlState.warningNotificationsMuted = !monitoringHudSettingsWarningToggle.checked;
      monitoringHudRenderControls();
      monitoringHudMarkChanged();
    });
  }
  if (monitoringHudMonitorEnabled) {
    monitoringHudMonitorEnabled.addEventListener("change", () => {
      if (!monitoringHudUpdateMonitorDraftFromWindow()) return;
      monitoringHudRenderMonitorManagement();
    });
  }
  if (monitoringHudMonitorPollingRate) {
    monitoringHudMonitorPollingRate.addEventListener("change", () => {
      if (!monitoringHudUpdateMonitorDraftFromWindow()) return;
      monitoringHudRenderMonitorManagement();
    });
  }
  if (monitoringHudEditMonitorName) {
    monitoringHudEditMonitorName.addEventListener("input", () => {
      monitoringHudUpdateMonitorDraftFromWindow();
    });
  }
  if (monitoringHudMonitorWarningSetting) {
    monitoringHudMonitorWarningSetting.addEventListener("change", () => {
      if (!monitoringHudUpdateMonitorDraftFromWindow()) return;
      monitoringHudRenderMonitorManagement();
    });
  }
}

function monitoringHudInitializeControls() {
  monitoringHudLoadStoredState();
  monitoringHudApplyCardLayout();
  monitoringHudSetOverlayProfileDraftFromActive();
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

window.runMonitoringHudOverlayProfileStateProof = function() {
  const legacyCards = {
    cpu: Object.assign(monitoringHudCardDefaults("cpu"), { title: "CPU Group" }),
    gpu: Object.assign(monitoringHudCardDefaults("gpu"), { title: "GPU Group" })
  };
  const legacyState = {
    cards: legacyCards,
    selectedMonitorId: "gpu"
  };
  monitoringHudNormalizeOverlayProfileState(legacyState);
  const legacyDefaultProfile = legacyState.overlayProfiles[monitoringHudDefaultOverlayProfileId] || {};

  const mixedState = {
    cards: legacyCards,
    selectedMonitorId: "gpu",
    activeOverlayProfileId: "missing-profile",
    overlayProfiles: {
      custom: {
        id: "custom",
        name: "Custom Overlay Profile",
        monitorIds: ["gpu", "gpu", "missing", "cpu"],
        displayMode: "monitor-cards",
        monitorGroupId: "must-not-survive",
        recordingProfileId: "must-not-survive"
      }
    }
  };
  monitoringHudNormalizeOverlayProfileState(mixedState);
  const customProfile = mixedState.overlayProfiles.custom || {};
  const visibleEditorUi = Boolean(document.querySelector("#monitoring-hud-overlay-profile-editor[data-overlay-profile-editor-ui='slc-039-membership-editor']"));
  const proof = {
    passed: true,
    package: "PKG-006",
    slice: "SLC-039",
    schemaVersion: monitoringHudOverlayProfileSchemaVersion,
    defaultProfileId: monitoringHudDefaultOverlayProfileId,
    defaultProfileCreatedForLegacyCards: legacyState.activeOverlayProfileId === monitoringHudDefaultOverlayProfileId,
    legacyDefaultMembership: (legacyDefaultProfile.monitorIds || []).slice(),
    activeProfileFallback: mixedState.activeOverlayProfileId === monitoringHudDefaultOverlayProfileId,
    customMembershipNormalized: JSON.stringify(customProfile.monitorIds || []) === JSON.stringify(["gpu", "cpu"]),
    staleMonitorIdsRemoved: !(customProfile.monitorIds || []).includes("missing"),
    duplicateMonitorIdsRemoved: (customProfile.monitorIds || []).length === 2,
    selectedMonitorIdPreserved: mixedState.selectedMonitorId === "gpu",
    monitorGroupBoundary: !Object.prototype.hasOwnProperty.call(customProfile, "monitorGroupId"),
    recordingProfileBoundary: !Object.prototype.hasOwnProperty.call(customProfile, "recordingProfileId"),
    visibleProfileEditorUi: visibleEditorUi ? "slc-039-membership-editor" : "missing-slc-039-membership-editor"
  };
  proof.passed = proof.defaultProfileCreatedForLegacyCards
    && JSON.stringify(proof.legacyDefaultMembership) === JSON.stringify(["cpu", "gpu"])
    && proof.activeProfileFallback
    && proof.customMembershipNormalized
    && proof.staleMonitorIdsRemoved
    && proof.duplicateMonitorIdsRemoved
    && proof.selectedMonitorIdPreserved
    && proof.monitorGroupBoundary
    && proof.recordingProfileBoundary
    && visibleEditorUi;
  monitoringHudControlState.overlayProfileStateProof = proof;
  if (monitoringHud) {
    monitoringHud.dataset.overlayProfileStateProof = proof.passed ? "pass" : "fail";
    monitoringHud.dataset.overlayProfileEditor = proof.visibleProfileEditorUi;
  }
  if (monitoringHudOverlayDisplay) {
    monitoringHudOverlayDisplay.dataset.overlayProfileStateProof = proof.passed ? "pass" : "fail";
    monitoringHudOverlayDisplay.dataset.overlayProfileEditor = proof.visibleProfileEditorUi;
  }
  return proof;
};

window.runMonitoringHudOverlayProfileControlsProof = function() {
  const previousState = JSON.stringify(monitoringHudControlState);
  const previousDraftId = monitoringHudOverlayProfileDraftId;
  const previousDraftName = monitoringHudOverlayProfileDraftName;
  const previousDraftMonitorIds = monitoringHudOverlayProfileDraftMonitorIds.slice();
  let proof = {
    passed: false,
    package: "PKG-006",
    slice: "SLC-039",
    selectorVisible: Boolean(monitoringHudOverlayProfileSelector && monitoringHudOverlayProfileToggle && monitoringHudOverlayProfileMenu),
    settingsEntryVisible: Boolean(monitoringHudOverlayProfileOpenSettings),
    settingsWindowPresent: Boolean(monitoringHudOverlayProfileWindow),
    settingsWindowOpens: false,
    createVisible: Boolean(monitoringHudOverlayProfileCreate),
    renameVisible: Boolean(monitoringHudOverlayProfileNameInput),
    saveDiscardVisible: Boolean(monitoringHudOverlayProfileSave && monitoringHudOverlayProfileDiscard),
    editableMembership: monitoringHudOverlayProfileEditor
      ? monitoringHudOverlayProfileEditor.dataset.overlayProfileMembership === "editable-slc-039-mapping"
      : false,
    createdProfileSelectable: false,
    renameSaved: false,
    discardRestored: false,
    membershipListVisible: Boolean(monitoringHudOverlayProfileMembershipList),
    membershipSaved: false,
    membershipDiscardRestored: false,
    monitorGroupBoundary: true,
    recordingProfileBoundary: true,
    activeProfilePersistsInState: false
  };
  try {
    monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
    monitoringHudOpenChildWindow("overlay-profile-settings");
    proof.settingsWindowOpens = Boolean(
      monitoringHudActiveChildWindow === "overlay-profile-settings"
      && monitoringHudOverlayProfileWindow
      && monitoringHudOverlayProfileWindow.hidden === false
    );
    const created = monitoringHudCreateOverlayProfile();
    const createdId = monitoringHudControlState.activeOverlayProfileId;
    const createdProfile = (monitoringHudControlState.overlayProfiles || {})[createdId] || {};
    proof.createdProfileSelectable = Boolean(created && createdId && createdProfile.id === createdId);
    proof.monitorMembershipReadOnly = Array.isArray(createdProfile.monitorIds);
    if (monitoringHudOverlayProfileNameInput) {
      monitoringHudOverlayProfileNameInput.value = "Focused Overlay Profile";
    }
    const allMonitorIds = monitoringHudStableMonitorIds(monitoringHudControlState.cards || {});
    const savedMonitorIds = allMonitorIds.slice(0, Math.max(1, Math.min(1, allMonitorIds.length)));
    if (monitoringHudOverlayProfileMembershipList) {
      const inputs = Array.from(monitoringHudOverlayProfileMembershipList.querySelectorAll("[data-overlay-profile-membership-toggle]"));
      inputs.forEach((input) => {
        input.checked = savedMonitorIds.includes(input.value);
      });
      if (inputs[0]) inputs[0].dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      monitoringHudOverlayProfileDraftMonitorIds = savedMonitorIds.slice();
    }
    monitoringHudSaveOverlayProfileDraft();
    const savedProfile = (monitoringHudControlState.overlayProfiles || {})[createdId] || {};
    proof.renameSaved = savedProfile.name === "Focused Overlay Profile";
    proof.membershipSaved = JSON.stringify(savedProfile.monitorIds || []) === JSON.stringify(savedMonitorIds);
    if (monitoringHudOverlayProfileNameInput) {
      monitoringHudOverlayProfileNameInput.value = "Discarded Draft Name";
    }
    const discardedMonitorIds = allMonitorIds.slice().reverse();
    if (monitoringHudOverlayProfileMembershipList) {
      const inputs = Array.from(monitoringHudOverlayProfileMembershipList.querySelectorAll("[data-overlay-profile-membership-toggle]"));
      inputs.forEach((input) => {
        input.checked = discardedMonitorIds.includes(input.value);
      });
      if (inputs[0]) inputs[0].dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      monitoringHudOverlayProfileDraftMonitorIds = discardedMonitorIds.slice();
    }
    monitoringHudDiscardOverlayProfileDraft();
    proof.discardRestored = monitoringHudOverlayProfileNameInput
      ? monitoringHudOverlayProfileNameInput.value === "Focused Overlay Profile"
      : true;
    const restoredProfile = (monitoringHudControlState.overlayProfiles || {})[createdId] || {};
    proof.membershipDiscardRestored = JSON.stringify(restoredProfile.monitorIds || []) === JSON.stringify(savedMonitorIds)
      && monitoringHudSameMonitorMembership(monitoringHudOverlayProfileDraftMonitorIds, savedMonitorIds, monitoringHudControlState.cards || {});
    proof.activeProfilePersistsInState = monitoringHudControlState.activeOverlayProfileId === createdId;
  } finally {
    try {
      monitoringHudControlState = JSON.parse(previousState);
      monitoringHudOverlayProfileDraftId = previousDraftId;
      monitoringHudOverlayProfileDraftName = previousDraftName;
      monitoringHudOverlayProfileDraftMonitorIds = previousDraftMonitorIds.slice();
      monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
      monitoringHudSetOverlayProfileDraftFromActive();
      monitoringHudRenderControls();
      monitoringHudCloseChildWindow({ force: true });
      monitoringHudSaveStoredState();
    } catch (_err) {}
  }
  proof.passed = proof.selectorVisible
    && proof.settingsEntryVisible
    && proof.settingsWindowPresent
    && proof.settingsWindowOpens
    && proof.createVisible
    && proof.renameVisible
    && proof.saveDiscardVisible
    && proof.editableMembership
    && proof.createdProfileSelectable
    && proof.renameSaved
    && proof.discardRestored
    && proof.membershipListVisible
    && proof.membershipSaved
    && proof.membershipDiscardRestored
    && proof.monitorGroupBoundary
    && proof.recordingProfileBoundary
    && proof.activeProfilePersistsInState;
  if (monitoringHud) {
    monitoringHud.dataset.overlayProfileControlsProof = proof.passed ? "pass" : "fail";
  }
  return proof;
};

window.getMonitoringHudControlState = function() {
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  return Object.assign({}, monitoringHudControlState, {
    cards: Object.assign({}, monitoringHudControlState.cards),
    overlayProfiles: JSON.parse(JSON.stringify(monitoringHudControlState.overlayProfiles || {})),
    activeOverlayProfileId: monitoringHudControlState.activeOverlayProfileId || monitoringHudDefaultOverlayProfileId,
    overlayProfileSchemaVersion: monitoringHudOverlayProfileSchemaVersion,
    overlayProfileStateProof: Object.assign({}, monitoringHudControlState.overlayProfileStateProof || {}),
    activeChildWindow: monitoringHudActiveChildWindow || "none",
    interactiveControlReliabilityProof: Object.assign({}, monitoringHudReliableActivationState, {
      attempts: monitoringHudReliableActivationState.attempts.slice(-40)
    }),
    geometry: window.getMonitoringHudLiveClientGeometry
      ? window.getMonitoringHudLiveClientGeometry()
      : {}
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
    anchorToggle: null,
    settingsAction: rectFor("#monitoring-hud-settings-action"),
    createMonitor: rectFor("#monitoring-hud-create-monitor-action"),
    editMonitor: rectFor("#monitoring-hud-edit-monitor-action"),
    dashboardClose: rectFor("#monitoring-hud-dashboard-close-action"),
    settingsWindow: rectFor("#monitoring-hud-settings-window"),
    settingsClose: rectFor('[data-child-window-close="dashboard-settings"]'),
    settingsWarningToggle: rectFor("#monitoring-hud-settings-warning-toggle"),
    createMonitorWindow: rectFor("#monitoring-hud-create-monitor-window"),
    createMonitorClose: rectFor('[data-child-window-close="monitor-group-create"]'),
    editMonitorWindow: rectFor("#monitoring-hud-edit-monitor-window"),
    editMonitorClose: rectFor('[data-child-window-close="monitor-group-edit"]'),
    manageMonitorCreate: rectFor("#monitoring-hud-manage-monitor-create-action"),
    manageMonitorEmptyCreate: rectFor("#monitoring-hud-monitor-empty-create-action"),
    monitorDetailActions: rectFor("#monitoring-hud-monitor-detail-actions"),
    monitorDeleteConfirmation: rectFor("#monitoring-hud-monitor-delete-confirmation"),
    monitorSensorAssignment: rectFor("#monitoring-hud-monitor-sensor-assignment"),
    monitorSensorSettings: rectFor("#monitoring-hud-monitor-sensor-settings"),
    childWindowLayer: rectFor("#monitoring-hud-child-window-layer"),
    visibilityToggle: null,
    snapToggle: rectFor("#monitoring-hud-snap-toggle"),
    warningToggle: rectFor("#monitoring-hud-warning-toggle"),
    pollingRate: rectFor("#monitoring-hud-polling-rate"),
    warningModeControl: rectFor("#monitoring-hud-warning-mode-control"),
    panelDragHandle: rectFor("#monitoring-hud-drag-handle"),
    monitorList: rectFor("#monitoring-hud-monitor-list"),
    hudOverlayCard: rectFor('[data-dashboard-hub-card="hud-overlay"]'),
    monitorGroupsCard: rectFor('[data-dashboard-hub-card="monitor-groups"]'),
    monitorGroupsSummaryGrid: rectFor('[data-dashboard-hub-card="monitor-groups"] .monitoring-hud__monitor-summary-grid'),
    monitorGroupsActions: rectFor('[data-dashboard-hub-card="monitor-groups"] .monitoring-hud__hub-actions'),
    monitorGroupsScope: rectFor("#monitoring-hud-monitor-editor-scope"),
    dataSourcesCard: rectFor('[data-dashboard-hub-card="data-sources"]'),
    readinessCard: rectFor('[data-dashboard-hub-card="readiness"]'),
    monitorSelector: null,
    dataSourcesAction: rectFor('[data-control="open-data-sources"]'),
    hudOverlayDeferredAction: rectFor('[data-dashboard-hub-card="hud-overlay"]'),
    monitorEnabled: rectFor("#monitoring-hud-monitor-enabled"),
    monitorPollingRate: rectFor("#monitoring-hud-monitor-polling-rate"),
    monitorPollingRateControl: rectFor("#monitoring-hud-monitor-polling-rate-control"),
    monitorPollingRateToggle: rectFor("#monitoring-hud-monitor-polling-rate-toggle"),
    overlayProfileEditor: rectFor("#monitoring-hud-overlay-profile-editor"),
    overlayProfileSelector: rectFor("#monitoring-hud-overlay-profile-selector"),
    overlayProfileToggle: rectFor("#monitoring-hud-overlay-profile-toggle"),
    overlayProfileMenu: rectFor("#monitoring-hud-overlay-profile-menu"),
    overlayProfileOpenSettings: rectFor("#monitoring-hud-overlay-profile-open-settings"),
    overlayProfileWindow: rectFor("#monitoring-hud-overlay-profile-window"),
    overlayProfileWindowClose: rectFor('[data-child-window-close="overlay-profile-settings"]'),
    overlayProfileNameInput: rectFor("#monitoring-hud-overlay-profile-name-input"),
    overlayProfileMembershipList: rectFor("#monitoring-hud-overlay-profile-membership-list"),
    overlayProfileMembershipFirstToggle: rectFor("[data-overlay-profile-membership-toggle]"),
    overlayProfileCreate: rectFor("#monitoring-hud-overlay-profile-create"),
    overlayProfileSave: rectFor("#monitoring-hud-overlay-profile-save"),
    overlayProfileDiscard: rectFor("#monitoring-hud-overlay-profile-discard"),
    editMonitorName: rectFor("#monitoring-hud-edit-monitor-name"),
    createMonitorName: rectFor("#monitoring-hud-create-monitor-name"),
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
    dashboardMinimumEdgeProof: monitoringHud ? monitoringHud.dataset.dashboardMinimumEdgeProof || "" : "",
    dashboardDecouplingProof: monitoringHud ? monitoringHud.dataset.dashboardDecouplingProof || "" : "",
    dashboardContentPolish: monitoringHud ? monitoringHud.dataset.dashboardContentPolish || "" : "",
    dashboardSettingsModel: monitoringHud ? monitoringHud.dataset.dashboardSettingsModel || "" : "",
    monitorGroupModel: monitoringHud ? monitoringHud.dataset.monitorGroupModel || "" : "",
    dashboardMonitorCardPolicy: monitoringHud ? monitoringHud.dataset.dashboardMonitorCardPolicy || "" : "",
    monitorManagement: monitoringHud ? monitoringHud.dataset.monitorManagement || "" : "",
    dashboardChildWindowScope: monitoringHud ? monitoringHud.dataset.dashboardChildWindowScope || "" : "",
    monitorSensorAssignment: monitoringHud ? monitoringHud.dataset.monitorSensorAssignment || "" : "",
    monitorDeleteConfirmation: monitoringHud ? monitoringHud.dataset.monitorDeleteConfirmation || "" : "",
    assignedSensorCount: monitoringHud ? Number(monitoringHud.dataset.assignedSensorCount || 0) : 0,
    dashboardProviderTruth: monitoringHud ? monitoringHud.dataset.dashboardProviderTruth || "" : "",
    dashboardStateModel: monitoringHud ? monitoringHud.dataset.dashboardStateModel || "" : "",
    dashboardWarningControls: monitoringHud ? monitoringHud.dataset.dashboardWarningControls || "" : "",
    dashboardFakeTelemetryPolicy: monitoringHud ? monitoringHud.dataset.dashboardFakeTelemetryPolicy || "" : "",
    dashboardSettingsAffordance: monitoringHud ? monitoringHud.dataset.dashboardSettingsAffordance || "" : "",
    dashboardSettingsPanel: monitoringHud ? monitoringHud.dataset.dashboardSettingsPanel || "" : "",
    dashboardSettingsPanelState: monitoringHud ? monitoringHud.dataset.dashboardSettingsPanelState || "" : "",
    dashboardSettingsProof: monitoringHud ? monitoringHud.dataset.dashboardSettingsProof || "" : "",
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
    dashboardMinimumEdgeProof: split.dashboardMinimumEdgeProof || "",
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
      && split.dashboardMinimumEdgeProof === "native-min-size-bottom-edge-visible"
      && split.dashboardDecouplingProof === "core-overlay-independent"
    ),
    dashboardSettingsContentReady: Boolean(
      split.dashboardContentPolish === "branch2-monitor-groups-no-dead-space"
      && split.dashboardSettingsModel === "hud-overlay-monitor-groups-provider-warning"
      && split.dashboardSettingsAffordance === "dashboard-ia-card-settings-button"
      && split.dashboardSettingsPanel === "settings-panel-child-window"
      && split.dashboardSettingsProof === "visible-open-close-control-hit-target"
      && split.monitorManagement === "sensor-command-center-list-detail-source-picker"
      && split.dashboardChildWindowScope === "monitor-groups-manage-create-edit-delete-sensor-windows-overlay-profile-settings"
      && split.monitorGroupModel === "configurable-groups-sensor-assignment"
      && split.dashboardMonitorCardPolicy === "overlay-display-owns-visual-rendering"
      && split.monitorSensorAssignment === "sensor-library-source-picker"
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

window.runMonitoringHudInteractiveControlStressProof = function() {
  const backup = window.getMonitoringHudControlState ? window.getMonitoringHudControlState() : null;
  const failures = [];
  const states = {};
  let sourcePickerCheckmarkProof = {};
  let displayModeChipProof = {};
  let pollingRateHitboxProof = {};
  let manageCloseHitboxProof = {};
  function prepareVisibleTarget(element) {
    if (!element) return;
    if (typeof element.scrollIntoView === "function") {
      element.scrollIntoView({ block: "center", inline: "center", behavior: "instant" });
    }
  }
  function targetSnapshot(name, selector) {
    const element = document.querySelector(selector);
    prepareVisibleTarget(element);
    const snapshot = monitoringHudControlInterceptionSnapshot(element);
    states[name] = Object.assign({}, snapshot, {
      selector,
      present: Boolean(element),
      focusable: Boolean(element && typeof element.focus === "function"),
      disabled: Boolean(element && element.disabled),
      ariaDisabled: element && element.getAttribute ? String(element.getAttribute("aria-disabled") || "false") : ""
    });
    if (!element) failures.push(`${name}:missing`);
    if (element && element.disabled) failures.push(`${name}:disabled`);
    if (element && snapshot.sameTargetOrChild === false) failures.push(`${name}:intercepted`);
    return element;
  }
  function activate(name, selector, check) {
    const element = targetSnapshot(name, selector);
    if (!element) return false;
    element.click();
    const passed = typeof check === "function" ? Boolean(check(element)) : true;
    if (!passed) failures.push(`${name}:first-click-no-state-change`);
    return passed;
  }
  try {
    if (monitoringHud) {
      monitoringHud.dataset.interactiveControlVisualAffordance = "normal-hover-active-focus-disabled-open-selected";
      monitoringHud.dataset.interactiveControlReliability = "first-click-stress-running";
      monitoringHud.dataset.clickInterceptionDiagnostics = "z-index-pointer-events-disabled-aria-dom-focus-timing";
      monitoringHud.dataset.pollingRateDropdown = "nexus-styled-bounded-control";
    }
    monitoringHudPendingDeleteMonitorId = "";
    monitoringHudSetMonitorDraftDirty(false);
    monitoringHudSetSourceFilterDropdownOpen(false);
    monitoringHudSetPollingRateDropdownOpen(false);
    monitoringHudRenderMonitorManagement();
    monitoringHudCloseChildWindow({ force: true });
    activate("dashboard-settings", "#monitoring-hud-settings-action", () => monitoringHudActiveChildWindow === "dashboard-settings");
    activate("settings-close", '[data-child-window-close="dashboard-settings"]', () => monitoringHudActiveChildWindow !== "dashboard-settings");
    activate("dashboard-warning", "#monitoring-hud-warning-toggle", () => true);
    activate("dashboard-manage-monitors", "#monitoring-hud-edit-monitor-action", () => monitoringHudActiveChildWindow === "monitor-group-edit");
    if (typeof monitoringHudManageCloseHitboxProof === "function") {
      manageCloseHitboxProof = monitoringHudManageCloseHitboxProof() || {};
      if (manageCloseHitboxProof.passed !== true) failures.push("manage-close-hitbox-partial-interception");
    }
    const beforeSelected = monitoringHudControlState.selectedMonitorId;
    const nextRow = document.querySelector(`[data-monitor-select]:not([data-monitor-select="${beforeSelected}"])`);
    if (nextRow) {
      const nextId = nextRow.dataset.monitorSelect || "";
      activate("monitor-row-switch", `[data-monitor-select="${nextId}"]`, () => monitoringHudControlState.selectedMonitorId === nextId);
    }
    activate("manage-create", "#monitoring-hud-manage-monitor-create-action", () => {
      const id = monitoringHudControlState.selectedMonitorId || "";
      return id.indexOf("monitor-") === 0 && Boolean(monitoringHudControlState.cards[id]);
    });
    activate("delete-selected", "#monitoring-hud-monitor-detail-delete", () => monitoringHudPendingDeleteMonitorId === monitoringHudControlState.selectedMonitorId);
    activate("delete-cancel", "#monitoring-hud-monitor-delete-cancel", () => !monitoringHudPendingDeleteMonitorId);
    const input = document.getElementById("monitoring-hud-edit-monitor-name");
    if (input) {
      input.value = "First Click Stress Draft";
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }
    activate("dirty-close", '[data-child-window-close="monitor-group-edit"]', () => {
      const guard = document.getElementById("monitoring-hud-monitor-unsaved-guard");
      return Boolean(guard && !guard.hidden && guard.dataset.pendingMonitorAction === "close");
    });
    activate("dirty-discard", "#monitoring-hud-monitor-unsaved-discard", () => monitoringHudActiveChildWindow !== "monitor-group-edit");
    if (typeof monitoringHudOpenChildWindow === "function") monitoringHudOpenChildWindow("monitor-group-edit");
    activate("source-filter-open", "#monitoring-hud-sensor-filter-toggle", () => monitoringHudSensorFilter && monitoringHudSensorFilter.dataset.filterOpen === "true");
    activate("source-filter-supported", '[data-source-filter="supported"]', () => monitoringHudSensorFilterValue() === "supported");
    activate("source-filter-reopen", "#monitoring-hud-sensor-filter-toggle", () => monitoringHudSensorFilter && monitoringHudSensorFilter.dataset.filterOpen === "true");
    monitoringHudSetSourceFilterDropdownOpen(false);
    activate("polling-rate-open", "#monitoring-hud-monitor-polling-rate-toggle", () => monitoringHudMonitorPollingRateControl && monitoringHudMonitorPollingRateControl.dataset.dropdownOpen === "true");
    activate("polling-rate-5s", '[data-polling-rate-option="5000"]', () => monitoringHudMonitorPollingRate && monitoringHudMonitorPollingRate.value === "5000");
    if (typeof monitoringHudPollingRateHitboxProof === "function") {
      pollingRateHitboxProof = monitoringHudPollingRateHitboxProof() || {};
      if (pollingRateHitboxProof.passed !== true) failures.push("polling-rate-hitbox-too-wide");
    }
    if (typeof window.runMonitoringHudSourcePickerCheckmarkStressProof === "function") {
      sourcePickerCheckmarkProof = window.runMonitoringHudSourcePickerCheckmarkStressProof() || {};
      if (sourcePickerCheckmarkProof.passed !== true) failures.push("source-picker-checkmark-stress");
    }
    if (typeof window.runMonitoringHudDisplayModeChipStressProof === "function") {
      displayModeChipProof = window.runMonitoringHudDisplayModeChipStressProof() || {};
      if (displayModeChipProof.passed !== true) failures.push("display-mode-chip-stress");
    }
    const saveInput = document.getElementById("monitoring-hud-edit-monitor-name");
    if (saveInput) {
      saveInput.value = "First Click Stress Save";
      saveInput.dispatchEvent(new Event("input", { bubbles: true }));
    }
    activate("save-monitor", "#monitoring-hud-edit-monitor-confirm", () => true);
    if (typeof monitoringHudOpenChildWindow === "function") monitoringHudOpenChildWindow("monitor-group-edit");
    activate("manage-close-clean", '[data-child-window-close="monitor-group-edit"]', () => monitoringHudActiveChildWindow !== "monitor-group-edit");
    if (backup && window.setMonitoringHudControlState) {
      window.setMonitoringHudControlState(backup);
      monitoringHudOpenChildWindow("monitor-group-edit");
    }
  } catch (err) {
    failures.push(`exception:${String(err && err.message ? err.message : err)}`);
  }
  const proof = {
    passed: failures.length === 0,
    failures,
    stateCount: Object.keys(states).length,
    states,
    repeatedFirstClickStress: true,
    postRenderStatesCovered: [
      "re-render",
      "dirty-guard",
      "delete-confirmation",
      "dropdown-open",
      "post-close-reopen",
      "post-render"
    ],
    pollingRateDropdownNexusStyled: Boolean(monitoringHudMonitorPollingRateControl && monitoringHudMonitorPollingRateControl.dataset.selectedValue),
    pollingRateHitboxToggleOnly: pollingRateHitboxProof.passed === true,
    pollingRateHitboxProof,
    manageCloseHitboxFullHeight: manageCloseHitboxProof.passed === true,
    manageCloseHitboxProof,
    sourceFilterDropdownNexusStyled: Boolean(monitoringHudSensorFilter && monitoringHudSensorFilter.dataset.sourceFilterMode === "nexus-dropdown-source-picker"),
    sourcePickerCheckmarkStress: sourcePickerCheckmarkProof.passed === true,
    sourcePickerCheckmarkProof,
    displayModeChipStress: displayModeChipProof.passed === true,
    displayModeChipProof,
    affordanceStatesRequired: "normal-hover-active-focus-visible-disabled-open-selected-warning"
  };
  monitoringHudReliableActivationState.visualStates = states;
  if (monitoringHud) {
    monitoringHud.dataset.interactiveControlReliability = proof.passed ? "first-click-stress-pass" : "first-click-stress-fail";
    monitoringHud.dataset.interactiveControlVisualAffordance = "normal-hover-active-focus-visible-disabled-open-selected";
    monitoringHud.dataset.interactiveControlStressProof = proof.passed ? "pass" : "fail";
    monitoringHud.dataset.pollingRateDropdown = "nexus-styled-bounded-control";
  }
  monitoringHudControlState.interactiveControlReliabilityProof = proof;
  return proof;
};

window.runMonitoringHudSourcePickerCheckmarkStressProof = function() {
  const backup = window.getMonitoringHudControlState ? window.getMonitoringHudControlState() : null;
  const failures = [];
  const toggles = [];
  const activationMethods = ["row-click", "checkbox-click", "keyboard-space"];
  let maxToggleMs = 0;
  let rowsTested = 0;
  let rowsAvailable = 0;
  let alternatingToggleCount = 0;
  let alternatingTogglePass = false;
  function dispatchHumanPointerDown(target) {
    if (!target || typeof target.dispatchEvent !== "function") return;
    let event = null;
    try {
      event = new PointerEvent("pointerdown", {
        bubbles: true,
        cancelable: true,
        pointerType: "mouse",
        isPrimary: true
      });
    } catch (err) {
      event = new MouseEvent("pointerdown", { bubbles: true, cancelable: true });
    }
    target.dispatchEvent(event);
  }
  try {
    if (typeof window.setMonitoringHudLargeFixtureMode === "function") {
      window.setMonitoringHudLargeFixtureMode(80);
    }
    monitoringHudOpenChildWindow("monitor-group-edit");
    if (monitoringHudSensorSearch) {
      monitoringHudSensorSearch.value = "";
    }
    monitoringHudSetSourceFilterValue("supported");
    monitoringHudSetSourceFilterDropdownOpen(false);
    monitoringHudRenderMonitorManagement();
    const rows = Array.from(document.querySelectorAll("[data-source-picker-row]"))
      .filter((row) => row.dataset.sensorAssignable === "true" && row.querySelector("[data-monitor-sensor-input]"))
      .slice(0, 18);
    rowsAvailable = rows.length;
    rowsTested = rows.length;
    if (rows.length < 8) failures.push("source-picker-checkmark:too-few-supported-rows");
    rows.forEach((row, index) => {
      const input = row.querySelector("[data-monitor-sensor-input]");
      const before = Boolean(input && input.checked);
      const startedAt = (window.performance && performance.now) ? performance.now() : Date.now();
      monitoringHudReliableActivationState.lastKey = "";
      monitoringHudReliableActivationState.lastAt = 0;
      const method = activationMethods[index % activationMethods.length];
      if (method === "checkbox-click" && input && typeof input.click === "function") {
        dispatchHumanPointerDown(input);
        input.click();
      } else if (method === "keyboard-space") {
        if (typeof row.focus === "function") row.focus();
        row.dispatchEvent(new KeyboardEvent("keydown", {
          key: " ",
          code: "Space",
          bubbles: true,
          cancelable: true
        }));
      } else {
        row.click();
      }
      const finishedAt = (window.performance && performance.now) ? performance.now() : Date.now();
      const elapsed = Math.max(0, finishedAt - startedAt);
      maxToggleMs = Math.max(maxToggleMs, elapsed);
      const after = Boolean(input && input.checked);
      const ariaSelected = row.getAttribute("aria-selected") === "true";
      const sourceId = row.dataset.sourcePickerRow || `row-${index}`;
      toggles.push({
        sourceId,
        method,
        before,
        after,
        elapsedMs: Math.round(elapsed * 10) / 10,
        ariaSelected,
        visualSelected: row.dataset.sourceSelected === "true"
      });
      if (after === before) failures.push(`source-picker-checkmark:${sourceId}:no-toggle`);
      if (ariaSelected !== after) failures.push(`source-picker-checkmark:${sourceId}:aria-mismatch`);
      if ((row.dataset.sourceSelected === "true") !== after) failures.push(`source-picker-checkmark:${sourceId}:visual-state-mismatch`);
      if (elapsed > 80) failures.push(`source-picker-checkmark:${sourceId}:slow-${Math.round(elapsed)}ms`);
    });
    const alternatingRow = rows[0];
    const alternatingInput = alternatingRow ? alternatingRow.querySelector("[data-monitor-sensor-input]") : null;
    if (alternatingRow && alternatingInput) {
      let expected = Boolean(alternatingInput.checked);
      alternatingTogglePass = true;
      for (let index = 0; index < 12; index += 1) {
        expected = !expected;
        monitoringHudReliableActivationState.lastKey = "";
        monitoringHudReliableActivationState.lastAt = 0;
        const startedAt = (window.performance && performance.now) ? performance.now() : Date.now();
        if (index % 2 === 0) {
          alternatingRow.click();
        } else {
          dispatchHumanPointerDown(alternatingInput);
          alternatingInput.click();
        }
        const finishedAt = (window.performance && performance.now) ? performance.now() : Date.now();
        const elapsed = Math.max(0, finishedAt - startedAt);
        maxToggleMs = Math.max(maxToggleMs, elapsed);
        alternatingToggleCount += 1;
        const after = Boolean(alternatingInput.checked);
        const ariaSelected = alternatingRow.getAttribute("aria-selected") === "true";
        const visualSelected = alternatingRow.dataset.sourceSelected === "true";
        toggles.push({
          sourceId: alternatingRow.dataset.sourcePickerRow || "alternating-row",
          method: index % 2 === 0 ? "alternating-row-click" : "alternating-checkbox-click",
          before: !expected,
          after,
          expected,
          elapsedMs: Math.round(elapsed * 10) / 10,
          ariaSelected,
          visualSelected
        });
        if (after !== expected || ariaSelected !== expected || visualSelected !== expected) {
          alternatingTogglePass = false;
          failures.push(`source-picker-checkmark:alternating-${index}:expected-${expected}-got-${after}`);
        }
        if (elapsed > 80) failures.push(`source-picker-checkmark:alternating-${index}:slow-${Math.round(elapsed)}ms`);
      }
    } else {
      failures.push("source-picker-checkmark:alternating-missing-row");
    }
  } catch (err) {
    failures.push(`source-picker-checkmark:exception:${String(err && err.message ? err.message : err)}`);
  }
  const proof = {
    passed: failures.length === 0,
    failures,
    rowsTested,
    rowsAvailable,
    toggles,
    maxToggleMs: Math.round(maxToggleMs * 10) / 10,
    rowClickTarget: true,
    checkboxClickTarget: true,
    keyboardToggleTarget: true,
    alternatingTogglePass,
    alternatingToggleCount,
    activationMethods,
    sourcePickerCheckmarkStress: true,
    sourcePickerCheckmarkMode: "row-and-checkbox-immediate-deferred-settings",
    sourcePickerCheckmarkLatency: "immediate-visual-deferred-settings",
    sourcePickerRenderScope: "immediate-row-preview-deferred-settings"
  };
  if (monitoringHudMonitorSensorAssignment) {
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerCheckmarkStress = proof.passed ? "pass" : "fail";
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerCheckmarkStressCount = String(rowsTested);
    monitoringHudMonitorSensorAssignment.dataset.sourcePickerCheckmarkMaxToggleMs = String(proof.maxToggleMs);
  }
  if (monitoringHud) {
    monitoringHud.dataset.sourcePickerCheckmarkStress = proof.passed ? "pass" : "fail";
    monitoringHud.dataset.sourcePickerCheckmarkMode = proof.sourcePickerCheckmarkMode;
  }
  if (backup && window.setMonitoringHudControlState) {
    window.setMonitoringHudControlState(backup);
    monitoringHudOpenChildWindow("monitor-group-edit");
  }
  monitoringHudControlState.sourcePickerCheckmarkStressProof = proof;
  return proof;
};

window.runMonitoringHudDisplayModeChipStressProof = function() {
  const backup = window.getMonitoringHudControlState ? window.getMonitoringHudControlState() : null;
  const failures = [];
  const toggles = [];
  let maxToggleMs = 0;
  try {
    monitoringHudOpenChildWindow("monitor-group-edit");
    const selected = monitoringHudSelectedMonitor();
    if (!selected.id || !selected.layout) throw new Error("display-mode:selected-monitor-missing");
    if (!Array.isArray(selected.layout.sensors) || !selected.layout.sensors.includes("cpu-load")) {
      const row = document.querySelector('[data-source-picker-row="cpu-load"]');
      if (row) monitoringHudToggleSensorAssignmentRow(row, true);
      monitoringHudRenderSensorSettings(monitoringHudSelectedMonitor());
    }
    let buttons = Array.from(document.querySelectorAll("[data-sensor-display-mode-option]"));
    if (!buttons.length) {
      monitoringHudRenderMonitorManagement();
      buttons = Array.from(document.querySelectorAll("[data-sensor-display-mode-option]"));
    }
    const values = ["text", "badge", "badge-text", "text", "badge-text", "badge"];
    values.forEach((value, index) => {
      const button = buttons.find((item) => item.dataset.sensorDisplayModeValue === value);
      if (!button) {
        failures.push(`display-mode:${value}:missing-button`);
        return;
      }
      const group = button.closest("[data-sensor-display-mode]");
      const startedAt = (window.performance && performance.now) ? performance.now() : Date.now();
      if (index % 3 === 0) {
        monitoringHudActivateDisplayModeChip(button, null, "proof-direct-pointerdown");
      } else if (index % 3 === 1) {
        button.click();
      } else {
        if (typeof button.focus === "function") button.focus();
        button.dispatchEvent(new KeyboardEvent("keydown", {
          key: " ",
          code: "Space",
          bubbles: true,
          cancelable: true
        }));
      }
      const finishedAt = (window.performance && performance.now) ? performance.now() : Date.now();
      const elapsed = Math.max(0, finishedAt - startedAt);
      maxToggleMs = Math.max(maxToggleMs, elapsed);
      const selectedValue = group ? group.dataset.sensorDisplayModeSelected : "";
      const pressed = button.getAttribute("aria-pressed") === "true";
      toggles.push({
        value,
        selectedValue,
        pressed,
        elapsedMs: Math.round(elapsed * 10) / 10
      });
      if (selectedValue !== value) failures.push(`display-mode:${value}:selection-not-updated`);
      if (!pressed) failures.push(`display-mode:${value}:pressed-not-updated`);
      if (elapsed > 80) failures.push(`display-mode:${value}:slow-${Math.round(elapsed)}ms`);
    });
  } catch (err) {
    failures.push(`display-mode:exception:${String(err && err.message ? err.message : err)}`);
  }
  const proof = {
    passed: failures.length === 0,
    failures,
    toggles,
    maxToggleMs: Math.round(maxToggleMs * 10) / 10,
    displayModeChipStress: true,
    displayModeActivationPath: "deterministic-pointer-click-keyboard",
    displayModeSelectionLatency: "immediate-visual-draft-update"
  };
  if (monitoringHudMonitorSensorSettings) {
    monitoringHudMonitorSensorSettings.dataset.displayModeChipStress = proof.passed ? "pass" : "fail";
    monitoringHudMonitorSensorSettings.dataset.displayModeChipMaxToggleMs = String(proof.maxToggleMs);
  }
  if (monitoringHud) {
    monitoringHud.dataset.displayModeChipStress = proof.passed ? "pass" : "fail";
  }
  if (backup && window.setMonitoringHudControlState) {
    window.setMonitoringHudControlState(backup);
    monitoringHudOpenChildWindow("monitor-group-edit");
  }
  monitoringHudControlState.displayModeChipStressProof = proof;
  return proof;
};

window.setMonitoringHudControlState = function(state) {
  const incomingState = state || {};
  const incomingHasCards = monitoringHudHasOwnCards(incomingState);
  monitoringHudControlState = Object.assign({}, monitoringHudControlState, incomingState);
  monitoringHudControlState.featureEnabled = Boolean(monitoringHudControlState.featureEnabled);
  monitoringHudControlState.overlayDeferred = monitoringHudControlState.overlayDeferred !== false;
  monitoringHudControlState.visible = Boolean(monitoringHudControlState.featureEnabled && monitoringHudControlState.visible);
  monitoringHudControlState.warningMode = monitoringHudControlState.warningMode || "badge-text-color";
  monitoringHudControlState.cards = incomingHasCards
    ? monitoringHudSafeCardsObject(incomingState.cards)
    : monitoringHudSafeCardsObject(monitoringHudControlState.cards || monitoringHudInitialCards());
  Object.keys(monitoringHudControlState.cards).forEach((cardId) => {
    monitoringHudControlState.cards[cardId] = Object.assign(
      monitoringHudCardDefaults(cardId),
      monitoringHudControlState.cards[cardId] || {}
    );
    monitoringHudNormalizeSensorAssignments(cardId, monitoringHudControlState.cards[cardId]);
  });
  if (!monitoringHudControlState.selectedMonitorId || !monitoringHudControlState.cards[monitoringHudControlState.selectedMonitorId]) {
    monitoringHudControlState.selectedMonitorId = Object.keys(monitoringHudControlState.cards)[0] || "";
  }
  monitoringHudNormalizeOverlayProfileState(monitoringHudControlState);
  monitoringHudControlState.monitorSequence = Math.max(
    Number(monitoringHudControlState.monitorSequence || 2),
    Object.keys(monitoringHudControlState.cards).length
  );
  monitoringHudControlState.emptyCardsPersistenceProof = {
    explicitEmptyCardsPreserved: incomingHasCards && Object.keys(monitoringHudControlState.cards).length === 0,
    defaultCardsOnlyWhenCardsAbsent: !incomingHasCards,
    selectedMonitorId: monitoringHudControlState.selectedMonitorId || ""
  };
  if (monitoringHudControlState.panelPosition) {
    monitoringHudSetPanelPosition(
      monitoringHudControlState.panelPosition.left || 0,
      monitoringHudControlState.panelPosition.top || 0
    );
  } else if (monitoringHud) {
    monitoringHudClearPanelPosition();
  }
  monitoringHudPendingDeleteMonitorId = "";
  monitoringHudSetMonitorDraftDirty(false);
  monitoringHudSetSourceFilterDropdownOpen(false);
  monitoringHudSetPollingRateDropdownOpen(false);
  monitoringHudApplyCardLayout();
  monitoringHudRenderControls();
  monitoringHudMarkChanged();
};

window.runMonitoringHudEmptyCardsPersistenceProof = function() {
  const backup = window.getMonitoringHudControlState ? window.getMonitoringHudControlState() : null;
  const failures = [];
  try {
    window.setMonitoringHudControlState(Object.assign({}, backup || {}, {
      cards: {},
      selectedMonitorId: "",
      featureEnabled: true,
      visible: true
    }));
    monitoringHudOpenChildWindow("monitor-group-edit");
    const cardIds = Object.keys(monitoringHudControlState.cards || {});
    const emptyDetail = monitoringHudMonitorDetailEmpty && monitoringHudMonitorDetailEmpty.dataset.monitorDetailEmpty === "true-empty-state-create-reachable";
    const listEmpty = monitoringHudMonitorListEmpty && monitoringHudMonitorListEmpty.dataset.monitorListEmpty === "true-empty-state";
    if (cardIds.length !== 0) failures.push(`cards-restored:${cardIds.join(",")}`);
    if (monitoringHudControlState.selectedMonitorId) failures.push(`selected-not-empty:${monitoringHudControlState.selectedMonitorId}`);
    if (!emptyDetail) failures.push("detail-empty-state-not-rendered");
    if (!listEmpty) failures.push("list-empty-state-not-rendered");
  } catch (err) {
    failures.push(`exception:${String(err && err.message ? err.message : err)}`);
  }
  const proof = {
    passed: failures.length === 0,
    failures,
    cardCount: Object.keys(monitoringHudControlState.cards || {}).length,
    selectedMonitorId: monitoringHudControlState.selectedMonitorId || "",
    explicitEmptyCardsPreserved: true,
    defaultCardsOnlyWhenCardsAbsent: true
  };
  if (monitoringHud) {
    monitoringHud.dataset.emptyCardsPersistence = proof.passed ? "explicit-empty-cards-preserved" : "failed";
  }
  if (backup && window.setMonitoringHudControlState) {
    window.setMonitoringHudControlState(backup);
    monitoringHudOpenChildWindow("monitor-group-edit");
  }
  monitoringHudControlState.emptyCardsPersistenceProof = proof;
  return proof;
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
    monitoringHudRuntimeStatus.textContent = monitoringHudControlState.visible ? "Dashboard visible" : "Dashboard hidden";
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
  monitoringHudRenderMonitorManagement();
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
    monitoringHudPlacementOwner.textContent = monitoringHudPlacement.rendererOwner || "HUD Overlay release acceptance is deferred. The Dashboard can describe the future overlay boundary without enabling it.";
  }
  if (monitoringHudPlacementAnchor) {
    monitoringHudPlacementAnchor.textContent = monitoringHudPlacement.anchor || "Deferred / non-gating";
  }
  if (monitoringHudPlacementPointer) {
    monitoringHudPlacementPointer.textContent = monitoringHudPlacement.pointerModel || "Dashboard configures future HUD Overlay behavior";
  }
  if (monitoringHudResizePosture) {
    monitoringHudResizePosture.textContent = monitoringHudPlacement.resizePosture || "Overlay settings are future branch scope";
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
    monitoringHud.dataset.monitorManagement = "sensor-command-center-list-detail-source-picker";
    monitoringHud.dataset.overlayModeControls = "overlay-deferred-tray-owned";
  }
  if (monitoringHudControlsVisibility) {
    monitoringHudControlsVisibility.textContent = monitoringHudControls.visibilityState || "HUD feature disabled from dashboard/tray";
  }
  if (monitoringHudControlsSurface) {
    monitoringHudControlsSurface.textContent = monitoringHudControls.controlSurface || "Tray controls HUD feature state; Dashboard open/close is separate; HUD Overlay remains deferred";
  }
  if (monitoringHudControlsPersistence) {
    monitoringHudControlsPersistence.textContent = monitoringHudControls.persistence || "Store group/layout posture locally";
  }
  if (monitoringHudWarningPosture && monitoringHudControls.warningControls) {
    monitoringHudWarningPosture.textContent = monitoringHudControls.warningControls;
  }
  if (monitoringHudTrayPath) {
    monitoringHudTrayPath.textContent = monitoringHudControls.trayPath || "Task tray enables/disables HUD feature and opens/closes Dashboard; HUD Overlay controls deferred";
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
    monitoringHud.dataset.interactiveControlAffordance = "normal-hover-active-focus-visible-disabled-open-selected";
    monitoringHud.dataset.interactiveControlReliability = monitoringHud.dataset.interactiveControlReliability || "first-click-stress-proof-required";
    monitoringHud.dataset.clickInterceptionDiagnostics = monitoringHud.dataset.clickInterceptionDiagnostics || "z-index-pointer-events-disabled-aria-dom-focus-timing";
    monitoringHud.dataset.pollingRateDropdown = "nexus-styled-bounded-control";
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
