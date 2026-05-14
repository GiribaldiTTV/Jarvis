"""Provider/no-provider and foundation-readiness state contract for FAM-007.

This module owns local-only FAM-007 scaffolds. It does not load models, call
provider SDKs, persist memory, probe hardware, or infer a configured provider.
"""

from __future__ import annotations

from dataclasses import dataclass


PACKAGE_ID = "PKG-007"
SLC_017_ID = "SLC-017"
SLC_018_ID = "SLC-018"
SLC_031_ID = "SLC-031"
SLC_032_ID = "SLC-032"
SLC_033_ID = "SLC-033"
SLC_034_ID = "SLC-034"
SLC_035_ID = "SLC-035"
SLC_036_ID = "SLC-036"
STATE_ID = "provider-boundary-no-provider-shell"
PROVIDER_SELECTION_STATE_ID = "provider-selection-consent-boundary"
LOCAL_PROVIDER_REGISTRY_STATE_ID = "local-provider-registry-configuration-state"
LOCAL_HARDWARE_CAPABILITY_STATE_ID = "hardware-gpu-cpu-capability-planning"
FAM007_FOUNDATION_READINESS_STATE_ID = "fam007-foundation-readiness-scaffold"

NO_PROVIDER_MODE = "no-provider"
NO_PROVIDER_AVAILABILITY = "disabled"
NO_PROVIDER_PRIVACY_SCOPE = "local-only"
PROVIDER_SELECTION_MODE = "provider-selection"
PROVIDER_SELECTION_AVAILABILITY = "unavailable"
LOCAL_PROVIDER_REGISTRY_MODE = "provider-registry"
LOCAL_PROVIDER_REGISTRY_AVAILABILITY = "unavailable"
LOCAL_HARDWARE_CAPABILITY_MODE = "hardware-capability-planning"
LOCAL_HARDWARE_CAPABILITY_AVAILABILITY = "planning-only"
FAM007_FOUNDATION_READINESS_MODE = "foundation-readiness"
FAM007_FOUNDATION_READINESS_AVAILABILITY = "planning-only"
NO_PROVIDER_ID = "no-provider"
NO_PROVIDER_FALLBACK_SELECTION = "fallback-no-provider"
PROVIDER_CONSENT_REQUIRED = "required-before-provider"
NO_PROVIDER_INTERACTION_AFFORDANCE = "disabled-no-provider-interaction"
PROVIDER_CONFIGURATION_UNCONFIGURED = "unconfigured"
PROVIDER_CONFIGURATION_FALLBACK_ACTIVE = "fallback-active"
LOCAL_PROVIDER_REGISTRY_STATE = "local-only-registry"
LOCAL_HARDWARE_CAPABILITY_STATE = "local-planning-only"
GPU_CAPABILITY_UNPROBED = "gpu-unprobed"
CPU_FALLBACK_PRESERVED = "cpu-fallback-preserved"
POWER_STATE_NOT_EVALUATED = "power-state-not-evaluated"
THERMAL_GUARDRAILS_REQUIRED = "thermal-guardrails-required"
MODEL_WORKLOAD_DISABLED = "model-workload-disabled"
CAPABILITY_RECOMMENDATION_PENDING = "recommendation-pending"
CAPABILITY_PACK_LIFECYCLE_PLANNED = "capability-pack-lifecycle-planned"
CAPABILITY_PACK_DOWNLOADS_BLOCKED = "capability-pack-downloads-blocked"
DATA_CLASSIFICATION_LOCAL_ONLY = "data-classification-local-only"
MEMORY_CONTEXT_DISABLED = "memory-context-disabled"
AUDIT_SECRETS_PLANNED = "audit-secrets-planned"
WINDOWS_RESILIENCE_PLANNED = "windows-resilience-planned"
OFFLINE_DEGRADED_PLANNED = "offline-degraded-planned"
PERSONA_CORE_VOICE_BOUNDARY_PLANNED = "persona-core-voice-boundary-planned"
VOICE_RUNTIME_DISABLED = "voice-runtime-disabled"
VALIDATION_PROOF_GATES_PLANNED = "validation-proof-gates-planned"
ABUSE_EVAL_PENDING = "abuse-eval-pending"
RELEASE_PROOF_PENDING = "release-proof-pending"


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
class AIFoundationReadinessSnapshot:
    slice_id: str
    label: str
    state: str
    visible_status: str
    proof_status: str
    blocked_work: str

    def as_dict(self) -> dict[str, str]:
        return {
            "slice_id": self.slice_id,
            "label": self.label,
            "state": self.state,
            "visible_status": self.visible_status,
            "proof_status": self.proof_status,
            "blocked_work": self.blocked_work,
        }

    def as_renderer_payload(self) -> dict[str, str]:
        return {
            "sliceId": self.slice_id,
            "label": self.label,
            "state": self.state,
            "visibleStatus": self.visible_status,
            "proofStatus": self.proof_status,
            "blockedWork": self.blocked_work,
        }


@dataclass(frozen=True)
class AIProviderStateSnapshot:
    package_id: str
    slice_ids: tuple[str, ...]
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
    hardware_capability_state: str
    hardware_capability_label: str
    gpu_capability_state: str
    gpu_capability_label: str
    cpu_fallback_state: str
    cpu_fallback_label: str
    power_state: str
    power_state_label: str
    thermal_guardrail_state: str
    thermal_guardrail_label: str
    model_workload_state: str
    model_workload_label: str
    capability_recommendation_state: str
    capability_recommendation_label: str
    capability_pack_lifecycle_state: str
    capability_pack_lifecycle_label: str
    capability_pack_download_state: str
    capability_pack_download_label: str
    data_classification_state: str
    data_classification_label: str
    memory_context_state: str
    memory_context_label: str
    audit_secrets_state: str
    audit_secrets_label: str
    windows_resilience_state: str
    windows_resilience_label: str
    offline_degraded_state: str
    offline_degraded_label: str
    persona_core_voice_state: str
    persona_core_voice_label: str
    voice_runtime_state: str
    voice_runtime_label: str
    validation_proof_gate_state: str
    validation_proof_gate_label: str
    abuse_eval_state: str
    abuse_eval_label: str
    release_proof_gate_state: str
    release_proof_gate_label: str
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
    foundation_readiness_items: tuple[AIFoundationReadinessSnapshot, ...]

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
            "hardware_capability_state": self.hardware_capability_state,
            "hardware_capability_label": self.hardware_capability_label,
            "gpu_capability_state": self.gpu_capability_state,
            "gpu_capability_label": self.gpu_capability_label,
            "cpu_fallback_state": self.cpu_fallback_state,
            "cpu_fallback_label": self.cpu_fallback_label,
            "power_state": self.power_state,
            "power_state_label": self.power_state_label,
            "thermal_guardrail_state": self.thermal_guardrail_state,
            "thermal_guardrail_label": self.thermal_guardrail_label,
            "model_workload_state": self.model_workload_state,
            "model_workload_label": self.model_workload_label,
            "capability_recommendation_state": self.capability_recommendation_state,
            "capability_recommendation_label": self.capability_recommendation_label,
            "capability_pack_lifecycle_state": self.capability_pack_lifecycle_state,
            "capability_pack_lifecycle_label": self.capability_pack_lifecycle_label,
            "capability_pack_download_state": self.capability_pack_download_state,
            "capability_pack_download_label": self.capability_pack_download_label,
            "data_classification_state": self.data_classification_state,
            "data_classification_label": self.data_classification_label,
            "memory_context_state": self.memory_context_state,
            "memory_context_label": self.memory_context_label,
            "audit_secrets_state": self.audit_secrets_state,
            "audit_secrets_label": self.audit_secrets_label,
            "windows_resilience_state": self.windows_resilience_state,
            "windows_resilience_label": self.windows_resilience_label,
            "offline_degraded_state": self.offline_degraded_state,
            "offline_degraded_label": self.offline_degraded_label,
            "persona_core_voice_state": self.persona_core_voice_state,
            "persona_core_voice_label": self.persona_core_voice_label,
            "voice_runtime_state": self.voice_runtime_state,
            "voice_runtime_label": self.voice_runtime_label,
            "validation_proof_gate_state": self.validation_proof_gate_state,
            "validation_proof_gate_label": self.validation_proof_gate_label,
            "abuse_eval_state": self.abuse_eval_state,
            "abuse_eval_label": self.abuse_eval_label,
            "release_proof_gate_state": self.release_proof_gate_state,
            "release_proof_gate_label": self.release_proof_gate_label,
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
            "foundation_readiness_items": tuple(item.as_dict() for item in self.foundation_readiness_items),
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
            "hardwareCapabilityState": self.hardware_capability_state,
            "hardwareCapabilityLabel": self.hardware_capability_label,
            "gpuCapabilityState": self.gpu_capability_state,
            "gpuCapabilityLabel": self.gpu_capability_label,
            "cpuFallbackState": self.cpu_fallback_state,
            "cpuFallbackLabel": self.cpu_fallback_label,
            "powerState": self.power_state,
            "powerStateLabel": self.power_state_label,
            "thermalGuardrailState": self.thermal_guardrail_state,
            "thermalGuardrailLabel": self.thermal_guardrail_label,
            "modelWorkloadState": self.model_workload_state,
            "modelWorkloadLabel": self.model_workload_label,
            "capabilityRecommendationState": self.capability_recommendation_state,
            "capabilityRecommendationLabel": self.capability_recommendation_label,
            "capabilityPackLifecycleState": self.capability_pack_lifecycle_state,
            "capabilityPackLifecycleLabel": self.capability_pack_lifecycle_label,
            "capabilityPackDownloadState": self.capability_pack_download_state,
            "capabilityPackDownloadLabel": self.capability_pack_download_label,
            "dataClassificationState": self.data_classification_state,
            "dataClassificationLabel": self.data_classification_label,
            "memoryContextState": self.memory_context_state,
            "memoryContextLabel": self.memory_context_label,
            "auditSecretsState": self.audit_secrets_state,
            "auditSecretsLabel": self.audit_secrets_label,
            "windowsResilienceState": self.windows_resilience_state,
            "windowsResilienceLabel": self.windows_resilience_label,
            "offlineDegradedState": self.offline_degraded_state,
            "offlineDegradedLabel": self.offline_degraded_label,
            "personaCoreVoiceState": self.persona_core_voice_state,
            "personaCoreVoiceLabel": self.persona_core_voice_label,
            "voiceRuntimeState": self.voice_runtime_state,
            "voiceRuntimeLabel": self.voice_runtime_label,
            "validationProofGateState": self.validation_proof_gate_state,
            "validationProofGateLabel": self.validation_proof_gate_label,
            "abuseEvalState": self.abuse_eval_state,
            "abuseEvalLabel": self.abuse_eval_label,
            "releaseProofGateState": self.release_proof_gate_state,
            "releaseProofGateLabel": self.release_proof_gate_label,
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
            "foundationReadiness": [item.as_renderer_payload() for item in self.foundation_readiness_items],
            "canAcceptPrompts": False,
            "requiresConsent": self.consent_state == PROVIDER_CONSENT_REQUIRED,
            "sentToProvider": False,
            "storedLocally": False,
        }


def _foundation_readiness_items() -> tuple[AIFoundationReadinessSnapshot, ...]:
    return (
        AIFoundationReadinessSnapshot(
            slice_id=SLC_017_ID,
            label="No-provider shell",
            state="green",
            visible_status="Disabled Assisted Desktop affordance and no-provider fallback are visible",
            proof_status="static-validation-green",
            blocked_work="provider calls",
        ),
        AIFoundationReadinessSnapshot(
            slice_id=SLC_018_ID,
            label="Provider/privacy boundary",
            state="green",
            visible_status="Consent-required provider state and provider-visible-data none are visible",
            proof_status="static-validation-green",
            blocked_work="provider SDK integration",
        ),
        AIFoundationReadinessSnapshot(
            slice_id=SLC_031_ID,
            label="Hardware capability planning",
            state=LOCAL_HARDWARE_CAPABILITY_STATE,
            visible_status="GPU capability is unprobed and CPU fallback is preserved",
            proof_status="planning-validation-green",
            blocked_work="hardware probing and model workload execution",
        ),
        AIFoundationReadinessSnapshot(
            slice_id=SLC_032_ID,
            label="Capability-pack lifecycle",
            state=CAPABILITY_PACK_LIFECYCLE_PLANNED,
            visible_status="Capability packs are not installed and downloads are blocked",
            proof_status="planning-validation-green",
            blocked_work="pack downloads and install/update/uninstall execution",
        ),
        AIFoundationReadinessSnapshot(
            slice_id=SLC_033_ID,
            label="Data, memory, context, audit, and secrets",
            state=MEMORY_CONTEXT_DISABLED,
            visible_status="Memory and context retention are disabled; no secrets are stored",
            proof_status="planning-validation-green",
            blocked_work="memory indexing and persistent context",
        ),
        AIFoundationReadinessSnapshot(
            slice_id=SLC_034_ID,
            label="Windows resilience and platform posture",
            state=WINDOWS_RESILIENCE_PLANNED,
            visible_status="Offline/degraded posture is planned; shortcuts and installers are untouched",
            proof_status="planning-validation-green",
            blocked_work="shortcut, installer, startup, and process-owner changes",
        ),
        AIFoundationReadinessSnapshot(
            slice_id=SLC_035_ID,
            label="Persona, Core, and voice boundary",
            state=PERSONA_CORE_VOICE_BOUNDARY_PLANNED,
            visible_status="ORIN/Core presence stays visual-only and voice runtime is disabled",
            proof_status="planning-validation-green",
            blocked_work="voice runtime and persona/Core sync",
        ),
        AIFoundationReadinessSnapshot(
            slice_id=SLC_036_ID,
            label="Validation, eval, abuse, and release proof gates",
            state=VALIDATION_PROOF_GATES_PLANNED,
            visible_status="Static proof gates are active; abuse/eval and release proof remain gated",
            proof_status="validation-green",
            blocked_work="release execution, artifacts, and live provider eval",
        ),
    )


def _foundation_readiness_fields() -> dict[str, object]:
    return {
        "capability_pack_lifecycle_state": CAPABILITY_PACK_LIFECYCLE_PLANNED,
        "capability_pack_lifecycle_label": "Capability packs: lifecycle planned",
        "capability_pack_download_state": CAPABILITY_PACK_DOWNLOADS_BLOCKED,
        "capability_pack_download_label": "Capability pack downloads: blocked",
        "data_classification_state": DATA_CLASSIFICATION_LOCAL_ONLY,
        "data_classification_label": "Data classification: local-only planning",
        "memory_context_state": MEMORY_CONTEXT_DISABLED,
        "memory_context_label": "Memory/context: disabled; no indexing",
        "audit_secrets_state": AUDIT_SECRETS_PLANNED,
        "audit_secrets_label": "Audit/secrets: planned; no secrets stored",
        "windows_resilience_state": WINDOWS_RESILIENCE_PLANNED,
        "windows_resilience_label": "Windows resilience: planning only",
        "offline_degraded_state": OFFLINE_DEGRADED_PLANNED,
        "offline_degraded_label": "Offline/degraded mode: planned",
        "persona_core_voice_state": PERSONA_CORE_VOICE_BOUNDARY_PLANNED,
        "persona_core_voice_label": "Persona/Core/voice: planning boundary",
        "voice_runtime_state": VOICE_RUNTIME_DISABLED,
        "voice_runtime_label": "Voice runtime: disabled",
        "validation_proof_gate_state": VALIDATION_PROOF_GATES_PLANNED,
        "validation_proof_gate_label": "Validation gates: static proof active",
        "abuse_eval_state": ABUSE_EVAL_PENDING,
        "abuse_eval_label": "Abuse/eval: pending future approval",
        "release_proof_gate_state": RELEASE_PROOF_PENDING,
        "release_proof_gate_label": "Release proof: pending future approval",
        "foundation_readiness_items": _foundation_readiness_items(),
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
        hardware_capability_state=LOCAL_HARDWARE_CAPABILITY_STATE,
        hardware_capability_label="Hardware capability: planning only",
        gpu_capability_state=GPU_CAPABILITY_UNPROBED,
        gpu_capability_label="GPU acceleration: not evaluated",
        cpu_fallback_state=CPU_FALLBACK_PRESERVED,
        cpu_fallback_label="CPU fallback: preserved",
        power_state=POWER_STATE_NOT_EVALUATED,
        power_state_label="Power state: not evaluated",
        thermal_guardrail_state=THERMAL_GUARDRAILS_REQUIRED,
        thermal_guardrail_label="Thermal guardrails required before model workloads",
        model_workload_state=MODEL_WORKLOAD_DISABLED,
        model_workload_label="Model workloads: disabled",
        capability_recommendation_state=CAPABILITY_RECOMMENDATION_PENDING,
        capability_recommendation_label="Capability recommendation pending",
        **_foundation_readiness_fields(),
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
        hardware_capability_state=LOCAL_HARDWARE_CAPABILITY_STATE,
        hardware_capability_label="Hardware capability: planning only",
        gpu_capability_state=GPU_CAPABILITY_UNPROBED,
        gpu_capability_label="GPU acceleration: not evaluated",
        cpu_fallback_state=CPU_FALLBACK_PRESERVED,
        cpu_fallback_label="CPU fallback: preserved",
        power_state=POWER_STATE_NOT_EVALUATED,
        power_state_label="Power state: not evaluated",
        thermal_guardrail_state=THERMAL_GUARDRAILS_REQUIRED,
        thermal_guardrail_label="Thermal guardrails required before model workloads",
        model_workload_state=MODEL_WORKLOAD_DISABLED,
        model_workload_label="Model workloads: disabled",
        capability_recommendation_state=CAPABILITY_RECOMMENDATION_PENDING,
        capability_recommendation_label="Capability recommendation pending",
        **_foundation_readiness_fields(),
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
        hardware_capability_state=LOCAL_HARDWARE_CAPABILITY_STATE,
        hardware_capability_label="Hardware capability: planning only",
        gpu_capability_state=GPU_CAPABILITY_UNPROBED,
        gpu_capability_label="GPU acceleration: not evaluated",
        cpu_fallback_state=CPU_FALLBACK_PRESERVED,
        cpu_fallback_label="CPU fallback: preserved",
        power_state=POWER_STATE_NOT_EVALUATED,
        power_state_label="Power state: not evaluated",
        thermal_guardrail_state=THERMAL_GUARDRAILS_REQUIRED,
        thermal_guardrail_label="Thermal guardrails required before model workloads",
        model_workload_state=MODEL_WORKLOAD_DISABLED,
        model_workload_label="Model workloads: disabled",
        capability_recommendation_state=CAPABILITY_RECOMMENDATION_PENDING,
        capability_recommendation_label="Capability recommendation pending",
        **_foundation_readiness_fields(),
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


def build_local_hardware_capability_state(*, surface_role: str = "hud") -> AIProviderStateSnapshot:
    """Build the local-only hardware/capability planning scaffold.

    This records visible planning posture only. It does not probe hardware,
    choose acceleration, run model workloads, or make provider calls.
    """

    normalized_surface = surface_role if surface_role in {"core", "hud", "combined"} else "hud"
    return AIProviderStateSnapshot(
        package_id=PACKAGE_ID,
        slice_ids=(SLC_017_ID, SLC_018_ID, SLC_031_ID),
        state_id=LOCAL_HARDWARE_CAPABILITY_STATE_ID,
        mode=LOCAL_HARDWARE_CAPABILITY_MODE,
        availability=LOCAL_HARDWARE_CAPABILITY_AVAILABILITY,
        provider_label="No provider configured",
        provider_kind="local-hardware-planning-scaffold",
        status_label="Hardware capability planning",
        disabled_reason="Hardware capability planning is local-only and model workloads are disabled",
        selected_provider_id=NO_PROVIDER_ID,
        provider_selection_state=NO_PROVIDER_FALLBACK_SELECTION,
        provider_selection_label="No-provider fallback active",
        provider_configuration_state=PROVIDER_CONFIGURATION_UNCONFIGURED,
        provider_configuration_label="Provider configuration: none",
        provider_registry_state=LOCAL_PROVIDER_REGISTRY_STATE,
        provider_registry_label="Local provider registry: no configured providers",
        configured_provider_count=0,
        available_provider_count=0,
        hardware_capability_state=LOCAL_HARDWARE_CAPABILITY_STATE,
        hardware_capability_label="Hardware capability: local planning only",
        gpu_capability_state=GPU_CAPABILITY_UNPROBED,
        gpu_capability_label="GPU acceleration: unprobed; no model workload active",
        cpu_fallback_state=CPU_FALLBACK_PRESERVED,
        cpu_fallback_label="CPU fallback: preserved",
        power_state=POWER_STATE_NOT_EVALUATED,
        power_state_label="Power state: not evaluated",
        thermal_guardrail_state=THERMAL_GUARDRAILS_REQUIRED,
        thermal_guardrail_label="Thermal guardrails required before model workloads",
        model_workload_state=MODEL_WORKLOAD_DISABLED,
        model_workload_label="Model workloads: disabled",
        capability_recommendation_state=CAPABILITY_RECOMMENDATION_PENDING,
        capability_recommendation_label="Capability recommendation pending hardware proof",
        **_foundation_readiness_fields(),
        privacy_scope=NO_PROVIDER_PRIVACY_SCOPE,
        privacy_label="Local capability planning only; nothing is sent",
        provider_visible_data="none",
        provider_visible_data_label="Provider-visible data: none",
        local_storage="none",
        consent_state=PROVIDER_CONSENT_REQUIRED,
        consent_label="Consent required before provider or capability setup",
        interaction_affordance=NO_PROVIDER_INTERACTION_AFFORDANCE,
        interaction_label="Hardware capability planning only",
        interaction_disabled_reason="Hardware proof and consent are required before model workloads can run",
        no_provider_fallback_label="No-provider fallback active",
        prompt_acceptance="disabled",
        external_calls="blocked",
        model_state="not installed",
        capability_pack_state="not installed",
        source_truth="renderer-local hardware capability planning scaffold",
        surface_role=normalized_surface,
        provider_options=_provider_selection_options(),
    )


def build_fam007_foundation_readiness_state(*, surface_role: str = "hud") -> AIProviderStateSnapshot:
    """Build the local-only all-slice FAM-007 Workstream readiness scaffold."""

    normalized_surface = surface_role if surface_role in {"core", "hud", "combined"} else "hud"
    return AIProviderStateSnapshot(
        package_id=PACKAGE_ID,
        slice_ids=(
            SLC_017_ID,
            SLC_018_ID,
            SLC_031_ID,
            SLC_032_ID,
            SLC_033_ID,
            SLC_034_ID,
            SLC_035_ID,
            SLC_036_ID,
        ),
        state_id=FAM007_FOUNDATION_READINESS_STATE_ID,
        mode=FAM007_FOUNDATION_READINESS_MODE,
        availability=FAM007_FOUNDATION_READINESS_AVAILABILITY,
        provider_label="No provider configured",
        provider_kind="local-foundation-readiness-scaffold",
        status_label="FAM-007 foundation readiness",
        disabled_reason="All admitted FAM-007 branch-material seams are local-only and provider execution is disabled",
        selected_provider_id=NO_PROVIDER_ID,
        provider_selection_state=NO_PROVIDER_FALLBACK_SELECTION,
        provider_selection_label="No-provider fallback active",
        provider_configuration_state=PROVIDER_CONFIGURATION_UNCONFIGURED,
        provider_configuration_label="Provider configuration: none",
        provider_registry_state=LOCAL_PROVIDER_REGISTRY_STATE,
        provider_registry_label="Local provider registry: no configured providers",
        configured_provider_count=0,
        available_provider_count=0,
        hardware_capability_state=LOCAL_HARDWARE_CAPABILITY_STATE,
        hardware_capability_label="Hardware capability: local planning only",
        gpu_capability_state=GPU_CAPABILITY_UNPROBED,
        gpu_capability_label="GPU acceleration: unprobed; no model workload active",
        cpu_fallback_state=CPU_FALLBACK_PRESERVED,
        cpu_fallback_label="CPU fallback: preserved",
        power_state=POWER_STATE_NOT_EVALUATED,
        power_state_label="Power state: not evaluated",
        thermal_guardrail_state=THERMAL_GUARDRAILS_REQUIRED,
        thermal_guardrail_label="Thermal guardrails required before model workloads",
        model_workload_state=MODEL_WORKLOAD_DISABLED,
        model_workload_label="Model workloads: disabled",
        capability_recommendation_state=CAPABILITY_RECOMMENDATION_PENDING,
        capability_recommendation_label="Capability recommendation pending hardware proof",
        **_foundation_readiness_fields(),
        privacy_scope=NO_PROVIDER_PRIVACY_SCOPE,
        privacy_label="Local foundation planning only; nothing is sent",
        provider_visible_data="none",
        provider_visible_data_label="Provider-visible data: none",
        local_storage="none",
        consent_state=PROVIDER_CONSENT_REQUIRED,
        consent_label="Consent required before provider or capability setup",
        interaction_affordance=NO_PROVIDER_INTERACTION_AFFORDANCE,
        interaction_label="FAM-007 foundation readiness only",
        interaction_disabled_reason="Provider consent, capability proof, and future USER approval are required before AI prompts can run",
        no_provider_fallback_label="No-provider fallback active",
        prompt_acceptance="disabled",
        external_calls="blocked",
        model_state="not installed",
        capability_pack_state="not installed",
        source_truth="renderer-local FAM-007 foundation readiness scaffold",
        surface_role=normalized_surface,
        provider_options=_provider_selection_options(),
    )
