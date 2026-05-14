"""Validate the FAM-007 no-provider/provider-privacy scaffold."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.ai_provider_state import (  # noqa: E402
    NO_PROVIDER_AVAILABILITY,
    NO_PROVIDER_FALLBACK_SELECTION,
    NO_PROVIDER_ID,
    NO_PROVIDER_INTERACTION_AFFORDANCE,
    NO_PROVIDER_MODE,
    NO_PROVIDER_PRIVACY_SCOPE,
    PACKAGE_ID,
    PROVIDER_CONSENT_REQUIRED,
    PROVIDER_SELECTION_AVAILABILITY,
    PROVIDER_SELECTION_MODE,
    PROVIDER_SELECTION_STATE_ID,
    SLC_017_ID,
    SLC_018_ID,
    build_no_provider_ai_state,
    build_provider_selection_consent_state,
)


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def validate() -> list[str]:
    failures: list[str] = []

    snapshot = build_no_provider_ai_state(surface_role="core")
    selection_snapshot = build_provider_selection_consent_state(surface_role="core")
    payload = snapshot.as_renderer_payload()
    selection_payload = selection_snapshot.as_renderer_payload()
    renderer = _read("desktop/desktop_renderer.py")
    core_renderer = _read("desktop/core_visualization_renderer.py")
    html = _read("nexus_visual/orin_core.html")
    desktop_html = _read("nexus_visual/orin_core_desktop.html")
    css = _read("nexus_visual/orin_core.css")
    js = _read("nexus_visual/orin_core.js")
    branch_record = _read("Docs/branch_records/feature_fam_007_provider_boundary_no_provider_shell.md")

    _require(snapshot.package_id == PACKAGE_ID, "snapshot must remain in PKG-007", failures)
    _require(snapshot.slice_ids == (SLC_017_ID, SLC_018_ID), "snapshot must carry SLC-017 and SLC-018", failures)
    _require(snapshot.mode == NO_PROVIDER_MODE, "default mode must be no-provider", failures)
    _require(snapshot.availability == NO_PROVIDER_AVAILABILITY, "default availability must be disabled", failures)
    _require(snapshot.privacy_scope == NO_PROVIDER_PRIVACY_SCOPE, "default privacy scope must be local-only", failures)
    _require(payload["sentToProvider"] is False, "no-provider state must send nothing to providers", failures)
    _require(payload["storedLocally"] is False, "no-provider state must not persist local memory", failures)
    _require(payload["canAcceptPrompts"] is False, "no-provider state must not accept prompts", failures)
    _require(
        payload["interactionAffordance"] == NO_PROVIDER_INTERACTION_AFFORDANCE,
        "no-provider state must expose the disabled interaction affordance",
        failures,
    )
    _require(
        payload["providerVisibleDataLabel"] == "Provider-visible data: none",
        "no-provider state must disclose provider-visible data as none",
        failures,
    )
    _require(payload["externalCalls"] == "blocked", "external calls must be blocked", failures)
    _require(payload["modelState"] == "not installed", "model state must not imply an installed model", failures)
    _require(payload["surfaceRole"] == "core", "desktop Core visualization must own the visible provider rail", failures)
    _require(selection_snapshot.state_id == PROVIDER_SELECTION_STATE_ID, "provider-selection scaffold must use the admitted state id", failures)
    _require(selection_snapshot.mode == PROVIDER_SELECTION_MODE, "provider-selection scaffold must use provider-selection mode", failures)
    _require(
        selection_snapshot.availability == PROVIDER_SELECTION_AVAILABILITY,
        "provider-selection scaffold must be unavailable until configured",
        failures,
    )
    _require(
        selection_payload["selectedProviderId"] == NO_PROVIDER_ID,
        "provider-selection scaffold must default to no-provider fallback",
        failures,
    )
    _require(
        selection_payload["providerSelectionState"] == NO_PROVIDER_FALLBACK_SELECTION,
        "provider-selection scaffold must expose no-provider fallback state",
        failures,
    )
    _require(
        selection_payload["consentState"] == PROVIDER_CONSENT_REQUIRED,
        "provider-selection scaffold must expose consent-required posture",
        failures,
    )
    _require(selection_payload["requiresConsent"] is True, "provider-selection scaffold must require consent", failures)
    _require(selection_payload["sentToProvider"] is False, "provider-selection scaffold must send nothing to providers", failures)
    _require(selection_payload["storedLocally"] is False, "provider-selection scaffold must not persist local memory", failures)
    _require(selection_payload["canAcceptPrompts"] is False, "provider-selection scaffold must not accept prompts", failures)
    _require(selection_payload["externalCalls"] == "blocked", "provider-selection scaffold must block external calls", failures)
    _require(selection_payload["providerVisibleData"] == "none", "provider-selection scaffold must expose no provider-visible data", failures)
    _require(
        selection_payload["providerVisibleDataLabel"] == "Provider-visible data: none",
        "provider-selection scaffold must visibly disclose provider-visible data",
        failures,
    )
    _require(
        selection_payload["interactionAffordance"] == NO_PROVIDER_INTERACTION_AFFORDANCE,
        "provider-selection scaffold must keep the Assisted Desktop interaction disabled",
        failures,
    )
    _require(
        "Consent and provider configuration" in selection_payload["interactionDisabledReason"],
        "provider-selection scaffold must explain the consent/configuration block",
        failures,
    )
    _require(
        len(selection_payload["providerOptions"]) >= 3,
        "provider-selection scaffold must publish visible local/provider option metadata",
        failures,
    )

    for forbidden in ("openai", "anthropic", "ollama", "llama_cpp", "pynvml", "cuda"):
        _require(
            forbidden not in _read("desktop/ai_provider_state.py").casefold(),
            f"no-provider scaffold must not import or name provider/runtime dependency {forbidden}",
            failures,
        )

    for needle in (
        "build_provider_selection_consent_state",
        "_publish_ai_provider_state_to_page",
        "AI_PROVIDER_STATE_READY",
        "window.setAIProviderState",
    ):
        _require(needle in renderer, f"desktop renderer is missing {needle!r}", failures)
        _require(needle in core_renderer, f"Core visualization renderer is missing {needle!r}", failures)

    for label, markup in (
        ("core HTML", html),
        ("desktop Core HTML", desktop_html),
    ):
        for needle in (
            'id="ai-provider-status"',
            'data-mode="no-provider"',
            'data-privacy-scope="local-only"',
            'data-provider-selection="fallback-no-provider"',
            'data-consent-state="required-before-provider"',
            "No AI provider",
            "No-provider fallback active",
            "Consent required before provider setup",
            "Provider-visible data: none",
            'id="ai-provider-status-action"',
            "Assisted Desktop unavailable",
            "Local shell only; nothing is sent",
        ):
            _require(needle in markup, f"{label} is missing {needle!r}", failures)

    for needle in (
        'href="orin_core.css"',
        'src="orin_core.js"',
        'data-surface-role="core-visualization"',
    ):
        _require(needle in desktop_html, f"desktop Core HTML is missing {needle!r}", failures)

    for needle in (
        ".ai-provider-status",
        'data-availability="ready"',
        "overflow-wrap: anywhere",
    ):
        _require(needle in css, f"core CSS is missing {needle!r}", failures)

    for needle in (
        "const aiProviderStatus",
        "renderAIProviderState",
        "window.setAIProviderState",
        "providerSelectionState",
        "requiresConsent",
        "consentState",
        "interactionAffordance",
        "providerVisibleDataLabel",
        "aiProviderStatusAction.disabled = true",
        "sentToProvider",
        "canAcceptPrompts",
    ):
        _require(needle in js, f"core JS is missing {needle!r}", failures)

    for needle in (
        "SLC-017/SLC-018 No-Provider Shell And Provider-Privacy State",
        "SLC-017/SLC-018 Provider Selection And Consent Boundary Scaffold",
        "SLC-017/SLC-018 Assisted Desktop Mode No-Provider Interaction And Consent Surface",
        "model downloads",
        "real provider SDK integration",
        "AI Product Contract v0.6.2",
    ):
        _require(needle in branch_record, f"branch record is missing {needle!r}", failures)

    return failures


def main() -> int:
    failures = validate()
    if failures:
        print(f"FAIL: FAM-007 provider-state validation found {len(failures)} issue(s).")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: FAM-007 provider-state validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
