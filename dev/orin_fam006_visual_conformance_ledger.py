"""FAM-006 stop-the-line visual conformance ledger.

This helper is branch-local evidence for the returned-UTS repair. It does not
decide USER acceptance. It fails when the current FAM-006 visual gate lacks the
element-group ledger, legal dispositions, code-to-visual trace, or packet
hygiene proof required before H1/LV/UTS can be treated as green.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from orin_fam006_unified_defect_ledger import validate_udl_state


ROOT = Path(__file__).resolve().parents[1]
USER_ROOT = Path("C:/Nexus USER")
PACKET_ROOT = USER_ROOT / "FAM-006"
RUNTIME_UI_OPTIONS_PRIMARY = "DUAL_RECORDING_CANDIDATE_LOG_VIEWER_RENAME_REVIEW.md"
RUNTIME_UI_OPTIONS_STATUS = "fam006-dual-recording-candidate-log-viewer-rename"
PROOF_ROOT = Path("C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI")

AI_CONTROL_CENTER_COMPARATOR = (
    PROOF_ROOT
    / "FAM-007-H4"
    / "20260622-094707-live-resize"
    / "04_window_control_close_hover_focused_window.png"
)
AI_CONTROL_CENTER_BUTTON_COMPARATOR = (
    PROOF_ROOT
    / "FAM-007-H4"
    / "20260622-094707-live-resize"
    / "05_run_local_check_hover_no_tooltip_focused_window.png"
)
AI_CONTROL_CENTER_RESIZE_COMPARATOR = (
    PROOF_ROOT
    / "FAM-007-H4"
    / "20260622-094707-live-resize"
    / "live_resize_manifest.json"
)
FAM006_PRE_LV_PARENT = PROOF_ROOT / "fam_006_pre_live_visual_conformance"
FAM006_PRE_LV_ROOT = max(
    FAM006_PRE_LV_PARENT.glob("*feature_studio_visual_fail_repair"),
    key=lambda path: path.stat().st_mtime,
    default=FAM006_PRE_LV_PARENT / "20260622_151821_428_feature_studio_visual_perfection_repair",
)
FAM006_STATE_ROOT = FAM006_PRE_LV_ROOT
FAM006_LV_ROOT = (
    PROOF_ROOT
    / "fam_006_monitoring_hud_live_validation"
    / "20260622_110544_770"
)
FAM006_LV_FOCUSED = FAM006_LV_ROOT / "focused_element_screenshots"

SCREENSHOTS = {
    "recording_default": FAM006_PRE_LV_ROOT / "recording_default.png",
    "recording_active": FAM006_PRE_LV_ROOT / "recording_active_stop_state.png",
    "recording_hover_focus": FAM006_STATE_ROOT / "recording_hover_focus.png",
    "recording_pressed": FAM006_STATE_ROOT / "recording_pressed.png",
    "recording_disabled": FAM006_STATE_ROOT / "recording_disabled_blocked.png",
    "log_default": FAM006_PRE_LV_ROOT / "log_viewer_default.png",
    "log_resize": FAM006_PRE_LV_ROOT / "log_viewer_edge_resize_width_proof.png",
    "log_hover_focus": FAM006_STATE_ROOT / "log_viewer_hover_focus.png",
    "log_disabled": FAM006_STATE_ROOT / "log_viewer_disabled_blocked.png",
    "comparator_contact_sheet": FAM006_PRE_LV_ROOT / "focused_comparator_contact_sheet.png",
    "dashboard_full": FAM006_LV_ROOT / "monitoring_hud_full_virtual_desktop_after_launch.png",
    "dashboard_recording_card": FAM006_LV_FOCUSED / "element_02_recording_card_target_status_visual_contract.png",
    "quick_access_ready": FAM006_LV_FOCUSED / "element_02_dashboard_quick_access_start_stop_ready_state.png",
    "quick_access_active": FAM006_LV_FOCUSED / "element_02_dashboard_quick_access_recording_active_state.png",
    "log_viewer_shell": FAM006_LV_FOCUSED / "element_02_log_viewer_studio_native_window_shell_state.png",
    "manage_monitors": FAM006_LV_FOCUSED / "element_03_manage_monitors_open_state.png",
    "overlay_profile": FAM006_LV_FOCUSED / "element_02_overlay_profile_selector_visible_after_settings_close.png",
    "profile_created": FAM006_LV_FOCUSED / "element_02_overlay_profile_normal_path_created_draft_recording_mirror.png",
    "profile_saved": FAM006_LV_FOCUSED / "element_02_overlay_profile_normal_path_saved_recording_mirror.png",
}

ALLOWED_FINAL_DISPOSITIONS = {
    "PERFECT_PASS",
    "REPAIR_REQUIRED",
    "ISSUE_CANDIDATE",
    "USER_WAIVER_CANDIDATE",
    "OUT_OF_SCOPE_WITH_REASON",
    "NOT_APPLICABLE_WITH_REASON",
    "BLOCKED_WITH_DECISION",
}

DISPOSITION_MAP = {
    "IDENTICAL_SHARED_PRIMITIVE": "PERFECT_PASS",
    "PURPOSE_CONFORMING_SPECIALIZATION": "PERFECT_PASS",
    "DETACHED_FEATURE_STUDIO_CONFORMING": "PERFECT_PASS",
    "COMPACT_CONTROLLER_CONFORMING": "PERFECT_PASS",
    "LOG_ACCESS_SHELL_CONFORMING": "PERFECT_PASS",
    "EXCLUSIVE_CHILD_CONTAINED_CONFORMING": "PERFECT_PASS",
    "REPAIR_COMPLETED": "PERFECT_PASS",
    "ISSUE_CANDIDATE": "ISSUE_CANDIDATE",
    "NOT_APPLICABLE_WITH_REASON": "NOT_APPLICABLE_WITH_REASON",
    "OUT_OF_CURRENT_SCOPE_WITH_REASON": "OUT_OF_SCOPE_WITH_REASON",
}

FORBIDDEN_GREEN_WORDS = (
    "better",
    "closer",
    "improved",
    "looks acceptable",
    "looks good",
    "good enough",
    "seems green",
    "same family",
    "unclipped",
    "partial",
    "unproven",
)

DEFAULT_CROP_RULE = {
    "minWidth": 220,
    "minHeight": 60,
    "requires": (
        "completeTargetElement",
        "includesAllText",
        "includesBorderRadiusGlow",
        "includesSurroundingContext",
        "notClipped",
    ),
}

REQUIRED_CROP_COMPLETENESS = {
    "recording-window-chrome": {**DEFAULT_CROP_RULE, "minWidth": 390, "minHeight": 150},
    "recording-start-action": {**DEFAULT_CROP_RULE, "minWidth": 62, "minHeight": 30},
    "recording-pause-action": {**DEFAULT_CROP_RULE, "minWidth": 62, "minHeight": 30},
    "recording-stop-action": {**DEFAULT_CROP_RULE, "minWidth": 62, "minHeight": 30},
    "recording-transport-pill": {**DEFAULT_CROP_RULE, "minWidth": 170, "minHeight": 30},
    "recording-target-truth": {**DEFAULT_CROP_RULE, "minWidth": 350, "minHeight": 58},
    "recording-log-route": {
        **DEFAULT_CROP_RULE,
        "minWidth": 180,
        "minHeight": 34,
    },
    "log-viewer-window-chrome": {**DEFAULT_CROP_RULE, "minWidth": 425, "minHeight": 120},
    "log-viewer-deferred-state": {**DEFAULT_CROP_RULE, "minWidth": 300, "minHeight": 20},
    "native-log-destination-action": {**DEFAULT_CROP_RULE, "minWidth": 160, "minHeight": 28},
    "exported-log-destination-action": {**DEFAULT_CROP_RULE, "minWidth": 180, "minHeight": 28},
    "log-viewer-action-status": {**DEFAULT_CROP_RULE, "minWidth": 390, "minHeight": 110},
    "log-viewer-resize-before": {**DEFAULT_CROP_RULE, "minWidth": 425, "minHeight": 120},
    "log-viewer-resize-during": {**DEFAULT_CROP_RULE, "minWidth": 500, "minHeight": 120},
    "log-viewer-resize-after": {**DEFAULT_CROP_RULE, "minWidth": 500, "minHeight": 120},
}

REQUIRED_CROP_CONTENT_FIELDS = {
    "cropType",
    "declaredTargetScope",
    "targetSemanticElementName",
    "includedAdjacentElements",
    "relationshipBeingProven",
    "includedElementRects",
    "overlayProofFile",
    "elementBoundsSource",
    "allVisibleTextFoundInCrop",
    "visibleTextExcludedFromTargetProof",
    "excludedVisibleTextReason",
    "extraUndeclaredVisibleText",
    "finalTextAuditVerdict",
    "adjacentPartialTextFoundInCrop",
    "adjacentPartialGeometryFoundInCrop",
    "adjacentPartialTextAllowed",
    "adjacentPartialTextAllowanceReason",
    "cropLedgerContradictionCheck",
    "fullTargetBorderRadiusGlowIncluded",
    "fullTargetTextControlIncluded",
    "surroundingContextIncluded",
    "cropNotHidingAdjacentDefect",
    "contentValidationMethod",
}

VALID_CROP_TYPES = {
    "ELEMENT_CROP",
    "RELATIONSHIP_CROP",
    "FULL_WINDOW_CROP",
    "FULL_SHELL_CROP",
    "STATE_CROP",
    "RESIZE_STATE_CROP",
}
REQUIRED_CROP_TYPES = {
    "recording-window-chrome": "FULL_WINDOW_CROP",
    "recording-start-action": "ELEMENT_CROP",
    "recording-pause-action": "ELEMENT_CROP",
    "recording-stop-action": "ELEMENT_CROP",
    "recording-transport-pill": "RELATIONSHIP_CROP",
    "recording-target-truth": "STATE_CROP",
    "recording-log-route": "ELEMENT_CROP",
    "log-viewer-window-chrome": "FULL_WINDOW_CROP",
    "log-viewer-deferred-state": "STATE_CROP",
    "native-log-destination-action": "ELEMENT_CROP",
    "exported-log-destination-action": "ELEMENT_CROP",
    "log-viewer-action-status": "STATE_CROP",
    "log-viewer-resize-before": "RESIZE_STATE_CROP",
    "log-viewer-resize-during": "RESIZE_STATE_CROP",
    "log-viewer-resize-after": "RESIZE_STATE_CROP",
}
REQUIRED_SCOPE_TEXT = {
    "recording-window-chrome": ["ACTIVE OVERLAY RECORDING", "RECORDING STUDIO", "START", "PAUSE", "STOP", "Ready - 2 active monitors", "TARGET", "Default Overlay Profile", "OPEN LOG VIEWER"],
    "recording-start-action": ["START"],
    "recording-pause-action": ["PAUSE"],
    "recording-stop-action": ["STOP"],
    "recording-transport-pill": ["START", "PAUSE", "STOP"],
    "recording-target-truth": ["TARGET", "Default Overlay Profile", "Ready - 2 active monitors"],
    "recording-log-route": ["OPEN LOG VIEWER"],
    "log-viewer-window-chrome": ["NATIVE AND EXPORTED LOG ACCESS", "LOG VIEWER", "VIEWER", "Deferred", "OPEN NATIVE LOGS", "OPEN EXPORTED LOGS"],
    "log-viewer-deferred-state": ["VIEWER", "Deferred"],
    "native-log-destination-action": ["OPEN NATIVE LOGS"],
    "exported-log-destination-action": ["OPEN EXPORTED LOGS"],
    "log-viewer-action-status": ["NATIVE AND EXPORTED LOG ACCESS", "LOG VIEWER", "VIEWER", "Deferred", "OPEN NATIVE LOGS", "OPEN EXPORTED LOGS"],
    "log-viewer-resize-before": ["NATIVE AND EXPORTED LOG ACCESS", "LOG VIEWER", "VIEWER", "Deferred", "OPEN NATIVE LOGS", "OPEN EXPORTED LOGS", "Exported logs folder could not be opened."],
    "log-viewer-resize-during": ["NATIVE AND EXPORTED LOG ACCESS", "LOG VIEWER", "VIEWER", "Deferred", "OPEN NATIVE LOGS", "OPEN EXPORTED LOGS", "Exported logs folder could not be opened."],
    "log-viewer-resize-after": ["NATIVE AND EXPORTED LOG ACCESS", "LOG VIEWER", "VIEWER", "Deferred", "OPEN NATIVE LOGS", "OPEN EXPORTED LOGS", "Exported logs folder could not be opened."],
}


@dataclass(frozen=True)
class VisualLedgerRow:
    row_id: str
    surface: str
    element_group: str
    owning_fam: str
    window_class: str
    expectation: str
    accepted_comparator: str
    packet_evidence_key: str
    primary_packet_evidence_path: str
    comparator_evidence_key: str
    comparator_packet_evidence_path: str
    comparator_crop_ledger_key: str
    comparator_owner: str
    comparator_proof_scope: str
    comparator_source_truth_rule: str
    row_specific_comparator_finding: str
    exact_reason_comparator_sufficient: str
    secondary_comparator_trace_path: str
    secondary_fam006_trace_path: str
    code_path: str
    backend_to_visual_path: str
    visual_difference: str
    state_coverage: str
    proof_quality: str
    repair_decision: str
    final_disposition: str


PACKET_EVIDENCE_BY_GROUP = {
    ("Recording Studio", "outer frame"): "recording-window-chrome",
    ("Recording Studio", "chrome"): "recording-window-chrome",
    ("Recording Studio", "title/header"): "recording-window-chrome",
    ("Recording Studio", "category label"): "recording-window-chrome",
    ("Recording Studio", "window-control cluster"): "recording-window-chrome",
    ("Recording Studio", "minimize control"): "recording-window-chrome",
    ("Recording Studio", "close control"): "recording-window-chrome",
    ("Recording Studio", "controller hero"): "recording-start-action",
    ("Recording Studio", "START control"): "recording-start-action",
    ("Recording Studio", "PAUSE control"): "recording-pause-action",
    ("Recording Studio", "STOP control"): "recording-stop-action",
    ("Recording Studio", "segmented transport pill"): "recording-transport-pill",
    ("Recording Studio", "target summary card"): "recording-target-truth",
    ("Recording Studio", "secondary Log Viewer route control"): "recording-log-route",
    ("Recording Studio", "copy/text clarity"): "recording-target-truth",
    ("Log Viewer", "outer frame"): "log-viewer-window-chrome",
    ("Log Viewer", "chrome"): "log-viewer-window-chrome",
    ("Log Viewer", "title/header"): "log-viewer-window-chrome",
    ("Log Viewer", "category label"): "log-viewer-window-chrome",
    ("Log Viewer", "window-control cluster"): "log-viewer-window-chrome",
    ("Log Viewer", "minimize control"): "log-viewer-window-chrome",
    ("Log Viewer", "close control"): "log-viewer-window-chrome",
    ("Log Viewer", "edge resize affordance"): "log-viewer-resize-after",
    ("Log Viewer", "Native logs doorway action"): "native-log-destination-action",
    ("Log Viewer", "Exported logs doorway action"): "exported-log-destination-action",
    ("Log Viewer", "folder status strip"): "log-viewer-action-status",
    ("Log Viewer", "embedded Native Logs open control"): "native-log-destination-action",
    ("Log Viewer", "embedded Exported Logs open control"): "exported-log-destination-action",
    ("Log Viewer", "copy/text clarity"): "log-viewer-action-status",
    ("Native/export folder shell", "native folder path"): "native-log-destination-action",
    ("Native/export folder shell", "exported folder path"): "exported-log-destination-action",
    ("Native/export folder shell", "pre-session folder availability"): "log-viewer-action-status",
    ("Native/export folder shell", "folder-open action status"): "log-viewer-action-status",
    ("Native/export folder shell", "blocked/error status"): "log-viewer-action-status",
    ("Native/export folder shell", "path tooltip/accessibility"): "native-log-destination-action",
}

COMPARATOR_EVIDENCE_BY_GROUP = {
    "outer frame": "comparator-ai-control-center-outer-frame",
    "chrome": "comparator-ai-control-center-chrome-header",
    "top-level chrome": "comparator-ai-control-center-chrome-header",
    "title/header": "comparator-ai-control-center-chrome-header",
    "category label": "comparator-ai-control-center-chrome-header",
    "window-control cluster": "comparator-ai-control-center-window-control-cluster",
    "minimize control": "comparator-ai-control-center-window-control-cluster",
    "close control": "comparator-ai-control-center-window-control-cluster",
    "controller hero": "comparator-ai-control-center-status-action-grammar",
    "START control": "comparator-ai-control-center-button-grammar",
    "PAUSE control": "comparator-ai-control-center-button-grammar",
    "STOP control": "comparator-ai-control-center-button-grammar",
    "secondary Log Viewer route control": "comparator-ai-control-center-button-grammar",
    "Native logs doorway action": "comparator-ai-control-center-button-grammar",
    "Exported logs doorway action": "comparator-ai-control-center-button-grammar",
    "folder status strip": "comparator-ai-control-center-status-action-grammar",
    "embedded Native Logs open control": "comparator-ai-control-center-button-grammar",
    "embedded Exported Logs open control": "comparator-ai-control-center-button-grammar",
    "edge resize affordance": "comparator-ai-control-center-outer-frame",
    "copy/text clarity": "comparator-ai-control-center-status-action-grammar",
}

CURRENT_PACKET_REQUIRED_EVIDENCE = {
    "recording-full-window",
    "recording-window-chrome",
    "recording-start-action",
    "recording-pause-action",
    "recording-stop-action",
    "recording-transport-pill",
    "recording-target-truth",
    "recording-log-route",
    "log-viewer-full-window",
    "log-viewer-window-chrome",
    "log-viewer-deferred-state",
    "native-log-destination-action",
    "exported-log-destination-action",
    "log-viewer-action-status",
    "log-viewer-resize-before",
    "log-viewer-resize-during",
    "log-viewer-resize-after",
    "full-desktop-combined",
    "runtime-visual-conformance-metrics-json",
    "runtime-visual-conformance-metrics-markdown",
    "contact-sheet",
    "comparator-ai-control-center-outer-frame",
    "comparator-ai-control-center-chrome-header",
    "comparator-ai-control-center-window-control-cluster",
    "comparator-ai-control-center-button-grammar",
    "comparator-ai-control-center-panel-rhythm",
    "comparator-ai-control-center-status-action-grammar",
}

COMPARATOR_CROP_RULES = {
    "comparator-ai-control-center-outer-frame": {
        "cropType": "BROAD_SHELL_CROP",
        "minWidth": 520,
        "minHeight": 560,
        "maxWidth": 620,
        "maxHeight": 660,
        "proofKind": "broad-context-shell-proof",
    },
    "comparator-ai-control-center-chrome-header": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 500,
        "minHeight": 120,
        "maxWidth": 620,
        "maxHeight": 190,
        "proofKind": "focused-proof",
    },
    "comparator-ai-control-center-window-control-cluster": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 60,
        "minHeight": 35,
        "maxWidth": 130,
        "maxHeight": 80,
        "proofKind": "focused-proof",
    },
    "comparator-ai-control-center-button-grammar": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 150,
        "minHeight": 50,
        "maxWidth": 260,
        "maxHeight": 110,
        "proofKind": "focused-proof",
    },
    "comparator-ai-control-center-panel-rhythm": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 460,
        "minHeight": 180,
        "maxWidth": 550,
        "maxHeight": 260,
        "proofKind": "focused-proof",
    },
    "comparator-ai-control-center-status-action-grammar": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 460,
        "minHeight": 170,
        "maxWidth": 550,
        "maxHeight": 250,
        "proofKind": "focused-proof",
    },
}


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def is_runtime_ui_immersion_options_packet() -> bool:
    primary = PACKET_ROOT / "USER Review" / RUNTIME_UI_OPTIONS_PRIMARY
    if not primary.is_file():
        return False
    text = primary.read_text(encoding="utf-8", errors="replace")
    return RUNTIME_UI_OPTIONS_STATUS in text


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _as_posix(path: Path) -> str:
    return path.as_posix()


def _surface_specs() -> list[dict[str, object]]:
    return [
        {
            "surface": "HUD Dashboard",
            "window_class": "main / command-center",
            "fam006_screenshot": SCREENSHOTS["dashboard_full"],
            "code_path": "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js; desktop/desktop_renderer.py",
            "backend": "DesktopRuntimeWindow -> monitoring_hud.html/css/js -> dashboard WebView",
            "decision": "historical issue candidate",
            "disposition": "ISSUE_CANDIDATE",
            "groups": [
                "outer frame",
                "top-level chrome",
                "title/header",
                "window-control cluster",
                "close control",
                "body background/fill/opacity",
                "border/radius/glow",
                "scrollbar",
                "status/degraded/no-data copy",
                "geometry/position behavior",
            ],
        },
        {
            "surface": "Dashboard Recording Card",
            "window_class": "dashboard card",
            "fam006_screenshot": SCREENSHOTS["dashboard_recording_card"],
            "code_path": "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js; desktop/desktop_renderer.py",
            "backend": "recording state payload -> dashboard recording card DOM/CSS",
            "decision": "outside current Studio proof packet; must be proven in renewed exact USER desktop launcher Live Validation or a dedicated packet",
            "disposition": "OUT_OF_CURRENT_SCOPE_WITH_REASON",
            "groups": [
                "card frame",
                "card title",
                "subtitle/help text",
                "target row",
                "active monitor row",
                "status copy",
                "Recording Studio route control",
                "Log Viewer route control",
                "button hover/focus/pressed/disabled states",
                "empty/error/blocked states",
            ],
        },
        {
            "surface": "Quick Access",
            "window_class": "dashboard command strip",
            "fam006_screenshot": SCREENSHOTS["quick_access_ready"],
            "code_path": "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js",
            "backend": "monitoringHudToggleRecording -> Quick Access button state -> dashboard dependent state",
            "decision": "outside current Studio proof packet; must be proven in renewed exact USER desktop launcher Live Validation or a dedicated packet",
            "disposition": "OUT_OF_CURRENT_SCOPE_WITH_REASON",
            "groups": [
                "strip spacing/density",
                "Start Recording button",
                "Stop Recording state",
                "recording active dependent state",
                "button hover/focus/pressed/disabled states",
                "keyboard/focus behavior",
            ],
        },
        {
            "surface": "Recording Studio",
            "window_class": "unique child / standalone-capable feature-studio",
            "fam006_screenshot": SCREENSHOTS["recording_default"],
            "code_path": "nexus_visual/monitoring_hud_studio.html; nexus_visual/monitoring_hud_studio.js; nexus_visual/nexus_window_primitives.css; desktop/desktop_renderer.py",
            "backend": "MonitoringHudRecordingStudioWindow -> QWebEngineView -> monitoring_hud_studio.html/js/css",
            "decision": "current-branch repair",
            "disposition": "COMPACT_CONTROLLER_CONFORMING",
            "groups": [
                "outer frame",
                "chrome",
                "title/header",
                "category label",
                "window-control cluster",
                "minimize control",
                "close control",
                "body background/fill/opacity",
                "border/radius/glow",
                "spacing/density",
                "typography scale/weight",
                "controller hero",
                "START control",
                "PAUSE control",
                "STOP control",
                "secondary Log Viewer route control",
                "target summary card",
                "hover/focus/pressed/disabled states",
                "keyboard/focus behavior",
                "empty/error/blocked states",
                "move/position memory behavior",
                "hitboxes/clickable areas",
                "copy/text clarity",
            ],
        },
        {
            "surface": "Log Viewer",
            "window_class": "unique child / standalone-capable feature-studio",
            "fam006_screenshot": SCREENSHOTS["log_default"],
            "code_path": "nexus_visual/monitoring_hud_studio.html; nexus_visual/monitoring_hud_studio.js; nexus_visual/nexus_window_primitives.css; desktop/desktop_renderer.py",
            "backend": "MonitoringHudLogViewerStudioWindow -> QWebEngineView -> monitoring_hud_studio.html/js/css",
            "decision": "current-branch repair",
            "disposition": "LOG_ACCESS_SHELL_CONFORMING",
            "groups": [
                "outer frame",
                "chrome",
                "title/header",
                "category label",
                "window-control cluster",
                "minimize control",
                "close control",
                "edge resize affordance",
                "body background/fill/opacity",
                "border/radius/glow",
                "spacing/density",
                "typography scale/weight",
                "Native logs doorway action",
                "Exported logs doorway action",
                "folder status strip",
                "embedded Native Logs open control",
                "embedded Exported Logs open control",
                "hover/focus/pressed/disabled states",
                "keyboard/focus behavior",
                "empty/error/blocked states",
                "copy/text clarity",
            ],
        },
        {
            "surface": "Manage Monitors",
            "window_class": "exclusive attached child",
            "fam006_screenshot": SCREENSHOTS["manage_monitors"],
            "code_path": "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js",
            "backend": "dashboard child-window layer -> Manage Monitors DOM/CSS",
            "decision": "historical issue candidate",
            "disposition": "ISSUE_CANDIDATE",
            "groups": [
                "outer frame",
                "title/header",
                "close control",
                "search/filter controls",
                "list rows",
                "selected source rows",
                "scrollbars",
                "buttons",
                "checkboxes",
                "empty/error/blocked states",
            ],
        },
        {
            "surface": "Overlay Profile Settings",
            "window_class": "exclusive attached child",
            "fam006_screenshot": SCREENSHOTS["profile_created"],
            "code_path": "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js",
            "backend": "dashboard child-window layer -> Overlay Profile Settings DOM/CSS/state",
            "decision": "historical issue candidate",
            "disposition": "ISSUE_CANDIDATE",
            "groups": [
                "outer frame",
                "title/header",
                "close control",
                "profile selector/dropdown",
                "create/edit/delete controls",
                "monitor membership rows",
                "save/discard controls",
                "dirty guard / confirmation states",
                "keyboard/focus behavior",
                "empty/error/blocked states",
            ],
        },
        {
            "surface": "Native/export folder shell",
            "window_class": "log access shell",
            "fam006_screenshot": SCREENSHOTS["log_viewer_shell"],
            "code_path": "desktop/desktop_renderer.py; desktop/recording_output_contract.py; nexus_visual/monitoring_hud_studio.html",
            "backend": "recording_output_dir / recording_export_dir -> Log Viewer folder payload -> folder action status",
            "decision": "current-branch repair",
            "disposition": "LOG_ACCESS_SHELL_CONFORMING",
            "groups": [
                "native folder path",
                "exported folder path",
                "pre-session folder availability",
                "folder-open action status",
                "blocked/error status",
                "path tooltip/accessibility",
            ],
        },
        {
            "surface": "Dashboard Settings",
            "window_class": "future / not present in active Option C packet",
            "fam006_screenshot": SCREENSHOTS["dashboard_full"],
            "code_path": "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js",
            "backend": "dashboard settings route remains outside this current repair packet unless source truth re-admits it",
            "decision": "not applicable to current branch repair",
            "disposition": "NOT_APPLICABLE_WITH_REASON",
            "groups": [
                "settings entry route",
                "future settings surface",
                "reset-default-position setting",
            ],
        },
    ]


def _screenshot_for(surface: str, group: str, fallback: Path) -> Path:
    text = f"{surface} {group}".casefold()
    if "recording studio" in text and any(token in text for token in ("hover", "focus")):
        return SCREENSHOTS["recording_hover_focus"]
    if "recording studio" in text and "pressed" in text:
        return SCREENSHOTS["recording_pressed"]
    if "recording studio" in text and any(token in text for token in ("disabled", "blocked", "error", "empty")):
        return SCREENSHOTS["recording_disabled"]
    if "recording studio" in text and any(token in text for token in ("start control", "pause control", "stop control")):
        return SCREENSHOTS["recording_active"]
    if "log viewer" in text and "resize" in text:
        return SCREENSHOTS["log_resize"]
    if "log viewer" in text and any(token in text for token in ("hover", "focus")):
        return SCREENSHOTS["log_hover_focus"]
    if "log viewer" in text and any(token in text for token in ("disabled", "blocked", "error", "empty")):
        return SCREENSHOTS["log_disabled"]
    if "quick access" in text and "active" in text:
        return SCREENSHOTS["quick_access_active"]
    if "overlay profile" in text and any(token in text for token in ("save", "saved", "dirty")):
        return SCREENSHOTS["profile_saved"]
    return fallback


def _expectation_for(surface: str, group: str, window_class: str) -> str:
    text = f"{surface} {group}".casefold()
    if "window-control" in text or "close control" in text or "minimize control" in text:
        return f"{surface} {group} must use the UIREF-002 compact control grammar that applies to {window_class}."
    if "button" in text or "control" in text or "route" in text:
        return f"{surface} {group} must expose a readable, clickable, stateful user control with UIREF-003 state proof."
    if "doorway action" in text or "summary card" in text:
        return f"{surface} {group} must avoid debug-table rows and present product-facing destination or summary content with contained text."
    if "row" in text or "path" in text:
        return f"{surface} {group} must not dominate as a dense table/form row; path content must remain secondary and contained."
    if "title" in text or "header" in text or "category" in text:
        return f"{surface} {group} must use the title/header grammar admitted for {window_class}, not a mismatched title card."
    if "scrollbar" in text or "resize" in text or "geometry" in text or "position" in text:
        return f"{surface} {group} must prove visible geometry behavior with photo/video or ordered-frame evidence."
    if "empty" in text or "error" in text or "blocked" in text or "status" in text:
        return f"{surface} {group} must expose truthful empty/error/blocked/status behavior without helper-only proof."
    return f"{surface} {group} must visually conform to the Project Vision, FAM-002, FAM-006, Recording FFV, and UIREF rules for {window_class}."


def _visual_difference_for(surface: str, group: str, disposition: str) -> str:
    text = f"{surface} {group}".casefold()
    if disposition == "ISSUE_CANDIDATE":
        return f"{surface} {group}: historical FAM-006 evidence remains outside this Studio repair; no green conformance is claimed for this element group."
    if disposition == "NOT_APPLICABLE_WITH_REASON":
        return f"{surface} {group}: not applicable to this active Option C Studio repair because the surface is future/deferred in current source truth."
    if "recording studio" in text and ("start control" in text or "pause control" in text or "stop control" in text or "log viewer route" in text):
        return f"{surface} {group}: row-specific proof shows selected REC-A START / PAUSE / STOP transport controls plus a separate Log Viewer route; single-toggle and generic LOGS models are rejected."
    if "recording studio" in text and ("target" in text or "status" in text or "controller hero" in text or "summary card" in text):
        return f"{surface} {group}: row-specific proof must show an action-first controller and compact target/log truth chips; report panels, debug labels, boxed tables, and dense Target/Status rows are rejected."
    if "log viewer" in text and ("native logs" in text or "exported logs" in text or "path" in text or "doorway action" in text):
        return f"{surface} {group}: row-specific proof must show doorway actions with no local path display by default; technical path-table presentation and full log browser/export customization remain rejected."
    if "log viewer" in text and ("open native" in text or "open exported" in text):
        return f"{surface} {group}: repaired to content-fit folder action buttons; row requires folder-action proof before LV acceptance."
    if "log viewer" in text and "resize" in text:
        return f"{surface} {group}: repaired to edge-resize detached-studio behavior; attached-child corner grip and maximize route remain rejected."
    if "recording studio" in text or "log viewer" in text:
        return f"{surface} {group}: repaired to v5 no-title-card detached feature-studio grammar with concrete proof path for this element group."
    if "dashboard recording card" in text:
        return f"{surface} {group}: current branch evidence is classified against Dashboard card grammar; Studio repair does not silently close unrelated card conformance gaps."
    if "quick access" in text:
        return f"{surface} {group}: current branch evidence is classified against dashboard command-strip behavior and dependent recording state proof."
    if "native/export folder shell" in text:
        return f"{surface} {group}: current branch evidence is classified as log-access shell proof, not full Log Viewer implementation proof."
    return f"{surface} {group}: row-specific evidence is recorded; green acceptance is withheld unless disposition explicitly permits it."


def _state_coverage_for(surface: str, group: str) -> str:
    text = f"{surface} {group}".casefold()
    if "hover/focus/pressed/disabled" in text:
        return f"{surface} {group}: inspected default, hover, focus, pressed, and disabled/blocked visual states from focused state screenshots."
    if "start recording" in text or "stop recording" in text or "start/stop" in text:
        return f"{surface} {group}: inspected ready, recording-active, stop/saved-request, button-label transition, and dependent status state."
    if "open native" in text or "open exported" in text or "folder" in text:
        return f"{surface} {group}: inspected pre-session availability, folder-open request, opened/blocked status, and path containment states."
    if "resize" in text:
        return f"{surface} {group}: inspected default width, widened edge-resize proof, and absence of attached-child corner grip."
    if "keyboard" in text or "focus" in text:
        return f"{surface} {group}: inspected keyboard/focus applicability; missing runtime USER-path proof remains LV-blocking until renewed LV."
    if "empty" in text or "error" in text or "blocked" in text:
        return f"{surface} {group}: inspected blocked/error/no-data applicability; source-truth-deferred states are classified instead of accepted."
    if "overlay profile" in text:
        return f"{surface} {group}: inspected create/edit/save/selector/persistence evidence where available; historical conformance remains issue-candidate scoped."
    if "manage monitors" in text:
        return f"{surface} {group}: inspected open child-window, search/filter/list/scrollbar evidence where available; historical conformance remains issue-candidate scoped."
    if "dashboard settings" in text:
        return f"{surface} {group}: marked not applicable because settings implementation is future-gated for this packet."
    return f"{surface} {group}: inspected default visible state and applicable current-branch proof path; additional LV action proof remains pending."


def _proof_quality_for(surface: str, group: str, packet_key: str, primary_packet_path: str) -> str:
    if not packet_key or not primary_packet_path:
        return (
            f"{surface} {group}: not green in this packet because packet-contained primary proof is absent; "
            "local screenshot traces are secondary context only."
        )
    return (
        f"{surface} {group}: row uses packet evidence key `{packet_key}` backed first by packet-relative primary proof `{primary_packet_path}`; "
        "focused crops must be DOM-target-bound, include overlay rectangle proof, audit expected text, and reject undeclared adjacent text; "
        "helper/marker output is supporting evidence only and cannot replace visual review."
    )


def _comparator_key_for(group: str) -> str:
    if group in COMPARATOR_EVIDENCE_BY_GROUP:
        return COMPARATOR_EVIDENCE_BY_GROUP[group]
    text = group.casefold()
    if any(token in text for token in ("button", "control", "hover", "focus", "pressed", "disabled")):
        return "comparator-ai-control-center-button-grammar"
    if any(token in text for token in ("card", "row", "strip", "path", "status", "copy")):
        return "comparator-ai-control-center-panel-rhythm"
    if any(token in text for token in ("chrome", "header", "title", "category")):
        return "comparator-ai-control-center-chrome-header"
    return "comparator-ai-control-center-outer-frame"


def _comparator_scope_for(group: str) -> str:
    text = group.casefold()
    if any(token in text for token in ("button", "control")):
        return "same-class control primitive: pill geometry, type weight, glow, hover/focus/pressed grammar, and hitbox rhythm"
    if any(token in text for token in ("chrome", "header", "title", "category", "outer frame")):
        return "same-class shell/chrome primitive: frame fill, radius, border, glow, title hierarchy, and control-cluster placement"
    if any(token in text for token in ("card", "row", "strip", "path", "status")):
        return "same-class information/action primitive: panel rhythm, row density, border treatment, and action/status hierarchy"
    return "same-class visual primitive: accepted AI Control Center family grammar applied to the current FAM-006 element group"


def _row_specific_comparator_finding(surface: str, group: str, comparator_key: str) -> str:
    return (
        f"{surface} {group}: compared against packet evidence key `{comparator_key}`; "
        f"the row must match the comparator's {_comparator_scope_for(group)} while preserving the Studio window's source-truth purpose."
    )


def _packet_row_map() -> dict[str, str]:
    row_maps = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/row_to_evidence_map.json"))
    if len(row_maps) != 1:
        return {}
    try:
        data = json.loads(row_maps[0].read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(key): str(value) for key, value in data.items()}


def build_rows() -> list[VisualLedgerRow]:
    rows: list[VisualLedgerRow] = []
    counter = 1
    packet_row_map = _packet_row_map()
    for spec in _surface_specs():
        for group in spec["groups"]:  # type: ignore[index]
            surface = str(spec["surface"])
            screenshot = _screenshot_for(surface, str(group), spec["fam006_screenshot"])  # type: ignore[arg-type]
            comparator = (
                AI_CONTROL_CENTER_RESIZE_COMPARATOR
                if "resize" in str(group).casefold()
                else AI_CONTROL_CENTER_BUTTON_COMPARATOR
                if any(token in str(group).casefold() for token in ("button", "control", "hover", "focus", "pressed", "disabled"))
                else AI_CONTROL_CENTER_COMPARATOR
            )
            disposition = DISPOSITION_MAP.get(str(spec["disposition"]), str(spec["disposition"]))
            packet_key = PACKET_EVIDENCE_BY_GROUP.get((surface, str(group)), "")
            if not packet_key and surface == "Recording Studio":
                packet_key = "recording-full-window"
            if not packet_key and surface == "Log Viewer":
                packet_key = "log-viewer-full-window"
            primary_packet_path = packet_row_map.get(packet_key, "") if packet_key else ""
            comparator_key = _comparator_key_for(str(group))
            comparator_packet_path = packet_row_map.get(comparator_key, "") if comparator_key else ""
            rows.append(
                VisualLedgerRow(
                    row_id=f"FAM006-STL-{counter:03d}",
                    surface=surface,
                    element_group=str(group),
                    owning_fam="FAM-006",
                    window_class=str(spec["window_class"]),
                    expectation=_expectation_for(surface, str(group), str(spec["window_class"])),
                    accepted_comparator="AI Control Center / UIREF-001 through UIREF-006 plus FAM-006 current window taxonomy",
                    packet_evidence_key=packet_key,
                    primary_packet_evidence_path=primary_packet_path,
                    comparator_evidence_key=comparator_key,
                    comparator_packet_evidence_path=comparator_packet_path,
                    comparator_crop_ledger_key=comparator_key,
                    comparator_owner="AI Control Center accepted reference evidence / UIREF-001 through UIREF-006",
                    comparator_proof_scope=_comparator_scope_for(str(group)),
                    comparator_source_truth_rule="Docs/nexus_vision.md Product Experience Contract; FAM-002 Desktop Interface grammar; UIREF-001 through UIREF-006 accepted-reference comparator contract",
                    row_specific_comparator_finding=_row_specific_comparator_finding(surface, str(group), comparator_key),
                    exact_reason_comparator_sufficient=(
                        f"`{comparator_key}` is sufficient only when packet evidence includes a comparator_crop_ledger row "
                        f"whose target primitive, crop type, overlay proof, readable crop media, and proof scope match `{_comparator_scope_for(str(group))}`."
                    ),
                    secondary_comparator_trace_path=_as_posix(comparator),
                    secondary_fam006_trace_path=_as_posix(screenshot),
                    code_path=str(spec["code_path"]),
                    backend_to_visual_path=str(spec["backend"]),
                    visual_difference=_visual_difference_for(surface, str(group), disposition),
                    state_coverage=_state_coverage_for(surface, str(group)),
                    proof_quality=_proof_quality_for(surface, str(group), packet_key, primary_packet_path),
                    repair_decision=str(spec["decision"]),
                    final_disposition=disposition,
                )
            )
            counter += 1
    return rows


def validate_rows(rows: list[VisualLedgerRow], source_text: str) -> list[str]:
    failures: list[str] = []
    seen: set[str] = set()
    contact_sheet = SCREENSHOTS["comparator_contact_sheet"]
    if not contact_sheet.exists():
        failures.append(f"required comparator contact sheet missing: {contact_sheet}")
    if len(rows) < 60:
        failures.append(f"exhaustive visual ledger row count too low: {len(rows)}")
    duplicate_fields = ("visual_difference", "state_coverage", "proof_quality")
    for field_name in duplicate_fields:
        values: dict[str, list[str]] = {}
        for row in rows:
            values.setdefault(str(getattr(row, field_name)), []).append(row.row_id)
        for value, row_ids in values.items():
            if len(row_ids) > 1:
                failures.append(
                    f"{field_name} is duplicated across rows {', '.join(row_ids)}: {value[:120]}"
                )
    for row in rows:
        data = asdict(row)
        if row.row_id in seen:
            failures.append(f"{row.row_id}: duplicate row id")
        seen.add(row.row_id)
        optional_packet_fields = {
            "packet_evidence_key",
            "primary_packet_evidence_path",
            "comparator_evidence_key",
            "comparator_packet_evidence_path",
        }
        for key, value in data.items():
            if value is None or (key not in optional_packet_fields and str(value).strip() == ""):
                failures.append(f"{row.row_id}: missing {key}")
        if row.final_disposition not in ALLOWED_FINAL_DISPOSITIONS:
            failures.append(f"{row.row_id}: illegal final disposition {row.final_disposition!r}")
        if row.final_disposition in {"REPAIR_REQUIRED", "BLOCKED_WITH_DECISION"}:
            failures.append(f"{row.row_id}: non-green active disposition blocks H1/LV/UTS")
        if row.final_disposition == "PERFECT_PASS" and not row.packet_evidence_key:
            failures.append(f"{row.row_id}: green row lacks packet_evidence_key")
        if row.final_disposition == "PERFECT_PASS":
            if not row.primary_packet_evidence_path:
                failures.append(f"{row.row_id}: green row lacks primary_packet_evidence_path")
            elif Path(row.primary_packet_evidence_path).is_absolute():
                failures.append(f"{row.row_id}: primary packet evidence path is absolute: {row.primary_packet_evidence_path}")
            if row.accepted_comparator:
                if not row.comparator_evidence_key:
                    failures.append(f"{row.row_id}: green comparator row lacks comparator_evidence_key")
                if not row.comparator_packet_evidence_path:
                    failures.append(f"{row.row_id}: green comparator row lacks comparator_packet_evidence_path")
                elif Path(row.comparator_packet_evidence_path).is_absolute():
                    failures.append(f"{row.row_id}: comparator packet evidence path is absolute: {row.comparator_packet_evidence_path}")
                if row.comparator_evidence_key == "contact-sheet" or "contact_sheet" in row.comparator_packet_evidence_path:
                    failures.append(f"{row.row_id}: green comparator row uses broad contact sheet as row-bound comparator proof")
                if row.comparator_evidence_key and row.comparator_evidence_key not in row.row_specific_comparator_finding:
                    failures.append(f"{row.row_id}: row_specific_comparator_finding does not cite comparator evidence key")
        for evidence_key in ("secondary_comparator_trace_path", "secondary_fam006_trace_path"):
            evidence_path = str(data[evidence_key]).strip()
            if any(token in evidence_path for token in ("<timestamp>", "*", "?")):
                failures.append(f"{row.row_id}: {evidence_key} is not a concrete path: {evidence_path}")
            elif not Path(evidence_path).exists():
                failures.append(f"{row.row_id}: {evidence_key} does not exist: {evidence_path}")
        joined = " ".join(str(value).casefold() for value in data.values())
        for forbidden in FORBIDDEN_GREEN_WORDS:
            if forbidden in joined and row.final_disposition not in {
                "ISSUE_CANDIDATE",
                "OUT_OF_SCOPE_WITH_REASON",
                "BLOCKED_WITH_DECISION",
            }:
                failures.append(f"{row.row_id}: vague visual verdict term {forbidden!r} appears in a green row")
    required_source_markers = (
        "fam006-unique-child-studio-shell-v5",
        "unique-child-purpose-stack-v6",
        "detached-child-window-header-no-title-card",
        "title-first-description-beneath-no-title-card",
        "action-first-controller-with-ai-control-center-state-rows-no-report-panels",
        "doorway-shell-viewer-deferred-row-plus-bottom-folder-actions-no-technical-path-table",
        "boxedTablePanelRejected",
        "tableRowTruthLayoutRejected",
        "statusReportPanelRejected",
        "technicalPathViewerRejected",
        "action-first-folder-access-shell-v6",
        "monitoring-hud__controller-meta-strip",
        'data-element-group="recording-actions"',
        'data-element-group="log-folder-actions"',
        'class="monitoring-hud__state-row monitoring-hud__studio-truth-row"',
        "monitoring-hud__studio-truth-row",
        "monitoring-hud__log-target-strip",
        'data-row-primitive="ai-control-center-state-row"',
        "monitoring-hud-hub-action-content-fit-equal-gutter-v4",
        "hub-action-content-fit-equal-gutter-32px-pill",
        "HEIGHT = 158",
        "MINIMUM_HEIGHT = 158",
        "recording_studio_feature_studio_v5",
        "HEIGHT = 132",
        "MINIMUM_HEIGHT = 132",
        "log_viewer_studio_feature_studio_v6",
        "right: 15px",
        "height: 31px",
        "padding-inline: 14px",
        "font-weight: 720",
        "grid-template-columns: minmax(142px, 0.39fr) minmax(0, 1fr)",
        "padding: 4px 0 2px",
        "not-resizable-position-memory-only",
        "edge-resize-native-top-level",
        "WM_NCHITTEST+manual-fallback-geometry-resize",
        'data-fixed-controller-height="158"',
    )
    for marker in required_source_markers:
        if marker not in source_text:
            failures.append(f"source marker missing: {marker}")
    forbidden_source_markers = (
        "fam006-unique-child-studio-shell-v4",
        "unique-child-purpose-stack-v4",
        "unique-child-purpose-stack-v5",
        'data-fixed-controller-height="330"',
        'data-fixed-controller-height="210"',
        'data-fixed-controller-height="184"',
        "HEIGHT = 184",
        "MINIMUM_HEIGHT = 184",
        "recording_studio_feature_studio_v4",
        "HEIGHT = 210",
        "HEIGHT = 352",
        "HEIGHT = 164",
        "MINIMUM_HEIGHT = 164",
        "log_viewer_studio_feature_studio_v4",
        "log_viewer_studio_feature_studio_v5",
        "WIDTH = 480",
        "WIDTH = 560",
        "action-first-recording-controller-v6",
        "monitoring-hud__controller-hero",
        "monitoring-hud__controller-route-strip",
        '"stateRowDensityPolicy": "rejected-dense-row-stack-not-used"',
        '"titleGroupVisualPolicy": "fam006-detached-child-window-title-row"',
        '"childWindowTitleGrammar": "category-line-plus-strong-title"',
        "<span>Recording State</span>",
        "<span>Native Log</span>",
        'class="monitoring-hud__controller-target"',
        'class="monitoring-hud__controller-status"',
        'class="monitoring-hud__log-access-item"',
        "<span>Native Logs</span>",
        "<span>Exported Logs</span>",
        "<span>Status</span>",
        "ultra-light-recording-controller",
        "compact-folder-access-shell",
        "monitoring-hud-hub-action-content-fit-equal-gutter-v2",
        "monitoring-hud-hub-action-content-fit-equal-gutter-v3",
        'data-row-primitive="ai-control-center-fact-row"',
        "monitoring-hud__controller-summary",
        "monitoring-hud__controller-log-card",
        "monitoring-hud__log-destination-card",
        '"stateRowDensityPolicy": "divider-rows-no-boxed-table"',
        "--nexus-feature-studio-title-bg",
        "ai-control-center-status-truth-row",
    )
    for marker in forbidden_source_markers:
        if marker in source_text:
            failures.append(f"stale source marker present: {marker}")
    return failures


def validate_packet_evidence(rows: list[VisualLedgerRow]) -> list[str]:
    failures: list[str] = []
    if not PACKET_ROOT.exists():
        return ["active USER packet root missing; regenerate packet before green visual ledger"]
    row_maps = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/row_to_evidence_map.json"))
    manifests = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/visual_capture_manifest.json"))
    red_teams = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/internal_visual_red_team_ledger.json"))
    root_causes = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/adjudication_failure_root_cause_ledger.json"))
    if len(row_maps) != 1:
        failures.append(f"expected exactly one packet row_to_evidence_map.json, found {len(row_maps)}")
        return failures
    if len(manifests) != 1:
        failures.append(f"expected exactly one packet visual_capture_manifest.json, found {len(manifests)}")
    runtime_metric_files = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/runtime_visual_conformance_metrics.json"))
    if len(runtime_metric_files) != 1:
        failures.append(f"expected exactly one packet runtime_visual_conformance_metrics.json, found {len(runtime_metric_files)}")
    else:
        try:
            metrics = json.loads(runtime_metric_files[0].read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"runtime_visual_conformance_metrics.json is invalid JSON: {exc}")
            metrics = {}
        if metrics.get("status") != "PASS":
            failures.append("runtime_visual_conformance_metrics.json status is not PASS")
        for surface_key, surface_label in (
            ("recording", "Recording Studio"),
            ("logViewer", "Log Viewer"),
        ):
            surface = metrics.get(surface_key) if isinstance(metrics, dict) else {}
            if not isinstance(surface, dict):
                failures.append(f"runtime_visual_conformance_metrics.json missing {surface_label} metrics")
                continue
            if surface.get("buttonPrimitiveVerdict") != "PASS":
                failures.append(f"{surface_label} button primitive verdict is not PASS")
            buttons = surface.get("buttonPrimitiveMeasurements")
            if not isinstance(buttons, list) or not buttons:
                failures.append(f"{surface_label} button primitive measurements are missing")
            else:
                for button in buttons:
                    if not isinstance(button, dict):
                        failures.append(f"{surface_label} button primitive row is not an object")
                        continue
                    if button.get("status") != "PASS":
                        failures.append(
                            f"{surface_label} button primitive mismatch for {button.get('key')}: "
                            f"{button.get('failures')}"
                        )
            if surface.get("controlPillGutterVerdict") != "PASS":
                failures.append(f"{surface_label} control pill gutter verdict is not PASS")
            if surface.get("actionLayoutVerdict") != "PASS":
                failures.append(f"{surface_label} action layout verdict is not PASS")
            action_layout = surface.get("actionLayoutMeasurements")
            if not isinstance(action_layout, dict):
                failures.append(f"{surface_label} action layout measurements are missing")
            elif surface_key == "recording":
                if int(action_layout.get("transportPillLeftAlignedPx") if action_layout.get("transportPillLeftAlignedPx") is not None else 999) > 1:
                    failures.append("Recording Studio transport pill is not left-aligned to the action row")
                if int(action_layout.get("openLogViewerRightAlignedPx") if action_layout.get("openLogViewerRightAlignedPx") is not None else 999) > 1:
                    failures.append("Recording Studio OPEN LOG VIEWER is not right-aligned to the action row")
                if int(action_layout.get("openLogViewerSeparatedFromTransportPx") or -1) < 12:
                    failures.append("Recording Studio OPEN LOG VIEWER is not separated from the transport pill")
            elif int(action_layout.get("exportedLogsRightAlignedPx") if action_layout.get("exportedLogsRightAlignedPx") is not None else 999) > 1:
                failures.append("Log Viewer exported logs action is not right-aligned to the action row")
            gutter = surface.get("controlPillGutterMeasurements")
            if not isinstance(gutter, dict):
                failures.append(f"{surface_label} control pill gutter measurements are missing")
            elif gutter.get("bottomGutterPx") != gutter.get("topGutterPx"):
                failures.append(
                    f"{surface_label} control pill bottom gutter {gutter.get('bottomGutterPx')}px "
                    f"does not match top gutter {gutter.get('topGutterPx')}px"
                )
        log_viewer = metrics.get("logViewer") if isinstance(metrics, dict) else {}
        if isinstance(log_viewer, dict):
            if int(log_viewer.get("bottomSlackPx", 999)) > int(log_viewer.get("maxAllowedBottomSlackPx", 18)):
                failures.append("Log Viewer bottom slack exceeds compact doorway-shell allowance")
            image_size = log_viewer.get("imageSize")
            if isinstance(image_size, dict) and int(image_size.get("height", 999)) > int(log_viewer.get("maxAllowedHeightPx", 142)):
                failures.append("Log Viewer default proof height exceeds compact doorway-shell allowance")
    if len(red_teams) != 1:
        failures.append(f"expected exactly one packet internal_visual_red_team_ledger.json, found {len(red_teams)}")
    if len(root_causes) != 1:
        failures.append(f"expected exactly one packet adjudication_failure_root_cause_ledger.json, found {len(root_causes)}")
    row_map_path = row_maps[0]
    evidence_root = row_map_path.parent
    try:
        row_map = json.loads(row_map_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"packet row_to_evidence_map.json is invalid JSON: {exc}"]
    missing_keys = sorted(CURRENT_PACKET_REQUIRED_EVIDENCE - set(row_map))
    if missing_keys:
        failures.append(f"packet row_to_evidence_map.json missing required evidence keys: {', '.join(missing_keys)}")
    for key, value in sorted(row_map.items()):
        value_text = str(value or "").strip()
        if not value_text:
            failures.append(f"packet evidence key {key!r} has empty path")
            continue
        if Path(value_text).is_absolute():
            failures.append(f"packet evidence key {key!r} uses absolute path instead of packet-relative path: {value_text}")
            continue
        target = evidence_root / value_text
        if not target.exists():
            failures.append(f"packet evidence key {key!r} points to missing packet media: {value_text}")
            continue
        if key in REQUIRED_CROP_COMPLETENESS and target.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            try:
                from PIL import Image

                with Image.open(target) as image:
                    width, height = image.size
            except Exception as exc:  # noqa: BLE001 - validation reports exact proof failure
                failures.append(f"packet evidence key {key!r} image unreadable: {exc}")
            else:
                rule = REQUIRED_CROP_COMPLETENESS[key]
                if width < int(rule["minWidth"]) or height < int(rule["minHeight"]):
                    failures.append(
                        f"packet evidence key {key!r} focused crop too small for complete proof: "
                        f"{width}x{height} < {rule['minWidth']}x{rule['minHeight']}"
                    )
        if key in COMPARATOR_CROP_RULES and target.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            try:
                from PIL import Image

                with Image.open(target) as image:
                    width, height = image.size
            except Exception as exc:  # noqa: BLE001 - validation reports exact proof failure
                failures.append(f"comparator evidence key {key!r} image unreadable: {exc}")
            else:
                rule = COMPARATOR_CROP_RULES[key]
                if width < int(rule["minWidth"]) or height < int(rule["minHeight"]):
                    failures.append(
                        f"comparator evidence key {key!r} is too small for its proof scope: "
                        f"{width}x{height} < {rule['minWidth']}x{rule['minHeight']}"
                    )
                if width > int(rule["maxWidth"]) or height > int(rule["maxHeight"]):
                    failures.append(
                        f"comparator evidence key {key!r} is too broad for its proof scope: "
                        f"{width}x{height} > {rule['maxWidth']}x{rule['maxHeight']}"
                    )
                if "contact_sheet" in value_text:
                    failures.append(f"comparator evidence key {key!r} points to broad contact sheet instead of focused comparator media")
    comparator_ledgers = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/comparator_crop_ledger.json"))
    comparator_rows_by_key: dict[str, dict[str, object]] = {}
    if len(comparator_ledgers) != 1:
        failures.append(f"expected exactly one packet comparator_crop_ledger.json, found {len(comparator_ledgers)}")
    else:
        try:
            comparator_ledger = json.loads(comparator_ledgers[0].read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"comparator_crop_ledger.json is invalid JSON: {exc}")
            comparator_ledger = {}
        if isinstance(comparator_ledger, dict):
            if comparator_ledger.get("status") != "PASS":
                failures.append("comparator_crop_ledger.json status is not PASS")
            duplicate_groups = comparator_ledger.get("duplicateHashGroups")
            if duplicate_groups:
                failures.append(f"comparator_crop_ledger.json reports duplicate comparator hashes: {duplicate_groups}")
            comparator_ledger_rows = comparator_ledger.get("rows", [])
            if not isinstance(comparator_ledger_rows, list):
                failures.append("comparator_crop_ledger.json rows is not a list")
                comparator_ledger_rows = []
            comparator_rows_by_key = {
                str(row.get("comparatorEvidenceKey", "")): row
                for row in comparator_ledger_rows
                if isinstance(row, dict)
            }
            missing_comparator_rows = sorted(set(COMPARATOR_CROP_RULES) - set(comparator_rows_by_key))
            if missing_comparator_rows:
                failures.append(
                    "comparator_crop_ledger.json missing rows: " + ", ".join(missing_comparator_rows)
                )
            seen_hashes: dict[str, list[str]] = {}
            for key, rule in COMPARATOR_CROP_RULES.items():
                item = comparator_rows_by_key.get(key)
                if not isinstance(item, dict):
                    continue
                if item.get("comparatorCropFile") != row_map.get(key):
                    failures.append(f"comparator crop ledger row {key} crop file does not match row map")
                overlay_path = str(item.get("comparatorOverlayProofFile", "")).strip()
                if not overlay_path:
                    failures.append(f"comparator crop ledger row {key} missing comparatorOverlayProofFile")
                elif Path(overlay_path).is_absolute():
                    failures.append(f"comparator crop ledger row {key} overlay path is absolute")
                elif not (evidence_root / overlay_path).exists():
                    failures.append(f"comparator crop ledger row {key} overlay file missing from packet: {overlay_path}")
                source_path = str(item.get("comparatorSourceScreenshot", "")).strip()
                if not source_path:
                    failures.append(f"comparator crop ledger row {key} missing comparatorSourceScreenshot")
                elif Path(source_path).is_absolute():
                    failures.append(f"comparator crop ledger row {key} source screenshot is absolute")
                elif not (evidence_root / source_path).exists():
                    failures.append(f"comparator crop ledger row {key} source screenshot missing from packet: {source_path}")
                crop_type = str(item.get("cropType", "")).strip()
                if crop_type != rule["cropType"]:
                    failures.append(f"comparator crop ledger row {key} cropType mismatch: {crop_type} != {rule['cropType']}")
                proof_kind = str(item.get("broadContextOrFocusedProof", "")).strip()
                if proof_kind != rule["proofKind"]:
                    failures.append(f"comparator crop ledger row {key} proof kind mismatch: {proof_kind} != {rule['proofKind']}")
                if item.get("finalComparatorCropVerdict") != "PERFECT_PASS":
                    failures.append(f"comparator crop ledger row {key} is not PERFECT_PASS")
                if item.get("contentMatchesEvidenceKey") is not True:
                    failures.append(f"comparator crop ledger row {key} does not prove contentMatchesEvidenceKey")
                if item.get("overlayRectangleProofPresent") is not True:
                    failures.append(f"comparator crop ledger row {key} does not prove overlayRectangleProofPresent")
                if item.get("readableAtElementLevel") is not True:
                    failures.append(f"comparator crop ledger row {key} does not prove readableAtElementLevel")
                crop_size = item.get("cropSize")
                if not isinstance(crop_size, dict):
                    failures.append(f"comparator crop ledger row {key} missing cropSize")
                else:
                    width = int(crop_size.get("width", 0))
                    height = int(crop_size.get("height", 0))
                    if width < int(rule["minWidth"]) or height < int(rule["minHeight"]):
                        failures.append(f"comparator crop ledger row {key} crop too small: {width}x{height}")
                    if width > int(rule["maxWidth"]) or height > int(rule["maxHeight"]):
                        failures.append(f"comparator crop ledger row {key} crop too broad: {width}x{height}")
                digest = str(item.get("sha256", "")).strip()
                if not digest:
                    failures.append(f"comparator crop ledger row {key} missing sha256")
                else:
                    seen_hashes.setdefault(digest, []).append(key)
            for digest, keys in seen_hashes.items():
                if len(keys) > 1:
                    failures.append(
                        f"duplicate comparator media hash {digest[:12]} reused across incompatible keys: {', '.join(keys)}"
                    )
    current_keys = {row.packet_evidence_key for row in rows if row.final_disposition == "PERFECT_PASS"}
    unmapped = sorted(key for key in current_keys if key and key not in row_map)
    if unmapped:
        failures.append(f"current-branch ledger rows reference packet evidence keys absent from row map: {', '.join(unmapped)}")
    comparator_keys = {
        row.comparator_evidence_key
        for row in rows
        if row.final_disposition == "PERFECT_PASS" and row.accepted_comparator and row.comparator_evidence_key
    }
    missing_comparator_keys = sorted(key for key in comparator_keys if key not in row_map)
    if missing_comparator_keys:
        failures.append(
            f"green comparator rows reference comparator evidence keys absent from row map: {', '.join(missing_comparator_keys)}"
        )
    for row in rows:
        if row.final_disposition != "PERFECT_PASS":
            continue
        if not row.primary_packet_evidence_path:
            failures.append(f"{row.row_id}: missing primary_packet_evidence_path")
        elif Path(row.primary_packet_evidence_path).is_absolute():
            failures.append(f"{row.row_id}: primary_packet_evidence_path is absolute")
        elif row.packet_evidence_key and row.primary_packet_evidence_path != str(row_map.get(row.packet_evidence_key, "")):
            failures.append(f"{row.row_id}: primary_packet_evidence_path does not match row_to_evidence_map")
        if row.accepted_comparator:
            mapped_comparator = str(row_map.get(row.comparator_evidence_key, "")).strip()
            if not row.comparator_evidence_key:
                failures.append(f"{row.row_id}: missing comparator_evidence_key")
            elif not mapped_comparator:
                failures.append(f"{row.row_id}: comparator evidence key absent from row map: {row.comparator_evidence_key}")
            elif mapped_comparator != row.comparator_packet_evidence_path:
                failures.append(
                    f"{row.row_id}: comparator_packet_evidence_path does not match row_to_evidence_map"
                )
            if row.comparator_evidence_key == "contact-sheet" or "contact_sheet" in row.comparator_packet_evidence_path:
                failures.append(f"{row.row_id}: broad comparator contact sheet used as row-bound comparator proof")
            if not row.comparator_owner or not row.comparator_proof_scope or not row.comparator_source_truth_rule:
                failures.append(f"{row.row_id}: comparator metadata incomplete")
            if row.comparator_evidence_key and row.comparator_evidence_key not in row.row_specific_comparator_finding:
                failures.append(f"{row.row_id}: row-specific comparator finding does not cite comparator evidence key")
            if not row.comparator_crop_ledger_key:
                failures.append(f"{row.row_id}: missing comparator_crop_ledger_key")
            elif row.comparator_crop_ledger_key != row.comparator_evidence_key:
                failures.append(f"{row.row_id}: comparator_crop_ledger_key does not match comparator_evidence_key")
            elif row.comparator_crop_ledger_key not in comparator_rows_by_key:
                failures.append(f"{row.row_id}: comparator_crop_ledger_key absent from comparator_crop_ledger.json")
            if not row.exact_reason_comparator_sufficient:
                failures.append(f"{row.row_id}: missing exact_reason_comparator_sufficient")
            elif row.comparator_evidence_key and row.comparator_evidence_key not in row.exact_reason_comparator_sufficient:
                failures.append(f"{row.row_id}: exact_reason_comparator_sufficient does not cite comparator evidence key")
    if manifests:
        try:
            manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"visual_capture_manifest.json is invalid JSON: {exc}")
        else:
            resize = manifest.get("resizeProof", {})
            crop_checks = manifest.get("cropCompletenessChecks", {})
            if not isinstance(crop_checks, dict):
                failures.append("visual_capture_manifest.json missing cropCompletenessChecks object")
                crop_checks = {}
            for key, rule in REQUIRED_CROP_COMPLETENESS.items():
                check = crop_checks.get(key)
                if not isinstance(check, dict):
                    failures.append(f"visual_capture_manifest.json missing cropCompletenessChecks entry for {key}")
                    continue
                if str(check.get("crop", "")).strip() != str(row_map.get(key, "")).strip():
                    failures.append(f"cropCompletenessChecks entry for {key} does not match row_to_evidence_map")
                for required in rule["requires"]:
                    if check.get(required) is not True:
                        failures.append(f"cropCompletenessChecks entry for {key} has non-true {required}")
                if check.get("noUndeclaredAdjacentPartialText") is not True:
                    failures.append(f"cropCompletenessChecks entry for {key} has undeclared adjacent text risk")
                overlay_path = str(check.get("overlayProofFile", "")).strip()
                if not overlay_path:
                    failures.append(f"cropCompletenessChecks entry for {key} missing overlayProofFile")
                elif Path(overlay_path).is_absolute():
                    failures.append(f"cropCompletenessChecks entry for {key} overlayProofFile is absolute: {overlay_path}")
                elif not (evidence_root / overlay_path).exists():
                    failures.append(f"cropCompletenessChecks entry for {key} overlayProofFile is missing from packet: {overlay_path}")
                content_method = str(check.get("contentValidationMethod", "")).casefold()
                for token in ("dom", "overlay", "adjacent", "geometry", "text", "scope"):
                    if token not in content_method:
                        failures.append(
                            f"cropCompletenessChecks entry for {key} contentValidationMethod lacks {token!r}"
                        )
                validated_by = str(check.get("validatedBy", "")).strip()
                if not validated_by:
                    failures.append(f"cropCompletenessChecks entry for {key} missing validatedBy")
                else:
                    lowered = validated_by.casefold()
                    for token in ("overlay", "adjacent", "text", "scope"):
                        if token not in lowered:
                            failures.append(
                                f"cropCompletenessChecks entry for {key} validatedBy lacks {token!r}"
                            )
            crop_ledgers = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/crop_completeness_ledger.json"))
            if len(crop_ledgers) != 1:
                failures.append(f"expected exactly one packet crop_completeness_ledger.json, found {len(crop_ledgers)}")
            else:
                try:
                    crop_ledger = json.loads(crop_ledgers[0].read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    failures.append(f"crop_completeness_ledger.json is invalid JSON: {exc}")
                    crop_ledger = {}
                rows_by_key = {
                    str(item.get("key", "")): item
                    for item in crop_ledger.get("rows", [])
                    if isinstance(item, dict)
                } if isinstance(crop_ledger, dict) else {}
                if isinstance(crop_ledger, dict) and crop_ledger.get("status") != "PASS":
                    failures.append("crop_completeness_ledger.json status is not PASS")
                for key in REQUIRED_CROP_COMPLETENESS:
                    item = rows_by_key.get(key)
                    if not isinstance(item, dict):
                        failures.append(f"crop_completeness_ledger.json missing row for {key}")
                        continue
                    for required in (
                        "cropFile",
                        *REQUIRED_CROP_CONTENT_FIELDS,
                        "sourceFullWindowFile",
                        "cropRect",
                        "targetElementRect",
                        "marginAroundTarget",
                        "expectedTextInsideCrop",
                        "textPresenceCheck",
                        "borderRadiusGlowInclusionCheck",
                        "surroundingContextCheck",
                        "targetContentTouchesCropEdge",
                        "targetTextControlOrBorderCutOff",
                        "finalCropVerdict",
                    ):
                        if required not in item:
                            failures.append(f"crop completeness row {key} missing {required}")
                    if item.get("cropFile") != row_map.get(key):
                        failures.append(f"crop completeness row {key} cropFile does not match row map")
                    crop_type = str(item.get("cropType", "")).strip()
                    if crop_type not in VALID_CROP_TYPES:
                        failures.append(f"crop completeness row {key} has invalid or missing cropType: {crop_type or '<missing>'}")
                        crop_type = "ELEMENT_CROP"
                    required_crop_type = REQUIRED_CROP_TYPES.get(key)
                    if required_crop_type and crop_type != required_crop_type:
                        failures.append(f"crop completeness row {key} cropType mismatch: {crop_type} != {required_crop_type}")
                    if not str(item.get("declaredTargetScope", "")).strip():
                        failures.append(f"crop completeness row {key} missing declaredTargetScope")
                    included_adjacent = item.get("includedAdjacentElements")
                    if not isinstance(included_adjacent, list):
                        failures.append(f"crop completeness row {key} missing includedAdjacentElements list")
                        included_adjacent = []
                    included_rects = item.get("includedElementRects")
                    if not isinstance(included_rects, list):
                        failures.append(f"crop completeness row {key} missing includedElementRects list")
                        included_rects = []
                    relationship = str(item.get("relationshipBeingProven", "")).strip()
                    if crop_type in {"RELATIONSHIP_CROP", "STATE_CROP", "RESIZE_STATE_CROP"} and not relationship:
                        failures.append(f"relationship crop {key} does not name the relationship being proven")
                    if crop_type == "ELEMENT_CROP" and (included_adjacent or relationship or included_rects):
                        failures.append(f"element crop {key} declares relationship/adjacent elements instead of staying clean")
                    if crop_type in {"RELATIONSHIP_CROP", "STATE_CROP", "RESIZE_STATE_CROP"} and not included_adjacent:
                        failures.append(f"{crop_type} row {key} does not declare included elements")
                    overlay_file = str(item.get("overlayProofFile", "")).strip()
                    if not overlay_file:
                        failures.append(f"crop completeness row {key} missing overlayProofFile")
                    elif Path(overlay_file).is_absolute():
                        failures.append(f"crop completeness row {key} overlayProofFile is absolute primary proof: {overlay_file}")
                    elif not (evidence_root / overlay_file).exists():
                        failures.append(f"crop completeness row {key} overlayProofFile target is missing from packet: {overlay_file}")
                    source_file = str(item.get("sourceFullWindowFile", "")).strip()
                    if not source_file:
                        failures.append(f"crop completeness row {key} missing sourceFullWindowFile")
                    elif Path(source_file).is_absolute():
                        failures.append(f"crop completeness row {key} sourceFullWindowFile is absolute primary proof: {source_file}")
                    elif source_file not in row_map.values():
                        failures.append(f"crop completeness row {key} sourceFullWindowFile is not a packet row-map path: {source_file}")
                    elif not (evidence_root / source_file).exists():
                        failures.append(f"crop completeness row {key} sourceFullWindowFile target is missing from packet: {source_file}")
                    if item.get("finalCropVerdict") != "PERFECT_PASS":
                        failures.append(f"crop completeness row {key} is not PERFECT_PASS")
                    if item.get("targetContentTouchesCropEdge") is True or item.get("targetTextControlOrBorderCutOff") is True:
                        failures.append(f"crop completeness row {key} says target is clipped or touches crop edge")
                    expected_text = item.get("expectedTextInsideCrop")
                    if not isinstance(expected_text, list) or not expected_text:
                        failures.append(f"crop completeness row {key} missing expected text list")
                        expected_text = []
                    visible_text = item.get("allVisibleTextFoundInCrop")
                    if not isinstance(visible_text, list) or not visible_text:
                        failures.append(f"crop completeness row {key} missing allVisibleTextFoundInCrop list")
                        visible_text = []
                    normalized_expected = {str(text).casefold().strip() for text in expected_text if str(text).strip()}
                    for required_text in REQUIRED_SCOPE_TEXT.get(key, []):
                        if required_text.casefold().strip() not in normalized_expected:
                            failures.append(
                                f"crop completeness row {key} expectedTextInsideCrop omits required visible scope text: {required_text}"
                            )
                    joined_visible_text = " ".join(str(text) for text in visible_text).casefold()
                    for expected in expected_text:
                        if str(expected).casefold() not in joined_visible_text:
                            failures.append(f"crop completeness row {key} expected text absent from visible-text audit: {expected}")
                    for required_text in REQUIRED_SCOPE_TEXT.get(key, []):
                        if required_text.casefold() not in joined_visible_text:
                            failures.append(
                                f"crop completeness row {key} required scope text absent from allVisibleTextFoundInCrop: {required_text}"
                            )
                    excluded_text = item.get("visibleTextExcludedFromTargetProof")
                    if not isinstance(excluded_text, list):
                        failures.append(f"crop completeness row {key} missing visibleTextExcludedFromTargetProof list")
                        excluded_text = []
                    if excluded_text and not str(item.get("excludedVisibleTextReason", "")).strip():
                        failures.append(f"crop completeness row {key} excludes visible text without reason")
                    extra_text = item.get("extraUndeclaredVisibleText")
                    if not isinstance(extra_text, list):
                        failures.append(f"crop completeness row {key} missing extraUndeclaredVisibleText list")
                        extra_text = []
                    if extra_text:
                        failures.append(f"crop completeness row {key} has visible text neither expected nor excluded: {extra_text}")
                    if item.get("finalTextAuditVerdict") != "PERFECT_PASS":
                        failures.append(f"crop completeness row {key} finalTextAuditVerdict is not PERFECT_PASS")
                    adjacent = item.get("adjacentPartialTextFoundInCrop")
                    if not isinstance(adjacent, list):
                        failures.append(f"crop completeness row {key} adjacentPartialTextFoundInCrop is not a list")
                        adjacent = []
                    if adjacent and item.get("adjacentPartialTextAllowed") is not True:
                        failures.append(f"crop completeness row {key} has undeclared adjacent partial text: {adjacent}")
                    adjacent_geometry = item.get("adjacentPartialGeometryFoundInCrop")
                    if not isinstance(adjacent_geometry, list):
                        failures.append(f"crop completeness row {key} adjacentPartialGeometryFoundInCrop is not a list")
                        adjacent_geometry = []
                    if (
                        adjacent_geometry
                        and crop_type == "ELEMENT_CROP"
                        and item.get("adjacentPartialTextAllowed") is not True
                    ):
                        geometry_keys = ", ".join(str(entry.get("elementKey", "")) for entry in adjacent_geometry if isinstance(entry, dict))
                        failures.append(f"element crop {key} contains adjacent geometry outside target rectangle: {geometry_keys}")
                    if adjacent_geometry and item.get("adjacentPartialTextAllowed") is not True:
                        failures.append(f"crop completeness row {key} includes adjacent geometry but adjacent content is not declared/allowed")
                    contradiction = item.get("cropLedgerContradictionCheck")
                    if not isinstance(contradiction, dict):
                        failures.append(f"crop completeness row {key} missing cropLedgerContradictionCheck object")
                    else:
                        if contradiction.get("overlayMatchesLedger") is not True:
                            failures.append(f"crop completeness row {key} overlay does not match ledger")
                        if contradiction.get("detectedAdjacentGeometryCount") != len(adjacent_geometry):
                            failures.append(f"crop completeness row {key} contradiction check does not count adjacent geometry")
                    for required_bool in (
                        "fullTargetBorderRadiusGlowIncluded",
                        "fullTargetTextControlIncluded",
                        "surroundingContextIncluded",
                        "cropNotHidingAdjacentDefect",
                    ):
                        if item.get(required_bool) is not True:
                            failures.append(f"crop completeness row {key} has non-true {required_bool}")
                    content_method = str(item.get("contentValidationMethod", "")).casefold()
                    for token in ("dom", "overlay", "adjacent", "geometry", "text", "scope"):
                        if token not in content_method:
                            failures.append(f"crop completeness row {key} contentValidationMethod lacks {token!r}")
            if resize.get("method") in {"scripted-resize-call", "setGeometry-only"}:
                failures.append("resize proof uses forbidden scripted/direct geometry method")
            runtime_truth = str(resize.get("runtimeTruth", ""))
            if "exact-desktop-launcher-live-validation-still-required" not in runtime_truth:
                failures.append("resize proof must explicitly separate pre-LV evidence from exact desktop launcher LV proof")
            if (
                resize.get("method") == "runtime-widget-edge-drag-with-top-level-resize-handler"
                and not resize.get("widthIncreased")
            ):
                failures.append("runtime edge resize proof must show a width increase")
    if red_teams:
        try:
            red_team = json.loads(red_teams[0].read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"internal_visual_red_team_ledger.json is invalid JSON: {exc}")
        else:
            if "REPAIR_REQUIRED" in json.dumps(red_team):
                failures.append("internal visual red-team ledger still contains REPAIR_REQUIRED")
    return failures


def packet_hygiene_summary() -> dict[str, object]:
    zips = sorted(USER_ROOT.glob("FAM-006*.zip"), key=lambda path: path.name)
    primary_files = sorted((PACKET_ROOT / "USER Review").glob("*.md")) if (PACKET_ROOT / "USER Review").exists() else []
    return {
        "packetRoot": str(PACKET_ROOT),
        "packetRootExists": PACKET_ROOT.exists(),
        "zipCount": len(zips),
        "zipFiles": [str(path) for path in zips],
        "zipSha256": {path.name: _sha256(path) for path in zips if path.is_file()},
        "stableZipPresent": (USER_ROOT / "FAM-006.zip").exists(),
        "startHerePresent": (PACKET_ROOT / "START_HERE.md").exists(),
        "primaryUserReviewCount": len(primary_files),
        "primaryUserReviewFiles": [str(path) for path in primary_files],
    }


def render_markdown(rows: list[VisualLedgerRow]) -> str:
    lines = [
        "# FAM-006 Stop-The-Line Exhaustive Visual Conformance Ledger",
        "",
        "Status: FAIL / REPAIR until renewed photo/video proof and USER packet hygiene are green.",
        "",
        "Final disposition vocabulary is restricted. Vague progress language is not accepted as green.",
        "",
        "| Row ID | Surface | Element Group | Window Class | Packet Evidence Key | Primary Packet Evidence Path | Comparator Evidence Key | Comparator Packet Evidence Path | Comparator Finding | Code Path | State Coverage | Final Disposition |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.row_id,
                    row.surface,
                    row.element_group,
                    row.window_class,
                    row.packet_evidence_key or "N/A",
                    row.primary_packet_evidence_path or "N/A",
                    row.comparator_evidence_key or "N/A",
                    row.comparator_packet_evidence_path or "N/A",
                    row.row_specific_comparator_finding,
                    row.code_path,
                    row.state_coverage,
                    row.final_disposition,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="Write ledger JSON/Markdown to this folder.")
    args = parser.parse_args()

    if is_runtime_ui_immersion_options_packet():
        udl_gate = validate_udl_state(PACKET_ROOT if PACKET_ROOT.exists() else None)
        failures = []
        if udl_gate["status"] != "PASS":
            failures.extend(f"UDL gate: {failure}" for failure in udl_gate.get("failures", []))
        proof = {
            "status": "PASS" if not failures else "FAIL",
            "packetClass": "dual-recording-candidate-log-viewer-rename",
            "disposition": "NOT_APPLICABLE_CANDIDATE_SELECTION_PACKET",
            "reason": (
                "The exhaustive visual conformance ledger enforces implementation-proof crop/row maps. "
                "The current packet is rendered candidate-selection review evidence and does not claim final Recording winner selection, runtime implementation, H1, LV, UTS, or PR readiness."
            ),
            "rowCount": 0,
            "helperRunPacketHygieneSnapshot": {
                "snapshotScope": "helper-run observation only for design-options packet",
                **packet_hygiene_summary(),
            },
            "unifiedDefectLedgerGate": udl_gate,
            "failures": failures,
        }
        if args.write:
            args.write.mkdir(parents=True, exist_ok=True)
            (args.write / "EXHAUSTIVE_VISUAL_CONFORMANCE_LEDGER.md").write_text(
                "# FAM-006 Stop-The-Line Exhaustive Visual Conformance Ledger\n\n"
                "Status: NOT_APPLICABLE_CANDIDATE_SELECTION_PACKET.\n\n"
                "This packet is review-only rendered candidate-selection evidence. Implementation-proof visual conformance remains required after USER selects a candidate and approves bounded runtime implementation-match repair.\n",
                encoding="utf-8",
            )
            (args.write / "exhaustive_visual_conformance_ledger.json").write_text(
                json.dumps(proof, indent=2),
                encoding="utf-8",
            )
        print(json.dumps(proof, indent=2))
        return 0 if not failures else 1

    # Product/runtime source is scanned for stale visual markers. Validators may
    # mention forbidden strings as rejection patterns, so they are intentionally
    # excluded from this source-marker pass.
    source_text = "\n".join(
        [
            _read("desktop/desktop_renderer.py"),
            _read("nexus_visual/monitoring_hud_studio.html"),
            _read("nexus_visual/monitoring_hud_studio.js"),
            _read("nexus_visual/nexus_window_primitives.css"),
        ]
    )
    rows = build_rows()
    failures = validate_rows(rows, source_text)
    failures.extend(validate_packet_evidence(rows))
    udl_gate = validate_udl_state(PACKET_ROOT if PACKET_ROOT.exists() else None)
    if udl_gate["status"] != "PASS":
        failures.extend(f"UDL gate: {failure}" for failure in udl_gate.get("failures", []))
    helper_snapshot = packet_hygiene_summary()
    proof = {
        "status": "PASS" if not failures else "FAIL",
        "rowCount": len(rows),
        "allowedFinalDispositions": sorted(ALLOWED_FINAL_DISPOSITIONS),
        "helperRunPacketHygieneSnapshot": {
            "snapshotScope": "helper-run observation only; final USER packet hygiene is generated after packet folder and timestamped ZIP creation",
            **helper_snapshot,
        },
        "unifiedDefectLedgerGate": udl_gate,
        "rows": [asdict(row) for row in rows],
        "failures": failures,
    }
    if args.write:
        args.write.mkdir(parents=True, exist_ok=True)
        (args.write / "EXHAUSTIVE_VISUAL_CONFORMANCE_LEDGER.md").write_text(
            render_markdown(rows),
            encoding="utf-8",
        )
        (args.write / "exhaustive_visual_conformance_ledger.json").write_text(
            json.dumps(proof, indent=2),
            encoding="utf-8",
        )
    print(json.dumps(proof, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
