"""Provider/no-provider and foundation-readiness state contract for FAM-007.

This module owns local-only FAM-007 scaffolds. It does not load models, call
provider SDKs, persist memory, probe hardware, or infer a configured provider.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


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
LOCAL_AI_RUNTIME_FOUNDATION_STATE_ID = "local-ai-runtime-foundation-provider-boundary"

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
LOCAL_AI_RUNTIME_FOUNDATION_MODE = "runtime-foundation-provider-boundary"
LOCAL_AI_RUNTIME_FOUNDATION_AVAILABILITY = "disabled"
NO_PROVIDER_ID = "no-provider"
NO_PROVIDER_FALLBACK_SELECTION = "fallback-no-provider"
PROVIDER_CONSENT_REQUIRED = "required-before-provider"
NO_PROVIDER_INTERACTION_AFFORDANCE = "disabled-no-provider-interaction"
PROVIDER_CONFIGURATION_UNCONFIGURED = "unconfigured"
PROVIDER_CONFIGURATION_FALLBACK_ACTIVE = "fallback-active"
LOCAL_PROVIDER_REGISTRY_STATE = "local-only-registry"
PROVIDER_BOUNDARY_INTERACTION_PLAN_STATE = "provider-boundary-interaction-plan"
PROVIDER_NEXT_ACTION_DISABLED = "provider-setup-disabled-until-consent"
LOCAL_HARDWARE_CAPABILITY_STATE = "local-planning-only"
GPU_CAPABILITY_UNPROBED = "gpu-unprobed"
CPU_FALLBACK_PRESERVED = "cpu-fallback-preserved"
POWER_STATE_NOT_EVALUATED = "power-state-not-evaluated"
THERMAL_GUARDRAILS_REQUIRED = "thermal-guardrails-required"
MODEL_WORKLOAD_DISABLED = "model-workload-disabled"
CAPABILITY_RECOMMENDATION_PENDING = "recommendation-pending"
CAPABILITY_PACK_LIFECYCLE_PLANNED = "capability-pack-lifecycle-planned"
CAPABILITY_PACK_DOWNLOADS_BLOCKED = "capability-pack-downloads-blocked"
HARDWARE_DETECTION_LEVEL_0 = "level-0-unknown-unprobed"
HARDWARE_DETECTION_LEVEL_1 = "level-1-safe-local-static-snapshot"
HARDWARE_DETECTION_LEVEL_2 = "level-2-lightweight-capability-check-future-gated"
HARDWARE_DETECTION_LEVEL_3 = "level-3-heavy-runtime-validation-blocked"
CAPABILITY_SNAPSHOT_POLICY_LOCAL_STATIC = "local-static-no-heavy-probe"
CAPABILITY_SNAPSHOT_SOURCE_DEFAULT = "default-static-snapshot"
RAM_READINESS_UNPROBED = "ram-unprobed"
DISK_READINESS_UNPROBED = "disk-unprobed"
CAPABILITY_PACK_MANIFEST_SCHEMA_VERSION = "capability-pack-manifest.v1"
CAPABILITY_PACK_MANIFEST_PLANNED = "manifest-planned"
CAPABILITY_PACK_SOURCE_LOCAL_ONLY = "local-source-future-gated"
CAPABILITY_PACK_CHECKSUM_REQUIRED = "checksum-required-before-install"
CAPABILITY_PACK_SIGNATURE_REQUIRED = "signature-required-before-install"
CAPABILITY_PACK_COMPATIBILITY_UNPROVEN = "compatibility-unproven"
CAPABILITY_PACK_INSTALL_BLOCKED = "install-blocked"
CAPABILITY_PACK_UPDATE_BLOCKED = "update-blocked"
CAPABILITY_PACK_UNINSTALL_BLOCKED = "uninstall-blocked"
MODEL_WORKLOAD_METADATA_PLANNED = "model-workload-metadata-planned"
DATA_CLASSIFICATION_LOCAL_ONLY = "data-classification-local-only"
DATA_CLASSIFICATION_SCHEMA_VERSION = "data-classification.v1"
PROVIDER_VISIBLE_DATA_GUARANTEE_NONE = "provider-visible-data-none-guaranteed"
MEMORY_CONTEXT_DISABLED = "memory-context-disabled"
MEMORY_INDEXING_DISABLED = "memory-indexing-disabled"
RETRIEVAL_DISABLED = "retrieval-disabled"
LEARNING_DISABLED = "learning-disabled"
PERSISTENCE_DISABLED = "persistence-disabled"
CONSENT_ENVELOPE_REQUIRED = "consent-envelope-required"
AUDIT_ENVELOPE_PLANNED = "audit-envelope-planned"
AUDIT_SECRETS_PLANNED = "audit-secrets-planned"
SECRET_BOUNDARY_NO_SECRETS = "secret-boundary-no-secrets-stored"
NETWORK_EGRESS_BLOCKED = "network-egress-blocked"
FUTURE_MEMORY_ELIGIBILITY_GATED = "future-memory-eligibility-gated"
WINDOWS_RESILIENCE_PLANNED = "windows-resilience-planned"
OFFLINE_DEGRADED_PLANNED = "offline-degraded-planned"
PERSONA_CORE_VOICE_BOUNDARY_PLANNED = "persona-core-voice-boundary-planned"
VOICE_RUNTIME_DISABLED = "voice-runtime-disabled"
VALIDATION_PROOF_GATES_PLANNED = "validation-proof-gates-planned"
ABUSE_EVAL_PENDING = "abuse-eval-pending"
RELEASE_PROOF_PENDING = "release-proof-pending"
CORE_DESKTOP_COPY_CONTRACT_VERSION = "core-desktop-provider-state-copy.v1"
CORE_DESKTOP_RUNTIME_STATE_CONTRACT = "core-desktop-runtime-state-contract"
DISABLED_PROMPT_BEHAVIOR_CONTRACT = "disabled-prompt-provider-behavior"
GOLDEN_PROVIDER_STATE_FIXTURES = "golden-provider-state-fixtures"
VALIDATOR_EXPANSION_ACTIVE = "validator-expansion-active"
CONTRACT_READY_MARKER = "contract-ready"
UI_READY_MARKER = "ui-ready"
VALIDATOR_READY_MARKER = "validator-ready"
FUTURE_IMPLEMENTATION_GATED_MARKER = "future-implementation-gated"
PROVIDER_RUNTIME_STATE_SCHEMA_VERSION = "provider-runtime-state.v1"
PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION = "provider-runtime-config.v1"
PROVIDER_RUNTIME_CONFIG_MIGRATION_POSTURE = "no-runtime-migration-required"
PROVIDER_RUNTIME_CATEGORY_NO_PROVIDER = "no_provider"
PROVIDER_RUNTIME_CATEGORY_SETUP_DISABLED = "provider_setup_disabled"
PROVIDER_RUNTIME_CATEGORY_UNCONFIGURED = "provider_unconfigured"
PROVIDER_RUNTIME_CATEGORY_UNAVAILABLE = "provider_unavailable"
PROVIDER_RUNTIME_CATEGORY_CONSENT_MISSING = "provider_consent_missing"
PROVIDER_RUNTIME_CATEGORY_CAPABILITY_MISSING = "provider_capability_missing"
PROVIDER_RUNTIME_CATEGORY_READY_FUTURE_GATED = "provider_ready_future_gated"
PROVIDER_RUNTIME_CATEGORY_ERROR_DEGRADED = "provider_error_degraded"
PROVIDER_RUNTIME_REASON_NO_PROVIDER_CONFIGURED = "no_provider_configured"
PROVIDER_RUNTIME_REASON_SETUP_DISABLED_LOCAL_ONLY = "provider_setup_disabled_local_only"
PROVIDER_RUNTIME_REASON_PROVIDER_UNCONFIGURED = "provider_unconfigured"
PROVIDER_RUNTIME_REASON_PROVIDER_UNAVAILABLE = "provider_unavailable"
PROVIDER_RUNTIME_REASON_CONSENT_REQUIRED = "provider_consent_required"
PROVIDER_RUNTIME_REASON_CAPABILITY_MISSING = "provider_capability_missing"
PROVIDER_RUNTIME_REASON_READY_FUTURE_GATED = "provider_ready_future_gated"
PROVIDER_RUNTIME_REASON_INVALID_CONFIG_FAIL_CLOSED = "invalid_config_fail_closed"
PROVIDER_RUNTIME_REASON_MISSING_CONFIG_FAIL_CLOSED = "missing_config_fail_closed"
PROVIDER_RUNTIME_PROVENANCE_DEFAULT_CONFIG = "default_config"
PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG = "local_config"
PROVIDER_RUNTIME_PROVENANCE_HARDWARE_SNAPSHOT = "hardware_snapshot"
PROVIDER_RUNTIME_PROVENANCE_MANIFEST_STATE = "manifest_state"
PROVIDER_RUNTIME_PROVENANCE_VALIDATOR_FIXTURE = "validator_fixture"
PROVIDER_RUNTIME_PROVENANCE_FUTURE_RUNTIME_CHECK = "future_runtime_check"
PROVIDER_RUNTIME_CONFIG_STATE_DEFAULT = "default_config"
PROVIDER_RUNTIME_CONFIG_STATE_MISSING = "missing_config"
PROVIDER_RUNTIME_CONFIG_STATE_INVALID = "invalid_config"
PROVIDER_RUNTIME_CONFIG_STATE_LOCAL = "local_config"
PROVIDER_RUNTIME_STATE_CATEGORIES = (
    PROVIDER_RUNTIME_CATEGORY_NO_PROVIDER,
    PROVIDER_RUNTIME_CATEGORY_SETUP_DISABLED,
    PROVIDER_RUNTIME_CATEGORY_UNCONFIGURED,
    PROVIDER_RUNTIME_CATEGORY_UNAVAILABLE,
    PROVIDER_RUNTIME_CATEGORY_CONSENT_MISSING,
    PROVIDER_RUNTIME_CATEGORY_CAPABILITY_MISSING,
    PROVIDER_RUNTIME_CATEGORY_READY_FUTURE_GATED,
    PROVIDER_RUNTIME_CATEGORY_ERROR_DEGRADED,
)
PROVIDER_RUNTIME_REASON_CODES = (
    PROVIDER_RUNTIME_REASON_NO_PROVIDER_CONFIGURED,
    PROVIDER_RUNTIME_REASON_SETUP_DISABLED_LOCAL_ONLY,
    PROVIDER_RUNTIME_REASON_PROVIDER_UNCONFIGURED,
    PROVIDER_RUNTIME_REASON_PROVIDER_UNAVAILABLE,
    PROVIDER_RUNTIME_REASON_CONSENT_REQUIRED,
    PROVIDER_RUNTIME_REASON_CAPABILITY_MISSING,
    PROVIDER_RUNTIME_REASON_READY_FUTURE_GATED,
    PROVIDER_RUNTIME_REASON_INVALID_CONFIG_FAIL_CLOSED,
    PROVIDER_RUNTIME_REASON_MISSING_CONFIG_FAIL_CLOSED,
)
PROVIDER_RUNTIME_PROVENANCE_SOURCES = (
    PROVIDER_RUNTIME_PROVENANCE_DEFAULT_CONFIG,
    PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
    PROVIDER_RUNTIME_PROVENANCE_HARDWARE_SNAPSHOT,
    PROVIDER_RUNTIME_PROVENANCE_MANIFEST_STATE,
    PROVIDER_RUNTIME_PROVENANCE_VALIDATOR_FIXTURE,
    PROVIDER_RUNTIME_PROVENANCE_FUTURE_RUNTIME_CHECK,
)


@dataclass(frozen=True)
class AIProviderRuntimeConfigSnapshot:
    schema_version: str
    config_state: str
    selected_provider_id: str
    provider_configured: bool
    provider_available: bool
    consent_granted: bool
    capability_ready: bool
    config_valid: bool
    provenance: str


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
    hardware_detection_level: str
    hardware_detection_label: str
    capability_snapshot_policy: str
    capability_snapshot_source: str
    capability_snapshot_budget_label: str
    ram_readiness_state: str
    ram_readiness_label: str
    disk_readiness_state: str
    disk_readiness_label: str
    model_workload_metadata_state: str
    model_workload_metadata_label: str
    capability_pack_lifecycle_state: str
    capability_pack_lifecycle_label: str
    capability_pack_download_state: str
    capability_pack_download_label: str
    capability_pack_manifest_schema_version: str
    capability_pack_manifest_state: str
    capability_pack_source_type: str
    capability_pack_checksum_state: str
    capability_pack_signature_state: str
    capability_pack_compatibility_state: str
    capability_pack_disk_requirement: str
    capability_pack_ram_requirement: str
    capability_pack_gpu_requirement: str
    capability_pack_install_state: str
    capability_pack_update_state: str
    capability_pack_uninstall_state: str
    data_classification_state: str
    data_classification_label: str
    data_classification_schema_version: str
    provider_visible_data_guarantee: str
    memory_context_state: str
    memory_context_label: str
    memory_indexing_state: str
    retrieval_state: str
    learning_state: str
    persistence_state: str
    future_memory_eligibility_marker: str
    consent_envelope_state: str
    audit_envelope_state: str
    secret_boundary_state: str
    network_egress_state: str
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
    core_desktop_copy_contract_version: str
    core_desktop_runtime_state_contract: str
    disabled_prompt_behavior_contract: str
    golden_provider_state_fixtures: str
    validator_expansion_state: str
    contract_ready_marker: str
    ui_ready_marker: str
    validator_ready_marker: str
    future_implementation_gated_marker: str
    privacy_scope: str
    privacy_label: str
    provider_visible_data: str
    provider_visible_data_label: str
    provider_visible_data_detail: str
    provider_interaction_state: str
    provider_interaction_label: str
    provider_interaction_detail: str
    provider_consent_boundary_label: str
    provider_next_action_label: str
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
    runtime_state_schema_version: str
    runtime_state_category: str
    runtime_state_label: str
    runtime_reason_code: str
    runtime_reason_label: str
    runtime_config_schema_version: str
    runtime_config_state: str
    runtime_config_label: str
    runtime_config_migration: str
    runtime_config_valid: bool
    runtime_fail_closed: bool
    runtime_provenance: str
    runtime_provenance_label: str
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
            "hardware_detection_level": self.hardware_detection_level,
            "hardware_detection_label": self.hardware_detection_label,
            "capability_snapshot_policy": self.capability_snapshot_policy,
            "capability_snapshot_source": self.capability_snapshot_source,
            "capability_snapshot_budget_label": self.capability_snapshot_budget_label,
            "ram_readiness_state": self.ram_readiness_state,
            "ram_readiness_label": self.ram_readiness_label,
            "disk_readiness_state": self.disk_readiness_state,
            "disk_readiness_label": self.disk_readiness_label,
            "model_workload_metadata_state": self.model_workload_metadata_state,
            "model_workload_metadata_label": self.model_workload_metadata_label,
            "capability_pack_lifecycle_state": self.capability_pack_lifecycle_state,
            "capability_pack_lifecycle_label": self.capability_pack_lifecycle_label,
            "capability_pack_download_state": self.capability_pack_download_state,
            "capability_pack_download_label": self.capability_pack_download_label,
            "capability_pack_manifest_schema_version": self.capability_pack_manifest_schema_version,
            "capability_pack_manifest_state": self.capability_pack_manifest_state,
            "capability_pack_source_type": self.capability_pack_source_type,
            "capability_pack_checksum_state": self.capability_pack_checksum_state,
            "capability_pack_signature_state": self.capability_pack_signature_state,
            "capability_pack_compatibility_state": self.capability_pack_compatibility_state,
            "capability_pack_disk_requirement": self.capability_pack_disk_requirement,
            "capability_pack_ram_requirement": self.capability_pack_ram_requirement,
            "capability_pack_gpu_requirement": self.capability_pack_gpu_requirement,
            "capability_pack_install_state": self.capability_pack_install_state,
            "capability_pack_update_state": self.capability_pack_update_state,
            "capability_pack_uninstall_state": self.capability_pack_uninstall_state,
            "data_classification_state": self.data_classification_state,
            "data_classification_label": self.data_classification_label,
            "data_classification_schema_version": self.data_classification_schema_version,
            "provider_visible_data_guarantee": self.provider_visible_data_guarantee,
            "memory_context_state": self.memory_context_state,
            "memory_context_label": self.memory_context_label,
            "memory_indexing_state": self.memory_indexing_state,
            "retrieval_state": self.retrieval_state,
            "learning_state": self.learning_state,
            "persistence_state": self.persistence_state,
            "future_memory_eligibility_marker": self.future_memory_eligibility_marker,
            "consent_envelope_state": self.consent_envelope_state,
            "audit_envelope_state": self.audit_envelope_state,
            "secret_boundary_state": self.secret_boundary_state,
            "network_egress_state": self.network_egress_state,
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
            "core_desktop_copy_contract_version": self.core_desktop_copy_contract_version,
            "core_desktop_runtime_state_contract": self.core_desktop_runtime_state_contract,
            "disabled_prompt_behavior_contract": self.disabled_prompt_behavior_contract,
            "golden_provider_state_fixtures": self.golden_provider_state_fixtures,
            "validator_expansion_state": self.validator_expansion_state,
            "contract_ready_marker": self.contract_ready_marker,
            "ui_ready_marker": self.ui_ready_marker,
            "validator_ready_marker": self.validator_ready_marker,
            "future_implementation_gated_marker": self.future_implementation_gated_marker,
            "privacy_scope": self.privacy_scope,
            "privacy_label": self.privacy_label,
            "provider_visible_data": self.provider_visible_data,
            "provider_visible_data_label": self.provider_visible_data_label,
            "provider_visible_data_detail": self.provider_visible_data_detail,
            "provider_interaction_state": self.provider_interaction_state,
            "provider_interaction_label": self.provider_interaction_label,
            "provider_interaction_detail": self.provider_interaction_detail,
            "provider_consent_boundary_label": self.provider_consent_boundary_label,
            "provider_next_action_label": self.provider_next_action_label,
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
            "runtime_state_schema_version": self.runtime_state_schema_version,
            "runtime_state_category": self.runtime_state_category,
            "runtime_state_label": self.runtime_state_label,
            "runtime_reason_code": self.runtime_reason_code,
            "runtime_reason_label": self.runtime_reason_label,
            "runtime_config_schema_version": self.runtime_config_schema_version,
            "runtime_config_state": self.runtime_config_state,
            "runtime_config_label": self.runtime_config_label,
            "runtime_config_migration": self.runtime_config_migration,
            "runtime_config_valid": self.runtime_config_valid,
            "runtime_fail_closed": self.runtime_fail_closed,
            "runtime_provenance": self.runtime_provenance,
            "runtime_provenance_label": self.runtime_provenance_label,
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
            "hardwareDetectionLevel": self.hardware_detection_level,
            "hardwareDetectionLabel": self.hardware_detection_label,
            "capabilitySnapshotPolicy": self.capability_snapshot_policy,
            "capabilitySnapshotSource": self.capability_snapshot_source,
            "capabilitySnapshotBudgetLabel": self.capability_snapshot_budget_label,
            "ramReadinessState": self.ram_readiness_state,
            "ramReadinessLabel": self.ram_readiness_label,
            "diskReadinessState": self.disk_readiness_state,
            "diskReadinessLabel": self.disk_readiness_label,
            "modelWorkloadMetadataState": self.model_workload_metadata_state,
            "modelWorkloadMetadataLabel": self.model_workload_metadata_label,
            "capabilityPackLifecycleState": self.capability_pack_lifecycle_state,
            "capabilityPackLifecycleLabel": self.capability_pack_lifecycle_label,
            "capabilityPackDownloadState": self.capability_pack_download_state,
            "capabilityPackDownloadLabel": self.capability_pack_download_label,
            "capabilityPackManifestSchemaVersion": self.capability_pack_manifest_schema_version,
            "capabilityPackManifestState": self.capability_pack_manifest_state,
            "capabilityPackSourceType": self.capability_pack_source_type,
            "capabilityPackChecksumState": self.capability_pack_checksum_state,
            "capabilityPackSignatureState": self.capability_pack_signature_state,
            "capabilityPackCompatibilityState": self.capability_pack_compatibility_state,
            "capabilityPackDiskRequirement": self.capability_pack_disk_requirement,
            "capabilityPackRamRequirement": self.capability_pack_ram_requirement,
            "capabilityPackGpuRequirement": self.capability_pack_gpu_requirement,
            "capabilityPackInstallState": self.capability_pack_install_state,
            "capabilityPackUpdateState": self.capability_pack_update_state,
            "capabilityPackUninstallState": self.capability_pack_uninstall_state,
            "dataClassificationState": self.data_classification_state,
            "dataClassificationLabel": self.data_classification_label,
            "dataClassificationSchemaVersion": self.data_classification_schema_version,
            "providerVisibleDataGuarantee": self.provider_visible_data_guarantee,
            "memoryContextState": self.memory_context_state,
            "memoryContextLabel": self.memory_context_label,
            "memoryIndexingState": self.memory_indexing_state,
            "retrievalState": self.retrieval_state,
            "learningState": self.learning_state,
            "persistenceState": self.persistence_state,
            "futureMemoryEligibilityMarker": self.future_memory_eligibility_marker,
            "consentEnvelopeState": self.consent_envelope_state,
            "auditEnvelopeState": self.audit_envelope_state,
            "secretBoundaryState": self.secret_boundary_state,
            "networkEgressState": self.network_egress_state,
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
            "coreDesktopCopyContractVersion": self.core_desktop_copy_contract_version,
            "coreDesktopRuntimeStateContract": self.core_desktop_runtime_state_contract,
            "disabledPromptBehaviorContract": self.disabled_prompt_behavior_contract,
            "goldenProviderStateFixtures": self.golden_provider_state_fixtures,
            "validatorExpansionState": self.validator_expansion_state,
            "contractReadyMarker": self.contract_ready_marker,
            "uiReadyMarker": self.ui_ready_marker,
            "validatorReadyMarker": self.validator_ready_marker,
            "futureImplementationGatedMarker": self.future_implementation_gated_marker,
            "privacyScope": self.privacy_scope,
            "privacyLabel": self.privacy_label,
            "providerVisibleData": self.provider_visible_data,
            "providerVisibleDataLabel": self.provider_visible_data_label,
            "providerVisibleDataDetail": self.provider_visible_data_detail,
            "providerInteractionState": self.provider_interaction_state,
            "providerInteractionLabel": self.provider_interaction_label,
            "providerInteractionDetail": self.provider_interaction_detail,
            "providerConsentBoundaryLabel": self.provider_consent_boundary_label,
            "providerNextActionLabel": self.provider_next_action_label,
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
            "runtimeStateSchemaVersion": self.runtime_state_schema_version,
            "runtimeStateCategory": self.runtime_state_category,
            "runtimeStateLabel": self.runtime_state_label,
            "runtimeReasonCode": self.runtime_reason_code,
            "runtimeReasonLabel": self.runtime_reason_label,
            "runtimeConfigSchemaVersion": self.runtime_config_schema_version,
            "runtimeConfigState": self.runtime_config_state,
            "runtimeConfigLabel": self.runtime_config_label,
            "runtimeConfigMigration": self.runtime_config_migration,
            "runtimeConfigValid": self.runtime_config_valid,
            "runtimeFailClosed": self.runtime_fail_closed,
            "runtimeProvenance": self.runtime_provenance,
            "runtimeProvenanceLabel": self.runtime_provenance_label,
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
        "hardware_detection_level": HARDWARE_DETECTION_LEVEL_1,
        "hardware_detection_label": "Hardware detection: Level 1 safe local static snapshot",
        "capability_snapshot_policy": CAPABILITY_SNAPSHOT_POLICY_LOCAL_STATIC,
        "capability_snapshot_source": CAPABILITY_SNAPSHOT_SOURCE_DEFAULT,
        "capability_snapshot_budget_label": "Capability snapshot budget: static only; no heavy probe",
        "ram_readiness_state": RAM_READINESS_UNPROBED,
        "ram_readiness_label": "RAM readiness: unprobed",
        "disk_readiness_state": DISK_READINESS_UNPROBED,
        "disk_readiness_label": "Disk readiness: unprobed",
        "model_workload_metadata_state": MODEL_WORKLOAD_METADATA_PLANNED,
        "model_workload_metadata_label": "Model workload metadata: planned; no execution",
        "capability_pack_manifest_schema_version": CAPABILITY_PACK_MANIFEST_SCHEMA_VERSION,
        "capability_pack_manifest_state": CAPABILITY_PACK_MANIFEST_PLANNED,
        "capability_pack_source_type": CAPABILITY_PACK_SOURCE_LOCAL_ONLY,
        "capability_pack_checksum_state": CAPABILITY_PACK_CHECKSUM_REQUIRED,
        "capability_pack_signature_state": CAPABILITY_PACK_SIGNATURE_REQUIRED,
        "capability_pack_compatibility_state": CAPABILITY_PACK_COMPATIBILITY_UNPROVEN,
        "capability_pack_disk_requirement": "disk requirement: future manifest required",
        "capability_pack_ram_requirement": "ram requirement: future manifest required",
        "capability_pack_gpu_requirement": "gpu requirement: future manifest required",
        "capability_pack_install_state": CAPABILITY_PACK_INSTALL_BLOCKED,
        "capability_pack_update_state": CAPABILITY_PACK_UPDATE_BLOCKED,
        "capability_pack_uninstall_state": CAPABILITY_PACK_UNINSTALL_BLOCKED,
        "data_classification_schema_version": DATA_CLASSIFICATION_SCHEMA_VERSION,
        "provider_visible_data_guarantee": PROVIDER_VISIBLE_DATA_GUARANTEE_NONE,
        "memory_indexing_state": MEMORY_INDEXING_DISABLED,
        "retrieval_state": RETRIEVAL_DISABLED,
        "learning_state": LEARNING_DISABLED,
        "persistence_state": PERSISTENCE_DISABLED,
        "future_memory_eligibility_marker": FUTURE_MEMORY_ELIGIBILITY_GATED,
        "consent_envelope_state": CONSENT_ENVELOPE_REQUIRED,
        "audit_envelope_state": AUDIT_ENVELOPE_PLANNED,
        "secret_boundary_state": SECRET_BOUNDARY_NO_SECRETS,
        "network_egress_state": NETWORK_EGRESS_BLOCKED,
        "core_desktop_copy_contract_version": CORE_DESKTOP_COPY_CONTRACT_VERSION,
        "core_desktop_runtime_state_contract": CORE_DESKTOP_RUNTIME_STATE_CONTRACT,
        "disabled_prompt_behavior_contract": DISABLED_PROMPT_BEHAVIOR_CONTRACT,
        "golden_provider_state_fixtures": GOLDEN_PROVIDER_STATE_FIXTURES,
        "validator_expansion_state": VALIDATOR_EXPANSION_ACTIVE,
        "contract_ready_marker": CONTRACT_READY_MARKER,
        "ui_ready_marker": UI_READY_MARKER,
        "validator_ready_marker": VALIDATOR_READY_MARKER,
        "future_implementation_gated_marker": FUTURE_IMPLEMENTATION_GATED_MARKER,
        "foundation_readiness_items": _foundation_readiness_items(),
    }


def _provider_boundary_interaction_fields(
    *,
    interaction_label: str,
    interaction_detail: str,
) -> dict[str, str]:
    return {
        "provider_visible_data_detail": "No prompt, file, screen, memory, or telemetry is sent",
        "provider_interaction_state": PROVIDER_BOUNDARY_INTERACTION_PLAN_STATE,
        "provider_interaction_label": interaction_label,
        "provider_interaction_detail": interaction_detail,
        "provider_consent_boundary_label": "Consent boundary: provider setup required before prompts",
        "provider_next_action_label": "Next: provider setup is disabled in this local-only foundation seam",
    }


def _runtime_contract_fields(
    *,
    category: str,
    reason_code: str,
    provenance: str = PROVIDER_RUNTIME_PROVENANCE_DEFAULT_CONFIG,
    config_state: str = PROVIDER_RUNTIME_CONFIG_STATE_DEFAULT,
    config_valid: bool = True,
    fail_closed: bool = True,
) -> dict[str, object]:
    category_labels = {
        PROVIDER_RUNTIME_CATEGORY_NO_PROVIDER: "Runtime state: no provider",
        PROVIDER_RUNTIME_CATEGORY_SETUP_DISABLED: "Runtime state: provider setup disabled",
        PROVIDER_RUNTIME_CATEGORY_UNCONFIGURED: "Runtime state: provider unconfigured",
        PROVIDER_RUNTIME_CATEGORY_UNAVAILABLE: "Runtime state: provider unavailable",
        PROVIDER_RUNTIME_CATEGORY_CONSENT_MISSING: "Runtime state: consent required",
        PROVIDER_RUNTIME_CATEGORY_CAPABILITY_MISSING: "Runtime state: capability missing",
        PROVIDER_RUNTIME_CATEGORY_READY_FUTURE_GATED: "Runtime state: ready but future-gated",
        PROVIDER_RUNTIME_CATEGORY_ERROR_DEGRADED: "Runtime state: degraded and fail-closed",
    }
    reason_labels = {
        PROVIDER_RUNTIME_REASON_NO_PROVIDER_CONFIGURED: "Reason: no provider configured",
        PROVIDER_RUNTIME_REASON_SETUP_DISABLED_LOCAL_ONLY: "Reason: setup disabled in local-only seam",
        PROVIDER_RUNTIME_REASON_PROVIDER_UNCONFIGURED: "Reason: provider configuration missing",
        PROVIDER_RUNTIME_REASON_PROVIDER_UNAVAILABLE: "Reason: provider unavailable",
        PROVIDER_RUNTIME_REASON_CONSENT_REQUIRED: "Reason: consent required before provider use",
        PROVIDER_RUNTIME_REASON_CAPABILITY_MISSING: "Reason: capability proof missing",
        PROVIDER_RUNTIME_REASON_READY_FUTURE_GATED: "Reason: future USER approval required",
        PROVIDER_RUNTIME_REASON_INVALID_CONFIG_FAIL_CLOSED: "Reason: invalid config failed closed",
        PROVIDER_RUNTIME_REASON_MISSING_CONFIG_FAIL_CLOSED: "Reason: missing config failed closed",
    }
    config_labels = {
        PROVIDER_RUNTIME_CONFIG_STATE_DEFAULT: "Config: safe default local-only",
        PROVIDER_RUNTIME_CONFIG_STATE_MISSING: "Config: missing; safe fallback active",
        PROVIDER_RUNTIME_CONFIG_STATE_INVALID: "Config: invalid; safe fallback active",
        PROVIDER_RUNTIME_CONFIG_STATE_LOCAL: "Config: local-only",
    }
    provenance_labels = {
        PROVIDER_RUNTIME_PROVENANCE_DEFAULT_CONFIG: "Provenance: default config",
        PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG: "Provenance: local config",
        PROVIDER_RUNTIME_PROVENANCE_HARDWARE_SNAPSHOT: "Provenance: hardware snapshot",
        PROVIDER_RUNTIME_PROVENANCE_MANIFEST_STATE: "Provenance: manifest state",
        PROVIDER_RUNTIME_PROVENANCE_VALIDATOR_FIXTURE: "Provenance: validator fixture",
        PROVIDER_RUNTIME_PROVENANCE_FUTURE_RUNTIME_CHECK: "Provenance: future runtime check",
    }
    normalized_category = category if category in PROVIDER_RUNTIME_STATE_CATEGORIES else PROVIDER_RUNTIME_CATEGORY_ERROR_DEGRADED
    normalized_reason = reason_code if reason_code in PROVIDER_RUNTIME_REASON_CODES else PROVIDER_RUNTIME_REASON_INVALID_CONFIG_FAIL_CLOSED
    normalized_config = config_state if config_state in {
        PROVIDER_RUNTIME_CONFIG_STATE_DEFAULT,
        PROVIDER_RUNTIME_CONFIG_STATE_MISSING,
        PROVIDER_RUNTIME_CONFIG_STATE_INVALID,
        PROVIDER_RUNTIME_CONFIG_STATE_LOCAL,
    } else PROVIDER_RUNTIME_CONFIG_STATE_INVALID
    normalized_provenance = (
        provenance if provenance in PROVIDER_RUNTIME_PROVENANCE_SOURCES else PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG
    )
    return {
        "runtime_state_schema_version": PROVIDER_RUNTIME_STATE_SCHEMA_VERSION,
        "runtime_state_category": normalized_category,
        "runtime_state_label": category_labels[normalized_category],
        "runtime_reason_code": normalized_reason,
        "runtime_reason_label": reason_labels[normalized_reason],
        "runtime_config_schema_version": PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION,
        "runtime_config_state": normalized_config,
        "runtime_config_label": config_labels[normalized_config],
        "runtime_config_migration": PROVIDER_RUNTIME_CONFIG_MIGRATION_POSTURE,
        "runtime_config_valid": bool(config_valid),
        "runtime_fail_closed": bool(fail_closed),
        "runtime_provenance": normalized_provenance,
        "runtime_provenance_label": provenance_labels[normalized_provenance],
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


def build_default_provider_runtime_config() -> AIProviderRuntimeConfigSnapshot:
    """Return the safe local-only default provider runtime config."""

    return AIProviderRuntimeConfigSnapshot(
        schema_version=PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION,
        config_state=PROVIDER_RUNTIME_CONFIG_STATE_DEFAULT,
        selected_provider_id=NO_PROVIDER_ID,
        provider_configured=False,
        provider_available=False,
        consent_granted=False,
        capability_ready=False,
        config_valid=True,
        provenance=PROVIDER_RUNTIME_PROVENANCE_DEFAULT_CONFIG,
    )


def normalize_provider_runtime_config(
    config: AIProviderRuntimeConfigSnapshot | dict[str, object] | None,
) -> AIProviderRuntimeConfigSnapshot:
    """Normalize local config into a fail-closed provider runtime contract input."""

    if config is None:
        return AIProviderRuntimeConfigSnapshot(
            schema_version=PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION,
            config_state=PROVIDER_RUNTIME_CONFIG_STATE_MISSING,
            selected_provider_id=NO_PROVIDER_ID,
            provider_configured=False,
            provider_available=False,
            consent_granted=False,
            capability_ready=False,
            config_valid=False,
            provenance=PROVIDER_RUNTIME_PROVENANCE_DEFAULT_CONFIG,
        )

    if isinstance(config, AIProviderRuntimeConfigSnapshot):
        if config.schema_version == PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION and config.config_valid:
            return config
        return replace(
            build_default_provider_runtime_config(),
            config_state=PROVIDER_RUNTIME_CONFIG_STATE_INVALID,
            config_valid=False,
            provenance=config.provenance
            if config.provenance in PROVIDER_RUNTIME_PROVENANCE_SOURCES
            else PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
        )

    if not isinstance(config, dict):
        return replace(
            build_default_provider_runtime_config(),
            config_state=PROVIDER_RUNTIME_CONFIG_STATE_INVALID,
            config_valid=False,
            provenance=PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
        )

    schema_version = str(config.get("schema_version") or "")
    selected_provider_id = str(config.get("selected_provider_id") or NO_PROVIDER_ID)
    provenance = str(config.get("provenance") or PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG)
    valid_provider_ids = {option.provider_id for option in _provider_selection_options()}
    config_valid = (
        bool(config.get("config_valid", True))
        and schema_version == PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION
        and selected_provider_id in valid_provider_ids
    )
    if not config_valid:
        return replace(
            build_default_provider_runtime_config(),
            config_state=PROVIDER_RUNTIME_CONFIG_STATE_INVALID,
            config_valid=False,
            provenance=provenance
            if provenance in PROVIDER_RUNTIME_PROVENANCE_SOURCES
            else PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
        )

    return AIProviderRuntimeConfigSnapshot(
        schema_version=schema_version,
        config_state=PROVIDER_RUNTIME_CONFIG_STATE_LOCAL,
        selected_provider_id=selected_provider_id,
        provider_configured=bool(config.get("provider_configured", False)),
        provider_available=bool(config.get("provider_available", False)),
        consent_granted=bool(config.get("consent_granted", False)),
        capability_ready=bool(config.get("capability_ready", False)),
        config_valid=True,
        provenance=provenance if provenance in PROVIDER_RUNTIME_PROVENANCE_SOURCES else PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
    )


def build_provider_runtime_contract_state(
    config: AIProviderRuntimeConfigSnapshot | dict[str, object] | None = None,
    *,
    surface_role: str = "hud",
) -> AIProviderStateSnapshot:
    """Resolve local provider runtime config into a fail-closed visible state."""

    normalized_config = normalize_provider_runtime_config(config)
    if normalized_config.config_state == PROVIDER_RUNTIME_CONFIG_STATE_MISSING:
        base_state = build_no_provider_ai_state(surface_role=surface_role)
        return replace(
            base_state,
            **_runtime_contract_fields(
                category=PROVIDER_RUNTIME_CATEGORY_NO_PROVIDER,
                reason_code=PROVIDER_RUNTIME_REASON_MISSING_CONFIG_FAIL_CLOSED,
                provenance=normalized_config.provenance,
                config_state=normalized_config.config_state,
                config_valid=False,
                fail_closed=True,
            ),
        )
    if normalized_config.config_state == PROVIDER_RUNTIME_CONFIG_STATE_INVALID:
        base_state = build_no_provider_ai_state(surface_role=surface_role)
        return replace(
            base_state,
            status_label="AI unavailable - config failed closed",
            disabled_reason="Provider runtime config is invalid, so provider behavior is disabled",
            interaction_disabled_reason="Invalid provider runtime config failed closed; prompts remain disabled",
            **_runtime_contract_fields(
                category=PROVIDER_RUNTIME_CATEGORY_ERROR_DEGRADED,
                reason_code=PROVIDER_RUNTIME_REASON_INVALID_CONFIG_FAIL_CLOSED,
                provenance=normalized_config.provenance,
                config_state=normalized_config.config_state,
                config_valid=False,
                fail_closed=True,
            ),
        )
    if normalized_config.selected_provider_id == NO_PROVIDER_ID:
        return build_local_ai_runtime_foundation_provider_boundary_state(surface_role=surface_role)
    if not normalized_config.provider_configured:
        base_state = build_local_provider_registry_state(surface_role=surface_role)
        return replace(
            base_state,
            **_runtime_contract_fields(
                category=PROVIDER_RUNTIME_CATEGORY_UNCONFIGURED,
                reason_code=PROVIDER_RUNTIME_REASON_PROVIDER_UNCONFIGURED,
                provenance=normalized_config.provenance,
                config_state=normalized_config.config_state,
                config_valid=True,
                fail_closed=True,
            ),
        )
    if not normalized_config.provider_available:
        base_state = build_provider_selection_consent_state(
            selected_provider_id=normalized_config.selected_provider_id,
            surface_role=surface_role,
        )
        return replace(
            base_state,
            **_runtime_contract_fields(
                category=PROVIDER_RUNTIME_CATEGORY_UNAVAILABLE,
                reason_code=PROVIDER_RUNTIME_REASON_PROVIDER_UNAVAILABLE,
                provenance=normalized_config.provenance,
                config_state=normalized_config.config_state,
                config_valid=True,
                fail_closed=True,
            ),
        )
    if not normalized_config.consent_granted:
        base_state = build_provider_selection_consent_state(
            selected_provider_id=normalized_config.selected_provider_id,
            surface_role=surface_role,
        )
        return replace(
            base_state,
            **_runtime_contract_fields(
                category=PROVIDER_RUNTIME_CATEGORY_CONSENT_MISSING,
                reason_code=PROVIDER_RUNTIME_REASON_CONSENT_REQUIRED,
                provenance=normalized_config.provenance,
                config_state=normalized_config.config_state,
                config_valid=True,
                fail_closed=True,
            ),
        )
    if not normalized_config.capability_ready:
        base_state = build_local_hardware_capability_state(surface_role=surface_role)
        return replace(
            base_state,
            **_runtime_contract_fields(
                category=PROVIDER_RUNTIME_CATEGORY_CAPABILITY_MISSING,
                reason_code=PROVIDER_RUNTIME_REASON_CAPABILITY_MISSING,
                provenance=normalized_config.provenance,
                config_state=normalized_config.config_state,
                config_valid=True,
                fail_closed=True,
            ),
        )

    base_state = build_local_ai_runtime_foundation_provider_boundary_state(surface_role=surface_role)
    return replace(
        base_state,
        **_runtime_contract_fields(
            category=PROVIDER_RUNTIME_CATEGORY_READY_FUTURE_GATED,
            reason_code=PROVIDER_RUNTIME_REASON_READY_FUTURE_GATED,
            provenance=normalized_config.provenance,
            config_state=normalized_config.config_state,
            config_valid=True,
            fail_closed=True,
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
        **_provider_boundary_interaction_fields(
            interaction_label="Provider boundary plan: no-provider fallback",
            interaction_detail="Choose and approve a provider before AI prompts can run",
        ),
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
        **_runtime_contract_fields(
            category=PROVIDER_RUNTIME_CATEGORY_NO_PROVIDER,
            reason_code=PROVIDER_RUNTIME_REASON_NO_PROVIDER_CONFIGURED,
        ),
        surface_role=normalized_surface,
        provider_options=_provider_selection_options(),
    )


def build_local_ai_runtime_foundation_provider_boundary_state(
    *,
    surface_role: str = "hud",
) -> AIProviderStateSnapshot:
    """Build the active local-only FAM-007 runtime-foundation provider boundary."""

    normalized_surface = surface_role if surface_role in {"core", "hud", "combined"} else "hud"
    return AIProviderStateSnapshot(
        package_id=PACKAGE_ID,
        slice_ids=(SLC_017_ID, SLC_018_ID),
        state_id=LOCAL_AI_RUNTIME_FOUNDATION_STATE_ID,
        mode=LOCAL_AI_RUNTIME_FOUNDATION_MODE,
        availability=LOCAL_AI_RUNTIME_FOUNDATION_AVAILABILITY,
        provider_label="No AI provider",
        provider_kind="local-runtime-foundation-scaffold",
        status_label="Local AI foundation: no provider",
        disabled_reason="Local AI runtime foundation is active, but provider execution is disabled",
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
        privacy_label="Local runtime foundation only; nothing is sent",
        provider_visible_data="none",
        provider_visible_data_label="Provider-visible data: none",
        **_provider_boundary_interaction_fields(
            interaction_label="Provider boundary: local foundation active",
            interaction_detail="Local runtime foundation is visible while provider calls and prompts stay disabled",
        ),
        local_storage="none",
        consent_state=PROVIDER_CONSENT_REQUIRED,
        consent_label="Consent required before any provider setup",
        interaction_affordance=NO_PROVIDER_INTERACTION_AFFORDANCE,
        interaction_label="Assisted Desktop unavailable",
        interaction_disabled_reason="Local AI foundation is provider-disabled; consent and configuration are required before prompts can run",
        no_provider_fallback_label="No-provider fallback active",
        prompt_acceptance="disabled",
        external_calls="blocked",
        model_state="not installed",
        capability_pack_state="not installed",
        source_truth="renderer-local FAM-007 runtime foundation provider boundary",
        **_runtime_contract_fields(
            category=PROVIDER_RUNTIME_CATEGORY_SETUP_DISABLED,
            reason_code=PROVIDER_RUNTIME_REASON_SETUP_DISABLED_LOCAL_ONLY,
        ),
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
        **_provider_boundary_interaction_fields(
            interaction_label="Provider boundary plan: consent required",
            interaction_detail="Provider selection remains local-only until consent and configuration are complete",
        ),
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
        **_runtime_contract_fields(
            category=PROVIDER_RUNTIME_CATEGORY_CONSENT_MISSING,
            reason_code=PROVIDER_RUNTIME_REASON_CONSENT_REQUIRED,
        ),
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
        **_provider_boundary_interaction_fields(
            interaction_label="Provider boundary plan: registry local-only",
            interaction_detail="Provider configuration remains unconfigured and no-provider fallback stays active",
        ),
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
        **_runtime_contract_fields(
            category=PROVIDER_RUNTIME_CATEGORY_UNCONFIGURED,
            reason_code=PROVIDER_RUNTIME_REASON_PROVIDER_UNCONFIGURED,
        ),
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
        **_provider_boundary_interaction_fields(
            interaction_label="Provider boundary plan: capability proof first",
            interaction_detail="Hardware proof and consent are required before model workloads can run",
        ),
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
        **_runtime_contract_fields(
            category=PROVIDER_RUNTIME_CATEGORY_CAPABILITY_MISSING,
            reason_code=PROVIDER_RUNTIME_REASON_CAPABILITY_MISSING,
        ),
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
        **_provider_boundary_interaction_fields(
            interaction_label="Provider boundary plan: local foundation only",
            interaction_detail="Provider consent, capability proof, and future USER approval are required before AI prompts can run",
        ),
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
        **_runtime_contract_fields(
            category=PROVIDER_RUNTIME_CATEGORY_READY_FUTURE_GATED,
            reason_code=PROVIDER_RUNTIME_REASON_READY_FUTURE_GATED,
        ),
        surface_role=normalized_surface,
        provider_options=_provider_selection_options(),
    )
