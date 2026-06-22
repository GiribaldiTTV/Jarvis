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


def _capture(widget, path: Path) -> tuple[bool, int, int]:
    image = widget.grab()
    ok = image.save(str(path))
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

    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication, QPushButton

    from desktop.desktop_renderer import ResidentAccessSettingsDialog
    from desktop.resident_access import DEFAULT_QUICK_SLOT_ROUTE_IDS

    app = QApplication.instance() or QApplication([])
    dialog = ResidentAccessSettingsDialog()
    dialog.show()
    app.processEvents()

    rows: list[tuple[str, bool, str]] = []

    default_path = log_dir / "01_default_quick_access.png"
    default_ok, width, height = _capture(dialog, default_path)
    light_ratio = _light_pixel_ratio(default_path)
    rows.append(("default screenshot saved", default_ok and width >= 680 and height >= 430, f"{default_path} ({width}x{height})"))
    rows.append(("default surface is not white/native-light", light_ratio < 0.20, f"light_pixel_ratio={light_ratio:.3f}"))
    button_texts = [button.text().replace("&&", "&") for button in dialog.findChildren(QPushButton)]
    compact_action_buttons = [
        button
        for button in dialog.findChildren(QPushButton)
        if button.objectName() in {"residentAccessQuickSlotMoveUp", "residentAccessQuickSlotMoveDown", "residentAccessQuickSlotRemove"}
    ]
    rows.append(
        (
            "single actionable settings category",
            dialog.section_heading.text() == "Quick Access"
            and not dialog._nav_buttons
            and "Connected Surfaces" not in button_texts
            and "Connected Surfaces" not in dialog.section_detail.text()
            and "Connected Surfaces" not in dialog.route_summary.text(),
            f"heading={dialog.section_heading.text()!r}; nav={list(dialog._nav_buttons)}; buttons={button_texts}",
        )
    )
    rows.append(
        (
            "compact quick-slot controls",
            "Move Up" not in button_texts
            and "Move Down" not in button_texts
            and "Reset Quick Access" not in button_texts
            and all(button.width() <= 66 and button.height() <= 32 for button in compact_action_buttons),
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
        dirty_ok, _, _ = _capture(dialog, dirty_path)
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
        popup_ok, popup_width, popup_height = _capture(combo.view(), popup_path)
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
    guard_ok, _, _ = _capture(dialog, guard_path)
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
    reset_ok, _, _ = _capture(dialog, reset_path)
    rows.append(("defaults staged screenshot saved", reset_ok, str(reset_path)))
    rows.append(
        ("reset semantics stage defaults",
        dialog._has_unsaved_changes()
        and tuple(dialog._settings.quick_slot_ids) == tuple(DEFAULT_QUICK_SLOT_ROUTE_IDS)
        and "Default Quick Access slots are staged" in dialog.change_summary.text(),
        f"settings={dialog._settings.quick_slot_ids}; summary={dialog.change_summary.text()!r}",
    )
    )

    dialog._save_settings()
    app.processEvents()
    saved_path = log_dir / "06_saved_state.png"
    saved_ok, _, _ = _capture(dialog, saved_path)
    rows.append(("saved state screenshot saved", saved_ok, str(saved_path)))
    rows.append(
        ("save clears dirty state",
        not dialog._has_unsaved_changes()
        and not dialog.save_button.isEnabled()
        and "Quick Access changes saved" in dialog.change_summary.text(),
        f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}",
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
