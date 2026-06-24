"""Generate and validate the FAM-007 visual acceptance target USER packet.

Helper Status: Workstream-scoped
Owner Workstream: FAM-007 AI Dashboard / AI Control Center visual target gate
Reason Reusable Helper Was Not Extended: this pass is branch-local and depends on
the active FAM-007 external state, current proof roots, and accepted historical
packet retention rules.
Consolidation Target: future reusable visual-target packet helper after
Governance/FAM-002 defines a global template.
Promotion Decision Point: before PR Readiness or when a second branch needs the
same visual-target packet contract.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKTREE_LABEL = "FAM-007"
BRANCH_SLUG = "feature_fam_007_ai_control_center_readiness_diagnostics"
EXTERNAL_BRANCH_ROOT = Path(r"C:\Nexus Governance State\branches") / BRANCH_SLUG
BRANCH_STATE = EXTERNAL_BRANCH_ROOT / "branch_state.md"
BRANCH_PLAN = EXTERNAL_BRANCH_ROOT / "branch_plan.md"
UDL_PATH = EXTERNAL_BRANCH_ROOT / "unified_defect_ledger.md"
USER_ROOT = Path(r"C:\Nexus USER")
PACKET_DIR = USER_ROOT / WORKTREE_LABEL
ACCEPTED_HISTORICAL_ZIP = USER_ROOT / "FAM-007-20260623-123429.zip"
PRIMARY_REVIEW_FILE = "VISUAL_ACCEPTANCE_TARGET_REVIEW.md"
RECOVERY_PRIMARY_REVIEW_FILE = "ACCEPTED_HISTORICAL_PACKET_RECOVERY_REVIEW.md"
BLOCKED_GATES = (
    "H1/LV acceptance; USER UTS acceptance; PR Readiness; PR creation; merge; release; "
    "cleanup; issue mutation; provider/model execution; prompt send; downloads; runtime "
    "cache behavior; memory/learning/personalization; private Developer/Owner setup; "
    "installer/shortcut/packaging execution; sibling/Governance mutation; imports; "
    "v1.8.0 work."
)
VISUAL_PACKET_PURPOSE = (
    "Branch-local visual acceptance target process and review packet. It creates rendered "
    "targets, legends, selection ledgers, a draft target, rejected-pattern and reusable-"
    "recipe templates, and validation evidence before any future visible UI/UX "
    "implementation."
)
VISUAL_NEXT_LEGAL_PHASE = (
    "USER review of the branch-local Visual Acceptance Target packet only. H1/LV "
    "acceptance, the later LV1 review gate, USER UTS acceptance, and PR Readiness "
    "remain separate pending gates requiring later source-truth-routed USER decisions "
    "after this packet is accepted or revised."
)
RECOVERY_NEXT_LEGAL_PHASE = (
    "USER decision on the accepted-historical packet recovery / retention blocker packet. "
    "USER may provide the missing accepted historical ZIP, approve a retention waiver, "
    "or hold the packet chain blocked until the artifact is recovered."
)
PROOF_ROOT = Path(
    r"C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI"
    r"\FAM-007-H4\20260623-112831-child-window"
)
PROOF_LOG_ROOT = REPO_ROOT / "dev" / "logs" / "fam_007_ai_control_center_live_resize" / "20260623-112831"
MANIFEST_PATH = PROOF_LOG_ROOT / "live_resize_manifest.json"

REQUIRED_PACKET_FILES = [
    "START_HERE.md",
    "USER Review/VISUAL_ACCEPTANCE_TARGET_REVIEW.md",
    "Review Aids/VISUAL_IMPACT_CLASSIFICATION.md",
    "Review Aids/VISUAL_OPTIONS_PACKET.md",
    "Review Aids/ELEMENT_LEGENDS.md",
    "Review Aids/ANNOTATION_MANIFEST.md",
    "Review Aids/STATE_COVERAGE_MATRIX.md",
    "Review Aids/VISUAL_SELECTION_LEDGER_TEMPLATE.md",
    "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
    "Review Aids/REJECTED_PATTERNS_LEDGER.md",
    "Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
    "Review Aids/SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md",
    "Review Aids/GOVERNANCE_CANDIDATE_ONLY.md",
    "Review Aids/UDL_FALSE_GREEN_STATUS.md",
    "Review Aids/VALIDATION_SUMMARY.md",
    "Source Truth Context/current_external_branch_state.md",
    "Source Truth Context/current_external_branch_plan.md",
    "Source Truth Context/branch_record.md",
    "Source Truth Context/validation_helper_registry.md",
    "Source Truth Context/ui_reference_catalog_index.md",
    "Source Truth Context/UIREF-001_top_level_window_frame.md",
    "Source Truth Context/UIREF-002_window_control_cluster.md",
    "Source Truth Context/UIREF-003_control_state_and_selector_grammar.md",
    "Source Truth Context/UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
    "Source Truth Context/UIREF-005_design_token_and_shared_rule_baseline.md",
    "Source Truth Context/UIREF-006_negative_example_and_enforcement_contract.md",
]


@dataclass(frozen=True)
class RenderOption:
    option_id: str
    authority: str
    footprint: str
    focused_media: str
    desktop_media: str
    annotated_focused_media: str
    annotated_desktop_media: str
    description: str


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(relative_path: str, text: str) -> None:
    target = PACKET_DIR / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + "\n", encoding="utf-8")


def _copy_file(source: Path, relative_path: str) -> None:
    target = PACKET_DIR / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _packet_file_entries() -> list[Path]:
    return sorted(path for path in PACKET_DIR.rglob("*") if path.is_file())


def _zip_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _accepted_historical_zips() -> set[Path]:
    text = ""
    for source in (BRANCH_STATE, BRANCH_PLAN):
        if source.exists():
            text += "\n" + _read_text(source)
    accepted = {Path(match.group(1)) for match in re.finditer(r"Accepted Historical Packet:\s*`([^`]+\.zip)`", text)}
    accepted.add(ACCEPTED_HISTORICAL_ZIP)
    return accepted


def _purge_packet_root() -> None:
    if PACKET_DIR.exists():
        shutil.rmtree(PACKET_DIR)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    accepted = _accepted_historical_zips()
    for zip_path in USER_ROOT.glob(f"{WORKTREE_LABEL}-*.zip"):
        if zip_path not in accepted:
            zip_path.unlink()
    stable_zip = USER_ROOT / f"{WORKTREE_LABEL}.zip"
    if stable_zip.exists():
        stable_zip.unlink()


def _update_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(field)}: `.*?`$", re.MULTILINE)
    replacement = f"{field}: `{value}`"
    if pattern.search(text):
        return pattern.sub(lambda _match: replacement, text, count=1)
    return text.rstrip() + "\n" + replacement + "\n"


def _replace_section(text: str, heading: str, lines: list[str]) -> str:
    replacement = "\n".join([heading, "", *lines]).rstrip()
    pattern = re.compile(rf"^{re.escape(heading)}\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        return pattern.sub(lambda _match: replacement + "\n\n", text, count=1)
    return text.rstrip() + "\n\n" + replacement + "\n"


def _section(text: str, heading: str) -> str:
    text = text.replace("\r\n", "\n")
    match = re.search(rf"^{re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    return match.group("body") if match else ""


def _visual_exact_user_decision_text(zip_path: Path) -> str:
    return (
        f"I accept the FAM-007 branch-local Visual Acceptance Target packet at {zip_path} "
        "as the current USER review packet for visual target/process selection only. I "
        "accept that the visible current review surface is USER Review/"
        f"{PRIMARY_REVIEW_FILE}, that packet validation is not USER acceptance, and that "
        f"the accepted historical packet {ACCEPTED_HISTORICAL_ZIP} remains preserved as "
        "historical evidence only. This does not approve H1/LV acceptance, the later "
        "LV1 review gate, USER UTS acceptance, PR Readiness, PR creation, merge, release, "
        "cleanup, issue mutation, provider/model execution, prompt send, downloads, "
        "runtime cache behavior, memory/learning/personalization, private Developer/Owner "
        "setup, installer/shortcut/packaging execution, sibling/Governance mutation, "
        "imports, or v1.8.0 work."
    )


def _visual_next_legal_phase_lines(zip_path: Path) -> list[str]:
    return [
        f"Next Legal Phase: `{VISUAL_NEXT_LEGAL_PHASE}`",
        f"Exact USER Decision Text: `{_visual_exact_user_decision_text(zip_path)}`",
    ]


def _recovery_exact_user_decision_text(zip_path: Path) -> str:
    return (
        f"I accept the FAM-007 accepted-historical packet recovery / retention blocker "
        f"packet at {zip_path}. I understand that {ACCEPTED_HISTORICAL_ZIP} was not found "
        "in the searched local roots, that Codex did not recreate or fake the accepted "
        "historical artifact, and that the current packet chain remains blocked unless I "
        "provide/upload the missing ZIP, approve a retention waiver, or direct a later "
        "source-truth-routed recovery path. This does not approve H1/LV acceptance, USER "
        "UTS acceptance, PR Readiness, PR creation, merge, release, unrelated cleanup, "
        "issue mutation, provider/model execution, prompt send, downloads, runtime cache "
        "behavior, memory/learning/personalization, private Developer/Owner setup, "
        "installer/shortcut/packaging execution, sibling/Governance mutation, imports, "
        "or v1.8.0 work."
    )


def _recovery_next_legal_phase_lines(zip_path: Path) -> list[str]:
    return [
        f"Next Legal Phase: `{RECOVERY_NEXT_LEGAL_PHASE}`",
        f"Exact USER Decision Text: `{_recovery_exact_user_decision_text(zip_path)}`",
    ]


def _update_branch_state_for_visual_packet(text: str, zip_path: Path) -> str:
    text = _update_field(
        text,
        "External State Item Status",
        (
            f"Current USER review packet is the branch-local Visual Acceptance Target packet "
            f"{zip_path}. It is a reviewable visual-target/process packet only. The accepted "
            f"historical Workstream implementation / H1-LV proof packet "
            f"{ACCEPTED_HISTORICAL_ZIP} remains preserved as historical evidence. H1/LV "
            f"acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, "
            f"cleanup, issue mutation, provider/model execution, prompt send, downloads, "
            f"runtime cache behavior, memory/learning/personalization, private Developer/Owner "
            f"setup, installer/shortcut/packaging execution, sibling/Governance mutation, "
            f"imports, and v1.8.0 remain blocked."
        ),
    )
    text = _update_field(
        text,
        "Current Gate",
        (
            "USER review of the branch-local Visual Acceptance Target packet; the underlying "
            "Hardening H1 / Live Validation decision gate remains pending separate USER "
            "approval and is not accepted by this packet."
        ),
    )
    text = _update_field(
        text,
        "Packet Reviewability State",
        (
            f"Visual Acceptance Target packet generated for USER review at {zip_path}; "
            "packet validation is supporting evidence only and is not USER acceptance."
        ),
    )
    text = _update_field(
        text,
        "USER Gate State",
        (
            "Pending USER review of the Visual Acceptance Target packet; H1/LV acceptance "
            "and USER UTS acceptance remain pending separate USER decision."
        ),
    )
    text = _update_field(
        text,
        "Next Legal Phase",
        VISUAL_NEXT_LEGAL_PHASE,
    )
    return _replace_section(text, "## Next Legal Phase", _visual_next_legal_phase_lines(zip_path))


def _update_branch_plan_for_visual_packet(text: str, zip_path: Path) -> str:
    text = _replace_section(
        text,
        "## Packet Review State",
        [
            (
                "Packet Reviewability State: `Reviewable branch-local Visual Acceptance Target "
                f"packet at {zip_path}. Packet validation is not USER acceptance; this packet "
                "does not accept H1/LV, USER UTS, PR Readiness, PR creation, merge, release, "
                "or runtime/provider/private/cache/memory/download/packaging work.`"
            ),
            "RAR Packet Reviewability State: `Accepted historical RAR evidence remains context only; this Visual Acceptance Target packet is the current USER review packet.`",
            "USER Gate State: `Pending USER review of the Visual Acceptance Target packet; H1/LV resume requires separate approval.`",
            f"Primary USER Review File: `{PRIMARY_REVIEW_FILE}`",
            f"USER Review Folder: `{PACKET_DIR}`",
            f"USER Review ZIP: `{zip_path}`",
            "Packet Validation Is USER Acceptance: `No`",
        ],
    )
    return _replace_section(text, "## Next Legal Phase", _visual_next_legal_phase_lines(zip_path))


def _update_branch_state_for_recovery_packet(text: str, zip_path: Path) -> str:
    text = _update_field(
        text,
        "External State Item Status",
        (
            f"Current USER review packet is the accepted-historical packet recovery / "
            f"retention blocker packet {zip_path}. The accepted historical Workstream "
            f"implementation / H1-LV proof packet {ACCEPTED_HISTORICAL_ZIP} is missing "
            f"from local retained artifacts after required search and is not currently "
            f"preserved. H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, "
            f"merge, release, unrelated cleanup, issue mutation, provider/model execution, "
            f"prompt send, downloads, runtime cache behavior, memory/learning/personalization, "
            f"private Developer/Owner setup, installer/shortcut/packaging execution, "
            f"sibling/Governance mutation, imports, and v1.8.0 remain blocked."
        ),
    )
    text = _update_field(
        text,
        "Current Gate",
        (
            "USER review of the accepted-historical packet recovery / retention blocker "
            "packet; the missing accepted historical ZIP must be provided, waived, or kept "
            "as a blocker before the Visual Acceptance Target packet can be accepted."
        ),
    )
    text = _update_field(
        text,
        "Packet Reviewability State",
        (
            f"Accepted-historical recovery / retention blocker packet generated for USER "
            f"review at {zip_path}; packet validation is supporting evidence only and is "
            "not USER acceptance."
        ),
    )
    text = _update_field(
        text,
        "USER Gate State",
        (
            "Pending USER review of accepted-historical artifact recovery / retention "
            "blocker; H1/LV acceptance and USER UTS acceptance remain pending separate "
            "USER decision."
        ),
    )
    text = _update_field(text, "Next Legal Phase", RECOVERY_NEXT_LEGAL_PHASE)
    return _replace_section(text, "## Next Legal Phase", _recovery_next_legal_phase_lines(zip_path))


def _update_branch_plan_for_recovery_packet(text: str, zip_path: Path) -> str:
    text = _replace_section(
        text,
        "## Packet Review State",
        [
            (
                "Packet Reviewability State: `Reviewable accepted-historical packet "
                f"recovery / retention blocker packet at {zip_path}. Packet validation is "
                "not USER acceptance; the accepted historical ZIP is missing and is not "
                "claimed preserved by this active packet.`"
            ),
            "Accepted Historical Packet: `MISSING - C:\\Nexus USER\\FAM-007-20260623-123429.zip was not recovered in searched local roots.`",
            "USER Gate State: `Pending USER review of recovery / waiver / blocked-chain decision.`",
            f"Primary USER Review File: `{RECOVERY_PRIMARY_REVIEW_FILE}`",
            f"USER Review Folder: `{PACKET_DIR}`",
            f"USER Review ZIP: `{zip_path}`",
            "Packet Validation Is USER Acceptance: `No`",
        ],
    )
    return _replace_section(text, "## Next Legal Phase", _recovery_next_legal_phase_lines(zip_path))


def _append_receipt(path: Path, heading: str, lines: list[str]) -> None:
    text = _read_text(path)
    if heading in text:
        return
    body = "\n\n" + heading + "\n\n" + "\n".join(lines) + "\n"
    path.write_text(text.rstrip() + body, encoding="utf-8")


def _remove_visual_target_receipts(path: Path) -> None:
    text = _read_text(path)
    cleaned = re.sub(
        r"\n## Branch-Local Visual Acceptance Target Packet Receipt - .+?(?=\n## |\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    if cleaned != text:
        path.write_text(cleaned.rstrip() + "\n", encoding="utf-8")


def _update_external_state(zip_path: Path) -> None:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    head = _git_value("rev-parse", "HEAD")
    origin_main = _git_value("rev-parse", "origin/main")
    for path in (BRANCH_STATE, BRANCH_PLAN):
        text = _read_text(path)
        text = _update_field(text, "Last Updated", now)
        text = _update_field(text, "Source Repo HEAD", head)
        text = _update_field(text, "Source origin/main", origin_main)
        text = _update_field(text, "USER Review ZIP", str(zip_path))
        if path == BRANCH_STATE:
            text = _update_branch_state_for_visual_packet(text, zip_path)
        if path == BRANCH_PLAN:
            text = _update_branch_plan_for_visual_packet(text, zip_path)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        _remove_visual_target_receipts(path)
        _append_receipt(
            path,
            f"## Branch-Local Visual Acceptance Target Packet Receipt - {now}",
            [
                "Receipt Status: `VISUAL_ACCEPTANCE_TARGET_PACKET_GENERATED_PENDING_USER_REVIEW`",
                f"USER Review ZIP: `{zip_path}`",
                f"Accepted Historical Packet: `{ACCEPTED_HISTORICAL_ZIP}`",
                f"Packet Purpose: `{VISUAL_PACKET_PURPOSE}`",
                "Implementation Status: `No product/runtime UI implementation authorized or performed by this packet.`",
                f"Blocked Gates: `{BLOCKED_GATES}`",
            ],
        )
    if UDL_PATH.exists():
        udl_text = _read_text(UDL_PATH)
        udl_text = re.sub(
            r"^Current HEAD: `.*?`$",
            f"Current HEAD: `{head}`",
            udl_text,
            count=1,
            flags=re.MULTILINE,
        )
        classification = (
            "Current HEAD Field Classification: `Active current packet metadata; refreshed "
            "during Visual Acceptance Target packet regeneration so copied Source Truth "
            "Context cannot be mistaken for stale proof-snapshot truth.`"
        )
        if "Current HEAD Field Classification:" not in udl_text:
            udl_text = udl_text.replace(f"Current HEAD: `{head}`", f"Current HEAD: `{head}`\n{classification}", 1)
        else:
            udl_text = re.sub(
                r"^Current HEAD Field Classification: `.*?`$",
                classification,
                udl_text,
                count=1,
                flags=re.MULTILINE,
            )
        UDL_PATH.write_text(udl_text.rstrip() + "\n", encoding="utf-8")


def _update_external_state_for_recovery_packet(zip_path: Path) -> None:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    head = _git_value("rev-parse", "HEAD")
    origin_main = _git_value("rev-parse", "origin/main")
    for path in (BRANCH_STATE, BRANCH_PLAN):
        text = _read_text(path)
        text = _update_field(text, "Last Updated", now)
        text = _update_field(text, "Source Repo HEAD", head)
        text = _update_field(text, "Source origin/main", origin_main)
        text = _update_field(text, "USER Review ZIP", str(zip_path))
        if path == BRANCH_STATE:
            text = _update_branch_state_for_recovery_packet(text, zip_path)
        if path == BRANCH_PLAN:
            text = _update_branch_plan_for_recovery_packet(text, zip_path)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        _append_receipt(
            path,
            f"## Accepted-Historical Packet Recovery / Retention Blocker Receipt - {now}",
            [
                "Receipt Status: `ACCEPTED_HISTORICAL_PACKET_MISSING_BLOCKER_PACKET_GENERATED_PENDING_USER_REVIEW`",
                f"USER Review ZIP: `{zip_path}`",
                f"Missing Accepted Historical Packet: `{ACCEPTED_HISTORICAL_ZIP}`",
                "Recovery Result: `NOT RECOVERED - do not fake preservation or convert missing historical artifact into PASS.`",
                "Packet Purpose: `USER decision packet for accepted-historical artifact recovery, retention waiver, or blocked-chain disposition.`",
                f"Blocked Gates: `{BLOCKED_GATES}`",
            ],
        )
    if UDL_PATH.exists():
        udl_text = _read_text(UDL_PATH)
        udl_text = re.sub(
            r"^Current HEAD: `.*?`$",
            f"Current HEAD: `{head}`",
            udl_text,
            count=1,
            flags=re.MULTILINE,
        )
        classification = (
            "Current HEAD Field Classification: `Active current packet metadata; refreshed "
            "during accepted-historical recovery blocker packet regeneration so copied "
            "Source Truth Context cannot be mistaken for stale proof-snapshot truth.`"
        )
        if "Current HEAD Field Classification:" not in udl_text:
            udl_text = udl_text.replace(f"Current HEAD: `{head}`", f"Current HEAD: `{head}`\n{classification}", 1)
        else:
            udl_text = re.sub(
                r"^Current HEAD Field Classification: `.*?`$",
                classification,
                udl_text,
                count=1,
                flags=re.MULTILINE,
            )
        if "F7-UDL-018" not in udl_text:
            udl_text += (
                "\n\n## F7-UDL-018 Accepted-Historical Artifact Missing - 2026-06-24\n\n"
                "Status: `BLOCKED_SOURCE_TRUTH`\n"
                f"Missing Artifact: `{ACCEPTED_HISTORICAL_ZIP}`\n"
                "Finding: `The accepted historical Workstream implementation / H1-LV proof packet is not present in the retained local USER packet root, Recycle Bin, known local workspaces, user profile roots, OneDrive roots, Downloads/Documents/Desktop, artifact roots, or Codex attachment cache searched by this recovery pass.`\n"
                "Required Disposition: `USER must provide/upload the missing ZIP, approve an explicit retention waiver, or keep the packet chain blocked until recovered.`\n"
                "No-Fake-Preservation Rule: `Do not recreate the accepted historical packet or claim it is preserved without the original artifact bytes or an explicit USER waiver/source-truth disposition.`\n"
                f"Current Recovery Packet: `{zip_path}`\n"
            )
        else:
            udl_text = re.sub(
                r"^Current Recovery Packet: `.*?`$",
                lambda _match: f"Current Recovery Packet: `{zip_path}`",
                udl_text,
                flags=re.MULTILINE,
            )
        UDL_PATH.write_text(udl_text.rstrip() + "\n", encoding="utf-8")


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (Path(r"C:\Windows\Fonts\segoeui.ttf"), Path(r"C:\Windows\Fonts\arial.ttf")):
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def _draw_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, lines: list[str]) -> None:
    draw.rounded_rectangle(box, radius=18, fill=(5, 24, 38), outline=(66, 185, 210), width=2)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 58, y1 + 52), radius=12, fill=(8, 54, 74), outline=(76, 214, 234))
    draw.text((x1 + 28, y1 + 25), "ID", fill=(158, 240, 237), font=_font(11))
    draw.text((x1 + 74, y1 + 19), title.upper(), fill=(235, 248, 252), font=_font(18))
    yy = y1 + 56
    for line in lines:
        draw.text((x1 + 74, yy), line, fill=(158, 205, 213), font=_font(13))
        yy += 23
    button_y = y2 - 50
    draw.rounded_rectangle((x2 - 186, button_y, x2 - 24, button_y + 30), radius=15, fill=(7, 34, 49), outline=(61, 168, 198), width=2)
    draw.text((x2 - 166, button_y + 8), "OPEN SURFACE", fill=(226, 245, 249), font=_font(11))


ANNOTATION_ELEMENTS = [
    ("CHROME-001", "cyan box", "NDAI custom window frame / shell"),
    ("CTRL-001", "yellow circle", "compact window control cluster"),
    ("TITLE-001", "magenta bracket", "title strip and subtitle copy"),
    ("PANEL-001", "green box", "category doorway card or panel body"),
    ("ACTION-001", "amber arrow", "primary open/action button"),
    ("STATUS-001", "blue bracket", "compact AI/provider/trust status"),
]


def _annotation_targets(width: int, height: int, *, desktop: bool) -> dict[str, tuple[int, int, int, int]]:
    if desktop:
        x, y, win_w, win_h = 850, 82, 650, 620
    else:
        x, y, win_w, win_h = 48, 48, 650, 620
    return {
        "CHROME-001": (x, y, x + win_w, y + win_h),
        "CTRL-001": (x + win_w - 136, y + 32, x + win_w - 38, y + 76),
        "TITLE-001": (x + 40, y + 36, x + 430, y + 126),
        "PANEL-001": (x + 30, y + 168, x + win_w - 30, y + 502),
        "ACTION-001": (x + win_w - 220, y + 270, x + win_w - 44, y + 486),
        "STATUS-001": (x + 30, y + 510, x + win_w - 30, y + 674),
    }


def _draw_callout(
    draw: ImageDraw.ImageDraw,
    label: str,
    target: tuple[int, int, int, int],
    index: int,
    *,
    color: tuple[int, int, int],
    shape: str,
) -> None:
    x1, y1, x2, y2 = target
    draw.rounded_rectangle(target, radius=12, outline=color, width=4)
    anchor_x = x1 if index % 2 == 0 else x2
    anchor_y = y1 + max(16, min(44, (y2 - y1) // 3))
    label_x = max(18, min(x1 - 118 if index % 2 == 0 else x2 + 18, 1450))
    label_y = max(18, min(y1 + (index % 3) * 18, 820))
    if label_x > x1:
        label_x = min(label_x, max(18, x2 + 18))
    label_box = (label_x, label_y, label_x + 104, label_y + 28)
    draw.line((anchor_x, anchor_y, label_x + 52, label_y + 28), fill=color, width=3)
    draw.rounded_rectangle(label_box, radius=10, fill=(1, 14, 23), outline=color, width=3)
    if shape == "circle":
        draw.ellipse((label_x + 7, label_y + 7, label_x + 21, label_y + 21), outline=color, width=3)
    elif shape == "bracket":
        draw.line((label_x + 8, label_y + 7, label_x + 8, label_y + 21), fill=color, width=3)
        draw.line((label_x + 8, label_y + 7, label_x + 20, label_y + 7), fill=color, width=3)
        draw.line((label_x + 8, label_y + 21, label_x + 20, label_y + 21), fill=color, width=3)
    elif shape == "arrow":
        draw.polygon([(label_x + 8, label_y + 14), (label_x + 22, label_y + 7), (label_x + 22, label_y + 21)], fill=color)
    else:
        draw.rectangle((label_x + 7, label_y + 7, label_x + 21, label_y + 21), outline=color, width=3)
    draw.text((label_x + 28, label_y + 8), label, fill=(238, 248, 252), font=_font(10))


def _annotate_render(source: Path, target: Path, option_id: str, *, desktop: bool) -> list[dict[str, str]]:
    colors = [
        (80, 218, 238),
        (236, 202, 89),
        (230, 112, 225),
        (92, 220, 156),
        (242, 166, 80),
        (105, 164, 255),
    ]
    shapes = ["box", "circle", "bracket", "box", "arrow", "bracket"]
    with Image.open(source) as image:
        annotated = image.convert("RGB")
    draw = ImageDraw.Draw(annotated)
    targets = _annotation_targets(*annotated.size, desktop=desktop)
    rows: list[dict[str, str]] = []
    for index, (element_id, cue, purpose) in enumerate(ANNOTATION_ELEMENTS, start=1):
        marker_id = f"{option_id}-A{index:02d}"
        target_box = targets[element_id]
        color = colors[index - 1]
        _draw_callout(draw, marker_id, target_box, index, color=color, shape=shapes[index - 1])
        rows.append(
            {
                "option": option_id,
                "annotation": marker_id,
                "element": element_id,
                "cue": cue,
                "region": f"{target_box[0]},{target_box[1]},{target_box[2]},{target_box[3]}",
                "purpose": purpose,
                "file": str(target.relative_to(PACKET_DIR)).replace("\\", "/"),
            }
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    annotated.save(target)
    return rows


def _draw_option_mockup(path: Path, option: str, title: str, subtitle: str, desktop: bool) -> None:
    width, height = (1600, 900) if desktop else (760, 760)
    img = Image.new("RGB", (width, height), (0, 5, 8))
    draw = ImageDraw.Draw(img)
    for radius in range(80, 420, 60):
        draw.ellipse((130 - radius, 340 - radius, 130 + radius, 340 + radius), outline=(8, 47, 62), width=1)
    win_w, win_h = 650, 620
    x = 850 if desktop else 48
    y = 82 if desktop else 48
    draw.rounded_rectangle((x, y, x + win_w, y + win_h), radius=28, fill=(3, 14, 25), outline=(65, 183, 214), width=2)
    draw.rounded_rectangle((x + 26, y + 24, x + win_w - 26, y + 128), radius=24, fill=(5, 22, 35), outline=(25, 96, 119), width=1)
    draw.text((x + 48, y + 42), "NEXUS DESKTOP AI", fill=(96, 220, 239), font=_font(13))
    draw.text((x + 48, y + 66), title, fill=(238, 248, 252), font=_font(29))
    draw.text((x + 48, y + 106), subtitle, fill=(158, 205, 213), font=_font(13))
    draw.rounded_rectangle((x + win_w - 128, y + 38, x + win_w - 46, y + 68), radius=15, fill=(4, 28, 40), outline=(79, 201, 225), width=2)
    draw.text((x + win_w - 102, y + 46), "-  x", fill=(230, 247, 250), font=_font(13))
    draw.text((x + 36, y + 146), f"{option} ELEMENT LEGEND", fill=(108, 225, 236), font=_font(12))
    _draw_card(draw, (x + 34, y + 174, x + win_w - 34, y + 324), "CHROME-001 / TITLE-001", ["NDAI chrome, compact controls, dashboard title group"])
    _draw_card(draw, (x + 34, y + 346, x + win_w - 34, y + 496), "PANEL-001 / ACTION-001", ["Category doorway card, one primary open action, compact truth copy"])
    _draw_card(draw, (x + 34, y + 518, x + win_w - 34, y + 668), "STATUS-001 / ERROR-001", ["Provider-visible data none, blocked provider/model/cache/memory paths"])
    if desktop:
        draw.rectangle((0, height - 62, width, height), fill=(0, 10, 14))
        draw.text((24, height - 42), "Full desktop/context render: monitor-space footprint and surrounding UI relationship", fill=(130, 190, 198), font=_font(15))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _copy_actual_media() -> list[RenderOption]:
    option_root = PACKET_DIR / "Review Aids" / "Render Media" / "Option-A-current-implementation"
    for kind, source in {
        "focused": PROOF_ROOT / "01_dashboard_initial_focused_window.png",
        "desktop": PROOF_ROOT / "01_dashboard_initial_full_desktop.png",
    }.items():
        target = option_root / f"option_a_current_{kind}.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    focused = option_root / "option_a_current_focused.png"
    desktop = option_root / "option_a_current_desktop.png"
    annotated_focused = option_root / "option_a_current_focused_annotated.png"
    annotated_desktop = option_root / "option_a_current_desktop_annotated.png"
    _annotate_render(focused, annotated_focused, "OPTION-A", desktop=False)
    _annotate_render(desktop, annotated_desktop, "OPTION-A", desktop=True)
    return [
        RenderOption(
            "OPTION-A",
            "Design Candidate Render using actual app/runtime screenshot",
            "DOORWAY_SHELL",
            "Review Aids/Render Media/Option-A-current-implementation/option_a_current_focused.png",
            "Review Aids/Render Media/Option-A-current-implementation/option_a_current_desktop.png",
            "Review Aids/Render Media/Option-A-current-implementation/option_a_current_focused_annotated.png",
            "Review Aids/Render Media/Option-A-current-implementation/option_a_current_desktop_annotated.png",
            "Actual current branch render: compact hub, category doorways, and child/domain window proof carry-in.",
        )
    ]


def _copy_manifest_media() -> None:
    if not PROOF_ROOT.exists():
        raise FileNotFoundError(f"Missing proof media root: {PROOF_ROOT}")
    for source in sorted(PROOF_ROOT.glob("*.png")):
        if source.name.endswith("_focused_window.png"):
            target_dir = PACKET_DIR / "Review Aids" / "Inspectable Evidence" / "focused_window_screenshots"
        elif source.name.endswith("_full_desktop.png"):
            target_dir = PACKET_DIR / "Review Aids" / "Inspectable Evidence" / "full_desktop_screenshots"
        else:
            target_dir = PACKET_DIR / "Review Aids" / "Inspectable Evidence" / "other_screenshots"
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target_dir / source.name)


def _current_packet_section(text: str) -> str:
    return _section(text, "## Packet Review State")


def _generate_candidate_media() -> list[RenderOption]:
    specs = [
        ("OPTION-B", "Compact Directory Variant", "Slightly denser doorway shell with stronger category grouping.", "Option-B-compact-directory", "DOORWAY_SHELL"),
        ("OPTION-C", "Studio-Weighted Variant", "Larger information-forward shell retained only as a rejected-risk comparator.", "Option-C-studio-weighted", "SETTINGS_PANEL"),
    ]
    result = []
    for option_id, title, subtitle, folder, footprint in specs:
        focused = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_focused.png"
        desktop = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_desktop.png"
        annotated_focused = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_focused_annotated.png"
        annotated_desktop = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_desktop_annotated.png"
        _draw_option_mockup(focused, option_id, title, subtitle, desktop=False)
        _draw_option_mockup(desktop, option_id, title, subtitle, desktop=True)
        _annotate_render(focused, annotated_focused, option_id, desktop=False)
        _annotate_render(desktop, annotated_desktop, option_id, desktop=True)
        result.append(
            RenderOption(
                option_id,
                "Design Candidate Render using deterministic branch-local layout mockup",
                footprint,
                str(focused.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(annotated_focused.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(annotated_desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
                subtitle,
            )
        )
    return result


def _options_table(options: list[RenderOption]) -> str:
    rows = [
        "| Option ID | Surface | Footprint | Authority | Clean Focused Render | Annotated Focused Render | Clean Desktop / Context Render | Annotated Desktop / Context Render | USER critique focus |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for option in options:
        rows.append(
            f"| `{option.option_id}` | AI Dashboard / AI Control Center visual acceptance target guide | `{option.footprint}` | `{option.authority}` | `{option.focused_media}` | `{option.annotated_focused_media}` | `{option.desktop_media}` | `{option.annotated_desktop_media}` | {option.description} |"
        )
    return "\n".join(rows)


def _annotation_manifest_table(options: list[RenderOption]) -> str:
    rows = [
        "| Option ID | Annotation ID | Element ID | Color + non-color cue | Visual region | Purpose | Annotated file |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for option in options:
        for image_path, desktop in (
            (option.annotated_focused_media, False),
            (option.annotated_desktop_media, True),
        ):
            target_path = PACKET_DIR / image_path
            with Image.open(target_path) as image:
                targets = _annotation_targets(*image.size, desktop=desktop)
            for index, (element_id, cue, purpose) in enumerate(ANNOTATION_ELEMENTS, start=1):
                marker_id = f"{option.option_id}-A{index:02d}"
                box = targets[element_id]
                rows.append(
                    f"| `{option.option_id}` | `{marker_id}` | `{element_id}` | {cue}; visible label `{marker_id}` plus outline/callout line | `{box[0]},{box[1]},{box[2]},{box[3]}` | {purpose} | `{image_path}` |"
                )
    return "\n".join(rows)


def _write_packet_files(options: list[RenderOption]) -> None:
    options_table = _options_table(options)
    annotation_table = _annotation_manifest_table(options)
    _write_text(
        "START_HERE.md",
        """
# FAM-007 Visual Acceptance Target Packet

Primary review file: `USER Review/VISUAL_ACCEPTANCE_TARGET_REVIEW.md`

Current gate: branch-local UI/UX Visual Acceptance Target review.

Purpose: review a branch-local process that requires rendered visual targets before future visible UI/UX implementation. A visual target is a planning guide/template candidate, not final implemented product truth by itself. This packet does not accept H1/LV, USER UTS, PR Readiness, PR creation, merge, release, or runtime/provider/private/cache/memory/download/packaging work.

Review order:

1. Open the primary USER Review file.
2. Inspect the clean and annotated render media under `Review Aids/Render Media`.
3. Use `Review Aids/ANNOTATION_MANIFEST.md` and `Review Aids/ELEMENT_LEGENDS.md` to map every callout marker to the exact visual region it identifies.
4. Use the Visual Selection Ledger template to accept, reject, combine, or revise specific options and element IDs.
5. Review the Draft Branch Visual Acceptance Target. It remains a branch-local guide until USER accepts or revises it, and implementation still requires code-to-visual proof and later review where source truth requires it.
""",
    )
    _write_text(
        "USER Review/VISUAL_ACCEPTANCE_TARGET_REVIEW.md",
        f"""
# FAM-007 Visual Acceptance Target Review

Verdict requested: accept, revise, reject, or hold this branch-local Visual Acceptance Target guide process.

## What This Packet Does

This packet creates a current-branch visual target guide process for FAM-007 visible UI/UX work. Future visible UI/UX implementation on this branch should not proceed from prose alone. It should first have a rendered visual target substantial enough to judge scale, footprint, spacing, density, hierarchy, controls, state behavior, resize behavior, copy, and relation to accepted Nexus references.

Visual Target Boundary: a USER-accepted visual target is a branch-local guide, comparator, template candidate, or expectation-alignment artifact. It should be as close to the intended product result as practical, but it is not final implemented product truth by itself. Final implementation still requires source-truth reconciliation, code-to-visual proof, validation, and USER review where the current phase requires it.

## Current Branch Visual Impact Classification

Current branch classification includes `MATERIAL_UI_UX_CHANGE`, `EXISTING_SURFACE_LAYOUT_CHANGE`, `NEW_SURFACE_OR_WINDOW`, `NEW_CONTROL_CLUSTER`, `SETTINGS_OR_IA_CHANGE`, `STATUS_ERROR_OR_EMPTY_STATE_CHANGE`, `VISUAL_SYSTEM_ADOPTION`, `USER_REPORTED_VISUAL_FAILURE`, and `FALSE_GREEN_VISUAL_PROOF_FAILURE`.

Any future visible UI/UX change on this branch needs a rendered visual target before product/runtime UI implementation, unless source truth records a narrow exception.

## Render Authority Levels

1. `Concept Render`: brainstorming only, not source truth.
2. `Design Candidate Render`: USER selection artifact, substantial and labeled.
3. `Visual Acceptance Target`: USER-accepted branch-local visual guide / expectation target.
4. `Implementation Match Proof`: actual implementation screenshot or video proving the implementation matches the accepted target.

## Visual Options

{options_table}

## Recommended Decision

Recommended: promote `OPTION-A` as the draft target basis because it uses actual current branch runtime screenshot evidence, keeps AI Dashboard as a compact doorway shell, and carries the accepted child/domain window proof. Treat `OPTION-B` as a possible future refinement candidate only if USER wants denser grouping. Treat `OPTION-C` as a rejected-risk comparator because it trends toward the larger workspace/report pattern that caused earlier false-green loops.

## USER Decision Needed

Decide whether this branch-local process and draft target guide are accepted, revised, rejected, combined from multiple options, or held for future visible UI/UX changes on this branch.

This decision does not approve H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, cleanup, issue mutation, provider/model execution, prompt send, downloads, runtime cache behavior, memory/learning/personalization, private Developer/Owner setup, installer/shortcut/packaging execution, sibling/Governance mutation, imports, or v1.8.0 work.
""",
    )
    _write_text(
        "Review Aids/VISUAL_IMPACT_CLASSIFICATION.md",
        """
# Visual Impact Classification

| Classification | Result | Basis |
| --- | --- | --- |
| `NO_VISUAL_IMPACT` | `NO` | Current branch owns visible AI Dashboard / AI Control Center UI and proof surfaces. |
| `TEXT_ONLY_VISIBLE_CHANGE` | `YES` | Copy and labels were repaired repeatedly and remain visual-proof relevant. |
| `MINOR_EXISTING_UI_CHANGE` | `YES` | Window controls, status rows, scrollbars, and copy have visible impact. |
| `MATERIAL_UI_UX_CHANGE` | `YES` | AI Dashboard/category doorway and child-window model materially changed product IA. |
| `EXISTING_SURFACE_LAYOUT_CHANGE` | `YES` | AI Control Center layout moved from stacked content to doorway shell. |
| `NEW_SURFACE_OR_WINDOW` | `YES` | Child/domain windows were introduced and proved. |
| `NEW_CONTROL_CLUSTER` | `YES` | Compact NDAI window controls exist. |
| `SETTINGS_OR_IA_CHANGE` | `YES` | Settings route and IA model are future-gated but visible. |
| `STATUS_ERROR_OR_EMPTY_STATE_CHANGE` | `YES` | Provider/no-provider/blocked/capability states are visible. |
| `VISUAL_SYSTEM_ADOPTION` | `YES` | UIREF and FAM-002 visual grammar adoption are in scope. |
| `AMBIGUOUS_VISUAL_CONTRACT` | `YES` | Prior false-green loops show prose-only targets were not enough. |
| `USER_REPORTED_VISUAL_FAILURE` | `YES` | USER repeatedly rejected visual/IA mismatches. |
| `FALSE_GREEN_VISUAL_PROOF_FAILURE` | `YES` | Branch records multiple packet/proof false-green repairs. |
""",
    )
    _write_text("Review Aids/VISUAL_OPTIONS_PACKET.md", "# Visual Options Packet\n\n" + options_table)
    _write_text(
        "Review Aids/ELEMENT_LEGENDS.md",
        """
# Element Legends

Use this with `Review Aids/ANNOTATION_MANIFEST.md`. Each annotation uses color plus a non-color cue: a stable marker ID, outline shape, and pointer/callout line. Color alone is never the mapping proof.

| Element ID | Meaning | Visible cue in annotated renders | Applies To |
| --- | --- | --- | --- |
| `CHROME-001` | NDAI custom window chrome / frame | cyan box with `OPTION-*-A01` marker | all options |
| `CTRL-001` | compact window control cluster | yellow circle with `OPTION-*-A02` marker | all options |
| `TITLE-001` | title strip and subtitle copy | magenta bracket with `OPTION-*-A03` marker | all options |
| `PANEL-001` | category doorway card or panel body | green box with `OPTION-*-A04` marker | all options |
| `ACTION-001` | primary open/action button | amber arrow with `OPTION-*-A05` marker | all options |
| `STATUS-001` | compact AI/provider/trust status | blue bracket with `OPTION-*-A06` marker | all options |
| `ROW-001` | state row inside child/detail surface | future implementation-match proof marker required | child/detail surfaces |
| `SCROLL-001` | scrollbar treatment | future implementation-match proof marker required | options with overflow |
| `RESIZE-001` | resize affordance / behavior | future implementation-match proof marker required | all product windows |
| `EMPTY-001` | empty/no-data state | future implementation-match proof marker required | future child surfaces |
| `ERROR-001` | blocked/error/unavailable state | future implementation-match proof marker required | all options |

Example review language: `I accept ACTION-001 from OPTION-A, reject PANEL-001 from OPTION-C, and want STATUS-001 revised.`
""",
    )
    _write_text(
        "Review Aids/ANNOTATION_MANIFEST.md",
        f"""
# Annotation Manifest

Purpose: map every visible callout marker in the annotated render files to an exact element ID and visual region. The clean renders remain available beside the annotated renders so the USER can inspect the design without callout overlays.

Annotation Rule: every current visual target option must include color plus a non-color cue such as marker ID, outline shape, bracket, arrow, box, circle, and pointer line. Annotations should identify the region without hiding critical UI content.

{annotation_table}
""",
    )
    _write_text(
        "Review Aids/STATE_COVERAGE_MATRIX.md",
        """
# State Coverage Matrix

| State | Required Handling | Current Packet Coverage |
| --- | --- | --- |
| default | render focused surface and desktop footprint | covered by all options |
| hover | required for future implementation-match proof | target requirement recorded |
| focus | required for future implementation-match proof | target requirement recorded |
| pressed/active | required for future implementation-match proof | target requirement recorded |
| disabled | required for blocked/future-gated actions | target requirement recorded |
| empty/no-data | required when no report/result exists | target requirement recorded |
| blocked/error | required for provider/model/download/cache/memory/private setup gates | target requirement recorded |
| success/complete | required for local readiness report generated/copied state | target requirement recorded |
| resized/fixed-size | required for product windows | current actual proof carried from H1/LV; future target must prove again after change |
""",
    )
    _write_text("Review Aids/VISUAL_SELECTION_LEDGER_TEMPLATE.md", "# Visual Selection Ledger Template\n\n| Decision ID | Surface | Option ID | Element ID | Accepted / Rejected / Combine / Revise | USER Notes | Source-Truth Impact | Branch-Local Vs Durable Design Principle | Implementation Requirement | Proof Requirement | Future Reuse Note |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| `VSL-001` | AI Dashboard / AI Control Center |  |  |  |  |  |  |  |  |  |")
    _write_text(
        "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
        """
# Draft Branch Visual Acceptance Target

Target ID: `FAM007-VAT-001`

Target Status: `DRAFT`

Target Boundary: `Branch-local guide/template candidate only; not final implemented product truth by itself.`

Selected Option(s): `Pending USER selection`

Surface Purpose: AI Dashboard / AI Control Center should be a compact top-level AI orientation and control-entry doorway. It should tell the USER what AI exists, what state it is in, what is safe or blocked, and where to go for grouped AI subsystems.

Footprint Class: `DOORWAY_SHELL`

Default Dimensions: current implementation proof carries 570x610 dashboard context; future accepted target may revise dimensions only with render proof.

Resize Behavior: product windows must declare resizable/fixed behavior and prove move/resize or not-applicable reason.

State Matrix: default, hover, focus, pressed, disabled, empty/no-data, blocked/error, success/complete, and resized/fixed-size proof must be classified.

Copy Rules: copy must be truthful, compact, user-readable, and must not imply provider/model/cache/memory/download/private setup execution.

Spacing / Density Rules: top-level content stays compact, orienting, trust-critical, or navigational. Long report bodies and setup/detail flows go behind focused surfaces.

Button / Control Rules: same-purpose buttons and window controls consume UIREF-002 and UIREF-003 unless a source-truth exception is recorded.

Status / Error / Empty Rules: provider-visible data, no-provider, blocked install intent, and future-gated private/setup states must map to backend truth.

Accepted Reference Surfaces: UIREF-001 through UIREF-006; current FAM-007 actual runtime proof is a branch-local candidate, not global template promotion.

Implementation Constraints: no future visible UI/UX implementation on this branch should proceed without USER_ACCEPTED target guide or source-truth-governed exception. Final implementation still requires code-to-visual proof, validation, and USER review where source truth requires it.

Proof Requirements: implementation-match screenshots/video, focused element proof, full desktop/context proof, state coverage, and code-to-visual trace.

LV Gating Rule: Live Validation cannot claim UI green by helper output, screenshot existence, or marker presence alone.
""",
    )
    _write_text("Review Aids/REJECTED_PATTERNS_LEDGER.md", "# Rejected Patterns Ledger\n\n| Pattern ID | Rejected UI/UX Pattern | Source Option Or Prior Evidence | Reason Rejected | Affected Surface/Class | Future Avoidance Guidance | Source-Truth Impact | Linked USER Feedback |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n| `RPL-001` | oversized inner cards | prior AI Control Center repair loops | consumes space and weakens doorway clarity | dashboard/card layout | keep doorway cards compact | branch-local, possible durable candidate | USER visual repair feedback |\n| `RPL-002` | path-dominant or proof-token layout | prior readiness rows | reads like debug/proof instead of product | diagnostics/readiness report | show USER-readable trust copy first | branch-local | USER readability feedback |\n| `RPL-003` | verbose inline helper copy | prior stacked top-level report body | turns hub into workspace | dashboard top level | route detail behind child/domain surface | branch-local and FFV carrydown | LV1 FAIL / IA feedback |\n| `RPL-004` | action buried under status | prior stacked layout | USER cannot see doorway action quickly | category cards | keep one primary launcher/action visible | branch-local | repeated AI Control Center feedback |\n| `RPL-005` | fake workspace for deferred feature | capability/provider/private placeholders | implies implementation that does not exist | future-gated cards | use compact blocked/future-gated copy | branch-local | trust-boundary feedback |\n| `RPL-006` | marker-only or local-path proof | packet false-green incidents | not reviewable or not artifact-of-record proof | USER packets/proof | include real media in ZIP | validation/packet owner | false-green repair receipts |")
    _write_text("Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md", "# Reusable Design Recipe Template\n\nStatus: `TEMPLATE ONLY - fill after USER accepts a Visual Acceptance Target guide. This template is not final implemented product truth by itself.`\n\n| Field | Value |\n| --- | --- |\n| Accepted surface class |  |\n| Accepted footprint class |  |\n| Token values / dimensions |  |\n| Padding |  |\n| Spacing |  |\n| Button heights |  |\n| Font scale |  |\n| Status chip pattern |  |\n| Title/header grammar |  |\n| Resize behavior |  |\n| Copy pattern |  |\n| State pattern |  |\n| Accepted comparator references |  |\n| Rejected alternatives |  |\n| Future branch reuse notes |  |\n| Proof requirements |  |")
    _write_text("Review Aids/SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md", "# Source-Truth Conflict Classification\n\n| Candidate Decision | Classification | Disposition |\n| --- | --- | --- |\n| Require rendered visual target before future visible UI implementation on this branch | `BRANCH_LOCAL_VISUAL_DECISION` | legal branch-local process; Governance/global version is candidate only |\n| Treat current FAM-007 actual screenshot as branch-local target candidate | `NO_CONFLICT` | comparator seed only, not global template promotion |\n| Require FAM-002/UIREF comparison for same-class controls | `NO_CONFLICT` | matches Project Vision, FAM-002, UIREF-001 through UIREF-006 |\n| Promote AI Dashboard / AI Control Center as global gold standard | `GOVERNANCE_CANDIDATE_ONLY` | not done here |\n| Add reusable global helper/validator for all branches | `GOVERNANCE_CANDIDATE_ONLY` | not done here |\n| Implement product/runtime UI change in this pass | `USER_DECISION_REQUIRED` | not approved by this packet |")
    _write_text("Review Aids/GOVERNANCE_CANDIDATE_ONLY.md", "# Governance Candidate Only\n\nCandidate: create a global Visual Acceptance Target process for all future Nexus visible UI/UX work.\n\nReason: FAM-007 and FAM-006 false-green loops show that implementation-first UI work creates repair loops. A global rule should require substantial rendered targets, annotated and clean render media, annotation manifests, element legends, state matrices, full desktop/context renders, rejected-pattern ledgers, reusable design recipes, and implementation-match proof before visible UI work can proceed.\n\nTemplate Boundary: a global visual target process should say that accepted targets are guides/templates/comparators for implementation alignment, not final product truth by themselves.\n\nApproval Needed: USER-approved Governance/FAM-002 carrier after this branch-local process is reviewed. This FAM-007 pass does not mutate Governance and does not promote a global template.")
    _write_text("Review Aids/UDL_FALSE_GREEN_STATUS.md", "# UDL / False-Green Status\n\nCurrent branch has a Unified Defect Ledger and multiple false-green packet/proof repair receipts.\n\nThis visual target packet prevents another implementation-first loop by requiring rendered design candidate media, annotated and clean visual-to-legend mapping, full desktop/context render media, stable element IDs, state coverage, a draft target guide, rejected-pattern ledger, reusable design recipe template, and packet media included in the ZIP.\n\nNo current-owned UDL row is marked closed by this packet. Existing known-bad packet defects remain preserved as historical false-green evidence.")
    _write_text("Review Aids/VALIDATION_SUMMARY.md", "# Packet Check Notes\n\nPacket-local checks are run by `dev/orin_fam007_visual_acceptance_target_packet.py --validate`.\n\nRequired checks include required files, exactly one primary USER review file, render media in the packet, image openability, focused and full desktop/context render media for each option, annotated renders for each option, annotation manifest mapping marker IDs to visual regions, element legend, state matrix, template-not-endstate wording, Visual Selection Ledger template, Draft Branch Visual Acceptance Target, Rejected Patterns Ledger, Reusable Design Recipe template, timestamped ZIP, and folder/ZIP parity.\n\nDetailed command results stay in Codex/helper output and final digest rather than in USER-facing text walls.")

    context_files = {
        "Source Truth Context/current_external_branch_state.md": BRANCH_STATE,
        "Source Truth Context/current_external_branch_plan.md": BRANCH_PLAN,
        "Source Truth Context/branch_record.md": REPO_ROOT / "Docs" / "branch_records" / "feature_fam_007_ai_control_center_readiness_diagnostics.md",
        "Source Truth Context/validation_helper_registry.md": REPO_ROOT / "Docs" / "validation_helper_registry.md",
        "Source Truth Context/ui_reference_catalog_index.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "index.md",
        "Source Truth Context/UIREF-001_top_level_window_frame.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-001_top_level_window_frame.md",
        "Source Truth Context/UIREF-002_window_control_cluster.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-002_window_control_cluster.md",
        "Source Truth Context/UIREF-003_control_state_and_selector_grammar.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-003_control_state_and_selector_grammar.md",
        "Source Truth Context/UIREF-004_dialog_status_recovery_and_doorway_surfaces.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
        "Source Truth Context/UIREF-005_design_token_and_shared_rule_baseline.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-005_design_token_and_shared_rule_baseline.md",
        "Source Truth Context/UIREF-006_negative_example_and_enforcement_contract.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-006_negative_example_and_enforcement_contract.md",
    }
    if UDL_PATH.exists():
        context_files["Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md"] = UDL_PATH
    for relative, source in context_files.items():
        _copy_file(source, relative)
    if MANIFEST_PATH.exists():
        _copy_file(MANIFEST_PATH, "Review Aids/Inspectable Evidence/live_resize_manifest.json")
    _copy_manifest_media()


def _recovery_search_roots() -> list[Path]:
    return [
        USER_ROOT,
        Path(r"C:\$Recycle.Bin"),
        Path(r"C:\Nexus Worktrees"),
        Path(r"C:\Nexus Desktop AI"),
        Path(r"C:\Users\anden\OneDrive\Desktop"),
        Path(r"C:\Users\anden\OneDrive\Documents"),
        Path(r"C:\Users\anden\OneDrive\Pictures"),
        Path(r"C:\Users\anden\Downloads"),
        Path(r"C:\Users\anden\Documents"),
        Path(r"C:\Users\anden\Desktop"),
        Path(r"C:\Users\anden\.codex\attachments"),
        Path(r"D:\Nexus Artifacts"),
        Path(r"D:\Nexus Repos"),
        Path(r"D:\Nexus Worktrees"),
        Path(r"D:\Nexus Dev ORIN"),
    ]


def _find_accepted_historical_packet() -> tuple[list[Path], list[str]]:
    matches: list[Path] = []
    searched: list[str] = []
    for root in _recovery_search_roots():
        if not root.exists():
            searched.append(f"{root} - missing root")
            continue
        searched.append(str(root))
        try:
            matches.extend(path for path in root.rglob(ACCEPTED_HISTORICAL_ZIP.name) if path.is_file())
        except (OSError, PermissionError) as exc:
            searched.append(f"{root} - search error: {exc}")
    unique = sorted({path.resolve() for path in matches})
    return unique, searched


def _copy_recovery_context() -> None:
    context_files = {
        "Source Truth Context/current_external_branch_state.md": BRANCH_STATE,
        "Source Truth Context/current_external_branch_plan.md": BRANCH_PLAN,
        "Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md": UDL_PATH,
        "Source Truth Context/branch_record.md": REPO_ROOT / "Docs" / "branch_records" / "feature_fam_007_ai_control_center_readiness_diagnostics.md",
        "Source Truth Context/validation_helper_registry.md": REPO_ROOT / "Docs" / "validation_helper_registry.md",
        "Source Truth Context/phase_governance.md": REPO_ROOT / "Docs" / "phase_governance.md",
    }
    for relative, source in context_files.items():
        if source.exists():
            _copy_file(source, relative)


def _write_recovery_packet_files(zip_path: Path, searched: list[str], matches: list[Path]) -> None:
    search_rows = "\n".join(f"| `{root}` | searched |" for root in searched)
    match_text = "\n".join(f"- `{match}`" for match in matches) if matches else "- None found."
    _write_text(
        "START_HERE.md",
        f"""
# FAM-007 Accepted-Historical Packet Recovery / Retention Blocker

Review Purpose: decide how to handle the missing accepted historical packet artifact.

Local USER Hub Folder: `C:\\Nexus USER\\FAM-007`

Review Order:

1. `USER Review/{RECOVERY_PRIMARY_REVIEW_FILE}`
2. `Review Aids/ACCEPTED_HISTORICAL_SEARCH_PROOF.md`
3. `Review Aids/ARTIFACT_DISPOSITION_OPTIONS.md`
4. `Source Truth Context/current_external_branch_state.md`
5. `Source Truth Context/current_external_branch_plan.md`
6. `Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md`

USER Decision This Packet Supports: provide/upload the missing accepted historical ZIP, approve a retention waiver, or keep the packet chain blocked until recovered.

Pending USER Decisions: accepted-historical artifact disposition only. H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, provider/model execution, downloads, cache, memory, private setup, packaging, sibling/Governance mutation, imports, and v1.8.0 remain blocked.
""",
    )
    _write_text(
        f"USER Review/{RECOVERY_PRIMARY_REVIEW_FILE}",
        f"""
# Accepted-Historical Packet Recovery / Retention Review

## Current Decision

Verdict For This Packet: `BLOCKER / USER DECISION REQUIRED`

Missing Accepted Historical Packet: `{ACCEPTED_HISTORICAL_ZIP}`

Current Recovery Packet: `{zip_path}`

## What Happened

What Happened: the active FAM-007 source truth recorded the accepted historical Workstream implementation / H1-LV proof packet as preserved evidence, but the local artifact is missing from the searched roots. Codex did not recover a copy and must not recreate or fake preservation.

## Why This Matters

Why It Matters: accepted-historical validation requires the original timestamped ZIP artifact as the immutable evidence record. UDL rows F7-UDL-016 and F7-UDL-017 rely on that artifact being available and byte-validated in accepted-historical mode.

## Current Disposition

Current Disposition: the Visual Acceptance Target packet chain is blocked on accepted-historical artifact disposition. The branch may not claim the accepted historical packet is preserved while the ZIP is missing.

## USER Options

USER Options:

| Option | Meaning | Result |
| --- | --- | --- |
| Provide / upload the missing ZIP | USER supplies the original `FAM-007-20260623-123429.zip` artifact. | Codex restores it to `C:\\Nexus USER`, validates accepted-historical mode, regenerates the Visual Acceptance Target packet, and resumes packet review. |
| Approve retention waiver | USER explicitly accepts that the local historical ZIP is unavailable and waives local retained-ZIP proof for this chain. | Codex records waiver wording in source truth/external state and regenerates the current packet without claiming local preservation. |
| Keep blocked | USER does not waive and cannot provide the ZIP. | Packet chain remains blocked until artifact recovery succeeds. |

Not Approved By This Packet: H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, unrelated cleanup, issue mutation, provider/model execution, prompt send, downloads, runtime cache behavior, memory/learning/personalization, private Developer/Owner setup, installer/shortcut/packaging execution, sibling/Governance mutation, imports, or v1.8.0 work.

## Exact USER Decision Supported

Suggested USER Decision Text:

`{_recovery_exact_user_decision_text(zip_path)}`
""",
    )
    _write_text(
        "Review Aids/ACCEPTED_HISTORICAL_SEARCH_PROOF.md",
        f"""
# Accepted-Historical Packet Search Proof

Target Filename: `{ACCEPTED_HISTORICAL_ZIP.name}`

Target Restore Path: `{ACCEPTED_HISTORICAL_ZIP}`

Search Result: `NOT RECOVERED`

Matches Found:

{match_text}

Searched Roots:

| Root | Result |
| --- | --- |
{search_rows}

Search Interpretation: no exact retained artifact was found. No same-packet copy can be validated without artifact bytes or a recorded matching SHA/source artifact.
""",
    )
    _write_text(
        "Review Aids/ARTIFACT_DISPOSITION_OPTIONS.md",
        """
# Artifact Disposition Options

| Disposition | Allowed Now | Notes |
| --- | --- | --- |
| Restore exact ZIP | Yes, if USER supplies or local search finds it | Must validate in accepted-historical mode after restore. |
| Mark recovered without ZIP bytes | No | Would fake preservation and reintroduce false-green risk. |
| Recreate ZIP from current folder | No | Would not be the accepted historical artifact. |
| Waive local retained-ZIP proof | USER decision required | Must be explicit and source-truth-routed. |
| Keep chain blocked | Yes | Safest default if the artifact cannot be recovered and USER does not waive. |
""",
    )
    _write_text(
        "Review Aids/PACKET_CHECK_NOTES.md",
        """
# Packet Check Notes

This packet is intentionally a blocker/decision packet. It should validate as a current USER review packet while preserving that the accepted historical ZIP is missing.

Required checks:

- exactly one primary USER review file
- timestamped ZIP
- folder/ZIP parity
- copied Source Truth Context says the accepted historical ZIP is missing, not preserved
- no H1/LV acceptance
- no USER UTS acceptance
- no wording that opens PR Readiness
- no PR creation approval
- no packet validation as USER acceptance
""",
    )
    _copy_recovery_context()


def generate_recovery_blocker() -> Path:
    zip_path = USER_ROOT / f"{WORKTREE_LABEL}-{_stamp()}.zip"
    matches, searched = _find_accepted_historical_packet()
    if matches:
        raise RuntimeError(f"Accepted historical packet was found and should be restored instead: {matches[0]}")
    _purge_packet_root()
    _update_external_state_for_recovery_packet(zip_path)
    _write_recovery_packet_files(zip_path, searched, matches)
    _create_zip(zip_path)
    return zip_path


def validate_recovery_blocker(packet_dir: Path = PACKET_DIR, zip_path: Path | None = None) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if zip_path is None:
        zips = sorted(USER_ROOT.glob(f"{WORKTREE_LABEL}-*.zip"), key=lambda path: path.stat().st_mtime, reverse=True)
        zip_path = zips[0] if zips else None
    if zip_path is None or not zip_path.exists():
        return False, ["Timestamped recovery ZIP missing"]
    primary = packet_dir / "USER Review" / RECOVERY_PRIMARY_REVIEW_FILE
    if not primary.exists():
        failures.append(f"Recovery primary review file missing: {RECOVERY_PRIMARY_REVIEW_FILE}")
    primary_files = list((packet_dir / "USER Review").glob("*.md")) if (packet_dir / "USER Review").exists() else []
    if len(primary_files) != 1:
        failures.append(f"Expected exactly one recovery primary USER review file; found {len(primary_files)}")
    with zipfile.ZipFile(zip_path, "r") as archive:
        zip_entries = {info.filename for info in archive.infolist() if not info.is_dir()}
        folder_entries = {path.relative_to(packet_dir).as_posix() for path in _packet_file_entries()}
        if folder_entries != zip_entries:
            failures.append("Recovery packet folder/ZIP parity failed")
        if f"USER Review/{RECOVERY_PRIMARY_REVIEW_FILE}" not in zip_entries:
            failures.append("Recovery ZIP missing primary review file")
        state_text = archive.read("Source Truth Context/current_external_branch_state.md").decode("utf-8")
        plan_text = archive.read("Source Truth Context/current_external_branch_plan.md").decode("utf-8")
        udl_text = archive.read("Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md").decode("utf-8")
        active_text = (
            _section(state_text, "## Next Legal Phase")
            + "\n"
            + _section(plan_text, "## Packet Review State")
            + "\n"
            + _section(plan_text, "## Next Legal Phase")
        )
        head = _git_value("rev-parse", "HEAD")
        source_head_pattern = re.compile(r"^Source Repo HEAD: `(.*?)`\r?$", re.MULTILINE)
        state_heads = source_head_pattern.findall(state_text)
        plan_heads = source_head_pattern.findall(plan_text)
        if not state_heads or state_heads[0] != head:
            failures.append("Recovery copied branch state Source Repo HEAD does not match live HEAD")
        if not plan_heads or plan_heads[0] != head:
            failures.append("Recovery copied branch plan Source Repo HEAD does not match live HEAD")
        if f"Current HEAD: `{head}`" not in udl_text:
            failures.append("Recovery copied UDL Current HEAD does not match live HEAD")
        if "Current HEAD Field Classification:" not in udl_text:
            failures.append("Recovery copied UDL does not classify Current HEAD currentness")
        if str(zip_path) not in active_text:
            failures.append("Recovery active copied context does not name final ZIP")
        if str(zip_path) not in udl_text:
            failures.append("Recovery copied UDL does not name final recovery packet")
        if udl_text.count("F7-UDL-018") != 1:
            failures.append("Copied UDL must contain F7-UDL-018 exactly once")
        for required in ("MISSING", "not currently preserved", "recovery / retention blocker"):
            if required not in state_text and required not in plan_text:
                failures.append(f"Recovery copied context missing required blocker wording: {required}")
        forbidden = [
            "remains preserved as historical evidence",
            "I accept the FAM-007 Hardening H1 Green packet",
            "PR Readiness active",
            "PR creation approved",
            "packet validation is USER acceptance",
        ]
        for term in forbidden:
            if term in active_text:
                failures.append(f"Recovery active copied context contains forbidden wording: {term}")
        if "F7-UDL-018" not in udl_text or "BLOCKED_SOURCE_TRUTH" not in udl_text:
            failures.append("Copied UDL missing F7-UDL-018 blocked artifact row")
    return not failures, failures


def _create_zip(zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in _packet_file_entries():
            archive.write(path, path.relative_to(PACKET_DIR).as_posix())


def generate() -> Path:
    zip_path = USER_ROOT / f"{WORKTREE_LABEL}-{_stamp()}.zip"
    _purge_packet_root()
    _update_external_state(zip_path)
    options = _copy_actual_media() + _generate_candidate_media()
    _write_packet_files(options)
    _create_zip(zip_path)
    return zip_path


def validate(packet_dir: Path = PACKET_DIR, zip_path: Path | None = None) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not packet_dir.exists():
        return False, [f"Packet folder missing: {packet_dir}"]
    if zip_path is None:
        zips = sorted(USER_ROOT.glob(f"{WORKTREE_LABEL}-*.zip"), key=lambda path: path.stat().st_mtime, reverse=True)
        zip_path = zips[0] if zips else None
    if zip_path is None or not zip_path.exists():
        failures.append("Timestamped ZIP missing")
    if not ACCEPTED_HISTORICAL_ZIP.exists():
        failures.append(f"Accepted historical ZIP missing: {ACCEPTED_HISTORICAL_ZIP}")
    for relative in REQUIRED_PACKET_FILES:
        if not (packet_dir / relative).exists():
            failures.append(f"Required packet file missing: {relative}")
    primary_files = list((packet_dir / "USER Review").glob("*.md"))
    if len(primary_files) != 1:
        failures.append(f"Expected exactly one primary USER review file; found {len(primary_files)}")
    option_text_path = packet_dir / "Review Aids" / "VISUAL_OPTIONS_PACKET.md"
    option_text = option_text_path.read_text(encoding="utf-8") if option_text_path.exists() else ""
    for option_id in ("OPTION-A", "OPTION-B", "OPTION-C"):
        if option_id not in option_text:
            failures.append(f"Visual option missing: {option_id}")
    media_files = sorted((packet_dir / "Review Aids" / "Render Media").rglob("*.png"))
    if len(media_files) < 6:
        failures.append(f"Expected at least 6 render media PNGs; found {len(media_files)}")
    for image_path in media_files:
        try:
            with Image.open(image_path) as image:
                image.verify()
        except Exception as exc:
            failures.append(f"Image cannot be opened: {image_path}: {exc}")
    annotation_manifest = packet_dir / "Review Aids" / "ANNOTATION_MANIFEST.md"
    annotation_text = annotation_manifest.read_text(encoding="utf-8") if annotation_manifest.exists() else ""
    if not annotation_text:
        failures.append("Annotation manifest missing or empty")
    for option_id in ("OPTION-A", "OPTION-B", "OPTION-C"):
        for index in range(1, len(ANNOTATION_ELEMENTS) + 1):
            marker_id = f"{option_id}-A{index:02d}"
            if marker_id not in annotation_text:
                failures.append(f"Annotation manifest missing marker: {marker_id}")
    generated_text = ""
    for relative in (
        "START_HERE.md",
        f"USER Review/{PRIMARY_REVIEW_FILE}",
        "Review Aids/VISUAL_OPTIONS_PACKET.md",
        "Review Aids/ELEMENT_LEGENDS.md",
        "Review Aids/ANNOTATION_MANIFEST.md",
        "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
        "Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
        "Review Aids/GOVERNANCE_CANDIDATE_ONLY.md",
        "Review Aids/VALIDATION_SUMMARY.md",
    ):
        path = packet_dir / relative
        if path.exists():
            generated_text += "\n" + path.read_text(encoding="utf-8")
    required_boundary_terms = (
        "not final implemented product truth by itself",
        "code-to-visual proof",
        "clean and annotated render media",
    )
    for term in required_boundary_terms:
        if term not in generated_text:
            failures.append(f"Generated visual packet text missing required boundary wording: {term}")
    forbidden_final_product_terms = (
        "final UI",
        "true end state",
        "guaranteed final render",
        "accepted final product",
        "final branch visual contract",
    )
    for term in forbidden_final_product_terms:
        if term.casefold() in generated_text.casefold():
            failures.append(f"Generated visual packet text implies final product truth: {term}")
    if zip_path and zip_path.exists():
        folder_entries = {path.relative_to(packet_dir).as_posix() for path in _packet_file_entries()}
        with zipfile.ZipFile(zip_path, "r") as archive:
            zip_entries = {info.filename for info in archive.infolist() if not info.is_dir()}
            if folder_entries != zip_entries:
                failures.append("Folder/ZIP parity failed")
            image_entries = [entry for entry in zip_entries if entry.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))]
            if len(image_entries) < 6:
                failures.append(f"Expected at least 6 ZIP images; found {len(image_entries)}")
            annotated_entries = [entry for entry in image_entries if "_annotated" in entry]
            if len(annotated_entries) < 6:
                failures.append(f"Expected annotated ZIP images for every option render; found {len(annotated_entries)}")
            if "Review Aids/ANNOTATION_MANIFEST.md" not in zip_entries:
                failures.append("ZIP missing annotation manifest")
            primary_entries = [entry for entry in zip_entries if entry.startswith("USER Review/") and entry.endswith(".md")]
            if primary_entries != [f"USER Review/{PRIMARY_REVIEW_FILE}"]:
                failures.append(f"Unexpected primary USER review entries in ZIP: {primary_entries}")
            required_zip_entries = {
                "Source Truth Context/current_external_branch_state.md",
                "Source Truth Context/current_external_branch_plan.md",
                "Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md",
            }
            missing_context = sorted(required_zip_entries - zip_entries)
            if missing_context:
                failures.append(f"ZIP missing required Source Truth Context entries: {missing_context}")
            else:
                head = _git_value("rev-parse", "HEAD")
                state_text = archive.read("Source Truth Context/current_external_branch_state.md").decode("utf-8")
                plan_text = archive.read("Source Truth Context/current_external_branch_plan.md").decode("utf-8")
                udl_text = archive.read("Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md").decode("utf-8")
                state_next_gate = _section(state_text, "## Next Legal Phase")
                plan_next_gate = _section(plan_text, "## Next Legal Phase")
                stale_next_gate_terms = [
                    "Live Validation LV1 Review",
                    "Hardening H1 Green packet",
                    "I accept the FAM-007 Hardening H1 Green packet",
                    "approve bounded Live Validation LV1 review",
                ]
                if str(zip_path) not in state_text or str(zip_path) not in plan_text:
                    failures.append("Copied Source Truth Context does not name the final ZIP path")
                if "VISUAL_ACCEPTANCE_TARGET_REVIEW.md" not in plan_text:
                    failures.append("Copied branch plan does not name the visual acceptance target primary review file")
                if "WORKSTREAM_IMPLEMENTATION_H1_LV_REVIEW.md" in _current_packet_section(plan_text):
                    failures.append("Copied branch plan active Packet Review State still names stale H1/LV primary review file")
                if not state_next_gate:
                    failures.append("Copied branch state missing active Next Legal Phase section")
                if not plan_next_gate:
                    failures.append("Copied branch plan missing active Next Legal Phase section")
                if VISUAL_NEXT_LEGAL_PHASE not in state_next_gate or VISUAL_NEXT_LEGAL_PHASE not in plan_next_gate:
                    failures.append("Copied active Next Legal Phase sections do not match the Visual Acceptance Target gate")
                if str(zip_path) not in state_next_gate or str(zip_path) not in plan_next_gate:
                    failures.append("Copied active Next Legal Phase decision text does not name the final ZIP path")
                for term in stale_next_gate_terms:
                    if term in state_next_gate or term in plan_next_gate or term in _current_packet_section(plan_text):
                        failures.append(f"Copied active current packet sections contain stale H1/LV next-gate text: {term}")
                if "H1/LV decision-preparation packet generated" in state_text:
                    failures.append("Copied branch state still describes the current visual packet as H1/LV decision-prep")
                if f"Current HEAD: `{head}`" not in udl_text:
                    failures.append("Copied UDL Current HEAD does not match live HEAD")
                if "Current HEAD Field Classification:" not in udl_text:
                    failures.append("Copied UDL does not classify Current HEAD currentness")
            for entry in zip_entries:
                if entry.lower().endswith(".png"):
                    try:
                        with archive.open(entry) as handle:
                            with Image.open(handle) as image:
                                image.verify()
                    except Exception as exc:
                        failures.append(f"ZIP image cannot be opened: {entry}: {exc}")
    return not failures, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--generate-recovery-blocker", action="store_true")
    parser.add_argument("--validate-recovery-blocker", action="store_true")
    parser.add_argument("--zip", type=Path)
    args = parser.parse_args()
    zip_path = args.zip
    if args.generate_recovery_blocker:
        zip_path = generate_recovery_blocker()
        print(f"Generated recovery blocker packet folder: {PACKET_DIR}")
        print(f"Generated recovery blocker packet ZIP: {zip_path}")
        print(f"ZIP SHA256: {_zip_sha256(zip_path)}")
    if args.validate_recovery_blocker:
        ok, failures = validate_recovery_blocker(zip_path=zip_path)
        if ok:
            print("FAM-007 accepted-historical recovery blocker packet validation: PASS")
            if zip_path:
                print(f"ZIP: {zip_path}")
                print(f"ZIP SHA256: {_zip_sha256(zip_path)}")
            return 0
        print("FAM-007 accepted-historical recovery blocker packet validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    if args.generate:
        zip_path = generate()
        print(f"Generated packet folder: {PACKET_DIR}")
        print(f"Generated packet ZIP: {zip_path}")
        print(f"ZIP SHA256: {_zip_sha256(zip_path)}")
    if args.validate:
        ok, failures = validate(zip_path=zip_path)
        if ok:
            print("FAM-007 visual acceptance target packet validation: PASS")
            if zip_path:
                print(f"ZIP: {zip_path}")
                print(f"ZIP SHA256: {_zip_sha256(zip_path)}")
            return 0
        print("FAM-007 visual acceptance target packet validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    if not args.generate and not args.validate and not args.generate_recovery_blocker and not args.validate_recovery_blocker:
        parser.error("choose --generate, --validate, or both")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
