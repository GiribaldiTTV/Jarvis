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


def _write_artifact_ledger(log_dir: Path, artifacts: list[dict[str, str]], rows: list[tuple[str, bool, str]]) -> tuple[Path, Path]:
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

    manifest_path = log_dir / "fam003_settings_visual_fail_repair_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "surface": "Global Settings / Quick Access",
                "proofClass": "supporting-focused-visual-proof-user-retest-required",
                "artifactCount": len(artifacts),
                "allChecksPass": all(ok for _name, ok, _detail in rows),
                "artifacts": artifacts,
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
    return ledger_path, manifest_path


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
            default_ok and 800 <= width <= 850 and 510 <= height <= 545,
            f"{default_path} ({width}x{height})",
        )
    )
    rows.append(
        (
            "global settings shell geometry",
            800 <= width <= 850 and 510 <= height <= 545,
            f"window={width}x{height}; required left-nav shell must not collapse to old Quick Access-only dialog",
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
            and dialog.chrome_bar.control_cluster.objectName() == "residentAccessSettingsWindowControls"
            and dialog.chrome_bar.minimize_button.isVisible()
            and dialog.chrome_bar.close_button.isVisible()
            and not dialog.chrome_bar.maximize_button.isVisible()
            and dialog.chrome_bar.close_button.accessibleName() == "Close Global Settings",
            f"{chrome_path} ({chrome_width}x{chrome_height}); cluster={dialog.chrome_bar.control_cluster.objectName()!r}; minimize={dialog.chrome_bar.minimize_button.isVisible()}; close={dialog.chrome_bar.close_button.isVisible()}; maximize_visible={dialog.chrome_bar.maximize_button.isVisible()}",
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
            and set(dialog._nav_buttons) == {"quick_access"}
            and "Only active settings are shown." in dialog.nav_detail.text(),
            f"{nav_path} ({nav_width}x{nav_height}); nav={list(dialog._nav_buttons)}; checked={dialog.quick_access_nav_button.isChecked()}",
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
            and set(dialog._nav_buttons) == {"quick_access"}
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and dialog.quick_access_nav_button.isChecked()
            and dialog.slot_count_badge.text() == "2/5 slots"
            and dialog.quick_slot_container.objectName() == "residentAccessQuickSlotContainer"
            and dialog.footer_frame.objectName() == "residentAccessSettingsFooter"
            and "Connected Surfaces" not in button_texts
            and "Connected Surfaces" not in dialog.section_detail.text()
            and "Connected Surfaces" not in dialog.route_summary.text(),
            f"heading={dialog.section_heading.text()!r}; badge={dialog.slot_count_badge.text()!r}; nav={list(dialog._nav_buttons)}; buttons={button_texts}",
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
        "No pending Quick Access changes." in dialog.change_summary.text()
        and not dialog.save_button.isEnabled()
        and not dialog.revert_button.isEnabled(),
        f"change_summary={dialog.change_summary.text()!r}",
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
            and "Default Quick Access slots are staged" in dialog.change_summary.text(),
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

    ledger_path, manifest_path = _write_artifact_ledger(log_dir, artifacts, rows)
    rows.append(("artifact-to-surface ledger written", ledger_path.exists() and manifest_path.exists(), f"{ledger_path}; {manifest_path}"))
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
