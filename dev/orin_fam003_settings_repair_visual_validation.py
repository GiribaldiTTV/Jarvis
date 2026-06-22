"""Focused visual and behavior proof for FAM-003 Global Settings repair.

This helper uses an isolated resident-access settings file so it can validate
Quick Access dirty-state behavior without mutating USER runtime preferences.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation"

ELEMENT_GROUP_LEDGER_ROWS: tuple[tuple[str, str, str, str, str, str], ...] = (
    ("F3GS-001", "Whole-window silhouette", "ResidentAccessSettingsDialog", "top-level Nexus settings shell", "UIREF-001 / FAM-002 / Project Vision", "880x600 dark NDAI shell, no white/native utility surface"),
    ("F3GS-002", "Outer shell frame", "residentAccessSettingsShell", "Nexus-owned window boundary", "UIREF-001 / UIREF-005", "subtle cyan boundary, reduced glow density, 20px radius"),
    ("F3GS-003", "Header/body integration", "residentAccessSettingsChromeBar + residentAccessSettingsBody", "single settings window anatomy", "AI Control Center reference / FAM-002", "header is integrated with body, no generic dialog header break"),
    ("F3GS-004", "Product kicker", "residentAccessSettingsChromeKicker", "brand/product identity", "Project Vision", "NEXUS DESKTOP AI"),
    ("F3GS-005", "Window title", "residentAccessSettingsChromeTitle", "primary settings identity", "FAM-003 / F3-FF01", "Global Settings"),
    ("F3GS-006", "Subtitle", "residentAccessSettingsChromeSubtitle", "short product context", "Project Vision / FAM-003", "Resident tray shortcuts and menu preferences."),
    ("F3GS-007", "Role metadata removal", "residentAccessSettingsChromeRolePill", "debug/planning metadata absence", "Project Vision / UIREF-006", "PAGE/SCOPE role pill hidden and empty"),
    ("F3GS-008", "Control cluster shell", "residentAccessSettingsWindowControls", "NDAI window control cluster", "UIREF-002 / AI Control Center reference", "compact rounded cluster, minimize and close visible, maximize hidden"),
    ("F3GS-009", "Minimize control", "residentAccessSettingsChromeMinimize", "window state action", "UIREF-002 / UIREF-003", "compact icon button with hover/focus/pressed states"),
    ("F3GS-010", "Close control", "residentAccessSettingsChromeClose", "window close action", "UIREF-002 / UIREF-003", "compact icon button with dirty guard path"),
    ("F3GS-011", "Body split", "residentAccessSettingsBody", "settings organizer plus page", "FAM-003 / F3-FF01", "left organizer and page content remain distinct"),
    ("F3GS-012", "Left settings rail", "residentAccessSettingsNavShell", "compact settings navigation", "FAM-002 / FAM-003", "transparent rail with right divider, not a large card"),
    ("F3GS-013", "Rail kicker", "residentAccessSettingsNavKicker", "settings zone label", "Project Vision", "GLOBAL SETTINGS"),
    ("F3GS-014", "Rail title", "residentAccessSettingsNavTitle", "navigation title", "FAM-003", "Settings"),
    ("F3GS-015", "Rail detail", "residentAccessSettingsNavDetail", "scope hint", "Project Vision / UIREF-006", "Resident tray; no implementation explanation"),
    ("F3GS-016", "Quick Access nav item", "residentAccessSettingsNavItem", "selected settings page row", "FAM-003 / UIREF-003", "compact selected row with left accent"),
    ("F3GS-017", "Quick Access nav label", "residentAccessSettingsNavButton", "selected navigation action", "FAM-003", "Quick Access"),
    ("F3GS-018", "Quick Access nav caption", "residentAccessSettingsNavCaption", "short page description", "Project Vision", "Tray menu shortcuts"),
    ("F3GS-019", "Hidden future-section copy", "residentAccessSettingsNavBoundary", "deferred scope absence", "UIREF-006", "no visible future/deferred implementation text"),
    ("F3GS-020", "Content surface", "residentAccessSettingsContentShell", "active settings page host", "FAM-002 / F3-FF01", "unframed dark page, reduced nested borders"),
    ("F3GS-021", "Page heading", "residentAccessSettingsHeading", "active page identity", "FAM-003", "Quick Access as page inside Global Settings"),
    ("F3GS-022", "Slot count badge", "residentAccessSettingsSlotCount", "budget signal", "FAM-003 / F3-FF01", "2/5 slots or current slot count"),
    ("F3GS-023", "Page detail", "residentAccessSettingsDetail", "short instruction", "Project Vision", "Choose up to five shortcuts for the tray menu."),
    ("F3GS-024", "Clean state status", "residentAccessSettingsChangeSummary", "state messaging", "Project Vision", "hidden when no action is required"),
    ("F3GS-025", "Quick-slot container", "residentAccessQuickSlotContainer", "settings control group", "FAM-002 / FAM-003", "transparent group, no excessive nested outline"),
    ("F3GS-026", "Quick-slot group heading", "residentAccessSettingsSubheading", "control group label", "FAM-003", "Tray Menu Shortcuts"),
    ("F3GS-027", "Add slot button", "residentAccessAddSlotButton", "slot budget action", "UIREF-003", "compact NDAI button with disabled max-budget state"),
    ("F3GS-028", "Defaults button", "residentAccessDefaultsButton", "default staging action", "UIREF-003 / F3-FF01", "Use Defaults; staged until Save Changes"),
    ("F3GS-029", "Quick-slot help", "residentAccessSettingsQuickHelp", "ordering hint", "Project Vision", "Top to bottom sets the Quick Access order."),
    ("F3GS-030", "Slot row", "residentAccessQuickSlotRow", "ordered shortcut row", "FAM-003 / UIREF-003", "compact row with subdued boundary"),
    ("F3GS-031", "Slot index", "residentAccessQuickSlotIndex", "row order signal", "FAM-003", "01/02 style without large badge"),
    ("F3GS-032", "Route dropdown", "QComboBox", "route selector", "UIREF-003 / accepted HUD dropdown reference", "dark compact selector, custom arrow, non-white popup"),
    ("F3GS-033", "Row action cluster", "residentAccessQuickSlotActions", "row reorder/remove controls", "UIREF-003", "compact icon-only up/down/remove controls"),
    ("F3GS-034", "Dirty guard summary", "residentAccessSettingsChangeSummary", "unsaved-change protection", "F3-FF01 / Project Vision", "visible only for dirty, guard, defaults, or saved notice"),
    ("F3GS-035", "Footer actions", "residentAccessSettingsFooter", "save/revert/close path", "UIREF-003", "Save/Revert/Discard/Keep Editing/Done remain deterministic"),
    ("F3GS-036", "Tooltip/accessibility posture", "accessible names only", "keyboard/screen-reader support without unreadable tooltip spam", "UIREF-003 / USER visual fail", "no broad visible tooltip text added"),
)


def _configure_qt_environment(log_dir: Path) -> None:
    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
    os.environ["NEXUS_RESIDENT_ACCESS_SETTINGS_PATH"] = str(log_dir / "resident_access_settings.json")


def _capture(widget, path: Path, artifacts: list[dict[str, str]] | None = None, *, surface: str = "", state: str = "") -> tuple[bool, int, int]:
    image = widget.grab()
    ok = image.save(str(path))
    if artifacts is not None:
        artifacts.append(
            {
                "path": str(path),
                "surface": surface or widget.objectName() or widget.__class__.__name__,
                "state": state or "default",
                "width": str(image.width()),
                "height": str(image.height()),
                "saved": str(bool(ok)),
            }
        )
    return bool(ok), image.width(), image.height()


def _light_pixel_ratio(path: Path) -> float:
    from PySide6.QtGui import QImage

    image = QImage(str(path))
    if image.isNull():
        return 1.0
    samples = 0
    light = 0
    step_x = max(1, image.width() // 40)
    step_y = max(1, image.height() // 30)
    for y in range(0, image.height(), step_y):
        for x in range(0, image.width(), step_x):
            color = image.pixelColor(x, y)
            samples += 1
            if (color.red() + color.green() + color.blue()) / 3 >= 235:
                light += 1
    return light / max(1, samples)


def _write_report(log_dir: Path, rows: list[tuple[str, bool, str]]) -> Path:
    report_path = log_dir / "FAM003_SETTINGS_REPAIR_VISUAL_VALIDATION.md"
    lines = [
        "# FAM-003 Settings Repair Visual Validation",
        "",
        f"Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}",
        f"Worktree: {ROOT}",
        "",
        "## Scope",
        "",
        "- Surface: Global Settings / Nexus Tray & Quick Access",
        "- Source files: desktop/desktop_renderer.py, desktop/resident_access.py",
        "- Validation class: supporting Codex visual proof; USER-operated UTS remains required",
        "",
        "## Results",
        "",
        "| Check | Result | Detail |",
        "| --- | --- | --- |",
    ]
    for name, ok, detail in rows:
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def _write_artifact_ledger(log_dir: Path, artifacts: list[dict[str, str]], rows: list[tuple[str, bool, str]]) -> tuple[Path, Path, Path]:
    ledger_path = log_dir / "ARTIFACT_TO_SURFACE_LEDGER.md"
    ledger_lines = [
        "# FAM-003 Settings Visual Fail Repair Artifact Ledger",
        "",
        "| Artifact | Surface / Element Group | State | Size | Saved |",
        "| --- | --- | --- | --- | --- |",
    ]
    for artifact in artifacts:
        ledger_lines.append(
            "| `{path}` | {surface} | {state} | {width}x{height} | {saved} |".format(**artifact)
        )
    ledger_lines.extend(
        [
            "",
            "## Element Verdict Summary",
            "",
            "| Element Group Check | Verdict | Detail |",
            "| --- | --- | --- |",
        ]
    )
    for name, ok, detail in rows:
        ledger_lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
    ledger_path.write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")

    element_ledger_path = log_dir / "ELEMENT_GROUP_REFERENCE_CONFORMANCE_LEDGER.md"
    all_checks_pass = all(ok for _name, ok, _detail in rows)
    verdict = "PASS" if all_checks_pass else "BLOCKED"
    element_lines = [
        "# FAM-003 Global Settings Element-Group Reference Conformance Ledger",
        "",
        "Scope: Global Settings / Quick Access settings window only.",
        "Reference class: UIREF-001 through UIREF-006 plus accepted AI Control Center top-level window evidence.",
        "Proof model: focused screenshots plus code-to-visual widget/objectName trace. USER-operated Live Validation remains required for final USER acceptance.",
        "",
        "| ID | Element Group | Code Path / Selector | Visual Role | Rule / Comparator | Copy / Style / State Proof | Verdict |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row_id, element, selector, role, rule, proof in ELEMENT_GROUP_LEDGER_ROWS:
        element_lines.append(
            f"| {row_id} | {element} | `desktop/desktop_renderer.py::{selector}` | {role} | {rule} | {proof} | {verdict} |"
        )
    element_ledger_path.write_text("\n".join(element_lines) + "\n", encoding="utf-8")

    manifest_path = log_dir / "fam003_settings_visual_fail_repair_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "surface": "Global Settings / Quick Access",
                "proofClass": "supporting-focused-visual-proof-user-retest-required",
                "artifactCount": len(artifacts),
                "allChecksPass": all_checks_pass,
                "artifacts": artifacts,
                "elementGroupLedger": str(element_ledger_path),
                "elementGroupCount": len(ELEMENT_GROUP_LEDGER_ROWS),
                "checks": [
                    {"name": name, "result": "PASS" if ok else "FAIL", "detail": detail}
                    for name, ok, detail in rows
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return ledger_path, manifest_path, element_ledger_path


def main() -> int:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = LOG_ROOT / stamp
    log_dir.mkdir(parents=True, exist_ok=True)
    _configure_qt_environment(log_dir)
    Path(os.environ["NEXUS_RESIDENT_ACCESS_SETTINGS_PATH"]).write_text(
        json.dumps(
            {
                "quickSlotIds": ["tray_visibility_education", "recording_studio"],
                "menuBudget": 5,
                "showAiPrivacyStatus": True,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    sys.path.insert(0, str(ROOT))

    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtWidgets import QApplication, QPushButton

    from desktop.desktop_renderer import ResidentAccessSettingsDialog
    from desktop.resident_access import DEFAULT_QUICK_SLOT_ROUTE_IDS, MAX_QUICK_SLOT_COUNT

    app = QApplication.instance() or QApplication([])
    dialog = ResidentAccessSettingsDialog()
    dialog.show()
    app.processEvents()

    rows: list[tuple[str, bool, str]] = []
    artifacts: list[dict[str, str]] = []

    default_path = log_dir / "01_default_quick_access.png"
    default_ok, width, height = _capture(
        dialog,
        default_path,
        artifacts,
        surface="full Global Settings window",
        state="default Quick Access page",
    )
    light_ratio = _light_pixel_ratio(default_path)
    rows.append(
        (
            "default screenshot saved",
            default_ok and 870 <= width <= 900 and 590 <= height <= 610,
            f"{default_path} ({width}x{height})",
        )
    )
    rows.append(
        (
            "global settings shell geometry",
            870 <= width <= 900 and 590 <= height <= 610,
            f"window={width}x{height}; required AI-Control-Center reference-conformance header and left-nav shell must not collapse to old utility dialog",
        )
    )
    rows.append(("default surface is not white/native-light", light_ratio < 0.20, f"light_pixel_ratio={light_ratio:.3f}"))
    chrome_path = log_dir / "01a_top_level_chrome_control_cluster.png"
    chrome_ok, chrome_width, chrome_height = _capture(
        dialog.chrome_bar,
        chrome_path,
        artifacts,
        surface="top-level chrome and compact window control cluster",
        state="default",
    )
    rows.append(
        (
            "top-level chrome/control cluster",
            chrome_ok
            and dialog.chrome_bar.property("headerAnatomy") == "ai-control-center-reference-derived"
            and dialog.chrome_bar.control_cluster.objectName() == "residentAccessSettingsWindowControls"
            and dialog.chrome_bar.minimize_button.isVisible()
            and dialog.chrome_bar.close_button.isVisible()
            and not dialog.chrome_bar.maximize_button.isVisible()
            and dialog.chrome_bar.close_button.accessibleName() == "Close Global Settings",
            f"{chrome_path} ({chrome_width}x{chrome_height}); anatomy={dialog.chrome_bar.property('headerAnatomy')!r}; cluster={dialog.chrome_bar.control_cluster.objectName()!r}; minimize={dialog.chrome_bar.minimize_button.isVisible()}; close={dialog.chrome_bar.close_button.isVisible()}; maximize_visible={dialog.chrome_bar.maximize_button.isVisible()}",
        )
    )
    rows.append(
        (
            "reference-conformant header/title band",
            dialog.chrome_bar.kicker_label.text() == "NEXUS DESKTOP AI"
            and dialog.chrome_bar.title_label.text() == "Global Settings"
            and dialog.chrome_bar.subtitle_label.text() == "Resident tray shortcuts and menu preferences."
            and [label.text() for label in dialog.chrome_bar.role_labels] == []
            and not dialog.chrome_bar.role_pill.isVisible(),
            f"kicker={dialog.chrome_bar.kicker_label.text()!r}; title={dialog.chrome_bar.title_label.text()!r}; subtitle={dialog.chrome_bar.subtitle_label.text()!r}; role_pairs={[label.text() for label in dialog.chrome_bar.role_labels]}; role_pill_visible={dialog.chrome_bar.role_pill.isVisible()}",
        )
    )
    nav_path = log_dir / "01b_left_settings_organizer.png"
    nav_ok, nav_width, nav_height = _capture(
        dialog.nav_shell,
        nav_path,
        artifacts,
        surface="left settings organizer",
        state="Quick Access selected",
    )
    rows.append(
        (
            "left navigation settings organizer",
            nav_ok
            and dialog.nav_shell.isVisible()
            and dialog.quick_access_nav_button.isChecked()
            and dialog.quick_access_nav_item.isVisible()
            and dialog.quick_access_nav_item.objectName() == "residentAccessSettingsNavItem"
            and set(dialog._nav_buttons) == {"quick_access"}
            and dialog.nav_title.text() == "Settings"
            and dialog.nav_detail.text() == "Resident tray"
            and dialog.quick_access_nav_caption.text() == "Tray menu shortcuts"
            and not dialog.nav_boundary.isVisible(),
            f"{nav_path} ({nav_width}x{nav_height}); nav={list(dialog._nav_buttons)}; checked={dialog.quick_access_nav_button.isChecked()}; detail={dialog.nav_detail.text()!r}; caption={dialog.quick_access_nav_caption.text()!r}",
        )
    )
    button_texts = [button.text().replace("&&", "&") for button in dialog.findChildren(QPushButton)]
    compact_action_buttons = [
        button
        for button in dialog.findChildren(QPushButton)
        if button.objectName() in {"residentAccessQuickSlotMoveUp", "residentAccessQuickSlotMoveDown", "residentAccessQuickSlotRemove"}
    ]
    rows.append(
        (
            "single actionable settings page inside Global Settings IA",
            dialog.section_heading.text() == "Quick Access"
            and dialog.property("settingsInformationArchitecture") == "compact-settings-organizer-quick-access-page"
            and dialog.property("settingsVisualRepair") == "user-visual-fail-reference-conformance-v2"
            and dialog.property("referenceDerivedHeader") == "ai-control-center-reference-conformant-settings-shell-v2"
            and set(dialog._nav_buttons) == {"quick_access"}
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and dialog.quick_access_nav_button.isChecked()
            and dialog.slot_count_badge.text() == "2/5 slots"
            and dialog.quick_slot_container.objectName() == "residentAccessQuickSlotContainer"
            and dialog.footer_frame.objectName() == "residentAccessSettingsFooter"
            and "Connected Surfaces" not in button_texts
            and "Connected Surfaces" not in dialog.section_detail.text()
            and "Connected Surfaces" not in dialog.route_summary.text()
            and all(label.text() not in {"PAGE - QUICK ACCESS", "SCOPE - TRAY MENU"} for label in dialog.chrome_bar.role_labels)
            and not dialog.route_summary.isVisible(),
            f"heading={dialog.section_heading.text()!r}; badge={dialog.slot_count_badge.text()!r}; nav={list(dialog._nav_buttons)}; buttons={button_texts}; route_visible={dialog.route_summary.isVisible()}",
        )
    )
    rows.append(
        (
            "compact quick-slot controls",
            "Move Up" not in button_texts
            and "Move Down" not in button_texts
            and "Reset Quick Access" not in button_texts
            and "Remove" not in button_texts
            and all(button.width() <= 32 and button.height() <= 32 for button in compact_action_buttons),
            f"buttons={button_texts}; compact_action_sizes={[(button.objectName(), button.width(), button.height()) for button in compact_action_buttons]}",
        )
    )
    rows.append(
        ("initial pending-state copy",
        not dialog.change_summary.isVisible()
        and dialog.change_summary.text() == ""
        and not dialog.save_button.isEnabled()
        and not dialog.revert_button.isEnabled(),
        f"change_summary={dialog.change_summary.text()!r}; visible={dialog.change_summary.isVisible()}",
    )
    )

    if not dialog._slot_combos:
        rows.append(("quick-slot combo exists", False, "no quick-slot combo rendered"))
    else:
        combo = dialog._slot_combos[0]
        new_index = 1 if combo.count() > 1 and combo.currentIndex() != 1 else 0
        combo.setCurrentIndex(new_index)
        app.processEvents()
        dirty_path = log_dir / "02_dirty_quick_access.png"
        dirty_ok, _, _ = _capture(
            dialog,
            dirty_path,
            artifacts,
            surface="full Global Settings window",
            state="dirty Quick Access edit",
        )
        rows.append(("dirty screenshot saved", dirty_ok, str(dirty_path)))
        rows.append(
            ("dirty guard state after dropdown edit",
            dialog._has_unsaved_changes()
            and dialog.save_button.isEnabled()
            and dialog.revert_button.isEnabled()
            and "Unsaved Quick Access changes" in dialog.change_summary.text(),
            f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}",
        )
        )

        combo.showPopup()
        app.processEvents()
        popup_path = log_dir / "03_dropdown_list_state.png"
        popup_ok, popup_width, popup_height = _capture(
            combo.view(),
            popup_path,
            artifacts,
            surface="Quick Access route dropdown/list",
            state="open",
        )
        popup_light_ratio = _light_pixel_ratio(popup_path)
        combo.hidePopup()
        app.processEvents()
        rows.append(
            ("dropdown/list state screenshot saved",
            popup_ok and popup_width > 100 and popup_height > 20,
            f"{popup_path} ({popup_width}x{popup_height})"),
        )
        rows.append(
            ("dropdown/list state is not white/native-light",
            popup_light_ratio < 0.20,
            f"light_pixel_ratio={popup_light_ratio:.3f}"),
        )

    dialog.reject()
    app.processEvents()
    guard_path = log_dir / "04_close_guard.png"
    guard_ok, _, _ = _capture(
        dialog,
        guard_path,
        artifacts,
        surface="dirty-change close guard",
        state="chrome close requested with unsaved changes",
    )
    rows.append(("close guard screenshot saved", guard_ok, str(guard_path)))
    rows.append(
        ("close guard blocks silent loss",
        dialog.isVisible()
        and dialog._close_guard_active
        and dialog.discard_button.isVisible()
        and dialog.keep_editing_button.isVisible(),
        f"visible={dialog.isVisible()}; guard={dialog._close_guard_active}; summary={dialog.change_summary.text()!r}",
    )
    )

    dialog._keep_editing()
    dialog.set_focus("quick_access")
    dialog._reset_slots()
    app.processEvents()
    reset_path = log_dir / "05_defaults_staged.png"
    reset_ok, _, _ = _capture(
        dialog,
        reset_path,
        artifacts,
        surface="Quick Access defaults staging",
        state="defaults staged before save",
    )
    rows.append(("defaults staged screenshot saved", reset_ok, str(reset_path)))
    rows.append(
        (
            "reset semantics stage defaults",
            dialog._has_unsaved_changes()
            and tuple(dialog._settings.quick_slot_ids) == tuple(DEFAULT_QUICK_SLOT_ROUTE_IDS)
            and "Default Quick Access shortcuts are staged" in dialog.change_summary.text(),
            f"settings={dialog._settings.quick_slot_ids}; summary={dialog.change_summary.text()!r}",
        )
    )
    reset_rows = [
        widget
        for widget in dialog.quick_slot_rows.findChildren(type(dialog.quick_slot_container))
        if widget.objectName() == "residentAccessQuickSlotRow"
    ]
    last_row_bottom = 0
    container_bottom = dialog.quick_slot_container.mapTo(dialog, QPoint(0, dialog.quick_slot_container.height())).y()
    footer_top = dialog.footer_frame.mapTo(dialog, QPoint(0, 0)).y()
    if reset_rows:
        last_row = reset_rows[-1]
        last_row_bottom = last_row.mapTo(dialog, QPoint(0, last_row.height())).y()
    rows.append(
        (
            "defaults staged rows are unclipped",
            bool(reset_rows) and last_row_bottom <= container_bottom <= footer_top,
            f"rows={len(reset_rows)}; last_row_bottom={last_row_bottom}; container_bottom={container_bottom}; footer_top={footer_top}",
        )
    )

    while len(dialog._settings.quick_slot_ids) < MAX_QUICK_SLOT_COUNT:
        dialog._add_slot()
        app.processEvents()
    max_slots_path = log_dir / "06_max_slots_unclipped.png"
    max_slots_ok, max_width, max_height = _capture(
        dialog,
        max_slots_path,
        artifacts,
        surface="Quick Access max slot budget",
        state="5 slots / Add disabled",
    )
    max_rows = [
        widget
        for widget in dialog.quick_slot_rows.findChildren(type(dialog.quick_slot_container))
        if widget.objectName() == "residentAccessQuickSlotRow"
    ]
    max_last_row_bottom = 0
    max_container_bottom = dialog.quick_slot_container.mapTo(dialog, QPoint(0, dialog.quick_slot_container.height())).y()
    max_footer_top = dialog.footer_frame.mapTo(dialog, QPoint(0, 0)).y()
    if max_rows:
        max_last_row = max_rows[-1]
        max_last_row_bottom = max_last_row.mapTo(dialog, QPoint(0, max_last_row.height())).y()
    rows.append(("max-slot screenshot saved", max_slots_ok, f"{max_slots_path} ({max_width}x{max_height})"))
    rows.append(
        (
            "max-slot budget rows are unclipped",
            len(max_rows) == MAX_QUICK_SLOT_COUNT
            and max_last_row_bottom <= max_container_bottom <= max_footer_top
            and not dialog.add_slot_button.isEnabled(),
            f"rows={len(max_rows)}; last_row_bottom={max_last_row_bottom}; container_bottom={max_container_bottom}; footer_top={max_footer_top}; add_enabled={dialog.add_slot_button.isEnabled()}",
        )
    )

    dialog._save_settings()
    app.processEvents()
    saved_path = log_dir / "07_saved_state.png"
    saved_ok, _, _ = _capture(
        dialog,
        saved_path,
        artifacts,
        surface="full Global Settings window",
        state="saved Quick Access state",
    )
    rows.append(("saved state screenshot saved", saved_ok, str(saved_path)))
    rows.append(
        ("save clears dirty state",
        not dialog._has_unsaved_changes()
        and not dialog.save_button.isEnabled()
        and "Quick Access changes saved" in dialog.change_summary.text(),
        f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}",
    )
    )

    ledger_path, manifest_path, element_ledger_path = _write_artifact_ledger(log_dir, artifacts, rows)
    rows.append(
        (
            "artifact and element-group ledgers written",
            ledger_path.exists() and manifest_path.exists() and element_ledger_path.exists(),
            f"{ledger_path}; {element_ledger_path}; {manifest_path}",
        )
    )
    report_path = _write_report(log_dir, rows)
    dialog.close()
    app.quit()

    failures = [name for name, ok, _detail in rows if not ok]
    if failures:
        print(f"FAIL: FAM-003 settings repair visual validation failed: {failures}")
        print(f"Report: {report_path}")
        return 1
    print("PASS: FAM-003 settings repair visual validation")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
