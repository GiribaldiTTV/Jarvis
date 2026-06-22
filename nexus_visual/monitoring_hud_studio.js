(() => {
  const commandPrefix = "NEXUS_MONITORING_HUD_STUDIO_COMMAND:";
  const byId = (id) => document.getElementById(id);
  const setText = (id, value) => {
    const target = byId(id);
    if (target) {
      target.textContent = String(value || "");
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

  const bindRecordingToggle = () => {
    const target = byId("monitoring-hud-studio-recording-toggle-action");
    if (!target) {
      return;
    }
    target.addEventListener("click", () => {
      const command = target.dataset.recordingCommand === "stop" ? "stop" : "start";
      emitCommand(command);
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
      ? "fam006-log-viewer-studio"
      : "fam006-recording-studio";
    surface.dataset.productSurfaceRole = mode === "log-viewer"
      ? "compact-current-branch-log-access-shell"
      : "ultra-lightweight-detached-recording-controller";
    surface.dataset.featureStudioPurpose = surface.dataset.productSurfaceRole;
    surface.dataset.resizeContract = mode === "log-viewer"
      ? "resizable-log-access-shell"
      : "not-resizable-position-memory-only";
    surface.dataset.fixedControllerHeight = mode === "log-viewer" ? "not-applicable" : "238";
    surface.setAttribute(
      "aria-label",
      mode === "log-viewer"
        ? "Nexus Desktop AI Log Viewer Studio"
        : "Nexus Desktop AI Recording Studio",
    );
    setText("monitoring-hud-studio-kicker", payload.kicker || "Nexus Desktop AI");
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
    setText("monitoring-hud-studio-recording-target", state.recordingTarget || "No active overlay profile");
    setText("monitoring-hud-studio-recording-status", state.recordingStatus || state.recordingState || "Ready for local recording.");
    setText("monitoring-hud-studio-recording-boundary", state.recordingBoundary || "");
    const toggle = byId("monitoring-hud-studio-recording-toggle-action");
    const isRecording = state.stopEnabled === true;
    if (toggle) {
      const label = isRecording ? "Stop Recording" : "Start Recording";
      toggle.dataset.recordingCommand = isRecording ? "stop" : "start";
      toggle.dataset.recordingState = isRecording ? "recording-active" : "recording-ready";
      toggle.setAttribute("aria-label", label);
      const labelTarget = toggle.querySelector(".monitoring-hud__button-label");
      if (labelTarget) {
        labelTarget.textContent = label;
      } else {
        toggle.textContent = label;
      }
    }
    setActionState("monitoring-hud-studio-recording-toggle-action", isRecording || state.startEnabled === true);
    setText("monitoring-hud-studio-native-folder", state.nativeFolder || "");
    setText("monitoring-hud-studio-export-folder", state.exportFolder || "");
    setText("monitoring-hud-studio-log-boundary", state.logBoundary || "");
    setText("monitoring-hud-studio-folder-status", state.folderStatus || "Native and exported log folders are ready to open.");
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
  bindRecordingToggle();
  bindCommand("monitoring-hud-studio-open-log-viewer-action", "open-log-viewer");
  bindCommand("monitoring-hud-studio-open-native-action", "open-native");
  bindCommand("monitoring-hud-studio-open-export-action", "open-export");
  window.nexusMonitoringHudStudioApplyState(window.NEXUS_MONITORING_HUD_STUDIO_INITIAL_STATE || {});
})();
