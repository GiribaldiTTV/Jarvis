"""Validate the FAM-003 resident access / quick actions workstream contract."""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_true(condition: bool, message: str, failures: list[str]):
    if not condition:
        failures.append(message)


def validate_resident_model(failures: list[str]):
    from desktop.resident_access import (
        DEFAULT_QUICK_SLOT_COUNT,
        DEFAULT_QUICK_SLOT_ROUTE_IDS,
        IMMUTABLE_ROUTE_IDS,
        MAX_QUICK_SLOT_COUNT,
        TRAY_DISCOVERY_MESSAGE,
        TRAY_IDENTITY_LABEL,
        TRAY_TOOLTIP_TEXT,
        WINDOWS_TRAY_VISIBILITY_LIMITATION,
        build_resident_access_menu_plan,
        normalize_resident_access_settings,
    )

    plan = build_resident_access_menu_plan()
    immutable_ids = [route["routeId"] for route in plan["immutableRoutes"]]
    quick_ids = [route["routeId"] for route in plan["quickSlots"]]
    route_owner = {route["routeId"]: route["ownerFamily"] for route in plan["immutableRoutes"]}

    assert_true(TRAY_IDENTITY_LABEL == "Nexus Desktop AI", "tray identity label drifted", failures)
    assert_true(
        TRAY_TOOLTIP_TEXT.startswith("Nexus Desktop AI - ")
        and "Provider-visible data: none" in TRAY_TOOLTIP_TEXT,
        "tray tooltip must include compact AI/privacy status, not identity only",
        failures,
    )
    assert_true(tuple(immutable_ids) == IMMUTABLE_ROUTE_IDS, "immutable route order drifted", failures)
    assert_true(
        set(IMMUTABLE_ROUTE_IDS)
        == {
            "hud_dashboard",
            "global_settings",
            "ai_status_command_center",
            "privacy_lockdown",
            "exit_nexus",
        },
        "immutable route set is incomplete",
        failures,
    )
    assert_true(route_owner.get("hud_dashboard") == "FAM-006", "HUD Dashboard owner must remain FAM-006", failures)
    assert_true(
        route_owner.get("ai_status_command_center") == "FAM-007",
        "AI Status / Command Center owner must remain FAM-007",
        failures,
    )
    assert_true(
        route_owner.get("privacy_lockdown") == "FAM-007",
        "Privacy Lockdown owner must remain FAM-007",
        failures,
    )
    assert_true(
        tuple(quick_ids) == DEFAULT_QUICK_SLOT_ROUTE_IDS,
        f"default quick slots drifted: {quick_ids}",
        failures,
    )
    assert_true(
        plan["menuBudget"]["defaultQuickSlots"] == DEFAULT_QUICK_SLOT_COUNT,
        "default quick-slot count must remain three",
        failures,
    )
    assert_true(
        plan["menuBudget"]["maximumQuickSlots"] == MAX_QUICK_SLOT_COUNT == 5,
        "maximum quick-slot budget must remain five",
        failures,
    )
    assert_true(
        "cannot force permanent tray placement" in WINDOWS_TRAY_VISIBILITY_LIMITATION,
        "Windows tray visibility limitation proof wording is missing force-placement honesty",
        failures,
    )
    assert_true(
        "hidden icons" in TRAY_DISCOVERY_MESSAGE,
        "tray discovery message must mention hidden icons",
        failures,
    )
    assert_true(
        "single tray icon" in plan["singleTrayIconContract"],
        "single tray icon contract is missing",
        failures,
    )
    assert_true(
        "Provider-visible data: none" in plan["aiPrivacy"]["providerVisibleDataLabel"],
        "AI/privacy status must preserve provider-visible data none",
        failures,
    )
    assert_true(
        str(plan.get("tooltipText", "")).startswith("Nexus Desktop AI - ")
        and "Provider-visible data: none" in str(plan.get("tooltipText", "")),
        "resident access plan tooltip must carry compact AI/privacy status",
        failures,
    )

    normalized = normalize_resident_access_settings(
        {
            "quickSlotIds": [
                "command_overlay",
                "command_overlay",
                "recording_studio",
                "unknown",
                "log_viewer",
                "tray_visibility_education",
                "open_saved_actions_folder",
            ],
            "menuBudget": 99,
        }
    )
    assert_true(
        normalized.quick_slot_ids
        == (
            "command_overlay",
            "recording_studio",
            "log_viewer",
            "tray_visibility_education",
            "open_saved_actions_folder",
        ),
        f"quick-slot normalization failed: {normalized.quick_slot_ids}",
        failures,
    )
    assert_true(normalized.menu_budget == 5, "quick-slot menu budget did not clamp to five", failures)


def validate_static_wiring(failures: list[str]):
    tray_text = read("desktop/tray_controller.py")
    renderer_text = read("desktop/desktop_renderer.py")
    main_text = read("desktop/orin_desktop_main.py")
    registry_text = read("Docs/validation_helper_registry.md")

    ast.parse(tray_text, filename="desktop/tray_controller.py")
    ast.parse(renderer_text, filename="desktop/desktop_renderer.py")
    ast.parse(main_text, filename="desktop/orin_desktop_main.py")

    assert_true("SP_ComputerIcon" not in tray_text, "tray icon still falls back to monitor/computer icon", failures)
    for token in (
        "build_resident_tray_icon",
        "TRAY_RESIDENT_ACCESS_TRAY_ICON_READY",
        "request_global_settings_from_tray",
        "request_ai_status_from_tray",
        "TRAY_AI_STATUS_COMMAND_CENTER_ROUTED",
        "request_privacy_lockdown_from_tray",
        "request_quick_slot_from_tray",
        "TRAY_RESIDENT_ACCESS_ACTIONS_REFRESHED",
        "_native_menu_status_text",
        "nexusDesktopTrayStatus",
        "#07111f",
    ):
        assert_true(token in tray_text, f"tray resident access token missing: {token}", failures)
    assert_true(
        'self.ai_control_center_action = self._add_button_action(' not in tray_text,
        "tray menu must not expose a duplicate top-level AI Control Center action",
        failures,
    )
    assert_true(
        'self.ai_control_center_button = self.tray_popup.add_button(' not in tray_text,
        "resident popup must not expose a duplicate AI Control Center button",
        failures,
    )
    assert_true(
        'append(90, "AI Control Center"' not in tray_text,
        "native tray menu must not expose a duplicate AI Control Center command",
        failures,
    )

    for token in (
        "class ResidentAccessSettingsDialog",
        "open_resident_access_settings",
        "resident_access_status_snapshot",
        "request_ai_status_from_resident_access",
        "request_privacy_lockdown_from_resident_access",
        "request_resident_quick_action_from_tray",
        "self._replace_quick_slots(self._selected_slot_ids())",
        "setAccessibleName(\"Add Quick Access Slot\")",
        "setMinimumWidth(280)",
        "RESIDENT_ACCESS_PRIVACY_LOCKDOWN_ROUTE_ONLY",
        "Provider-visible data: none",
    ):
        assert_true(token in renderer_text, f"renderer resident access token missing: {token}", failures)

    assert_true(
        "button.setMinimumWidth(240)" in tray_text,
        "tray resident action buttons must keep enough width for long labels",
        failures,
    )
    assert_true(
        'else ""' in tray_text,
        "hidden unused quick slots must not keep visible placeholder labels",
        failures,
    )

    for token in (
        "build_resident_access_menu_plan",
        "resident_access_status_snapshot",
        "RESIDENT_ACCESS_QUICK_ACTION_ABORTED",
    ):
        assert_true(token in main_text, f"runtime fallback resident access token missing: {token}", failures)

    assert_true(
        "`dev/orin_fam003_resident_access_validation.py`" in registry_text,
        "FAM-003 resident access validator is not registered",
        failures,
    )


def validate_no_forbidden_runtime_work(failures: list[str]):
    model_text = read("desktop/resident_access.py").casefold()
    forbidden = (
        "openai",
        "anthropic",
        "provider sdk",
        "memory index",
        "cache migration",
        "shortcut",
        "installer",
        "startup behavior",
    )
    for token in forbidden:
        assert_true(token not in model_text, f"resident_access.py contains out-of-scope token {token!r}", failures)


def main() -> int:
    previous_settings = os.environ.get("NEXUS_RESIDENT_ACCESS_SETTINGS_PATH")
    os.environ["NEXUS_RESIDENT_ACCESS_SETTINGS_PATH"] = str(
        ROOT / "dev" / "logs" / "fam003_resident_access_validation" / "settings.json"
    )
    failures: list[str] = []
    try:
        validate_resident_model(failures)
        validate_static_wiring(failures)
        validate_no_forbidden_runtime_work(failures)
    finally:
        if previous_settings is None:
            os.environ.pop("NEXUS_RESIDENT_ACCESS_SETTINGS_PATH", None)
        else:
            os.environ["NEXUS_RESIDENT_ACCESS_SETTINGS_PATH"] = previous_settings

    if failures:
        print("FAIL: FAM-003 resident access validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: FAM-003 resident access / quick actions contract is wired and bounded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
