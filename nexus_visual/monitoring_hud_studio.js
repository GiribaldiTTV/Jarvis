(() => {
  const commandPrefix = "NEXUS_MONITORING_HUD_STUDIO_COMMAND:";
  const byId = (id) => document.getElementById(id);
  const setText = (id, value) => {
    const target = byId(id);
    if (target) {
      target.textContent = String(value || "");
    }
  };
  const setTitle = (id, value) => {
    const target = byId(id);
    if (target) {
      const text = String(value || "");
      if (text) {
        target.setAttribute("title", text);
      } else {
        target.removeAttribute("title");
      }
    }
  };
  const emitCommand = (name) => {
    console.info(`${commandPrefix}${name}`);
  };

  const windowControls = {
    minimize: "monitoring-hud-studio-minimize-action",
    close: "monitoring-hud-studio-close-action",
  };

  const bindCommand = (id, command) => {
    const target = byId(id);
    if (!target) {
      return;
    }
    target.addEventListener("click", () => emitCommand(command));
  };

  const bindRecordingCommand = (id, command) => {
    const target = byId(id);
    if (!target) {
      return;
    }
    target.addEventListener("click", () => {
      emitCommand(target.dataset.recordingCommand || command);
    });
  };

  const setActionState = (id, enabled) => {
    const target = byId(id);
    if (!target) {
      return;
    }
    target.disabled = !enabled;
    target.setAttribute("aria-disabled", enabled ? "false" : "true");
  };

  const applySurface = (payload) => {
    const surface = byId("monitoring-hud");
    if (!surface) {
      return;
    }
    const mode = payload.surface === "log-viewer" ? "log-viewer" : "recording";
    surface.dataset.studioSurface = mode;
    surface.dataset.surfaceId = mode === "log-viewer"
      ? "fam006-log-viewer"
      : "fam006-recording-studio";
    surface.dataset.productSurfaceRole = mode === "log-viewer"
      ? "compact-current-branch-log-access-shell"
      : "ultra-lightweight-detached-recording-controller";
    surface.dataset.featureStudioPurpose = surface.dataset.productSurfaceRole;
    surface.dataset.featureStudioPrimitive = "fam006-unique-child-studio-shell-v5";
    surface.dataset.windowTaxonomy = "unique-child-standalone-feature-studio";
    surface.dataset.windowResizeTaxonomy = "no-resize-recording-edge-resize-log-viewer";
    surface.dataset.attachedChildResizeGrip = "absent";
    surface.dataset.resizeContract = mode === "log-viewer"
      ? "edge-resizable-log-access-shell"
      : "not-resizable-position-memory-only";
    surface.dataset.fixedControllerHeight = mode === "log-viewer" ? "not-applicable" : "144";
    surface.dataset.titleTreatment = "detached-child-window-header-no-title-card";
    surface.dataset.titleCardState = "absent";
    surface.dataset.childWindowTitleGrammar = "title-first-description-beneath-no-title-card";
    surface.setAttribute(
      "aria-label",
      mode === "log-viewer"
        ? "Nexus Desktop AI Log Viewer"
        : "Nexus Desktop AI Recording Studio",
    );
    setText("monitoring-hud-studio-kicker", payload.kicker || (mode === "log-viewer" ? "NATIVE AND EXPORTED LOG ACCESS" : "ACTIVE OVERLAY RECORDING"));
    setText("monitoring-hud-studio-title", payload.title || "");
    setText("monitoring-hud-studio-subtitle", payload.subtitle || "");
    setText("monitoring-hud-studio-role-label-a", payload.roleLabelA || "Surface");
    setText("monitoring-hud-studio-role-value-a", payload.roleValueA || "");
    setText("monitoring-hud-studio-role-label-b", payload.roleLabelB || "State");
    setText("monitoring-hud-studio-role-value-b", payload.roleValueB || "");
    setText("monitoring-hud-studio-role-label-c", payload.roleLabelC || "Boundary");
    setText("monitoring-hud-studio-role-value-c", payload.roleValueC || "");
    byId("monitoring-hud-studio-recording-card").hidden = mode !== "recording";
    byId("monitoring-hud-studio-log-card").hidden = mode !== "log-viewer";
  };

  window.nexusMonitoringHudStudioApplyState = (payload) => {
    const state = payload && typeof payload === "object" ? payload : {};
    applySurface(state);
    setText("monitoring-hud-studio-recording-state-label", state.recordingStateLabel || "Now");
    setText("monitoring-hud-studio-recording-target", state.recordingTarget || "No active overlay profile");
    setText("monitoring-hud-studio-recording-target-detail", state.recordingTargetDetail || "No active monitors.");
    setText("monitoring-hud-studio-recording-status", state.recordingStatus || state.recordingState || "Selected overlay ready.");
    setText("monitoring-hud-studio-recording-detail", state.recordingDetail || "");
    setText("monitoring-hud-studio-recording-boundary", state.recordingBoundary || "");
    const start = byId("monitoring-hud-studio-start-action");
    const pause = byId("monitoring-hud-studio-pause-action");
    const stop = byId("monitoring-hud-studio-stop-action");
    if (start) {
      start.dataset.recordingState = state.pausedResumeEnabled === true ? "recording-paused-resume" : "recording-ready";
      start.setAttribute("aria-label", state.pausedResumeEnabled === true ? "Resume Recording" : "Start Recording");
    }
    if (pause) {
      pause.dataset.recordingState = state.pauseEnabled === true ? "recording-active-pause" : "recording-pause-disabled";
    }
    if (stop) {
      stop.dataset.recordingState = state.stopEnabled === true ? "recording-stop-enabled" : "recording-stop-disabled";
    }
    setActionState("monitoring-hud-studio-start-action", state.startEnabled === true || state.pausedResumeEnabled === true);
    setActionState("monitoring-hud-studio-pause-action", state.pauseEnabled === true);
    setActionState("monitoring-hud-studio-stop-action", state.stopEnabled === true);
    setText("monitoring-hud-studio-viewer-state", state.viewerState || "Deferred");
    setTitle("monitoring-hud-studio-viewer-state", state.viewerStateTooltip || "Full in-app log viewing remains future-gated.");
    setText("monitoring-hud-studio-log-boundary", state.logBoundary || "");
    const folderStatus = state.folderStatus || "Choose a log destination to open.";
    setText("monitoring-hud-studio-folder-status", folderStatus);
    const statusContainer = document.querySelector("[data-element-group='log-folder-action-status']");
    if (statusContainer) {
      statusContainer.hidden = folderStatus === "Choose a log destination to open.";
    }
  };

  window.nexusMonitoringHudStudioSetWindowState = (state, controls = {}) => {
    const surface = byId("monitoring-hud");
    if (surface) {
      surface.dataset.windowState = state === "maximized" ? "maximized" : "normal";
    }
    Object.entries(windowControls).forEach(([key, id]) => {
      const button = byId(id);
      if (!button) {
        return;
      }
      const controlState = controls[key] || "active";
      button.dataset.windowControlState = controlState;
      if (controlState === "hidden") {
        button.hidden = true;
        button.disabled = true;
        button.tabIndex = -1;
        button.setAttribute("aria-hidden", "true");
        button.setAttribute("aria-disabled", "true");
        return;
      }
      button.hidden = false;
      button.removeAttribute("aria-hidden");
      button.disabled = controlState !== "active";
      button.tabIndex = controlState === "active" ? 0 : -1;
      button.setAttribute("aria-disabled", controlState === "active" ? "false" : "true");
    });
  };

  bindCommand("monitoring-hud-studio-minimize-action", "minimize");
  bindCommand("monitoring-hud-studio-close-action", "close");
  bindRecordingCommand("monitoring-hud-studio-start-action", "start");
  bindRecordingCommand("monitoring-hud-studio-pause-action", "pause");
  bindRecordingCommand("monitoring-hud-studio-stop-action", "stop");
  bindCommand("monitoring-hud-studio-open-log-viewer-action", "open-log-viewer");
  bindCommand("monitoring-hud-studio-open-native-action", "open-native");
  bindCommand("monitoring-hud-studio-open-export-action", "open-export");
  window.nexusMonitoringHudStudioApplyState(window.NEXUS_MONITORING_HUD_STUDIO_INITIAL_STATE || {});
})();
