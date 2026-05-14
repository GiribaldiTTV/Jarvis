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

NO_PROVIDER_MODE = "no-provider"
NO_PROVIDER_AVAILABILITY = "disabled"
NO_PROVIDER_PRIVACY_SCOPE = "local-only"


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
    privacy_scope: str
    privacy_label: str
    provider_visible_data: str
    local_storage: str
    consent_state: str
    prompt_acceptance: str
    external_calls: str
    model_state: str
    capability_pack_state: str
    source_truth: str
    surface_role: str

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
            "privacy_scope": self.privacy_scope,
            "privacy_label": self.privacy_label,
            "provider_visible_data": self.provider_visible_data,
            "local_storage": self.local_storage,
            "consent_state": self.consent_state,
            "prompt_acceptance": self.prompt_acceptance,
            "external_calls": self.external_calls,
            "model_state": self.model_state,
            "capability_pack_state": self.capability_pack_state,
            "source_truth": self.source_truth,
            "surface_role": self.surface_role,
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
            "privacyScope": self.privacy_scope,
            "privacyLabel": self.privacy_label,
            "providerVisibleData": self.provider_visible_data,
            "localStorage": self.local_storage,
            "consentState": self.consent_state,
            "promptAcceptance": self.prompt_acceptance,
            "externalCalls": self.external_calls,
            "modelState": self.model_state,
            "capabilityPackState": self.capability_pack_state,
            "sourceTruth": self.source_truth,
            "surfaceRole": self.surface_role,
            "canAcceptPrompts": False,
            "requiresConsent": False,
            "sentToProvider": False,
            "storedLocally": False,
        }


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
        privacy_scope=NO_PROVIDER_PRIVACY_SCOPE,
        privacy_label="Local shell only; nothing is sent",
        provider_visible_data="none",
        local_storage="none",
        consent_state="not required until a provider is configured",
        prompt_acceptance="disabled",
        external_calls="blocked",
        model_state="not installed",
        capability_pack_state="not installed",
        source_truth="renderer-local no-provider shell",
        surface_role=normalized_surface,
    )
