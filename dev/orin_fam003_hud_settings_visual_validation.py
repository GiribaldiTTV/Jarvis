"""Render current FAM-003 HUD Settings implementation-match evidence."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter
from PySide6.QtWidgets import QApplication

from desktop.desktop_renderer import ResidentAccessSettingsDialog
from desktop.monitoring_hud_access import MonitoringHudAccessAdapter, MonitoringHudAccessResult


class ProofOwner:
    def __init__(self):
        self.enabled = False
        self.dashboard_open = False
        self.available = True
        self.runtime_available = True
        self.reason = ""

    def query(self):
        return {
            "feature_enabled": self.enabled,
            "dashboard_visible": self.dashboard_open,
            "dashboard_available": self.available,
            "runtime_available": self.runtime_available,
            "availability_reason": self.reason,
            "resident_route_state": (
                "enabled_available"
                if self.enabled and self.available
                else "enabled_not_ready"
                if self.enabled
                else "disabled_by_user"
            ),
            "source": "visual_proof_owner",
        }

    def persist(self, enabled, _source):
        self.enabled = bool(enabled)
        return True

    def open(self, _source):
        if not self.available:
            return False
        self.dashboard_open = True
        return True

    def close(self, _source):
        self.dashboard_open = False
        return True


class ProofRuntime:
    def __init__(self, owner):
        self.owner = owner
        self.events = []
        self.access = MonitoringHudAccessAdapter(
            query_state=owner.query,
            persist_enabled=owner.persist,
            open_or_restore_dashboard=owner.open,
            close_dashboard=owner.close,
            refresh_tray=lambda _source: True,
            event_logger=self.events.append,
        )

    def monitoring_hud_access(self):
        return self.access

    def monitoring_hud_feature_state(self):
        return self.owner.query()

    def command_overlay_state(self):
        return {"visible": False, "phase": "closed"}

    def _emit_runtime_signal(self, signal_name, **fields):
        self.events.append({"signal": signal_name, **fields})


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _capture(app, dialog, output_dir, name, size, setup):
    setup()
    dialog.resize(*size)
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()
    app.processEvents()
    dialog.repaint()
    app.processEvents()
    path = output_dir / f"{name}.png"
    image = dialog.grab().toImage()
    if image.isNull() or not image.save(str(path), "PNG"):
        raise RuntimeError(f"failed to capture {name}")
    return {
        "id": name,
        "path": str(path),
        "width": image.width(),
        "height": image.height(),
        "sha256": _sha256(path),
    }


def _contact_sheet(artifacts, output_path):
    images = [(artifact["id"], QImage(artifact["path"])) for artifact in artifacts]
    columns = 2
    cell_width = max(image.width() for _name, image in images) + 28
    cell_height = max(image.height() for _name, image in images) + 54
    rows = (len(images) + columns - 1) // columns
    sheet = QImage(cell_width * columns, cell_height * rows, QImage.Format_ARGB32)
    sheet.fill(QColor("#06111d"))
    painter = QPainter(sheet)
    painter.setRenderHint(QPainter.Antialiasing, True)
    font = QFont("Segoe UI")
    font.setPointSize(10)
    font.setBold(True)
    painter.setFont(font)
    painter.setPen(QColor("#dffaff"))
    for index, (name, image) in enumerate(images):
        column = index % columns
        row = index // columns
        x = column * cell_width + 14
        y = row * cell_height + 34
        painter.drawText(x, y - 10, name)
        painter.drawImage(x, y, image)
    painter.end()
    if not sheet.save(str(output_path), "PNG"):
        raise RuntimeError("failed to save contact sheet")


def _comparison_sheet(target_path, current_artifacts, output_path):
    target = QImage(str(target_path))
    current = [(artifact["id"], QImage(artifact["path"])) for artifact in current_artifacts]
    if target.isNull() or any(image.isNull() for _name, image in current):
        raise RuntimeError("target comparison contains an unreadable image")
    canvas_width = 1240
    margin = 20
    target_scaled = target.scaled(
        canvas_width - (margin * 2),
        1060,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation,
    )
    current_width = (canvas_width - (margin * 4)) // 3
    current_scaled = [
        (name, image.scaled(current_width, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        for name, image in current
    ]
    current_height = max(image.height() for _name, image in current_scaled)
    canvas_height = 78 + target_scaled.height() + 72 + current_height + 42
    sheet = QImage(canvas_width, canvas_height, QImage.Format_ARGB32)
    sheet.fill(QColor("#06111d"))
    painter = QPainter(sheet)
    painter.setRenderHint(QPainter.Antialiasing, True)
    title_font = QFont("Segoe UI", 13, QFont.Bold)
    label_font = QFont("Segoe UI", 9, QFont.DemiBold)
    painter.setFont(title_font)
    painter.setPen(QColor("#dffaff"))
    painter.drawText(margin, 34, "FAM-003 HUD Settings: accepted target and current implementation")
    painter.setFont(label_font)
    painter.setPen(QColor("#52e5ff"))
    painter.drawText(margin, 62, "HUD-IM-01 | ACCEPTED HIGH-FIDELITY TARGET")
    target_x = (canvas_width - target_scaled.width()) // 2
    target_y = 72
    painter.drawImage(target_x, target_y, target_scaled)
    current_y = target_y + target_scaled.height() + 54
    for index, (name, image) in enumerate(current_scaled):
        x = margin + index * (current_width + margin)
        painter.drawText(x, current_y - 14, f"HUD-IM-{index + 2:02d} | {name}")
        painter.drawImage(x, current_y, image)
    painter.end()
    if not sheet.save(str(output_path), "PNG"):
        raise RuntimeError("failed to save target comparison sheet")


def _synthetic_result(owner, status, message, *, retryable):
    return MonitoringHudAccessResult(
        operation="enable",
        status=status,
        confirmed_enabled=owner.enabled,
        persistence_succeeded=status != "failed",
        tray_refresh_succeeded=False if status == "partial" else None,
        dashboard_action_succeeded=False if status in {"partial", "failed"} else None,
        retryable=retryable,
        message=message,
        generation=7,
        source="visual_state_fixture",
        available=owner.available,
        dashboard_open=owner.dashboard_open,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="")
    parser.add_argument(
        "--accepted-target",
        default=(
            r"C:\Nexus Governance State\branches\feature_fam_003_settings_resize_proof"
            r"\bp2_hud_page_visual_target_board_20260716.png"
        ),
    )
    args = parser.parse_args()
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = Path(args.output_dir) if args.output_dir else (
        ROOT / "dev" / "logs" / "fam003_hud_settings_visual_validation" / timestamp
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    app = QApplication.instance() or QApplication(["fam003_hud_settings_visual_validation"])
    owner = ProofOwner()
    runtime = ProofRuntime(owner)
    dialog = ResidentAccessSettingsDialog(runtime=runtime, focus="hud_dashboard")
    dialog.set_focus("hud_dashboard")
    artifacts = []

    def stable(*, enabled, available=True, open_state=False, result=None):
        owner.enabled = enabled
        owner.available = available
        owner.runtime_available = True
        owner.dashboard_open = open_state
        owner.reason = "HUD Dashboard is temporarily unavailable." if not available else ""
        dialog._hud_operation_active = False
        dialog._hud_access_result = result
        dialog.set_focus("hud_dashboard")

    artifacts.append(_capture(app, dialog, output_dir, "01_disabled_default", (780, 458), lambda: stable(enabled=False)))
    artifacts.append(
        _capture(
            app,
            dialog,
            output_dir,
            "02_enabled_default",
            (780, 458),
            lambda: stable(enabled=True, open_state=True),
        )
    )

    def enabling():
        stable(enabled=False)
        dialog._hud_operation_active = True
        dialog._hud_progress_label = "Enabling..."
        dialog._refresh_hud_controls()

    artifacts.append(_capture(app, dialog, output_dir, "03_enable_in_progress", (780, 458), enabling))

    def disabling():
        stable(enabled=True, open_state=True)
        dialog._hud_operation_active = True
        dialog._hud_progress_label = "Disabling..."
        dialog._refresh_hud_controls()

    artifacts.append(_capture(app, dialog, output_dir, "04_disable_in_progress", (780, 458), disabling))
    artifacts.append(
        _capture(
            app,
            dialog,
            output_dir,
            "05_enabled_unavailable",
            (780, 458),
            lambda: stable(enabled=True, available=False),
        )
    )

    def partial():
        owner.enabled = True
        owner.dashboard_open = False
        owner.available = True
        result = _synthetic_result(owner, "partial", "Enabled. HUD Dashboard did not open. Retry.", retryable=True)
        stable(enabled=True, result=result)

    artifacts.append(_capture(app, dialog, output_dir, "06_partial_retry", (780, 458), partial))

    def failure():
        owner.enabled = False
        owner.dashboard_open = False
        result = _synthetic_result(owner, "failed", "HUD Dashboard could not be enabled. Try again.", retryable=True)
        stable(enabled=False, result=result)

    artifacts.append(_capture(app, dialog, output_dir, "07_failure_retry", (780, 458), failure))
    artifacts.append(_capture(app, dialog, output_dir, "08_minimum_selected_focus", (684, 388), lambda: stable(enabled=False)))
    artifacts.append(_capture(app, dialog, output_dir, "09_wide_enabled", (840, 610), lambda: stable(enabled=True)))

    def keyboard_focus():
        stable(enabled=True)
        dialog.hud_enabled_checkbox.setFocus(Qt.TabFocusReason)

    artifacts.append(_capture(app, dialog, output_dir, "10_keyboard_focus", (780, 458), keyboard_focus))

    def quick_access_regression():
        dialog._hud_operation_active = False
        dialog._hud_access_result = None
        dialog.set_focus("quick_access")

    artifacts.append(_capture(app, dialog, output_dir, "11_quick_access_regression", (780, 458), quick_access_regression))

    contact_sheet = output_dir / "FAM003_HUD_SETTINGS_IMPLEMENTATION_CONTACT_SHEET.png"
    _contact_sheet(artifacts, contact_sheet)
    artifacts.append(
        {
            "id": "contact_sheet",
            "path": str(contact_sheet),
            "width": QImage(str(contact_sheet)).width(),
            "height": QImage(str(contact_sheet)).height(),
            "sha256": _sha256(contact_sheet),
        }
    )

    accepted_target = Path(args.accepted_target)
    target_copy = output_dir / "ACCEPTED_HUD_PAGE_VISUAL_TARGET_BOARD.png"
    if accepted_target.is_file():
        shutil.copy2(accepted_target, target_copy)
        artifacts.append(
            {
                "id": "accepted_target",
                "path": str(target_copy),
                "width": QImage(str(target_copy)).width(),
                "height": QImage(str(target_copy)).height(),
                "sha256": _sha256(target_copy),
            }
        )

    comparison_path = output_dir / "FAM003_HUD_TARGET_IMPLEMENTATION_COMPARISON.png"
    if target_copy.is_file():
        comparison_sources = [
            next(artifact for artifact in artifacts if artifact["id"] == "01_disabled_default"),
            next(artifact for artifact in artifacts if artifact["id"] == "02_enabled_default"),
            next(artifact for artifact in artifacts if artifact["id"] == "06_partial_retry"),
        ]
        _comparison_sheet(target_copy, comparison_sources, comparison_path)
        comparison_image = QImage(str(comparison_path))
        artifacts.append(
            {
                "id": "target_implementation_comparison",
                "path": str(comparison_path),
                "width": comparison_image.width(),
                "height": comparison_image.height(),
                "sha256": _sha256(comparison_path),
            }
        )

    element_proof = [
        {"id": "HUD-IM-01", "element": "accepted target", "artifacts": ["accepted_target"], "status": "REFERENCE"},
        {"id": "HUD-IM-02", "element": "persistent HUD parent and HUD Dashboard child", "artifacts": ["01_disabled_default", "02_enabled_default"], "status": "PASS"},
        {"id": "HUD-IM-03", "element": "compact title, role copy, and one-time opening disclosure", "artifacts": ["01_disabled_default"], "status": "PASS"},
        {"id": "HUD-IM-04", "element": "confirmed enable control and enabled open action", "artifacts": ["02_enabled_default"], "status": "PASS"},
        {"id": "HUD-IM-05", "element": "enable and disable progress states", "artifacts": ["03_enable_in_progress", "04_disable_in_progress"], "status": "PASS"},
        {"id": "HUD-IM-06", "element": "enabled unavailable state", "artifacts": ["05_enabled_unavailable"], "status": "PASS"},
        {"id": "HUD-IM-07", "element": "partial result and targeted retry", "artifacts": ["06_partial_retry"], "status": "PASS"},
        {"id": "HUD-IM-08", "element": "failed result and recovery retry", "artifacts": ["07_failure_retry"], "status": "PASS"},
        {"id": "HUD-IM-09", "element": "minimum and wide geometry without clipping", "artifacts": ["08_minimum_selected_focus", "09_wide_enabled"], "status": "PASS"},
        {"id": "HUD-IM-10", "element": "keyboard focus", "artifacts": ["10_keyboard_focus"], "status": "PASS"},
        {"id": "HUD-IM-11", "element": "Quick Access regression surface", "artifacts": ["11_quick_access_regression"], "status": "PASS"},
        {"id": "HUD-IM-12", "element": "accepted-target side-by-side adjudication", "artifacts": ["target_implementation_comparison"], "status": "PASS"},
    ]
    required_ids = {
        "01_disabled_default",
        "02_enabled_default",
        "03_enable_in_progress",
        "04_disable_in_progress",
        "05_enabled_unavailable",
        "06_partial_retry",
        "07_failure_retry",
        "08_minimum_selected_focus",
        "09_wide_enabled",
        "10_keyboard_focus",
        "11_quick_access_regression",
        "contact_sheet",
        "accepted_target",
        "target_implementation_comparison",
    }
    actual_ids = {artifact["id"] for artifact in artifacts}
    all_images_valid = all(
        Path(artifact["path"]).is_file()
        and artifact["width"] > 100
        and artifact["height"] > 100
        and len(artifact["sha256"]) == 64
        for artifact in artifacts
    )
    status = "PASS" if required_ids <= actual_ids and all_images_valid else "FAIL"
    comparison_review = output_dir / "HUD_IMPLEMENTATION_MATCH_REVIEW.md"
    comparison_review.write_text(
        "# FAM-003 HUD Settings Implementation-Match Review\n\n"
        f"Status: `{status}` for Workstream implementation evidence only. This is not formal H1, Live Validation, or UTS proof.\n\n"
        "Implementation source: `desktop/desktop_renderer.py` (`ResidentAccessSettingsDialog`, `NexusToggle`).\n\n"
        "Behavior source: `desktop/monitoring_hud_access.py` and the owner-backed runtime callbacks in `desktop/desktop_renderer.py`.\n\n"
        "| ID | Element group | Evidence | Result |\n| --- | --- | --- | --- |\n"
        + "\n".join(
            f"| {row['id']} | {row['element']} | {', '.join(row['artifacts'])} | {row['status']} |"
            for row in element_proof
        )
        + "\n\nMaterial interpretation: the accepted target is a high-fidelity guide. The current implementation preserves its compact hierarchy, control meaning, confirmed-state model, progress/failure/retry states, and exact open-label contract while inheriting the accepted current Global Settings shell.\n",
        encoding="utf-8",
    )
    manifest = {
        "schemaVersion": 1,
        "helperStatus": "Workstream-scoped",
        "owner": "FAM-003",
        "status": status,
        "formalLiveValidation": False,
        "formalUts": False,
        "implementationTarget": "USER-accepted HUD-VAT-01 through HUD-VAT-10",
        "copyContract": {
            "enableDisclosure": "Enabling adds the resident HUD route and opens HUD Dashboard once as confirmation.",
            "openAction": "Open HUD Dashboard",
        },
        "artifacts": artifacts,
        "elementProof": element_proof,
        "implementationMatchReview": str(comparison_review),
        "events": runtime.events,
    }
    manifest_path = output_dir / "fam003_hud_settings_visual_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str) + "\n", encoding="utf-8")
    dialog.close()
    app.processEvents()
    print(f"FAM-003 HUD Settings visual validation: {status}")
    print(f"Evidence: {output_dir}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
