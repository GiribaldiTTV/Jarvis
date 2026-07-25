# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-false-green-fixtures; status=shared
"""Regression fixtures for USER review packet false-green classes."""

from __future__ import annotations

import base64
import inspect
import json
import re
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

FIXTURE_ORIGIN_MAIN = "b" * 40


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
        original_git_output = bundle._git_output
        live_origin_main = _current_origin_main()
        fixture_origin_main = expected_origin_main or live_origin_main
        if expected_origin_main is None and fixture_origin_main == "UNKNOWN":
            fixture_origin_main = FIXTURE_ORIGIN_MAIN

            def fixture_git_output(*args: str) -> str:
                if args == ("rev-parse", "origin/main"):
                    return fixture_origin_main
                return original_git_output(*args)

            bundle._git_output = fixture_git_output
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
                    else fixture_origin_main
                ),
            ).failures
        finally:
            bundle._git_output = original_git_output
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


def _assert_fam007_canonical_active_surface_fixtures() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-fam007-canonical-root-") as temp_dir:
        review_root = Path(temp_dir)
        packet = review_root / "FAM-007"
        packet.mkdir()
        export_zip = review_root / "FAM-007-20260724-120000.zip"
        kwargs = {
            "validation_mode": PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
            "expected_branch": "feature/fam-007-ai-dashboard-child-domain-diagnostics",
        }

        failures = bundle._fam007_active_surface_failures(
            packet,
            export_zip,
            "FAM-007",
            **kwargs,
        )
        if failures:
            raise AssertionError(
                "canonical FAM-007 active surface failed unexpectedly:\n"
                + "\n".join(failures)
            )

        unrelated = review_root / "FAM-006"
        unrelated.mkdir()
        failures = bundle._fam007_active_surface_failures(
            packet,
            export_zip,
            "FAM-007",
            **kwargs,
        )
        if failures:
            raise AssertionError(
                "unrelated family artifact was treated as FAM-007 drift:\n"
                + "\n".join(failures)
            )

        stage_folder = review_root / "FAM-007-Decomposition"
        stage_folder.mkdir()
        failures = bundle._fam007_active_surface_failures(
            packet,
            export_zip,
            "FAM-007",
            **kwargs,
        )
        if not any("Parallel or stale FAM-007" in failure for failure in failures):
            raise AssertionError("parallel FAM-007 stage folder was not rejected")
        stage_folder.rmdir()

        transfer_folder = review_root / "FAM-007-20260723-171541-upload-parts"
        transfer_folder.mkdir()
        failures = bundle._fam007_active_surface_failures(
            packet,
            export_zip,
            "FAM-007",
            **kwargs,
        )
        if not any("Parallel or stale FAM-007" in failure for failure in failures):
            raise AssertionError("FAM-007 transfer-part folder was not rejected")
        transfer_folder.rmdir()

        loose_receipt = review_root / "UTS - FAM-007.txt"
        loose_receipt.write_text("historical receipt", encoding="utf-8")
        failures = bundle._fam007_active_surface_failures(
            packet,
            export_zip,
            "FAM-007",
            **kwargs,
        )
        if not any("Parallel or stale FAM-007" in failure for failure in failures):
            raise AssertionError("loose FAM-007 root receipt was not rejected")
        loose_receipt.unlink()

        stage_packet = review_root / "FAM-007-Decomposition"
        stage_export = review_root / "FAM-007-Decomposition-20260724-120000.zip"
        failures = bundle._fam007_active_surface_failures(
            stage_packet,
            stage_export,
            "FAM-007-Decomposition",
            **kwargs,
        )
        if not any("stage-neutral" in failure for failure in failures):
            raise AssertionError("stage-specific FAM-007 active label was not rejected")
        historical_failures = bundle._fam007_active_surface_failures(
            stage_packet,
            stage_export,
            "FAM-007-Decomposition",
            validation_mode=PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL,
            expected_branch=kwargs["expected_branch"],
        )
        if historical_failures:
            raise AssertionError(
                "accepted-historical FAM-007 stage packet was treated as active drift:\n"
                + "\n".join(historical_failures)
            )

    generation_failures = bundle._fam007_generation_label_failures(
        "FAM-007-Decomposition"
    )
    if not generation_failures:
        raise AssertionError("FAM-007 generation accepted a stage-specific active label")
    if bundle._fam007_generation_label_failures("FAM-007"):
        raise AssertionError("FAM-007 generation rejected its canonical family label")


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
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
    ):
        raise AssertionError("The FAM-007 Stage 2 decision was not classified as Stage 2")
    if bundle._is_pr_readiness_stage2_packet(
        source_branch=source_branch,
        normalized_decision=normalized_decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_REPAIR,
    ):
        raise AssertionError(
            "A repair-required Stage 1 outcome bypassed the Stage 2 readiness gate"
        )
    if bundle._is_pr_readiness_stage1_packet(
        source_branch=source_branch,
        normalized_decision=normalized_decision,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
    ):
        raise AssertionError(
            "An actual FAM-007 Stage 2 decision after Stage 1 readiness was misclassified as Stage 1"
        )
    primary = bundle._primary_user_review_file(
        decision,
        source_branch=source_branch,
        stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
    )
    if primary != "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md":
        raise AssertionError(
            "An actual FAM-007 Stage 2 packet after Stage 1 readiness must keep "
            f"WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md primary; found {primary!r}."
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
            stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
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

    with tempfile.TemporaryDirectory(prefix="ndai-governance-stage1-support-context-") as temp_dir:
        target = Path(temp_dir) / "Review Aids"
        target.mkdir(parents=True)
        support = bundle._write_user_branch_plan_review(
            target=target,
            title="Governance Stage 1 Ready Support Context",
            review_purpose="PR Readiness Stage 1 ready support context.",
            source_branch="feature/release-readiness-source-truth-intake",
            source_head="a" * 40,
            upstream="origin/feature/release-readiness-source-truth-intake",
            origin_main="b" * 40,
            exact_user_decision=decision,
            pending_user_decisions=["PR Readiness Stage 2 remains pending USER approval."],
            copied=[],
            stage1_outcome=bundle.PR_STAGE1_OUTCOME_READY,
        )
        support_text = support.read_text(encoding="utf-8").casefold()
        for forbidden in (
            "does user approve pr readiness stage 1 analysis",
            "pending user response - bp2 gate remains open",
            "accept the bp2 engineering plan as written",
        ):
            if forbidden in support_text:
                raise AssertionError(
                    "Governance Stage 1-ready support context retained stale gate wording: "
                    + forbidden
                )
        for required in (
            "context only",
            "stage 1 is ready for the separate stage 2 user decision",
            "stage 2 remains pending",
        ):
            if required not in support_text:
                raise AssertionError(
                    "Governance Stage 1-ready support context omitted required wording: "
                    + required
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


def _assert_stage1_repair_status_is_machine_readable() -> None:
    text = (
        "Decision Path Summary: pr readiness stage1 repair review - Stage 1 remains held.\n"
        "PR Readiness Stage 2 is not supported."
    )
    status = bundle._packet_text_status(text)
    if status != bundle.DECISION_STATUS_PR_READINESS_STAGE1_REVIEW:
        raise AssertionError(
            "generator-emitted Stage 1 repair status was not classified as the Stage 1 review status: "
            + status
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

    binary_coverage = {
        "START_HERE.md": (
            "Primary USER Review File: `USER Review/PR_READINESS_STAGE1_REVIEW.md`\n"
        ),
        "Review Aids/PR_READINESS_STAGE1_SOURCE_COVERAGE.md": (
            "`Source Truth Context/Docs__Main.md`\n"
            "`Source Truth Context/dev__orin_user_review_bundle.py`\n"
            "Copied Source Count: `2`\n"
        ),
    }
    binary_coverage_failures = bundle._pr_stage1_source_coverage_failures(
        binary_coverage,
        packet_entries=set(binary_coverage)
        | {"Source Truth Context/Docs__Main.md"}
        | {"Source Truth Context/dev__orin_user_review_bundle.py"},
    )
    if binary_coverage_failures:
        raise AssertionError(
            "binary source coverage was not counted from packet entries: "
            + "; ".join(binary_coverage_failures)
        )

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


def _assert_stale_primary_aid_is_not_skipped() -> None:
    packet_files = {
        "START_HERE.md": (
            "Primary USER Review File: USER Review/FALSE_GREEN_FIXTURE_REVIEW.md\n"
            "Current Gate: Systemic false-green regression fixture review\n"
        ),
        "USER Review/FALSE_GREEN_FIXTURE_REVIEW.md": "Current review.\n",
        "Review Aids/USER_BRANCH_PLAN_REVIEW.md": (
            "USER_BRANCH_PLAN_REVIEW.md is the primary active decision file.\n"
        ),
    }
    failures = bundle._active_review_aid_false_green_failures(packet_files)
    if not any("stale primary/current decision file" in failure for failure in failures):
        raise AssertionError(
            "non-Stage-1 stale primary aid was skipped:\n" + "\n".join(failures)
        )


def _assert_misrouted_stage1_primary_runs_all_guards() -> None:
    packet_files = {
        "START_HERE.md": (
            "Primary USER Review File: USER Review/USER_BRANCH_PLAN_REVIEW.md\n"
            "Current Gate: PR Readiness Stage 1\n"
            "Decision Path Summary: pr readiness stage1 approval review - Stage 1 remains held.\n"
        ),
        "Review Aids/USER_BRANCH_PLAN_REVIEW.md": (
            "BP2 planning context is not the current PR Readiness Stage 1 decision surface.\n"
        ),
        "Review Aids/USER_BRANCH_VISION_REVIEW.md": (
            "Supporting BP1 context only.\n"
        ),
        "Source Truth Context/Docs__Main.md": "# Main\n",
        "Review Aids/PR_READINESS_STAGE1_SOURCE_COVERAGE.md": (
            "Copied Source Count: `0`\n"
        ),
    }
    review_failures = bundle._pr_stage1_review_failures(packet_files)
    coherence_failures = bundle._pr_stage1_packet_coherence_failures(packet_files)
    coverage_failures = bundle._pr_stage1_source_coverage_failures(
        packet_files,
        packet_entries=set(packet_files),
    )
    failures = review_failures + coherence_failures + coverage_failures
    if not any("PR Stage 1 packet must identify" in failure for failure in failures):
        raise AssertionError(
            "misrouted Stage 1 primary did not fail primary routing:\n"
            + "\n".join(failures)
        )
    if not any("PR Readiness Stage 1 primary artifact is missing" in failure for failure in failures):
        raise AssertionError(
            "misrouted Stage 1 primary skipped the dedicated artifact guard:\n"
            + "\n".join(failures)
        )
    if not any("copied source files missing from coverage list" in failure for failure in failures):
        raise AssertionError(
            "misrouted Stage 1 primary skipped source coverage validation:\n"
            + "\n".join(failures)
        )


def _assert_stage1_zip_start_here_contract() -> None:
    valid = (
        "Primary USER Review File: USER Review/PR_READINESS_STAGE1_REVIEW.md\n"
        "Current Gate: PR Readiness Stage 1\n"
        "Review Purpose: Current PR Readiness Stage 1 review.\n"
        "USER Decision This Packet Supports: Stage 1 decision.\n"
    )
    for missing, needle in (
        ("Review Purpose:", "missing Review Purpose"),
        (
            "USER Decision This Packet Supports:",
            "missing USER Decision This Packet Supports",
        ),
    ):
        failures = bundle._start_here_contract_failures(valid.replace(missing, ""))
        if not any(needle in failure for failure in failures):
            raise AssertionError(
                f"Stage 1 ZIP START_HERE guard did not reject {missing!r}: {failures}"
            )
    if bundle._start_here_contract_failures(valid):
        raise AssertionError("complete Stage 1 ZIP START_HERE contract failed")


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


DECOMPOSITION_ACCEPTANCE_RECEIPT = "USER-DECISION-1-FIXTURE"
DECOMPOSITION_ACCEPTANCE_TEXT = (
    bundle.FAM007_DECOMPOSITION_ACCEPTANCE_EXACT_USER_DECISION
)


def _decomposition_state_values(
    state: str,
    *,
    candidate_code: str = "NONE",
    candidate_name: str = "NONE",
) -> dict[str, str]:
    values = {
        "DECOMPOSITION_UNSELECTED": {
            "selected_next": "CONSUMED_NO_SUCCESSOR",
            "branch_exists": "NO",
            "branch_mutation": "NONE",
            "stage1": "NOT_STARTED",
            "stage2": "NOT_APPROVED",
            "identity": "NOT_APPLICABLE",
            "bp_entry": "NOT_APPROVED",
            "current_gate": "DECOMPOSITION_DECISION_1_REVIEW",
            "next_gate": "USER_DECISION_1_CURRENT_BRANCH_SUPERSESSION",
        },
        "DECOMPOSITION_ACCEPTED_NO_CANDIDATE": {
            "selected_next": "CONSUMED_NO_SUCCESSOR",
            "branch_exists": "NO",
            "branch_mutation": "NONE",
            "stage1": "NOT_STARTED",
            "stage2": "NOT_APPROVED",
            "identity": "NOT_APPLICABLE",
            "bp_entry": "NOT_APPROVED",
            "current_gate": "DECOMPOSITION_DECISION_2_REVIEW",
            "next_gate": "USER_DECISION_2_STAGE1_CANDIDATE_SELECTION",
        },
        "STAGE1_CANDIDATE_SELECTED": {
            "selected_next": "SELECTED_STAGE1_ANALYSIS_ONLY",
            "branch_exists": "NO",
            "branch_mutation": "NONE",
            "stage1": "ADMITTED_NOT_STARTED",
            "stage2": "NOT_APPROVED",
            "identity": "NOT_APPLICABLE",
            "bp_entry": "NOT_APPROVED",
            "current_gate": "BRANCH_READINESS_STAGE_1_ANALYSIS",
            "next_gate": "BRANCH_READINESS_STAGE_1_ANALYSIS_COMPLETE",
        },
        "STAGE1_ANALYSIS_COMPLETE": {
            "selected_next": "SELECTED_STAGE1_ANALYSIS_ONLY",
            "branch_exists": "NO",
            "branch_mutation": "NONE",
            "stage1": "COMPLETE",
            "stage2": "NOT_APPROVED",
            "identity": "NOT_APPLICABLE",
            "bp_entry": "NOT_APPROVED",
            "current_gate": "USER_BRANCH_READINESS_STAGE_2_DECISION",
            "next_gate": "BRANCH_READINESS_STAGE_2_IF_APPROVED",
        },
        "STAGE2_CREATION_APPROVED": {
            "selected_next": "SELECTED_STAGE1_ANALYSIS_ONLY",
            "branch_exists": "NO",
            "branch_mutation": "APPROVED_NOT_EXECUTED",
            "stage1": "COMPLETE",
            "stage2": "APPROVED",
            "identity": "NOT_APPLICABLE",
            "bp_entry": "NOT_APPROVED",
            "current_gate": "BRANCH_READINESS_STAGE_2_EXECUTION",
            "next_gate": "SUCCESSOR_IDENTITY_VERIFICATION",
        },
        "SUCCESSOR_CREATED_IDENTITY_VERIFIED": {
            "selected_next": "SELECTED_SUCCESSOR_CREATED",
            "branch_exists": "YES",
            "branch_mutation": "COMPLETED",
            "stage1": "COMPLETE",
            "stage2": "APPROVED",
            "identity": "VERIFIED",
            "bp_entry": "NOT_APPROVED",
            "current_gate": "SUCCESSOR_IDENTITY_VERIFIED",
            "next_gate": "USER_BRANCH_PLANNING_ENTRY_DECISION",
        },
        "BRANCH_PLANNING_ENTRY_APPROVED": {
            "selected_next": "SELECTED_SUCCESSOR_CREATED",
            "branch_exists": "YES",
            "branch_mutation": "COMPLETED",
            "stage1": "COMPLETE",
            "stage2": "APPROVED",
            "identity": "VERIFIED",
            "bp_entry": "APPROVED",
            "current_gate": "BRANCH_PLANNING_ENTRY_APPROVED",
            "next_gate": "BP1_USER_BRANCH_VISION_REVIEW",
        },
    }[state]
    return {
        **values,
        "state": state,
        "candidate_code": candidate_code,
        "candidate_name": candidate_name,
    }


def _decomposition_approval_values(values: dict[str, str]) -> dict[str, str]:
    state = values["state"]
    candidate_name = values["candidate_name"]
    decomposition_accepted = state != "DECOMPOSITION_UNSELECTED"
    stage1_selected = state in {
        "STAGE1_CANDIDATE_SELECTED",
        "STAGE1_ANALYSIS_COMPLETE",
        "STAGE2_CREATION_APPROVED",
        "SUCCESSOR_CREATED_IDENTITY_VERIFIED",
        "BRANCH_PLANNING_ENTRY_APPROVED",
    }
    stage2_or_later = state in {
        "STAGE2_CREATION_APPROVED",
        "SUCCESSOR_CREATED_IDENTITY_VERIFIED",
        "BRANCH_PLANNING_ENTRY_APPROVED",
    }
    identity_verified = state in {
        "SUCCESSOR_CREATED_IDENTITY_VERIFIED",
        "BRANCH_PLANNING_ENTRY_APPROVED",
    }
    bp_entry = state == "BRANCH_PLANNING_ENTRY_APPROVED"
    return {
        "decomposition_receipt": (
            DECOMPOSITION_ACCEPTANCE_RECEIPT if decomposition_accepted else "NONE"
        ),
        "decomposition_text": (
            DECOMPOSITION_ACCEPTANCE_TEXT if decomposition_accepted else "NONE"
        ),
        "decomposition_target": (
            "CURRENT_FAM007_DECOMPOSITION_CARRIER"
            if decomposition_accepted
            else "NONE"
        ),
        "decomposition_stage": (
            "DECISION_1_DECOMPOSITION_ACCEPTANCE"
            if decomposition_accepted
            else "NONE"
        ),
        "decomposition_scope": (
            "CURRENT_BRANCH_POSTURE_ONLY" if decomposition_accepted else "NONE"
        ),
        "decomposition_prohibited": (
            "SUCCESSOR_SELECTION; BRANCH_READINESS_STAGE_1; STAGE_2; "
            "BRANCH_WORKTREE_CREATION; BRANCH_PLANNING_ENTRY; IMPLEMENTATION"
            if decomposition_accepted
            else "NONE"
        ),
        "decomposition_reference": (
            "USER_MESSAGE_FIXTURE_DECISION_1" if decomposition_accepted else "NONE"
        ),
        "stage1_receipt": (
            "USER-STAGE1-SELECTION-FIXTURE" if stage1_selected else "NONE"
        ),
        "stage1_text": (
            f"I approve {candidate_name} for Branch Readiness Stage 1 analysis only; "
            "no branch/worktree mutation; Stage 2 remains separate; "
            "Branch Planning Entry remains separate."
            if stage1_selected
            else "NONE"
        ),
        "stage1_target": (
            "CURRENT_FAM007_DECOMPOSITION_CARRIER" if stage1_selected else "NONE"
        ),
        "stage1_stage": (
            "DECISION_2_STAGE1_CANDIDATE_SELECTION" if stage1_selected else "NONE"
        ),
        "stage1_scope": (
            "NAMED_CANDIDATE_STAGE1_ANALYSIS_ONLY" if stage1_selected else "NONE"
        ),
        "stage1_prohibited": (
            "BRANCH_WORKTREE_MUTATION; STAGE_2; BRANCH_PLANNING_ENTRY; "
            "IMPLEMENTATION"
            if stage1_selected
            else "NONE"
        ),
        "stage1_reference": (
            "USER_MESSAGE_FIXTURE_DECISION_2" if stage1_selected else "NONE"
        ),
        "stage2_receipt": (
            "USER-STAGE2-CREATION-FIXTURE" if stage2_or_later else "NONE"
        ),
        "stage2_text": (
            f"I approve {candidate_name} for Branch Readiness Stage 2 "
            "branch/worktree creation only; Branch Planning Entry remains separate; "
            "implementation remains blocked."
            if stage2_or_later
            else "NONE"
        ),
        "stage2_target": (
            "NAMED_SUCCESSOR_CARRIER" if stage2_or_later else "NONE"
        ),
        "stage2_stage": (
            "BRANCH_READINESS_STAGE_2_CREATION_APPROVAL"
            if stage2_or_later
            else "NONE"
        ),
        "stage2_scope": (
            "ONE_SUCCESSOR_BRANCH_WORKTREE_CREATION_ONLY"
            if stage2_or_later
            else "NONE"
        ),
        "stage2_prohibited": (
            "BRANCH_PLANNING_ENTRY; BP1; IMPLEMENTATION"
            if stage2_or_later
            else "NONE"
        ),
        "stage2_reference": (
            "USER_MESSAGE_FIXTURE_STAGE_2" if stage2_or_later else "NONE"
        ),
        "identity_receipt": (
            "SUCCESSOR-IDENTITY-FIXTURE" if identity_verified else "NONE"
        ),
        "identity_target": (
            "NAMED_SUCCESSOR_CARRIER" if identity_verified else "NONE"
        ),
        "identity_stage": (
            "SUCCESSOR_IDENTITY_VERIFICATION" if identity_verified else "NONE"
        ),
        "identity_scope": (
            "BRANCH_WORKTREE_IDENTITY_ONLY" if identity_verified else "NONE"
        ),
        "identity_prohibited": (
            "BRANCH_PLANNING_ENTRY; BP1; IMPLEMENTATION"
            if identity_verified
            else "NONE"
        ),
        "identity_reference": (
            "IDENTITY_PROOF_FIXTURE_SUCCESSOR" if identity_verified else "NONE"
        ),
        "bp_receipt": "USER-BP-ENTRY-FIXTURE" if bp_entry else "NONE",
        "bp_text": (
            f"I approve Branch Planning Entry for {candidate_name}; BP1 is next and "
            "implementation remains blocked."
            if bp_entry
            else "NONE"
        ),
        "bp_target": "NAMED_SUCCESSOR_CARRIER" if bp_entry else "NONE",
        "bp_stage": "BRANCH_PLANNING_ENTRY_APPROVAL" if bp_entry else "NONE",
        "bp_scope": "BP1_ENTRY_ONLY" if bp_entry else "NONE",
        "bp_prohibited": (
            "BP2; BP3; WORKSTREAM; IMPLEMENTATION" if bp_entry else "NONE"
        ),
        "bp_reference": "USER_MESSAGE_FIXTURE_BP_ENTRY" if bp_entry else "NONE",
    }


def _decomposition_state_text(values: dict[str, str], route: str) -> str:
    approvals = _decomposition_approval_values(values)
    return "\n".join(
        [
            "# Current Decomposition State",
            f"Declared Decomposition State: `{values['state']}`",
            f"Named Candidate Code: `{values['candidate_code']}`",
            f"Named Candidate: `{values['candidate_name']}`",
            f"Selected-next Posture: `{values['selected_next']}`",
            f"Shell / Lifecycle Route Code: `{route}`",
            f"Successor Branch / Worktree Exists: `{values['branch_exists']}`",
            f"Branch / Worktree Mutation: `{values['branch_mutation']}`",
            f"Stage 1 Analysis Status: `{values['stage1']}`",
            f"Stage 2 Creation Approval: `{values['stage2']}`",
            f"Successor Identity Verification: `{values['identity']}`",
            f"Branch Planning Entry Approval: `{values['bp_entry']}`",
            "Implementation Approval: `NOT_APPROVED`",
            f"Current Gate Code: `{values['current_gate']}`",
            f"Next Legal Gate Code: `{values['next_gate']}`",
            "Forbidden Phase Collapse: `CONFIRMED`",
            f"Decomposition Acceptance Receipt: `{approvals['decomposition_receipt']}`",
            f"Decomposition Acceptance Exact USER Decision: `{approvals['decomposition_text']}`",
            f"Decomposition Acceptance Target Carrier: `{approvals['decomposition_target']}`",
            f"Decomposition Acceptance Approval Stage: `{approvals['decomposition_stage']}`",
            f"Decomposition Acceptance Approval Scope: `{approvals['decomposition_scope']}`",
            f"Decomposition Acceptance Prohibited Later Gates: `{approvals['decomposition_prohibited']}`",
            f"Decomposition Acceptance Record Reference: `{approvals['decomposition_reference']}`",
            f"Stage 1 Selection Approval Receipt: `{approvals['stage1_receipt']}`",
            f"Stage 1 Selection Exact USER Decision: `{approvals['stage1_text']}`",
            f"Stage 1 Selection Target Carrier: `{approvals['stage1_target']}`",
            f"Stage 1 Selection Approval Stage: `{approvals['stage1_stage']}`",
            f"Stage 1 Selection Approval Scope: `{approvals['stage1_scope']}`",
            f"Stage 1 Selection Prohibited Later Gates: `{approvals['stage1_prohibited']}`",
            f"Stage 1 Selection Record Reference: `{approvals['stage1_reference']}`",
            f"Stage 2 Creation Approval Receipt: `{approvals['stage2_receipt']}`",
            f"Stage 2 Creation Exact USER Decision: `{approvals['stage2_text']}`",
            f"Stage 2 Creation Target Carrier: `{approvals['stage2_target']}`",
            f"Stage 2 Creation Approval Stage: `{approvals['stage2_stage']}`",
            f"Stage 2 Creation Approval Scope: `{approvals['stage2_scope']}`",
            f"Stage 2 Creation Prohibited Later Gates: `{approvals['stage2_prohibited']}`",
            f"Stage 2 Creation Record Reference: `{approvals['stage2_reference']}`",
            f"Successor Identity Receipt: `{approvals['identity_receipt']}`",
            f"Successor Identity Target Carrier: `{approvals['identity_target']}`",
            f"Successor Identity Verification Stage: `{approvals['identity_stage']}`",
            f"Successor Identity Verification Scope: `{approvals['identity_scope']}`",
            f"Successor Identity Prohibited Later Gates: `{approvals['identity_prohibited']}`",
            f"Successor Identity Record Reference: `{approvals['identity_reference']}`",
            f"Branch Planning Entry Approval Receipt: `{approvals['bp_receipt']}`",
            f"Branch Planning Entry Exact USER Decision: `{approvals['bp_text']}`",
            f"Branch Planning Entry Target Carrier: `{approvals['bp_target']}`",
            f"Branch Planning Entry Approval Stage: `{approvals['bp_stage']}`",
            f"Branch Planning Entry Approval Scope: `{approvals['bp_scope']}`",
            f"Branch Planning Entry Prohibited Later Gates: `{approvals['bp_prohibited']}`",
            f"Branch Planning Entry Record Reference: `{approvals['bp_reference']}`",
        ]
    )


def _decomposition_transition_model_text(current_state: str) -> str:
    states = "\n".join(
        f"| `{state}` | Required USER Approval Receipt | Forbidden Receipts | Selected-next Posture | "
        "Named Candidate | Branch / Worktree Existence | Allowed Mutation | "
        "Required Packet Artifacts | Current Gate | Next Legal Gate | "
        "Forbidden Phase Collapse |"
        for state in bundle.FAM007_DECOMPOSITION_STATES
    )
    return (
        "# Decomposition Transition State Model\n\n"
        f"Current Packet State: `{current_state}`\n\n"
        "The rows below define validator capability. Only the declared current packet "
        "state controls this packet.\n\n"
        "| State | Required USER Approval Receipt | Forbidden Receipts | Selected-next Posture | "
        "Named Candidate | Branch / Worktree Existence | Allowed Mutation | "
        "Required Packet Artifacts | Current Gate | Next Legal Gate | "
        "Forbidden Phase Collapse |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        f"{states}\n"
    )


def _receipt_requirement_matrix_text(current_state: str) -> str:
    expectation = bundle.FAM007_DECOMPOSITION_STATE_CONTRACTS[current_state]
    return "\n".join(
        [
            "# Receipt Requirement Matrix",
            "",
            f"Current Packet State: `{current_state}`",
            "Current Required Receipts: "
            f"`{bundle._fam007_decomposition_receipt_set_code(expectation['required_receipts'])}`",
            "Current Forbidden Receipts: "
            f"`{bundle._fam007_decomposition_receipt_set_code(expectation['forbidden_receipts'])}`",
            "",
            "Each transition uses explicit Required Receipts and Forbidden Receipts contracts.",
            "",
            "| Receipt | Receipt Identifier | Exact USER Decision | Target Carrier / Branch | Approval Stage | Approval Scope | Prohibited Later Gates | Timestamp / Routed Record Reference |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            "| Decomposition Acceptance Receipt | required after Decision 1 | exact canonical text | current decomposition carrier | Decision 1 | posture only | successor and later gates | required |",
            "| Stage 1 Candidate-Selection Receipt | required after Decision 2 | exact candidate-specific text | current decomposition carrier | Decision 2 | Stage 1 analysis only | mutation and later gates | required |",
            "| Stage 2 Creation Receipt | required after separate approval | exact candidate-specific text | named successor carrier | Stage 2 | one creation only | BP and implementation | required |",
            "| Successor Identity Receipt | required after creation | not a USER approval | named successor carrier | identity verification | identity only | BP and implementation | required |",
            "| Branch Planning Entry Receipt | required after separate approval | exact candidate-specific text | named successor carrier | BP entry | BP1 entry only | BP2 and later gates | required |",
            "| Issue #307 Resolution Receipt | required only for atomic resolution | exact route/owner text | Issue #307 carrier | issue resolution | one final owner | implementation, closeout, issue mutation | required |",
        ]
    )


def _approval_stage_table_text(state: str) -> str:
    rows = bundle._fam007_decomposition_approval_authorizations(state)
    lines = [
        "# Approval stage table",
        "",
        "| Stage | Action / legal carrier | Required artifact | Mutation occurs | Required USER approval | Current authorization | Next permissible action | Prohibited progression |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for stage_name, authorization in rows.items():
        lines.append(
            f"| {stage_name} | fixture carrier | fixture artifact | no | separate gate | "
            f"{authorization} | source-truth-routed next action | no phase collapse |"
        )
    return "\n".join(lines)


def _recovery_ledger_text(state: str) -> str:
    approval_recorded = "NO" if state == "DECOMPOSITION_UNSELECTED" else "YES"
    return "\n".join(
        [
            "# Current-Gate Recovery Defect Ledger",
            "",
            "Current Result: `REPAIRED_AND_REVALIDATED`",
            f"Current State Preserved: `{state}`",
            f"USER Approval Recorded: `{approval_recorded}`",
        ]
    )


def _route_rules_text(route: str) -> str:
    return "\n".join(
        [
            "# Transition-Safe Route Rules",
            f"Declared Route: `{route}`",
            "Route A permits separate visual-shell and lifecycle carriers with complete ownership and proof boundaries.",
            "Route B requires source-truth permission, explicit shared-shell invariance, and child-local or exact-owner-local lifecycle ownership.",
            "Route C requires complete indivisibility, unsafe-separation, independent visual/lifecycle adjudication, bounded carrier, rollback, and proof evidence.",
            "Same-file or same-class placement is never sufficient atomicity proof.",
        ]
    )


def _route_separability_text(route: str) -> str:
    common = [f"Declared Route: `{route}`"]
    if route == "ROUTE_A_SEPARATE":
        return "\n".join(
            [
                "# Separability",
                *common,
                "Selected route: Route A - separate shared carriers.",
                "Code-region result: SEPARABLE.",
                "Visual Shell Ownership: `SEPARATE_CARRIER`",
                "Lifecycle Ownership: `SEPARATE_CARRIER`",
                "Code-Region Ownership: `COMPLETE`",
                "Dependency Boundaries: `EXPLICIT`",
                "Proof Boundaries: `EXPLICIT`",
                "Same-File/Class Atomicity Claim: `NOT_USED`",
            ]
        )
    if route == "ROUTE_B_SHARED_SHELL_LOCAL_LIFECYCLE":
        return "\n".join(
            [
                "# Separability",
                *common,
                "Selected route: Route B - shared shell with exact-owner-local lifecycle.",
                "Source-Truth Route Permission: `CONFIRMED`",
                "Visual Shell Sharing: `EXPLICIT`",
                "Lifecycle Ownership: `CHILD_LOCAL_OR_EXACT_OWNER_LOCAL`",
                "Code-Region Ownership: `COMPLETE`",
                "Cross-Window Invariance Proof: `COMPLETE`",
                "Dependency Boundaries: `EXPLICIT`",
                "Proof Boundaries: `EXPLICIT`",
                "Same-File/Class Atomicity Claim: `NOT_USED`",
            ]
        )
    return "\n".join(
        [
            "# Separability",
            *common,
            "Selected route: Route C - one combined shell/lifecycle carrier.",
            "Atomicity Result: `PROVEN_INDIVISIBLE`",
            "Unsafe Separation Evidence: `COMPLETE`",
            "Independent Visual Adjudication: `COMPLETE`",
            "Independent Lifecycle Adjudication: `COMPLETE`",
            "Child-Specific Product Work: `EXCLUDED`",
            "Carrier Boundary: `BOUNDED`",
            "Rollback Boundary: `EXPLICIT`",
            "Proof Boundary: `EXPLICIT`",
            "Same-File/Class Atomicity Claim: `NOT_USED`",
        ]
    )


def _apply_decomposition_state(
    files: dict[str, str],
    state: str,
    *,
    candidate_code: str = "NONE",
    candidate_name: str = "NONE",
) -> None:
    route = bundle._fam007_field_code(
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"],
        "Shell / Lifecycle Route Code",
    )
    values = _decomposition_state_values(
        state,
        candidate_code=candidate_code,
        candidate_name=candidate_name,
    )
    approvals = _decomposition_approval_values(values)
    decision1_state = (
        "PENDING_USER_DECISION"
        if state == "DECOMPOSITION_UNSELECTED"
        else "ACCEPTED"
    )
    decision2_state = (
        "NOT_REACHED"
        if state == "DECOMPOSITION_UNSELECTED"
        else (
            "PENDING_USER_DECISION"
            if state == "DECOMPOSITION_ACCEPTED_NO_CANDIDATE"
            else "ACCEPTED"
        )
    )
    files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = (
        _decomposition_state_text(values, route)
    )
    files["Review Aids/CURRENT_GATE_RECOVERY_DEFECT_LEDGER.md"] = (
        _recovery_ledger_text(state)
    )
    files["Review Aids/DECOMPOSITION_TRANSITION_STATE_MODEL.md"] = (
        _decomposition_transition_model_text(state)
    )
    files["Review Aids/RECEIPT_REQUIREMENT_MATRIX.md"] = (
        _receipt_requirement_matrix_text(state)
    )
    files["Review Aids/APPROVAL_STAGE_TABLE.md"] = (
        _approval_stage_table_text(state)
    )
    files["START_HERE.md"] = "\n".join(
        [
            "# FAM-007 Decomposition Decision Packet",
            f"Declared Decomposition State: `{state}`",
            f"Selected-next Posture: `{values['selected_next']}`",
            f"Named Candidate: `{candidate_name}`",
            f"Decision 1 State: `{decision1_state}`",
            f"Decision 2 State: `{decision2_state}`",
            "Final Packet Receipt Authority: active external state after ZIP generation; no loose sidecar is permitted.",
            "Primary USER Review File: `USER Review/FAM007_BRANCH_SUPERSESSION_DECOMPOSITION_REVIEW.md`",
        ]
    )
    files["USER Review/FAM007_BRANCH_SUPERSESSION_DECOMPOSITION_REVIEW.md"] = "\n".join(
        [
            "# FAM-007 Decomposition Review",
            f"Declared Decomposition State: `{state}`",
            f"Selected-next Posture: `{values['selected_next']}`",
            f"Named Candidate: `{candidate_name}`",
            f"Decision 1 State: `{decision1_state}`",
            f"Decision 2 State: `{decision2_state}`",
            "Review the decomposition and legal successor analysis route. "
            "This current-gate review does not authorize implementation.",
            *(
                [
                    "Exact Next USER Decision: "
                    f"`{bundle.FAM007_DECOMPOSITION_ACCEPTANCE_EXACT_USER_DECISION}`"
                ]
                if state == "DECOMPOSITION_UNSELECTED"
                else []
            ),
        ]
    )
    files["Review Aids/SELECTED_NEXT_STATE_RECEIPT.md"] = "\n".join(
        [
            "# Selected-Next State Receipt",
            f"Declared Decomposition State: `{state}`",
            f"Named Candidate Code: `{candidate_code}`",
            f"Named Candidate: `{candidate_name}`",
            f"Selected-next Posture: `{values['selected_next']}`",
            "External-State Consistency: `CONFIRMED`",
        ]
    )
    ai_posture = (
        "SELECTED_FOR_STAGE1_ANALYSIS_ONLY"
        if candidate_code == "AI_READINESS_DIAGNOSTICS"
        else "RECOMMENDATION_ONLY_NOT_SELECTED"
    )
    ai_receipt = (
        approvals["stage1_receipt"]
        if candidate_code == "AI_READINESS_DIAGNOSTICS"
        else "NONE"
    )
    files["Review Aids/AI_READINESS_RECOMMENDATION_SELECTION_RECEIPT.md"] = "\n".join(
        [
            "# AI Readiness Recommendation / Selection Receipt",
            f"Declared Decomposition State: `{state}`",
            f"Named Candidate Code: `{candidate_code}`",
            f"AI Readiness Posture: `{ai_posture}`",
            f"Stage 1 Selection Approval Receipt: `{ai_receipt}`",
        ]
    )
    files[
        "Source Truth Context/Proof Artifacts/Operational Receipts/IDENTITY_RECEIPT.md"
    ] = "\n".join(
        [
            "Worktree: exact",
            "Git Root: exact",
            "Branch: exact",
            "HEAD: exact",
            "Upstream: exact",
            "origin/main: exact",
            "Merge Base: exact",
            "Upstream Divergence: exact",
            "origin/main...HEAD Orientation: exact",
            "Cleanliness: clean",
            "Untracked Inventory: none",
            "Open PR State: none",
            "Current Phase: Live Validation",
            "Current Approval State: packet repair only",
            f"Declared Decomposition State: `{state}`",
            f"Selected-next State: `{values['selected_next']}`",
            f"Named Candidate Code: `{candidate_code}`",
            f"Successor Branch / Worktree Exists: `{values['branch_exists']}`",
            f"Successor Identity Verification: `{values['identity']}`",
            "Current Branch Role: decomposition",
            "Current Packet Receipt: exact",
            "Preserved Evidence Packet Receipt: exact",
        ]
    )
    issue307_state = bundle._fam007_field_code(
        files["Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md"],
        "Issue #307 Resolution State",
    )
    files[
        "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md"
    ] = "\n".join(
        [
            *[f"Projection {number}: exact" for number in range(1, 8)],
            "External State Schema: exact",
            "State Version: exact",
            "Target Branch: exact",
            "Target HEAD: exact",
            f"Declared Decomposition State: `{state}`",
            f"Named Candidate Code: `{candidate_code}`",
            f"Named Candidate: `{candidate_name}`",
            "Current Gate: exact",
            "Next Legal Gate: exact",
            "Packet Boundary: exact",
            f"Selected-next Posture: `{values['selected_next']}`",
            f"Shell / Lifecycle Route Code: `{route}`",
            f"Issue #307 Resolution State: `{issue307_state}`",
            f"Decomposition Acceptance Receipt: `{approvals['decomposition_receipt']}`",
            f"Stage 1 Selection Approval Receipt: `{approvals['stage1_receipt']}`",
            f"Stage 2 Creation Approval Receipt: `{approvals['stage2_receipt']}`",
            f"Successor Identity Receipt: `{approvals['identity_receipt']}`",
            f"Branch Planning Entry Approval Receipt: `{approvals['bp_receipt']}`",
            "Validation Result: PASS",
        ]
    )


def _apply_route(files: dict[str, str], route: str) -> None:
    for old_route in bundle.FAM007_DECOMPOSITION_ROUTE_CODES:
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(old_route, route)
        files[
            "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md"
        ] = files[
            "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md"
        ].replace(old_route, route)
    files["Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md"] = (
        _route_separability_text(route)
    )
    files["Review Aids/TRANSITION_SAFE_ROUTE_RULES.md"] = _route_rules_text(route)


def _resolve_issue307(
    files: dict[str, str],
    route: str = "USER_APPROVED_LIVE_ISSUE_CLARIFICATION",
) -> None:
    route_phrase = {
        "USER_APPROVED_SPLIT": "split",
        "USER_APPROVED_REPLACEMENT": "replacement",
        "USER_APPROVED_LIVE_ISSUE_CLARIFICATION": "live issue clarification",
    }[route]
    files["Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md"] = "\n".join(
        [
            "# Issue #307 Resolution Receipt",
            "Issue #307 Resolution State: `RESOLVED_ATOMIC`",
            f"Issue #307 Resolution Route: `{route}`",
            "Issue #307 USER Approval Receipt: `USER-ISSUE-307-FIXTURE`",
            f"Issue #307 Exact USER Decision: `I approve the Issue #307 {route_phrase} with one final closure owner F7-LIFECYCLE.`",
            "Issue #307 Approval Stage: `ISSUE_307_ATOMIC_RESOLUTION`",
            "Issue #307 Approval Scope: `ONE_ATOMIC_FINAL_CLOSURE_OWNER_ONLY`",
            "Issue #307 Prohibited Later Gates: `IMPLEMENTATION; CLOSEOUT; ISSUE_MUTATION`",
            "Issue #307 Record Reference: `USER_MESSAGE_FIXTURE_ISSUE_307`",
            "Issue #307 Final Closure Owner: `F7-LIFECYCLE`",
            "Issue / Ledger / Carrier Consistency: `CONFIRMED`",
            "Implementation Obligations Atomic: `YES`",
            "Proof Obligations Atomic: `YES`",
            "Historical Traceability Preserved: `YES`",
            "Implementation Or Closeout Allowed: `NO_SEPARATELY_GATED`",
        ]
    )
    files["Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md"] = files[
        "Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md"
    ].replace(
        "SPLIT_REQUIRED_BEFORE_IMPLEMENTATION_OR_CLOSEOUT",
        "ATOMIC_RESOLVED",
    )
    files[
        "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md"
    ] = files[
        "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md"
    ].replace(
        "Issue #307 Resolution State: `UNRESOLVED`",
        "Issue #307 Resolution State: `RESOLVED_ATOMIC`",
    )


def _valid_fam007_decomposition_packet_files() -> dict[str, str]:
    owners = {
        292: ("F7-SHELL", "F7-SHELL"),
        293: ("F7-SHELL", "F7-SHELL"),
        294: ("F7-SHELL", "F7-SHELL"),
        295: ("F7-CONTROL", "F7-CONTROL"),
        296: ("F7-READINESS", "F7-READINESS"),
        297: ("F7-CAPABILITIES", "F7-CAPABILITIES"),
        298: ("F7-CURRENT", "F7-CURRENT"),
        299: ("F7-CURRENT", "F7-CURRENT"),
        300: ("F7-CURRENT", "F7-CURRENT"),
        301: ("FAM001-RUNTIME", "FAM001-RUNTIME"),
        302: ("F7-CURRENT", "F7-CURRENT"),
        303: ("F7-CURRENT", "F7-CURRENT"),
        304: ("F7-CURRENT", "F7-CURRENT"),
        305: ("UI-STANDARDS", "UI-STANDARDS"),
        306: ("GOV-TOOLING", "GOV-TOOLING"),
        307: ("F7-LIFECYCLE", "F7-LIFECYCLE"),
        308: ("F7-PARENT", "F7-PARENT"),
    }
    ownership_lines = [
        "| Issue | Implementation Owner | Final Closure Owner | Inherited Proof Obligations | Downstream Acceptance Dependencies | Atomicity / Split | Dependency Contributors |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for issue_number, (implementation_owner, final_owner) in owners.items():
        split_state = (
            "SPLIT_REQUIRED_BEFORE_IMPLEMENTATION_OR_CLOSEOUT"
            if issue_number == 307
            else "ATOMIC"
        )
        ownership_lines.append(
            f"| #{issue_number} | `{implementation_owner}` | `{final_owner}` | "
            f"Window-specific proof | Later acceptance | `{split_state}` | `NONE` |"
        )

    files = {
        "START_HERE.md": "",
        "USER Review/FAM007_BRANCH_SUPERSESSION_DECOMPOSITION_REVIEW.md": "",
        "Review Aids/CURRENT_DECOMPOSITION_STATE.md": "",
        "Review Aids/CURRENT_GATE_RECOVERY_DEFECT_LEDGER.md": (
            _recovery_ledger_text("DECOMPOSITION_UNSELECTED")
        ),
        "Review Aids/DECOMPOSITION_TRANSITION_STATE_MODEL.md": (
            _decomposition_transition_model_text("DECOMPOSITION_UNSELECTED")
        ),
        "Review Aids/RECEIPT_REQUIREMENT_MATRIX.md": (
            _receipt_requirement_matrix_text("DECOMPOSITION_UNSELECTED")
        ),
        "Review Aids/TRANSITION_SAFE_ROUTE_RULES.md": _route_rules_text(
            "ROUTE_A_SEPARATE"
        ),
        "Review Aids/SELECTED_NEXT_STATE_RECEIPT.md": "",
        "Review Aids/AI_READINESS_RECOMMENDATION_SELECTION_RECEIPT.md": "",
        "Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md": "\n".join(
            [
                "# Issue #307 Resolution Receipt",
                "Issue #307 Resolution State: `UNRESOLVED`",
                "Issue #307 Resolution Route: `PENDING_USER_APPROVED_RESOLUTION`",
                "Issue #307 USER Approval Receipt: `NONE`",
                "Issue #307 Exact USER Decision: `NONE`",
                "Issue #307 Approval Stage: `NONE`",
                "Issue #307 Approval Scope: `NONE`",
                "Issue #307 Prohibited Later Gates: `NONE`",
                "Issue #307 Record Reference: `NONE`",
                "Issue #307 Final Closure Owner: `F7-LIFECYCLE`",
                "Issue / Ledger / Carrier Consistency: `CONFIRMED`",
                "Implementation Obligations Atomic: `NO`",
                "Proof Obligations Atomic: `NO`",
                "Historical Traceability Preserved: `YES`",
                "Implementation Or Closeout Allowed: `NO`",
            ]
        ),
        "Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md": (
            _route_separability_text("ROUTE_A_SEPARATE")
        ),
        "Review Aids/CORRECTED_CARRIER_MAP.md": "# Corrected carrier map\n",
        "Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md": "\n".join(
            ownership_lines
        ),
        "Review Aids/TYPED_SUCCESSOR_DEPENDENCY_GRAPH.md": "\n".join(
            [
                "# Typed dependency graph",
                "Implementation dependency",
                "Proof dependency",
                "Acceptance dependency",
                "Source-truth dependency",
                "Branch-creation dependency",
                "Branch Planning order",
                "Implementation order",
                "Acceptance order",
            ]
        ),
        "Review Aids/LEGAL_SUCCESSOR_ENTRY_SEQUENCE.md": "\n".join(
            [
                "# Legal successor entry sequence",
                "Branch Readiness Stage 1 - analysis with no branch mutation.",
                "Branch Readiness Stage 2 - separately approved.",
                "Branch/worktree creation - branch/worktree mutation occurs only in approved BR2.",
                "Branch Planning Entry - separate USER overlay after identity verification.",
                "BP1, BP2, and BP3 remain distinct planning gates.",
            ]
        ),
        "Review Aids/APPROVAL_STAGE_TABLE.md": (
            _approval_stage_table_text("DECOMPOSITION_UNSELECTED")
        ),
        "Review Aids/RISKS_AND_ROLLBACK.md": "# Risks and rollback\n",
        "Source Truth Context/Proof Artifacts/Operational Receipts/IDENTITY_RECEIPT.md": "",
        "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md": "",
        "Source Truth Context/Proof Artifacts/Operational Receipts/VALIDATION_RECEIPT.md": "\n".join(
            [
                "Command: exact",
                "Result: PASS",
                "Timestamp: exact",
                "Target Identity: exact",
                "Failed-Before-Pass Attempts: recorded",
                "Final Result: PASS",
            ]
        ),
    }
    files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = (
        _decomposition_state_text(
            _decomposition_state_values("DECOMPOSITION_UNSELECTED"),
            "ROUTE_A_SEPARATE",
        )
    )
    _apply_decomposition_state(files, "DECOMPOSITION_UNSELECTED")
    archive_root = r"D:\Nexus Artifacts\FAM-007\USER Review Archive"
    receipt_artifacts = [
        {
            "classification": classification,
            "originalPath": original_path,
            "archivedPath": archived_path,
            "sizeBytes": 123,
            "sha256": "A" * 64,
            "purpose": purpose,
            "targetCurrentnessLimitation": "EVIDENCE_ONLY_NOT_ACTIVE_STATE",
            "archiveVerification": "PASS",
            "sourceHashMatchesArchive": True,
            "archiveReadable": True,
        }
        for classification, original_path, archived_path, purpose in (
            (
                "IMMUTABLE_EVIDENCE",
                r"C:\Nexus USER\FAM-007-20260723-171541.zip",
                archive_root
                + r"\Immutable Evidence\FAM-007-20260723-171541"
                + r"\FAM-007-20260723-171541.zip",
                "Preserve the immutable focused-closure evidence packet.",
            ),
            (
                "HISTORICAL_RECEIPT",
                r"C:\Nexus USER\FAM-007-Decomposition-20260724-122330.zip",
                archive_root
                + r"\Historical Review Packets\FAM-007-Decomposition-20260724-122330"
                + r"\FAM-007-Decomposition-20260724-122330.zip",
                "Preserve the superseded decomposition decision packet.",
            ),
            (
                "TRANSFER_RECEIPT",
                r"C:\Nexus USER\FAM-007-20260723-171541-upload-parts"
                + r"\FAM-007-20260723-171541-UPLOAD-MANIFEST.zip",
                archive_root
                + r"\Transfer Receipts\FAM-007-20260723-171541"
                + r"\FAM-007-20260723-171541-UPLOAD-MANIFEST.zip",
                "Preserve the minimum transfer and reconstruction audit receipt.",
            ),
        )
    ]
    files["Review Aids/IMMUTABLE_EVIDENCE_ARCHIVE_RECEIPT.json"] = json.dumps(
        {
            "schema": "ndai-fam007-evidence-archive-receipt-v1",
            "archiveRoot": archive_root,
            "artifacts": receipt_artifacts,
            "transferPartsDisposition": {
                "verifiedOriginalArchived": True,
                "minimumReceiptSetArchived": True,
                "removedPartCount": 11,
            },
        },
        indent=2,
    )
    files["Review Aids/IMMUTABLE_EVIDENCE_ARCHIVE_RECEIPT.md"] = "\n".join(
        [
            "# Immutable Evidence Archive Receipt",
            f"Archive Root: `{archive_root}`",
            "Receipt JSON: `Review Aids/IMMUTABLE_EVIDENCE_ARCHIVE_RECEIPT.json`",
            "Archive Verification: `PASS`",
            "Target Currentness Limitation: `EVIDENCE_ONLY_NOT_ACTIVE_STATE`",
        ]
    )
    files["Review Aids/ARCHIVE_EVIDENCE_INDEX.md"] = "\n".join(
        [
            "# Archive Evidence Index",
            f"Archive Root: `{archive_root}`",
            "Target Currentness Limitation: `EVIDENCE_ONLY_NOT_ACTIVE_STATE`",
            "The archive is evidence only and is not active external state.",
        ]
    )
    files["Review Aids/PRIOR_DECOMPOSITION_PACKET_SUPERSESSION_RECEIPT.md"] = "\n".join(
        [
            "# Prior Decomposition Packet Supersession Receipt",
            r"Canonical Active Packet Folder: `C:\Nexus USER\FAM-007`",
            "Prior Active Label: `FAM-007-Decomposition`",
            "Supersession State: `ARCHIVED_SUPERSEDED_NOT_ACTIVE`",
        ]
    )
    files["Review Aids/ROOT_CLEANUP_REPORT.md"] = "\n".join(
        [
            "# Root Cleanup Report",
            "Canonical Active Folder Count: `1`",
            "Canonical Active ZIP Count: `1`",
            "Noncanonical Same-Family Root Artifact Count: `0`",
            "Unrelated Family Mutation Count: `0`",
            "Cleanup Finding: `PASS`",
        ]
    )
    external_receipt_name = (
        "Source Truth Context/Proof Artifacts/Operational Receipts/"
        "EXTERNAL_STATE_RECEIPT.md"
    )
    files[external_receipt_name] += "\n" + "\n".join(
        [
            r"Canonical Active USER Folder: `C:\Nexus USER\FAM-007`",
            r"Canonical Active USER ZIP: `C:\Nexus USER\FAM-007-20260724-120000.zip`",
            "Prior FAM-007-Decomposition Packet State: `ARCHIVED_SUPERSEDED_NOT_ACTIVE`",
            "Immutable Evidence Currentness: `EVIDENCE_ONLY_NOT_ACTIVE_STATE`",
        ]
    )
    return files


def _assert_fam007_decomposition_semantic_fixtures() -> None:
    def assert_pass(name: str, packet_files: dict[str, str]) -> None:
        failures = bundle._fam007_decomposition_packet_failures(packet_files)
        if failures:
            raise AssertionError(
                f"{name} failed unexpectedly:\n" + "\n".join(failures)
            )

    def assert_failure(name: str, needle: str, mutate) -> None:
        packet_files = dict(_valid_fam007_decomposition_packet_files())
        mutate(packet_files)
        found = bundle._fam007_decomposition_packet_failures(packet_files)
        if not any(needle in failure for failure in found):
            raise AssertionError(
                f"{name} did not fail on {needle!r}; failures were:\n"
                + "\n".join(found)
            )

    assert_pass(
        "current-route-a-unselected",
        _valid_fam007_decomposition_packet_files(),
    )

    accepted_no_candidate = _valid_fam007_decomposition_packet_files()
    _apply_decomposition_state(
        accepted_no_candidate,
        "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
    )
    assert_pass(
        "decision1-accepted-no-candidate-decision2-separate",
        accepted_no_candidate,
    )

    route_b = _valid_fam007_decomposition_packet_files()
    _apply_route(route_b, "ROUTE_B_SHARED_SHELL_LOCAL_LIFECYCLE")
    assert_pass("source-truth-complete-route-b", route_b)

    route_c = _valid_fam007_decomposition_packet_files()
    _apply_route(route_c, "ROUTE_C_INDIVISIBLE")
    assert_pass("source-truth-complete-route-c", route_c)

    stage1_selected = _valid_fam007_decomposition_packet_files()
    _apply_decomposition_state(
        stage1_selected,
        "STAGE1_CANDIDATE_SELECTED",
        candidate_code="DETACHED_CHILD_VISUAL_SHELL",
        candidate_name="Detached Child Visual Shell",
    )
    assert_pass("user-approved-stage1-candidate-selection", stage1_selected)

    ai_readiness_selected = _valid_fam007_decomposition_packet_files()
    _apply_decomposition_state(
        ai_readiness_selected,
        "STAGE1_CANDIDATE_SELECTED",
        candidate_code="AI_READINESS_DIAGNOSTICS",
        candidate_name="AI Readiness & Diagnostics",
    )
    assert_pass("ai-readiness-approved-stage1-selection", ai_readiness_selected)

    for issue_route in (
        "USER_APPROVED_SPLIT",
        "USER_APPROVED_REPLACEMENT",
        "USER_APPROVED_LIVE_ISSUE_CLARIFICATION",
    ):
        issue307_resolved = _valid_fam007_decomposition_packet_files()
        _resolve_issue307(issue307_resolved, issue_route)
        assert_pass(
            f"issue-307-approved-atomic-resolution-{issue_route.casefold()}",
            issue307_resolved,
        )

    stage1_complete = _valid_fam007_decomposition_packet_files()
    _apply_decomposition_state(
        stage1_complete,
        "STAGE1_ANALYSIS_COMPLETE",
        candidate_code="DETACHED_CHILD_VISUAL_SHELL",
        candidate_name="Detached Child Visual Shell",
    )
    assert_pass("stage1-analysis-complete-stage2-separate", stage1_complete)

    stage2_approved = _valid_fam007_decomposition_packet_files()
    _apply_decomposition_state(
        stage2_approved,
        "STAGE2_CREATION_APPROVED",
        candidate_code="DETACHED_CHILD_VISUAL_SHELL",
        candidate_name="Detached Child Visual Shell",
    )
    assert_pass("stage2-creation-approved-bp-entry-separate", stage2_approved)

    successor_created = _valid_fam007_decomposition_packet_files()
    _apply_decomposition_state(
        successor_created,
        "SUCCESSOR_CREATED_IDENTITY_VERIFIED",
        candidate_code="DETACHED_CHILD_VISUAL_SHELL",
        candidate_name="Detached Child Visual Shell",
    )
    assert_pass("successor-created-identity-verified", successor_created)

    bp_entry_approved = _valid_fam007_decomposition_packet_files()
    _apply_decomposition_state(
        bp_entry_approved,
        "BRANCH_PLANNING_ENTRY_APPROVED",
        candidate_code="DETACHED_CHILD_VISUAL_SHELL",
        candidate_name="Detached Child Visual Shell",
    )
    assert_pass("branch-planning-entry-approved-bp1-next", bp_entry_approved)

    assert_failure(
        "combined-shell-lifecycle-without-atomicity",
        "combined without the required indivisible-atomicity proof",
        lambda files: files.__setitem__(
            "Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md",
            "# Separability\nDeclared Route: `ROUTE_A_SEPARATE`\n"
            "Combined shell/lifecycle carrier.",
        ),
    )
    assert_failure(
        "same-file-is-not-atomicity",
        "same-file or same-class placement",
        lambda files: files.__setitem__(
            "Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md",
            files["Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md"]
            + "\nThe same file proves this must be one carrier.",
        ),
    )

    def incomplete_route_c(files: dict[str, str]) -> None:
        _apply_route(files, "ROUTE_C_INDIVISIBLE")
        files["Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md"] = files[
            "Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md"
        ].replace("Unsafe Separation Evidence: `COMPLETE`\n", "")

    assert_failure(
        "route-c-missing-unsafe-separation-proof",
        "Unsafe Separation Evidence=COMPLETE",
        incomplete_route_c,
    )

    def incomplete_route_b(files: dict[str, str]) -> None:
        _apply_route(files, "ROUTE_B_SHARED_SHELL_LOCAL_LIFECYCLE")
        files["Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md"] = files[
            "Review Aids/SHELL_LIFECYCLE_SEPARABILITY_MATRIX.md"
        ].replace("Source-Truth Route Permission: `CONFIRMED`\n", "")

    assert_failure(
        "route-b-missing-source-truth-permission",
        "Source-Truth Route Permission=CONFIRMED",
        incomplete_route_b,
    )

    assert_failure(
        "accepted-plan-before-creation",
        "circularly gated on an accepted Branch Plan",
        lambda files: files.__setitem__(
            "Review Aids/LEGAL_SUCCESSOR_ENTRY_SEQUENCE.md",
            files["Review Aids/LEGAL_SUCCESSOR_ENTRY_SEQUENCE.md"]
            + "\nBranch/worktree creation must wait until an accepted Branch Plan.",
        ),
    )
    assert_failure(
        "collapsed-br1-br2-entry",
        "collapses or omits distinct",
        lambda files: files.__setitem__(
            "Review Aids/LEGAL_SUCCESSOR_ENTRY_SEQUENCE.md",
            files["Review Aids/LEGAL_SUCCESSOR_ENTRY_SEQUENCE.md"].replace(
                "Branch Readiness Stage 2", "Second readiness step"
            ),
        ),
    )

    assert_failure(
        "missing-decomposition-state",
        "declared decomposition state is missing",
        lambda files: files.__setitem__(
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md",
            files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"].replace(
                "Declared Decomposition State: `DECOMPOSITION_UNSELECTED`\n", ""
            ),
        ),
    )
    assert_failure(
        "unknown-decomposition-state",
        "unknown declared decomposition state",
        lambda files: files.__setitem__(
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md",
            files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"].replace(
                "DECOMPOSITION_UNSELECTED", "UNKNOWN_TRANSITION"
            ),
        ),
    )

    def pending_state_carries_decision1_receipt(files: dict[str, str]) -> None:
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Decomposition Acceptance Receipt: `NONE`",
            "Decomposition Acceptance Receipt: `USER-DECISION-1-FABRICATED`",
        )

    assert_failure(
        "pending-state-carries-decision1-receipt",
        "DECOMPOSITION_UNSELECTED forbids decomposition receipt fields",
        pending_state_carries_decision1_receipt,
    )

    def pending_surface_falsely_accepts_decision1(files: dict[str, str]) -> None:
        files["USER Review/FAM007_BRANCH_SUPERSESSION_DECOMPOSITION_REVIEW.md"] = (
            files[
                "USER Review/FAM007_BRANCH_SUPERSESSION_DECOMPOSITION_REVIEW.md"
            ].replace(
                "Decision 1 State: `PENDING_USER_DECISION`",
                "Decision 1 State: `ACCEPTED`",
            )
        )

    assert_failure(
        "pending-surface-falsely-implies-decision1-approval",
        "primary USER review falsely represents Decision 1 State",
        pending_surface_falsely_accepts_decision1,
    )

    def accepted_state_missing_decision1_receipt(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            f"Decomposition Acceptance Receipt: `{DECOMPOSITION_ACCEPTANCE_RECEIPT}`",
            "Decomposition Acceptance Receipt: `NONE`",
        )

    assert_failure(
        "accepted-no-candidate-missing-decision1-receipt",
        "requires decomposition receipt field receipt",
        accepted_state_missing_decision1_receipt,
    )

    def accepted_support_claims_unselected(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_GATE_RECOVERY_DEFECT_LEDGER.md"] = files[
            "Review Aids/CURRENT_GATE_RECOVERY_DEFECT_LEDGER.md"
        ].replace(
            "Current State Preserved: `DECOMPOSITION_ACCEPTED_NO_CANDIDATE`",
            "Current State Preserved: `DECOMPOSITION_UNSELECTED`",
        )

    assert_failure(
        "accepted-support-falsely-claims-unselected",
        "recovery ledger disagrees on current state",
        accepted_support_claims_unselected,
    )

    def accepted_support_denies_user_approval(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_GATE_RECOVERY_DEFECT_LEDGER.md"] = files[
            "Review Aids/CURRENT_GATE_RECOVERY_DEFECT_LEDGER.md"
        ].replace("USER Approval Recorded: `YES`", "USER Approval Recorded: `NO`")

    assert_failure(
        "accepted-support-denies-user-approval",
        "recovery ledger falsely represents USER approval",
        accepted_support_denies_user_approval,
    )

    def accepted_transition_preamble_claims_unselected(
        files: dict[str, str],
    ) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/DECOMPOSITION_TRANSITION_STATE_MODEL.md"] = files[
            "Review Aids/DECOMPOSITION_TRANSITION_STATE_MODEL.md"
        ].replace(
            "Current Packet State: `DECOMPOSITION_ACCEPTED_NO_CANDIDATE`",
            "Current Packet State: `DECOMPOSITION_UNSELECTED`",
        )

    assert_failure(
        "accepted-transition-preamble-claims-unselected",
        "transition-state model disagrees on current packet state",
        accepted_transition_preamble_claims_unselected,
    )

    def accepted_matrix_claims_no_required_receipts(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/RECEIPT_REQUIREMENT_MATRIX.md"] = files[
            "Review Aids/RECEIPT_REQUIREMENT_MATRIX.md"
        ].replace(
            "Current Required Receipts: `DECOMPOSITION`",
            "Current Required Receipts: `NONE`",
        )

    assert_failure(
        "accepted-matrix-claims-no-required-receipts",
        "receipt-requirement matrix disagrees on current required receipts",
        accepted_matrix_claims_no_required_receipts,
    )

    def accepted_table_leaves_decision1_at_review(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/APPROVAL_STAGE_TABLE.md"] = files[
            "Review Aids/APPROVAL_STAGE_TABLE.md"
        ].replace(
            "| Decomposition acceptance | fixture carrier | fixture artifact | no | "
            "separate gate | COMPLETED / RECORDED |",
            "| Decomposition acceptance | fixture carrier | fixture artifact | no | "
            "separate gate | AUTHORIZED FOR USER REVIEW |",
        )

    assert_failure(
        "accepted-table-leaves-decision1-at-review",
        "approval-stage table disagrees on Decomposition acceptance",
        accepted_table_leaves_decision1_at_review,
    )

    def accepted_table_says_posture_not_reached(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/APPROVAL_STAGE_TABLE.md"] = files[
            "Review Aids/APPROVAL_STAGE_TABLE.md"
        ].replace(
            "| Accepted posture / no candidate selected | fixture carrier | fixture "
            "artifact | no | separate gate | CURRENT |",
            "| Accepted posture / no candidate selected | fixture carrier | fixture "
            "artifact | no | separate gate | NOT REACHED |",
        )

    assert_failure(
        "accepted-table-says-posture-not-reached",
        "approval-stage table disagrees on Accepted posture / no candidate selected",
        accepted_table_says_posture_not_reached,
    )

    def accepted_table_blocks_decision2_review(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/APPROVAL_STAGE_TABLE.md"] = files[
            "Review Aids/APPROVAL_STAGE_TABLE.md"
        ].replace(
            "| Stage 1 analysis selection | fixture carrier | fixture artifact | no | "
            "separate gate | CURRENT USER REVIEW GATE |",
            "| Stage 1 analysis selection | fixture carrier | fixture artifact | no | "
            "separate gate | NOT AUTHORIZED |",
        )

    assert_failure(
        "accepted-table-blocks-decision2-review",
        "approval-stage table disagrees on Stage 1 analysis selection",
        accepted_table_blocks_decision2_review,
    )

    def accepted_state_carries_stage1_receipt(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Stage 1 Selection Approval Receipt: `NONE`",
            "Stage 1 Selection Approval Receipt: `USER-STAGE1-FABRICATED`",
        )

    assert_failure(
        "stage1-receipt-before-candidate-selection",
        "DECOMPOSITION_ACCEPTED_NO_CANDIDATE forbids stage1 receipt fields",
        accepted_state_carries_stage1_receipt,
    )

    def accepted_state_candidate_leakage(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace("Named Candidate Code: `NONE`", "Named Candidate Code: `LEAKED`")
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace("Named Candidate: `NONE`", "Named Candidate: `Leaked Candidate`")

    assert_failure(
        "candidate-leakage-before-decision2",
        "no-candidate state must not name a candidate",
        accepted_state_candidate_leakage,
    )

    def accepted_state_selected_next_leakage(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace("CONSUMED_NO_SUCCESSOR", "SELECTED_STAGE1_ANALYSIS_ONLY")

    assert_failure(
        "selected-next-leakage-before-decision2",
        "requires selected_next=CONSUMED_NO_SUCCESSOR",
        accepted_state_selected_next_leakage,
    )

    def arbitrary_decision1_approval_text(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            DECOMPOSITION_ACCEPTANCE_TEXT,
            "approved",
        )

    assert_failure(
        "arbitrary-decision1-approval-text",
        "decomposition exact USER decision does not exactly match",
        arbitrary_decision1_approval_text,
    )

    def arbitrary_decision1_receipt_identifier(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            f"Decomposition Acceptance Receipt: `{DECOMPOSITION_ACCEPTANCE_RECEIPT}`",
            "Decomposition Acceptance Receipt: `approved`",
        )

    assert_failure(
        "arbitrary-decision1-receipt-identifier",
        "decomposition receipt identifier is not structured proof",
        arbitrary_decision1_receipt_identifier,
    )

    def paraphrased_decision1_approval_text(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            DECOMPOSITION_ACCEPTANCE_TEXT,
            "I accept the decomposition carrier and will choose a successor later.",
        )

    assert_failure(
        "paraphrased-or-fabricated-decision1",
        "decomposition exact USER decision does not exactly match",
        paraphrased_decision1_approval_text,
    )

    assert_failure(
        "missing-receipt-requirement-matrix",
        "required FAM-007 decomposition decision artifact is missing",
        lambda files: files.__setitem__(
            "Review Aids/RECEIPT_REQUIREMENT_MATRIX.md", ""
        ),
    )

    def stage1_missing_approval(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE1_CANDIDATE_SELECTED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Stage 1 Selection Approval Receipt: `USER-STAGE1-SELECTION-FIXTURE`",
            "Stage 1 Selection Approval Receipt: `NONE`",
        )

    assert_failure(
        "stage1-selection-missing-approval",
        "requires stage1 receipt field receipt",
        stage1_missing_approval,
    )

    def stage1_wrong_scope(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE1_CANDIDATE_SELECTED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Branch Readiness Stage 1 analysis only",
            "Branch Readiness Stage 1 analysis and creation",
        )

    assert_failure(
        "stage1-selection-wrong-approval-scope",
        "stage1 exact USER decision does not exactly match",
        stage1_wrong_scope,
    )

    def stage1_stale_selected_next(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE1_CANDIDATE_SELECTED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/SELECTED_NEXT_STATE_RECEIPT.md"] = files[
            "Review Aids/SELECTED_NEXT_STATE_RECEIPT.md"
        ].replace("SELECTED_STAGE1_ANALYSIS_ONLY", "CONSUMED_NO_SUCCESSOR")

    assert_failure(
        "stage1-selection-stale-selected-next",
        "selected-next receipt disagrees",
        stage1_stale_selected_next,
    )

    def stage1_external_state_mismatch(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE1_CANDIDATE_SELECTED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files[
            "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md"
        ] = files[
            "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md"
        ].replace(
            "Declared Decomposition State: `STAGE1_CANDIDATE_SELECTED`",
            "Declared Decomposition State: `DECOMPOSITION_UNSELECTED`",
        )

    assert_failure(
        "stage1-selection-packet-external-mismatch",
        "packet/external-state mismatch",
        stage1_external_state_mismatch,
    )

    def stage1_branch_mutation(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE1_CANDIDATE_SELECTED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Branch / Worktree Mutation: `NONE`",
            "Branch / Worktree Mutation: `COMPLETED`",
        )

    assert_failure(
        "branch-mutation-during-stage1",
        "requires branch_mutation=NONE",
        stage1_branch_mutation,
    )

    def branch_exists_before_stage2(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE1_CANDIDATE_SELECTED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Successor Branch / Worktree Exists: `NO`",
            "Successor Branch / Worktree Exists: `YES`",
        )

    assert_failure(
        "branch-exists-before-stage2",
        "requires branch_exists=NO",
        branch_exists_before_stage2,
    )

    def stale_current_gate(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Current Gate Code: `DECOMPOSITION_DECISION_2_REVIEW`",
            "Current Gate Code: `DECOMPOSITION_DECISION_1_REVIEW`",
        )

    assert_failure(
        "stale-current-gate",
        "requires current_gate=DECOMPOSITION_DECISION_2_REVIEW",
        stale_current_gate,
    )

    def stale_next_gate(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "DECOMPOSITION_ACCEPTED_NO_CANDIDATE",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Next Legal Gate Code: `USER_DECISION_2_STAGE1_CANDIDATE_SELECTION`",
            "Next Legal Gate Code: `BRANCH_READINESS_STAGE_2_EXECUTION`",
        )

    assert_failure(
        "stale-next-gate",
        "requires next_gate=USER_DECISION_2_STAGE1_CANDIDATE_SELECTION",
        stale_next_gate,
    )

    def stage1_phase_collapse(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE1_ANALYSIS_COMPLETE",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Implementation Approval: `NOT_APPROVED`",
            "Implementation Approval: `APPROVED`",
        )

    assert_failure(
        "stage1-analysis-complete-phase-collapse",
        "must not imply implementation approval",
        stage1_phase_collapse,
    )

    def stage2_missing_approval(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE2_CREATION_APPROVED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Stage 2 Creation Approval Receipt: `USER-STAGE2-CREATION-FIXTURE`",
            "Stage 2 Creation Approval Receipt: `NONE`",
        )

    assert_failure(
        "stage2-creation-missing-approval",
        "requires stage2 receipt field receipt",
        stage2_missing_approval,
    )

    def stage2_implies_bp_entry(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "STAGE2_CREATION_APPROVED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Branch Planning Entry Approval: `NOT_APPROVED`",
            "Branch Planning Entry Approval: `APPROVED`",
        )

    assert_failure(
        "stage2-creation-implies-branch-planning",
        "requires bp_entry=NOT_APPROVED",
        stage2_implies_bp_entry,
    )

    def created_identity_missing(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "SUCCESSOR_CREATED_IDENTITY_VERIFIED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Successor Identity Verification: `VERIFIED`",
            "Successor Identity Verification: `MISSING`",
        )

    assert_failure(
        "created-successor-missing-identity",
        "requires identity=VERIFIED",
        created_identity_missing,
    )

    def created_successor_missing_identity_receipt(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "SUCCESSOR_CREATED_IDENTITY_VERIFIED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Successor Identity Receipt: `SUCCESSOR-IDENTITY-FIXTURE`",
            "Successor Identity Receipt: `NONE`",
        )

    assert_failure(
        "created-successor-missing-identity-receipt",
        "requires identity receipt field receipt",
        created_successor_missing_identity_receipt,
    )

    def branch_planning_before_identity(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "SUCCESSOR_CREATED_IDENTITY_VERIFIED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Successor Identity Verification: `VERIFIED`",
            "Successor Identity Verification: `MISSING`",
        ).replace(
            "Branch Planning Entry Approval: `NOT_APPROVED`",
            "Branch Planning Entry Approval: `APPROVED`",
        )

    assert_failure(
        "branch-planning-before-identity-verification",
        "requires identity=VERIFIED",
        branch_planning_before_identity,
    )

    def bp_entry_missing_approval(files: dict[str, str]) -> None:
        _apply_decomposition_state(
            files,
            "BRANCH_PLANNING_ENTRY_APPROVED",
            candidate_code="DETACHED_CHILD_VISUAL_SHELL",
            candidate_name="Detached Child Visual Shell",
        )
        files["Review Aids/CURRENT_DECOMPOSITION_STATE.md"] = files[
            "Review Aids/CURRENT_DECOMPOSITION_STATE.md"
        ].replace(
            "Branch Planning Entry Approval Receipt: `USER-BP-ENTRY-FIXTURE`",
            "Branch Planning Entry Approval Receipt: `NONE`",
        )

    assert_failure(
        "branch-planning-entry-missing-approval",
        "requires bp_entry receipt field receipt",
        bp_entry_missing_approval,
    )

    assert_failure(
        "multiple-final-closure-owners",
        "exactly one coded final closure owner",
        lambda files: files.__setitem__(
            "Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md",
            files["Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md"].replace(
                "| #292 | `F7-SHELL` | `F7-SHELL` |",
                "| #292 | `F7-SHELL` | `F7-SHELL + F7-READINESS` |",
            ),
        ),
    )
    assert_failure(
        "contributors-are-not-closure-owners",
        "confuses dependency contributors",
        lambda files: files.__setitem__(
            "Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md",
            files["Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md"].replace(
                "| #292 | `F7-SHELL` | `F7-SHELL` | Window-specific proof | Later acceptance | `ATOMIC` | `NONE` |",
                "| #292 | `F7-SHELL` | `F7-SHELL` | Window-specific proof | Later acceptance | `ATOMIC` | `F7-SHELL` |",
            ),
        ),
    )
    assert_failure(
        "dependency-is-not-ownership",
        "uses a dependency statement",
        lambda files: files.__setitem__(
            "Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md",
            files["Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md"].replace(
                "| #293 | `F7-SHELL` | `F7-SHELL` |",
                "| #293 | `F7-SHELL` | `DEPENDS-THEN-CLOSE` |",
            ),
        ),
    )

    def resolved_issue_missing_approval(files: dict[str, str]) -> None:
        _resolve_issue307(files)
        files["Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md"] = files[
            "Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md"
        ].replace(
            "Issue #307 USER Approval Receipt: `USER-ISSUE-307-FIXTURE`",
            "Issue #307 USER Approval Receipt: `NONE`",
        )

    assert_failure(
        "issue-307-resolution-missing-approval",
        "lacks an exact USER approval receipt",
        resolved_issue_missing_approval,
    )

    def resolved_issue_owner_ambiguity(files: dict[str, str]) -> None:
        _resolve_issue307(files)
        files["Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md"] = files[
            "Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md"
        ].replace(
            "| #307 | `F7-LIFECYCLE` | `F7-LIFECYCLE` |",
            "| #307 | `F7-LIFECYCLE` | `F7-LIFECYCLE + F7-SHELL` |",
        )

    assert_failure(
        "issue-307-resolution-owner-ambiguity",
        "exactly one coded final closure owner",
        resolved_issue_owner_ambiguity,
    )

    def unresolved_issue_allows_implementation(files: dict[str, str]) -> None:
        files["Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md"] = files[
            "Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md"
        ].replace(
            "Implementation Or Closeout Allowed: `NO`",
            "Implementation Or Closeout Allowed: `YES`",
        )

    assert_failure(
        "unresolved-issue307-implementation-or-closeout",
        "must block implementation and closeout",
        unresolved_issue_allows_implementation,
    )

    def issue307_paraphrased_approval(files: dict[str, str]) -> None:
        _resolve_issue307(files)
        files["Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md"] = files[
            "Review Aids/ISSUE_307_RESOLUTION_RECEIPT.md"
        ].replace(
            "I approve the Issue #307 live issue clarification with one final closure owner F7-LIFECYCLE.",
            "I approve Issue #307 with F7-LIFECYCLE.",
        )

    assert_failure(
        "issue307-paraphrased-or-fabricated-approval",
        "exact USER decision does not exactly match",
        issue307_paraphrased_approval,
    )

    assert_failure(
        "hidden-issue-split",
        "Issue #307 must expose",
        lambda files: files.__setitem__(
            "Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md",
            files["Review Aids/CORRECTED_ISSUE_OWNERSHIP_MATRIX.md"].replace(
                "SPLIT_REQUIRED_BEFORE_IMPLEMENTATION_OR_CLOSEOUT", "ATOMIC"
            ),
        ),
    )
    assert_failure(
        "implied-selected-next",
        "implied as selected-next",
        lambda files: files.__setitem__(
            "START_HERE.md",
            files["START_HERE.md"] + "\nSuccessor Selected: `YES`",
        ),
    )
    assert_failure(
        "recommendation-selection-drift",
        "recommendation/selection posture",
        lambda files: files.__setitem__(
            "Review Aids/AI_READINESS_RECOMMENDATION_SELECTION_RECEIPT.md",
            files[
                "Review Aids/AI_READINESS_RECOMMENDATION_SELECTION_RECEIPT.md"
            ].replace(
                "RECOMMENDATION_ONLY_NOT_SELECTED",
                "SELECTED_FOR_STAGE1_ANALYSIS_ONLY",
            ),
        ),
    )
    assert_failure(
        "missing-identity-fact",
        "identity receipt is incomplete",
        lambda files: files.__setitem__(
            "Source Truth Context/Proof Artifacts/Operational Receipts/IDENTITY_RECEIPT.md",
            files[
                "Source Truth Context/Proof Artifacts/Operational Receipts/IDENTITY_RECEIPT.md"
            ].replace("Merge Base: exact\n", ""),
        ),
    )
    assert_failure(
        "missing-external-state-version",
        "external-state receipt is missing State Version:",
        lambda files: files.__setitem__(
            "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md",
            files[
                "Source Truth Context/Proof Artifacts/Operational Receipts/EXTERNAL_STATE_RECEIPT.md"
            ].replace("State Version: exact\n", ""),
        ),
    )
    assert_failure(
        "absent-codex-digest-proof",
        "depends on an absent Codex digest",
        lambda files: files.__setitem__(
            "START_HERE.md",
            files["START_HERE.md"]
            + "\nValidation is recorded in the Codex digest.",
        ),
    )
    assert_failure(
        "self-embedded-final-sha",
        "falsely embedded",
        lambda files: files.__setitem__(
            "START_HERE.md",
            files["START_HERE.md"] + "\nFinal packet SHA256: " + ("A" * 64),
        ),
    )
    assert_failure(
        "loose-sidecar-receipt-boundary",
        "no-loose-sidecar boundary",
        lambda files: files.__setitem__(
            "START_HERE.md",
            files["START_HERE.md"].replace("no loose sidecar", "separate sidecar"),
        ),
    )


def _assert_fam007_active_normalization_receipt_fixtures() -> None:
    def failures_for(files: dict[str, str]) -> list[str]:
        return bundle._fam007_active_normalization_receipt_failures(
            files,
            validation_mode=PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
        )

    valid = _valid_fam007_decomposition_packet_files()
    valid_failures = failures_for(valid)
    if valid_failures:
        raise AssertionError(
            "valid canonical archive/cleanup receipt set failed unexpectedly:\n"
            + "\n".join(valid_failures)
        )
    metadata_failures = bundle._generic_user_facing_technical_metadata_failures(valid)
    if metadata_failures:
        raise AssertionError(
            "required FAM-007 archive receipts were rejected as loose USER-facing "
            "technical metadata:\n" + "\n".join(metadata_failures)
        )
    guard_packet = dict(valid)
    guard_packet["Review Aids/UNROUTED_HASH_SIDECAR.md"] = (
        "Final ZIP SHA256: `" + ("A" * 64) + "`"
    )
    guard_failures = bundle._generic_user_facing_technical_metadata_failures(
        guard_packet
    )
    if not any(
        "UNROUTED_HASH_SIDECAR.md" in failure
        and "technical metadata" in failure
        for failure in guard_failures
    ):
        raise AssertionError(
            "archive-receipt exemption weakened the generic loose-hash guard"
        )

    missing_receipt = dict(valid)
    missing_receipt.pop("Review Aids/IMMUTABLE_EVIDENCE_ARCHIVE_RECEIPT.json")
    if not any(
        "normalization artifact is missing" in failure
        for failure in failures_for(missing_receipt)
    ):
        raise AssertionError("missing archive receipt did not fail closed")

    missing_historical = json.loads(json.dumps(valid))
    receipt_name = "Review Aids/IMMUTABLE_EVIDENCE_ARCHIVE_RECEIPT.json"
    receipt = json.loads(missing_historical[receipt_name])
    receipt["artifacts"] = [
        item
        for item in receipt["artifacts"]
        if item["classification"] != "HISTORICAL_RECEIPT"
    ]
    missing_historical[receipt_name] = json.dumps(receipt)
    if not any(
        "required archive classes are missing" in failure
        for failure in failures_for(missing_historical)
    ):
        raise AssertionError("deleted historical receipt lacked archive-verification failure")

    missing_sha = json.loads(json.dumps(valid))
    receipt = json.loads(missing_sha[receipt_name])
    receipt["artifacts"][0].pop("sha256")
    missing_sha[receipt_name] = json.dumps(receipt)
    if not any("missing sha256" in failure for failure in failures_for(missing_sha)):
        raise AssertionError("archive receipt without SHA256 did not fail closed")

    missing_purpose = json.loads(json.dumps(valid))
    receipt = json.loads(missing_purpose[receipt_name])
    receipt["artifacts"][0]["purpose"] = ""
    missing_purpose[receipt_name] = json.dumps(receipt)
    if not any(
        "missing purpose" in failure for failure in failures_for(missing_purpose)
    ):
        raise AssertionError("archive receipt without purpose did not fail closed")

    promoted_archive = json.loads(json.dumps(valid))
    receipt = json.loads(promoted_archive[receipt_name])
    receipt["artifacts"][0]["targetCurrentnessLimitation"] = "CURRENT_ACTIVE_PROOF"
    promoted_archive[receipt_name] = json.dumps(receipt)
    if not any(
        "EVIDENCE_ONLY_NOT_ACTIVE_STATE" in failure
        for failure in failures_for(promoted_archive)
    ):
        raise AssertionError("archived evidence was allowed to become current proof")

    unverified_archive = json.loads(json.dumps(valid))
    receipt = json.loads(unverified_archive[receipt_name])
    receipt["artifacts"][0]["archiveVerification"] = "PENDING"
    receipt["artifacts"][0]["sourceHashMatchesArchive"] = False
    unverified_archive[receipt_name] = json.dumps(receipt)
    unverified_failures = failures_for(unverified_archive)
    if not any("archiveVerification must be PASS" in failure for failure in unverified_failures):
        raise AssertionError("cleanup could delete the only evidence copy without verified archive")

    unverified_transfer = json.loads(json.dumps(valid))
    receipt = json.loads(unverified_transfer[receipt_name])
    receipt["transferPartsDisposition"]["verifiedOriginalArchived"] = False
    unverified_transfer[receipt_name] = json.dumps(receipt)
    if not any(
        "transfer parts cannot be removed" in failure
        for failure in failures_for(unverified_transfer)
    ):
        raise AssertionError("transfer-part removal lacked verified original archive proof")

    archived_as_active = json.loads(json.dumps(valid))
    external_name = (
        "Source Truth Context/Proof Artifacts/Operational Receipts/"
        "EXTERNAL_STATE_RECEIPT.md"
    )
    archived_as_active[external_name] = re.sub(
        r"Canonical Active USER ZIP:\s*`[^`]+`",
        lambda _match: (
            "Canonical Active USER ZIP: "
            r"`D:\Nexus Artifacts\FAM-007\USER Review Archive\historical.zip`"
        ),
        archived_as_active[external_name],
    )
    if not any(
        "points to an archived/superseded packet" in failure
        for failure in failures_for(archived_as_active)
    ):
        raise AssertionError("active external state accepted an archived packet pointer")

    accepted_historical = bundle._fam007_active_normalization_receipt_failures(
        {"START_HERE.md": "# FAM-007 decomposition"},
        validation_mode=PACKET_VALIDATION_MODE_ACCEPTED_HISTORICAL,
    )
    if accepted_historical:
        raise AssertionError(
            "accepted-historical packet was forced through current active normalization:\n"
            + "\n".join(accepted_historical)
        )


def main() -> int:
    _assert_origin_main_fallback()
    _assert_fam007_canonical_active_surface_fixtures()
    _assert_fam007_decomposition_semantic_fixtures()
    _assert_fam007_active_normalization_receipt_fixtures()
    _assert_failure(
        "unknown-origin-main-identity",
        "requires explicit identity expectations",
        lambda _packet: None,
        expected_origin_main="UNKNOWN",
    )
    _assert_stage1_primary_for_stage2_decision()
    _assert_misrouted_stage1_primary_runs_all_guards()
    _assert_stage1_zip_start_here_contract()
    _assert_stale_primary_aid_is_not_skipped()
    _assert_non_fam007_stage2_wording_requires_ready_stage1()
    _assert_stage1_repair_status_is_machine_readable()
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
        "active-review-mapped-binary-copy-missing",
        "mapped copied source path is missing from packet",
        lambda packet: (packet / "START_HERE.md").write_text(
            (packet / "START_HERE.md").read_text(encoding="utf-8")
            + "\n| `dev/orin_user_review_bundle.py` | `Source Truth Context/dev__orin_user_review_bundle.py` |\n",
            encoding="utf-8",
        ),
    )
    _assert_failure(
        "active-review-unmapped-source-context",
        "copied Source Truth Context file is not mapped in START_HERE.md",
        lambda packet: (packet / "Source Truth Context" / "Docs__phase_governance.md").write_text(
            "# stale unmapped source context\n",
            encoding="utf-8",
        ),
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
        copied_source = "Source Truth Context/helper_source.py"
        source_bytes = bundle._git_file_bytes(
            _current_head(), "dev/orin_user_review_bundle.py"
        )
        if source_bytes is None:
            raise AssertionError("fixture source file is missing at the expected HEAD")
        (packet / copied_source).write_bytes(source_bytes)
        (packet / "START_HERE.md").write_text(
            (packet / "START_HERE.md").read_text(encoding="utf-8")
            + "\n| `dev/orin_user_review_bundle.py` | "
            + f"`{copied_source}` |\n",
            encoding="utf-8",
        )

    _assert_success(
        "source-context-code-is-not-user-facing-template-shell",
        _legitimate_source_context_shell_tokens,
        validation_mode=PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
        external_state_files=None,
    )

    def _stale_binary_source_context(packet: Path) -> None:
        copied_source = "Source Truth Context/dev__orin_user_review_bundle.py"
        (packet / copied_source).write_bytes(b"# stale copied helper source\n")
        (packet / "START_HERE.md").write_text(
            (packet / "START_HERE.md").read_text(encoding="utf-8")
            + "\n| `dev/orin_user_review_bundle.py` | "
            f"`{copied_source}` |\n",
            encoding="utf-8",
        )

    _assert_failure(
        "stale-binary-source-context-copy",
        "copied file does not match expected HEAD content",
        _stale_binary_source_context,
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
