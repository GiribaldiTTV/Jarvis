# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-false-green-fixtures; status=shared
"""Regression fixtures for USER review packet false-green classes."""

from __future__ import annotations

import base64
import tempfile
import zipfile
from pathlib import Path

from orin_user_review_bundle import ROOT, validate_local_user_packet


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


PRIMARY = """# Current Gate Review

## Current Gate

Systemic false-green regression fixture review.

## Decision Context

This fixture deliberately contains enough plain-language decision content to
avoid the empty-primary guard. The USER needs a meaningful review surface with
current gate wording, a clear statement that validation is not acceptance, and
specific blocker language when the packet is defective. This paragraph is
intentionally long enough to satisfy the primary-review content threshold while
remaining harmless fixture data. It describes a current packet review, not a
runtime approval, not PR readiness, not merge, and not release.

## USER Decision

Packet validation is not USER acceptance. This fixture should fail only because
the scenario-specific false-green defect is present.
"""


def _write_base_packet(root: Path, primary_text: str = PRIMARY) -> None:
    (root / "USER Review").mkdir(parents=True)
    (root / "Review Aids").mkdir(parents=True)
    (root / "Source Truth Context").mkdir(parents=True)
    primary_path = "USER Review/FALSE_GREEN_FIXTURE_REVIEW.md"
    (root / "START_HERE.md").write_text(
        "\n".join(
            [
                "# False-Green Fixture Packet",
                "",
                "Current Gate: `Systemic false-green regression fixture review`",
                f"Primary USER Review File: `{primary_path}`",
                "",
                "Open the primary review file. Packet validation is not USER acceptance.",
            ]
        ),
        encoding="utf-8",
    )
    (root / primary_path).write_text(primary_text, encoding="utf-8")


def _zip_packet(root: Path, zip_path: Path, overrides: dict[str, str] | None = None) -> None:
    overrides = overrides or {}
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            archive_name = path.relative_to(root).as_posix()
            if archive_name in overrides:
                archive.writestr(archive_name, overrides[archive_name])
            else:
                archive.write(path, archive_name)
        for archive_name, text in sorted(overrides.items()):
            if not (root / archive_name).exists():
                archive.writestr(archive_name, text)


def _current_head() -> str:
    import subprocess

    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def _run_fixture(name: str, mutate, *, zip_overrides=None) -> list[str]:
    with tempfile.TemporaryDirectory(prefix=f"ndai-{name}-") as temp_dir:
        review_root = Path(temp_dir)
        packet = review_root / "FAM-007"
        packet.mkdir()
        _write_base_packet(packet)
        mutate(packet)
        export_zip = review_root / "FAM-007-20260623-120000.zip"
        _zip_packet(packet, export_zip, overrides=zip_overrides)
        return validate_local_user_packet(packet, export_zip=export_zip, worktree_label="FAM-007").failures


def _assert_failure(name: str, needle: str, mutate, *, zip_overrides=None) -> None:
    failures = _run_fixture(name, mutate, zip_overrides=zip_overrides)
    joined = "\n".join(failures)
    if needle not in joined:
        raise AssertionError(f"{name} did not fail on {needle!r}; failures were:\n{joined}")


def main() -> int:
    _assert_failure(
        "empty-primary",
        "primary USER review file is empty",
        lambda packet: (packet / "USER Review" / "FALSE_GREEN_FIXTURE_REVIEW.md").write_text("", encoding="utf-8"),
    )
    _assert_failure(
        "stale-review-aid",
        "stale false-green marker",
        lambda packet: (packet / "Review Aids" / "USER_BRANCH_PLAN_REVIEW.md").write_text(
            "Option A - Approve PR Readiness Stage 1 analysis as recommended.",
            encoding="utf-8",
        ),
    )
    _assert_failure(
        "wrong-primary-reference",
        "stale primary/current decision file",
        lambda packet: (packet / "Review Aids" / "USER_REVIEW_FOLDER_AND_FILE_DIGEST.md").write_text(
            "Review Summary: USER_BRANCH_PLAN_REVIEW.md is the primary active decision file.",
            encoding="utf-8",
        ),
    )
    _assert_failure(
        "pending-external-state",
        "packet regeneration is pending",
        lambda packet: (packet / "Source Truth Context" / "current_external_branch_state.md").write_text(
            "Packet Reviewability State: `Pending regeneration`\nUSER Review ZIP: `PENDING_REGENERATION_AFTER_CHILD_WINDOW_SHELL_REPAIR`\n",
            encoding="utf-8",
        ),
    )
    live_head = _current_head()
    stale_head = "d7352db4fb1816df24daf3e05670b1023a77d1c5"
    _assert_failure(
        "stale-source-truth-plan-head",
        "does not match live HEAD",
        lambda packet: (
            (packet / "Source Truth Context" / "current_external_branch_state.md").write_text(
                f"Source Repo HEAD: `{live_head}`\n",
                encoding="utf-8",
            ),
            (packet / "Source Truth Context" / "current_external_branch_plan.md").write_text(
                f"Source Repo HEAD: `{stale_head}`\n",
                encoding="utf-8",
            ),
        ),
    )
    _assert_failure(
        "branch-state-plan-head-disagree",
        "disagrees with copied branch plan Source Repo HEAD",
        lambda packet: (
            (packet / "Source Truth Context" / "current_external_branch_state.md").write_text(
                f"Source Repo HEAD: `{live_head}`\n",
                encoding="utf-8",
            ),
            (packet / "Source Truth Context" / "current_external_branch_plan.md").write_text(
                "Source Repo HEAD: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`\n",
                encoding="utf-8",
            ),
        ),
    )
    _assert_failure(
        "udl-false-closure-with-stale-source-context",
        "F7-UDL-003 is CLOSED_WITH_PROOF",
        lambda packet: (
            (packet / "Source Truth Context" / "current_external_branch_state.md").write_text(
                f"Source Repo HEAD: `{live_head}`\n",
                encoding="utf-8",
            ),
            (packet / "Source Truth Context" / "current_external_branch_plan.md").write_text(
                f"Source Repo HEAD: `{stale_head}`\n",
                encoding="utf-8",
            ),
            (packet / "Review Aids" / "FAM_007_UNIFIED_DEFECT_LEDGER.md").write_text(
                "| Defect ID | Status |\n| --- | --- |\n| F7-UDL-003 | CLOSED_WITH_PROOF |\n",
                encoding="utf-8",
            ),
        ),
    )
    _assert_failure(
        "folder-green-zip-stale-source-context",
        "does not match live HEAD",
        lambda packet: (
            (packet / "Source Truth Context" / "current_external_branch_state.md").write_text(
                f"Source Repo HEAD: `{live_head}`\n",
                encoding="utf-8",
            ),
            (packet / "Source Truth Context" / "current_external_branch_plan.md").write_text(
                f"Source Repo HEAD: `{live_head}`\n",
                encoding="utf-8",
            ),
        ),
        zip_overrides={
            "Source Truth Context/current_external_branch_plan.md": f"Source Repo HEAD: `{stale_head}`\n"
        },
    )
    _assert_failure(
        "cropped-only-proof",
        "focused/cropped window screenshots exist without full-desktop proof",
        lambda packet: (
            (packet / "Review Aids" / "Inspectable Evidence" / "focused_window_screenshots").mkdir(parents=True),
            (packet / "Review Aids" / "Inspectable Evidence" / "focused_window_screenshots" / "focused.png").write_bytes(PNG_1X1),
        ),
    )
    _assert_failure(
        "duplicate-full-desktop-proof",
        "duplicate full-desktop screenshot bytes",
        lambda packet: (
            (packet / "Review Aids" / "Inspectable Evidence" / "full_desktop_screenshots").mkdir(parents=True),
            (packet / "Review Aids" / "Inspectable Evidence" / "full_desktop_screenshots" / "a.png").write_bytes(PNG_1X1),
            (packet / "Review Aids" / "Inspectable Evidence" / "full_desktop_screenshots" / "b.png").write_bytes(PNG_1X1),
        ),
    )
    _assert_failure(
        "missing-live-proof-check",
        "required false-green proof check is not true",
        lambda packet: (packet / "Review Aids" / "live_resize_manifest.json").write_text(
            '{"checks":{"settingsCogIconOnlyNoVisibleFutureCopy":true},"childChromeProbe":{}}',
            encoding="utf-8",
        ),
    )
    print("False-green fixture validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
