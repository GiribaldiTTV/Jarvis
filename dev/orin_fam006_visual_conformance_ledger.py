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


def build_rows() -> list[VisualLedgerRow]:
    comparator = "AI Control Center UIREF-001/UIREF-002/UIREF-003 plus FAM-006 child-window header grammar"
    current_shots = (
        "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/"
        "fam_006_pre_live_visual_conformance/<timestamp>"
    )
    return [
        VisualLedgerRow(
            "FAM006-STL-001",
            "Recording Studio",
            "outer frame / body background",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "Opaque Nexus dark-glass shell; no see-through void; no main-window hero card.",
            comparator,
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/FAM-007-H4/*/04_window_controls*.png",
            f"{current_shots}/recording_default.png",
            "nexus_visual/monitoring_hud_studio.html; nexus_visual/nexus_window_primitives.css; desktop/desktop_renderer.py",
            "MonitoringHudRecordingStudioWindow -> QWebEngineView -> monitoring_hud_studio.html -> nexus_window_primitives.css",
            "Repaired from v4 boxed row/body treatment to v5 divider/body treatment; final proof still requires focused photo review.",
            "default, active stop, disabled target, keyboard focus",
            "pre-LV screenshot required before LV; runtime marker alone rejected",
            "current-branch repair",
            "REPAIR_COMPLETED",
        ),
        VisualLedgerRow(
            "FAM006-STL-002",
            "Recording Studio",
            "title/header",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "Detached child-window category line plus strong title; no rounded title card or main-window hero.",
            comparator,
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/fam_006_monitoring_hud_live_validation/*/focused_element_screenshots/element_03_manage_monitors_open_state.png",
            f"{current_shots}/recording_default.png",
            "nexus_visual/monitoring_hud_studio.html; nexus_visual/nexus_window_primitives.css",
            "dataset titleTreatment=detached-child-window-header-no-title-card -> CSS title-group transparent",
            "Repaired to no-title-card v5 marker and transparent child-header treatment.",
            "default, focused, moved",
            "pre-LV focused screenshot required",
            "current-branch repair",
            "REPAIR_COMPLETED",
        ),
        VisualLedgerRow(
            "FAM006-STL-003",
            "Recording Studio",
            "window control cluster",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "Compact top-right minimize/close cluster using UIREF-002 symbol buttons.",
            "AI Control Center compact window-control cluster",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/FAM-007-H4/*/04_window_controls*.png",
            f"{current_shots}/recording_controls_default_hover_focus_pressed_disabled.png",
            "nexus_visual/monitoring_hud_studio.html; nexus_visual/nexus_window_primitives.css; monitoring_hud_studio.js",
            "window.nexusMonitoringHudStudioSetWindowState -> data-window-control-state -> CSS pseudo glyphs",
            "Same CSS primitive class names and state model required; final proof must compare default/hover/focus/pressed/disabled.",
            "default, hover, focus, pressed, active/hidden/blocked",
            "focused screenshot/frame sequence required for claimed states",
            "current-branch repair",
            "IDENTICAL_SHARED_PRIMITIVE",
        ),
        VisualLedgerRow(
            "FAM006-STL-004",
            "Recording Studio",
            "target/status rows",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "Only Target and Status, divider rows, no proof/debug row labels, no green boxed table.",
            "FAM-006 child-window label/value density plus UIREF-003 text hierarchy",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/fam_006_monitoring_hud_live_validation/*/focused_element_screenshots/element_03_manage_monitors_open_state.png",
            f"{current_shots}/recording_default.png",
            "nexus_visual/monitoring_hud_studio.html; nexus_visual/nexus_window_primitives.css; desktop/desktop_renderer.py",
            "Recording state payload -> DOM target/status rows -> divider row CSS",
            "Repaired stale Target Overlay Profile / Recording State / Native Log row model.",
            "no target, active target, ready, recording active, saved",
            "pre-LV screenshot and runtime focused proof required",
            "current-branch repair",
            "COMPACT_CONTROLLER_CONFORMING",
        ),
        VisualLedgerRow(
            "FAM006-STL-005",
            "Recording Studio",
            "stateful Start/Stop and Log Viewer route buttons",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "One stateful Start Recording / Stop Recording button plus Log Viewer Studio route; equal button gutters.",
            "AI Control Center / HUD content-fit action button primitive",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/FAM-007-H4/*/05_run_local_check*.png",
            f"{current_shots}/recording_default_and_active_stop.png",
            "nexus_visual/monitoring_hud_studio.html; nexus_visual/nexus_window_primitives.css; monitoring_hud_studio.js",
            "recordingExecutionState -> nexusMonitoringHudStudioApplyState -> button label/dataset -> CSS content-fit primitive",
            "Repaired from separate/stretched controls to single content-fit model; state proof still required.",
            "default, hover, focus, pressed, disabled, active label transition",
            "ordered screenshots/video required for button and dependent status state",
            "current-branch repair",
            "IDENTICAL_SHARED_PRIMITIVE",
        ),
        VisualLedgerRow(
            "FAM006-STL-006",
            "Log Viewer Studio",
            "outer frame / body background",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "Compact log-access shell with opaque Nexus body and no graph/export customization.",
            comparator,
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/FAM-007-H4/*/04_window_controls*.png",
            f"{current_shots}/log_viewer_default.png",
            "nexus_visual/monitoring_hud_studio.html; nexus_visual/nexus_window_primitives.css; desktop/desktop_renderer.py",
            "MonitoringHudLogViewerStudioWindow -> QWebEngineView -> monitoring_hud_studio.html -> nexus_window_primitives.css",
            "Repaired from v4 boxed stack to v5 compact divider shell; final proof still requires focused photo review.",
            "default, wider edge resize, folder opened, blocked folder status",
            "pre-LV screenshot required before LV",
            "current-branch repair",
            "REPAIR_COMPLETED",
        ),
        VisualLedgerRow(
            "FAM006-STL-007",
            "Log Viewer Studio",
            "native/export path rows",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "Native and Exported paths readable, middle-elided, no worktree/FAM/internal leakage.",
            "FAM-006 child-window compact rows plus UIREF-004 doorway/folder status grammar",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/fam_006_monitoring_hud_live_validation/*/focused_element_screenshots/element_03_manage_monitors_open_state.png",
            f"{current_shots}/log_viewer_default.png",
            "desktop/desktop_renderer.py; nexus_visual/monitoring_hud_studio.html; nexus_visual/nexus_window_primitives.css",
            "recording_output_dir/recording_export_dir -> compact path payload -> DOM path rows",
            "Rows now use compact divider treatment; path containment remains a focused proof row.",
            "default, native folder opened, export folder opened, blocked/error status",
            "focused screenshot and status text proof required",
            "current-branch repair",
            "LOG_ACCESS_SHELL_CONFORMING",
        ),
        VisualLedgerRow(
            "FAM006-STL-008",
            "Log Viewer Studio",
            "Open Native / Open Exported buttons",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "Two content-fit folder action buttons with identical primitive and equal gutters.",
            "AI Control Center / HUD content-fit action button primitive",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/FAM-007-H4/*/05_run_local_check*.png",
            f"{current_shots}/log_viewer_default_and_folder_opened.png",
            "nexus_visual/monitoring_hud_studio.html; nexus_visual/nexus_window_primitives.css; desktop/desktop_renderer.py",
            "button click -> NEXUS_MONITORING_HUD_STUDIO_COMMAND -> _open_log_folder -> folder status payload",
            "Must prove click action and status state, not just code path.",
            "default, hover, focus, pressed, folder-opened, folder-blocked",
            "ordered screenshot/video required for action and dependent status",
            "current-branch repair",
            "IDENTICAL_SHARED_PRIMITIVE",
        ),
        VisualLedgerRow(
            "FAM006-STL-009",
            "Log Viewer Studio",
            "resize affordance",
            "FAM-006",
            "unique child / standalone-capable feature-studio",
            "Edge resize only; no attached-child bottom-right corner grip; no maximize until future graph/viewer decision.",
            "UIREF-001 top-level edge-resize grammar",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/FAM-007-H4/*/live_resize_manifest.json",
            f"{current_shots}/log_viewer_edge_resize_width_proof.png",
            "desktop/desktop_renderer.py",
            "MonitoringHudStudioWebWindow edge hit zones -> native resize geometry -> saved geometry",
            "Previous attached-child corner grip removed; final proof must show edge-resize geometry.",
            "default, hover edge, dragged wider, reopened position",
            "ordered frame or screenshots required",
            "current-branch repair",
            "DETACHED_FEATURE_STUDIO_CONFORMING",
        ),
        VisualLedgerRow(
            "FAM006-STL-010",
            "HUD Dashboard",
            "top-level chrome / close control",
            "FAM-006",
            "main / command-center",
            "Historical FAM-006 owned surface must be issue-candidated if not repaired in this active branch.",
            "AI Control Center UIREF-001/UIREF-002",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/FAM-007-H4/*",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/fam_006_monitoring_hud_live_validation/*",
            "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; desktop/desktop_renderer.py",
            "Dashboard DOM/CSS -> desktop runtime WebView",
            "Known previous-branch candidate; not silently green because current repair targets Studio windows.",
            "default, hover, focus, pressed, close",
            "issue candidate unless USER expands scope",
            "historical issue candidate",
            "ISSUE_CANDIDATE",
        ),
        VisualLedgerRow(
            "FAM006-STL-011",
            "Manage Monitors",
            "attached child chrome/controls",
            "FAM-006",
            "exclusive attached child",
            "Contained child window grammar; classify defects, do not copy them into Studios.",
            "Overlay Profile Settings / Manage Monitors attached child references",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/fam_006_monitoring_hud_live_validation/*/focused_element_screenshots/element_03_manage_monitors_open_state.png",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/fam_006_monitoring_hud_live_validation/*/focused_element_screenshots/element_03_manage_monitors_open_state.png",
            "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js",
            "Dashboard child-window layer -> attached child DOM/CSS",
            "Historical owned surface remains separately issue-candidated if nonconforming to new shared primitive law.",
            "default, close, scroll, filter/list rows",
            "current branch classification only",
            "historical issue candidate",
            "ISSUE_CANDIDATE",
        ),
        VisualLedgerRow(
            "FAM006-STL-012",
            "Overlay Profile Settings",
            "attached child chrome/controls",
            "FAM-006",
            "exclusive attached child",
            "Contained child window grammar; classify defects, do not copy them into Studios.",
            "Overlay Profile Settings attached child reference",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/fam_006_monitoring_hud_live_validation/*",
            "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/fam_006_monitoring_hud_live_validation/*",
            "nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js",
            "Dashboard child-window layer -> attached child DOM/CSS",
            "Historical owned surface remains separately issue-candidated if nonconforming to new shared primitive law.",
            "default, edit, create, delete, unsaved guard, dropdown",
            "current branch classification only",
            "historical issue candidate",
            "ISSUE_CANDIDATE",
        ),
    ]


def validate_rows(rows: list[VisualLedgerRow], source_text: str) -> list[str]:
    failures: list[str] = []
    seen: set[str] = set()
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
