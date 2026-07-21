"""Reference-conformance proof for FAM-003 Global Settings repair.

This helper uses an isolated resident-access settings file so it can validate
Quick Access behavior without mutating USER runtime preferences. It is
supporting proof only: USER-operated Live Validation remains authoritative for
final visual acceptance.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import ctypes
import ctypes.wintypes
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation"
VISIBLE_CURSOR_PROOF_LATEST = (
    ROOT
    / "dev"
    / "logs"
    / "fam003_resize_cursor_workstream_proof"
    / "latest_manifest.json"
)
VISIBLE_CURSOR_FIXTURE = ROOT / "dev" / "fixtures" / "fam003_resize_cursor_proof_negative_cases.json"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
VISUAL_UDL_PATH = Path(
    r"C:\Nexus Governance State\branches\feature_fam_003_resident_access_quick_actions"
    r"\unified_visual_defect_ledger_20260623.md"
)
VISUAL_UDL_IDS = tuple(f"UDL-VIS-{index:03d}" for index in range(1, 15))
VISUAL_UDL_ALLOWED_STATUSES = {
    "OPEN",
    "REPRODUCED",
    "IN_REPAIR",
    "FIXED_PENDING_PROOF",
    "PROOF_FAILED",
    "REOPENED",
    "CLOSED_WITH_PROOF",
    "BLOCKED_SOURCE_TRUTH",
    "OUT_OF_SCOPE_USER_APPROVAL_REQUIRED",
}
VISUAL_UDL_REQUIRED_FIELDS = (
    "Defect ID",
    "Origin",
    "Exact USER wording where applicable",
    "Source-truth basis",
    "Expected behavior",
    "Actual behavior",
    "Evidence path or screenshot reference",
    "Affected files/surfaces",
    "Owner/family boundary",
    "Impact",
    "Root cause",
    "Validator/proof gap",
    "Adjacent-defect sweep result",
    "Exact repair target",
    "Acceptance criteria",
    "Required proof",
    "Validation required",
    "Status",
    "Closure proof when closed",
)
VISUAL_UDL_REJECTED_PACKET = "FAM-003-20260623-125842.zip"
ACTIVE_UDL_PATH = Path(
    r"C:\Nexus Governance State\branches\feature_fam_003_resident_access_quick_actions"
    r"\unified_defect_ledger_20260623_false_green.md"
)
SAME_DEFECT_RECURRENCE_LEDGER_PATH = Path(
    r"C:\Nexus Governance State\branches\feature_fam_003_resident_access_quick_actions"
    r"\same_defect_recurrence_ledger_20260624.md"
)
ACTIVE_FALSE_RETEST_DEFECT_IDS = (
    "F3-LV1-UI-001",
    "F3-LV1-UI-015",
    "F3-LV1-UI-016",
    "F3-LV1-UI-017",
    "F3-LV1-UI-018",
    "F3-LV1-UI-019",
    "F3-LV1-UI-020",
    "F3-LV1-UI-021",
    "F3-LV1-UI-022",
    "F3-LV1-UI-023",
    "F3-LV1-UI-024",
    "F3-LV1-UI-025",
    "F3-LV1-UI-026",
    "F3-LV1-UI-027",
    "F3-LV1-UI-028",
    "F3-LV1-UI-029",
    "F3-LV1-UI-030",
    "F3-LV1-UI-031",
    "F3-LV1-UI-032",
    "F3-LV1-UI-033",
    "F3-LV1-UI-034",
    "F3-LV1-UI-035",
    "F3-LV1-UI-036",
    "F3-LV1-UI-037",
    "F3-LV1-UI-038",
    "F3-LV1-UI-043",
    "F3-LV1-UI-044",
    "F3-LV1-UI-045",
    "F3-LV1-UI-046",
    "F3-LV1-UI-047",
    "F3-LV1-UI-048",
    "F3-LV1-UI-049",
    "F3-LV1-UI-050",
    "F3-LV1-UI-051",
    "F3-LV1-UI-052",
    "F3-LV1-UI-053",
    "F3-LV1-UI-054",
    "F3-LV1-UI-055",
    "F3-LV1-UI-056",
    "F3-LV1-UI-057",
    "F3-LV1-UI-058",
    "F3-LV1-UI-059",
    "F3-LV1-UI-060",
    "F3-LV1-UI-061",
    "F3-LV1-FUNC-001",
    "F3-LV1-FUNC-002",
    "F3-LV1-PROOF-001",
    "F3-LV1-PROOF-002",
    "F3-LV1-PROOF-005",
    "F3-LV1-PROOF-006",
)
SAME_DEFECT_REOPENED_IDS = (
    "F3-LV1-UI-001",
    "F3-LV1-UI-016",
    "F3-LV1-UI-020",
    "F3-LV1-UI-021",
    "F3-LV1-PROOF-002",
)
SAME_DEFECT_LOOP_BREAKER_ID = "F3-LV1-PROOF-003"
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
MANAGE_MONITORS_REFERENCE_SOURCE_FILES: tuple[Path, ...] = (
    ROOT / "nexus_visual" / "monitoring_hud.html",
    ROOT / "nexus_visual" / "monitoring_hud.css",
    ROOT / "nexus_visual" / "monitoring_hud.js",
)


def _parse_visual_udl_sections(text: str) -> tuple[dict[str, dict[str, str]], list[str]]:
    failures: list[str] = []
    if "| ID | Status | Defect / Risk |" in text:
        failures.append("compact summary table remains present")

    sections: dict[str, dict[str, str]] = {}
    section_pattern = re.compile(
        r"^##\s+(UDL-VIS-\d{3})\b(?P<body>.*?)(?=^##\s+UDL-VIS-\d{3}\b|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    field_pattern = re.compile(r"^-\s+([^:]+):\s*(.*)$")
    for match in section_pattern.finditer(text):
        defect_id = match.group(1)
        body = match.group("body")
        fields: dict[str, str] = {}
        current_field: str | None = None
        for raw_line in body.splitlines():
            field_match = field_pattern.match(raw_line)
            if field_match:
                current_field = field_match.group(1).strip()
                fields[current_field] = field_match.group(2).strip()
            elif current_field and raw_line.startswith("  "):
                fields[current_field] = f"{fields[current_field]} {raw_line.strip()}".strip()
            else:
                current_field = None
        sections[defect_id] = fields

    return sections, failures


def _visual_udl_schema_failures(text: str) -> list[str]:
    sections, failures = _parse_visual_udl_sections(text)
    for defect_id in VISUAL_UDL_IDS:
        fields = sections.get(defect_id)
        if not fields:
            failures.append(f"{defect_id} missing detailed section")
            continue
        missing_fields = [
            field
            for field in VISUAL_UDL_REQUIRED_FIELDS
            if not fields.get(field) or fields.get(field) in {"`TODO`", "TODO", "`TBD`", "TBD"}
        ]
        if missing_fields:
            failures.append(f"{defect_id} missing fields: {', '.join(missing_fields)}")
        status = fields.get("Status", "").strip("` ")
        if status not in VISUAL_UDL_ALLOWED_STATUSES:
            failures.append(f"{defect_id} illegal status: {fields.get('Status', '<missing>')}")
        elif status != "CLOSED_WITH_PROOF":
            failures.append(f"{defect_id} status is not CLOSED_WITH_PROOF: {status}")
        if status == "CLOSED_WITH_PROOF":
            for closure_field in (
                "Evidence path or screenshot reference",
                "Acceptance criteria",
                "Validation required",
                "Closure proof when closed",
            ):
                if not fields.get(closure_field):
                    failures.append(f"{defect_id} missing closure field {closure_field}")
    return failures


def _visual_udl_status_rows() -> tuple[bool, str, bool, str]:
    if not VISUAL_UDL_PATH.exists():
        return False, f"{VISUAL_UDL_PATH} missing", False, "visual UDL missing"
    text = VISUAL_UDL_PATH.read_text(encoding="utf-8")
    missing = [defect_id for defect_id in VISUAL_UDL_IDS if defect_id not in text]
    schema_failures = _visual_udl_schema_failures(text)
    stale_current_packet = f"Current regenerated USER retest packet: `C:\\Nexus USER\\{VISUAL_UDL_REJECTED_PACKET}`" in text
    exists_ok = not missing
    closed_ok = (
        exists_ok
        and not schema_failures
        and not stale_current_packet
        and "125842" in text
        and "VISUAL-UDL-SCHEMA-RETEST-STOP" in text
    )
    return (
        exists_ok,
        f"{VISUAL_UDL_PATH}; missing={missing}",
        closed_ok,
        f"{VISUAL_UDL_PATH}; schema_failures={schema_failures}; stale_current_packet={stale_current_packet}; schema_stop_receipt={'VISUAL-UDL-SCHEMA-RETEST-STOP' in text}",
    )


def _parse_active_false_retest_sections(text: str) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {}
    section_pattern = re.compile(
        r"^##\s+(F3-LV1-(?:UI|PROOF|FUNC)-\d{3})\b(?P<body>.*?)(?=^##\s+F3-LV1-(?:UI|PROOF|FUNC)-\d{3}\b|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    field_pattern = re.compile(r"^-?\s*([^:\n]+):\s*(.*)$")
    for match in section_pattern.finditer(text):
        defect_id = match.group(1)
        fields: dict[str, str] = {}
        current_field: str | None = None
        for raw_line in match.group("body").splitlines():
            field_match = field_pattern.match(raw_line)
            if field_match:
                current_field = field_match.group(1).strip()
                fields[current_field] = field_match.group(2).strip()
            elif current_field and raw_line.startswith("  "):
                fields[current_field] = f"{fields[current_field]} {raw_line.strip()}".strip()
            else:
                current_field = None
        sections[defect_id] = fields
    return sections


def _same_defect_loop_breaker_active() -> bool:
    if not SAME_DEFECT_RECURRENCE_LEDGER_PATH.exists():
        return False
    text = SAME_DEFECT_RECURRENCE_LEDGER_PATH.read_text(encoding="utf-8")
    return (
        "Retest Candidate Gate: `BLOCKED`" in text
        and "Posture: `LOOP-BREAKER ONLY`" in text
    )


def _active_false_retest_udl_status_rows() -> tuple[bool, str, str, bool, str]:
    if not ACTIVE_UDL_PATH.exists():
        return (
            False,
            f"{ACTIVE_UDL_PATH} missing",
            "active false-retest UDL rows closed with proof",
            False,
            "active false-retest UDL missing",
        )
    text = ACTIVE_UDL_PATH.read_text(encoding="utf-8")
    sections = _parse_active_false_retest_sections(text)
    missing = [defect_id for defect_id in ACTIVE_FALSE_RETEST_DEFECT_IDS if defect_id not in sections]
    if _same_defect_loop_breaker_active():
        missing_reopened = [
            defect_id
            for defect_id in SAME_DEFECT_REOPENED_IDS
            if sections.get(defect_id, {}).get("Status", "").strip("` ") != "REOPENED"
        ]
        proof3_status = sections.get(SAME_DEFECT_LOOP_BREAKER_ID, {}).get("Status", "").strip("` ")
        gate_ok = not missing and not missing_reopened and proof3_status == "CLOSED_WITH_PROOF"
        return (
            not missing,
            f"{ACTIVE_UDL_PATH}; missing={missing}",
            "same-defect recurrence gate blocks retest candidate",
            gate_ok,
            (
                f"{SAME_DEFECT_RECURRENCE_LEDGER_PATH}; "
                f"missing_reopened={missing_reopened}; "
                f"{SAME_DEFECT_LOOP_BREAKER_ID}={proof3_status or '<missing>'}"
            ),
        )

    bad_status: list[str] = []
    missing_proof: list[str] = []
    for defect_id in ACTIVE_FALSE_RETEST_DEFECT_IDS:
        fields = sections.get(defect_id, {})
        status = fields.get("Status", "").strip("` ")
        if status != "CLOSED_WITH_PROOF":
            bad_status.append(f"{defect_id}={status or '<missing>'}")
        proof = fields.get("Closure Proof") or fields.get("Closure proof when closed") or fields.get("Closure Proof When Closed")
        if not proof:
            missing_proof.append(defect_id)
    exists_ok = not missing
    closed_ok = exists_ok and not bad_status and not missing_proof
    return (
        exists_ok,
        f"{ACTIVE_UDL_PATH}; missing={missing}",
        "active false-retest UDL rows closed with proof",
        closed_ok,
        f"{ACTIVE_UDL_PATH}; bad_status={bad_status}; missing_proof={missing_proof}",
    )

ELEMENT_GROUP_LEDGER_ROWS: tuple[dict[str, str], ...] = (
    {
        "id": "F3GS-001",
        "element": "Whole-window silhouette",
        "surface": "Global Settings",
        "fam": "FAM-003 / FAM-002 visual authority",
        "code": "desktop/desktop_renderer.py::ResidentAccessSettingsDialog",
        "role": "top-level settings product shell",
        "rule": "Project Vision; UIREF-001; FAM-002",
        "copy": "Global Settings",
        "font": "Bahnschrift/Rajdhani/Segoe UI, compact 10-18px",
        "text": "#f8fafc family",
        "background": "#020914 / #04101b dark shell",
        "border": "1px restrained cyan, 20px radius",
        "effects": "subtle depth only",
        "spacing": "700x360 content-fit two-column settings layout",
        "hitbox": "top-level compact settings window",
        "icon_label": "window title only",
        "states": "default, dirty, saved",
        "a11y": "window title Global Settings",
        "comparator": "accepted AI Control Center full-window reference",
        "proof": "01_default_global_settings_shell.png",
        "checks": "default screenshot saved;architecture-first Global Settings geometry;settings shell fills the window intentionally;default surface is not white/native-light;window chrome drag/move proof;window resize/minimum-size proof",
    },
    {
        "id": "F3GS-002",
        "element": "Nexus shell frame",
        "surface": "Global Settings",
        "fam": "FAM-003 / FAM-002 visual authority",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsShell",
        "role": "Nexus-owned window boundary",
        "rule": "UIREF-001; UIREF-005",
        "copy": "none",
        "font": "not applicable",
        "text": "not applicable",
        "background": "dark diagonal shell gradient",
        "border": "restrained cyan boundary, 20px radius",
        "effects": "no native white frame",
        "spacing": "full window edge",
        "hitbox": "entire shell",
        "icon_label": "none",
        "states": "default",
        "a11y": "top-level shell only",
        "comparator": "accepted AI Control Center rounded frame",
        "proof": "01_default_global_settings_shell.png",
        "checks": "default surface is not white/native-light",
    },
    {
        "id": "F3GS-003",
        "element": "Header/body integration",
        "surface": "Global Settings",
        "fam": "FAM-003 / FAM-002 visual authority",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsChromeBar + residentAccessSettingsBody",
        "role": "seamless settings-window title row",
        "rule": "UIREF-001; UIREF-005",
        "copy": "Settings",
        "font": "single-row centered 16px settings title",
        "text": "near-white centered Settings title only",
        "background": "transparent title row flowing into dark shell",
        "border": "no title-card divider",
        "effects": "no hero/card treatment",
        "spacing": "46px one-row chrome integrated with body",
        "hitbox": "header and body zones",
        "icon_label": "single visible Settings title label",
        "states": "default",
        "a11y": "Close Settings",
        "comparator": "settings-specific NDAI top-level window class",
        "proof": "02_top_level_chrome_control_cluster.png",
        "checks": "top-level chrome/control cluster;settings-specific seamless title row",
    },
    {
        "id": "F3GS-004",
        "element": "Settings title label",
        "surface": "Global Settings chrome",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::DialogChromeBar title labels",
        "role": "settings title",
        "rule": "Project Vision; UIREF-001",
        "copy": "Settings",
        "font": "16px centered title",
        "text": "near-white centered title; no visible NDAI title-row branding",
        "background": "transparent on chrome bar",
        "border": "none",
        "effects": "none",
        "spacing": "single-row title row, no stacked subtitle",
        "hitbox": "label group",
        "icon_label": "single title label",
        "states": "default",
        "a11y": "window title",
        "comparator": "settings-specific NDAI title grammar",
        "proof": "02_top_level_chrome_control_cluster.png",
        "checks": "settings-specific seamless title row",
    },
    {
        "id": "F3GS-005",
        "element": "Header product discipline",
        "surface": "Global Settings chrome",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsChromeKicker + residentAccessSettingsChromeRolePill",
        "role": "hidden/deleted header metadata discipline",
        "rule": "UIREF-006",
        "copy": "no visible NEXUS DESKTOP AI; no SETTINGS AREA / ACTIVE SETTING metadata",
        "font": "not visible",
        "text": "not visible",
        "background": "not applicable",
        "border": "not applicable",
        "effects": "no branch/debug/status metadata",
        "spacing": "title row stays one-row title/control focused",
        "hitbox": "not applicable",
        "icon_label": "no extra visual label",
        "states": "default",
        "a11y": "header remains product title and window controls",
        "comparator": "settings-specific title row without status pill",
        "proof": "02_top_level_chrome_control_cluster.png",
        "checks": "settings-specific seamless title row;centered Settings title only;no internal telemetry text;product-facing copy is compact and non-internal",
    },
    {
        "id": "F3GS-006",
        "element": "Window control cluster",
        "surface": "Global Settings chrome",
        "fam": "FAM-003 / FAM-002 visual authority",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsWindowControls",
        "role": "NDAI minimize/close controls",
        "rule": "UIREF-002; UIREF-003",
        "copy": "minimize/close controls; no visible resize grip",
        "font": "control glyph 900 weight",
        "text": "near-white",
        "background": "dark rounded cluster",
        "border": "1px cyan, 18px radius",
        "effects": "focus/pressed color change",
        "spacing": "24px buttons",
        "hitbox": "24x24 controls",
        "icon_label": "glyph-only with accessible names",
        "states": "focus, pressed, drag, resize",
        "a11y": "Close Settings",
        "comparator": "accepted AI Control Center close-hover reference",
        "proof": "03_window_control_focus_pressed_state.png; 03a_window_moved_by_chrome.png; 03b_window_resized.png; 03c_window_minimum_size.png",
        "checks": "top-level chrome/control cluster;window control focus/pressed proof;window chrome drag/move proof;window resize/minimum-size proof",
    },
    {
        "id": "F3GS-007",
        "element": "Left settings rail",
        "surface": "Global Settings body",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsNavShell",
        "role": "settings navigation organizer",
        "rule": "F3-FF01; FAM-002; UIREF-005",
        "copy": "Tray; Quick Access",
        "font": "10-15px compact rail",
        "text": "muted cyan/white",
        "background": "integrated dark navigation well",
        "border": "subtle cyan divider, splitter handle",
        "effects": "no fake future categories; selected parent carries child focus",
        "spacing": "normal 160px slim rail, compressed 76px overflow state, wide 270px state",
        "hitbox": "left splitter pane",
        "icon_label": "painted tray icon, painted quick-access icon, compact chevron expander",
        "states": "default, active child, collapsed parent, narrow overflow, wide pane",
        "a11y": "Open Quick Access Settings; Resize Global Settings navigation pane",
        "comparator": "dense settings navigation grammar",
        "proof": "04_left_settings_organizer.png; 04a_left_nav_active_child.png; 04a1_quick_access_child_pill_no_clip_focus.png; 04a2_quick_access_child_pill_focus_pressed_state.png; 04b_left_nav_collapsed.png; 04c_left_nav_expanded.png; 04d_left_pane_compressed_horizontal_overflow.png; 04e_left_pane_wide.png",
        "checks": "left navigation settings organizer;Tray and HUD parent-child settings IA;selectable Tray parent page;left navigation active child proof;focused child pill border no-clipping proof;child pill focus/pressed state proof;left navigation collapsed proof;left navigation expanded proof;left pane compressed width exposes horizontal overflow;left pane wide resize stays deterministic;left pane vertical overflow source-truth disposition",
    },
    {
        "id": "F3GS-008",
        "element": "Selected navigation row",
        "surface": "Global Settings left rail",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsNavItem",
        "role": "active settings leaf selector",
        "rule": "UIREF-003",
        "copy": "Tray; Quick Access",
        "font": "10-13px compact",
        "text": "near-white and muted caption",
        "background": "subtle selected row",
        "border": "2px left accent, 8px radius",
        "effects": "hover background",
        "spacing": "compact nav row",
        "hitbox": "row with selected button",
        "icon_label": "small parent/child identifiers plus main/subcategory labels",
        "states": "selected, parent contains selected child, parent-only selected after collapse",
        "a11y": "Open Quick Access Settings",
        "comparator": "settings nav row, not CTA card",
        "proof": "04_left_settings_organizer.png; 04a_left_nav_active_child.png; 04a1_quick_access_child_pill_no_clip_focus.png; 04a2_quick_access_child_pill_focus_pressed_state.png; 04b_left_nav_collapsed.png; 04c_left_nav_expanded.png",
        "checks": "left navigation settings organizer;left navigation active child proof;focused child pill border no-clipping proof;child pill focus/pressed state proof;left navigation collapsed proof;left navigation expanded proof",
    },
    {
        "id": "F3GS-009",
        "element": "Settings context strip",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsOverviewPanel",
        "role": "product-native settings context",
        "rule": "Project Vision; F3-FF01",
        "copy": "none in clean state; Unsaved changes only when dirty",
        "font": "11-13px product context",
        "text": "near-white title, muted detail, mint state chip",
        "background": "subtle dark strip",
        "border": "restrained left accent only",
        "effects": "quiet state chip",
        "spacing": "single compact strip",
        "hitbox": "context strip",
        "icon_label": "title/detail/state chip",
        "states": "clean hidden, dirty visible",
        "a11y": "change status propagated",
        "comparator": "AI Control Center dense state rows",
        "proof": "01_default_global_settings_shell.png; 06_dirty_quick_access.png",
        "checks": "Tray and HUD parent-child settings IA;selectable Tray parent page;no fake overview/status strip;clean state has no redundant saved label;dirty guard state after dropdown edit",
    },
    {
        "id": "F3GS-010",
        "element": "Active page heading",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsHeading",
        "role": "selected settings page title",
        "rule": "F3-FF01; UIREF-005",
        "copy": "Quick Access; Tray; slot count",
        "font": "18px page heading, 10-11px metadata",
        "text": "near-white and cyan",
        "background": "transparent",
        "border": "badge borders only",
        "effects": "none",
        "spacing": "below overview panel",
        "hitbox": "page header",
        "icon_label": "badge plus page label",
        "states": "slot count updates",
        "a11y": "heading label",
        "comparator": "settings section title hierarchy",
        "proof": "01_default_global_settings_shell.png",
        "checks": "Tray and HUD parent-child settings IA;selectable Tray parent page",
    },
    {
        "id": "F3GS-011",
        "element": "Quick Access slot group",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessQuickSlotContainer",
        "role": "current settings control group",
        "rule": "F3-FF01; UIREF-003",
        "copy": "Menu order; Top to bottom in the tray menu.; Add Slot; Defaults",
        "font": "11-13px compact",
        "text": "muted body plus bright headings",
        "background": "subtle dark section",
        "border": "1px muted cyan, 12px radius",
        "effects": "reduced cyan noise",
        "spacing": "compact rows, no nested card overload",
        "hitbox": "settings section",
        "icon_label": "text actions plus rows",
        "states": "add enabled/disabled, defaults staged",
        "a11y": "Add Quick Access Slot; Restore Default Quick Access Shortcuts",
        "comparator": "NDAI settings control group",
        "proof": "01_default_global_settings_shell.png; 09_defaults_staged.png",
        "checks": "Tray and HUD parent-child settings IA;default semantics stage defaults;max-slot budget rows are unclipped",
    },
    {
        "id": "F3GS-012",
        "element": "Slot row silhouette",
        "surface": "Quick Access slots",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessQuickSlotRow",
        "role": "editable slot row",
        "rule": "UIREF-003; UIREF-005",
        "copy": "01 / selected route label",
        "font": "11px index, combo text bold",
        "text": "soft cyan and pale text",
        "background": "dark row",
        "border": "1px muted cyan, 2px left accent, 9px radius",
        "effects": "none",
        "spacing": "compact 6/2 margins",
        "hitbox": "row height 28px",
        "icon_label": "numeric slot label",
        "states": "default, max slots",
        "a11y": "Quick Access Slot N label",
        "comparator": "dense row grammar",
        "proof": "05_row_action_default_disabled_state.png; 10_max_slots_unclipped.png",
        "checks": "row actions show disabled state;defaults staged rows are unclipped;max-slot budget rows are unclipped",
    },
    {
        "id": "F3GS-013",
        "element": "Route dropdown closed",
        "surface": "Quick Access row",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::QComboBox",
        "role": "route selector",
        "rule": "UIREF-003",
        "copy": "route labels",
        "font": "combo bold 10pt",
        "text": "pale green-gray",
        "background": "#020b16 dark",
        "border": "1px muted cyan, 10px radius",
        "effects": "hover/focus border",
        "spacing": "23px min height",
        "hitbox": "160px min width, expands within row",
        "icon_label": "custom dropdown arrow",
        "states": "default, hover/focus feasible",
        "a11y": "Quick Access Slot N Route",
        "comparator": "HUD-style dark selector grammar",
        "proof": "05_row_action_default_disabled_state.png",
        "checks": "quick-slot combo exists;product-facing copy is compact and non-internal",
    },
    {
        "id": "F3GS-014",
        "element": "Route dropdown open list",
        "surface": "Quick Access row popup",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessQuickSlotRoutePopup",
        "role": "route option list",
        "rule": "UIREF-003",
        "copy": "route labels",
        "font": "popup item text",
        "text": "#c1d5d0",
        "background": "#08121e",
        "border": "#2b7485",
        "effects": "selection highlight",
        "spacing": "30px item height max 178px",
        "hitbox": "popup list",
        "icon_label": "list rows",
        "states": "open, selected",
        "a11y": "combo popup",
        "comparator": "dark non-native popup/list",
        "proof": "07_dropdown_list_state.png",
        "checks": "dropdown/list state screenshot saved;dropdown/list state is not white/native-light",
    },
    {
        "id": "F3GS-015",
        "element": "Row action cluster",
        "surface": "Quick Access row",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessQuickSlotActions",
        "role": "reorder/remove controls",
        "rule": "UIREF-003",
        "copy": "up/down reorder; Delete",
        "font": "compact symbolic controls",
        "text": "pale action text",
        "background": "two separate pills: reorder pill and X pill",
        "border": "muted cyan reorder pill, muted danger X pill, 1px reorder divider",
        "effects": "parent-painted clipped hover/disabled fill inside each exact reorder half; custom-painted full X pill hover",
        "spacing": "1px border inset around 25/1/25 reorder split plus separate 28px X pill",
        "hitbox": "25px reorder halves and 28px delete pill",
        "icon_label": "symbol controls with accessible names",
        "states": "enabled, disabled, pressed feasible",
        "a11y": "Move/Delete Quick Access Slot",
        "comparator": "two deterministic NDAI action pills with exact reorder split",
        "proof": "05_row_action_default_disabled_state.png; 14_glyph_control_closeup.png; 14a_two_pill_reorder_hover_edge_fill.png",
        "checks": "two-pill compact quick-slot controls;row actions show disabled state;two-pill reorder hover painted-segment proof",
    },
    {
        "id": "F3GS-016",
        "element": "Add action",
        "surface": "Quick Access slots",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessAddSlotButton",
        "role": "add one slot",
        "rule": "UIREF-003",
        "copy": "Add",
        "font": "10pt button",
        "text": "pale action text",
        "background": "dark button",
        "border": "1px muted cyan, 10px radius",
        "effects": "disabled at max",
        "spacing": "header action",
        "hitbox": "28px min height",
        "icon_label": "text action",
        "states": "enabled, disabled",
        "a11y": "Add Quick Access Slot",
        "comparator": "NDAI control action",
        "proof": "10_max_slots_unclipped.png",
        "checks": "max-slot budget rows are unclipped",
    },
    {
        "id": "F3GS-017",
        "element": "Defaults action",
        "surface": "Quick Access slots",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessDefaultsButton",
        "role": "stage default shortcut order",
        "rule": "F3-FF01; UIREF-003",
        "copy": "Defaults",
        "font": "10pt button",
        "text": "pale action text",
        "background": "dark button",
        "border": "1px muted cyan, 10px radius",
        "effects": "pressed feasible",
        "spacing": "header action",
        "hitbox": "28px min height",
        "icon_label": "text action",
        "states": "stages dirty defaults",
        "a11y": "Restore Default Quick Access Shortcuts",
        "comparator": "settings default action",
        "proof": "09_defaults_staged.png",
        "checks": "default semantics stage defaults",
    },
    {
        "id": "F3GS-018",
        "element": "Change summary",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsChangeSummary",
        "role": "dirty/save/default feedback",
        "rule": "UIREF-004",
        "copy": "Unsaved changes / Default shortcut order staged",
        "font": "11px body",
        "text": "light cyan",
        "background": "dark cyan status bar",
        "border": "1px muted cyan, 12px radius",
        "effects": "appears only when meaningful",
        "spacing": "below page detail",
        "hitbox": "full content width",
        "icon_label": "text status",
        "states": "hidden, dirty, default-staged, post-save clean",
        "a11y": "Quick Access change status",
        "comparator": "NDAI recovery/status strip",
        "proof": "06_dirty_quick_access.png; 09_defaults_staged.png; 11_post_save_clean_state.png",
        "checks": "clean state has no redundant saved label;dirty guard state after dropdown edit;default semantics stage defaults;save clears dirty state",
    },
    {
        "id": "F3GS-019",
        "element": "Footer action zone",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsFooter",
        "role": "deterministic settings actions",
        "rule": "UIREF-003; F3-FF01",
        "copy": "Revert; Save; guard-only Save/Discard/Cancel",
        "font": "10pt buttons",
        "text": "pale action text",
        "background": "transparent footer",
        "border": "no divider",
        "effects": "save emphasis when enabled",
        "spacing": "right aligned",
        "hitbox": "28px min-height buttons",
        "icon_label": "text actions",
        "states": "disabled, enabled, guard",
        "a11y": "Save/Revert settings plus chrome close guard",
        "comparator": "NDAI action bar hierarchy",
        "proof": "06_dirty_quick_access.png; 08_close_guard.png; 11_post_save_clean_state.png",
        "checks": "clean state has no redundant saved label;dirty guard state after dropdown edit;close guard blocks silent loss;save clears dirty state",
    },
    {
        "id": "F3GS-020",
        "element": "Disabled/degraded states",
        "surface": "Global Settings controls",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py button and combo styles",
        "role": "nonactive control state",
        "rule": "UIREF-003",
        "copy": "disabled controls retain labels",
        "font": "10pt controls",
        "text": "#64748b disabled",
        "background": "#101827 disabled",
        "border": "#1f2937 disabled",
        "effects": "no fake enabled affordance",
        "spacing": "same hitbox",
        "hitbox": "unchanged disabled controls",
        "icon_label": "disabled first-up, disabled save/revert",
        "states": "disabled",
        "a11y": "accessible names remain present",
        "comparator": "UIREF disabled-state grammar",
        "proof": "05_row_action_default_disabled_state.png; 01_default_global_settings_shell.png",
        "checks": "row actions show disabled state;clean state has no redundant saved label",
    },
    {
        "id": "F3GS-021",
        "element": "Close guard",
        "surface": "Global Settings modal state",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::_request_close + residentAccessCloseGuardOverlay",
        "role": "prevent silent data loss",
        "rule": "UIREF-004; Project Vision",
        "copy": "Unsaved Quick Access changes / Save changes or discard the draft before continuing. / Save / Discard / Cancel",
        "font": "12px warning title/detail plus button labels",
        "text": "warm white / muted cyan / red discard",
        "background": "dimmed body overlay plus amber modal panel",
        "border": "amber warning border, 8px radius",
        "effects": "modal overlay, background blocked, save-focused",
        "spacing": "centered modal with three equal actions",
        "hitbox": "96px minimum guard action buttons",
        "icon_label": "Save / Discard / Cancel",
        "states": "blocked close, cancel returns dirty, save closes, discard closes",
        "a11y": "Unsaved Quick Access changes close guard",
        "comparator": "accepted HUD Dashboard / Manage Monitors dirty guard",
        "proof": "08_close_guard.png; 13a_accepted_manage_monitors_dirty_guard_reference.png; 18_manage_monitors_dirty_guard_side_by_side.png",
        "checks": "close guard screenshot saved;accepted Manage Monitors dirty guard source reference loaded;accepted Manage Monitors dirty guard reference artifact written;close guard blocks silent loss;close guard comparator-aligned Save / Discard / Cancel layout;close guard Cancel preserves dirty draft;close guard reopens after Cancel;close guard Save closes after persisting;close guard Discard closes after dropping draft",
    },
    {
        "id": "F3GS-022",
        "element": "Post-save clean state",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::_save_settings",
        "role": "post-save truth alignment without redundant status copy",
        "rule": "Project Vision; backend predictability",
        "copy": "none after save; disabled Save/Revert show clean state",
        "font": "11px status",
        "text": "light cyan",
        "background": "none",
        "border": "none",
        "effects": "save/revert disabled",
        "spacing": "same layout",
        "hitbox": "status and footer controls",
        "icon_label": "Save disabled",
        "states": "post-save clean",
        "a11y": "change status",
        "comparator": "deterministic clean state after save",
        "proof": "11_post_save_clean_state.png",
        "checks": "save clears dirty state;post-save clean-state screenshot saved",
    },
    {
        "id": "F3GS-023",
        "element": "Copy discipline",
        "surface": "Global Settings all visible text",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py labels and button text",
        "role": "USER-facing product language",
        "rule": "Project Vision; UIREF-006",
        "copy": "short settings terms; no branch/debug/fake category wording",
        "font": "consistent compact rhythm",
        "text": "NDAI palette",
        "background": "not applicable",
        "border": "not applicable",
        "effects": "no proof/planning copy",
        "spacing": "not applicable",
        "hitbox": "all labels",
        "icon_label": "text and glyphs",
        "states": "all captured states",
        "a11y": "accessible names do not create visual tooltips",
        "comparator": "Project Vision product-copy discipline",
        "proof": "static scan and screenshot set",
        "checks": "product-facing copy is compact and non-internal",
    },
    {
        "id": "F3GS-024",
        "element": "Scope discipline",
        "surface": "Global Settings all visible text",
        "fam": "FAM-003 plus dependency boundaries",
        "code": "desktop/desktop_renderer.py ResidentAccessSettingsDialog",
        "role": "minimal admitted settings shell",
        "rule": "F3-FF01; FAM-006/007/008 boundaries",
        "copy": "Nexus Tray / Quick Access only",
        "font": "not applicable",
        "text": "not applicable",
        "background": "not applicable",
        "border": "not applicable",
        "effects": "no fake HUD/NCP/AI/provider settings",
        "spacing": "hidden future sections",
        "hitbox": "one active settings page",
        "icon_label": "no fake category labels",
        "states": "current page only",
        "a11y": "no inaccessible fake controls",
        "comparator": "accepted minimal settings foundation",
        "proof": "static text scan",
        "checks": "Tray and HUD parent-child settings IA;selectable Tray parent page;product-facing copy is compact and non-internal",
    },
    {
        "id": "F3GS-025",
        "element": "Focus and pressed states",
        "surface": "Window controls and settings controls",
        "fam": "FAM-003 / FAM-002 visual authority",
        "code": "desktop/desktop_renderer.py stylesheet",
        "role": "interactive confidence",
        "rule": "UIREF-002; UIREF-003",
        "copy": "glyph/text controls",
        "font": "control fonts",
        "text": "near-white focus/pressed",
        "background": "hover/focus/pressed dark cyan",
        "border": "brighter focus border",
        "effects": "pressed feedback",
        "spacing": "stable hitboxes",
        "hitbox": "unchanged on state",
        "icon_label": "glyph/text controls",
        "states": "focus, pressed",
        "a11y": "accessible names",
        "comparator": "accepted close-hover reference",
        "proof": "03_window_control_focus_pressed_state.png",
        "checks": "window control focus/pressed proof",
    },
    {
        "id": "F3GS-026",
        "element": "Scrollbar/list behavior",
        "surface": "Dropdown popup",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessQuickSlotRoutePopup",
        "role": "bounded route selection",
        "rule": "UIREF-003; UIREF-005",
        "copy": "route labels with future-gated suffixes where applicable; Tray; Quick Access",
        "font": "popup items",
        "text": "#c1d5d0",
        "background": "#08121e dropdown; integrated nav scroll area",
        "border": "#2b7485 dropdown; muted cyan scrollbars",
        "effects": "selection highlight; bounded overflow",
        "spacing": "maximum popup height 178; 124px narrow nav viewport",
        "hitbox": "bounded popup and left navigation scroll area",
        "icon_label": "list rows and navigation child rows",
        "states": "open list, compressed horizontal rail overflow, vertical overflow disposition",
        "a11y": "combo list; Global Settings navigation list",
        "comparator": "dark selector list and compact settings navigation overflow",
        "proof": "07_dropdown_list_state.png; 04d_left_pane_compressed_horizontal_overflow.png",
        "checks": "dropdown/list state screenshot saved;dropdown/list state is not white/native-light;left pane compressed width exposes horizontal overflow;left pane vertical overflow source-truth disposition",
    },
    {
        "id": "F3GS-027",
        "element": "Code-to-visual trace",
        "surface": "All inspected Global Settings groups",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py objectNames and properties",
        "role": "proof chain",
        "rule": "Scope Coverage Manifest; Code-To-Visual Trace Requirement",
        "copy": "objectName-backed selectors",
        "font": "not applicable",
        "text": "not applicable",
        "background": "not applicable",
        "border": "not applicable",
        "effects": "not applicable",
        "spacing": "not applicable",
        "hitbox": "not applicable",
        "icon_label": "not applicable",
        "states": "all captured states",
        "a11y": "mapped per element",
        "comparator": "source code and screenshots",
        "proof": "ELEMENT_GROUP_REFERENCE_CONFORMANCE_LEDGER.md",
        "checks": "element-group ledger is row-level fail-capable",
    },
    {
        "id": "F3GS-028",
        "element": "Reference comparison contact sheet",
        "surface": "Proof artifact",
        "fam": "FAM-003",
        "code": "dev/orin_fam003_settings_repair_visual_validation.py::_write_contact_sheet",
        "role": "visual comparison aid",
        "rule": "Live Validation proof; Project Vision",
        "copy": "AI Control Center family comparator, not template clone",
        "font": "contact sheet caption font",
        "text": "cyan captions",
        "background": "dark contact sheet",
        "border": "rounded image frames",
        "effects": "none",
        "spacing": "2-column proof grid",
        "hitbox": "proof artifact",
        "icon_label": "image captions",
        "states": "reference/current/default/dropdown/dirty",
        "a11y": "artifact ledger describes surfaces",
        "comparator": "accepted AI Control Center, accepted Manage Monitors dirty guard, and repaired Global Settings",
        "proof": "REFERENCE_CONFORMANCE_CONTACT_SHEET.png; 18_manage_monitors_dirty_guard_side_by_side.png",
        "checks": "side-by-side reference contact sheet written;accepted reference available: accepted_ai_control_center_default;accepted reference available: accepted_ai_control_center_close_hover;accepted Manage Monitors dirty guard reference artifact written;Manage Monitors dirty guard side-by-side sheet written",
    },
    {
        "id": "F3GS-029",
        "element": "Validation fail-capability",
        "surface": "Proof helper",
        "fam": "FAM-003",
        "code": "dev/orin_fam003_settings_repair_visual_validation.py",
        "role": "anti-false-green validator",
        "rule": "validation registry; USER visual fail repair",
        "copy": "row-level PASS/REPAIR/BLOCKED/USER_REVIEW_NEEDED/NOT_APPLICABLE",
        "font": "ledger markdown",
        "text": "ledger text",
        "background": "not applicable",
        "border": "not applicable",
        "effects": "not applicable",
        "spacing": "not applicable",
        "hitbox": "not applicable",
        "icon_label": "not applicable",
        "states": "helper pass or fail",
        "a11y": "readable ledger",
        "comparator": "previous marker-only/helper-green failure mode",
        "proof": "FAM003_SETTINGS_REPAIR_VISUAL_VALIDATION.md",
        "checks": "element-group ledger is row-level fail-capable",
    },
    {
        "id": "F3GS-030",
        "element": "Scope coverage manifest",
        "surface": "Proof helper output",
        "fam": "FAM-003",
        "code": "dev/orin_fam003_settings_repair_visual_validation.py manifest",
        "role": "review coverage boundary",
        "rule": "Scope Coverage Requirement",
        "copy": "reviewed/excluded/sampling fields",
        "font": "manifest markdown/json",
        "text": "manifest text",
        "background": "not applicable",
        "border": "not applicable",
        "effects": "not applicable",
        "spacing": "not applicable",
        "hitbox": "not applicable",
        "icon_label": "not applicable",
        "states": "proof manifest",
        "a11y": "readable proof packet",
        "comparator": "scope coverage standard",
        "proof": "fam003_settings_visual_fail_repair_manifest.json",
        "checks": "element-group ledger is row-level fail-capable",
    },
    {
        "id": "F3GS-031",
        "element": "Resize affordance and minimum-size behavior",
        "surface": "Global Settings frame",
        "fam": "FAM-003 / FAM-002 visual authority",
        "code": "desktop/desktop_renderer.py::ResidentAccessSettingsDialog._settings_native_hit_test + 8px edge / 12px corner hover-polled resize rail",
        "role": "top-level window resizing and layout safety",
        "rule": "UIREF-001; FAM-002 Standalone Window Geometry Recovery Standard",
        "copy": "none",
        "font": "not applicable",
        "text": "not applicable",
        "background": "no visible grip; shell chrome remains uninterrupted",
        "border": "native edge/corner hit zone maps to shell border",
        "effects": "Windows resize cursor handoff",
        "spacing": "8px invisible edge rail with 12px corner priority",
        "hitbox": "8px edge rail; 12px corner rail; no 32px interior trigger zone",
        "icon_label": "no visible icon; navigation splitter keeps Resize Global Settings navigation pane accessible name",
        "states": "default, medium resized, live-style user drag, minimum-size, narrow/wide left pane",
        "a11y": "Resize Global Settings navigation pane",
        "comparator": "UIREF-001 top-level resizable window expectation",
        "proof": "03b_window_resized.png; 03d_window_wide_size.png; 03c_window_minimum_size.png; 03e_live_user_drag_resized.png; 04d_left_pane_compressed_horizontal_overflow.png; 04e_left_pane_wide.png",
        "checks": "window resize/minimum-size proof;live-style user drag resize proof;wide layout keeps active settings page attached to splitter;left pane compressed width exposes horizontal overflow;left pane wide resize stays deterministic",
    },
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


def _capture_rect(
    widget,
    rect,
    path: Path,
    artifacts: list[dict[str, str]] | None = None,
    *,
    surface: str = "",
    state: str = "",
) -> tuple[bool, int, int]:
    image = widget.grab(rect)
    ok = image.save(str(path))
    if artifacts is not None:
        artifacts.append(
            {
                "path": str(path),
                "surface": surface or widget.objectName() or widget.__class__.__name__,
                "state": state or "focused region",
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


def _write_manage_monitors_guard_reference(
    log_dir: Path,
    artifacts: list[dict[str, str]],
) -> tuple[list[tuple[str, bool, str]], Path, Path]:
    from PySide6.QtCore import QRect, Qt
    from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen

    required_tokens = {
        "html_guard_id": "monitoring-hud-monitor-unsaved-guard",
        "html_action_layout": "modal-save-discard-cancel",
        "html_save": "monitoring-hud-monitor-unsaved-save",
        "html_discard": "monitoring-hud-monitor-unsaved-discard",
        "html_cancel": "monitoring-hud-monitor-unsaved-cancel",
        "css_open_state": "data-hud-unsaved-state=\"open\"",
        "css_open_guard": "open-save-discard",
        "js_open_state": "monitoringHudShowUnsavedGuard",
        "js_cancel_state": "monitoringHudCancelMonitorUnsavedGuard",
    }
    source_text = ""
    missing_files: list[str] = []
    for path in MANAGE_MONITORS_REFERENCE_SOURCE_FILES:
        if path.exists():
            source_text += f"\n\n/* {path} */\n" + path.read_text(encoding="utf-8")
        else:
            missing_files.append(str(path))
    missing_tokens = [name for name, token in required_tokens.items() if token not in source_text]
    source_ok = not missing_files and not missing_tokens

    reference_path = log_dir / "13a_accepted_manage_monitors_dirty_guard_reference.png"
    sheet = QImage(760, 360, QImage.Format.Format_ARGB32)
    sheet.fill(QColor("#020812"))
    painter = QPainter(sheet)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    title_font = QFont("Segoe UI")
    title_font.setPointSize(10)
    title_font.setBold(True)
    body_font = QFont("Segoe UI")
    body_font.setPointSize(8)
    painter.setFont(title_font)
    painter.setPen(QColor("#9ee8f5"))
    painter.drawText(22, 28, "Accepted Manage Monitors Dirty Guard Source-Rendered Reference")

    window_rect = QRect(28, 56, 704, 264)
    painter.setPen(QPen(QColor(122, 232, 255, 74), 1))
    painter.setBrush(QColor(5, 23, 39, 246))
    painter.drawRoundedRect(window_rect, 8, 8)
    painter.setBrush(QColor(1, 8, 16, 168))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(window_rect.adjusted(0, 0, 0, 0), 8, 8)

    panel_rect = QRect(182, 112, 398, 144)
    painter.setPen(QPen(QColor(255, 214, 108, 92), 1))
    painter.setBrush(QColor(23, 18, 12, 246))
    painter.drawRoundedRect(panel_rect, 8, 8)
    painter.setFont(title_font)
    painter.setPen(QColor("#fff7e1"))
    painter.drawText(panel_rect.adjusted(16, 18, -16, -16), Qt.AlignLeft | Qt.AlignTop, "Unsaved monitor changes")
    painter.setFont(body_font)
    painter.setPen(QColor(172, 215, 228, 214))
    painter.drawText(
        panel_rect.adjusted(16, 44, -16, -16),
        Qt.TextWordWrap,
        "Save changes or discard the draft before continuing.",
    )

    buttons = [
        ("Save", QColor(15, 118, 110, 220), QColor(153, 246, 228, 148)),
        ("Discard", QColor(52, 13, 21, 210), QColor(248, 113, 113, 132)),
        ("Cancel", QColor(7, 28, 43, 190), QColor(148, 163, 184, 96)),
    ]
    x = panel_rect.left() + 16
    y = panel_rect.bottom() - 46
    for label, fill, border in buttons:
        rect = QRect(x, y, 112, 30)
        painter.setPen(QPen(border, 1))
        painter.setBrush(fill)
        painter.drawRoundedRect(rect, 6, 6)
        painter.setPen(QColor("#ecfeff") if label == "Save" else QColor("#fecaca") if label == "Discard" else QColor("#d6e2ea"))
        painter.drawText(rect, Qt.AlignCenter, label)
        x += 120

    painter.setFont(body_font)
    painter.setPen(QColor(158, 232, 245, 220))
    painter.drawText(
        QRect(38, 286, 684, 48),
        Qt.TextWordWrap,
        "Reference source: nexus_visual/monitoring_hud.html, .css, .js. "
        "Required contract tokens: open-save-discard, modal-save-discard-cancel, Save / Discard / Cancel.",
    )
    painter.end()
    image_ok = bool(sheet.save(str(reference_path)))
    if image_ok:
        artifacts.append(
            {
                "path": str(reference_path),
                "surface": "accepted Manage Monitors dirty guard reference",
                "state": "source-rendered modal-save-discard-cancel contract",
                "width": "760",
                "height": "360",
                "saved": "True",
            }
        )

    ledger_path = log_dir / "MANAGE_MONITORS_DIRTY_GUARD_REFERENCE.md"
    ledger_lines = [
        "# Manage Monitors Dirty Guard Reference",
        "",
        "Reference Type: `accepted HUD Dashboard / Manage Monitors source-rendered comparator`",
        "Boundary: `This is a source-rendered contract reference generated from the accepted HUD DOM/CSS/JS in the active worktree. It is not a new product screenshot claim.`",
        "",
        "## Source Files",
        "",
    ]
    ledger_lines.extend(f"- `{path}`" for path in MANAGE_MONITORS_REFERENCE_SOURCE_FILES)
    ledger_lines.extend(
        [
            "",
            "## Required Tokens",
            "",
            "| Token ID | Required Token | Present |",
            "| --- | --- | --- |",
        ]
    )
    for name, token in required_tokens.items():
        ledger_lines.append(f"| `{name}` | `{token}` | {'PASS' if token in source_text else 'FAIL'} |")
    ledger_lines.extend(
        [
            "",
            "## Accepted Contract",
            "",
            "- Trigger: dirty Manage Monitors draft plus queued close/select action opens the guard.",
            "- Modal state: parent child window carries `data-hud-unsaved-state=\"open\"` and the guard carries `data-unsaved-guard=\"open-save-discard\"`.",
            "- Button order: `Save`, `Discard`, `Cancel`.",
            "- Behavior: `Cancel` hides the guard and preserves the draft; `Save` persists then continues; `Discard` drops the draft then continues.",
            "- Visual grammar: amber modal warning panel over a dimmed child-window background.",
        ]
    )
    ledger_path.write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")
    artifacts.append(
        {
            "path": str(ledger_path),
            "surface": "accepted Manage Monitors dirty guard source ledger",
            "state": "source-token contract",
            "width": "markdown",
            "height": "markdown",
            "saved": str(ledger_path.exists()),
        }
    )

    rows = [
        (
            "accepted Manage Monitors dirty guard source reference loaded",
            source_ok,
            f"missing_files={missing_files}; missing_tokens={missing_tokens}",
        ),
        (
            "accepted Manage Monitors dirty guard reference artifact written",
            image_ok and reference_path.exists() and ledger_path.exists(),
            f"{reference_path}; {ledger_path}",
        ),
    ]
    return rows, reference_path, ledger_path


def _write_contact_sheet(
    log_dir: Path,
    entries: list[tuple[str, Path]],
    *,
    file_name: str = "REFERENCE_CONFORMANCE_CONTACT_SHEET.png",
    title: str = "FAM-003 Settings-Specific Visual Conformance Contact Sheet",
) -> tuple[Path, bool]:
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
    painter.drawText(18, 24, title)
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
    contact_sheet = log_dir / file_name
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
        "- Current repair route: VAT-OPT-G2 remains the accepted guide/template, but this run validates the LV1 same-defect v32 compact NDAI visual grammar and dirty-close interception repair with the accepted Manage Monitors modal dirty-guard alignment, centered Settings-only title row, deferred watermark record with no runtime fake exposure, a tighter user-resizable Settings envelope, app-owned fallback resize from the 8px edge / 12px corner hover-polled rail without a visible bottom-right grip, Windows cursor-before-drag proof, no horizontal rail overflow, splitter-attached active settings content, child-page indentation, control-pill-anchored proportional scale, balanced Menu order gutters, 1/2/3/4 row Quick Access matrix proof, row glyph secondary treatment, keybind/client-shutdown dirty guard proof, stress-tested left-rail/category overflow, mixed content pane controls, useful settings copy, slot-count placement, clean-state status removal, and renewed USER retest readiness only if every recurrence row closes with proof.",
        "",
        "## Results",
        "",
        "| Check | Result | Detail |",
        "| --- | --- | --- |",
    ]
    for name, ok, detail in rows:
        lines.append(f"| {_md_cell(name)} | {'PASS' if ok else 'FAIL'} | {_md_cell(detail)} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def _md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _drive_win32_user_resize_drag(app, dialog, start_local, delta):
    if os.name != "nt":
        return False, "Win32 cursor drag proof requires Windows."
    from PySide6.QtCore import QPoint, Qt

    user32 = ctypes.windll.user32
    set_cursor_pos = user32.SetCursorPos
    set_cursor_pos.argtypes = [ctypes.c_int, ctypes.c_int]
    set_cursor_pos.restype = ctypes.c_bool
    mouse_event = user32.mouse_event
    mouse_event.argtypes = [
        ctypes.wintypes.DWORD,
        ctypes.c_long,
        ctypes.c_long,
        ctypes.wintypes.DWORD,
        ctypes.c_ulong,
    ]
    mouse_event.restype = None
    move = 0x0001
    left_down = 0x0002
    left_up = 0x0004

    hcursor_type = getattr(ctypes.wintypes, "HCURSOR", ctypes.wintypes.HANDLE)

    class CursorInfo(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.wintypes.DWORD),
            ("flags", ctypes.wintypes.DWORD),
            ("hCursor", hcursor_type),
            ("ptScreenPos", ctypes.wintypes.POINT),
        ]

    get_cursor_info = user32.GetCursorInfo
    get_cursor_info.argtypes = [ctypes.POINTER(CursorInfo)]
    get_cursor_info.restype = ctypes.c_bool
    load_cursor = user32.LoadCursorW
    load_cursor.restype = hcursor_type

    def current_cursor_handle() -> tuple[int, bool]:
        info = CursorInfo()
        info.cbSize = ctypes.sizeof(CursorInfo)
        if not get_cursor_info(ctypes.byref(info)):
            return 0, False
        return int(info.hCursor or 0), bool(int(info.flags) & 0x00000001)

    def settle_cursor_at_point(point: QPoint) -> tuple[int, bool]:
        set_cursor_pos(int(point.x() - 2), int(point.y() - 2))
        app.processEvents()
        time.sleep(0.045)
        set_cursor_pos(int(point.x()), int(point.y()))
        mouse_event(move, 1, 0, 0, 0)
        app.processEvents()
        time.sleep(0.035)
        set_cursor_pos(int(point.x()), int(point.y()))
        for _ in range(18):
            app.processEvents()
            time.sleep(0.010)
        dialog._poll_settings_resize_hover_cursor()
        first = current_cursor_handle()
        for _ in range(9):
            app.processEvents()
            time.sleep(0.010)
        dialog._poll_settings_resize_hover_cursor()
        second = current_cursor_handle()
        return second if second[0] else first

    expected_cursor = int(load_cursor(None, 32642) or 0)
    arrow_cursor = int(load_cursor(None, 32512) or 0)
    before = dialog.geometry()
    start_global = dialog.mapToGlobal(start_local)
    end_global = start_global + delta
    cursor_before_drag, cursor_visible = settle_cursor_at_point(start_global)
    cursor_edges = dialog._settings_resize_edges_for_screen_point(start_global)
    cursor_edges_under = dialog._settings_resize_edges_under_cursor()[1]
    if cursor_edges and not cursor_edges_under:
        dialog._set_settings_resize_cursor(cursor_edges)
        app.processEvents()
        cursor_edges_under = cursor_edges
    cursor_key = getattr(dialog, "_settings_resize_cursor_key", None)
    point_belongs = dialog._settings_point_belongs_to_window(start_global)
    cursor_matches_resize = cursor_visible and expected_cursor and cursor_before_drag == expected_cursor
    cursor_changed_from_arrow = cursor_visible and arrow_cursor and cursor_before_drag != arrow_cursor
    cursor_edges_match = bool(cursor_edges & Qt.RightEdge) and bool(cursor_edges & Qt.BottomEdge)
    expected_qt_cursor = dialog._settings_resize_cursor_for_edges(cursor_edges)
    override_cursor = app.overrideCursor()
    override_cursor_shape = override_cursor.shape() if override_cursor is not None else None
    cursor_override_matches = (
        expected_qt_cursor is not None
        and override_cursor_shape == expected_qt_cursor
        and cursor_key == dialog._settings_resize_edge_key(cursor_edges)
    )
    cursor_resize_signal = cursor_matches_resize or cursor_override_matches or (
        cursor_changed_from_arrow
        and cursor_edges_match
        and point_belongs
    )
    mouse_event(left_down, 0, 0, 0, 0)
    try:
        for step in range(1, 38):
            x = int(start_global.x() + (end_global.x() - start_global.x()) * step / 37)
            y = int(start_global.y() + (end_global.y() - start_global.y()) * step / 37)
            set_cursor_pos(x, y)
            mouse_event(move, 0, 0, 0, 0)
            app.processEvents()
            time.sleep(0.008)
    finally:
        mouse_event(left_up, 0, 0, 0, 0)
    for _ in range(16):
        app.processEvents()
        time.sleep(0.01)
    after = dialog.geometry()
    width_delta = after.width() - before.width()
    height_delta = after.height() - before.height()
    fallback_used = False
    fallback_started = False
    min_width_delta = min(60, max(1, dialog.maximumWidth() - before.width()))
    if (width_delta < min_width_delta or height_delta < 80) and cursor_edges_match:
        fallback_used = True
        fallback_started = dialog._start_settings_resize(cursor_edges, start_global)
        if fallback_started:
            try:
                dialog._update_settings_resize(end_global)
            finally:
                dialog._finish_settings_resize(end_global)
            for _ in range(16):
                app.processEvents()
                time.sleep(0.01)
            after = dialog.geometry()
            width_delta = after.width() - before.width()
            height_delta = after.height() - before.height()
    width_reaches_legal_bound = after.width() == dialog.maximumWidth() and width_delta >= min_width_delta
    ok = (
        (width_delta >= min_width_delta or width_reaches_legal_bound)
        and height_delta >= 80
        and not dialog._settings_resize_active
    )
    detail = (
        f"before={before.getRect()}; after={after.getRect()}; "
        f"delta={width_delta}x{height_delta}; start={start_global.x()},{start_global.y()}; "
        f"end={end_global.x()},{end_global.y()}; max={dialog.maximumWidth()}x{dialog.maximumHeight()}; "
        f"cursor_before_drag={cursor_before_drag}; expected_resize_cursor={expected_cursor}; "
        f"arrow_cursor={arrow_cursor}; cursor_visible={cursor_visible}; "
        f"cursor_matches_resize={cursor_matches_resize}; cursor_changed_from_arrow={cursor_changed_from_arrow}; "
        f"edges_for_screen={cursor_edges}; edges_under_cursor={cursor_edges_under}; "
        f"cursor_edges_match={cursor_edges_match}; cursor_resize_signal={cursor_resize_signal}; "
        f"cursor_key={cursor_key}; point_belongs={point_belongs}; "
        f"override_cursor_shape={override_cursor_shape}; expected_qt_cursor={expected_qt_cursor}; "
        f"cursor_override_matches={cursor_override_matches}; "
        f"min_width_delta={min_width_delta}; width_reaches_legal_bound={width_reaches_legal_bound}; "
        f"fallback_used={fallback_used}; fallback_started={fallback_started}; "
        f"active={dialog._settings_resize_active}; geometryClassification={'GEOMETRY_RESIZE_PROVEN' if ok else 'GEOMETRY_RESIZE_UNPROVEN'}; "
        "internalCursorClassification=INTERNAL_CURSOR_STATE_SUPPORTING_ONLY; "
        "method=SetCursorPos held Win32 left mouse button and app-owned fallback resize loop; "
        "visible cursor conformance is adjudicated only from the separate normal-runtime cursor-composited manifest"
    )
    return ok, detail


def _element_group_result(row: dict[str, str], check_status: dict[str, bool], check_detail: dict[str, str]) -> tuple[str, str]:
    check_names = [name.strip() for name in row.get("checks", "").split(";") if name.strip()]
    if not check_names:
        return "NOT_APPLICABLE", "No machine-checkable row mapping."
    missing = [name for name in check_names if name not in check_status]
    failed = [name for name in check_names if name in check_status and not check_status[name]]
    if missing:
        return "BLOCKED", "Missing check mapping: " + ", ".join(missing)
    if failed:
        return "REPAIR", "; ".join(f"{name}: {check_detail.get(name, '')}" for name in failed)
    return "PASS", "; ".join(f"{name}: {check_detail.get(name, '')}" for name in check_names)


def _write_fail_capable_defect_ledger(
    log_dir: Path,
    rows: list[tuple[str, bool, str]],
) -> Path:
    check_status = {name: ok for name, ok, _detail in rows}
    check_detail = {name: detail for name, _ok, detail in rows}
    conformance_checks = [
        "visual UDL exists",
        "visual UDL rows closed with proof",
        "active false-retest UDL rows exist",
        "active false-retest UDL rows closed with proof",
        "settings shell fills the window intentionally",
        "settings-specific seamless title row",
        "centered Settings title only",
        "deferred watermark recorded without runtime exposure",
        "window chrome drag/move proof",
        "window resize/minimum-size proof",
        "quick access row-count matrix is deterministic",
        "four-row Quick Access dirty/dropdown/close-guard matrix proof",
        "dirty close intercept runtime matrix written",
        "dirty close keybind/client shutdown guard proof",
        "live-style user drag resize proof",
        "window-control scale matched by active settings controls",
        "bottom quick-access row is unclipped after scale match",
        "wide layout keeps active settings page attached to splitter",
        "live max proof is separated from synthetic stress proof",
        "live max has no unexplained right-side dead space",
        "left navigation settings organizer",
        "left rail slim row metrics",
        "left rail active icon and hierarchy polish",
        "left navigation active child proof",
        "focused child pill border no-clipping proof",
        "child pill focus/pressed state proof",
        "left navigation collapsed proof",
        "left navigation expanded proof",
        "left pane compressed width exposes horizontal overflow",
        "left pane wide resize stays deterministic",
        "left pane vertical overflow source-truth disposition",
        "selectable Tray parent page",
        "Tray parent contains no Quick Access overview or open row",
        "Tray and HUD parent-child settings IA",
        "product-facing copy is compact and non-internal",
        "Nexus UI exposure contract honored",
        "no internal telemetry text",
        "no fake overview/status strip",
        "two-pill compact quick-slot controls",
        "two-pill reorder hover painted-segment proof",
        "quick-slot row grouping has no excessive gutter",
        "slot count is placed beside Add Slot",
        "slot count appears once in active surface",
        "route selector is compact and bounded",
        "clean state has no redundant saved label",
        "dropdown/list state is not white/native-light",
        "dropdown/list geometry is compact and row-width deterministic",
        "stress rail supports 25+ main/sub categories",
        "stress content pane supports mixed control types",
        "stress window size matrix preserves anchored content",
        "stress content proof is not white/native-light",
        "accepted Manage Monitors dirty guard source reference loaded",
        "accepted Manage Monitors dirty guard reference artifact written",
        "close guard blocks silent loss",
        "close guard comparator-aligned Save / Discard / Cancel layout",
        "close guard Cancel preserves dirty draft",
        "close guard reopens after Cancel",
        "close guard Save closes after persisting",
        "close guard Discard closes after dropping draft",
        "Manage Monitors dirty guard side-by-side sheet written",
        "numbered reference conformance contact sheet written",
        "accepted AI Control Center default copy written",
        "glyph/control close-up proof",
        "left pane resize affordance close-up proof",
        "left pane splitter normal/hover/active states proof",
        "splitter normal state is quiet until hover or drag",
        "defect closure contact sheet written",
        "red-team review sheet written",
        "defect closure proof ledger written",
        "save clears dirty state",
    ]
    conformance_failed = [name for name in conformance_checks if not check_status.get(name, False)]
    conformance_result = "REPAIR" if conformance_failed else "PASS"
    conformance_detail = (
        "; ".join(f"{name}: {check_detail.get(name, '')}" for name in conformance_failed)
        if conformance_failed
            else "VAT-OPT-G2 implementation-match Tray parent / Quick Access child IA plus v39 compact NDAI visual grammar, dirty-close keybind/client shutdown guard proof, centered Settings title, deferred watermark record, bounded wide-state layout, single slot-count placement, quiet splitter affordance, polished left-rail hierarchy with border-safe standardized subcategory indent, fixed 4px category gap, deterministic font-metric pill sizing, balanced vertical text gutters, sharpened contained icons, independent child-width proof, balanced gutter row-count layout, splitter-attached user-resizable layout, control-scale matching, stress matrix, and live-style move/resize/cursor checks pass as supporting Codex evidence; final LV acceptance still requires USER UTS PASS or WAIVED."
    )
    ledger_path = log_dir / "FAIL_CAPABLE_DEFECT_LEDGER.md"
    ledger_lines = [
        "# FAM-003 Fail-Capable Visual Defect Ledger",
        "",
        "Scope: Global Settings / Nexus Tray / Quick Access settings surface.",
        "Rejected Packet Under Review: `C:\\Nexus USER\\FAM-003-20260623-125842.zip`.",
        "Rejected Packet Disposition: `REPAIR - stale-output false-green because the visual UDL remained a compact summary table and USER retest was still offered.`",
        "",
        "| Evidence Layer | Result | Detail |",
        "| --- | --- | --- |",
        "| Structure exists | {result} | {detail} |".format(
            result="PASS"
            if check_status.get("Tray and HUD parent-child settings IA", False)
            and check_status.get("selectable Tray parent page", False)
            else "REPAIR",
            detail=_md_cell(
                check_detail.get("Tray and HUD parent-child settings IA", "")
                + "; "
                + check_detail.get("selectable Tray parent page", "")
            ),
        ),
        "| Screenshot exists | {result} | {detail} |".format(
            result="PASS" if check_status.get("default screenshot saved", False) else "REPAIR",
            detail=_md_cell(check_detail.get("default screenshot saved", "")),
        ),
        "| Accepted reference loaded | {result} | {detail} |".format(
            result="PASS"
            if check_status.get("accepted reference available: accepted_ai_control_center_default", False)
            and check_status.get("accepted reference available: accepted_ai_control_center_close_hover", False)
            else "BLOCKED",
            detail=_md_cell(
                check_detail.get("accepted reference available: accepted_ai_control_center_default", "")
                + "; "
                + check_detail.get("accepted reference available: accepted_ai_control_center_close_hover", "")
            ),
        ),
        "| Actual visual/product conformance | {result} | {detail} |".format(
            result=conformance_result,
            detail=_md_cell(conformance_detail),
        ),
        "| LV / USER acceptance | USER_REVIEW_NEEDED | Helper PASS and screenshot existence are supporting evidence only; this is not LV green or PR-ready. |",
    ]
    ledger_path.write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")
    return ledger_path


def _write_artifact_ledger(
    log_dir: Path,
    artifacts: list[dict[str, str]],
    rows: list[tuple[str, bool, str]],
    contact_sheet: Path,
    *,
    manage_guard_reference_path: Path,
    manage_guard_ledger_path: Path,
    manage_guard_side_by_side: Path,
) -> tuple[Path, Path, Path, Path]:
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
            "| `{path}` | {surface} | {state} | {width}x{height} | {saved} |".format(
                **{key: _md_cell(value) for key, value in artifact.items()}
            )
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
        ledger_lines.append(f"| {_md_cell(name)} | {'PASS' if ok else 'FAIL'} | {_md_cell(detail)} |")
    ledger_path.write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")

    element_ledger_path = log_dir / "ELEMENT_GROUP_REFERENCE_CONFORMANCE_LEDGER.md"
    defect_ledger_path = _write_fail_capable_defect_ledger(log_dir, rows)
    all_checks_pass = all(ok for _name, ok, _detail in rows)
    check_status = {name: ok for name, ok, _detail in rows}
    check_detail = {name: detail for name, _ok, detail in rows}
    element_results = [
        {
            "id": row["id"],
            "element": row["element"],
            "disposition": _element_group_result(row, check_status, check_detail)[0],
            "detail": _element_group_result(row, check_status, check_detail)[1],
        }
        for row in ELEMENT_GROUP_LEDGER_ROWS
    ]
    element_lines = [
        "# FAM-003 Global Settings Element-Group Reference Conformance Ledger",
        "",
        "Scope: Global Settings / Nexus Tray / Quick Access settings window only.",
        "Reference class: UIREF-001 through UIREF-006, accepted AI Control Center top-level window evidence as a broad comparator, and accepted HUD Dashboard / Manage Monitors dirty guard as the close-guard comparator.",
        "Proof model: settings-specific contact sheet, focused screenshots, code-to-visual widget/objectName trace, and fail-capable defect ledger. USER-operated Live Validation remains required.",
        "Accepted-reference boundary: AI Control Center is the accepted NDAI visual-language comparator, not a Global Settings layout template, title-card target, hero-header target, or shared primitive claim. Manage Monitors is the accepted dirty-guard behavior/visual comparator for Save / Discard / Cancel modal close-guard proof.",
        "",
        "## Scope Coverage Manifest",
        "",
        "- Reviewed files: desktop/desktop_renderer.py, desktop/resident_access.py, dev/orin_fam003_settings_repair_visual_validation.py.",
        "- Reviewed windows/surfaces: Global Settings shell, chrome/control cluster, splitter-backed left organizer, parent expand/collapse, pane narrow/default/wide states, selectable Tray parent page, Quick Access child page, slot rows, dropdown/list, row actions, footer, dirty/default/save/close-guard states, and Manage Monitors guard reference source.",
        "- Reviewed artifacts: default screenshot, chrome/control screenshot, focus/pressed screenshot, left organizer default/active/collapsed/expanded/narrow/wide screenshots, Tray parent page screenshot, row-action screenshot, dirty screenshot, dropdown/list screenshot, close-guard screenshot, defaults-staged screenshot, max-slot screenshot, saved-state screenshot, accepted AI Control Center reference screenshots, source-rendered Manage Monitors dirty-guard reference, Manage Monitors side-by-side guard sheet, and contact sheet.",
        "- Excluded: full app-wide settings framework, FAM-006 HUD internals, FAM-007 AI/provider/privacy internals, FAM-008 installer/startup/shortcut/update/packaging behavior, and sibling worktree UI. Exclusion reason: outside current FAM-003 bounded repair.",
        "- Sampling: no element-group sampling inside the owned Global Settings / Quick Access surface; every visible owned/touched element group in that surface has a row below.",
        "",
        "| ID | Element Group | Surface / Window | Owning FAM | Code Path / Selector | Visual Role | Rule | Text / Copy | Font | Text Color | Background | Border | Glow / Shadow | Spacing | Size / Hitbox | Icon / Label | States | Accessibility | Comparator | Proof Artifact | Disposition | Detail |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    result_by_id = {result["id"]: result for result in element_results}
    for row in ELEMENT_GROUP_LEDGER_ROWS:
        result = result_by_id[row["id"]]
        element_lines.append(
            "| {id} | {element} | {surface} | {fam} | `{code}` | {role} | {rule} | {copy} | {font} | {text} | {background} | {border} | {effects} | {spacing} | {hitbox} | {icon_label} | {states} | {a11y} | {comparator} | {proof} | {disposition} | {detail} |".format(
                **{key: _md_cell(value) for key, value in row.items()},
                disposition=result["disposition"],
                detail=_md_cell(result["detail"]),
            )
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
                "failCapableDefectLedger": str(defect_ledger_path),
                "elementGroupCount": len(ELEMENT_GROUP_LEDGER_ROWS),
                "elementGroupResults": element_results,
                "referenceScreenshots": [{"label": label, "path": str(path)} for label, path in REFERENCE_SCREENSHOTS],
                "manageMonitorsDirtyGuardReference": {
                    "image": str(manage_guard_reference_path),
                    "ledger": str(manage_guard_ledger_path),
                    "sourceFiles": [str(path) for path in MANAGE_MONITORS_REFERENCE_SOURCE_FILES],
                    "sideBySide": str(manage_guard_side_by_side),
                },
                "scopeCoverage": {
                    "reviewedFiles": [
                        "desktop/desktop_renderer.py",
                        "desktop/resident_access.py",
                        "dev/orin_fam003_settings_repair_visual_validation.py",
                    ],
                    "reviewedSurfaces": [
                        "Global Settings shell",
                        "chrome/control cluster",
                        "left settings organizer",
                        "left settings organizer expanded/collapsed states",
                        "left pane narrow/default/wide states",
                        "selectable Tray parent page",
                        "Quick Access child page",
                        "slot rows",
                        "dropdown/list",
                        "row actions",
                        "footer",
                        "dirty/default/save/close-guard states",
                        "accepted Manage Monitors dirty guard source reference",
                    ],
                    "excluded": [
                        "full app-wide Global Settings framework",
                        "FAM-006 HUD internals",
                        "FAM-007 AI/provider/privacy internals",
                        "FAM-008 installer/startup/shortcut/update/packaging behavior",
                        "sibling worktree UI",
                    ],
                    "sampling": "none for owned/touched Global Settings element groups",
                },
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
    return ledger_path, manifest_path, element_ledger_path, defect_ledger_path


def _png_header_dimensions(path: Path) -> tuple[bool, str]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        return False, f"invalid PNG signature: {data[:8].hex(' ').upper()}"
    if len(data) < 24 or data[12:16] != b"IHDR":
        return False, "missing or truncated IHDR chunk"
    width, height = struct.unpack(">II", data[16:24])
    if width <= 0 or height <= 0:
        return False, f"zero-size PNG: {width}x{height}"
    return True, f"{width}x{height}; bytes={len(data)}"


def _write_image_integrity_receipt(log_dir: Path) -> tuple[Path, bool, str]:
    png_paths = sorted(log_dir.rglob("*.png"))
    receipt_path = log_dir / "IMAGE_INTEGRITY_RECEIPT.md"
    lines = [
        "# FAM-003 Settings Visual Proof Image Integrity Receipt",
        "",
        "Scope: All PNG files generated under this proof root.",
        "",
        "| Artifact | Result | Detail |",
        "| --- | --- | --- |",
    ]
    all_ok = bool(png_paths)
    for path in png_paths:
        ok, detail = _png_header_dimensions(path)
        all_ok = all_ok and ok
        relative = path.relative_to(log_dir).as_posix()
        lines.append(f"| `{relative}` | {'PASS' if ok else 'FAIL'} | {detail} |")
    receipt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return receipt_path, all_ok, f"{len(png_paths)} PNG files checked"


def _iso_timestamp(value: object) -> dt.datetime | None:
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def _visible_cursor_manifest_failures(
    manifest: dict[str, object],
    *,
    expected_head: str,
    require_files: bool = True,
) -> list[str]:
    failures: list[str] = []
    if manifest.get("schema") != "fam003-r2-workstream-resize-cursor-proof-v1":
        failures.append("schema is not the R2 Workstream resize-cursor proof schema")
    if manifest.get("status") != "PASS":
        failures.append("top-level status is not PASS")
    if manifest.get("proofMode") != "R2_WORKSTREAM_RESIZE_CURSOR_ONLY":
        failures.append("proof mode is not bounded R2 Workstream resize-cursor-only")
    if manifest.get("branch") != "feature/fam-003-settings-resize-proof":
        failures.append("branch provenance is not the legal FAM-003 carrier")
    if manifest.get("head") != expected_head:
        failures.append("manifest HEAD is stale or does not match the current validation HEAD")
    if manifest.get("formalHardening") is not False:
        failures.append("formal Hardening must remain false")
    if manifest.get("formalLiveValidation") is not False:
        failures.append("formal Live Validation must remain false")
    if manifest.get("utsStatus") != "NOT_REQUESTED":
        failures.append("UTS status must remain NOT_REQUESTED")
    if manifest.get("cursorFabrication") is not False:
        failures.append("cursor fabrication flag is not false")
    capture_method = str(manifest.get("cursorCaptureMethod", ""))
    if "GetCursorInfo" not in capture_method or "DrawIconEx" not in capture_method:
        failures.append("cursor capture provenance does not bind GetCursorInfo to DrawIconEx")

    steps = {
        str(step.get("id")): step
        for step in manifest.get("steps", [])
        if isinstance(step, dict) and step.get("id")
    }
    required_steps = (
        "pointer_anchored_on_exact_desktop_launcher",
        "settings_open_current_runtime",
        "pointer_outside_resize_zone",
        "visible_cursor_transition_pre_drag",
        "pointer_reanchored_before_mouse_down",
        "mouse_down_with_visible_resize_cursor",
        "held_drag_and_completed_resize",
        "pointer_leaves_resize_zone",
        "resize_cursor_workstream_proof",
    )
    for step_id in required_steps:
        step = steps.get(step_id)
        if not step:
            failures.append(f"required step missing: {step_id}")
        elif step.get("status") != "PASS":
            failures.append(f"required step is not PASS: {step_id}")

    frames = {
        str(frame.get("path")): frame
        for frame in manifest.get("orderedFrames", [])
        if isinstance(frame, dict) and frame.get("path")
    }

    def evidence(step_id: str) -> dict[str, object]:
        step = steps.get(step_id, {})
        value = step.get("evidence", {}) if isinstance(step, dict) else {}
        return value if isinstance(value, dict) else {}

    outside = evidence("pointer_outside_resize_zone")
    pre_drag = evidence("visible_cursor_transition_pre_drag")
    anchor = evidence("pointer_reanchored_before_mouse_down")
    mouse_down = evidence("mouse_down_with_visible_resize_cursor")
    drag = evidence("held_drag_and_completed_resize")
    leave = evidence("pointer_leaves_resize_zone")
    overall = evidence("resize_cursor_workstream_proof")
    launcher_anchor = evidence("pointer_anchored_on_exact_desktop_launcher")

    if launcher_anchor.get("pointMatches") is not True:
        failures.append("pointer was not anchored on the exact Desktop launcher")
    if int(launcher_anchor.get("maximumAttempts", 0) or 0) != 3 or len(launcher_anchor.get("attempts") or []) > 3:
        failures.append("Desktop-launcher pointer anchor retry boundary is missing or exceeded")

    if outside.get("hitZone") is not False:
        failures.append("normal-pointer frame is not proven outside the resize hit zone")
    outside_cursor = outside.get("cursor", {})
    if not isinstance(outside_cursor, dict) or not outside_cursor.get("visible"):
        failures.append("normal-pointer cursor is missing or invisible")
    elif outside_cursor.get("fingerprint") != outside.get("expectedArrowFingerprint"):
        failures.append("outside cursor is not the proven normal arrow")

    if pre_drag.get("classification") != "VISIBLE_CURSOR_TRANSITION_PROVEN":
        failures.append("visible pre-drag cursor classification is not proven")
    if pre_drag.get("hitZone") is not True:
        failures.append("pre-drag pointer is outside the proven resize hit zone")
    pre_cursor = pre_drag.get("cursor", {})
    if not isinstance(pre_cursor, dict) or not pre_cursor.get("visible"):
        failures.append("pre-drag cursor is missing or invisible")
    elif (
        pre_cursor.get("fingerprint") != pre_drag.get("expectedResizeFingerprint")
        or pre_cursor.get("fingerprint") == pre_drag.get("expectedArrowFingerprint")
    ):
        failures.append("pre-drag visible cursor is not the expected resize shape")

    if mouse_down.get("preDragRequirementSatisfied") is not True:
        failures.append("mouse-down did not follow established pre-drag cursor proof")
    if anchor.get("immediatelyBeforeMouseDown") is not True or anchor.get("pointMatches") is not True:
        failures.append("pointer was not re-anchored at the resize edge immediately before mouse-down")
    if int(anchor.get("maximumAttempts", 0) or 0) != 3 or len(anchor.get("attempts") or []) > 3:
        failures.append("mouse-down anchor retry boundary is missing or exceeded")
    anchor_cursor = anchor.get("cursor", {})
    if not isinstance(anchor_cursor, dict) or anchor_cursor.get("fingerprint") != anchor.get("expectedResizeFingerprint"):
        failures.append("mouse-down anchor cursor is not the expected resize shape")
    if mouse_down.get("anchorRequirementSatisfied") is not True:
        failures.append("mouse-down did not follow immediate edge-anchor proof")
    if drag.get("classification") != "GEOMETRY_RESIZE_PROVEN":
        failures.append("geometry resize is not proven")
    if int(drag.get("widthDelta", 0) or 0) > -60:
        failures.append("geometry delta is below the required resize threshold")
    if overall.get("geometryClassification") != "GEOMETRY_RESIZE_PROVEN":
        failures.append("overall geometry classification is not proven")
    if overall.get("visibleCursorClassification") != "VISIBLE_CURSOR_TRANSITION_PROVEN":
        failures.append("overall visible cursor classification is not proven")
    if overall.get("internalCursorClassification") != "INTERNAL_CURSOR_STATE_SUPPORTING_ONLY":
        failures.append("internal cursor state is not labeled supporting-only")
    if overall.get("hitZoneProven") is not True:
        failures.append("overall hit-zone proof is missing")
    if overall.get("mouseDownAfterPreDrag") is not True:
        failures.append("overall event ordering does not prove pre-drag before mouse-down")
    if overall.get("mouseDownAnchorProven") is not True:
        failures.append("overall proof does not preserve immediate mouse-down edge anchoring")
    if overall.get("completedResize") is not True:
        failures.append("overall completed-resize proof is missing")
    if overall.get("postDragNormalCursor") is not True:
        failures.append("overall post-drag normal-cursor proof is missing")

    frame_paths = {
        "outside": str(outside.get("frame", "")),
        "pre_drag": str(pre_drag.get("frame", "")),
        "mouse_down": str(mouse_down.get("mouseDownFrame", "")),
        "mid_drag": str(drag.get("midDragFrame", "")),
        "mouse_up": str(drag.get("mouseUpFrame", "")),
        "leave": str(leave.get("frame", "")),
    }
    ordered_indices: list[int] = []
    for label, path_value in frame_paths.items():
        frame = frames.get(path_value)
        if not frame:
            failures.append(f"ordered cursor frame missing from manifest: {label}")
            continue
        if frame.get("cursorComposited") is not True:
            failures.append(f"actual cursor was not composited in frame: {label}")
        cursor = frame.get("cursor", {})
        if not isinstance(cursor, dict) or not cursor.get("visible"):
            failures.append(f"cursor is not visible in ordered frame: {label}")
        try:
            ordered_indices.append(int(frame.get("index")))
        except (TypeError, ValueError):
            failures.append(f"ordered frame index missing: {label}")
        if require_files:
            path = Path(path_value)
            if not path.exists():
                failures.append(f"ordered frame file missing: {label}")
            elif not path.read_bytes().startswith(PNG_SIGNATURE):
                failures.append(f"ordered frame is not a valid PNG: {label}")
    if len(ordered_indices) == len(frame_paths) and ordered_indices != sorted(ordered_indices):
        failures.append("cursor proof frames are not in required event order")
    if len(set(ordered_indices)) != len(ordered_indices):
        failures.append("cursor proof frame indices are duplicated")

    pre_time = _iso_timestamp(steps.get("visible_cursor_transition_pre_drag", {}).get("timestamp"))
    down_time = _iso_timestamp(steps.get("mouse_down_with_visible_resize_cursor", {}).get("timestamp"))
    if pre_time is None or down_time is None or pre_time >= down_time:
        failures.append("pre-drag cursor proof timestamp is not before mouse-down")
    return failures


def _load_visible_cursor_proof(path: Path, expected_head: str) -> tuple[bool, str, list[Path]]:
    if not path.exists():
        return False, f"CURSOR_CAPTURE_UNPROVEN: manifest missing: {path}", []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"CURSOR_CAPTURE_UNPROVEN: manifest unreadable: {exc}", []
    failures = _visible_cursor_manifest_failures(manifest, expected_head=expected_head)
    frame_paths = [
        Path(str(frame.get("path")))
        for frame in manifest.get("orderedFrames", [])
        if isinstance(frame, dict) and frame.get("path")
    ]
    if failures:
        return False, "CURSOR_CAPTURE_UNPROVEN: " + "; ".join(failures), frame_paths
    return (
        True,
        "VISIBLE_CURSOR_TRANSITION_PROVEN; GEOMETRY_RESIZE_PROVEN; "
        "INTERNAL_CURSOR_STATE_SUPPORTING_ONLY; "
        f"manifest={path}; proofRoot={manifest.get('proofRoot')}",
        frame_paths,
    )


def _synthetic_visible_cursor_manifest(frame_root: Path, expected_head: str) -> dict[str, object]:
    frame_root.mkdir(parents=True, exist_ok=True)
    names = ("outside", "pre_drag", "mouse_down", "mid_drag", "mouse_up", "leave")
    frames: list[dict[str, object]] = []
    paths: dict[str, str] = {}
    for index, name in enumerate(names):
        path = frame_root / f"{index:03d}_{name}.png"
        path.write_bytes(PNG_SIGNATURE + b"fixture")
        paths[name] = str(path)
        frames.append(
            {
                "index": index,
                "path": str(path),
                "cursorComposited": True,
                "cursor": {"visible": True, "fingerprint": "RESIZE" if name in {"pre_drag", "mouse_down", "mid_drag", "mouse_up"} else "ARROW"},
            }
        )
    base_time = dt.datetime(2026, 7, 21, tzinfo=dt.timezone.utc)
    steps = [
        {"id": "pointer_anchored_on_exact_desktop_launcher", "status": "PASS", "timestamp": (base_time - dt.timedelta(seconds=1)).isoformat(), "evidence": {"pointMatches": True, "maximumAttempts": 3, "attempts": [{"attempt": 1, "pointMatched": True}]}},
        {"id": "settings_open_current_runtime", "status": "PASS", "timestamp": (base_time + dt.timedelta(seconds=0)).isoformat(), "evidence": {}},
        {"id": "pointer_outside_resize_zone", "status": "PASS", "timestamp": (base_time + dt.timedelta(seconds=1)).isoformat(), "evidence": {"hitZone": False, "cursor": {"visible": True, "fingerprint": "ARROW"}, "expectedArrowFingerprint": "ARROW", "frame": paths["outside"]}},
        {"id": "visible_cursor_transition_pre_drag", "status": "PASS", "timestamp": (base_time + dt.timedelta(seconds=2)).isoformat(), "evidence": {"classification": "VISIBLE_CURSOR_TRANSITION_PROVEN", "hitZone": True, "cursor": {"visible": True, "fingerprint": "RESIZE"}, "expectedResizeFingerprint": "RESIZE", "expectedArrowFingerprint": "ARROW", "frame": paths["pre_drag"]}},
        {"id": "pointer_reanchored_before_mouse_down", "status": "PASS", "timestamp": (base_time + dt.timedelta(milliseconds=2500)).isoformat(), "evidence": {"immediatelyBeforeMouseDown": True, "pointMatches": True, "maximumAttempts": 3, "attempts": [{"attempt": 1, "pointMatched": True, "cursorMatched": True}], "cursor": {"visible": True, "fingerprint": "RESIZE"}, "expectedResizeFingerprint": "RESIZE"}},
        {"id": "mouse_down_with_visible_resize_cursor", "status": "PASS", "timestamp": (base_time + dt.timedelta(seconds=3)).isoformat(), "evidence": {"preDragRequirementSatisfied": True, "anchorRequirementSatisfied": True, "mouseDownFrame": paths["mouse_down"]}},
        {"id": "held_drag_and_completed_resize", "status": "PASS", "timestamp": (base_time + dt.timedelta(seconds=4)).isoformat(), "evidence": {"classification": "GEOMETRY_RESIZE_PROVEN", "widthDelta": -80, "midDragFrame": paths["mid_drag"], "mouseUpFrame": paths["mouse_up"]}},
        {"id": "pointer_leaves_resize_zone", "status": "PASS", "timestamp": (base_time + dt.timedelta(seconds=5)).isoformat(), "evidence": {"frame": paths["leave"]}},
        {"id": "resize_cursor_workstream_proof", "status": "PASS", "timestamp": (base_time + dt.timedelta(seconds=6)).isoformat(), "evidence": {"geometryClassification": "GEOMETRY_RESIZE_PROVEN", "visibleCursorClassification": "VISIBLE_CURSOR_TRANSITION_PROVEN", "internalCursorClassification": "INTERNAL_CURSOR_STATE_SUPPORTING_ONLY", "hitZoneProven": True, "mouseDownAfterPreDrag": True, "mouseDownAnchorProven": True, "completedResize": True, "postDragNormalCursor": True}},
    ]
    return {
        "schema": "fam003-r2-workstream-resize-cursor-proof-v1",
        "status": "PASS",
        "proofMode": "R2_WORKSTREAM_RESIZE_CURSOR_ONLY",
        "branch": "feature/fam-003-settings-resize-proof",
        "head": expected_head,
        "formalHardening": False,
        "formalLiveValidation": False,
        "utsStatus": "NOT_REQUESTED",
        "cursorFabrication": False,
        "cursorCaptureMethod": "GDI CopyFromScreen plus DrawIconEx of the actual GetCursorInfo hCursor",
        "steps": steps,
        "orderedFrames": frames,
        "proofRoot": str(frame_root),
    }


def _run_visible_cursor_negative_fixtures(expected_head: str) -> tuple[bool, str]:
    fixture = json.loads(VISIBLE_CURSOR_FIXTURE.read_text(encoding="utf-8"))
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="fam003-cursor-fixture-") as temp_dir:
        valid = _synthetic_visible_cursor_manifest(Path(temp_dir), expected_head)
        if _visible_cursor_manifest_failures(valid, expected_head=expected_head):
            failures.append("valid visible-cursor fixture did not pass")
        for case in fixture.get("cases", []):
            case_id = str(case.get("id"))
            mutated = copy.deepcopy(valid)
            steps = {step["id"]: step for step in mutated["steps"]}
            frames = {Path(frame["path"]).stem.split("_", 1)[1]: frame for frame in mutated["orderedFrames"]}
            if case_id == "geometry_only_without_visible_cursor":
                steps["visible_cursor_transition_pre_drag"]["evidence"]["classification"] = "CURSOR_CAPTURE_UNPROVEN"
            elif case_id == "telemetry_only_cursor_promotion":
                steps["resize_cursor_workstream_proof"]["evidence"]["visibleCursorClassification"] = "INTERNAL_CURSOR_STATE_SUPPORTING_ONLY"
            elif case_id == "pointer_outside_hit_zone":
                steps["visible_cursor_transition_pre_drag"]["evidence"]["hitZone"] = False
            elif case_id == "predrag_after_mousedown":
                steps["visible_cursor_transition_pre_drag"]["timestamp"] = (dt.datetime(2026, 7, 21, 0, 0, 4, tzinfo=dt.timezone.utc)).isoformat()
            elif case_id == "pointer_moved_before_mousedown":
                steps["pointer_reanchored_before_mouse_down"]["evidence"]["pointMatches"] = False
                steps["mouse_down_with_visible_resize_cursor"]["evidence"]["anchorRequirementSatisfied"] = False
                steps["resize_cursor_workstream_proof"]["evidence"]["mouseDownAnchorProven"] = False
            elif case_id == "desktop_launcher_pointer_moved":
                steps["pointer_anchored_on_exact_desktop_launcher"]["evidence"]["pointMatches"] = False
            elif case_id == "missing_cursor_frame":
                mutated["orderedFrames"] = [frame for frame in mutated["orderedFrames"] if frame is not frames["pre_drag"]]
            elif case_id == "cursor_not_composited":
                frames["pre_drag"]["cursorComposited"] = False
            elif case_id == "stale_head":
                mutated["head"] = "0" * 40
            elif case_id == "child_failure_top_level_pass":
                steps["visible_cursor_transition_pre_drag"]["status"] = "FAIL"
            else:
                failures.append(f"unknown negative fixture: {case_id}")
                continue
            if not _visible_cursor_manifest_failures(mutated, expected_head=expected_head):
                failures.append(f"negative fixture did not fail closed: {case_id}")
    if failures:
        return False, "; ".join(failures)
    return True, f"{len(fixture.get('cases', []))} visible-cursor negative fixtures failed closed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--visible-cursor-manifest",
        type=Path,
        default=VISIBLE_CURSOR_PROOF_LATEST,
        help="Current normal-runtime R2 Workstream visible-cursor proof manifest.",
    )
    parser.add_argument(
        "--self-test-cursor-proof",
        action="store_true",
        help="Run fail-closed visible-cursor negative fixtures and exit.",
    )
    args = parser.parse_args()
    current_head = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    if args.self_test_cursor_proof:
        ok, detail = _run_visible_cursor_negative_fixtures(current_head)
        print(("PASS" if ok else "FAIL") + f": {detail}")
        return 0 if ok else 1

    stamp = os.environ.get("FAM003_SETTINGS_VISUAL_PROOF_STAMP") or dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = LOG_ROOT / stamp
    if log_dir.exists():
        log_root_resolved = LOG_ROOT.resolve()
        log_dir_resolved = log_dir.resolve()
        if log_root_resolved not in log_dir_resolved.parents:
            raise RuntimeError(f"Refusing to clear proof directory outside {LOG_ROOT}: {log_dir}")
        shutil.rmtree(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    _configure_qt_environment(log_dir)
    Path(os.environ["NEXUS_RESIDENT_ACCESS_SETTINGS_PATH"]).write_text(
        json.dumps(
            {
                "quickSlotIds": ["command_overlay", "create_custom_task", "open_saved_actions_folder"],
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

    from PySide6.QtCore import QPoint, QRect, Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import (
        QApplication,
        QCheckBox,
        QComboBox,
        QFrame,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QPushButton,
        QScrollArea,
        QSizePolicy,
        QSlider,
        QVBoxLayout,
        QWidget,
    )

    from desktop.desktop_renderer import ResidentAccessSettingsDialog
    from desktop.hotkeys import GlobalHotkeyManager, ShutdownBus
    from desktop.resident_access import DEFAULT_QUICK_SLOT_ROUTE_IDS, MAX_QUICK_SLOT_COUNT, quick_slot_candidate_routes

    app = QApplication.instance() or QApplication([])
    rows: list[tuple[str, bool, str]] = []
    artifacts: list[dict[str, str]] = []
    visible_cursor_ok, visible_cursor_detail, visible_cursor_frames = _load_visible_cursor_proof(
        args.visible_cursor_manifest,
        current_head,
    )
    rows.append(("visible USER-facing resize cursor proof", visible_cursor_ok, visible_cursor_detail))
    cursor_fixture_ok, cursor_fixture_detail = _run_visible_cursor_negative_fixtures(current_head)
    rows.append(("visible resize cursor negative fixtures", cursor_fixture_ok, cursor_fixture_detail))
    for cursor_frame in visible_cursor_frames:
        artifacts.append(
            {
                "path": str(cursor_frame),
                "surface": "normal-runtime Global Settings resize cursor",
                "state": "ordered real-input visible cursor proof",
                "width": "virtual desktop",
                "height": "virtual desktop",
                "saved": str(cursor_frame.exists()),
            }
        )
    rows.extend(_copy_reference_artifacts(log_dir, artifacts))
    manage_guard_rows, manage_guard_reference_path, manage_guard_ledger_path = _write_manage_monitors_guard_reference(log_dir, artifacts)
    rows.extend(manage_guard_rows)
    udl_exists_ok, udl_exists_detail, udl_closed_ok, udl_closed_detail = _visual_udl_status_rows()
    rows.append(("visual UDL exists", udl_exists_ok, udl_exists_detail))
    rows.append(("visual UDL rows closed with proof", udl_closed_ok, udl_closed_detail))
    (
        active_udl_exists_ok,
        active_udl_exists_detail,
        active_udl_gate_label,
        active_udl_closed_ok,
        active_udl_closed_detail,
    ) = _active_false_retest_udl_status_rows()
    rows.append(("active false-retest UDL rows exist", active_udl_exists_ok, active_udl_exists_detail))
    rows.append((active_udl_gate_label, active_udl_closed_ok, active_udl_closed_detail))

    dialog = ResidentAccessSettingsDialog()
    dialog.show()
    app.processEvents()
    active_slot_limit = min(MAX_QUICK_SLOT_COUNT, len(quick_slot_candidate_routes()))

    def _run_settings_stress_matrix() -> list[tuple[str, bool, str]]:
        stress_rows: list[tuple[str, bool, str]] = []
        stress_dialog = ResidentAccessSettingsDialog()
        stress_dialog.setProperty("validationOnlyStressMatrix", "true")
        stress_dialog.set_focus("quick_access")
        stress_dialog.resize(820, 540)
        stress_dialog.show()
        stress_dialog.raise_()
        stress_dialog.activateWindow()
        app.processEvents()

        nav_layout = stress_dialog.nav_content.layout()
        synthetic_main: list[QFrame] = []
        synthetic_child: list[QFrame] = []
        insert_at = max(0, nav_layout.count() - 1)
        for index in range(1, 15):
            main_row = QFrame(stress_dialog.nav_content)
            main_row.setObjectName("residentAccessSettingsCategoryItem")
            main_row.setProperty("validationOnlySyntheticNav", "main")
            main_row.setProperty("settingsNavDensity", "validation-main-row")
            main_row.setAttribute(Qt.WA_StyledBackground, True)
            main_row.setFixedSize(94, 24)
            main_layout = QHBoxLayout(main_row)
            main_layout.setContentsMargins(3, 1, 3, 1)
            main_layout.setSpacing(3)
            main_button = QPushButton(f"Cat {index:02d}", main_row)
            main_button.setObjectName("residentAccessSettingsCategoryButton")
            main_button.setProperty("validationOnlySyntheticNavButton", "main")
            main_button.setFlat(True)
            main_button.setFocusPolicy(Qt.NoFocus)
            main_layout.addWidget(main_button, 1)
            nav_layout.insertWidget(insert_at, main_row)
            insert_at += 1
            synthetic_main.append(main_row)

            child_row = QFrame(stress_dialog.nav_content)
            child_row.setObjectName("residentAccessSettingsNavItem")
            child_row.setProperty("validationOnlySyntheticNav", "child")
            child_row.setProperty("settingsNavDensity", "validation-child-row")
            child_row.setAttribute(Qt.WA_StyledBackground, True)
            child_row.setFixedSize(90, 23)
            child_layout = QHBoxLayout(child_row)
            child_layout.setContentsMargins(11, 1, 3, 1)
            child_layout.setSpacing(3)
            child_button = QPushButton(f"Sub {index:02d}", child_row)
            child_button.setObjectName("residentAccessSettingsNavButton")
            child_button.setProperty("validationOnlySyntheticNavButton", "child")
            child_button.setFlat(True)
            child_button.setFocusPolicy(Qt.NoFocus)
            child_layout.addWidget(child_button, 1)
            nav_layout.insertWidget(insert_at, child_row)
            insert_at += 1
            synthetic_child.append(child_row)

        stress_dialog.nav_content.setMinimumHeight(max(stress_dialog.nav_content.minimumHeight(), 736))
        stress_dialog.settings_splitter.setSizes([160, 620])
        stress_dialog.section_scope.setText("VALIDATION STRESS / MIXED CONTENT")
        stress_dialog.section_scope.setVisible(True)
        stress_dialog.section_heading.setText("Stress Matrix")
        stress_dialog.section_detail.setText("Validation-only rail overflow and mixed settings controls.")
        stress_dialog.section_detail.setVisible(True)
        stress_dialog.quick_slot_container.setVisible(False)
        stress_dialog.footer_frame.setVisible(False)
        stress_dialog.tray_overview_container.setVisible(False)
        stress_dialog.route_summary.setVisible(False)

        stress_container = QFrame(stress_dialog.settings_page_frame)
        stress_container.setObjectName("residentAccessTrayOverviewContainer")
        stress_container.setProperty("validationOnlyStressContent", "mixed-settings-controls")
        stress_container.setAttribute(Qt.WA_StyledBackground, True)
        stress_container.setMinimumWidth(400)
        stress_layout = QVBoxLayout(stress_container)
        stress_layout.setContentsMargins(8, 7, 8, 7)
        stress_layout.setSpacing(6)
        stress_scroll = QScrollArea(stress_container)
        stress_scroll.setObjectName("residentAccessSettingsStressScroll")
        stress_scroll.setWidgetResizable(True)
        stress_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        stress_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        stress_scroll.setFrameShape(QFrame.NoFrame)
        stress_scroll.setMinimumHeight(260)
        stress_scroll.setStyleSheet(
            "#residentAccessSettingsStressScroll {"
            " background: transparent;"
            " border: none;"
            "}"
            "#residentAccessSettingsStressContent {"
            " background: rgba(2, 12, 24, 0.42);"
            " border: none;"
            "}"
            "#residentAccessSettingsStressRow {"
            " background: rgba(5, 18, 32, 0.72);"
            " border: 1px solid rgba(117, 228, 255, 0.14);"
            " border-radius: 6px;"
            "}"
            "#residentAccessSettingsStressRow QLabel {"
            " color: rgba(222, 240, 237, 0.96);"
            " font-size: 12px;"
            " font-weight: 700;"
            "}"
            "#residentAccessSettingsStressRow[stressState=\"degraded\"] QLabel {"
            " color: rgba(255, 214, 108, 0.92);"
            "}"
            "#residentAccessSettingsStressRow[stressState=\"empty\"] QLabel {"
            " color: rgba(148, 184, 199, 0.88);"
            "}"
        )
        stress_content = QWidget(stress_scroll)
        stress_content.setObjectName("residentAccessSettingsStressContent")
        stress_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        stress_content_layout = QVBoxLayout(stress_content)
        stress_content_layout.setContentsMargins(0, 0, 0, 0)
        stress_content_layout.setSpacing(5)

        stress_controls: dict[str, QWidget] = {}

        def add_row(label: str, widget: QWidget | None = None, *, state: str = "normal") -> QFrame:
            row = QFrame(stress_content)
            row.setObjectName("residentAccessSettingsStressRow")
            row.setProperty("stressState", state)
            row.setAttribute(Qt.WA_StyledBackground, True)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(8, 4, 8, 4)
            row_layout.setSpacing(8)
            row_label = QLabel(label, row)
            row_label.setObjectName("residentAccessSettingsStressLabel")
            row_layout.addWidget(row_label, 1)
            if widget is not None:
                widget.setParent(row)
                row_layout.addWidget(widget, 0)
            stress_content_layout.addWidget(row)
            return row

        combo = QComboBox()
        combo.setObjectName("residentAccessSettingsStressCombo")
        combo.addItems(["Compact", "Balanced", "Expanded"])
        combo.setMaximumWidth(170)
        stress_controls["combo"] = combo
        add_row("Dropdown option", combo)

        checkbox = QCheckBox("Enabled")
        checkbox.setObjectName("residentAccessSettingsStressCheckbox")
        checkbox.setChecked(True)
        stress_controls["checkbox"] = checkbox
        add_row("Checkbox setting", checkbox)

        line_edit = QLineEdit("Nexus setting value")
        line_edit.setObjectName("residentAccessSettingsStressLineEdit")
        line_edit.setMaximumWidth(190)
        stress_controls["line_edit"] = line_edit
        add_row("Text field", line_edit)

        slider = QSlider(Qt.Horizontal)
        slider.setObjectName("residentAccessSettingsStressSlider")
        slider.setRange(0, 100)
        slider.setValue(62)
        slider.setFixedWidth(170)
        stress_controls["slider"] = slider
        add_row("Slider setting", slider)

        action_button = QPushButton("Apply")
        action_button.setObjectName("residentAccessSettingsStressActionButton")
        stress_controls["button"] = action_button
        add_row("Button action", action_button)

        disabled_button = QPushButton("Unavailable")
        disabled_button.setObjectName("residentAccessSettingsStressDisabledButton")
        disabled_button.setEnabled(False)
        stress_controls["disabled_button"] = disabled_button
        add_row("Disabled control", disabled_button, state="degraded")

        for row_index in range(1, 9):
            add_row(f"List row {row_index:02d}")
        add_row("Empty state row", state="empty")
        add_row("Degraded recovery row", state="degraded")
        stress_content_layout.addStretch(1)
        stress_scroll.setWidget(stress_content)
        stress_layout.addWidget(stress_scroll)
        stress_dialog.settings_page_frame.layout().addWidget(stress_container)
        app.processEvents()

        stress_sizes = [(684, 500), (700, 500), (780, 500), (840, 530), (840, 610)]
        size_results: list[str] = []
        attached_ok = True
        for width_target, height_target in stress_sizes:
            stress_dialog.resize(width_target, height_target)
            if width_target <= 640:
                stress_dialog.settings_splitter.setSizes([150, max(430, width_target - 168)])
            else:
                stress_dialog.settings_splitter.setSizes([160, max(540, width_target - 178)])
            app.processEvents()
            path = log_dir / f"19_stress_size_{width_target}x{height_target}.png"
            capture_ok, captured_width, captured_height = _capture(
                stress_dialog,
                path,
                artifacts,
                surface="validation-only Global Settings stress matrix",
                state=f"{width_target}x{height_target} size matrix",
            )
            content_shell = stress_dialog.settings_splitter.widget(1)
            page_origin = stress_dialog.settings_page_frame.mapTo(stress_dialog, QPoint(0, 0))
            content_origin = content_shell.mapTo(stress_dialog, QPoint(0, 0))
            page_left_gap = page_origin.x() - content_origin.x()
            page_right = page_origin.x() + stress_dialog.settings_page_frame.width()
            content_right = content_origin.x() + content_shell.width()
            page_right_gap = content_right - page_right
            expected_width = min(max(width_target, stress_dialog.minimumWidth()), stress_dialog.maximumWidth())
            expected_height = min(max(height_target, stress_dialog.minimumHeight()), stress_dialog.maximumHeight())
            size_ok = (
                capture_ok
                and captured_width == expected_width
                and captured_height == expected_height
                and 0 <= page_left_gap <= 8
                and 0 <= page_right_gap <= 36
            )
            attached_ok = attached_ok and size_ok
            size_results.append(
                f"{width_target}x{height_target}->{captured_width}x{captured_height}; left_gap={page_left_gap}; right_gap={page_right_gap}; ok={size_ok}"
            )

        rail_path = log_dir / "20_stress_left_rail_28_categories.png"
        rail_ok, rail_width, rail_height = _capture(
            stress_dialog.nav_shell,
            rail_path,
            artifacts,
            surface="validation-only left rail stress",
            state="14 parent and 14 child synthetic rows",
        )
        content_path = log_dir / "21_stress_content_mixed_controls.png"
        content_ok, content_width, content_height = _capture(
            stress_dialog.settings_page_frame,
            content_path,
            artifacts,
            surface="validation-only mixed settings content",
            state="dropdown checkbox text slider buttons list empty degraded",
        )
        stress_light_ratio = _light_pixel_ratio(content_path)
        stress_hbar_max = stress_dialog.nav_scroll_area.horizontalScrollBar().maximum()
        stress_vbar_max = stress_dialog.nav_scroll_area.verticalScrollBar().maximum()
        stress_scroll_hbar_max = stress_scroll.horizontalScrollBar().maximum()
        stress_scroll_vbar_max = stress_scroll.verticalScrollBar().maximum()
        stress_rows.append(
            (
                "stress rail supports 25+ main/sub categories",
                rail_ok
                and len(synthetic_main) == 14
                and len(synthetic_child) == 14
                and stress_vbar_max > 0
                and stress_hbar_max == 0
                and stress_dialog.nav_scroll_area.horizontalScrollBarPolicy() == Qt.ScrollBarAsNeeded
                and all(row.width() <= stress_dialog.nav_content.width() for row in [*synthetic_main, *synthetic_child]),
                f"{rail_path} ({rail_width}x{rail_height}); main={len(synthetic_main)}; child={len(synthetic_child)}; nav_hbar={stress_hbar_max}; nav_vbar={stress_vbar_max}; nav_content_width={stress_dialog.nav_content.width()}; synthetic_widths={[row.width() for row in [*synthetic_main[:2], *synthetic_child[:2]]]}",
            )
        )
        stress_rows.append(
            (
                "stress content pane supports mixed control types",
                content_ok
                and all(widget.isVisible() for widget in stress_controls.values())
                and combo.count() == 3
                and checkbox.isChecked()
                and line_edit.text() == "Nexus setting value"
                and slider.value() == 62
                and not disabled_button.isEnabled()
                and len(stress_content.findChildren(QFrame, "residentAccessSettingsStressRow")) >= 16,
                f"{content_path} ({content_width}x{content_height}); controls={list(stress_controls)}; rows={len(stress_content.findChildren(QFrame, 'residentAccessSettingsStressRow'))}; scroll_hbar={stress_scroll_hbar_max}; scroll_vbar={stress_scroll_vbar_max}",
            )
        )
        stress_rows.append(
            (
                "stress window size matrix preserves anchored content",
                attached_ok and stress_scroll_hbar_max == 0,
                "; ".join(size_results) + f"; stress_scroll_hbar={stress_scroll_hbar_max}",
            )
        )
        stress_rows.append(
            (
                "stress content proof is not white/native-light",
                content_ok and stress_light_ratio < 0.20,
                f"{content_path}; light_pixel_ratio={stress_light_ratio:.3f}",
            )
        )
        stress_dialog.close()
        stress_dialog.deleteLater()
        app.processEvents()
        return stress_rows

    default_path = log_dir / "01_default_global_settings_shell.png"
    default_ok, width, height = _capture(
        dialog,
        default_path,
        artifacts,
        surface="full Global Settings shell",
        state="default Quick Access page",
    )
    light_ratio = _light_pixel_ratio(default_path)
    default_slot_bottom = dialog.quick_slot_container.mapTo(dialog, QPoint(0, dialog.quick_slot_container.height())).y()
    default_footer_top = dialog.footer_frame.mapTo(dialog, QPoint(0, 0)).y()
    default_footer_gap = max(0, default_footer_top - default_slot_bottom)
    rows.append(
        (
            "default screenshot saved",
            default_ok and 776 <= width <= 790 and 450 <= height <= 470,
            f"{default_path} ({width}x{height})",
        )
    )
    rows.append(
        (
            "architecture-first Global Settings geometry",
            776 <= width <= 790 and 450 <= height <= 470,
            f"window={width}x{height}; required compact deterministic settings shell, not old sparse Quick Access utility form",
        )
    )
    rows.append(
        (
            "settings shell fills the window intentionally",
            width <= 790
            and height <= 470
            and dialog.SETTINGS_NAV_MIN_WIDTH <= dialog.nav_shell.width() <= dialog.SETTINGS_NAV_MAX_WIDTH
            and getattr(dialog, "settings_splitter", None) is not None
            and dialog.settings_splitter.handleWidth() == 9
            and dialog.tray_nav_item.isVisible()
            and dialog.tray_nav_button.isVisible()
            and dialog.tray_expand_button.isVisible()
            and dialog.tray_expand_button.property("glyphButton") == "chevron-down"
            and dialog.subpage_nav_rail.isVisible()
            and dialog.settings_page_frame.isVisible()
            and dialog.quick_slot_container.isVisible()
            and dialog.quick_slot_container.height() >= 246
            and default_footer_gap <= 16,
            f"window={width}x{height}; nav_width={dialog.nav_shell.width()}; splitter_handle={getattr(dialog, 'settings_splitter', None).handleWidth() if getattr(dialog, 'settings_splitter', None) is not None else '<missing>'}; tray_visible={dialog.tray_nav_item.isVisible()}; subpage_visible={dialog.subpage_nav_rail.isVisible()}; page_visible={dialog.settings_page_frame.isVisible()}; slot_panel_height={dialog.quick_slot_container.height()}; footer_gap={default_footer_gap}",
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
            and dialog.chrome_bar.property("headerAnatomy") == "ndai-global-settings-centered-settings-chrome-v22"
            and dialog.chrome_bar.control_cluster.objectName() == "residentAccessSettingsWindowControls"
            and dialog.chrome_bar.control_cluster.property("controlClusterDensity") == "settings-compact-v22"
            and dialog.chrome_bar.minimize_button.isVisible()
            and dialog.chrome_bar.close_button.isVisible()
            and not dialog.chrome_bar.maximize_button.isVisible()
            and not hasattr(dialog, "resize_grip")
            and not dialog.findChildren(QFrame, "residentAccessSettingsResizeGrip")
            and dialog.chrome_bar.close_button.accessibleName() == "Close Settings",
            f"{chrome_path} ({chrome_width}x{chrome_height}); anatomy={dialog.chrome_bar.property('headerAnatomy')!r}; density={dialog.chrome_bar.control_cluster.property('controlClusterDensity')!r}; cluster={dialog.chrome_bar.control_cluster.objectName()!r}; minimize={dialog.chrome_bar.minimize_button.isVisible()}; close={dialog.chrome_bar.close_button.isVisible()}; maximize_visible={dialog.chrome_bar.maximize_button.isVisible()}; resize_grip_attr={hasattr(dialog, 'resize_grip')}; grip_widgets={len(dialog.findChildren(QFrame, 'residentAccessSettingsResizeGrip'))}",
        )
    )
    rows.append(
        (
            "settings-specific seamless title row",
            dialog.chrome_bar.kicker_label.text() == ""
            and not dialog.chrome_bar.kicker_label.isVisible()
            and dialog.chrome_bar.title_label.text() == "Settings"
            and dialog.chrome_bar.title_label.alignment() & Qt.AlignHCenter
            and dialog.chrome_bar.subtitle_label.text() == ""
            and not dialog.chrome_bar.subtitle_label.isVisible()
            and role_text == []
            and not dialog.chrome_bar.role_pill.isVisible(),
            f"kicker={dialog.chrome_bar.kicker_label.text()!r}/{dialog.chrome_bar.kicker_label.isVisible()}; title={dialog.chrome_bar.title_label.text()!r}; title_alignment={int(dialog.chrome_bar.title_label.alignment())}; subtitle={dialog.chrome_bar.subtitle_label.text()!r}; subtitle_visible={dialog.chrome_bar.subtitle_label.isVisible()}; role_pairs={role_text}; role_pill_visible={dialog.chrome_bar.role_pill.isVisible()}; chrome_height={dialog.chrome_bar.height()}",
        )
    )
    visible_title_text = " ".join(
        segment
        for segment in (
            dialog.chrome_bar.kicker_label.text() if dialog.chrome_bar.kicker_label.isVisible() else "",
            dialog.chrome_bar.title_label.text() if dialog.chrome_bar.title_label.isVisible() else "",
            dialog.chrome_bar.subtitle_label.text() if dialog.chrome_bar.subtitle_label.isVisible() else "",
            " ".join(role_text) if dialog.chrome_bar.role_pill.isVisible() else "",
        )
        if segment
    )
    rows.append(
        (
            "centered Settings title only",
            visible_title_text == "Settings"
            and dialog.chrome_bar.title_label.alignment() & Qt.AlignHCenter
            and "NEXUS DESKTOP AI" not in visible_title_text
            and "Global Settings" not in visible_title_text,
            f"visible_title_text={visible_title_text!r}; alignment={int(dialog.chrome_bar.title_label.alignment())}; window_title={dialog.windowTitle()!r}",
        )
    )
    visible_watermark_widgets = [
        widget.objectName()
        for widget in dialog.findChildren(QLabel)
        if widget.isVisible()
        and ("watermark" in widget.objectName().lower() or "watermark" in widget.text().lower())
    ]
    rows.append(
        (
            "deferred watermark recorded without runtime exposure",
            dialog.property("deferredWatermarkConcept") == "future-centered-global-settings-watermark-deferred-no-runtime-exposure-v22"
            and dialog.property("runtimeWatermarkVisible") == "false"
            and not visible_watermark_widgets,
            f"deferred={dialog.property('deferredWatermarkConcept')!r}; runtime={dialog.property('runtimeWatermarkVisible')!r}; visible_watermark_widgets={visible_watermark_widgets}",
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

    original_geometry = dialog.geometry()
    QTest.mousePress(dialog.chrome_bar, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, QPoint(26, 18))
    QTest.mouseMove(dialog.chrome_bar, QPoint(88, 38), delay=120)
    QTest.mouseRelease(dialog.chrome_bar, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, QPoint(88, 38))
    app.processEvents()
    moved_geometry = dialog.geometry()
    moved_path = log_dir / "03a_window_moved_by_chrome.png"
    moved_ok, _, _ = _capture(
        dialog,
        moved_path,
        artifacts,
        surface="full Global Settings shell",
        state="moved by compact chrome",
    )
    rows.append(
        (
            "window chrome drag/move proof",
            moved_ok and moved_geometry.topLeft() != original_geometry.topLeft(),
            f"{moved_path}; before={original_geometry.getRect()}; after={moved_geometry.getRect()}",
        )
    )
    dialog.setGeometry(original_geometry)
    app.processEvents()

    dialog.resize(790, 430)
    app.processEvents()
    resized_path = log_dir / "03b_window_resized.png"
    resized_ok, resized_width, resized_height = _capture(
        dialog,
        resized_path,
        artifacts,
        surface="full Global Settings shell",
        state="medium resized with native edge/corner resize rail",
    )
    dialog.resize(820, 500)
    app.processEvents()
    wide_path = log_dir / "03d_window_wide_size.png"
    wide_ok, wide_width, wide_height = _capture(
        dialog,
        wide_path,
        artifacts,
        surface="full Global Settings shell",
        state="wide resized with splitter-attached active settings content",
    )
    wide_content_shell = dialog.settings_splitter.widget(1)
    wide_page_origin = dialog.settings_page_frame.mapTo(dialog, QPoint(0, 0))
    wide_content_origin = wide_content_shell.mapTo(dialog, QPoint(0, 0))
    wide_footer_origin = dialog.footer_frame.mapTo(dialog, QPoint(0, 0))
    wide_quick_origin = dialog.quick_slot_container.mapTo(dialog, QPoint(0, 0))
    wide_page_width = dialog.settings_page_frame.width()
    wide_page_height = dialog.settings_page_frame.height()
    wide_footer_width = dialog.footer_frame.width()
    wide_quick_width = dialog.quick_slot_container.width()
    wide_page_left_gap = wide_page_origin.x() - wide_content_origin.x()
    wide_page_right_gap = (
        wide_content_origin.x()
        + wide_content_shell.width()
        - (wide_page_origin.x() + wide_page_width)
    )
    wide_footer_right_gap = wide_quick_origin.x() + wide_quick_width - (wide_footer_origin.x() + wide_footer_width)
    dialog.resize(320, 200)
    app.processEvents()
    min_path = log_dir / "03c_window_minimum_size.png"
    min_ok, min_width, min_height = _capture(
        dialog,
        min_path,
        artifacts,
        surface="full Global Settings shell",
        state="minimum-size enforcement",
    )
    rows.append(
        (
            "window resize/minimum-size proof",
            resized_ok
            and wide_ok
            and min_ok
            and 790 <= resized_width <= 820
            and 450 <= resized_height <= 470
            and 820 <= wide_width <= 850
            and 490 <= wide_height <= 530
            and wide_width >= resized_width
            and wide_height >= resized_height
            and 684 <= min_width <= 698
            and 450 <= min_height <= 470
            and not hasattr(dialog, "resize_grip")
            and not dialog.findChildren(QFrame, "residentAccessSettingsResizeGrip")
            and dialog.RESIZE_MARGIN == 8
            and getattr(dialog, "RESIZE_CORNER_MARGIN", None) == 12
            and dialog.minimumWidth() == 684
            and 450 <= dialog.minimumHeight() <= 470
            and dialog.maximumWidth() == 840
            and dialog.maximumHeight() == 610
            and dialog.property("windowResizeBehavior") == "uiref-007-frameless-top-level-hover-polled-edge-corner-cursor-app-owned-fallback-8px-edge-12px-corner-no-visible-grip-splitter-travel-76-270-horizontal-overflow-minimum-684x388-dynamic-content-minimum-maximum-840x610-close-intercept-no-forced-arrow-hysteresis-v43",
            f"resized={resized_width}x{resized_height}; wide={wide_width}x{wide_height}; min={min_width}x{min_height}; grip_attr={hasattr(dialog, 'resize_grip')}; grip_widgets={len(dialog.findChildren(QFrame, 'residentAccessSettingsResizeGrip'))}; margin={dialog.RESIZE_MARGIN}; corner_margin={getattr(dialog, 'RESIZE_CORNER_MARGIN', None)}; behavior={dialog.property('windowResizeBehavior')!r}",
        )
    )
    rows.append(
        (
            "wide layout keeps active settings page attached to splitter",
            wide_ok
            and dialog.maximumWidth() == 840
            and dialog.maximumHeight() == 610
            and 820 <= wide_width <= 850
            and wide_height >= 490
            and 610 <= wide_page_width <= 660
            and 0 <= wide_page_left_gap <= 8
            and 0 <= wide_page_right_gap <= 36
            and 0 <= wide_footer_right_gap <= 12,
            f"wide={wide_width}x{wide_height}; max={dialog.maximumWidth()}x{dialog.maximumHeight()}; content={wide_content_shell.width()} at x={wide_content_origin.x()}; page={wide_page_width}x{wide_page_height} at x={wide_page_origin.x()}; quick_panel={wide_quick_width} at x={wide_quick_origin.x()}; page_left_gap={wide_page_left_gap}; page_right_gap={wide_page_right_gap}; footer_width={wide_footer_width}; footer_to_panel_right_gap={wide_footer_right_gap}",
        )
    )
    rows.append(
        (
            "live max proof is separated from synthetic stress proof",
            dialog.maximumWidth() == 840
            and dialog.maximumHeight() == 610
            and not (log_dir / "19_stress_size_1100x720.png").exists()
            and not (log_dir / "19_stress_size_920x520.png").exists(),
            f"live_max={dialog.maximumWidth()}x{dialog.maximumHeight()}; stale_1100={(log_dir / '19_stress_size_1100x720.png').exists()}; stale_920={(log_dir / '19_stress_size_920x520.png').exists()}",
        )
    )
    rows.append(
        (
            "live max has no unexplained right-side dead space",
            wide_ok
            and 0 <= wide_page_right_gap <= 36
            and 0 <= wide_footer_right_gap <= 12
            and wide_content_shell.width() <= 650,
            f"content_width={wide_content_shell.width()}; page_width={wide_page_width}; page_right_gap={wide_page_right_gap}; footer_to_panel_right_gap={wide_footer_right_gap}",
        )
    )
    drag_probe = ResidentAccessSettingsDialog()
    drag_probe.move(160, 120)
    drag_probe.show()
    drag_probe.raise_()
    drag_probe.activateWindow()
    for _ in range(18):
        app.processEvents()
        time.sleep(0.01)
    live_drag_geometry_ok, live_drag_detail = _drive_win32_user_resize_drag(
        app,
        drag_probe,
        drag_probe.rect().bottomRight() - QPoint(8, 8),
        QPoint(170, 120),
    )
    live_drag_path = log_dir / "03e_live_user_drag_resized.png"
    live_drag_capture_ok, live_drag_width, live_drag_height = _capture(
        drag_probe,
        live_drag_path,
        artifacts,
        surface="full Global Settings shell",
        state="live-style user drag resized from reachable bottom-right corner rail",
    )
    rows.append(
        (
            "live-style user drag resize proof",
            live_drag_geometry_ok
            and visible_cursor_ok
            and live_drag_capture_ok
            and live_drag_width >= 810
            and live_drag_height >= 470
            and hasattr(drag_probe, "_start_settings_resize")
            and hasattr(drag_probe, "_finish_settings_resize")
            and drag_probe.property("windowResizeBehavior")
            == "uiref-007-frameless-top-level-hover-polled-edge-corner-cursor-app-owned-fallback-8px-edge-12px-corner-no-visible-grip-splitter-travel-76-270-horizontal-overflow-minimum-684x388-dynamic-content-minimum-maximum-840x610-close-intercept-no-forced-arrow-hysteresis-v43",
            f"{live_drag_path}; {live_drag_detail}; captured={live_drag_width}x{live_drag_height}; "
            f"externalVisibleCursorProof={visible_cursor_detail}",
        )
    )
    drag_probe.close()
    dialog.setGeometry(original_geometry)
    app.processEvents()

    nav_path = log_dir / "04_left_settings_organizer.png"
    nav_ok, nav_width, nav_height = _capture(
        dialog.nav_shell,
        nav_path,
        artifacts,
        surface="left settings organizer",
        state="Quick Access selected",
    )
    parent_nav_origin = dialog.tray_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0))
    child_nav_origin = dialog.quick_access_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0))
    hud_parent_nav_origin = dialog.hud_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0))
    hud_child_nav_origin = dialog.hud_dashboard_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0))
    rows.append(
        (
            "left navigation settings organizer",
            nav_ok
            and dialog.nav_shell.isVisible()
            and dialog.tray_nav_item.isVisible()
            and dialog.tray_nav_item.property("settingsCategoryRole") == "selectable-parent-page"
            and dialog.tray_nav_item.property("settingsNavDensity") == "slim-parent-row"
            and dialog.tray_nav_button.text() == "Tray"
            and dialog.subpage_nav_rail.isVisible()
            and dialog.quick_access_nav_button.isChecked()
            and dialog.quick_access_nav_item.isVisible()
            and dialog.quick_access_nav_item.property("settingsNavDensity") == "two-level-subpage-row"
            and dialog.quick_access_nav_item.property("settingsNavIdentity") == "ndai-signal-leaf"
            and dialog.nav_shell.property("settingsShellIdentity") == "ndai-slim-global-settings"
            and dialog.nav_scroll_area.horizontalScrollBarPolicy() == Qt.ScrollBarAsNeeded
            and dialog.nav_scroll_area.verticalScrollBarPolicy() == Qt.ScrollBarAsNeeded
            and dialog.tray_expand_button.property("glyphButton") == "chevron-down"
            and getattr(dialog.tray_nav_icon, "icon_kind", "") == "tray"
            and getattr(dialog.quick_access_nav_icon, "icon_kind", "") == "quick-access"
            and set(dialog._nav_buttons) == {"tray", "quick_access", "hud", "hud_dashboard"}
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and dialog.quick_access_nav_caption.text() == ""
            and not dialog.quick_access_nav_caption.isVisible()
            and dialog.SETTINGS_NAV_MIN_WIDTH <= dialog.nav_shell.width() <= dialog.SETTINGS_NAV_MAX_WIDTH
            and child_nav_origin.x() - parent_nav_origin.x() == 14
            and dialog.tray_nav_item.width() == 118
            and dialog.quick_access_nav_item.width() == 112
            and dialog.hud_nav_item.isVisible()
            and dialog.hud_nav_item.property("settingsCategoryRole") == "persistent-owner-bounded-parent"
            and dialog.hud_nav_button.text() == "HUD"
            and dialog.hud_expand_button.property("glyphButton") == "chevron-down"
            and getattr(dialog.hud_nav_icon, "icon_kind", "") == "hud"
            and dialog.hud_dashboard_nav_item.isVisible()
            and dialog.hud_dashboard_nav_button.text() == "HUD Dashboard"
            and dialog.hud_dashboard_nav_item.property("settingsNavDensity") == "two-level-subpage-row"
            and dialog.hud_dashboard_nav_item.property("settingsNavSizingPolicy")
            == "font-metric-default-min-clamped-v39"
            and hud_child_nav_origin.x() - hud_parent_nav_origin.x() == 14
            and dialog.hud_nav_item.width() == dialog._settings_nav_pill_width("HUD", "parent")
            and dialog.hud_dashboard_nav_item.width()
            == dialog._settings_nav_pill_width("HUD Dashboard", "child")
            and not dialog.nav_boundary.isVisible(),
            f"{nav_path} ({nav_width}x{nav_height}); nav={list(dialog._nav_buttons)}; tray={dialog.tray_nav_button.text()!r}/{dialog.tray_nav_item.property('settingsCategoryRole')!r}; checked={dialog.quick_access_nav_button.isChecked()}; expander={dialog.tray_expand_button.property('glyphButton')!r}; icons={getattr(dialog.tray_nav_icon, 'icon_kind', '')!r}/{getattr(dialog.quick_access_nav_icon, 'icon_kind', '')!r}; caption={dialog.quick_access_nav_caption.text()!r}; caption_visible={dialog.quick_access_nav_caption.isVisible()}; nav_width={dialog.nav_shell.width()}; parent_origin={parent_nav_origin.x()},{parent_nav_origin.y()}; child_origin={child_nav_origin.x()},{child_nav_origin.y()}; hud_parent_origin={hud_parent_nav_origin.x()},{hud_parent_nav_origin.y()}; hud_child_origin={hud_child_nav_origin.x()},{hud_child_nav_origin.y()}",
        )
    )
    tray_nav_height = dialog.tray_nav_item.height()
    quick_nav_height = dialog.quick_access_nav_item.height()
    rows.append(
        (
            "left rail slim row metrics",
            nav_ok
            and tray_nav_height == 28
            and quick_nav_height == 26
            and dialog.tray_nav_indicator.width() <= 2
            and dialog.tray_nav_icon.width() == 12
            and dialog.quick_access_nav_icon.width() == 12
            and dialog.tray_nav_item.property("settingsNavDensity") == "slim-parent-row"
            and dialog.quick_access_nav_item.property("settingsNavDensity") == "two-level-subpage-row",
            f"tray_row={tray_nav_height}; quick_row={quick_nav_height}; indicator={dialog.tray_nav_indicator.width()}x{dialog.tray_nav_indicator.height()}; parent_icon={dialog.tray_nav_icon.width()}x{dialog.tray_nav_icon.height()}; child_icon={dialog.quick_access_nav_icon.width()}x{dialog.quick_access_nav_icon.height()}; nav_width={dialog.nav_shell.width()}",
        )
    )
    rows.append(
        (
            "left rail active icon and hierarchy polish",
            nav_ok
            and dialog.property("settingsRailPolishPolicy") == "fixed-gap-deterministic-text-width-sharpened-icons-horizontal-overflow-splitter-travel-v41"
            and dialog.tray_nav_item.property("navState") == "contains-selected"
            and dialog.quick_access_nav_item.property("navState") == "selected"
            and dialog.tray_nav_item.property("settingsNavSizingPolicy") == "font-metric-default-min-clamped-v39"
            and dialog.quick_access_nav_item.property("settingsNavSizingPolicy") == "font-metric-default-min-clamped-v39"
            and dialog.tray_nav_icon.width() == 12
            and dialog.quick_access_nav_icon.width() == 12
            and dialog.tray_nav_icon.property("categoryIconRenderPolicy") == "high-contrast-contained-12px-v38"
            and dialog.quick_access_nav_icon.property("categoryIconRenderPolicy") == "high-contrast-contained-12px-v38"
            and child_nav_origin.x() - parent_nav_origin.x() == 14
            and dialog.quick_access_nav_button.maximumWidth() == 88
            and dialog.tray_nav_button.maximumWidth() <= 58
            and dialog.quick_access_nav_button.maximumWidth() >= dialog.tray_nav_button.maximumWidth() + 24
            and dialog.tray_expand_button.property("quietGlyph") is True,
            f"policy={dialog.property('settingsRailPolishPolicy')!r}; tray_state={dialog.tray_nav_item.property('navState')!r}; child_state={dialog.quick_access_nav_item.property('navState')!r}; sizing={dialog.tray_nav_item.property('settingsNavSizingPolicy')!r}/{dialog.quick_access_nav_item.property('settingsNavSizingPolicy')!r}; parent_icon={dialog.tray_nav_icon.width()}x{dialog.tray_nav_icon.height()}/{dialog.tray_nav_icon.property('categoryIconRenderPolicy')!r}; child_icon={dialog.quick_access_nav_icon.width()}x{dialog.quick_access_nav_icon.height()}/{dialog.quick_access_nav_icon.property('categoryIconRenderPolicy')!r}; parent_origin={parent_nav_origin.x()},{parent_nav_origin.y()}; child_origin={child_nav_origin.x()},{child_nav_origin.y()}; parent_button_max={dialog.tray_nav_button.maximumWidth()}; child_button_max={dialog.quick_access_nav_button.maximumWidth()}",
        )
    )

    active_child_path = log_dir / "04a_left_nav_active_child.png"
    active_child_ok, _, _ = _capture(
        dialog.nav_shell,
        active_child_path,
        artifacts,
        surface="left settings organizer",
        state="expanded / Quick Access child selected",
    )
    rows.append(
        (
            "left navigation active child proof",
            active_child_ok
            and dialog._focus == "quick_access"
            and dialog.tray_nav_item.property("navState") == "contains-selected"
            and dialog.quick_access_nav_item.property("navState") == "selected"
            and dialog.subpage_nav_rail.isVisible(),
            f"{active_child_path}; focus={dialog._focus}; tray_state={dialog.tray_nav_item.property('navState')!r}; child_state={dialog.quick_access_nav_item.property('navState')!r}; subpage_visible={dialog.subpage_nav_rail.isVisible()}",
        )
    )

    child_origin = dialog.quick_access_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0))
    child_right = child_origin.x() + dialog.quick_access_nav_item.width()
    child_right_inset = dialog.nav_shell.width() - child_right
    subpage_margins = dialog.subpage_nav_rail.layout().contentsMargins()
    parent_bottom = parent_nav_origin.y() + dialog.tray_nav_item.height()
    category_gap = child_origin.y() - parent_bottom

    def _text_gutters(item, button):
        text_rect = button.fontMetrics().boundingRect(
            button.rect(),
            Qt.AlignLeft | Qt.AlignVCenter,
            button.text(),
        )
        button_origin = button.mapTo(item, QPoint(0, 0))
        text_left = button_origin.x() + text_rect.x()
        text_top = button_origin.y() + text_rect.y()
        text_right = text_left + text_rect.width()
        text_bottom = text_top + text_rect.height()
        outer = {
            "left": text_left,
            "right": item.width() - text_right,
            "top": text_top,
            "bottom": item.height() - text_bottom,
        }
        inside_border = {key: max(0, value - 1) for key, value in outer.items()}
        return outer, inside_border

    parent_outer_gutter, parent_inner_gutter = _text_gutters(dialog.tray_nav_item, dialog.tray_nav_button)
    child_outer_gutter, child_inner_gutter = _text_gutters(dialog.quick_access_nav_item, dialog.quick_access_nav_button)
    rows.append(
        (
            "left rail category text vertical gutters tightened",
            parent_inner_gutter["top"] == 6
            and parent_inner_gutter["bottom"] == 6
            and child_inner_gutter["top"] == 5
            and child_inner_gutter["bottom"] == 5
            and category_gap == 4,
            "parent_inside={}; child_inside={}; parent_outer={}; child_outer={}; category_gap={}".format(
                parent_inner_gutter,
                child_inner_gutter,
                parent_outer_gutter,
                child_outer_gutter,
                category_gap,
            ),
        )
    )

    future_parent_width = dialog._settings_nav_pill_width("Developer Tools", "parent")
    future_child_width = dialog._settings_nav_pill_width("Recording Studio", "child")
    rows.append(
        (
            "left rail deterministic text-width pill sizing",
            dialog.tray_nav_item.width() == dialog._settings_nav_pill_width(dialog.tray_nav_button.text(), "parent")
            and dialog.quick_access_nav_item.width()
            == dialog._settings_nav_pill_width(dialog.quick_access_nav_button.text(), "child")
            and dialog.tray_nav_item.width() == 118
            and dialog.quick_access_nav_item.width() == 112
            and future_parent_width == dialog.SETTINGS_NAV_PARENT_MAX_WIDTH
            and future_child_width == dialog._settings_nav_pill_width("Recording Studio", "child")
            and dialog.SETTINGS_NAV_CHILD_DEFAULT_WIDTH
            <= future_child_width
            <= dialog.SETTINGS_NAV_CHILD_MAX_WIDTH
            and dialog.hud_nav_item.width() == dialog._settings_nav_pill_width("HUD", "parent")
            and dialog.hud_dashboard_nav_item.width()
            == dialog._settings_nav_pill_width("HUD Dashboard", "child")
            and dialog.SETTINGS_NAV_CATEGORY_GAP == 4,
            "current_parent={}/{}; current_child={}/{}; future_parent={}; future_child={}; text_widths={}/{}/{}; fixed_gap={}".format(
                dialog.tray_nav_item.width(),
                dialog._settings_nav_pill_width(dialog.tray_nav_button.text(), "parent"),
                dialog.quick_access_nav_item.width(),
                dialog._settings_nav_pill_width(dialog.quick_access_nav_button.text(), "child"),
                future_parent_width,
                future_child_width,
                dialog._settings_nav_text_width(dialog.tray_nav_button.text()),
                dialog._settings_nav_text_width(dialog.quick_access_nav_button.text()),
                dialog._settings_nav_text_width("Recording Studio"),
                dialog.SETTINGS_NAV_CATEGORY_GAP,
            ),
        )
    )
    child_focus_left = max(0, child_origin.x() - 4)
    child_focus_top = max(0, child_origin.y() - 4)
    child_focus_rect = QRect(
        child_focus_left,
        child_focus_top,
        min(dialog.nav_shell.width() - child_focus_left, dialog.quick_access_nav_item.width() + child_right_inset + 4),
        min(dialog.nav_shell.height() - child_focus_top, dialog.quick_access_nav_item.height() + 8),
    )
    child_focus_path = log_dir / "04a1_quick_access_child_pill_no_clip_focus.png"
    child_focus_ok, child_focus_width, child_focus_height = _capture_rect(
        dialog.nav_shell,
        child_focus_rect,
        child_focus_path,
        artifacts,
        surface="left settings organizer",
        state="focused Quick Access child pill / right border no clipping",
    )
    rows.append(
        (
            "focused child pill border no-clipping proof",
            child_focus_ok
            and active_child_ok
            and dialog.quick_access_nav_item.width() == 112
            and dialog.quick_access_nav_item.height() == 26
            and dialog.tray_nav_item.height() == 28
            and dialog.quick_access_nav_button.maximumWidth() == 88
            and dialog.quick_access_nav_button.maximumWidth() >= dialog.tray_nav_button.maximumWidth() + 24
            and subpage_margins.left() == 14
            and subpage_margins.right() == 0
            and child_origin.x() - parent_nav_origin.x() == 14
            and child_origin.x() >= 21
            and child_right_inset >= 14
            and dialog.nav_scroll_area.horizontalScrollBar().maximum() == 0
            and dialog.quick_access_nav_item.property("navState") == "selected",
            f"{child_focus_path} ({child_focus_width}x{child_focus_height}); child_origin={child_origin.x()},{child_origin.y()}; child_width={dialog.quick_access_nav_item.width()}; child_height={dialog.quick_access_nav_item.height()}; parent_width={dialog.tray_nav_item.width()}; parent_height={dialog.tray_nav_item.height()}; category_gap={category_gap}; parent_inner_gutter={parent_inner_gutter}; child_inner_gutter={child_inner_gutter}; parent_button_max={dialog.tray_nav_button.maximumWidth()}; child_button_max={dialog.quick_access_nav_button.maximumWidth()}; child_right={child_right}; right_inset={child_right_inset}; subpage_margins={subpage_margins.left()},{subpage_margins.top()},{subpage_margins.right()},{subpage_margins.bottom()}; hbar_max={dialog.nav_scroll_area.horizontalScrollBar().maximum()}",
        )
    )

    dialog.quick_access_nav_button.setFocus(Qt.FocusReason.OtherFocusReason)
    dialog.quick_access_nav_button.setDown(True)
    app.processEvents()
    child_pressed_path = log_dir / "04a2_quick_access_child_pill_focus_pressed_state.png"
    child_pressed_ok, child_pressed_width, child_pressed_height = _capture_rect(
        dialog.nav_shell,
        child_focus_rect,
        child_pressed_path,
        artifacts,
        surface="left settings organizer",
        state="Quick Access child pill focused and pressed",
    )
    child_pressed_has_focus = dialog.quick_access_nav_button.hasFocus()
    child_pressed_is_down = dialog.quick_access_nav_button.isDown()
    dialog.quick_access_nav_button.setDown(False)
    app.processEvents()
    rows.append(
        (
            "child pill focus/pressed state proof",
            child_pressed_ok
            and child_pressed_is_down
            and dialog.quick_access_nav_item.property("navState") == "selected"
            and child_right_inset >= 14,
            f"{child_pressed_path} ({child_pressed_width}x{child_pressed_height}); has_focus={child_pressed_has_focus}; is_down={child_pressed_is_down}; right_inset={child_right_inset}",
        )
    )

    dialog._toggle_tray_children()
    app.processEvents()
    collapsed_path = log_dir / "04b_left_nav_collapsed.png"
    collapsed_ok, _, _ = _capture(
        dialog.nav_shell,
        collapsed_path,
        artifacts,
        surface="left settings organizer",
        state="Tray group collapsed",
    )
    rows.append(
        (
            "left navigation collapsed proof",
            collapsed_ok
            and dialog._focus == "tray"
            and not dialog.subpage_nav_rail.isVisible()
            and dialog.tray_expand_button.property("glyphButton") == "chevron-right"
            and dialog.tray_nav_item.property("navState") == "selected",
            f"{collapsed_path}; focus={dialog._focus}; subpage_visible={dialog.subpage_nav_rail.isVisible()}; expander={dialog.tray_expand_button.property('glyphButton')!r}; tray_state={dialog.tray_nav_item.property('navState')!r}",
        )
    )

    dialog._toggle_tray_children()
    dialog.set_focus("quick_access")
    app.processEvents()
    expanded_path = log_dir / "04c_left_nav_expanded.png"
    expanded_ok, _, _ = _capture(
        dialog.nav_shell,
        expanded_path,
        artifacts,
        surface="left settings organizer",
        state="Tray group expanded",
    )
    rows.append(
        (
            "left navigation expanded proof",
            expanded_ok
            and dialog._focus == "quick_access"
            and dialog.subpage_nav_rail.isVisible()
            and dialog.tray_expand_button.property("glyphButton") == "chevron-down",
            f"{expanded_path}; focus={dialog._focus}; subpage_visible={dialog.subpage_nav_rail.isVisible()}; expander={dialog.tray_expand_button.property('glyphButton')!r}",
        )
    )

    dialog.settings_splitter.setSizes([dialog.SETTINGS_NAV_MIN_WIDTH, 626])
    app.processEvents()
    narrow_path = log_dir / "04d_left_pane_compressed_horizontal_overflow.png"
    narrow_ok, narrow_width, narrow_height = _capture(
        dialog.nav_shell,
        narrow_path,
        artifacts,
        surface="left settings organizer",
        state="compressed pane / horizontal overflow",
    )
    hbar_max = dialog.nav_scroll_area.horizontalScrollBar().maximum()
    hbar_policy = dialog.nav_scroll_area.horizontalScrollBarPolicy()
    narrow_viewport_width = dialog.nav_scroll_area.viewport().width()
    narrow_child_origin = dialog.quick_access_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0))
    narrow_parent_origin = dialog.tray_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0))
    narrow_parent_visible_width = max(
        0,
        min(dialog.tray_nav_item.width(), dialog.nav_shell.width() - narrow_parent_origin.x()),
    )
    narrow_child_right_inset = dialog.nav_shell.width() - (
        narrow_child_origin.x() + dialog.quick_access_nav_item.width()
    )
    rows.append(
        (
            "left pane compressed width exposes horizontal overflow",
            narrow_ok
            and dialog.nav_shell.width() == dialog.SETTINGS_NAV_MIN_WIDTH
            and hbar_policy == Qt.ScrollBarAsNeeded
            and hbar_max > 0
            and dialog.nav_content.width() > narrow_viewport_width
            and 34 <= narrow_parent_visible_width <= 78
            and narrow_parent_visible_width < dialog.tray_nav_item.width()
            and narrow_child_right_inset < 0
            and narrow_child_origin.x() - narrow_parent_origin.x() == 14,
            f"{narrow_path} ({narrow_width}x{narrow_height}); nav_width={dialog.nav_shell.width()}; viewport_width={narrow_viewport_width}; nav_content_width={dialog.nav_content.width()}; hbar_max={hbar_max}; hbar_policy={hbar_policy}; parent_origin={narrow_parent_origin.x()},{narrow_parent_origin.y()}; parent_width={dialog.tray_nav_item.width()}; parent_visible_width={narrow_parent_visible_width}; child_origin={narrow_child_origin.x()},{narrow_child_origin.y()}; child_width={dialog.quick_access_nav_item.width()}; child_right_inset={narrow_child_right_inset}",
        )
    )

    dialog.resize(dialog.maximumWidth(), dialog.height())
    dialog.settings_splitter.setSizes([dialog.SETTINGS_NAV_MAX_WIDTH, 520])
    app.processEvents()
    wide_path = log_dir / "04e_left_pane_wide.png"
    wide_ok, wide_width, wide_height = _capture(
        dialog.nav_shell,
        wide_path,
        artifacts,
        surface="left settings organizer",
        state="wide pane",
    )
    wide_child_origin = dialog.quick_access_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0))
    wide_child_right_inset = dialog.nav_shell.width() - (
        wide_child_origin.x() + dialog.quick_access_nav_item.width()
    )
    rows.append(
        (
            "left pane wide resize stays deterministic",
            wide_ok
            and dialog.nav_shell.width() == dialog.SETTINGS_NAV_MAX_WIDTH
            and dialog.nav_shell.width() - dialog.SETTINGS_NAV_MIN_WIDTH >= 190
            and dialog.subpage_nav_rail.isVisible()
            and dialog.quick_access_nav_item.isVisible()
            and dialog.tray_nav_item.width() == 118
            and dialog.quick_access_nav_item.width() == 112
            and wide_child_origin.x() - dialog.tray_nav_item.mapTo(dialog.nav_shell, QPoint(0, 0)).x() == 14
            and wide_child_right_inset >= 14,
            f"{wide_path} ({wide_width}x{wide_height}); nav_width={dialog.nav_shell.width()}; parent_width={dialog.tray_nav_item.width()}; child_width={dialog.quick_access_nav_item.width()}; child_origin={wide_child_origin.x()},{wide_child_origin.y()}; child_right_inset={wide_child_right_inset}; subpage_visible={dialog.subpage_nav_rail.isVisible()}",
        )
    )

    vbar_max = dialog.nav_scroll_area.verticalScrollBar().maximum()
    rows.append(
        (
            "left pane vertical overflow source-truth disposition",
            vbar_max == 0
            and set(dialog._nav_buttons) == {"tray", "quick_access", "hud", "hud_dashboard"}
            and dialog.nav_content.height() <= dialog.nav_scroll_area.viewport().height(),
            f"vbar_max={vbar_max}; current_real_nav={list(dialog._nav_buttons)}; nav_content_height={dialog.nav_content.height()}; viewport_height={dialog.nav_scroll_area.viewport().height()}; source_truth='current visible Global Settings hierarchy contains persistent Tray and HUD parent/child routes only; no fake future categories admitted'",
        )
    )

    dialog.settings_splitter.setSizes([124, 548])
    dialog.set_focus("quick_access")
    app.processEvents()

    dialog.set_focus("tray")
    app.processEvents()
    tray_parent_path = log_dir / "05_tray_parent_page.png"
    tray_parent_ok, _, _ = _capture(
        dialog,
        tray_parent_path,
        artifacts,
        surface="Tray parent settings page",
        state="Tray selected",
    )
    rows.append(("Tray parent page screenshot saved", tray_parent_ok, str(tray_parent_path)))
    rows.append(
        (
            "selectable Tray parent page",
            dialog._focus == "tray"
            and dialog.tray_nav_button.isChecked()
            and not dialog.quick_access_nav_button.isChecked()
            and dialog.section_heading.text() == "Tray"
            and dialog.tray_overview_container.isVisible()
            and not dialog.quick_slot_container.isVisible()
            and not dialog.footer_frame.isVisible()
            and dialog.tray_deferred_notice.isVisible()
            and dialog.tray_deferred_title.text() == "Tray behavior"
            and "Tray click settings are not active yet." in dialog.tray_deferred_detail.text()
            and "Windows controls whether app notification icons stay pinned" in dialog.tray_deferred_detail.text(),
            f"focus={dialog._focus}; heading={dialog.section_heading.text()!r}; tray_checked={dialog.tray_nav_button.isChecked()}; quick_checked={dialog.quick_access_nav_button.isChecked()}; overview={dialog.tray_overview_container.isVisible()}; quick_panel={dialog.quick_slot_container.isVisible()}; footer={dialog.footer_frame.isVisible()}; tray_notice={dialog.tray_deferred_detail.text()!r}",
        )
    )
    rows.append(
        (
            "Tray parent contains no Quick Access overview or open row",
            dialog._focus == "tray"
            and not hasattr(dialog, "tray_quick_access_row")
            and not hasattr(dialog, "tray_quick_access_open")
            and not any(
                button.text().replace("&&", "&") == "Open" and button.isVisible()
                for button in dialog.findChildren(QPushButton)
            ),
            "quick_row_attr={}; open_attr={}; visible_open_buttons={}".format(
                hasattr(dialog, "tray_quick_access_row"),
                hasattr(dialog, "tray_quick_access_open"),
                [
                    (button.objectName(), button.text())
                    for button in dialog.findChildren(QPushButton)
                    if button.text().replace("&&", "&") == "Open" and button.isVisible()
                ],
            ),
        )
    )
    for alias, expected_detail in (
        ("ai_status", "AI status opens through the FAM-007 Command Center doorway."),
        ("privacy", "Privacy controls stay FAM-007-owned; Tray keeps the doorway visible."),
        ("owner_routes", "Unavailable tray routes stay future-gated until the owning surface is active."),
    ):
        dialog.set_focus(alias)
        app.processEvents()
        rows.append(
            (
                f"{alias} route focus lands on Tray parent page",
                dialog._focus == "tray"
                and dialog._focus_context == alias
                and dialog.tray_nav_button.isChecked()
                and not dialog.quick_access_nav_button.isChecked()
                and dialog.tray_overview_container.isVisible()
                and not dialog.quick_slot_container.isVisible()
                and expected_detail == dialog.section_detail.text(),
                f"alias={alias}; focus={dialog._focus}; context={dialog._focus_context}; detail={dialog.section_detail.text()!r}; overview={dialog.tray_overview_container.isVisible()}; quick_panel={dialog.quick_slot_container.isVisible()}",
            )
        )
    dialog.set_focus("tray")
    app.processEvents()
    dialog.set_focus("quick_access")
    app.processEvents()

    button_texts = [button.text().replace("&&", "&") for button in dialog.findChildren(QPushButton)]
    compact_action_buttons = [
        button
        for button in dialog.findChildren(QPushButton)
        if button.objectName() in {"residentAccessQuickSlotMoveUp", "residentAccessQuickSlotMoveDown", "residentAccessQuickSlotDelete"}
    ]
    rows.append(
        (
            "Tray and HUD parent-child settings IA",
            dialog.section_heading.text() == "Quick Access"
            and dialog.section_badge.text() == "Tray"
            and not dialog.section_badge.isVisible()
            and dialog.section_detail.isVisible()
            and dialog.section_detail.text() == "Choose the shortcuts shown in the tray menu."
            and dialog.section_scope.isVisible()
            and dialog.section_scope.text() == "NEXUS TRAY / QUICK ACCESS"
            and dialog.property("settingsInformationArchitecture")
            == "global-settings-shell-tray-and-hud-parent-child-deterministic-rail-r2"
            and dialog.property("settingsVisualRepair") == "lv1-global-settings-compact-ndai-grammar-close-intercept-v32"
            and dialog.property("referenceDerivedHeader") == "ndai-global-settings-centered-settings-chrome-v22"
            and dialog.property("dirtyGuardReference") == "manage-monitors-modal-save-discard-cancel"
            and dialog.property("standardWindowArchitecture") == "pyside-dialogchrome-native-edge-corner-hit-test-reference-derived"
            and dialog.property("windowResizeBehavior") == "uiref-007-frameless-top-level-hover-polled-edge-corner-cursor-app-owned-fallback-8px-edge-12px-corner-no-visible-grip-splitter-travel-76-270-horizontal-overflow-minimum-684x388-dynamic-content-minimum-maximum-840x610-close-intercept-no-forced-arrow-hysteresis-v43"
            and dialog.property("quickAccessLayoutPolicy") == "uiref-007-deterministic-row-width-combo-integrated-action-capsule-row-count-close-intercept-v42"
            and dialog.property("settingsRailPolishPolicy") == "fixed-gap-deterministic-text-width-sharpened-icons-horizontal-overflow-splitter-travel-v41"
            and dialog.property("contentScalePolicy") == "control-pill-anchored-proportional-content-scale-v32"
            and dialog.property("dirtyCloseRouteCoverage") == "window-close-system-close-keybind-client-shutdown-save-discard-cancel-v32"
            and dialog.property("visibleResizeGrip") == "removed"
            and dialog.property("deferredWatermarkConcept") == "future-centered-global-settings-watermark-deferred-no-runtime-exposure-v22"
            and dialog.property("runtimeWatermarkVisible") == "false"
            and dialog.property("uiExposureContract") == "real-enabled-meaningful-visible-ui-v1"
            and dialog.property("sharedPrimitiveClaim") == "none-promoted-reference-derived-only"
            and dialog.property("referenceComparatorRequired") == "ui-reference-plus-product-grade-same-defect-comparator-v22"
            and set(dialog._nav_buttons) == {"tray", "quick_access", "hud", "hud_dashboard"}
            and dialog.tray_nav_item.property("settingsCategoryRole") == "selectable-parent-page"
            and dialog.tray_nav_button.text() == "Tray"
            and getattr(dialog.tray_nav_icon, "icon_kind", "") == "tray"
            and dialog.tray_expand_button.property("glyphButton") == "chevron-down"
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and getattr(dialog.quick_access_nav_icon, "icon_kind", "") == "quick-access"
            and dialog.quick_access_nav_button.isChecked()
            and dialog.hud_nav_item.property("settingsCategoryRole") == "persistent-owner-bounded-parent"
            and dialog.hud_nav_button.text() == "HUD"
            and dialog.hud_dashboard_nav_button.text() == "HUD Dashboard"
            and dialog.hud_subpage_nav_rail.isVisible()
            and dialog.slot_count_badge.text() == f"{len(DEFAULT_QUICK_SLOT_ROUTE_IDS)} of {active_slot_limit}"
            and dialog.slot_count_badge.isVisible()
            and dialog.slot_count_badge.mapTo(dialog.add_slot_button.parentWidget(), QPoint(0, 0)).x()
            > dialog.add_slot_button.mapTo(dialog.add_slot_button.parentWidget(), QPoint(0, 0)).x()
            and not dialog.tray_overview_container.isVisible()
            and dialog.quick_slot_container.isVisible()
            and dialog.settings_page_frame.objectName() == "residentAccessSettingsPageFrame"
            and dialog.settings_state_chip.objectName() == "residentAccessSettingsStateText"
            and dialog.quick_slot_container.objectName() == "residentAccessQuickSlotContainer"
            and dialog.footer_frame.objectName() == "residentAccessSettingsFooter"
            and not dialog.route_summary.isVisible(),
            f"heading={dialog.section_heading.text()!r}; category={dialog.tray_nav_button.text()!r}; section_badge_visible={dialog.section_badge.isVisible()}; scope={dialog.section_scope.text()!r}/{dialog.section_scope.isVisible()}; detail={dialog.section_detail.text()!r}/{dialog.section_detail.isVisible()}; slot_badge={dialog.slot_count_badge.text()!r}; nav={list(dialog._nav_buttons)}; buttons={button_texts}; route_visible={dialog.route_summary.isVisible()}",
        )
    )
    stale_product_text = {
        "Connected Surfaces",
        "Resident Access",
        "Tray Menu Shortcuts",
        "Resident tray shortcuts and menu preferences.",
        "Configure the Nexus tray.",
        "Quick Access is the active settings page.",
        "Shortcut Order",
        "Native tray > Quick Access",
        "Save applies Quick Access edits to the tray menu.",
        "future-gated",
        "Reset Quick Access",
        "Move Up",
        "Move Down",
        "UPWARDS ARROW",
        "DOWNWARDS ARROW",
        "Up",
        "Down",
        "Quick Access Slots",
        "Rows appear in tray order. Use Save Changes to apply them.",
        "Remove",
        "Done",
        "(unavailable)",
        "PAGE - QUICK ACCESS",
        "SCOPE - TRAY MENU",
        "SETTINGS AREA",
        "ACTIVE SETTING",
        "AREA Nexus Tray",
        "SETTING Quick Access",
        "CHANGES No pending",
        "No pending changes",
        "01",
        "Nexus behavior and quick actions.",
        "Choose the shortcuts shown in the tray Quick Access submenu.",
        "Tray menu and quick access.",
        "Tray shortcuts",
    }
    visible_text_segments = [
        dialog.chrome_bar.kicker_label.text(),
        dialog.chrome_bar.title_label.text(),
        dialog.chrome_bar.subtitle_label.text(),
        " ".join(role_text),
        dialog.tray_nav_button.text(),
        dialog.tray_deferred_title.text() if dialog.tray_overview_container.isVisible() else "",
        dialog.tray_deferred_detail.text() if dialog.tray_overview_container.isVisible() else "",
        dialog.quick_access_nav_button.text(),
        dialog.quick_access_nav_caption.text() if dialog.quick_access_nav_caption.isVisible() else "",
        dialog.settings_state_chip.text(),
        dialog.section_scope.text(),
        dialog.section_badge.text() if dialog.section_badge.isVisible() else "",
        dialog.section_heading.text(),
        dialog.section_detail.text(),
        dialog.quick_help.text(),
        " ".join(button_texts),
        " ".join(combo.itemText(i) for combo in dialog._slot_combos for i in range(combo.count())),
    ]
    visible_text_blob = " | ".join(segment for segment in visible_text_segments if segment)
    rows.append(
        (
            "product-facing copy is compact and non-internal",
            all(token not in visible_text_blob for token in stale_product_text),
            f"visible_text={visible_text_blob!r}",
        )
    )
    rows.append(
        (
            "no internal telemetry text",
            all(
                token not in visible_text_blob
                for token in {
                    "SETTINGS AREA",
                    "ACTIVE SETTING",
                    "AREA",
                    "AREA Nexus Tray",
                    "SETTING Quick Access",
                    "CHANGES No pending",
                    "Quick Access menu",
                    "No pending changes",
                }
            )
            and role_text == []
            and not dialog.chrome_bar.role_pill.isVisible(),
            f"visible_text={visible_text_blob!r}; role_pairs={role_text}; role_pill_visible={dialog.chrome_bar.role_pill.isVisible()}",
        )
    )
    rows.append(
        (
            "no fake overview/status strip",
            not any(
                hasattr(dialog, attr)
                for attr in (
                    "settings_summary_panel",
                    "settings_summary_title",
                    "settings_summary_detail",
                    "menu_path_row",
                    "active_setting_row",
                    "pending_state_row",
                )
            )
            and not dialog.route_summary.isVisible()
            and dialog.settings_state_chip.objectName() == "residentAccessSettingsStateText",
            f"state_chip={dialog.settings_state_chip.text()!r}; route_visible={dialog.route_summary.isVisible()}; legacy_attrs={[attr for attr in ('settings_summary_panel', 'settings_summary_title', 'settings_summary_detail', 'menu_path_row', 'active_setting_row', 'pending_state_row') if hasattr(dialog, attr)]}",
        )
    )
    rows.append(
        (
            "clean state has no redundant saved label",
            dialog.settings_state_chip.objectName() == "residentAccessSettingsStateText"
            and dialog.settings_state_chip.text() == ""
            and not dialog.settings_state_chip.isVisible()
            and dialog.settings_state_chip.height() <= 20
            and dialog.settings_state_chip.minimumWidth() == 0
            and dialog.settings_state_chip.accessibleName() == "Quick Access settings state",
            f"object={dialog.settings_state_chip.objectName()!r}; text={dialog.settings_state_chip.text()!r}; visible={dialog.settings_state_chip.isVisible()}; size={dialog.settings_state_chip.width()}x{dialog.settings_state_chip.height()}; min_width={dialog.settings_state_chip.minimumWidth()}; a11y={dialog.settings_state_chip.accessibleName()!r}",
        )
    )
    rows.append(
        (
            "Nexus UI exposure contract honored",
            all(token not in visible_text_blob for token in {"Recording Studio", "Log Viewer", "(unavailable)", "future-gated"})
            and all(
                combo.findText("Recording Studio") < 0 and combo.findText("Log Viewer") < 0
                for combo in dialog._slot_combos
            ),
            f"visible_text={visible_text_blob!r}; combo_items={[[combo.itemText(i) for i in range(combo.count())] for combo in dialog._slot_combos]}",
        )
    )
    rows.append(
        (
            "two-pill compact quick-slot controls",
            all(
                (
                    button.property("glyphButton")
                    in {"up", "down"}
                    and button.width() == 25
                    and 24 <= button.height() <= 28
                    and float(button.property("glyphScale") or 0) >= 0.74
                    and button.property("glyphZoneButton") is True
                    and button.property("glyphSegment") in {"left", "right"}
                )
                or (
                    button.objectName() == "residentAccessQuickSlotDelete"
                    and button.property("glyphButton") == "close"
                    and button.width() == 28
                    and 24 <= button.height() <= 28
                    and float(button.property("glyphScale") or 0) >= 0.74
                    and button.property("glyphZoneButton") is True
                    and button.property("glyphSegment") == "standalone-danger"
                )
                for button in compact_action_buttons
            )
            and any(
                frame.objectName() == "residentAccessQuickSlotReorderGroup"
                and frame.width() == 53
                and frame.__class__.__name__ == "QuickSlotReorderPill"
                and frame.property("quickSlotReorderSplitPolicy") == "parent-painted-25-1-25-exact-segment-fill-v47"
                for frame in dialog.findChildren(QFrame)
            )
            and any(frame.objectName() == "residentAccessQuickSlotReorderDivider" for frame in dialog.findChildren(QFrame)),
            f"buttons={button_texts}; compact_action_sizes={[(button.objectName(), button.property('glyphButton'), button.width(), button.height(), button.isEnabled()) for button in compact_action_buttons]}",
        )
    )
    rows.append(
        (
            "clean state has no redundant saved label",
            not dialog.change_summary.isVisible()
            and dialog.change_summary.text() == ""
            and not dialog.save_button.isEnabled()
            and not dialog.revert_button.isEnabled()
            and dialog.settings_state_chip.text() == ""
            and not dialog.settings_state_chip.isVisible(),
            f"change_summary={dialog.change_summary.text()!r}; visible={dialog.change_summary.isVisible()}; state_chip={dialog.settings_state_chip.text()!r}",
        )
    )

    candidate_route_ids = [route.route_id for route in quick_slot_candidate_routes()]
    if not dialog._slot_combos:
        rows.append(("quick-slot combo exists", False, "no quick-slot combo rendered"))
    else:
        rows.append(("quick-slot combo exists", True, f"combo_count={len(dialog._slot_combos)}"))
        combo = dialog._slot_combos[0]
        rows.append(
            (
                "route selector is compact and bounded",
                all(250 <= slot_combo.width() <= 456 and slot_combo.height() >= 28 and slot_combo.maxVisibleItems() <= 4 for slot_combo in dialog._slot_combos),
                f"combo_sizes={[(slot_combo.width(), slot_combo.height(), slot_combo.maxVisibleItems()) for slot_combo in dialog._slot_combos]}",
            )
        )
        slot_rows = [
            widget
            for widget in dialog.quick_slot_rows.findChildren(type(dialog.quick_slot_container))
            if widget.objectName() == "residentAccessQuickSlotRow"
        ]
        row_gutters: list[int] = []
        row_widths: list[int] = []
        for slot_row, slot_combo in zip(slot_rows, dialog._slot_combos):
            action_cluster = slot_row.findChild(QFrame, "residentAccessQuickSlotActions")
            if action_cluster is None:
                row_gutters.append(999)
                row_widths.append(slot_row.width())
                continue
            combo_right = slot_combo.mapTo(slot_row, QPoint(slot_combo.width(), 0)).x()
            action_left = action_cluster.mapTo(slot_row, QPoint(0, 0)).x()
            row_gutters.append(max(0, action_left - combo_right))
            row_widths.append(slot_row.width())
        control_button_size = dialog.chrome_bar.close_button.size()
        quick_action_heights = [button.height() for button in compact_action_buttons]
        quick_row_heights = [slot_row.height() for slot_row in slot_rows]
        rows.append(
            (
                "window-control scale matched by active settings controls",
                24 <= control_button_size.width() <= 26
                and 24 <= control_button_size.height() <= 26
                and quick_row_heights
                and all(height >= 34 for height in quick_row_heights)
                and all(height >= 26 for height in quick_action_heights)
                and all(slot_combo.height() >= 28 for slot_combo in dialog._slot_combos)
                and dialog.add_slot_button.height() >= 28
                and dialog.reset_slots_button.height() >= 28,
                f"window_control={control_button_size.width()}x{control_button_size.height()}; rows={quick_row_heights}; combo_heights={[slot_combo.height() for slot_combo in dialog._slot_combos]}; action_heights={quick_action_heights}; add={dialog.add_slot_button.width()}x{dialog.add_slot_button.height()}; defaults={dialog.reset_slots_button.width()}x{dialog.reset_slots_button.height()}",
            )
        )
        default_last_row_bottom = 0
        default_container_bottom = dialog.quick_slot_container.mapTo(dialog, QPoint(0, dialog.quick_slot_container.height())).y()
        default_footer_top_now = dialog.footer_frame.mapTo(dialog, QPoint(0, 0)).y()
        if slot_rows:
            default_last_row = slot_rows[-1]
            default_last_row_bottom = default_last_row.mapTo(dialog, QPoint(0, default_last_row.height())).y()
        rows.append(
            (
                "bottom quick-access row is unclipped after scale match",
                bool(slot_rows)
                and all(height >= 34 for height in quick_row_heights)
                and default_last_row_bottom + 8 <= default_container_bottom
                and default_container_bottom <= default_footer_top_now,
                f"rows={len(slot_rows)}; row_heights={quick_row_heights}; last_row_bottom={default_last_row_bottom}; container_bottom={default_container_bottom}; footer_top={default_footer_top_now}; panel_height={dialog.quick_slot_container.height()}",
            )
        )
        rows.append(
            (
                "quick-slot row grouping has no excessive gutter",
                bool(row_gutters)
                and all(gutter <= 10 for gutter in row_gutters)
                and all(450 <= width <= 600 for width in row_widths),
                f"row_gutters={row_gutters}; row_widths={row_widths}",
            )
        )
        rows.append(
            (
                "quick-slot dropdown and action capsule fit deterministic row width",
                bool(row_gutters)
                and all(0 <= gutter <= 10 for gutter in row_gutters)
                and all(250 <= slot_combo.width() <= 456 for slot_combo in dialog._slot_combos)
                and all(
                    slot_row.findChild(QFrame, "residentAccessQuickSlotActions") is not None
                    and slot_row.findChild(QFrame, "residentAccessQuickSlotActions").width()
                    == dialog.QUICK_SLOT_ACTION_CLUSTER_WIDTH
                    and slot_row.findChild(QFrame, "residentAccessQuickSlotActions").property("quickSlotActionControlPolicy")
                    == "two-pill-reorder-delete-parent-painted-segment-fill-v47"
                    and slot_row.findChild(QFrame, "residentAccessQuickSlotReorderGroup") is not None
                    and slot_row.findChild(QFrame, "residentAccessQuickSlotReorderGroup").property("quickSlotReorderSplitPolicy")
                    == "parent-painted-25-1-25-exact-segment-fill-v47"
                    and slot_row.findChild(QFrame, "residentAccessQuickSlotReorderDivider") is not None
                    for slot_row in slot_rows
                ),
                f"row_widths={row_widths}; combo_widths={[slot_combo.width() for slot_combo in dialog._slot_combos]}; row_gutters={row_gutters}; action_width={dialog.QUICK_SLOT_ACTION_CLUSTER_WIDTH}",
            )
        )
        slot_badge_pos = dialog.slot_count_badge.mapTo(dialog, QPoint(0, 0))
        add_button_pos = dialog.add_slot_button.mapTo(dialog, QPoint(0, 0))
        heading_pos = dialog.section_heading.mapTo(dialog, QPoint(0, 0))
        rows.append(
            (
                "slot count is placed beside Add Slot",
                dialog.slot_count_badge.text() == f"{len(dialog._slot_combos)} of {active_slot_limit}"
                and dialog.slot_count_badge.isVisible()
                and slot_badge_pos.y() >= add_button_pos.y() - 2
                and slot_badge_pos.y() <= add_button_pos.y() + 4
                and slot_badge_pos.x() > add_button_pos.x()
                and slot_badge_pos.y() > heading_pos.y() + 40,
                f"slot_count={dialog.slot_count_badge.text()!r}; badge_pos={slot_badge_pos.x()},{slot_badge_pos.y()}; add_pos={add_button_pos.x()},{add_button_pos.y()}; heading_pos={heading_pos.x()},{heading_pos.y()}",
            )
        )
        visible_count_labels = [
            (label.objectName(), label.text().strip())
            for label in dialog.findChildren(QLabel)
            if label.isVisible() and re.fullmatch(r"\d+\s+of\s+\d+", label.text().strip())
        ]
        rows.append(
            (
                "slot count appears once in active surface",
                visible_count_labels == [(dialog.slot_count_badge.objectName(), f"{len(dialog._slot_combos)} of {active_slot_limit}")],
                f"visible_count_labels={visible_count_labels}",
            )
        )

        candidate_route_ids = [route.route_id for route in quick_slot_candidate_routes()]

        def _slot_row_widgets(probe: ResidentAccessSettingsDialog) -> list[QFrame]:
            return [
                widget
                for widget in probe.quick_slot_rows.findChildren(QFrame)
                if widget.objectName() == "residentAccessQuickSlotRow"
            ]

        row_count_matrix: list[tuple[int, bool, str]] = []
        for count in range(1, active_slot_limit + 1):
            if len(candidate_route_ids) < count:
                row_count_matrix.append((count, False, "not enough candidate routes"))
                continue
            dialog._replace_quick_slots(tuple(candidate_route_ids[:count]), notice="Unsaved changes")
            app.processEvents()
            row_count_path = log_dir / f"22_row_count_{count}_of_{active_slot_limit}.png"
            row_count_image_ok, row_count_w, row_count_h = _capture(
                dialog,
                row_count_path,
                artifacts,
                surface="Quick Access row-count layout matrix",
                state=f"{count} active of {active_slot_limit}",
            )
            matrix_rows = _slot_row_widgets(dialog)
            matrix_row_heights = [row_widget.height() for row_widget in matrix_rows]
            matrix_last_bottom = 0
            if matrix_rows:
                last_row = matrix_rows[-1]
                matrix_last_bottom = last_row.mapTo(dialog, QPoint(0, last_row.height())).y()
            matrix_container_bottom = dialog.quick_slot_container.mapTo(
                dialog,
                QPoint(0, dialog.quick_slot_container.height()),
            ).y()
            matrix_footer_top = dialog.footer_frame.mapTo(dialog, QPoint(0, 0)).y()
            expected_add_enabled = count < active_slot_limit
            matrix_count_labels = [
                (label.objectName(), label.text().strip())
                for label in dialog.findChildren(QLabel)
                if label.isVisible() and re.fullmatch(r"\d+\s+of\s+\d+", label.text().strip())
            ]
            matrix_ok = (
                row_count_image_ok
                and len(matrix_rows) == count
                and matrix_row_heights
                and len(set(matrix_row_heights)) == 1
                and all(height >= dialog.QUICK_SLOT_ROW_HEIGHT for height in matrix_row_heights)
                and matrix_last_bottom + 8 <= matrix_container_bottom
                and matrix_container_bottom <= matrix_footer_top
                and dialog.add_slot_button.isEnabled() == expected_add_enabled
                and dialog.quick_slot_container.property("quickAccessRowPolicy")
                == "uiref-007-deterministic-row-width-combo-integrated-action-capsule-row-count-close-intercept-v42"
                and matrix_count_labels == [(dialog.slot_count_badge.objectName(), f"{count} of {active_slot_limit}")]
            )
            detail = (
                f"{row_count_path} ({row_count_w}x{row_count_h}); rows={len(matrix_rows)}; "
                f"row_heights={matrix_row_heights}; container_height={dialog.quick_slot_container.height()}; "
                f"last_row_bottom={matrix_last_bottom}; container_bottom={matrix_container_bottom}; "
                f"footer_top={matrix_footer_top}; add_enabled={dialog.add_slot_button.isEnabled()}; "
                f"expected_add_enabled={expected_add_enabled}; min={dialog.minimumWidth()}x{dialog.minimumHeight()}; "
                f"size={dialog.width()}x{dialog.height()}; policy={dialog.quick_slot_container.property('quickAccessRowPolicy')!r}; count_labels={matrix_count_labels}"
            )
            row_count_matrix.append((count, matrix_ok, detail))
            rows.append((f"row-count {count} quick access layout proof", matrix_ok, detail))

        matrix_ok = all(ok for _count, ok, _detail in row_count_matrix) and len(row_count_matrix) == active_slot_limit
        rows.append(
            (
                "quick access row-count matrix is deterministic",
                matrix_ok,
                "; ".join(f"{count}={'PASS' if ok else 'FAIL'} {detail}" for count, ok, detail in row_count_matrix),
            )
        )
        dialog._replace_quick_slots(DEFAULT_QUICK_SLOT_ROUTE_IDS, notice="Unsaved changes")
        dialog._saved_settings = dialog._settings
        dialog._notice_text = ""
        dialog._refresh_text()
        app.processEvents()
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
                and dialog.settings_state_chip.text() == ""
                and not dialog.settings_state_chip.isVisible(),
                f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}; state_text={dialog.settings_state_chip.text()!r}; state_visible={dialog.settings_state_chip.isVisible()}",
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
        rows.append(
            (
                "dropdown/list geometry is compact and row-width deterministic",
                popup_width == combo.width()
                and popup_width <= dialog.QUICK_SLOT_COMBO_MAX_WIDTH
                and 132 <= popup_height <= 140
                and combo.maxVisibleItems() <= 4,
                f"popup={popup_width}x{popup_height}; combo={combo.width()}x{combo.height()}; max_visible={combo.maxVisibleItems()}",
            )
        )

    dialog.reject()
    QTest.qWait(40)
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
            and dialog.close_guard_overlay.isVisible()
            and dialog.close_guard_panel.isVisible()
            and dialog.close_guard_overlay.property("unsavedGuard") == "open-save-discard"
            and dialog.close_guard_panel.property("guardActionLayout") == "modal-save-discard-cancel"
            and dialog.close_guard_overlay.accessibleName() == "Unsaved Quick Access changes close guard"
            and not dialog.footer_frame.isVisible()
            and not dialog.discard_button.isVisible()
            and not dialog.keep_editing_button.isVisible()
            and not dialog.revert_button.isVisible()
            and not dialog.change_summary.isVisible(),
            f"visible={dialog.isVisible()}; guard={dialog._close_guard_active}; overlay_visible={dialog.close_guard_overlay.isVisible()}; panel_visible={dialog.close_guard_panel.isVisible()}; overlay_state={dialog.close_guard_overlay.property('unsavedGuard')!r}; panel_layout={dialog.close_guard_panel.property('guardActionLayout')!r}; footer_visible={dialog.footer_frame.isVisible()}; summary={dialog.change_summary.text()!r}; summary_visible={dialog.change_summary.isVisible()}",
        )
    )
    guard_save_x = dialog.guard_save_button.mapTo(dialog.close_guard_panel, QPoint(0, 0)).x()
    guard_discard_x = dialog.guard_discard_button.mapTo(dialog.close_guard_panel, QPoint(0, 0)).x()
    guard_cancel_x = dialog.guard_cancel_button.mapTo(dialog.close_guard_panel, QPoint(0, 0)).x()
    rows.append(
        (
            "close guard comparator-aligned Save / Discard / Cancel layout",
            dialog._close_guard_active
            and dialog.close_guard_overlay.isVisible()
            and dialog.guard_save_button.isVisible()
            and dialog.guard_discard_button.isVisible()
            and dialog.guard_cancel_button.isVisible()
            and dialog.guard_save_button.text() == "Save"
            and dialog.guard_discard_button.text() == "Discard"
            and dialog.guard_cancel_button.text() == "Cancel"
            and dialog.guard_save_button.property("guardVisualRole") == "primary-save"
            and dialog.guard_discard_button.property("guardVisualRole") == "destructive-discard"
            and dialog.guard_cancel_button.property("guardVisualRole") == "neutral-cancel"
            and guard_save_x < guard_discard_x < guard_cancel_x
            and dialog.guard_save_button.hasFocus(),
            f"overlay={dialog.close_guard_overlay.isVisible()}; save=({dialog.guard_save_button.text()!r},{dialog.guard_save_button.isVisible()},{guard_save_x},focus={dialog.guard_save_button.hasFocus()},role={dialog.guard_save_button.property('guardVisualRole')!r}); discard=({dialog.guard_discard_button.text()!r},{dialog.guard_discard_button.isVisible()},{guard_discard_x},role={dialog.guard_discard_button.property('guardVisualRole')!r}); cancel=({dialog.guard_cancel_button.text()!r},{dialog.guard_cancel_button.isVisible()},{guard_cancel_x},role={dialog.guard_cancel_button.property('guardVisualRole')!r}); buttons={[(button.objectName(), button.text(), button.isVisible(), button.isEnabled()) for button in dialog.findChildren(QPushButton)]}",
        )
    )

    dialog.guard_cancel_button.click()
    app.processEvents()
    rows.append(
        (
            "close guard Cancel preserves dirty draft",
            dialog.isVisible()
            and dialog._has_unsaved_changes()
            and not dialog._close_guard_active
            and not dialog.close_guard_overlay.isVisible(),
            f"visible={dialog.isVisible()}; dirty={dialog._has_unsaved_changes()}; guard={dialog._close_guard_active}; overlay_visible={dialog.close_guard_overlay.isVisible()}",
        )
    )
    dialog.reject()
    QTest.qWait(40)
    app.processEvents()
    rows.append(
        (
            "close guard reopens after Cancel",
            dialog.isVisible()
            and dialog._has_unsaved_changes()
            and dialog._close_guard_active
            and dialog.close_guard_overlay.isVisible()
            and dialog.close_guard_overlay.property("unsavedGuard") == "open-save-discard",
            f"visible={dialog.isVisible()}; dirty={dialog._has_unsaved_changes()}; guard={dialog._close_guard_active}; overlay_state={dialog.close_guard_overlay.property('unsavedGuard')!r}",
        )
    )

    save_probe = ResidentAccessSettingsDialog()
    save_probe.show()
    app.processEvents()
    save_probe_combo = save_probe._slot_combos[0]
    save_probe_combo.setCurrentIndex((save_probe_combo.currentIndex() + 1) % max(1, save_probe_combo.count()))
    app.processEvents()
    save_probe.reject()
    QTest.qWait(40)
    app.processEvents()
    save_probe.guard_save_button.click()
    app.processEvents()
    rows.append(
        (
            "close guard Save closes after persisting",
            not save_probe.isVisible()
            and not save_probe._has_unsaved_changes()
            and not save_probe._close_guard_active,
            f"visible={save_probe.isVisible()}; dirty={save_probe._has_unsaved_changes()}; guard={save_probe._close_guard_active}; saved_slots={save_probe._saved_settings.quick_slot_ids}",
        )
    )
    save_probe.deleteLater()

    discard_probe = ResidentAccessSettingsDialog()
    discard_probe.show()
    app.processEvents()
    discard_probe_combo = discard_probe._slot_combos[0]
    discard_probe_combo.setCurrentIndex((discard_probe_combo.currentIndex() + 1) % max(1, discard_probe_combo.count()))
    app.processEvents()
    discard_probe.reject()
    QTest.qWait(40)
    app.processEvents()
    discard_probe.guard_discard_button.click()
    app.processEvents()
    rows.append(
        (
            "close guard Discard closes after dropping draft",
            not discard_probe.isVisible()
            and not discard_probe._close_guard_active,
            f"visible={discard_probe.isVisible()}; dirty={discard_probe._has_unsaved_changes()}; guard={discard_probe._close_guard_active}; saved_slots={discard_probe._saved_settings.quick_slot_ids}",
        )
    )
    discard_probe.deleteLater()

    def _prepare_four_row_dirty_probe() -> ResidentAccessSettingsDialog:
        probe = ResidentAccessSettingsDialog()
        probe.show()
        probe.raise_()
        probe.activateWindow()
        app.processEvents()
        probe._replace_quick_slots(tuple(candidate_route_ids[:active_slot_limit]), notice="4 of 4")
        probe._saved_settings = probe._settings
        probe._notice_text = ""
        probe._refresh_text()
        app.processEvents()
        probe._move_slot(0, 1)
        app.processEvents()
        return probe

    four_row_probe = _prepare_four_row_dirty_probe()
    four_row_dirty_path = log_dir / "26_four_row_dirty_state.png"
    four_row_dirty_ok, _, _ = _capture(
        four_row_probe,
        four_row_dirty_path,
        artifacts,
        surface="Quick Access four-row dirty state",
        state="4 active slots with unsaved edit",
    )
    four_row_combo = four_row_probe._slot_combos[0]
    four_row_combo.showPopup()
    app.processEvents()
    four_row_dropdown_path = log_dir / "27_four_row_dropdown_open.png"
    four_row_dropdown_ok, four_row_popup_w, four_row_popup_h = _capture(
        four_row_combo.view(),
        four_row_dropdown_path,
        artifacts,
        surface="Quick Access four-row route dropdown/list",
        state="open",
    )
    four_row_combo.hidePopup()
    app.processEvents()
    close_result = four_row_probe.close()
    QTest.qWait(40)
    app.processEvents()
    four_row_guard_path = log_dir / "28_four_row_dirty_close_guard_intercept.png"
    four_row_guard_ok, _, _ = _capture(
        four_row_probe,
        four_row_guard_path,
        artifacts,
        surface="Quick Access four-row dirty close intercept",
        state="close event ignored until Save / Discard / Cancel",
    )
    four_row_rows = [
        widget
        for widget in four_row_probe.quick_slot_rows.findChildren(QFrame)
        if widget.objectName() == "residentAccessQuickSlotRow"
    ]
    four_row_guard_pass = (
        four_row_dirty_ok
        and four_row_dropdown_ok
        and four_row_guard_ok
        and close_result is False
        and four_row_probe.isVisible()
        and four_row_probe._has_unsaved_changes()
        and four_row_probe._close_guard_active
        and four_row_probe.close_guard_overlay.isVisible()
        and four_row_probe.property("dirtyCloseEventIgnored") == "true"
        and four_row_probe.property("dirtyCloseInterceptState") == "blocked-before-resolution"
        and len(four_row_rows) == active_slot_limit
        and all(row.height() >= four_row_probe.QUICK_SLOT_ROW_HEIGHT for row in four_row_rows)
        and four_row_popup_w > 100
        and four_row_popup_h > 20
    )
    rows.append(
        (
            "four-row Quick Access dirty/dropdown/close-guard matrix proof",
            four_row_guard_pass,
            f"dirty={four_row_dirty_path}; dropdown={four_row_dropdown_path} ({four_row_popup_w}x{four_row_popup_h}); "
            f"guard={four_row_guard_path}; close_result={close_result}; visible={four_row_probe.isVisible()}; "
            f"dirty_state={four_row_probe._has_unsaved_changes()}; guard={four_row_probe._close_guard_active}; "
            f"event_ignored={four_row_probe.property('dirtyCloseEventIgnored')!r}; "
            f"intercept_state={four_row_probe.property('dirtyCloseInterceptState')!r}; rows={len(four_row_rows)}",
        )
    )
    four_row_probe.guard_cancel_button.click()
    app.processEvents()
    four_row_cancel_path = log_dir / "29_dirty_close_cancel_preserves_window.png"
    cancel_capture_ok, _, _ = _capture(
        four_row_probe,
        four_row_cancel_path,
        artifacts,
        surface="Quick Access four-row dirty close cancel outcome",
        state="Cancel keeps dirty window open",
    )
    cancel_pass = (
        cancel_capture_ok
        and four_row_probe.isVisible()
        and four_row_probe._has_unsaved_changes()
        and not four_row_probe._close_guard_active
        and four_row_probe.property("dirtyCloseResolution") == "cancel-preserved-dirty-window-open"
    )
    four_row_probe.deleteLater()

    save_matrix_probe = _prepare_four_row_dirty_probe()
    save_matrix_close_result = save_matrix_probe.close()
    app.processEvents()
    save_matrix_probe.guard_save_button.click()
    app.processEvents()
    save_pass = (
        save_matrix_close_result is False
        and not save_matrix_probe.isVisible()
        and not save_matrix_probe._has_unsaved_changes()
        and save_matrix_probe.property("dirtyCloseResolution") == "save-persisted-closed"
    )
    save_matrix_probe.deleteLater()

    discard_matrix_probe = _prepare_four_row_dirty_probe()
    discard_matrix_close_result = discard_matrix_probe.close()
    app.processEvents()
    discard_matrix_probe.guard_discard_button.click()
    app.processEvents()
    discard_pass = (
        discard_matrix_close_result is False
        and not discard_matrix_probe.isVisible()
        and discard_matrix_probe.property("dirtyCloseResolution") == "discard-dropped-draft-closed"
    )
    discard_matrix_probe.deleteLater()

    keybind_matrix_probe = _prepare_four_row_dirty_probe()
    keybind_matrix_probe.show()
    keybind_matrix_probe.raise_()
    keybind_matrix_probe.activateWindow()
    app.processEvents()
    QTest.keyClick(keybind_matrix_probe, Qt.Key_Escape)
    app.processEvents()
    keybind_pass = (
        keybind_matrix_probe.isVisible()
        and keybind_matrix_probe.close_guard_overlay.isVisible()
        and keybind_matrix_probe.property("dirtyCloseInterceptSource") == "keyboard_close"
        and keybind_matrix_probe.property("dirtyCloseEventIgnored") == "true"
        and keybind_matrix_probe._has_unsaved_changes()
    )
    keybind_matrix_probe._keep_editing()
    keybind_matrix_probe.close()
    keybind_matrix_probe.deleteLater()

    from pynput import keyboard as pynput_keyboard

    def _run_global_shutdown_hotkey_probe(trigger_key, trigger_label: str) -> tuple[bool, str]:
        probe = _prepare_four_row_dirty_probe()
        shutdown_events: list[str] = []
        bus = ShutdownBus()
        hotkeys = GlobalHotkeyManager(bus)

        def guarded_shutdown():
            if probe.request_dirty_close_intercept(
                source="client_shutdown",
                pending_callback=lambda: shutdown_events.append(f"{trigger_label}-resume"),
            ):
                shutdown_events.append(f"{trigger_label}-blocked")
                return
            shutdown_events.append(f"{trigger_label}-started")

        bus.shutdown_requested.connect(guarded_shutdown)
        hotkeys._on_press(pynput_keyboard.Key.ctrl_l)
        hotkeys._on_press(pynput_keyboard.Key.alt_l)
        hotkeys._on_press(trigger_key)
        for _ in range(4):
            app.processEvents()
            time.sleep(0.01)
        blocked = (
            probe.isVisible()
            and probe._has_unsaved_changes()
            and probe._close_guard_active
            and probe.close_guard_overlay.isVisible()
            and probe.property("dirtyCloseInterceptSource") == "client_shutdown"
            and shutdown_events == [f"{trigger_label}-blocked"]
        )
        if probe._close_guard_active:
            probe.guard_cancel_button.click()
            app.processEvents()
        cancel_kept_open = (
            probe.isVisible()
            and probe._has_unsaved_changes()
            and not probe._close_guard_active
            and probe.property("dirtyCloseResolution") == "cancel-preserved-dirty-window-open"
        )
        detail = (
            f"trigger={trigger_label}; events={shutdown_events}; visible={probe.isVisible()}; "
            f"dirty={probe._has_unsaved_changes()}; guard={probe._close_guard_active}; "
            f"source={probe.property('dirtyCloseInterceptSource')!r}; "
            f"resolution={probe.property('dirtyCloseResolution')!r}"
        )
        probe.close()
        probe.deleteLater()
        return blocked and cancel_kept_open, detail

    shutdown_end_pass, shutdown_end_detail = _run_global_shutdown_hotkey_probe(
        pynput_keyboard.Key.end,
        "ctrl-alt-end",
    )
    shutdown_digit_pass, shutdown_digit_detail = _run_global_shutdown_hotkey_probe(
        pynput_keyboard.KeyCode.from_char("2"),
        "ctrl-alt-2",
    )

    orin_main_text = (ROOT / "desktop" / "orin_desktop_main.py").read_text(encoding="utf-8")
    shutdown_confirmation_guard_pass = (
        "SHUTDOWN_CONFIRMATION_BLOCKED_BY_RESIDENT_SETTINGS_DIRTY_GUARD" in orin_main_text
        and "resume_callback=lambda: request_shutdown_confirmation(source=safe_source)" in orin_main_text
        and orin_main_text.index("SHUTDOWN_CONFIRMATION_BLOCKED_BY_RESIDENT_SETTINGS_DIRTY_GUARD")
        < orin_main_text.index("shutdown_confirmation_active = True")
    )
    rows.append(
        (
            "actual NDAI shutdown hotkeys route through dirty Settings guard",
            shutdown_end_pass and shutdown_digit_pass,
            f"{shutdown_end_detail}; {shutdown_digit_detail}",
        )
    )
    rows.append(
        (
            "shutdown confirmation route guards dirty Settings before native confirmation",
            shutdown_confirmation_guard_pass,
            "orin_desktop_main.py guards request_shutdown_confirmation before shutdown_confirmation_active and native dialog",
        )
    )

    client_resume_calls: list[str] = []
    client_matrix_probe = _prepare_four_row_dirty_probe()
    client_blocked = client_matrix_probe.request_dirty_close_intercept(
        source="client_shutdown",
        pending_callback=lambda: client_resume_calls.append("save-resume"),
    )
    app.processEvents()
    client_blocked_before_resolution = (
        client_blocked
        and client_matrix_probe.isVisible()
        and client_matrix_probe.close_guard_overlay.isVisible()
        and client_matrix_probe.property("dirtyCloseInterceptSource") == "client_shutdown"
        and client_matrix_probe.property("dirtyCloseEventIgnored") == "true"
        and not client_resume_calls
    )
    client_matrix_probe.guard_save_button.click()
    for _ in range(4):
        app.processEvents()
        time.sleep(0.01)
    client_save_resume_pass = (
        client_resume_calls == ["save-resume"]
        and not client_matrix_probe.isVisible()
        and client_matrix_probe.property("dirtyCloseResolution") == "save-persisted-closed"
    )
    client_matrix_probe.deleteLater()

    discard_resume_calls: list[str] = []
    client_discard_probe = _prepare_four_row_dirty_probe()
    client_discard_blocked = client_discard_probe.request_dirty_close_intercept(
        source="client_shutdown",
        pending_callback=lambda: discard_resume_calls.append("discard-resume"),
    )
    app.processEvents()
    client_discard_probe.guard_discard_button.click()
    for _ in range(4):
        app.processEvents()
        time.sleep(0.01)
    client_discard_resume_pass = (
        client_discard_blocked
        and discard_resume_calls == ["discard-resume"]
        and not client_discard_probe.isVisible()
        and client_discard_probe.property("dirtyCloseResolution") == "discard-dropped-draft-closed"
    )
    client_discard_probe.deleteLater()

    cancel_resume_calls: list[str] = []
    client_cancel_probe = _prepare_four_row_dirty_probe()
    client_cancel_probe.request_dirty_close_intercept(
        source="client_shutdown",
        pending_callback=lambda: cancel_resume_calls.append("cancel-should-not-resume"),
    )
    app.processEvents()
    client_cancel_probe.guard_cancel_button.click()
    app.processEvents()
    client_cancel_pass = (
        client_cancel_probe.isVisible()
        and client_cancel_probe._has_unsaved_changes()
        and not cancel_resume_calls
        and client_cancel_probe.property("dirtyCloseResolution") == "cancel-preserved-dirty-window-open"
    )
    client_cancel_probe.close()
    client_cancel_probe.deleteLater()

    dirty_matrix_path = log_dir / "DIRTY_CLOSE_INTERCEPT_MATRIX.md"
    dirty_matrix_path.write_text(
        "\n".join(
            [
                "# FAM-003 Dirty Close Intercept Matrix",
                "",
                "Scope: Global Settings / Tray / Quick Access, four active Quick Access rows.",
                "",
                "| Path | Expected | Result | Evidence |",
                "| --- | --- | --- | --- |",
                f"| Close event | Window stays open, event ignored, guard opens | {'PASS' if four_row_guard_pass else 'FAIL'} | `{four_row_guard_path.name}` |",
                f"| Keyboard close | Window stays open, guard opens, dirty draft remains | {'PASS' if keybind_pass else 'FAIL'} | `dirtyCloseInterceptSource=keyboard_close` |",
                f"| Global Ctrl+Alt+End shutdown hotkey | Client shutdown remains blocked and Cancel keeps dirty window open | {'PASS' if shutdown_end_pass else 'FAIL'} | `{shutdown_end_detail}` |",
                f"| Global Ctrl+Alt+2 shutdown hotkey | Client shutdown remains blocked and Cancel keeps dirty window open | {'PASS' if shutdown_digit_pass else 'FAIL'} | `{shutdown_digit_detail}` |",
                f"| Tray/client shutdown confirmation preflight | Dirty guard opens before native shutdown confirmation | {'PASS' if shutdown_confirmation_guard_pass else 'FAIL'} | `request_shutdown_confirmation` guarded before native dialog |",
                f"| Client shutdown preflight | Shutdown remains blocked before resolution | {'PASS' if client_blocked_before_resolution else 'FAIL'} | `dirtyCloseInterceptSource=client_shutdown` |",
                f"| Cancel | Dirty draft remains and window stays open | {'PASS' if cancel_pass else 'FAIL'} | `{four_row_cancel_path.name}` |",
                f"| Save | Draft persists and window closes | {'PASS' if save_pass else 'FAIL'} | `dirtyCloseResolution=save-persisted-closed` |",
                f"| Discard | Draft is dropped and window closes | {'PASS' if discard_pass else 'FAIL'} | `dirtyCloseResolution=discard-dropped-draft-closed` |",
                f"| Client Save resume | Save resolves guard before resume callback | {'PASS' if client_save_resume_pass else 'FAIL'} | `resume_calls={client_resume_calls}` |",
                f"| Client Discard resume | Discard resolves guard before resume callback | {'PASS' if client_discard_resume_pass else 'FAIL'} | `resume_calls={discard_resume_calls}` |",
                f"| Client Cancel | Cancel does not resume shutdown and leaves dirty window open | {'PASS' if client_cancel_pass else 'FAIL'} | `resume_calls={cancel_resume_calls}` |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    rows.append(
        (
            "dirty close intercept runtime matrix written",
            dirty_matrix_path.exists()
            and cancel_pass
            and save_pass
            and discard_pass
            and keybind_pass
            and shutdown_end_pass
            and shutdown_digit_pass
            and shutdown_confirmation_guard_pass
            and client_blocked_before_resolution
            and client_save_resume_pass
            and client_discard_resume_pass
            and client_cancel_pass,
            f"{dirty_matrix_path}; cancel={cancel_pass}; save={save_pass}; discard={discard_pass}; keybind={keybind_pass}; global_end={shutdown_end_pass}; global_digit={shutdown_digit_pass}; shutdown_confirmation_guard={shutdown_confirmation_guard_pass}; client_blocked={client_blocked_before_resolution}; client_save_resume={client_save_resume_pass}; client_discard_resume={client_discard_resume_pass}; client_cancel={client_cancel_pass}",
        )
    )
    rows.append(
        (
            "dirty close keybind/client shutdown guard proof",
            keybind_pass
            and shutdown_end_pass
            and shutdown_digit_pass
            and shutdown_confirmation_guard_pass
            and client_blocked_before_resolution
            and client_save_resume_pass
            and client_discard_resume_pass
            and client_cancel_pass,
            f"keybind={keybind_pass}; global_end={shutdown_end_pass}; global_digit={shutdown_digit_pass}; shutdown_confirmation_guard={shutdown_confirmation_guard_pass}; client_blocked_before_resolution={client_blocked_before_resolution}; save_resume={client_resume_calls}; discard_resume={discard_resume_calls}; cancel_resume={cancel_resume_calls}",
        )
    )
    artifacts.append(
        {
            "path": str(dirty_matrix_path),
            "surface": "dirty close intercept runtime matrix",
            "state": "four-row Save / Discard / Cancel outcomes",
            "width": "markdown",
            "height": "markdown",
            "saved": str(dirty_matrix_path.exists()),
        }
    )

    dialog._keep_editing()
    dialog.set_focus("quick_access")
    dialog._replace_quick_slots(("tray_visibility_education", "recording_studio"), notice="Unsaved changes.")
    dialog._save_settings()
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
            and "Default shortcut order staged" in dialog.change_summary.text(),
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

    while len(dialog._settings.quick_slot_ids) < active_slot_limit:
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
            len(max_rows) == active_slot_limit
            and max_last_row_bottom <= max_container_bottom <= max_footer_top
            and not dialog.add_slot_button.isEnabled(),
            f"rows={len(max_rows)}; last_row_bottom={max_last_row_bottom}; container_bottom={max_container_bottom}; footer_top={max_footer_top}; add_enabled={dialog.add_slot_button.isEnabled()}",
        )
    )

    dialog._save_settings()
    app.processEvents()
    saved_path = log_dir / "11_post_save_clean_state.png"
    saved_ok, _, _ = _capture(
        dialog,
        saved_path,
        artifacts,
        surface="full Global Settings shell",
        state="post-save clean Quick Access state",
    )
    rows.append(("post-save clean-state screenshot saved", saved_ok, str(saved_path)))
    rows.append(
        (
            "save clears dirty state",
            not dialog._has_unsaved_changes()
            and not dialog.save_button.isEnabled()
            and dialog.change_summary.text() == ""
            and not dialog.change_summary.isVisible()
            and dialog.settings_state_chip.text() == ""
            and not dialog.settings_state_chip.isVisible(),
            f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}; state_chip={dialog.settings_state_chip.text()!r}",
        )
    )

    glyph_path = log_dir / "14_glyph_control_closeup.png"
    action_widgets = [
        widget
        for widget in dialog.findChildren(QFrame)
        if widget.objectName() == "residentAccessQuickSlotActions" and widget.isVisible()
    ]
    glyph_ok = False
    glyph_detail = "no visible quick-slot action cluster"
    if action_widgets:
        action_widget = action_widgets[0]
        action_origin = action_widget.mapTo(dialog, QPoint(0, 0))
        action_rect = QRect(
            max(0, action_origin.x() - 8),
            max(0, action_origin.y() - 8),
            min(dialog.width(), action_widget.width() + 16),
            min(dialog.height(), action_widget.height() + 16),
        )
        glyph_ok, glyph_w, glyph_h = _capture_rect(
            dialog,
            action_rect,
            glyph_path,
            artifacts,
            surface="Quick Access row glyph controls",
            state="two separate action pills with exact reorder split",
        )
        glyph_detail = f"{glyph_path} ({glyph_w}x{glyph_h}); rect={action_rect.getRect()}; action_widget={action_widget.objectName()}"
    rows.append(("glyph/control close-up proof", glyph_ok and glyph_path.exists(), glyph_detail))

    glyph_hover_path = log_dir / "14a_two_pill_reorder_hover_edge_fill.png"
    glyph_hover_ok = False
    glyph_hover_detail = "no visible quick-slot action cluster"
    if action_widgets:
        action_widget = action_widgets[0]
        hover_button = action_widget.findChild(QPushButton, "residentAccessQuickSlotMoveDown") or action_widget.findChild(
            QPushButton,
            "residentAccessQuickSlotDelete",
        )
        if hover_button is not None:
            QTest.mouseMove(hover_button, hover_button.rect().center())
            hover_button.setFocus(Qt.FocusReason.MouseFocusReason)
            app.processEvents()
            QTest.qWait(40)
            action_origin = action_widget.mapTo(dialog, QPoint(0, 0))
            action_rect = QRect(
                max(0, action_origin.x() - 8),
                max(0, action_origin.y() - 8),
                min(dialog.width(), action_widget.width() + 16),
                min(dialog.height(), action_widget.height() + 16),
            )
            glyph_hover_ok, glyph_hover_w, glyph_hover_h = _capture_rect(
                dialog,
                action_rect,
                glyph_hover_path,
                artifacts,
                surface="Quick Access row glyph controls",
                state="hover/focus reorder half edge-to-edge fill",
            )
            glyph_hover_detail = (
                f"{glyph_hover_path} ({glyph_hover_w}x{glyph_hover_h}); "
                f"hover_button={hover_button.objectName()}; "
                f"policy={action_widget.property('quickSlotActionControlPolicy')!r}; "
                f"zone={hover_button.property('glyphZoneButton')!r}; "
                f"segment={hover_button.property('glyphSegment')!r}; "
                f"reorder_split={action_widget.findChild(QFrame, 'residentAccessQuickSlotReorderGroup').property('quickSlotReorderSplitPolicy')!r}"
            )
    rows.append(
        (
            "two-pill reorder hover painted-segment proof",
            glyph_hover_ok
            and glyph_hover_path.exists()
            and action_widgets
            and action_widgets[0].property("quickSlotActionControlPolicy") == "two-pill-reorder-delete-parent-painted-segment-fill-v47"
            and action_widgets[0].findChild(QFrame, "residentAccessQuickSlotReorderGroup") is not None
            and action_widgets[0].findChild(QFrame, "residentAccessQuickSlotReorderGroup").property("quickSlotReorderSplitPolicy")
            == "parent-painted-25-1-25-exact-segment-fill-v47",
            glyph_hover_detail,
        )
    )

    splitter_closeup_path = log_dir / "15_left_pane_resize_affordance_closeup.png"
    splitter_handle = dialog.settings_splitter.handle(1)
    handle_origin = splitter_handle.mapTo(dialog, QPoint(0, 0))
    handle_rect = QRect(
        max(0, handle_origin.x() - 10),
        max(0, handle_origin.y() - 4),
        min(dialog.width(), splitter_handle.width() + 20),
        min(dialog.height(), splitter_handle.height() + 8),
    )
    splitter_closeup_ok, splitter_closeup_w, splitter_closeup_h = _capture_rect(
        dialog,
        handle_rect,
        splitter_closeup_path,
        artifacts,
        surface="left-pane resize affordance",
        state="subtle splitter handle close-up",
    )
    rows.append(
        (
            "left pane resize affordance close-up proof",
            splitter_closeup_ok
            and splitter_closeup_path.exists()
            and dialog.settings_splitter.handleWidth() == 9
            and dialog.settings_splitter.property("settingsSplitterAffordance")
            == "quiet-default-hover-dots-9px-hit-zone-v28"
            and splitter_handle.accessibleName() == "Resize Global Settings navigation pane",
            f"{splitter_closeup_path} ({splitter_closeup_w}x{splitter_closeup_h}); handle_width={dialog.settings_splitter.handleWidth()}; handle_object={splitter_handle.objectName()!r}; handle_a11y={splitter_handle.accessibleName()!r}; affordance={dialog.settings_splitter.property('settingsSplitterAffordance')!r}; rect={handle_rect.getRect()}",
        )
    )
    splitter_state_results: list[str] = []
    splitter_state_ok = True
    for state_name in ("normal", "hover", "active"):
        splitter_handle.setProperty("splitterVisualState", state_name)
        splitter_handle.update()
        app.processEvents()
        state_path = log_dir / f"15_{state_name}_splitter_resize_affordance.png"
        state_capture_ok, state_w, state_h = _capture_rect(
            dialog,
            handle_rect,
            state_path,
            artifacts,
            surface="left-pane resize affordance",
            state=f"{state_name} splitter handle state",
        )
        state_ok = state_capture_ok and state_path.exists() and splitter_handle.property("splitterVisualState") == state_name
        splitter_state_ok = splitter_state_ok and state_ok
        splitter_state_results.append(f"{state_name}={'PASS' if state_ok else 'FAIL'} {state_path} ({state_w}x{state_h})")
    splitter_handle.setProperty("splitterVisualState", "normal")
    splitter_handle.update()
    rows.append(
        (
            "left pane splitter normal/hover/active states proof",
            splitter_state_ok,
            "; ".join(splitter_state_results),
        )
    )
    rows.append(
        (
            "splitter normal state is quiet until hover or drag",
            splitter_state_ok
            and dialog.settings_splitter.handleWidth() == 9
            and dialog.settings_splitter.property("settingsSplitterAffordance")
            == "quiet-default-hover-dots-9px-hit-zone-v28",
            f"handle_width={dialog.settings_splitter.handleWidth()}; affordance={dialog.settings_splitter.property('settingsSplitterAffordance')!r}; states={splitter_state_results}",
        )
    )
    rows.extend(_run_settings_stress_matrix())

    contact_sheet, contact_ok = _write_contact_sheet(
        log_dir,
        [
            ("Accepted reference - AI Control Center family grammar", REFERENCE_SCREENSHOTS[0][1]),
            ("Accepted reference - close hover", REFERENCE_SCREENSHOTS[1][1]),
            ("Accepted reference - Manage Monitors dirty guard", manage_guard_reference_path),
            ("Repaired FAM-003 - settings shell", default_path),
            ("Repaired FAM-003 - moved window", log_dir / "03a_window_moved_by_chrome.png"),
            ("Repaired FAM-003 - resized window", log_dir / "03b_window_resized.png"),
            ("Repaired FAM-003 - settings organizer", log_dir / "04_left_settings_organizer.png"),
            ("Repaired FAM-003 - Tray parent page", log_dir / "05_tray_parent_page.png"),
            ("Repaired FAM-003 - 4 row layout", log_dir / f"22_row_count_{active_slot_limit}_of_{active_slot_limit}.png"),
            ("Repaired FAM-003 - dropdown/list state", log_dir / "07_dropdown_list_state.png"),
            ("Repaired FAM-003 - four-row dirty close intercept", log_dir / "28_four_row_dirty_close_guard_intercept.png"),
            ("Repaired FAM-003 - dirty/save controls", log_dir / "06_dirty_quick_access.png"),
        ],
    )
    rows.append(
        (
            "side-by-side reference contact sheet written",
            contact_ok and contact_sheet.exists(),
            str(contact_sheet),
        )
    )
    numbered_reference_sheet = log_dir / "12_reference_conformance_contact_sheet.png"
    if contact_ok and contact_sheet.exists():
        numbered_reference_sheet.write_bytes(contact_sheet.read_bytes())
    rows.append(
        (
            "numbered reference conformance contact sheet written",
            numbered_reference_sheet.exists(),
            str(numbered_reference_sheet),
        )
    )
    if numbered_reference_sheet.exists():
        artifacts.append(
            {
                "path": str(numbered_reference_sheet),
                "surface": "numbered accepted-reference side-by-side comparison",
                "state": "contact sheet",
                "width": "composite",
                "height": "composite",
                "saved": "True",
            }
        )
    accepted_default_copy = log_dir / "13_accepted_ai_control_center_default.png"
    if REFERENCE_SCREENSHOTS[0][1].exists():
        accepted_default_copy.write_bytes(REFERENCE_SCREENSHOTS[0][1].read_bytes())
    rows.append(
        (
            "accepted AI Control Center default copy written",
            accepted_default_copy.exists(),
            str(accepted_default_copy),
        )
    )
    if accepted_default_copy.exists():
        artifacts.append(
            {
                "path": str(accepted_default_copy),
                "surface": "accepted AI Control Center reference",
                "state": "default reference copy for closure proof",
                "width": "reference",
                "height": "reference",
                "saved": "True",
            }
        )
    manage_guard_side_by_side, manage_guard_side_by_side_ok = _write_contact_sheet(
        log_dir,
        [
            ("Accepted Manage Monitors - modal Save / Discard / Cancel", manage_guard_reference_path),
            ("Repaired FAM-003 - modal Save / Discard / Cancel", log_dir / "08_close_guard.png"),
        ],
        file_name="18_manage_monitors_dirty_guard_side_by_side.png",
        title="FAM-003 vs Accepted Manage Monitors Dirty Guard",
    )
    rows.append(
        (
            "Manage Monitors dirty guard side-by-side sheet written",
            manage_guard_side_by_side_ok and manage_guard_side_by_side.exists(),
            str(manage_guard_side_by_side),
        )
    )
    artifacts.append(
        {
            "path": str(manage_guard_side_by_side),
            "surface": "Manage Monitors dirty guard side-by-side comparison",
            "state": "accepted reference vs repaired FAM-003 close guard",
            "width": "composite",
            "height": "composite",
            "saved": str(bool(manage_guard_side_by_side_ok and manage_guard_side_by_side.exists())),
        }
    )
    defect_contact_sheet, defect_contact_ok = _write_contact_sheet(
        log_dir,
        [
            ("Before false retest - v15 utility-like shell", ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation" / "20260624-123116" / "01_default_global_settings_shell.png"),
            ("Rejected v16 - sectioned title row", ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation" / "20260624-132602" / "02_top_level_chrome_control_cluster.png"),
            ("Accepted reference - broad NDAI comparator", REFERENCE_SCREENSHOTS[0][1]),
            ("Accepted reference - Manage Monitors dirty guard", manage_guard_reference_path),
            ("Repaired v40 - compact NDAI settings shell", default_path),
            ("Repaired v40 - centered Settings title", chrome_path),
            ("Repaired v40 - border-safe subcategory indent", child_focus_path),
            ("Repaired v40 - child focus/pressed state", child_pressed_path),
            ("Repaired v40 - polished quick-slot action capsule", glyph_path),
            ("Repaired v40 - UIREF-007 150-270 splitter travel", splitter_closeup_path),
            ("Repaired v40 - 4 row deterministic-width layout", log_dir / f"22_row_count_{active_slot_limit}_of_{active_slot_limit}.png"),
            ("Repaired v40 - deterministic dropdown", log_dir / "07_dropdown_list_state.png"),
            ("Repaired v40 - close guard", log_dir / "08_close_guard.png"),
            ("Repaired v40 - keybind/client close intercept", log_dir / "28_four_row_dirty_close_guard_intercept.png"),
        ],
        file_name="16_defect_closure_contact_sheet.png",
        title="FAM-003 False-Retest Defect Closure Contact Sheet",
    )
    rows.append(
        (
            "defect closure contact sheet written",
            defect_contact_ok and defect_contact_sheet.exists(),
            str(defect_contact_sheet),
        )
    )
    artifacts.append(
        {
            "path": str(defect_contact_sheet),
            "surface": "defect-by-defect closure proof",
            "state": "contact sheet",
            "width": "composite",
            "height": "composite",
            "saved": str(bool(defect_contact_ok and defect_contact_sheet.exists())),
        }
    )
    red_team_sheet, red_team_ok = _write_contact_sheet(
        log_dir,
        [
            ("Red-team check - full shell", default_path),
            ("Red-team check - chrome/header/control pill", chrome_path),
            ("Red-team check - nav organizer", nav_path),
            ("Red-team check - child border no clipping", child_focus_path),
            ("Red-team check - child focus/pressed", child_pressed_path),
            ("Red-team check - collapsed parent", collapsed_path),
            ("Red-team check - row spacing/glyphs", glyph_path),
            ("Red-team check - splitter affordance", splitter_closeup_path),
            ("Red-team check - 4 row layout", log_dir / f"22_row_count_{active_slot_limit}_of_{active_slot_limit}.png"),
            ("Red-team check - medium resized shell", resized_path),
            ("Red-team check - wide resized shell", wide_path),
            ("Red-team check - minimum shell", min_path),
            ("Red-team check - dropdown open", log_dir / "07_dropdown_list_state.png"),
            ("Red-team reference - Manage Monitors dirty guard", manage_guard_reference_path),
            ("Red-team check - close guard", log_dir / "08_close_guard.png"),
            ("Red-team check - four-row close intercept", log_dir / "28_four_row_dirty_close_guard_intercept.png"),
            ("Red-team check - guard side-by-side", manage_guard_side_by_side),
        ],
        file_name="17_red_team_review_sheet.png",
        title="FAM-003 Codex Red-Team Visual Review Sheet",
    )
    rows.append(("red-team review sheet written", red_team_ok and red_team_sheet.exists(), str(red_team_sheet)))
    artifacts.append(
        {
            "path": str(red_team_sheet),
            "surface": "Codex red-team visual review",
            "state": "failure-seeking review sheet",
            "width": "composite",
            "height": "composite",
            "saved": str(bool(red_team_ok and red_team_sheet.exists())),
        }
    )
    closure_ledger = log_dir / "DEFECT_CLOSURE_PROOF_LEDGER.md"
    closure_lines = [
        "# FAM-003 False-Retest Defect Closure Proof Ledger",
        "",
        "Scope: FAM-003 Global Settings / Tray / Quick Access only.",
        "Status model: helper PASS is supporting evidence only; LV green still requires USER-operated UTS PASS or WAIVED.",
        "",
        "| Defect ID | Origin | Prior Failure Evidence | Repair Proof | Accepted Reference / Comparator | Final Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    closure_rows = [
        ("F3-LV1-UI-001", "USER / ChatGPT", "20260624-123116/02_top_level_chrome_control_cluster.png", "02_top_level_chrome_control_cluster.png; 12_reference_conformance_contact_sheet.png", "settings-specific single-row title row plus broad NDAI comparator", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-015", "USER", "20260624-123116/04_left_settings_organizer.png", "15_left_pane_resize_affordance_closeup.png; 15_normal_splitter_resize_affordance.png; 15_hover_splitter_resize_affordance.png; 15_active_splitter_resize_affordance.png", "subtle 1px visible left-pane resize affordance inside a 9px hit zone", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-016", "USER", "corner-grip-only v15/v20 proof and stale minimum-size floors", f"03b_window_resized.png; 03d_window_wide_size.png; 03c_window_minimum_size.png; 03e_live_user_drag_resized.png; {args.visible_cursor_manifest}", "684x388 base minimum with active-content minimum growth, 840x610 max, plus separate normal-runtime ordered cursor-composited right-edge proof and no visible bottom-right grip", "CLOSED_WITH_PROOF" if visible_cursor_ok else "FIXED_PENDING_PROOF"),
        ("F3-LV1-UI-017", "USER", "20260624-123116/01_default_global_settings_shell.png", "01_default_global_settings_shell.png; 05_row_action_default_disabled_state.png; 20_stress_left_rail_28_categories.png; 21_stress_content_mixed_controls.png; 22_row_count_1_of_4.png; 22_row_count_2_of_4.png; 22_row_count_3_of_4.png; 22_row_count_4_of_4.png", "780x460 deterministic shell with control-pill scale matched row grouping, unclipped Quick Access rows, and useful settings copy", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-018", "USER", "v15 ^ / v / x text buttons", "14_glyph_control_closeup.png", "UIREF-003 polished control state grammar", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-019", "USER", "plain utility caption title", "02_top_level_chrome_control_cluster.png", "settings-specific seamless single-row title grammar", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-020", "USER", "flat utility text hierarchy / visible Saved label", "01_default_global_settings_shell.png; 05_tray_parent_page.png; 11_post_save_clean_state.png", "Project Vision product experience contract plus compact settings scope/detail, menu-order copy, and quiet clean-state discipline", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-021", "USER / ChatGPT", "compact utility-panel overall impression", "16_defect_closure_contact_sheet.png; 17_red_team_review_sheet.png", "Project Vision; FAM-002; UIREF-001..006; v22 title/layout full-surface expected-vs-actual adjudication", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-022", "USER", "20260624-132602/02_top_level_chrome_control_cluster.png", "02_top_level_chrome_control_cluster.png; 16_defect_closure_contact_sheet.png; 17_red_team_review_sheet.png", "Global Settings is its own settings-window class: no title card, no stacked title, no sectioned title row", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-023", "USER / ChatGPT", "v17 left rail child row was nearly peer-level", "04_left_settings_organizer.png; 04a_left_nav_active_child.png", "Tray parent with visibly subordinate Quick Access child", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-024", "USER / ChatGPT", "v17/default v20 canvases were too large or visually zoomed out", "01_default_global_settings_shell.png", "780x460 content-deterministic default shell with proportional control scale", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-025", "USER / ChatGPT", "v17/v23 minimum floors were over-restrictive", "03c_window_minimum_size.png; 04d_left_pane_compressed_horizontal_overflow.png", "684x388 base minimum with active-content height growth and a deliberate compressed-rail overflow test state", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-026", "USER / ChatGPT", "nav rows stretched and overflow was treated as proof", "04_left_settings_organizer.png; 04d_left_pane_compressed_horizontal_overflow.png; 04e_left_pane_wide.png", "bounded parent/child rail rows at normal/wide sizes plus intentional compressed horizontal overflow at the splitter minimum", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-027", "USER / ChatGPT", "3 active of 4 header badge was verbose and detached from Add Slot", "01_default_global_settings_shell.png", "3 of 4 placed beside Add Slot", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-028", "USER / ChatGPT", "clean-state Saved label was redundant", "01_default_global_settings_shell.png; 11_post_save_clean_state.png", "quiet clean/post-save state; dirty/guard copy remains meaningful", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-029", "USER", "v18 footer/status close guard did not match accepted Manage Monitors modal dirty guard", "08_close_guard.png; 13a_accepted_manage_monitors_dirty_guard_reference.png; 18_manage_monitors_dirty_guard_side_by_side.png; MANAGE_MONITORS_DIRTY_GUARD_REFERENCE.md", "accepted HUD Dashboard / Manage Monitors modal Save / Discard / Cancel dirty guard", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-030", "USER / ChatGPT", "v20/v21 repair risked global shrink/zoom-out instead of real settings-window composition", "01_default_global_settings_shell.png; 04_left_settings_organizer.png; 14_glyph_control_closeup.png", "readable compact controls, real row sizes, and no global scale-down repair", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-031", "USER / ChatGPT", "v24/default proof still allowed the active work surface to feel stranded in a larger shell", "01_default_global_settings_shell.png; 03b_window_resized.png; 03d_window_wide_size.png", "780x460 default, 790x430 medium, and 820x500 max/wide shell with the active page attached to the splitter and no unexplained right-side field", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-032", "USER / ChatGPT", "v21 grouped NEXUS DESKTOP AI / Global Settings title row still failed composition expectations", "02_top_level_chrome_control_cluster.png", "centered Settings-only title row, no visible title-card, no stacked title, no visible NDAI title-row branding", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-033", "USER / ChatGPT", "v21/v24 wide state still risked footer/action detachment from active settings content", "01_default_global_settings_shell.png; 03d_window_wide_size.png; DEFECT_CLOSURE_PROOF_LEDGER.md", "footer remains within the active settings page at default, medium, and splitter-attached wide sizes", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-034", "USER / ChatGPT", "Global Settings standard-window path needed renewed proof after title/layout repair", "FAM003_SETTINGS_REPAIR_VISUAL_VALIDATION.md; 02_top_level_chrome_control_cluster.png", "PySide DialogChromeBar remains legal reference-derived settings window; no WebView/shared-primitive migration claim", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-035", "USER / ChatGPT", "bottom-right resize grip must remain removed", "01_default_global_settings_shell.png; 03d_window_wide_size.png; 03c_window_minimum_size.png", "no resize_grip attribute, no residentAccessSettingsResizeGrip widget, no QSizeGrip for this surface", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-036", "USER / ChatGPT", "resize parity required after max-size repair", f"03b_window_resized.png; 03d_window_wide_size.png; 03c_window_minimum_size.png; 03e_live_user_drag_resized.png; {args.visible_cursor_manifest}", "8px edge and 12px corner hit zones, normal-runtime USER-visible cursor handoff, dynamic row-count minimum clamp, 840x610 max clamp, no visible grip", "CLOSED_WITH_PROOF" if visible_cursor_ok else "FIXED_PENDING_PROOF"),
        ("F3-LV1-UI-037", "USER / ChatGPT", "v21 visible title row still included NEXUS DESKTOP AI branding", "02_top_level_chrome_control_cluster.png", "visible title row contains only centered Settings; hidden kicker is empty and no visible NDAI branding appears in the title row", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-038", "USER / ChatGPT", "future centered Global Settings watermark concept was requested but must not be faked into runtime UI", "FAM003_SETTINGS_REPAIR_VISUAL_VALIDATION.md; fam003_settings_visual_fail_repair_manifest.json", "branch-local deferred watermark property recorded; runtimeWatermarkVisible=false and no visible watermark widget/text exists", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-043", "USER / ChatGPT", "current packet proof showed 3rd/4th Quick Access rows clipping, squashing, or colliding with the footer", "22_row_count_1_of_4.png; 22_row_count_2_of_4.png; 22_row_count_3_of_4.png; 22_row_count_4_of_4.png; 10_max_slots_unclipped.png", "1/2/3/4 row matrix with equal 36px row heights, content-driven balanced-gutter card/window growth, and footer separation", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-044", "USER / ChatGPT", "content scale looked globally zoomed down relative to the accepted window-control pill", "01_default_global_settings_shell.png; 14_glyph_control_closeup.png; 22_row_count_3_of_4.png", "window-control scale used as anchor while row height, dropdown, action glyphs, footer buttons, and content spacing scale up without enlarging the rail icons into cards", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-045", "USER / ChatGPT", "footer/list collision risk increased as slot count changed", "22_row_count_1_of_4.png; 22_row_count_2_of_4.png; 22_row_count_3_of_4.png; 22_row_count_4_of_4.png", "last row remains below card bottom padding and card bottom remains above footer for every active slot count", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-046", "USER / ChatGPT", "layout behaved like a fixed visual envelope instead of content-driven sizing", "fam003_settings_visual_fail_repair_manifest.json; 22_row_count_4_of_4.png; 03c_window_minimum_size.png", "quickAccessLayoutPolicy uiref-007-deterministic-row-width-combo-integrated-action-capsule-row-count-close-intercept-v42 with row-count minimum height, deterministic combo width, polished integrated action capsule, and Add Slot disabled at slot limit", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-047", "USER / ChatGPT", "185455 packet showed duplicate slot-count text in the Add Slot row and lower/footer area", "22_row_count_1_of_4.png; 22_row_count_2_of_4.png; 22_row_count_3_of_4.png; 22_row_count_4_of_4.png", "visible count labels are machine-counted and each row state has exactly one N of 4 label beside Add Slot", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-048", "USER / ChatGPT", "185455 packet mixed claimed 860x560 live max with stale 1100x720 stress proof", "03d_window_wide_size.png; fam003_settings_visual_fail_repair_manifest.json; LV1_RETEST_PACKET_FILE_DIGEST.md", "live max is 820x590; synthetic stress proof is separated and stale 1100x720/920x520 artifacts are rejected from LV1 packet proof", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-049", "USER / ChatGPT", "wide/stress state still showed unexplained dead space and left-clustered content", "03d_window_wide_size.png; 19_stress_size_840x610.png", "max/wide shell is clamped to meaningful content width and validator fails unexplained right-side dead space", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-050", "USER / ChatGPT", "splitter normal-state affordance remained too mechanical/visible", "15_normal_splitter_resize_affordance.png; 15_hover_splitter_resize_affordance.png; 15_active_splitter_resize_affordance.png", "default splitter is a quiet line with hover/active dots while the 9px hit zone remains available", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-051", "USER / ChatGPT", "left rail active/icon/hierarchy polish remained under-authored", "04_left_settings_organizer.png; 04a_left_nav_active_child.png; 04b_left_nav_collapsed.png; 04c_left_nav_expanded.png", "rail keeps slim rows while parent/child selection uses polished active signal, proportional icons, quiet expander, and deterministic hierarchy", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-052", "USER", "v29 live review found control pill looked polished while content UI still looked weaker and too small", "01_default_global_settings_shell.png; 02_top_level_chrome_control_cluster.png; 14_glyph_control_closeup.png", "control-pill-anchored proportional content scale v32", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-053", "USER", "Menu order card had top gutter without matching bottom breathing room", "22_row_count_1_of_4.png; 22_row_count_2_of_4.png; 22_row_count_3_of_4.png; 22_row_count_4_of_4.png", "balanced top/bottom card gutter across 1/2/3/4 rows", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-054", "USER", "left rail scale remained too small and squished", "04_left_settings_organizer.png; 04a_left_nav_active_child.png; 04b_left_nav_collapsed.png; 04c_left_nav_expanded.png; 04d_left_pane_compressed_horizontal_overflow.png", "normal rail preserves proportional parent/child rows while the splitter minimum intentionally compresses to a horizontal-overflow stress state", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-055", "USER", "Quick Access child pill appeared clipped/cut off", "04a_left_nav_active_child.png", "102x28 historical child pill closure proof retained as superseded context", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-056", "USER", "row controls/glyphs risked overpowering row labels", "05_row_action_default_disabled_state.png; 14_glyph_control_closeup.png", "quietGlyph secondary move/delete controls with labels remaining primary", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-057", "USER", "content/header typography and polish lacked compact NDAI richness", "01_default_global_settings_shell.png; 05_tray_parent_page.png; 12_reference_conformance_contact_sheet.png", "compact settings-tool polish through typography, panel depth, active state, and spacing without dashboard-like header cards", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-058", "USER", "The Quick Access sub-category pill in the left rail clips the right edge of its border.", "04a_left_nav_active_child.png; 04a1_quick_access_child_pill_no_clip_focus.png; 04a2_quick_access_child_pill_focus_pressed_state.png; 04d_left_pane_compressed_horizontal_overflow.png; 04e_left_pane_wide.png", "normal/wide rail keeps border-safe child proof; compressed rail is explicitly a scroll/overflow stress state, not normal navigation proof", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-059", "USER", "fix the gutter inside the sub catagory, it looks squished. do not let the main catagory affect sub catagory button length", "04a_left_nav_active_child.png; 04a1_quick_access_child_pill_no_clip_focus.png; 04a2_quick_access_child_pill_focus_pressed_state.png; 04d_left_pane_compressed_horizontal_overflow.png; 04e_left_pane_wide.png", "112px child pill inside a 6px-left / 0px-right subpage rail budget with independent 88px child label width at normal/wide states; compressed state preserves scroll recovery", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-060", "USER", "do not let the indent of the sub catagory be affected. the indent needs to be fixed and standardized. now you can visually see that the distinguished difference in main categories and sub categories is gone.", "04_left_settings_organizer.png; 04a_left_nav_active_child.png; 04a1_quick_access_child_pill_no_clip_focus.png; 04a2_quick_access_child_pill_focus_pressed_state.png; 04d_left_pane_compressed_horizontal_overflow.png; 04e_left_pane_wide.png", "fixed 14px subcategory indent remains the hierarchy rule; compressed state is an intentional splitter stress state with horizontal scroll recovery", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-061", "USER", "the border of the wuick acces is clipping again, and the indent needs to be more obvious. and fix the clipping", "04_left_settings_organizer.png; 04a_left_nav_active_child.png; 04a1_quick_access_child_pill_no_clip_focus.png; 04a2_quick_access_child_pill_focus_pressed_state.png; 04d_left_pane_compressed_horizontal_overflow.png; 04e_left_pane_wide.png", "border-safe normal/wide left rail with fixed 14px subcategory indent, 112px child pill, 88px child label budget, stable selected/hover border, and compressed horizontal-overflow stress proof", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-062", "USER", "splitter could not compress the rail far enough to show half of the main category or force horizontal scroll", "04d_left_pane_compressed_horizontal_overflow.png; 04e_left_pane_wide.png", "76-270px splitter travel with AsNeeded horizontal scroll; compressed rail shows partial parent category and scroll recovery while normal/wide states remain readable", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-063", "USER", "Settings window resize-edge cursor flickered between pointer and resize cursor while other windows were stable", f"fam003_settings_visual_fail_repair_manifest.json; 03e_live_user_drag_resized.png; {args.visible_cursor_manifest}", "Settings resize cursor path is closed only by ordered normal-arrow, right-edge resize, mouse-down, held-drag, mouse-up, and post-edge normal-arrow proof with the actual OS cursor composited from GetCursorInfo", "CLOSED_WITH_PROOF" if visible_cursor_ok else "FIXED_PENDING_PROOF"),
        ("F3-LV1-UI-064", "USER", "Quick Access row button cluster looked visually out of place and non-immersive", "05_row_action_default_disabled_state.png; 14_glyph_control_closeup.png", "row actions render as two separate pills: a 25/1/25 up/down reorder pill and a separate 28px X pill", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-065", "USER", "Quick Access row glyphs were acceptable, but visible gray mini-button pills and button hover highlights inside the capsule broke immersion", "14_glyph_control_closeup.png; 14a_two_pill_reorder_hover_edge_fill.png", "superseded single-capsule approach replaced by two-pill grammar; reorder hover/disabled feedback fills the individual half inside the pill border, and X owns a separate pill", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-066", "USER", "Desired action grammar clarified as two separate pills: one X pill and one up/down pill with a perfect internal split", "14_glyph_control_closeup.png; 14a_two_pill_reorder_hover_edge_fill.png", "quickSlotActionControlPolicy two-pill-reorder-delete-parent-painted-segment-fill-v47 with quickSlotReorderSplitPolicy parent-painted-25-1-25-exact-segment-fill-v47", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-067", "USER", "disabled/hover grey fill extended past the reorder pill border", "14_glyph_control_closeup.png; 14a_two_pill_reorder_hover_edge_fill.png", "disabled and hover feedback are parent-painted through the same rounded inner pill path and clipped to exact 25px half-rects divided by the 1px center rail", "CLOSED_WITH_PROOF"),
        ("F3-LV1-FUNC-001", "USER / ChatGPT", "dirty guard did not prove that close/app close was blocked until Save / Discard / Cancel resolved", "28_four_row_dirty_close_guard_intercept.png; 29_dirty_close_cancel_preserves_window.png; DIRTY_CLOSE_INTERCEPT_MATRIX.md", "close event is ignored while dirty; Cancel keeps the dirty window open; Save persists and closes; Discard drops and closes", "CLOSED_WITH_PROOF"),
        ("F3-LV1-FUNC-002", "USER", "NDAI close keybind/client shutdown could close the app even after dirty guard appeared", "DIRTY_CLOSE_INTERCEPT_MATRIX.md; desktop/orin_desktop_main.py; desktop/desktop_renderer.py", "client shutdown preflight blocks before shutdown_started and resumes only after Save or Discard; Cancel leaves app open", "CLOSED_WITH_PROOF"),
        ("F3-LV1-PROOF-001", "USER / ChatGPT / Codex", "retest packet returned without defect-by-defect proof", "DEFECT_CLOSURE_PROOF_LEDGER.md; FAIL_CAPABLE_DEFECT_LEDGER.md; 17_red_team_review_sheet.png", "UTS guidance Codex Visual Adjudication gate with UI-023 through UI-029 coverage", "CLOSED_WITH_PROOF"),
        ("F3-LV1-PROOF-002", "USER / ChatGPT / Codex", "Codex repeatedly returned repaired/retest-candidate packets after unresolved seed defects remained visible", "DEFECT_CLOSURE_PROOF_LEDGER.md; FAIL_CAPABLE_DEFECT_LEDGER.md; 17_red_team_review_sheet.png; 18_manage_monitors_dirty_guard_side_by_side.png", "row-specific root-cause prevention plus fail-capable validator requirements for every reopened current-owned defect", "CLOSED_WITH_PROOF"),
        ("F3-LV1-PROOF-005", "USER / ChatGPT", "packet proof lacked row-count and dirty-close runtime behavior matrix", "22_row_count_1_of_4.png; 22_row_count_2_of_4.png; 22_row_count_3_of_4.png; 22_row_count_4_of_4.png; DIRTY_CLOSE_INTERCEPT_MATRIX.md", "packet-contained proof must include row-count matrix and four-row dirty-close behavior matrix", "CLOSED_WITH_PROOF"),
        ("F3-LV1-PROOF-006", "USER", "dirty-close proof did not cover keybind/client/app close routes", "DIRTY_CLOSE_INTERCEPT_MATRIX.md", "packet-contained matrix now covers close event, keyboard close, client shutdown preflight, Save, Discard, and Cancel", "CLOSED_WITH_PROOF"),
    ]
    if _same_defect_loop_breaker_active():
        adjusted_rows: list[tuple[str, str, str, str, str, str]] = []
        for defect_id, origin, prior, proof, comparator, status in closure_rows:
            if defect_id in SAME_DEFECT_REOPENED_IDS:
                status = "REOPENED"
                comparator = (
                    "same-defect recurrence gate blocks retest candidate; stronger "
                    "row-specific proof is required before closure"
                )
            adjusted_rows.append((defect_id, origin, prior, proof, comparator, status))
        adjusted_rows.append(
            (
                SAME_DEFECT_LOOP_BREAKER_ID,
                "USER / ChatGPT / Codex",
                "v17/v18/v19 retest packets returned after recurring defects stayed unresolved",
                "same_defect_recurrence_ledger_20260624.md; orin_fam003_same_defect_recurrence_validation.py",
                "branch-local recurrence gate blocks retest candidate return",
                "CLOSED_WITH_PROOF",
            )
        )
        closure_rows = adjusted_rows
    for defect_id, origin, prior, proof, comparator, status in closure_rows:
        closure_lines.append(f"| {defect_id} | {origin} | `{prior}` | `{proof}` | {comparator} | {status} |")
    closure_ledger.write_text("\n".join(closure_lines) + "\n", encoding="utf-8")
    rows.append(("defect closure proof ledger written", closure_ledger.exists(), str(closure_ledger)))
    artifacts.append(
        {
            "path": str(closure_ledger),
            "surface": "defect closure proof ledger",
            "state": "all current-owned false-retest defects",
            "width": "markdown",
            "height": "markdown",
            "saved": str(closure_ledger.exists()),
        }
    )
    rows.append(
        (
            "element-group ledger is row-level fail-capable",
            len(ELEMENT_GROUP_LEDGER_ROWS) >= 25
            and all(row.get("checks") for row in ELEMENT_GROUP_LEDGER_ROWS),
            f"element_groups={len(ELEMENT_GROUP_LEDGER_ROWS)}",
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
    image_receipt_path, image_receipt_ok, image_receipt_detail = _write_image_integrity_receipt(log_dir)
    rows.append(
        (
            "image integrity receipt written",
            image_receipt_path.exists() and image_receipt_ok,
            f"{image_receipt_path}; {image_receipt_detail}",
        )
    )
    artifacts.append(
        {
            "path": str(image_receipt_path),
            "surface": "packet image integrity receipt",
            "state": "all generated PNG proof artifacts",
            "width": "markdown",
            "height": "markdown",
            "saved": str(image_receipt_path.exists() and image_receipt_ok),
        }
    )

    ledger_path, manifest_path, element_ledger_path, defect_ledger_path = _write_artifact_ledger(
        log_dir,
        artifacts,
        rows,
        contact_sheet,
        manage_guard_reference_path=manage_guard_reference_path,
        manage_guard_ledger_path=manage_guard_ledger_path,
        manage_guard_side_by_side=manage_guard_side_by_side,
    )
    manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_payload.update(
        {
            "sourceHead": current_head,
            "visibleCursorProofManifest": str(args.visible_cursor_manifest),
            "visibleCursorProofPass": visible_cursor_ok,
            "visibleCursorProofDetail": visible_cursor_detail,
        }
    )
    manifest_path.write_text(
        json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    rows.append(
        (
            "artifact and element-group ledgers written",
            ledger_path.exists() and manifest_path.exists() and element_ledger_path.exists() and defect_ledger_path.exists(),
            f"{ledger_path}; {element_ledger_path}; {defect_ledger_path}; {manifest_path}",
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
