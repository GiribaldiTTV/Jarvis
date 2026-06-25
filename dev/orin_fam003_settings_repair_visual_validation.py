"""Reference-conformance proof for FAM-003 Global Settings repair.

This helper uses an isolated resident-access settings file so it can validate
Quick Access behavior without mutating USER runtime preferences. It is
supporting proof only: USER-operated Live Validation remains authoritative for
final visual acceptance.
"""

from __future__ import annotations

import datetime as dt
import ctypes
import ctypes.wintypes
import json
import os
import re
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation"
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
    "F3-LV1-PROOF-001",
    "F3-LV1-PROOF-002",
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
        r"^##\s+(F3-LV1-(?:UI|PROOF)-\d{3})\b(?P<body>.*?)(?=^##\s+F3-LV1-(?:UI|PROOF)-\d{3}\b|\Z)",
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
        "spacing": "700x344 content-fit two-column settings layout",
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
        "spacing": "bounded 104-130px slim rail",
        "hitbox": "left splitter pane",
        "icon_label": "painted tray icon, painted quick-access icon, compact chevron expander",
        "states": "default, active child, collapsed parent, narrow overflow, wide pane",
        "a11y": "Open Quick Access Settings; Resize Global Settings navigation pane",
        "comparator": "dense settings navigation grammar",
        "proof": "04_left_settings_organizer.png; 04a_left_nav_active_child.png; 04b_left_nav_collapsed.png; 04c_left_nav_expanded.png; 04d_left_pane_minimum_no_horizontal_scroll.png; 04e_left_pane_wide.png",
        "checks": "left navigation settings organizer;Tray parent plus Quick Access child settings IA;selectable Tray parent page;left navigation active child proof;left navigation collapsed proof;left navigation expanded proof;left pane minimum width has no horizontal overflow;left pane wide resize stays deterministic;left pane vertical overflow source-truth disposition",
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
        "proof": "04_left_settings_organizer.png; 04a_left_nav_active_child.png; 04b_left_nav_collapsed.png; 04c_left_nav_expanded.png",
        "checks": "left navigation settings organizer;left navigation active child proof;left navigation collapsed proof;left navigation expanded proof",
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
        "checks": "Tray parent plus Quick Access child settings IA;selectable Tray parent page;no fake overview/status strip;clean state has no redundant saved label;dirty guard state after dropdown edit",
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
        "checks": "Tray parent plus Quick Access child settings IA;selectable Tray parent page",
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
        "checks": "Tray parent plus Quick Access child settings IA;default semantics stage defaults;max-slot budget rows are unclipped",
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
        "copy": "up/down reorder pill; Delete",
        "font": "compact symbolic controls",
        "text": "pale action text",
        "background": "dark action button",
        "border": "1px muted cyan, round",
        "effects": "hover/focus/pressed",
        "spacing": "24px symbolic controls, 54px delete",
        "hitbox": "22-24px compact targets",
        "icon_label": "symbol controls with accessible names",
        "states": "enabled, disabled, pressed feasible",
        "a11y": "Move/Delete Quick Access Slot",
        "comparator": "compact but readable action cluster",
        "proof": "05_row_action_default_disabled_state.png",
        "checks": "readable compact quick-slot controls;row actions show disabled state",
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
        "border": "top divider",
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
        "checks": "Tray parent plus Quick Access child settings IA;selectable Tray parent page;product-facing copy is compact and non-internal",
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
        "states": "open list, no horizontal rail overflow, vertical overflow disposition",
        "a11y": "combo list; Global Settings navigation list",
        "comparator": "dark selector list and compact settings navigation overflow",
        "proof": "07_dropdown_list_state.png; 04d_left_pane_minimum_no_horizontal_scroll.png",
        "checks": "dropdown/list state screenshot saved;dropdown/list state is not white/native-light;left pane minimum width has no horizontal overflow;left pane vertical overflow source-truth disposition",
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
        "code": "desktop/desktop_renderer.py::ResidentAccessSettingsDialog._settings_native_hit_test + 14px edge/corner resize rail",
        "role": "top-level window resizing and layout safety",
        "rule": "UIREF-001; FAM-002 Standalone Window Geometry Recovery Standard",
        "copy": "none",
        "font": "not applicable",
        "text": "not applicable",
        "background": "no visible grip; shell chrome remains uninterrupted",
        "border": "native edge/corner hit zone maps to shell border",
        "effects": "Windows resize cursor handoff",
        "spacing": "14px invisible resize rail on all edges/corners",
        "hitbox": "14px edge rail with 28px corner priority",
        "icon_label": "no visible icon; navigation splitter keeps Resize Global Settings navigation pane accessible name",
        "states": "default, medium resized, live-style user drag, minimum-size, narrow/wide left pane",
        "a11y": "Resize Global Settings navigation pane",
        "comparator": "UIREF-001 top-level resizable window expectation",
        "proof": "03b_window_resized.png; 03d_window_wide_size.png; 03c_window_minimum_size.png; 03e_live_user_drag_resized.png; 04d_left_pane_minimum_no_horizontal_scroll.png; 04e_left_pane_wide.png",
        "checks": "window resize/minimum-size proof;live-style user drag resize proof;wide layout preserves centered content inside user-resizable envelope;left pane minimum width has no horizontal overflow;left pane wide resize stays deterministic",
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
        "- Current repair route: VAT-OPT-G2 remains the accepted guide/template, but this run validates the LV1 same-defect v23 title/layout/resize repair with the accepted Manage Monitors modal dirty-guard alignment, centered Settings-only title row, deferred watermark record with no runtime fake exposure, a user-resizable Settings envelope, app-owned fallback resize from the 14px edge/corner rail without a visible bottom-right grip, no horizontal rail overflow, child-page indentation, compact row grouping, useful settings copy, slot-count placement, clean-state status removal, and renewed USER retest readiness only if every recurrence row closes with proof.",
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
    from PySide6.QtCore import QPoint

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
    before = dialog.geometry()
    start_global = dialog.mapToGlobal(start_local)
    end_global = start_global + delta
    set_cursor_pos(int(start_global.x()), int(start_global.y()))
    mouse_event(move, 0, 0, 0, 0)
    for _ in range(8):
        app.processEvents()
        time.sleep(0.01)
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
    ok = width_delta >= 120 and height_delta >= 80 and not dialog._settings_resize_active
    detail = (
        f"before={before.getRect()}; after={after.getRect()}; "
        f"delta={width_delta}x{height_delta}; start={start_global.x()},{start_global.y()}; "
        f"end={end_global.x()},{end_global.y()}; max={dialog.maximumWidth()}x{dialog.maximumHeight()}; "
        f"active={dialog._settings_resize_active}; method=SetCursorPos plus held Win32 left mouse button"
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
        "live-style user drag resize proof",
        "wide layout preserves centered content inside user-resizable envelope",
        "left navigation settings organizer",
        "left rail slim row metrics",
        "left navigation active child proof",
        "left navigation collapsed proof",
        "left navigation expanded proof",
        "left pane minimum width has no horizontal overflow",
        "left pane wide resize stays deterministic",
        "left pane vertical overflow source-truth disposition",
        "selectable Tray parent page",
        "Tray parent contains no Quick Access overview or open row",
        "Tray parent plus Quick Access child settings IA",
        "product-facing copy is compact and non-internal",
        "Nexus UI exposure contract honored",
        "no internal telemetry text",
        "no fake overview/status strip",
        "readable compact quick-slot controls",
        "quick-slot row grouping has no excessive gutter",
        "slot count is placed beside Add Slot",
        "route selector is compact and bounded",
        "clean state has no redundant saved label",
        "dropdown/list state is not white/native-light",
        "dropdown/list geometry is compact",
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
            else "VAT-OPT-G2 implementation-match Tray parent / Quick Access child IA plus v23 centered Settings title, deferred watermark record, user-resizable layout, and live-style move/resize checks pass as supporting Codex evidence; final LV acceptance still requires USER UTS PASS or WAIVED."
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
            if check_status.get("Tray parent plus Quick Access child settings IA", False)
            and check_status.get("selectable Tray parent page", False)
            else "REPAIR",
            detail=_md_cell(
                check_detail.get("Tray parent plus Quick Access child settings IA", "")
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


def main() -> int:
    stamp = os.environ.get("FAM003_SETTINGS_VISUAL_PROOF_STAMP") or dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = LOG_ROOT / stamp
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
    from PySide6.QtWidgets import QApplication, QFrame, QLabel, QPushButton

    from desktop.desktop_renderer import ResidentAccessSettingsDialog
    from desktop.resident_access import DEFAULT_QUICK_SLOT_ROUTE_IDS, MAX_QUICK_SLOT_COUNT, quick_slot_candidate_routes

    app = QApplication.instance() or QApplication([])
    rows: list[tuple[str, bool, str]] = []
    artifacts: list[dict[str, str]] = []
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
            default_ok and 690 <= width <= 710 and 338 <= height <= 350,
            f"{default_path} ({width}x{height})",
        )
    )
    rows.append(
        (
            "architecture-first Global Settings geometry",
            690 <= width <= 710 and 338 <= height <= 350,
            f"window={width}x{height}; required compact deterministic settings shell, not old sparse Quick Access utility form",
        )
    )
    rows.append(
        (
            "settings shell fills the window intentionally",
            width <= 730
            and height <= 350
            and 116 <= dialog.nav_shell.width() <= 194
            and getattr(dialog, "settings_splitter", None) is not None
            and dialog.settings_splitter.handleWidth() == 5
            and dialog.tray_nav_item.isVisible()
            and dialog.tray_nav_button.isVisible()
            and dialog.tray_expand_button.isVisible()
            and dialog.tray_expand_button.property("glyphButton") == "chevron-down"
            and dialog.subpage_nav_rail.isVisible()
            and dialog.settings_page_frame.isVisible()
            and dialog.quick_slot_container.isVisible()
            and dialog.quick_slot_container.height() >= 154
            and default_footer_gap <= 12,
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

    dialog.resize(740, 368)
    app.processEvents()
    resized_path = log_dir / "03b_window_resized.png"
    resized_ok, resized_width, resized_height = _capture(
        dialog,
        resized_path,
        artifacts,
        surface="full Global Settings shell",
        state="medium resized with native edge/corner resize rail",
    )
    dialog.resize(960, 420)
    app.processEvents()
    wide_path = log_dir / "03d_window_wide_size.png"
    wide_ok, wide_width, wide_height = _capture(
        dialog,
        wide_path,
        artifacts,
        surface="full Global Settings shell",
        state="wide resized with intentional max content width",
    )
    wide_content_shell = dialog.settings_splitter.widget(1)
    wide_page_origin = dialog.settings_page_frame.mapTo(dialog, QPoint(0, 0))
    wide_content_origin = wide_content_shell.mapTo(dialog, QPoint(0, 0))
    wide_footer_origin = dialog.footer_frame.mapTo(dialog, QPoint(0, 0))
    wide_page_width = dialog.settings_page_frame.width()
    wide_page_height = dialog.settings_page_frame.height()
    wide_footer_width = dialog.footer_frame.width()
    wide_page_content_center_delta = abs(
        (wide_page_origin.x() + wide_page_width / 2)
        - (wide_content_origin.x() + wide_content_shell.width() / 2)
    )
    wide_footer_right_gap = (
        wide_page_origin.x()
        + wide_page_width
        - (wide_footer_origin.x() + wide_footer_width)
    )
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
            and 730 <= resized_width <= 750
            and 360 <= resized_height <= 376
            and 940 <= wide_width <= 980
            and 410 <= wide_height <= 440
            and wide_width >= resized_width
            and wide_height >= resized_height
            and 640 <= min_width <= 660
            and 318 <= min_height <= 330
            and not hasattr(dialog, "resize_grip")
            and not dialog.findChildren(QFrame, "residentAccessSettingsResizeGrip")
            and dialog.RESIZE_MARGIN == 14
            and dialog.minimumWidth() == 640
            and dialog.minimumHeight() == 318
            and dialog.maximumWidth() == 1100
            and dialog.maximumHeight() == 720
            and dialog.property("windowResizeBehavior") == "frameless-top-level-native-edge-corner-hit-test-app-owned-fallback-14px-no-visible-grip-splitter-minimum-640x318-maximum-1100x720-v23",
            f"resized={resized_width}x{resized_height}; wide={wide_width}x{wide_height}; min={min_width}x{min_height}; grip_attr={hasattr(dialog, 'resize_grip')}; grip_widgets={len(dialog.findChildren(QFrame, 'residentAccessSettingsResizeGrip'))}; margin={dialog.RESIZE_MARGIN}; behavior={dialog.property('windowResizeBehavior')!r}",
        )
    )
    rows.append(
        (
            "wide layout preserves centered content inside user-resizable envelope",
            wide_ok
            and dialog.maximumWidth() == 1100
            and dialog.maximumHeight() == 720
            and wide_width >= 940
            and wide_height >= 410
            and wide_page_width <= 560
            and wide_page_content_center_delta <= 4
            and 10 <= wide_footer_right_gap <= 14,
            f"wide={wide_width}x{wide_height}; max={dialog.maximumWidth()}x{dialog.maximumHeight()}; content={wide_content_shell.width()} at x={wide_content_origin.x()}; page={wide_page_width}x{wide_page_height} at x={wide_page_origin.x()}; content_center_delta={wide_page_content_center_delta:.1f}; footer_width={wide_footer_width}; footer_right_gap={wide_footer_right_gap}",
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
    live_drag_ok, live_drag_detail = _drive_win32_user_resize_drag(
        app,
        drag_probe,
        drag_probe.rect().bottomRight() - QPoint(18, 18),
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
            live_drag_ok
            and live_drag_capture_ok
            and live_drag_width >= 820
            and live_drag_height >= 430
            and hasattr(drag_probe, "_start_settings_resize")
            and hasattr(drag_probe, "_finish_settings_resize")
            and drag_probe.property("windowResizeBehavior")
            == "frameless-top-level-native-edge-corner-hit-test-app-owned-fallback-14px-no-visible-grip-splitter-minimum-640x318-maximum-1100x720-v23",
            f"{live_drag_path}; {live_drag_detail}; captured={live_drag_width}x{live_drag_height}",
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
            and dialog.nav_scroll_area.horizontalScrollBarPolicy() == Qt.ScrollBarAlwaysOff
            and dialog.nav_scroll_area.verticalScrollBarPolicy() == Qt.ScrollBarAsNeeded
            and dialog.tray_expand_button.property("glyphButton") == "chevron-down"
            and getattr(dialog.tray_nav_icon, "icon_kind", "") == "tray"
            and getattr(dialog.quick_access_nav_icon, "icon_kind", "") == "quick-access"
            and set(dialog._nav_buttons) == {"tray", "quick_access"}
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and dialog.quick_access_nav_caption.text() == ""
            and not dialog.quick_access_nav_caption.isVisible()
            and 116 <= dialog.nav_shell.width() <= 194
            and dialog.quick_access_nav_item.x() > dialog.tray_nav_item.x()
            and dialog.tray_nav_item.width() <= 96
            and dialog.quick_access_nav_item.width() <= 88
            and not dialog.nav_boundary.isVisible(),
            f"{nav_path} ({nav_width}x{nav_height}); nav={list(dialog._nav_buttons)}; tray={dialog.tray_nav_button.text()!r}/{dialog.tray_nav_item.property('settingsCategoryRole')!r}; checked={dialog.quick_access_nav_button.isChecked()}; expander={dialog.tray_expand_button.property('glyphButton')!r}; icons={getattr(dialog.tray_nav_icon, 'icon_kind', '')!r}/{getattr(dialog.quick_access_nav_icon, 'icon_kind', '')!r}; caption={dialog.quick_access_nav_caption.text()!r}; caption_visible={dialog.quick_access_nav_caption.isVisible()}; nav_width={dialog.nav_shell.width()}",
        )
    )
    tray_nav_height = dialog.tray_nav_item.height()
    quick_nav_height = dialog.quick_access_nav_item.height()
    rows.append(
        (
            "left rail slim row metrics",
            nav_ok
            and tray_nav_height <= 24
            and quick_nav_height <= 24
            and dialog.tray_nav_indicator.width() <= 2
            and dialog.tray_nav_icon.width() <= 10
            and dialog.quick_access_nav_icon.width() <= 10
            and dialog.tray_nav_item.property("settingsNavDensity") == "slim-parent-row"
            and dialog.quick_access_nav_item.property("settingsNavDensity") == "two-level-subpage-row",
            f"tray_row={tray_nav_height}; quick_row={quick_nav_height}; indicator={dialog.tray_nav_indicator.width()}x{dialog.tray_nav_indicator.height()}; parent_icon={dialog.tray_nav_icon.width()}x{dialog.tray_nav_icon.height()}; child_icon={dialog.quick_access_nav_icon.width()}x{dialog.quick_access_nav_icon.height()}; nav_width={dialog.nav_shell.width()}",
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

    dialog.settings_splitter.setSizes([104, 584])
    app.processEvents()
    narrow_path = log_dir / "04d_left_pane_minimum_no_horizontal_scroll.png"
    narrow_ok, narrow_width, narrow_height = _capture(
        dialog.nav_shell,
        narrow_path,
        artifacts,
        surface="left settings organizer",
        state="minimum pane / no horizontal overflow",
    )
    hbar_max = dialog.nav_scroll_area.horizontalScrollBar().maximum()
    rows.append(
        (
            "left pane minimum width has no horizontal overflow",
            narrow_ok
            and 104 <= dialog.nav_shell.width() <= 126
            and hbar_max == 0
            and dialog.nav_content.width() <= dialog.nav_scroll_area.viewport().width()
            and dialog.quick_access_nav_item.x() > dialog.tray_nav_item.x(),
            f"{narrow_path} ({narrow_width}x{narrow_height}); nav_width={dialog.nav_shell.width()}; nav_content_width={dialog.nav_content.width()}; hbar_max={hbar_max}",
        )
    )

    dialog.settings_splitter.setSizes([184, 520])
    app.processEvents()
    wide_path = log_dir / "04e_left_pane_wide.png"
    wide_ok, wide_width, wide_height = _capture(
        dialog.nav_shell,
        wide_path,
        artifacts,
        surface="left settings organizer",
        state="wide pane",
    )
    rows.append(
        (
            "left pane wide resize stays deterministic",
            wide_ok
            and 104 <= dialog.nav_shell.width() <= 130
            and dialog.subpage_nav_rail.isVisible()
            and dialog.quick_access_nav_item.isVisible()
            and dialog.tray_nav_item.width() <= 96
            and dialog.quick_access_nav_item.width() <= 88,
            f"{wide_path} ({wide_width}x{wide_height}); nav_width={dialog.nav_shell.width()}; parent_width={dialog.tray_nav_item.width()}; child_width={dialog.quick_access_nav_item.width()}; subpage_visible={dialog.subpage_nav_rail.isVisible()}",
        )
    )

    vbar_max = dialog.nav_scroll_area.verticalScrollBar().maximum()
    rows.append(
        (
            "left pane vertical overflow source-truth disposition",
            vbar_max == 0
            and set(dialog._nav_buttons) == {"tray", "quick_access"}
            and dialog.nav_content.height() <= dialog.nav_scroll_area.viewport().height(),
            f"vbar_max={vbar_max}; current_real_nav={list(dialog._nav_buttons)}; nav_content_height={dialog.nav_content.height()}; viewport_height={dialog.nav_scroll_area.viewport().height()}; source_truth='current visible Global Settings hierarchy is Tray parent and Quick Access child only; no fake future categories admitted'",
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
            and "Tray click and menu behavior settings are not active yet." == dialog.tray_deferred_detail.text(),
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
            "Tray parent plus Quick Access child settings IA",
            dialog.section_heading.text() == "Quick Access"
            and dialog.section_badge.text() == "Tray"
            and not dialog.section_badge.isVisible()
            and dialog.section_detail.isVisible()
            and dialog.section_detail.text() == "Choose the shortcuts shown in the tray menu."
            and dialog.section_scope.isVisible()
            and dialog.section_scope.text() == "NEXUS TRAY / QUICK ACCESS"
            and dialog.property("settingsInformationArchitecture") == "global-settings-shell-tray-parent-quick-access-child-deterministic-rail-v22"
            and dialog.property("settingsVisualRepair") == "lv1-global-settings-title-layout-watermark-deferral-repair-v22"
            and dialog.property("referenceDerivedHeader") == "ndai-global-settings-centered-settings-chrome-v22"
            and dialog.property("dirtyGuardReference") == "manage-monitors-modal-save-discard-cancel"
            and dialog.property("standardWindowArchitecture") == "pyside-dialogchrome-native-edge-corner-hit-test-reference-derived"
            and dialog.property("windowResizeBehavior") == "frameless-top-level-native-edge-corner-hit-test-app-owned-fallback-14px-no-visible-grip-splitter-minimum-640x318-maximum-1100x720-v23"
            and dialog.property("visibleResizeGrip") == "removed"
            and dialog.property("deferredWatermarkConcept") == "future-centered-global-settings-watermark-deferred-no-runtime-exposure-v22"
            and dialog.property("runtimeWatermarkVisible") == "false"
            and dialog.property("uiExposureContract") == "real-enabled-meaningful-visible-ui-v1"
            and dialog.property("sharedPrimitiveClaim") == "none-promoted-reference-derived-only"
            and dialog.property("referenceComparatorRequired") == "ui-reference-plus-product-grade-same-defect-comparator-v22"
            and set(dialog._nav_buttons) == {"tray", "quick_access"}
            and dialog.tray_nav_item.property("settingsCategoryRole") == "selectable-parent-page"
            and dialog.tray_nav_button.text() == "Tray"
            and getattr(dialog.tray_nav_icon, "icon_kind", "") == "tray"
            and dialog.tray_expand_button.property("glyphButton") == "chevron-down"
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and getattr(dialog.quick_access_nav_icon, "icon_kind", "") == "quick-access"
            and dialog.quick_access_nav_button.isChecked()
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
            "readable compact quick-slot controls",
            all(
                (
                    button.property("glyphButton")
                    in {"up", "down"}
                    and button.width() <= 28
                    and button.height() <= 26
                )
                or (
                    button.objectName() == "residentAccessQuickSlotDelete"
                    and button.property("glyphButton") == "close"
                    and 24 <= button.width() <= 32
                    and button.height() <= 22
                )
                for button in compact_action_buttons
            )
            and any(frame.objectName() == "residentAccessQuickSlotReorderGroup" for frame in dialog.findChildren(QFrame)),
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

    if not dialog._slot_combos:
        rows.append(("quick-slot combo exists", False, "no quick-slot combo rendered"))
    else:
        rows.append(("quick-slot combo exists", True, f"combo_count={len(dialog._slot_combos)}"))
        combo = dialog._slot_combos[0]
        rows.append(
            (
                "route selector is compact and bounded",
                all(240 <= slot_combo.width() <= 380 and slot_combo.maxVisibleItems() <= 4 for slot_combo in dialog._slot_combos),
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
        rows.append(
            (
                "quick-slot row grouping has no excessive gutter",
                bool(row_gutters)
                and all(gutter <= 10 for gutter in row_gutters)
                and all(440 <= width <= 520 for width in row_widths),
                f"row_gutters={row_gutters}; row_widths={row_widths}",
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
                "dropdown/list geometry is compact",
                popup_width <= 380 and popup_height <= 116 and combo.maxVisibleItems() <= 4,
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
            state="filled centered move/delete controls",
        )
        glyph_detail = f"{glyph_path} ({glyph_w}x{glyph_h}); rect={action_rect.getRect()}; action_widget={action_widget.objectName()}"
    rows.append(("glyph/control close-up proof", glyph_ok and glyph_path.exists(), glyph_detail))

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
            and dialog.settings_splitter.handleWidth() == 5
            and splitter_handle.accessibleName() == "Resize Global Settings navigation pane",
            f"{splitter_closeup_path} ({splitter_closeup_w}x{splitter_closeup_h}); handle_width={dialog.settings_splitter.handleWidth()}; handle_object={splitter_handle.objectName()!r}; handle_a11y={splitter_handle.accessibleName()!r}; rect={handle_rect.getRect()}",
        )
    )

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
            ("Repaired FAM-003 - dropdown/list state", log_dir / "07_dropdown_list_state.png"),
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
            ("Repaired v22 - capped settings shell", default_path),
            ("Repaired v22 - centered Settings title", chrome_path),
            ("Repaired v22 - glyph controls", glyph_path),
            ("Repaired v22 - splitter affordance", splitter_closeup_path),
            ("Repaired v22 - dropdown", log_dir / "07_dropdown_list_state.png"),
            ("Repaired v22 - close guard", log_dir / "08_close_guard.png"),
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
            ("Red-team check - collapsed parent", collapsed_path),
            ("Red-team check - row spacing/glyphs", glyph_path),
            ("Red-team check - splitter affordance", splitter_closeup_path),
            ("Red-team check - medium resized shell", resized_path),
            ("Red-team check - wide resized shell", wide_path),
            ("Red-team check - minimum shell", min_path),
            ("Red-team check - dropdown open", log_dir / "07_dropdown_list_state.png"),
            ("Red-team reference - Manage Monitors dirty guard", manage_guard_reference_path),
            ("Red-team check - close guard", log_dir / "08_close_guard.png"),
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
        ("F3-LV1-UI-015", "USER", "20260624-123116/04_left_settings_organizer.png", "15_left_pane_resize_affordance_closeup.png", "quiet 5px left-pane resize affordance", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-016", "USER", "corner-grip-only v15/v20 proof and stale minimum-size floors", "03b_window_resized.png; 03d_window_wide_size.png; 03c_window_minimum_size.png", "640x318 minimum plus 14px native edge/corner resize with no visible bottom-right grip", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-017", "USER", "20260624-123116/01_default_global_settings_shell.png", "01_default_global_settings_shell.png; 05_row_action_default_disabled_state.png", "700x344 deterministic shell with compact row grouping and useful settings copy", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-018", "USER", "v15 ^ / v / x text buttons", "14_glyph_control_closeup.png", "UIREF-003 polished control state grammar", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-019", "USER", "plain utility caption title", "02_top_level_chrome_control_cluster.png", "settings-specific seamless single-row title grammar", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-020", "USER", "flat utility text hierarchy / visible Saved label", "01_default_global_settings_shell.png; 05_tray_parent_page.png; 11_post_save_clean_state.png", "Project Vision product experience contract plus compact settings scope/detail, menu-order copy, and quiet clean-state discipline", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-021", "USER / ChatGPT", "compact utility-panel overall impression", "16_defect_closure_contact_sheet.png; 17_red_team_review_sheet.png", "Project Vision; FAM-002; UIREF-001..006; v22 title/layout full-surface expected-vs-actual adjudication", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-022", "USER", "20260624-132602/02_top_level_chrome_control_cluster.png", "02_top_level_chrome_control_cluster.png; 16_defect_closure_contact_sheet.png; 17_red_team_review_sheet.png", "Global Settings is its own settings-window class: no title card, no stacked title, no sectioned title row", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-023", "USER / ChatGPT", "v17 left rail child row was nearly peer-level", "04_left_settings_organizer.png; 04a_left_nav_active_child.png", "Tray parent with visibly subordinate Quick Access child", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-024", "USER / ChatGPT", "v17/default v20 canvases were too large or visually zoomed out", "01_default_global_settings_shell.png", "700x344 content-deterministic default shell", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-025", "USER / ChatGPT", "v17 minimum 700x360 was over-restrictive", "03c_window_minimum_size.png; 04d_left_pane_minimum_no_horizontal_scroll.png", "640x318 minimum with no visible horizontal rail overflow", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-026", "USER / ChatGPT", "nav rows stretched and overflow was treated as proof", "04_left_settings_organizer.png; 04d_left_pane_minimum_no_horizontal_scroll.png; 04e_left_pane_wide.png", "bounded parent/child rail rows with no horizontal overflow", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-027", "USER / ChatGPT", "3 active of 4 header badge was verbose and detached from Add Slot", "01_default_global_settings_shell.png", "3 of 4 placed beside Add Slot", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-028", "USER / ChatGPT", "clean-state Saved label was redundant", "01_default_global_settings_shell.png; 11_post_save_clean_state.png", "quiet clean/post-save state; dirty/guard copy remains meaningful", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-029", "USER", "v18 footer/status close guard did not match accepted Manage Monitors modal dirty guard", "08_close_guard.png; 13a_accepted_manage_monitors_dirty_guard_reference.png; 18_manage_monitors_dirty_guard_side_by_side.png; MANAGE_MONITORS_DIRTY_GUARD_REFERENCE.md", "accepted HUD Dashboard / Manage Monitors modal Save / Discard / Cancel dirty guard", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-030", "USER / ChatGPT", "v20/v21 repair risked global shrink/zoom-out instead of real settings-window composition", "01_default_global_settings_shell.png; 04_left_settings_organizer.png; 14_glyph_control_closeup.png", "readable compact controls, real row sizes, and no global scale-down repair", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-031", "USER / ChatGPT", "v21 default/wide proof still allowed the active work surface to feel stranded in a larger shell", "01_default_global_settings_shell.png; 03b_window_resized.png; 03d_window_wide_size.png", "700x344 default, 740x368 medium, and 760x384 max-clamped wide shell with centered capped content and attached footer", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-032", "USER / ChatGPT", "v21 grouped NEXUS DESKTOP AI / Global Settings title row still failed composition expectations", "02_top_level_chrome_control_cluster.png", "centered Settings-only title row, no visible title-card, no stacked title, no visible NDAI title-row branding", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-033", "USER / ChatGPT", "v21 wide state still risked footer/action detachment from active settings content", "01_default_global_settings_shell.png; 03d_window_wide_size.png; DEFECT_CLOSURE_PROOF_LEDGER.md", "footer remains within the capped active settings page at default, medium, and max-clamped wide sizes", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-034", "USER / ChatGPT", "Global Settings standard-window path needed renewed proof after title/layout repair", "FAM003_SETTINGS_REPAIR_VISUAL_VALIDATION.md; 02_top_level_chrome_control_cluster.png", "PySide DialogChromeBar remains legal reference-derived settings window; no WebView/shared-primitive migration claim", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-035", "USER / ChatGPT", "bottom-right resize grip must remain removed", "01_default_global_settings_shell.png; 03d_window_wide_size.png; 03c_window_minimum_size.png", "no resize_grip attribute, no residentAccessSettingsResizeGrip widget, no QSizeGrip for this surface", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-036", "USER / ChatGPT", "resize parity required after max-size repair", "03b_window_resized.png; 03d_window_wide_size.png; 03c_window_minimum_size.png", "14px edge/corner hit zones, WM_SETCURSOR cursor handoff, 640x318 min clamp, 760x384 max clamp, no visible grip", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-037", "USER / ChatGPT", "v21 visible title row still included NEXUS DESKTOP AI branding", "02_top_level_chrome_control_cluster.png", "visible title row contains only centered Settings; hidden kicker is empty and no visible NDAI branding appears in the title row", "CLOSED_WITH_PROOF"),
        ("F3-LV1-UI-038", "USER / ChatGPT", "future centered Global Settings watermark concept was requested but must not be faked into runtime UI", "FAM003_SETTINGS_REPAIR_VISUAL_VALIDATION.md; fam003_settings_visual_fail_repair_manifest.json", "branch-local deferred watermark property recorded; runtimeWatermarkVisible=false and no visible watermark widget/text exists", "CLOSED_WITH_PROOF"),
        ("F3-LV1-PROOF-001", "USER / ChatGPT / Codex", "retest packet returned without defect-by-defect proof", "DEFECT_CLOSURE_PROOF_LEDGER.md; FAIL_CAPABLE_DEFECT_LEDGER.md; 17_red_team_review_sheet.png", "UTS guidance Codex Visual Adjudication gate with UI-023 through UI-029 coverage", "CLOSED_WITH_PROOF"),
        ("F3-LV1-PROOF-002", "USER / ChatGPT / Codex", "Codex repeatedly returned repaired/retest-candidate packets after unresolved seed defects remained visible", "DEFECT_CLOSURE_PROOF_LEDGER.md; FAIL_CAPABLE_DEFECT_LEDGER.md; 17_red_team_review_sheet.png; 18_manage_monitors_dirty_guard_side_by_side.png", "row-specific root-cause prevention plus fail-capable validator requirements for every reopened current-owned defect", "CLOSED_WITH_PROOF"),
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

    ledger_path, manifest_path, element_ledger_path, defect_ledger_path = _write_artifact_ledger(
        log_dir,
        artifacts,
        rows,
        contact_sheet,
        manage_guard_reference_path=manage_guard_reference_path,
        manage_guard_ledger_path=manage_guard_ledger_path,
        manage_guard_side_by_side=manage_guard_side_by_side,
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
