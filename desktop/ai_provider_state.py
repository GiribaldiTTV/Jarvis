"""Provider/no-provider state contract for FAM-007.

This module owns the first SLC-017/SLC-018 scaffold: a truthful local
no-provider state. It does not load models, call provider SDKs, persist memory,
or infer a configured provider.
"""

from __future__ import annotations

from dataclasses import dataclass


PACKAGE_ID = "PKG-007"
SLC_017_ID = "SLC-017"
SLC_018_ID = "SLC-018"
STATE_ID = "provider-boundary-no-provider-shell"
PROVIDER_SELECTION_STATE_ID = "provider-selection-consent-boundary"
LOCAL_PROVIDER_REGISTRY_STATE_ID = "local-provider-registry-configuration-state"

NO_PROVIDER_MODE = "no-provider"
NO_PROVIDER_AVAILABILITY = "disabled"
NO_PROVIDER_PRIVACY_SCOPE = "local-only"
PROVIDER_SELECTION_MODE = "provider-selection"
PROVIDER_SELECTION_AVAILABILITY = "unavailable"
LOCAL_PROVIDER_REGISTRY_MODE = "provider-registry"
LOCAL_PROVIDER_REGISTRY_AVAILABILITY = "unavailable"
NO_PROVIDER_ID = "no-provider"
NO_PROVIDER_FALLBACK_SELECTION = "fallback-no-provider"
PROVIDER_CONSENT_REQUIRED = "required-before-provider"
NO_PROVIDER_INTERACTION_AFFORDANCE = "disabled-no-provider-interaction"
PROVIDER_CONFIGURATION_UNCONFIGURED = "unconfigured"
PROVIDER_CONFIGURATION_FALLBACK_ACTIVE = "fallback-active"
LOCAL_PROVIDER_REGISTRY_STATE = "local-only-registry"


@dataclass(frozen=True)
class AIProviderChoiceSnapshot:
    provider_id: str
    label: str
    provider_kind: str
    availability: str
    consent_state: str
    privacy_scope: str
    visible_status: str
    configuration_state: str
    configured: bool
    requires_consent: bool
    provider_visible_data: str
    external_calls: str

    def as_dict(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "label": self.label,
            "provider_kind": self.provider_kind,
            "availability": self.availability,
            "consent_state": self.consent_state,
            "privacy_scope": self.privacy_scope,
            "visible_status": self.visible_status,
            "configuration_state": self.configuration_state,
            "configured": self.configured,
            "requires_consent": self.requires_consent,
            "provider_visible_data": self.provider_visible_data,
            "external_calls": self.external_calls,
        }

    def as_renderer_payload(self) -> dict[str, object]:
        return {
            "providerId": self.provider_id,
            "label": self.label,
            "providerKind": self.provider_kind,
            "availability": self.availability,
            "consentState": self.consent_state,
            "privacyScope": self.privacy_scope,
            "visibleStatus": self.visible_status,
            "configurationState": self.configuration_state,
            "configured": self.configured,
            "requiresConsent": self.requires_consent,
            "providerVisibleData": self.provider_visible_data,
            "externalCalls": self.external_calls,
        }


@dataclass(frozen=True)
class AIProviderStateSnapshot:
    package_id: str
    slice_ids: tuple[str, str]
    state_id: str
    mode: str
    availability: str
    provider_label: str
    provider_kind: str
    status_label: str
    disabled_reason: str
    selected_provider_id: str
    provider_selection_state: str
    provider_selection_label: str
    provider_configuration_state: str
    provider_configuration_label: str
    provider_registry_state: str
    provider_registry_label: str
    configured_provider_count: int
    available_provider_count: int
    privacy_scope: str
    privacy_label: str
    provider_visible_data: str
    provider_visible_data_label: str
    local_storage: str
    consent_state: str
    consent_label: str
    interaction_affordance: str
    interaction_label: str
    interaction_disabled_reason: str
    no_provider_fallback_label: str
    prompt_acceptance: str
    external_calls: str
    model_state: str
    capability_pack_state: str
    source_truth: str
    surface_role: str
    provider_options: tuple[AIProviderChoiceSnapshot, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "package_id": self.package_id,
            "slice_ids": self.slice_ids,
            "state_id": self.state_id,
            "mode": self.mode,
            "availability": self.availability,
            "provider_label": self.provider_label,
            "provider_kind": self.provider_kind,
            "status_label": self.status_label,
            "disabled_reason": self.disabled_reason,
            "selected_provider_id": self.selected_provider_id,
            "provider_selection_state": self.provider_selection_state,
            "provider_selection_label": self.provider_selection_label,
            "provider_configuration_state": self.provider_configuration_state,
            "provider_configuration_label": self.provider_configuration_label,
            "provider_registry_state": self.provider_registry_state,
            "provider_registry_label": self.provider_registry_label,
            "configured_provider_count": self.configured_provider_count,
            "available_provider_count": self.available_provider_count,
            "privacy_scope": self.privacy_scope,
            "privacy_label": self.privacy_label,
            "provider_visible_data": self.provider_visible_data,
            "provider_visible_data_label": self.provider_visible_data_label,
            "local_storage": self.local_storage,
            "consent_state": self.consent_state,
            "consent_label": self.consent_label,
            "interaction_affordance": self.interaction_affordance,
            "interaction_label": self.interaction_label,
            "interaction_disabled_reason": self.interaction_disabled_reason,
            "no_provider_fallback_label": self.no_provider_fallback_label,
            "prompt_acceptance": self.prompt_acceptance,
            "external_calls": self.external_calls,
            "model_state": self.model_state,
            "capability_pack_state": self.capability_pack_state,
            "source_truth": self.source_truth,
            "surface_role": self.surface_role,
            "provider_options": tuple(option.as_dict() for option in self.provider_options),
        }

    def as_renderer_payload(self) -> dict[str, object]:
        return {
            "packageId": self.package_id,
            "sliceIds": list(self.slice_ids),
            "stateId": self.state_id,
            "mode": self.mode,
            "availability": self.availability,
            "providerLabel": self.provider_label,
            "providerKind": self.provider_kind,
            "statusLabel": self.status_label,
            "disabledReason": self.disabled_reason,
            "selectedProviderId": self.selected_provider_id,
            "providerSelectionState": self.provider_selection_state,
            "providerSelectionLabel": self.provider_selection_label,
            "providerConfigurationState": self.provider_configuration_state,
            "providerConfigurationLabel": self.provider_configuration_label,
            "providerRegistryState": self.provider_registry_state,
            "providerRegistryLabel": self.provider_registry_label,
            "configuredProviderCount": self.configured_provider_count,
            "availableProviderCount": self.available_provider_count,
            "privacyScope": self.privacy_scope,
            "privacyLabel": self.privacy_label,
            "providerVisibleData": self.provider_visible_data,
            "providerVisibleDataLabel": self.provider_visible_data_label,
            "localStorage": self.local_storage,
            "consentState": self.consent_state,
            "consentLabel": self.consent_label,
            "interactionAffordance": self.interaction_affordance,
            "interactionLabel": self.interaction_label,
            "interactionDisabledReason": self.interaction_disabled_reason,
            "noProviderFallbackLabel": self.no_provider_fallback_label,
            "promptAcceptance": self.prompt_acceptance,
            "externalCalls": self.external_calls,
            "modelState": self.model_state,
            "capabilityPackState": self.capability_pack_state,
            "sourceTruth": self.source_truth,
            "surfaceRole": self.surface_role,
            "providerOptions": [option.as_renderer_payload() for option in self.provider_options],
            "providerRegistry": [option.as_renderer_payload() for option in self.provider_options],
            "canAcceptPrompts": False,
            "requiresConsent": self.consent_state == PROVIDER_CONSENT_REQUIRED,
            "sentToProvider": False,
            "storedLocally": False,
        }


def _provider_selection_options() -> tuple[AIProviderChoiceSnapshot, ...]:
    return (
        AIProviderChoiceSnapshot(
            provider_id=NO_PROVIDER_ID,
            label="No provider fallback",
            provider_kind="none",
            availability="disabled",
            consent_state="not-required",
            privacy_scope=NO_PROVIDER_PRIVACY_SCOPE,
            visible_status="Active fallback",
            configuration_state=PROVIDER_CONFIGURATION_FALLBACK_ACTIVE,
            configured=False,
            requires_consent=False,
            provider_visible_data="none",
            external_calls="blocked",
        ),
        AIProviderChoiceSnapshot(
            provider_id="local-capability-pack",
            label="Local capability pack",
            provider_kind="local",
            availability=PROVIDER_SELECTION_AVAILABILITY,
            consent_state=PROVIDER_CONSENT_REQUIRED,
            privacy_scope=NO_PROVIDER_PRIVACY_SCOPE,
            visible_status="Unavailable until installed and approved",
            configuration_state=PROVIDER_CONFIGURATION_UNCONFIGURED,
            configured=False,
            requires_consent=True,
            provider_visible_data="none",
            external_calls="blocked",
        ),
        AIProviderChoiceSnapshot(
            provider_id="external-provider",
            label="External provider",
            provider_kind="external",
            availability=PROVIDER_SELECTION_AVAILABILITY,
            consent_state=PROVIDER_CONSENT_REQUIRED,
            privacy_scope="external-disabled",
            visible_status="Unavailable until configured and approved",
            configuration_state=PROVIDER_CONFIGURATION_UNCONFIGURED,
            configured=False,
            requires_consent=True,
            provider_visible_data="none",
            external_calls="blocked",
        ),
    )


def build_no_provider_ai_state(*, surface_role: str = "hud") -> AIProviderStateSnapshot:
    """Build the local-only no-provider state used before any provider is admitted."""

    normalized_surface = surface_role if surface_role in {"core", "hud", "combined"} else "hud"
    return AIProviderStateSnapshot(
        package_id=PACKAGE_ID,
        slice_ids=(SLC_017_ID, SLC_018_ID),
        state_id=STATE_ID,
        mode=NO_PROVIDER_MODE,
        availability=NO_PROVIDER_AVAILABILITY,
        provider_label="No AI provider",
        provider_kind="none",
        status_label="AI unavailable",
        disabled_reason="No local or remote provider is configured",
        selected_provider_id=NO_PROVIDER_ID,
        provider_selection_state=NO_PROVIDER_FALLBACK_SELECTION,
        provider_selection_label="No provider selected",
        provider_configuration_state=PROVIDER_CONFIGURATION_FALLBACK_ACTIVE,
        provider_configuration_label="No provider configured",
        provider_registry_state=LOCAL_PROVIDER_REGISTRY_STATE,
        provider_registry_label="Local provider registry: no configured providers",
        configured_provider_count=0,
        available_provider_count=0,
        privacy_scope=NO_PROVIDER_PRIVACY_SCOPE,
        privacy_label="Local shell only; nothing is sent",
        provider_visible_data="none",
        provider_visible_data_label="Provider-visible data: none",
        local_storage="none",
        consent_state="not required until a provider is configured",
        consent_label="No provider consent requested",
        interaction_affordance=NO_PROVIDER_INTERACTION_AFFORDANCE,
        interaction_label="Assisted Desktop unavailable",
        interaction_disabled_reason="Choose and approve a provider before AI prompts can run",
        no_provider_fallback_label="No-provider fallback active",
        prompt_acceptance="disabled",
        external_calls="blocked",
        model_state="not installed",
        capability_pack_state="not installed",
        source_truth="renderer-local no-provider shell",
        surface_role=normalized_surface,
        provider_options=_provider_selection_options(),
    )


def build_provider_selection_consent_state(
    *,
    selected_provider_id: str = NO_PROVIDER_ID,
    surface_role: str = "hud",
) -> AIProviderStateSnapshot:
    """Build the local-only provider-selection scaffold with no-provider fallback."""

    normalized_surface = surface_role if surface_role in {"core", "hud", "combined"} else "hud"
    valid_provider_ids = {option.provider_id for option in _provider_selection_options()}
    requested_provider_id = selected_provider_id if selected_provider_id in valid_provider_ids else NO_PROVIDER_ID
    normalized_provider_id = NO_PROVIDER_ID if requested_provider_id != NO_PROVIDER_ID else requested_provider_id

    return AIProviderStateSnapshot(
        package_id=PACKAGE_ID,
        slice_ids=(SLC_017_ID, SLC_018_ID),
        state_id=PROVIDER_SELECTION_STATE_ID,
        mode=PROVIDER_SELECTION_MODE,
        availability=PROVIDER_SELECTION_AVAILABILITY,
        provider_label="No provider selected",
        provider_kind="selection-scaffold",
        status_label="Provider consent required",
        disabled_reason="Provider selection requires explicit consent and configuration",
        selected_provider_id=normalized_provider_id,
        provider_selection_state=NO_PROVIDER_FALLBACK_SELECTION,
        provider_selection_label="No-provider fallback active",
        provider_configuration_state=PROVIDER_CONFIGURATION_UNCONFIGURED,
        provider_configuration_label="No provider configured",
        provider_registry_state=LOCAL_PROVIDER_REGISTRY_STATE,
        provider_registry_label="Local provider registry: no configured providers",
        configured_provider_count=0,
        available_provider_count=0,
        privacy_scope=NO_PROVIDER_PRIVACY_SCOPE,
        privacy_label="Local selection only; nothing is sent",
        provider_visible_data="none",
        provider_visible_data_label="Provider-visible data: none",
        local_storage="none",
        consent_state=PROVIDER_CONSENT_REQUIRED,
        consent_label="Consent required before a provider can be configured",
        interaction_affordance=NO_PROVIDER_INTERACTION_AFFORDANCE,
        interaction_label="Assisted Desktop setup paused",
        interaction_disabled_reason="Consent and provider configuration are required before prompts can run",
        no_provider_fallback_label="No-provider fallback active",
        prompt_acceptance="disabled",
        external_calls="blocked",
        model_state="not installed",
        capability_pack_state="not installed",
        source_truth="renderer-local provider-selection consent scaffold",
        surface_role=normalized_surface,
        provider_options=_provider_selection_options(),
    )


def build_local_provider_registry_state(*, surface_role: str = "hud") -> AIProviderStateSnapshot:
    """Build the local-only provider registry/configuration scaffold."""

    normalized_surface = surface_role if surface_role in {"core", "hud", "combined"} else "hud"
    return AIProviderStateSnapshot(
        package_id=PACKAGE_ID,
        slice_ids=(SLC_017_ID, SLC_018_ID),
        state_id=LOCAL_PROVIDER_REGISTRY_STATE_ID,
        mode=LOCAL_PROVIDER_REGISTRY_MODE,
        availability=LOCAL_PROVIDER_REGISTRY_AVAILABILITY,
        provider_label="No provider configured",
        provider_kind="local-registry-scaffold",
        status_label="Provider setup unavailable",
        disabled_reason="Provider registry is local-only and no AI provider is configured",
        selected_provider_id=NO_PROVIDER_ID,
        provider_selection_state=NO_PROVIDER_FALLBACK_SELECTION,
        provider_selection_label="No-provider fallback active",
        provider_configuration_state=PROVIDER_CONFIGURATION_UNCONFIGURED,
        provider_configuration_label="Provider configuration: none",
        provider_registry_state=LOCAL_PROVIDER_REGISTRY_STATE,
        provider_registry_label="Local provider registry: no configured providers",
        configured_provider_count=0,
        available_provider_count=0,
        privacy_scope=NO_PROVIDER_PRIVACY_SCOPE,
        privacy_label="Local registry only; nothing is sent",
        provider_visible_data="none",
        provider_visible_data_label="Provider-visible data: none",
        local_storage="none",
        consent_state=PROVIDER_CONSENT_REQUIRED,
        consent_label="Consent required before provider configuration",
        interaction_affordance=NO_PROVIDER_INTERACTION_AFFORDANCE,
        interaction_label="Provider setup paused",
        interaction_disabled_reason="Provider configuration is local-only and requires consent before prompts can run",
        no_provider_fallback_label="No-provider fallback active",
        prompt_acceptance="disabled",
        external_calls="blocked",
        model_state="not installed",
        capability_pack_state="not installed",
        source_truth="renderer-local provider registry configuration scaffold",
        surface_role=normalized_surface,
        provider_options=_provider_selection_options(),
    )
