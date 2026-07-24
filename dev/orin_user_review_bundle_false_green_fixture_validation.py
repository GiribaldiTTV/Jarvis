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
        "\n## Current Actionable Decision - BP3 Acceptance Only\n\n"
        f"{bundle.FAM003_OPTION_G_BP3_CURRENT_DECISION}\n"
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
        "Codex Response Digest: Pending USER Response - no BP3 acceptance recorded; "
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
        "`OPTION_G_BP3_DECISION_SURFACE_REPAIRED_READY_FOR_USER_REVIEW`\n"
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
            "Owner Class: `Branch Record`\n"
            "Canonical Owner File: `Docs/branch_records/feature_fam_003_settings_resize_proof.md`\n"
            "Workstream Severity: `Level 2 seam-blocking`\n"
            "Status: `Closed`\n"
            "Fold-Down Target: `Branch record`\n"
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
            "Remaining USER Decision: `BP3 acceptance only`\n"
        )
    ufd_text = (
        "# Option G UFD And Fold-Down\n"
        "USER Feedback Disposition Required: `Yes`\n"
        "UFD Ledger Status: `Complete`\n"
        "UFD Ledger Owner: `C:\\Nexus Governance State\\branches\\"
        "feature_fam_003_settings_resize_proof\\branch_plan.md`\n"
        "Open UFD Count: `0`\n"
        "Blocking UFD Count: `0`\n"
        "Fold-Down Status: `Pending`\n"
        "Deferred / Future-Gated Scope Admission: `NONE`\n\n"
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
        "# Element-to-Phase Proof Matrix\n"
        "Element-to-Phase Proof Matrix Status: `COMPLETE`\n"
        + "\n".join(
            f"| `OPTG-ELEM-{index:02d}` | element {index} | Workstream proof | "
            "H1 proof | Live Validation proof | UTS proof |"
            for index in range(1, 12)
        )
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
    valid = {
        "START_HERE.md": (
            "# FAM-003 Option G BP3\n"
            "Branch: `feature/fam-003-settings-resize-proof`\n"
            "Primary USER Review File: `USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`\n"
            "Current Gate: `BP3 Workstream Entry / Orchestration Validation USER review "
            "pending; Workstream implementation remains blocked`\n"
            "Current Actionable Decision: `BP3 acceptance only`\n\n"
            f"{bundle.FAM003_OPTION_G_BP3_CURRENT_DECISION}\n"
        ),
        "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md": primary,
        "Review Aids/USER_DECISIONS.md": (
            "# USER Decisions\n\n"
            "## Current Actionable Decision - BP3 Acceptance Only\n\n"
            f"{bundle.FAM003_OPTION_G_BP3_CURRENT_DECISION}\n\n"
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
        "Source Truth Context/Proof Artifacts/Validation/PACKET_MANIFEST.json": (
            '{"currentActionableDecision": "BP3 acceptance only", '
            '"futureWorkstreamDecision": "FUTURE_ONLY_NON_ACTIONABLE", '
            '"userGateState": "Pending USER Review", '
            '"workstreamImplementation": "UNAPPROVED"}\n'
        ),
        "Source Truth Context/Proof Artifacts/Validation/VALIDATION_RESULTS.md": (
            "BP3 Decision Surface Validation: `PASS`\n"
            "USER Review Response: `Pending USER Review`\n"
            "Workstream Implementation: `UNAPPROVED`\n"
            "Future Workstream Decision: `FUTURE_ONLY_NON_ACTIONABLE`\n"
        ),
        "Source Truth Context/current_external_branch_plan.md": active_header,
        "Source Truth Context/current_external_branch_state.md": active_header,
        "Source Truth Context/current_external_worktree_state.md": active_header,
    }
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
            "at least eleven",
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
                    "I accept the repaired FAM-003",
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
                    "I accept the repaired FAM-003",
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
                    "Codex Response Digest: Pending USER Response - no BP3 acceptance "
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
            "BP3 acceptance and Workstream implementation approval are combined",
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
                    "`OPTION_G_BP3_DECISION_SURFACE_REPAIRED_READY_FOR_USER_REVIEW`",
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
        "(Option G BP3: 22 proof-carrydown + 26 decision-surface cases)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
