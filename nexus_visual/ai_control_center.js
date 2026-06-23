(() => {
  const commandPrefix = "NEXUS_AI_CONTROL_CENTER_COMMAND:";
  let providerState = {};
  let scrollbarDrag = null;
  let currentReadinessReportText = "";
  const windowControlStates = {
    minimize: "active",
    maximizeRestore: "hidden",
    close: "active",
  };
  const windowControlDefaults = {
    minimize: {
      id: "ai-control-center-minimize-action",
      command: "minimize",
      activeLabel: "Minimize AI Dashboard",
      blockedLabel: "Minimize AI Dashboard blocked",
      hiddenLabel: "Minimize AI Dashboard hidden",
    },
    maximizeRestore: {
      id: "ai-control-center-maximize-action",
      command: "maximize-restore",
      activeLabel: "Maximize AI Dashboard",
      activeMaximizedLabel: "Restore AI Dashboard",
      blockedLabel: "Maximize or restore AI Dashboard blocked",
      hiddenLabel: "Maximize or restore AI Dashboard hidden until future implementation",
    },
    close: {
      id: "ai-control-center-close-action",
      command: "close",
      activeLabel: "Close AI Dashboard",
      blockedLabel: "Close AI Dashboard blocked",
      hiddenLabel: "Close AI Dashboard hidden",
    },
  };
  const validWindowControlStates = new Set(["hidden", "blocked", "active"]);

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
  const formatReportItems = (items, keys = ["label"]) => {
    const list = Array.isArray(items) ? items : [];
    if (!list.length) {
      return "None";
    }
    return list
      .map((item) => {
        if (item && typeof item === "object") {
          return keys
            .map((key) => String(item[key] || "").trim())
            .filter(Boolean)
            .join(" - ");
        }
        return String(item || "").trim();
      })
      .filter(Boolean)
      .join("; ");
  };
  const buildReportText = (report) => {
    const title = String(report.title || "Local AI Readiness Report");
    const lines = [
      title,
      "",
      `Summary: ${String(report.summary || "No local readiness report is available.")}`,
      `Useful outcome: ${String(report.usefulOutcome || "Not available")}`,
      `Provider-visible data: ${String(report.providerVisibleData || "none")}`,
      `Copy/persistence: ${String(report.copyMode || "clipboard-only-user-initiated")} / ${String(report.persistence || "view-only-no-file-persistence")}`,
      "",
      `Ready: ${formatReportItems(report.readyConditions, ["label", "evidence"])}`,
      `Missing: ${formatReportItems(report.missingRequirements, ["label", "reason"])}`,
      `Blocked: ${formatReportItems(report.blockedPaths, ["label", "state", "gate"])}`,
      `Evidence checked: ${formatReportItems(report.localEvidenceChecked)}`,
      `Safe next steps: ${formatReportItems(report.safeNextSteps)}`,
      `Trust boundaries: ${formatReportItems(report.trustBoundaries)}`,
    ];
    return lines.join("\n");
  };
  const setReportCopyEnabled = (enabled) => {
    const button = byId("ai-control-center-copy-report-action");
    if (!button) {
      return;
    }
    button.disabled = !enabled;
    button.setAttribute("aria-disabled", enabled ? "false" : "true");
  };
  const setReadinessDetailOpen = (open) => {
    setFocusedSurfaceOpen("ai-control-center-readiness-detail", open);
  };
  const setFocusedSurfaceOpen = (surfaceId, open) => {
    const detail = byId(surfaceId);
    if (!detail) {
      return;
    }
    detail.hidden = !open;
    detail.dataset.focusedSurfaceState = open ? "open" : "closed";
    detail.dataset.surfaceOpen = open ? "true" : "false";
  };
  const openFocusedSurface = (surfaceId, commandName) => {
    const surfaces = Array.from(document.querySelectorAll("[data-focused-surface]"));
    surfaces.forEach((surface) => setFocusedSurfaceOpen(surface.id, surface.id === surfaceId));
    const surface = byId(surfaceId);
    if (surface) {
      surface.scrollIntoView({ block: "nearest" });
    }
    if (commandName) {
      emitCommand(commandName);
    }
    requestAnimationFrame(syncCustomScrollbar);
  };
  const copyTextThroughLocalSurface = (text) => {
    const copySurface = document.createElement("textarea");
    copySurface.value = text;
    copySurface.setAttribute("readonly", "");
    copySurface.style.position = "fixed";
    copySurface.style.left = "-9999px";
    copySurface.style.top = "0";
    document.body.appendChild(copySurface);
    copySurface.focus();
    copySurface.select();
    const copied = document.execCommand("copy");
    copySurface.remove();
    return copied;
  };
  const renderReadinessReport = (report) => {
    const normalized = report && typeof report === "object" ? report : {};
    const guardClosed = (
      normalized.providerVisibleData === "none"
      && normalized.sentToProvider === false
      && normalized.canAcceptPrompts === false
      && normalized.promptSendPosture === "prompt-send-disabled"
      && normalized.networkEgressState === "network-egress-blocked"
      && normalized.memoryIndexingState === "memory-indexing-disabled"
    );
    const body = byId("ai-control-center-report-body");
    if (!guardClosed) {
      currentReadinessReportText = "";
      setText("ai-control-center-report-state", "Blocked by boundary mismatch");
      setText("ai-control-center-report-summary", "Report blocked because local trust-boundary proof is inconsistent.");
      if (body) {
        body.hidden = true;
      }
      setReadinessDetailOpen(true);
      setReportCopyEnabled(false);
      requestAnimationFrame(syncCustomScrollbar);
      return false;
    }

    currentReadinessReportText = buildReportText(normalized);
    setText("ai-control-center-report-state", "Generated locally");
    setText("ai-control-center-report-persistence", "View-only; copy is USER initiated");
    setText("ai-control-center-report-summary", normalized.summary || "Local readiness report generated.");
    setText("ai-control-center-report-ready", formatReportItems(normalized.readyConditions, ["label", "evidence"]));
    setText("ai-control-center-report-missing", formatReportItems(normalized.missingRequirements, ["label", "reason"]));
    setText("ai-control-center-report-blocked", formatReportItems(normalized.blockedPaths, ["label", "state", "gate"]));
    setText("ai-control-center-report-evidence", formatReportItems(normalized.localEvidenceChecked));
    setText("ai-control-center-report-next", formatReportItems(normalized.safeNextSteps));
    setText("ai-control-center-report-boundary", formatReportItems(normalized.trustBoundaries));
    if (body) {
      body.hidden = false;
    }
    setReadinessDetailOpen(true);
    byId("ai-control-center-readiness-detail")?.scrollIntoView({ block: "nearest" });
    setReportCopyEnabled(true);
    requestAnimationFrame(syncCustomScrollbar);
    return true;
  };
  const copyReadinessReport = async () => {
    if (!currentReadinessReportText) {
      setText("ai-control-center-report-state", "Generate report before copying");
      return false;
    }
    try {
      if (copyTextThroughLocalSurface(currentReadinessReportText)) {
        setText("ai-control-center-report-state", "Copied locally");
        return true;
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(currentReadinessReportText);
      } else {
        throw new Error("clipboard unavailable");
      }
      setText("ai-control-center-report-state", "Copied locally");
      return true;
    } catch (error) {
      setText("ai-control-center-report-state", "Copy unavailable; report remains visible");
      return false;
    }
  };
  const attachActivationHandler = (element, handler) => {
    if (!element || typeof handler !== "function") {
      return;
    }
    let lastActivationAt = 0;
    const activate = (event) => {
      const now = Date.now();
      if (now - lastActivationAt < 90) {
        return;
      }
      lastActivationAt = now;
      handler(event);
    };
    element.addEventListener("click", activate);
    element.addEventListener("pointerup", activate);
  };
  const stripNativeTooltips = () => {
    const surface = byId("monitoring-hud");
    if (!surface) {
      return;
    }
    surface.querySelectorAll("[title]").forEach((element) => {
      element.removeAttribute("title");
    });
  };
  const observeNativeTooltipDrift = () => {
    const surface = byId("monitoring-hud");
    if (!surface || !window.MutationObserver) {
      return;
    }
    const observer = new MutationObserver(() => {
      stripNativeTooltips();
    });
    observer.observe(surface, {
      attributes: true,
      attributeFilter: ["title"],
      childList: true,
      subtree: true,
    });
  };

  const normalizeWindowControlState = (value) => (
    validWindowControlStates.has(value) ? value : "blocked"
  );

  const hydrateWindowControlStatesFromMarkup = () => {
    Object.entries(windowControlDefaults).forEach(([key, config]) => {
      const button = byId(config.id);
      if (!button) {
        return;
      }
      windowControlStates[key] = normalizeWindowControlState(
        button.dataset.windowControlState || windowControlStates[key],
      );
      button.dataset.windowControlKey = key;
      button.dataset.windowControlCommand = button.dataset.windowControlCommand || config.command;
      button.removeAttribute("title");
    });
  };

  const syncSingleWindowControlState = (key, windowState) => {
    const config = windowControlDefaults[key];
    const button = config ? byId(config.id) : null;
    if (!button) {
      return;
    }
    const controlState = normalizeWindowControlState(windowControlStates[key]);
    button.dataset.windowControlState = controlState;
    button.removeAttribute("title");

    if (key === "maximizeRestore") {
      button.dataset.windowState = controlState === "active" ? windowState : controlState;
    }

    if (controlState === "hidden") {
      button.hidden = true;
      button.disabled = true;
      button.tabIndex = -1;
      button.setAttribute("aria-hidden", "true");
      button.setAttribute("aria-disabled", "true");
      button.setAttribute("aria-label", config.hiddenLabel);
      button.removeAttribute("aria-pressed");
      return;
    }

    button.hidden = false;
    button.removeAttribute("aria-hidden");
    if (controlState === "blocked") {
      button.disabled = true;
      button.tabIndex = -1;
      button.setAttribute("aria-disabled", "true");
      button.setAttribute("aria-label", config.blockedLabel);
      button.removeAttribute("aria-pressed");
      return;
    }

    button.disabled = false;
    button.tabIndex = 0;
    button.removeAttribute("aria-disabled");
    if (key === "maximizeRestore") {
      button.setAttribute("aria-pressed", windowState === "maximized" ? "true" : "false");
      button.setAttribute(
        "aria-label",
        windowState === "maximized" ? config.activeMaximizedLabel : config.activeLabel,
      );
      return;
    }
    button.setAttribute("aria-label", config.activeLabel);
  };

  const syncWindowControlState = (state, controlStateOverrides = null) => {
    const surface = byId("monitoring-hud");
    const normalized = state === "maximized" ? "maximized" : "normal";
    if (controlStateOverrides && typeof controlStateOverrides === "object") {
      Object.keys(windowControlDefaults).forEach((key) => {
        if (Object.prototype.hasOwnProperty.call(controlStateOverrides, key)) {
          windowControlStates[key] = normalizeWindowControlState(controlStateOverrides[key]);
        }
      });
    }
    if (surface) {
      surface.dataset.windowState = normalized;
    }
    Object.keys(windowControlDefaults).forEach((key) => syncSingleWindowControlState(key, normalized));
  };
  window.nexusAiControlCenterSetWindowState = syncWindowControlState;
  window.nexusAiControlCenterSetWindowControlStates = (states) => {
    syncWindowControlState(byId("monitoring-hud")?.dataset.windowState || "normal", states);
  };

  const syncCustomScrollbar = () => {
    const surface = byId("monitoring-hud");
    const chrome = surface?.querySelector(".monitoring-hud__chrome");
    const hub = byId("ai-control-center-card-hub");
    const rail = byId("ai-control-center-scrollbar");
    const track = byId("ai-control-center-scrollbar-track");
    const thumb = byId("ai-control-center-scrollbar-thumb");
    if (!surface || !chrome || !hub || !rail || !track || !thumb) {
      return;
    }

    const maxScroll = Math.max(0, hub.scrollHeight - hub.clientHeight);
    surface.dataset.customScrollbarVisible = maxScroll > 1 ? "true" : "false";
    if (maxScroll <= 1) {
      thumb.style.height = "44px";
      thumb.style.transform = "translateY(0px)";
      return;
    }

    const chromeRect = chrome.getBoundingClientRect();
    const hubRect = hub.getBoundingClientRect();
    const trackTop = Math.max(0, hubRect.top - chromeRect.top + 10);
    const trackHeight = Math.max(44, hubRect.height - 26);
    const rightInset = Math.max(10, chromeRect.right - hubRect.right + 4);
    rail.style.top = `${trackTop}px`;
    rail.style.right = `${rightInset}px`;
    rail.style.height = `${trackHeight}px`;

    const thumbHeight = Math.max(44, Math.round(trackHeight * (hub.clientHeight / hub.scrollHeight)));
    const travel = Math.max(0, trackHeight - thumbHeight);
    const y = Math.round((hub.scrollTop / maxScroll) * travel);
    thumb.style.height = `${thumbHeight}px`;
    thumb.style.transform = `translateY(${y}px)`;
  };
  window.nexusAiControlCenterSyncScrollbar = syncCustomScrollbar;

  const scrollHubToTrackPosition = (clientY) => {
    const hub = byId("ai-control-center-card-hub");
    const track = byId("ai-control-center-scrollbar-track");
    const thumb = byId("ai-control-center-scrollbar-thumb");
    if (!hub || !track || !thumb) {
      return;
    }
    const maxScroll = Math.max(0, hub.scrollHeight - hub.clientHeight);
    const trackRect = track.getBoundingClientRect();
    const thumbHeight = thumb.getBoundingClientRect().height || 44;
    const travel = Math.max(1, trackRect.height - thumbHeight);
    const y = Math.min(Math.max(0, clientY - trackRect.top - (thumbHeight / 2)), travel);
    hub.scrollTop = Math.round((y / travel) * maxScroll);
    syncCustomScrollbar();
  };

  window.nexusAiControlCenterApplyProviderState = (payload) => {
    providerState = payload && typeof payload === "object" ? payload : {};
    const firstText = (...values) => {
      for (const value of values) {
        const text = String(value || "").trim();
        if (text) {
          return text;
        }
      }
      return "";
    };
    const providerExecution = (
      providerState.providerExecutionGateState === "provider-execution-disabled"
      && providerState.modelExecutionGateState === "model-execution-disabled"
    )
      ? "Disabled and blocked"
      : (providerState.providerExecutionGateLabel || "Disabled and blocked");
    const rawCapabilityPacks = String(providerState.installIntentLabel || "");
    let capabilityPacks = rawCapabilityPacks || "Install blocked; downloads disabled";
    if (
      String(providerState.installIntentState || "").toLowerCase().includes("blocked")
      || rawCapabilityPacks.toLowerCase().includes("blocked")
    ) {
      capabilityPacks = "Install blocked; downloads disabled";
    }
    if (!String(capabilityPacks).toLowerCase().includes("download")) {
      capabilityPacks = `${capabilityPacks}; downloads disabled`;
    }
    const providerVisibleData = providerState.providerVisibleData || "none";
    const providerVisibleDataDisplay = providerVisibleData === "none" ? "None" : providerVisibleData;
    const providerVisibleDataDetail = providerVisibleData === "none"
      ? "No prompt, file, memory, telemetry, or provider config is sent."
      : (
        providerState.providerVisibleDataDetail
        || "Provider-visible data state requires review before any provider path runs."
      );
    const diagnosticLabel = firstText(
      providerState.aiControlCenterDiagnosticLabel,
      "No provider configured; fail-closed",
    );
    const boundaryLabel = firstText(
      providerState.aiControlCenterProviderBoundaryLabel,
      "Provider boundary: blocked",
    );
    const blockedActionLabel = firstText(
      providerState.aiControlCenterBlockedActionLabel,
      "Prompt/provider/model action blocked",
    );
    const unavailableCapabilityLabel = firstText(
      providerState.aiControlCenterUnavailableCapabilityLabel,
      "Capability packs unavailable",
    );
    const recoveryLabel = firstText(
      providerState.aiControlCenterRecoveryLabel,
      "Retry local check only",
    );
    const degradedPathLabel = firstText(
      providerState.aiControlCenterDegradedPathLabel,
      "Local guidance only",
    );

    setText("ai-control-center-orin-state", "Not implemented; no real AI executing");
    setText("ai-control-center-provider-visible-data", providerVisibleDataDisplay);
    setText("ai-control-center-provider-model", providerExecution);
    setText("ai-control-center-prompt-memory", "Not accepted, sent, stored, or indexed");
    setText("ai-control-center-capability-packs", capabilityPacks);
    setText("ai-control-center-maintenance-updates", "Lifecycle placement only; update execution blocked");
    setText("ai-control-center-edition-lanes", "Public only; Developer and Owner gated");
    setText("ai-control-center-provider-boundary", boundaryLabel);
    setText("ai-control-center-diagnostic-state", diagnosticLabel);
    setText("ai-control-center-recovery", recoveryLabel);
    setText("ai-control-center-local-result", "Waiting for local action");
    setText(
      "ai-control-center-local-detail",
      providerVisibleDataDetail,
    );
    setText("ai-control-center-blocked-action", blockedActionLabel);
    setText("ai-control-center-unavailable-capability", unavailableCapabilityLabel);
    setText("ai-control-center-degraded-path", degradedPathLabel);
    currentReadinessReportText = "";
    setText("ai-control-center-report-state", "Not generated");
    setText("ai-control-center-report-persistence", "View-only; copy is USER initiated");
    setText("ai-control-center-report-summary", "Generate the report to inspect local readiness.");
    byId("ai-control-center-report-body")?.setAttribute("hidden", "");
    Array.from(document.querySelectorAll("[data-focused-surface]")).forEach((surface) => {
      setFocusedSurfaceOpen(surface.id, false);
    });
    setReportCopyEnabled(false);
    requestAnimationFrame(syncCustomScrollbar);
  };

  window.nexusAiControlCenterRunLocalCheck = () => {
    const guardClosed = providerState.sentToProvider === false
      && providerState.canAcceptPrompts === false
      && providerState.providerVisibleData === "none"
      && providerState.promptSendPosture === "prompt-send-disabled"
      && providerState.networkEgressState === "network-egress-blocked"
      && providerState.memoryIndexingState === "memory-indexing-disabled";
    const rawLocalResult = String(providerState.localActionResultLabel || "No provider configured");
    const localResult = rawLocalResult === "No-provider check: no provider configured"
      ? "No provider configured"
      : rawLocalResult.replace(": no provider configured", ": No provider configured");
    const localDetail = String(
      providerState.localActionResultDetail
      || "No prompt was accepted or sent; provider-visible data remains none. Capability packs, private lanes, downloads, memory, and network remain blocked.",
    );
    setText(
      "ai-control-center-local-result",
      guardClosed ? localResult : "Local check: blocked",
    );
    setText(
      "ai-control-center-local-detail",
      guardClosed
        ? localDetail
        : "Provider boundary mismatch; no local result was produced.",
    );
    setText(
      "ai-control-center-diagnostic-state",
      guardClosed
        ? (providerState.aiControlCenterDiagnosticLabel || "No provider configured; fail-closed")
        : "Boundary mismatch; fail-closed",
    );
    setText(
      "ai-control-center-blocked-action",
      guardClosed
        ? (providerState.aiControlCenterBlockedActionLabel || "Prompt/provider/model action blocked")
        : "Local check blocked by boundary mismatch",
    );
    requestAnimationFrame(syncCustomScrollbar);
  };
  window.nexusAiControlCenterGenerateReadinessReport = () => (
    renderReadinessReport(providerState.localAiReadinessReport || {})
  );
  window.nexusAiControlCenterCopyReadinessReport = copyReadinessReport;

  const attachWindowControlHandlers = () => {
    Object.entries(windowControlDefaults).forEach(([key, config]) => {
      const button = byId(config.id);
      if (!button) {
        return;
      }
      button.addEventListener("click", (event) => {
        if (button.hidden || button.disabled || button.dataset.windowControlState !== "active") {
          event.preventDefault();
          event.stopPropagation();
          return;
        }
        const command = button.dataset.windowControlCommand || config.command;
        if (command) {
          emitCommand(command);
        }
      });
    });
  };

  hydrateWindowControlStatesFromMarkup();
  stripNativeTooltips();
  observeNativeTooltipDrift();
  attachWindowControlHandlers();
  attachActivationHandler(byId("ai-control-center-open-control-surface-action"), () => {
    openFocusedSurface("ai-control-center-control-surface", "open-ai-control-center-domain-surface");
  });
  attachActivationHandler(byId("ai-control-center-open-readiness-surface-action"), () => {
    openFocusedSurface("ai-control-center-readiness-detail", "open-ai-readiness-diagnostics-surface");
  });
  attachActivationHandler(byId("ai-control-center-open-maintenance-surface-action"), () => {
    openFocusedSurface("ai-control-center-maintenance-detail", "open-ai-maintenance-lifecycle-surface");
  });
  attachActivationHandler(byId("ai-control-center-local-check-action"), () => {
    setReadinessDetailOpen(true);
    window.nexusAiControlCenterRunLocalCheck();
    emitCommand("run-local-check");
  });
  attachActivationHandler(byId("ai-control-center-generate-report-action"), () => {
    setReadinessDetailOpen(true);
    const generated = window.nexusAiControlCenterGenerateReadinessReport();
    emitCommand(generated ? "generate-readiness-report" : "generate-readiness-report-blocked");
  });
  attachActivationHandler(byId("ai-control-center-copy-report-action"), () => {
    window.nexusAiControlCenterCopyReadinessReport().then((copied) => {
      emitCommand(copied ? "copy-readiness-report" : "copy-readiness-report-blocked");
    });
  });
  attachActivationHandler(byId("ai-dashboard-settings-action"), () => {
    setText("ai-dashboard-settings-status", "Global Settings / AI route is future-gated; no settings window opened.");
    emitCommand("open-settings-future-gated");
  });

  byId("ai-control-center-card-hub")?.addEventListener("scroll", syncCustomScrollbar, { passive: true });
  byId("ai-control-center-scrollbar-track")?.addEventListener("mousedown", (event) => {
    event.preventDefault();
    scrollHubToTrackPosition(event.clientY);
  });
  byId("ai-control-center-scrollbar-thumb")?.addEventListener("mousedown", (event) => {
    event.preventDefault();
    event.stopPropagation();
    scrollbarDrag = { startY: event.clientY, startScrollTop: byId("ai-control-center-card-hub")?.scrollTop || 0 };
  });
  window.addEventListener("mousemove", (event) => {
    if (!scrollbarDrag) {
      return;
    }
    const hub = byId("ai-control-center-card-hub");
    const track = byId("ai-control-center-scrollbar-track");
    const thumb = byId("ai-control-center-scrollbar-thumb");
    if (!hub || !track || !thumb) {
      return;
    }
    const maxScroll = Math.max(0, hub.scrollHeight - hub.clientHeight);
    const travel = Math.max(1, track.getBoundingClientRect().height - thumb.getBoundingClientRect().height);
    const delta = event.clientY - scrollbarDrag.startY;
    hub.scrollTop = Math.round(scrollbarDrag.startScrollTop + ((delta / travel) * maxScroll));
    syncCustomScrollbar();
  });
  window.addEventListener("mouseup", () => {
    scrollbarDrag = null;
  });
  window.addEventListener("resize", syncCustomScrollbar);
  window.addEventListener("load", () => requestAnimationFrame(syncCustomScrollbar));
  syncWindowControlState("normal");
  requestAnimationFrame(syncCustomScrollbar);
})();
