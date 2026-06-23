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
        "font": "Bahnschrift/Rajdhani/Segoe UI, 10-29px",
        "text": "#f8fafc family",
        "background": "#020914 / #04101b dark shell",
        "border": "1px restrained cyan, 20px radius",
        "effects": "subtle depth only",
        "spacing": "860x560 compact two-column settings layout",
        "hitbox": "top-level window with normal resize baseline",
        "icon_label": "window title plus product kicker",
        "states": "default, dirty, saved",
        "a11y": "window title Global Settings",
        "comparator": "accepted AI Control Center full-window reference",
        "proof": "01_default_global_settings_shell.png",
        "checks": "default screenshot saved;architecture-first Global Settings geometry;settings shell fills the window intentionally;default surface is not white/native-light",
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
        "role": "integrated settings anatomy",
        "rule": "UIREF-001; UIREF-005",
        "copy": "Settings",
        "font": "header 29px, subtitle 13px",
        "text": "near-white plus muted cyan",
        "background": "dark header to dark body",
        "border": "single header divider",
        "effects": "reference-family depth",
        "spacing": "hero header above content",
        "hitbox": "header and body zones",
        "icon_label": "product title labels",
        "states": "default",
        "a11y": "Close Global Settings",
        "comparator": "accepted AI Control Center header/body relationship",
        "proof": "02_top_level_chrome_control_cluster.png",
        "checks": "top-level chrome/control cluster;compact settings product header",
    },
    {
        "id": "F3GS-004",
        "element": "Product title group",
        "surface": "Global Settings chrome",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::DialogChromeBar title labels",
        "role": "product identity and settings title",
        "rule": "Project Vision; UIREF-001",
        "copy": "Settings",
        "font": "11px kicker, 29px title, 13px subtitle",
        "text": "cyan kicker, near-white title, muted subtitle",
        "background": "transparent on chrome bar",
        "border": "none",
        "effects": "none",
        "spacing": "AI Control Center family rhythm",
        "hitbox": "label group",
        "icon_label": "text-only product group",
        "states": "default",
        "a11y": "window title",
        "comparator": "accepted AI Control Center product/title hierarchy",
        "proof": "02_top_level_chrome_control_cluster.png",
        "checks": "compact settings product header",
    },
    {
        "id": "F3GS-005",
        "element": "Header product discipline",
        "surface": "Global Settings chrome",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsChromeRolePill",
        "role": "compact settings context",
        "rule": "UIREF-006",
        "copy": "no visible role/status pill; no SETTINGS AREA / ACTIVE SETTING metadata",
        "font": "10px bold",
        "text": "soft mint",
        "background": "not applicable",
        "border": "not applicable",
        "effects": "no branch/debug/status metadata",
        "spacing": "header stays title/subtitle/control focused",
        "hitbox": "not applicable",
        "icon_label": "no extra visual label",
        "states": "default",
        "a11y": "header remains product title and window controls",
        "comparator": "accepted AI Control Center status/context pill",
        "proof": "02_top_level_chrome_control_cluster.png",
        "checks": "compact settings product header;no internal telemetry text;product-facing copy is compact and non-internal",
    },
    {
        "id": "F3GS-006",
        "element": "Window control cluster",
        "surface": "Global Settings chrome",
        "fam": "FAM-003 / FAM-002 visual authority",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsWindowControls",
        "role": "NDAI minimize/close controls",
        "rule": "UIREF-002; UIREF-003",
        "copy": "- and x controls",
        "font": "control glyph 900 weight",
        "text": "near-white",
        "background": "dark rounded cluster",
        "border": "1px cyan, 18px radius",
        "effects": "focus/pressed color change",
        "spacing": "28px buttons",
        "hitbox": "28x28 controls",
        "icon_label": "glyph-only with accessible names",
        "states": "focus, pressed",
        "a11y": "Close Global Settings",
        "comparator": "accepted AI Control Center close-hover reference",
        "proof": "03_window_control_focus_pressed_state.png",
        "checks": "top-level chrome/control cluster;window control focus/pressed proof",
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
        "background": "transparent rail",
        "border": "right divider",
        "effects": "no fake future categories",
        "spacing": "142px slim rail",
        "hitbox": "left column",
        "icon_label": "category and selected page label",
        "states": "Quick Access selected",
        "a11y": "Open Quick Access Settings",
        "comparator": "dense settings navigation grammar",
        "proof": "04_left_settings_organizer.png",
        "checks": "left navigation settings organizer;single actionable page inside Global Settings IA",
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
        "icon_label": "small gear mark plus main/subcategory labels",
        "states": "selected, hover/focus feasible",
        "a11y": "Open Quick Access Settings",
        "comparator": "settings nav row, not CTA card",
        "proof": "04_left_settings_organizer.png",
        "checks": "left navigation settings organizer",
    },
    {
        "id": "F3GS-009",
        "element": "Settings context strip",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsOverviewPanel",
        "role": "product-native settings context",
        "rule": "Project Vision; F3-FF01",
        "copy": "Saved",
        "font": "11-13px product context",
        "text": "near-white title, muted detail, mint state chip",
        "background": "subtle dark strip",
        "border": "restrained left accent only",
        "effects": "quiet state chip",
        "spacing": "single compact strip",
        "hitbox": "context strip",
        "icon_label": "title/detail/state chip",
        "states": "saved, dirty",
        "a11y": "change status propagated",
        "comparator": "AI Control Center dense state rows",
        "proof": "01_default_global_settings_shell.png; 06_dirty_quick_access.png",
        "checks": "single actionable page inside Global Settings IA;no fake overview/status strip;initial saved-state copy;dirty guard state after dropdown edit",
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
        "font": "18px heading, 10-11px metadata",
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
        "checks": "single actionable page inside Global Settings IA",
    },
    {
        "id": "F3GS-011",
        "element": "Quick Access slot group",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessQuickSlotContainer",
        "role": "current settings control group",
        "rule": "F3-FF01; UIREF-003",
        "copy": "Slots; Add; Defaults; Top to bottom sets menu order.",
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
        "checks": "single actionable page inside Global Settings IA;default semantics stage defaults;max-slot budget rows are unclipped",
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
        "spacing": "compact 7/4 margins",
        "hitbox": "row height about 38px",
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
        "spacing": "34px min height",
        "hitbox": "250px min width",
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
        "spacing": "26px buttons",
        "hitbox": "24-30px compact targets",
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
        "copy": "Unsaved changes / Default shortcut order staged / Saved",
        "font": "11px body",
        "text": "light cyan",
        "background": "dark cyan status bar",
        "border": "1px muted cyan, 12px radius",
        "effects": "appears only when meaningful",
        "spacing": "below page detail",
        "hitbox": "full content width",
        "icon_label": "text status",
        "states": "hidden, dirty, default, saved",
        "a11y": "Quick Access change status",
        "comparator": "NDAI recovery/status strip",
        "proof": "06_dirty_quick_access.png; 09_defaults_staged.png; 11_saved_state.png",
        "checks": "initial saved-state copy;dirty guard state after dropdown edit;default semantics stage defaults;save clears dirty state",
    },
    {
        "id": "F3GS-019",
        "element": "Footer action zone",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::residentAccessSettingsFooter",
        "role": "deterministic settings actions",
        "rule": "UIREF-003; F3-FF01",
        "copy": "Revert; Save; Done; guard-only Cancel/Discard",
        "font": "10pt buttons",
        "text": "pale action text",
        "background": "transparent footer",
        "border": "top divider",
        "effects": "save emphasis when enabled",
        "spacing": "right aligned",
        "hitbox": "28px min-height buttons",
        "icon_label": "text actions",
        "states": "disabled, enabled, guard",
        "a11y": "Save/Revert/Done settings",
        "comparator": "NDAI action bar hierarchy",
        "proof": "06_dirty_quick_access.png; 08_close_guard.png; 11_saved_state.png",
        "checks": "initial saved-state copy;dirty guard state after dropdown edit;close guard blocks silent loss;save clears dirty state",
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
        "checks": "row actions show disabled state;initial saved-state copy",
    },
    {
        "id": "F3GS-021",
        "element": "Close guard",
        "surface": "Global Settings modal state",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::_request_close",
        "role": "prevent silent data loss",
        "rule": "UIREF-004; Project Vision",
        "copy": "Unsaved changes - Save, discard, or cancel before closing.",
        "font": "11px status plus buttons",
        "text": "light cyan / red discard",
        "background": "dark status/footer",
        "border": "muted status borders",
        "effects": "guard-only actions appear",
        "spacing": "footer action row",
        "hitbox": "guard action buttons",
        "icon_label": "Cancel / Discard",
        "states": "blocked close",
        "a11y": "Cancel Close",
        "comparator": "NDAI recovery/guard pattern",
        "proof": "08_close_guard.png",
        "checks": "close guard screenshot saved;close guard blocks silent loss",
    },
    {
        "id": "F3GS-022",
        "element": "Saved state",
        "surface": "Global Settings content",
        "fam": "FAM-003",
        "code": "desktop/desktop_renderer.py::_save_settings",
        "role": "post-save truth alignment",
        "rule": "Project Vision; backend predictability",
        "copy": "Saved.",
        "font": "11px status",
        "text": "light cyan",
        "background": "status strip",
        "border": "status border",
        "effects": "save/revert disabled",
        "spacing": "same layout",
        "hitbox": "status and footer controls",
        "icon_label": "Save disabled",
        "states": "saved",
        "a11y": "change status",
        "comparator": "deterministic saved state",
        "proof": "11_saved_state.png",
        "checks": "save clears dirty state;saved state screenshot saved",
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
        "checks": "single actionable page inside Global Settings IA;product-facing copy is compact and non-internal",
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
        "rule": "UIREF-003",
        "copy": "route labels with future-gated suffixes where applicable",
        "font": "popup items",
        "text": "#c1d5d0",
        "background": "#08121e",
        "border": "#2b7485",
        "effects": "selection highlight",
        "spacing": "maximum height 178",
        "hitbox": "bounded popup",
        "icon_label": "list rows",
        "states": "open list",
        "a11y": "combo list",
        "comparator": "dark selector list",
        "proof": "07_dropdown_list_state.png",
        "checks": "dropdown/list state screenshot saved;dropdown/list state is not white/native-light",
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
        "comparator": "accepted AI Control Center and repaired Global Settings",
        "proof": "REFERENCE_CONFORMANCE_CONTACT_SHEET.png",
        "checks": "side-by-side reference contact sheet written;accepted reference available: accepted_ai_control_center_default;accepted reference available: accepted_ai_control_center_close_hover",
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
    painter.drawText(18, 24, "FAM-003 Settings-Specific Visual Conformance Contact Sheet")
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
        "- Current failure digestion: the prior packet is traceable evidence but is not accepted for USER retest; this run repairs and re-proves the Global Settings / Quick Access visual product surface.",
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
        "settings shell fills the window intentionally",
        "compact settings product header",
        "left navigation settings organizer",
        "single actionable page inside Global Settings IA",
        "product-facing copy is compact and non-internal",
        "Nexus UI exposure contract honored",
        "no internal telemetry text",
        "no fake overview/status strip",
        "readable compact quick-slot controls",
        "dropdown/list state is not white/native-light",
        "close guard blocks silent loss",
        "save clears dirty state",
    ]
    conformance_failed = [name for name in conformance_checks if not check_status.get(name, False)]
    conformance_result = "REPAIR" if conformance_failed else "PASS"
    conformance_detail = (
        "; ".join(f"{name}: {check_detail.get(name, '')}" for name in conformance_failed)
        if conformance_failed
        else "V10 settings IA / UI Exposure Contract checks pass as supporting Codex evidence; final LV acceptance still requires USER UTS PASS or WAIVED."
    )
    ledger_path = log_dir / "FAIL_CAPABLE_DEFECT_LEDGER.md"
    ledger_lines = [
        "# FAM-003 Fail-Capable Visual Defect Ledger",
        "",
        "Scope: Global Settings / Nexus Tray / Quick Access settings surface.",
        "Prior Packet Under Review: `C:\\Nexus USER\\FAM-003-20260622-200820.zip`.",
        "Prior Packet Disposition: `REPAIR - traceable but not accepted for USER retest because visual/product conformance failed.`",
        "",
        "| Evidence Layer | Result | Detail |",
        "| --- | --- | --- |",
        "| Structure exists | {result} | {detail} |".format(
            result="PASS" if check_status.get("single actionable page inside Global Settings IA", False) else "REPAIR",
            detail=_md_cell(check_detail.get("single actionable page inside Global Settings IA", "")),
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
        "Reference class: UIREF-001 through UIREF-006 plus accepted AI Control Center top-level window evidence.",
        "Proof model: settings-specific contact sheet, focused screenshots, code-to-visual widget/objectName trace, and fail-capable defect ledger. USER-operated Live Validation remains required.",
        "Accepted-reference boundary: AI Control Center is the accepted NDAI visual-language comparator, not a Global Settings layout template or shared primitive claim.",
        "",
        "## Scope Coverage Manifest",
        "",
        "- Reviewed files: desktop/desktop_renderer.py, desktop/resident_access.py, dev/orin_fam003_settings_repair_visual_validation.py.",
        "- Reviewed windows/surfaces: Global Settings shell, chrome/control cluster, left organizer, settings overview, Quick Access page, slot rows, dropdown/list, row actions, footer, dirty/default/save/close-guard states.",
        "- Reviewed artifacts: default screenshot, chrome/control screenshot, focus/pressed screenshot, left organizer screenshot, row-action screenshot, dirty screenshot, dropdown/list screenshot, close-guard screenshot, defaults-staged screenshot, max-slot screenshot, saved-state screenshot, accepted AI Control Center reference screenshots, and contact sheet.",
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
                        "settings overview",
                        "Quick Access page",
                        "slot rows",
                        "dropdown/list",
                        "row actions",
                        "footer",
                        "dirty/default/save/close-guard states",
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
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
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

    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication, QFrame, QPushButton

    from desktop.desktop_renderer import ResidentAccessSettingsDialog
    from desktop.resident_access import DEFAULT_QUICK_SLOT_ROUTE_IDS, MAX_QUICK_SLOT_COUNT, quick_slot_candidate_routes

    app = QApplication.instance() or QApplication([])
    rows: list[tuple[str, bool, str]] = []
    artifacts: list[dict[str, str]] = []
    rows.extend(_copy_reference_artifacts(log_dir, artifacts))

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
    rows.append(
        (
            "default screenshot saved",
            default_ok and 740 <= width <= 790 and 360 <= height <= 385,
            f"{default_path} ({width}x{height})",
        )
    )
    rows.append(
        (
            "architecture-first Global Settings geometry",
            740 <= width <= 790 and 360 <= height <= 385,
            f"window={width}x{height}; required compact settings shell, not old sparse Quick Access utility form",
        )
    )
    rows.append(
        (
            "settings shell fills the window intentionally",
            width >= 740
            and height <= 385
            and 138 <= dialog.nav_shell.width() <= 150
            and not dialog.primary_nav_rail.isVisible()
            and dialog.subpage_nav_rail.isVisible()
            and dialog.settings_page_frame.isVisible()
            and dialog.quick_slot_container.isVisible()
            and dialog.quick_slot_container.height() >= 170,
            f"window={width}x{height}; nav_width={dialog.nav_shell.width()}; primary_visible={dialog.primary_nav_rail.isVisible()}; subpage_visible={dialog.subpage_nav_rail.isVisible()}; page_visible={dialog.settings_page_frame.isVisible()}; slot_panel_height={dialog.quick_slot_container.height()}",
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
            and dialog.chrome_bar.property("headerAnatomy") == "compact-dialog-bar"
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
            "compact settings product header",
            dialog.chrome_bar.kicker_label.text() == ""
            and dialog.chrome_bar.title_label.text() == "Global Settings"
            and dialog.chrome_bar.subtitle_label.text() == ""
            and role_text == []
            and not dialog.chrome_bar.role_pill.isVisible(),
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
            and not dialog.primary_nav_rail.isVisible()
            and dialog.primary_tray_button.isChecked()
            and dialog.primary_tray_button.text() == "\N{GEAR}"
            and dialog.primary_tray_button.width() <= 24
            and dialog.primary_tray_button.height() <= 24
            and dialog.tray_category_label.isVisible()
            and dialog.tray_category_label.text() == "Tray"
            and dialog.tray_category_label.property("settingsCategoryRole") == "real-category-no-direct-page"
            and dialog.subpage_nav_rail.isVisible()
            and dialog.quick_access_nav_button.isChecked()
            and dialog.quick_access_nav_item.isVisible()
            and dialog.quick_access_nav_item.property("settingsNavDensity") == "two-level-subpage-row"
            and dialog.quick_access_nav_item.property("settingsNavIdentity") == "ndai-signal-leaf"
            and dialog.nav_shell.property("settingsShellIdentity") == "ndai-slim-global-settings"
            and set(dialog._nav_buttons) == {"quick_access"}
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and dialog.quick_access_nav_caption.text() == ""
            and not dialog.quick_access_nav_caption.isVisible()
            and 138 <= dialog.nav_shell.width() <= 150
            and not dialog.nav_boundary.isVisible(),
            f"{nav_path} ({nav_width}x{nav_height}); nav={list(dialog._nav_buttons)}; primary_visible={dialog.primary_nav_rail.isVisible()}; category={dialog.tray_category_label.text()!r}/{dialog.tray_category_label.isVisible()}; checked={dialog.quick_access_nav_button.isChecked()}; caption={dialog.quick_access_nav_caption.text()!r}; caption_visible={dialog.quick_access_nav_caption.isVisible()}; nav_width={dialog.nav_shell.width()}",
        )
    )

    button_texts = [button.text().replace("&&", "&") for button in dialog.findChildren(QPushButton)]
    compact_action_buttons = [
        button
        for button in dialog.findChildren(QPushButton)
        if button.objectName() in {"residentAccessQuickSlotMoveUp", "residentAccessQuickSlotMoveDown", "residentAccessQuickSlotDelete"}
    ]
    rows.append(
        (
            "single actionable page inside Global Settings IA",
            dialog.section_heading.text() == "Quick Access"
            and dialog.section_badge.text() == "Tray"
            and not dialog.section_badge.isVisible()
            and not dialog.section_detail.isVisible()
            and not dialog.section_scope.isVisible()
            and dialog.property("settingsInformationArchitecture") == "global-settings-shell-tray-category-quick-access-subpage-v10"
            and dialog.property("settingsVisualRepair") == "settings-ia-exposure-contract-v10"
            and dialog.property("referenceDerivedHeader") == "compact-ndai-settings-window-frame-v10"
            and dialog.property("uiExposureContract") == "real-enabled-meaningful-visible-ui-v1"
            and dialog.property("sharedPrimitiveClaim") == "none-promoted-reference-derived-only"
            and dialog.property("referenceComparatorRequired") == "accepted-ai-control-center-contact-sheet"
            and set(dialog._nav_buttons) == {"quick_access"}
            and dialog.tray_category_label.text() == "Tray"
            and dialog.quick_access_nav_button.text() == "Quick Access"
            and dialog.quick_access_nav_button.isChecked()
            and dialog.slot_count_badge.text() == f"{len(DEFAULT_QUICK_SLOT_ROUTE_IDS)}/{active_slot_limit} slots"
            and dialog.settings_page_frame.objectName() == "residentAccessSettingsPageFrame"
            and dialog.settings_state_chip.text() == "Saved"
            and dialog.quick_slot_container.objectName() == "residentAccessQuickSlotContainer"
            and dialog.footer_frame.objectName() == "residentAccessSettingsFooter"
            and not dialog.route_summary.isVisible(),
            f"heading={dialog.section_heading.text()!r}; category={dialog.tray_category_label.text()!r}; section_badge_visible={dialog.section_badge.isVisible()}; detail_visible={dialog.section_detail.isVisible()}; slot_badge={dialog.slot_count_badge.text()!r}; nav={list(dialog._nav_buttons)}; buttons={button_texts}; route_visible={dialog.route_summary.isVisible()}",
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
        "Save Changes",
        "Add Slot",
        "Remove",
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
        dialog.primary_tray_button.text() if dialog.primary_tray_button.text() != "\N{GEAR}" else "",
        dialog.tray_category_label.text(),
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
            and dialog.settings_state_chip.text() == "Saved",
            f"state_chip={dialog.settings_state_chip.text()!r}; route_visible={dialog.route_summary.isVisible()}; legacy_attrs={[attr for attr in ('settings_summary_panel', 'settings_summary_title', 'settings_summary_detail', 'menu_path_row', 'active_setting_row', 'pending_state_row') if hasattr(dialog, attr)]}",
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
                    button.text()
                    in {"\N{BLACK UP-POINTING TRIANGLE}", "\N{BLACK DOWN-POINTING TRIANGLE}"}
                    and button.width() <= 28
                    and button.height() <= 26
                )
                or (
                    button.objectName() == "residentAccessQuickSlotDelete"
                    and button.text() == "Delete"
                    and 50 <= button.width() <= 64
                    and button.height() <= 26
                )
                for button in compact_action_buttons
            )
            and any(frame.objectName() == "residentAccessQuickSlotReorderGroup" for frame in dialog.findChildren(QFrame)),
            f"buttons={button_texts}; compact_action_sizes={[(button.objectName(), button.text(), button.width(), button.height(), button.isEnabled()) for button in compact_action_buttons]}",
        )
    )
    rows.append(
        (
            "initial saved-state copy",
            not dialog.change_summary.isVisible()
            and dialog.change_summary.text() == ""
            and not dialog.save_button.isEnabled()
            and not dialog.revert_button.isEnabled()
            and dialog.settings_state_chip.text() == "Saved",
            f"change_summary={dialog.change_summary.text()!r}; visible={dialog.change_summary.isVisible()}; state_chip={dialog.settings_state_chip.text()!r}",
        )
    )

    if not dialog._slot_combos:
        rows.append(("quick-slot combo exists", False, "no quick-slot combo rendered"))
    else:
        rows.append(("quick-slot combo exists", True, f"combo_count={len(dialog._slot_combos)}"))
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
                and dialog.settings_state_chip.text() == "Unsaved",
                f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}; state_chip={dialog.settings_state_chip.text()!r}",
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
            and dialog.change_summary.text() == "Saved."
            and dialog.settings_state_chip.text() == "Saved",
            f"dirty={dialog._has_unsaved_changes()}; summary={dialog.change_summary.text()!r}; state_chip={dialog.settings_state_chip.text()!r}",
        )
    )

    contact_sheet, contact_ok = _write_contact_sheet(
        log_dir,
        [
            ("Accepted reference - AI Control Center family grammar", REFERENCE_SCREENSHOTS[0][1]),
            ("Accepted reference - close hover", REFERENCE_SCREENSHOTS[1][1]),
            ("Repaired FAM-003 - settings shell", default_path),
            ("Repaired FAM-003 - settings organizer", log_dir / "04_left_settings_organizer.png"),
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

    ledger_path, manifest_path, element_ledger_path, defect_ledger_path = _write_artifact_ledger(log_dir, artifacts, rows, contact_sheet)
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
