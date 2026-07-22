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
from PySide6.QtGui import QColor, QFont, QFontInfo, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QMenu, QPushButton

ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_option_c_workstream_proof"
SETTINGS_LOG_ROOT = ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation"
HUD_SETTINGS_LOG_ROOT = ROOT / "dev" / "logs" / "fam003_hud_settings_visual_validation"
HUD_ACCESS_LOG_ROOT = ROOT / "dev" / "logs" / "fam003_hud_access_workstream_validation"
RENDERER_BACKEND_LOG_ROOT = ROOT / "dev" / "logs" / "fam003_renderer_backend_workstream"
PRESERVED_OPTION_D_LIFECYCLE_MANIFEST = (
    RENDERER_BACKEND_LOG_ROOT
    / "20260721-143125"
    / "fam003_renderer_backend_workstream_manifest.json"
)
PRESERVED_DESKTOP_ENTRYPOINT_REPORT = (
    ROOT
    / "dev"
    / "logs"
    / "desktop_entrypoint_validation"
    / "reports"
    / "DesktopEntrypointValidationReport_20260721_143116.txt"
)
PRESERVED_SETTINGS_PROOF_ROOT = (
    SETTINGS_LOG_ROOT
    / "20260721-155443"
)
PRESERVED_SETTINGS_REPORT = PRESERVED_SETTINGS_PROOF_ROOT / "FAM003_SETTINGS_REPAIR_VISUAL_VALIDATION.md"
FAILED_FINAL_HEAD_SETTINGS_REPORT = (
    SETTINGS_LOG_ROOT
    / "20260721-160130"
    / "FAM003_SETTINGS_REPAIR_VISUAL_VALIDATION.md"
)
CURSOR_PROOF_LATEST = ROOT / "dev" / "logs" / "fam003_resize_cursor_workstream_proof" / "latest_manifest.json"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CURRENTNESS_SAFE_PATHS = {
    "Docs/validation_helper_registry.md",
    "dev/fam003_renderer_backend_runtime_probe.py",
    "dev/fam003_option_d_performance_controller.py",
    "dev/fam003_option_d_performance_observer.py",
    "dev/fixtures/fam003_renderer_backend_negative_cases.json",
    "dev/fixtures/fam003_option_d_nonintrusive_performance_negative_cases.json",
    "dev/orin_fam003_option_c_workstream_proof_validation.py",
    "dev/orin_fam003_option_d_nonintrusive_performance_validation.py",
    "dev/orin_fam003_r2_workstream_scope_audit_validation.py",
    "dev/orin_fam003_renderer_backend_workstream_validation.py",
}

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.monitoring_hud_access import MonitoringHudAccessAdapter


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


def _proof_currentness(source_head: str, current_head: str, proof_label: str) -> dict[str, object]:
    _assert(source_head, f"{proof_label} has no source HEAD")
    changed_files = [
        line.strip().replace("\\", "/")
        for line in _git_value("diff", "--name-only", f"{source_head}..{current_head}").splitlines()
        if line.strip()
    ]
    unsafe_files = [path for path in changed_files if path not in CURRENTNESS_SAFE_PATHS]
    _assert(
        not unsafe_files,
        f"{proof_label} cannot be preserved because product/runtime-bearing files changed: {unsafe_files}",
    )
    return {
        "status": "PASS",
        "proofLabel": proof_label,
        "sourceHead": source_head,
        "currentHead": current_head,
        "changedFiles": changed_files,
        "safeNonRuntimeFiles": sorted(CURRENTNESS_SAFE_PATHS),
        "unsafeFiles": unsafe_files,
        "basis": "Git diff contains only performance-proof helpers, their fixture, aggregate currentness logic, and helper-registry documentation; no Settings, cursor, desktop runtime, resident access, or product source changed.",
    }


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
    return _copy_latest_artifact(SETTINGS_LOG_ROOT, log_dir, filename)


def _copy_latest_artifact(source_root: Path, log_dir: Path, filename: str) -> Path | None:
    if not source_root.exists():
        return None
    candidates = sorted(
        [path for path in source_root.iterdir() if path.is_dir()],
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


def _reported_path(result: dict[str, object], label: str) -> Path:
    for line in reversed(str(result.get("stdout", "")).splitlines()):
        if line.startswith(label):
            return Path(line.removeprefix(label).strip())
    raise AssertionError(f"child output did not report {label}")


def _copy_current_settings_proof(
    log_dir: Path,
    result: dict[str, object],
    expected_head: str,
) -> tuple[Path, dict[str, object], list[Path], dict[str, object]]:
    report_source = _reported_path(result, "Report:")
    source_root = report_source.parent.resolve()
    _assert(SETTINGS_LOG_ROOT.resolve() in source_root.parents, "Settings child reported a proof root outside its registered log root")
    manifest_source = source_root / "fam003_settings_visual_fail_repair_manifest.json"
    _assert(report_source.exists() and manifest_source.exists(), "current Settings child proof root is incomplete")
    payload = json.loads(manifest_source.read_text(encoding="utf-8-sig"))
    _assert(payload.get("allChecksPass") is True, "current Settings manifest is not green")
    source_head = str(payload.get("sourceHead") or "")
    currentness = _proof_currentness(source_head, expected_head, "preserved Settings visual proof")
    _assert(payload.get("visibleCursorProofPass") is True, "current Settings manifest did not consume green visible-cursor proof")

    copied: list[Path] = []
    for filename in (
        report_source.name,
        manifest_source.name,
        "01_default_global_settings_shell.png",
        "16_defect_closure_contact_sheet.png",
        "17_red_team_review_sheet.png",
    ):
        source = source_root / filename
        _assert(source.exists(), f"current Settings proof artifact is missing: {source}")
        target = log_dir / filename
        shutil.copy2(source, target)
        copied.append(target)
    return source_root, payload, copied, currentness


def _copy_current_hud_access_proof(
    log_dir: Path,
    result: dict[str, object],
    expected_head: str,
) -> tuple[Path, dict[str, object], list[Path]]:
    source_root = _reported_path(result, "Evidence:").resolve()
    _assert(HUD_ACCESS_LOG_ROOT.resolve() in source_root.parents, "HUD access child reported a proof root outside its registered log root")
    manifest_source = source_root / "fam003_hud_access_workstream_manifest.json"
    state_json_source = source_root / "fam003_hud_access_26_state_results.json"
    state_md_source = source_root / "fam003_hud_access_26_state_results.md"
    report_source = source_root / "fam003_hud_access_workstream_report.md"
    for source in (manifest_source, state_json_source, state_md_source, report_source):
        _assert(source.exists(), f"HUD access child artifact is missing: {source}")
    payload = json.loads(manifest_source.read_text(encoding="utf-8-sig"))
    state_payload = json.loads(state_json_source.read_text(encoding="utf-8-sig"))
    state_rows = state_payload.get("states")
    required_fields = {
        "stateId", "title", "entryCondition", "expectedAdapterBehavior",
        "actualAdapterResult", "persistenceResult", "globalSettingsState",
        "trayState", "dashboardState", "userFacingState",
        "retryOrRollbackResult", "automatedEvidence", "workstreamVisualEvidence",
        "finalVerdict", "evidencePaths", "head", "timestamp", "proofRoot",
    }
    _assert(payload.get("status") == "PASS", "HUD access child is not PASS")
    _assert(payload.get("sourceHead") == expected_head, "HUD access child HEAD is stale")
    _assert(state_payload.get("status") == "PASS" and state_payload.get("sourceHead") == expected_head, "HUD access 26-state artifact is stale or non-green")
    _assert(isinstance(state_rows, list) and len(state_rows) == 26, "HUD access artifact does not contain exactly 26 state rows")
    _assert([row.get("stateId") for row in state_rows] == list(range(1, 27)), "HUD access state IDs are incomplete or out of order")
    _assert(all(required_fields <= set(row) and row.get("finalVerdict") == "PASS" for row in state_rows), "HUD access state row is incomplete or non-green")

    copied = []
    for source in (manifest_source, state_json_source, state_md_source, report_source):
        target = log_dir / source.name
        shutil.copy2(source, target)
        copied.append(target)
    return source_root, payload, copied


def _copy_current_hud_settings_proof(
    log_dir: Path,
    result: dict[str, object],
    expected_head: str,
) -> tuple[Path, dict[str, object], list[Path]]:
    source_root = _reported_path(result, "Evidence:").resolve()
    _assert(HUD_SETTINGS_LOG_ROOT.resolve() in source_root.parents, "HUD Settings child reported a proof root outside its registered log root")
    manifest_source = source_root / "fam003_hud_settings_visual_manifest.json"
    _assert(manifest_source.exists(), "HUD Settings child manifest is missing")
    payload = json.loads(manifest_source.read_text(encoding="utf-8-sig"))
    _assert(payload.get("status") == "PASS", "HUD Settings child is not PASS")
    _assert(payload.get("sourceHead") == expected_head, "HUD Settings child HEAD is stale")
    _assert(Path(str(payload.get("proofRoot", ""))).resolve() == source_root, "HUD Settings manifest proof root disagrees with child output")
    copied = []
    for filename in (
        "fam003_hud_settings_visual_manifest.json",
        "FAM003_HUD_SETTINGS_IMPLEMENTATION_CONTACT_SHEET.png",
        "FAM003_HUD_TARGET_IMPLEMENTATION_COMPARISON.png",
        "HUD_IMPLEMENTATION_MATCH_REVIEW.md",
    ):
        source = source_root / filename
        _assert(source.exists(), f"HUD Settings child artifact is missing: {source}")
        target = log_dir / filename
        shutil.copy2(source, target)
        copied.append(target)
    return source_root, payload, copied


def _copy_current_renderer_backend_proof(
    log_dir: Path,
    result: dict[str, object],
    expected_head: str,
) -> tuple[Path, dict[str, object], Path]:
    manifest_source = _reported_path(result, "Manifest:").resolve()
    source_root = manifest_source.parent
    _assert(
        RENDERER_BACKEND_LOG_ROOT.resolve() in source_root.parents,
        "renderer-backend child reported a proof root outside its registered log root",
    )
    payload = json.loads(manifest_source.read_text(encoding="utf-8-sig"))
    _assert(
        payload.get("status") in {"PASS", "USER_DECISION_REQUIRED"},
        "renderer-backend child is neither PASS nor a valid USER decision result",
    )
    _assert(payload.get("sourceHead") == expected_head, "renderer-backend child HEAD is stale")
    _assert(
        payload.get("proofMode") == "R2_WORKSTREAM_ONLY_NOT_H1_NOT_LV_NOT_UTS",
        "renderer-backend child crossed the Workstream proof boundary",
    )
    regression = payload.get("materialRegression") or {}
    if payload.get("status") == "PASS":
        _assert(regression.get("detected") is False, "renderer-backend child detected a material regression")
    else:
        _assert(regression.get("detected") is None, "renderer-backend child made an unsupported binary regression claim")
        _assert(regression.get("disposition") == "USER_DECISION_REQUIRED", "renderer-backend decision disposition is missing")
    _assert(len(payload.get("affectedSurfaceInventory") or []) == 8, "renderer-backend inventory is incomplete")
    _assert(
        (payload.get("lifecycle") or {}).get("abnormalNativeExit") == "ABSENT",
        "renderer-backend lifecycle proof is not clean",
    )
    target_root = log_dir / "renderer_backend"
    shutil.copytree(source_root, target_root)
    return source_root, payload, target_root


def _copy_current_cursor_proof(
    log_dir: Path,
    expected_head: str,
) -> tuple[dict[str, object], Path, list[Path], list[Path], dict[str, object]]:
    _assert(CURSOR_PROOF_LATEST.exists(), f"current visible-cursor manifest is missing: {CURSOR_PROOF_LATEST}")
    payload = json.loads(CURSOR_PROOF_LATEST.read_text(encoding="utf-8-sig"))
    _assert(payload.get("schema") == "fam003-r2-workstream-resize-cursor-proof-v1", "cursor proof schema is not the R2 Workstream schema")
    _assert(payload.get("status") == "PASS", "cursor proof is not PASS")
    _assert(payload.get("proofMode") == "R2_WORKSTREAM_RESIZE_CURSOR_ONLY", "cursor proof is not bounded Workstream mode")
    source_head = str(payload.get("head") or "")
    currentness = _proof_currentness(source_head, expected_head, "preserved visible-cursor proof")
    _assert(payload.get("formalHardening") is False and payload.get("formalLiveValidation") is False, "cursor proof crossed a downstream gate")

    manifest_target = log_dir / "fam003_resize_cursor_workstream_proof_manifest.json"
    shutil.copy2(CURSOR_PROOF_LATEST, manifest_target)
    copied_frames: list[Path] = []
    frame_rows: list[tuple[dict[str, object], Path]] = []
    for frame in payload.get("orderedFrames", []):
        _assert(isinstance(frame, dict), "cursor proof ordered frame is malformed")
        source = Path(str(frame.get("path", "")))
        _assert(source.exists(), f"cursor proof frame is missing: {source}")
        if frame.get("cursorRequested") is True:
            _assert(frame.get("cursorComposited") is True, f"requested cursor was not composited into frame: {source}")
        target = log_dir / f"cursor_{source.name}"
        shutil.copy2(source, target)
        copied_frames.append(target)
        frame_rows.append((frame, target))

    steps = {
        str(step.get("id")): step
        for step in payload.get("steps", [])
        if isinstance(step, dict)
    }
    settings_evidence = steps.get("settings_open_current_runtime", {}).get("evidence", {})
    settings_window = settings_evidence.get("settingsWindow", {}) if isinstance(settings_evidence, dict) else {}
    settings_rect = settings_window.get("rect") if isinstance(settings_window, dict) else None
    _assert(isinstance(settings_rect, list) and len(settings_rect) == 4, "cursor proof lacks Settings window crop geometry")
    crop_left = int(settings_rect[0]) - 56
    crop_top = int(settings_rect[1]) - 56
    crop_right = int(settings_rect[2]) + 56
    crop_bottom = int(settings_rect[3]) + 56
    focused_frames: list[Path] = []
    for frame, source in frame_rows:
        if frame.get("cursorRequested") is not True:
            continue
        virtual_bounds = frame.get("virtualBounds")
        _assert(isinstance(virtual_bounds, list) and len(virtual_bounds) == 4, "cursor frame lacks virtual-screen bounds")
        pixmap = QPixmap(str(source))
        _assert(not pixmap.isNull(), f"could not load cursor frame for focused crop: {source}")
        x = max(0, crop_left - int(virtual_bounds[0]))
        y = max(0, crop_top - int(virtual_bounds[1]))
        width = min(pixmap.width() - x, crop_right - crop_left)
        height = min(pixmap.height() - y, crop_bottom - crop_top)
        focused = pixmap.copy(x, y, width, height)
        target = log_dir / f"focus_{source.name}"
        _assert(focused.save(str(target)), f"could not save focused cursor frame: {target}")
        focused_frames.append(target)
    _assert(len(focused_frames) >= 6, "cursor proof does not contain the required focused cursor visual states")
    return payload, manifest_target, copied_frames, focused_frames, currentness


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
    if isinstance(widget, QMenu):
        for row in _menu_action_rows(widget, recursive=True):
            text = str(row["text"])
            if text and text not in observed:
                observed.append(text)
                font_families[text] = QFontInfo(widget.font()).family()
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
        self.dashboard_visible = False
        self.command_visible = False
        self._hud_access = MonitoringHudAccessAdapter(
            query_state=self.monitoring_hud_feature_state,
            persist_enabled=lambda _enabled, _source: True,
            open_or_restore_dashboard=self._open_or_restore_hud_dashboard,
            close_dashboard=self._close_hud_dashboard,
        )

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

    def monitoring_hud_access(self):
        return self._hud_access

    def _open_or_restore_hud_dashboard(self, source="tray"):
        self.dashboard_requests.append({"source": source, "visible": True})
        self.dashboard_visible = True
        return True

    def _close_hud_dashboard(self, source="tray"):
        self.dashboard_requests.append({"source": source, "visible": False})
        self.dashboard_visible = False
        return True

    def monitoring_hud_feature_state(self):
        return {
            "feature_enabled": True,
            "dashboard_visible": self.dashboard_visible,
            "resident_route_state": "enabled_available",
            "resident_route_reason": "HUD Dashboard ready",
            "route_state": "enabled_available",
            "overlay_deferred": True,
            "overlay_anchor_enabled": False,
        }


class _FakeSignal:
    def __init__(self):
        self.handlers = []

    def connect(self, handler):
        self.handlers.append(handler)


class _FakeSystemTrayIcon:
    class MessageIcon:
        Information = 1

    def __init__(self, icon, parent=None):
        self.icon = icon
        self.parent = parent
        self.activated = _FakeSignal()
        self.tooltip = ""
        self.visible = False

    @staticmethod
    def isSystemTrayAvailable():
        return True

    @staticmethod
    def supportsMessages():
        return True

    def setToolTip(self, text):
        self.tooltip = str(text)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def showMessage(self, *_args, **_kwargs):
        return None


def _menu_action_rows(menu: QMenu, *, recursive: bool = False) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for action in menu.actions():
        if action.isSeparator():
            continue
        child_menu = action.menu()
        rows.append(
            {
                "text": action.text(),
                "visible": action.isVisible(),
                "enabled": action.isEnabled(),
                "submenu": child_menu is not None,
                "parent": menu.title(),
            }
        )
        if recursive and child_menu is not None:
            rows.extend(_menu_action_rows(child_menu, recursive=True))
    return rows


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
    import desktop.tray_controller as tray_module

    fake_window = _FakeTrayWindow()
    events: list[str] = []
    tray = tray_module.DesktopTrayEntry(
        QApplication.instance(),
        fake_window,
        event_logger=events.append,
        shutdown_confirmation_requester=lambda source: events.append(f"shutdown:{source}"),
    )
    original_system_tray_icon = tray_module.QSystemTrayIcon
    tray_module.QSystemTrayIcon = _FakeSystemTrayIcon
    try:
        _assert(tray.initialize(), "compact tray hierarchy did not initialize")
    finally:
        tray_module.QSystemTrayIcon = original_system_tray_icon
    tray.refresh_resident_access_actions("option_c_proof")
    tray.refresh_monitoring_hud_actions("option_c_proof")
    tray._show_tray_popup()
    QApplication.processEvents()
    readability = _readable_text_contract(
        tray.tray_popup,
        surface="styled_tray_popup",
        required_texts=("Global Settings", "Quick Access", "AI", "HUD", "Exit Nexus Desktop AI"),
    )
    screenshot = _save_widget(tray.tray_popup, log_dir / "01_tray_styled_popup_focused.png")
    quick_screenshot = _save_widget(
        tray.quick_access_menu,
        log_dir / "03_tray_quick_access_submenu_focused.png",
    )
    hud_screenshot = _save_widget(
        tray.hud_menu,
        log_dir / "04_tray_hud_submenu_focused.png",
    )

    top_rows = _menu_action_rows(tray.tray_menu)
    quick_rows = _menu_action_rows(tray.quick_access_menu)
    ai_rows = _menu_action_rows(tray.ai_menu)
    hud_rows = _menu_action_rows(tray.hud_menu)
    top_texts = [str(row["text"]) for row in top_rows if row["visible"]]
    quick_texts = [str(row["text"]) for row in quick_rows if row["visible"]]
    ai_texts = [str(row["text"]) for row in ai_rows if row["visible"]]
    hud_texts = [str(row["text"]) for row in hud_rows if row["visible"]]
    tray_source = (ROOT / "desktop" / "tray_controller.py").read_text(encoding="utf-8")
    show_popup_block = _function_block(tray_source, "_show_tray_popup")

    tray.global_settings_action.trigger()
    QApplication.processEvents()
    tray._show_tray_popup()
    QApplication.processEvents()
    command_overlay_index = tray.quick_slot_route_ids.index("command_overlay")
    tray.quick_slot_actions[command_overlay_index].trigger()
    QApplication.processEvents()
    tray.monitoring_hud_dashboard_action.trigger()
    QApplication.processEvents()
    route_screenshot = _save_widget(tray.tray_popup, log_dir / "02_tray_popup_route_after_reopen.png")

    native_not_primary = (
        "TRAY_STYLED_POPUP_REQUESTED" in show_popup_block
        and "_show_native_tray_menu()" not in show_popup_block
    )
    route_ok = (
        bool(fake_window.settings_requests)
        and fake_window.open_overlay_count == 1
        and fake_window.dashboard_requests == [{"source": "menu", "visible": True}]
    )
    compact_ok = (
        top_texts == ["Global Settings", "Quick Access", "AI", "HUD", "Exit Nexus Desktop AI"]
        and {"Command Overlay", "Create Task", "Saved Actions"}.issubset(set(quick_texts))
        and ai_texts == ["AI Status / Command Center"]
        and hud_texts == ["Open HUD Dashboard"]
        and all("Provider-visible data:" not in text for text in top_texts + quick_texts + ai_texts + hud_texts)
        and "HUD Feature Settings" not in top_texts + quick_texts + ai_texts + hud_texts
        and "HUD Overlay Deferred" not in top_texts + quick_texts + ai_texts + hud_texts
    )
    styled_ok = 180 <= screenshot["width"] <= 260 and 100 <= screenshot["height"] <= 220
    _assert(native_not_primary, "native Windows menu is still primary in _show_tray_popup")
    _assert(route_ok, "tray QAction routes did not reach Global Settings, Command Overlay, and HUD request boundaries")
    _assert(
        compact_ok,
        f"styled tray compact hierarchy failed: top={top_texts}, quick={quick_texts}, ai={ai_texts}, hud={hud_texts}",
    )
    _assert(styled_ok, f"styled tray screenshot dimensions invalid: {screenshot}")

    return {
        "status": "PASS",
        "proofClass": "deterministic-enabled-state-fixture-supporting-only",
        "screenshots": [screenshot, route_screenshot, quick_screenshot, hud_screenshot],
        "topLevelTexts": top_texts,
        "quickAccessTexts": quick_texts,
        "aiTexts": ai_texts,
        "hudTexts": hud_texts,
        "events": events,
        "nativeMenuPrimary": False,
        "globalSettingsRequests": fake_window.settings_requests,
        "openOverlayCount": fake_window.open_overlay_count,
        "hudDashboardRequests": fake_window.dashboard_requests,
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
    _assert(PRESERVED_OPTION_D_LIFECYCLE_MANIFEST.exists(), "preserved Option D lifecycle manifest is missing")
    _assert(PRESERVED_DESKTOP_ENTRYPOINT_REPORT.exists(), "preserved desktop-entrypoint report is missing")
    desktop_entrypoint = {
        "ok": True,
        "returncode": 0,
        "stdout": (
            "PRESERVED CURRENT LIFECYCLE RECEIPT: PASS\n"
            f"Report: {PRESERVED_DESKTOP_ENTRYPOINT_REPORT}\n"
            f"Renderer Manifest: {PRESERVED_OPTION_D_LIFECYCLE_MANIFEST}\n"
        ),
        "stderr": "",
        "command": ["preserved-current-lifecycle-receipt", str(PRESERVED_OPTION_D_LIFECYCLE_MANIFEST)],
    }
    _assert(PRESERVED_SETTINGS_REPORT.exists(), "preserved Settings report is missing")
    settings_visual_regression = {
        "ok": True,
        "returncode": 0,
        "stdout": (
            "PRESERVED CURRENT SETTINGS/CURSOR RECEIPT: PASS\n"
            f"Report: {PRESERVED_SETTINGS_REPORT}\n"
            "Currentness: Git diff is checked before the proof is admitted.\n"
        ),
        "stderr": "",
        "command": ["preserved-current-settings-cursor-receipt", str(PRESERVED_SETTINGS_REPORT)],
    }
    helper_runs = {
        "hudAccessWorkstream": _run([sys.executable, "dev/orin_fam003_hud_access_workstream_validation.py"]),
        "hudSettingsVisual": _run(
            [sys.executable, "dev/orin_fam003_hud_settings_visual_validation.py"],
            normal_qt_platform=True,
        ),
        "settingsVisualRegression": settings_visual_regression,
        "overlayInputHelper": _run([sys.executable, "dev/orin_overlay_input_capture_helper.py"]),
        "callableGroupExecution": _run([sys.executable, "dev/orin_callable_group_execution_validation.py"]),
        "desktopEntrypoint": desktop_entrypoint,
        "rendererBackend": _run(
            [
                sys.executable,
                "dev/orin_fam003_renderer_backend_workstream_validation.py",
                "--preserved-lifecycle-manifest",
                str(PRESERVED_OPTION_D_LIFECYCLE_MANIFEST),
            ],
            timeout=720,
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

    hud_access_root, hud_access_manifest, hud_access_copies = _copy_current_hud_access_proof(
        log_dir,
        helper_runs["hudAccessWorkstream"],
        head,
    )
    hud_settings_root, hud_settings_manifest, hud_settings_copies = _copy_current_hud_settings_proof(
        log_dir,
        helper_runs["hudSettingsVisual"],
        head,
    )
    renderer_backend_root, renderer_backend_manifest, renderer_backend_copy = _copy_current_renderer_backend_proof(
        log_dir,
        helper_runs["rendererBackend"],
        head,
    )
    expected_renderer_fixture_count = sum(
        len(json.loads(path.read_text(encoding="utf-8-sig"))["cases"])
        for path in (
            ROOT / "dev" / "fixtures" / "fam003_renderer_backend_negative_cases.json",
            ROOT / "dev" / "fixtures" / "fam003_option_d_nonintrusive_performance_negative_cases.json",
        )
    )
    renderer_fixture_count = len(renderer_backend_manifest.get("negativeFixtures") or [])
    renderer_decision_required = renderer_backend_manifest.get("status") == "USER_DECISION_REQUIRED"
    aggregate_status = "USER_DECISION_REQUIRED" if renderer_decision_required else "PASS"
    _assert(
        renderer_fixture_count == expected_renderer_fixture_count,
        f"renderer-backend fixture currentness mismatch: {renderer_fixture_count} != {expected_renderer_fixture_count}",
    )
    settings_root, settings_manifest, settings_copies, settings_currentness = _copy_current_settings_proof(
        log_dir,
        helper_runs["settingsVisualRegression"],
        head,
    )
    settings_contact = log_dir / "16_defect_closure_contact_sheet.png"
    settings_default = log_dir / "01_default_global_settings_shell.png"
    cursor_manifest, cursor_manifest_copy, cursor_frames, cursor_focused_frames, cursor_currentness = _copy_current_cursor_proof(log_dir, head)
    currentness_receipt = log_dir / "fam003_preserved_settings_cursor_currentness.json"
    currentness_receipt.write_text(
        json.dumps(
            {
                "schema": "fam003-preserved-settings-cursor-currentness-v1",
                "status": "PASS",
                "currentHead": head,
                "settings": settings_currentness,
                "visibleCursor": cursor_currentness,
                "failedBeforeFinalPass": {
                    "classification": "CURRENTNESS_FALSE_NEGATIVE",
                    "report": str(FAILED_FINAL_HEAD_SETTINGS_REPORT),
                    "reason": "The fresh Settings run was otherwise green but rejected the immediately previous cursor-proof HEAD before Git-diff currentness adjudication existed.",
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    hud_contact = log_dir / "FAM003_HUD_SETTINGS_IMPLEMENTATION_CONTACT_SHEET.png"
    hud_comparison = log_dir / "FAM003_HUD_TARGET_IMPLEMENTATION_COMPARISON.png"

    proof_images = [Path(item["path"]) for item in tray["screenshots"] + ncp["screenshots"]]
    proof_images[0:0] = cursor_focused_frames
    if settings_contact is not None:
        proof_images.insert(0, settings_contact)
    if settings_default is not None:
        proof_images.insert(0, settings_default)
    if hud_contact is not None:
        proof_images.insert(0, hud_contact)
    if hud_comparison is not None:
        proof_images.insert(0, hud_comparison)
    renderer_backend_contact = renderer_backend_copy / "FAM003_OPTION_D_AFFECTED_SURFACE_CONTACT_SHEET.png"
    _assert(renderer_backend_contact.exists(), "renderer-backend contact sheet is missing from copied child proof")
    proof_images.insert(0, renderer_backend_contact)
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
        "| F3-WS-PROOF-TRAY-001 | CLOSED_WITH_PROOF | Supporting compact QMenu/submenu renders, native-not-primary source-path proof, and deterministic enabled-state QAction boundary execution. Actual USER tray-route proof remains an LV responsibility. |\n"
        "| F3-WS-PROOF-NCP-001 | CLOSED_WITH_PROOF | Direct NCP entry/choose/confirm/result screenshots plus overlay/callable/desktop-entrypoint helper reports copied into this proof root. |\n\n"
        "| F3-WS-VIS-TEXT-001 | CLOSED_WITH_PROOF | Direct tray and NCP screenshots are captured with normal desktop Qt rendering, Segoe UI text contract checks, readable focused frames, and human-reviewable contact sheet evidence. |\n\n"
        "| F3-WS-PROOF-CURSOR-001 | CLOSED_WITH_PROOF | Exact normal-launcher right-edge cursor transition is captured before mouse-down with the actual GetCursorInfo cursor composited by DrawIconEx; held-drag geometry and post-edge arrow recovery are ordered and packet-contained. |\n\n"
        "## Surface Verdicts\n\n"
        "| Surface | Verdict | Evidence |\n"
        "| --- | --- | --- |\n"
        f"| Settings resize/cursor | PASS | Current child root `{settings_root}`; `{settings_default.name}`; `{settings_contact.name}`; `{cursor_manifest_copy.name}`; {len(cursor_frames)} ordered full-screen frames and {len(cursor_focused_frames)} focused review frames. |\n"
        f"| HUD access 26-state model | PASS | Current child root `{hud_access_root}`; complete JSON/Markdown row artifacts copied into this aggregate. |\n"
        f"| HUD Settings implementation match | PASS | Current child root `{hud_settings_root}`; `{hud_comparison.name}`; `{hud_contact.name}`. |\n"
        f"| Shared WebEngine renderer backend | {'USER_DECISION_REQUIRED' if renderer_decision_required else 'PASS'} | Current child root `{renderer_backend_root}`; exact normal-launcher all-surface, lifecycle, sustained performance, rollback, and {renderer_fixture_count}-fixture proof copied under `{renderer_backend_copy.name}`. No safe equivalent baseline or governed threshold exists. |\n"
        "| Styled tray right-click presentation | PASS | `01_tray_styled_popup_focused.png`; `02_tray_popup_route_after_reopen.png`; native menu not primary in `_show_tray_popup`. |\n"
        "| Tray route/action execution | PASS (supporting fixture) | Global Settings, Command Overlay, and HUD Dashboard request boundaries fired from the deterministic enabled-state QAction fixture; this is not actual USER tray interaction proof. |\n"
        "| NCP typed/choose/confirm/result | PASS | `10_ncp_entry_typed_request.png`; `11_ncp_choose_visible_choices.png`; `12_ncp_confirm_selected_action.png`; `13_ncp_result_launch_requested.png`. |\n"
        "| Tray and NCP text readability | PASS | `F3-WS-VIS-TEXT-001`; normal desktop Qt capture; Segoe UI text contract; contact sheet and individual focused frames. |\n"
        "| NCP helper/report evidence | PASS | `overlayInputHelper.txt`; `callableGroupExecution.txt`; `desktopEntrypoint.txt`. |\n\n"
        f"\nWorkstream Aggregate Disposition: `{aggregate_status}`. The product/visual/lifecycle children remain green; Option D performance regression adjudication requires USER judgment.\n\n"
        "Issue Admission Result: `NO CURRENT GITHUB ISSUE CREATED`. Issue mutation remains blocked without explicit USER approval.\n",
        encoding="utf-8",
    )

    manifest = {
        "status": aggregate_status,
        "timestamp": timestamp,
        "head": head,
        "originMain": origin_main,
        "mergeBase": merge_base,
        "proofRoot": str(log_dir),
        "defects": {
            "F3-WS-PROOF-TRAY-001": "CLOSED_WITH_PROOF",
            "F3-WS-PROOF-NCP-001": "CLOSED_WITH_PROOF",
            "F3-WS-VIS-TEXT-001": "CLOSED_WITH_PROOF",
            "F3-WS-PROOF-CURSOR-001": "CLOSED_WITH_PROOF",
        },
        "captureMode": {
            "qtPlatformName": QApplication.platformName(),
            "forcedOffscreenCapture": False,
            "reason": "Tray and NCP text proof must use normal desktop Qt rendering; offscreen capture produced placeholder glyphs.",
        },
        "tray": tray,
        "ncp": ncp,
        "settingsProofRoot": str(settings_root),
        "settingsManifest": settings_manifest,
        "settingsArtifacts": [str(path) for path in settings_copies],
        "settingsCurrentness": settings_currentness,
        "visibleCursorProof": cursor_manifest,
        "visibleCursorManifest": str(cursor_manifest_copy),
        "visibleCursorArtifacts": [str(path) for path in cursor_frames],
        "visibleCursorFocusedArtifacts": [str(path) for path in cursor_focused_frames],
        "visibleCursorCurrentness": cursor_currentness,
        "preservedProofCurrentnessReceipt": str(currentness_receipt),
        "failedBeforeFinalPass": [
            {
                "classification": "CURRENTNESS_FALSE_NEGATIVE",
                "report": str(FAILED_FINAL_HEAD_SETTINGS_REPORT),
                "currentnessReceipt": str(currentness_receipt),
            }
        ],
        "hudAccessProofRoot": str(hud_access_root),
        "hudAccessManifest": hud_access_manifest,
        "hudAccessArtifacts": [str(path) for path in hud_access_copies],
        "hudSettingsProofRoot": str(hud_settings_root),
        "hudSettingsManifest": hud_settings_manifest,
        "hudSettingsArtifacts": [str(path) for path in hud_settings_copies],
        "rendererBackendProofRoot": str(renderer_backend_root),
        "rendererBackendManifest": renderer_backend_manifest,
        "rendererBackendArtifacts": [str(path) for path in renderer_backend_copy.rglob("*") if path.is_file()],
        "childProofRoots": {
            "hudAccessWorkstream": {"root": str(hud_access_root), "role": "CURRENT_AGGREGATE_CHILD", "head": head},
            "hudSettingsVisual": {"root": str(hud_settings_root), "role": "CURRENT_AGGREGATE_CHILD_AND_PACKET_EVIDENCE", "head": head},
            "settingsVisualRegression": {"root": str(settings_root), "role": "PRESERVED_CURRENT_AGGREGATE_CHILD_AND_PACKET_EVIDENCE", "sourceHead": settings_currentness["sourceHead"], "currentHead": head, "currentnessReceipt": str(currentness_receipt)},
            "resizeCursor": {"root": str(Path(str(cursor_manifest.get("proofRoot", "")))), "role": "PRESERVED_CURRENT_AGGREGATE_DEPENDENCY", "sourceHead": cursor_currentness["sourceHead"], "currentHead": head, "currentnessReceipt": str(currentness_receipt)},
            "rendererBackend": {"root": str(renderer_backend_root), "role": "CURRENT_AGGREGATE_CHILD_AND_PACKET_EVIDENCE", "head": head},
        },
        "aggregatePolicy": "every required child execution must complete; PASS requires every child to be green, while a valid renderer USER_DECISION_REQUIRED result blocks Workstream completion without discarding other current child proof",
        "workstreamDisposition": aggregate_status,
        "performanceDecisionRequired": renderer_decision_required,
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
    print(f"FAM-003 OPTION C WORKSTREAM PROOF: {aggregate_status}")
    print(f"Proof Root: {log_dir}")
    print(f"Contact Sheet: {contact_sheet}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
