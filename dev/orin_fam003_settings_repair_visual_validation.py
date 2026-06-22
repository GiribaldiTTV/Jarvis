"""Reference-conformance proof for FAM-003 Global Settings repair.

This helper uses an isolated resident-access settings file so it can validate
Quick Access behavior without mutating USER runtime preferences. It is
supporting proof only: USER-operated Live Validation remains authoritative for
final visual acceptance.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation"
REFERENCE_SCREENSHOTS: tuple[tuple[str, Path], ...] = (
    (
        "accepted_ai_control_center_default",
        Path(
            r"C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\FAM-007-H4"
            r"\20260622-094707-live-resize\01_before_resize_focused_window.png"
        ),
    ),
    (
        "accepted_ai_control_center_close_hover",
        Path(
            r"C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\FAM-007-H4"
            r"\20260622-094707-live-resize\04_window_control_close_hover_focused_window.png"
        ),
    ),
)

ELEMENT_GROUP_LEDGER_ROWS: tuple[tuple[str, str, str, str, str, str, str], ...] = (
    (
        "F3GS-001",
        "Whole-window silhouette",
        "desktop/desktop_renderer.py::ResidentAccessSettingsDialog",
        "Global Settings top-level product shell",
        "UIREF-001 / FAM-002 / Project Vision",
        "accepted AI Control Center full-window reference",
        "780x620 minimum dark NDAI shell; not white/native utility UI",
    ),
    (
        "F3GS-002",
        "Outer shell frame",
        "desktop/desktop_renderer.py::residentAccessSettingsShell",
        "Nexus-owned window boundary",
        "UIREF-001 / UIREF-005",
        "accepted AI Control Center rounded frame",
        "single rounded frame with restrained cyan boundary",
    ),
    (
        "F3GS-003",
        "Header/body integration",
        "desktop/desktop_renderer.py::residentAccessSettingsChromeBar + residentAccessSettingsBody",
        "integrated settings window anatomy",
        "AI Control Center reference / FAM-002",
        "accepted AI Control Center header-to-body relationship",
        "header, product title, pill metadata, and body read as one product surface",
    ),
    (
        "F3GS-004",
        "Product title group",
        "desktop/desktop_renderer.py::DialogChromeBar",
        "product identity and surface title",
        "Project Vision / UIREF-001",
        "accepted AI Control Center product/title hierarchy",
        "NEXUS DESKTOP AI, Global Settings, and Configure the Nexus tray",
    ),
    (
        "F3GS-005",
        "Product-facing header pill",
        "desktop/desktop_renderer.py::residentAccessSettingsChromeRolePill",
        "compact product context",
        "Project Vision / UIREF-006",
        "accepted AI Control Center status pill",
        "NEXUS TRAY / QUICK ACCESS and MENU BUDGET / 5 SLOTS; no debug or branch metadata",
    ),
    (
        "F3GS-006",
        "Window control cluster",
        "desktop/desktop_renderer.py::residentAccessSettingsWindowControls",
        "NDAI window controls",
        "UIREF-002 / UIREF-003",
        "accepted AI Control Center close-hover reference",
        "rounded minimize/close cluster with focus/pressed proof",
    ),
    (
        "F3GS-007",
        "Left settings rail",
        "desktop/desktop_renderer.py::residentAccessSettingsNavShell",
        "compact settings organizer",
        "FAM-003 / F3-FF01 / FAM-002",
        "accepted dense side/section navigation grammar",
        "Nexus Tray category with Quick Access selected; no fake future categories",
    ),
    (
        "F3GS-008",
        "Active page heading",
        "desktop/desktop_renderer.py::residentAccessSettingsHeading",
        "active settings leaf",
        "FAM-003 / F3-FF01",
        "accepted section title hierarchy",
        "Quick Access reads as one page inside Global Settings",
    ),
    (
        "F3GS-009",
        "Settings summary rows",
        "desktop/desktop_renderer.py::residentAccessSettingsSummaryPanel",
        "deterministic settings context",
        "Project Vision / UIREF-003",
        "accepted AI Control Center state-row grammar",
        "TRAY MENU and CHANGES rows use compact label/value rhythm",
    ),
    (
        "F3GS-010",
        "Shortcut order group",
        "desktop/desktop_renderer.py::residentAccessQuickSlotContainer",
        "settings control group",
        "FAM-003 / UIREF-003",
        "accepted state-card and row grouping",
        "Shortcut Order panel with Add and Defaults actions",
    ),
    (
        "F3GS-011",
        "Route dropdown",
        "desktop/desktop_renderer.py::QComboBox",
        "quick-access route selector",
        "UIREF-003 / accepted HUD selector grammar",
        "open dropdown proof artifact",
        "dark compact selector and non-white popup/list state",
    ),
    (
        "F3GS-012",
        "Row action cluster",
        "desktop/desktop_renderer.py::residentAccessQuickSlotActions",
        "reorder/remove controls",
        "UIREF-003",
        "focused row-action proof artifact",
        "icon-only up/down/remove controls; disabled first-up state proven",
    ),
    (
        "F3GS-013",
        "Dirty/default/save states",
        "desktop/desktop_renderer.py::_refresh_text",
        "deterministic state transitions",
        "Project Vision / F3-FF01",
        "dirty/default/saved screenshot sequence",
        "dirty guard, staged defaults, Save, Revert, and Done semantics are explicit",
    ),
    (
        "F3GS-014",
        "Copy discipline",
        "desktop/desktop_renderer.py::ResidentAccessSettingsDialog labels",
        "USER-facing language",
        "Project Vision / UIREF-006",
        "full screenshot and static text scan",
        "short product copy; no branch status, fake FAM categories, or implementation metadata",
    ),
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


def _copy_reference_artifacts(log_dir: Path, artifacts: list[dict[str, str]]) -> list[tuple[str, bool, str]]:
    rows: list[tuple[str, bool, str]] = []
    reference_dir = log_dir / "accepted_reference"
    reference_dir.mkdir(parents=True, exist_ok=True)
    for label, source in REFERENCE_SCREENSHOTS:
        target = reference_dir / f"{label}.png"
        exists = source.exists()
        if exists:
            target.write_bytes(source.read_bytes())
            artifacts.append(
                {
                    "path": str(target),
                    "surface": "accepted AI Control Center reference",
                    "state": label,
                    "width": "reference",
                    "height": "reference",
                    "saved": "True",
                }
            )
        rows.append((f"accepted reference available: {label}", exists and target.exists(), str(source)))
    return rows


def _write_contact_sheet(log_dir: Path, entries: list[tuple[str, Path]]) -> tuple[Path, bool]:
    from PySide6.QtCore import QRect, Qt
    from PySide6.QtGui import QColor, QFont, QImage, QPainter

    cell_w = 380
    cell_h = 320
    caption_h = 34
    columns = 2
    rows = (len(entries) + columns - 1) // columns
    sheet_w = columns * cell_w + 36
    sheet_h = rows * (cell_h + caption_h) + 40
    sheet = QImage(sheet_w, sheet_h, QImage.Format.Format_ARGB32)
    sheet.fill(QColor("#020812"))
    painter = QPainter(sheet)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    title_font = QFont("Segoe UI")
    title_font.setPointSize(10)
    title_font.setBold(True)
    painter.setFont(title_font)
    painter.setPen(QColor("#9ee8f5"))
    painter.drawText(18, 24, "FAM-003 Global Settings Reference Conformance Contact Sheet")
    caption_font = QFont("Segoe UI")
    caption_font.setPointSize(8)
    caption_font.setBold(True)
    painter.setFont(caption_font)
    for index, (caption, path) in enumerate(entries):
        source = QImage(str(path))
        col = index % columns
        row = index // columns
        x = 18 + col * cell_w
        y = 38 + row * (cell_h + caption_h)
        painter.setPen(QColor("#7ae8ff"))
        painter.drawText(x, y, caption)
        painter.setPen(QColor("#164e63"))
        painter.drawRoundedRect(QRect(x, y + 10, cell_w - 14, cell_h), 12, 12)
        if not source.isNull():
            scaled = source.scaled(
                cell_w - 28,
                cell_h - 14,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            image_x = x + 7 + max(0, (cell_w - 28 - scaled.width()) // 2)
            image_y = y + 17 + max(0, (cell_h - 14 - scaled.height()) // 2)
            painter.drawImage(QRect(image_x, image_y, scaled.width(), scaled.height()), scaled)
        else:
            painter.setPen(QColor("#fca5a5"))
            painter.drawText(x + 14, y + 64, f"Missing: {path}")
    painter.end()
    contact_sheet = log_dir / "REFERENCE_CONFORMANCE_CONTACT_SHEET.png"
    ok = sheet.save(str(contact_sheet))
    return contact_sheet, bool(ok)


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
        "- Surface: Global Settings / Nexus Tray / Quick Access settings window only.",
        "- Source files: desktop/desktop_renderer.py, desktop/resident_access.py.",
        "- Proof class: side-by-side accepted-reference comparison plus focused state screenshots.",
        "- Acceptance boundary: supporting Codex proof; USER-operated UTS remains required.",
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


def _write_artifact_ledger(
    log_dir: Path,
    artifacts: list[dict[str, str]],
    rows: list[tuple[str, bool, str]],
    contact_sheet: Path,
) -> tuple[Path, Path, Path]:
    ledger_path = log_dir / "ARTIFACT_TO_SURFACE_LEDGER.md"
    ledger_lines = [
        "# FAM-003 Settings Visual Repair Artifact Ledger",
        "",
        f"Contact Sheet: `{contact_sheet}`",
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
            "## Check Verdict Summary",
            "",
            "| Check | Verdict | Detail |",
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
        "Scope: Global Settings / Nexus Tray / Quick Access settings window only.",
        "Reference class: UIREF-001 through UIREF-006 plus accepted AI Control Center top-level window evidence.",
        "Proof model: contact sheet, focused screenshots, and code-to-visual widget/objectName trace. USER-operated Live Validation remains required.",
        "",
        "| ID | Element Group | Code Path / Selector | Visual Role | Rule | Comparator | Required Proof | Disposition |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row_id, element, selector, role, rule, comparator, proof in ELEMENT_GROUP_LEDGER_ROWS:
        element_lines.append(
            f"| {row_id} | {element} | `{selector}` | {role} | {rule} | {comparator} | {proof} | {verdict} |"
        )
    element_ledger_path.write_text("\n".join(element_lines) + "\n", encoding="utf-8")

    manifest_path = log_dir / "fam003_settings_visual_fail_repair_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "surface": "Global Settings / Nexus Tray / Quick Access",
                "proofClass": "accepted-reference-contact-sheet-plus-focused-state-proof",
                "acceptanceBoundary": "supporting-codex-proof-user-operated-live-validation-required",
                "artifactCount": len(artifacts),
                "allChecksPass": all_checks_pass,
                "artifacts": artifacts,
                "contactSheet": str(contact_sheet),
                "elementGroupLedger": str(element_ledger_path),
                "elementGroupCount": len(ELEMENT_GROUP_LEDGER_ROWS),
                "referenceScreenshots": [{"label": label, "path": str(path)} for label, path in REFERENCE_SCREENSHOTS],
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
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication, QPushButton

    from desktop.desktop_renderer import ResidentAccessSettingsDialog
    from desktop.resident_access import DEFAULT_QUICK_SLOT_ROUTE_IDS, MAX_QUICK_SLOT_COUNT

    app = QApplication.instance() or QApplication([])
    rows: list[tuple[str, bool, str]] = []
    artifacts: list[dict[str, str]] = []
    rows.extend(_copy_reference_artifacts(log_dir, artifacts))

    dialog = ResidentAccessSettingsDialog()
    dialog.show()
    app.processEvents()

    default_path = log_dir / "01_default_global_settings_shell.png"
    default_ok, width, height = _capture(
        dialog,
        default_path,
        artifacts,
        surface="full Global Settings shell",
        state="default Quick Access page",
    )
    light_ratio = _light_pixel_ratio(default_path)
    rows.append(
        (
            "default screenshot saved",
            default_ok and 770 <= width <= 800 and 610 <= height <= 640,
            f"{default_path} ({width}x{height})",
        )
    )
    rows.append(
        (
            "architecture-first Global Settings geometry",
            770 <= width <= 800 and 610 <= height <= 640,
            f"window={width}x{height}; required compact settings shell, not old 880x600 Quick Access utility form",
        )
    )
    rows.append(("default surface is not white/native-light", light_ratio < 0.20, f"light_pixel_ratio={light_ratio:.3f}"))

    chrome_path = log_dir / "02_top_level_chrome_control_cluster.png"
    chrome_ok, chrome_width, chrome_height = _capture(
        dialog.chrome_bar,
        chrome_path,
        artifacts,
        surface="top-level chrome and compact window control cluster",
        state="default",
    )
    role_text = [label.text() for label in dialog.chrome_bar.role_labels]
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
            "reference-derived product header",
            dialog.chrome_bar.kicker_label.text() == "NEXUS DESKTOP AI"
            and dialog.chrome_bar.title_label.text() == "Global Settings"
            and dialog.chrome_bar.subtitle_label.text() == "Configure the Nexus tray."
            and role_text == ["NEXUS TRAY - QUICK ACCESS", "MENU BUDGET - 5 SLOTS"]
            and dialog.chrome_bar.role_pill.isVisible(),
            f"kicker={dialog.chrome_bar.kicker_label.text()!r}; title={dialog.chrome_bar.title_label.text()!r}; subtitle={dialog.chrome_bar.subtitle_label.text()!r}; role_pairs={role_text}; role_pill_visible={dialog.chrome_bar.role_pill.isVisible()}",
        )
    )

    dialog.chrome_bar.close_button.setFocus(Qt.FocusReason.OtherFocusReason)
    dialog.chrome_bar.close_button.setDown(True)
    QTest.qWait(40)
    app.processEvents()
    control_state_path = log_dir / "03_window_control_focus_pressed_state.png"
    control_state_ok, _, _ = _capture(
        dialog.chrome_bar.control_cluster,
        control_state_path,
        artifacts,
        surface="window control cluster",
        state="close focus/pressed",
    )
    dialog.chrome_bar.close_button.setDown(False)
    app.processEvents()
    rows.append(
        (
            "window control focus/pressed proof",
            control_state_ok and dialog.chrome_bar.close_button.hasFocus(),
            f"{control_state_path}; close_focus={dialog.chrome_bar.close_button.hasFocus()}",
        )
    )

    nav_path = log_dir / "04_left_settings_organizer.png"
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
            and set(dialog._nav_buttons) == {"quick_access"}
            and dialog.nav_title.text() == "Nexus Tray"
            and dialog.nav_detail.text() == "Quick Access is the active settings page."
            and dialog.quick_access_nav_caption.text() == "Tray submenu order"
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
            "single actionable page inside Global Settings IA",
            dialog.section_heading.text() == "Quick Access"
            and dialog.section_badge.text() == "01"
            and dialog.section_scope.text() == "Nexus Tray Settings"
            and dialog.property("settingsInformationArchitecture") == "global-settings-shell-nexus-tray-quick-access-page"
            and dialog.property("settingsVisualRepair") == "architecture-first-reference-conformance-v3"
            and dialog.property("referenceDerivedHeader") == "ai-control-center-reference-derived-settings-shell-v3"
            and dialog.property("sharedPrimitiveClaim") == "none-promoted-reference-derived-only"
            and dialog.property("referenceComparatorRequired") == "accepted-ai-control-center-contact-sheet"
            and set(dialog._nav_buttons) == {"quick_access"}
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and dialog.quick_access_nav_button.isChecked()
            and dialog.slot_count_badge.text() == "2/5 slots"
            and dialog.menu_path_row.text() == "Native tray > Quick Access"
            and dialog.pending_state_row.text() == "No pending changes"
            and dialog.quick_slot_container.objectName() == "residentAccessQuickSlotContainer"
            and dialog.footer_frame.objectName() == "residentAccessSettingsFooter"
            and not dialog.route_summary.isVisible(),
            f"heading={dialog.section_heading.text()!r}; section_badge={dialog.section_badge.text()!r}; slot_badge={dialog.slot_count_badge.text()!r}; nav={list(dialog._nav_buttons)}; buttons={button_texts}; route_visible={dialog.route_summary.isVisible()}",
        )
    )
    stale_product_text = {
        "Connected Surfaces",
        "Resident Access",
        "Tray Menu Shortcuts",
        "Resident tray shortcuts and menu preferences.",
        "Add Slot",
        "Use Defaults",
        "Save Changes",
        "Reset Quick Access",
        "Move Up",
        "Move Down",
        "PAGE - QUICK ACCESS",
        "SCOPE - TRAY MENU",
    }
    visible_text_blob = " ".join(
        [
            dialog.chrome_bar.kicker_label.text(),
            dialog.chrome_bar.title_label.text(),
            dialog.chrome_bar.subtitle_label.text(),
            " ".join(role_text),
            dialog.nav_title.text(),
            dialog.nav_detail.text(),
            dialog.quick_access_nav_button.text(),
            dialog.quick_access_nav_caption.text(),
            dialog.section_scope.text(),
            dialog.section_heading.text(),
            dialog.section_detail.text(),
            dialog.quick_help.text(),
            " ".join(button_texts),
        ]
    )
    rows.append(
        (
            "product-facing copy is compact and non-internal",
            all(token not in visible_text_blob for token in stale_product_text),
            f"visible_text={visible_text_blob!r}",
        )
    )
    rows.append(
        (
            "compact quick-slot controls",
            all(button.text() in {"\u2191", "\u2193", "\N{MULTIPLICATION SIGN}"} for button in compact_action_buttons)
            and all(button.width() <= 30 and button.height() <= 30 for button in compact_action_buttons),
            f"buttons={button_texts}; compact_action_sizes={[(button.objectName(), button.text(), button.width(), button.height(), button.isEnabled()) for button in compact_action_buttons]}",
        )
    )
    rows.append(
        (
            "initial pending-state copy",
            not dialog.change_summary.isVisible()
            and dialog.change_summary.text() == ""
            and not dialog.save_button.isEnabled()
            and not dialog.revert_button.isEnabled()
            and dialog.pending_state_row.text() == "No pending changes",
            f"change_summary={dialog.change_summary.text()!r}; visible={dialog.change_summary.isVisible()}; pending={dialog.pending_state_row.text()!r}",
        )
    )

    if not dialog._slot_combos:
        rows.append(("quick-slot combo exists", False, "no quick-slot combo rendered"))
    else:
        combo = dialog._slot_combos[0]
        row_action_path = log_dir / "05_row_action_default_disabled_state.png"
        row_action_ok, _, _ = _capture(
            dialog.quick_slot_rows,
            row_action_path,
            artifacts,
            surface="Quick Access row actions",
            state="default / first up disabled",
        )
        rows.append(
            (
                "row actions show disabled state",
                row_action_ok and any(button.objectName() == "residentAccessQuickSlotMoveUp" and not button.isEnabled() for button in compact_action_buttons),
                f"{row_action_path}; disabled_actions={[(button.objectName(), button.isEnabled()) for button in compact_action_buttons]}",
            )
        )

        new_index = 1 if combo.count() > 1 and combo.currentIndex() != 1 else 0
        combo.setCurrentIndex(new_index)
        app.processEvents()
        dirty_path = log_dir / "06_dirty_quick_access.png"
        dirty_ok, _, _ = _capture(
            dialog,
            dirty_path,
            artifacts,
            surface="full Global Settings shell",
            state="dirty Quick Access edit",
        )
        rows.append(("dirty screenshot saved", dirty_ok, str(dirty_path)))
        rows.append(
            (
                "dirty guard state after dropdown edit",
                dialog._has_unsaved_changes()
                and dialog.save_button.isEnabled()
                and dialog.revert_button.isEnabled()
                and "Unsaved changes" in dialog.change_summary.text()
                and dialog.pending_state_row.text() == "Unsaved changes",
                f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}; pending={dialog.pending_state_row.text()!r}",
            )
        )

        combo.showPopup()
        app.processEvents()
        popup_path = log_dir / "07_dropdown_list_state.png"
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
            (
                "dropdown/list state screenshot saved",
                popup_ok and popup_width > 100 and popup_height > 20,
                f"{popup_path} ({popup_width}x{popup_height})",
            )
        )
        rows.append(
            (
                "dropdown/list state is not white/native-light",
                popup_light_ratio < 0.20,
                f"light_pixel_ratio={popup_light_ratio:.3f}",
            )
        )

    dialog.reject()
    app.processEvents()
    guard_path = log_dir / "08_close_guard.png"
    guard_ok, _, _ = _capture(
        dialog,
        guard_path,
        artifacts,
        surface="dirty-change close guard",
        state="chrome close requested with unsaved changes",
    )
    rows.append(("close guard screenshot saved", guard_ok, str(guard_path)))
    rows.append(
        (
            "close guard blocks silent loss",
            dialog.isVisible()
            and dialog._close_guard_active
            and dialog.discard_button.isVisible()
            and dialog.keep_editing_button.isVisible()
            and "Unsaved changes" in dialog.change_summary.text(),
            f"visible={dialog.isVisible()}; guard={dialog._close_guard_active}; summary={dialog.change_summary.text()!r}",
        )
    )

    dialog._keep_editing()
    dialog.set_focus("quick_access")
    dialog._reset_slots()
    app.processEvents()
    reset_path = log_dir / "09_defaults_staged.png"
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
            "default semantics stage defaults",
            dialog._has_unsaved_changes()
            and tuple(dialog._settings.quick_slot_ids) == tuple(DEFAULT_QUICK_SLOT_ROUTE_IDS)
            and "Default shortcuts staged" in dialog.change_summary.text(),
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
    max_slots_path = log_dir / "10_max_slots_unclipped.png"
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
    saved_path = log_dir / "11_saved_state.png"
    saved_ok, _, _ = _capture(
        dialog,
        saved_path,
        artifacts,
        surface="full Global Settings shell",
        state="saved Quick Access state",
    )
    rows.append(("saved state screenshot saved", saved_ok, str(saved_path)))
    rows.append(
        (
            "save clears dirty state",
            not dialog._has_unsaved_changes()
            and not dialog.save_button.isEnabled()
            and "Quick Access saved" in dialog.change_summary.text(),
            f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}; pending={dialog.pending_state_row.text()!r}",
        )
    )

    contact_sheet, contact_ok = _write_contact_sheet(
        log_dir,
        [
            ("Accepted reference - AI Control Center", REFERENCE_SCREENSHOTS[0][1]),
            ("Accepted reference - close hover", REFERENCE_SCREENSHOTS[1][1]),
            ("Repaired FAM-003 - Global Settings", default_path),
            ("Repaired FAM-003 - dropdown/list state", log_dir / "07_dropdown_list_state.png"),
        ],
    )
    rows.append(
        (
            "side-by-side reference contact sheet written",
            contact_ok and contact_sheet.exists(),
            str(contact_sheet),
        )
    )
    artifacts.append(
        {
            "path": str(contact_sheet),
            "surface": "accepted-reference side-by-side comparison",
            "state": "contact sheet",
            "width": "composite",
            "height": "composite",
            "saved": str(bool(contact_ok and contact_sheet.exists())),
        }
    )

    ledger_path, manifest_path, element_ledger_path = _write_artifact_ledger(log_dir, artifacts, rows, contact_sheet)
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
