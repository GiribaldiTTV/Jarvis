# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-false-green-fixtures; status=shared
"""Regression fixtures for USER review packet false-green classes."""

from __future__ import annotations

import base64
import hashlib
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


def _assert_migrated_live_header_ignores_historical_receipt_metadata() -> None:
    live_head = bundle._git_text("rev-parse", "HEAD")
    if not live_head:
        raise AssertionError("fixture requires current Git HEAD")
    export_zip = Path(r"C:\Nexus USER\FAM-003-20990101-000000.zip")
    active_header = (
        "External State Schema: `external-state-v1`\n"
        f"Source Repo HEAD: `{live_head}`\n"
        "Historical Receipt Boundary: `Historical content follows.`\n"
    )
    packet_files = {
        "Source Truth Context/current_external_branch_state.md": (
            active_header
            + "Source Repo HEAD: `1111111111111111111111111111111111111111`\n"
            + "USER Review ZIP: `C:\\Nexus USER\\FAM-003-19990101-000000.zip`\n"
        ),
        "Source Truth Context/current_external_branch_plan.md": (
            active_header
            + "Source Repo HEAD: `2222222222222222222222222222222222222222`\n"
        ),
    }
    failures = bundle._final_zip_active_metadata_failures(
        packet_files,
        export_zip,
        validation_mode=bundle.PACKET_VALIDATION_MODE_ACTIVE_REVIEW,
    )
    if failures:
        raise AssertionError(
            "migrated live-header metadata was polluted by historical receipts:\n"
            + "\n".join(failures)
        )


def _assert_source_context_text_normalization() -> None:
    lf = b"line one\nline two\n"
    crlf = b"\xef\xbb\xbfline one\r\nline two\r\n"
    changed = b"line one\nline three\n"
    if (
        bundle._normalized_source_context_text_bytes(lf)
        != bundle._normalized_source_context_text_bytes(crlf)
    ):
        raise AssertionError("source-context UTF-8 BOM/line-ending normalization failed")
    if (
        bundle._normalized_source_context_text_bytes(lf)
        == bundle._normalized_source_context_text_bytes(changed)
    ):
        raise AssertionError("source-context normalization masked a content change")


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


def _assert_fam003_option_g_bp2_planning_guards() -> None:
    seams = "\n".join(f"`OPTG-WS{index:02d}`" for index in range(1, 8))
    recording_fixtures = "\n".join(
        f"`OPTG-RS-FG-{index:02d}`" for index in range(1, 11)
    )
    packet_fixtures = "\n".join(
        f"`OPTG-PKT-FG-{index:02d}`" for index in range(1, 16)
    )
    allowlist = "\n".join(
        (
            f"| `OPTG-ALLOW-{index:02d}` | `desktop/desktop_renderer.py` | "
            f"`ExactClass.method_{index}` | Exact bounded native lifecycle region |"
        )
        for index in range(1, 9)
    )
    plan_path = (
        "Source Truth Context/Active External Snapshot/"
        "decision2_option_g_bp2_gate_repair_20260724.md"
    )
    valid = {
        "START_HERE.md": (
            "# FAM-003 Option G BP2 Repair\n"
            "Branch: `feature/fam-003-settings-resize-proof`\n"
            "Primary USER Review File: `USER Review/USER_BRANCH_PLAN_REVIEW.md`\n"
            "Option G revised BP2 USER review pending.\n"
        ),
        "USER Review/USER_BRANCH_PLAN_REVIEW.md": (
            "# USER Branch Plan Review - FAM-003 Option G\n"
            "Primary Review Type: `BP2 USER Branch Plan Review`\n"
            "Accept revised Option G BP2 only and authorize revised BP3 "
            "orchestration-validation preparation.\n"
            "BP3 Status: `NOT_ENTERED`\n"
            "Workstream Implementation: `UNAPPROVED`\n"
            "Workstream implementation requires a later separate USER decision.\n"
        ),
        "Review Aids/USER_DECISIONS.md": (
            "Accept revised Option G BP2 only and authorize revised BP3 "
            "orchestration-validation preparation.\n"
        ),
        "Review Aids/DECISION_AND_GATE_DIGEST.md": (
            "Combined BP2/BP3 Acceptance Legal: `NO`\n"
            "BP2 must be accepted or waived before BP3 preparation.\n"
            "BP3 Status: `NOT_ENTERED`\n"
        ),
        plan_path: (
            "# Option G repaired BP2\n"
            "Combined BP2/BP3 Acceptance Legal: `NO`\n"
            "BP2 must be accepted or waived before BP3 preparation.\n"
            "BP3 Status: `NOT_ENTERED`\n"
            "Workstream Implementation: `UNAPPROVED`\n"
            "Workstream implementation requires a later separate USER decision.\n"
            "`MonitoringHudStudioWebWindow`\n"
            "`MonitoringHudStudioWebWindow.__init__` / `_resize_hover_timer` "
            "construction and start guard\n"
            "`MonitoringHudLogViewerStudioWindow`\n"
            "`MonitoringHudRecordingStudioWindow`\n"
            "`STUDIO_RESIZABLE = False`\n"
            "`Start / Pause / Stop`\n"
            "If attribution identifies a path, object, resource, or owner not "
            "explicitly enumerated in the accepted conditional repair matrix, "
            "Workstream must return `BLOCKED / USER decision required` before mutation.\n"
            "Current-carrier access does not establish ownership or self-admit repair scope.\n"
            "FAM-006/shared-owner stop\n"
            "Stage 1 Explicit Exclusions: Recording Studio product behavior; "
            "FAM-006 JavaScript; generic WebEngine lifetime; renderer policy; "
            "ORIN Core; AI.\n"
            "ORIN Core Decision 3 carryforward\n"
            "H1 remains `NOT_ENTERED`\n"
            "LV remains `NOT_ENTERED`\n"
            "UTS remains `NOT_REQUESTED`\n"
            f"{seams}\n{recording_fixtures}\n{packet_fixtures}\n{allowlist}\n"
        ),
    }
    valid_failures = bundle._fam003_option_g_bp2_planning_failures(valid)
    if valid_failures:
        raise AssertionError(
            "Valid FAM-003 Option G BP2 planning fixture failed:\n"
            + "\n".join(valid_failures)
        )

    cases = (
        (
            "OPTG-PKT-FG-01",
            "USER Review/USER_BRANCH_PLAN_REVIEW.md",
            "Accept revised Option G BP2 only and authorize revised BP3 orchestration-validation preparation.",
            "Accept revised Option G BP2 and approve revised BP3.",
            "forbidden current BP3 acceptance request",
        ),
        (
            "OPTG-PKT-FG-02",
            plan_path,
            "Combined BP2/BP3 Acceptance Legal: `NO`",
            "Combined gate basis is unspecified.",
            "active plan lacks required combined gate rejection",
        ),
        (
            "OPTG-PKT-FG-03",
            "USER Review/USER_BRANCH_PLAN_REVIEW.md",
            "Primary Review Type: `BP2 USER Branch Plan Review`",
            "Primary Review Type: `BP3 Workstream Entry`",
            "required primary review type",
        ),
        (
            "OPTG-PKT-FG-04",
            "USER Review/USER_BRANCH_PLAN_REVIEW.md",
            "BP3 Status: `NOT_ENTERED`",
            "BP3 requirements are complete.",
            "required BP3 not entered",
        ),
        (
            "OPTG-PKT-FG-05",
            plan_path,
            "# Option G repaired BP2",
            "# Option G repaired BP2\nRecording Studio must not enter the changed-file set.",
            "forbidden file-absence Recording proof",
        ),
        (
            "OPTG-PKT-FG-06",
            plan_path,
            "`MonitoringHudStudioWebWindow.__init__` / `_resize_hover_timer` construction and start guard",
            "Shared base changes may be made as needed.",
            "required shared timer construction region",
        ),
        (
            "OPTG-PKT-FG-07",
            plan_path,
            "`STUDIO_RESIZABLE = False`",
            "`STUDIO_RESIZABLE = True`",
            "required Recording Studio non-resizable invariant",
        ),
        (
            "OPTG-PKT-FG-08",
            plan_path,
            "`Start / Pause / Stop`",
            "Recording controls remain generally available.",
            "required Recording controls invariant",
        ),
        (
            "OPTG-PKT-FG-09",
            plan_path,
            "| `OPTG-ALLOW-08` | `desktop/desktop_renderer.py` | `ExactClass.method_8` | Exact bounded native lifecycle region |",
            "",
            "exactly eight OPTG-ALLOW rows",
        ),
        (
            "OPTG-PKT-FG-10",
            plan_path,
            "If attribution identifies a path, object, resource, or owner not explicitly enumerated in the accepted conditional repair matrix, Workstream must return `BLOCKED / USER decision required` before mutation.",
            "Newly attributed paths may be repaired after local classification.",
            "required unknown attribution stop",
        ),
        (
            "OPTG-PKT-FG-11",
            plan_path,
            "Current-carrier access does not establish ownership or self-admit repair scope.",
            "Current-carrier access establishes ownership.",
            "required current carrier not ownership",
        ),
        (
            "OPTG-PKT-FG-12",
            plan_path,
            "FAM-006/shared-owner stop",
            "Shared-owner work may continue.",
            "required FAM-006 stop",
        ),
        (
            "OPTG-PKT-FG-13",
            plan_path,
            "Stage 1 Explicit Exclusions: Recording Studio product behavior; FAM-006 JavaScript; generic WebEngine lifetime; renderer policy; ORIN Core; AI.",
            "Stage 1 exclusions are unchanged.",
            "required Stage 1 exclusions",
        ),
        (
            "OPTG-PKT-FG-14",
            plan_path,
            "# Option G repaired BP2",
            "# Option G repaired BP2\nBP2 acceptance authorizes Workstream implementation.",
            "forbidden planning-implies-implementation",
        ),
        (
            "OPTG-PKT-FG-15",
            plan_path,
            "# Option G repaired BP2",
            "# Option G repaired BP2\nH1 executes under Workstream authority.",
            "forbidden downstream phase execution",
        ),
    )
    for case_id, file_name, old, new, expected in cases:
        mutated = dict(valid)
        mutated[file_name] = mutated[file_name].replace(old, new, 1)
        failures = bundle._fam003_option_g_bp2_planning_failures(mutated)
        if not any(expected.casefold() in failure.casefold() for failure in failures):
            raise AssertionError(
                f"{case_id} did not fail on {expected!r}: {failures}"
            )


def _assert_fam003_option_g_bp3_orchestration_guards() -> None:
    seam_proof = (
        "UFD-FAM003-20260724-001; formal normal USER launch; observability; "
        "ordered frames/video; raw evidence; manual USER validation; Workstream "
        "proof; H1 proof; LV proof; UTS proof; rollback; stop conditions"
    )
    seams = "\n".join(
        f"| `OPTG-WS{index:02d}` | `READY` | Seam {index} | {seam_proof} |"
        for index in range(1, 8)
    )
    allowlist = "\n".join(
        f"| `OPTG-ALLOW-{index:02d}` | `desktop/desktop_renderer.py` | Exact region {index} |"
        for index in range(1, 9)
    )
    recording = "\n".join(
        f"| `OPTG-RS-FG-{index:02d}` | Recording invariant {index} |"
        for index in range(1, 11)
    )
    workstream = "\n".join(
        f"| `OPTG-WS-FG-{index:02d}` | Workstream false-green {index} |"
        for index in range(1, 21)
    )
    packet = "\n".join(
        f"| `OPTG-PKT-FG-{index:02d}` | Packet false-green {index} |"
        for index in range(1, 23)
    )
    exact_entrypoints = "\n".join(
        (
            "`NonintrusivePerformanceController._surface_inventory`",
            "`NonintrusivePerformanceController._request_observation`",
            "`NonintrusivePerformanceController._open_active_surfaces`",
            "`NonintrusivePerformanceController._close_active_surfaces`",
            "`NonintrusivePerformanceController._request_post_use_idle`",
            "`_role`",
            "`_product_tree`",
            "`_process_snapshot`",
            "`_observe`",
        )
    )
    primary = (
        "# FAM-003 Option G BP3\n"
        "Primary Review Type: `BP3 Workstream Entry / Orchestration Validation`\n"
        "Branch: `feature/fam-003-settings-resize-proof`\n"
        "Packet Reviewability State: `Reviewable`\n"
        "USER Gate State: Pending USER Review\n"
        "BP1 Status: `USER Accepted`\n"
        "BP2 Status: `USER Accepted`\n"
        "BP3 Status: `Pending USER Review`\n"
        "Workstream Implementation: `UNAPPROVED`\n"
        "Whole-Package Result: `READY_FOR_USER_BP3_REVIEW`\n"
        "Entry Seam: `OPTG-WS01`\n"
        "Current Gate: `BP3 Workstream Entry / Orchestration Validation USER review "
        "pending; Workstream implementation remains blocked`\n"
        "H1 remains `NOT_ENTERED`\n"
        "LV remains `NOT_ENTERED`\n"
        "UTS remains `NOT_REQUESTED`\n"
        "ORIN Core CPU Contribution: `UNRESOLVED / DECISION 3`\n"
        "\n## Current Actionable Decision - BP3 Approval Only\n\n"
        f"{bundle.FAM003_OPTION_G_BP3_CURRENT_DECISION}\n"
        f"{bundle.FAM003_OPTION_G_BP3_DECISION_EFFECT}\n"
        "\n## USER Review Packet Finding\n\n"
        "USER Review Packet Finding: `PASS`\n"
        "Replacement Packet Folder: `C:\\Nexus USER\\FAM-003`\n"
        "Replacement ZIP Path: `C:\\Nexus USER\\FAM-003-20260724-120000.zip`\n"
        "Replacement ZIP Filename: `FAM-003-20260724-120000.zip`\n"
        "External Archive Receipt: `Recorded in the post-generation Codex return "
        "and FAM-003 external packet receipt outside this hashed archive.`\n"
        "Folder / ZIP Parity: `PASS (73 / 73; file-list and content-hash equality)`\n"
        "Primary USER Review Filename: "
        "`USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`\n"
        "Packet Reviewability State: `Reviewable`\n"
        "BP3 Readiness Result: `READY_FOR_USER_BP3_REVIEW`\n"
        "Workstream Implementation: `UNAPPROVED`\n"
        "\n## USER Review Response\n\n"
        "USER Review Response: Pending USER Review\n"
        "\n## Codex Response Digest\n\n"
        "Codex Response Digest: Pending USER Response - no BP3 approval recorded; "
        "Workstream implementation remains unapproved.\n"
        "\n## Future decision only - not requested, granted, or actionable at the "
        "current BP3 gate\n\n"
        f"{bundle.FAM003_OPTION_G_FUTURE_WORKSTREAM_DECISION}\n"
    )
    active_header = (
        "External State Schema: `external-state-v1`\n"
        "State Version: `7`\n"
        "Branch: `feature/fam-003-settings-resize-proof`\n"
        "Source Repo HEAD: `0123456789abcdef0123456789abcdef01234567`\n"
        "Current Gate: `BP3 Workstream Entry / Orchestration Validation USER review "
        "pending; Workstream implementation remains blocked`\n"
        "Workstream Result: `USER_DECISION_REQUIRED`\n"
        "H1 / LV / UTS: `NOT_ENTERED / NOT_ENTERED / NOT_REQUESTED`\n"
        "Next Legal Phase: `USER BP3 review and approval, waiver, revision, or block`\n"
        "Transition Status: "
        "`OPTION_G_BP3_FALSE_GREEN_PREVENTION_REPAIRED_READY_FOR_USER_REVIEW`\n"
        "Historical Receipt Boundary: `Historical content follows.`\n"
        "## Current Phase\n"
        "Current Gate: `Branch Planning - BP2 USER review pending`\n"
        "Next Legal Phase: `USER review of BP2`\n"
    )
    orchestration_text = (
        f"{seams}\n"
        "Bounded continuation remains active through `OPTG-WS07` until Workstream "
        "Green, a real blocker, or an explicit USER waiver.\n"
        "If attribution identifies a path, object, resource, or owner not explicitly "
        "enumerated in the accepted conditional repair matrix, Workstream must return "
        "`BLOCKED / USER decision required` before mutation.\n"
        "Current-carrier access does not establish ownership or self-admit repair scope.\n"
        "FAM-006/shared-owner stop\n"
    )
    boundary_text = (
        f"{allowlist}\n{exact_entrypoints}\n"
        "`STUDIO_RESIZABLE = False`\n"
        "`Start / Pause / Stop`\n"
    )
    fixture_text = f"{recording}\n{workstream}\n{packet}\n"
    ufd_topics = (
        "premature Workstream completion",
        "nonintrusive performance measurement",
        "Option G selection",
        "migration-first sequencing",
        "hidden HUD native-polling lifecycle",
        "Log Viewer Studio resize-hover polling",
        "Recording Studio exclusion",
        "Recording Studio direct behavior invariants",
        "attribution before conditional repair",
        "eight exact conditional repair allowlist regions",
        "unknown path/resource/object/owner stop",
        "FAM-006/shared-owner stop boundary",
        "current-carrier access does not transfer ownership",
        "ORIN Core Decision 3 deferral",
        "temporary-only Option D status",
        "BP2/BP3 separate USER gates",
        "Workstream/H1/LV/UTS phase separation",
        "proof-carrydown and validator false-green repair",
    )
    ufd_rows = []
    for index, topic in enumerate(ufd_topics, start=1):
        item_id = f"UFD-FAM003-20260724-{index:03d}"
        ufd_rows.append(
            f"### UFD Item: {item_id}\n"
            f"Feedback ID: `{item_id}`\n"
            f"Feedback Summary: `{topic}`\n"
            "Feedback Source: `USER direction`\n"
            "Feedback Phase: `BP3 repair`\n"
            "Disposition Type: `Current Branch Requirement`\n"
            "USER Decision State: `Accepted by USER`\n"
            "Owner Class: `Branch Plan`\n"
            "Canonical Owner File: `C:\\Nexus Governance State\\branches\\"
            "feature_fam_003_settings_resize_proof\\branch_plan.md`\n"
            "Workstream Severity: `Level 2 seam-blocking`\n"
            "Status: `Closed`\n"
            "Fold-Down Target: `Docs/branch_records/"
            "feature_fam_003_settings_resize_proof.md`\n"
            "Pointer Locations: `Active branch plan compact pointer`\n"
            "Source / Date: `USER / 2026-07-24`\n"
            f"USER Direction Or Finding: `Accepted Option G direction {index}`\n"
            "Affected Scope: `Option G`\n"
            "Affected Artifact: `BP3 packet`\n"
            "Classification: `Incorporated`\n"
            "Owner: `FAM-003`\n"
            "Carrier: `feature/fam-003-settings-resize-proof`\n"
            "Planning Or Implementation Effect: `Planning carrydown only`\n"
            "Proof / Closure Requirement: `Packet and fixture proof`\n"
            "Remaining USER Decision: `BP3 approval only`\n"
        )
    ufd_text = (
        "# Option G UFD And Fold-Down\n"
        "UFD Authority Classification: `SUPPORTING REVIEW COPY`\n"
        "USER Feedback Disposition Required: `Yes`\n"
        "UFD Ledger Status: `Complete`\n"
        "UFD Ledger Owner: `C:\\Nexus Governance State\\branches\\"
        "feature_fam_003_settings_resize_proof\\branch_plan.md`\n"
        "UFD Current Owner Class: `Branch Plan`\n"
        "UFD Current Canonical Owner File: `C:\\Nexus Governance State\\branches\\"
        "feature_fam_003_settings_resize_proof\\branch_plan.md`\n"
        "UFD Future Fold-Down Target: `Docs/branch_records/"
        "feature_fam_003_settings_resize_proof.md`\n"
        "Open UFD Count: `0`\n"
        "Blocking UFD Count: `0`\n"
        "Fold-Down Status: `Pending`\n"
        "Deferred / Future-Gated Scope Admission: `NONE`\n\n"
        + "\n".join(ufd_rows)
    )
    canonical_ufd_owner = (
        "C:\\Nexus Governance State\\branches\\"
        "feature_fam_003_settings_resize_proof\\branch_plan.md"
    )
    element_classifications = (
        "Touched",
        "Touched",
        "Touched",
        "Affected",
        "Planned",
        "Planned",
        "Affected",
        "Affected",
        "Affected",
        "Affected",
        "Deferred",
    )
    element_rows = "\n".join(
        f"| `OPTG-ELEM-{index:02d}` | element {index} | {classification} | "
        f"implementation {index} | Workstream proof {index} | H1 proof {index} | "
        f"Live Validation proof {index} | UTS proof {index} | boundary {index} | "
        f"BP3 pending | {canonical_ufd_owner} |"
        for index, classification in enumerate(element_classifications, start=1)
    )
    element_section = (
        "## Element-to-Phase Proof Matrix\n\n"
        "Matrix Status: `Present`\n"
        "USER Review Status: `Pending`\n"
        "Open Element Questions: `None`\n"
        f"Element Coverage Owner: `{canonical_ufd_owner}`\n"
        f"Element Validation Ledger Owner: `{canonical_ufd_owner}`\n\n"
        "| Element ID | Element / Surface | Element Classification | "
        "Workstream Implementation Plan | Workstream Proof Plan | "
        "Hardening Proof Plan | Live Validation Proof / Waiver Plan | "
        "UTS / USER Acceptance Path | Future / Deferred Boundary | "
        "USER Decision State | Source Owner / Ledger Owner |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        f"{element_rows}"
    )
    canonical_ufd_plan = (
        "External State Schema: `external-state-v1`\n"
        "State Version: `7`\n"
        "Record Class: `Live Branch Plan`\n"
        "Record Role: `Current branch planning projection`\n"
        "Branch: `feature/fam-003-settings-resize-proof`\n"
        "Source Repo HEAD: `0123456789abcdef0123456789abcdef01234567`\n"
        "USER Feedback Disposition Required: `Yes`\n"
        "UFD Ledger Status: `Complete`\n"
        f"UFD Ledger Owner: `{canonical_ufd_owner}`\n"
        "UFD Item Count: `18`\n"
        f"UFD Physical Detail Location: `{canonical_ufd_owner}`\n"
        "UFD Current Owner Class: `Branch Plan`\n"
        f"UFD Current Canonical Owner File: `{canonical_ufd_owner}`\n"
        "UFD Future Fold-Down Target: `Docs/branch_records/"
        "feature_fam_003_settings_resize_proof.md`\n"
        "UFD Supporting Evidence Copy: "
        "`decision2_option_g_bp3_proof_carrydown_repair_20260724.md`\n"
        "UFD Packet Review Copy: `Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md`\n"
        "Open UFD Count: `0`\n"
        "Blocking UFD Count: `0`\n"
        "Fold-Down Status: `Pending`\n"
        "Current Gate: `BP3 Workstream Entry / Orchestration Validation USER review "
        "pending; Workstream implementation remains blocked`\n"
        "Workstream Result: `USER_DECISION_REQUIRED`\n"
        "H1 / LV / UTS: `NOT_ENTERED / NOT_ENTERED / NOT_REQUESTED`\n"
        "Next Legal Phase: `USER BP3 review and approval, waiver, revision, or block`\n"
        "Transition Status: "
        "`OPTION_G_BP3_FALSE_GREEN_PREVENTION_REPAIRED_READY_FOR_USER_REVIEW`\n\n"
        + "\n".join(ufd_rows)
        + f"\n{element_section}\n"
        + "Historical Receipt Boundary: `Historical content follows.`\n"
        "## Current Phase\n"
        "Current Gate: `Branch Planning - BP2 USER review pending`\n"
    )
    supporting_ufd_record = (
        "# Option G BP3 Proof Carrydown Repair\n"
        "UFD Authority Classification: `SUPPORTING EVIDENCE COPY`\n"
        "UFD Ledger Status: `Complete`\n"
        f"UFD Ledger Owner: `{canonical_ufd_owner}`\n"
        "UFD Item Count: `18`\n"
        "UFD Current Owner Class: `Branch Plan`\n"
        f"UFD Current Canonical Owner File: `{canonical_ufd_owner}`\n"
        "UFD Future Fold-Down Target: `Docs/branch_records/"
        "feature_fam_003_settings_resize_proof.md`\n"
        "Open UFD Count: `0`\n"
        "Blocking UFD Count: `0`\n"
        "Fold-Down Status: `Pending`\n\n"
        + "\n".join(ufd_rows)
    )
    observability_claims = (
        "hidden HUD polling stopping",
        "HUD polling resuming",
        "HUD click-bridge lifecycle",
        "Log Viewer resize-hover polling state",
        "Recording Studio non-resizable behavior",
        "Recording Studio Start / Pause / Stop",
        "repeated retention cycles",
        "PID and process-role attribution",
        "allowlisted repair attribution",
        "unknown-owner stop",
        "clean shutdown/relaunch",
        "Option D effective flags",
        "performance evidence",
        "stale-UI avoidance after reopening",
    )
    observability_text = (
        "# Runtime Observability Decision Matrix\n"
        "Runtime Observability Decision Matrix Status: `COMPLETE`\n"
        + "\n".join(
            f"| {claim} | signal | ordered state | raw evidence | phase route |"
            for claim in observability_claims
        )
    )
    visual_claims = (
        "HUD visible/hidden transitions",
        "HUD reopen/resume behavior",
        "Log Viewer visible/hidden/resize-hover transitions",
        "resize cursor and hit-zone behavior",
        "active resize",
        "Recording Studio resize rejection",
        "Recording Studio Start / Pause / Stop",
        "Studio reopen behavior",
        "no stale UI",
        "no blank, black, partial, or corrupted WebEngine content",
        "conditional repair before/after behavior",
        "clean relaunch",
    )
    visual_text = (
        "# Visual Manual And Raw Evidence Plan\n"
        "Still-Image-Only Time-Dependent Proof: `REJECTED`\n"
        "Manual USER Validation / Waiver Routing: `COMPLETE`\n"
        "Raw-Evidence Plan Status: `COMPLETE`\n"
        "External-Pointer-Only Closure: `PROHIBITED`\n"
        + "\n".join(
            f"| {claim} | ordered frames/video | manual USER fallback | packet raw evidence |"
            for claim in visual_claims
        )
    )
    element_text = (
        "Element-to-Phase Authority Classification: `SUPPORTING REVIEW COPY`\n\n"
        f"{element_section}\n"
    )
    reconciliation_text = (
        "# Option G BP2 Acceptance Reconciliation\n"
        "Accepted BP2 Authority: `RECONCILED`\n"
        "Historical BP2 ZIP Disposition: `ABSENT / NOT RECONSTRUCTED`\n"
        "Stale BP2 Primary Disposition: `HISTORICAL PRE-ACCEPTANCE COPY`\n"
    )
    launcher_text = (
        "# Launcher And Proof Classification\n"
        "Exact Formal Launcher Path: "
        "`C:\\Users\\anden\\OneDrive\\Desktop\\Nexus Desktop Launcher.lnk`\n"
        "Shortcut Target: `C:\\Nexus Worktrees\\FAM-003\\launch_orin_desktop.vbs`\n"
        "Working Directory: `C:\\Nexus Worktrees\\FAM-003`\n"
        "Arguments: `NONE`\n"
        "Launcher Parity Result: `PASS`\n"
        "Troubleshooting / Helper Formal-Proof Substitution: `PROHIBITED`\n"
    )
    carrydown_text = (
        "# Accepted BP2 Proof Contract Carrydown\n"
        "Accepted BP2 observability, launcher, visual, manual, raw-evidence, "
        "and phase obligations are mapped to OPTG-WS01 through OPTG-WS07.\n"
    )
    provenance_checks = []
    provenance_files: dict[str, str] = {}
    validation_result_rows = []
    for index in range(1, 21):
        check_id = f"{index:02d}_fixture_check"
        command = f"py -3 dev/fixture_check_{index:02d}.py"
        raw_log = (
            "Source Truth Context/Proof Artifacts/Validation/Raw Logs/"
            f"{check_id}.txt"
        )
        expected_failure = index == 20
        expected_signature = "EXPECTED_FIXTURE_FAILURE_SIGNATURE"
        exit_code = 1 if expected_failure else 0
        result_output = (
            f"{expected_signature}\n"
            if expected_failure
            else f"{check_id}: PASS\n"
        )
        final_disposition = (
            "EXPECTED_FAIL_CONFIRMED" if expected_failure else "PASS"
        )
        raw_text = (
            f"Command: {command}\n"
            "Working Directory: C:\\Nexus Worktrees\\FAM-003\n"
            "Started UTC: 2026-07-25T00:00:00Z\n"
            "Ended UTC: 2026-07-25T00:00:01Z\n"
            "Duration MS: 1000\n"
            f"Exit Code: {exit_code}\n"
            "Output Mode: merged stdout/stderr\n"
            "--- MERGED STDOUT/STDERR ---\n"
            f"{result_output}"
        )
        provenance_files[raw_log] = raw_text
        provenance_checks.append(
            {
                "id": check_id,
                "executable": "py",
                "arguments": ["-3", f"dev/fixture_check_{index:02d}.py"],
                "command": command,
                "workingDirectory": r"C:\Nexus Worktrees\FAM-003",
                "startedUtc": "2026-07-25T00:00:00Z",
                "endedUtc": "2026-07-25T00:00:01Z",
                "durationMs": 1000,
                "exitCode": exit_code,
                "stdout": "NOT_SEPARATELY_CAPTURED",
                "stderr": "NOT_SEPARATELY_CAPTURED",
                "mergedOutput": result_output,
                "outputMode": "merged stdout/stderr",
                "rawLog": raw_log,
                "rawLogSha256": hashlib.sha256(raw_text.encode("utf-8"))
                .hexdigest()
                .upper(),
                "helperIdentity": f"dev/fixture_check_{index:02d}.py@fixture",
                "fixture": f"fixture-{index:02d}",
                "targets": [f"fixture-target-{index:02d}"],
                "expectedIdentities": {
                    "branch": "feature/fam-003-settings-resize-proof",
                    "head": "0123456789abcdef0123456789abcdef01234567",
                },
                "expectedHashes": {
                    "HEAD": "0123456789abcdef0123456789abcdef01234567"
                },
                "applicabilityResult": "APPLICABLE",
                "applicabilityReason": "Executed as part of the complete current BP3 final validation suite.",
                "expectedDisposition": "EXPECTED_FAIL" if expected_failure else "PASS",
                "expectedFailureSignature": (
                    expected_signature if expected_failure else "NONE"
                ),
                "finalDisposition": final_disposition,
                "finalValidationResult": "PASS",
            }
        )
        validation_result_rows.append(
            f"| `{check_id}` | {command} | `{final_disposition}` | `{raw_log}` |"
        )
    applicability_row = {
        "id": "NA01_fam003_r2_scope_audit",
        "helperIdentity": bundle.FAM003_OPTION_G_SCOPE_AUDIT_HELPER,
        "registeredScope": "Workstream-scoped",
        "currentPacketClass": "BP3 Workstream Entry / Orchestration Validation USER review",
        "executed": False,
        "applicabilityResult": "Not Applicable With Reason",
        "applicabilityReason": bundle.FAM003_OPTION_G_SCOPE_AUDIT_NA_REASON,
        "sourceTruthBasis": "Docs/validation_helper_registry.md: FAM-003 R2 Workstream completion scope-audit helper row",
        "expectedDisposition": "NOT_APPLICABLE_WITH_REASON",
        "finalDisposition": "NOT_APPLICABLE_WITH_REASON",
        "finalValidationResult": "PASS",
    }
    provenance_summary = json.dumps(
        {
            "schema": bundle.FAM003_OPTION_G_VALIDATION_PROVENANCE_SCHEMA,
            "finalSuiteInventory": [
                *(check["id"] for check in provenance_checks),
                applicability_row["id"],
            ],
            "suiteDispositionCounts": {
                "PASS": 19,
                "EXPECTED_FAIL_CONFIRMED": 1,
                "NOT_APPLICABLE_WITH_REASON": 1,
                "FAILED": 0,
            },
            "finalValidationResult": "PASS",
            "applicability": [applicability_row],
            "checks": provenance_checks,
        },
        indent=2,
    )
    validation_results_text = (
        "BP3 Decision Surface Validation: `PASS`\n"
        "USER Review Response: `Pending USER Review`\n"
        "Workstream Implementation: `UNAPPROVED`\n"
        "Future Workstream Decision: `FUTURE_ONLY_NON_ACTIONABLE`\n\n"
        "| Check ID | Exact command | Result | Raw log |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(validation_result_rows)
        + "\n"
    )
    fixture_head = "0123456789abcdef0123456789abcdef01234567"
    fixture_projection_hashes = {
        "Source Truth Context/current_external_branch_plan.md": "1" * 64,
        "Source Truth Context/current_external_branch_state.md": "2" * 64,
        "Source Truth Context/current_external_worktree_state.md": "3" * 64,
    }
    fixture_delta_files = [
        "Docs/validation_helper_registry.md",
        "dev/orin_user_review_bundle.py",
        "dev/orin_user_review_bundle_false_green_fixture_validation.py",
    ]
    fixture_lineage_files = sorted(bundle.FAM003_OPTION_G_APPROVED_REPAIR_FILES)
    fixture_lineage_commits = ["a" * 40, "b" * 40, "c" * 40, fixture_head]
    fixture_snapshot = "snapshot-20260726T010203Z-a1b2c3d4"
    fixture_receipt = "fam003-option-g-bp3-validation-disposition-repair-20260726T010203Z.json"
    fixture_packet = r"C:\Nexus USER\FAM-003-20260726-010203.zip"
    fixture_rollback = (
        f"Revert {fixture_head}, restore {fixture_snapshot} only if the governed "
        "external transition is defective, then revalidate all three projections."
    )
    packet_manifest = json.dumps(
        {
            "currentActionableDecision": "BP3 approval only",
            "futureWorkstreamDecision": "FUTURE_ONLY_NON_ACTIONABLE",
            "userGateState": "Pending USER Review",
            "workstreamImplementation": "UNAPPROVED",
            "Source Repo HEAD": fixture_head,
            "externalStateVersion": 24,
            "Replacement ZIP": fixture_packet,
            "Projection Raw Hashes": fixture_projection_hashes,
            "Current Repair Delta": {
                "commitCount": 1,
                "commits": [fixture_head],
                "changedFileCount": len(fixture_delta_files),
                "changedFiles": fixture_delta_files,
                "sourceHead": fixture_head,
                "snapshotIdentity": fixture_snapshot,
                "stateVersion": 24,
                "projectionHashes": fixture_projection_hashes,
                "transactionReceipt": fixture_receipt,
                "rollbackRoute": fixture_rollback,
                "packetIdentity": fixture_packet,
            },
            "Repair Lineage": {
                "commitCount": len(fixture_lineage_commits),
                "commits": fixture_lineage_commits,
                "changedFileCount": len(fixture_lineage_files),
                "changedFiles": fixture_lineage_files,
            },
        },
        indent=2,
    )
    active_rollback_ledger = (
        "# Option G BP3 External Transaction And Rollback Ledger\n\n"
        "## Current Actionable Rollback Model\n\n"
        f"Source HEAD: `{fixture_head}`\n"
        f"Current repair commit: `{fixture_head}`\n"
        + "\n".join(f"- Current repair file: `{path}`" for path in fixture_delta_files)
        + "\n"
        f"Snapshot Identity: `{fixture_snapshot}`\n"
        f"Transaction Receipt: `{fixture_receipt}`\n"
        f"Packet Identity: `{fixture_packet}`\n"
        + "\n".join(
            f"Projection Hash: `{value}`" for value in fixture_projection_hashes.values()
        )
        + "\n"
        f"Rollback Route: {fixture_rollback}\n\n"
        "## Historical / Superseded Evidence\n\n"
        "The prior two-file model and snapshot-20260725T021152Z-da786968 are "
        "historical only and are not current rollback instructions.\n"
    )
    valid = {
        "START_HERE.md": (
            "# FAM-003 Option G BP3\n"
            "Branch: `feature/fam-003-settings-resize-proof`\n"
            "Primary USER Review File: `USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`\n"
            "Current Gate: `BP3 Workstream Entry / Orchestration Validation USER review "
            "pending; Workstream implementation remains blocked`\n"
            "Current Actionable Decision: `BP3 approval only`\n"
            "Workstream Implementation: `UNAPPROVED`\n\n"
            f"{bundle.FAM003_OPTION_G_BP3_CURRENT_DECISION}\n"
            f"{bundle.FAM003_OPTION_G_BP3_DECISION_EFFECT}\n"
        ),
        "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md": primary,
        "Review Aids/USER_DECISIONS.md": (
            "# USER Decisions\n\n"
            "## Current Actionable Decision - BP3 Approval Only\n\n"
            "Workstream Implementation: `UNAPPROVED`\n\n"
            f"{bundle.FAM003_OPTION_G_BP3_CURRENT_DECISION}\n\n"
            f"{bundle.FAM003_OPTION_G_BP3_DECISION_EFFECT}\n\n"
            "## Future decision only - not requested, granted, or actionable at the "
            "current BP3 gate\n\n"
            f"{bundle.FAM003_OPTION_G_FUTURE_WORKSTREAM_DECISION}\n"
        ),
        "Review Aids/OPTION_G_WHOLE_PACKAGE_ORCHESTRATION.md": orchestration_text,
        "Review Aids/OPTION_G_CODE_AND_ALLOWLIST_BOUNDARY.md": boundary_text,
        "Review Aids/OPTION_G_FALSE_GREEN_AND_PROOF_MATRIX.md": fixture_text,
        "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md": ufd_text,
        "Review Aids/OPTION_G_BP2_ACCEPTANCE_RECONCILIATION.md": reconciliation_text,
        "Review Aids/OPTION_G_BP2_PROOF_CONTRACT_CARRYDOWN.md": carrydown_text,
        "Review Aids/OPTION_G_LAUNCHER_AND_PROOF_CLASSIFICATION.md": launcher_text,
        "Review Aids/OPTION_G_RUNTIME_OBSERVABILITY_DECISION_MATRIX.md": observability_text,
        "Review Aids/OPTION_G_VISUAL_MANUAL_RAW_EVIDENCE_PLAN.md": visual_text,
        "Review Aids/OPTION_G_ELEMENT_TO_PHASE_MATRIX.md": element_text,
        "Review Aids/OPTION_G_BP3_REPAIR_DEFECT_LEDGER.md": (
            "# Defect Ledger\n"
            "`OPTG-BP3-DS-DEF-01`\n"
            "`OPTG-BP3-DS-DEF-02`\n"
            "`OPTG-BP3-DS-DEF-03`\n"
            "`OPTG-BP3-DS-DEF-04`\n"
            "`OPTG-BP3-DS-DEF-05`\n"
            "`OPTG-BP3-DS-DEF-06`\n"
            "`OPTG-BP3-DS-DEF-07`\n"
            "Validator false-green defects are closed with proof.\n"
        ),
        "Review Aids/OPTION_G_EXTERNAL_TRANSACTION_AND_ROLLBACK_LEDGER.md": (
            active_rollback_ledger
        ),
        "Source Truth Context/Proof Artifacts/Validation/PACKET_MANIFEST.json": packet_manifest,
        "Source Truth Context/Proof Artifacts/Validation/VALIDATION_RESULTS.md": (
            validation_results_text
        ),
        (
            "Source Truth Context/Proof Artifacts/Validation/Raw Logs/"
            "validation_summary.json"
        ): provenance_summary,
        "Source Truth Context/current_external_branch_plan.md": canonical_ufd_plan,
        "Source Truth Context/current_external_branch_state.md": active_header,
        "Source Truth Context/current_external_worktree_state.md": active_header,
        (
            "Source Truth Context/Repo Owners/"
            "feature_fam_003_settings_resize_proof.md"
        ): (
            "# Branch Record: feature/fam-003-settings-resize-proof\n"
            "External Branch Plan Owner: "
            "`C:\\Nexus Governance State\\branches\\"
            "feature_fam_003_settings_resize_proof\\branch_plan.md`\n"
            "Receipt Class: `Compact future fold-down target`\n"
        ),
        (
            "Source Truth Context/Active External Snapshot/"
            "decision2_option_g_bp3_proof_carrydown_repair_20260724.md"
        ): supporting_ufd_record,
    }
    valid.update(provenance_files)
    valid_failures = bundle._fam003_option_g_bp3_orchestration_failures(
        valid,
        status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
    )
    if valid_failures:
        raise AssertionError(
            "Valid FAM-003 Option G BP3 orchestration fixture failed:\n"
            + "\n".join(valid_failures)
        )
    active_state_failures = bundle._bp3_active_state_consistency_failures(
        valid,
        status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
    )
    if active_state_failures:
        raise AssertionError(
            "Valid external-state-v1 BP3 live header failed active-state validation:\n"
            + "\n".join(active_state_failures)
        )

    cases = (
        (
            "OPTG-BP3-FG-01",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            "USER Feedback Disposition Required: `Yes`",
            "",
            "required UFD required",
        ),
        (
            "OPTG-BP3-FG-02",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            "UFD Ledger Status: `Complete`",
            "",
            "required UFD ledger",
        ),
        (
            "OPTG-BP3-FG-03",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            "Open UFD Count: `0`",
            "Open UFD Count: `1`",
            "UFD Open count disagrees",
        ),
        (
            "OPTG-BP3-FG-04",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            "proof-carrydown and validator false-green repair",
            "minor note",
            "material USER direction is absent",
        ),
        (
            "OPTG-BP3-FG-05",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            "Deferred / Future-Gated Scope Admission: `NONE`",
            "Deferred / Future-Gated Scope Admission: `ADMITTED`",
            "deferred/future-gated feedback",
        ),
        (
            "OPTG-BP3-FG-06",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            "# Option G UFD And Fold-Down",
            "# Option G Defect Reference",
            "required UFD heading",
        ),
        (
            "OPTG-BP3-FG-07",
            "Review Aids/OPTION_G_RUNTIME_OBSERVABILITY_DECISION_MATRIX.md",
            "hidden HUD polling stopping",
            "HUD state",
            "observability obligation is missing",
        ),
        (
            "OPTG-BP3-FG-08",
            "Review Aids/OPTION_G_LAUNCHER_AND_PROOF_CLASSIFICATION.md",
            "Exact Formal Launcher Path:",
            "Launcher Path:",
            "required formal normal launcher",
        ),
        (
            "OPTG-BP3-FG-09",
            "Review Aids/OPTION_G_LAUNCHER_AND_PROOF_CLASSIFICATION.md",
            "Launcher Parity Result: `PASS`",
            "Launcher Parity Result: `UNPROVEN`",
            "required launcher parity",
        ),
        (
            "OPTG-BP3-FG-10",
            "Review Aids/OPTION_G_LAUNCHER_AND_PROOF_CLASSIFICATION.md",
            "Troubleshooting / Helper Formal-Proof Substitution: `PROHIBITED`",
            "Troubleshooting / Helper Formal-Proof Substitution: `ALLOWED`",
            "required troubleshooting not formal",
        ),
        (
            "OPTG-BP3-FG-11",
            "Review Aids/OPTION_G_BP2_ACCEPTANCE_RECONCILIATION.md",
            "Stale BP2 Primary Disposition: `HISTORICAL PRE-ACCEPTANCE COPY`",
            "Stale BP2 Primary Disposition: `Pending USER Response`",
            "required stale BP2 copy classified",
        ),
        (
            "OPTG-BP3-FG-12",
            "Review Aids/OPTION_G_VISUAL_MANUAL_RAW_EVIDENCE_PLAN.md",
            "Still-Image-Only Time-Dependent Proof: `REJECTED`",
            "Still-Image-Only Time-Dependent Proof: `ACCEPTED`",
            "required time-dependent still rejection",
        ),
        (
            "OPTG-BP3-FG-13",
            "Review Aids/OPTION_G_VISUAL_MANUAL_RAW_EVIDENCE_PLAN.md",
            "HUD visible/hidden transitions",
            "HUD final state",
            "visual/video/ordered-frame plan is missing",
        ),
        (
            "OPTG-BP3-FG-14",
            "Review Aids/OPTION_G_VISUAL_MANUAL_RAW_EVIDENCE_PLAN.md",
            "Manual USER Validation / Waiver Routing: `COMPLETE`",
            "",
            "required manual validation routed",
        ),
        (
            "OPTG-BP3-FG-15",
            "Review Aids/OPTION_G_VISUAL_MANUAL_RAW_EVIDENCE_PLAN.md",
            "Raw-Evidence Plan Status: `COMPLETE`",
            "",
            "required raw evidence complete",
        ),
        (
            "OPTG-BP3-FG-16",
            "Review Aids/OPTION_G_VISUAL_MANUAL_RAW_EVIDENCE_PLAN.md",
            "External-Pointer-Only Closure: `PROHIBITED`",
            "External-Pointer-Only Closure: `ALLOWED`",
            "required external pointers insufficient",
        ),
        (
            "OPTG-BP3-FG-17",
            "Review Aids/OPTION_G_ELEMENT_TO_PHASE_MATRIX.md",
            "| `OPTG-ELEM-11`",
            "| element-11",
            "packet aid differs from the canonical",
        ),
        (
            "OPTG-BP3-FG-18",
            "Review Aids/OPTION_G_WHOLE_PACKAGE_ORCHESTRATION.md",
            "UFD-FAM003-20260724-001; formal normal USER launch; observability;",
            "basic proof;",
            "seam omits proof-contract carrydown",
        ),
        (
            "OPTG-BP3-FG-19",
            "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
            "ORIN Core CPU Contribution: `UNRESOLVED / DECISION 3`",
            "ORIN Core CPU Contribution: `RESOLVED`",
            "required ORIN Core unresolved",
        ),
        (
            "OPTG-BP3-FG-20",
            "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
            "Workstream Implementation: `UNAPPROVED`",
            "Workstream Implementation: `APPROVED`",
            "forbidden implementation already authorized",
        ),
        (
            "OPTG-BP3-FG-21",
            "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
            "H1 remains `NOT_ENTERED`",
            "H1 executes under Workstream authority",
            "required H1 boundary",
        ),
        (
            "OPTG-BP3-FG-22",
            "Review Aids/OPTION_G_BP2_ACCEPTANCE_RECONCILIATION.md",
            "Historical BP2 ZIP Disposition: `ABSENT / NOT RECONSTRUCTED`",
            "Historical BP2 ZIP was reconstructed from packet copies",
            "required historical BP2 ZIP not reconstructed",
        ),
    )
    for case_id, file_name, old, new, expected in cases:
        mutated = dict(valid)
        mutated[file_name] = mutated[file_name].replace(old, new, 1)
        failures = bundle._fam003_option_g_bp3_orchestration_failures(
            mutated,
            status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
        )
        if not any(expected.casefold() in failure.casefold() for failure in failures):
            raise AssertionError(
                f"{case_id} did not fail on {expected!r}: {failures}"
            )

    canonical_ufd_cases = (
        (
            "OPTG-BP3-UFD-FG-01",
            "Source Truth Context/current_external_branch_plan.md",
            "\n".join(ufd_rows),
            "",
            "physically contain exactly 18",
        ),
        (
            "OPTG-BP3-UFD-FG-02",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            "UFD Authority Classification: `SUPPORTING REVIEW COPY`",
            "UFD Authority Classification: `CANONICAL SOURCE TRUTH`",
            "supporting review copy",
        ),
        (
            "OPTG-BP3-UFD-FG-03",
            (
                "Source Truth Context/Active External Snapshot/"
                "decision2_option_g_bp3_proof_carrydown_repair_20260724.md"
            ),
            "UFD Authority Classification: `SUPPORTING EVIDENCE COPY`",
            "UFD Authority Classification: `CANONICAL SOURCE TRUTH`",
            "supporting evidence copy",
        ),
        (
            "OPTG-BP3-UFD-FG-04",
            "Source Truth Context/current_external_branch_plan.md",
            f"UFD Ledger Owner: `{canonical_ufd_owner}`",
            "UFD Ledger Owner: `Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md`",
            "owner marker disagrees",
        ),
        (
            "OPTG-BP3-UFD-FG-05",
            "Source Truth Context/current_external_branch_plan.md",
            f"UFD Physical Detail Location: `{canonical_ufd_owner}`",
            "UFD Physical Detail Location: `separate-annex.md`",
            "physical-detail location",
        ),
        (
            "OPTG-BP3-UFD-FG-06",
            "Source Truth Context/current_external_branch_plan.md",
            "UFD Item Count: `18`",
            "UFD Item Count: `17`",
            "UFD Item Count must be 18",
        ),
        (
            "OPTG-BP3-UFD-FG-07",
            "Source Truth Context/current_external_branch_plan.md",
            ufd_rows[-1],
            "",
            "physically contain exactly 18",
        ),
        (
            "OPTG-BP3-UFD-FG-08",
            "Source Truth Context/current_external_branch_plan.md",
            "Open UFD Count: `0`",
            "Open UFD Count: `1`",
            "open count disagrees",
        ),
        (
            "OPTG-BP3-UFD-FG-09",
            "Source Truth Context/current_external_branch_plan.md",
            "Blocking UFD Count: `0`",
            "Blocking UFD Count: `1`",
            "blocking count disagrees",
        ),
        (
            "OPTG-BP3-UFD-FG-10",
            "Source Truth Context/current_external_branch_plan.md",
            "UFD Supporting Evidence Copy:",
            "UFD Detail Record:",
            "redirects UFD detail",
        ),
        (
            "OPTG-BP3-UFD-FG-11",
            "Source Truth Context/current_external_branch_plan.md",
            "UFD Packet Review Copy: `Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md`\n",
            "",
            "generated packet UFD aid",
        ),
        (
            "OPTG-BP3-UFD-FG-12",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            "USER Direction Or Finding: `Accepted Option G direction 1`",
            "USER Direction Or Finding: `Divergent packet copy`",
            "differs from the canonical",
        ),
        (
            "OPTG-BP3-UFD-FG-13",
            (
                "Source Truth Context/Active External Snapshot/"
                "decision2_option_g_bp3_proof_carrydown_repair_20260724.md"
            ),
            "USER Direction Or Finding: `Accepted Option G direction 1`",
            "USER Direction Or Finding: `Divergent evidence copy`",
            "differs from the canonical",
        ),
        (
            "OPTG-BP3-UFD-FG-14",
            "Source Truth Context/current_external_branch_plan.md",
            "\n".join(ufd_rows)
            + f"\n{element_section}\n"
            + "Historical Receipt Boundary: `Historical content follows.`\n",
            f"{element_section}\n"
            + "Historical Receipt Boundary: `Historical content follows.`\n"
            + "\n".join(ufd_rows)
            + "\n",
            "physically contain exactly 18",
        ),
        (
            "OPTG-BP3-UFD-FG-15",
            "Source Truth Context/current_external_branch_plan.md",
            "Proof / Closure Requirement: `Packet and fixture proof`",
            "Proof Closure Requirement: `Packet and fixture proof`",
            "differs from the canonical",
        ),
        (
            "OPTG-BP3-UFD-FG-16",
            "Source Truth Context/current_external_branch_plan.md",
            ufd_rows[-1],
            ufd_rows[-2],
            "physically contain exactly 18",
        ),
        (
            "OPTG-BP3-UFD-FG-17",
            "Source Truth Context/current_external_branch_plan.md",
            "UFD Supporting Evidence Copy: "
            "`decision2_option_g_bp3_proof_carrydown_repair_20260724.md`\n",
            "",
            "proof-carrydown record",
        ),
        (
            "OPTG-BP3-UFD-FG-18",
            "Source Truth Context/current_external_branch_plan.md",
            f"UFD Physical Detail Location: `{canonical_ufd_owner}`",
            "UFD Physical Detail Location: `ufd_ledger.md`",
            "physical-detail location",
        ),
        (
            "OPTG-BP3-UFD-FG-19",
            "Source Truth Context/current_external_branch_plan.md",
            "Owner Class: `Branch Plan`",
            "Owner Class: `Branch Record`",
            "Owner Class must be Branch Plan",
        ),
        (
            "OPTG-BP3-UFD-FG-20",
            "Source Truth Context/current_external_branch_plan.md",
            f"Canonical Owner File: `{canonical_ufd_owner}`",
            "Canonical Owner File: `Docs/branch_records/"
            "feature_fam_003_settings_resize_proof.md`",
            "Canonical Owner File must match",
        ),
        (
            "OPTG-BP3-UFD-FG-21",
            "Source Truth Context/current_external_branch_plan.md",
            f"Canonical Owner File: `{canonical_ufd_owner}`",
            "Canonical Owner File: `Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md`",
            "Canonical Owner File must match",
        ),
        (
            "OPTG-BP3-UFD-FG-22",
            "Source Truth Context/current_external_branch_plan.md",
            "Fold-Down Target: `Docs/branch_records/"
            "feature_fam_003_settings_resize_proof.md`",
            f"Fold-Down Target: `{canonical_ufd_owner}`",
            "Fold-Down Target must identify",
        ),
        (
            "OPTG-BP3-UFD-FG-23",
            "Source Truth Context/current_external_branch_plan.md",
            "Fold-Down Target: `Docs/branch_records/"
            "feature_fam_003_settings_resize_proof.md`",
            "Fold-Down Target: ``",
            "Fold-Down Target must identify",
        ),
        (
            "OPTG-BP3-UFD-FG-24",
            "Source Truth Context/current_external_branch_plan.md",
            "UFD Current Owner Class: `Branch Plan`",
            "UFD Current Owner Class: `Branch Record`",
            "UFD Current Owner Class must be Branch Plan",
        ),
        (
            "OPTG-BP3-UFD-FG-25",
            "Source Truth Context/current_external_branch_plan.md",
            f"UFD Current Canonical Owner File: `{canonical_ufd_owner}`",
            "UFD Current Canonical Owner File: `Docs/branch_records/"
            "feature_fam_003_settings_resize_proof.md`",
            "UFD Current Canonical Owner File must match",
        ),
        (
            "OPTG-BP3-UFD-FG-26",
            "Source Truth Context/current_external_branch_plan.md",
            "UFD Future Fold-Down Target: `Docs/branch_records/"
            "feature_fam_003_settings_resize_proof.md`",
            f"UFD Future Fold-Down Target: `{canonical_ufd_owner}`",
            "UFD Future Fold-Down Target must identify",
        ),
        (
            "OPTG-BP3-UFD-FG-27",
            "Source Truth Context/current_external_branch_plan.md",
            "UFD Future Fold-Down Target: `Docs/branch_records/"
            "feature_fam_003_settings_resize_proof.md`",
            "UFD Future Fold-Down Target: ``",
            "UFD Future Fold-Down Target must identify",
        ),
        (
            "OPTG-BP3-UFD-FG-28",
            "Source Truth Context/current_external_branch_plan.md",
            "Pointer Locations: `Active branch plan compact pointer`",
            "Pointer Locations: `this annex`",
            "context-relative location wording",
        ),
        (
            "OPTG-BP3-UFD-FG-29",
            "Source Truth Context/current_external_branch_plan.md",
            "Pointer Locations: `Active branch plan compact pointer`",
            "Pointer Locations: `the annex`",
            "context-relative location wording",
        ),
        (
            "OPTG-BP3-UFD-FG-30",
            "Source Truth Context/current_external_branch_plan.md",
            "Pointer Locations: `Active branch plan compact pointer`",
            "Pointer Locations: `this supporting record`",
            "context-relative location wording",
        ),
        (
            "OPTG-BP3-UFD-FG-31",
            "Source Truth Context/current_external_branch_plan.md",
            "Pointer Locations: `Active branch plan compact pointer`",
            "Pointer Locations: `the record above`",
            "context-relative location wording",
        ),
        (
            "OPTG-BP3-UFD-FG-32",
            (
                "Source Truth Context/Repo Owners/"
                "feature_fam_003_settings_resize_proof.md"
            ),
            "Receipt Class: `Compact future fold-down target`\n",
            "Receipt Class: `Compact future fold-down target`\n"
            + ufd_rows[0],
            "repo branch record must remain a compact",
        ),
        (
            "OPTG-BP3-UFD-FG-33",
            (
                "Source Truth Context/Repo Owners/"
                "feature_fam_003_settings_resize_proof.md"
            ),
            canonical_ufd_owner,
            "missing-current-owner",
            "repo branch record must point",
        ),
        (
            "OPTG-BP3-UFD-FG-34",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            ufd_rows[0],
            ufd_rows[0].replace(
                "Owner Class: `Branch Plan`",
                "Owner Class: `Branch Record`",
            ),
            "differs from the canonical",
        ),
        (
            "OPTG-BP3-UFD-FG-35",
            (
                "Source Truth Context/Active External Snapshot/"
                "decision2_option_g_bp3_proof_carrydown_repair_20260724.md"
            ),
            ufd_rows[0],
            ufd_rows[0].replace(
                "Owner Class: `Branch Plan`",
                "Owner Class: `Branch Record`",
            ),
            "differs from the canonical",
        ),
        (
            "OPTG-BP3-UFD-FG-36",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            ufd_rows[0],
            ufd_rows[0].replace(
                f"Canonical Owner File: `{canonical_ufd_owner}`",
                "Canonical Owner File: `Docs/branch_records/"
                "feature_fam_003_settings_resize_proof.md`",
            ),
            "differs from the canonical",
        ),
        (
            "OPTG-BP3-UFD-FG-37",
            (
                "Source Truth Context/Active External Snapshot/"
                "decision2_option_g_bp3_proof_carrydown_repair_20260724.md"
            ),
            ufd_rows[0],
            ufd_rows[0].replace(
                f"Canonical Owner File: `{canonical_ufd_owner}`",
                "Canonical Owner File: `Docs/branch_records/"
                "feature_fam_003_settings_resize_proof.md`",
            ),
            "differs from the canonical",
        ),
        (
            "OPTG-BP3-UFD-FG-38",
            "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md",
            ufd_rows[0],
            ufd_rows[0].replace(
                "Pointer Locations: `Active branch plan compact pointer`",
                "Pointer Locations: `this annex`",
            ),
            "differs from the canonical",
        ),
    )
    for case_id, file_name, old, new, expected in canonical_ufd_cases:
        mutated = dict(valid)
        mutated[file_name] = mutated[file_name].replace(old, new, 1)
        failures = bundle._fam003_option_g_bp3_orchestration_failures(
            mutated,
            status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
        )
        if not any(expected.casefold() in failure.casefold() for failure in failures):
            raise AssertionError(
                f"{case_id} did not fail on {expected!r}: {failures}"
            )

    element_matrix_cases = (
        (
            "OPTG-BP3-ELEM-FG-01",
            "Source Truth Context/current_external_branch_plan.md",
            element_section + "\n",
            "",
            "physically contain the Element-to-Phase",
        ),
        (
            "OPTG-BP3-ELEM-FG-02",
            "Source Truth Context/current_external_branch_plan.md",
            f"Element Coverage Owner: `{canonical_ufd_owner}`",
            "Element Coverage Owner: `this branch-plan-owned annex`",
            "Element Coverage Owner must name",
        ),
        (
            "OPTG-BP3-ELEM-FG-03",
            "Source Truth Context/current_external_branch_plan.md",
            f"Element Validation Ledger Owner: `{canonical_ufd_owner}`",
            "Element Validation Ledger Owner: `future Workstream raw-evidence manifest`",
            "Element Validation Ledger Owner must name",
        ),
        (
            "OPTG-BP3-ELEM-FG-04",
            "Source Truth Context/current_external_branch_plan.md",
            "Element Classification | Workstream Implementation Plan",
            "Classification | Workstream Implementation Plan",
            "exact 11-column schema",
        ),
        (
            "OPTG-BP3-ELEM-FG-05",
            "Source Truth Context/current_external_branch_plan.md",
            "| element 7 | Affected |",
            "| element 7 | Preserved |",
            "invalid Element Classification",
        ),
        (
            "OPTG-BP3-ELEM-FG-06",
            "Source Truth Context/current_external_branch_plan.md",
            next(
                line
                for line in element_section.splitlines()
                if line.startswith("| `OPTG-ELEM-11`")
            )
            + "\n",
            "",
            "exactly the ordered rows",
        ),
        (
            "OPTG-BP3-ELEM-FG-07",
            "Review Aids/OPTION_G_ELEMENT_TO_PHASE_MATRIX.md",
            "Element-to-Phase Authority Classification: `SUPPORTING REVIEW COPY`",
            "Element-to-Phase Authority Classification: `CANONICAL SOURCE TRUTH`",
            "SUPPORTING REVIEW COPY",
        ),
        (
            "OPTG-BP3-ELEM-FG-08",
            "Review Aids/OPTION_G_ELEMENT_TO_PHASE_MATRIX.md",
            "| element 1 | Touched |",
            "| divergent element 1 | Touched |",
            "packet aid differs from the canonical",
        ),
        (
            "OPTG-BP3-ELEM-FG-09",
            "Source Truth Context/current_external_branch_plan.md",
            element_section
            + "\nHistorical Receipt Boundary: `Historical content follows.`\n",
            "Historical Receipt Boundary: `Historical content follows.`\n"
            + element_section
            + "\n",
            "physically contain the Element-to-Phase",
        ),
        (
            "OPTG-BP3-ELEM-FG-10",
            "Source Truth Context/current_external_branch_plan.md",
            "| Workstream proof 1 |",
            "|  |",
            "empty Element-to-Phase proof-path cell",
        ),
        (
            "OPTG-BP3-ELEM-FG-11",
            "Source Truth Context/current_external_branch_plan.md",
            "| boundary 1 | BP3 pending |",
            "| boundary 1 | extra | BP3 pending |",
            "has 12 columns",
        ),
        (
            "OPTG-BP3-ELEM-FG-12",
            "Source Truth Context/current_external_branch_plan.md",
            "Matrix Status: `Present`",
            "Matrix Status: `COMPLETE`",
            "Matrix Status is missing or invalid",
        ),
    )
    for case_id, file_name, old, new, expected in element_matrix_cases:
        mutated = dict(valid)
        mutated[file_name] = mutated[file_name].replace(old, new, 1)
        failures = bundle._fam003_option_g_bp3_orchestration_failures(
            mutated,
            status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
        )
        if not any(expected.casefold() in failure.casefold() for failure in failures):
            raise AssertionError(
                f"{case_id} did not fail on {expected!r}: {failures}"
            )

    provenance_summary_path = (
        "Source Truth Context/Proof Artifacts/Validation/Raw Logs/"
        "validation_summary.json"
    )

    def _assert_provenance_failure(
        case_id: str,
        summary_value: object,
        expected: str,
        *,
        remove_file: str | None = None,
        validation_text: str | None = None,
        file_updates: dict[str, str] | None = None,
    ) -> None:
        mutated = dict(valid)
        mutated[provenance_summary_path] = json.dumps(summary_value, indent=2)
        if remove_file:
            mutated.pop(remove_file, None)
        if validation_text is not None:
            mutated[
                "Source Truth Context/Proof Artifacts/Validation/VALIDATION_RESULTS.md"
            ] = validation_text
        if file_updates:
            mutated.update(file_updates)
        failures = bundle._fam003_option_g_bp3_orchestration_failures(
            mutated,
            status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
        )
        if not any(expected.casefold() in failure.casefold() for failure in failures):
            raise AssertionError(
                f"{case_id} did not fail on {expected!r}: {failures}"
            )

    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-01",
        provenance_checks,
        "must be a provenance object",
    )
    truncated = json.loads(provenance_summary)
    truncated["checks"] = truncated["checks"][:15]
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-02",
        truncated,
        "expected at least 20",
    )
    for case_index, field in enumerate(
        (
            "id",
            "executable",
            "arguments",
            "command",
            "workingDirectory",
            "startedUtc",
            "endedUtc",
            "durationMs",
            "exitCode",
            "outputMode",
            "rawLog",
            "rawLogSha256",
            "helperIdentity",
            "fixture",
            "targets",
            "expectedIdentities",
            "expectedHashes",
            "applicabilityResult",
            "applicabilityReason",
            "expectedDisposition",
            "expectedFailureSignature",
            "finalDisposition",
            "finalValidationResult",
        ),
        start=3,
    ):
        missing_field = json.loads(provenance_summary)
        missing_field["checks"][0].pop(field)
        _assert_provenance_failure(
            f"OPTG-BP3-PROV-FG-{case_index:02d}",
            missing_field,
            f"missing {field}",
        )
    noncontiguous = json.loads(provenance_summary)
    noncontiguous["checks"][-1]["id"] = "22_fixture_check"
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-21",
        noncontiguous,
        "not one contiguous 01-N sequence",
    )
    missing_log = json.loads(provenance_summary)
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-22",
        missing_log,
        "raw log is missing",
        remove_file=missing_log["checks"][0]["rawLog"],
    )
    wrong_hash = json.loads(provenance_summary)
    wrong_hash["checks"][0]["rawLogSha256"] = "0" * 64
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-23",
        wrong_hash,
        "raw log SHA256 does not match",
    )
    missing_digest_row = validation_results_text.replace(validation_result_rows[0], "")
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-24",
        json.loads(provenance_summary),
        "human validation digest omits exact command provenance",
        validation_text=missing_digest_row,
    )
    invalid_timestamp = json.loads(provenance_summary)
    invalid_timestamp["checks"][0]["endedUtc"] = "2026-07-24T23:59:59Z"
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-25",
        invalid_timestamp,
        "invalid start/end timestamps",
    )
    false_pass = json.loads(provenance_summary)
    false_pass["checks"][0]["exitCode"] = 1
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-26",
        false_pass,
        "claims PASS but exitCode is nonzero",
    )

    arbitrary_na = json.loads(provenance_summary)
    arbitrary_na_check = arbitrary_na["checks"][0]
    arbitrary_na_raw = provenance_files[arbitrary_na_check["rawLog"]].replace(
        "Exit Code: 0\n", "Exit Code: 1\n"
    ).replace("01_fixture_check: PASS\n", "RuntimeError: arbitrary unrelated fatal error\n")
    arbitrary_na_check.update(
        {
            "exitCode": 1,
            "mergedOutput": "RuntimeError: arbitrary unrelated fatal error\n",
            "expectedDisposition": "EXPECTED_NOT_APPLICABLE",
            "expectedFailureSignature": "NOT_APPLICABLE",
            "finalDisposition": "NOT_APPLICABLE_CONFIRMED",
            "rawLogSha256": hashlib.sha256(arbitrary_na_raw.encode("utf-8")).hexdigest().upper(),
        }
    )
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-NA-01",
        arbitrary_na,
        "unsupported expected disposition",
        file_updates={arbitrary_na_check["rawLog"]: arbitrary_na_raw},
    )

    traceback_na = json.loads(provenance_summary)
    traceback_check = traceback_na["checks"][0]
    traceback_raw = provenance_files[traceback_check["rawLog"]].replace(
        "01_fixture_check: PASS\n",
        "Traceback (most recent call last):\nRuntimeError: unrelated failure\n",
    )
    traceback_check["mergedOutput"] = (
        "Traceback (most recent call last):\nRuntimeError: unrelated failure\n"
    )
    traceback_check["rawLogSha256"] = hashlib.sha256(
        traceback_raw.encode("utf-8")
    ).hexdigest().upper()
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-NA-02",
        traceback_na,
        "uncontrolled traceback or exception",
        file_updates={traceback_check["rawLog"]: traceback_raw},
    )

    missing_na_reason = json.loads(provenance_summary)
    missing_na_reason["applicability"][0]["applicabilityReason"] = ""
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-NA-03",
        missing_na_reason,
        "missing applicabilityReason",
    )
    applicable_na = json.loads(provenance_summary)
    applicable_na["applicability"][0]["executed"] = True
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-NA-04",
        applicable_na,
        "must be unexecuted",
    )
    wrong_failure_signature = json.loads(provenance_summary)
    wrong_failure_signature["checks"][-1]["expectedFailureSignature"] = "WRONG_SIGNATURE"
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-MAP-01",
        wrong_failure_signature,
        "does not contain the exact expected failure signature",
    )
    missing_final = json.loads(provenance_summary)
    missing_final["checks"][0].pop("finalDisposition")
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-MAP-02",
        missing_final,
        "missing finalDisposition",
    )
    mismatched_final = json.loads(provenance_summary)
    mismatched_final["checks"][0]["finalDisposition"] = "EXPECTED_FAIL_CONFIRMED"
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-MAP-03",
        mismatched_final,
        "expected/final disposition mismatch for PASS",
    )
    zero_expected_failure = json.loads(provenance_summary)
    zero_expected_failure["checks"][-1]["exitCode"] = 0
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-MAP-04",
        zero_expected_failure,
        "must have a nonzero exitCode",
    )
    inconsistent_counts = json.loads(provenance_summary)
    inconsistent_counts["suiteDispositionCounts"]["PASS"] = 20
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-COUNT-01",
        inconsistent_counts,
        "suite disposition counts disagree",
    )
    digest_mismatch = validation_results_text.replace(
        "`01_fixture_check` | py -3 dev/fixture_check_01.py | `PASS`",
        "`01_fixture_check` | py -3 dev/fixture_check_01.py | `FAILED`",
    )
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-DIGEST-01",
        json.loads(provenance_summary),
        "human validation digest disposition disagrees",
        validation_text=digest_mismatch,
    )
    omitted_inventory = json.loads(provenance_summary)
    omitted_inventory["finalSuiteInventory"].pop()
    _assert_provenance_failure(
        "OPTG-BP3-PROV-FG-INVENTORY-01",
        omitted_inventory,
        "finalSuiteInventory omits",
    )

    manifest_path = "Source Truth Context/Proof Artifacts/Validation/PACKET_MANIFEST.json"

    def _assert_active_repair_failure(
        case_id: str,
        manifest_value: dict[str, object],
        expected: str,
        *,
        rollback_text: str | None = None,
        defect_text: str | None = None,
    ) -> None:
        mutated = dict(valid)
        mutated[manifest_path] = json.dumps(manifest_value, indent=2)
        if rollback_text is not None:
            mutated[
                "Review Aids/OPTION_G_EXTERNAL_TRANSACTION_AND_ROLLBACK_LEDGER.md"
            ] = rollback_text
        if defect_text is not None:
            mutated["Review Aids/OPTION_G_BP3_REPAIR_DEFECT_LEDGER.md"] = defect_text
        failures = bundle._fam003_option_g_bp3_orchestration_failures(
            mutated,
            status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
        )
        if not any(expected.casefold() in failure.casefold() for failure in failures):
            raise AssertionError(f"{case_id} did not fail on {expected!r}: {failures}")

    bad_commit_count = json.loads(packet_manifest)
    bad_commit_count["Current Repair Delta"]["commitCount"] = 2
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-01",
        bad_commit_count,
        "commit count disagrees",
    )
    bad_file_count = json.loads(packet_manifest)
    bad_file_count["Current Repair Delta"]["changedFileCount"] = 4
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-02",
        bad_file_count,
        "changed-file count disagrees",
    )
    bad_file_identity = json.loads(packet_manifest)
    bad_file_identity["Current Repair Delta"]["changedFiles"].append("desktop/desktop_renderer.py")
    bad_file_identity["Current Repair Delta"]["changedFileCount"] = 4
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-03",
        bad_file_identity,
        "outside the approved repair set",
    )
    bad_snapshot = json.loads(packet_manifest)
    bad_snapshot["Current Repair Delta"]["snapshotIdentity"] = "snapshot-20990101T000000Z-deadbeef"
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-04",
        bad_snapshot,
        "active rollback ledger disagrees with current snapshotIdentity",
    )
    bad_state = json.loads(packet_manifest)
    bad_state["Current Repair Delta"]["stateVersion"] = 25
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-05",
        bad_state,
        "external-state version disagrees",
    )
    bad_projection = json.loads(packet_manifest)
    first_projection = next(iter(fixture_projection_hashes))
    bad_projection["Current Repair Delta"]["projectionHashes"][first_projection] = "9" * 64
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-06",
        bad_projection,
        "projection hashes disagree",
    )
    bad_receipt = json.loads(packet_manifest)
    bad_receipt["Current Repair Delta"]["transactionReceipt"] = "wrong-receipt.json"
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-07",
        bad_receipt,
        "active rollback ledger disagrees with current transactionReceipt",
    )
    bad_rollback = json.loads(packet_manifest)
    bad_rollback["Current Repair Delta"]["rollbackRoute"] = "unsafe rollback route"
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-08",
        bad_rollback,
        "active rollback ledger disagrees with current rollbackRoute",
    )
    bad_packet = json.loads(packet_manifest)
    bad_packet["Current Repair Delta"]["packetIdentity"] = r"C:\Nexus USER\FAM-003-20990101-000000.zip"
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-09",
        bad_packet,
        "packet identity disagrees",
    )
    _assert_active_repair_failure(
        "OPTG-BP3-ROLLBACK-FG-10",
        json.loads(packet_manifest),
        "stale active rollback evidence",
        rollback_text=active_rollback_ledger.replace(
            "## Historical / Superseded Evidence", "## Unlabeled Prior Notes"
        ),
    )
    historical_failures = bundle._fam003_option_g_active_repair_evidence_failures(valid)
    if historical_failures:
        raise AssertionError(
            "OPTG-BP3-ROLLBACK-POS-01 rejected clearly labeled historical evidence: "
            f"{historical_failures}"
        )

    if bundle._byte_exact_projection_copy_failures(
        "current_external_branch_plan.md",
        b"line\r\n",
        b"line\r\n",
        "live-branch-plan",
    ):
        raise AssertionError("Byte-exact projection copy positive fixture failed")
    projection_failures = bundle._byte_exact_projection_copy_failures(
        "current_external_branch_plan.md",
        b"line\n",
        b"line\r\n",
        "live-branch-plan",
    )
    if not any("not byte-exact" in failure for failure in projection_failures):
        raise AssertionError(
            "OPTG-BP3-PROJ-FG-01 did not reject LF-normalized projection copy"
        )
    projection_failures = bundle._byte_exact_projection_copy_failures(
        "current_external_branch_plan.md",
        None,
        b"line\r\n",
        "live-branch-plan",
    )
    if not any("proof is missing" in failure for failure in projection_failures):
        raise AssertionError(
            "OPTG-BP3-PROJ-FG-02 did not reject missing projection bytes"
        )

    current_decision = bundle.FAM003_OPTION_G_BP3_CURRENT_DECISION
    future_decision = bundle.FAM003_OPTION_G_FUTURE_WORKSTREAM_DECISION
    decision_surface_cases = (
        (
            "OPTG-BP3-DS-FG-01",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    current_decision,
                    "Accept, waive, revise, or block the Option G BP3 packet.",
                    1,
                ),
            ),
            {},
            "exact packet-contained current BP3 decision",
        ),
        (
            "OPTG-BP3-DS-FG-02",
            tuple(
                (file_name, current_decision, "", 1)
                for file_name in (
                    "START_HERE.md",
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Review Aids/USER_DECISIONS.md",
                )
            ),
            {"Review Aids/CODEX_CHAT_RETURN.md": current_decision},
            "exact packet-contained current BP3 decision",
        ),
        (
            "OPTG-BP3-DS-FG-03",
            (
                (
                    "Review Aids/USER_DECISIONS.md",
                    "I approve the repaired FAM-003",
                    "I revise the repaired FAM-003",
                    1,
                ),
            ),
            {},
            "exact packet-contained current BP3 decision",
        ),
        (
            "OPTG-BP3-DS-FG-04",
            (
                (
                    "START_HERE.md",
                    "I approve the repaired FAM-003",
                    "I approve implementation for the repaired FAM-003",
                    1,
                ),
            ),
            {},
            "exact packet-contained current BP3 decision",
        ),
        (
            "OPTG-BP3-DS-FG-05",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "USER Review Packet Finding:",
                    "Packet Finding:",
                    1,
                ),
            ),
            {},
            "required closed-loop USER Review Packet Finding marker",
        ),
        (
            "OPTG-BP3-DS-FG-06",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "USER Review Response:",
                    "Response:",
                    1,
                ),
            ),
            {},
            "required closed-loop USER Review Response marker",
        ),
        (
            "OPTG-BP3-DS-FG-07",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Codex Response Digest:",
                    "Digest:",
                    1,
                ),
            ),
            {},
            "required closed-loop Codex Response Digest marker",
        ),
        (
            "OPTG-BP3-DS-FG-08",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "USER Review Response: Pending USER Review",
                    "USER Review Response: USER Accepted",
                    1,
                ),
            ),
            {},
            "pre-response USER Review Response",
        ),
        (
            "OPTG-BP3-DS-FG-09",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "USER Gate State: Pending USER Review",
                    "USER Gate State: USER Approved",
                    1,
                ),
            ),
            {},
            "retain USER Gate State Pending USER Review",
        ),
        (
            "OPTG-BP3-DS-FG-10",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "External Archive Receipt: `Recorded in the post-generation "
                    "Codex return and FAM-003 external packet receipt outside this "
                    "hashed archive.`\n",
                    "",
                    1,
                ),
            ),
            {},
            "Finding lacks external archive receipt model",
        ),
        (
            "OPTG-BP3-DS-FG-11",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Codex Response Digest: Pending USER Response - no BP3 approval "
                    "recorded; Workstream implementation remains unapproved.",
                    "Codex Response Digest: BP3 accepted and Workstream implementation ready.",
                    1,
                ),
            ),
            {},
            "Codex Response Digest must state",
        ),
        (
            "OPTG-BP3-DS-FG-12",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    future_decision,
                    "Future Workstream approval text will be supplied later.",
                    1,
                ),
            ),
            {},
            "exact future-only Workstream approval text",
        ),
        (
            "OPTG-BP3-DS-FG-13",
            (
                (
                    "Review Aids/USER_DECISIONS.md",
                    "Future decision only - not requested, granted, or actionable at the "
                    "current BP3 gate",
                    "Current actionable Workstream decision",
                    1,
                ),
            ),
            {},
            "future-only and non-actionable",
        ),
        (
            "OPTG-BP3-DS-FG-14",
            tuple(
                (
                    file_name,
                    "`OPTG-WS01` through `OPTG-WS07`",
                    "`OPTG-WS01` through `OPTG-WS06`",
                    0,
                )
                for file_name in (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Review Aids/USER_DECISIONS.md",
                )
            ),
            {},
            "future Workstream decision omits seven seams",
        ),
        (
            "OPTG-BP3-DS-FG-15",
            tuple(
                (
                    file_name,
                    "`F3-OPTG-D01`",
                    "`F3-OPTG-DXX`",
                    0,
                )
                for file_name in (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Review Aids/USER_DECISIONS.md",
                )
            ),
            {},
            "future Workstream decision omits dependency F3-OPTG-D01",
        ),
        (
            "OPTG-BP3-DS-FG-16",
            tuple(
                (
                    file_name,
                    "`OPTG-ALLOW-01` through `OPTG-ALLOW-08`",
                    "`OPTG-ALLOW-01` through `OPTG-ALLOW-09`",
                    0,
                )
                for file_name in (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Review Aids/USER_DECISIONS.md",
                )
            ),
            {},
            "future Workstream decision omits eight-region allowlist",
        ),
        (
            "OPTG-BP3-DS-FG-17",
            tuple(
                (
                    file_name,
                    "Any unknown path, resource, object, owner, FAM-006/shared-owner "
                    "ambiguity",
                    "Any unknown path, resource, object, owner may self-admit; "
                    "FAM-006/shared-owner ambiguity",
                    1,
                )
                for file_name in (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Review Aids/USER_DECISIONS.md",
                )
            ),
            {},
            "permits unknown paths/resources/objects/owners",
        ),
        (
            "OPTG-BP3-DS-FG-18",
            tuple(
                (
                    file_name,
                    "Recording Studio stays non-resizable and its Start / Pause / Stop "
                    "controls, geometry, lifecycle, and visuals remain unchanged.",
                    "",
                    1,
                )
                for file_name in (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Review Aids/USER_DECISIONS.md",
                )
            ),
            {},
            "future Workstream decision omits Recording non-resizable",
        ),
        (
            "OPTG-BP3-DS-FG-19",
            (
                (
                    "Review Aids/USER_DECISIONS.md",
                    future_decision,
                    future_decision
                    + " FAM-006, ORIN Core, renderer, generic WebEngine, and "
                    "AI-lifetime scope are admitted.",
                    1,
                ),
            ),
            {},
            "admits excluded FAM-006",
        ),
        (
            "OPTG-BP3-DS-FG-20",
            (
                (
                    "Review Aids/USER_DECISIONS.md",
                    future_decision,
                    future_decision
                    + " H1, Live Validation, and UTS are authorized.",
                    1,
                ),
            ),
            {},
            "authorizes H1, Live Validation, or UTS",
        ),
        (
            "OPTG-BP3-DS-FG-21",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    current_decision,
                    current_decision + " I approve Workstream implementation now.",
                    1,
                ),
            ),
            {},
            "BP3 approval and Workstream implementation approval are combined",
        ),
        (
            "OPTG-BP3-DS-FG-22",
            (
                (
                    "Review Aids/USER_DECISIONS.md",
                    future_decision,
                    "Future Workstream approval text withheld by governed exception.",
                    1,
                ),
            ),
            {},
            "governed exception to withholding future Workstream approval text lacks",
        ),
        (
            "OPTG-BP3-DS-FG-23",
            (
                (
                    "Review Aids/USER_DECISIONS.md",
                    current_decision,
                    "Accept, waive, revise, or block.",
                    1,
                ),
            ),
            {},
            "exact packet-contained current BP3 decision",
        ),
        (
            "OPTG-BP3-DS-FG-24",
            (
                (
                    "Source Truth Context/current_external_branch_plan.md",
                    "Transition Status: "
                    "`OPTION_G_BP3_FALSE_GREEN_PREVENTION_REPAIRED_READY_FOR_USER_REVIEW`",
                    "Transition Status: `REPAIR_REQUIRED`",
                    1,
                ),
            ),
            {},
            "active external state still says BP3 repair is required",
        ),
        (
            "OPTG-BP3-DS-FG-25",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "USER Review Response: Pending USER Review",
                    "USER Review Response: Pending USER Review\n"
                    "USER Review Response: Pending USER Review",
                    1,
                ),
            ),
            {},
            "required closed-loop USER Review Response marker must appear exactly once",
        ),
        (
            "OPTG-BP3-DS-FG-26",
            (
                (
                    "Review Aids/OPTION_G_BP3_REPAIR_DEFECT_LEDGER.md",
                    "`OPTG-BP3-DS-DEF-07`",
                    "`OPTG-BP3-DS-DEF-07`\n`OPTG-BP3-DS-DEF-07`",
                    1,
                ),
            ),
            {},
            "decision-surface defect row OPTG-BP3-DS-DEF-07 must appear exactly once",
        ),
        (
            "OPTG-BP3-DS-FG-27",
            tuple(
                (
                    file_name,
                    "I approve the repaired FAM-003",
                    "I accept the repaired FAM-003",
                    1,
                )
                for file_name in (
                    "START_HERE.md",
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Review Aids/USER_DECISIONS.md",
                )
            ),
            {},
            "uses accept where exact approve vocabulary is required",
        ),
        (
            "OPTG-BP3-DS-FG-28",
            (
                (
                    "Review Aids/USER_DECISIONS.md",
                    "I approve the repaired FAM-003",
                    "I accept the repaired FAM-003",
                    1,
                ),
            ),
            {},
            "uses accept where exact approve vocabulary is required",
        ),
        (
            "OPTG-BP3-DS-FG-29",
            tuple(
                (
                    file_name,
                    bundle.FAM003_OPTION_G_BP3_DECISION_EFFECT,
                    bundle.FAM003_OPTION_G_BP3_DECISION_EFFECT.replace(
                        "USER Approved", "USER Accepted"
                    ),
                    1,
                )
                for file_name in (
                    "START_HERE.md",
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "Review Aids/USER_DECISIONS.md",
                )
            ),
            {},
            "future USER Approved state mapping is missing",
        ),
        (
            "OPTG-BP3-DS-FG-30",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    current_decision,
                    current_decision + " I approve Workstream implementation now.",
                    1,
                ),
            ),
            {},
            "BP3 approval and Workstream implementation approval are combined",
        ),
        (
            "OPTG-BP3-DS-FG-31",
            (
                (
                    "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
                    "USER Gate State: Pending USER Review",
                    "USER Gate State: USER Approved",
                    1,
                ),
            ),
            {},
            "packet claims BP3 is already USER Approved",
        ),
    )
    for case_id, mutations, additions, expected in decision_surface_cases:
        mutated = dict(valid)
        for file_name, old, new, count in mutations:
            if count == 0:
                mutated[file_name] = mutated[file_name].replace(old, new)
            else:
                mutated[file_name] = mutated[file_name].replace(old, new, count)
        mutated.update(additions)
        failures = bundle._fam003_option_g_bp3_orchestration_failures(
            mutated,
            status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
        )
        if not any(expected.casefold() in failure.casefold() for failure in failures):
            raise AssertionError(
                f"{case_id} did not fail on {expected!r}: {failures}"
            )

    r2_failures = bundle._fam003_bp3_r2_orchestration_consistency_failures(
        valid,
        status=bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
    )
    if r2_failures:
        raise AssertionError(
            "Option G BP3 incorrectly triggered the historical R2-only guard:\n"
            + "\n".join(r2_failures)
        )


def main() -> int:
    _assert_fam003_option_g_bp2_planning_guards()
    _assert_fam003_option_g_bp3_orchestration_guards()
    _assert_migrated_live_header_ignores_historical_receipt_metadata()
    _assert_source_context_text_normalization()
    _assert_origin_main_fallback()
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
    print(
        "False-green fixture validation: PASS "
        "(Option G BP3: 22 proof-carrydown + 31 decision-surface + "
        "38 canonical-UFD + 12 Element-to-Phase + 45 provenance + "
        "10 active-rollback negatives + 1 labeled-history positive + "
        "2 byte-exact projection cases)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
