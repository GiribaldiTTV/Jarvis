"""Generate and validate the FAM-006 full-desktop false-green review packet.

This is a branch-local process/proof helper. It does not repair runtime UI and
does not clear H1, Live Validation, UTS, PR Readiness, or release gates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


WORKTREE = Path("C:/Nexus Worktrees/FAM-006")
USER_ROOT = Path("C:/Nexus USER")
PACKET_ROOT = USER_ROOT / "FAM-006"
EXTERNAL_ROOT = Path(
    "C:/Nexus Governance State/branches/feature_fam_006_dashboard_recording_start_stop_local_file"
)
KNOWN_BAD_ROOT = EXTERNAL_ROOT / "false_accept_regression_corpus"
REJECTED_PACKET = USER_ROOT / "FAM-006-20260624-121535.zip"
REJECTED_SHA256 = "1ED2108CD4EC129476303C0E267D5B0F2D8A573770675B5BD57157534B65A6D3"
REJECTED_OPTIONS_PACKET = USER_ROOT / "FAM-006-20260624-130151.zip"
REJECTED_OPTIONS_SHA256 = "0929BF53FCAD8F5BC3751BF51CC053351C1103C97D6C8776C288B870FE9BE73F"
PROOF_ROOT = Path(
    "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/"
    "fam_006_pre_live_visual_conformance/20260624_121443_feature_studio_visual_fail_repair"
)
AI_CONTROL_SCREENSHOT = Path(
    "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/AI Control Center- Accepted.png"
)

PRIMARY_REVIEW = "USER Review/FULL_DESKTOP_FALSE_GREEN_REVIEW.md"
STATUS = "full-desktop-visual-false-green-review"


def _run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=WORKTREE, text=True).strip()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _copy_file(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst.as_posix()


def _purge_user_hub() -> None:
    if PACKET_ROOT.exists():
        shutil.rmtree(PACKET_ROOT)
    for path in USER_ROOT.glob("FAM-006*.zip"):
        path.unlink()
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)


def _image_thumb(src: Path, max_size: tuple[int, int]) -> Image.Image:
    img = Image.open(src).convert("RGB")
    img.thumbnail(max_size)
    return img


def _font(size: int = 16) -> ImageFont.ImageFont:
    for candidate in (
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def _label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int = 18) -> None:
    draw.text(xy, text, fill=(210, 236, 245), font=_font(size))


def _wrap_text(text: str, width: int, font: ImageFont.ImageFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    probe = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(probe)
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_button(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str) -> None:
    draw.rounded_rectangle(box, radius=17, fill=(8, 45, 66), outline=(73, 178, 203), width=2)
    draw.rounded_rectangle(
        (box[0] + 3, box[1] + 3, box[2] - 3, box[3] - 3),
        radius=14,
        outline=(18, 72, 95),
        width=1,
    )
    text_font = _font(15)
    bbox = draw.textbbox((0, 0), label.upper(), font=text_font)
    tx = box[0] + (box[2] - box[0] - (bbox[2] - bbox[0])) // 2
    ty = box[1] + (box[3] - box[1] - (bbox[3] - bbox[1])) // 2 - 1
    draw.text((tx, ty), label.upper(), fill=(224, 244, 249), font=text_font)


def _draw_truth_row(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    width: int,
    label: str,
    value: str,
    *,
    action: str | None = None,
) -> int:
    row_h = 38 if action is None else 46
    draw.line((x, y, x + width, y), fill=(74, 170, 191), width=2)
    draw.rectangle((x, y + 1, x + width, y + 11), fill=(7, 36, 52))
    draw.text((x + 14, y + 12), label.upper(), fill=(111, 194, 211), font=_font(13))
    value_x = x + 150
    value_w = width - 170
    if action:
        value_w -= 150
    draw.text((value_x, y + 12), value, fill=(158, 246, 218), font=_font(13))
    if action:
        _draw_button(draw, (x + width - 136, y + 7, x + width - 14, y + 39), action)
    return y + row_h


def _draw_window_shell(
    size: tuple[int, int],
    title: str,
    subtitle: str,
    *,
    stronger: bool = False,
) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", size, (3, 11, 17))
    draw = ImageDraw.Draw(img)
    w, h = size
    draw.rounded_rectangle((1, 1, w - 2, h - 2), radius=24, fill=(5, 23, 35), outline=(37, 139, 160), width=2)
    draw.rounded_rectangle((18, 18, w - 18, 76), radius=20, fill=(5, 26, 41), outline=(24, 82, 104), width=1)
    if stronger:
        draw.rounded_rectangle((22, 22, w - 22, 72), radius=17, outline=(47, 151, 169), width=1)
    draw.text((36, 30), subtitle.upper(), fill=(118, 207, 223), font=_font(11))
    draw.text((36, 45), title.upper(), fill=(235, 247, 250), font=_font(22))
    _draw_button(draw, (w - 112, 28, w - 34, 62), "Close")
    return img, draw


def _render_recording_option(option_id: str, media_dir: Path) -> str:
    specs = {
        "A1": {
            "title": "A1 Minimal Shell",
            "subtitle": "Recording Studio",
            "rows": [("Target", "Default Overlay Profile"), ("State", "Ready - 2 active monitors")],
            "note": "Smallest footprint; row density improved but container inheritance stays light.",
            "size": (520, 300),
            "group": False,
            "stronger": False,
        },
        "A2": {
            "title": "A2 Subtle Contained Row Group",
            "subtitle": "Recording Studio",
            "rows": [("Target", "Default Overlay Profile / 2 active monitors"), ("State", "Ready")],
            "note": "Recommended: AI/HUD row-container rhythm without becoming a dashboard card.",
            "size": (540, 310),
            "group": True,
            "stronger": False,
        },
        "A3": {
            "title": "A3 Stronger Parent-Family Card Grammar",
            "subtitle": "Recording Studio",
            "rows": [("Target", "Default Overlay Profile / 2 active monitors"), ("State", "Ready"), ("Session", "No recording active")],
            "note": "Most inherited card feel; largest footprint and highest fake-dashboard risk.",
            "size": (570, 344),
            "group": True,
            "stronger": True,
        },
    }
    spec = specs[option_id]
    img, draw = _draw_window_shell(spec["size"], spec["subtitle"], spec["title"], stronger=spec["stronger"])
    x, y, w = 28, 96, spec["size"][0] - 56
    if spec["group"]:
        draw.rounded_rectangle((x - 8, y - 10, x + w + 8, y + 48 * len(spec["rows"]) + 14), radius=18, fill=(4, 27, 38), outline=(22, 82, 101), width=1)
    for label, value in spec["rows"]:
        y = _draw_truth_row(draw, x, y, w, label, value)
    note_font = _font(12)
    note_y = y + 10
    for line in _wrap_text(spec["note"], w, note_font)[:2]:
        draw.text((x, note_y), line, fill=(178, 210, 221), font=note_font)
        note_y += 17
    button_y = spec["size"][1] - 58
    _draw_button(draw, (x, button_y, x + 156, button_y + 40), "Start Recording")
    _draw_button(draw, (x + 172, button_y, x + 342, button_y + 40), "Log Viewer Studio")
    out = media_dir / f"{option_id.lower()}_nested_card_inheritance.png"
    img.save(out)
    return out.as_posix()


def _render_log_option(option_id: str, media_dir: Path) -> str:
    specs = {
        "C1": {
            "title": "C1 Tight Vertical Doorway",
            "rows": [("Native Logs", "Recordings folder"), ("Exported Logs", "Exported Logs folder")],
            "mode": "stacked",
            "note": "Tighter vertical stack; actions stay close to truth rows.",
            "size": (560, 292),
        },
        "C2": {
            "title": "C2 Inline Row Actions",
            "rows": [("Native Logs", "Recordings folder", "Open"), ("Exported Logs", "Exported Logs folder", "Open")],
            "mode": "inline",
            "note": "Recommended: truth and action are tied on each row; less dead space.",
            "size": (660, 270),
        },
        "C3": {
            "title": "C3 Compact Footer Actions",
            "rows": [("Native Logs", "Recordings folder"), ("Exported Logs", "Exported Logs folder")],
            "mode": "footer",
            "note": "Simplest action rail; must avoid disconnected dead space.",
            "size": (600, 288),
        },
    }
    spec = specs[option_id]
    img, draw = _draw_window_shell(spec["size"], "Log Viewer Studio", spec["title"])
    x, y, w = 28, 96, spec["size"][0] - 56
    if spec["mode"] == "inline":
        for label, value, action in spec["rows"]:
            y = _draw_truth_row(draw, x, y, w, label, value, action=action)
    else:
        for label, value in spec["rows"]:
            y = _draw_truth_row(draw, x, y, w, label, value)
    note_font = _font(12)
    note_y = y + 8
    for line in _wrap_text(spec["note"], w, note_font)[:2]:
        draw.text((x, note_y), line, fill=(178, 210, 221), font=note_font)
        note_y += 17
    if spec["mode"] in {"stacked", "footer"}:
        button_y = spec["size"][1] - 58
        _draw_button(draw, (x, button_y, x + 166, button_y + 40), "Open Native Logs")
        _draw_button(draw, (x + 182, button_y, x + 366, button_y + 40), "Open Exported Logs")
    out = media_dir / f"{option_id.lower()}_log_viewer_doorway_layout.png"
    img.save(out)
    return out.as_posix()


def _render_placement_option(option_id: str, media_dir: Path) -> str:
    specs = {
        "B1": (
            "Always open near parent surface",
            "Default: parent-neighbor every launch",
            "Same session: user move ignored on reopen",
            "Restart: parent-neighbor",
            (620, 190),
            (690, 220),
        ),
        "B2": (
            "Same-session restore, restart reset",
            "Default: parent-neighbor",
            "Same session: restore last user-moved position",
            "Restart: reset near parent",
            (620, 190),
            (1040, 420),
        ),
        "B3": (
            "Persistent last-used position",
            "Default: parent-neighbor until moved",
            "Same session: restore moved position",
            "Restart: persist moved position; needs reset",
            (1020, 430),
            (1040, 570),
        ),
    }
    title, default_text, session_text, restart_text, rec_pos, log_pos = specs[option_id]
    img = Image.new("RGB", (1280, 760), (4, 12, 18))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 704, 1280, 760), fill=(9, 24, 34))
    draw.text((38, 28), f"{option_id} - {title}", fill=(232, 246, 250), font=_font(28))
    # Parent dashboard context.
    parent = (66, 118, 560, 640)
    draw.rounded_rectangle(parent, radius=26, fill=(5, 24, 37), outline=(47, 148, 166), width=2)
    draw.text((96, 152), "HUD DASHBOARD PARENT SURFACE", fill=(232, 246, 250), font=_font(22))
    draw.rounded_rectangle((96, 250, 530, 424), radius=22, fill=(6, 30, 43), outline=(31, 101, 122), width=2)
    draw.text((126, 286), "RECORDING CARD", fill=(232, 246, 250), font=_font(20))
    _draw_button(draw, (326, 354, 514, 396), "Recording Studio")
    _draw_button(draw, (326, 444, 514, 486), "Log Viewer Studio")
    # Child windows.
    for name, pos, color in (
        ("Recording Studio", rec_pos, (67, 181, 202)),
        ("Log Viewer Studio", log_pos, (102, 215, 188)),
    ):
        x, y = pos
        draw.rounded_rectangle((x, y, x + 210, y + 116), radius=18, fill=(6, 27, 39), outline=color, width=2)
        draw.text((x + 20, y + 24), name.upper(), fill=(235, 247, 250), font=_font(15))
        draw.line((x + 20, y + 56, x + 190, y + 56), fill=color, width=2)
        draw.text((x + 20, y + 72), "feature-studio child", fill=(169, 214, 223), font=_font(12))
    # Behavior key.
    key_x, key_y = 690, 96
    draw.rounded_rectangle((key_x, key_y, 1220, key_y + 86), radius=18, fill=(6, 29, 43), outline=(35, 119, 140), width=1)
    for idx, text in enumerate((default_text, session_text, restart_text)):
        draw.text((key_x + 22, key_y + 16 + idx * 22), text, fill=(206, 232, 239), font=_font(14))
    draw.line((560, 356, rec_pos[0], rec_pos[1] + 58), fill=(79, 178, 199), width=2)
    draw.line((560, 468, log_pos[0], log_pos[1] + 58), fill=(102, 215, 188), width=2)
    draw.text((38, 712), "Full desktop/context diagram: parent surface, Recording Studio, Log Viewer Studio, and placement behavior.", fill=(186, 216, 225), font=_font(15))
    out = media_dir / f"{option_id.lower()}_child_window_placement_context.png"
    img.save(out)
    return out.as_posix()


def _create_option_renders(media_dir: Path) -> list[str]:
    media_dir.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    for option_id in ("A1", "A2", "A3"):
        paths.append(_render_recording_option(option_id, media_dir))
    for option_id in ("B1", "B2", "B3"):
        paths.append(_render_placement_option(option_id, media_dir))
    for option_id in ("C1", "C2", "C3"):
        paths.append(_render_log_option(option_id, media_dir))
    paths.append(_create_options_board(media_dir))
    return paths


def _create_full_desktop_board(media_dir: Path) -> str:
    media_dir.mkdir(parents=True, exist_ok=True)
    sources = [
        ("Full desktop proof that reopened the packet", PROOF_ROOT / "full_desktop_recording_and_log_viewer_after_repair.png"),
        ("Recording Studio focused proof from rejected packet", PROOF_ROOT / "recording_default.png"),
        ("Log Viewer Studio focused proof from rejected packet", PROOF_ROOT / "log_viewer_default.png"),
        ("Accepted AI Control Center comparator", AI_CONTROL_SCREENSHOT),
    ]
    canvas = Image.new("RGB", (1800, 1120), (4, 14, 22))
    draw = ImageDraw.Draw(canvas)
    _label(draw, (36, 28), "FAM-006 Full-Desktop False-Green Comparison Board", 28)
    x, y = 36, 84
    for idx, (title, src) in enumerate(sources):
        if not src.exists():
            continue
        thumb = _image_thumb(src, (820, 420))
        px = x + (idx % 2) * 880
        py = y + (idx // 2) * 500
        draw.rounded_rectangle((px - 10, py - 10, px + 840, py + 455), radius=22, outline=(36, 131, 151), width=2, fill=(7, 25, 37))
        _label(draw, (px, py), title, 17)
        canvas.paste(thumb, (px, py + 36))
    out = media_dir / "full_desktop_false_green_comparison_board.png"
    canvas.save(out)
    return out.as_posix()


def _create_options_board(media_dir: Path) -> str:
    media_dir.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (1900, 1420), (4, 14, 22))
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 32), "FAM-006 Visual / Placement Options For USER Review", fill=(222, 246, 250), font=_font(30))
    draw.text(
        (42, 72),
        "Rendered mockup evidence only; no runtime UI implementation is performed by this packet.",
        fill=(171, 213, 224),
        font=_font(16),
    )
    option_files = [
        ("A1", media_dir / "a1_nested_card_inheritance.png"),
        ("A2", media_dir / "a2_nested_card_inheritance.png"),
        ("A3", media_dir / "a3_nested_card_inheritance.png"),
        ("B1", media_dir / "b1_child_window_placement_context.png"),
        ("B2", media_dir / "b2_child_window_placement_context.png"),
        ("B3", media_dir / "b3_child_window_placement_context.png"),
        ("C1", media_dir / "c1_log_viewer_doorway_layout.png"),
        ("C2", media_dir / "c2_log_viewer_doorway_layout.png"),
        ("C3", media_dir / "c3_log_viewer_doorway_layout.png"),
    ]
    for i, (option_id, src) in enumerate(option_files):
        row = i // 3
        col = i % 3
        x = 42 + col * 610
        y = 122 + row * 420
        draw.rounded_rectangle((x, y, x + 570, y + 380), radius=24, outline=(46, 143, 164), width=2, fill=(7, 28, 41))
        draw.text((x + 18, y + 14), option_id, fill=(122, 224, 233), font=_font(22))
        if src.exists():
            thumb = _image_thumb(src, (532, 315))
            canvas.paste(thumb, (x + 18, y + 52))
        else:
            draw.text((x + 18, y + 52), "MISSING RENDER", fill=(255, 116, 116), font=_font(22))
    out = media_dir / "visual_and_placement_options_board.png"
    canvas.save(out)
    return out.as_posix()


def _source_truth_files() -> dict[str, Path]:
    return {
        "Docs_Main.md": WORKTREE / "Docs/Main.md",
        "Docs_nexus_startup_contract.md": WORKTREE / "Docs/nexus_startup_contract.md",
        "Docs_phase_governance.md": WORKTREE / "Docs/phase_governance.md",
        "Docs_branch_plans_README.md": WORKTREE / "Docs/branch_plans/README.md",
        "Docs_nexus_vision.md": WORKTREE / "Docs/nexus_vision.md",
        "FAM-002_desktop_interface.md": WORKTREE / "Docs/family_visions/FAM-002_desktop_interface.md",
        "FAM-006_monitoring_and_hud.md": WORKTREE / "Docs/family_visions/FAM-006_monitoring_and_hud.md",
        "FAM-006_recording.md": WORKTREE / "Docs/family_feature_visions/FAM-006_recording.md",
        "ui_reference_catalog_index.md": WORKTREE / "Docs/ui_reference_catalog/index.md",
        "UIREF-001_top_level_window_frame.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-001_top_level_window_frame.md",
        "UIREF-002_window_control_cluster.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-002_window_control_cluster.md",
        "UIREF-003_control_state_and_selector_grammar.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-003_control_state_and_selector_grammar.md",
        "UIREF-004_dialog_status_recovery_and_doorway_surfaces.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
        "UIREF-005_design_token_and_shared_rule_baseline.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-005_design_token_and_shared_rule_baseline.md",
        "UIREF-006_negative_example_and_enforcement_contract.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-006_negative_example_and_enforcement_contract.md",
        "Docs_user_test_summary_guidance.md": WORKTREE / "Docs/user_test_summary_guidance.md",
        "Docs_validation_helper_registry.md": WORKTREE / "Docs/validation_helper_registry.md",
        "Docs_incident_patterns.md": WORKTREE / "Docs/incident_patterns.md",
        "Docs_external_operational_state_store_reform_plan.md": WORKTREE / "Docs/external_operational_state_store_reform_plan.md",
        "feature_fam_006_dashboard_recording_start_stop_local_file.md": WORKTREE / "Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md",
        "external_branch_plan.md": EXTERNAL_ROOT / "branch_plan.md",
    }


def _identity() -> dict[str, str]:
    upstream = _run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"])
    return {
        "worktree": str(WORKTREE),
        "gitRoot": _run_git(["rev-parse", "--show-toplevel"]),
        "branch": _run_git(["branch", "--show-current"]),
        "upstream": upstream,
        "head": _run_git(["rev-parse", "HEAD"]),
        "originMain": _run_git(["rev-parse", "origin/main"]),
        "mergeBase": _run_git(["merge-base", "HEAD", "origin/main"]),
        "aheadBehindOriginMain": _run_git(["rev-list", "--left-right", "--count", "origin/main...HEAD"]),
        "aheadBehindUpstream": _run_git(["rev-list", "--left-right", "--count", f"{upstream}...HEAD"]),
        "status": _run_git(["status", "--short", "--branch"]),
    }


def _root_cause_rows() -> list[dict[str, str]]:
    return [
        {
            "defectId": "FAM006-FD-FG-001",
            "falseGreenSymptom": "The 121535 packet claimed ACCEPT while the full desktop showed the studio windows as detached islands.",
            "evidenceThatExposedIt": "Review Aids/Evidence/Full Desktop/full_desktop_recording_and_log_viewer_after_repair.png",
            "whyPacketProofMissedIt": "Focused crops were treated as primary visual acceptance evidence; the full desktop screenshot existed but was not a blocking comparator row.",
            "whyValidatorHelperMissedIt": "The existing gates checked packet-relative crop completeness and comparator crops, but did not require a full-context red-team disposition for scale, placement, or composition.",
            "whyCodexReviewMissedIt": "Codex over-indexed on compact focused proof and prior row-grammar fixes rather than re-reading the full desktop as the controlling visual evidence.",
            "whyChatGPTReviewMissedIt": "The upload packet emphasized row and crop proofs, so ChatGPT could inspect narrow proof without a mandatory full-desktop contradiction checklist.",
            "sourceTruthOwnerGap": "FAM-006 Recording FFV lacked an explicit full-desktop contradiction rule for Recording/Log Viewer acceptance packets.",
            "validatorToolingGap": "No branch-local helper required a full-context red-team ledger before a visual ACCEPT packet could be regenerated.",
            "repairRequired": "Add branch-local source truth and packet/helper validation requiring full-desktop proof hierarchy and red-team rows.",
            "futurePreventionRule": "Material window visual acceptance must fail closed when full-desktop proof contradicts focused crops.",
            "proofRequiredToClose": "Packet contains full-desktop proof, contradiction ledger, source-truth carrydown, and USER options before any renewed LV.",
        },
        {
            "defectId": "FAM006-FD-FG-002",
            "falseGreenSymptom": "Log Viewer Studio looked acceptable in a focused crop but too tall and doorway-like in full desktop context.",
            "evidenceThatExposedIt": "Full desktop comparison board plus rejected log_viewer_default.png.",
            "whyPacketProofMissedIt": "The packet did not require dead-space and footprint-context rows tied to the full desktop image.",
            "whyValidatorHelperMissedIt": "The height/row checks used numeric size contracts and crop geometry, not visual footprint burden in the user's monitor context.",
            "whyCodexReviewMissedIt": "Codex treated a reduced height as sufficient instead of asking whether the doorway shell still looked too large for two folder actions.",
            "whyChatGPTReviewMissedIt": "The focused evidence made the window appear proportionate and did not force a side-by-side desktop scale callout.",
            "sourceTruthOwnerGap": "FAM-006 Recording FFV did not require Log Viewer doorway options when footprint remains arguable after proof.",
            "validatorToolingGap": "No helper required classifying fake-workspace smell or dead-space burden as a visual issue.",
            "repairRequired": "Record Log Viewer doorway layout options and classify the issue as VISUAL_OPTIONS_REQUIRED plus future implementation repair.",
            "futurePreventionRule": "Doorway shells need full-context footprint and dead-space review before ACCEPT.",
            "proofRequiredToClose": "USER-selected Log Viewer option and implementation-match proof with full-desktop context.",
        },
        {
            "defectId": "FAM006-FD-FG-003",
            "falseGreenSymptom": "Window placement was unproven even though placement changed how the studios read in the desktop.",
            "evidenceThatExposedIt": "USER reported moving the windows; full desktop proof shows free-floating placement away from an explicit parent-neighbor rule.",
            "whyPacketProofMissedIt": "Focused screenshots omit parent, monitor, taskbar, and neighboring surface context.",
            "whyValidatorHelperMissedIt": "Existing helpers validated window existence, size, crops, and resize proof but not deterministic default placement behavior.",
            "whyCodexReviewMissedIt": "Codex did not distinguish same-session user-moved position from default-open placement doctrine.",
            "whyChatGPTReviewMissedIt": "The packet did not include placement options or a parent-relative proof row to review.",
            "sourceTruthOwnerGap": "FAM-006 Recording FFV lacked child-window placement/default-position doctrine for feature-studio windows.",
            "validatorToolingGap": "No packet validator failed when child placement proof or options were absent.",
            "repairRequired": "Add branch-local child placement doctrine candidate and visual options to the USER packet.",
            "futurePreventionRule": "Material child/feature-studio placement must be proven or optioned before implementation acceptance.",
            "proofRequiredToClose": "USER selects placement behavior; later implementation proves default, moved, restart, and unavailable-location cases.",
        },
        {
            "defectId": "FAM006-FD-FG-004",
            "falseGreenSymptom": "Recording Studio label pressure and row rhythm were not reclassified after full-context review.",
            "evidenceThatExposedIt": "Full desktop proof shows OPEN LOG VIEWER STUDIO consuming the compact controller button row.",
            "whyPacketProofMissedIt": "Button crop proof checked text visibility and border/glow but not compact-controller pressure across the whole window.",
            "whyValidatorHelperMissedIt": "The gate lacked a row for label pressure as a product-experience issue.",
            "whyCodexReviewMissedIt": "Codex accepted the text fit as a pass instead of checking whether the label undermined compact purpose.",
            "whyChatGPTReviewMissedIt": "The packet did not surface label pressure as a decision row.",
            "sourceTruthOwnerGap": "FAM-006 Recording FFV did not tie compact controller footprint to action-label pressure in visual packets.",
            "validatorToolingGap": "No helper classified label pressure as a must-repair or options-required issue.",
            "repairRequired": "Seed the defect ledger with label pressure and require USER-readable classification.",
            "futurePreventionRule": "Compact-controller visual review must inspect action-label pressure, not just text clipping.",
            "proofRequiredToClose": "Implementation-match proof after the selected compact-controller action grammar is applied.",
        },
    ]


def _defect_rows() -> list[dict[str, str]]:
    return [
        {"id": "FAM006-FD-VIS-001", "issue": "Log Viewer Studio reads too large/tall in full desktop.", "classification": "VISUAL_OPTIONS_REQUIRED", "reason": "Runtime repair is excluded; user needs doorway layout options before implementation."},
        {"id": "FAM006-FD-VIS-002", "issue": "Log Viewer Studio has too much empty/dead body space.", "classification": "VISUAL_OPTIONS_REQUIRED", "reason": "Must be solved by selected doorway layout and later implementation-match repair."},
        {"id": "FAM006-FD-VIS-003", "issue": "Log Viewer button row is disconnected from truth rows.", "classification": "VISUAL_OPTIONS_REQUIRED", "reason": "Options compare tighter stack, inline actions, and compact footer action variants."},
        {"id": "FAM006-FD-VIS-004", "issue": "Log Viewer risks fake workspace feel despite doorway-only scope.", "classification": "SOURCE_TRUTH_RULE_REQUIRED", "reason": "Doorway shells must avoid visual implication of graph/viewer/export implementation."},
        {"id": "FAM006-FD-VIS-005", "issue": "Recording Studio row rhythm still does not fully inherit AI/HUD grammar.", "classification": "VISUAL_OPTIONS_REQUIRED", "reason": "Nested-card inheritance amount remains a USER visual decision."},
        {"id": "FAM006-FD-VIS-006", "issue": "Recording Studio OPEN LOG VIEWER STUDIO label creates horizontal pressure.", "classification": "MUST_REPAIR_NOW", "reason": "Current packet must mark it as a blocking implementation-match issue, not a pass."},
        {"id": "FAM006-FD-VIS-007", "issue": "Studios borrow row lines but not enough contained row-group feeling.", "classification": "VISUAL_OPTIONS_REQUIRED", "reason": "Three child-window nested-card inheritance options are packeted."},
        {"id": "FAM006-FD-VIS-008", "issue": "Underglow/divider rhythm is flatter than AI/HUD.", "classification": "VISUAL_OPTIONS_REQUIRED", "reason": "Needs comparator-guided option selection before runtime repair."},
        {"id": "FAM006-FD-VIS-009", "issue": "Child-window placement proof is material and missing.", "classification": "SOURCE_TRUTH_RULE_REQUIRED", "reason": "Branch-local placement doctrine and options are required."},
        {"id": "FAM006-FD-VIS-010", "issue": "Focused/cropped proof hid full-desktop scale, placement, empty-space, and composition issues.", "classification": "VALIDATOR_HELPER_REQUIRED", "reason": "New packet helper validates full-context proof and red-team ledgers."},
        {"id": "FAM006-FD-VIS-011", "issue": "Codex and ChatGPT both missed obvious full-desktop issues.", "classification": "VALIDATOR_HELPER_REQUIRED", "reason": "False-green incident must be recorded with row-specific root cause."},
    ]


def _placement_doctrine() -> dict[str, Any]:
    return {
        "status": "BRANCH_LOCAL_PROPOSED_DOCTRINE_PENDING_USER_SELECTION",
        "owner": "FAM-006 Recording FFV and active external branch plan",
        "rules": [
            "Feature-studio child windows should use deterministic parent-relative placement unless source truth or USER selection says otherwise.",
            "Same-session reopen may restore the last user-moved position.",
            "After app or computer restart, child windows should default near their parent surface unless USER selects persistent last-position behavior.",
            "Material placement behavior must be proven with full-desktop/context screenshots or option renders.",
            "If multiple viable placement behaviors exist, Codex must packet visual options before runtime implementation.",
        ],
        "options": [
            "B1: always open near parent surface.",
            "B2: same-session last-used position; restart resets near parent.",
            "B3: persistent last-used position across restarts plus future reset behavior.",
        ],
    }


def _visual_options_markdown() -> str:
    return """# FAM-006 Visual And Placement Options

Status: USER review options only. This packet does not implement runtime UI.

ChatGPT product recommendation is non-binding:

- A2 is likely preferred because it inherits AI Control Center / HUD Dashboard row-container grammar without becoming a fake dashboard.
- B2 is likely preferred because it respects same-session user placement but resets near parent after restart.
- C2 is likely preferred because each truth row owns its action and avoids disconnected dead button rows.
- If C2 creates width pressure, C1 is the safer compact fallback.

## A. Child-Window Nested-Card Inheritance

| Option | Rendered media | Source-truth basis | Pros | Risks / what USER should critique |
| --- | --- | --- | --- | --- |
| A1 | `Review Aids/Evidence/Options/a1_nested_card_inheritance.png` | Compact unique child controller; row density and proof-debug avoidance. | Smallest footprint; least dashboard-card cloning. | May still feel too detached from AI/HUD row-container grammar; critique row grouping and glow rhythm. |
| A2 | `Review Aids/Evidence/Options/a2_nested_card_inheritance.png` | Subtle contained row group / section-card inheritance from AI Control Center. | Stronger row rhythm while staying compact. | Needs careful density to avoid table/proof-panel feel; critique nested-card inheritance amount. |
| A3 | `Review Aids/Evidence/Options/a3_nested_card_inheritance.png` | Stronger parent-family card grammar while preserving compact footprint. | Most immersive family relationship. | Could become too large or fake-workspace-like; critique whether it overcopies dashboard/card grammar. |

## B. Child-Window Placement Behavior

| Option | Rendered media | Default-open behavior | Same-session behavior | Restart behavior | Risk / validation obligation |
| --- | --- | --- | --- | --- | --- |
| B1 | `Review Aids/Evidence/Options/b1_child_window_placement_context.png` | Always near parent. | User move is not preserved on reopen. | Near parent. | Most predictable, but may feel hostile to user placement; prove parent-neighbor opening. |
| B2 | `Review Aids/Evidence/Options/b2_child_window_placement_context.png` | Near parent. | Restore last user-moved position. | Reset near parent. | Recommended balance; prove same-session restore and restart reset. |
| B3 | `Review Aids/Evidence/Options/b3_child_window_placement_context.png` | Near parent until moved. | Restore last user-moved position. | Persist moved position. | Requires reset-default-position control and stale-screen recovery proof. |

## C. Log Viewer Doorway Layout

| Option | Rendered media | Doorway scope | Pros | Risks / what USER should critique |
| --- | --- | --- | --- | --- |
| C1 | `Review Aids/Evidence/Options/c1_log_viewer_doorway_layout.png` | Native/export folder access only; no graph, previous-log selection, or export customization. | Reduces dead space and preserves compact vertical reading. | Still vertically structured; critique whether actions feel close enough to rows. |
| C2 | `Review Aids/Evidence/Options/c2_log_viewer_doorway_layout.png` | Native/export folder access only; no full-viewer/workspace behavior. | Ties each path/truth row directly to its action. | Needs width discipline for path text; critique row/action pressure. |
| C3 | `Review Aids/Evidence/Options/c3_log_viewer_doorway_layout.png` | Native/export folder access only; footer action lane. | Clear action area and simple shell. | Must avoid disconnected buttons and empty body; critique dead-space risk. |

## Implementation Risk And Proof If Selected

- Selected A option must later prove row grouping, underglow rhythm, density, and compact footprint with implementation screenshots, not helper text.
- Selected B option must later prove default-open, moved, reopened, restart/unavailable-location, and restore behavior with full-desktop evidence or USER validation where photo/video cannot prove it.
- Selected C option must later prove native/export folder actions without implying full Log Viewer, graph, export customization, or previous-log selection scope.
- Any selected option still remains subordinate to Project Vision, FAM-002, FAM-006, UIREF, and the Recording FFV.
"""


def _primary_markdown(identity: dict[str, str], zip_path: Path) -> str:
    return f"""# FAM-006 Full-Desktop Visual False-Green Review

Packet Status: `{STATUS}`

This packet reopens the rejected row-grammar / footprint packet as a false green.
It is not H1 acceptance, Live Validation acceptance, UTS acceptance, PR Readiness,
runtime UI repair, or release readiness.

## Identity

| Field | Value |
| --- | --- |
| Worktree | `{identity['worktree']}` |
| Branch | `{identity['branch']}` |

Detailed Git identity and upload proof are recorded in helper output and the
external manifest, not in the primary USER decision file.

## Rejected Packet

- Rejected ZIP: `C:\\Nexus USER\\FAM-006-20260624-121535.zip`
- Rejected options ZIP: `C:\\Nexus USER\\FAM-006-20260624-130151.zip`
- Known-bad corpus copy: `C:\\Nexus Governance State\\branches\\feature_fam_006_dashboard_recording_start_stop_local_file\\false_accept_regression_corpus\\FAM-006-20260624-121535.zip`

The rejected packet proof values are recorded in helper output and the external
manifest.

## Full-Desktop Red-Team Result

Verdict: `REPAIR`

The focused crops in the rejected packet were not enough. The included full
desktop proof shows the Studio windows in real monitor context and exposes
scale, placement, empty-space, button-row relationship, and child-window
composition defects that the cropped packet underweighted.

Controlling media:

- `Review Aids/Evidence/Full Desktop/full_desktop_recording_and_log_viewer_after_repair.png`
- `Review Aids/Evidence/Full Desktop/full_desktop_false_green_comparison_board.png`
- `Review Aids/Evidence/Rejected 121535 Proof/recording_default.png`
- `Review Aids/Evidence/Rejected 121535 Proof/log_viewer_default.png`
- `Review Aids/Evidence/References/AI Control Center- Accepted.png`

## Defect Classification

See `Review Aids/USER_REPORTED_VISUAL_DEFECT_LEDGER.md`.

Key result:

- `MUST_REPAIR_NOW`: the active implementation-match packet must not claim visual green while label pressure and crop-only acceptance remain unresolved.
- `VISUAL_OPTIONS_REQUIRED`: nested-card inheritance, placement behavior, Log Viewer doorway layout, and underglow/rhythm details need USER option review before runtime repair.
- `SOURCE_TRUTH_RULE_REQUIRED`: full-desktop proof hierarchy and child-window placement doctrine must be recorded in branch-local source truth.
- `VALIDATOR_HELPER_REQUIRED`: packet/helper logic must fail if future packets omit full-context red-team proof for material windows.

## Source-Truth Repair Summary

Updated branch-local source truth records:

- `Docs/family_feature_visions/FAM-006_recording.md`
- `Docs/validation_helper_registry.md`
- `Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md`
- `C:\\Nexus Governance State\\branches\\feature_fam_006_dashboard_recording_start_stop_local_file\\branch_plan.md`

Global Governance promotion remains a candidate only. This branch does not mutate
the Governance worktree, FAM-007, neutral main, GitHub issues, release state, or
runtime UI layout.

## Child-Window Placement Doctrine

See `Review Aids/CHILD_WINDOW_PLACEMENT_DOCTRINE.md`.

Current disposition: branch-local proposed doctrine pending USER selection.

## Visual Options

See:

- `Review Aids/VISUAL_AND_PLACEMENT_OPTIONS.md`
- `Review Aids/Evidence/Options/visual_and_placement_options_board.png`
- `Review Aids/Evidence/Options/a1_nested_card_inheritance.png`
- `Review Aids/Evidence/Options/a2_nested_card_inheritance.png`
- `Review Aids/Evidence/Options/a3_nested_card_inheritance.png`
- `Review Aids/Evidence/Options/b1_child_window_placement_context.png`
- `Review Aids/Evidence/Options/b2_child_window_placement_context.png`
- `Review Aids/Evidence/Options/b3_child_window_placement_context.png`
- `Review Aids/Evidence/Options/c1_log_viewer_doorway_layout.png`
- `Review Aids/Evidence/Options/c2_log_viewer_doorway_layout.png`
- `Review Aids/Evidence/Options/c3_log_viewer_doorway_layout.png`

The prior 130151 packet is repaired here because its option board was mostly
text cards, several option cards were clipped, and validation evidence was not
complete inside the packet.

## Validation Evidence

See `Review Aids/VALIDATION_OUTPUT_EVIDENCE.md` and
`Review Aids/Validation Outputs/`. Validation records include command, cwd,
timestamp, exit code, PASS/FAIL, stdout, and stderr for every command captured
inside this packet. Final post-ZIP SHA proof is external/non-self-mutating.

## Next Legal Phase

USER review of this false-green / full-desktop proof repair packet.

After USER review, the next legal implementation path is a bounded FAM-006
runtime visual/options implementation repair only if USER approves the selected
visual and placement direction. Renewed exact USER desktop launcher Live
Validation, UTS acceptance, later PR gates, merge, release, and cleanup remain
blocked.

## Exact USER Decision Needed

Review this packet and choose one:

- Accept the branch-local full-desktop false-green repair packet and select the child-window inheritance, placement, and Log Viewer doorway options for the next bounded runtime repair.
- Request revisions to the packet, source-truth rule, or visual options.
- Reject the packet and provide the corrected visual/process direction.

Current upload artifact path is returned by the helper and Codex completion
packet.
"""


def _ledger_markdown(title: str, rows: list[dict[str, str]]) -> str:
    keys = list(rows[0].keys())
    lines = [f"# {title}", "", "| " + " | ".join(keys) + " |", "| " + " | ".join("---" for _ in keys) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ") for key in keys) + " |")
    return "\n".join(lines) + "\n"


def _copy_source_truth(packet: Path) -> None:
    dst = packet / "Source Truth Context"
    for name, src in _source_truth_files().items():
        if src.exists():
            _copy_file(src, dst / name)


def _copy_udl(packet: Path) -> None:
    target = packet / "Review Aids" / "Unified Defect Ledger"
    for src_name in (
        "unified_defect_ledger.json",
        "UNIFIED_DEFECT_LEDGER.md",
        "false_green_incident_ledger.json",
        "FALSE_GREEN_INCIDENT_LEDGER.md",
        "unified_defect_ledger_gate.json",
    ):
        src = EXTERNAL_ROOT / src_name
        if src.exists():
            _copy_file(src, target / src_name)


def _capture_command(command_id: str, command: list[str]) -> dict[str, Any]:
    started = datetime.now().isoformat(timespec="seconds")
    result = subprocess.run(command, cwd=WORKTREE, text=True, capture_output=True)
    return {
        "commandId": command_id,
        "cwd": str(WORKTREE),
        "timestamp": started,
        "command": command,
        "exitCode": result.returncode,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _write_validation_outputs(packet: Path) -> list[dict[str, Any]]:
    output_dir = packet / "Review Aids" / "Validation Outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    commands = [
        ("git_status_branch", ["git", "status", "--short", "--branch"]),
        ("git_diff_check", ["git", "diff", "--check"]),
        ("git_diff_check_origin_main", ["git", "diff", "--check", "origin/main...HEAD"]),
        ("udl_gate", ["python", "dev/orin_fam006_unified_defect_ledger.py"]),
    ]
    results = [_capture_command(command_id, command) for command_id, command in commands]
    for result in results:
        _write_json(output_dir / f"{result['commandId']}.json", result)
        _write_text(
            output_dir / f"{result['commandId']}.txt",
            "\n".join(
                [
                    f"Command ID: {result['commandId']}",
                    f"CWD: {result['cwd']}",
                    f"Timestamp: {result['timestamp']}",
                    f"Command: {' '.join(result['command'])}",
                    f"Exit Code: {result['exitCode']}",
                    f"Status: {result['status']}",
                    "",
                    "STDOUT:",
                    result["stdout"],
                    "",
                    "STDERR:",
                    result["stderr"],
                ]
            ),
        )
    _write_json(output_dir / "validation_outputs_summary.json", {"results": results})
    _write_text(
        packet / "Review Aids" / "VALIDATION_OUTPUT_EVIDENCE.md",
        "# Validation Output Evidence\n\n"
        "Each listed validation includes command, cwd, timestamp, exit code, PASS/FAIL, stdout, and stderr. "
        "The final post-ZIP SHA and post-ZIP validation are intentionally reported outside the ZIP to avoid self-mutating hash proof.\n\n"
        + "\n".join(
            f"- `{result['commandId']}`: `{result['status']}`; see `Review Aids/Validation Outputs/{result['commandId']}.json`."
            for result in results
        )
        + "\n",
    )
    return results


def _write_external_receipt(zip_path: Path, zip_sha: str) -> None:
    plan = EXTERNAL_ROOT / "branch_plan.md"
    marker_start = "<!-- FAM006_FULL_DESKTOP_FALSE_GREEN_REVIEW_START -->"
    marker_end = "<!-- FAM006_FULL_DESKTOP_FALSE_GREEN_REVIEW_END -->"
    section = f"""{marker_start}
## FAM-006 Full-Desktop Visual False-Green Review Receipt - 2026-06-24

Status: `REPAIR / Pending USER review`.

Rejected packet: `C:\\Nexus USER\\FAM-006-20260624-121535.zip`.
Rejected packet SHA256: `{REJECTED_SHA256}`.
Rejected options packet: `C:\\Nexus USER\\FAM-006-20260624-130151.zip`.
Rejected options packet SHA256: `{REJECTED_OPTIONS_SHA256}`.
Known-bad corpus copy: `C:\\Nexus Governance State\\branches\\feature_fam_006_dashboard_recording_start_stop_local_file\\false_accept_regression_corpus\\FAM-006-20260624-121535.zip`.

Root cause: focused/cropped row-grammar proof and comparator media were treated
as sufficient even though the full-desktop proof contradicted the visual
acceptance claim for scale, placement, dead space, control relationship, and
child-window composition.

Second root cause: the 130151 repair packet carried the right false-green
direction but represented visual/spatial decisions with mostly text cards,
clipped option content, and incomplete in-packet validation output evidence.

Branch-local source-truth disposition: FAM-006 Recording now requires
full-desktop/full-context contradiction review for material Recording Studio and
Log Viewer Studio visual acceptance packets, and requires branch-local
child-window placement/options review with actual rendered visual media before
runtime implementation of unresolved placement behavior.

Current USER packet: `{zip_path}`.
Current USER packet SHA256: `{zip_sha}`.

Next legal phase: USER reviews the false-green / full-desktop proof packet and
selects or revises the child-window visual inheritance, placement, and Log
Viewer doorway options. Renewed H1/LV/UTS and PR Readiness remain blocked.
{marker_end}
"""
    text = plan.read_text(encoding="utf-8") if plan.exists() else ""
    if marker_start in text and marker_end in text:
        before = text.split(marker_start, 1)[0].rstrip()
        after = text.split(marker_end, 1)[1].lstrip()
        text = before + "\n\n" + section + "\n" + after
    else:
        text = text.rstrip() + "\n\n" + section
    _write_text(plan, text)


def generate() -> dict[str, Any]:
    identity = _identity()
    if identity["branch"] != "feature/fam-006-dashboard-recording-start-stop-local-file":
        raise SystemExit(f"wrong branch: {identity['branch']}")
    if identity["originMain"] != identity["mergeBase"]:
        raise SystemExit("origin/main is not merged into this branch")

    KNOWN_BAD_ROOT.mkdir(parents=True, exist_ok=True)
    known_bad_copy = KNOWN_BAD_ROOT / REJECTED_PACKET.name
    known_bad_options_copy = KNOWN_BAD_ROOT / REJECTED_OPTIONS_PACKET.name
    if REJECTED_PACKET.exists():
        if _sha256(REJECTED_PACKET) != REJECTED_SHA256:
            raise SystemExit("rejected 121535 packet SHA mismatch")
        shutil.copy2(REJECTED_PACKET, known_bad_copy)
    if REJECTED_OPTIONS_PACKET.exists():
        if _sha256(REJECTED_OPTIONS_PACKET) != REJECTED_OPTIONS_SHA256:
            raise SystemExit("rejected 130151 packet SHA mismatch")
        shutil.copy2(REJECTED_OPTIONS_PACKET, known_bad_options_copy)

    _purge_user_hub()
    for folder in ("USER Review", "Review Aids", "Source Truth Context"):
        (PACKET_ROOT / folder).mkdir(parents=True, exist_ok=True)

    evidence = PACKET_ROOT / "Review Aids" / "Evidence"
    full_desktop_dir = evidence / "Full Desktop"
    rejected_dir = evidence / "Rejected 121535 Proof"
    reference_dir = evidence / "References"
    options_dir = evidence / "Options"

    copied_media = []
    media_sources = [
        (PROOF_ROOT / "full_desktop_recording_and_log_viewer_after_repair.png", full_desktop_dir / "full_desktop_recording_and_log_viewer_after_repair.png"),
        (PROOF_ROOT / "recording_default.png", rejected_dir / "recording_default.png"),
        (PROOF_ROOT / "log_viewer_default.png", rejected_dir / "log_viewer_default.png"),
        (AI_CONTROL_SCREENSHOT, reference_dir / "AI Control Center- Accepted.png"),
    ]
    for src, dst in media_sources:
        if src.exists():
            copied_media.append(_copy_file(src, dst))

    board = _create_full_desktop_board(full_desktop_dir)
    option_renders = _create_option_renders(options_dir)
    copied_media.extend([board, *option_renders])

    root_cause = _root_cause_rows()
    defects = _defect_rows()
    doctrine = _placement_doctrine()

    _write_json(PACKET_ROOT / "Review Aids" / "false_green_root_cause_ledger.json", root_cause)
    _write_text(PACKET_ROOT / "Review Aids" / "FALSE_GREEN_ROOT_CAUSE_LEDGER.md", _ledger_markdown("FAM-006 Full-Desktop False-Green Root-Cause Ledger", root_cause))
    _write_json(PACKET_ROOT / "Review Aids" / "user_reported_visual_defects_ledger.json", defects)
    _write_text(PACKET_ROOT / "Review Aids" / "USER_REPORTED_VISUAL_DEFECT_LEDGER.md", _ledger_markdown("FAM-006 USER-Reported Visual Defect Ledger", defects))
    _write_json(PACKET_ROOT / "Review Aids" / "child_window_placement_doctrine.json", doctrine)
    _write_text(PACKET_ROOT / "Review Aids" / "CHILD_WINDOW_PLACEMENT_DOCTRINE.md", "# FAM-006 Child-Window Placement Doctrine Candidate\n\n" + "\n".join(f"- {rule}" for rule in doctrine["rules"]) + "\n")
    _write_text(PACKET_ROOT / "Review Aids" / "VISUAL_AND_PLACEMENT_OPTIONS.md", _visual_options_markdown())
    _write_json(PACKET_ROOT / "Review Aids" / "packet_media_manifest.json", {"media": copied_media})
    _write_validation_outputs(PACKET_ROOT)
    _write_text(PACKET_ROOT / "Review Aids" / "FULL_DESKTOP_RED_TEAM_REVIEW.md", """# Full-Desktop Red-Team Review

Verdict: REPAIR.

The rejected 121535 packet contained focused crops that were useful for element
inspection, but the full desktop proof is the controlling evidence for scale,
placement, footprint, and window relationship. In that full context, Log Viewer
Studio reads too large and disconnected for a doorway-only shell, the Recording
Studio secondary action label pressures the compact controller, and placement
behavior is unproven. The packet therefore cannot support renewed Live
Validation or UTS handoff.
""")

    _copy_source_truth(PACKET_ROOT)
    _copy_udl(PACKET_ROOT)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = USER_ROOT / f"FAM-006-{timestamp}.zip"
    _write_text(PACKET_ROOT / "START_HERE.md", f"""# START HERE

Packet Status: `{STATUS}`

Primary review file: `{PRIMARY_REVIEW}`

This is a false-green / full-desktop proof repair packet. It does not approve
runtime UI repair, H1, Live Validation, UTS, PR Readiness, PR creation, merge,
release, or cleanup.
""")
    _write_text(PACKET_ROOT / PRIMARY_REVIEW, _primary_markdown(identity, zip_path))

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(p for p in PACKET_ROOT.rglob("*") if p.is_file()):
            zf.write(path, path.relative_to(PACKET_ROOT).as_posix())

    zip_sha = _sha256(zip_path)
    _write_external_receipt(zip_path, zip_sha)
    manifest = {
        "packetRoot": str(PACKET_ROOT),
        "zipPath": str(zip_path),
        "zipSha256": zip_sha,
        "knownBadCopy": str(known_bad_copy),
        "knownBadOptionsCopy": str(known_bad_options_copy),
        "rejectedSha256": REJECTED_SHA256,
        "rejectedOptionsSha256": REJECTED_OPTIONS_SHA256,
        "optionRenderCount": len(option_renders),
        "identity": identity,
    }
    _write_json(EXTERNAL_ROOT / "full_desktop_false_green_review_manifest.json", manifest)
    return manifest


def validate(packet_root: Path = PACKET_ROOT) -> list[str]:
    failures: list[str] = []
    if not packet_root.exists():
        return [f"packet root missing: {packet_root}"]
    zips = sorted(USER_ROOT.glob("FAM-006-*.zip"))
    if len(zips) != 1:
        failures.append(f"expected exactly one timestamped FAM-006 ZIP, found {len(zips)}")
    if (USER_ROOT / "FAM-006.zip").exists():
        failures.append("stable FAM-006.zip is forbidden for this packet")
    if not (KNOWN_BAD_ROOT / REJECTED_PACKET.name).exists():
        failures.append("121535 known-bad corpus copy is missing")
    elif _sha256(KNOWN_BAD_ROOT / REJECTED_PACKET.name) != REJECTED_SHA256:
        failures.append("121535 known-bad corpus copy SHA mismatch")
    if not (KNOWN_BAD_ROOT / REJECTED_OPTIONS_PACKET.name).exists():
        failures.append("130151 known-bad options packet corpus copy is missing")
    elif _sha256(KNOWN_BAD_ROOT / REJECTED_OPTIONS_PACKET.name) != REJECTED_OPTIONS_SHA256:
        failures.append("130151 known-bad options packet corpus copy SHA mismatch")

    required = [
        "START_HERE.md",
        PRIMARY_REVIEW,
        "Review Aids/FALSE_GREEN_ROOT_CAUSE_LEDGER.md",
        "Review Aids/false_green_root_cause_ledger.json",
        "Review Aids/USER_REPORTED_VISUAL_DEFECT_LEDGER.md",
        "Review Aids/user_reported_visual_defects_ledger.json",
        "Review Aids/FULL_DESKTOP_RED_TEAM_REVIEW.md",
        "Review Aids/CHILD_WINDOW_PLACEMENT_DOCTRINE.md",
        "Review Aids/VISUAL_AND_PLACEMENT_OPTIONS.md",
        "Review Aids/VALIDATION_OUTPUT_EVIDENCE.md",
        "Review Aids/Validation Outputs/git_status_branch.json",
        "Review Aids/Validation Outputs/git_diff_check.json",
        "Review Aids/Validation Outputs/git_diff_check_origin_main.json",
        "Review Aids/Validation Outputs/udl_gate.json",
        "Review Aids/Validation Outputs/validation_outputs_summary.json",
        "Review Aids/Unified Defect Ledger/unified_defect_ledger.json",
        "Review Aids/Unified Defect Ledger/UNIFIED_DEFECT_LEDGER.md",
        "Review Aids/Unified Defect Ledger/false_green_incident_ledger.json",
        "Review Aids/Unified Defect Ledger/FALSE_GREEN_INCIDENT_LEDGER.md",
        "Review Aids/Unified Defect Ledger/unified_defect_ledger_gate.json",
        "Review Aids/Evidence/Full Desktop/full_desktop_recording_and_log_viewer_after_repair.png",
        "Review Aids/Evidence/Full Desktop/full_desktop_false_green_comparison_board.png",
        "Review Aids/Evidence/Options/visual_and_placement_options_board.png",
        "Review Aids/Evidence/Options/a1_nested_card_inheritance.png",
        "Review Aids/Evidence/Options/a2_nested_card_inheritance.png",
        "Review Aids/Evidence/Options/a3_nested_card_inheritance.png",
        "Review Aids/Evidence/Options/b1_child_window_placement_context.png",
        "Review Aids/Evidence/Options/b2_child_window_placement_context.png",
        "Review Aids/Evidence/Options/b3_child_window_placement_context.png",
        "Review Aids/Evidence/Options/c1_log_viewer_doorway_layout.png",
        "Review Aids/Evidence/Options/c2_log_viewer_doorway_layout.png",
        "Review Aids/Evidence/Options/c3_log_viewer_doorway_layout.png",
        "Review Aids/Evidence/Rejected 121535 Proof/recording_default.png",
        "Review Aids/Evidence/Rejected 121535 Proof/log_viewer_default.png",
        "Review Aids/Evidence/References/AI Control Center- Accepted.png",
        "Source Truth Context/Docs_nexus_startup_contract.md",
        "Source Truth Context/Docs_external_operational_state_store_reform_plan.md",
        "Source Truth Context/FAM-006_recording.md",
        "Source Truth Context/UIREF-006_negative_example_and_enforcement_contract.md",
    ]
    for rel in required:
        if not (packet_root / rel).exists():
            failures.append(f"missing required packet artifact: {rel}")

    option_media = sorted((packet_root / "Review Aids/Evidence/Options").glob("*.png"))
    if len(option_media) < 10:
        failures.append(f"expected at least 10 option PNG renders/contact sheets, found {len(option_media)}")
    for path in option_media:
        try:
            with Image.open(path) as img:
                if img.size[0] < 320 or img.size[1] < 180:
                    failures.append(f"option media too small to review: {path.name} {img.size}")
        except Exception as exc:
            failures.append(f"option media unreadable: {path.name}: {exc}")

    review_files = [p for p in (packet_root / "USER Review").glob("*.md") if p.is_file()]
    if len(review_files) != 1 or review_files[0].relative_to(packet_root).as_posix() != PRIMARY_REVIEW:
        failures.append(f"expected exactly one primary review file {PRIMARY_REVIEW}, found {[p.name for p in review_files]}")

    try:
        root_rows = json.loads((packet_root / "Review Aids/false_green_root_cause_ledger.json").read_text(encoding="utf-8"))
        if len(root_rows) < 4:
            failures.append("root-cause ledger has fewer than four row-specific defects")
        for row in root_rows:
            for key in (
                "defectId",
                "falseGreenSymptom",
                "whyPacketProofMissedIt",
                "whyValidatorHelperMissedIt",
                "whyCodexReviewMissedIt",
                "whyChatGPTReviewMissedIt",
                "futurePreventionRule",
                "proofRequiredToClose",
            ):
                if not str(row.get(key, "")).strip():
                    failures.append(f"root-cause row missing {key}: {row.get('defectId', '<unknown>')}")
    except Exception as exc:
        failures.append(f"root-cause ledger invalid: {exc}")

    try:
        defects = json.loads((packet_root / "Review Aids/user_reported_visual_defects_ledger.json").read_text(encoding="utf-8"))
        if len(defects) != 11:
            failures.append(f"expected 11 seeded USER visual defects, found {len(defects)}")
        classes = {row.get("classification") for row in defects}
        for expected in ("MUST_REPAIR_NOW", "VISUAL_OPTIONS_REQUIRED", "SOURCE_TRUTH_RULE_REQUIRED", "VALIDATOR_HELPER_REQUIRED"):
            if expected not in classes:
                failures.append(f"missing visual defect classification: {expected}")
    except Exception as exc:
        failures.append(f"visual defect ledger invalid: {exc}")

    primary = (packet_root / PRIMARY_REVIEW).read_text(encoding="utf-8") if (packet_root / PRIMARY_REVIEW).exists() else ""
    required_phrases = [
        "Packet Status: `full-desktop-visual-false-green-review`",
        "Verdict: `REPAIR`",
        "Global Governance promotion remains a candidate only",
        "renewed exact USER desktop launcher Live",
    ]
    primary_lower = primary.lower()
    for phrase in required_phrases:
        if phrase.lower() not in primary_lower:
            failures.append(f"primary review file missing phrase: {phrase}")
    forbidden = ["Verdict: `ACCEPT`", "User Test Summary Results: `PASS`", "PR Readiness green"]
    for phrase in forbidden:
        if phrase in primary:
            failures.append(f"primary review file contains forbidden acceptance phrase: {phrase}")

    options_text = (packet_root / "Review Aids/VISUAL_AND_PLACEMENT_OPTIONS.md").read_text(encoding="utf-8", errors="replace") if (packet_root / "Review Aids/VISUAL_AND_PLACEMENT_OPTIONS.md").exists() else ""
    for token in ("A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "Rendered media", "ChatGPT product recommendation is non-binding"):
        if token not in options_text:
            failures.append(f"visual options review aid missing token: {token}")

    validation_summary = packet_root / "Review Aids/Validation Outputs/validation_outputs_summary.json"
    if validation_summary.exists():
        try:
            results = json.loads(validation_summary.read_text(encoding="utf-8")).get("results", [])
            if len(results) < 4:
                failures.append(f"validation output summary has too few command records: {len(results)}")
            for result in results:
                for key in ("command", "cwd", "timestamp", "exitCode", "status", "stdout", "stderr"):
                    if key not in result:
                        failures.append(f"validation output missing {key}: {result.get('commandId', '<unknown>')}")
                if result.get("status") != "PASS" or result.get("exitCode") != 0:
                    failures.append(f"validation output records failing command: {result.get('commandId', '<unknown>')}")
        except Exception as exc:
            failures.append(f"validation output summary invalid: {exc}")

    if zips:
        with zipfile.ZipFile(zips[0]) as zf:
            names = set(zf.namelist())
        for rel in required:
            if rel not in names:
                failures.append(f"ZIP missing required artifact: {rel}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

    if args.generate:
        result = generate()
        print(json.dumps(result, indent=2))
    if args.validate:
        failures = validate()
        if failures:
            print("FAIL: FAM-006 full-desktop false-green packet validation failed.")
            for failure in failures:
                print(f"- {failure}")
            return 1
        print("PASS: FAM-006 full-desktop false-green packet is complete and reviewable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
