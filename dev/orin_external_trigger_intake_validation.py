import os
import sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from desktop.external_trigger_intake import (
    InternalTriggerIntakeBoundary,
    TRIGGER_INTAKE_DECISION_DEFERRED,
    TRIGGER_INTAKE_DECISION_REJECTED,
    TriggerOriginRegistration,
    TriggerOriginRegistry,
)


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _assert_no_execution(result, message: str) -> None:
    _assert(not result.routed_to_execution, f"{message}: routed_to_execution must stay false")
    _assert(not result.execution_authorized, f"{message}: execution_authorized must stay false")
    _assert(not result.cleanup_required, f"{message}: cleanup_required must stay false")
    _assert(not result.accepted, f"{message}: accepted must stay false")


def validate_registration_contract() -> None:
    registry = TriggerOriginRegistry()

    registered = registry.register(
        {
            "origin_id": "Deck Button 1",
            "origin_category": "hardware-adjacent",
            "user_visible_label": "Deck Button 1",
            "enabled": True,
        }
    )
    _assert(registered.registered, "supported trigger origin should register")
    _assert(registered.reason == "registered", "supported registration should report registered")

    duplicate = registry.register(
        {
            "origin_id": "Deck Button 1",
            "origin_category": "hardware_adjacent",
        }
    )
    _assert(not duplicate.registered, "duplicate trigger origin should reject")
    _assert(duplicate.reason == "duplicate_origin_id", "duplicate should report duplicate_origin_id")

    blocked = registry.register(
        {
            "origin_id": "Remote Network",
            "origin_category": "remote_network",
        }
    )
    _assert(not blocked.registered, "blocked trigger origin should reject")
    _assert(blocked.reason == "blocked_origin_category", "blocked should report blocked category")

    unsupported = registry.register(
        {
            "origin_id": "Unknown Trigger",
            "origin_category": "unknown_tool",
        }
    )
    _assert(not unsupported.registered, "unsupported trigger origin should reject")
    _assert(
        unsupported.reason == "unsupported_origin_category",
        "unsupported should report unsupported category",
    )

    print("PASS: trigger origin registration contract")


def validate_invocation_follow_through_contract() -> None:
    registry = TriggerOriginRegistry()
    result = registry.register(
        TriggerOriginRegistration(
            origin_id="Deck Button 1",
            origin_category="hardware_adjacent",
            user_visible_label="Deck Button 1",
            enabled=True,
        )
    )
    _assert(result.registered, "enabled origin setup should register")

    disabled_registry = TriggerOriginRegistry()
    disabled_result = disabled_registry.register(
        TriggerOriginRegistration(
            origin_id="Automation A",
            origin_category="desktop_automation",
            enabled=False,
        )
    )
    _assert(disabled_result.registered, "disabled origin setup should register")

    no_registry = InternalTriggerIntakeBoundary().receive(
        {
            "origin_id": "Deck Button 1",
            "origin_category": "hardware_adjacent",
        }
    )
    _assert(
        no_registry.decision == TRIGGER_INTAKE_DECISION_DEFERRED,
        "request without registry should defer",
    )
    _assert(
        no_registry.reason == "registration_support_not_admitted",
        "request without registry should report missing registration support",
    )
    _assert_no_execution(no_registry, "request without registry")

    boundary = InternalTriggerIntakeBoundary(origin_registry=registry)
    unregistered = boundary.receive(
        {
            "origin_id": "Unregistered Button",
            "origin_category": "hardware_adjacent",
        }
    )
    _assert(
        unregistered.decision == TRIGGER_INTAKE_DECISION_DEFERRED,
        "unregistered origin should defer",
    )
    _assert(
        unregistered.reason == "origin_not_registered",
        "unregistered origin should report origin_not_registered",
    )
    _assert_no_execution(unregistered, "unregistered origin")

    disabled = InternalTriggerIntakeBoundary(origin_registry=disabled_registry).receive(
        {
            "origin_id": "Automation A",
            "origin_category": "desktop_automation",
        }
    )
    _assert(
        disabled.decision == TRIGGER_INTAKE_DECISION_DEFERRED,
        "disabled registered origin should defer",
    )
    _assert(disabled.reason == "origin_not_enabled", "disabled origin should report disabled")
    _assert(disabled.origin_registered, "disabled origin should be marked registered")
    _assert(not disabled.origin_enabled, "disabled origin should not be marked enabled")
    _assert_no_execution(disabled, "disabled origin")

    enabled = boundary.receive(
        {
            "origin_id": "Deck Button 1",
            "origin_category": "hardware_adjacent",
        }
    )
    _assert(
        enabled.decision == TRIGGER_INTAKE_DECISION_DEFERRED,
        "enabled registered origin should still defer",
    )
    _assert(
        enabled.reason == "invocation_follow_through_not_admitted",
        "enabled origin should stop at follow-through boundary",
    )
    _assert(enabled.origin_registered, "enabled origin should be marked registered")
    _assert(enabled.origin_enabled, "enabled origin should be marked enabled")
    _assert_no_execution(enabled, "enabled registered origin")

    mismatch = boundary.receive(
        {
            "origin_id": "Deck Button 1",
            "origin_category": "desktop_automation",
        }
    )
    _assert(
        mismatch.decision == TRIGGER_INTAKE_DECISION_REJECTED,
        "registration mismatch should reject",
    )
    _assert(
        mismatch.reason == "origin_registration_mismatch",
        "registration mismatch should report mismatch",
    )
    _assert(mismatch.origin_registered, "mismatch should identify known registration")
    _assert(mismatch.origin_enabled, "mismatch should preserve registration enabled state")
    _assert_no_execution(mismatch, "registration mismatch")

    print("PASS: trigger invocation follow-through contract")


def main() -> int:
    validate_registration_contract()
    validate_invocation_follow_through_contract()
    print("EXTERNAL TRIGGER INTAKE VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
