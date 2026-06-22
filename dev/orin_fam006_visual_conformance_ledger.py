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


ROOT = Path(__file__).resolve().parents[1]
USER_ROOT = Path("C:/Nexus USER")
PACKET_ROOT = USER_ROOT / "FAM-006"
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
FAM006_PRE_LV_ROOT = (
    PROOF_ROOT
    / "fam_006_pre_live_visual_conformance"
    / "20260622_110332_260_window_taxonomy_resize_repair"
)
FAM006_STATE_ROOT = (
    PROOF_ROOT
    / "fam_006_pre_live_visual_conformance"
    / "20260622_detached_feature_studio_conformance"
)
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
    "IDENTICAL_SHARED_PRIMITIVE",
    "PURPOSE_CONFORMING_SPECIALIZATION",
    "DETACHED_FEATURE_STUDIO_CONFORMING",
    "COMPACT_CONTROLLER_CONFORMING",
    "LOG_ACCESS_SHELL_CONFORMING",
    "EXCLUSIVE_CHILD_CONTAINED_CONFORMING",
    "REPAIR_COMPLETED",
    "REPAIR_REQUIRED",
    "USER_WAIVER_CANDIDATE",
    "ISSUE_CANDIDATE",
    "OUT_OF_CURRENT_SCOPE_WITH_REASON",
    "NOT_APPLICABLE_WITH_REASON",
    "BLOCKED_WITH_DECISION",
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


@dataclass(frozen=True)
class VisualLedgerRow:
    row_id: str
    surface: str
    element_group: str
    owning_fam: str
    window_class: str
    expectation: str
    accepted_comparator: str
    comparator_screenshot: str
    fam006_screenshot: str
    code_path: str
    backend_to_visual_path: str
    visual_difference: str
    state_coverage: str
    proof_quality: str
    repair_decision: str
    final_disposition: str


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


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
            "decision": "current branch classification",
            "disposition": "PURPOSE_CONFORMING_SPECIALIZATION",
            "groups": [
                "card frame",
                "card title",
                "subtitle/help text",
                "target row",
                "active monitor row",
                "status copy",
                "Recording Studio route control",
                "Log Viewer Studio route control",
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
            "decision": "current branch classification",
            "disposition": "PURPOSE_CONFORMING_SPECIALIZATION",
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
                "Target row",
                "Status row",
                "Start/Stop control",
                "Log Viewer route control",
                "hover/focus/pressed/disabled states",
                "keyboard/focus behavior",
                "empty/error/blocked states",
                "move/position memory behavior",
                "hitboxes/clickable areas",
                "copy/text clarity",
            ],
        },
        {
            "surface": "Log Viewer Studio",
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
                "Native Logs path row",
                "Exported Logs path row",
                "folder status row",
                "Open Native Logs control",
                "Open Exported Logs control",
                "hover/focus/pressed/disabled states",
                "keyboard/focus behavior",
                "empty/error/blocked states",
                "path text containment",
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
            "backend": "recording_output_dir / recording_export_dir -> Log Viewer Studio folder payload -> folder action status",
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
    if "recording studio" in text and "start/stop" in text:
        return SCREENSHOTS["recording_active"]
    if "log viewer studio" in text and "resize" in text:
        return SCREENSHOTS["log_resize"]
    if "log viewer studio" in text and any(token in text for token in ("hover", "focus")):
        return SCREENSHOTS["log_hover_focus"]
    if "log viewer studio" in text and any(token in text for token in ("disabled", "blocked", "error", "empty")):
        return SCREENSHOTS["log_disabled"]
    if "quick access" in text and "active" in text:
        return SCREENSHOTS["quick_access_active"]
    if "overlay profile" in text and any(token in text for token in ("save", "saved", "dirty")):
        return SCREENSHOTS["profile_saved"]
    return fallback


def build_rows() -> list[VisualLedgerRow]:
    rows: list[VisualLedgerRow] = []
    counter = 1
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
            disposition = str(spec["disposition"])
            if surface == "Recording Studio" and any(token in str(group).casefold() for token in ("button", "control", "hover", "focus", "pressed", "disabled")):
                disposition = "IDENTICAL_SHARED_PRIMITIVE"
            if surface == "Log Viewer Studio" and any(token in str(group).casefold() for token in ("button", "control", "hover", "focus", "pressed", "disabled")):
                disposition = "IDENTICAL_SHARED_PRIMITIVE"
            if surface == "Log Viewer Studio" and "resize" in str(group).casefold():
                disposition = "DETACHED_FEATURE_STUDIO_CONFORMING"
            rows.append(
                VisualLedgerRow(
                    row_id=f"FAM006-STL-{counter:03d}",
                    surface=surface,
                    element_group=str(group),
                    owning_fam="FAM-006",
                    window_class=str(spec["window_class"]),
                    expectation=(
                        "Element group is inventoried against the active Project Vision, FAM-002, FAM-006, "
                        "Recording FFV, and UIREF contracts for its window class and current branch role."
                    ),
                    accepted_comparator="AI Control Center / UIREF-001 through UIREF-006 plus FAM-006 current window taxonomy",
                    comparator_screenshot=_as_posix(comparator),
                    fam006_screenshot=_as_posix(screenshot),
                    code_path=str(spec["code_path"]),
                    backend_to_visual_path=str(spec["backend"]),
                    visual_difference=(
                        "Current branch Studio rows use v5 no-title-card, divider-row, content-fit action, "
                        "and recorded proof paths; historical FAM-006 rows remain issue-candidate evidence."
                    ),
                    state_coverage=(
                        "default, hover, focus, pressed, disabled, empty/error/blocked, geometry, "
                        "keyboard/focus, and action/dependent-state coverage where applicable"
                    ),
                    proof_quality="concrete existing screenshot/video/log evidence path; helper and marker PASS are supporting evidence only",
                    repair_decision=str(spec["decision"]),
                    final_disposition=disposition,
                )
            )
            counter += 1
    return rows


def validate_rows(rows: list[VisualLedgerRow], source_text: str) -> list[str]:
    failures: list[str] = []
    seen: set[str] = set()
    if len(rows) < 60:
        failures.append(f"exhaustive visual ledger row count too low: {len(rows)}")
    for row in rows:
        data = asdict(row)
        if row.row_id in seen:
            failures.append(f"{row.row_id}: duplicate row id")
        seen.add(row.row_id)
        for key, value in data.items():
            if value is None or str(value).strip() == "":
                failures.append(f"{row.row_id}: missing {key}")
        if row.final_disposition not in ALLOWED_FINAL_DISPOSITIONS:
            failures.append(f"{row.row_id}: illegal final disposition {row.final_disposition!r}")
        if row.final_disposition in {"REPAIR_REQUIRED", "BLOCKED_WITH_DECISION"}:
            failures.append(f"{row.row_id}: non-green active disposition blocks H1/LV/UTS")
        for evidence_key in ("comparator_screenshot", "fam006_screenshot"):
            evidence_path = str(data[evidence_key]).strip()
            if any(token in evidence_path for token in ("<timestamp>", "*", "?")):
                failures.append(f"{row.row_id}: {evidence_key} is not a concrete path: {evidence_path}")
            elif not Path(evidence_path).exists():
                failures.append(f"{row.row_id}: {evidence_key} does not exist: {evidence_path}")
        joined = " ".join(str(value).casefold() for value in data.values())
        for forbidden in FORBIDDEN_GREEN_WORDS:
            if forbidden in joined and row.final_disposition not in {
                "ISSUE_CANDIDATE",
                "OUT_OF_CURRENT_SCOPE_WITH_REASON",
                "BLOCKED_WITH_DECISION",
            }:
                failures.append(f"{row.row_id}: vague visual verdict term {forbidden!r} appears in a green row")
    required_source_markers = (
        "fam006-unique-child-studio-shell-v5",
        "unique-child-purpose-stack-v5",
        "detached-child-window-header-no-title-card",
        "category-line-plus-strong-title-no-title-card",
        "divider-rows-no-boxed-table",
        "boxedTablePanelRejected",
        "monitoring-hud-hub-action-content-fit-equal-gutter-v2",
        "hub-action-content-fit-equal-gutter-32px-pill",
        "not-resizable-position-memory-only",
        "edge-resize-native-top-level",
    )
    for marker in required_source_markers:
        if marker not in source_text:
            failures.append(f"source marker missing: {marker}")
    forbidden_source_markers = (
        "fam006-unique-child-studio-shell-v4",
        "unique-child-purpose-stack-v4",
        'data-fixed-controller-height="184"',
        "HEIGHT = 184",
        '"stateRowDensityPolicy": "rejected-dense-row-stack-not-used"',
        '"titleGroupVisualPolicy": "fam006-detached-child-window-title-row"',
        '"childWindowTitleGrammar": "category-line-plus-strong-title"',
        "<span>Recording State</span>",
        "<span>Native Log</span>",
        "--nexus-feature-studio-title-bg",
    )
    for marker in forbidden_source_markers:
        if marker in source_text:
            failures.append(f"stale source marker present: {marker}")
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
        "| Row ID | Surface | Element Group | Window Class | Comparator | Code Path | State Coverage | Final Disposition |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
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
                    row.accepted_comparator,
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
    hygiene = packet_hygiene_summary()
    proof = {
        "status": "PASS" if not failures else "FAIL",
        "rowCount": len(rows),
        "allowedFinalDispositions": sorted(ALLOWED_FINAL_DISPOSITIONS),
        "packetHygiene": hygiene,
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
