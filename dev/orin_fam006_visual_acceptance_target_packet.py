"""Generate and validate FAM-006 branch-local Visual Acceptance Target packets.

This helper is intentionally branch-local. It creates deterministic rendered
visual options for USER review before any further Recording Studio / Log Viewer
Studio product UI repair. It does not implement runtime UI and does not claim
Live Validation or UTS acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
USER_ROOT = Path("C:/Nexus USER")
PACKET_ROOT = USER_ROOT / "FAM-006"
EXTERNAL_ROOT = Path(
    "C:/Nexus Governance State/branches/feature_fam_006_dashboard_recording_start_stop_local_file"
)
EXTERNAL_PROCESS_MD = EXTERNAL_ROOT / "visual_acceptance_target_process.md"
EXTERNAL_PROCESS_JSON = EXTERNAL_ROOT / "visual_acceptance_target_process.json"
BRANCH_PLAN = EXTERNAL_ROOT / "branch_plan.md"
BRANCH_STATE = EXTERNAL_ROOT / "branch_state.md"
UDL_JSON = EXTERNAL_ROOT / "unified_defect_ledger.json"
UDL_MD = EXTERNAL_ROOT / "UNIFIED_DEFECT_LEDGER.md"
INCIDENT_JSON = EXTERNAL_ROOT / "false_green_incident_ledger.json"
INCIDENT_MD = EXTERNAL_ROOT / "FALSE_GREEN_INCIDENT_LEDGER.md"
UDL_GATE_JSON = EXTERNAL_ROOT / "unified_defect_ledger_gate.json"

PRIMARY_FILE = "CURRENT_BRANCH_VISUAL_ACCEPTANCE_TARGET_REVIEW.md"
EXPECTED_DIRS = ("USER Review", "Review Aids", "Source Truth Context")
TIMESTAMP_FORMAT = "%Y%m%d-%H%M%S"

SOURCE_TRUTH_FILES = [
    "Docs/Main.md",
    "Docs/nexus_startup_contract.md",
    "Docs/phase_governance.md",
    "Docs/branch_plans/README.md",
    "Docs/nexus_vision.md",
    "Docs/family_visions/FAM-002_desktop_interface.md",
    "Docs/family_visions/FAM-006_monitoring_and_hud.md",
    "Docs/family_feature_visions/FAM-006_recording.md",
    "Docs/ui_reference_catalog/index.md",
    "Docs/ui_reference_catalog/UIREF-001_top_level_window_frame.md",
    "Docs/ui_reference_catalog/UIREF-002_window_control_cluster.md",
    "Docs/ui_reference_catalog/UIREF-003_control_state_and_selector_grammar.md",
    "Docs/ui_reference_catalog/UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
    "Docs/ui_reference_catalog/UIREF-005_design_token_and_shared_rule_baseline.md",
    "Docs/ui_reference_catalog/UIREF-006_negative_example_and_enforcement_contract.md",
    "Docs/user_test_summary_guidance.md",
    "Docs/validation_helper_registry.md",
    "Docs/incident_patterns.md",
    "Docs/external_operational_state_store_reform_plan.md",
    "Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md",
]

VISUAL_CLASSIFICATIONS = [
    "MATERIAL_UI_UX_CHANGE",
    "EXISTING_SURFACE_LAYOUT_CHANGE",
    "NEW_SURFACE_OR_WINDOW",
    "NEW_CONTROL_CLUSTER",
    "STATUS_ERROR_OR_EMPTY_STATE_CHANGE",
    "VISUAL_SYSTEM_ADOPTION",
    "AMBIGUOUS_VISUAL_CONTRACT",
    "USER_REPORTED_VISUAL_FAILURE",
    "FALSE_GREEN_VISUAL_PROOF_FAILURE",
]

AUTHORITY_LEVELS = {
    "Concept Render": "Brainstorming only; not source truth and not an implementation target.",
    "Design Candidate Render": "USER selection artifact; substantial enough to critique final direction.",
    "Visual Acceptance Target": "USER-accepted final branch visual contract; not accepted by this packet.",
    "Implementation Match Proof": "Actual implementation screenshot/video proving match to an accepted target.",
}

STATE_RENDER_SEQUENCE = (
    "ready",
    "hover",
    "focus",
    "pressed",
    "disabled",
    "recording",
    "saved_complete",
    "blocked_error",
    "footprint_proof",
)

RECORDING_REQUIRED_STATES = {
    "ready",
    "recording",
    "saved_complete",
    "blocked_error",
    "hover",
    "focus",
    "pressed",
    "disabled",
    "fixed_size_footprint",
}

LOG_REQUIRED_STATES = {
    "native_logs_ready",
    "exported_logs_empty",
    "exported_logs_available",
    "open_failed_blocked",
    "hover",
    "focus",
    "pressed",
    "disabled",
    "fixed_or_resize_behavior",
}

RECORDING_ACCEPTED_REQUIRED_STATES = {
    "ACTION-001-hover",
    "ACTION-001-focus",
    "ACTION-001-pressed",
    "ACTION-001-disabled",
    "ACTION-001-ready",
    "ACTION-001-recording",
    "ACTION-001-saved-complete",
    "ACTION-001-blocked-error",
    "ACTION-002-hover",
    "ACTION-002-focus",
    "ACTION-002-pressed",
    "ACTION-002-disabled",
    "FOOTPRINT-001-fixed-size",
}

LOG_ACCEPTED_REQUIRED_STATES = {
    "ROW-001-native-ready",
    "ACTION-001-hover",
    "ACTION-001-focus",
    "ACTION-001-pressed",
    "ACTION-001-disabled",
    "ACTION-001-blocked",
    "ROW-002-export-empty",
    "ROW-002-export-available",
    "ACTION-002-hover",
    "ACTION-002-focus",
    "ACTION-002-pressed",
    "ACTION-002-disabled",
    "ACTION-002-blocked",
    "FOOTPRINT-001-doorway",
}

REJECTED_PATTERNS = [
    (
        "RPL-001",
        "oversized inner cards",
        "Prior Recording/Log Viewer repair screenshots",
        "Made compact studio windows feel huge, detached from purpose, and non-intuitive.",
        "Unique child feature-studio",
        "Start with footprint and purpose before body panels; reject large internal card wells unless USER selects them.",
        "Branch-local; Governance candidate for future branches",
        "USER said the windows felt big and huge.",
    ),
    (
        "RPL-002",
        "path-dominant layout",
        "Prior Log Viewer shells and LOG-B risk area",
        "Paths overpowered the current-branch doorway purpose and looked like local-path proof instead of product UI.",
        "Log Viewer Studio",
        "Prefer direct action labels and concise path truth unless USER selects a path-aware option.",
        "Branch-local",
        "USER suggested two side-by-side actions may be enough.",
    ),
    (
        "RPL-003",
        "debug/status-table feel",
        "Prior Recording Studio row stacks",
        "Read like proof tooling rather than a small product controller.",
        "Recording Studio",
        "Keep status truth compact, product-worded, and action-led.",
        "Branch-local",
        "USER rejected table-like/cramped shells.",
    ),
    (
        "RPL-004",
        "verbose inline helper copy",
        "Prior Studio body copy and REC-B risk area",
        "Made the product surface explain governance/proof concepts instead of user intent.",
        "Recording Studio / Log Viewer Studio",
        "Use short product copy and move proof detail to review aids.",
        "Branch-local",
        "USER rejected proof/debug text inside product surfaces.",
    ),
    (
        "RPL-005",
        "action buried under status",
        "Prior status-first controller attempts",
        "Recording controller purpose became secondary to explanatory rows.",
        "Recording Studio",
        "Primary Start/Stop must be visually discoverable before secondary detail.",
        "Branch-local",
        "USER asked for an intuitive ultra-light controller.",
    ),
    (
        "RPL-006",
        "giant button well",
        "Prior button-heavy visual repairs",
        "Action area became bulky and dominated the window footprint.",
        "Recording Studio / Log Viewer Studio",
        "Use shared content-fit control primitives with equal gutters and bounded height.",
        "Branch-local",
        "USER rejected huge button/button-area feel.",
    ),
    (
        "RPL-007",
        "fake workspace for deferred feature",
        "LOG-C risk area",
        "A large viewer-like shell can imply graph/log viewer/export work that is not current-branch scope.",
        "Log Viewer Studio",
        "Keep current shell as folder access only unless USER selects future-leaning target with explicit risk.",
        "USER_DECISION_REQUIRED if selected",
        "Prompt requires LOG-C risk classification.",
    ),
    (
        "RPL-008",
        "generic form shell",
        "Rejected utility-window patterns",
        "Breaks Project Vision immersion and FAM-006 visual inheritance.",
        "All Nexus-owned product windows",
        "Use Nexus/FAM-006 chrome, typography, button, row, glow, and density grammar.",
        "Project/FAM-002/FAM-006 carrydown",
        "Repeated USER feedback that generic windows are unacceptable.",
    ),
    (
        "RPL-009",
        "broad comparator proof",
        "Prior RAR/LV proof loops",
        "Window-level screenshots did not prove element-group parity or state behavior.",
        "Visual proof",
        "Use element IDs, state renders, and side-by-side target proof.",
        "Governance Candidate Only",
        "USER required row/element-level visual adjudication.",
    ),
    (
        "RPL-010",
        "local-path proof",
        "Prior packet evidence defects",
        "Local paths alone cannot prove media is inside the uploaded packet.",
        "USER packets",
        "Include actual media files in the packet ZIP and validate ZIP membership.",
        "Branch-local packet gate",
        "Repair prompt requires actual media in ZIP.",
    ),
    (
        "RPL-011",
        "marker-only proof",
        "Prior helper/validator green loops",
        "Markers and manifests did not prove visual quality or USER-facing behavior.",
        "Validation/proof",
        "Treat helper output as evidence and require rendered state media plus USER review.",
        "UDL / false-green integration",
        "USER repeatedly rejected false-green claims.",
    ),
    (
        "RPL-012",
        "better/closer/improved acceptance language",
        "Prior Codex summaries",
        "Progress wording allowed REPAIR to be misreported as ACCEPT.",
        "All visual review packets",
        "Use PASS/REPAIR/BLOCKED/USER_DECISION_REQUIRED only; never accept because a result is better.",
        "FAM-002 and false-green gate",
        "Prompt explicitly names this false-acceptance class.",
    ),
]

CONFLICT_CLASSIFICATION_ROWS = [
    {
        "decision": "Visual target packet before product UI repair",
        "classification": "BRANCH_LOCAL_VISUAL_DECISION",
        "riskArea": "process sequencing",
        "basis": "FAM-006 returned-UTS false-green loop; branch-local repair approved.",
        "userDecisionNeeded": "USER must select/revise target before implementation-match repair.",
    },
    {
        "decision": "Recording Studio compact controller footprint",
        "classification": "USER_DECISION_REQUIRED",
        "riskArea": "surface footprint and density",
        "basis": "Recording FFV requires ultra-light detached controller; final dimensions are USER visual target choice.",
        "userDecisionNeeded": "Choose, combine, or revise REC-A/REC-B/REC-C.",
    },
    {
        "decision": "REC-B proof-like copy: Dashboard and Studio share target truth",
        "classification": "BRANCH_LOCAL_VISUAL_DECISION",
        "riskArea": "internal/proof-like copy",
        "basis": "Valid concept but potentially too proof-like for product UI; packet must expose it for critique.",
        "userDecisionNeeded": "Accept shorter product copy or revise wording.",
    },
    {
        "decision": "Log Viewer fixed-size versus edge-resizable doorway shell",
        "classification": "USER_DECISION_REQUIRED",
        "riskArea": "resize behavior",
        "basis": "Current branch is folder access only; future graph/viewer placement remains deferred.",
        "userDecisionNeeded": "Choose fixed-size LOG-A or path/future-leaning LOG-B/LOG-C with explicit risk.",
    },
    {
        "decision": "LOG-B path-forward / local-path-looking text",
        "classification": "BRANCH_LOCAL_VISUAL_DECISION",
        "riskArea": "local-path proof smell",
        "basis": "Path truth may help, but product UI must not look like validation proof.",
        "userDecisionNeeded": "Accept path-aware shell or prefer direct action-only shell.",
    },
    {
        "decision": "LOG-C FEATURE_STUDIO-like shape while scope is doorway/shell only",
        "classification": "USER_DECISION_REQUIRED",
        "riskArea": "deferred full viewer/export/graph scope",
        "basis": "LOG-C may imply future workspace not admitted by current branch.",
        "userDecisionNeeded": "Accept as future-leaning target or reject/defer it.",
    },
    {
        "decision": "Any dashboard, report-table, debug-panel, or workspace drift",
        "classification": "NO_CONFLICT",
        "riskArea": "rejected pattern",
        "basis": "Rejected Patterns Ledger blocks those patterns unless USER explicitly selects an exception.",
        "userDecisionNeeded": "Only needed if USER wants to revive one of those patterns.",
    },
    {
        "decision": "Global Visual Acceptance Target governance promotion",
        "classification": "GOVERNANCE_CANDIDATE_ONLY",
        "riskArea": "global policy",
        "basis": "Current approval excludes Governance worktree mutation.",
        "userDecisionNeeded": "Separate Governance approval if USER wants global promotion.",
    },
]


@dataclass(frozen=True)
class Option:
    option_id: str
    surface: str
    footprint_class: str
    window_class: str
    title: str
    purpose: str
    default_size: tuple[int, int]
    min_size: tuple[int, int]
    resize_behavior: str
    tradeoffs: str
    risks: str
    primary_action: str
    secondary_action: str
    rows: tuple[tuple[str, str], ...]
    footer: str


@dataclass(frozen=True)
class CalloutSpec:
    marker: str
    element_id: str
    element_name: str
    status: str
    purpose_note: str
    rect: tuple[int, int, int, int]


OPTIONS = [
    Option(
        option_id="REC-A",
        surface="Recording Studio",
        footprint_class="COMPACT_CONTROLLER",
        window_class="Unique child / standalone-capable feature-studio window",
        title="Recording Studio",
        purpose="Smallest viable floating controller: one stateful Start/Stop action plus target truth.",
        default_size=(360, 184),
        min_size=(340, 176),
        resize_behavior="Fixed-size; movable with remembered position; no resize affordance.",
        tradeoffs="Lowest screen footprint, fastest to read; less room for secondary explanation.",
        risks="May feel too compressed if future warning or error copy grows.",
        primary_action="Start Recording",
        secondary_action="Logs",
        rows=(("TARGET", "Default Overlay Profile"), ("STATE", "Ready - 2 active monitors")),
        footer="Uses active Overlay Profile. No automatic export.",
    ),
    Option(
        option_id="REC-B",
        surface="Recording Studio",
        footprint_class="COMPACT_CONTROLLER",
        window_class="Unique child / standalone-capable feature-studio window",
        title="Recording Studio",
        purpose="Balanced compact controller with explicit native-log state and clear action rail.",
        default_size=(420, 198),
        min_size=(392, 184),
        resize_behavior="Fixed-size; movable with remembered position; no resize affordance.",
        tradeoffs="More explicit state than REC-A while still smaller than current repair attempts.",
        risks="Could still read too information-heavy if native-log row is not useful enough.",
        primary_action="Start Recording",
        secondary_action="Log Viewer",
        rows=(
            ("TARGET", "Default Overlay Profile"),
            ("RECORDING", "Ready"),
            ("NATIVE LOG", "None yet"),
        ),
        footer="Dashboard and Studio share the same target truth.",
    ),
    Option(
        option_id="REC-C",
        surface="Recording Studio",
        footprint_class="COMPACT_CONTROLLER",
        window_class="Unique child / standalone-capable feature-studio window",
        title="Recording Studio",
        purpose="Action-first controller: large enough primary action without a giant button well.",
        default_size=(392, 184),
        min_size=(368, 170),
        resize_behavior="Fixed-size; movable with remembered position; no resize affordance.",
        tradeoffs="Strongest Start/Stop prominence; less table-like than status-first layouts.",
        risks="Requires precise button sizing so it does not become bulky again.",
        primary_action="Start Recording",
        secondary_action="Open Logs",
        rows=(("TARGET", "Default Overlay Profile / 2 active monitors"), ("STATE", "Ready")),
        footer="Compact controller, not a dashboard card.",
    ),
    Option(
        option_id="LOG-A",
        surface="Log Viewer Studio",
        footprint_class="DOORWAY_SHELL",
        window_class="Unique child / standalone-capable feature-studio window",
        title="Log Viewer Studio",
        purpose="Minimal two-action doorway shell: native logs and exported logs only.",
        default_size=(430, 184),
        min_size=(392, 176),
        resize_behavior="Movable; fixed-size for current branch; no corner grip.",
        tradeoffs="Very slim and non-obtrusive; matches current branch's limited folder-access scope.",
        risks="May need redesign later if full graph/log viewing lands inside this same window.",
        primary_action="Open Native Logs",
        secondary_action="Open Exported Logs",
        rows=(("NATIVE", "Recordings folder"), ("EXPORT", "Exported Logs folder")),
        footer="Full previous-log viewing and export customization remain future-gated.",
    ),
    Option(
        option_id="LOG-B",
        surface="Log Viewer Studio",
        footprint_class="DOORWAY_SHELL",
        window_class="Unique child / standalone-capable feature-studio window",
        title="Log Viewer Studio",
        purpose="Compact path-aware shell with truncated path truth and folder actions.",
        default_size=(500, 190),
        min_size=(440, 170),
        resize_behavior="Movable and edge-resizable; no attached-child corner grip.",
        tradeoffs="Clearer native/export distinction and future-safe path readability.",
        risks="Bigger footprint may be rejected if USER wants only two buttons.",
        primary_action="Open Native Logs",
        secondary_action="Open Exported Logs",
        rows=(
            ("NATIVE", "C:/.../Nexus Desktop AI/Recordings"),
            ("EXPORT", "C:/.../Nexus Desktop AI/Exported Logs"),
        ),
        footer="Folder access shell only; no fake graph workspace.",
    ),
    Option(
        option_id="LOG-C",
        surface="Log Viewer Studio",
        footprint_class="FEATURE_STUDIO",
        window_class="Unique child / standalone-capable feature-studio window",
        title="Log Viewer Studio",
        purpose="Future-leaning shell that leaves a narrow preview/status lane without implementing the viewer.",
        default_size=(540, 220),
        min_size=(460, 190),
        resize_behavior="Movable and edge-resizable; no maximize until graph/viewer placement is decided.",
        tradeoffs="Most future-expandable; still avoids fake graph/viewer controls.",
        risks="May be too large and too suggestive of deferred full Log Viewer implementation.",
        primary_action="Open Native Logs",
        secondary_action="Open Exported Logs",
        rows=(
            ("NATIVE", "Recordings folder"),
            ("EXPORT", "Exported Logs folder"),
            ("STATUS", "No log selected in this branch"),
        ),
        footer="Graph, previous-log selection, and export customization are future-gated.",
    ),
]

ACCEPTED_TARGETS = [
    Option(
        option_id="REC-C-ACCEPTED",
        surface="Recording Studio",
        footprint_class="COMPACT_CONTROLLER",
        window_class="Unique child / standalone-capable feature-studio window",
        title="Recording Studio",
        purpose="Accepted compact detached controller: REC-C action-first base with REC-A target/state separation.",
        default_size=(392, 184),
        min_size=(368, 170),
        resize_behavior="Fixed-size; movable with remembered position; no resize affordance.",
        tradeoffs="USER accepted REC-C as the base while requiring REC-A clearer target/state separation.",
        risks="Implementation repair must not reintroduce REC-B proof copy, native-log status rows, mini-dashboard report tables, or giant button wells.",
        primary_action="Start Recording",
        secondary_action="Open Logs",
        rows=(("TARGET", "Default Overlay Profile"), ("STATE", "Ready - 2 active monitors")),
        footer="Compact controller; native logs remain product artifacts, export is user-requested.",
    ),
    Option(
        option_id="LOG-A-ACCEPTED",
        surface="Log Viewer Studio",
        footprint_class="DOORWAY_SHELL",
        window_class="Unique child / standalone-capable feature-studio window",
        title="Log Viewer Studio",
        purpose="Accepted compact doorway shell: LOG-A base for native/export folder access only.",
        default_size=(430, 184),
        min_size=(392, 176),
        resize_behavior="Movable; fixed-size for current accepted doorway shell unless later source truth admits viewer workspace resizing.",
        tradeoffs="USER accepted LOG-A as the current branch doorway target and rejected path/debug and full-workspace drift.",
        risks="Implementation repair must not display local paths by default, fake graph/viewer/export customization, previous-log selection, or Recording Studio state labels.",
        primary_action="Open Native Logs",
        secondary_action="Open Exported Logs",
        rows=(("NATIVE", "Recordings folder"), ("EXPORT", "Exported Logs folder")),
        footer="Full Log Viewer, previous-log selection, graph viewing, and export customization remain future-gated.",
    ),
]

ACCEPTED_SELECTION_ROWS = [
    (
        "VSL-001",
        "Recording Studio",
        "REC-C",
        "WINDOW/ACTION/ROW",
        "ACCEPTED_WITH_REVISIONS",
        "Accept REC-C as base; borrow REC-A clearer target/state separation.",
        "Branch-local accepted visual target; not runtime proof.",
        "Use compact detached-controller class.",
        "One stateful Start Recording / Stop Recording button; one Open Logs route; Target row; State row.",
        "Later actual implementation screenshots/video must match this target.",
        "Reusable candidate after implementation-match proof passes.",
    ),
    (
        "VSL-002",
        "Recording Studio",
        "REC-B",
        "COPY/ROWS",
        "REJECTED",
        "Reject helper/proof copy, native-log status row, mini-dashboard/report-table feel, internal proof wording.",
        "Rejected pattern carried into implementation-match checklist.",
        "Do not use REC-B body or proof language.",
        "No native-log status row in Recording Studio accepted target.",
        "Visual target packet and later implementation-match evidence must show absence.",
        "False-green prevention row.",
    ),
    (
        "VSL-003",
        "Log Viewer Studio",
        "LOG-A",
        "WINDOW/ACTION/ROW",
        "ACCEPTED",
        "Accept LOG-A as base.",
        "Branch-local accepted visual target; not runtime proof.",
        "Use compact doorway-shell class.",
        "Native and Export rows with folder labels and corresponding actions.",
        "Later actual implementation screenshots/video must match this target.",
        "Reusable doorway-shell candidate after proof.",
    ),
    (
        "VSL-004",
        "Log Viewer Studio",
        "LOG-B/LOG-C",
        "COPY/SCOPE",
        "REJECTED_DEFERRED",
        "Reject LOG-B local-path/debug display; defer LOG-C full feature-studio workspace.",
        "Future-gated feature scope remains deferred.",
        "No local paths by default; no fake full-viewer workspace.",
        "Doorway shell only: native/export folder access.",
        "Visual target packet and later implementation-match evidence must show absence.",
        "False-green prevention row.",
    ),
]


def _run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def _rounded(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], radius: int, fill: str, outline: str, width: int = 1) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def _draw_button(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], label: str, *, primary: bool = False) -> None:
    fill = "#092C3E" if primary else "#061F2F"
    outline = "#39B7D1" if primary else "#255E72"
    _rounded(draw, xy, 12, fill, outline, 1)
    font = _font(11, bold=True)
    w, h = _text_size(draw, label.upper(), font)
    draw.text(
        (xy[0] + ((xy[2] - xy[0]) - w) // 2, xy[1] + ((xy[3] - xy[1]) - h) // 2 - 1),
        label.upper(),
        font=font,
        fill="#EAF8FF",
    )


def _callout_specs(option: Option) -> list[CalloutSpec]:
    width, height = option.default_size
    body_top = 66
    body_bottom = height - 58
    row_h = max(26, (body_bottom - body_top - 12) // max(1, len(option.rows)))
    action_y = height - 42
    ctrl_w = 66 if option.resize_behavior.startswith("Fixed") else 96
    common = [
        CalloutSpec("01", "CHROME-001", "window shell and edge", "accepted", "Unique child/feature-studio shell, not product overlay art.", (0, 0, width - 1, height - 1)),
        CalloutSpec("02", "TITLE-001", "category and title text", "accepted", "Child-window title grammar: category line plus strong title, no title card.", (18, 14, width - 94, 58)),
        CalloutSpec("03", "CTRL-001", "window control cluster", "accepted", "Compact minimize/close controls for the accepted window class.", (width - ctrl_w - 18, 18, width - 18, 48)),
    ]
    if option.surface.startswith("Recording"):
        common.extend(
            [
                CalloutSpec("04", "TARGET-001", "target truth row", "accepted", "Target row only; shows the active Overlay Profile target truth.", (18, body_top + 8, width - 18, body_top + row_h + 4)),
                CalloutSpec("05", "STATUS-001", "state truth row", "accepted", "State row only; separate from target truth.", (18, body_top + row_h + 8, width - 18, body_top + (row_h * 2) + 4)),
                CalloutSpec("06", "ACTION-001", "primary Start/Stop action", "accepted", "Primary stateful control only; does not include Open Logs.", (18, action_y, 178, action_y + 32)),
                CalloutSpec("07", "ACTION-002", "Open Logs secondary action", "accepted", "Secondary route action only; does not share ACTION-001 proof.", (190, action_y, width - 18, action_y + 32)),
            ]
        )
    else:
        mid = width // 2
        common.extend(
            [
                CalloutSpec("04", "ROW-001", "native logs row", "accepted", "Native row only; not grouped with export row.", (18, body_top + 8, width - 18, body_top + row_h + 4)),
                CalloutSpec("05", "ROW-002", "exported logs row", "accepted", "Export row only; not grouped with native row.", (18, body_top + row_h + 8, width - 18, body_top + (row_h * 2) + 4)),
                CalloutSpec("06", "ACTION-001", "Open Native Logs action", "accepted", "Native folder action only.", (18, action_y, mid - 7, action_y + 32)),
                CalloutSpec("07", "ACTION-002", "Open Exported Logs action", "accepted", "Export folder action only.", (mid + 7, action_y, width - 18, action_y + 32)),
            ]
        )
    return common


def _draw_window(option: Option, target: Path, *, context: bool = False) -> None:
    width, height = option.default_size
    canvas_w = 900 if context else width
    canvas_h = 520 if context else height
    img = Image.new("RGB", (canvas_w, canvas_h), "#020811")
    draw = ImageDraw.Draw(img)
    if context:
        for x in range(0, canvas_w, 32):
            draw.line((x, 0, x, canvas_h), fill="#061826")
        for y in range(0, canvas_h, 32):
            draw.line((0, y, canvas_w, y), fill="#061826")
        wx, wy = 36, 58
        draw.text((36, 18), f"{option.option_id} context footprint on a 900x520 desktop canvas", font=_font(13, bold=True), fill="#9DC8D8")
    else:
        wx, wy = 0, 0
    shell = (wx, wy, wx + width - 1, wy + height - 1)
    _rounded(draw, shell, 22, "#03111C", "#1E5C70", 1)
    draw.rectangle((wx + 2, wy + 2, wx + width - 3, wy + height - 3), outline="#071A28")
    # Child-window title grammar: text, not a separated title card.
    draw.text((wx + 22, wy + 18), "ACTIVE OVERLAY RECORDING" if option.surface.startswith("Recording") else "RECORDING LOGS", font=_font(9, bold=True), fill="#67C9E2")
    draw.text((wx + 22, wy + 36), option.title.upper(), font=_font(18, bold=True), fill="#F1FAFF")
    # Compact window control pill.
    ctrl_w = 66 if option.resize_behavior.startswith("Fixed") else 96
    ctrl = (wx + width - ctrl_w - 18, wy + 18, wx + width - 18, wy + 48)
    _rounded(draw, ctrl, 15, "#08283A", "#2B7790", 1)
    labels = ["-", "x"] if ctrl_w == 66 else ["-", "[]", "x"]
    step = ctrl_w // len(labels)
    for i, label in enumerate(labels):
        x = ctrl[0] + i * step + step // 2 - 4
        draw.text((x, ctrl[1] + 7), label, font=_font(11, bold=True), fill="#D8F4FF")
    # Body panel.
    body_top = wy + 66
    body_bottom = wy + height - 58
    body = (wx + 18, body_top, wx + width - 18, body_bottom)
    _rounded(draw, body, 14, "#061725", "#173D4E", 1)
    row_h = max(26, (body_bottom - body_top - 12) // max(1, len(option.rows)))
    y = body_top + 8
    label_font = _font(9, bold=True)
    value_font = _font(11, bold=True)
    for label, value in option.rows:
        draw.line((body[0] + 10, y + row_h - 3, body[2] - 10, y + row_h - 3), fill="#174255")
        draw.text((body[0] + 14, y + 7), label.upper(), font=label_font, fill="#72C5DD")
        draw.text((body[0] + 112, y + 7), value, font=value_font, fill="#9FFFE3")
        y += row_h
    # Actions.
    action_y = wy + height - 42
    if option.surface.startswith("Recording"):
        _draw_button(draw, (wx + 18, action_y, wx + 178, action_y + 32), option.primary_action, primary=True)
        _draw_button(draw, (wx + 190, action_y, wx + width - 18, action_y + 32), option.secondary_action)
    else:
        mid = wx + width // 2
        _draw_button(draw, (wx + 18, action_y, mid - 7, action_y + 32), option.primary_action, primary=True)
        _draw_button(draw, (mid + 7, action_y, wx + width - 18, action_y + 32), option.secondary_action)
    if height > 194:
        draw.text((wx + 22, wy + height - 74), option.footer, font=_font(9), fill="#A9C9D7")
    # Legend.
    legend_x = wx + width + 28 if context else 0
    if context:
        legend = [f"{option.option_id} - {option.surface}"]
        legend.extend(f"{spec.element_id}: {spec.element_name}" for spec in _callout_specs(option))
        legend.extend([f"FOOTPRINT: {option.footprint_class}", f"SIZE: {width}x{height}"])
        draw.text((legend_x, wy + 8), "ELEMENT LEGEND", font=_font(12, bold=True), fill="#EAF8FF")
        ly = wy + 34
        for line in legend:
            draw.text((legend_x, ly), line, font=_font(10), fill="#A9C9D7")
            ly += 18
    target.parent.mkdir(parents=True, exist_ok=True)
    img.save(target)


def _draw_state_contact_sheet(option: Option, target: Path) -> None:
    frames = _accepted_state_frames(option) if option.option_id.endswith("-ACCEPTED") else _legacy_state_frames(option)
    tile_w, tile_h = 300, 132
    cols = 3
    rows = (len(frames) + cols - 1) // cols
    margin = 18
    header_h = 38
    img = Image.new("RGB", (cols * tile_w + margin * 2, rows * tile_h + header_h + margin * 2), "#020811")
    draw = ImageDraw.Draw(img)
    draw.text((margin, 12), f"{option.option_id} required state render contact sheet", font=_font(16, bold=True), fill="#EAF8FF")
    state_font = _font(10, bold=True)
    small = _font(8, bold=True)
    value = _font(9, bold=True)
    for index, frame in enumerate(frames):
        col = index % cols
        row = index // cols
        x = margin + col * tile_w
        y = header_h + margin + row * tile_h
        state_label = frame["label"]
        _rounded(draw, (x, y, x + tile_w - 14, y + tile_h - 12), 17, "#03111C", "#1E5C70", 1)
        draw.text((x + 14, y + 10), state_label, font=state_font, fill="#7BD2E8")
        draw.text((x + 14, y + 26), option.title.upper(), font=_font(13, bold=True), fill="#F1FAFF")

        panel = (x + 14, y + 50, x + tile_w - 28, y + 82)
        fill = "#061725"
        outline = "#173D4E"
        state_style = frame["style"]
        if state_style == "blocked":
            fill, outline = "#211218", "#7C3D45"
        elif state_style in {"active", "pressed"}:
            fill, outline = "#0D1F24", "#34BFA4"
        elif state_style == "disabled":
            fill, outline = "#06111A", "#244052"
        elif state_style == "focus":
            fill, outline = "#071F31", "#8CEBFF"
        elif state_style == "hover":
            fill, outline = "#08283A", "#39B7D1"
        _rounded(draw, panel, 11, fill, outline, 1)

        draw.text((panel[0] + 10, panel[1] + 10), frame["truth"], font=value, fill="#9FFFE3" if state_style != "disabled" else "#647684")

        button = (x + 14, y + 91, x + 145, y + 119)
        button_fill = "#092C3E"
        button_outline = "#39B7D1"
        if state_style == "disabled":
            button_fill, button_outline = "#06111A", "#244052"
        elif state_style == "pressed":
            button_fill, button_outline = "#0D403F", "#7DFFE6"
        elif state_style == "focus":
            button_fill, button_outline = "#092C3E", "#EAF8FF"
        elif state_style == "hover":
            button_fill, button_outline = "#0A354C", "#69E8FF"
        _rounded(draw, button, 10, button_fill, button_outline, 1)
        label = frame["button"].upper()
        tw, th = _text_size(draw, label, small)
        draw.text(
            (button[0] + ((button[2] - button[0]) - tw) // 2, button[1] + ((button[3] - button[1]) - th) // 2 - 1),
            label,
            font=small,
            fill="#EAF8FF" if state_style != "disabled" else "#647684",
        )
        if frame["state_id"].startswith("FOOTPRINT-"):
            draw.line((x + tile_w - 58, y + 22, x + tile_w - 28, y + 22), fill="#8CEBFF")
            draw.line((x + tile_w - 28, y + 22, x + tile_w - 28, y + 52), fill="#8CEBFF")
            grip = "no corner grip" if "Fixed" in option.resize_behavior or "fixed" in option.resize_behavior else "edge resize only"
            draw.text((x + tile_w - 120, y + 84), grip, font=_font(8), fill="#A9C9D7")
    target.parent.mkdir(parents=True, exist_ok=True)
    img.save(target)


def _legacy_state_frames(option: Option) -> list[dict[str, str]]:
    frames: list[dict[str, str]] = []
    for state in STATE_RENDER_SEQUENCE:
        if option.surface.startswith("Recording"):
            label = state.replace("_", " ").upper()
            truth = {
                "ready": "Ready - 2 active monitors",
                "hover": "Hover: Start Recording",
                "focus": "Focus ring visible",
                "pressed": "Pressed: starting...",
                "disabled": "Disabled: target missing",
                "recording": "Recording active",
                "saved_complete": "Saved native log",
                "blocked_error": "Blocked: no active monitor",
                "footprint_proof": f"Fixed {option.default_size[0]}x{option.default_size[1]}",
            }[state]
            button = "Stop Recording" if state == "recording" else option.primary_action
        else:
            label = {
                "ready": "NATIVE READY",
                "hover": "HOVER ACTION",
                "focus": "FOCUS RING",
                "pressed": "OPENING FOLDER",
                "disabled": "DISABLED ACTION",
                "recording": "EXPORT AVAILABLE",
                "saved_complete": "EXPORT READY",
                "blocked_error": "OPEN FAILED",
                "footprint_proof": "DOORWAY FOOTPRINT",
            }[state]
            truth = {
                "ready": "Native logs ready",
                "hover": "Hover: Open Native Logs",
                "focus": "Focus ring visible",
                "pressed": "Pressed: opening folder",
                "disabled": "Disabled: folder unavailable",
                "recording": "Exported logs available",
                "saved_complete": "Export folder ready",
                "blocked_error": "Blocked: open failed",
                "footprint_proof": option.resize_behavior,
            }[state]
            button = option.primary_action
        frames.append(
            {
                "state_id": state,
                "label": label,
                "truth": truth,
                "button": button,
                "style": _style_for_state_id(state),
            }
        )
    return frames


def _accepted_state_frames(option: Option) -> list[dict[str, str]]:
    if option.surface.startswith("Recording"):
        rows = [
            ("ACTION-001-ready", "ACTION-001 READY", "Ready: target and active monitors available", "Start Recording", "ready"),
            ("ACTION-001-hover", "ACTION-001 HOVER", "Hover: primary Start Recording", "Start Recording", "hover"),
            ("ACTION-001-focus", "ACTION-001 FOCUS", "Focus: primary action ring visible", "Start Recording", "focus"),
            ("ACTION-001-pressed", "ACTION-001 PRESSED", "Pressed: starting recording", "Start Recording", "pressed"),
            ("ACTION-001-recording", "ACTION-001 RECORDING", "Stateful variation: Stop Recording", "Stop Recording", "active"),
            ("ACTION-001-saved-complete", "ACTION-001 SAVED", "Saved complete: ready for another recording", "Start Recording", "active"),
            ("ACTION-001-disabled", "ACTION-001 DISABLED", "Disabled: target unavailable", "Start Recording", "disabled"),
            ("ACTION-001-blocked-error", "ACTION-001 BLOCKED", "Blocked: no active monitor", "Start Recording", "blocked"),
            ("ACTION-002-hover", "ACTION-002 HOVER", "Hover: Open Logs secondary action", "Open Logs", "hover"),
            ("ACTION-002-focus", "ACTION-002 FOCUS", "Focus: Open Logs secondary action", "Open Logs", "focus"),
            ("ACTION-002-pressed", "ACTION-002 PRESSED", "Pressed: opening Log Viewer Studio", "Open Logs", "pressed"),
            ("ACTION-002-disabled", "ACTION-002 DISABLED", "Disabled: log route unavailable", "Open Logs", "disabled"),
            ("FOOTPRINT-001-fixed-size", "FOOTPRINT PROOF", option.resize_behavior, "Fixed footprint", "ready"),
        ]
    else:
        rows = [
            ("ROW-001-native-ready", "ROW-001 NATIVE READY", "Native logs row: Recordings folder ready", "Native Row", "ready"),
            ("ACTION-001-hover", "ACTION-001 HOVER", "Hover: Open Native Logs", "Open Native Logs", "hover"),
            ("ACTION-001-focus", "ACTION-001 FOCUS", "Focus: Open Native Logs", "Open Native Logs", "focus"),
            ("ACTION-001-pressed", "ACTION-001 PRESSED", "Pressed: opening native folder", "Open Native Logs", "pressed"),
            ("ACTION-001-disabled", "ACTION-001 DISABLED", "Disabled: native folder unavailable", "Open Native Logs", "disabled"),
            ("ACTION-001-blocked", "ACTION-001 BLOCKED", "Blocked: native folder open failed", "Open Native Logs", "blocked"),
            ("ROW-002-export-empty", "ROW-002 EXPORT EMPTY", "Export row: no user export yet", "Export Row", "ready"),
            ("ROW-002-export-available", "ROW-002 EXPORT READY", "Export row: exported logs available", "Export Row", "active"),
            ("ACTION-002-hover", "ACTION-002 HOVER", "Hover: Open Exported Logs", "Open Exported Logs", "hover"),
            ("ACTION-002-focus", "ACTION-002 FOCUS", "Focus: Open Exported Logs", "Open Exported Logs", "focus"),
            ("ACTION-002-pressed", "ACTION-002 PRESSED", "Pressed: opening exported folder", "Open Exported Logs", "pressed"),
            ("ACTION-002-disabled", "ACTION-002 DISABLED", "Disabled: exported folder unavailable", "Open Exported Logs", "disabled"),
            ("ACTION-002-blocked", "ACTION-002 BLOCKED", "Blocked: exported folder open failed", "Open Exported Logs", "blocked"),
            ("FOOTPRINT-001-doorway", "DOORWAY FOOTPRINT", option.resize_behavior, "Doorway shell", "ready"),
        ]
    return [
        {"state_id": state_id, "label": label, "truth": truth, "button": button, "style": style}
        for state_id, label, truth, button, style in rows
    ]


def _style_for_state_id(state_id: str) -> str:
    if "blocked" in state_id or "error" in state_id:
        return "blocked"
    if "disabled" in state_id:
        return "disabled"
    if "pressed" in state_id:
        return "pressed"
    if "focus" in state_id:
        return "focus"
    if "hover" in state_id:
        return "hover"
    if "recording" in state_id or "available" in state_id or "saved" in state_id:
        return "active"
    return "ready"


def _draw_annotated_callout(option: Option, target: Path) -> None:
    base = target.with_name(target.stem + "_base.png")
    _draw_window(option, base)
    callouts = _callout_specs(option)
    canvas_h = max(option.default_size[1] + 54, 62 + len(callouts) * 52)
    img = Image.new("RGB", (option.default_size[0] + 430, canvas_h), "#020811")
    img.paste(Image.open(base), (14, 17))
    base.unlink(missing_ok=True)
    draw = ImageDraw.Draw(img)
    offset_x, offset_y = 14, 17
    width, height = option.default_size
    legend_x = offset_x + width + 24
    draw.text((legend_x, 18), "ANNOTATED LEGEND", font=_font(13, bold=True), fill="#EAF8FF")
    y = 44
    colors = ["#7DFFE6", "#8CEBFF", "#F5D06C", "#9FFFE3", "#F1FAFF", "#FFB86C", "#C0FF72", "#B28DFF"]
    for index, spec in enumerate(callouts, start=1):
        outline = colors[(index - 1) % len(colors)]
        rect = (
            offset_x + spec.rect[0],
            offset_y + spec.rect[1],
            offset_x + spec.rect[2],
            offset_y + spec.rect[3],
        )
        draw.rounded_rectangle(rect, radius=8, outline=outline, width=2)
        badge = (rect[0] + 4, rect[1] + 4, rect[0] + 38, rect[1] + 23)
        _rounded(draw, badge, 6, "#061725", outline, 1)
        draw.text((badge[0] + 5, badge[1] + 4), spec.marker, font=_font(8, bold=True), fill="#EAF8FF")
        anchor_x = rect[2] if rect[2] < legend_x else rect[0]
        anchor_y = rect[1] + max(8, (rect[3] - rect[1]) // 2)
        target_y = y + 9
        draw.line((anchor_x, anchor_y, legend_x - 12, target_y), fill=outline, width=2)
        draw.ellipse((legend_x - 18, target_y - 4, legend_x - 10, target_y + 4), fill=outline)
        draw.text((legend_x, y), f"{spec.marker}. {spec.element_id}", font=_font(10, bold=True), fill=outline)
        draw.text((legend_x, y + 14), spec.element_name, font=_font(9), fill="#EAF8FF")
        draw.text((legend_x, y + 28), spec.purpose_note[:58], font=_font(8), fill="#A9C9D7")
        y += 52
    draw.text((legend_x, y + 4), "Callouts are packet proof overlays only.", font=_font(9), fill="#A9C9D7")
    target.parent.mkdir(parents=True, exist_ok=True)
    img.save(target)


def _callout_legend_records(option: Option) -> list[dict[str, object]]:
    return [
        {
            "calloutMarker": spec.marker,
            "elementId": spec.element_id,
            "elementName": spec.element_name,
            "acceptedRejectedReviseStatus": spec.status,
            "purposeNote": spec.purpose_note,
            "rect": list(spec.rect),
            "nonColorMarkerMethod": "outlined box plus printed marker badge plus connector line",
        }
        for spec in _callout_specs(option)
    ]


def _copy_source_context() -> list[str]:
    copied: list[str] = []
    context = PACKET_ROOT / "Source Truth Context"
    for rel in SOURCE_TRUTH_FILES:
        source = ROOT / rel
        if not source.exists():
            continue
        dest = context / _source_context_name(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        copied.append(rel)
    if BRANCH_PLAN.exists():
        shutil.copy2(BRANCH_PLAN, context / "external_branch_plan.md")
        copied.append(str(BRANCH_PLAN))
    return copied


def _source_context_name(rel: str) -> str:
    path = Path(rel)
    parts = path.parts
    if rel == "Docs/ui_reference_catalog/index.md":
        return "ui_reference_catalog_index.md"
    if len(parts) >= 3 and parts[0] == "Docs" and parts[1] in {"family_visions", "family_feature_visions", "ui_reference_catalog", "branch_records"}:
        return path.name
    return rel.replace("/", "_")


def _copy_udl_context() -> list[str]:
    copied: list[str] = []
    target_dir = PACKET_ROOT / "Review Aids" / "Unified Defect Ledger"
    target_dir.mkdir(parents=True, exist_ok=True)
    for source, name in (
        (UDL_JSON, "unified_defect_ledger.json"),
        (UDL_MD, "UNIFIED_DEFECT_LEDGER.md"),
        (INCIDENT_JSON, "false_green_incident_ledger.json"),
        (INCIDENT_MD, "FALSE_GREEN_INCIDENT_LEDGER.md"),
        (UDL_GATE_JSON, "unified_defect_ledger_gate.json"),
    ):
        if source.exists():
            shutil.copy2(source, target_dir / name)
            copied.append(str(source))
    status = {
        "status": "REVIEWABLE_EVIDENCE_INCLUDED" if len(copied) == 5 else "PARTIAL_EVIDENCE_INCLUDED",
        "absenceOfVisualAcceptanceTargetRepresented": "The packet preserves the branch-local false-green / UDL evidence and records the USER-accepted visual target as a pre-implementation contract.",
        "currentOwnedUdlBlocksThisPacket": "Packet generation is allowed as accepted visual-target evidence; product UI repair remains blocked until USER separately approves implementation-match repair.",
        "knownBadFalseGreenDefects": [
            "missing required state renders",
            "stale or inconsistent packet hash proof",
            "incomplete validation output inclusion",
            "under-seeded rejected patterns",
            "thin conflict classification",
            "progress-language false acceptance",
        ],
        "udlRowsClosedWithoutProof": "None by this packet generator.",
        "copiedEvidence": copied,
    }
    _write_json(target_dir / "udl_false_green_status.json", status)
    md = [
        "# UDL / False-Green Status",
        "",
        f"Status: `{status['status']}`",
        "",
        "This packet is allowed to become reviewable only as a Visual Acceptance Target packet. It does not close product defects, UDL rows, H1, Live Validation, UTS, or PR Readiness.",
        "",
        "## Known-Bad Classes Preserved",
        "",
    ]
    md.extend(f"- {item}" for item in status["knownBadFalseGreenDefects"])
    md.extend(
        [
            "",
            "## Process Guard",
            "",
            "The repaired process prevents implementation-first false greens by requiring packet-contained focused renders, desktop/context renders, rendered state contact sheets, legends, decision ledgers, rejected-pattern rows, conflict classifications, and validation-output evidence before USER selects the visual target.",
            "",
            "UDL rows closed without proof: `None by this packet generator`.",
        ]
    )
    (target_dir / "UDL_FALSE_GREEN_STATUS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    copied.extend([str(target_dir / "udl_false_green_status.json"), str(target_dir / "UDL_FALSE_GREEN_STATUS.md")])
    return copied


def _purge_packet() -> None:
    if PACKET_ROOT.exists():
        shutil.rmtree(PACKET_ROOT)
    for zip_path in USER_ROOT.glob("FAM-006-*.zip"):
        zip_path.unlink()
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)
    for name in EXPECTED_DIRS:
        (PACKET_ROOT / name).mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _option_record(option: Option, focus: Path, context: Path, states: Path) -> dict[str, object]:
    required_states = RECORDING_REQUIRED_STATES if option.surface.startswith("Recording") else LOG_REQUIRED_STATES
    return {
        "optionId": option.option_id,
        "surface": option.surface,
        "footprintClass": option.footprint_class,
        "windowSurfaceClass": option.window_class,
        "intendedUserPurpose": option.purpose,
        "sourceTruthBasis": "Docs/nexus_vision.md; FAM-002; FAM-006; FAM-006 Recording FFV; UIREF-001..006; active external branch plan",
        "referenceSurfaces": ["AI Control Center controls", "HUD Dashboard doorway semantics", "FAM-006 child-window title grammar"],
        "renderAuthorityLevel": "Design Candidate Render",
        "focusedRenderMediaPath": focus.relative_to(PACKET_ROOT).as_posix(),
        "fullDesktopContextRenderMediaPath": context.relative_to(PACKET_ROOT).as_posix(),
        "stateContactSheetMediaPath": states.relative_to(PACKET_ROOT).as_posix(),
        "elementLegend": ["CHROME-001", "TITLE-001", "CTRL-001", "PANEL-001", "ROW-001", "ACTION-001", "ACTION-002", "FOOTER-001"],
        "stateCoverage": {
            state: f"Rendered in {states.relative_to(PACKET_ROOT).as_posix()}" for state in sorted(required_states)
        },
        "requiredStates": sorted(required_states),
        "densitySizeNotes": f"default {option.default_size[0]}x{option.default_size[1]}, min {option.min_size[0]}x{option.min_size[1]}",
        "copyTextNotes": "Short product copy only; no proof/debug/governance copy.",
        "resizeBehavior": option.resize_behavior,
        "tradeoffs": option.tradeoffs,
        "knownRisks": option.risks,
        "whatUserShouldCritique": "Footprint, title treatment, row density, button sizing, action hierarchy, and whether the purpose reads instantly.",
    }


def _accepted_target_record(option: Option, focus: Path, context: Path, states: Path, annotated: Path) -> dict[str, object]:
    required_states = RECORDING_ACCEPTED_REQUIRED_STATES if option.surface.startswith("Recording") else LOG_ACCEPTED_REQUIRED_STATES
    callout_legend = _callout_legend_records(option)
    accepted_basis = "REC-C accepted as base with REC-A target/state separation" if option.surface.startswith("Recording") else "LOG-A accepted as current branch doorway shell"
    rejected_patterns = [
        "REC-B proof/helper copy",
        "native-log status row inside Recording Studio target",
        "mini-dashboard/report-table feel",
        "LOG-B local-path/debug display by default",
        "LOG-C full feature-studio workspace implication",
    ]
    return {
        "targetId": f"FAM006-VAT-{option.option_id}",
        "targetStatus": "USER_ACCEPTED",
        "surface": option.surface,
        "acceptedBasis": accepted_basis,
        "footprintClass": option.footprint_class,
        "windowSurfaceClass": option.window_class,
        "intendedUserPurpose": option.purpose,
        "defaultDimensions": f"{option.default_size[0]}x{option.default_size[1]}",
        "minimumDimensions": f"{option.min_size[0]}x{option.min_size[1]}",
        "resizeBehavior": option.resize_behavior,
        "headerText": "ACTIVE OVERLAY RECORDING" if option.surface.startswith("Recording") else "RECORDING LOGS",
        "titleText": option.title.upper(),
        "rows": [{"label": label, "value": value} for label, value in option.rows],
        "primaryAction": "START RECORDING / STOP RECORDING" if option.surface.startswith("Recording") else option.primary_action.upper(),
        "secondaryAction": option.secondary_action.upper(),
        "rejectedPatterns": rejected_patterns,
        "renderAuthorityLevel": "Visual Acceptance Target",
        "focusedRenderMediaPath": focus.relative_to(PACKET_ROOT).as_posix(),
        "fullDesktopContextRenderMediaPath": context.relative_to(PACKET_ROOT).as_posix(),
        "stateContactSheetMediaPath": states.relative_to(PACKET_ROOT).as_posix(),
        "annotatedCalloutMediaPath": annotated.relative_to(PACKET_ROOT).as_posix(),
        "elementLegend": [row["elementId"] for row in callout_legend],
        "calloutLegend": callout_legend,
        "annotationClarityRequirement": "Each callout uses a printed marker badge, outline, and connector line; color is supportive only.",
        "stateCoverage": {
            state: f"Rendered in {states.relative_to(PACKET_ROOT).as_posix()}" for state in sorted(required_states)
        },
        "requiredStates": sorted(required_states),
        "implementationMatchRequirement": "Later product UI repair must compare actual runtime screenshots/video against this target before H1/LV/UTS progression.",
    }


def _markdown_table(rows: Iterable[Iterable[str]]) -> str:
    return "\n".join("| " + " | ".join(row) + " |" for row in rows)


def _write_packet(stamp: str) -> Path:
    _purge_packet()
    media_root = PACKET_ROOT / "Review Aids" / "Accepted Visual Target" / "media"
    accepted_records: list[dict[str, object]] = []
    for option in ACCEPTED_TARGETS:
        focus = media_root / f"{option.option_id}_focused.png"
        context = media_root / f"{option.option_id}_desktop_context.png"
        states = media_root / f"{option.option_id}_state_contact_sheet.png"
        annotated = media_root / f"{option.option_id}_annotated_callouts.png"
        _draw_window(option, focus)
        _draw_window(option, context, context=True)
        _draw_state_contact_sheet(option, states)
        _draw_annotated_callout(option, annotated)
        accepted_records.append(_accepted_target_record(option, focus, context, states, annotated))

    option_media_root = PACKET_ROOT / "Review Aids" / "Superseded Visual Options" / "media"
    superseded_records: list[dict[str, object]] = []
    for option in OPTIONS:
        focus = option_media_root / f"{option.option_id}_focused.png"
        context = option_media_root / f"{option.option_id}_desktop_context.png"
        states = option_media_root / f"{option.option_id}_state_contact_sheet.png"
        _draw_window(option, focus)
        _draw_window(option, context, context=True)
        _draw_state_contact_sheet(option, states)
        superseded_records.append(_option_record(option, focus, context, states))

    copied = _copy_source_context()
    copied_udl = _copy_udl_context()
    review_aids = PACKET_ROOT / "Review Aids"
    user_review = PACKET_ROOT / "USER Review" / PRIMARY_FILE

    _write_json(review_aids / "Visual Impact Classification.json", {
        "status": "USER_ACCEPTED_VISUAL_TARGET_RECORDED",
        "classifications": VISUAL_CLASSIFICATIONS,
        "rule": "Visible UI/UX repair now proceeds only by separate implementation-match approval against this accepted target.",
        "currentBranchSurfaces": ["Recording Studio", "Log Viewer Studio"],
    })
    _write_json(review_aids / "Accepted Branch Visual Acceptance Target.json", {"status": "USER_ACCEPTED", "targets": accepted_records})
    _write_json(review_aids / "Superseded Visual Options Packet.json", {"options": superseded_records})

    accepted_md = [
        "# Accepted Branch Visual Acceptance Target",
        "",
        "Target Status: `USER_ACCEPTED`",
        "Authority Level: `Visual Acceptance Target`",
        "",
        "This file records the USER/ChatGPT visual decision. It is a pre-implementation visual guide contract, not proof that the runtime implementation already exists or matches it.",
        "",
        "| Target | Surface | Accepted basis | Footprint | Size | Resize | Focused render | Context render | State sheet | Annotated callouts |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in accepted_records:
        accepted_md.append(
            "| {target} | {surface} | {basis} | {footprint} | {size} | {resize} | `{focus}` | `{context}` | `{states}` | `{annotated}` |".format(
                target=record["targetId"],
                surface=record["surface"],
                basis=record["acceptedBasis"],
                footprint=record["footprintClass"],
                size=record["defaultDimensions"],
                resize=record["resizeBehavior"],
                focus=record["focusedRenderMediaPath"],
                context=record["fullDesktopContextRenderMediaPath"],
                states=record["stateContactSheetMediaPath"],
                annotated=record["annotatedCalloutMediaPath"],
            )
        )
    (review_aids / "Accepted Branch Visual Acceptance Target.md").write_text("\n".join(accepted_md) + "\n", encoding="utf-8")

    callout_md = [
        "# Annotated Callout Legend Table",
        "",
        "Every marker below appears in the accepted-target annotated media as a printed badge, outline, and connector line. Color is supportive only and is not the sole identification method.",
        "",
        "| Surface | Callout marker | Element ID | Element name | Status | Purpose note | Non-color marker method |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in accepted_records:
        for row in record["calloutLegend"]:
            callout_md.append(
                "| {surface} | `{marker}` | `{element}` | {name} | `{status}` | {note} | {method} |".format(
                    surface=record["surface"],
                    marker=row["calloutMarker"],
                    element=row["elementId"],
                    name=row["elementName"],
                    status=row["acceptedRejectedReviseStatus"],
                    note=row["purposeNote"],
                    method=row["nonColorMarkerMethod"],
                )
            )
    (review_aids / "Annotated Callout Legend Table.md").write_text("\n".join(callout_md) + "\n", encoding="utf-8")

    selection = [
        "# Visual Selection Ledger",
        "",
        "| decision ID | surface | option ID | element ID | accepted / rejected / combine / revise | USER notes | source-truth impact | branch-local vs durable design principle | implementation requirement | proof requirement | future reuse note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    selection.extend("| " + " | ".join(row) + " |" for row in ACCEPTED_SELECTION_ROWS)
    (review_aids / "Visual Selection Ledger.md").write_text("\n".join(selection) + "\n", encoding="utf-8")

    target = [
        "# Branch Visual Acceptance Target",
        "",
        "Target ID: `FAM006-VAT-USER-ACCEPTED-20260624`",
        "Target Status: `USER_ACCEPTED`",
        "Selected Option(s): `REC-C as base with REC-A target/state separation; LOG-A as base`",
        "Selected Element Decisions: `See Visual Selection Ledger`",
        "Surface Purpose: `Recording Studio is a compact detached controller; Log Viewer Studio is a compact native/export doorway shell`",
        "Footprint Class: `Recording Studio COMPACT_CONTROLLER; Log Viewer Studio DOORWAY_SHELL`",
        "Default Dimensions: `Recording Studio 392x184 target render; Log Viewer Studio 430x184 target render`",
        "Resize Behavior: `Recording fixed-size/movable/no resize affordance; Log doorway shell fixed-size unless later source truth admits viewer workspace resizing`",
        "State Matrix: `default, hover, focus, pressed/active, disabled, empty/no-data, blocked/error, success/complete, fixed-size proof required before implementation-match proof`",
        "Copy Rules: `Short product copy only; no proof/debug/governance/internal wording`",
        "Spacing/Density Rules: `Same-class primitives must be identical or explicitly varied by accepted target`",
        "Button/Control Rules: `Content-fit primitive, equal left/right gutters, shared hover/focus/pressed/disabled grammar`",
        "Status/Error/Empty Rules: `Truthful runtime state; no fake readiness; no hidden failures`",
        "Accepted Reference Surfaces: `AI Control Center same-class control primitives; FAM-006 child-window title grammar; HUD Dashboard doorway/action semantics only`",
        "Accepted Exceptions: `None for proof/debug copy, dashboard/report-table feel, default local-path display, fake full-viewer workspace, or Recording labels in Log Viewer state names`",
        "Implementation Constraints: `This packet does not approve runtime/product UI repair by itself; implementation-match repair still needs separate approval`",
        "Proof Requirements: `Focused implementation screenshots/video, full desktop/context screenshots, element legends, state matrix, implementation-match checklist, LV exact desktop launcher proof`",
    ]
    (review_aids / "Branch Visual Acceptance Target.md").write_text("\n".join(target) + "\n", encoding="utf-8")

    checklist = [
        "# Implementation-Match Checklist",
        "",
        "| ID | Surface | Requirement | Required implementation proof | Blocking disposition |",
        "| --- | --- | --- | --- | --- |",
        "| IMC-REC-001 | Recording Studio | Header `ACTIVE OVERLAY RECORDING`; title `RECORDING STUDIO`; no separated title card. | Focused runtime screenshot and annotated crop. | Blocks H1/LV if missing. |",
        "| IMC-REC-002 | Recording Studio | Target row `Default Overlay Profile`; State row `Ready - 2 active monitors`. | Focused row crop with readable text. | Blocks H1/LV if missing. |",
        "| IMC-REC-003 | Recording Studio | One stateful primary action: `START RECORDING` changes to `STOP RECORDING`; one secondary `OPEN LOGS`. | Ordered screenshot/video frames before/after click. | Blocks H1/LV if missing. |",
        "| IMC-REC-004 | Recording Studio | Reject REC-B proof copy, native-log status row, report-table/minidashboard feel, and internal proof wording. | Negative visual proof / text audit. | Blocks H1/LV if present. |",
        "| IMC-LOG-001 | Log Viewer Studio | Header `RECORDING LOGS`; title `LOG VIEWER STUDIO`; no Recording Studio state names. | Focused runtime screenshot and text audit. | Blocks H1/LV if missing. |",
        "| IMC-LOG-002 | Log Viewer Studio | Row 1 `NATIVE - Recordings folder`; action `OPEN NATIVE LOGS`. | Focused row/action crop and activation proof. | Blocks H1/LV if missing. |",
        "| IMC-LOG-003 | Log Viewer Studio | Row 2 `EXPORT - Exported Logs folder`; action `OPEN EXPORTED LOGS`. | Focused row/action crop and activation proof. | Blocks H1/LV if missing. |",
        "| IMC-LOG-004 | Log Viewer Studio | No default local path display, graph/export customization, previous-log selection, or fake full-viewer workspace. | Negative visual proof / text audit. | Blocks H1/LV if present. |",
        "| IMC-BOTH-001 | Both studios | Same-class controls, gutters, type, glow, radius, hover/focus/pressed/disabled states match accepted primitives or explicitly logged exception. | State contact sheet and implementation screenshots. | Blocks H1/LV if unproven. |",
    ]
    (review_aids / "Implementation-Match Checklist.md").write_text("\n".join(checklist) + "\n", encoding="utf-8")

    rejected = [
        "# Rejected Options And Patterns Ledger",
        "",
        "| pattern ID | rejected UI/UX pattern | source option or prior screenshot | reason rejected | affected surface/class | future avoidance guidance | source-truth impact | linked USER feedback |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    rejected.extend("| " + " | ".join(row) + " |" for row in REJECTED_PATTERNS)
    rejected.extend([
        "| VSL-REC-B | REC-B final body/copy | REC-B | USER rejected helper/proof copy, native-log status row, mini-dashboard/report-table feel, and internal proof wording. | Recording Studio | Do not implement REC-B final structure. | Branch-local accepted target | Current USER/ChatGPT decision |",
        "| VSL-LOG-B | LOG-B local-path/debug display | LOG-B | USER rejected local-path/technical/debug appearance. | Log Viewer Studio | Do not display local paths by default. | Branch-local accepted target | Current USER/ChatGPT decision |",
        "| VSL-LOG-C | LOG-C full feature-studio workspace | LOG-C | USER deferred full viewer workspace; current branch is doorway shell only. | Log Viewer Studio | Keep graph/export customization/previous-log selection future-gated. | Branch-local accepted target | Current USER/ChatGPT decision |",
    ])
    (review_aids / "Rejected Options And Patterns Ledger.md").write_text("\n".join(rejected) + "\n", encoding="utf-8")

    recipe = [
        "# Reusable Design Recipe Template",
        "",
        "Accepted Surface Class: `Unique child / standalone-capable feature-studio window`",
        "Accepted Footprint Class: `COMPACT_CONTROLLER for Recording; DOORWAY_SHELL for Log Viewer`",
        "Token Values / Dimensions: `See Branch Visual Acceptance Target; exact runtime tokens require implementation-match proof`",
        "Padding: `Content-fit and compact; no giant button wells`",
        "Spacing: `Equal left/right gutters and same-class primitive rhythm`",
        "Button Heights: `Compact content-fit; prove by screenshot/video after implementation`",
        "Font Scale: `Nexus same-class primitive type; prove by implementation match`",
        "Status Chip Pattern: `No debug/proof/internal copy`",
        "Title/Header Grammar: `Category line plus strong title; no separated title card`",
        "Resize Behavior: `Recording fixed; Log Viewer fixed doorway shell unless later accepted source truth changes it`",
        "Copy Pattern: `Short product copy only`",
        "State Pattern: `default, hover, focus, pressed, disabled, blocked/error, empty, success`",
        "Accepted Comparator References: `AI Control Center same-class controls; FAM-006 child-window title grammar; HUD doorway semantics only`",
        "Rejected Alternatives: `See Rejected Options And Patterns Ledger`",
        "Future Branch Reuse Notes: `Fold down after implementation proof passes`",
        "Proof Requirements: `packet-contained render media plus later implementation-match screenshots/video`",
    ]
    (review_aids / "Reusable Design Recipe Template.md").write_text("\n".join(recipe) + "\n", encoding="utf-8")

    _write_json(review_aids / "Source Truth Conflict Classification.json", {
        "status": "USER_ACCEPTED_VISUAL_DECISIONS_CLASSIFIED",
        "classificationVocabulary": ["BRANCH_LOCAL_VISUAL_DECISION", "GOVERNANCE_CANDIDATE_ONLY", "NO_CONFLICT"],
        "classifications": CONFLICT_CLASSIFICATION_ROWS,
    })
    conflict_md = [
        "# Source Truth Conflict Classification",
        "",
        "Accepted visual target decisions are branch-local source-truth records. Governance promotion remains candidate only.",
        "",
        "| decision | classification | risk area | basis | USER decision needed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in CONFLICT_CLASSIFICATION_ROWS:
        conflict_md.append("| {decision} | `{classification}` | {riskArea} | {basis} | {userDecisionNeeded} |".format(**row))
    (review_aids / "Source Truth Conflict Classification.md").write_text("\n".join(conflict_md) + "\n", encoding="utf-8")

    (review_aids / "Governance Candidate Only.md").write_text(
        "# Governance Candidate Only\n\n"
        "Candidate: promote a global Visual Acceptance Target gate for visible UI/UX changes.\n\n"
        "Current packet records branch-local FAM-006 target acceptance only. Governance worktree mutation remains excluded.\n\n"
        "Exact future approval needed: `I approve Governance to evaluate and promote the FAM-006 Visual Acceptance Target process into global source truth and validators, using the FAM-006 branch-local packet as evidence only.`\n",
        encoding="utf-8",
    )
    (review_aids / "Visual Acceptance Lifecycle.md").write_text(
        "# Visual Acceptance Lifecycle Clarification\n\n"
        "- `Concept Render`: brainstorming only.\n"
        "- `Design Candidate Render`: selectable review option, not accepted source truth.\n"
        "- `Visual Acceptance Target`: USER-accepted pre-implementation visual guide contract.\n"
        "- `Implementation Match Proof`: actual product screenshot/video proving runtime UI matches the accepted target.\n\n"
        "This packet records `Visual Acceptance Target`. It does not claim implementation match, H1 green, Live Validation green, UTS acceptance, PR Readiness, release readiness, or issue closure.\n",
        encoding="utf-8",
    )
    (review_aids / "Annotated Callout Legend Requirement.md").write_text(
        "# Annotated / Callout Legend Requirement\n\n"
        "Future visual-target and implementation-match packets must include annotated/callout renders, not only plain tables.\n\n"
        "- Stable callout IDs for material element groups.\n"
        "- Visible outlines/arrows/badges/markers.\n"
        "- No reliance on color alone.\n"
        "- Recording Studio callouts must split TARGET-001, STATUS-001, ACTION-001, and ACTION-002.\n"
        "- Log Viewer Studio callouts must split ROW-001, ROW-002, ACTION-001, and ACTION-002.\n"
        "- State contact sheets must explicitly include secondary-action states, not infer them from primary actions.\n"
        "- Annotations are review/proof artifacts only and must not be injected into product UI.\n"
        "- The ZIP must include the actual media files, not only local paths.\n",
        encoding="utf-8",
    )
    (review_aids / "Superseded Visual Options Packet.md").write_text(
        "# Superseded Visual Options Context\n\n"
        "These Design Candidate Renders are retained as context only. The accepted target is `REC-C-ACCEPTED` and `LOG-A-ACCEPTED`.\n\n"
        "| Option | Surface | Status | Reason |\n"
        "| --- | --- | --- | --- |\n"
        "| REC-A | Recording Studio | PARTIAL_SOURCE | Clearer target/state separation borrowed into accepted target. |\n"
        "| REC-B | Recording Studio | REJECTED | Proof/helper copy, native-log status row, mini-dashboard/report-table feel, internal proof wording. |\n"
        "| REC-C | Recording Studio | ACCEPTED_BASE | Action-first compact controller base. |\n"
        "| LOG-A | Log Viewer Studio | ACCEPTED_BASE | Compact native/export doorway shell. |\n"
        "| LOG-B | Log Viewer Studio | REJECTED | Local-path/technical/debug presentation. |\n"
        "| LOG-C | Log Viewer Studio | DEFERRED | Future full viewer workspace implication. |\n",
        encoding="utf-8",
    )

    (review_aids / "Validation Outputs.md").write_text(
        "# Validation Outputs\n\nPacket generator validation is run after packet creation and copied here.\nLive Validation was not run.\nUTS acceptance was not claimed.\n\nFinal ZIP SHA policy: authoritative final ZIP SHA is external to the ZIP because embedding it would mutate the ZIP bytes.\n",
        encoding="utf-8",
    )

    primary = [
        "# FAM-006 Accepted Branch Visual Acceptance Target Review",
        "",
        "Packet Status: `branch-local-accepted-visual-target-review`",
        "Packet Reviewability State: `Reviewable`",
        "USER Gate State: `USER_ACCEPTED Visual Acceptance Target; implementation-match repair pending separate approval`",
        "Runtime Implementation State: `Blocked until separate implementation-match repair approval`",
        "Live Validation State: `Not run; blocked until implementation-match proof`",
        "",
        "## Accepted Recording Studio Target",
        "",
        "- Base: `REC-C` with REC-A target/state separation.",
        "- Header: `ACTIVE OVERLAY RECORDING`; title: `RECORDING STUDIO`.",
        "- Rows: `TARGET - Default Overlay Profile`; `STATE - Ready - 2 active monitors`.",
        "- Primary stateful button: `START RECORDING / STOP RECORDING`; secondary action: `OPEN LOGS`.",
        "- Rejected: REC-B proof/helper copy, native-log status row, mini-dashboard/report-table feel, internal proof wording.",
        "",
        "## Accepted Log Viewer Studio Target",
        "",
        "- Base: `LOG-A`.",
        "- Header: `RECORDING LOGS`; title: `LOG VIEWER STUDIO`.",
        "- Row 1: `NATIVE - Recordings folder`; action `OPEN NATIVE LOGS`.",
        "- Row 2: `EXPORT - Exported Logs folder`; action `OPEN EXPORTED LOGS`.",
        "- Rejected: local path display by default, technical/debug copy, LOG-C full viewer workspace, graph/export customization, previous-log selection.",
        "- State labels are Log Viewer specific and do not use Recording Studio labels like `RECORDING` or `SAVED COMPLETE`.",
        "",
        "## Media To Review",
        "",
        "Open `Review Aids/Accepted Branch Visual Acceptance Target.md` and inspect the packet-contained focused, desktop-context, state/contact-sheet, and annotated/callout PNGs under `Review Aids/Accepted Visual Target/media/`.",
        "",
        "## USER Decision Needed",
        "",
        "Confirm whether Codex may proceed to separate implementation-match repair using this accepted Visual Acceptance Target.",
        "",
        "```text",
        "I approve bounded FAM-006 implementation-match repair for Recording Studio and Log Viewer Studio against the USER_ACCEPTED Visual Acceptance Target recorded in the current packet.",
        "```",
    ]
    user_review.write_text("\n".join(primary) + "\n", encoding="utf-8")

    (PACKET_ROOT / "START_HERE.md").write_text(
        "# FAM-006 Accepted Visual Acceptance Target Packet\n\n"
        f"Generated: `{stamp}`\n"
        "Review Purpose: inspect the accepted branch visual target and decide whether to approve separate implementation-match repair.\n"
        f"Primary USER Review File: `USER Review/{PRIMARY_FILE}`\n"
        "Packet Reviewability State: `Reviewable`\n"
        "USER Gate State: `USER_ACCEPTED Visual Acceptance Target; implementation-match repair pending separate approval`\n"
        "Runtime Implementation State: `Blocked`\n"
        "Live Validation State: `Not run`\n\n"
        "## Review Order\n\n"
        "1. Open the primary USER review file.\n"
        "2. Inspect `Review Aids/Accepted Branch Visual Acceptance Target.md` and media in `Review Aids/Accepted Visual Target/media/`.\n"
        "3. Review `Review Aids/Visual Selection Ledger.md`, `Review Aids/Branch Visual Acceptance Target.md`, and `Review Aids/Implementation-Match Checklist.md`.\n"
        "4. Review `Review Aids/Rejected Options And Patterns Ledger.md`, `Review Aids/Visual Acceptance Lifecycle.md`, and `Review Aids/Annotated Callout Legend Requirement.md`.\n"
        "5. Decide whether Codex may proceed to separate implementation-match repair.\n",
        encoding="utf-8",
    )

    process_payload = {
        "External State Schema": "external-state-v1",
        "status": "USER_ACCEPTED_VISUAL_TARGET_PACKET_GENERATED",
        "branch": _run_git("branch", "--show-current"),
        "head": _run_git("rev-parse", "HEAD"),
        "visualImpactClassification": VISUAL_CLASSIFICATIONS,
        "authorityLevels": AUTHORITY_LEVELS,
        "acceptedTargets": accepted_records,
        "supersededOptions": superseded_records,
        "copiedSourceTruthContext": copied,
        "copiedUdlFalseGreenEvidence": copied_udl,
        "userPacket": str(PACKET_ROOT),
        "nextLegalPhase": "USER decision on separate implementation-match repair against the USER_ACCEPTED visual target",
        "governanceCandidateOnly": "Promote globally after USER approves a Governance carrier; not implemented globally here.",
    }
    _write_json(EXTERNAL_PROCESS_JSON, process_payload)
    EXTERNAL_PROCESS_MD.parent.mkdir(parents=True, exist_ok=True)
    EXTERNAL_PROCESS_MD.write_text(
        "# FAM-006 Branch-Local Visual Acceptance Target Process\n\n"
        "Status: `USER_ACCEPTED_VISUAL_TARGET_PACKET_GENERATED / Pending separate implementation-match repair approval`.\n\n"
        "This branch-local process records the accepted rendered visual target before any further visible UI/UX implementation repair for Recording Studio or Log Viewer Studio.\n\n"
        "Authority levels:\n\n"
        + "\n".join(f"- `{key}`: {value}" for key, value in AUTHORITY_LEVELS.items())
        + "\n\nUSER packet: `C:\\Nexus USER\\FAM-006`.\n\nGlobal/Governance promotion remains candidate only.\n",
        encoding="utf-8",
    )

    if BRANCH_PLAN.exists():
        marker = "\n## FAM-006 Branch-Local Visual Acceptance Target Gate - 2026-06-24\n"
        text = BRANCH_PLAN.read_text(encoding="utf-8")
        receipt = (
            marker
            + "\n"
            + "Status: `USER_ACCEPTED / Pending separate implementation-match repair approval`.\n\n"
            + "USER accepted REC-C as the Recording Studio base with REC-A target/state separation and LOG-A as the Log Viewer Studio base. This accepted target is a pre-implementation visual guide contract, not implementation proof.\n\n"
            + f"USER packet: `C:\\Nexus USER\\FAM-006` with primary file `USER Review/{PRIMARY_FILE}`.\n\n"
            + "Next legal phase: `USER decision on bounded implementation-match repair against the accepted Visual Acceptance Target`; renewed H1, Live Validation, UTS, and PR Readiness remain pending.\n"
        )
        if marker.strip() in text:
            text = text.split(marker, 1)[0].rstrip() + receipt
        else:
            text = text.rstrip() + "\n" + receipt
        BRANCH_PLAN.write_text(text, encoding="utf-8")

    if BRANCH_STATE.exists():
        marker = "\n## Accepted Visual Acceptance Target Receipt - 2026-06-24\n"
        text = BRANCH_STATE.read_text(encoding="utf-8")
        receipt = (
            marker
            + "\n"
            + "Status: `USER_ACCEPTED / Pending separate implementation-match repair approval`.\n\n"
            + "Accepted Recording Target: `REC-C base with REC-A target/state separation; compact controller; TARGET Default Overlay Profile; STATE Ready - 2 active monitors; START/STOP stateful primary action; OPEN LOGS secondary action; REC-B proof/debug/native-log-status/report-table patterns rejected`.\n\n"
            + "Accepted Log Viewer Target: `LOG-A base; compact doorway shell; NATIVE Recordings folder with OPEN NATIVE LOGS; EXPORT Exported Logs folder with OPEN EXPORTED LOGS; LOG-B path/debug and LOG-C full viewer workspace rejected/deferred`.\n\n"
            + "Lifecycle: `Visual Acceptance Target is accepted as pre-implementation guidance only. Runtime implementation match, H1, Live Validation, UTS, PR Readiness, issue closeout, merge, release, and cleanup remain pending.`\n\n"
            + f"USER packet: `C:\\Nexus USER\\FAM-006` with primary file `USER Review/{PRIMARY_FILE}`.\n\n"
            + "Next Legal Phase: `USER decision on bounded implementation-match repair against the accepted Visual Acceptance Target`.\n"
        )
        if marker.strip() in text:
            text = text.split(marker, 1)[0].rstrip() + receipt
        else:
            text = text.rstrip() + "\n" + receipt
        BRANCH_STATE.write_text(text, encoding="utf-8")

    return _zip_packet(stamp)


def _zip_packet(stamp: str) -> Path:
    zip_path = USER_ROOT / f"FAM-006-{stamp}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKET_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKET_ROOT).as_posix())
    return zip_path


def _command_record(name: str, command: list[str], *, timeout: int = 120) -> dict[str, object]:
    started = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        return {
            "name": name,
            "command": command,
            "cwd": str(ROOT),
            "timestamp": started,
            "exitCode": completed.returncode,
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "stdout": completed.stdout[-12000:],
            "stderr": completed.stderr[-12000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "name": name,
            "command": command,
            "cwd": str(ROOT),
            "timestamp": started,
            "exitCode": 124,
            "status": "TIMEOUT",
            "stdout": (exc.stdout or "")[-12000:] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[-12000:] if isinstance(exc.stderr, str) else "",
        }


def _write_validation_outputs(stamp: str, zip_path: Path, packet_failures: list[str]) -> None:
    out_dir = PACKET_ROOT / "Review Aids" / "Validation Outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    packet_validation = {
        "name": "visual target packet validator",
        "command": [sys.executable, "dev/orin_fam006_visual_acceptance_target_packet.py", "--validate", "--zip", str(zip_path)],
        "cwd": str(ROOT),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "exitCode": 0 if not packet_failures else 1,
        "status": "PASS" if not packet_failures else "FAIL",
        "stdout": json.dumps({"status": "PASS" if not packet_failures else "FAIL", "failures": packet_failures}, indent=2),
        "stderr": "",
    }
    _write_json(out_dir / "visual_acceptance_target_packet_validation.json", packet_validation)

    commands = [
        ("git identity status", ["git", "status", "--short", "--branch"]),
        ("git head", ["git", "rev-parse", "HEAD"]),
        ("git origin main", ["git", "rev-parse", "origin/main"]),
        ("git merge base", ["git", "merge-base", "HEAD", "origin/main"]),
        ("git ahead behind origin main", ["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"]),
        ("git diff check", ["git", "diff", "--check"]),
        ("git diff check origin main head", ["git", "diff", "--check", "origin/main...HEAD"]),
        ("git diff cached check", ["git", "diff", "--cached", "--check"]),
        ("unified defect ledger gate", [sys.executable, "dev/orin_fam006_unified_defect_ledger.py"]),
        ("false accept known bad replay", [sys.executable, "dev/orin_fam006_false_accept_regression_gate.py", "--known-bad-only"]),
        ("visual conformance ledger", [sys.executable, "dev/orin_fam006_visual_conformance_ledger.py"]),
        ("hardening h1 helper", [sys.executable, "dev/orin_fam006_hardening_h1.py"]),
        ("monitoring hud surface validation", [sys.executable, "dev/orin_monitoring_hud_surface_validation.py"]),
        ("monitoring hud internal sandbox validation", [sys.executable, "dev/orin_monitoring_hud_internal_sandbox_validation.py"]),
        ("branch governance validation", [sys.executable, "dev/orin_branch_governance_validation.py"]),
        ("worktree confinement gate", [sys.executable, "dev/orin_branch_governance_validation.py", "--worktree-confinement-gate"]),
        ("release readiness health gate", [sys.executable, "dev/orin_branch_governance_validation.py", "--release-readiness-health-gate"]),
        ("branch readiness planning fixture validation", [sys.executable, "dev/orin_branch_readiness_planning_fixture_validation.py"]),
        ("source owner marker validation", [sys.executable, "dev/orin_source_owner_marker_validation.py"]),
        ("external state validation", [sys.executable, "dev/orin_external_state_validation.py", "--root", "C:/Nexus Governance State", "--repo", str(ROOT), "--require-root"]),
        ("release body validation", [sys.executable, "dev/orin_release_body_validation.py"]),
        ("ai provider state validation", [sys.executable, "dev/orin_ai_provider_state_validation.py"]),
        ("compileall", [sys.executable, "-m", "compileall", "-q", "dev", "desktop", "Audio", "main.py", "nexus_visual"]),
    ]
    nonblocking_for_this_packet = {
        "visual conformance ledger",
        "hardening h1 helper",
    }
    packet_validation["blockingForVisualTargetPacket"] = True
    records = [packet_validation]
    for name, command in commands:
        record = _command_record(name, command)
        record["blockingForVisualTargetPacket"] = name not in nonblocking_for_this_packet
        records.append(record)
        safe_name = name.replace(" ", "_").replace("/", "_")
        _write_json(out_dir / f"{safe_name}.json", record)

    blocking_records = [record for record in records if record.get("blockingForVisualTargetPacket", True)]
    summary = {
        "status": "PASS" if all(record["status"] == "PASS" for record in blocking_records) else "FAIL_OR_REVIEW",
        "stamp": stamp,
        "zipPathAtPreZipValidationTime": str(zip_path),
        "postZipShaPolicy": "Final ZIP SHA cannot be embedded inside the ZIP without changing the ZIP. The final SHA is written to external state and returned by Codex after final ZIP creation.",
        "nonBlockingEvidenceForThisPacket": sorted(nonblocking_for_this_packet),
        "records": [
            {
                "name": record["name"],
                "command": record["command"],
                "exitCode": record["exitCode"],
                "status": record["status"],
                "blockingForVisualTargetPacket": record.get("blockingForVisualTargetPacket", True),
            }
            for record in records
        ],
    }
    _write_json(out_dir / "validation_outputs_summary.json", summary)
    lines = [
        "# Validation Outputs",
        "",
        f"Validation Output Summary Status: `{summary['status']}`",
        "",
        "Final ZIP SHA policy: the byte-identical final ZIP SHA is not embedded inside the ZIP because doing so would change the ZIP. Final post-ZIP SHA proof is recorded in external state and the Codex return packet.",
        "",
        "| command | status | blocking for this packet | exit code | output file |",
        "| --- | --- | --- | --- | --- |",
    ]
    for record in records:
        output_file = "visual_acceptance_target_packet_validation.json" if record is packet_validation else record["name"].replace(" ", "_").replace("/", "_") + ".json"
        lines.append(f"| {record['name']} | `{record['status']}` | `{record.get('blockingForVisualTargetPacket', True)}` | {record['exitCode']} | `Review Aids/Validation Outputs/{output_file}` |")
    (PACKET_ROOT / "Review Aids" / "Validation Outputs.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_post_zip_external_manifest(stamp: str, zip_path: Path, failures: list[str]) -> None:
    manifest = {
        "External State Schema": "external-state-v1",
        "status": "POST_ZIP_MANIFEST_RECORDED",
        "stamp": stamp,
        "packetRoot": str(PACKET_ROOT),
        "zipPath": str(zip_path),
        "zipSha256": _sha256(zip_path) if zip_path.exists() else "",
        "finalPacketValidationStatus": "PASS" if not failures else "FAIL",
        "finalPacketValidationFailures": failures,
        "postZipShaPolicy": "Authoritative final ZIP SHA is external to the ZIP because embedding it would mutate the ZIP bytes.",
    }
    _write_json(EXTERNAL_ROOT / "visual_acceptance_target_post_zip_manifest.json", manifest)
    (EXTERNAL_ROOT / "visual_acceptance_target_post_zip_manifest.md").write_text(
        "# FAM-006 Visual Acceptance Target Post-ZIP Manifest\n\n"
        f"Status: `{manifest['finalPacketValidationStatus']}`\n\n"
        f"Packet Root: `{PACKET_ROOT}`\n\n"
        f"Timestamped ZIP: `{zip_path}`\n\n"
        f"ZIP SHA256: `{manifest['zipSha256']}`\n\n"
        "Post-ZIP SHA Policy: authoritative final ZIP SHA is external to the ZIP because embedding it would mutate the ZIP bytes.\n",
        encoding="utf-8",
    )


def validate(packet_root: Path = PACKET_ROOT, zip_path: Path | None = None) -> list[str]:
    failures: list[str] = []
    if not packet_root.exists():
        return [f"packet root missing: {packet_root}"]
    for required in ["START_HERE.md", f"USER Review/{PRIMARY_FILE}"]:
        if not (packet_root / required).is_file():
            failures.append(f"missing required packet file: {required}")
    for name in EXPECTED_DIRS:
        if not (packet_root / name).is_dir():
            failures.append(f"missing required packet directory: {name}")
    primary_files = list((packet_root / "USER Review").glob("*.md")) if (packet_root / "USER Review").exists() else []
    if len(primary_files) != 1:
        failures.append(f"USER Review must contain exactly one primary Markdown file; found {len(primary_files)}")
    required_aids = [
        "Visual Impact Classification.json",
        "Accepted Branch Visual Acceptance Target.json",
        "Accepted Branch Visual Acceptance Target.md",
        "Superseded Visual Options Packet.json",
        "Superseded Visual Options Packet.md",
        "Visual Selection Ledger.md",
        "Branch Visual Acceptance Target.md",
        "Implementation-Match Checklist.md",
        "Rejected Options And Patterns Ledger.md",
        "Reusable Design Recipe Template.md",
        "Visual Acceptance Lifecycle.md",
        "Annotated Callout Legend Requirement.md",
        "Annotated Callout Legend Table.md",
        "Source Truth Conflict Classification.json",
        "Source Truth Conflict Classification.md",
        "Governance Candidate Only.md",
        "Unified Defect Ledger/UDL_FALSE_GREEN_STATUS.md",
        "Unified Defect Ledger/udl_false_green_status.json",
        "Validation Outputs.md",
    ]
    for rel in required_aids:
        if not (packet_root / "Review Aids" / rel).is_file():
            failures.append(f"missing review aid: {rel}")
    accepted_json = packet_root / "Review Aids" / "Accepted Branch Visual Acceptance Target.json"
    if accepted_json.exists():
        data = json.loads(accepted_json.read_text(encoding="utf-8"))
        if data.get("status") != "USER_ACCEPTED":
            failures.append("accepted target JSON must have USER_ACCEPTED status")
        targets = data.get("targets", [])
        if len(targets) != 2:
            failures.append(f"expected exactly 2 accepted targets, found {len(targets)}")
        surfaces = {target.get("surface") for target in targets}
        for surface in ("Recording Studio", "Log Viewer Studio"):
            if surface not in surfaces:
                failures.append(f"accepted target missing surface: {surface}")
        for option in targets:
            for field in (
                "targetId",
                "targetStatus",
                "surface",
                "footprintClass",
                "windowSurfaceClass",
                "renderAuthorityLevel",
                "focusedRenderMediaPath",
                "fullDesktopContextRenderMediaPath",
                "stateContactSheetMediaPath",
                "annotatedCalloutMediaPath",
                "elementLegend",
                "calloutLegend",
                "annotationClarityRequirement",
                "stateCoverage",
                "requiredStates",
                "resizeBehavior",
            ):
                if not option.get(field):
                    failures.append(f"accepted target missing field {field}: {option.get('targetId')}")
            if option.get("targetStatus") != "USER_ACCEPTED":
                failures.append(f"accepted target has wrong status: {option.get('targetId')}")
            for field in ("focusedRenderMediaPath", "fullDesktopContextRenderMediaPath", "stateContactSheetMediaPath", "annotatedCalloutMediaPath"):
                rel = option.get(field)
                if rel and not (packet_root / rel).is_file():
                    failures.append(f"accepted target media missing: {rel}")
            if option.get("renderAuthorityLevel") != "Visual Acceptance Target":
                failures.append(f"accepted target has wrong authority level: {option.get('targetId')}")
            required_states = set(option.get("requiredStates", []))
            rendered_states = set((option.get("stateCoverage") or {}).keys())
            if required_states != rendered_states:
                failures.append(f"state coverage mismatch for {option.get('targetId')}: required {sorted(required_states)} rendered {sorted(rendered_states)}")
            surface = option.get("surface")
            required_elements = (
                {"CHROME-001", "TITLE-001", "CTRL-001", "TARGET-001", "STATUS-001", "ACTION-001", "ACTION-002"}
                if surface == "Recording Studio"
                else {"CHROME-001", "TITLE-001", "CTRL-001", "ROW-001", "ROW-002", "ACTION-001", "ACTION-002"}
            )
            element_legend = set(option.get("elementLegend", []))
            if element_legend != required_elements:
                failures.append(f"element legend mismatch for {option.get('targetId')}: required {sorted(required_elements)} found {sorted(element_legend)}")
            if "PANEL-001" in element_legend:
                failures.append(f"grouped body/panel callout is forbidden for accepted target: {option.get('targetId')}")
            callout_legend = option.get("calloutLegend") or []
            callout_elements = {row.get("elementId") for row in callout_legend}
            if callout_elements != required_elements:
                failures.append(f"callout legend mismatch for {option.get('targetId')}: required {sorted(required_elements)} found {sorted(callout_elements)}")
            for row in callout_legend:
                if not row.get("calloutMarker") or not row.get("elementId") or not row.get("elementName") or not row.get("purposeNote"):
                    failures.append(f"callout legend row incomplete for {option.get('targetId')}: {row}")
                method = row.get("nonColorMarkerMethod", "")
                if not all(token in method for token in ("printed marker", "outline", "connector line")):
                    failures.append(f"callout row relies on insufficient non-color marker method for {option.get('targetId')}: {row}")
                rect = row.get("rect")
                if not isinstance(rect, list) or len(rect) != 4:
                    failures.append(f"callout row missing rect for {option.get('targetId')}: {row}")
            if surface == "Recording Studio":
                for token in ("ACTION-002-hover", "ACTION-002-focus", "ACTION-002-pressed", "ACTION-002-disabled"):
                    if token not in rendered_states:
                        failures.append(f"Recording accepted target missing secondary-action state: {token}")
                for forbidden_element in ("ROW-001", "ROW-002"):
                    if forbidden_element in element_legend:
                        failures.append(f"Recording accepted target uses wrong row element ID: {forbidden_element}")
            if surface == "Log Viewer Studio":
                for token in ("ACTION-002-hover", "ACTION-002-focus", "ACTION-002-pressed", "ACTION-002-disabled", "ACTION-002-blocked", "ROW-002-export-empty", "ROW-002-export-available"):
                    if token not in rendered_states:
                        failures.append(f"Log Viewer accepted target missing secondary/export state: {token}")
                for forbidden_token in ("recording", "saved_complete", "ACTION-001-recording", "ACTION-001-saved-complete"):
                    if forbidden_token in rendered_states:
                        failures.append(f"Log Viewer accepted target contains Recording-specific state token: {forbidden_token}")
    accepted_media = list((packet_root / "Review Aids" / "Accepted Visual Target" / "media").glob("*.png"))
    if len(accepted_media) < 8:
        failures.append(f"expected at least 8 accepted target PNG media files, found {len(accepted_media)}")
    annotated_media = [path for path in accepted_media if path.name.endswith("_annotated_callouts.png")]
    if len(annotated_media) < 2:
        failures.append(f"expected at least 2 annotated/callout media files, found {len(annotated_media)}")
    state_media = [path for path in accepted_media if path.name.endswith("_state_contact_sheet.png")]
    if len(state_media) < 2:
        failures.append(f"expected at least 2 accepted target state contact sheets, found {len(state_media)}")
    source_context_files = list((packet_root / "Source Truth Context").glob("*")) if (packet_root / "Source Truth Context").exists() else []
    if len(source_context_files) < 15:
        failures.append(f"source truth context too small: {len(source_context_files)} files")
    start = (packet_root / "START_HERE.md").read_text(encoding="utf-8", errors="replace")
    if f"USER Review/{PRIMARY_FILE}" not in start:
        failures.append("START_HERE does not point to primary USER review file")
    generated_text_roots = [
        packet_root / "START_HERE.md",
        packet_root / "USER Review",
        packet_root / "Review Aids",
    ]
    generated_text_files: list[Path] = []
    for target in generated_text_roots:
        if target.is_file():
            generated_text_files.append(target)
        elif target.is_dir():
            generated_text_files.extend(
                path
                for path in target.rglob("*")
                if path.is_file()
                and path.suffix.lower() in {".md", ".json", ".txt"}
                and "Validation Outputs" not in path.parts
                and "Unified Defect Ledger" not in path.parts
            )
    text_blob = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in generated_text_files
    )
    forbidden = [
        "Live Validation State: `Green`",
        "UTS accepted",
        "PR-ready",
    ]
    for token in forbidden:
        if token in text_blob:
            failures.append(f"packet contains forbidden progression claim: {token}")
    text_requirements = {
        "USER_ACCEPTED": "accepted target status",
        "REC-C": "accepted Recording base",
        "REC-A target/state separation": "accepted Recording revision",
        "LOG-A": "accepted Log Viewer base",
        "Implementation-Match Checklist": "implementation-match checklist routing",
        "Annotated / Callout Legend Requirement": "annotated/callout requirement",
        "Annotated Callout Legend Table": "marker-to-element legend table",
        "ACTION-002": "secondary action callout/state coverage",
        "ROW-002": "split exported row callout/state coverage",
    }
    for token, label in text_requirements.items():
        if token not in text_blob:
            failures.append(f"packet missing required {label}: {token}")
    rejected_path = packet_root / "Review Aids" / "Rejected Options And Patterns Ledger.md"
    if rejected_path.exists():
        rejected_text = rejected_path.read_text(encoding="utf-8", errors="replace")
        for token in ("oversized inner cards", "path-dominant layout", "marker-only proof", "better/closer/improved"):
            if token not in rejected_text:
                failures.append(f"Rejected Options And Patterns Ledger missing required pattern: {token}")
        for token in ("REC-B", "LOG-B", "LOG-C", "native-log status row", "local-path", "full viewer workspace"):
            if token not in rejected_text:
                failures.append(f"Rejected Options And Patterns Ledger missing rejected option/detail: {token}")
        pattern_rows = [line for line in rejected_text.splitlines() if line.startswith("| RPL-")]
        if len(pattern_rows) < 12:
            failures.append(f"Rejected Options And Patterns Ledger under-seeded: {len(pattern_rows)} rows")
    conflict_path = packet_root / "Review Aids" / "Source Truth Conflict Classification.json"
    if conflict_path.exists():
        conflict = json.loads(conflict_path.read_text(encoding="utf-8"))
        classifications = {row.get("classification") for row in conflict.get("classifications", [])}
        for classification in ("BRANCH_LOCAL_VISUAL_DECISION", "GOVERNANCE_CANDIDATE_ONLY", "NO_CONFLICT"):
            if classification not in classifications:
                failures.append(f"Source Truth Conflict Classification missing {classification}")
        decisions = " ".join(row.get("decision", "") for row in conflict.get("classifications", []))
        for token in ("LOG-C", "LOG-B", "REC-B"):
            if token not in decisions:
                failures.append(f"Source Truth Conflict Classification missing risk area: {token}")
    validation_dir = packet_root / "Review Aids" / "Validation Outputs"
    if not validation_dir.is_dir():
        failures.append("missing Validation Outputs directory")
    else:
        validation_files = list(validation_dir.glob("*.json"))
        if len(validation_files) < 10:
            failures.append(f"validation outputs incomplete: {len(validation_files)} json files")
        summary = validation_dir / "validation_outputs_summary.json"
        if not summary.is_file():
            failures.append("missing validation outputs summary")
    post_zip_policy = packet_root / "Review Aids" / "Validation Outputs.md"
    if post_zip_policy.exists() and "Final ZIP SHA policy" not in post_zip_policy.read_text(encoding="utf-8", errors="replace"):
        failures.append("Validation Outputs.md missing final ZIP SHA policy distinction")
    if zip_path is not None:
        if not zip_path.is_file():
            failures.append(f"zip missing: {zip_path}")
        else:
            with zipfile.ZipFile(zip_path, "r") as archive:
                names = {item.filename for item in archive.infolist() if not item.is_dir()}
            folder_names = {path.relative_to(packet_root).as_posix() for path in packet_root.rglob("*") if path.is_file()}
            if names != folder_names:
                failures.append("zip entries do not match packet folder files")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--zip", type=Path)
    args = parser.parse_args()

    if args.generate:
        stamp = time.strftime(TIMESTAMP_FORMAT)
        zip_path = _write_packet(stamp)
        failures = validate(PACKET_ROOT, zip_path)
        bootstrap_only = (
            "missing review aid: Validation Outputs.md",
            "missing Validation Outputs directory",
            "validation outputs incomplete:",
            "missing validation outputs summary",
            "Validation Outputs.md missing final ZIP SHA policy distinction",
        )
        material_failures = [
            failure
            for failure in failures
            if not any(failure.startswith(prefix) for prefix in bootstrap_only)
        ]
        _write_validation_outputs(stamp, zip_path, material_failures)
        # Rebuild ZIP after validation outputs are copied into the packet.
        zip_path.unlink()
        zip_path = _zip_packet(stamp)
        failures = validate(PACKET_ROOT, zip_path)
        _write_post_zip_external_manifest(stamp, zip_path, failures)
        print(json.dumps({"status": "PASS" if not failures else "FAIL", "packetRoot": str(PACKET_ROOT), "zipPath": str(zip_path), "zipSha256": _sha256(zip_path), "failures": failures}, indent=2))
        return 0 if not failures else 1

    if args.validate:
        failures = validate(PACKET_ROOT, args.zip)
        print(json.dumps({"status": "PASS" if not failures else "FAIL", "failures": failures}, indent=2))
        return 0 if not failures else 1

    parser.error("use --generate or --validate")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
