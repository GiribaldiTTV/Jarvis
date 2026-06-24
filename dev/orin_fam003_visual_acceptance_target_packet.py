"""Generate the FAM-003 branch-local visual acceptance target packet.

The generated packet is USER-review material only. It does not mutate product
runtime UI, does not claim Live Validation green, and does not create a global
Governance rule.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import textwrap
import zipfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
STATE_ROOT = Path(
    r"C:\Nexus Governance State\branches\feature_fam_003_resident_access_quick_actions"
)
WORKTREE_STATE = Path(r"C:\Nexus Governance State\worktrees\FAM-003\worktree_state.md")
USER_ROOT = Path(r"C:\Nexus USER")
PACKET_LABEL = "FAM-003-Visual-Acceptance"
PACKET_ROOT = USER_ROOT / PACKET_LABEL
CURRENT_PROOF_ROOT = (
    ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation" / "20260623-140739"
)

BG = (2, 8, 18)
SHELL = (4, 16, 28)
PANEL = (5, 18, 32)
PANEL_2 = (7, 28, 43)
LINE = (42, 105, 128)
LINE_SOFT = (24, 67, 84)
CYAN = (122, 232, 255)
MINT = (153, 246, 228)
TEXT = (244, 250, 255)
MUTED = (154, 183, 201)
MUTED_2 = (108, 135, 153)
GREEN = (30, 160, 135)
DANGER = (222, 82, 96)
DISABLED = (69, 82, 101)


@dataclass(frozen=True)
class VisualOption:
    id: str
    name: str
    rail_width: int
    rail_header: str
    nav: tuple[tuple[str, bool, str], ...]
    row_height: int
    nav_gap: int
    title_large: bool
    badge: str
    editor_style: str
    state_text: str
    dirty: bool
    tray_hover: int
    critique: str


OPTIONS = (
    VisualOption(
        id="VAT-OPT-A",
        name="NDAI Slim Tree Settings",
        rail_width=128,
        rail_header="Tray",
        nav=(("Tray", False, ""), ("Quick Access", True, ".")),
        row_height=20,
        nav_gap=3,
        title_large=True,
        badge="3/4 slots",
        editor_style="table",
        state_text="Saved",
        dirty=False,
        tray_hover=1,
        critique=(
            "Most conservative refinement of the current branch: slim left hierarchy, "
            "compact rows, compact tray menu, and no Settings content that behaves like "
            "a branch status wall."
        ),
    ),
    VisualOption(
        id="VAT-OPT-B",
        name="NDAI Section Rail With Micro Icons",
        rail_width=150,
        rail_header="Nexus",
        nav=(("Tray", False, "N"), ("Quick Access", True, "+")),
        row_height=24,
        nav_gap=4,
        title_large=False,
        badge="3/4 slots",
        editor_style="rail_editor",
        state_text="Unsaved changes",
        dirty=True,
        tray_hover=2,
        critique=(
            "Polished settings-app direction with tiny icons and stronger grouping. "
            "Risk: wider and more generic; reject or trim if the extra rail feels too "
            "much like another application's settings shell."
        ),
    ),
    VisualOption(
        id="VAT-OPT-C",
        name="NDAI Ultra-Slim List Editor",
        rail_width=116,
        rail_header="Tray",
        nav=(("Tray", False, ""), ("Quick Access", True, "")),
        row_height=18,
        nav_gap=2,
        title_large=False,
        badge="3/4 slots",
        editor_style="micro",
        state_text="Saved",
        dirty=False,
        tray_hover=0,
        critique=(
            "Most ShareX-like density target: no big cards, no large icons, a small "
            "settings rail, and a list editor that spends space on the setting rather "
            "than decorative panels."
        ),
    ),
)


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = (
        r"C:\Windows\Fonts\bahnschrift.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


F8 = _font(8)
F9 = _font(9)
F10 = _font(10)
F10B = _font(10, True)
F11 = _font(11)
F11B = _font(11, True)
F12 = _font(12)
F12B = _font(12, True)
F14B = _font(14, True)
F16B = _font(16, True)
F18B = _font(18, True)


def _rr(draw: ImageDraw.ImageDraw, box, radius=8, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _label(
    draw: ImageDraw.ImageDraw,
    box,
    text: str,
    fill=PANEL_2,
    outline=LINE_SOFT,
    text_fill=TEXT,
    font=F10B,
    radius=6,
):
    _rr(draw, box, radius=radius, fill=fill, outline=outline, width=1)
    tb = draw.textbbox((0, 0), text, font=font)
    tx = box[0] + (box[2] - box[0] - (tb[2] - tb[0])) / 2
    ty = box[1] + (box[3] - box[1] - (tb[3] - tb[1])) / 2 - 1
    draw.text((tx, ty), text, fill=text_fill, font=font)


def _wrapped(draw: ImageDraw.ImageDraw, xy, text: str, font=F10, fill=MUTED, width=360, gap=3):
    x, y = xy
    words = text.split()
    line = ""
    lines: list[str] = []
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for line in lines:
        draw.text((x, y), line, fill=fill, font=font)
        y += draw.textbbox((x, y), line, font=font)[3] - draw.textbbox((x, y), line, font=font)[1] + gap
    return y


def _draw_slot_table(draw: ImageDraw.ImageDraw, x: int, y: int, w: int):
    _label(draw, (x + w - 166, y, x + w - 108, y + 26), "Add", font=F10B)
    _label(draw, (x + w - 100, y, x + w, y + 26), "Defaults", font=F10B)
    for i, name in enumerate(("Command Overlay", "Create Task", "Saved Actions Folder")):
        yy = y + 40 + i * 31
        _rr(draw, (x, yy, x + w, yy + 26), 6, fill=PANEL, outline=LINE_SOFT)
        draw.rectangle((x, yy + 4, x + 2, yy + 22), fill=MINT)
        draw.text((x + 16, yy + 7), str(i + 1), fill=CYAN, font=F9)
        _rr(draw, (x + 45, yy + 4, x + 220, yy + 23), 5, fill=BG, outline=(50, 129, 147))
        draw.text((x + 54, yy + 8), name, fill=TEXT, font=F9 if len(name) > 16 else F10B)
        draw.text((x + 202, yy + 7), "v", fill=MINT, font=F9)
        _label(draw, (x + w - 112, yy + 3, x + w - 66, yy + 23), "^ v", fill=(5, 21, 34), font=F9)
        _label(
            draw,
            (x + w - 58, yy + 3, x + w - 6, yy + 23),
            "Delete",
            fill=(34, 12, 18),
            outline=(112, 50, 58),
            text_fill=(255, 210, 214),
            font=F8,
        )


def _draw_rail_editor(draw: ImageDraw.ImageDraw, x: int, y: int, w: int):
    draw.text((x, y), "Quick Access slots", fill=MUTED, font=F10B)
    _label(draw, (x + w - 78, y - 4, x + w, y + 21), "3 of 4", fill=(6, 34, 54), text_fill=CYAN, font=F9)
    for i, name in enumerate(("Command Overlay", "Create Task", "Saved Actions Folder")):
        yy = y + 30 + i * 38
        _rr(draw, (x, yy, x + w, yy + 32), 5, fill=(7, 24, 38), outline=LINE_SOFT)
        draw.text((x + 10, yy + 9), f"{i + 1:02d}", fill=CYAN, font=F10B)
        draw.text((x + 52, yy + 8), name, fill=TEXT, font=F10B)
        _rr(draw, (x + w - 220, yy + 6, x + w - 90, yy + 26), 5, fill=BG, outline=(51, 129, 147))
        draw.text((x + w - 212, yy + 9), "route", fill=MUTED, font=F8)
        _label(draw, (x + w - 82, yy + 6, x + w - 48, yy + 26), "<>" if i == 1 else "--", fill=(4, 20, 32), font=F8)
        _label(
            draw,
            (x + w - 42, yy + 6, x + w - 8, yy + 26),
            "X",
            fill=(34, 12, 18),
            outline=(112, 50, 58),
            text_fill=(255, 210, 214),
            font=F9,
        )
    _label(draw, (x, y + 150, x + 72, y + 175), "Add Slot", font=F9)
    _label(draw, (x + 82, y + 150, x + 174, y + 175), "Use Defaults", font=F9)


def _draw_micro_editor(draw: ImageDraw.ImageDraw, x: int, y: int, w: int):
    for dx, name in ((0, "Slot"), (44, "Action"), (w - 154, "Order"), (w - 70, "Remove")):
        draw.text((x + dx, y), name, fill=MUTED_2, font=F8)
    for i, name in enumerate(("Command Overlay", "Create Task", "Saved Actions Folder")):
        yy = y + 18 + i * 25
        _rr(draw, (x, yy, x + w, yy + 20), 3, fill=PANEL, outline=(17, 52, 68))
        draw.text((x + 10, yy + 5), str(i + 1), fill=CYAN, font=F8)
        _rr(draw, (x + 40, yy + 2, x + 245, yy + 18), 3, fill=BG, outline=(41, 96, 112))
        draw.text((x + 47, yy + 4), name, fill=TEXT, font=F8)
        _label(draw, (x + w - 164, yy + 2, x + w - 112, yy + 18), "^ v", fill=(4, 18, 30), font=F8)
        _label(
            draw,
            (x + w - 70, yy + 2, x + w - 20, yy + 18),
            "Delete",
            fill=(34, 12, 18),
            outline=(112, 50, 58),
            text_fill=(255, 210, 214),
            font=F8,
        )
    _label(draw, (x, y + 130, x + 62, y + 151), "Add", font=F8)
    _label(draw, (x + 70, y + 130, x + 140, y + 151), "Defaults", font=F8)


def _draw_window(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, option: VisualOption):
    _rr(draw, (x, y, x + w, y + h), 20, fill=SHELL, outline=(55, 130, 154))
    _rr(draw, (x + 1, y + 1, x + w - 1, y + 36), 19, fill=(2, 12, 23))
    draw.line((x + 1, y + 36, x + w - 1, y + 36), fill=LINE_SOFT)
    draw.text((x + 14, y + 11), "Global Settings", fill=TEXT, font=F12B)
    _label(draw, (x + w - 66, y + 7, x + w - 43, y + 30), "-", fill=(5, 27, 43), outline=(63, 170, 200), font=F10B)
    _label(draw, (x + w - 36, y + 7, x + w - 13, y + 30), "x", fill=(5, 27, 43), outline=(63, 170, 200), font=F10B)

    body_y = y + 46
    rail_x = x + 14
    draw.line((x + option.rail_width + 12, body_y, x + option.rail_width + 12, y + h - 16), fill=LINE_SOFT)
    draw.text((rail_x, body_y + 8), option.rail_header, fill=MINT, font=F9)
    nav_y = body_y + 32
    for label, selected, icon in option.nav:
        row_box = (rail_x, nav_y, rail_x + option.rail_width - 18, nav_y + option.row_height)
        if selected:
            _rr(draw, row_box, 3, fill=(7, 31, 47))
            draw.rectangle((row_box[0], row_box[1] + 3, row_box[0] + 2, row_box[3] - 3), fill=MINT)
        text_x = row_box[0] + 7
        if icon:
            draw.text((row_box[0] + 7, row_box[1] + 4), icon, fill=MINT if selected else MUTED, font=F8)
            text_x += 19
        draw.text((text_x, row_box[1] + 4), label, fill=TEXT if selected else MUTED, font=F10B if selected else F10)
        nav_y += option.row_height + option.nav_gap

    cx = x + option.rail_width + 30
    cw = w - option.rail_width - 46
    cy = body_y + 10
    draw.text((cx, cy), "Quick Access", fill=TEXT, font=F18B if option.title_large else F16B)
    _label(draw, (x + w - 70, cy - 2, x + w - 16, cy + 24), option.badge, fill=(6, 34, 54), outline=(42, 118, 144), text_fill=CYAN, font=F9)
    cy += 34
    _rr(draw, (cx, cy, x + w - 16, y + h - 82), 10, fill=(3, 14, 26), outline=(20, 61, 78))
    if option.editor_style == "table":
        _draw_slot_table(draw, cx + 12, cy + 10, cw - 24)
    elif option.editor_style == "rail_editor":
        _draw_rail_editor(draw, cx + 12, cy + 10, cw - 24)
    else:
        _draw_micro_editor(draw, cx + 12, cy + 10, cw - 24)

    fy = y + h - 50
    draw.line((cx, fy - 8, x + w - 16, fy - 8), fill=LINE_SOFT)
    draw.text((cx, fy + 6), option.state_text, fill=MINT if "Saved" in option.state_text else CYAN, font=F9)
    _label(draw, (x + w - 168, fy, x + w - 98, fy + 28), "Revert", fill=(14, 24, 41), outline=(40, 64, 86), text_fill=MUTED_2, font=F10B)
    _label(
        draw,
        (x + w - 90, fy, x + w - 16, fy + 28),
        "Save",
        fill=GREEN if option.dirty else (14, 24, 41),
        outline=(55, 160, 138) if option.dirty else (40, 64, 86),
        text_fill=TEXT if option.dirty else MUTED_2,
        font=F10B,
    )
    draw.line((x + w - 18, y + h - 4, x + w - 4, y + h - 18), fill=(65, 150, 168))


def _draw_tray_menu(draw: ImageDraw.ImageDraw, x: int, y: int, option: VisualOption):
    _rr(draw, (x, y, x + 260, y + 222), 10, fill=(8, 11, 16), outline=(78, 82, 92))
    draw.text((x + 14, y + 12), "Tray menu target", fill=TEXT, font=F10B)
    rows = ("Global Settings", "Quick Access >", "AI >", "Exit Nexus")
    enabled = (True, True, True, True)
    yy = y + 38
    for i, row in enumerate(rows):
        if i in (1, 2, 3):
            draw.line((x + 10, yy - 5, x + 250, yy - 5), fill=(48, 50, 58))
        fill = (24, 27, 35) if i == option.tray_hover else (8, 11, 16)
        _rr(draw, (x + 8, yy, x + 252, yy + 26), 4, fill=fill)
        draw.text((x + 18, yy + 7), row, fill=TEXT if enabled[i] else DISABLED, font=F10)
        yy += 31
    draw.text((x + 10, y + 199), "No long status row. Tooltip owns status.", fill=MUTED, font=F8)


def _draw_legend(draw: ImageDraw.ImageDraw, x: int, y: int):
    legends = (
        ("CHROME-001", "Nexus top-level chrome"),
        ("CTRL-001", "compact window controls"),
        ("RAIL-001", "main + subcategory rail"),
        ("NAV-002", "Tray > Quick Access child"),
        ("SLOT-001", "quick-slot row"),
        ("SELECT-001", "route selector/dropdown"),
        ("ACTION-001", "add/defaults/save actions"),
        ("STATE-001", "saved/dirty/blocked truth"),
        ("MENU-001", "right-click tray menu"),
        ("RESIZE-001", "resize affordance"),
    )
    draw.text((x, y), "Element legend", fill=TEXT, font=F12B)
    y += 22
    for code, desc in legends:
        draw.text((x, y), code, fill=MINT, font=F8)
        draw.text((x + 82, y), desc, fill=MUTED, font=F8)
        y += 17


def render_focused(option: VisualOption) -> Image.Image:
    image = Image.new("RGB", (1320, 760), BG)
    draw = ImageDraw.Draw(image)
    draw.text((24, 20), f"{option.id} - {option.name}", fill=TEXT, font=F18B)
    draw.text((24, 46), "Authority: Design Candidate Render - not implementation proof, not LV green", fill=MUTED, font=F11)
    _draw_window(draw, 26, 84, 800, 340, option)
    _draw_tray_menu(draw, 854, 94, option)
    _draw_legend(draw, 854, 340)
    _rr(draw, (24, 450, 1296, 728), 12, fill=(4, 13, 24), outline=LINE_SOFT)
    draw.text((44, 470), "What this option is testing", fill=TEXT, font=F14B)
    _wrapped(draw, (44, 498), option.critique, font=F11, width=560)
    draw.text((690, 470), "Source-grounded constraints", fill=TEXT, font=F14B)
    y = 498
    for item in (
        "Global Settings remains first tray command.",
        "Quick Access lives under Tray as a subcategory/page.",
        "Right-click tray menu stays compact; hover tooltip carries resident status.",
        "No connected-surface/debug/status categories in Settings.",
        "No white/native default window; FAM-002/UIREF visual grammar applies.",
    ):
        draw.text((704, y), f"- {item}", fill=MUTED, font=F10)
        y += 22
    return image


def render_desktop(option: VisualOption) -> Image.Image:
    image = Image.new("RGB", (1920, 1080), (7, 12, 22))
    draw = ImageDraw.Draw(image)
    for yy in range(0, 1040, 80):
        shade = 9 + yy // 160
        draw.rectangle((0, yy, 1920, yy + 80), fill=(shade, 14 + yy // 180, 26 + yy // 170))
    draw.rectangle((0, 1032, 1920, 1080), fill=(13, 18, 26))
    _label(draw, (20, 1040, 54, 1070), "N", fill=(8, 37, 54), outline=(64, 174, 202), font=F12B)
    draw.text((64, 1048), "Nexus Desktop AI", fill=MUTED, font=F11)
    _draw_window(draw, 470, 260, 760, 320, option)
    _draw_tray_menu(draw, 1604, 778, option)
    _label(draw, (1746, 1040, 1778, 1070), "N", fill=(8, 37, 54), outline=(64, 174, 202), font=F12B)
    draw.line((1762, 1034, 1695, 778), fill=CYAN)
    draw.text(
        (470, 606),
        "Footprint: SETTINGS_PANEL, default 760x320, resizable, can remain open briefly while configuring.",
        fill=MUTED,
        font=F12,
    )
    draw.text((24, 22), f"{option.id} full desktop/context render", fill=TEXT, font=F18B)
    draw.text((24, 50), "Shows monitor-space footprint and tray-menu relation. Design candidate only.", fill=MUTED, font=F12)
    return image


def render_state_matrix(option: VisualOption) -> Image.Image:
    image = Image.new("RGB", (1320, 760), BG)
    draw = ImageDraw.Draw(image)
    draw.text((24, 20), f"{option.id} state matrix", fill=TEXT, font=F18B)
    states = (
        ("default", "Normal saved settings."),
        ("hover", "Row/menu hover only, no giant glow."),
        ("focus", "Keyboard/focus ring visible."),
        ("pressed", "Pressed action darkens or fills."),
        ("disabled", "Unavailable routes are muted or hidden."),
        ("empty", "No slots = compact empty guidance."),
        ("blocked/error", "Blocked owner route names safe reason."),
        ("success", "Saved state clears dirty actions."),
        ("dropdown open", "Bounded dark list, no white popup."),
        ("dirty", "Save/Revert active; close guard required."),
        ("resized", "Minimum size keeps rows unclipped."),
        ("tooltip", "Tray hover tooltip preserved for status."),
    )
    card_w, card_h = 300, 120
    for idx, (name, desc) in enumerate(states):
        col = idx % 4
        row = idx // 4
        x = 24 + col * (card_w + 20)
        y = 78 + row * (card_h + 28)
        fill = PANEL
        outline = LINE
        if name == "hover":
            fill = (10, 36, 54)
        if name == "focus":
            outline = MINT
        if name == "pressed":
            fill = GREEN
        if name == "disabled":
            fill = (16, 23, 35)
            outline = (37, 46, 60)
        if name == "blocked/error":
            outline = DANGER
        _rr(draw, (x, y, x + card_w, y + card_h), 10, fill=fill, outline=outline, width=2 if name == "focus" else 1)
        draw.text((x + 14, y + 12), name.upper(), fill=TEXT if name != "disabled" else DISABLED, font=F11B)
        _wrapped(draw, (x + 14, y + 36), desc, font=F10, fill=MUTED if name != "disabled" else DISABLED, width=card_w - 28)
        if name in {"default", "hover", "focus", "pressed", "disabled"}:
            _label(draw, (x + 160, y + 78, x + 270, y + 104), "Save", fill=fill, outline=outline, text_fill=TEXT if name != "disabled" else DISABLED, font=F9)
        elif name == "dropdown open":
            _rr(draw, (x + 154, y + 60, x + 286, y + 104), 6, fill=(3, 12, 21), outline=(54, 131, 149))
            draw.text((x + 166, y + 69), "Command Overlay", fill=TEXT, font=F8)
            draw.text((x + 166, y + 86), "Create Task", fill=MUTED, font=F8)
        elif name == "tooltip":
            _rr(draw, (x + 116, y + 66, x + 286, y + 102), 5, fill=(16, 27, 45), outline=(63, 170, 200))
            _wrapped(draw, (x + 124, y + 73), "Nexus Desktop AI - Local AI idle", font=F8, fill=TEXT, width=150)
    draw.text(
        (24, 704),
        "States marked not applicable in the packet must carry a reason. This matrix is a target-review artifact, not runtime proof.",
        fill=MUTED,
        font=F11,
    )
    return image


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def copy_if_exists(src: Path, dst: Path):
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def clean_roots(stamp: str) -> tuple[Path, Path]:
    proof_root = ROOT / "dev" / "logs" / "fam003_visual_acceptance_target" / stamp
    zip_path = USER_ROOT / f"{PACKET_LABEL}-{stamp}.zip"
    if PACKET_ROOT.exists():
        shutil.rmtree(PACKET_ROOT)
    for existing in USER_ROOT.glob(f"{PACKET_LABEL}-*.zip"):
        existing.unlink()
    for directory in (
        proof_root,
        PACKET_ROOT / "USER Review",
        PACKET_ROOT / "Review Aids",
        PACKET_ROOT / "Source Truth Context",
        PACKET_ROOT / "Render Media",
    ):
        directory.mkdir(parents=True, exist_ok=True)
    return proof_root, zip_path


def render_all(proof_root: Path):
    media_root = proof_root / "render_media"
    packet_media = PACKET_ROOT / "Render Media"
    for option in OPTIONS:
        option_dir = media_root / option.id
        packet_dir = packet_media / f"Option {option.id[-1]}"
        option_dir.mkdir(parents=True, exist_ok=True)
        packet_dir.mkdir(parents=True, exist_ok=True)
        renders = {
            "focused_surface.png": render_focused(option),
            "desktop_context.png": render_desktop(option),
            "state_matrix.png": render_state_matrix(option),
        }
        for name, image in renders.items():
            image.save(option_dir / name)
            image.save(packet_dir / name)

    contact = Image.new("RGB", (1600, 1000), BG)
    draw = ImageDraw.Draw(contact)
    draw.text((24, 18), "FAM-003 Visual Options Contact Sheet", fill=TEXT, font=F18B)
    for idx, option in enumerate(OPTIONS):
        source = Image.open(media_root / option.id / "focused_surface.png")
        thumb = source.resize((500, 288))
        x = 24 + idx * 520
        y = 68
        contact.paste(thumb, (x, y))
        draw.text((x, y + 302), option.id, fill=MINT, font=F12B)
        _wrapped(draw, (x, y + 326), option.name, fill=TEXT, font=F12B, width=470)
        _wrapped(draw, (x, y + 354), option.critique, fill=MUTED, font=F10, width=470)
    y = 610
    draw.text((24, y), "Shared non-negotiables", fill=TEXT, font=F14B)
    y += 28
    for item in (
        "Design Candidate Render only until USER promotes a target.",
        "Visual Acceptance Target must be accepted before future visible UI implementation.",
        "Implementation Match Proof must compare actual screenshots/video against the accepted target.",
        "Current LV1 retest remains not green and not PR-ready.",
    ):
        draw.text((44, y), f"- {item}", fill=MUTED, font=F12)
        y += 24
    contact.save(media_root / "visual_options_contact_sheet.png")
    contact.save(packet_media / "visual_options_contact_sheet.png")


def build_packet_files(stamp: str, proof_root: Path, zip_path: Path):
    source_files = (
        "Docs/Main.md",
        "Docs/nexus_startup_contract.md",
        "Docs/phase_governance.md",
        "Docs/branch_plans/README.md",
        "Docs/nexus_vision.md",
        "Docs/family_visions/FAM-002_desktop_interface.md",
        "Docs/family_visions/FAM-003_interaction_and_actions.md",
        "Docs/family_feature_visions/F3-FF01.md",
        "Docs/family_visions/FAM-006_monitoring_and_hud.md",
        "Docs/family_visions/FAM-007_local_ai_and_capability_packs.md",
        "Docs/family_visions/FAM-008_packaging_and_install_experience.md",
        "Docs/ai_runtime_and_trust_architecture.md",
        "Docs/branch_records/feature_fam_003_resident_access_quick_actions.md",
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
        str(STATE_ROOT / "branch_plan.md"),
        str(STATE_ROOT / "branch_state.md"),
        str(STATE_ROOT / "adoption_reconciliation.md"),
        str(STATE_ROOT / "unified_visual_defect_ledger_20260623.md"),
        str(STATE_ROOT / "unified_defect_ledger_20260623_false_green.md"),
        str(STATE_ROOT / "false_green_incident_20260623_packet_113946.md"),
        str(STATE_ROOT / "stale_output_false_green_incident_20260623_packet_125842.md"),
        "desktop/desktop_renderer.py",
        "desktop/resident_access.py",
        "desktop/tray_controller.py",
        "desktop/orin_desktop_main.py",
        "dev/orin_fam003_settings_repair_visual_validation.py",
        "dev/orin_fam003_resident_access_validation.py",
        "dev/orin_user_review_bundle.py",
        "dev/orin_fam003_visual_acceptance_target_validation.py",
        "dev/orin_fam003_visual_acceptance_target_packet.py",
        r"C:\Nexus USER\UTS - FAM-003.txt",
    )

    write(
        PACKET_ROOT / "START_HERE.md",
        """
        # FAM-003 Visual Acceptance Target Packet

        Primary review file: `USER Review/FAM003_VISUAL_ACCEPTANCE_TARGET_REVIEW.md`

        Review purpose: Select, reject, combine, or revise branch-local visual target direction before any future visible UI/UX implementation or renewed visual repair claims.

        Current gate: Live Validation Stage 1 USER-operated visual retest remains pending for the existing regenerated detailed-UDL packet. This packet is not LV green, not UTS complete, not PR-ready, not merge-ready, not release-ready, and not cleanup-ready.

        USER action: Review the three Design Candidate Renders, use the Visual Selection Ledger to accept/reject/combine/revise elements, and decide whether one candidate should become the Draft Branch Visual Acceptance Target after revision.

        Hash model: The final ZIP SHA256 is recorded outside the ZIP after generation. Packet-internal files intentionally do not contain their own final archive hash.
        """,
    )

    write(
        PACKET_ROOT / "USER Review" / "FAM003_VISUAL_ACCEPTANCE_TARGET_REVIEW.md",
        """
        # FAM-003 Visual Acceptance Target Review

        Verdict requested: choose `ACCEPT OPTION`, `COMBINE`, `REVISE`, or `REJECT ALL` for the visual target direction. This is a design-target review only.

        Current product gate: Live Validation Stage 1 USER-operated visual retest is still pending. This review does not accept LV, does not complete UTS, does not approve PR Readiness, and does not authorize merge, release, cleanup, sibling mutation, Governance mutation, or provider/private/cache/memory work.

        ## Options

        - `VAT-OPT-A`: NDAI Slim Tree Settings. Most conservative refinement of current branch layout.
        - `VAT-OPT-B`: NDAI Section Rail With Micro Icons. Stronger polished settings-app feel, higher width/risk.
        - `VAT-OPT-C`: NDAI Ultra-Slim List Editor. Most ShareX-like density with NDAI chrome identity.

        ## Render Authority

        These files are `Design Candidate Render` artifacts. They are not source truth until USER selection. A `Visual Acceptance Target` becomes binding only after USER accepts it. `Implementation Match Proof` later requires actual app screenshots/video compared against the accepted target.

        ## Media To Inspect

        - `Render Media/visual_options_contact_sheet.png`
        - `Render Media/Option A/focused_surface.png`
        - `Render Media/Option B/focused_surface.png`
        - `Render Media/Option C/focused_surface.png`
        - `Render Media/Option A/desktop_context.png`
        - `Render Media/Option B/desktop_context.png`
        - `Render Media/Option C/desktop_context.png`
        - `Render Media/Option A/state_matrix.png`
        - `Render Media/Option B/state_matrix.png`
        - `Render Media/Option C/state_matrix.png`

        ## Decision Summary

        Use the ledger in `Review Aids/VISUAL_SELECTION_LEDGER_TEMPLATE.md`.

        Required next state before implementation: the draft target must be promoted to `USER_ACCEPTED` or marked `REPAIR_REQUIRED` with exact revision notes.
        """,
    )

    write(
        PACKET_ROOT / "Source Truth Context" / "FILES_LOADED.md",
        "# Files Loaded\n\n"
        + "\n".join(f"- `{item}`" for item in source_files)
        + """

        Missing / stale / conflicting authority found:
        - No promoted UI implementation template or shared primitive exists in `Docs/ui_reference_catalog/index.md`; UIREF records are references, not implementation proof.
        - Current active LV1 packet remains separate from this visual-target packet.
        - Current source truth admits FAM-003 branch-local resident/tray/settings work, but reusable global visual-target enforcement must be Governance Candidate Only.
        """,
    )

    classifications = (
        ("MATERIAL_UI_UX_CHANGE", "Global Settings / Tray / Quick Access has repeated USER visual failures and future repair risk."),
        ("EXISTING_SURFACE_LAYOUT_CHANGE", "Current and future settings organization affects existing Global Settings surfaces."),
        ("NEW_CONTROL_CLUSTER", "Quick-slot selector, row actions, close guard, window controls, and tray menu grouping are control clusters."),
        ("SETTINGS_OR_IA_CHANGE", "Main category and subcategory organization is the core issue."),
        ("STATUS_ERROR_OR_EMPTY_STATE_CHANGE", "Saved/dirty/blocked/disabled/empty states must be designed before implementation."),
        ("VISUAL_SYSTEM_ADOPTION", "FAM-002/UIREF grammar applies, but no shared primitive exists."),
        ("USER_REPORTED_VISUAL_FAILURE", "USER rejected prior settings window quality and density."),
        ("FALSE_GREEN_VISUAL_PROOF_FAILURE", "Prior packet/helper green was insufficient without actual proof and USER visual judgment."),
        ("AMBIGUOUS_VISUAL_CONTRACT", "No global visual-target gate exists yet, so this is branch-local with Governance candidates."),
    )
    write(
        PACKET_ROOT / "Review Aids" / "VISUAL_IMPACT_CLASSIFICATION.md",
        """
        # Visual Impact Classification

        Any classification other than `NO_VISUAL_IMPACT` requires a rendered visual target before future visible UI/UX implementation.

        | Classification | Finding |
        | --- | --- |
        """
        + "\n".join(f"| `{key}` | {value} |" for key, value in classifications)
        + """

        Affected surfaces: Global Settings shell, Tray parent page, Quick Access child page, quick-slot rows, dropdown/list popup, save/revert/defaults/dirty close guard states, native tray right-click menu, tray hover tooltip/status mechanism.
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "VISUAL_OPTIONS_PACKET.md",
        """
        # Visual Options Packet

        Render authority level for all options: `Design Candidate Render`.

        | Option ID | Name | Footprint / Surface | Focused Render | Desktop Context Render | State Matrix | USER Critique Prompt |
        | --- | --- | --- | --- | --- | --- | --- |
        """
        + "\n".join(
            f"| `{option.id}` | {option.name} | SETTINGS_PANEL + tray menu context | `Render Media/Option {option.id[-1]}/focused_surface.png` | `Render Media/Option {option.id[-1]}/desktop_context.png` | `Render Media/Option {option.id[-1]}/state_matrix.png` | {option.critique} |"
            for option in OPTIONS
        )
        + """

        Shared source-truth basis:
        - FAM-003 owns the resident doorway, tray menu organization, tooltip/status mechanism, and minimal Nexus Tray & Quick Access settings foundation.
        - FAM-002/UIREF own reusable visual grammar; this packet does not claim a promoted shared primitive or template exists.
        - FAM-006/FAM-007/FAM-008 surfaces remain owner-bounded dependencies, not settings-window fake categories.
        - Windows tray visibility limitations remain honest; FAM-003 cannot force third-party tray permanence.
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "ELEMENT_LEGENDS_AND_STATE_COVERAGE.md",
        """
        # Element Legends And State Coverage

        | Element ID | Meaning | Required USER Decision Use |
        | --- | --- | --- |
        | `CHROME-001` | Nexus top-level window chrome | Accept/reject frame, title strip, resize affordance. |
        | `CTRL-001` | Compact window controls | Accept/reject minimize/close treatment and hitbox. |
        | `RAIL-001` | Main category and subcategory rail | Accept/reject rail density, icon size, hierarchy. |
        | `NAV-001` | Tray parent category | Accept/reject parent category label and selected state. |
        | `NAV-002` | Quick Access subcategory | Accept/reject child page placement under Tray. |
        | `SLOT-001` | Quick-slot row | Accept/reject density and visual rhythm. |
        | `SELECT-001` | Route selector/dropdown | Accept/reject width, list height, dark popup. |
        | `ACTION-001` | Add / defaults / save actions | Accept/reject action placement and mass. |
        | `STATE-001` | Saved / dirty / blocked truth text | Accept/reject state placement and copy. |
        | `MENU-001` | Tray right-click menu | Accept/reject compact categorized menu shape. |
        | `TOOLTIP-001` | Tray hover tooltip | Must preserve resident status tooltip mechanism. |
        | `RESIZE-001` | Resize affordance | Accept/reject bottom-right affordance. |

        Required state coverage: default, hover, focus, pressed, disabled, empty/no-data, blocked/error, success/complete, dropdown-open, dirty, resized/minimum-size, tray tooltip. If a future target marks any state not applicable, it must use `NOT_APPLICABLE_WITH_REASON`.
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "VISUAL_SELECTION_LEDGER_TEMPLATE.md",
        """
        # Visual Selection Ledger Template

        | Decision ID | Surface | Option ID | Element ID | Accepted / Rejected / Combine / Revise | USER Notes | Source-Truth Impact | Branch-Local vs Durable Design Principle | Implementation Requirement | Proof Requirement | Future Reuse Note |
        | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        | `VSL-001` | Global Settings | `VAT-OPT-?` | `CHROME-001` |  |  |  |  |  |  |  |
        | `VSL-002` | Global Settings rail | `VAT-OPT-?` | `RAIL-001` |  |  |  |  |  |  |  |
        | `VSL-003` | Quick Access rows | `VAT-OPT-?` | `SLOT-001` |  |  |  |  |  |  |  |
        | `VSL-004` | Dropdown/list | `VAT-OPT-?` | `SELECT-001` |  |  |  |  |  |  |  |
        | `VSL-005` | Tray right-click menu | `VAT-OPT-?` | `MENU-001` |  |  |  |  |  |  |  |
        | `VSL-006` | Tray hover tooltip | `VAT-OPT-?` | `TOOLTIP-001` |  |  |  |  |  |  |  |
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
        """
        # Draft Branch Visual Acceptance Target

        Target ID: `FAM003-VAT-20260624-DRAFT`
        Target Status: `DRAFT`

        Selected option(s): `PENDING USER SELECTION`

        No product/runtime UI implementation may proceed from this packet until this target is `USER_ACCEPTED` or a source-truth-governed exception is recorded.

        Required target fields before promotion: selected option(s), selected element decisions, final element map, surface purpose, footprint class, default dimensions, minimum size, resize behavior, state matrix, copy rules, spacing/density rules, button/control rules, status/error/empty rules, accepted references, UIREF obligations, accepted exceptions, source-truth conflict candidates, implementation constraints, proof requirements, implementation-match checklist, and LV gating rule.

        LV gating rule: future LV or UTS cannot claim visual green for affected surfaces until actual implementation proof is compared to the USER-accepted target.
        """,
    )

    rejected_rows = (
        ("RPL-001", "White/native Global Settings shell", "NDAI windows must not look like default white settings dialogs."),
        ("RPL-002", "Oversized left rail icons", "USER rejected large side-panel icons; ShareX-scale small icons or no icons are preferred."),
        ("RPL-003", "Long status/header text in tray right-click menu", "Tray menu stays compact; status belongs in hover tooltip or full owner surfaces."),
        ("RPL-004", "Connected Surfaces/status categories in Global Settings", "USER rejected non-settings branch/dependency status rows in settings."),
        ("RPL-005", "Debug/path/table metadata in product window", "Violates immersion and product-experience rules."),
        ("RPL-006", "Implementation-first visual repair", "Creates repeated USER repair loops and false-green risk."),
        ("RPL-007", "Screenshot existence as acceptance", "UIREF-006 requires adjudication, not screenshot-path-only proof."),
        ("RPL-008", "Local-path-only render proof", "USER packet must include actual media."),
    )
    write(
        PACKET_ROOT / "Review Aids" / "REJECTED_PATTERNS_LEDGER.md",
        """
        # Rejected Patterns Ledger

        | Pattern ID | Rejected UI/UX Pattern | Reason Rejected | Future Avoidance Guidance |
        | --- | --- | --- | --- |
        """
        + "\n".join(
            f"| `{pid}` | {name} | {reason} | Block or explicitly waive before future target promotion. |"
            for pid, name, reason in rejected_rows
        ),
    )

    write(
        PACKET_ROOT / "Review Aids" / "REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
        """
        # Reusable Design Recipe Template

        Status: `TEMPLATE ONLY - fill after USER accepts a Visual Acceptance Target`.

        | Field | Accepted Value |
        | --- | --- |
        | Accepted surface class |  |
        | Accepted footprint class |  |
        | Token values / dimensions |  |
        | Padding |  |
        | Spacing |  |
        | Button heights |  |
        | Font scale |  |
        | Status chip/text pattern |  |
        | Title/header grammar |  |
        | Resize behavior |  |
        | Copy pattern |  |
        | State pattern |  |
        | Accepted comparator references |  |
        | Rejected alternatives |  |
        | Future branch reuse notes |  |
        | Proof requirements |  |
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md",
        """
        # Source-Truth Conflict Classification

        | Candidate Decision / USER Preference | Classification | Disposition |
        | --- | --- | --- |
        | Quick Access lives under Tray with main categories and subcategories | `BRANCH_LOCAL_VISUAL_DECISION` + `NO_CONFLICT` | Supported by current FAM-003 family vision. |
        | Smaller side-rail icons, ShareX-like slim density | `BRANCH_LOCAL_VISUAL_DECISION` | Legal as FAM-003 visual target while consuming FAM-002/UIREF grammar. |
        | Exclusive NDAI Global Settings identity | `BRANCH_LOCAL_VISUAL_DECISION` + possible `FAM-002_REPAIR_REQUIRED` if made global | Current branch may target it; reusable global standard is Governance/FAM-002 candidate only. |
        | Future Tray click/right-click options | `BRANCH_LOCAL_VISUAL_DECISION` + `USER_DECISION_REQUIRED` for implementation | Future-gated; target can reserve IA without fake active controls. |
        | Developer/Owner tray category | `GOVERNANCE_CANDIDATE_ONLY` / FAM-007 future | Must remain hidden/deferred until FAM-007 admits semantics. |
        | AI privacy/provider status in tooltip/menu | `FAMILY_FEATURE_VISION_REPAIR_REQUIRED` only if taxonomy changes | FAM-003 scaffold is dependency evidence; FAM-007 may alter it through BP gates. |
        | Global reusable visual-target gate for all branches | `GOVERNANCE_CANDIDATE_ONLY` | Needs Governance source-truth change, helper/fixture approval, and USER approval. |
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "UDL_FALSE_GREEN_INTEGRATION.md",
        """
        # UDL / False-Green Integration

        Current FAM-003 Visual UDL status: `UDL-VIS-001` through `UDL-VIS-014` are recorded as `CLOSED_WITH_PROOF` for the latest detailed UDL packet. That remains supporting evidence only; USER LV1 retest is still pending.

        This visual-target process prevents future false green by requiring design candidate renders before visible UI implementation, USER_ACCEPTED Visual Acceptance Target before implementation claims, actual render media in the packet rather than local paths only, stable element legends for USER critique, state matrix coverage before LV/UTS, and implementation-match proof against the accepted target before visual green.

        No current-owned UDL defect blocks generating this visual options packet. This packet does not erase known-bad packets, superseded LV packets, stale-output incidents, or the active LV1 retest pending posture.
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "GOVERNANCE_CANDIDATE_ONLY.md",
        """
        # Governance Candidate Only

        | Candidate | Reason | USER Approval Needed |
        | --- | --- | --- |
        | Repo-wide Visual Acceptance Target phase/gate | Current prompt only approves branch-local process. | Approve Governance intake to add source-truth rule, helper expectations, fixtures, and packet schema. |
        | Shared implementation templates or primitives for NDAI settings windows | UIREF index has promoted references but no promoted templates/primitives. | Approve FAM-002/Governance carrier for shared tokens/templates. |
        | Global validator requiring visual targets for every UI diff | Could false-red without precise route rules and fixtures. | Approve helper/validator implementation with positive/negative fixtures. |
        | Durable Global Settings IA beyond FAM-003 Tray & Quick Access | FAM-003 current scope is minimal resident/settings foundation. | Approve a broader branch/FAM owner after branch planning. |
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "ARTIFACT_TO_SURFACE_LEDGER.md",
        """
        # Artifact To Surface Ledger

        | Artifact | Surface / Claim | Authority Level |
        | --- | --- | --- |
        | `Render Media/Option A/focused_surface.png` | Option A focused Settings + tray menu target | Design Candidate Render |
        | `Render Media/Option A/desktop_context.png` | Option A monitor footprint | Design Candidate Render |
        | `Render Media/Option A/state_matrix.png` | Option A state coverage | Design Candidate Render |
        | `Render Media/Option B/focused_surface.png` | Option B focused Settings + tray menu target | Design Candidate Render |
        | `Render Media/Option B/desktop_context.png` | Option B monitor footprint | Design Candidate Render |
        | `Render Media/Option B/state_matrix.png` | Option B state coverage | Design Candidate Render |
        | `Render Media/Option C/focused_surface.png` | Option C focused Settings + tray menu target | Design Candidate Render |
        | `Render Media/Option C/desktop_context.png` | Option C monitor footprint | Design Candidate Render |
        | `Render Media/Option C/state_matrix.png` | Option C state coverage | Design Candidate Render |
        | `Render Media/visual_options_contact_sheet.png` | Cross-option comparison | Design Candidate Render |
        | `Source Truth Context/Current Evidence/01_default_global_settings_shell.png` | Current implementation evidence only | Existing implementation screenshot, not acceptance target |
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "PACKET_MANIFEST.md",
        f"""
        # Packet Manifest

        Packet label: `{PACKET_LABEL}`
        Packet folder: `{PACKET_ROOT}`
        Generated: `{stamp}`
        Review file: `USER Review/FAM003_VISUAL_ACCEPTANCE_TARGET_REVIEW.md`
        Render option count: `3`
        Focused render count: `3`
        Desktop/context render count: `3`
        State matrix render count: `3`
        Contact sheet count: `1`

        Packet hygiene:
        - Active gate-specific folder purged before generation: `YES`
        - Stale matching gate-specific ZIPs removed: `YES`
        - Existing LV1 packet folder `C:\\Nexus USER\\FAM-003` not purged: `PRESERVED`
        - Existing LV1 timestamped ZIPs not removed by this gate-specific packet: `PRESERVED`
        - Final ZIP hash inside packet: `NO`
        """,
    )

    write(
        PACKET_ROOT / "Review Aids" / "VALIDATION_RESULTS.md",
        """
        # Validation Results

        This file records validation intent before final post-ZIP parity. Final packet ZIP SHA256 and post-ZIP parity are recorded outside the ZIP to avoid self-hash contradiction.

        Planned validation set: git identity/status/freshness proof; git diff whitespace checks; FAM-003 visual acceptance target packet validation; FAM-003 settings visual/UDL schema validation; FAM-003 resident access validation; external-state validation; branch governance validation with worktree confinement gate; normal branch governance validation; source owner marker validation; branch readiness planning fixture validation; governance efficiency validation; release-readiness health gate; release body validation; AI provider state validation; compileall for repo helper/code changes.
        """,
    )

    context = PACKET_ROOT / "Source Truth Context"
    copy_if_exists(CURRENT_PROOF_ROOT / "01_default_global_settings_shell.png", context / "Current Evidence" / "01_default_global_settings_shell.png")
    copy_if_exists(CURRENT_PROOF_ROOT / "REFERENCE_CONFORMANCE_CONTACT_SHEET.png", context / "Current Evidence" / "REFERENCE_CONFORMANCE_CONTACT_SHEET.png")
    for src in (
        STATE_ROOT / "unified_visual_defect_ledger_20260623.md",
        STATE_ROOT / "unified_defect_ledger_20260623_false_green.md",
        STATE_ROOT / "false_green_incident_20260623_packet_113946.md",
        STATE_ROOT / "stale_output_false_green_incident_20260623_packet_125842.md",
        ROOT / "Docs" / "family_visions" / "FAM-003_interaction_and_actions.md",
        ROOT / "Docs" / "family_feature_visions" / "F3-FF01.md",
        ROOT / "Docs" / "ui_reference_catalog" / "index.md",
        ROOT / "Docs" / "ui_reference_catalog" / "UIREF-001_top_level_window_frame.md",
        ROOT / "Docs" / "ui_reference_catalog" / "UIREF-002_window_control_cluster.md",
        ROOT / "Docs" / "ui_reference_catalog" / "UIREF-003_control_state_and_selector_grammar.md",
        ROOT / "Docs" / "ui_reference_catalog" / "UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
        ROOT / "Docs" / "ui_reference_catalog" / "UIREF-005_design_token_and_shared_rule_baseline.md",
        ROOT / "Docs" / "ui_reference_catalog" / "UIREF-006_negative_example_and_enforcement_contract.md",
        Path(r"C:\Nexus USER\UTS - FAM-003.txt"),
    ):
        copy_if_exists(src, context / "Source Snapshots" / src.name)

    state_map = {
        "visual_acceptance_target_process_20260624.md": PACKET_ROOT / "START_HERE.md",
        "visual_impact_classification_20260624.md": PACKET_ROOT / "Review Aids" / "VISUAL_IMPACT_CLASSIFICATION.md",
        "visual_options_packet_20260624.md": PACKET_ROOT / "Review Aids" / "VISUAL_OPTIONS_PACKET.md",
        "draft_branch_visual_acceptance_target_20260624.md": PACKET_ROOT / "Review Aids" / "DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
        "visual_selection_ledger_template_20260624.md": PACKET_ROOT / "Review Aids" / "VISUAL_SELECTION_LEDGER_TEMPLATE.md",
        "rejected_patterns_ledger_20260624.md": PACKET_ROOT / "Review Aids" / "REJECTED_PATTERNS_LEDGER.md",
        "reusable_design_recipe_template_20260624.md": PACKET_ROOT / "Review Aids" / "REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
        "source_truth_conflict_classification_20260624.md": PACKET_ROOT / "Review Aids" / "SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md",
        "udl_false_green_integration_20260624.md": PACKET_ROOT / "Review Aids" / "UDL_FALSE_GREEN_INTEGRATION.md",
        "visual_acceptance_target_packet_manifest_20260624.md": PACKET_ROOT / "Review Aids" / "PACKET_MANIFEST.md",
    }
    for name, src in state_map.items():
        copy_if_exists(src, STATE_ROOT / name)


def append_external_receipts(proof_root: Path, zip_path: Path):
    receipt = f"""

## Branch-Local Visual Acceptance Target Packet Receipt - 2026-06-24

Receipt Timestamp: `{dt.datetime.now().isoformat(timespec='seconds')}`
Task Type: `FAM-003 branch-local UI/UX Visual Acceptance Target process and USER packet generation; no product/runtime UI implementation, no renewed LV/UTS acceptance, no PR, merge, release, cleanup, issue, sibling, Governance, neutral-main, provider/model/private/cache/memory, installer/startup/shortcut/packaging mutation.`
Legal Carrier: `C:\\Nexus Worktrees\\FAM-003` on `feature/fam-003-resident-access-quick-actions`.
Current Gate Preserved: `Live Validation Stage 1 - USER-operated visual retest remains pending; this visual-target packet is not LV green, not UTS complete, not PR-ready, not merge-ready, not release-ready, and not cleanup-ready.`
Visual Impact Classification: `MATERIAL_UI_UX_CHANGE; EXISTING_SURFACE_LAYOUT_CHANGE; NEW_CONTROL_CLUSTER; SETTINGS_OR_IA_CHANGE; STATUS_ERROR_OR_EMPTY_STATE_CHANGE; VISUAL_SYSTEM_ADOPTION; AMBIGUOUS_VISUAL_CONTRACT; USER_REPORTED_VISUAL_FAILURE; FALSE_GREEN_VISUAL_PROOF_FAILURE.`
Visual Options Packet: `{PACKET_ROOT}\\Review Aids\\VISUAL_OPTIONS_PACKET.md`
Render Media Root: `{proof_root}\\render_media`
USER Packet Folder: `{PACKET_ROOT}`
USER Packet ZIP Path: `{zip_path}`
Hash Recording Model: `Final ZIP SHA256 is recorded after ZIP generation in active external state and Codex return output only; packet-internal files intentionally do not contain their own final hash.`
Branch-Local Helper: `dev/orin_fam003_visual_acceptance_target_validation.py validates packet media, legends, ledgers, draft target, templates, external state files, and folder/ZIP parity. It is branch-local support evidence only and does not prove USER acceptance.`
Governance Candidate Only: `Reusable repo-wide Visual Acceptance Target gate, global helper/fixture enforcement, and shared settings primitives/templates require separate Governance/FAM-002 approval.`
Next Legal Phase: `USER review of the FAM-003 Visual Acceptance Target packet. If USER accepts or revises a target that differs from current implementation, route to the correct bounded repair before renewed LV1 retest. If USER accepts current-equivalent target with no implementation delta, LV1 USER-operated retest may continue from the current source-truth packet after Codex digests that decision.`
"""
    for path in (STATE_ROOT / "branch_plan.md", STATE_ROOT / "branch_state.md", STATE_ROOT / "adoption_reconciliation.md", WORKTREE_STATE):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        marker = "\n## Branch-Local Visual Acceptance Target Packet Receipt - 2026-06-24"
        if marker in text:
            text = text[: text.index(marker)]
        path.write_text(text.rstrip() + receipt + "\n", encoding="utf-8")


def zip_packet(zip_path: Path) -> str:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKET_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKET_ROOT).as_posix())
    return hashlib.sha256(zip_path.read_bytes()).hexdigest().upper()


def main() -> int:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    proof_root, zip_path = clean_roots(stamp)
    render_all(proof_root)
    build_packet_files(stamp, proof_root, zip_path)
    append_external_receipts(proof_root, zip_path)
    digest = zip_packet(zip_path)
    summary = {
        "stamp": stamp,
        "packet_folder": str(PACKET_ROOT),
        "zip_path": str(zip_path),
        "zip_sha256": digest,
        "proof_root": str(proof_root),
        "folder_file_count": len([path for path in PACKET_ROOT.rglob("*") if path.is_file()]),
    }
    write(proof_root / "visual_acceptance_target_generation_summary.json", json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
