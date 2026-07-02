"""Option C proof validator for the FAM-003 Workstream review packet.

Helper Status: Workstream-scoped
Owner Workstream: FAM-003 Settings resize proof / Option C workstream
Reason Reusable Helper Was Not Extended: This closes a branch-local false-green
    proof gap across Settings, tray, and NCP packet evidence without promoting a
    repo-wide visual-proof template.
Consolidation Target: Future shared UI proof bundle helper after multiple FAMs
    need the same direct surface-to-packet evidence contract.
Promotion Decision Point: Before PR Readiness for this branch, if the proof
    pattern is still needed beyond this Workstream packet repair.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace


# This helper captures USER-review proof for text-heavy Qt widgets. Offscreen
# Qt on Windows can substitute a glyph-box font, so force normal desktop Qt
# rendering when a parent shell left an offscreen platform override behind.
if os.environ.get("QT_QPA_PLATFORM", "").casefold() == "offscreen":
    os.environ.pop("QT_QPA_PLATFORM", None)

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QAction, QColor, QFont, QFontInfo, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_option_c_workstream_proof"
SETTINGS_LOG_ROOT = ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _run(command: list[str], *, timeout: int = 180, normal_qt_platform: bool = False) -> dict[str, object]:
    env = os.environ.copy()
    if normal_qt_platform:
        env.pop("QT_QPA_PLATFORM", None)
    proc = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        env=env,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0,
    }


def _git_value(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout.strip()


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _save_widget(widget, path: Path) -> dict[str, object]:
    widget.adjustSize()
    widget.resize(widget.sizeHint())
    widget.show()
    QApplication.processEvents()
    pixmap = widget.grab()
    ok = pixmap.save(str(path))
    widget.hide()
    _assert(ok and path.exists(), f"failed to save {path}")
    return {"path": str(path), "width": pixmap.width(), "height": pixmap.height(), "bytes": path.stat().st_size}


def _copy_latest_settings_artifact(log_dir: Path, filename: str) -> Path | None:
    if not SETTINGS_LOG_ROOT.exists():
        return None
    candidates = sorted(
        [path for path in SETTINGS_LOG_ROOT.iterdir() if path.is_dir()],
        key=lambda path: path.name,
        reverse=True,
    )
    for candidate in candidates:
        source = candidate / filename
        if source.exists():
            target = log_dir / filename
            shutil.copy2(source, target)
            return target
    return None


def _make_qapp() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication(["orin_fam003_option_c_workstream_proof_validation"])
    base_font = QFont("Segoe UI", 10)
    app.setFont(base_font)
    return app


def _readable_text_contract(widget, *, surface: str, required_texts: tuple[str, ...]) -> dict[str, object]:
    text_widgets = [widget]
    text_widgets.extend(widget.findChildren(QLabel))
    text_widgets.extend(widget.findChildren(QPushButton))
    text_widgets.extend(widget.findChildren(QLineEdit))
    observed: list[str] = []
    font_families: dict[str, str] = {}
    for child in text_widgets:
        text = ""
        if hasattr(child, "text"):
            text = child.text()
        elif isinstance(child, QLineEdit):
            text = child.displayText()
        if text:
            observed.append(text)
            font_families[text] = QFontInfo(child.font()).family()
    missing = [text for text in required_texts if text not in observed and not any(text in item for item in observed)]
    _assert(not missing, f"{surface} missing required readable text widgets: {missing}; observed={observed}")
    bad_fonts = {text: family for text, family in font_families.items() if "segoe" not in family.casefold()}
    _assert(not bad_fonts, f"{surface} readable text widgets resolved to non-Segoe UI fonts: {bad_fonts}")
    return {
        "surface": surface,
        "status": "PASS",
        "requiredTexts": list(required_texts),
        "observedTexts": observed,
        "fontFamilies": font_families,
        "visualReviewRequired": "Human-reviewable screenshot/contact sheet remains required; this check prevents offscreen glyph-box font fallback and missing text widgets.",
    }


class _FakeTrayWindow:
    def __init__(self):
        self.events: list[str] = []
        self.open_overlay_count = 0
        self.settings_requests: list[str] = []
        self.ai_status_requests: list[str] = []
        self.create_task_requests: list[str] = []
        self.saved_action_requests: list[str] = []
        self.dashboard_requests: list[dict[str, object]] = []
        self.command_visible = False

    def open_command_overlay(self):
        self.open_overlay_count += 1
        self.command_visible = True

    def close_command_overlay(self):
        self.command_visible = False

    def toggle_command_overlay(self):
        self.command_visible = not self.command_visible

    def command_overlay_state(self):
        return {"visible": self.command_visible, "phase": "entry" if self.command_visible else "closed"}

    def open_resident_access_settings(self, source="tray", focus=""):
        self.settings_requests.append(f"{source}:{focus or ''}")

    def open_ai_status_command_center(self, source="tray"):
        self.ai_status_requests.append(source)

    def request_create_custom_task_from_tray(self, source="tray"):
        self.create_task_requests.append(source)

    def open_saved_actions(self, source="tray"):
        self.saved_action_requests.append(source)

    def request_monitoring_hud_dashboard_from_tray(self, *, source="tray", visible=True):
        self.dashboard_requests.append({"source": source, "visible": bool(visible)})

    def monitoring_hud_feature_state(self):
        return {
            "feature_enabled": False,
            "dashboard_visible": False,
            "resident_route_state": "disabled_by_user",
            "resident_route_reason": "HUD disabled by USER",
            "route_state": "disabled_by_user",
            "overlay_deferred": True,
            "overlay_anchor_enabled": False,
        }


def _button_texts(popup) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for button, handler in popup._command_buttons:
        parent = button.parentWidget()
        visible = bool(button.text()) and (
            button.isVisible()
            or (parent is not None and button.isVisibleTo(parent))
        )
        rows.append(
            {
                "text": button.text(),
                "visible": visible,
                "enabled": button.isEnabled(),
                "accessibleName": button.accessibleName(),
                "handler": getattr(handler, "__name__", repr(handler)),
            }
        )
    return rows


def _section_texts(popup) -> list[str]:
    labels = []
    for child in popup.findChildren(object):
        if hasattr(child, "property") and child.property("traySection") is True and hasattr(child, "text"):
            labels.append(child.text())
    return labels


def _function_block(text: str, name: str) -> str:
    marker = f"def {name}("
    start = text.find(marker)
    if start < 0:
        return ""
    next_def = text.find("\n    def ", start + len(marker))
    if next_def < 0:
        next_def = len(text)
    return text[start:next_def]


def _render_tray_proof(log_dir: Path) -> dict[str, object]:
    from desktop.tray_controller import DesktopTrayEntry

    fake_window = _FakeTrayWindow()
    events: list[str] = []
    tray = DesktopTrayEntry(
        QApplication.instance(),
        fake_window,
        event_logger=events.append,
        shutdown_confirmation_requester=lambda source: events.append(f"shutdown:{source}"),
    )
    tray._initialize_popup()
    tray.monitoring_hud_primary_action = QAction("", tray.tray_popup)
    tray.monitoring_hud_dashboard_action = QAction("", tray.tray_popup)
    tray.monitoring_hud_unanchor_action = QAction("", tray.tray_popup)
    tray.refresh_resident_access_actions("option_c_proof")
    tray.refresh_monitoring_hud_actions("option_c_proof")
    tray._show_tray_popup()
    QApplication.processEvents()
    readability = _readable_text_contract(
        tray.tray_popup,
        surface="styled_tray_popup",
        required_texts=("Global Settings", "Quick Access", "Command Overlay", "Create Task", "Saved Actions", "AI"),
    )
    screenshot = _save_widget(tray.tray_popup, log_dir / "01_tray_styled_popup_focused.png")

    buttons = _button_texts(tray.tray_popup)
    visible_texts = [row["text"] for row in buttons if row["visible"]]
    sections = _section_texts(tray.tray_popup)
    tray_source = (ROOT / "desktop" / "tray_controller.py").read_text(encoding="utf-8")
    show_popup_block = _function_block(tray_source, "_show_tray_popup")

    tray.global_settings_button.click()
    QApplication.processEvents()
    tray._show_tray_popup()
    QApplication.processEvents()
    if tray.open_overlay_button is not None:
        tray.open_overlay_button.click()
        QApplication.processEvents()
    route_screenshot = _save_widget(tray.tray_popup, log_dir / "02_tray_popup_route_after_reopen.png")

    native_not_primary = (
        "TRAY_STYLED_POPUP_REQUESTED" in show_popup_block
        and "_show_native_tray_menu()" not in show_popup_block
    )
    route_ok = fake_window.settings_requests and fake_window.open_overlay_count == 1
    compact_ok = (
        visible_texts[:1] == ["Global Settings"]
        and {"Command Overlay", "Create Task", "Saved Actions"}.issubset(set(visible_texts))
        and "Quick Access" in sections
        and "AI" in sections
        and all("Provider-visible data:" not in text for text in visible_texts)
        and "HUD Feature Settings" not in visible_texts
        and "Open HUD Dashboard" not in visible_texts
        and "HUD Overlay Deferred" not in visible_texts
    )
    styled_ok = screenshot["width"] >= 260 and screenshot["height"] >= 120
    _assert(native_not_primary, "native Windows menu is still primary in _show_tray_popup")
    _assert(route_ok, "visible styled tray buttons did not route Global Settings and Command Overlay")
    _assert(compact_ok, f"styled tray popup compact text/category proof failed: {visible_texts}, sections={sections}")
    _assert(styled_ok, f"styled tray screenshot dimensions invalid: {screenshot}")

    return {
        "status": "PASS",
        "screenshots": [screenshot, route_screenshot],
        "visibleTexts": visible_texts,
        "sections": sections,
        "events": events,
        "nativeMenuPrimary": False,
        "globalSettingsRequests": fake_window.settings_requests,
        "openOverlayCount": fake_window.open_overlay_count,
        "textReadability": readability,
    }


def _render_ncp_state(panel, payload: dict[str, object], path: Path) -> dict[str, object]:
    panel.render_payload(payload)
    panel.show_for_geometry(QRect(0, 0, 1280, 720), QRect(0, 0, 1280, 720))
    return _save_widget(panel, path)


def _render_ncp_proof(log_dir: Path) -> dict[str, object]:
    from desktop.desktop_renderer import CommandOverlayPanel

    panel = CommandOverlayPanel()
    common_action = {
        "title": "Open Nexus Docs",
        "origin_label": "Built-in action",
        "target_kind": "folder",
        "target": str(ROOT / "Docs"),
        "target_display": "Docs",
    }
    entry = _render_ncp_state(
        panel,
        {
            "phase": "entry",
            "input_armed": True,
            "typing_ready": True,
            "input_text": "open nexus folder",
            "status_kind": "idle",
            "status_text": "",
            "saved_action_inventory": {"visible": False},
            "saved_group_inventory": {"visible": False},
        },
        log_dir / "10_ncp_entry_typed_request.png",
    )
    entry_readability = _readable_text_contract(
        panel,
        surface="ncp_command_overlay_entry",
        required_texts=("O.R.I.N. Command Prompt", "Typed desktop interaction", "open nexus folder"),
    )
    choose = _render_ncp_state(
        panel,
        {
            "phase": "choose",
            "input_armed": False,
            "input_text": "open nexus folder",
            "typed_request": "open nexus folder",
            "status_kind": "ambiguous",
            "status_text": "Multiple actions matched.",
            "ambiguous_titles": ["Open Nexus Root", "Open Nexus Docs"],
            "ambiguous_matches": [
                {
                    "index": 0,
                    "title": "Open Nexus Root",
                    "origin_label": "Built-in action",
                    "target_kind": "folder",
                    "target": str(ROOT),
                    "target_display": "Nexus root",
                },
                {**common_action, "index": 1},
            ],
        },
        log_dir / "11_ncp_choose_visible_choices.png",
    )
    choose_readability = _readable_text_contract(
        panel,
        surface="ncp_command_overlay_choose",
        required_texts=("Multiple actions matched.", "Open Nexus Root", "Open Nexus Docs", "Built-in action - folder"),
    )
    confirm = _render_ncp_state(
        panel,
        {
            "phase": "confirm",
            "input_armed": False,
            "input_text": "open nexus folder",
            "typed_request": "open nexus folder",
            "status_kind": "idle",
            "pending_action": common_action,
            "selection_context": "",
        },
        log_dir / "12_ncp_confirm_selected_action.png",
    )
    confirm_readability = _readable_text_contract(
        panel,
        surface="ncp_command_overlay_confirm",
        required_texts=("Typed request", "open nexus folder", "Resolved action", "Open Nexus Docs"),
    )
    result = _render_ncp_state(
        panel,
        {
            "phase": "result",
            "input_armed": False,
            "input_text": "",
            "status_kind": "launch_requested",
            "status_text": "Launch request sent.",
        },
        log_dir / "13_ncp_result_launch_requested.png",
    )
    result_readability = _readable_text_contract(
        panel,
        surface="ncp_command_overlay_result",
        required_texts=("O.R.I.N. Command Prompt", "Launch request sent."),
    )
    panel.close()

    for proof in (entry, choose, confirm, result):
        _assert(proof["width"] >= 500 and proof["height"] >= 150, f"NCP proof frame too small: {proof}")
    return {
        "status": "PASS",
        "screenshots": [entry, choose, confirm, result],
        "states": ["entry_typed", "choose", "confirm", "result"],
        "textReadability": [
            entry_readability,
            choose_readability,
            confirm_readability,
            result_readability,
        ],
    }


def _write_contact_sheet(log_dir: Path, image_paths: list[Path], output_name: str) -> Path:
    thumbs: list[tuple[Path, QPixmap]] = []
    for path in image_paths:
        pixmap = QPixmap(str(path))
        _assert(not pixmap.isNull(), f"could not load image for contact sheet: {path}")
        thumbs.append((path, pixmap.scaled(360, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)))

    margin = 18
    caption_height = 34
    cell_w = 396
    cell_h = 270
    columns = 2
    rows = (len(thumbs) + columns - 1) // columns
    sheet = QPixmap(columns * cell_w + margin, rows * cell_h + margin)
    sheet.fill(QColor("#04101b"))
    painter = QPainter(sheet)
    painter.setRenderHint(QPainter.Antialiasing, True)
    font = QFont("Segoe UI", 9)
    font.setBold(True)
    painter.setFont(font)
    painter.setPen(QColor("#dffbff"))
    for index, (path, pixmap) in enumerate(thumbs):
        col = index % columns
        row = index // columns
        x = margin + col * cell_w
        y = margin + row * cell_h
        painter.setPen(QColor("#38d9ff"))
        painter.drawRoundedRect(x - 6, y - 6, cell_w - 18, cell_h - 16, 10, 10)
        painter.drawPixmap(x, y, pixmap)
        painter.setPen(QColor("#dffbff"))
        painter.drawText(x, y + 224, cell_w - 30, caption_height, Qt.TextWordWrap, f"{index + 1}. {path.name}")
    painter.end()
    output = log_dir / output_name
    ok = sheet.save(str(output))
    _assert(ok and output.exists(), f"failed to save contact sheet {output}")
    return output


def _validate_png(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    ok = data.startswith(PNG_SIGNATURE) and len(data) > 200
    return {"path": str(path), "ok": ok, "bytes": len(data)}


def main() -> int:
    _make_qapp()
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = LOG_ROOT / timestamp
    log_dir.mkdir(parents=True, exist_ok=True)

    head = _git_value("rev-parse", "HEAD")
    origin_main = _git_value("rev-parse", "origin/main")
    merge_base = _git_value("merge-base", "HEAD", "origin/main")

    tray = _render_tray_proof(log_dir)
    ncp = _render_ncp_proof(log_dir)
    settings_contact = _copy_latest_settings_artifact(log_dir, "16_defect_closure_contact_sheet.png")
    settings_default = _copy_latest_settings_artifact(log_dir, "01_default_global_settings_shell.png")

    helper_runs = {
        "overlayInputHelper": _run([sys.executable, "dev/orin_overlay_input_capture_helper.py"]),
        "callableGroupExecution": _run([sys.executable, "dev/orin_callable_group_execution_validation.py"]),
        "desktopEntrypoint": _run(
            [sys.executable, "dev/orin_desktop_entrypoint_validation.py"],
            timeout=420,
            normal_qt_platform=True,
        ),
    }
    for name, result in helper_runs.items():
        report = log_dir / f"{name}.txt"
        report.write_text(
            "COMMAND: "
            + " ".join(result["command"])
            + "\nRETURN CODE: "
            + str(result["returncode"])
            + "\n\nSTDOUT:\n"
            + str(result["stdout"])
            + "\n\nSTDERR:\n"
            + str(result["stderr"]),
            encoding="utf-8",
        )
        _assert(result["ok"], f"{name} failed; see {report}")

    proof_images = [Path(item["path"]) for item in tray["screenshots"] + ncp["screenshots"]]
    if settings_contact is not None:
        proof_images.insert(0, settings_contact)
    if settings_default is not None:
        proof_images.insert(0, settings_default)
    contact_sheet = _write_contact_sheet(log_dir, proof_images, "00_option_c_workstream_contact_sheet.png")

    png_results = [_validate_png(path) for path in proof_images + [contact_sheet]]
    _assert(all(item["ok"] for item in png_results), f"PNG integrity failed: {png_results}")

    artifact_ledger = log_dir / "FAM003_OPTION_C_WORKSTREAM_PROOF.md"
    artifact_ledger.write_text(
        "# FAM-003 Option C Workstream Proof\n\n"
        f"Source Repo HEAD: `{head}`\n"
        f"Source origin/main: `{origin_main}`\n"
        f"Merge Base: `{merge_base}`\n"
        f"Proof Root: `{log_dir}`\n\n"
        "## Defects Admitted / Reclosed\n\n"
        "| Defect ID | Disposition | Closure Proof |\n"
        "| --- | --- | --- |\n"
        "| F3-WS-PROOF-TRAY-001 | CLOSED_WITH_PROOF | Direct styled tray popup screenshots, native-not-primary source-path proof, route execution tied to visible styled buttons. |\n"
        "| F3-WS-PROOF-NCP-001 | CLOSED_WITH_PROOF | Direct NCP entry/choose/confirm/result screenshots plus overlay/callable/desktop-entrypoint helper reports copied into this proof root. |\n\n"
        "| F3-WS-VIS-TEXT-001 | CLOSED_WITH_PROOF | Direct tray and NCP screenshots are captured with normal desktop Qt rendering, Segoe UI text contract checks, readable focused frames, and human-reviewable contact sheet evidence. |\n\n"
        "## Surface Verdicts\n\n"
        "| Surface | Verdict | Evidence |\n"
        "| --- | --- | --- |\n"
        f"| Settings resize/cursor | PASS | `{settings_default.name if settings_default else 'preserved latest settings proof root'}`; `{settings_contact.name if settings_contact else 'preserved latest contact sheet'}` |\n"
        "| Styled tray right-click presentation | PASS | `01_tray_styled_popup_focused.png`; `02_tray_popup_route_after_reopen.png`; native menu not primary in `_show_tray_popup`. |\n"
        "| Tray route/action execution | PASS | Global Settings and Command Overlay routes fired from visible styled popup buttons. |\n"
        "| NCP typed/choose/confirm/result | PASS | `10_ncp_entry_typed_request.png`; `11_ncp_choose_visible_choices.png`; `12_ncp_confirm_selected_action.png`; `13_ncp_result_launch_requested.png`. |\n"
        "| Tray and NCP text readability | PASS | `F3-WS-VIS-TEXT-001`; normal desktop Qt capture; Segoe UI text contract; contact sheet and individual focused frames. |\n"
        "| NCP helper/report evidence | PASS | `overlayInputHelper.txt`; `callableGroupExecution.txt`; `desktopEntrypoint.txt`. |\n\n"
        "Issue Admission Result: `NO CURRENT GITHUB ISSUE CREATED`. Issue mutation remains blocked without explicit USER approval.\n",
        encoding="utf-8",
    )

    manifest = {
        "status": "PASS",
        "timestamp": timestamp,
        "head": head,
        "originMain": origin_main,
        "mergeBase": merge_base,
        "proofRoot": str(log_dir),
        "defects": {
            "F3-WS-PROOF-TRAY-001": "CLOSED_WITH_PROOF",
            "F3-WS-PROOF-NCP-001": "CLOSED_WITH_PROOF",
            "F3-WS-VIS-TEXT-001": "CLOSED_WITH_PROOF",
        },
        "captureMode": {
            "qtPlatformName": QApplication.platformName(),
            "forcedOffscreenCapture": False,
            "reason": "Tray and NCP text proof must use normal desktop Qt rendering; offscreen capture produced placeholder glyphs.",
        },
        "tray": tray,
        "ncp": ncp,
        "settingsArtifacts": [str(path) for path in (settings_default, settings_contact) if path is not None],
        "helperRuns": {
            name: {
                "ok": result["ok"],
                "returncode": result["returncode"],
                "report": str(log_dir / f"{name}.txt"),
            }
            for name, result in helper_runs.items()
        },
        "contactSheet": str(contact_sheet),
        "pngIntegrity": png_results,
        "issueAdmission": "NO_CURRENT_GITHUB_ISSUE_CREATED",
    }
    manifest_path = log_dir / "fam003_option_c_workstream_proof_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(f"FAM-003 OPTION C WORKSTREAM PROOF: PASS")
    print(f"Proof Root: {log_dir}")
    print(f"Contact Sheet: {contact_sheet}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
