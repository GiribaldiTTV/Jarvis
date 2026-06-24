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
    labels = ["-", "x"] if ctrl_w == 66 else ["-", "□", "x"]
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


def _copy_source_context() -> list[str]:
    copied: list[str] = []
    context = PACKET_ROOT / "Source Truth Context"
    for rel in SOURCE_TRUTH_FILES:
        source = ROOT / rel
        if not source.exists():
            continue
        dest = context / rel.replace("/", "__")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        copied.append(rel)
    if BRANCH_PLAN.exists():
        shutil.copy2(BRANCH_PLAN, context / "external_branch_plan.md")
        copied.append(str(BRANCH_PLAN))
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


def _option_record(option: Option, focus: Path, context: Path) -> dict[str, object]:
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
        "elementLegend": ["CHROME-001", "TITLE-001", "CTRL-001", "PANEL-001", "ROW-001", "ACTION-001", "ACTION-002", "FOOTER-001"],
        "stateCoverage": {
            "default": "Rendered",
            "hover": "Required before implementation-match proof; visual target packet states expected behavior.",
            "focus": "Required before implementation-match proof; visual target packet states expected behavior.",
            "pressedActive": "Required before implementation-match proof; visual target packet states expected behavior.",
            "disabled": "Required before implementation-match proof; visual target packet states expected behavior.",
            "emptyNoData": "Represented by native-log/export empty status where applicable.",
            "blockedError": "Must use same footprint and action hierarchy with explicit blocked reason.",
            "successComplete": "Must preserve same shell and row/action grammar.",
            "resizedOrFixedSizeProof": option.resize_behavior,
        },
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
        _draw_window(option, focus)
        _draw_window(option, context, context=True)
        records.append(_option_record(option, focus, context))

    copied = _copy_source_context()
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
        "| Option | Surface | Footprint | Size | Resize | Focused render | Context render |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for option, record in zip(OPTIONS, records, strict=True):
        visual_options_md.append(
            "| {option} | {surface} | {footprint} | {size} | {resize} | `{focus}` | `{context}` |".format(
                option=option.option_id,
                surface=option.surface,
                footprint=option.footprint_class,
                size=f"{option.default_size[0]}x{option.default_size[1]}",
                resize=option.resize_behavior,
                focus=record["focusedRenderMediaPath"],
                context=record["fullDesktopContextRenderMediaPath"],
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
        "| RPL-001 | oversized inner cards | Prior Recording/Log Viewer repair screenshots | Made compact studio windows feel huge and non-intuitive | Unique child feature-studio | Start with footprint and purpose before body panels | Branch-local; Governance candidate for future branches | USER said the windows felt big and huge |",
        "| RPL-002 | path-dominant layout | Prior Log Viewer shells | Paths overpowered the simple doorway purpose | Log Viewer Studio | Use action-first doorway shell unless USER selects path-aware option | Branch-local | USER suggested two side-by-side buttons may be enough |",
        "| RPL-003 | debug/status-table feel | Prior Recording Studio row stacks | Read like proof tooling rather than product | Recording Studio | Keep status truth compact and action-led | Branch-local | USER rejected table-like/cramped shells |",
        "| RPL-004 | implementation first, USER catches mismatch later | Repeated repair loop | Caused multi-day visual rework | All visible UI changes | Require Design Candidate Render and Visual Acceptance Target before product UI implementation | Governance Candidate Only | USER requested first-time green process |",
    ]
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
        "status": "NO_CONFLICT_FOR_PACKET_GENERATION",
        "classifications": [
            {
                "decision": "Visual target process before implementation",
                "classification": "BRANCH_LOCAL_VISUAL_DECISION",
                "governanceCandidate": "Promote this pattern globally after USER accepts and branch proves it reduces false greens.",
            },
            {
                "decision": "Recording Studio compact-controller footprint",
                "classification": "USER_DECISION_REQUIRED",
                "governanceCandidate": "",
            },
            {
                "decision": "Log Viewer fixed-size versus edge-resizable doorway shell",
                "classification": "USER_DECISION_REQUIRED",
                "governanceCandidate": "",
            },
        ],
    }
    _write_json(review_aids / "Source Truth Conflict Classification.json", conflict)

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
        "Open `Review Aids/Visual Options Packet.md` and inspect the actual PNG renders under `Review Aids/Visual Options/media/`.",
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
        "3. Fill or reference `Review Aids/Visual Selection Ledger Template.md`.",
        "4. Decide whether Codex should combine, revise, or reject options before implementation resumes.",
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
        "Governance Candidate Only.md",
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
                "elementLegend",
                "stateCoverage",
                "resizeBehavior",
            ):
                if not option.get(field):
                    failures.append(f"option missing field {field}: {option.get('optionId')}")
            for field in ("focusedRenderMediaPath", "fullDesktopContextRenderMediaPath"):
                rel = option.get(field)
                if rel and not (packet_root / rel).is_file():
                    failures.append(f"option media missing: {rel}")
            if option.get("renderAuthorityLevel") != "Design Candidate Render":
                failures.append(f"option has wrong authority level: {option.get('optionId')}")
    media = list((packet_root / "Review Aids" / "Visual Options" / "media").glob("*.png"))
    if len(media) < 12:
        failures.append(f"expected at least 12 PNG render media files, found {len(media)}")
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
        validation = {
            "status": "PASS" if not failures else "FAIL",
            "packetRoot": str(PACKET_ROOT),
            "zipPath": str(zip_path),
            "zipSha256": _sha256(zip_path) if zip_path.exists() else "",
            "failures": failures,
        }
        _write_json(PACKET_ROOT / "Review Aids" / "Validation Outputs" / "visual_acceptance_target_packet_validation.json", validation)
        (PACKET_ROOT / "Review Aids" / "Validation Outputs.md").write_text(
            "# Validation Outputs\n\n"
            f"Visual Acceptance Target Packet Validation: `{validation['status']}`\n\n"
            f"ZIP: `{zip_path}`\n\n"
            f"ZIP SHA256: `{validation['zipSha256']}`\n\n"
            + ("\n".join(f"- {failure}" for failure in failures) if failures else "No packet validation failures.\n"),
            encoding="utf-8",
        )
        # Rebuild ZIP after validation output is copied into the packet.
        zip_path.unlink()
        zip_path = _zip_packet(stamp)
        failures = validate(PACKET_ROOT, zip_path)
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
