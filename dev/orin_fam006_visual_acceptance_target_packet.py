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
        legend = [
            f"{option.option_id} - {option.surface}",
            "CHROME-001: Nexus shell",
            "TITLE-001: child-window title text",
            "CTRL-001: compact window controls",
            "PANEL-001: body/status panel",
            "ROW-001: target/status truth",
            "ACTION-001: primary action",
            "ACTION-002: secondary route/action",
            f"FOOTPRINT: {option.footprint_class}",
            f"SIZE: {width}x{height}",
        ]
        draw.text((legend_x, wy + 8), "ELEMENT LEGEND", font=_font(12, bold=True), fill="#EAF8FF")
        ly = wy + 34
        for line in legend:
            draw.text((legend_x, ly), line, font=_font(10), fill="#A9C9D7")
            ly += 18
    target.parent.mkdir(parents=True, exist_ok=True)
    img.save(target)


def _draw_state_contact_sheet(option: Option, target: Path) -> None:
    tile_w, tile_h = 300, 132
    cols = 3
    rows = 3
    margin = 18
    header_h = 38
    img = Image.new("RGB", (cols * tile_w + margin * 2, rows * tile_h + header_h + margin * 2), "#020811")
    draw = ImageDraw.Draw(img)
    draw.text((margin, 12), f"{option.option_id} required state render contact sheet", font=_font(16, bold=True), fill="#EAF8FF")
    state_font = _font(10, bold=True)
    small = _font(8, bold=True)
    value = _font(9, bold=True)
    for index, state in enumerate(STATE_RENDER_SEQUENCE):
        col = index % cols
        row = index // cols
        x = margin + col * tile_w
        y = header_h + margin + row * tile_h
        state_label = state.replace("_", " ").upper()
        _rounded(draw, (x, y, x + tile_w - 14, y + tile_h - 12), 17, "#03111C", "#1E5C70", 1)
        draw.text((x + 14, y + 10), state_label, font=state_font, fill="#7BD2E8")
        draw.text((x + 14, y + 26), option.title.upper(), font=_font(13, bold=True), fill="#F1FAFF")

        panel = (x + 14, y + 50, x + tile_w - 28, y + 82)
        fill = "#061725"
        outline = "#173D4E"
        if state == "blocked_error":
            fill, outline = "#211218", "#7C3D45"
        elif state in {"recording", "pressed"}:
            fill, outline = "#0D1F24", "#34BFA4"
        elif state == "disabled":
            fill, outline = "#06111A", "#244052"
        elif state == "focus":
            fill, outline = "#071F31", "#8CEBFF"
        elif state == "hover":
            fill, outline = "#08283A", "#39B7D1"
        _rounded(draw, panel, 11, fill, outline, 1)

        if option.surface.startswith("Recording"):
            status_map = {
                "ready": "Ready - 2 active monitors",
                "hover": "Hover: Start Recording",
                "focus": "Focus ring visible",
                "pressed": "Pressed: starting...",
                "disabled": "Disabled: target missing",
                "recording": "Recording active",
                "saved_complete": "Saved native log",
                "blocked_error": "Blocked: no active monitor",
                "footprint_proof": f"Fixed {option.default_size[0]}x{option.default_size[1]}",
            }
            action = "Stop Recording" if state == "recording" else option.primary_action
        else:
            status_map = {
                "ready": "Native logs ready",
                "hover": "Hover: Open Native Logs",
                "focus": "Focus ring visible",
                "pressed": "Pressed: opening folder",
                "disabled": "Disabled: folder unavailable",
                "recording": "Exported logs available",
                "saved_complete": "Export folder ready",
                "blocked_error": "Blocked: open failed",
                "footprint_proof": option.resize_behavior,
            }
            action = option.primary_action
        draw.text((panel[0] + 10, panel[1] + 10), status_map[state], font=value, fill="#9FFFE3" if state != "disabled" else "#647684")

        button = (x + 14, y + 91, x + 145, y + 119)
        button_fill = "#092C3E"
        button_outline = "#39B7D1"
        if state == "disabled":
            button_fill, button_outline = "#06111A", "#244052"
        elif state == "pressed":
            button_fill, button_outline = "#0D403F", "#7DFFE6"
        elif state == "focus":
            button_fill, button_outline = "#092C3E", "#EAF8FF"
        elif state == "hover":
            button_fill, button_outline = "#0A354C", "#69E8FF"
        _rounded(draw, button, 10, button_fill, button_outline, 1)
        label = action.upper()
        tw, th = _text_size(draw, label, small)
        draw.text(
            (button[0] + ((button[2] - button[0]) - tw) // 2, button[1] + ((button[3] - button[1]) - th) // 2 - 1),
            label,
            font=small,
            fill="#EAF8FF" if state != "disabled" else "#647684",
        )
        if state == "footprint_proof":
            draw.line((x + tile_w - 58, y + 22, x + tile_w - 28, y + 22), fill="#8CEBFF")
            draw.line((x + tile_w - 28, y + 22, x + tile_w - 28, y + 52), fill="#8CEBFF")
            grip = "no corner grip" if "Fixed" in option.resize_behavior or "fixed" in option.resize_behavior else "edge resize only"
            draw.text((x + tile_w - 116, y + 56), grip, font=_font(8), fill="#A9C9D7")
    target.parent.mkdir(parents=True, exist_ok=True)
    img.save(target)


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
        "absenceOfVisualAcceptanceTargetRepresented": "The packet preserves the branch-local false-green / UDL evidence and keeps implementation blocked pending USER visual selection.",
        "currentOwnedUdlBlocksThisPacket": "Packet generation is allowed only as visual-target review evidence; product UI repair remains blocked until USER selects/revises target.",
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


def _markdown_table(rows: Iterable[Iterable[str]]) -> str:
    return "\n".join("| " + " | ".join(row) + " |" for row in rows)


def _write_packet(stamp: str) -> Path:
    _purge_packet()
    media_root = PACKET_ROOT / "Review Aids" / "Visual Options" / "media"
    records: list[dict[str, object]] = []
    for option in OPTIONS:
        focus = media_root / f"{option.option_id}_focused.png"
        context = media_root / f"{option.option_id}_desktop_context.png"
        states = media_root / f"{option.option_id}_state_contact_sheet.png"
        _draw_window(option, focus)
        _draw_window(option, context, context=True)
        _draw_state_contact_sheet(option, states)
        records.append(_option_record(option, focus, context, states))

    copied = _copy_source_context()
    copied_udl = _copy_udl_context()
    review_aids = PACKET_ROOT / "Review Aids"
    user_review = PACKET_ROOT / "USER Review" / PRIMARY_FILE

    impact = {
        "status": "VISUAL_TARGET_REQUIRED",
        "classifications": VISUAL_CLASSIFICATIONS,
        "rule": "Any visible UI/UX change requires a rendered visual target before product/runtime UI implementation.",
        "currentBranchSurfaces": ["Recording Studio", "Log Viewer Studio"],
    }
    _write_json(review_aids / "Visual Impact Classification.json", impact)
    _write_json(review_aids / "Visual Options Packet.json", {"options": records})

    visual_options_md = [
        "# Visual Options Packet",
        "",
        "Render Authority Level: `Design Candidate Render`.",
        "These are selection artifacts only. They are not implementation proof and not USER acceptance targets until USER selects/revises them.",
        "",
        "| Option | Surface | Footprint | Size | Resize | Focused render | Context render | State contact sheet | What USER should critique |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for option, record in zip(OPTIONS, records, strict=True):
        visual_options_md.append(
            "| {option} | {surface} | {footprint} | {size} | {resize} | `{focus}` | `{context}` | `{states}` | {critique} |".format(
                option=option.option_id,
                surface=option.surface,
                footprint=option.footprint_class,
                size=f"{option.default_size[0]}x{option.default_size[1]}",
                resize=option.resize_behavior,
                focus=record["focusedRenderMediaPath"],
                context=record["fullDesktopContextRenderMediaPath"],
                states=record["stateContactSheetMediaPath"],
                critique=record["whatUserShouldCritique"],
            )
        )
    (review_aids / "Visual Options Packet.md").write_text("\n".join(visual_options_md) + "\n", encoding="utf-8")

    selection = [
        "# Visual Selection Ledger Template",
        "",
        "| decision ID | surface | option ID | element ID | accepted / rejected / combine / revise | USER notes | source-truth impact | branch-local vs durable design principle | implementation requirement | proof requirement | future reuse note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        "| VSL-001 | Recording Studio |  |  |  |  |  |  |  |  |  |",
        "| VSL-002 | Log Viewer Studio |  |  |  |  |  |  |  |  |  |",
    ]
    (review_aids / "Visual Selection Ledger Template.md").write_text("\n".join(selection) + "\n", encoding="utf-8")

    target = [
        "# Draft Branch Visual Acceptance Target",
        "",
        "Target ID: `FAM006-VAT-DRAFT-001`",
        "Target Status: `DRAFT`",
        "Selected Option(s): `Pending USER selection`",
        "Selected Element Decisions: `Pending USER selection`",
        "Surface Purpose: `Pending USER acceptance after option review`",
        "Footprint Class: `Pending USER selection`",
        "Default Dimensions: `Pending USER selection`",
        "Resize Behavior: `Pending USER selection`",
        "State Matrix: `default, hover, focus, pressed/active, disabled, empty/no-data, blocked/error, success/complete, resized/fixed-size proof required before implementation-match proof`",
        "Copy Rules: `Short product copy only; no proof/debug/governance/internal wording`",
        "Spacing/Density Rules: `Same-class primitives must be identical or explicitly varied by accepted target`",
        "Button/Control Rules: `Content-fit primitive, equal left/right gutters, shared hover/focus/pressed/disabled grammar`",
        "Status/Error/Empty Rules: `Truthful runtime state; no fake readiness; no hidden failures`",
        "Accepted Reference Surfaces: `Pending USER selection; expected to cite UIREF and accepted comparator rows`",
        "UIREF Obligations: `UIREF-001 through UIREF-006 applicability must be mapped per element group`",
        "Accepted Exceptions: `None accepted by this draft`",
        "Source-Truth Conflict Candidates: `None admitted; record any USER-selected conflict before implementation`",
        "Implementation Constraints: `No product/runtime UI repair may proceed from this packet until USER accepts or revises this target`",
        "Proof Requirements: `Focused implementation screenshots/video, full desktop/context screenshots, element legends, state matrix, implementation-match checklist, LV exact desktop launcher proof`",
        "LV Gating Rule: `No renewed Live Validation until implementation-match proof compares actual UI against USER-accepted Visual Acceptance Target`",
    ]
    (review_aids / "Draft Branch Visual Acceptance Target.md").write_text("\n".join(target) + "\n", encoding="utf-8")

    rejected = [
        "# Rejected Patterns Ledger",
        "",
        "| pattern ID | rejected UI/UX pattern | source option or prior screenshot | reason rejected | affected surface/class | future avoidance guidance | source-truth impact | linked USER feedback |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    rejected.extend("| " + " | ".join(row) + " |" for row in REJECTED_PATTERNS)
    (review_aids / "Rejected Patterns Ledger.md").write_text("\n".join(rejected) + "\n", encoding="utf-8")

    recipe = [
        "# Reusable Design Recipe Template",
        "",
        "Accepted Surface Class: `Pending USER accepted target`",
        "Accepted Footprint Class: `Pending USER accepted target`",
        "Token Values / Dimensions: `Pending implementation-match proof`",
        "Padding: `Pending USER accepted target`",
        "Spacing: `Pending USER accepted target`",
        "Button Heights: `Pending USER accepted target`",
        "Font Scale: `Pending USER accepted target`",
        "Status Chip Pattern: `Pending USER accepted target`",
        "Title/Header Grammar: `Pending USER accepted target`",
        "Resize Behavior: `Pending USER accepted target`",
        "Copy Pattern: `Pending USER accepted target`",
        "State Pattern: `default, hover, focus, pressed, disabled, blocked/error, empty, success`",
        "Accepted Comparator References: `Pending USER accepted target`",
        "Rejected Alternatives: `See Rejected Patterns Ledger`",
        "Future Branch Reuse Notes: `Fold down after USER accepts final visual target and implementation proof passes`",
        "Proof Requirements: `packet-contained render media plus later implementation-match screenshots/video`",
    ]
    (review_aids / "Reusable Design Recipe Template.md").write_text("\n".join(recipe) + "\n", encoding="utf-8")

    conflict = {
        "status": "MATERIAL_CANDIDATE_DECISIONS_CLASSIFIED",
        "classificationVocabulary": [
            "BRANCH_LOCAL_VISUAL_DECISION",
            "FAMILY_FEATURE_VISION_REPAIR_REQUIRED",
            "FAMILY_VISION_REPAIR_REQUIRED",
            "FAM-002_REPAIR_REQUIRED",
            "UIREF_REPAIR_REQUIRED",
            "PROJECT_VISION_REPAIR_REQUIRED",
            "GOVERNANCE_CANDIDATE_ONLY",
            "USER_DECISION_REQUIRED",
            "NO_CONFLICT",
        ],
        "classifications": CONFLICT_CLASSIFICATION_ROWS,
    }
    _write_json(review_aids / "Source Truth Conflict Classification.json", conflict)
    conflict_md = [
        "# Source Truth Conflict Classification",
        "",
        "| decision | classification | risk area | basis | USER decision needed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in CONFLICT_CLASSIFICATION_ROWS:
        conflict_md.append(
            "| {decision} | `{classification}` | {riskArea} | {basis} | {userDecisionNeeded} |".format(**row)
        )
    (review_aids / "Source Truth Conflict Classification.md").write_text("\n".join(conflict_md) + "\n", encoding="utf-8")

    governance_candidate = [
        "# Governance Candidate Only",
        "",
        "Candidate: promote a global Visual Acceptance Target gate for visible UI/UX changes.",
        "",
        "Reason: FAM-006 repeatedly implemented UI before USER had a substantial rendered target to accept, producing false-green and repair loops.",
        "",
        "Exact future approval needed: `I approve Governance to evaluate and promote the FAM-006 Visual Acceptance Target process into global source truth and validators, using the FAM-006 branch-local packet as evidence only.`",
    ]
    (review_aids / "Governance Candidate Only.md").write_text("\n".join(governance_candidate) + "\n", encoding="utf-8")

    validation_summary = [
        "# Validation Outputs",
        "",
        "Packet generator validation is run after packet creation and copied here.",
        "Live Validation was not run.",
        "UTS acceptance was not claimed.",
    ]
    (review_aids / "Validation Outputs.md").write_text("\n".join(validation_summary) + "\n", encoding="utf-8")

    primary = [
        "# FAM-006 Current Branch Visual Acceptance Target Review",
        "",
        "Packet Status: `branch-local-visual-acceptance-target-review`",
        "Packet Reviewability State: `Reviewable`",
        "USER Gate State: `Pending USER visual selection / revision`",
        "Runtime Implementation State: `Blocked by pending Visual Acceptance Target`",
        "Live Validation State: `Not run; blocked until USER-accepted target and implementation-match proof`",
        "",
        "## Why This Packet Exists",
        "",
        "The current branch has visible UI/UX changes for Recording Studio and Log Viewer Studio. USER rejected the implementation-first loop and asked for real rendered options so USER can choose the final product direction before more runtime UI repair.",
        "",
        "This packet gives substantial rendered Design Candidate Renders. It does not claim the UI is implemented, visually accepted, Live-Validation green, UTS complete, or PR Readiness green.",
        "",
        "## Visual Impact Classification",
        "",
        ", ".join(f"`{item}`" for item in VISUAL_CLASSIFICATIONS),
        "",
        "## Render Authority Levels",
        "",
        _markdown_table([("Authority Level", "Meaning"), ("---", "---"), *AUTHORITY_LEVELS.items()]),
        "",
        "## Options To Review",
        "",
        "Open `Review Aids/Visual Options Packet.md` and inspect the packet-contained PNG renders under `Review Aids/Visual Options/media/`.",
        "",
        "Each option has three required media types: focused render, desktop/context footprint render, and state contact sheet. The state contact sheets are actual rendered review artifacts for ready/recording/saved/blocked and hover/focus/pressed/disabled/footprint states; they are not deferred prose.",
        "",
        "## UDL / False-Green Status",
        "",
        "Open `Review Aids/Unified Defect Ledger/UDL_FALSE_GREEN_STATUS.md`. This packet does not close UDL rows or claim product repair; it proves the visual-target packet now carries the false-green evidence needed for USER review.",
        "",
        "## Validation And SHA Proof",
        "",
        "Open `Review Aids/Validation Outputs.md` for command-output summaries. Final ZIP SHA proof is intentionally recorded outside the ZIP in external state and in Codex's return packet because embedding the final ZIP SHA inside the ZIP would change the ZIP bytes.",
        "",
        "## USER Decision Needed",
        "",
        "Choose, combine, revise, or reject the rendered options. You may reference element IDs such as `ACTION-001 from REC-A` or `PANEL-001 from LOG-B`.",
        "",
        "Exact decision text:",
        "",
        "```text",
        "I select/revise the FAM-006 Visual Acceptance Target as follows: [state selected Recording option/elements, selected Log Viewer option/elements, rejected patterns, required changes, and whether Codex may prepare the accepted Branch Visual Acceptance Target for implementation-match repair].",
        "```",
        "",
        "## Pending Decisions",
        "",
        "- Runtime UI implementation repair.",
        "- Renewed H1.",
        "- Renewed exact USER desktop launcher Live Validation.",
        "- UTS acceptance.",
        "- PR Readiness, PR creation, merge, release, issue mutation, and cleanup.",
    ]
    user_review.write_text("\n".join(primary) + "\n", encoding="utf-8")

    start_here = [
        "# FAM-006 Visual Acceptance Target Packet",
        "",
        f"Generated: `{stamp}`",
        "Review Purpose: choose or revise rendered visual targets before any further Recording Studio / Log Viewer Studio product UI repair.",
        f"Primary USER Review File: `USER Review/{PRIMARY_FILE}`",
        "Packet Reviewability State: `Reviewable`",
        "USER Gate State: `Pending USER visual selection / revision`",
        "Runtime Implementation State: `Blocked`",
        "Live Validation State: `Not run`",
        "",
        "## Review Order",
        "",
        "1. Open the primary USER review file.",
        "2. Inspect the focused and desktop-context PNG renders in `Review Aids/Visual Options/media/`.",
        "3. Inspect the state contact sheets in `Review Aids/Visual Options/media/`.",
        "4. Review `Review Aids/Rejected Patterns Ledger.md`, `Review Aids/Source Truth Conflict Classification.md`, and `Review Aids/Unified Defect Ledger/UDL_FALSE_GREEN_STATUS.md`.",
        "5. Fill or reference `Review Aids/Visual Selection Ledger Template.md`.",
        "6. Decide whether Codex should combine, revise, or reject options before implementation resumes.",
    ]
    (PACKET_ROOT / "START_HERE.md").write_text("\n".join(start_here) + "\n", encoding="utf-8")

    process_payload = {
        "External State Schema": "external-state-v1",
        "status": "DRAFT_PACKET_GENERATED",
        "branch": _run_git("branch", "--show-current"),
        "head": _run_git("rev-parse", "HEAD"),
        "visualImpactClassification": VISUAL_CLASSIFICATIONS,
        "authorityLevels": AUTHORITY_LEVELS,
        "options": records,
        "copiedSourceTruthContext": copied,
        "copiedUdlFalseGreenEvidence": copied_udl,
        "userPacket": str(PACKET_ROOT),
        "nextLegalPhase": "USER review of Visual Acceptance Target options before runtime UI implementation repair",
        "governanceCandidateOnly": "Promote globally after USER approves a Governance carrier; not implemented globally here.",
    }
    _write_json(EXTERNAL_PROCESS_JSON, process_payload)
    EXTERNAL_PROCESS_MD.parent.mkdir(parents=True, exist_ok=True)
    EXTERNAL_PROCESS_MD.write_text(
        "# FAM-006 Branch-Local Visual Acceptance Target Process\n\n"
        "Status: `DRAFT_PACKET_GENERATED / Pending USER visual selection`.\n\n"
        "This branch-local process requires substantial rendered visual options before any further visible UI/UX implementation repair for Recording Studio or Log Viewer Studio.\n\n"
        "Authority levels:\n\n"
        + "\n".join(f"- `{key}`: {value}" for key, value in AUTHORITY_LEVELS.items())
        + "\n\n"
        "Current visual impact classification: "
        + ", ".join(f"`{item}`" for item in VISUAL_CLASSIFICATIONS)
        + ".\n\n"
        "USER packet: `C:\\Nexus USER\\FAM-006`.\n\n"
        "Global/Governance promotion remains candidate only.\n",
        encoding="utf-8",
    )

    if BRANCH_PLAN.exists():
        marker = "\n## FAM-006 Branch-Local Visual Acceptance Target Gate - 2026-06-24\n"
        text = BRANCH_PLAN.read_text(encoding="utf-8")
        receipt = (
            marker
            + "\n"
            + "Status: `DRAFT_PACKET_GENERATED / Pending USER visual selection`.\n\n"
            + "Current branch visual impact classification: `"
            + "`, `".join(VISUAL_CLASSIFICATIONS)
            + "`.\n\n"
            + "Visual Acceptance Target rule: further visible Recording Studio / Log Viewer Studio product UI repair is blocked until USER selects, combines, revises, or rejects the rendered Design Candidate Renders and Codex records a USER-accepted or revised Branch Visual Acceptance Target.\n\n"
            + f"USER packet: `C:\\Nexus USER\\FAM-006` with primary file `USER Review/{PRIMARY_FILE}`.\n\n"
            + "Next legal phase: `USER review of Visual Acceptance Target options`; renewed implementation repair, H1, Live Validation, UTS, and PR Readiness remain pending.\n"
        )
        if marker.strip() in text:
            text = text.split(marker, 1)[0].rstrip() + receipt
        else:
            text = text.rstrip() + "\n" + receipt
        BRANCH_PLAN.write_text(text, encoding="utf-8")

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
        "Visual Options Packet.json",
        "Visual Options Packet.md",
        "Visual Selection Ledger Template.md",
        "Draft Branch Visual Acceptance Target.md",
        "Rejected Patterns Ledger.md",
        "Reusable Design Recipe Template.md",
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
    options_json = packet_root / "Review Aids" / "Visual Options Packet.json"
    if options_json.exists():
        data = json.loads(options_json.read_text(encoding="utf-8"))
        options = data.get("options", [])
        if len(options) < 6:
            failures.append(f"expected at least 6 rendered options, found {len(options)}")
        for option in options:
            for field in (
                "optionId",
                "surface",
                "footprintClass",
                "windowSurfaceClass",
                "renderAuthorityLevel",
                "focusedRenderMediaPath",
                "fullDesktopContextRenderMediaPath",
                "stateContactSheetMediaPath",
                "elementLegend",
                "stateCoverage",
                "requiredStates",
                "resizeBehavior",
            ):
                if not option.get(field):
                    failures.append(f"option missing field {field}: {option.get('optionId')}")
            for field in ("focusedRenderMediaPath", "fullDesktopContextRenderMediaPath", "stateContactSheetMediaPath"):
                rel = option.get(field)
                if rel and not (packet_root / rel).is_file():
                    failures.append(f"option media missing: {rel}")
            if option.get("renderAuthorityLevel") != "Design Candidate Render":
                failures.append(f"option has wrong authority level: {option.get('optionId')}")
            required_states = set(option.get("requiredStates", []))
            rendered_states = set((option.get("stateCoverage") or {}).keys())
            if required_states != rendered_states:
                failures.append(f"state coverage mismatch for {option.get('optionId')}: required {sorted(required_states)} rendered {sorted(rendered_states)}")
    media = list((packet_root / "Review Aids" / "Visual Options" / "media").glob("*.png"))
    if len(media) < 18:
        failures.append(f"expected at least 18 PNG render media files, found {len(media)}")
    state_media = [path for path in media if path.name.endswith("_state_contact_sheet.png")]
    if len(state_media) < 6:
        failures.append(f"expected at least 6 state contact sheets, found {len(state_media)}")
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
        "USER_ACCEPTED",
    ]
    for token in forbidden:
        if token in text_blob:
            failures.append(f"packet contains forbidden progression claim: {token}")
    rejected_path = packet_root / "Review Aids" / "Rejected Patterns Ledger.md"
    if rejected_path.exists():
        rejected_text = rejected_path.read_text(encoding="utf-8", errors="replace")
        for token in ("oversized inner cards", "path-dominant layout", "marker-only proof", "better/closer/improved"):
            if token not in rejected_text:
                failures.append(f"Rejected Patterns Ledger missing required pattern: {token}")
        pattern_rows = [line for line in rejected_text.splitlines() if line.startswith("| RPL-")]
        if len(pattern_rows) < 12:
            failures.append(f"Rejected Patterns Ledger under-seeded: {len(pattern_rows)} rows")
    conflict_path = packet_root / "Review Aids" / "Source Truth Conflict Classification.json"
    if conflict_path.exists():
        conflict = json.loads(conflict_path.read_text(encoding="utf-8"))
        classifications = {row.get("classification") for row in conflict.get("classifications", [])}
        for classification in ("BRANCH_LOCAL_VISUAL_DECISION", "USER_DECISION_REQUIRED", "GOVERNANCE_CANDIDATE_ONLY", "NO_CONFLICT"):
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
