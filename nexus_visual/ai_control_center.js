(() => {
  const commandPrefix = "NEXUS_AI_CONTROL_CENTER_COMMAND:";
  let providerState = {};
  let scrollbarDrag = null;

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
    const providerExecution = (
      providerState.providerExecutionGateState === "provider-execution-disabled"
      && providerState.modelExecutionGateState === "model-execution-disabled"
    )
      ? "disabled and blocked"
      : (providerState.providerExecutionGateLabel || "disabled and blocked");
    const rawCapabilityPacks = String(providerState.installIntentLabel || "");
    let capabilityPacks = rawCapabilityPacks || "install blocked; downloads disabled";
    if (
      String(providerState.installIntentState || "").toLowerCase().includes("blocked")
      || rawCapabilityPacks.toLowerCase().includes("blocked")
    ) {
      capabilityPacks = "install blocked; downloads disabled";
    }
    if (!String(capabilityPacks).toLowerCase().includes("download")) {
      capabilityPacks = `${capabilityPacks}; downloads disabled`;
    }
    const providerVisibleData = providerState.providerVisibleData || "none";
    const providerVisibleDataDetail = providerVisibleData === "none"
      ? "No prompt, file, memory, telemetry, or provider config is sent."
      : (
        providerState.providerVisibleDataDetail
        || "Provider-visible data state requires review before any provider path runs."
      );

    setText("ai-control-center-orin-state", "Not implemented; no real AI executing");
    setText("ai-control-center-provider-visible-data", providerVisibleData);
    setText("ai-control-center-provider-model", providerExecution);
    setText("ai-control-center-prompt-memory", "not accepted, sent, stored, or indexed");
    setText("ai-control-center-capability-packs", capabilityPacks);
    setText("ai-control-center-edition-lanes", "Public only; Developer and Owner gated");
    setText("ai-control-center-local-result", "waiting for local action");
    setText(
      "ai-control-center-local-detail",
      providerVisibleDataDetail,
    );
    requestAnimationFrame(syncCustomScrollbar);
  };

  window.nexusAiControlCenterRunLocalCheck = () => {
    const guardClosed = providerState.sentToProvider === false
      && providerState.canAcceptPrompts === false
      && providerState.providerVisibleData === "none"
      && providerState.promptSendPosture === "prompt-send-disabled"
      && providerState.networkEgressState === "network-egress-blocked"
      && providerState.memoryIndexingState === "memory-indexing-disabled";
    setText(
      "ai-control-center-local-result",
      guardClosed ? (providerState.localActionResultLabel || "no provider configured") : "Local check: blocked",
    );
    setText(
      "ai-control-center-local-detail",
      guardClosed
        ? (providerState.localActionResultDetail || "No prompt was accepted or sent; provider-visible data remains none.")
        : "Provider boundary mismatch; no local result was produced.",
    );
  };

  byId("ai-control-center-close-action")?.addEventListener("click", () => emitCommand("close"));
  byId("ai-control-center-local-check-action")?.addEventListener("click", () => {
    window.nexusAiControlCenterRunLocalCheck();
    emitCommand("run-local-check");
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
  requestAnimationFrame(syncCustomScrollbar);
})();
