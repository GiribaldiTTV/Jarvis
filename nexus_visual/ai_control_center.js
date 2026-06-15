(() => {
  const commandPrefix = "NEXUS_AI_CONTROL_CENTER_COMMAND:";
  let providerState = {};

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

  window.nexusAiControlCenterApplyProviderState = (payload) => {
    providerState = payload && typeof payload === "object" ? payload : {};
    const providerExecution = (
      providerState.providerExecutionGateState === "provider-execution-disabled"
      && providerState.modelExecutionGateState === "model-execution-disabled"
    )
      ? "disabled and blocked"
      : (providerState.providerExecutionGateLabel || "disabled and blocked");
    let capabilityPacks = providerState.installIntentLabel || "install intent blocked; downloads disabled";
    if (!String(capabilityPacks).toLowerCase().includes("download")) {
      capabilityPacks = `${capabilityPacks}; downloads disabled`;
    }

    setText("ai-control-center-orin-state", "Not implemented; no real AI executing");
    setText("ai-control-center-provider-visible-data", providerState.providerVisibleData || "none");
    setText("ai-control-center-provider-model", providerExecution);
    setText("ai-control-center-prompt-memory", "not accepted, sent, stored, or indexed");
    setText("ai-control-center-capability-packs", capabilityPacks);
    setText("ai-control-center-edition-lanes", "Public no-provider only; Developer and Owner lanes gated");
    setText("ai-control-center-local-result", "waiting for local action");
    setText(
      "ai-control-center-local-detail",
      providerState.providerVisibleDataDetail || "No prompt, file, screen, memory, or telemetry is sent.",
    );
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
})();
