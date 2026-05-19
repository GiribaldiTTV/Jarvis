"""Validate the FAM-007 no-provider/provider-privacy scaffold."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.ai_provider_state import (  # noqa: E402
    CAPABILITY_PACK_DOWNLOADS_BLOCKED,
    CAPABILITY_PACK_LIFECYCLE_PLANNED,
    CAPABILITY_PACK_CHECKSUM_REQUIRED,
    CAPABILITY_PACK_COMPATIBILITY_UNPROVEN,
    CAPABILITY_PACK_INSTALL_BLOCKED,
    CAPABILITY_PACK_MANIFEST_PLANNED,
    CAPABILITY_PACK_MANIFEST_SCHEMA_VERSION,
    CAPABILITY_PACK_SIGNATURE_REQUIRED,
    CAPABILITY_PACK_SOURCE_LOCAL_ONLY,
    CAPABILITY_PACK_UNINSTALL_BLOCKED,
    CAPABILITY_PACK_UPDATE_BLOCKED,
    CONTRACT_READY_MARKER,
    CORE_DESKTOP_COPY_CONTRACT_VERSION,
    CORE_DESKTOP_RUNTIME_STATE_CONTRACT,
    DATA_CLASSIFICATION_SCHEMA_VERSION,
    DISABLED_PROMPT_BEHAVIOR_CONTRACT,
    FAM007_FOUNDATION_READINESS_MODE,
    FAM007_FOUNDATION_READINESS_STATE_ID,
    HARDWARE_DETECTION_LEVEL_1,
    LOCAL_AI_RUNTIME_FOUNDATION_AVAILABILITY,
    LOCAL_AI_RUNTIME_FOUNDATION_MODE,
    LOCAL_AI_RUNTIME_FOUNDATION_STATE_ID,
    LOCAL_HARDWARE_CAPABILITY_STATE,
    LOCAL_PROVIDER_REGISTRY_AVAILABILITY,
    LOCAL_PROVIDER_REGISTRY_MODE,
    LOCAL_PROVIDER_REGISTRY_STATE,
    LOCAL_PROVIDER_REGISTRY_STATE_ID,
    NO_PROVIDER_AVAILABILITY,
    NO_PROVIDER_FALLBACK_SELECTION,
    NO_PROVIDER_ID,
    NO_PROVIDER_INTERACTION_AFFORDANCE,
    NO_PROVIDER_MODE,
    NO_PROVIDER_PRIVACY_SCOPE,
    PACKAGE_ID,
    PROVIDER_CONFIGURATION_UNCONFIGURED,
    PROVIDER_CONSENT_REQUIRED,
    RAM_READINESS_UNPROBED,
    DISK_READINESS_UNPROBED,
    MODEL_WORKLOAD_METADATA_PLANNED,
    PROVIDER_SELECTION_AVAILABILITY,
    PROVIDER_SELECTION_MODE,
    PROVIDER_SELECTION_STATE_ID,
    SLC_017_ID,
    SLC_018_ID,
    SLC_031_ID,
    SLC_032_ID,
    SLC_033_ID,
    SLC_034_ID,
    SLC_035_ID,
    SLC_036_ID,
    VALIDATION_PROOF_GATES_PLANNED,
    MEMORY_CONTEXT_DISABLED,
    MEMORY_INDEXING_DISABLED,
    NETWORK_EGRESS_BLOCKED,
    PERSISTENCE_DISABLED,
    PROVIDER_VISIBLE_DATA_GUARANTEE_NONE,
    RETRIEVAL_DISABLED,
    LEARNING_DISABLED,
    SECRET_BOUNDARY_NO_SECRETS,
    CONSENT_ENVELOPE_REQUIRED,
    AUDIT_ENVELOPE_PLANNED,
    GOLDEN_PROVIDER_STATE_FIXTURES,
    VALIDATOR_EXPANSION_ACTIVE,
    UI_READY_MARKER,
    VALIDATOR_READY_MARKER,
    FUTURE_IMPLEMENTATION_GATED_MARKER,
    WINDOWS_RESILIENCE_PLANNED,
    PERSONA_CORE_VOICE_BOUNDARY_PLANNED,
    PROVIDER_BOUNDARY_INTERACTION_PLAN_STATE,
    PROVIDER_RUNTIME_CATEGORY_CAPABILITY_MISSING,
    PROVIDER_RUNTIME_CATEGORY_CONSENT_MISSING,
    PROVIDER_RUNTIME_CATEGORY_ERROR_DEGRADED,
    PROVIDER_RUNTIME_CATEGORY_NO_PROVIDER,
    PROVIDER_RUNTIME_CATEGORY_READY_FUTURE_GATED,
    PROVIDER_RUNTIME_CATEGORY_SETUP_DISABLED,
    PROVIDER_RUNTIME_CATEGORY_UNCONFIGURED,
    PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION,
    PROVIDER_RUNTIME_CONFIG_STATE_INVALID,
    PROVIDER_RUNTIME_CONFIG_STATE_MISSING,
    PROVIDER_RUNTIME_CONFIG_STATE_DEFAULT,
    PROVIDER_RUNTIME_PROVENANCE_DEFAULT_CONFIG,
    PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
    PROVIDER_RUNTIME_REASON_CAPABILITY_MISSING,
    PROVIDER_RUNTIME_REASON_CONSENT_REQUIRED,
    PROVIDER_RUNTIME_REASON_INVALID_CONFIG_FAIL_CLOSED,
    PROVIDER_RUNTIME_REASON_MISSING_CONFIG_FAIL_CLOSED,
    PROVIDER_RUNTIME_REASON_NO_PROVIDER_CONFIGURED,
    PROVIDER_RUNTIME_REASON_PROVIDER_UNCONFIGURED,
    PROVIDER_RUNTIME_REASON_READY_FUTURE_GATED,
    PROVIDER_RUNTIME_REASON_SETUP_DISABLED_LOCAL_ONLY,
    PROVIDER_RUNTIME_STATE_CATEGORIES,
    PROVIDER_RUNTIME_STATE_SCHEMA_VERSION,
    PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
    PROVIDER_READINESS_CONFIG_STATE_DEFAULT,
    PROVIDER_READINESS_CONFIG_STATE_INVALID,
    PROVIDER_READINESS_CONFIG_STATE_LOCAL,
    PROVIDER_READINESS_CONFIG_STATE_MISSING,
    PROVIDER_READINESS_PROVENANCE_CAPABILITY_MANIFEST,
    PROVIDER_READINESS_PROVENANCE_CONSENT_STATE,
    PROVIDER_READINESS_PROVENANCE_DEFAULT_CONFIG,
    PROVIDER_READINESS_PROVENANCE_FUTURE_RUNTIME_CHECK,
    PROVIDER_READINESS_PROVENANCE_HARDWARE_SNAPSHOT,
    PROVIDER_READINESS_PROVENANCE_RELEASE_SOURCE_TRUTH,
    PROVIDER_READINESS_REASON_CAPABILITY_MISSING,
    PROVIDER_READINESS_REASON_CONFIG_INVALID_FAIL_CLOSED,
    PROVIDER_READINESS_REASON_CONFIG_MISSING_FAIL_CLOSED,
    PROVIDER_READINESS_REASON_CONSENT_MISSING,
    PROVIDER_READINESS_REASON_DEFAULT_LOCAL_ONLY,
    PROVIDER_READINESS_REASON_FUTURE_PROVIDER_GATED,
    PROVIDER_READINESS_REASON_MANIFEST_INVALID_INSTALL_BLOCKED,
    PROVIDER_READINESS_REASON_MANIFEST_MISSING,
    PROVIDER_READINESS_REASON_PROVIDER_NOT_READY,
    PROVIDER_READINESS_REASON_PROVIDER_READY_EXECUTION_GATED,
    PROVIDER_READINESS_REASON_PROVIDER_UNCONFIGURED,
    PROVIDER_READINESS_STATE_PROVIDER_READY_EXECUTION_GATED,
    PROVIDER_READINESS_STATE_SCHEMA_VERSION,
    PROVIDER_READINESS_STATE_SETUP_AVAILABLE_FUTURE_GATED,
    PROVIDER_READINESS_STATE_SETUP_BLOCKED_BY_CAPABILITY,
    PROVIDER_READINESS_STATE_SETUP_BLOCKED_BY_CONSENT,
    PROVIDER_READINESS_STATE_SETUP_BLOCKED_BY_MANIFEST,
    PROVIDER_READINESS_STATE_SETUP_CONFIG_REQUIRED,
    PROVIDER_READINESS_STATE_SETUP_DISABLED,
    PROVIDER_READINESS_STATE_DEGRADED,
    PROVIDER_SETUP_BLOCKER_CAPABILITY_REQUIRED,
    PROVIDER_SETUP_BLOCKER_CONFIG_INVALID,
    PROVIDER_SETUP_BLOCKER_CONFIG_REQUIRED,
    PROVIDER_SETUP_BLOCKER_CONSENT_REQUIRED,
    PROVIDER_SETUP_BLOCKER_FUTURE_GATE,
    PROVIDER_SETUP_BLOCKER_MANIFEST_REQUIRED,
    PROVIDER_SETUP_BLOCKER_NONE,
    PROVIDER_SETUP_BLOCKER_PROVIDER_NOT_READY,
    PROVIDER_SETUP_BLOCKER_SETUP_DISABLED,
    PROVIDER_SETUP_ELIGIBILITY_BLOCKED,
    PROVIDER_SETUP_ELIGIBILITY_CONFIG_REQUIRED,
    PROVIDER_SETUP_ELIGIBILITY_DISABLED,
    PROVIDER_SETUP_ELIGIBILITY_EXECUTION_GATED,
    PROVIDER_SETUP_ELIGIBILITY_FUTURE_GATED,
    PROVIDER_FUTURE_GATE_STATUS_EXECUTION_REQUIRED,
    PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
    PROVIDER_ACTIVATION_CONFIG_SCHEMA_VERSION,
    PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
    PROVIDER_ACTIVATION_CONFIG_STATE_INVALID,
    PROVIDER_ACTIVATION_CONFIG_STATE_LOCAL,
    PROVIDER_ACTIVATION_CONFIG_STATE_MISSING,
    PROVIDER_ACTIVATION_PROVENANCE_ADAPTER_CONTRACT,
    PROVIDER_ACTIVATION_PROVENANCE_CAPABILITY_MANIFEST,
    PROVIDER_ACTIVATION_PROVENANCE_CONSENT_STATE,
    PROVIDER_ACTIVATION_PROVENANCE_DEFAULT_CONFIG,
    PROVIDER_ACTIVATION_PROVENANCE_FUTURE_RUNTIME_CHECK,
    PROVIDER_ACTIVATION_PROVENANCE_READINESS_STATE,
    PROVIDER_ACTIVATION_PROVENANCE_RELEASE_SOURCE_TRUTH,
    PROVIDER_ACTIVATION_REASON_ADAPTER_UNAVAILABLE,
    PROVIDER_ACTIVATION_REASON_CAPABILITY_REQUIRED,
    PROVIDER_ACTIVATION_REASON_CONFIG_INVALID_FAIL_CLOSED,
    PROVIDER_ACTIVATION_REASON_CONFIG_MISSING_FAIL_CLOSED,
    PROVIDER_ACTIVATION_REASON_CONSENT_REQUIRED,
    PROVIDER_ACTIVATION_REASON_DEFAULT_UNAVAILABLE,
    PROVIDER_ACTIVATION_REASON_EXECUTION_GATED,
    PROVIDER_ACTIVATION_REASON_FUTURE_GATED,
    PROVIDER_ACTIVATION_REASON_FUNCTIONAL_AI_FUTURE_VERSION,
    PROVIDER_ACTIVATION_REASON_MANIFEST_REQUIRED,
    PROVIDER_ACTIVATION_REASON_POLICY_BLOCKED,
    PROVIDER_ACTIVATION_REASON_READINESS_BLOCKED,
    PROVIDER_ACTIVATION_STATE_BLOCKED_BY_ADAPTER,
    PROVIDER_ACTIVATION_STATE_BLOCKED_BY_CAPABILITY,
    PROVIDER_ACTIVATION_STATE_BLOCKED_BY_CONSENT,
    PROVIDER_ACTIVATION_STATE_BLOCKED_BY_MANIFEST,
    PROVIDER_ACTIVATION_STATE_BLOCKED_BY_POLICY,
    PROVIDER_ACTIVATION_STATE_BLOCKED_BY_READINESS,
    PROVIDER_ACTIVATION_STATE_DEGRADED,
    PROVIDER_ACTIVATION_STATE_DISABLED,
    PROVIDER_ACTIVATION_STATE_ELIGIBLE_FUTURE_GATED,
    PROVIDER_ACTIVATION_STATE_FUNCTIONAL_AI_READY_FUTURE_VERSION,
    PROVIDER_ACTIVATION_STATE_READY_EXECUTION_GATED,
    PROVIDER_ACTIVATION_STATE_SCHEMA_VERSION,
    PROVIDER_ACTIVATION_STATE_UNAVAILABLE,
    PROVIDER_ACTIVATION_ELIGIBILITY_BLOCKED,
    PROVIDER_ACTIVATION_ELIGIBILITY_DISABLED,
    PROVIDER_ACTIVATION_ELIGIBILITY_EXECUTION_GATED,
    PROVIDER_ACTIVATION_ELIGIBILITY_FUTURE_GATED,
    PROVIDER_ACTIVATION_ELIGIBILITY_FUTURE_VERSION,
    PROVIDER_ACTIVATION_ELIGIBILITY_UNAVAILABLE,
    PROVIDER_ACTIVATION_BLOCKER_ADAPTER_UNAVAILABLE,
    PROVIDER_ACTIVATION_BLOCKER_CAPABILITY_REQUIRED,
    PROVIDER_ACTIVATION_BLOCKER_CONFIG_INVALID,
    PROVIDER_ACTIVATION_BLOCKER_CONSENT_REQUIRED,
    PROVIDER_ACTIVATION_BLOCKER_EXECUTION_GATE,
    PROVIDER_ACTIVATION_BLOCKER_FUTURE_ACTIVATION_GATE,
    PROVIDER_ACTIVATION_BLOCKER_MANIFEST_REQUIRED,
    PROVIDER_ACTIVATION_BLOCKER_POLICY_BLOCKED,
    PROVIDER_ACTIVATION_BLOCKER_READINESS_REQUIRED,
    PROVIDER_ACTIVATION_BLOCKER_VERSION_JUMP_REQUIRED,
    PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_EXECUTION_REQUIRED,
    PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
    PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_VERSION_JUMP_REQUIRED,
    PROVIDER_ADAPTER_POSTURE_NULL_LOCAL,
    PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
    PROVIDER_ADAPTER_AVAILABILITY_READY_FUTURE_GATED,
    PROVIDER_ADAPTER_EXECUTION_POSTURE_DISABLED,
    PROVIDER_METADATA_CONTRACT_VERSION,
    PROVIDER_CONFIG_ENVELOPE_VERSION,
    PROVIDER_ACTIVATION_HANDOFF_STATE_FUTURE_GATED,
    PROVIDER_SDK_INTEGRATION_BOUNDARY_FUTURE_APPROVAL,
    PROMPT_EXECUTION_GATE_DISABLED,
    MODEL_EXECUTION_GATE_DISABLED,
    PROVIDER_EXECUTION_GATE_DISABLED,
    FAM007_EXECUTION_READINESS_MODE,
    FAM007_EXECUTION_READINESS_STATE_ID,
    PROVIDER_EXECUTION_READINESS_CONFIG_SCHEMA_VERSION,
    PROVIDER_EXECUTION_READINESS_STATE_SCHEMA_VERSION,
    PROVIDER_EXECUTION_CONFIG_STATE_DEFAULT,
    PROVIDER_EXECUTION_CONFIG_STATE_INVALID,
    PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
    PROVIDER_EXECUTION_CONFIG_STATE_MISSING,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_ACTIVATION,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_ADAPTER,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_CONSENT,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_MODEL_GATE,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_NETWORK,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_POLICY,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_PROMPT_GATE,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_PROVIDER_PATH,
    PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_SAFETY,
    PROVIDER_EXECUTION_READINESS_STATE_DEGRADED,
    PROVIDER_EXECUTION_READINESS_STATE_DISABLED,
    PROVIDER_EXECUTION_READINESS_STATE_FUNCTIONAL_AI_READY_FUTURE_VERSION,
    PROVIDER_EXECUTION_READINESS_STATE_READY_BUT_NOT_APPROVED,
    PROVIDER_EXECUTION_READINESS_STATE_READY_FUTURE_GATED,
    PROVIDER_EXECUTION_READINESS_STATE_UNAVAILABLE,
    PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
    PROVIDER_EXECUTION_ELIGIBILITY_DISABLED,
    PROVIDER_EXECUTION_ELIGIBILITY_FUTURE_GATED,
    PROVIDER_EXECUTION_ELIGIBILITY_FUTURE_VERSION,
    PROVIDER_EXECUTION_ELIGIBILITY_READY_NOT_APPROVED,
    PROVIDER_EXECUTION_ELIGIBILITY_UNAVAILABLE,
    PROVIDER_EXECUTION_BLOCKER_ACTIVATION_REQUIRED,
    PROVIDER_EXECUTION_BLOCKER_ADAPTER_REQUIRED,
    PROVIDER_EXECUTION_BLOCKER_APPROVAL_REQUIRED,
    PROVIDER_EXECUTION_BLOCKER_CONFIG_INVALID,
    PROVIDER_EXECUTION_BLOCKER_CONSENT_REQUIRED,
    PROVIDER_EXECUTION_BLOCKER_FUTURE_EXECUTION_GATE,
    PROVIDER_EXECUTION_BLOCKER_MODEL_GATE,
    PROVIDER_EXECUTION_BLOCKER_NETWORK_APPROVAL_REQUIRED,
    PROVIDER_EXECUTION_BLOCKER_POLICY_BLOCKED,
    PROVIDER_EXECUTION_BLOCKER_PROMPT_GATE,
    PROVIDER_EXECUTION_BLOCKER_PROVIDER_PATH_REQUIRED,
    PROVIDER_EXECUTION_BLOCKER_SAFETY_EVAL_REQUIRED,
    PROVIDER_EXECUTION_BLOCKER_VERSION_JUMP_REQUIRED,
    PROVIDER_EXECUTION_REASON_ACTIVATION_BLOCKED,
    PROVIDER_EXECUTION_REASON_ADAPTER_UNAVAILABLE,
    PROVIDER_EXECUTION_REASON_APPROVAL_MISSING,
    PROVIDER_EXECUTION_REASON_CONFIG_INVALID_FAIL_CLOSED,
    PROVIDER_EXECUTION_REASON_CONFIG_MISSING_FAIL_CLOSED,
    PROVIDER_EXECUTION_REASON_CONSENT_REQUIRED,
    PROVIDER_EXECUTION_REASON_DEFAULT_UNAVAILABLE,
    PROVIDER_EXECUTION_REASON_FUNCTIONAL_AI_FUTURE_VERSION,
    PROVIDER_EXECUTION_REASON_FUTURE_GATED,
    PROVIDER_EXECUTION_REASON_MODEL_GATE_BLOCKED,
    PROVIDER_EXECUTION_REASON_NETWORK_BLOCKED,
    PROVIDER_EXECUTION_REASON_POLICY_BLOCKED,
    PROVIDER_EXECUTION_REASON_PROMPT_GATE_BLOCKED,
    PROVIDER_EXECUTION_REASON_PROVIDER_PATH_MISSING,
    PROVIDER_EXECUTION_REASON_SAFETY_EVAL_REQUIRED,
    PROVIDER_EXECUTION_PROVENANCE_ACTIVATION_STATE,
    PROVIDER_EXECUTION_PROVENANCE_ADAPTER_CONTRACT,
    PROVIDER_EXECUTION_PROVENANCE_CONSENT_STATE,
    PROVIDER_EXECUTION_PROVENANCE_DEFAULT_CONFIG,
    PROVIDER_EXECUTION_PROVENANCE_FUTURE_RUNTIME_CHECK,
    PROVIDER_EXECUTION_PROVENANCE_LOCAL_CONFIG,
    PROVIDER_EXECUTION_PROVENANCE_MODEL_GATE,
    PROVIDER_EXECUTION_PROVENANCE_NETWORK_POLICY,
    PROVIDER_EXECUTION_PROVENANCE_PROMPT_GATE,
    PROVIDER_EXECUTION_PROVENANCE_PROVIDER_PATH_CONTRACT,
    PROVIDER_EXECUTION_PROVENANCE_RELEASE_SOURCE_TRUTH,
    PROVIDER_EXECUTION_PROVENANCE_SAFETY_EVAL,
    PROVIDER_EXECUTION_APPROVAL_STATUS_GRANTED_FOR_PROOF,
    PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
    PROVIDER_EXECUTION_APPROVAL_STATUS_FUTURE_GATED,
    PROVIDER_PATH_STATUS_NOT_SELECTED,
    PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
    ADAPTER_SELECTION_POSTURE_NULL_LOCAL,
    ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
    PROMPT_ACCEPTANCE_GATE_DISABLED,
    PROMPT_ACCEPTANCE_GATE_FUTURE_GATED,
    PROMPT_ROUTING_GATE_DISABLED,
    PROMPT_ROUTING_GATE_FUTURE_GATED,
    PROMPT_SEND_POSTURE_DISABLED,
    MODEL_EXECUTION_STATUS_DISABLED,
    MODEL_EXECUTION_STATUS_FUTURE_GATED,
    MODEL_WORKLOAD_READINESS_DISABLED,
    MODEL_WORKLOAD_READINESS_FUTURE_GATED,
    PROVIDER_VISIBLE_DATA_EXECUTION_NONE,
    PROVIDER_VISIBLE_DATA_EXECUTION_FUTURE_GATED,
    EXTERNAL_CALL_READINESS_BLOCKED,
    EXTERNAL_CALL_READINESS_FUTURE_GATED,
    SAFETY_EVAL_READINESS_PENDING,
    SAFETY_EVAL_READINESS_READY,
    FUNCTIONAL_AI_RELEASE_GATE_PENDING,
    FUNCTIONAL_AI_RELEASE_GATE_READY_FUTURE_VERSION,
    V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
    V18_RELEASE_GATE_READY_FUTURE_VERSION,
    FUNCTIONAL_AI_CRITERIA_PENDING,
    FUNCTIONAL_AI_CRITERIA_READY_FUTURE_VERSION,
    V18_PREBETA_READINESS_PENDING,
    V18_PREBETA_READINESS_READY,
    READINESS_GATE_READY,
    CONSENT_GATE_READY,
    CAPABILITY_GATE_READY,
    MANIFEST_GATE_READY,
    ADAPTER_GATE_READY_FUTURE_GATED,
    SAFETY_EVAL_GATE_READY,
    CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
    CAPABILITY_PACK_ELIGIBILITY_FUTURE_GATED,
    CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
    CAPABILITY_PACK_INSTALL_INTENT_FUTURE_GATED,
    CAPABILITY_PACK_INSTALL_INTENT_NONE,
    CAPABILITY_PACK_MANIFEST_INVALID,
    CAPABILITY_PACK_MANIFEST_MISSING,
    CAPABILITY_PACK_MANIFEST_VALID_FUTURE_GATED,
    READINESS_ACTION_ALLOWED_LOCAL_READ_ONLY,
    READINESS_ACTION_FUTURE_USER_APPROVAL_REQUIRED,
    PROVIDER_NEXT_ACTION_DISABLED,
    build_default_provider_activation_config,
    build_default_provider_execution_readiness_config,
    build_fam007_foundation_readiness_state,
    build_default_provider_runtime_config,
    build_default_provider_readiness_config,
    build_local_ai_runtime_foundation_provider_boundary_state,
    build_local_provider_registry_state,
    build_no_provider_ai_state,
    build_provider_readiness_contract_state,
    build_provider_activation_foundation_state,
    build_provider_execution_readiness_gates_state,
    build_provider_runtime_contract_state,
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
    registry_snapshot = build_local_provider_registry_state(surface_role="core")
    runtime_foundation_snapshot = build_local_ai_runtime_foundation_provider_boundary_state(surface_role="core")
    foundation_snapshot = build_fam007_foundation_readiness_state(surface_role="core")
    default_runtime_snapshot = build_provider_runtime_contract_state(
        build_default_provider_runtime_config(),
        surface_role="core",
    )
    missing_config_snapshot = build_provider_runtime_contract_state(None, surface_role="core")
    invalid_config_snapshot = build_provider_runtime_contract_state(
        {
            "schema_version": "provider-runtime-config.v0",
            "selected_provider_id": "external-provider",
            "provenance": PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
        },
        surface_role="core",
    )
    unconfigured_runtime_snapshot = build_provider_runtime_contract_state(
        {
            "schema_version": PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION,
            "selected_provider_id": "local-capability-pack",
            "provider_configured": False,
            "provider_available": False,
            "consent_granted": False,
            "capability_ready": False,
            "provenance": PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
        },
        surface_role="core",
    )
    capability_missing_snapshot = build_provider_runtime_contract_state(
        {
            "schema_version": PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION,
            "selected_provider_id": "local-capability-pack",
            "provider_configured": True,
            "provider_available": True,
            "consent_granted": True,
            "capability_ready": False,
            "provenance": PROVIDER_RUNTIME_PROVENANCE_LOCAL_CONFIG,
        },
        surface_role="core",
    )
    default_readiness_snapshot = build_provider_readiness_contract_state(
        build_default_provider_readiness_config(),
        surface_role="core",
    )
    missing_readiness_snapshot = build_provider_readiness_contract_state(None, surface_role="core")
    invalid_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": "provider-readiness-config.v0",
            "provider_configured": True,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    unconfigured_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": False,
            "consent_granted": False,
            "capability_ready": False,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    consent_missing_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": False,
            "capability_ready": False,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    capability_missing_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": False,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    manifest_missing_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    manifest_invalid_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": False,
            "install_intent_requested": True,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    future_gated_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "future_provider_setup_approved": False,
            "install_intent_requested": True,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    provider_not_ready_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "future_provider_setup_approved": True,
            "provider_ready": False,
            "install_intent_requested": True,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    execution_gated_readiness_snapshot = build_provider_readiness_contract_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "future_provider_setup_approved": True,
            "provider_ready": True,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    default_activation_config_snapshot = build_default_provider_activation_config()
    default_activation_snapshot = build_provider_activation_foundation_state(
        build_default_provider_readiness_config(),
        surface_role="core",
    )
    missing_activation_config_snapshot = build_provider_activation_foundation_state(
        build_default_provider_readiness_config(),
        activation_config=None,
        surface_role="core",
    )
    invalid_activation_config_snapshot = build_provider_activation_foundation_state(
        build_default_provider_readiness_config(),
        activation_config={
            "schema_version": "provider-activation-config.v0",
            "provenance": "local_config",
        },
        surface_role="core",
    )
    readiness_blocked_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": False,
            "consent_granted": False,
            "capability_ready": False,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    consent_blocked_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": False,
            "capability_ready": False,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    capability_blocked_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": False,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    manifest_blocked_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    policy_blocked_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "policy_allows_setup": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    future_gated_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "future_provider_setup_approved": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    adapter_unavailable_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "future_provider_setup_approved": True,
            "provider_ready": True,
            "provenance": "local_config",
        },
        activation_config={
            "schema_version": PROVIDER_ACTIVATION_CONFIG_SCHEMA_VERSION,
            "future_activation_approved": True,
            "adapter_available": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    execution_gated_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "future_provider_setup_approved": True,
            "provider_ready": True,
            "provenance": "local_config",
        },
        activation_config={
            "schema_version": PROVIDER_ACTIVATION_CONFIG_SCHEMA_VERSION,
            "future_activation_approved": True,
            "adapter_available": True,
            "safety_eval_complete": True,
            "prompt_execution_approved": False,
            "model_execution_approved": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    functional_future_version_activation_snapshot = build_provider_activation_foundation_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "future_provider_setup_approved": True,
            "provider_ready": True,
            "provenance": "local_config",
        },
        activation_config={
            "schema_version": PROVIDER_ACTIVATION_CONFIG_SCHEMA_VERSION,
            "future_activation_approved": True,
            "adapter_available": True,
            "safety_eval_complete": True,
            "prompt_execution_approved": True,
            "model_execution_approved": True,
            "functional_ai_ready": True,
            "provenance": "local_config",
        },
        surface_role="core",
    )

    execution_ready_readiness_config = {
        "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
        "provider_configured": True,
        "consent_granted": True,
        "capability_ready": True,
        "manifest_available": True,
        "manifest_valid": True,
        "future_provider_setup_approved": True,
        "provider_ready": True,
        "provenance": "local_config",
    }
    execution_ready_activation_config = {
        "schema_version": PROVIDER_ACTIVATION_CONFIG_SCHEMA_VERSION,
        "future_activation_approved": True,
        "adapter_available": True,
        "safety_eval_complete": True,
        "prompt_execution_approved": False,
        "model_execution_approved": False,
        "provenance": "local_config",
    }

    def _execution_config(**overrides: object) -> dict[str, object]:
        config: dict[str, object] = {
            "schema_version": PROVIDER_EXECUTION_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_path_selected": False,
            "provider_adapter_selected": False,
            "prompt_acceptance_approved": False,
            "prompt_routing_approved": False,
            "model_execution_approved": False,
            "provider_visible_data_approved": False,
            "network_external_approved": False,
            "consent_granted": False,
            "safety_eval_complete": False,
            "policy_allows_execution": True,
            "execution_approved": False,
            "functional_ai_release_ready": False,
            "provenance": "local_config",
        }
        config.update(overrides)
        return config

    default_execution_config_snapshot = build_default_provider_execution_readiness_config()
    default_execution_snapshot = build_provider_execution_readiness_gates_state(
        build_default_provider_readiness_config(),
        surface_role="core",
    )
    missing_execution_config_snapshot = build_provider_execution_readiness_gates_state(
        build_default_provider_readiness_config(),
        execution_config=None,
        surface_role="core",
    )
    invalid_execution_config_snapshot = build_provider_execution_readiness_gates_state(
        build_default_provider_readiness_config(),
        execution_config={
            "schema_version": "provider-execution-readiness-config.v0",
            "provenance": "local_config",
        },
        surface_role="core",
    )
    activation_blocked_execution_snapshot = build_provider_execution_readiness_gates_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": False,
            "consent_granted": False,
            "capability_ready": False,
            "manifest_available": False,
            "manifest_valid": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    future_gated_execution_snapshot = build_provider_execution_readiness_gates_state(
        {
            "schema_version": PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            "provider_configured": True,
            "consent_granted": True,
            "capability_ready": True,
            "manifest_available": True,
            "manifest_valid": True,
            "future_provider_setup_approved": False,
            "provenance": "local_config",
        },
        surface_role="core",
    )
    provider_path_missing_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(),
        surface_role="core",
    )
    adapter_unavailable_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(provider_path_selected=True),
        surface_role="core",
    )
    prompt_gate_blocked_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(
            provider_path_selected=True,
            provider_adapter_selected=True,
        ),
        surface_role="core",
    )
    model_gate_blocked_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(
            provider_path_selected=True,
            provider_adapter_selected=True,
            prompt_acceptance_approved=True,
            prompt_routing_approved=True,
        ),
        surface_role="core",
    )
    consent_blocked_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(
            provider_path_selected=True,
            provider_adapter_selected=True,
            prompt_acceptance_approved=True,
            prompt_routing_approved=True,
            model_execution_approved=True,
        ),
        surface_role="core",
    )
    safety_blocked_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(
            provider_path_selected=True,
            provider_adapter_selected=True,
            prompt_acceptance_approved=True,
            prompt_routing_approved=True,
            model_execution_approved=True,
            consent_granted=True,
        ),
        surface_role="core",
    )
    network_blocked_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(
            provider_path_selected=True,
            provider_adapter_selected=True,
            prompt_acceptance_approved=True,
            prompt_routing_approved=True,
            model_execution_approved=True,
            consent_granted=True,
            safety_eval_complete=True,
        ),
        surface_role="core",
    )
    policy_blocked_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(
            provider_path_selected=True,
            provider_adapter_selected=True,
            prompt_acceptance_approved=True,
            prompt_routing_approved=True,
            model_execution_approved=True,
            consent_granted=True,
            safety_eval_complete=True,
            network_external_approved=True,
            policy_allows_execution=False,
        ),
        surface_role="core",
    )
    approval_missing_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(
            provider_path_selected=True,
            provider_adapter_selected=True,
            prompt_acceptance_approved=True,
            prompt_routing_approved=True,
            model_execution_approved=True,
            provider_visible_data_approved=True,
            consent_granted=True,
            safety_eval_complete=True,
            network_external_approved=True,
        ),
        surface_role="core",
    )
    functional_future_version_execution_snapshot = build_provider_execution_readiness_gates_state(
        execution_ready_readiness_config,
        activation_config=execution_ready_activation_config,
        execution_config=_execution_config(
            provider_path_selected=True,
            provider_adapter_selected=True,
            prompt_acceptance_approved=True,
            prompt_routing_approved=True,
            model_execution_approved=True,
            provider_visible_data_approved=True,
            consent_granted=True,
            safety_eval_complete=True,
            network_external_approved=True,
            execution_approved=True,
            functional_ai_release_ready=True,
        ),
        surface_role="core",
    )
    payload = snapshot.as_renderer_payload()
    selection_payload = selection_snapshot.as_renderer_payload()
    registry_payload = registry_snapshot.as_renderer_payload()
    runtime_foundation_payload = runtime_foundation_snapshot.as_renderer_payload()
    foundation_payload = foundation_snapshot.as_renderer_payload()
    default_runtime_payload = default_runtime_snapshot.as_renderer_payload()
    missing_config_payload = missing_config_snapshot.as_renderer_payload()
    invalid_config_payload = invalid_config_snapshot.as_renderer_payload()
    unconfigured_runtime_payload = unconfigured_runtime_snapshot.as_renderer_payload()
    capability_missing_payload = capability_missing_snapshot.as_renderer_payload()
    readiness_payloads = {
        "default": default_readiness_snapshot.as_renderer_payload(),
        "missing": missing_readiness_snapshot.as_renderer_payload(),
        "invalid": invalid_readiness_snapshot.as_renderer_payload(),
        "unconfigured": unconfigured_readiness_snapshot.as_renderer_payload(),
        "consent_missing": consent_missing_readiness_snapshot.as_renderer_payload(),
        "capability_missing": capability_missing_readiness_snapshot.as_renderer_payload(),
        "manifest_missing": manifest_missing_readiness_snapshot.as_renderer_payload(),
        "manifest_invalid": manifest_invalid_readiness_snapshot.as_renderer_payload(),
        "future_gated": future_gated_readiness_snapshot.as_renderer_payload(),
        "provider_not_ready": provider_not_ready_readiness_snapshot.as_renderer_payload(),
        "execution_gated": execution_gated_readiness_snapshot.as_renderer_payload(),
    }
    activation_payloads = {
        "default": default_activation_snapshot.as_renderer_payload(),
        "missing_config": missing_activation_config_snapshot.as_renderer_payload(),
        "invalid_config": invalid_activation_config_snapshot.as_renderer_payload(),
        "readiness_blocked": readiness_blocked_activation_snapshot.as_renderer_payload(),
        "consent_blocked": consent_blocked_activation_snapshot.as_renderer_payload(),
        "capability_blocked": capability_blocked_activation_snapshot.as_renderer_payload(),
        "manifest_blocked": manifest_blocked_activation_snapshot.as_renderer_payload(),
        "policy_blocked": policy_blocked_activation_snapshot.as_renderer_payload(),
        "future_gated": future_gated_activation_snapshot.as_renderer_payload(),
        "adapter_unavailable": adapter_unavailable_activation_snapshot.as_renderer_payload(),
        "execution_gated": execution_gated_activation_snapshot.as_renderer_payload(),
        "functional_future_version": functional_future_version_activation_snapshot.as_renderer_payload(),
    }
    execution_payloads = {
        "default": default_execution_snapshot.as_renderer_payload(),
        "missing_config": missing_execution_config_snapshot.as_renderer_payload(),
        "invalid_config": invalid_execution_config_snapshot.as_renderer_payload(),
        "activation_blocked": activation_blocked_execution_snapshot.as_renderer_payload(),
        "future_gated": future_gated_execution_snapshot.as_renderer_payload(),
        "provider_path_missing": provider_path_missing_execution_snapshot.as_renderer_payload(),
        "adapter_unavailable": adapter_unavailable_execution_snapshot.as_renderer_payload(),
        "prompt_gate_blocked": prompt_gate_blocked_execution_snapshot.as_renderer_payload(),
        "model_gate_blocked": model_gate_blocked_execution_snapshot.as_renderer_payload(),
        "consent_blocked": consent_blocked_execution_snapshot.as_renderer_payload(),
        "safety_blocked": safety_blocked_execution_snapshot.as_renderer_payload(),
        "network_blocked": network_blocked_execution_snapshot.as_renderer_payload(),
        "policy_blocked": policy_blocked_execution_snapshot.as_renderer_payload(),
        "approval_missing": approval_missing_execution_snapshot.as_renderer_payload(),
        "functional_future_version": functional_future_version_execution_snapshot.as_renderer_payload(),
    }
    renderer = _read("desktop/desktop_renderer.py")
    core_renderer = _read("desktop/core_visualization_renderer.py")
    html = _read("nexus_visual/orin_core.html")
    desktop_html = _read("nexus_visual/orin_core_desktop.html")
    css = _read("nexus_visual/orin_core.css")
    js = _read("nexus_visual/orin_core.js")
    branch_record = _read("Docs/branch_records/feature_fam_007_provider_boundary_no_provider_shell.md")
    active_activation_branch_record = _read(
        "Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md"
    )
    active_execution_branch_record = _read(
        "Docs/branch_records/feature_fam_007_local_ai_provider_execution_readiness_gates.md"
    )
    execution_branch_plan = _read(
        "Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md"
    )
    active_readiness_branch_record = _read(
        "Docs/branch_records/feature_fam_007_local_ai_provider_runtime_readiness.md"
    )
    continuation_branch_record = _read(
        "Docs/branch_records/feature_fam_007_local_ai_foundation_runtime_continuation.md"
    )

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
    _require(
        payload["providerVisibleDataDetail"] == "No prompt, file, screen, memory, or telemetry is sent",
        "no-provider state must disclose that no prompt, file, screen, memory, or telemetry is sent",
        failures,
    )
    _require(
        payload["providerInteractionState"] == PROVIDER_BOUNDARY_INTERACTION_PLAN_STATE,
        "no-provider state must publish the provider-boundary interaction plan",
        failures,
    )
    _require(
        payload["providerNextActionLabel"] == "Next: provider setup is disabled in this local-only foundation seam",
        "no-provider state must keep provider setup disabled inside the local-only foundation seam",
        failures,
    )
    _require(
        PROVIDER_NEXT_ACTION_DISABLED in _read("desktop/ai_provider_state.py"),
        "provider next-action disabled constant must be preserved in the local-only scaffold",
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
        selection_payload["providerInteractionState"] == PROVIDER_BOUNDARY_INTERACTION_PLAN_STATE,
        "provider-selection scaffold must expose provider-boundary interaction plan state",
        failures,
    )
    _require(
        selection_payload["providerConsentBoundaryLabel"] == "Consent boundary: provider setup required before prompts",
        "provider-selection scaffold must expose the consent boundary label",
        failures,
    )
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
    _require(
        registry_snapshot.state_id == LOCAL_PROVIDER_REGISTRY_STATE_ID,
        "provider registry scaffold must use the admitted registry/configuration state id",
        failures,
    )
    _require(
        registry_snapshot.mode == LOCAL_PROVIDER_REGISTRY_MODE,
        "provider registry scaffold must use provider-registry mode",
        failures,
    )
    _require(
        registry_snapshot.availability == LOCAL_PROVIDER_REGISTRY_AVAILABILITY,
        "provider registry scaffold must remain unavailable until configured",
        failures,
    )
    _require(
        registry_payload["selectedProviderId"] == NO_PROVIDER_ID,
        "provider registry scaffold must keep no-provider selected",
        failures,
    )
    _require(
        registry_payload["providerSelectionState"] == NO_PROVIDER_FALLBACK_SELECTION,
        "provider registry scaffold must preserve no-provider fallback compatibility",
        failures,
    )
    _require(
        registry_payload["providerConfigurationState"] == PROVIDER_CONFIGURATION_UNCONFIGURED,
        "provider registry scaffold must expose unconfigured provider state",
        failures,
    )
    _require(
        registry_payload["providerRegistryState"] == LOCAL_PROVIDER_REGISTRY_STATE,
        "provider registry scaffold must expose local-only registry state",
        failures,
    )
    _require(
        registry_payload["configuredProviderCount"] == 0,
        "provider registry scaffold must not report configured providers",
        failures,
    )
    _require(
        registry_payload["availableProviderCount"] == 0,
        "provider registry scaffold must not report available providers",
        failures,
    )
    _require(registry_payload["requiresConsent"] is True, "provider registry scaffold must require consent", failures)
    _require(registry_payload["sentToProvider"] is False, "provider registry scaffold must send nothing to providers", failures)
    _require(registry_payload["storedLocally"] is False, "provider registry scaffold must not persist local memory", failures)
    _require(registry_payload["canAcceptPrompts"] is False, "provider registry scaffold must not accept prompts", failures)
    _require(registry_payload["externalCalls"] == "blocked", "provider registry scaffold must block external calls", failures)
    _require(
        registry_payload["providerVisibleData"] == "none",
        "provider registry scaffold must expose no provider-visible data",
        failures,
    )
    _require(
        registry_payload["providerVisibleDataLabel"] == "Provider-visible data: none",
        "provider registry scaffold must keep provider-visible-data disclosure consistent",
        failures,
    )
    _require(
        registry_payload["providerConfigurationLabel"] == "Provider configuration: none",
        "provider registry scaffold must visibly disclose empty provider configuration",
        failures,
    )
    _require(
        registry_payload["providerRegistryLabel"] == "Local provider registry: no configured providers",
        "provider registry scaffold must visibly disclose local-only registry posture",
        failures,
    )
    _require(
        registry_payload["providerInteractionState"] == PROVIDER_BOUNDARY_INTERACTION_PLAN_STATE,
        "provider registry scaffold must expose provider-boundary interaction plan state",
        failures,
    )
    _require(
        len(registry_payload["providerRegistry"]) >= 3,
        "provider registry scaffold must publish local provider registry metadata",
        failures,
    )
    for entry in registry_payload["providerRegistry"]:
        _require(entry["configured"] is False, "provider registry entries must not be configured", failures)
        _require(entry["providerVisibleData"] == "none", "provider registry entries must not expose provider-visible data", failures)
        _require(entry["externalCalls"] == "blocked", "provider registry entries must block external calls", failures)

    _require(
        runtime_foundation_snapshot.state_id == LOCAL_AI_RUNTIME_FOUNDATION_STATE_ID,
        "runtime foundation boundary must use the current FAM-007 state id",
        failures,
    )
    _require(
        runtime_foundation_snapshot.mode == LOCAL_AI_RUNTIME_FOUNDATION_MODE,
        "runtime foundation boundary must use runtime-foundation provider-boundary mode",
        failures,
    )
    _require(
        runtime_foundation_snapshot.availability == LOCAL_AI_RUNTIME_FOUNDATION_AVAILABILITY,
        "runtime foundation boundary must remain disabled/local-only",
        failures,
    )
    _require(
        runtime_foundation_snapshot.slice_ids == (SLC_017_ID, SLC_018_ID),
        "runtime foundation boundary must stay bounded to SLC-017/SLC-018",
        failures,
    )
    _require(
        runtime_foundation_payload["providerLabel"] == "No AI provider",
        "runtime foundation boundary must keep visible no-provider posture",
        failures,
    )
    _require(
        runtime_foundation_payload["statusLabel"] == "Local AI foundation: no provider",
        "runtime foundation boundary must expose the current local foundation status",
        failures,
    )
    _require(
        runtime_foundation_payload["providerInteractionLabel"] == "Provider boundary: local foundation active",
        "runtime foundation boundary must expose an active local provider-boundary label",
        failures,
    )
    _require(
        runtime_foundation_payload["providerNextActionLabel"]
        == "Next: provider setup is disabled in this local-only foundation seam",
        "runtime foundation boundary must not gate the seam behind a later approval-missing blocker",
        failures,
    )
    _require(
        runtime_foundation_payload["privacyLabel"] == "Local runtime foundation only; nothing is sent",
        "runtime foundation boundary must visibly disclose local-only runtime posture",
        failures,
    )
    _require(
        runtime_foundation_payload["providerVisibleData"] == "none",
        "runtime foundation boundary must expose no provider-visible data",
        failures,
    )
    _require(
        runtime_foundation_payload["sentToProvider"] is False,
        "runtime foundation boundary must send nothing to providers",
        failures,
    )
    _require(
        runtime_foundation_payload["storedLocally"] is False,
        "runtime foundation boundary must not persist local memory",
        failures,
    )
    _require(
        runtime_foundation_payload["canAcceptPrompts"] is False,
        "runtime foundation boundary must keep prompts disabled",
        failures,
    )
    _require(
        runtime_foundation_payload["runtimeStateSchemaVersion"] == PROVIDER_RUNTIME_STATE_SCHEMA_VERSION,
        "runtime foundation boundary must expose the provider runtime state schema version",
        failures,
    )
    _require(
        runtime_foundation_payload["runtimeConfigSchemaVersion"] == PROVIDER_RUNTIME_CONFIG_SCHEMA_VERSION,
        "runtime foundation boundary must expose the provider runtime config schema version",
        failures,
    )
    _require(
        runtime_foundation_payload["runtimeStateCategory"] == PROVIDER_RUNTIME_CATEGORY_SETUP_DISABLED,
        "runtime foundation boundary must publish provider_setup_disabled runtime category",
        failures,
    )
    _require(
        runtime_foundation_payload["runtimeReasonCode"] == PROVIDER_RUNTIME_REASON_SETUP_DISABLED_LOCAL_ONLY,
        "runtime foundation boundary must publish a setup-disabled reason code",
        failures,
    )
    _require(
        runtime_foundation_payload["runtimeProvenance"] == PROVIDER_RUNTIME_PROVENANCE_DEFAULT_CONFIG,
        "runtime foundation boundary must publish default-config provenance",
        failures,
    )
    _require(
        runtime_foundation_payload["runtimeConfigState"] == PROVIDER_RUNTIME_CONFIG_STATE_DEFAULT,
        "runtime foundation boundary must publish safe default config state",
        failures,
    )
    _require(
        runtime_foundation_payload["runtimeFailClosed"] is True,
        "runtime foundation boundary must fail closed while provider execution is disabled",
        failures,
    )
    _require(
        default_runtime_payload["runtimeStateCategory"] == PROVIDER_RUNTIME_CATEGORY_SETUP_DISABLED,
        "default provider runtime config must resolve to setup-disabled local-only posture",
        failures,
    )
    _require(
        missing_config_payload["runtimeStateCategory"] == PROVIDER_RUNTIME_CATEGORY_NO_PROVIDER,
        "missing provider runtime config must resolve to no-provider posture",
        failures,
    )
    _require(
        missing_config_payload["runtimeReasonCode"] == PROVIDER_RUNTIME_REASON_MISSING_CONFIG_FAIL_CLOSED,
        "missing provider runtime config must publish missing-config fail-closed reason",
        failures,
    )
    _require(
        missing_config_payload["runtimeConfigState"] == PROVIDER_RUNTIME_CONFIG_STATE_MISSING,
        "missing provider runtime config must publish missing-config state",
        failures,
    )
    _require(
        invalid_config_payload["runtimeStateCategory"] == PROVIDER_RUNTIME_CATEGORY_ERROR_DEGRADED,
        "invalid provider runtime config must resolve to degraded fail-closed posture",
        failures,
    )
    _require(
        invalid_config_payload["runtimeReasonCode"] == PROVIDER_RUNTIME_REASON_INVALID_CONFIG_FAIL_CLOSED,
        "invalid provider runtime config must publish invalid-config fail-closed reason",
        failures,
    )
    _require(
        invalid_config_payload["runtimeConfigState"] == PROVIDER_RUNTIME_CONFIG_STATE_INVALID,
        "invalid provider runtime config must publish invalid-config state",
        failures,
    )
    _require(
        invalid_config_payload["runtimeFailClosed"] is True
        and invalid_config_payload["sentToProvider"] is False
        and invalid_config_payload["canAcceptPrompts"] is False,
        "invalid provider runtime config must fail closed without provider sends or prompt acceptance",
        failures,
    )
    _require(
        unconfigured_runtime_payload["runtimeStateCategory"] == PROVIDER_RUNTIME_CATEGORY_UNCONFIGURED,
        "local provider config without configured provider must resolve to provider_unconfigured",
        failures,
    )
    _require(
        unconfigured_runtime_payload["runtimeReasonCode"] == PROVIDER_RUNTIME_REASON_PROVIDER_UNCONFIGURED,
        "local provider config without configured provider must publish provider-unconfigured reason",
        failures,
    )
    _require(
        capability_missing_payload["runtimeStateCategory"] == PROVIDER_RUNTIME_CATEGORY_CAPABILITY_MISSING,
        "configured provider without capability proof must resolve to capability-missing",
        failures,
    )
    _require(
        capability_missing_payload["runtimeReasonCode"] == PROVIDER_RUNTIME_REASON_CAPABILITY_MISSING,
        "configured provider without capability proof must publish capability-missing reason",
        failures,
    )
    _require(
        "provider_unavailable" in PROVIDER_RUNTIME_STATE_CATEGORIES,
        "runtime categories must reserve provider_unavailable state",
        failures,
    )
    _require(
        "provider_consent_missing" in PROVIDER_RUNTIME_STATE_CATEGORIES,
        "runtime categories must reserve provider_consent_missing state",
        failures,
    )
    _require(
        default_runtime_payload["runtimeStateLabel"] == "Runtime state: provider setup disabled",
        "runtime state must publish visible runtime-state label",
        failures,
    )
    _require(
        default_runtime_payload["runtimeReasonLabel"] == "Reason: setup disabled in local-only seam",
        "runtime state must publish visible runtime reason-code label",
        failures,
    )
    _require(
        default_runtime_payload["runtimeProvenanceLabel"] == "Provenance: default config",
        "runtime state must publish visible runtime provenance label",
        failures,
    )

    readiness_expectations = {
        "default": (
            PROVIDER_READINESS_STATE_SETUP_DISABLED,
            PROVIDER_SETUP_ELIGIBILITY_DISABLED,
            PROVIDER_SETUP_BLOCKER_SETUP_DISABLED,
            PROVIDER_READINESS_REASON_DEFAULT_LOCAL_ONLY,
            PROVIDER_READINESS_PROVENANCE_DEFAULT_CONFIG,
            PROVIDER_READINESS_CONFIG_STATE_DEFAULT,
            CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
            CAPABILITY_PACK_MANIFEST_MISSING,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "missing": (
            PROVIDER_READINESS_STATE_SETUP_DISABLED,
            PROVIDER_SETUP_ELIGIBILITY_DISABLED,
            PROVIDER_SETUP_BLOCKER_SETUP_DISABLED,
            PROVIDER_READINESS_REASON_CONFIG_MISSING_FAIL_CLOSED,
            PROVIDER_READINESS_PROVENANCE_DEFAULT_CONFIG,
            PROVIDER_READINESS_CONFIG_STATE_MISSING,
            CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
            CAPABILITY_PACK_MANIFEST_MISSING,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "invalid": (
            PROVIDER_READINESS_STATE_DEGRADED,
            PROVIDER_SETUP_ELIGIBILITY_BLOCKED,
            PROVIDER_SETUP_BLOCKER_CONFIG_INVALID,
            PROVIDER_READINESS_REASON_CONFIG_INVALID_FAIL_CLOSED,
            "local_config",
            PROVIDER_READINESS_CONFIG_STATE_INVALID,
            CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
            CAPABILITY_PACK_MANIFEST_MISSING,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "unconfigured": (
            PROVIDER_READINESS_STATE_SETUP_CONFIG_REQUIRED,
            PROVIDER_SETUP_ELIGIBILITY_CONFIG_REQUIRED,
            PROVIDER_SETUP_BLOCKER_CONFIG_REQUIRED,
            PROVIDER_READINESS_REASON_PROVIDER_UNCONFIGURED,
            "local_config",
            PROVIDER_READINESS_CONFIG_STATE_LOCAL,
            CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
            CAPABILITY_PACK_MANIFEST_MISSING,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "consent_missing": (
            PROVIDER_READINESS_STATE_SETUP_BLOCKED_BY_CONSENT,
            PROVIDER_SETUP_ELIGIBILITY_BLOCKED,
            PROVIDER_SETUP_BLOCKER_CONSENT_REQUIRED,
            PROVIDER_READINESS_REASON_CONSENT_MISSING,
            PROVIDER_READINESS_PROVENANCE_CONSENT_STATE,
            PROVIDER_READINESS_CONFIG_STATE_LOCAL,
            CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
            CAPABILITY_PACK_MANIFEST_MISSING,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "capability_missing": (
            PROVIDER_READINESS_STATE_SETUP_BLOCKED_BY_CAPABILITY,
            PROVIDER_SETUP_ELIGIBILITY_BLOCKED,
            PROVIDER_SETUP_BLOCKER_CAPABILITY_REQUIRED,
            PROVIDER_READINESS_REASON_CAPABILITY_MISSING,
            PROVIDER_READINESS_PROVENANCE_HARDWARE_SNAPSHOT,
            PROVIDER_READINESS_CONFIG_STATE_LOCAL,
            CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
            CAPABILITY_PACK_MANIFEST_MISSING,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "manifest_missing": (
            PROVIDER_READINESS_STATE_SETUP_BLOCKED_BY_MANIFEST,
            PROVIDER_SETUP_ELIGIBILITY_BLOCKED,
            PROVIDER_SETUP_BLOCKER_MANIFEST_REQUIRED,
            PROVIDER_READINESS_REASON_MANIFEST_MISSING,
            PROVIDER_READINESS_PROVENANCE_CAPABILITY_MANIFEST,
            PROVIDER_READINESS_CONFIG_STATE_LOCAL,
            CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
            CAPABILITY_PACK_MANIFEST_MISSING,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "manifest_invalid": (
            PROVIDER_READINESS_STATE_SETUP_BLOCKED_BY_MANIFEST,
            PROVIDER_SETUP_ELIGIBILITY_BLOCKED,
            PROVIDER_SETUP_BLOCKER_MANIFEST_REQUIRED,
            PROVIDER_READINESS_REASON_MANIFEST_INVALID_INSTALL_BLOCKED,
            PROVIDER_READINESS_PROVENANCE_CAPABILITY_MANIFEST,
            PROVIDER_READINESS_CONFIG_STATE_LOCAL,
            CAPABILITY_PACK_ELIGIBILITY_BLOCKED,
            CAPABILITY_PACK_MANIFEST_INVALID,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "future_gated": (
            PROVIDER_READINESS_STATE_SETUP_AVAILABLE_FUTURE_GATED,
            PROVIDER_SETUP_ELIGIBILITY_FUTURE_GATED,
            PROVIDER_SETUP_BLOCKER_FUTURE_GATE,
            PROVIDER_READINESS_REASON_FUTURE_PROVIDER_GATED,
            PROVIDER_READINESS_PROVENANCE_RELEASE_SOURCE_TRUTH,
            PROVIDER_READINESS_CONFIG_STATE_LOCAL,
            CAPABILITY_PACK_ELIGIBILITY_FUTURE_GATED,
            CAPABILITY_PACK_MANIFEST_VALID_FUTURE_GATED,
            CAPABILITY_PACK_INSTALL_INTENT_FUTURE_GATED,
            PROVIDER_FUTURE_GATE_STATUS_SETUP_REQUIRED,
        ),
        "provider_not_ready": (
            PROVIDER_READINESS_STATE_DEGRADED,
            PROVIDER_SETUP_ELIGIBILITY_BLOCKED,
            PROVIDER_SETUP_BLOCKER_PROVIDER_NOT_READY,
            PROVIDER_READINESS_REASON_PROVIDER_NOT_READY,
            PROVIDER_READINESS_PROVENANCE_FUTURE_RUNTIME_CHECK,
            PROVIDER_READINESS_CONFIG_STATE_LOCAL,
            CAPABILITY_PACK_ELIGIBILITY_FUTURE_GATED,
            CAPABILITY_PACK_MANIFEST_VALID_FUTURE_GATED,
            CAPABILITY_PACK_INSTALL_INTENT_BLOCKED,
            PROVIDER_FUTURE_GATE_STATUS_EXECUTION_REQUIRED,
        ),
        "execution_gated": (
            PROVIDER_READINESS_STATE_PROVIDER_READY_EXECUTION_GATED,
            PROVIDER_SETUP_ELIGIBILITY_EXECUTION_GATED,
            PROVIDER_SETUP_BLOCKER_NONE,
            PROVIDER_READINESS_REASON_PROVIDER_READY_EXECUTION_GATED,
            PROVIDER_READINESS_PROVENANCE_FUTURE_RUNTIME_CHECK,
            PROVIDER_READINESS_CONFIG_STATE_LOCAL,
            CAPABILITY_PACK_ELIGIBILITY_FUTURE_GATED,
            CAPABILITY_PACK_MANIFEST_VALID_FUTURE_GATED,
            CAPABILITY_PACK_INSTALL_INTENT_NONE,
            PROVIDER_FUTURE_GATE_STATUS_EXECUTION_REQUIRED,
        ),
    }
    for label, expectation in readiness_expectations.items():
        readiness_payload = readiness_payloads[label]
        (
            expected_state,
            expected_eligibility,
            expected_blocker,
            expected_reason,
            expected_provenance,
            expected_config,
            expected_pack_eligibility,
            expected_manifest_validity,
            expected_install_intent,
            expected_future_gate,
        ) = expectation
        _require(
            readiness_payload["readinessStateSchemaVersion"] == PROVIDER_READINESS_STATE_SCHEMA_VERSION,
            f"{label} readiness fixture must publish provider readiness state schema",
            failures,
        )
        _require(
            readiness_payload["readinessConfigSchemaVersion"] == PROVIDER_READINESS_CONFIG_SCHEMA_VERSION,
            f"{label} readiness fixture must publish provider readiness config schema",
            failures,
        )
        _require(
            readiness_payload["providerReadinessState"] == expected_state,
            f"{label} readiness fixture must publish {expected_state}",
            failures,
        )
        _require(
            readiness_payload["setupEligibilityState"] == expected_eligibility,
            f"{label} readiness fixture must publish {expected_eligibility}",
            failures,
        )
        _require(
            readiness_payload["setupBlockerState"] == expected_blocker,
            f"{label} readiness fixture must publish setup blocker {expected_blocker}",
            failures,
        )
        _require(
            readiness_payload["readinessReasonCode"] == expected_reason,
            f"{label} readiness fixture must publish readiness reason {expected_reason}",
            failures,
        )
        _require(
            readiness_payload["readinessProvenance"] == expected_provenance,
            f"{label} readiness fixture must publish readiness provenance {expected_provenance}",
            failures,
        )
        _require(
            readiness_payload["readinessConfigState"] == expected_config,
            f"{label} readiness fixture must publish readiness config state {expected_config}",
            failures,
        )
        _require(
            readiness_payload["futureProviderGateStatus"] == expected_future_gate,
            f"{label} readiness fixture must publish future provider gate {expected_future_gate}",
            failures,
        )
        _require(
            readiness_payload["capabilityPackEligibilityState"] == expected_pack_eligibility,
            f"{label} readiness fixture must publish capability-pack eligibility {expected_pack_eligibility}",
            failures,
        )
        _require(
            readiness_payload["capabilityPackManifestValidityState"] == expected_manifest_validity,
            f"{label} readiness fixture must publish manifest validity {expected_manifest_validity}",
            failures,
        )
        _require(
            readiness_payload["installIntentState"] == expected_install_intent,
            f"{label} readiness fixture must publish install intent {expected_install_intent}",
            failures,
        )
        _require(readiness_payload["sentToProvider"] is False, f"{label} readiness fixture must send nothing", failures)
        _require(
            readiness_payload["canAcceptPrompts"] is False,
            f"{label} readiness fixture must keep prompts disabled",
            failures,
        )
        _require(
            readiness_payload["providerVisibleData"] == "none",
            f"{label} readiness fixture must keep provider-visible data as none",
            failures,
        )
        _require(
            readiness_payload["externalCalls"] == "blocked",
            f"{label} readiness fixture must keep external calls blocked",
            failures,
        )

    _require(
        default_activation_config_snapshot.schema_version == PROVIDER_ACTIVATION_CONFIG_SCHEMA_VERSION,
        "default activation config must expose provider activation config schema",
        failures,
    )
    _require(
        default_activation_config_snapshot.config_state == PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
        "default activation config must stay safe default local-only",
        failures,
    )

    activation_expectations = {
        "default": (
            PROVIDER_ACTIVATION_STATE_UNAVAILABLE,
            PROVIDER_ACTIVATION_ELIGIBILITY_UNAVAILABLE,
            PROVIDER_ACTIVATION_BLOCKER_READINESS_REQUIRED,
            PROVIDER_ACTIVATION_REASON_DEFAULT_UNAVAILABLE,
            PROVIDER_ACTIVATION_PROVENANCE_DEFAULT_CONFIG,
            PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "missing_config": (
            PROVIDER_ACTIVATION_STATE_DISABLED,
            PROVIDER_ACTIVATION_ELIGIBILITY_DISABLED,
            PROVIDER_ACTIVATION_BLOCKER_READINESS_REQUIRED,
            PROVIDER_ACTIVATION_REASON_CONFIG_MISSING_FAIL_CLOSED,
            PROVIDER_ACTIVATION_PROVENANCE_DEFAULT_CONFIG,
            PROVIDER_ACTIVATION_CONFIG_STATE_MISSING,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "invalid_config": (
            PROVIDER_ACTIVATION_STATE_DEGRADED,
            PROVIDER_ACTIVATION_ELIGIBILITY_BLOCKED,
            PROVIDER_ACTIVATION_BLOCKER_CONFIG_INVALID,
            PROVIDER_ACTIVATION_REASON_CONFIG_INVALID_FAIL_CLOSED,
            "local_config",
            PROVIDER_ACTIVATION_CONFIG_STATE_INVALID,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "readiness_blocked": (
            PROVIDER_ACTIVATION_STATE_BLOCKED_BY_READINESS,
            PROVIDER_ACTIVATION_ELIGIBILITY_BLOCKED,
            PROVIDER_ACTIVATION_BLOCKER_READINESS_REQUIRED,
            PROVIDER_ACTIVATION_REASON_READINESS_BLOCKED,
            PROVIDER_ACTIVATION_PROVENANCE_READINESS_STATE,
            PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "consent_blocked": (
            PROVIDER_ACTIVATION_STATE_BLOCKED_BY_CONSENT,
            PROVIDER_ACTIVATION_ELIGIBILITY_BLOCKED,
            PROVIDER_ACTIVATION_BLOCKER_CONSENT_REQUIRED,
            PROVIDER_ACTIVATION_REASON_CONSENT_REQUIRED,
            PROVIDER_ACTIVATION_PROVENANCE_CONSENT_STATE,
            PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "capability_blocked": (
            PROVIDER_ACTIVATION_STATE_BLOCKED_BY_CAPABILITY,
            PROVIDER_ACTIVATION_ELIGIBILITY_BLOCKED,
            PROVIDER_ACTIVATION_BLOCKER_CAPABILITY_REQUIRED,
            PROVIDER_ACTIVATION_REASON_CAPABILITY_REQUIRED,
            PROVIDER_ACTIVATION_PROVENANCE_READINESS_STATE,
            PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "manifest_blocked": (
            PROVIDER_ACTIVATION_STATE_BLOCKED_BY_MANIFEST,
            PROVIDER_ACTIVATION_ELIGIBILITY_BLOCKED,
            PROVIDER_ACTIVATION_BLOCKER_MANIFEST_REQUIRED,
            PROVIDER_ACTIVATION_REASON_MANIFEST_REQUIRED,
            PROVIDER_ACTIVATION_PROVENANCE_CAPABILITY_MANIFEST,
            PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "policy_blocked": (
            PROVIDER_ACTIVATION_STATE_BLOCKED_BY_POLICY,
            PROVIDER_ACTIVATION_ELIGIBILITY_BLOCKED,
            PROVIDER_ACTIVATION_BLOCKER_POLICY_BLOCKED,
            PROVIDER_ACTIVATION_REASON_POLICY_BLOCKED,
            PROVIDER_ACTIVATION_PROVENANCE_READINESS_STATE,
            PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "future_gated": (
            PROVIDER_ACTIVATION_STATE_ELIGIBLE_FUTURE_GATED,
            PROVIDER_ACTIVATION_ELIGIBILITY_FUTURE_GATED,
            PROVIDER_ACTIVATION_BLOCKER_FUTURE_ACTIVATION_GATE,
            PROVIDER_ACTIVATION_REASON_FUTURE_GATED,
            PROVIDER_ACTIVATION_PROVENANCE_RELEASE_SOURCE_TRUTH,
            PROVIDER_ACTIVATION_CONFIG_STATE_DEFAULT,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "adapter_unavailable": (
            PROVIDER_ACTIVATION_STATE_BLOCKED_BY_ADAPTER,
            PROVIDER_ACTIVATION_ELIGIBILITY_BLOCKED,
            PROVIDER_ACTIVATION_BLOCKER_ADAPTER_UNAVAILABLE,
            PROVIDER_ACTIVATION_REASON_ADAPTER_UNAVAILABLE,
            PROVIDER_ACTIVATION_PROVENANCE_ADAPTER_CONTRACT,
            PROVIDER_ACTIVATION_CONFIG_STATE_LOCAL,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_EXECUTION_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_UNAVAILABLE,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "execution_gated": (
            PROVIDER_ACTIVATION_STATE_READY_EXECUTION_GATED,
            PROVIDER_ACTIVATION_ELIGIBILITY_EXECUTION_GATED,
            PROVIDER_ACTIVATION_BLOCKER_EXECUTION_GATE,
            PROVIDER_ACTIVATION_REASON_EXECUTION_GATED,
            PROVIDER_ACTIVATION_PROVENANCE_FUTURE_RUNTIME_CHECK,
            PROVIDER_ACTIVATION_CONFIG_STATE_LOCAL,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_EXECUTION_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_READY_FUTURE_GATED,
            FUNCTIONAL_AI_CRITERIA_PENDING,
            V18_PREBETA_READINESS_PENDING,
        ),
        "functional_future_version": (
            PROVIDER_ACTIVATION_STATE_FUNCTIONAL_AI_READY_FUTURE_VERSION,
            PROVIDER_ACTIVATION_ELIGIBILITY_FUTURE_VERSION,
            PROVIDER_ACTIVATION_BLOCKER_VERSION_JUMP_REQUIRED,
            PROVIDER_ACTIVATION_REASON_FUNCTIONAL_AI_FUTURE_VERSION,
            PROVIDER_ACTIVATION_PROVENANCE_FUTURE_RUNTIME_CHECK,
            PROVIDER_ACTIVATION_CONFIG_STATE_LOCAL,
            PROVIDER_FUTURE_ACTIVATION_GATE_STATUS_VERSION_JUMP_REQUIRED,
            PROVIDER_ADAPTER_AVAILABILITY_READY_FUTURE_GATED,
            FUNCTIONAL_AI_CRITERIA_READY_FUTURE_VERSION,
            V18_PREBETA_READINESS_READY,
        ),
    }
    for label, expectation in activation_expectations.items():
        activation_payload = activation_payloads[label]
        (
            expected_state,
            expected_eligibility,
            expected_blocker,
            expected_reason,
            expected_provenance,
            expected_config,
            expected_future_gate,
            expected_adapter_availability,
            expected_functional_ai,
            expected_v18_readiness,
        ) = expectation
        _require(
            activation_payload["activationStateSchemaVersion"] == PROVIDER_ACTIVATION_STATE_SCHEMA_VERSION,
            f"{label} activation fixture must publish provider activation state schema",
            failures,
        )
        _require(
            activation_payload["activationConfigSchemaVersion"] == PROVIDER_ACTIVATION_CONFIG_SCHEMA_VERSION,
            f"{label} activation fixture must publish provider activation config schema",
            failures,
        )
        _require(
            activation_payload["providerActivationState"] == expected_state,
            f"{label} activation fixture must publish {expected_state}",
            failures,
        )
        _require(
            activation_payload["activationEligibilityState"] == expected_eligibility,
            f"{label} activation fixture must publish activation eligibility {expected_eligibility}",
            failures,
        )
        _require(
            activation_payload["activationBlockerState"] == expected_blocker,
            f"{label} activation fixture must publish activation blocker {expected_blocker}",
            failures,
        )
        _require(
            activation_payload["activationReasonCode"] == expected_reason,
            f"{label} activation fixture must publish activation reason {expected_reason}",
            failures,
        )
        _require(
            activation_payload["activationProvenance"] == expected_provenance,
            f"{label} activation fixture must publish activation provenance {expected_provenance}",
            failures,
        )
        _require(
            activation_payload["activationConfigState"] == expected_config,
            f"{label} activation fixture must publish activation config {expected_config}",
            failures,
        )
        _require(
            activation_payload["futureActivationGateStatus"] == expected_future_gate,
            f"{label} activation fixture must publish future activation gate {expected_future_gate}",
            failures,
        )
        _require(
            activation_payload["providerAdapterPosture"] == PROVIDER_ADAPTER_POSTURE_NULL_LOCAL,
            f"{label} activation fixture must keep null/local adapter posture",
            failures,
        )
        _require(
            activation_payload["providerAdapterAvailabilityState"] == expected_adapter_availability,
            f"{label} activation fixture must publish adapter availability {expected_adapter_availability}",
            failures,
        )
        _require(
            activation_payload["providerAdapterExecutionPosture"] == PROVIDER_ADAPTER_EXECUTION_POSTURE_DISABLED,
            f"{label} activation fixture must keep adapter execution disabled",
            failures,
        )
        _require(
            activation_payload["providerMetadataContractVersion"] == PROVIDER_METADATA_CONTRACT_VERSION,
            f"{label} activation fixture must publish provider metadata contract",
            failures,
        )
        _require(
            activation_payload["providerConfigEnvelopeVersion"] == PROVIDER_CONFIG_ENVELOPE_VERSION,
            f"{label} activation fixture must publish provider config envelope",
            failures,
        )
        _require(
            activation_payload["providerActivationHandoffState"] == PROVIDER_ACTIVATION_HANDOFF_STATE_FUTURE_GATED,
            f"{label} activation fixture must keep provider activation handoff future-gated",
            failures,
        )
        _require(
            activation_payload["futureSdkIntegrationBoundary"] == PROVIDER_SDK_INTEGRATION_BOUNDARY_FUTURE_APPROVAL,
            f"{label} activation fixture must keep SDK integration future-approved",
            failures,
        )
        _require(
            activation_payload["promptExecutionGateState"] == PROMPT_EXECUTION_GATE_DISABLED
            and activation_payload["modelExecutionGateState"] == MODEL_EXECUTION_GATE_DISABLED
            and activation_payload["providerExecutionGateState"] == PROVIDER_EXECUTION_GATE_DISABLED,
            f"{label} activation fixture must keep prompt/model/provider execution gates disabled",
            failures,
        )
        _require(
            activation_payload["functionalAiCriteriaState"] == expected_functional_ai,
            f"{label} activation fixture must publish functional-AI criteria {expected_functional_ai}",
            failures,
        )
        _require(
            activation_payload["v18PrebetaReadinessState"] == expected_v18_readiness,
            f"{label} activation fixture must publish v1.8.0 readiness {expected_v18_readiness}",
            failures,
        )
        if expected_adapter_availability == PROVIDER_ADAPTER_AVAILABILITY_READY_FUTURE_GATED:
            _require(
                activation_payload["readinessGateState"] == READINESS_GATE_READY
                and activation_payload["consentGateState"] == CONSENT_GATE_READY
                and activation_payload["capabilityGateState"] == CAPABILITY_GATE_READY
                and activation_payload["manifestGateState"] == MANIFEST_GATE_READY
                and activation_payload["adapterGateState"] == ADAPTER_GATE_READY_FUTURE_GATED
                and activation_payload["safetyEvalGateState"] == SAFETY_EVAL_GATE_READY,
                f"{label} activation fixture must show future-gated readiness/adapter/safety gates when eligible",
                failures,
            )
        _require(activation_payload["sentToProvider"] is False, f"{label} activation fixture must send nothing", failures)
        _require(
            activation_payload["canAcceptPrompts"] is False,
            f"{label} activation fixture must keep prompts disabled",
            failures,
        )
        _require(
            activation_payload["providerVisibleData"] == "none",
            f"{label} activation fixture must keep provider-visible data as none",
            failures,
        )
        _require(
            activation_payload["externalCalls"] == "blocked",
            f"{label} activation fixture must keep external calls blocked",
            failures,
        )
        _require(
            activation_payload["capabilityPackDownloadState"] == CAPABILITY_PACK_DOWNLOADS_BLOCKED
            and activation_payload["capabilityPackInstallState"] == CAPABILITY_PACK_INSTALL_BLOCKED,
            f"{label} activation fixture must keep capability-pack download/install blocked",
            failures,
        )
        _require(
            activation_payload["memoryIndexingState"] == MEMORY_INDEXING_DISABLED
            and activation_payload["networkEgressState"] == NETWORK_EGRESS_BLOCKED,
            f"{label} activation fixture must keep memory indexing and network egress blocked",
            failures,
        )

    _require(
        default_execution_config_snapshot.schema_version == PROVIDER_EXECUTION_READINESS_CONFIG_SCHEMA_VERSION,
        "default execution-readiness config must expose provider execution-readiness config schema",
        failures,
    )
    _require(
        default_execution_config_snapshot.config_state == PROVIDER_EXECUTION_CONFIG_STATE_DEFAULT,
        "default execution-readiness config must stay safe default local-only",
        failures,
    )
    execution_expectations = {
        "default": (
            PROVIDER_EXECUTION_READINESS_STATE_UNAVAILABLE,
            PROVIDER_EXECUTION_ELIGIBILITY_UNAVAILABLE,
            PROVIDER_EXECUTION_BLOCKER_ACTIVATION_REQUIRED,
            PROVIDER_EXECUTION_REASON_DEFAULT_UNAVAILABLE,
            PROVIDER_EXECUTION_PROVENANCE_ACTIVATION_STATE,
            PROVIDER_EXECUTION_CONFIG_STATE_DEFAULT,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_NOT_SELECTED,
            ADAPTER_SELECTION_POSTURE_NULL_LOCAL,
            PROMPT_ACCEPTANCE_GATE_DISABLED,
            PROMPT_ROUTING_GATE_DISABLED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "missing_config": (
            PROVIDER_EXECUTION_READINESS_STATE_DISABLED,
            PROVIDER_EXECUTION_ELIGIBILITY_DISABLED,
            PROVIDER_EXECUTION_BLOCKER_ACTIVATION_REQUIRED,
            PROVIDER_EXECUTION_REASON_CONFIG_MISSING_FAIL_CLOSED,
            PROVIDER_EXECUTION_PROVENANCE_DEFAULT_CONFIG,
            PROVIDER_EXECUTION_CONFIG_STATE_MISSING,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_NOT_SELECTED,
            ADAPTER_SELECTION_POSTURE_NULL_LOCAL,
            PROMPT_ACCEPTANCE_GATE_DISABLED,
            PROMPT_ROUTING_GATE_DISABLED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "invalid_config": (
            PROVIDER_EXECUTION_READINESS_STATE_DEGRADED,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_CONFIG_INVALID,
            PROVIDER_EXECUTION_REASON_CONFIG_INVALID_FAIL_CLOSED,
            PROVIDER_EXECUTION_PROVENANCE_LOCAL_CONFIG,
            PROVIDER_EXECUTION_CONFIG_STATE_INVALID,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_NOT_SELECTED,
            ADAPTER_SELECTION_POSTURE_NULL_LOCAL,
            PROMPT_ACCEPTANCE_GATE_DISABLED,
            PROMPT_ROUTING_GATE_DISABLED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "activation_blocked": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_ACTIVATION,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_ACTIVATION_REQUIRED,
            PROVIDER_EXECUTION_REASON_ACTIVATION_BLOCKED,
            PROVIDER_EXECUTION_PROVENANCE_ACTIVATION_STATE,
            PROVIDER_EXECUTION_CONFIG_STATE_DEFAULT,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_NOT_SELECTED,
            ADAPTER_SELECTION_POSTURE_NULL_LOCAL,
            PROMPT_ACCEPTANCE_GATE_DISABLED,
            PROMPT_ROUTING_GATE_DISABLED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "future_gated": (
            PROVIDER_EXECUTION_READINESS_STATE_READY_FUTURE_GATED,
            PROVIDER_EXECUTION_ELIGIBILITY_FUTURE_GATED,
            PROVIDER_EXECUTION_BLOCKER_FUTURE_EXECUTION_GATE,
            PROVIDER_EXECUTION_REASON_FUTURE_GATED,
            PROVIDER_EXECUTION_PROVENANCE_ACTIVATION_STATE,
            PROVIDER_EXECUTION_CONFIG_STATE_DEFAULT,
            PROVIDER_EXECUTION_APPROVAL_STATUS_FUTURE_GATED,
            PROVIDER_PATH_STATUS_NOT_SELECTED,
            ADAPTER_SELECTION_POSTURE_NULL_LOCAL,
            PROMPT_ACCEPTANCE_GATE_DISABLED,
            PROMPT_ROUTING_GATE_DISABLED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "provider_path_missing": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_PROVIDER_PATH,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_PROVIDER_PATH_REQUIRED,
            PROVIDER_EXECUTION_REASON_PROVIDER_PATH_MISSING,
            PROVIDER_EXECUTION_PROVENANCE_PROVIDER_PATH_CONTRACT,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_NOT_SELECTED,
            ADAPTER_SELECTION_POSTURE_NULL_LOCAL,
            PROMPT_ACCEPTANCE_GATE_DISABLED,
            PROMPT_ROUTING_GATE_DISABLED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "adapter_unavailable": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_ADAPTER,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_ADAPTER_REQUIRED,
            PROVIDER_EXECUTION_REASON_ADAPTER_UNAVAILABLE,
            PROVIDER_EXECUTION_PROVENANCE_ADAPTER_CONTRACT,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_NULL_LOCAL,
            PROMPT_ACCEPTANCE_GATE_DISABLED,
            PROMPT_ROUTING_GATE_DISABLED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "prompt_gate_blocked": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_PROMPT_GATE,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_PROMPT_GATE,
            PROVIDER_EXECUTION_REASON_PROMPT_GATE_BLOCKED,
            PROVIDER_EXECUTION_PROVENANCE_PROMPT_GATE,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
            PROMPT_ACCEPTANCE_GATE_DISABLED,
            PROMPT_ROUTING_GATE_DISABLED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "model_gate_blocked": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_MODEL_GATE,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_MODEL_GATE,
            PROVIDER_EXECUTION_REASON_MODEL_GATE_BLOCKED,
            PROVIDER_EXECUTION_PROVENANCE_MODEL_GATE,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
            PROMPT_ACCEPTANCE_GATE_FUTURE_GATED,
            PROMPT_ROUTING_GATE_FUTURE_GATED,
            MODEL_EXECUTION_STATUS_DISABLED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "consent_blocked": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_CONSENT,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_CONSENT_REQUIRED,
            PROVIDER_EXECUTION_REASON_CONSENT_REQUIRED,
            PROVIDER_EXECUTION_PROVENANCE_CONSENT_STATE,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
            PROMPT_ACCEPTANCE_GATE_FUTURE_GATED,
            PROMPT_ROUTING_GATE_FUTURE_GATED,
            MODEL_EXECUTION_STATUS_FUTURE_GATED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "safety_blocked": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_SAFETY,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_SAFETY_EVAL_REQUIRED,
            PROVIDER_EXECUTION_REASON_SAFETY_EVAL_REQUIRED,
            PROVIDER_EXECUTION_PROVENANCE_SAFETY_EVAL,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
            PROMPT_ACCEPTANCE_GATE_FUTURE_GATED,
            PROMPT_ROUTING_GATE_FUTURE_GATED,
            MODEL_EXECUTION_STATUS_FUTURE_GATED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "network_blocked": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_NETWORK,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_NETWORK_APPROVAL_REQUIRED,
            PROVIDER_EXECUTION_REASON_NETWORK_BLOCKED,
            PROVIDER_EXECUTION_PROVENANCE_NETWORK_POLICY,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
            PROMPT_ACCEPTANCE_GATE_FUTURE_GATED,
            PROMPT_ROUTING_GATE_FUTURE_GATED,
            MODEL_EXECUTION_STATUS_FUTURE_GATED,
            EXTERNAL_CALL_READINESS_BLOCKED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "policy_blocked": (
            PROVIDER_EXECUTION_READINESS_STATE_BLOCKED_BY_POLICY,
            PROVIDER_EXECUTION_ELIGIBILITY_BLOCKED,
            PROVIDER_EXECUTION_BLOCKER_POLICY_BLOCKED,
            PROVIDER_EXECUTION_REASON_POLICY_BLOCKED,
            PROVIDER_EXECUTION_PROVENANCE_RELEASE_SOURCE_TRUTH,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
            PROMPT_ACCEPTANCE_GATE_FUTURE_GATED,
            PROMPT_ROUTING_GATE_FUTURE_GATED,
            MODEL_EXECUTION_STATUS_FUTURE_GATED,
            EXTERNAL_CALL_READINESS_FUTURE_GATED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "approval_missing": (
            PROVIDER_EXECUTION_READINESS_STATE_READY_BUT_NOT_APPROVED,
            PROVIDER_EXECUTION_ELIGIBILITY_READY_NOT_APPROVED,
            PROVIDER_EXECUTION_BLOCKER_APPROVAL_REQUIRED,
            PROVIDER_EXECUTION_REASON_APPROVAL_MISSING,
            PROVIDER_EXECUTION_PROVENANCE_FUTURE_RUNTIME_CHECK,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_MISSING,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
            PROMPT_ACCEPTANCE_GATE_FUTURE_GATED,
            PROMPT_ROUTING_GATE_FUTURE_GATED,
            MODEL_EXECUTION_STATUS_FUTURE_GATED,
            EXTERNAL_CALL_READINESS_FUTURE_GATED,
            FUNCTIONAL_AI_RELEASE_GATE_PENDING,
            V18_RELEASE_GATE_PENDING_FUNCTIONAL_AI,
        ),
        "functional_future_version": (
            PROVIDER_EXECUTION_READINESS_STATE_FUNCTIONAL_AI_READY_FUTURE_VERSION,
            PROVIDER_EXECUTION_ELIGIBILITY_FUTURE_VERSION,
            PROVIDER_EXECUTION_BLOCKER_VERSION_JUMP_REQUIRED,
            PROVIDER_EXECUTION_REASON_FUNCTIONAL_AI_FUTURE_VERSION,
            PROVIDER_EXECUTION_PROVENANCE_FUTURE_RUNTIME_CHECK,
            PROVIDER_EXECUTION_CONFIG_STATE_LOCAL,
            PROVIDER_EXECUTION_APPROVAL_STATUS_GRANTED_FOR_PROOF,
            PROVIDER_PATH_STATUS_SELECTED_FUTURE_GATED,
            ADAPTER_SELECTION_POSTURE_READY_FUTURE_GATED,
            PROMPT_ACCEPTANCE_GATE_FUTURE_GATED,
            PROMPT_ROUTING_GATE_FUTURE_GATED,
            MODEL_EXECUTION_STATUS_FUTURE_GATED,
            EXTERNAL_CALL_READINESS_FUTURE_GATED,
            FUNCTIONAL_AI_RELEASE_GATE_READY_FUTURE_VERSION,
            V18_RELEASE_GATE_READY_FUTURE_VERSION,
        ),
    }
    for label, expectation in execution_expectations.items():
        execution_payload = execution_payloads[label]
        (
            expected_state,
            expected_eligibility,
            expected_blocker,
            expected_reason,
            expected_provenance,
            expected_config,
            expected_approval,
            expected_provider_path,
            expected_adapter_selection,
            expected_prompt_acceptance,
            expected_prompt_routing,
            expected_model_status,
            expected_external_call_readiness,
            expected_functional_release_gate,
            expected_v18_release_gate,
        ) = expectation
        _require(
            execution_payload["stateId"] == FAM007_EXECUTION_READINESS_STATE_ID,
            f"{label} execution fixture must use execution-readiness state id",
            failures,
        )
        _require(
            execution_payload["mode"] == FAM007_EXECUTION_READINESS_MODE,
            f"{label} execution fixture must use execution-readiness mode",
            failures,
        )
        _require(
            execution_payload["executionStateSchemaVersion"] == PROVIDER_EXECUTION_READINESS_STATE_SCHEMA_VERSION,
            f"{label} execution fixture must publish execution-readiness state schema",
            failures,
        )
        _require(
            execution_payload["executionConfigSchemaVersion"] == PROVIDER_EXECUTION_READINESS_CONFIG_SCHEMA_VERSION,
            f"{label} execution fixture must publish execution-readiness config schema",
            failures,
        )
        _require(
            execution_payload["providerExecutionReadinessState"] == expected_state,
            f"{label} execution fixture must publish {expected_state}",
            failures,
        )
        _require(
            execution_payload["executionEligibilityState"] == expected_eligibility,
            f"{label} execution fixture must publish execution eligibility {expected_eligibility}",
            failures,
        )
        _require(
            execution_payload["executionBlockerState"] == expected_blocker,
            f"{label} execution fixture must publish execution blocker {expected_blocker}",
            failures,
        )
        _require(
            execution_payload["executionReasonCode"] == expected_reason,
            f"{label} execution fixture must publish execution reason {expected_reason}",
            failures,
        )
        _require(
            execution_payload["executionProvenance"] == expected_provenance,
            f"{label} execution fixture must publish execution provenance {expected_provenance}",
            failures,
        )
        _require(
            execution_payload["executionConfigState"] == expected_config,
            f"{label} execution fixture must publish execution config {expected_config}",
            failures,
        )
        _require(
            execution_payload["executionApprovalStatus"] == expected_approval,
            f"{label} execution fixture must publish execution approval {expected_approval}",
            failures,
        )
        _require(
            execution_payload["providerPathStatus"] == expected_provider_path,
            f"{label} execution fixture must publish provider path {expected_provider_path}",
            failures,
        )
        _require(
            execution_payload["adapterSelectionPosture"] == expected_adapter_selection,
            f"{label} execution fixture must publish adapter selection {expected_adapter_selection}",
            failures,
        )
        _require(
            execution_payload["promptAcceptanceGateState"] == expected_prompt_acceptance,
            f"{label} execution fixture must publish prompt acceptance {expected_prompt_acceptance}",
            failures,
        )
        _require(
            execution_payload["promptRoutingGateState"] == expected_prompt_routing,
            f"{label} execution fixture must publish prompt routing {expected_prompt_routing}",
            failures,
        )
        _require(
            execution_payload["promptSendPosture"] == PROMPT_SEND_POSTURE_DISABLED,
            f"{label} execution fixture must keep prompt sends disabled",
            failures,
        )
        _require(
            execution_payload["modelExecutionStatus"] == expected_model_status,
            f"{label} execution fixture must publish model execution status {expected_model_status}",
            failures,
        )
        expected_model_workload = (
            MODEL_WORKLOAD_READINESS_FUTURE_GATED
            if expected_model_status == MODEL_EXECUTION_STATUS_FUTURE_GATED
            else MODEL_WORKLOAD_READINESS_DISABLED
        )
        _require(
            execution_payload["modelWorkloadReadinessPosture"] == expected_model_workload,
            f"{label} execution fixture must publish model workload readiness {expected_model_workload}",
            failures,
        )
        expected_visible_data = (
            PROVIDER_VISIBLE_DATA_EXECUTION_FUTURE_GATED
            if label in {"approval_missing", "functional_future_version"}
            else PROVIDER_VISIBLE_DATA_EXECUTION_NONE
        )
        _require(
            execution_payload["providerVisibleDataExecutionPosture"] == expected_visible_data,
            f"{label} execution fixture must publish provider-visible execution data posture",
            failures,
        )
        _require(
            execution_payload["externalCallReadinessState"] == expected_external_call_readiness,
            f"{label} execution fixture must publish external call readiness {expected_external_call_readiness}",
            failures,
        )
        _require(
            execution_payload["functionalAiReleaseGateState"] == expected_functional_release_gate,
            f"{label} execution fixture must publish functional-AI release gate",
            failures,
        )
        _require(
            execution_payload["v18ReleaseGateState"] == expected_v18_release_gate,
            f"{label} execution fixture must publish v1.8.0 release gate",
            failures,
        )
        _require(execution_payload["sentToProvider"] is False, f"{label} execution fixture must send nothing", failures)
        _require(
            execution_payload["canAcceptPrompts"] is False,
            f"{label} execution fixture must keep prompts disabled",
            failures,
        )
        _require(
            execution_payload["providerVisibleData"] == "none",
            f"{label} execution fixture must keep provider-visible data as none",
            failures,
        )
        _require(
            execution_payload["promptExecutionGateState"] == PROMPT_EXECUTION_GATE_DISABLED
            and execution_payload["modelExecutionGateState"] == MODEL_EXECUTION_GATE_DISABLED
            and execution_payload["providerExecutionGateState"] == PROVIDER_EXECUTION_GATE_DISABLED,
            f"{label} execution fixture must keep prompt/model/provider execution gates disabled",
            failures,
        )
        _require(
            execution_payload["externalCalls"] == "blocked",
            f"{label} execution fixture must keep external calls blocked",
            failures,
        )
        _require(
            execution_payload["memoryIndexingState"] == MEMORY_INDEXING_DISABLED
            and execution_payload["networkEgressState"] == NETWORK_EGRESS_BLOCKED,
            f"{label} execution fixture must keep memory indexing and network egress blocked",
            failures,
        )

    default_permissions = readiness_payloads["default"]["actionPermissionMatrix"]
    _require(
        len(default_permissions) == 9,
        "default readiness fixture must publish the full action-permission matrix",
        failures,
    )
    _require(
        all(item["permission"] == READINESS_ACTION_ALLOWED_LOCAL_READ_ONLY for item in default_permissions[:6]),
        "view readiness actions must be local read-only allowed",
        failures,
    )
    _require(
        all(item["permission"] == READINESS_ACTION_FUTURE_USER_APPROVAL_REQUIRED for item in default_permissions[6:]),
        "future consent/setup/execution actions must require USER approval",
        failures,
    )

    expected_foundation_slices = (
        SLC_017_ID,
        SLC_018_ID,
        SLC_031_ID,
        SLC_032_ID,
        SLC_033_ID,
        SLC_034_ID,
        SLC_035_ID,
        SLC_036_ID,
    )
    _require(
        foundation_snapshot.state_id == FAM007_FOUNDATION_READINESS_STATE_ID,
        "foundation readiness scaffold must use the admitted FAM-007 readiness state id",
        failures,
    )
    _require(
        foundation_snapshot.slice_ids == expected_foundation_slices,
        "foundation readiness scaffold must carry every admitted branch-material slice",
        failures,
    )
    _require(
        foundation_snapshot.mode == FAM007_FOUNDATION_READINESS_MODE,
        "foundation readiness scaffold must use foundation-readiness mode",
        failures,
    )
    _require(
        foundation_payload["selectedProviderId"] == NO_PROVIDER_ID,
        "foundation readiness scaffold must keep no-provider selected",
        failures,
    )
    _require(
        foundation_payload["providerConfigurationState"] == PROVIDER_CONFIGURATION_UNCONFIGURED,
        "foundation readiness scaffold must keep provider configuration unconfigured",
        failures,
    )
    _require(
        foundation_payload["providerRegistryState"] == LOCAL_PROVIDER_REGISTRY_STATE,
        "foundation readiness scaffold must preserve local-only registry posture",
        failures,
    )
    _require(
        foundation_payload["hardwareCapabilityState"] == LOCAL_HARDWARE_CAPABILITY_STATE,
        "foundation readiness scaffold must expose local-only hardware planning state",
        failures,
    )
    _require(
        foundation_payload["gpuCapabilityState"] == "gpu-unprobed",
        "foundation readiness scaffold must not claim GPU capability proof",
        failures,
    )
    _require(
        foundation_payload["cpuFallbackState"] == "cpu-fallback-preserved",
        "foundation readiness scaffold must preserve CPU fallback",
        failures,
    )
    _require(
        foundation_payload["modelWorkloadState"] == "model-workload-disabled",
        "foundation readiness scaffold must keep model workloads disabled",
        failures,
    )
    _require(
        foundation_payload["hardwareDetectionLevel"] == HARDWARE_DETECTION_LEVEL_1,
        "foundation readiness scaffold must expose Level 1 safe local static snapshot",
        failures,
    )
    _require(
        foundation_payload["capabilitySnapshotPolicy"] == "local-static-no-heavy-probe",
        "foundation readiness scaffold must prohibit heavy capability probes",
        failures,
    )
    _require(
        foundation_payload["ramReadinessState"] == RAM_READINESS_UNPROBED,
        "foundation readiness scaffold must keep RAM readiness unprobed",
        failures,
    )
    _require(
        foundation_payload["diskReadinessState"] == DISK_READINESS_UNPROBED,
        "foundation readiness scaffold must keep disk readiness unprobed",
        failures,
    )
    _require(
        foundation_payload["modelWorkloadMetadataState"] == MODEL_WORKLOAD_METADATA_PLANNED,
        "foundation readiness scaffold must plan model workload metadata without execution",
        failures,
    )
    _require(
        foundation_payload["gpuCapabilityLabel"] == "GPU acceleration: unprobed; no model workload active",
        "foundation readiness scaffold must visibly disclose GPU unprobed/no-workload posture",
        failures,
    )
    _require(
        foundation_payload["cpuFallbackLabel"] == "CPU fallback: preserved",
        "foundation readiness scaffold must visibly disclose CPU fallback posture",
        failures,
    )
    _require(
        foundation_payload["powerStateLabel"] == "Power state: not evaluated",
        "foundation readiness scaffold must keep power state unclaimed",
        failures,
    )
    _require(
        foundation_payload["thermalGuardrailLabel"] == "Thermal guardrails required before model workloads",
        "foundation readiness scaffold must visibly disclose thermal guardrails",
        failures,
    )
    _require(
        foundation_payload["capabilityPackLifecycleState"] == CAPABILITY_PACK_LIFECYCLE_PLANNED,
        "foundation readiness scaffold must expose capability-pack lifecycle planning state",
        failures,
    )
    _require(
        foundation_payload["capabilityPackDownloadState"] == CAPABILITY_PACK_DOWNLOADS_BLOCKED,
        "foundation readiness scaffold must block capability-pack downloads",
        failures,
    )
    _require(
        foundation_payload["capabilityPackManifestSchemaVersion"] == CAPABILITY_PACK_MANIFEST_SCHEMA_VERSION,
        "foundation readiness scaffold must expose capability-pack manifest schema version",
        failures,
    )
    _require(
        foundation_payload["capabilityPackManifestState"] == CAPABILITY_PACK_MANIFEST_PLANNED,
        "foundation readiness scaffold must keep manifest state planning-only",
        failures,
    )
    _require(
        foundation_payload["capabilityPackSourceType"] == CAPABILITY_PACK_SOURCE_LOCAL_ONLY,
        "foundation readiness scaffold must keep capability-pack source local/future-gated",
        failures,
    )
    _require(
        foundation_payload["capabilityPackChecksumState"] == CAPABILITY_PACK_CHECKSUM_REQUIRED,
        "foundation readiness scaffold must require checksums before install",
        failures,
    )
    _require(
        foundation_payload["capabilityPackSignatureState"] == CAPABILITY_PACK_SIGNATURE_REQUIRED,
        "foundation readiness scaffold must require signatures before install",
        failures,
    )
    _require(
        foundation_payload["capabilityPackCompatibilityState"] == CAPABILITY_PACK_COMPATIBILITY_UNPROVEN,
        "foundation readiness scaffold must keep compatibility unproven",
        failures,
    )
    _require(
        foundation_payload["capabilityPackInstallState"] == CAPABILITY_PACK_INSTALL_BLOCKED
        and foundation_payload["capabilityPackUpdateState"] == CAPABILITY_PACK_UPDATE_BLOCKED
        and foundation_payload["capabilityPackUninstallState"] == CAPABILITY_PACK_UNINSTALL_BLOCKED,
        "foundation readiness scaffold must block install/update/uninstall execution",
        failures,
    )
    _require(
        foundation_payload["capabilityPackDownloadLabel"] == "Capability pack downloads: blocked",
        "foundation readiness scaffold must visibly disclose blocked capability-pack downloads",
        failures,
    )
    _require(
        foundation_payload["memoryContextState"] == MEMORY_CONTEXT_DISABLED,
        "foundation readiness scaffold must keep memory/context disabled",
        failures,
    )
    _require(
        foundation_payload["dataClassificationSchemaVersion"] == DATA_CLASSIFICATION_SCHEMA_VERSION,
        "foundation readiness scaffold must expose data classification schema version",
        failures,
    )
    _require(
        foundation_payload["providerVisibleDataGuarantee"] == PROVIDER_VISIBLE_DATA_GUARANTEE_NONE,
        "foundation readiness scaffold must guarantee no provider-visible data",
        failures,
    )
    _require(
        foundation_payload["memoryIndexingState"] == MEMORY_INDEXING_DISABLED
        and foundation_payload["retrievalState"] == RETRIEVAL_DISABLED
        and foundation_payload["learningState"] == LEARNING_DISABLED
        and foundation_payload["persistenceState"] == PERSISTENCE_DISABLED,
        "foundation readiness scaffold must keep memory indexing, retrieval, learning, and persistence disabled",
        failures,
    )
    _require(
        foundation_payload["consentEnvelopeState"] == CONSENT_ENVELOPE_REQUIRED
        and foundation_payload["auditEnvelopeState"] == AUDIT_ENVELOPE_PLANNED,
        "foundation readiness scaffold must expose consent and audit envelope posture",
        failures,
    )
    _require(
        foundation_payload["secretBoundaryState"] == SECRET_BOUNDARY_NO_SECRETS,
        "foundation readiness scaffold must keep secret boundary at no stored secrets",
        failures,
    )
    _require(
        foundation_payload["networkEgressState"] == NETWORK_EGRESS_BLOCKED,
        "foundation readiness scaffold must block network egress",
        failures,
    )
    _require(
        foundation_payload["windowsResilienceState"] == WINDOWS_RESILIENCE_PLANNED,
        "foundation readiness scaffold must expose Windows resilience planning state",
        failures,
    )
    _require(
        foundation_payload["personaCoreVoiceState"] == PERSONA_CORE_VOICE_BOUNDARY_PLANNED,
        "foundation readiness scaffold must expose persona/Core/voice planning boundary",
        failures,
    )
    _require(
        foundation_payload["voiceRuntimeState"] == "voice-runtime-disabled",
        "foundation readiness scaffold must keep voice runtime disabled",
        failures,
    )
    _require(
        foundation_payload["validationProofGateState"] == VALIDATION_PROOF_GATES_PLANNED,
        "foundation readiness scaffold must expose validation proof gates",
        failures,
    )
    _require(
        foundation_payload["coreDesktopCopyContractVersion"] == CORE_DESKTOP_COPY_CONTRACT_VERSION,
        "foundation readiness scaffold must expose Core/Desktop copy contract version",
        failures,
    )
    _require(
        foundation_payload["coreDesktopRuntimeStateContract"] == CORE_DESKTOP_RUNTIME_STATE_CONTRACT,
        "foundation readiness scaffold must expose Core/Desktop runtime-state contract",
        failures,
    )
    _require(
        foundation_payload["disabledPromptBehaviorContract"] == DISABLED_PROMPT_BEHAVIOR_CONTRACT,
        "foundation readiness scaffold must expose disabled prompt/provider behavior contract",
        failures,
    )
    _require(
        foundation_payload["goldenProviderStateFixtures"] == GOLDEN_PROVIDER_STATE_FIXTURES
        and foundation_payload["validatorExpansionState"] == VALIDATOR_EXPANSION_ACTIVE,
        "foundation readiness scaffold must expose golden fixtures and validator expansion state",
        failures,
    )
    _require(
        foundation_payload["contractReadyMarker"] == CONTRACT_READY_MARKER
        and foundation_payload["uiReadyMarker"] == UI_READY_MARKER
        and foundation_payload["validatorReadyMarker"] == VALIDATOR_READY_MARKER
        and foundation_payload["futureImplementationGatedMarker"] == FUTURE_IMPLEMENTATION_GATED_MARKER,
        "foundation readiness scaffold must expose contract/UI/validator-ready and future-gated markers",
        failures,
    )
    _require(foundation_payload["sentToProvider"] is False, "foundation readiness scaffold must send nothing to providers", failures)
    _require(foundation_payload["storedLocally"] is False, "foundation readiness scaffold must not persist local memory", failures)
    _require(foundation_payload["canAcceptPrompts"] is False, "foundation readiness scaffold must not accept prompts", failures)
    _require(foundation_payload["externalCalls"] == "blocked", "foundation readiness scaffold must block external calls", failures)
    _require(
        foundation_payload["providerVisibleData"] == "none",
        "foundation readiness scaffold must expose no provider-visible data",
        failures,
    )
    _require(
        foundation_payload["providerInteractionState"] == PROVIDER_BOUNDARY_INTERACTION_PLAN_STATE,
        "foundation readiness scaffold must expose provider-boundary interaction plan state",
        failures,
    )
    _require(
        len(foundation_payload["foundationReadiness"]) == len(expected_foundation_slices),
        "foundation readiness scaffold must publish one readiness item per admitted slice",
        failures,
    )

    for forbidden in ("openai", "anthropic", "ollama", "llama_cpp", "pynvml", "cuda"):
        _require(
            forbidden not in _read("desktop/ai_provider_state.py").casefold(),
            f"no-provider scaffold must not import or name provider/runtime dependency {forbidden}",
            failures,
        )

    for needle in (
        "build_provider_execution_readiness_gates_state",
        "_publish_ai_provider_state_to_page",
        "AI_PROVIDER_STATE_READY",
        "window.setAIProviderState",
        "provider_interaction",
        "provider_next_action",
        "runtime_category",
        "runtime_reason",
        "runtime_provenance",
        "runtime_schema",
        "runtime_config",
        "runtime_fail_closed",
        "provider_readiness",
        "setup_eligibility",
        "setup_blocker",
        "readiness_reason",
        "readiness_provenance",
        "readiness_schema",
        "future_provider_gate",
        "provider_activation",
        "activation_eligibility",
        "activation_blocker",
        "activation_reason",
        "activation_provenance",
        "activation_schema",
        "future_activation_gate",
        "provider_adapter",
        "prompt_execution_gate",
        "model_execution_gate",
        "provider_execution_gate",
        "functional_ai_criteria",
        "v18_prebeta_readiness",
        "execution_readiness",
        "execution_eligibility",
        "execution_blocker",
        "execution_reason",
        "execution_provenance",
        "execution_schema",
        "execution_approval",
        "provider_path",
        "adapter_selection",
        "prompt_acceptance_gate",
        "prompt_routing_gate",
        "prompt_send",
        "model_execution_status",
        "provider_visible_data_execution",
        "functional_ai_release_gate",
        "v18_release_gate",
        "gpu_capability",
        "cpu_fallback",
        "hardware_detection_level",
        "ram_readiness",
        "disk_readiness",
        "model_workload",
        "model_workload_metadata",
        "capability_pack_download",
        "capability_pack_manifest",
        "capability_pack_compatibility",
        "capability_pack_eligibility",
        "install_intent",
        "data_classification",
        "provider_visible_data_guarantee",
        "voice_runtime",
        "memory_indexing",
        "network_egress",
        "copy_contract",
        "contract_ready",
        "release_proof",
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
            'data-provider-configuration="unconfigured"',
            'data-provider-registry="local-only-registry"',
            'data-provider-interaction="provider-boundary-interaction-plan"',
            'data-runtime-category="provider_setup_disabled"',
            'data-runtime-reason="provider_setup_disabled_local_only"',
            'data-runtime-provenance="default_config"',
            'data-runtime-schema="provider-runtime-state.v1"',
            'data-runtime-config="default_config"',
            'data-runtime-fail-closed="true"',
            'data-provider-readiness="setup_disabled"',
            'data-setup-eligibility="setup_eligibility_disabled"',
            'data-setup-blocker="setup_disabled"',
            'data-readiness-reason="readiness_default_local_only"',
            'data-readiness-provenance="default_config"',
            'data-readiness-schema="provider-readiness-state.v1"',
            'data-future-provider-gate="provider-setup-future-user-approval-required"',
            'data-provider-activation="activation_unavailable"',
            'data-activation-eligibility="activation_eligibility_unavailable"',
            'data-activation-blocker="readiness_required"',
            'data-activation-reason="activation_default_unavailable"',
            'data-activation-provenance="default_config"',
            'data-activation-schema="provider-activation-state.v1"',
            'data-future-activation-gate="activation-future-user-approval-required"',
            'data-provider-adapter="null-local-adapter"',
            'data-prompt-execution-gate="prompt-execution-disabled"',
            'data-model-execution-gate="model-execution-disabled"',
            'data-provider-execution-gate="provider-execution-disabled"',
            'data-functional-ai-criteria="functional-ai-criteria-pending"',
            'data-v18-prebeta-readiness="v1.8.0-prebeta-readiness-pending"',
            'data-execution-readiness="execution_unavailable"',
            'data-execution-eligibility="execution_eligibility_unavailable"',
            'data-execution-blocker="activation_required"',
            'data-execution-reason="execution_default_unavailable"',
            'data-execution-provenance="activation_state"',
            'data-execution-schema="provider-execution-readiness-state.v1"',
            'data-execution-approval="execution-approval-missing"',
            'data-provider-path="provider-path-not-selected"',
            'data-adapter-selection="adapter-selection-null-local"',
            'data-prompt-acceptance-gate="prompt-acceptance-disabled"',
            'data-prompt-routing-gate="prompt-routing-disabled"',
            'data-prompt-send="prompt-send-disabled"',
            'data-model-execution-status="model-execution-disabled"',
            'data-provider-visible-data-execution="provider-visible-data-execution-none"',
            'data-functional-ai-release-gate="functional-ai-release-gate-pending"',
            'data-v18-release-gate="v1.8.0-prebeta-release-gate-pending-functional-ai"',
            'data-configured-provider-count="0"',
            'data-available-provider-count="0"',
            'data-hardware-capability="local-planning-only"',
            'data-hardware-detection-level="level-1-safe-local-static-snapshot"',
            'data-ram-readiness="ram-unprobed"',
            'data-disk-readiness="disk-unprobed"',
            'data-model-workload-metadata="model-workload-metadata-planned"',
            'id="ai-provider-status-gpu"',
            "GPU acceleration: unprobed; no model workload active",
            'id="ai-provider-status-cpu"',
            "CPU fallback: preserved",
            'id="ai-provider-status-power"',
            "Power state: not evaluated",
            'id="ai-provider-status-thermal"',
            "Thermal guardrails required before model workloads",
            'id="ai-provider-status-model-workload"',
            "Model workloads: disabled",
            'id="ai-provider-status-hardware-detection"',
            "Hardware detection: Level 1 safe local static snapshot",
            'id="ai-provider-status-ram"',
            "RAM readiness: unprobed",
            'id="ai-provider-status-disk"',
            "Disk readiness: unprobed",
            'id="ai-provider-status-model-metadata"',
            "Model workload metadata: planned; no execution",
            'data-capability-pack-lifecycle="capability-pack-lifecycle-planned"',
            'data-capability-pack-manifest="manifest-planned"',
            'data-capability-pack-compatibility="compatibility-unproven"',
            'data-capability-pack-eligibility="capability-pack-eligibility-blocked"',
            'data-install-intent="install-intent-blocked"',
            'id="ai-provider-status-capability-download"',
            "Capability pack downloads: blocked",
            'id="ai-provider-status-capability-recommendation"',
            "Capability recommendation pending hardware proof",
            'id="ai-provider-status-capability-manifest"',
            "capability-pack-manifest.v1; manifest-planned",
            'id="ai-provider-status-capability-integrity"',
            "checksum-required-before-install; signature-required-before-install; compatibility-unproven",
            'id="ai-provider-status-data-classification"',
            "Data classification: local-only planning",
            'data-memory-context="memory-context-disabled"',
            'data-memory-indexing="memory-indexing-disabled"',
            'data-network-egress="network-egress-blocked"',
            'id="ai-provider-status-audit-secrets"',
            "Audit/secrets: planned; no secrets stored",
            'data-windows-resilience="windows-resilience-planned"',
            'id="ai-provider-status-offline"',
            "Offline/degraded mode: planned",
            'data-persona-voice-boundary="persona-core-voice-boundary-planned"',
            'id="ai-provider-status-voice"',
            "Voice runtime: disabled",
            'data-validation-gates="validation-proof-gates-planned"',
            'data-copy-contract="core-desktop-runtime-state-contract"',
            'data-contract-ready="contract-ready"',
            'id="ai-provider-status-abuse"',
            "Abuse/eval: pending future approval",
            'id="ai-provider-status-release-proof"',
            "Release proof: pending future approval",
            'data-consent-state="required-before-provider"',
            "No AI provider",
            "No-provider fallback active",
            "Provider configuration: none",
            "Local provider registry: no configured providers",
            "Hardware capability: local planning only",
            "Capability packs: lifecycle planned",
            "Memory/context: disabled; no indexing",
            'id="ai-provider-status-memory-contract"',
            "memory-indexing-disabled; retrieval-disabled; learning-disabled; persistence-disabled",
            'id="ai-provider-status-egress"',
            "network-egress-blocked",
            "Windows resilience: planning only",
            "Persona/Core/voice: planning boundary",
            "Validation gates: static proof active",
            'id="ai-provider-status-copy-contract"',
            "core-desktop-provider-state-copy.v1; core-desktop-runtime-state-contract",
            'id="ai-provider-status-fixtures"',
            "golden-provider-state-fixtures; validator-expansion-active",
            "Consent required before provider setup",
            "Provider-visible data: none",
            "No prompt, file, screen, memory, or telemetry is sent",
            "Consent boundary: provider setup required before prompts",
            'id="ai-provider-status-runtime"',
            "Runtime state: provider setup disabled",
            'id="ai-provider-status-runtime-reason"',
            "Reason: setup disabled in local-only seam",
            'id="ai-provider-status-runtime-provenance"',
            "Provenance: default config",
            'id="ai-provider-status-runtime-schema"',
            "provider-runtime-state.v1; provider-runtime-config.v1; Config: safe default local-only",
            'id="ai-provider-status-readiness"',
            "Provider readiness: setup disabled",
            'id="ai-provider-status-setup-eligibility"',
            "Setup eligibility: disabled",
            'id="ai-provider-status-setup-blocker"',
            "Setup blocker: setup disabled",
            'id="ai-provider-status-readiness-reason"',
            "Readiness reason: local-only default",
            'id="ai-provider-status-readiness-provenance"',
            "Readiness provenance: default config",
            'id="ai-provider-status-readiness-schema"',
            "provider-readiness-state.v1; provider-readiness-config.v1; Readiness config: safe default local-only",
            'id="ai-provider-status-future-gate"',
            "Future provider gate: USER approval required before setup",
            'id="ai-provider-status-activation"',
            "Provider activation: unavailable",
            'id="ai-provider-status-activation-eligibility"',
            "Activation eligibility: unavailable",
            'id="ai-provider-status-activation-blocker"',
            "Activation blocker: readiness required",
            'id="ai-provider-status-activation-reason"',
            "Activation reason: activation foundation only",
            'id="ai-provider-status-activation-provenance"',
            "Activation provenance: default config",
            'id="ai-provider-status-activation-schema"',
            "provider-activation-state.v1; provider-activation-config.v1; Activation config: safe default local-only",
            'id="ai-provider-status-future-activation-gate"',
            "Future activation gate: USER approval required before activation",
            'id="ai-provider-status-adapter"',
            "Provider adapter: null local adapter",
            'id="ai-provider-status-execution-gates"',
            "Prompt/model/provider execution: disabled",
            'id="ai-provider-status-functional-ai"',
            "Functional AI: criteria pending for v1.8.0-prebeta",
            'id="ai-provider-status-execution-readiness"',
            "Execution readiness: unavailable",
            'id="ai-provider-status-execution-eligibility"',
            "Execution eligibility: unavailable",
            'id="ai-provider-status-execution-blocker"',
            "Execution blocker: activation required",
            'id="ai-provider-status-execution-reason"',
            "Execution reason: execution readiness gates only",
            'id="ai-provider-status-execution-provenance"',
            "Execution provenance: activation state",
            'id="ai-provider-status-execution-schema"',
            "provider-execution-readiness-state.v1; provider-execution-readiness-config.v1; Execution config: safe default local-only",
            'id="ai-provider-status-execution-approval"',
            "Execution approval: USER approval missing",
            'id="ai-provider-status-provider-path"',
            "Provider path: not selected",
            'id="ai-provider-status-adapter-selection"',
            "Adapter selection: null local fallback",
            'id="ai-provider-status-prompt-gates"',
            "Prompt acceptance gate: disabled; Prompt routing gate: disabled; Prompt send: disabled",
            'id="ai-provider-status-model-execution"',
            "Model execution status: disabled; Model workload readiness: disabled",
            'id="ai-provider-status-execution-data"',
            "Provider-visible execution data: none; External call readiness: blocked",
            'id="ai-provider-status-functional-release"',
            "Functional-AI release gate: pending; v1.8.0-prebeta release gate: pending functional AI proof",
            'id="ai-provider-status-capability-eligibility"',
            "Capability-pack eligibility: blocked",
            'id="ai-provider-status-install-intent"',
            "Install intent: blocked",
            'id="ai-provider-status-action"',
            "Assisted Desktop unavailable",
            "Next: provider setup is disabled in this local-only foundation seam",
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
        ".ai-provider-status__runtime",
        ".ai-provider-status__readiness",
        ".ai-provider-status__activation",
        ".ai-provider-status__adapter",
        ".ai-provider-status__execution-gates",
        ".ai-provider-status__functional-ai",
        ".ai-provider-status__execution-readiness",
        ".ai-provider-status__execution-eligibility",
        ".ai-provider-status__execution-blocker",
        ".ai-provider-status__execution-reason",
        ".ai-provider-status__execution-schema",
        ".ai-provider-status__execution-approval",
        ".ai-provider-status__provider-path",
        ".ai-provider-status__adapter-selection",
        ".ai-provider-status__prompt-gates",
        ".ai-provider-status__model-execution",
        ".ai-provider-status__execution-data",
        ".ai-provider-status__functional-release",
        ".ai-provider-status__hardware-detection",
        ".ai-provider-status__capability-manifest",
        ".ai-provider-status__capability-eligibility",
        ".ai-provider-status__memory-contract",
        ".ai-provider-status__copy-contract",
        'data-availability="ready"',
        "overflow-wrap: anywhere",
    ):
        _require(needle in css, f"core CSS is missing {needle!r}", failures)

    for needle in (
        "const aiProviderStatus",
        "renderAIProviderState",
        "window.setAIProviderState",
        "providerSelectionState",
        "providerConfigurationState",
        "providerRegistryState",
        "providerInteractionState",
        "hardwareCapabilityState",
        "gpuCapabilityState",
        "cpuFallbackState",
        "hardwareDetectionLevel",
        "ramReadinessState",
        "diskReadinessState",
        "powerState",
        "thermalGuardrailState",
        "modelWorkloadState",
        "modelWorkloadMetadataState",
        "capabilityRecommendationState",
        "capabilityPackLifecycleState",
        "capabilityPackDownloadState",
        "capabilityPackManifestSchemaVersion",
        "capabilityPackManifestState",
        "capabilityPackChecksumState",
        "capabilityPackSignatureState",
        "capabilityPackCompatibilityState",
        "dataClassificationState",
        "dataClassificationSchemaVersion",
        "providerVisibleDataGuarantee",
        "memoryContextState",
        "memoryIndexingState",
        "retrievalState",
        "learningState",
        "persistenceState",
        "networkEgressState",
        "auditSecretsState",
        "windowsResilienceState",
        "offlineDegradedState",
        "personaCoreVoiceState",
        "voiceRuntimeState",
        "validationProofGateState",
        "abuseEvalState",
        "releaseProofGateState",
        "coreDesktopCopyContractVersion",
        "coreDesktopRuntimeStateContract",
        "disabledPromptBehaviorContract",
        "goldenProviderStateFixtures",
        "validatorExpansionState",
        "contractReadyMarker",
        "uiReadyMarker",
        "validatorReadyMarker",
        "futureImplementationGatedMarker",
        "configuredProviderCount",
        "availableProviderCount",
        "requiresConsent",
        "consentState",
        "interactionAffordance",
        "providerVisibleDataLabel",
        "providerVisibleDataDetail",
        "providerConsentBoundaryLabel",
        "providerNextActionLabel",
        "runtimeStateSchemaVersion",
        "runtimeStateCategory",
        "runtimeReasonCode",
        "runtimeProvenance",
        "runtimeConfigState",
        "runtimeFailClosed",
        "providerReadinessState",
        "setupEligibilityState",
        "setupBlockerState",
        "readinessReasonCode",
        "readinessProvenance",
        "readinessStateSchemaVersion",
        "futureProviderGateStatus",
        "providerActivationState",
        "activationEligibilityState",
        "activationBlockerState",
        "activationReasonCode",
        "activationProvenance",
        "activationStateSchemaVersion",
        "futureActivationGateStatus",
        "providerAdapterPosture",
        "providerAdapterAvailabilityState",
        "providerAdapterExecutionPosture",
        "providerMetadataContractVersion",
        "providerConfigEnvelopeVersion",
        "promptExecutionGateState",
        "modelExecutionGateState",
        "providerExecutionGateState",
        "functionalAiCriteriaState",
        "v18PrebetaReadinessState",
        "providerExecutionReadinessState",
        "executionEligibilityState",
        "executionBlockerState",
        "executionReasonCode",
        "executionProvenance",
        "executionStateSchemaVersion",
        "executionConfigSchemaVersion",
        "executionConfigState",
        "executionApprovalStatus",
        "providerPathStatus",
        "adapterSelectionPosture",
        "promptAcceptanceGateState",
        "promptRoutingGateState",
        "promptSendPosture",
        "modelExecutionStatus",
        "modelWorkloadReadinessPosture",
        "providerVisibleDataExecutionPosture",
        "externalCallReadinessState",
        "functionalAiReleaseGateState",
        "v18ReleaseGateState",
        "capabilityPackEligibilityState",
        "installIntentState",
        "aiProviderStatusReadiness",
        "aiProviderStatusSetupEligibility",
        "aiProviderStatusSetupBlocker",
        "aiProviderStatusReadinessReason",
        "aiProviderStatusFutureGate",
        "aiProviderStatusActivation",
        "aiProviderStatusActivationEligibility",
        "aiProviderStatusActivationBlocker",
        "aiProviderStatusActivationReason",
        "aiProviderStatusActivationProvenance",
        "aiProviderStatusActivationSchema",
        "aiProviderStatusFutureActivationGate",
        "aiProviderStatusAdapter",
        "aiProviderStatusExecutionGates",
        "aiProviderStatusFunctionalAi",
        "aiProviderStatusExecutionReadiness",
        "aiProviderStatusExecutionEligibility",
        "aiProviderStatusExecutionBlocker",
        "aiProviderStatusExecutionReason",
        "aiProviderStatusExecutionProvenance",
        "aiProviderStatusExecutionSchema",
        "aiProviderStatusExecutionApproval",
        "aiProviderStatusProviderPath",
        "aiProviderStatusAdapterSelection",
        "aiProviderStatusPromptGates",
        "aiProviderStatusModelExecution",
        "aiProviderStatusExecutionData",
        "aiProviderStatusFunctionalRelease",
        "aiProviderStatusCapabilityEligibility",
        "aiProviderStatusInstallIntent",
        "aiProviderStatusRuntime",
        "aiProviderStatusRuntimeReason",
        "aiProviderStatusRuntimeProvenance",
        "aiProviderStatusRuntimeSchema",
        "aiProviderStatusAction.disabled = true",
        "sentToProvider",
        "canAcceptPrompts",
    ):
        _require(needle in js, f"core JS is missing {needle!r}", failures)

    for needle in (
        "FAM-007 Local AI Provider Execution Readiness Gates",
        "Current Workstream State: `Green - bounded multi-seam execution-readiness implementation complete; H1 reviewed and green`",
        "Current Hardening State: `Green - H1 compared the local-only execution-readiness implementation against the admitted Workstream plan",
        "Workstream Completion State: `Green - H1 Green and ready for Live Validation LV1 after USER approval`",
        "Hardening H1 Status: `Green`",
        "Next Legal Phase: `Live Validation LV1 for FAM-007 Local AI Provider Execution Readiness Gates`",
        "Seam Family 1 - Execution Readiness Gate Contract: `Green`",
        "Seam Family 2 - Provider Path And Adapter Selection Contract: `Green`",
        "Seam Family 3 - Prompt Path And Model Execution Proof Contract: `Green`",
        "Seam Family 4 - Safety, Consent, Network, And Data Gate Alignment: `Green`",
        "Seam Family 5 - Functional-AI Release Gate And v1.8.0 Criteria: `Green`",
        "Seam Family 6 - Core/Desktop Execution Readiness UI And Validator Planning: `Green`",
        "provider-execution-readiness-state.v1",
        "provider-execution-readiness-config.v1",
        "execution_unavailable",
        "execution_blocked_by_activation",
        "execution_blocked_by_provider_path",
        "execution_blocked_by_adapter",
        "execution_blocked_by_prompt_gate",
        "execution_blocked_by_model_gate",
        "execution_blocked_by_consent",
        "execution_blocked_by_safety",
        "execution_blocked_by_network",
        "execution_blocked_by_policy",
        "execution_ready_future_gated",
        "execution_ready_but_not_approved",
        "functional_ai_execution_ready_future_version",
        "provider-path-not-selected",
        "adapter-selection-null-local",
        "prompt-send-disabled",
        "model-execution-disabled",
        "provider-visible-data-execution-none",
        "functional-ai-release-gate-pending",
        "v1.8.0-prebeta-release-gate-pending-functional-ai",
        "Provider SDK integration remains a pending USER decision",
        "Provider/model execution remains a pending USER decision",
        "Memory indexing, retrieval, learning, persistence, personalization, or long-term adaptation remains a pending USER decision",
    ):
        _require(needle in active_execution_branch_record, f"active FAM-007 execution record is missing {needle!r}", failures)

    for needle in (
        "Branch Runtime Engineering Plan: FAM-007 Local AI Provider Execution Readiness Gates",
        "Engineering Plan Status: `Implemented and H1 Green - bounded Workstream implementation maps the accepted plan into local-only execution-readiness state, UI, validator fixtures, source-truth proof, and hardening review; Live Validation LV1 remains pending USER approval.`",
        "Hardening H1 Result: `Green - H1 compared implementation against this plan",
        "Runtime Implementation Approval: `Granted - USER approved bounded Workstream implementation for this local-only execution-readiness gates branch; provider/model execution remains pending USER decision.`",
        "Plan-To-Implementation Traceability Table: `Implemented - planned execution-readiness state maps to actual file desktop/ai_provider_state.py; planned provider path and adapter selection map to actual local config/schema fields; planned prompt/model gates map to actual disabled prompt/model/provider execution fields; planned UI copy maps to actual Core/Desktop/ORIN status surfaces; validator implementation traces no prompt send, no model execution, provider-visible data none, blocked network egress, deferred memory/learning/personalization, and v1.8.0 criteria pending.`",
        "Workstream Completion Evidence: `Green - all admitted execution-readiness seam families implemented as local-only contracts, state, UI posture, validator fixtures, and source-truth proof.",
        "provider-execution-readiness-state.v1",
        "provider-execution-readiness-config.v1",
        "provider-visible data none",
        "prompt/provider sends disabled",
        "v1.8.0-prebeta",
    ):
        _require(needle in execution_branch_plan, f"active FAM-007 execution branch plan is missing {needle!r}", failures)

    for needle in (
        "FAM-007 Local AI Provider Activation Foundation",
        "Provider Activation Contract and Gate Model: `Green`",
        "Provider Adapter Boundary and Null Activation Surface: `Green`",
        "Prompt/Execution Gate and Functional-AI Criteria: `Green`",
        "Capability Pack, Consent, and Safety Gate Alignment: `Green`",
        "Core/Desktop Activation Posture and Validator Planning: `Green`",
        "Workstream Completion State: `Green - H1 and LV1 complete; PR Readiness Stage 1 selected-next/defer repair recorded; ready for PR Readiness Stage 2 after USER approval`",
        "Current Hardening State: `Green - H1 validated",
        "Hardening H1 State: `Green - completed after accepted Workstream completion evidence`",
        "Hardening Next Legal Phase: `Live Validation LV1 after USER approval`",
        "Current Live Validation State: `Green - LV1 classified this branch as disabled/status-only local activation foundation scaffolding",
        "Live Validation LV1 State: `Green - completed with static Core/Desktop/ORIN source-truth and provider-state validator proof`",
        "LV Classification: `disabled/status-only local activation foundation scaffold`",
        "User Test Summary Results: `WAIVED`",
        "User-Facing Shortcut Validation: `WAIVED -",
        "Codex Live Client Self-QA: `WAIVED -",
        "Live Validation LV1 Next Legal Phase: `PR Readiness Stage 1 after USER approval`",
        "PR Readiness Stage 1 Repair USER Approval: `Granted - USER approved selected-next defer/waiver truth",
        "Pre-PR Live State: `No live PR - PR Readiness Stage 2 / PR creation approval missing",
        "Post-Merge Branch Authority Projection: `PASS -",
        "Next Workstream User Waiver: Granted - USER approved selected-next defer/waiver",
        "Selected Next Workstream: None - USER-approved selected-next defer/waiver",
        "Selected Next Implementation Branch: Not created",
        "Release Window Audit: PASS",
        "provider-activation-state.v1",
        "provider-activation-config.v1",
        "activation_unavailable",
        "activation_blocked_by_readiness",
        "activation_blocked_by_consent",
        "activation_blocked_by_capability",
        "activation_blocked_by_manifest",
        "activation_blocked_by_adapter",
        "activation_eligible_future_gated",
        "activation_ready_but_execution_gated",
        "functional_ai_ready_future_version",
        "null-local-adapter",
        "prompt-execution-disabled",
        "model-execution-disabled",
        "provider-execution-disabled",
        "functional-ai-criteria-pending",
        "v1.8.0-prebeta-readiness-pending",
        "Provider SDK integration remains a pending USER decision",
        "Provider/model execution remains a pending USER decision",
        "Memory indexing, retrieval, learning, persistence, personalization, or long-term adaptation remains a pending USER decision",
    ):
        _require(needle in active_activation_branch_record, f"active FAM-007 activation record is missing {needle!r}", failures)

    for needle in (
        "FAM-007 Local AI Provider Runtime Readiness and Setup Eligibility",
        "SLC-017/SLC-018 Provider Readiness Contract",
        "SLC-017/SLC-018 Consent and Configuration Transition Contract",
        "SLC-031/SLC-032 Capability-Pack Eligibility and Install-Intent Posture",
        "SLC-035/SLC-036 Core/Desktop Readiness UI and Validator Fixtures",
        "Provider Readiness Contract: `Green`",
        "Consent and Configuration Transition Contract: `Green`",
        "Capability-Pack Eligibility and Install-Intent Posture: `Green`",
        "Core/Desktop Readiness UI and Validator Fixtures: `Green`",
        "Workstream Completion State: `Green - ready for Hardening H1 after USER approval`",
        "Hardening H1 Proof Review Status: `Green - Hardening H1 proof review completed",
        "Hardening H1 Result: `PASS - no runtime, UI, validator, or Engineering Contract defect repair was required",
        "Live Validation LV1 USER Approval: `Granted - USER approved Live Validation LV1",
        "Current Live Validation Seam: `Live Validation LV1 - FAM-007 Local AI Provider Runtime Readiness and Setup Eligibility`",
        "Live Validation LV1 Result: `PASS - disabled/status-only local readiness scaffold",
        "User Test Summary Results: `WAIVED`",
        "User-Facing Shortcut Validation: `WAIVED`",
        "Codex Live Client Self-QA: `WAIVED`",
        "PR Readiness Stage 1 Repair USER Approval: `Historical - USER approved selected-next defer/waiver truth and pre-PR live-state truth before PR #165",
        "Current PR Readiness State: `Closed by PR #165 merge",
        "Pre-PR Live State: Historical only - PR #165 was created and merged",
        "Post-Merge Branch Authority Projection: `PASS -",
        "Next Workstream User Waiver: Granted - USER approved selected-next defer/waiver",
        "Selected Next Workstream: None - USER-approved selected-next defer/waiver",
        "Selected Next Implementation Branch: Not created",
        "Release Window Audit: PASS",
        "Governance Drift Found:",
        "Next Legal Seam: `Release Readiness Stage 1 rerun after Governance RRI-20260519-001 merges",
        "provider-readiness-state.v1",
        "provider-readiness-config.v1",
        "setup_available_future_gated",
        "provider_ready_but_execution_gated",
        "readiness_manifest_invalid_install_blocked",
        "Capability-pack eligibility: blocked",
        "Install intent: blocked",
        "Provider SDK integration remains a pending USER decision",
        "Provider/model execution remains a pending USER decision",
        "Memory indexing, retrieval, learning, or persistence remains a pending USER decision",
    ):
        _require(needle in active_readiness_branch_record, f"active FAM-007 readiness record is missing {needle!r}", failures)

    for needle in (
        "SLC-017/SLC-018 No-Provider Shell And Provider-Privacy State",
        "SLC-017/SLC-018 Provider Selection And Consent Boundary Scaffold",
        "SLC-017/SLC-018 Assisted Desktop Mode No-Provider Interaction And Consent Surface",
        "SLC-018 Local Provider Registry And Configuration State",
        "SLC-031 Hardware/GPU/CPU Capability Planning Scaffold",
        "SLC-032 Model And Capability-Pack Lifecycle Planning Scaffold",
        "SLC-033 Data Classification Memory Context Consent Audit Secrets Planning Scaffold",
        "SLC-034 Windows Resilience Platform Posture Planning Scaffold",
        "SLC-035 Persona Core Voice Planning Boundary",
        "SLC-036 Validation Eval Abuse Release Proof Gates",
        "Hardening H1 - FAM-007 Provider Boundary And No-Provider Shell Local-Only Scaffold Chain",
        "Live Validation LV1 USER Approval: `Granted - USER approved Live Validation LV1",
        "Current Live Validation Seam: `Live Validation LV1 - FAM-007 Provider Boundary And No-Provider Shell Applicability And No-Provider Surface Proof`",
        "User Test Summary Results: `WAIVED`",
        "Codex Live Client Self-QA: `WAIVED`",
        "PR Readiness Execution User Approval Missing",
        "model downloads",
        "real provider SDK integration",
        "AI Product Contract v0.6.2",
    ):
        _require(needle in branch_record, f"branch record is missing {needle!r}", failures)

    for needle in (
        "SLC-017/SLC-018 Local AI Foundation Runtime Continuation - Provider Boundary Interaction Plan",
        "SLC-031/SLC-032 Local Capability-Readiness Continuation",
        "SLC-033/SLC-036 Local Data Resilience Persona And Proof-Gate Continuation",
        "SLC-017/SLC-018 provider-boundary interaction continuation",
        "local capability-readiness continuation",
        "local data/resilience/persona/proof-gate continuation",
        "visible consent-boundary copy",
        "provider-visible-data detail",
        "disabled provider setup next action",
        "Completion Status: `Green`",
        "Continue Decision: `Stop`",
        "Continuation Execution Latch:",
        "Historical merge proof: `PR #152 merged feature/fam-007-local-ai-foundation-runtime-continuation into main",
        "Branch Authority State: `Historical merged branch - not active, not selected-next, and not a live PR carrier`",
        "Completed Hardening: `H1 proof review was green with no runtime defect repair required`",
        "Proof Review Status: `Green - Hardening H1 proof review completed for all admitted same-branch FAM-007 local-only scaffolds.`",
        "Completed Live Validation: `LV1 classified the disabled/status-only scaffold as static/source-truth/compile validated with User Test Summary, user-facing shortcut validation, and Codex live-client self-QA waived`",
        "User Test Summary Results: `WAIVED`",
        "User-Facing Shortcut Validation: `WAIVED`",
        "Codex Live Client Self-QA: `WAIVED`",
        "Active seam: `None - historical after PR #152 merge`",
        "Future FAM-007 work must enter Branch Readiness on a valid carrier after current `origin/main` is reconciled",
        "Bounded means one active seam at a time, not one-seam Workstream authority",
    ):
        _require(
            needle in continuation_branch_record,
            f"continuation branch record is missing {needle!r}",
            failures,
        )

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
