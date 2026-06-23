# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-false-green-fixtures; status=shared
"""Regression fixtures for USER review packet false-green classes."""

from __future__ import annotations

import base64
import json
import tempfile
import zipfile
from pathlib import Path, PureWindowsPath

from orin_user_review_bundle import ROOT, validate_local_user_packet


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
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


def _zip_packet(
    root: Path,
    zip_path: Path,
    overrides: dict[str, str | bytes] | None = None,
    omit: set[str] | None = None,
) -> None:
    overrides = overrides or {}
    omit = omit or set()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            archive_name = path.relative_to(root).as_posix()
            if archive_name in omit:
                continue
            if archive_name in overrides:
                archive.writestr(archive_name, overrides[archive_name])
            else:
                archive.write(path, archive_name)
        for archive_name, text in sorted(overrides.items()):
            if archive_name not in omit and not (root / archive_name).exists():
                archive.writestr(archive_name, text)


def _current_head() -> str:
    import subprocess

    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def _run_fixture(name: str, mutate, *, zip_overrides=None, zip_omit=None) -> list[str]:
    with tempfile.TemporaryDirectory(prefix=f"ndai-{name}-") as temp_dir:
        review_root = Path(temp_dir)
        packet = review_root / "FAM-007"
        packet.mkdir()
        _write_base_packet(packet)
        mutate(packet)
        export_zip = review_root / "FAM-007-20260623-120000.zip"
        _zip_packet(packet, export_zip, overrides=zip_overrides, omit=zip_omit)
        return validate_local_user_packet(packet, export_zip=export_zip, worktree_label="FAM-007").failures


def _assert_failure(name: str, needle: str, mutate, *, zip_overrides=None, zip_omit=None) -> None:
    failures = _run_fixture(name, mutate, zip_overrides=zip_overrides, zip_omit=zip_omit)
    joined = "\n".join(failures)
    if needle not in joined:
        raise AssertionError(f"{name} did not fail on {needle!r}; failures were:\n{joined}")


def _write_live_manifest(packet: Path) -> None:
    manifest_dir = packet / "Review Aids" / "Inspectable Evidence"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    screenshot_classes = [
        "dashboard_initial",
        "settings_tooltip_visible",
        "control-center_opened",
        "control-center_moved_resized",
        "readiness-diagnostics_opened",
        "readiness-diagnostics_moved_resized",
        "readiness_after_actions",
        "readiness_persists_after_dashboard_close",
        "capabilities-maintenance_opened",
        "capabilities-maintenance_moved_resized",
    ]
    (manifest_dir / "live_resize_manifest.json").write_text(
        json.dumps(
            {
                "screenshots": {
                    screenshot_class: {
                        "focusedWindow": f"C:\\proof\\{screenshot_class}_focused_window.png",
                        "fullDesktop": f"C:\\proof\\{screenshot_class}_full_desktop.png",
                    }
                    for screenshot_class in screenshot_classes
                },
                "checks": {
                    "settingsCogIconOnlyNoVisibleFutureCopy": True,
                    "categoryLaunchersOpenRealWindows": True,
                    "childWindowsUseNativeNexusChrome": True,
                    "childWindowsMoveResizeFocus": True,
                    "fullDesktopProofNotDuplicated": True,
                    "explicitLauncherLabels": True,
                    "readinessReportFirstVisibleCopyIsUserReadable": True,
                    "readinessChildScrollbarIsNDAINative": True,
                    "readinessWorkRunsInsideChildWindow": True,
                    "providerExecutionStillBlocked": True,
                },
                "childChromeProbe": {
                    "control-center": {
                        "nativeChrome": "true",
                        "osChrome": "rejected",
                        "shellConformance": "ndai-webview-rounded-window-shell",
                        "moveBehavior": "header-drag",
                        "resizeBehavior": "edge-corner-resize",
                    }
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _write_manifest_images(packet: Path) -> tuple[set[str], set[str]]:
    _write_live_manifest(packet)
    focused_dir = packet / "Review Aids" / "Inspectable Evidence" / "focused_window_screenshots"
    full_dir = packet / "Review Aids" / "Inspectable Evidence" / "full_desktop_screenshots"
    focused_dir.mkdir(parents=True, exist_ok=True)
    full_dir.mkdir(parents=True, exist_ok=True)
    focused_entries: set[str] = set()
    full_entries: set[str] = set()
    manifest = json.loads((packet / "Review Aids" / "Inspectable Evidence" / "live_resize_manifest.json").read_text(encoding="utf-8"))
    for paths in manifest["screenshots"].values():
        focused_name = PureWindowsPath(paths["focusedWindow"]).name
        full_name = PureWindowsPath(paths["fullDesktop"]).name
        (focused_dir / focused_name).write_bytes(PNG_1X1)
        (full_dir / full_name).write_bytes(PNG_1X1)
        focused_entries.add(f"Review Aids/Inspectable Evidence/focused_window_screenshots/{focused_name}")
        full_entries.add(f"Review Aids/Inspectable Evidence/full_desktop_screenshots/{full_name}")
    return focused_entries, full_entries


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
        "final-zip-zero-pngs-with-manifest",
        "final ZIP contains zero image proof files",
        lambda packet: _write_live_manifest(packet),
    )
    _assert_failure(
        "manifest-json-no-screenshots",
        "final ZIP contains zero image proof files",
        lambda packet: _write_live_manifest(packet),
    )
    _assert_failure(
        "proof-index-references-missing-image",
        "proof index references image proof not present in final ZIP",
        lambda packet: (
            (packet / "Review Aids" / "CHILD_WINDOW_VISUAL_PROOF_INDEX.md").write_text(
                "Expected screenshot: Review Aids/Inspectable Evidence/full_desktop_screenshots/missing.png\n",
                encoding="utf-8",
            )
        ),
    )
    _assert_failure(
        "proof-index-references-local-only-image",
        "proof index references local-only image path",
        lambda packet: (
            (packet / "Review Aids" / "CHILD_WINDOW_VISUAL_PROOF_INDEX.md").write_text(
                r"Expected screenshot: C:\proof\missing.png" + "\n",
                encoding="utf-8",
            )
        ),
    )
    fixture_classes = [
        "dashboard_initial",
        "settings_tooltip_visible",
        "control-center_opened",
        "control-center_moved_resized",
        "readiness-diagnostics_opened",
        "readiness-diagnostics_moved_resized",
        "readiness_after_actions",
        "readiness_persists_after_dashboard_close",
        "capabilities-maintenance_opened",
        "capabilities-maintenance_moved_resized",
    ]
    all_manifest_image_entries = {
        f"Review Aids/Inspectable Evidence/focused_window_screenshots/{screenshot_class}_focused_window.png"
        for screenshot_class in fixture_classes
    } | {
        f"Review Aids/Inspectable Evidence/full_desktop_screenshots/{screenshot_class}_full_desktop.png"
        for screenshot_class in fixture_classes
    }

    _assert_failure(
        "local-proof-folder-images-but-final-zip-lacks-images",
        "Folder/ZIP parity failed",
        lambda packet: _write_manifest_images(packet),
        zip_omit=all_manifest_image_entries,
    )
    omitted_image_entry = "Review Aids/Inspectable Evidence/focused_window_screenshots/dashboard_initial_focused_window.png"

    def _one_zip_image_missing(packet: Path) -> None:
        _write_manifest_images(packet)

    _assert_failure(
        "proof-index-folder-pass-final-zip-image-inclusion-fails",
        "final ZIP image proof count is lower than manifest expectation",
        _one_zip_image_missing,
        zip_omit={omitted_image_entry},
    )
    _assert_failure(
        "udl-closed-with-proof-while-zip-lacks-screenshots",
        "F7-UDL-016 is CLOSED_WITH_PROOF",
        lambda packet: (
            _write_live_manifest(packet),
            (packet / "Review Aids" / "FAM_007_UNIFIED_DEFECT_LEDGER.md").write_text(
                "| Defect ID | Status |\n| --- | --- |\n| F7-UDL-016 | CLOSED_WITH_PROOF |\n",
                encoding="utf-8",
            ),
        ),
    )
    _assert_failure(
        "image-openability-uses-final-zip-bytes",
        "ZIP image proof file has invalid binary signature",
        _one_zip_image_missing,
        zip_overrides={omitted_image_entry: b"not-an-image"},
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
