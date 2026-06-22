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
        OPTIONAL_FEATURE_ROUTE_DISABLED_BY_USER,
        OPTIONAL_FEATURE_ROUTE_ENABLED_AVAILABLE,
        OPTIONAL_FEATURE_ROUTE_ENABLED_ERRORED,
        OPTIONAL_FEATURE_ROUTE_ENABLED_NOT_READY,
        OPTIONAL_FEATURE_ROUTE_ENABLED_TEMPORARILY_BLOCKED,
        OPTIONAL_FEATURE_ROUTE_NOT_INSTALLED,
        OPTIONAL_FEATURE_ROUTE_UNKNOWN,
        OPTIONAL_FEATURE_ROUTE_UNSUPPORTED,
        TRAY_DISCOVERY_MESSAGE,
        TRAY_IDENTITY_LABEL,
        TRAY_MENU_STRUCTURE,
        TRAY_TOOLTIP_TEXT,
        WINDOWS_TRAY_VISIBILITY_LIMITATION,
        build_monitoring_hud_route_model,
        build_optional_feature_route_state_model,
        build_resident_access_menu_plan,
        normalize_resident_access_settings,
    )

    plan = build_resident_access_menu_plan()
    immutable_ids = [route["routeId"] for route in plan["immutableRoutes"]]
    quick_ids = [route["routeId"] for route in plan["quickSlots"]]
    route_owner = {route["routeId"]: route["ownerFamily"] for route in plan["immutableRoutes"]}
    menu_structure = plan["menuStructure"]

    assert_true(TRAY_IDENTITY_LABEL == "Nexus Desktop AI", "tray identity label drifted", failures)
    assert_true(
        TRAY_TOOLTIP_TEXT.startswith("Nexus Desktop AI - ")
        and "Provider-visible data: none" in TRAY_TOOLTIP_TEXT,
        "tray icon hover tooltip must carry compact FAM-003 resident AI/privacy status",
        failures,
    )
    assert_true(tuple(immutable_ids) == IMMUTABLE_ROUTE_IDS, "immutable route order drifted", failures)
    assert_true(
        set(IMMUTABLE_ROUTE_IDS)
        == {
            "global_settings",
            "hud_dashboard",
            "ai_status_command_center",
            "exit_nexus",
        },
        "immutable route set is incomplete",
        failures,
    )
    assert_true(
        immutable_ids[0] == "global_settings",
        f"Global Settings must be the first immutable command route: {immutable_ids}",
        failures,
    )
    assert_true(route_owner.get("hud_dashboard") == "FAM-006", "HUD Dashboard owner must remain FAM-006", failures)
    assert_true(
        plan["hudState"]["routeState"] == OPTIONAL_FEATURE_ROUTE_UNKNOWN,
        f"default missing HUD route state must hide as unknown optional route: {plan['hudState']}",
        failures,
    )
    assert_true(
        plan["hudState"]["visibleInActiveMenu"] is False
        and plan["hudState"]["enabledInActiveMenu"] is False,
        f"default HUD route must be hidden from active menu: {plan['hudState']}",
        failures,
    )
    assert_true(
        route_owner.get("ai_status_command_center") == "FAM-007",
        "AI Status / Command Center owner must remain FAM-007",
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
        and "Provider-visible data: none" in str(plan.get("tooltipText", ""))
        and "Provider-visible data: none" in str(plan.get("statusLabel", "")),
        "resident access plan must carry compact AI/privacy status in both tray icon hover tooltip and visible status label",
        failures,
    )
    assert_true(
        TRAY_MENU_STRUCTURE["nativeStatusRow"] is False
        and menu_structure["nativeStatusRow"] is False,
        "native tray menu must not carry a long status/header row",
        failures,
    )
    assert_true(
        tuple(menu_structure["topLevel"]) == ("Global Settings", "Quick Access", "AI", "Exit Nexus Desktop AI"),
        f"native tray menu top-level structure drifted: {menu_structure['topLevel']}",
        failures,
    )
    assert_true(
        tuple(menu_structure["quickAccessMenu"]) == DEFAULT_QUICK_SLOT_ROUTE_IDS
        or tuple(menu_structure["quickAccessMenu"])
        == ("Open Command Overlay", "Create Custom Task", "Open Saved Actions Folder"),
        f"Quick Access submenu structure drifted: {menu_structure['quickAccessMenu']}",
        failures,
    )
    assert_true(
        tuple(menu_structure["aiMenu"]) == ("AI Status / Command Center",),
        f"AI submenu structure drifted: {menu_structure['aiMenu']}",
        failures,
    )
    assert_true(
        tuple(menu_structure["deferredOwnerMenus"]) == ("Developer", "Owner")
        and "Deferred to FAM-007" in menu_structure["developerOwnerDisposition"],
        "Developer/Owner tray categories must remain deferred to FAM-007 planning",
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

    state_matrix = {
        OPTIONAL_FEATURE_ROUTE_ENABLED_AVAILABLE: (True, True),
        OPTIONAL_FEATURE_ROUTE_ENABLED_TEMPORARILY_BLOCKED: (True, False),
        OPTIONAL_FEATURE_ROUTE_ENABLED_ERRORED: (True, False),
        OPTIONAL_FEATURE_ROUTE_ENABLED_NOT_READY: (True, False),
        OPTIONAL_FEATURE_ROUTE_DISABLED_BY_USER: (False, False),
        OPTIONAL_FEATURE_ROUTE_NOT_INSTALLED: (False, False),
        OPTIONAL_FEATURE_ROUTE_UNSUPPORTED: (False, False),
        OPTIONAL_FEATURE_ROUTE_UNKNOWN: (False, False),
    }
    for state_id, (expected_visible, expected_enabled) in state_matrix.items():
        model = build_optional_feature_route_state_model(
            raw_state=state_id,
            feature_enabled=state_id.startswith("enabled"),
            reason="Owner-bounded reason",
        )
        assert_true(
            model["visibleInActiveMenu"] is expected_visible
            and model["enabledInActiveMenu"] is expected_enabled,
            f"optional feature state model drifted for {state_id}: {model}",
            failures,
        )

    for state_id in (
        OPTIONAL_FEATURE_ROUTE_DISABLED_BY_USER,
        OPTIONAL_FEATURE_ROUTE_NOT_INSTALLED,
        OPTIONAL_FEATURE_ROUTE_UNSUPPORTED,
        OPTIONAL_FEATURE_ROUTE_UNKNOWN,
    ):
        hud_model = build_monitoring_hud_route_model(
            {
                "feature_enabled": False,
                "resident_route_state": state_id,
                "resident_route_reason": "Owner-bounded reason",
            }
        )
        assert_true(
            hud_model["visibleInActiveMenu"] is False,
            f"HUD {state_id} must hide tray/menu rows: {hud_model}",
            failures,
        )

    blocked_hud_model = build_monitoring_hud_route_model(
        {
            "feature_enabled": True,
            "resident_route_state": OPTIONAL_FEATURE_ROUTE_ENABLED_TEMPORARILY_BLOCKED,
            "resident_route_reason": "Dashboard is warming up",
        }
    )
    assert_true(
        blocked_hud_model["visibleInActiveMenu"] is True
        and blocked_hud_model["enabledInActiveMenu"] is False
        and blocked_hud_model["disabledWithReason"] is True
        and blocked_hud_model["ownerBoundedReason"] == "Dashboard is warming up",
        f"temporarily blocked HUD route must show disabled with reason: {blocked_hud_model}",
        failures,
    )


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
        "_monitoring_hud_route_model",
        "_monitoring_hud_dashboard_menu_text",
        "route_hidden",
        "route_unavailable",
        "request_global_settings_from_tray",
        "request_ai_status_from_tray",
        "TRAY_AI_STATUS_COMMAND_CENTER_ROUTED",
        "request_privacy_lockdown_from_tray",
        "request_quick_slot_from_tray",
        "TRAY_RESIDENT_ACCESS_ACTIONS_REFRESHED",
        "_resident_menu_identity_text",
        "self.quick_access_menu = self.tray_menu.addMenu(\"Quick Access\")",
        "self.ai_menu = self.tray_menu.addMenu(\"AI\")",
        "parent_menu=self.quick_access_menu",
        "parent_menu=self.ai_menu",
        "MF_POPUP",
        "append_submenu(menu, quick_access_menu, \"Quick Access\", True)",
        "append_submenu(menu, ai_menu, \"AI\", True)",
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
    assert_true(
        'self.global_settings_action = self._add_button_action(' in tray_text
        and tray_text.index('self.global_settings_action = self._add_button_action(')
        < tray_text.index('self.quick_access_menu = self.tray_menu.addMenu("Quick Access")')
        < tray_text.index('self.ai_menu = self.tray_menu.addMenu("AI")')
        < tray_text.index('self.monitoring_hud_primary_action = self._add_button_action(')
        and tray_text.index('append(menu, 110, "Global Settings", True)')
        < tray_text.index('append_submenu(menu, quick_access_menu, "Quick Access", True)')
        < tray_text.index('append_submenu(menu, ai_menu, "AI", True)')
        < tray_text.index('if hud_route_visible:'),
        "Global Settings and Quick Access must lead the native tray/menu command order",
        failures,
    )
    assert_true(
        'self.global_settings_button = self.tray_popup.add_button(' in tray_text
        and tray_text.index('self.global_settings_button = self.tray_popup.add_button(')
        < tray_text.index('self.quick_slot_buttons.append(button)')
        < tray_text.index('self.ai_status_button = self.tray_popup.add_button(')
        < tray_text.index('self.monitoring_hud_status_label = QLabel('),
        "Global Settings and Quick Access must lead the resident fallback popup order",
        failures,
    )
    assert_true(
        "app.setWindowIcon(build_resident_tray_icon())" in main_text,
        "runtime QApplication must bind the branch-local resident icon for taskbar/window identity proof",
        failures,
    )
    assert_true(
        "_native_menu_status_text" not in tray_text
        and "append(80," not in tray_text
        and "nativeStatusRow\": False" not in tray_text,
        "native tray menu must not keep a long status/header row implementation",
        failures,
    )
    assert_true(
        'self.privacy_lockdown_action = self._add_button_action(' not in tray_text
        and 'self.privacy_lockdown_button = self.tray_popup.add_button(' not in tray_text
        and 'append(130, "Privacy Lockdown"' not in tray_text
        and "130: self.request_privacy_lockdown_from_tray" not in tray_text,
        "Privacy Lockdown must not appear as a top-level tray/menu action until FAM-007 admits a real immediate action",
        failures,
    )
    assert_true(
        'append(100, "Enable HUD Feature"' not in tray_text
        and "append(100, feature_text" not in tray_text,
        "native tray menu must not expose a forced Enable HUD Feature row",
        failures,
    )
    assert_true(
        "settings_owned_optional_feature_configuration" in tray_text,
        "tray HUD toggle fallback must redirect to settings-owned optional feature configuration",
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
        "setMinimumSize(820, 520)",
        "surfaceClassification\", \"Nexus-Owned Product Surface",
        "settingsInformationArchitecture\", \"left-navigation-active-settings-only",
        "residentAccessSettingsWindowControls",
        "residentAccessSettingsChromeMinimize",
        "residentAccessSettingsChromeClose",
        "residentAccessSettingsNavShell",
        "residentAccessSettingsNavButton",
        "Only active settings are shown.",
        "setMinimumWidth(300)",
        "Quick Access",
        "slot_count_badge",
        "residentAccessSettingsSlotCount",
        "residentAccessSettingsFooter",
        "Stage Default Quick Access Slots",
        "Stage Defaults",
        "residentAccessQuickSlotActions",
        "residentAccessQuickSlotMoveUp",
        "residentAccessQuickSlotMoveDown",
        "residentAccessQuickSlotRemove",
        "Top to bottom becomes the tray submenu order.",
        "Core tray commands stay fixed",
        "Save Changes",
        "Discard Changes",
        "Keep Editing",
        "def _has_unsaved_changes",
        "def closeEvent",
        "RESIDENT_ACCESS_PRIVACY_LOCKDOWN_ROUTE_ONLY",
    ):
        assert_true(token in renderer_text, f"renderer resident access token missing: {token}", failures)

    for token in (
        "Connected Surfaces",
        "connected_surfaces",
        "Move Up",
        "Move Down",
        "Reset Quick Access",
        "setMinimumSize(700, 460)",
        "setMinimumSize(680, 408)",
        "Tray hover status:",
        "Provider-visible data: none",
        "Privacy Lockdown remains future-gated",
        '("quick_access", "Resident Access")',
        '("ai_status", "AI Status")',
        '("privacy", "Privacy / Trust")',
        '("tray_visibility", "Tray Visibility")',
        '("owner_routes", "Owner Routes")',
    ):
        assert_true(
            token not in renderer_text,
            f"Global Settings must not present stale fake settings category token: {token}",
            failures,
        )

    resident_settings_tooltip_tokens = (
        "Open the {label} settings section.",
        "Add one compact quick-access slot.",
        "Restore the default quick-access slots.",
        "Save Resident Access quick-slot settings.",
        "Close Global Settings.",
        "Select the route for quick-access slot",
        "Move quick-access slot",
        "Remove quick-access slot",
    )
    for token in resident_settings_tooltip_tokens:
        assert_true(
            token not in renderer_text,
            f"FAM-003 resident settings tooltip text must stay suppressed until readable tooltip styling is admitted: {token}",
            failures,
        )

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
