# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-false-green-fixtures; status=shared
"""Regression fixtures for USER review packet false-green classes."""

from __future__ import annotations

import base64
import inspect
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path, PureWindowsPath

import orin_user_review_bundle as bundle
from orin_user_review_bundle import (
    PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL,
    PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
    PACKET_VALIDATION_MODE_NEXT_GATE,
    ROOT,
    validate_local_user_packet,
)


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
    copied_source_path = "Source Truth Context/Docs__Main.md"
    (root / copied_source_path).write_text(
        (ROOT / "Docs" / "Main.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / "START_HERE.md").write_text(
        "\n".join(
            [
                "# False-Green Fixture Packet",
                "",
                "Current Gate: `Systemic false-green regression fixture review`",
                f"Primary USER Review File: `{primary_path}`",
                "",
                "Open the primary review file. Packet validation is not USER acceptance.",
                "",
                "## Files",
                "",
                "| Source path | Copied path |",
                "| --- | --- |",
                f"| `Docs/Main.md` | `{copied_source_path}` |",
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


def _current_branch() -> str:
    return subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=ROOT, text=True
    ).strip()


def _current_origin_main() -> str:
    return bundle._git_output("rev-parse", "origin/main")


def _assert_origin_main_fallback() -> None:
    original_git_output = bundle._git_output

    def missing_origin_main(*args: str) -> str:
        if args == ("rev-parse", "origin/main"):
            return "UNKNOWN"
        return original_git_output(*args)

    bundle._git_output = missing_origin_main
    try:
        if _current_origin_main() != "UNKNOWN":
            raise AssertionError("missing origin/main fixture did not use the UNKNOWN fallback")
    finally:
        bundle._git_output = original_git_output


def _run_fixture(
    name: str,
    mutate,
    *,
    zip_overrides=None,
    zip_omit=None,
    validation_mode: str = PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
    external_state_files=None,
    extra_zip_names: tuple[str, ...] = (),
    expected_branch: str | None = None,
    expected_head: str | None = None,
    expected_origin_main: str | None = None,
    omit_identity_arguments: bool = False,
) -> list[str]:
    with tempfile.TemporaryDirectory(prefix=f"ndai-{name}-") as temp_dir:
        review_root = Path(temp_dir)
        packet = review_root / "FAM-007"
        packet.mkdir()
        _write_base_packet(packet)
        export_zip = review_root / "FAM-007-20260623-120000.zip"
        if len(inspect.signature(mutate).parameters) >= 2:
            mutate(packet, export_zip)
        else:
            mutate(packet)
        external_state_dir = review_root / "external_state"
        if external_state_files is not None:
            external_state_dir.mkdir()
            for file_name, text in external_state_files(packet, export_zip).items():
                (external_state_dir / file_name).write_text(text, encoding="utf-8")
        original_external_state_dir = bundle._current_branch_external_state_dir
        if external_state_files is not None:
            bundle._current_branch_external_state_dir = lambda: external_state_dir
        try:
            _zip_packet(packet, export_zip, overrides=zip_overrides, omit=zip_omit)
            for extra_zip_name in extra_zip_names:
                (review_root / extra_zip_name).write_bytes(b"accepted historical placeholder")
            return validate_local_user_packet(
                packet,
                export_zip=export_zip,
                worktree_label="FAM-007",
                validation_mode=validation_mode,
                expected_branch=(
                    None
                    if omit_identity_arguments or validation_mode == PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL
                    else expected_branch or _current_branch()
                ),
                expected_head=(
                    None
                    if omit_identity_arguments or validation_mode == PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL
                    else expected_head or _current_head()
                ),
                expected_origin_main=(
                    None
                    if omit_identity_arguments or validation_mode == PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL
                    else expected_origin_main or _current_origin_main()
                ),
            ).failures
        finally:
            bundle._current_branch_external_state_dir = original_external_state_dir


def _assert_failure(
    name: str,
    needle: str,
    mutate,
    *,
    zip_overrides=None,
    zip_omit=None,
    validation_mode: str = PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
    external_state_files=None,
    extra_zip_names: tuple[str, ...] = (),
    expected_branch: str | None = None,
    expected_head: str | None = None,
    expected_origin_main: str | None = None,
    omit_identity_arguments: bool = False,
) -> None:
    failures = _run_fixture(
        name,
        mutate,
        zip_overrides=zip_overrides,
        zip_omit=zip_omit,
        validation_mode=validation_mode,
        external_state_files=external_state_files,
        extra_zip_names=extra_zip_names,
        expected_branch=expected_branch,
        expected_head=expected_head,
        expected_origin_main=expected_origin_main,
        omit_identity_arguments=omit_identity_arguments,
    )
    joined = "\n".join(failures)
    if needle not in joined:
        raise AssertionError(f"{name} did not fail on {needle!r}; failures were:\n{joined}")


def _assert_success(
    name: str,
    mutate,
    *,
    validation_mode: str,
    external_state_files,
    extra_zip_names: tuple[str, ...] = (),
) -> None:
    failures = _run_fixture(
        name,
        mutate,
        validation_mode=validation_mode,
        external_state_files=external_state_files,
        extra_zip_names=extra_zip_names,
    )
    if failures:
        raise AssertionError(f"{name} failed unexpectedly:\n" + "\n".join(failures))


def _assert_active_identity_arguments_required() -> None:
    failures = _run_fixture(
        "missing-active-identity-arguments",
        lambda _packet: None,
        omit_identity_arguments=True,
    )
    if not any("requires explicit identity expectations" in failure for failure in failures):
        raise AssertionError(
            "missing-active-identity-arguments did not fail closed:\n"
            + "\n".join(failures)
        )


def _assert_stage1_primary_for_stage2_decision() -> None:
    decision = (
        "I approve PR Readiness Stage 2 execution on C:\\Nexus Worktrees\\Governance "
        "/ feature/release-readiness-source-truth-intake."
    )
    source_branch = "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
    normalized_decision = decision.casefold()
    if bundle._is_pr_readiness_stage1_packet(
        source_branch=source_branch,
        normalized_decision=normalized_decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_REPAIR,
    ):
        raise AssertionError(
            "An actual FAM-007 Stage 2 decision was misclassified as Stage 1"
        )
    if not bundle._is_pr_readiness_stage2_packet(
        source_branch=source_branch,
        normalized_decision=normalized_decision,
    ):
        raise AssertionError("The FAM-007 Stage 2 decision was not classified as Stage 2")
    primary = bundle._primary_user_review_file(
        decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
    )
    if primary != bundle.PR_READINESS_STAGE1_REVIEW_FILE:
        raise AssertionError(
            "A green Stage 1 packet carrying the Stage 2 approval text must keep "
            f"{bundle.PR_READINESS_STAGE1_REVIEW_FILE} primary; found {primary!r}."
        )
    with tempfile.TemporaryDirectory(prefix="ndai-stage2-packet-") as temp_dir:
        target = Path(temp_dir) / "packet"
        target.mkdir()
        generated = bundle._write_workstream_entry_packet_digests(
            target=target,
            source_branch=source_branch,
            source_head="a" * 40,
            origin_main="b" * 40,
            packet_folder=target,
            export_zip=target / "FAM-007-20260717-000000.zip",
            copied=[],
            extra_bundle_files=[],
            bundle_file_count=0,
            expected_count=0,
            copied_count=0,
            exact_user_decision=decision,
            pending_user_decisions=["Merge remains pending USER approval."],
            stage1_outcome=bundle.PR_STAGE1_OUTCOME_REPAIR,
        )
        generated_names = {path.name for path in generated}
        if bundle.PR_READINESS_STAGE1_REVIEW_FILE in generated_names:
            raise AssertionError(
                "Actual FAM-007 Stage 2 packet generation emitted a Stage 1 primary artifact"
            )
        if "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md" not in generated_names:
            raise AssertionError(
                "Actual FAM-007 Stage 2 packet generation did not emit its Stage 2 digest"
            )

    if not bundle._is_pr_readiness_stage1_packet(
        source_branch=source_branch,
        normalized_decision=normalized_decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
    ):
        raise AssertionError(
            "A green Stage 1 packet carrying the Stage 2 next decision lost its Stage 1 classification"
        )


def _assert_non_fam007_stage2_wording_requires_ready_stage1() -> None:
    decision = (
        "I approve PR Readiness Stage 2 execution on C:\\Nexus Worktrees\\Governance "
        "/ feature/release-readiness-source-truth-intake."
    )
    normalized_decision = decision.casefold()
    source_branch = "feature/release-readiness-source-truth-intake"
    if bundle._is_pr_readiness_stage1_packet(
        source_branch=source_branch,
        normalized_decision=normalized_decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_REPAIR,
    ):
        raise AssertionError(
            "Stage 2 wording with a repair-required Stage 1 outcome was misclassified as Stage 1"
        )
    if not bundle._is_pr_readiness_stage1_packet(
        source_branch=source_branch,
        normalized_decision=normalized_decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
    ):
        raise AssertionError(
            "Stage 2 wording with a ready Stage 1 outcome did not retain Stage 1 packet classification"
        )


def _assert_non_stage1_live_validation_packet_classification() -> None:
    decision = (
        "I approve bounded PR Readiness Stage 1 analysis for the FAM-007 "
        "Dev/Owner Skeleton Readiness package."
    )
    normalized_decision = decision.casefold()
    source_branch = "feature/fam-007-dev-owner-skeleton-readiness"
    if bundle._is_pr_readiness_stage1_packet(
        source_branch=source_branch,
        normalized_decision=normalized_decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
    ):
        raise AssertionError(
            "FAM-007 Live Validation LV1 decision was misclassified as a Stage 1 packet"
        )
    if not bundle._is_dev_owner_live_validation_lv1_packet(
        source_branch,
        normalized_decision,
    ):
        raise AssertionError("FAM-007 Live Validation LV1 packet classification was not recognized")
    with tempfile.TemporaryDirectory(prefix="ndai-non-stage1-packet-") as temp_dir:
        target = Path(temp_dir) / "packet"
        target.mkdir()
        generated = bundle._write_workstream_entry_packet_digests(
            target=target,
            source_branch=source_branch,
            source_head="a" * 40,
            origin_main="b" * 40,
            packet_folder=target,
            export_zip=target / "FAM-007-20260717-000000.zip",
            copied=[],
            extra_bundle_files=[],
            bundle_file_count=0,
            expected_count=0,
            copied_count=0,
            exact_user_decision=decision,
            pending_user_decisions=["PR Readiness Stage 1 remains pending USER response."],
            stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
        )
        if bundle.PR_READINESS_STAGE1_REVIEW_FILE in {path.name for path in generated}:
            raise AssertionError(
                "Non-Stage-1 FAM-007 packet generation emitted Stage 1-only digest files"
            )

    legacy_source_branch = (
        "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
    )
    legacy_lv1_decision = (
        "I approve bounded PR Readiness Stage 1 analysis for the FAM-007 Breakpoint 2 carrier."
    )
    legacy_normalized_decision = legacy_lv1_decision.casefold()
    if bundle._is_pr_readiness_stage1_packet(
        source_branch=legacy_source_branch,
        normalized_decision=legacy_normalized_decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_REPAIR,
    ):
        raise AssertionError(
            "Legacy FAM-007 LV1-green packet was misclassified as PR Readiness Stage 1"
        )
    if not bundle._is_fam007_breakpoint2_live_validation_lv1_packet(
        source_branch=legacy_source_branch,
        normalized_decision=legacy_normalized_decision,
    ):
        raise AssertionError("Legacy FAM-007 LV1-green packet was not recognized")
    if bundle._primary_user_review_file(
        legacy_lv1_decision,
        source_branch=legacy_source_branch,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_REPAIR,
    ) != bundle.USER_BRANCH_PLAN_REVIEW_FILE:
        raise AssertionError(
            "Legacy FAM-007 LV1-green packet did not retain the LV1/plan primary artifact"
        )


def _assert_current_stage1_terms_are_not_stale() -> None:
    packet_files = {
        "START_HERE.md": (
            "Primary USER Review File: USER Review/PR_READINESS_STAGE1_REVIEW.md\n"
            "Current Gate: Stage 1 Ready For Stage 2\n"
        ),
        "USER Review/PR_READINESS_STAGE1_REVIEW.md": (
            "PR Readiness Stage 1 analysis is complete.\n"
            "Stage 1 Ready For Stage 2\n"
        ),
        "Review Aids/PR_READINESS_STAGE1_COVERAGE_DIGEST.md": (
            "Current Gate: PR Readiness Stage 1\n"
            "Stage 1 is complete; Stage 2 remains pending separate USER approval.\n"
        ),
    }
    failures = bundle._active_review_aid_false_green_failures(packet_files)
    if failures:
        raise AssertionError(
            "Current Stage 1 packet wording was incorrectly classified as stale:\n"
            + "\n".join(failures)
        )


def _assert_stage1_coherence_guards() -> None:
    coherent = {
        "START_HERE.md": (
            "Primary USER Review File: USER Review/PR_READINESS_STAGE1_REVIEW.md\n"
            "Decision Path Summary: pr readiness stage1 approval review - Stage 1 Ready For Stage 2.\n"
        ),
        "USER Review/PR_READINESS_STAGE1_REVIEW.md": (
            "## Stage 1 Outcome\nStage 1 Ready For Stage 2\n"
        ),
        "Review Aids/PR_READINESS_STAGE1_COVERAGE_DIGEST.md": (
            "Current Gate: PR Readiness Stage 1\nStage 2 remains pending.\n"
        ),
        "Review Aids/PR_READINESS_STAGE1_SOURCE_COVERAGE.md": (
            "`Source Truth Context/Docs__Main.md`\nCopied Source Count: `1`\n"
        ),
        "Review Aids/PR_READINESS_STAGE1_CONTRADICTION_CHECKLIST.md": (
            "PASS: no active Workstream Entry decision path is emitted.\n"
        ),
        "Review Aids/USER_BRANCH_VISION_REVIEW.md": (
            "Context Complete - no new BP1 response requested by this packet; "
            "PR Readiness Stage 1 analysis remains the next USER decision.\n"
        ),
        "Review Aids/USER_BRANCH_PLAN_REVIEW.md": (
            "Context Complete - no new BP1 response requested by this packet; "
            "PR Readiness Stage 1 analysis remains the next USER decision.\n"
        ),
        "Source Truth Context/Docs__Main.md": "# Main\n",
    }
    failures = bundle._pr_stage1_packet_coherence_failures(coherent)
    failures.extend(bundle._pr_stage1_source_coverage_failures(coherent))
    if failures:
        raise AssertionError("coherent Stage 1 packet failed:\n" + "\n".join(failures))

    workstream = dict(coherent)
    workstream["START_HERE.md"] = (
        "Primary USER Review File: USER Review/PR_READINESS_STAGE1_REVIEW.md\n"
        "Decision Path Summary: workstream entry final decision review.\n"
    )
    failures = bundle._pr_stage1_packet_coherence_failures(workstream)
    if not any("Decision Path Summary" in failure for failure in failures):
        raise AssertionError("Workstream summary did not fail Stage 1 coherence validation")

    pending_bp = dict(coherent)
    pending_bp["Review Aids/PR_READINESS_STAGE1_COVERAGE_DIGEST.md"] = (
        "BP2 USER Branch Plan Review remains pending USER acceptance.\n"
    )
    failures = bundle._pr_stage1_packet_coherence_failures(pending_bp)
    if not any("BP gate" in failure for failure in failures):
        raise AssertionError("active BP pending language did not fail Stage 1 coherence validation")

    false_coverage = dict(coherent)
    false_coverage["Review Aids/PR_READINESS_STAGE1_SOURCE_COVERAGE.md"] = (
        "`Source Truth Context/feature_backlog.md`\nCopied Source Count: `1`\n"
    )
    failures = bundle._pr_stage1_source_coverage_failures(false_coverage)
    if not any("absent files" in failure or "missing from coverage" in failure for failure in failures):
        raise AssertionError("false source coverage did not fail Stage 1 coverage validation")

    repair = dict(coherent)
    repair["START_HERE.md"] = (
        "Primary USER Review File: USER Review/PR_READINESS_STAGE1_REVIEW.md\n"
        "Decision Path Summary: pr readiness stage1 repair review - Stage 1 remains held.\n"
    )
    repair["USER Review/PR_READINESS_STAGE1_REVIEW.md"] = (
        "## Stage 1 Outcome\nPR Readiness Stage 1 Repair Required\n"
    )
    repair["Review Aids/PR_READINESS_STAGE1_COVERAGE_DIGEST.md"] = (
        "USER Decision: I approve PR Readiness Stage 1 analysis for the bounded repair.\n"
    )
    failures = bundle._pr_stage1_packet_coherence_failures(repair)
    if failures:
        raise AssertionError(
            "repair-required Stage 1 packet was rejected as non-approval posture:\n"
            + "\n".join(failures)
        )

    ready = dict(repair)
    ready["USER Review/PR_READINESS_STAGE1_REVIEW.md"] = (
        "## Stage 1 Outcome\nStage 1 Ready For Stage 2\n"
    )
    failures = bundle._pr_stage1_packet_coherence_failures(ready)
    if not any("requests or recommends Stage 1" in failure for failure in failures):
        raise AssertionError(
            "ready Stage 1 packet did not reject a stale Stage 1 request in a review aid"
        )


def _assert_local_stage1_validation_replays_stage1_checks() -> None:
    def stale_stage1_packet(packet: Path) -> None:
        (packet / "USER Review" / "FALSE_GREEN_FIXTURE_REVIEW.md").unlink()
        start_here = (packet / "START_HERE.md").read_text(encoding="utf-8")
        start_here = start_here.replace(
            "Primary USER Review File: `USER Review/FALSE_GREEN_FIXTURE_REVIEW.md`",
            f"Primary USER Review File: `USER Review/{bundle.PR_READINESS_STAGE1_REVIEW_FILE}`",
        )
        (packet / "START_HERE.md").write_text(
            start_here
            + "\nDecision Path Summary: workstream entry final decision review.\n",
            encoding="utf-8",
        )
        (packet / "USER Review" / bundle.PR_READINESS_STAGE1_REVIEW_FILE).write_text(
            "Stage 1 Ready For Stage 2\n",
            encoding="utf-8",
        )
        (packet / "Review Aids" / "PR_READINESS_STAGE1_SOURCE_COVERAGE.md").write_text(
            "Copied Source Count: `999`\n`Source Truth Context/Docs__Main.md`\n",
            encoding="utf-8",
        )

    failures = _run_fixture(
        "local-stage1-validation-replays-stage1-checks",
        stale_stage1_packet,
    )
    if not any(
        "PR Stage 1 artifact is missing" in failure
        or "Decision Path Summary" in failure
        or "Copied Source Count does not match" in failure
        for failure in failures
    ):
        raise AssertionError(
            "local packet validation did not replay Stage 1 checks:\n"
            + "\n".join(failures)
        )


def _snapshot_context(packet: Path, export_zip: Path, *, state_head: str, plan_head: str | None = None) -> None:
    plan_head = plan_head or state_head
    (packet / "Source Truth Context" / "current_external_branch_state.md").write_text(
        "\n".join(
            [
                f"Source Repo HEAD: `{state_head}`",
                f"USER Review ZIP: `{export_zip}`",
                "Packet Reviewability State: `Reviewable evidence packet`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (packet / "Source Truth Context" / "current_external_branch_plan.md").write_text(
        f"Source Repo HEAD: `{plan_head}`\nPlanning Snapshot: `packet generation context`\n",
        encoding="utf-8",
    )


def _accepted_live_state(snapshot_head: str, live_head: str = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"):
    def _files(_packet: Path, export_zip: Path) -> dict[str, str]:
        return {
            "branch_state.md": "\n".join(
                [
                    f"Source Repo HEAD: `{live_head}`",
                    f"USER Review ZIP: `{export_zip}`",
                    "Packet Reviewability State: `USER accepted reviewable proof packet only`",
                    "USER Gate State: `USER accepted reviewable evidence only`",
                    "",
                ]
            ),
            "branch_plan.md": "\n".join(
                [
                    f"Source Repo HEAD: `{live_head}`",
                    f"Accepted Historical Packet Source HEAD: `{snapshot_head}`",
                    f"USER accepted reviewable proof packet `{export_zip}` as historical evidence.",
                    "",
                ]
            ),
        }
    return _files


def _fresh_live_state(head: str):
    def _files(_packet: Path, export_zip: Path) -> dict[str, str]:
        return {
            "branch_state.md": "\n".join(
                [
                    f"Source Repo HEAD: `{head}`",
                    f"USER Review ZIP: `{export_zip}`",
                    "Packet Reviewability State: `Reviewable evidence packet`",
                    "",
                ]
            ),
            "branch_plan.md": f"Source Repo HEAD: `{head}`\nPlanning Snapshot: `packet generation context`\n",
        }
    return _files


def _snapshot_context_with_historical_zip(packet: Path, export_zip: Path, *, head: str, historical_zip_name: str) -> None:
    historical_zip = export_zip.with_name(historical_zip_name)
    (packet / "Source Truth Context" / "current_external_branch_state.md").write_text(
        "\n".join(
            [
                f"Source Repo HEAD: `{head}`",
                f"USER Review ZIP: `{export_zip}`",
                "Packet Reviewability State: `Reviewable evidence packet`",
                f"Accepted Historical Packet: `{historical_zip}`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (packet / "Source Truth Context" / "current_external_branch_plan.md").write_text(
        "\n".join(
            [
                f"Source Repo HEAD: `{head}`",
                "Planning Snapshot: `packet generation context`",
                f"Accepted Historical Packet: `{historical_zip}`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _fresh_live_state_with_historical_zip(head: str, historical_zip_name: str):
    def _files(_packet: Path, export_zip: Path) -> dict[str, str]:
        historical_zip = export_zip.with_name(historical_zip_name)
        return {
            "branch_state.md": "\n".join(
                [
                    f"Source Repo HEAD: `{head}`",
                    f"USER Review ZIP: `{export_zip}`",
                    "Packet Reviewability State: `Reviewable evidence packet`",
                    f"Accepted Historical Packet: `{historical_zip}`",
                    "",
                ]
            ),
            "branch_plan.md": "\n".join(
                [
                    f"Source Repo HEAD: `{head}`",
                    "Planning Snapshot: `packet generation context`",
                    f"Accepted Historical Packet: `{historical_zip}`",
                    "",
                ]
            ),
        }
    return _files


def _assert_generation_cleanup_removes_recorded_historical_zip() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-same-label-cleanup-") as temp_dir:
        review_root = Path(temp_dir)
        export_zip = review_root / "FAM-007-20260623-120000.zip"
        stale_zip = review_root / "FAM-007-20260623-123429.zip"
        external_state_dir = review_root / "external_state"
        external_state_dir.mkdir()
        export_zip.write_bytes(b"current packet placeholder")
        stale_zip.write_bytes(b"historical packet placeholder")
        (external_state_dir / "branch_state.md").write_text(
            f"Accepted Historical Packet: `{stale_zip}`\n",
            encoding="utf-8",
        )
        (external_state_dir / "branch_plan.md").write_text(
            f"Accepted Historical Packet: `{stale_zip}`\n",
            encoding="utf-8",
        )

        original_external_state_dir = bundle._current_branch_external_state_dir
        bundle._current_branch_external_state_dir = lambda: external_state_dir
        try:
            bundle._remove_stale_same_label_export_zips(review_root, "FAM-007", export_zip)
        finally:
            bundle._current_branch_external_state_dir = original_external_state_dir

        if stale_zip.exists():
            raise AssertionError("generation cleanup preserved recorded accepted-historical same-label ZIP")
        if not export_zip.exists():
            raise AssertionError("generation cleanup removed the active export ZIP")


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
    _assert_origin_main_fallback()
    _assert_stage1_primary_for_stage2_decision()
    _assert_non_fam007_stage2_wording_requires_ready_stage1()
    _assert_non_stage1_live_validation_packet_classification()
    _assert_current_stage1_terms_are_not_stale()
    _assert_stage1_coherence_guards()
    _assert_local_stage1_validation_replays_stage1_checks()
    _assert_active_identity_arguments_required()
    _assert_failure(
        "active-review-wrong-branch",
        "Folder active-review identity: Packet identity: expected branch",
        lambda _packet: None,
        expected_branch="feature/wrong-branch",
    )
    _assert_failure(
        "active-review-wrong-head",
        "Folder active-review identity: Packet identity: expected HEAD",
        lambda _packet: None,
        expected_head="1" * 40,
    )
    _assert_failure(
        "active-review-wrong-origin-main",
        "Folder active-review identity: Packet identity: expected origin/main",
        lambda _packet: None,
        expected_origin_main="2" * 40,
    )
    _assert_failure(
        "next-gate-wrong-head",
        "Folder next-gate identity: Packet identity: expected HEAD",
        lambda _packet: None,
        validation_mode=PACKET_VALIDATION_MODE_NEXT_GATE,
        expected_head="1" * 40,
    )
    _assert_success(
        "active-review-identity-positive",
        lambda _packet: None,
        validation_mode=PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
        external_state_files=None,
    )
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
    def _pending_stage1_packet(packet: Path) -> None:
        (packet / "START_HERE.md").write_text(
            (packet / "START_HERE.md").read_text(encoding="utf-8")
            + "\nDecision Path Summary: PR Readiness Stage 1 analysis remains pending USER approval; PR creation remains pending USER approval.\n"
            + "USER Decision: I approve or reject fresh PR Readiness Stage 1 analysis. This does not authorize PR Stage 2, PR creation, merge, or release.\n",
            encoding="utf-8",
        )
        (packet / "Review Aids" / "USER_BRANCH_PLAN_REVIEW.md").write_text(
            "Option A - Approve PR Readiness Stage 1 analysis as recommended.\n",
            encoding="utf-8",
        )

    _assert_success(
        "pending-stage1-posture-allows-stage1-language",
        _pending_stage1_packet,
        validation_mode=PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
        external_state_files=None,
    )

    def _pr_stage1_primary(packet: Path) -> None:
        old_primary = packet / "USER Review" / "FALSE_GREEN_FIXTURE_REVIEW.md"
        new_primary = packet / "USER Review" / bundle.PR_READINESS_STAGE1_REVIEW_FILE
        old_primary.rename(new_primary)
        (packet / "START_HERE.md").write_text(
            (packet / "START_HERE.md").read_text(encoding="utf-8").replace(
                "Current Gate: `Systemic false-green regression fixture review`",
                "Current Gate: `PR Readiness Stage 1 repair review`",
            ).replace(
                "USER Review/FALSE_GREEN_FIXTURE_REVIEW.md",
                f"USER Review/{bundle.PR_READINESS_STAGE1_REVIEW_FILE}",
            )
            + "\nDecision Path Summary: pr readiness stage1 repair review - Stage 1 remains held.\n",
            encoding="utf-8",
        )
        support_decision = "I approve bounded PR Readiness Stage 1 analysis for the Governance repair."
        support_sources = [("Docs/Main.md", "Source Truth Context/Docs__Main.md")]
        bundle._write_user_branch_vision_review(
            target=packet / "Review Aids",
            title="False-Green Fixture",
            review_purpose="PR Readiness Stage 1 repair review context.",
            exact_user_decision=support_decision,
            pending_user_decisions=["PR Readiness Stage 2 remains pending USER approval."],
            copied=support_sources,
        )
        bundle._write_user_branch_plan_review(
            target=packet / "Review Aids",
            title="False-Green Fixture",
            review_purpose="PR Readiness Stage 1 repair review context.",
            source_branch=_current_branch(),
            source_head=_current_head(),
            upstream="origin/feature/fixture",
            origin_main=_current_origin_main(),
            exact_user_decision=support_decision,
            pending_user_decisions=["PR Readiness Stage 2 remains pending USER approval."],
            copied=support_sources,
        )
        new_primary.write_text(
            "\n".join(
                [
                    "# PR Readiness Stage 1 Review",
                    "",
                    "## Review Status",
                    "Reviewable.",
                    "## Contract Status",
                    "Complete - current-gate artifact, not BP2.",
                    "## Packet Reviewability State",
                    "Reviewable.",
                    "## USER Gate State",
                    "Pending USER Review.",
                    "## Current-Gate Purpose",
                    "PR Readiness Stage 1 repair review for systemic false-green regression coverage.",
                    "## Scope And Authority",
                    "Governance repair scope.",
                    "## Transition-Safety Review",
                    "Target and snapshot proof.",
                    "## Adversarial And False-Green Review",
                    "Mutation and packet-class coverage.",
                    "## Stage 1 Outcome",
                    "PR Readiness Stage 1 Repair Required.",
                    "## Exact USER Decision Supported",
                    "Review this Stage 1 repair. This current-gate artifact explains why structural packet parity, generated support files, and helper output are evidence rather than acceptance. It records the transition-safety checks, false-green regression classes, and remaining USER decision boundary so the packet cannot silently present BP2 planning context as PR Readiness. The review remains bounded to Governance source truth, reusable helper behavior, validator coverage, and adversarial fixtures. No implementation, PR creation, merge, release, issue mutation, or sibling worktree action is authorized by this review surface.",
                ]
            ),
            encoding="utf-8",
        )
        (packet / "Review Aids" / "PR_READINESS_STAGE1_SOURCE_COVERAGE.md").write_text(
            "`Source Truth Context/Docs__Main.md`\nCopied Source Count: `1`\n",
            encoding="utf-8",
        )

    def _pr_stage1_repair_posture(packet: Path) -> None:
        _pr_stage1_primary(packet)
        (packet / "START_HERE.md").write_text(
            (packet / "START_HERE.md").read_text(encoding="utf-8")
            + "\nStage 1 remains in repair-required posture; Stage 2 is not supported.\n",
            encoding="utf-8",
        )
        (packet / "Review Aids" / "PR_READINESS_STAGE1_COVERAGE_DIGEST.md").write_text(
            "Current Gate: PR Readiness Stage 1\n"
            "PR Readiness Stage 1 analysis remains held while repair is required.\n",
            encoding="utf-8",
        )

    _assert_success(
        "pr-stage1-repair-posture-allows-stage1-language",
        _pr_stage1_repair_posture,
        validation_mode=PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
        external_state_files=None,
    )

    _assert_success(
        "pr-stage1-dedicated-primary",
        _pr_stage1_primary,
        validation_mode=PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
        external_state_files=None,
    )

    def _missing_stage1_support(packet: Path) -> None:
        _pr_stage1_primary(packet)
        (packet / "Review Aids" / bundle.USER_BRANCH_PLAN_REVIEW_FILE).unlink()

    _assert_failure(
        "pr-stage1-supporting-context-missing",
        "Stage 1 supporting planning context is missing",
        _missing_stage1_support,
    )

    def _legitimate_source_context_shell_tokens(packet: Path) -> None:
        (packet / "Source Truth Context" / "helper_source.py").write_text(
            "branch = '$branch'\nhead = '$head'\norigin = '$originMain'\n",
            encoding="utf-8",
        )

    _assert_success(
        "source-context-code-is-not-user-facing-template-shell",
        _legitimate_source_context_shell_tokens,
        validation_mode=PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
        external_state_files=None,
    )

    def _pr_stage1_missing_primary(packet: Path) -> None:
        (packet / "START_HERE.md").write_text(
            (packet / "START_HERE.md").read_text(encoding="utf-8").replace(
                "Current Gate: `Systemic false-green regression fixture review`",
                "Current Gate: `PR Readiness Stage 1 repair review`",
            ).replace(
                "USER Review/FALSE_GREEN_FIXTURE_REVIEW.md",
                f"USER Review/{bundle.PR_READINESS_STAGE1_REVIEW_FILE}",
            ),
            encoding="utf-8",
        )

    _assert_failure(
        "pr-stage1-primary-missing",
        "does not identify the primary USER review file",
        _pr_stage1_missing_primary,
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
    snapshot_head = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    _assert_failure(
        "active-review-stale-copied-context",
        "does not match live external state",
        lambda packet, export_zip: _snapshot_context(packet, export_zip, state_head=snapshot_head),
        external_state_files=_fresh_live_state(live_head),
    )
    _assert_success(
        "accepted-historical-post-acceptance-drift",
        lambda packet, export_zip: _snapshot_context(packet, export_zip, state_head=snapshot_head),
        validation_mode=PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL,
        external_state_files=_accepted_live_state(snapshot_head),
    )
    _assert_failure(
        "accepted-historical-stale-at-generation",
        "disagrees with copied branch plan Source Repo HEAD",
        lambda packet, export_zip: _snapshot_context(
            packet,
            export_zip,
            state_head=snapshot_head,
            plan_head="cccccccccccccccccccccccccccccccccccccccc",
        ),
        validation_mode=PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL,
        external_state_files=_accepted_live_state(snapshot_head),
    )
    _assert_failure(
        "next-gate-stale-copied-context",
        "does not match live external state",
        lambda packet, export_zip: _snapshot_context(packet, export_zip, state_head=snapshot_head),
        validation_mode=PACKET_VALIDATION_MODE_NEXT_GATE,
        external_state_files=_fresh_live_state(live_head),
    )
    _assert_failure(
        "accepted-historical-run-as-active-review",
        "does not match live external state",
        lambda packet, export_zip: _snapshot_context(packet, export_zip, state_head=snapshot_head),
        validation_mode=PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
        external_state_files=_accepted_live_state(snapshot_head),
    )
    _assert_success(
        "accepted-packet-not-regenerated-for-live-byte-match",
        lambda packet, export_zip: _snapshot_context(packet, export_zip, state_head=snapshot_head),
        validation_mode=PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL,
        external_state_files=_accepted_live_state(snapshot_head, live_head=live_head),
    )
    _assert_success(
        "new-next-gate-fresh-copied-context",
        lambda packet, export_zip: _snapshot_context(packet, export_zip, state_head=live_head),
        validation_mode=PACKET_VALIDATION_MODE_NEXT_GATE,
        external_state_files=_fresh_live_state(live_head),
    )
    historical_zip_name = "FAM-007-20260623-123429.zip"
    _assert_failure(
        "next-gate-recorded-accepted-historical-same-label-zip-still-fails-cleanup",
        "Stale same-label USER packet ZIP remains",
        lambda packet, export_zip: _snapshot_context_with_historical_zip(
            packet,
            export_zip,
            head=live_head,
            historical_zip_name=historical_zip_name,
        ),
        validation_mode=PACKET_VALIDATION_MODE_NEXT_GATE,
        external_state_files=_fresh_live_state_with_historical_zip(live_head, historical_zip_name),
        extra_zip_names=(historical_zip_name,),
    )
    _assert_generation_cleanup_removes_recorded_historical_zip()
    _assert_failure(
        "next-gate-unrecorded-same-label-zip-still-fails",
        "Stale same-label USER packet ZIP remains",
        lambda packet, export_zip: _snapshot_context(packet, export_zip, state_head=live_head),
        validation_mode=PACKET_VALIDATION_MODE_NEXT_GATE,
        external_state_files=_fresh_live_state(live_head),
        extra_zip_names=(historical_zip_name,),
    )
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
