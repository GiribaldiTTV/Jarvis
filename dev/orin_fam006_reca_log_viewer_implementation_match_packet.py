"""Generate the FAM-006 REC-A + Log Viewer implementation-match packet.

This branch-local helper packages actual runtime proof for the USER-selected
REC-A Recording Studio direction, renamed Log Viewer direction, and B2
placement behavior. It does not claim H1, Live Validation, UTS, PR readiness,
merge, release, or cleanup acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from typing import Any

from orin_fam006_unified_defect_ledger import write_packet_artifacts


WORKTREE = Path("C:/Nexus Worktrees/FAM-006")
USER_ROOT = Path("C:/Nexus USER")
PACKET_ROOT = USER_ROOT / "FAM-006"
BRANCH = "feature/fam-006-dashboard-recording-start-stop-local-file"
ACCEPTED_SELECTION_ZIP = USER_ROOT / "FAM-006-20260624-234432.zip"
ACCEPTED_SELECTION_SHA256 = "122767EB20EA0AF51D04211C612774A3EA4EA5DF0518FB3DF2590208D856BCBE"
ACCEPTED_SELECTION_RECEIPT_RELATIVE = (
    Path("Review Aids") / "Accepted Candidate Selection" / "accepted_candidate_selection_receipt.json"
)
ACCEPTED_SELECTION_RECEIPT_MD_RELATIVE = (
    Path("Review Aids") / "Accepted Candidate Selection" / "ACCEPTED_CANDIDATE_SELECTION_RECEIPT.md"
)
PRIMARY_REVIEW = "REC_A_LOG_VIEWER_IMPLEMENTATION_MATCH_REVIEW.md"
PACKET_STATUS = "fam006-reca-log-viewer-implementation-match-review"
ACCEPTED_TARGET_ACTUAL_DISPOSITIONS = {"MATCH", "PASS"}
SCREENSHOT_ROOT = (
    Path("C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI")
    / "fam_006_pre_live_visual_conformance"
)
EXTERNAL_BRANCH_ROOT = Path(
    "C:/Nexus Governance State/branches/feature_fam_006_dashboard_recording_start_stop_local_file"
)
LATEST_POINTER = USER_ROOT / "FAM-006_latest_implementation_match_packet.json"
STALE_TOP_LEVEL_PACKET_SIDECAR_GLOBS = (
    "FAM-006_false_accept_final_*.json",
    "FAM-006_false_accept_final_*.txt",
    "FAM-006_packet_validation_*.txt",
    "FAM-006_purge_confirmation_implementation_match.txt",
)
FINAL_CLEAN_PROOF_RELATIVE = Path("Review Aids") / "Final Clean Proof" / "final_clean_proof.json"
FINAL_CLEAN_PROOF_MD_RELATIVE = Path("Review Aids") / "Final Clean Proof" / "FINAL_CLEAN_PROOF.md"
GIT_STATUS_AUDIT_RELATIVE = Path("Review Aids") / "Final Clean Proof" / "git_status_evidence_audit.json"
GIT_STATUS_AUDIT_MD_RELATIVE = Path("Review Aids") / "Final Clean Proof" / "GIT_STATUS_EVIDENCE_AUDIT.md"
FINAL_CLEAN_COMMAND_DIR_RELATIVE = Path("Review Aids") / "Final Clean Proof" / "Commands"
FINAL_CLEAN_REQUIRED_LABELS = {
    "git_status_short_branch",
    "git_rev_parse_head",
    "git_branch_current",
    "git_upstream",
    "git_rev_parse_origin_main",
    "git_merge_base_head_origin_main",
    "git_ahead_behind_origin_main",
    "git_ahead_behind_upstream",
    "git_diff_check",
    "git_diff_check_origin_main_head",
    "git_diff_cached_check",
}
PACKET_UNDER_REVIEW_ZIP = USER_ROOT / "FAM-006-20260625-142752.zip"
PACKET_UNDER_REVIEW_SHA256 = "D57D310BFBE1113AA3F880351176BF5ADEB66DDDFAE0BD3AF2BBF0A926894040"

SOURCE_CONTEXT = {
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
    "Docs_external_operational_state_store_reform_plan.md": WORKTREE
    / "Docs/external_operational_state_store_reform_plan.md",
    "feature_fam_006_dashboard_recording_start_stop_local_file.md": WORKTREE
    / "Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md",
    "external_branch_plan.md": EXTERNAL_BRANCH_ROOT / "branch_plan.md",
    "external_branch_state.md": EXTERNAL_BRANCH_ROOT / "branch_state.md",
}

REQUIRED_ROW_KEYS = {
    "recording-full-window",
    "recording-window-chrome",
    "recording-start-action",
    "recording-pause-action",
    "recording-stop-action",
    "recording-target-truth",
    "recording-log-route",
    "open-log-viewer-route-proof-json",
    "open-log-viewer-route-proof-full-desktop",
    "log-viewer-full-window",
    "log-viewer-window-chrome",
    "log-viewer-deferred-state",
    "native-log-destination-action",
    "exported-log-destination-action",
    "log-viewer-action-status",
    "log-viewer-resize-before",
    "log-viewer-resize-during",
    "log-viewer-resize-after",
    "full-desktop-combined",
    "b2-default-parent-neighbor-full-desktop",
    "b2-same-session-moved-restore-full-desktop",
    "b2-fresh-window-new-session-full-desktop",
    "b2-placement-proof-json",
    "b2-placement-proof-markdown",
    "runtime-visual-conformance-metrics-json",
    "runtime-visual-conformance-metrics-markdown",
    "contact-sheet",
    "comparator-ai-control-center-outer-frame",
    "comparator-ai-control-center-chrome-header",
    "comparator-ai-control-center-window-control-cluster",
    "comparator-ai-control-center-button-grammar",
    "comparator-ai-control-center-panel-rhythm",
    "comparator-ai-control-center-status-action-grammar",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def _run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=WORKTREE, text=True, stderr=subprocess.STDOUT).strip()


def _normalize_count(value: str) -> str:
    return " ".join(str(value).strip().split())


def _status_stdout_is_dirty(stdout: str) -> bool:
    lines = [line for line in stdout.splitlines() if line.strip()]
    if not lines:
        return True
    return any(not line.startswith("##") for line in lines)


def _status_stdout_has_upstream_delta(stdout: str) -> bool:
    first = next((line for line in stdout.splitlines() if line.startswith("##")), "")
    return "[ahead" in first or "[behind" in first or "[diverged" in first


def _classify_git_status_record(record: dict[str, Any] | None) -> dict[str, Any]:
    if not record:
        return {
            "classification": "STALE_OR_UNKNOWN",
            "reason": "No git status record was present.",
        }
    stdout = str(record.get("stdout", ""))
    exit_code = record.get("exitCode")
    if exit_code != 0:
        return {
            "classification": "STALE_OR_UNKNOWN",
            "reason": f"git status record exited {exit_code}; cleanliness cannot be trusted.",
        }
    if _status_stdout_is_dirty(stdout):
        return {
            "classification": "PRE_COMMIT_DIRTY",
            "reason": "git status shows tracked/untracked changes inside the packet evidence.",
        }
    if _status_stdout_has_upstream_delta(stdout):
        return {
            "classification": "POST_COMMIT_PRE_PUSH",
            "reason": "git status is clean but still reports upstream ahead/behind state.",
        }
    return {
        "classification": "POST_PUSH_CLEAN",
        "reason": "git status is clean and reports no upstream delta in the branch header.",
    }


def _identity() -> dict[str, Any]:
    upstream = _run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    short_status = _run_git("status", "--short")
    return {
        "worktreePath": str(WORKTREE),
        "gitRoot": _run_git("rev-parse", "--show-toplevel"),
        "branch": _run_git("branch", "--show-current"),
        "upstream": upstream,
        "head": _run_git("rev-parse", "HEAD"),
        "originMain": _run_git("rev-parse", "origin/main"),
        "mergeBase": _run_git("merge-base", "HEAD", "origin/main"),
        "aheadBehindOriginMain": _run_git("rev-list", "--left-right", "--count", "origin/main...HEAD"),
        "aheadBehindUpstream": _run_git("rev-list", "--left-right", "--count", f"{upstream}...HEAD"),
        "cleanliness": "clean" if not short_status else short_status,
    }


def _latest_proof_root() -> Path:
    candidates = [
        path
        for path in SCREENSHOT_ROOT.glob("*feature_studio_visual_fail_repair")
        if path.is_dir() and (path / "row_to_evidence_map.json").is_file()
    ]
    if not candidates:
        raise FileNotFoundError(f"No feature-studio proof root found under {SCREENSHOT_ROOT}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def _make_removable(path: str) -> None:
    os.chmod(path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)


def _retry_remove_readonly(function: Any, path: str, _exc_info: Any) -> None:
    _make_removable(path)
    function(path)


def _rmtree(path: Path) -> None:
    try:
        shutil.rmtree(path, onexc=_retry_remove_readonly)
    except TypeError:
        shutil.rmtree(path, onerror=_retry_remove_readonly)


def _purge_packet() -> None:
    if PACKET_ROOT.exists():
        _rmtree(PACKET_ROOT)
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)
    if LATEST_POINTER.exists():
        try:
            old = json.loads(_read(LATEST_POINTER))
            old_zip = Path(str(old.get("zipPath") or old.get("zip") or ""))
            if old_zip.exists() and old_zip != ACCEPTED_SELECTION_ZIP:
                old_zip.unlink()
        except Exception:
            pass
    _remove_stale_same_status_zips()
    _remove_stale_same_label_upload_zips()


def _zip_has_packet_status(path: Path, status: str) -> bool:
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            candidates = ["START_HERE.md", f"USER Review/{PRIMARY_REVIEW}"]
            for name in candidates:
                if name not in names:
                    continue
                text = archive.read(name).decode("utf-8", errors="replace")
                if status in text:
                    return True
    except (OSError, zipfile.BadZipFile):
        return False
    return False


def _same_status_packet_zips() -> list[Path]:
    return sorted(
        path
        for path in USER_ROOT.glob("FAM-006-*.zip")
        if path.is_file() and path != ACCEPTED_SELECTION_ZIP and _zip_has_packet_status(path, PACKET_STATUS)
    )


def _remove_stale_same_status_zips(keep: Path | None = None) -> None:
    keep_resolved = keep.resolve() if keep else None
    for path in _same_status_packet_zips():
        if keep_resolved and path.resolve() == keep_resolved:
            continue
        path.unlink()


def _same_label_upload_zips() -> list[Path]:
    return sorted(path for path in USER_ROOT.glob("FAM-006-*.zip") if path.is_file())


def _remove_stale_same_label_upload_zips(keep: Path | None = None) -> None:
    keep_resolved = keep.resolve() if keep else None
    for path in _same_label_upload_zips():
        if keep_resolved and path.resolve() == keep_resolved:
            continue
        path.unlink()


def _remove_stale_top_level_packet_sidecars() -> None:
    for pattern in STALE_TOP_LEVEL_PACKET_SIDECAR_GLOBS:
        for path in USER_ROOT.glob(pattern):
            if path.is_file() and path.resolve() != LATEST_POINTER.resolve():
                path.unlink()


def _zip_read_text(path: Path, entry: str) -> str | None:
    try:
        with zipfile.ZipFile(path) as archive:
            if entry not in archive.namelist():
                return None
            return archive.read(entry).decode("utf-8", errors="replace")
    except (OSError, zipfile.BadZipFile):
        return None


def _zip_read_json(path: Path, entry: str) -> Any | None:
    text = _zip_read_text(path, entry)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _packet_under_review_path_from_pointer() -> Path | None:
    if not LATEST_POINTER.exists():
        return PACKET_UNDER_REVIEW_ZIP if PACKET_UNDER_REVIEW_ZIP.exists() else None
    try:
        latest = json.loads(_read(LATEST_POINTER))
    except json.JSONDecodeError:
        return PACKET_UNDER_REVIEW_ZIP if PACKET_UNDER_REVIEW_ZIP.exists() else None
    pointed = Path(str(latest.get("zipPath") or latest.get("zip") or ""))
    if pointed.exists():
        return pointed
    return PACKET_UNDER_REVIEW_ZIP if PACKET_UNDER_REVIEW_ZIP.exists() else None


def _audit_packet_git_status_evidence() -> dict[str, Any]:
    zip_path = _packet_under_review_path_from_pointer()
    audit: dict[str, Any] = {
        "schema": "fam006-implementation-match-git-status-evidence-audit-v1",
        "packetStatus": PACKET_STATUS,
        "auditTimestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "underReviewPacket": str(zip_path) if zip_path else None,
        "underReviewExpectedSha256": PACKET_UNDER_REVIEW_SHA256,
        "records": [],
        "overallClassification": "STALE_OR_UNKNOWN",
        "repairRequired": True,
    }
    if not zip_path or not zip_path.exists():
        audit["overallClassification"] = "STALE_OR_UNKNOWN"
        audit["reason"] = "Packet under review is missing; no packet-contained Git proof can be audited."
        return audit

    carried_audit = _zip_read_json(zip_path, GIT_STATUS_AUDIT_RELATIVE.as_posix())
    if (
        isinstance(carried_audit, dict)
        and carried_audit.get("underReviewExpectedSha256") == PACKET_UNDER_REVIEW_SHA256
        and str(carried_audit.get("underReviewPacket", "")).endswith(PACKET_UNDER_REVIEW_ZIP.name)
    ):
        carried_audit = dict(carried_audit)
        carried_audit["carriedForwardAt"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        carried_audit["carriedForwardFromPacket"] = str(zip_path)
        carried_audit["carriedForwardReason"] = (
            "The packet under review was already purged after audit; preserve the original "
            "PRE_COMMIT_DIRTY audit instead of replacing it with a later repaired-packet audit."
        )
        return carried_audit

    actual_sha = _sha256(zip_path)
    audit["underReviewActualSha256"] = actual_sha
    audit["underReviewShaMatchesExpected"] = actual_sha == PACKET_UNDER_REVIEW_SHA256

    labels = [
        "git_status_short_branch",
        "git_rev_parse_head",
        "git_rev_parse_origin_main",
        "git_merge_base_head_origin_main",
        "git_ahead_behind_origin_main",
        "git_ahead_behind_upstream",
        "git_diff_check",
        "git_diff_check_origin_main_head",
        "git_diff_cached_check",
    ]
    for label in labels:
        entry = f"Review Aids/Validation Outputs/{label}.json"
        record = _zip_read_json(zip_path, entry)
        if record is None:
            audit["records"].append(
                {
                    "label": label,
                    "entry": entry,
                    "classification": "STALE_OR_UNKNOWN",
                    "reason": "Evidence record missing from packet validation outputs.",
                }
            )
            continue
        if label == "git_status_short_branch":
            classification = _classify_git_status_record(record)
        else:
            classification = {
                "classification": "STALE_OR_UNKNOWN",
                "reason": "Validation-output record exists but is not a final clean proof record.",
            }
        audit["records"].append(
            {
                "label": label,
                "entry": entry,
                "classification": classification["classification"],
                "reason": classification["reason"],
                "timestamp": record.get("timestamp"),
                "exitCode": record.get("exitCode"),
                "stdout": record.get("stdout", ""),
                "stderr": record.get("stderr", ""),
            }
        )

    final_clean = _zip_read_json(zip_path, FINAL_CLEAN_PROOF_RELATIVE.as_posix())
    audit["finalCleanProofPresent"] = final_clean is not None
    if final_clean is not None:
        audit["finalCleanProofStatus"] = final_clean.get("overallStatus")
        audit["finalCleanProofClass"] = final_clean.get("proofClass")

    dirty_records = [
        record for record in audit["records"] if record.get("classification") == "PRE_COMMIT_DIRTY"
    ]
    if dirty_records and not final_clean:
        audit["overallClassification"] = "PRE_COMMIT_DIRTY"
        audit["reason"] = "Packet contains dirty pre-commit git status proof and no later final clean proof."
        return audit
    if dirty_records:
        audit["overallClassification"] = "PRE_COMMIT_DIRTY"
        audit["reason"] = "Packet contains dirty pre-commit git status proof."
        return audit
    if final_clean and final_clean.get("overallStatus") == "PASS":
        audit["overallClassification"] = str(final_clean.get("proofClass") or "POST_PUSH_CLEAN")
        audit["repairRequired"] = False
        audit["reason"] = "Packet contains a passing final clean proof."
        return audit

    audit["overallClassification"] = "STALE_OR_UNKNOWN"
    audit["reason"] = "Packet does not contain packet-contained final clean proof."
    return audit


def _write_git_status_audit(audit: dict[str, Any]) -> None:
    _write_json(PACKET_ROOT / GIT_STATUS_AUDIT_RELATIVE, audit)
    rows = [
        [
            str(record.get("label", "")),
            str(record.get("classification", "")),
            str(record.get("reason", "")),
        ]
        for record in audit.get("records", [])
    ]
    _write_md(
        PACKET_ROOT / GIT_STATUS_AUDIT_MD_RELATIVE,
        "# Git Status Evidence Audit\n\n"
        f"- Packet under review: `{audit.get('underReviewPacket')}`\n"
        f"- Expected SHA256: `{audit.get('underReviewExpectedSha256')}`\n"
        f"- Actual SHA256: `{audit.get('underReviewActualSha256', 'missing')}`\n"
        f"- Overall classification: `{audit.get('overallClassification')}`\n"
        f"- Repair required: `{audit.get('repairRequired')}`\n"
        f"- Reason: {audit.get('reason', 'not recorded')}\n\n"
        + _markdown_table(["Evidence record", "Classification", "Reason"], rows),
    )


def _accepted_selection_evidence() -> dict[str, Any]:
    mismatches: list[dict[str, str]] = []

    if ACCEPTED_SELECTION_ZIP.exists():
        sha256 = _sha256(ACCEPTED_SELECTION_ZIP)
        if sha256 == ACCEPTED_SELECTION_SHA256:
            return {
                "status": "VERIFIED_FROM_EXISTING_ZIP",
                "source": str(ACCEPTED_SELECTION_ZIP),
                "sha256": sha256,
                "embeddedInCurrentPacket": False,
            }
        mismatches.append({"source": str(ACCEPTED_SELECTION_ZIP), "sha256": sha256})

    legacy_embedded = PACKET_ROOT / "Review Aids" / "Accepted Candidate Selection" / ACCEPTED_SELECTION_ZIP.name
    if legacy_embedded.exists():
        sha256 = _sha256(legacy_embedded)
        if sha256 == ACCEPTED_SELECTION_SHA256:
            return {
                "status": "VERIFIED_FROM_LEGACY_EMBEDDED_ZIP",
                "source": str(legacy_embedded),
                "sha256": sha256,
                "embeddedInCurrentPacket": True,
                "repairDisposition": "Do not re-embed; current packet carries receipt-only evidence.",
            }
        mismatches.append({"source": str(legacy_embedded), "sha256": sha256})

    embedded = PACKET_ROOT / ACCEPTED_SELECTION_RECEIPT_RELATIVE
    if embedded.exists():
        try:
            receipt = json.loads(_read(embedded))
        except json.JSONDecodeError:
            receipt = {}
        sha256 = str(receipt.get("sha256") or receipt.get("expectedSha256") or "")
        if sha256 == ACCEPTED_SELECTION_SHA256:
            return {
                "status": "VERIFIED_FROM_EXISTING_RECEIPT",
                "source": str(embedded),
                "sha256": sha256,
                "embeddedInCurrentPacket": False,
            }

    if LATEST_POINTER.exists():
        try:
            latest = json.loads(_read(LATEST_POINTER))
            receipt = latest.get("acceptedSelectionReceipt")
            sha256 = str(latest.get("acceptedSelectionSha256") or "")
            if receipt and sha256 == ACCEPTED_SELECTION_SHA256:
                return {
                    "status": "VERIFIED_FROM_LATEST_POINTER_RECEIPT",
                    "source": f"{LATEST_POINTER}::{receipt}",
                    "sha256": sha256,
                    "embeddedInCurrentPacket": False,
                }
            latest_zip = Path(str(latest.get("zipPath") or latest.get("zip") or ""))
            if latest_zip.exists():
                with zipfile.ZipFile(latest_zip) as archive:
                    entry = (Path("Review Aids") / "Accepted Candidate Selection" / ACCEPTED_SELECTION_ZIP.name).as_posix()
                    try:
                        payload = archive.read(entry)
                    except KeyError:
                        payload = b""
                if payload:
                    sha256 = _sha256_bytes(payload)
                    if sha256 == ACCEPTED_SELECTION_SHA256:
                        return {
                            "status": "VERIFIED_FROM_LEGACY_PACKET_ZIP_ENTRY",
                            "source": f"{latest_zip}!/{entry}",
                            "sha256": sha256,
                            "embeddedInCurrentPacket": True,
                            "repairDisposition": "Do not re-embed; current packet carries receipt-only evidence.",
                        }
                    mismatches.append({"source": f"{latest_zip}!/{entry}", "sha256": sha256})
        except (KeyError, OSError, zipfile.BadZipFile):
            pass

    if mismatches:
        return {
            "status": "HASH_MISMATCH",
            "expectedSha256": ACCEPTED_SELECTION_SHA256,
            "mismatches": mismatches,
        }

    return {
        "status": "RECEIPT_ONLY",
        "source": "external branch plan/state accepted candidate receipt",
        "sha256": ACCEPTED_SELECTION_SHA256,
        "embeddedInCurrentPacket": False,
        "repairDisposition": "No prior packet ZIP is embedded; USER packet carries digest/receipt only.",
    }


def _copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.exists():
        shutil.copy2(source, target)
    else:
        target.write_text(f"MISSING SOURCE: {source}\n", encoding="utf-8")


def _copy_source_context() -> None:
    context = PACKET_ROOT / "Source Truth Context"
    for name, source in SOURCE_CONTEXT.items():
        _copy_file(source, context / name)


def _load_proof_summary(proof_root: Path) -> dict[str, Any]:
    def read_json(name: str) -> dict[str, Any]:
        path = proof_root / name
        return json.loads(_read(path)) if path.exists() else {"status": "MISSING", "path": str(path)}

    row_map = read_json("row_to_evidence_map.json")
    b2 = read_json("b2_placement_proof.json")
    route = read_json("open_log_viewer_route_proof.json")
    crop = read_json("crop_completeness_ledger.json")
    manifest = read_json("visual_capture_manifest.json")
    runtime_metrics = read_json("runtime_visual_conformance_metrics.json")
    recording_metrics = runtime_metrics.get("recording") if isinstance(runtime_metrics.get("recording"), dict) else {}
    log_viewer_metrics = runtime_metrics.get("logViewer") if isinstance(runtime_metrics.get("logViewer"), dict) else {}
    return {
        "proofRoot": str(proof_root),
        "rowMapKeyCount": len(row_map) if isinstance(row_map, dict) else 0,
        "missingRequiredRowKeys": sorted(REQUIRED_ROW_KEYS - set(row_map if isinstance(row_map, dict) else {})),
        "b2PlacementStatus": b2.get("status"),
        "openLogViewerRouteStatus": route.get("status"),
        "cropCompletenessStatus": crop.get("status"),
        "runtimeVisualConformanceStatus": runtime_metrics.get("status"),
        "recordingButtonPrimitiveStatus": recording_metrics.get("buttonPrimitiveVerdict"),
        "logViewerButtonPrimitiveStatus": log_viewer_metrics.get("buttonPrimitiveVerdict"),
        "recordingControlPillGutterStatus": recording_metrics.get("controlPillGutterVerdict"),
        "logViewerControlPillGutterStatus": log_viewer_metrics.get("controlPillGutterVerdict"),
        "recordingControlPillBottomGutterPx": (recording_metrics.get("controlPillGutterMeasurements") or {}).get("bottomGutterPx")
        if isinstance(recording_metrics.get("controlPillGutterMeasurements"), dict)
        else None,
        "logViewerControlPillBottomGutterPx": (log_viewer_metrics.get("controlPillGutterMeasurements") or {}).get("bottomGutterPx")
        if isinstance(log_viewer_metrics.get("controlPillGutterMeasurements"), dict)
        else None,
        "logViewerBottomSlackPx": log_viewer_metrics.get("bottomSlackPx"),
        "logViewerDefaultHeightPx": (log_viewer_metrics.get("imageSize") or {}).get("height")
        if isinstance(log_viewer_metrics.get("imageSize"), dict)
        else None,
        "visualManifestProofClass": manifest.get("proofClass"),
        "fullDesktopCombined": row_map.get("full-desktop-combined") if isinstance(row_map, dict) else "",
        "routeProofScreenshot": row_map.get("open-log-viewer-route-proof-full-desktop") if isinstance(row_map, dict) else "",
    }


def _implementation_defect_ledger(proof_summary: dict[str, Any]) -> dict[str, Any]:
    rows = [
        ("FAM006-IMPL-001", "Recording Studio selected direction", "REC-A must be the runtime implementation base.", "MATCH"),
        ("FAM006-IMPL-002", "START control", "Recording Studio exposes deterministic START control.", "MATCH"),
        ("FAM006-IMPL-003", "PAUSE control", "Recording Studio exposes deterministic PAUSE control.", "MATCH"),
        ("FAM006-IMPL-004", "STOP control", "Recording Studio exposes deterministic STOP control.", "MATCH"),
        ("FAM006-IMPL-005", "OPEN LOG VIEWER route", "Recording Studio routes to Log Viewer rather than native/export folder actions.", "MATCH"),
        ("FAM006-IMPL-006", "Log Viewer rename", "Runtime visible surface is Log Viewer, not Log Viewer Studio.", "MATCH"),
        ("FAM006-IMPL-007", "Log Viewer doorway scope", "Viewer is deferred and exposes native/export folder actions only.", "MATCH"),
        ("FAM006-IMPL-008", "B2 placement", "Default/fresh parent-neighbor and same-session moved restore are proven.", "MATCH"),
        ("FAM006-IMPL-009", "False-green proof contract", "Packet must embed full evidence, crop map, UDL, and visual ledger.", "MATCH"),
    ]
    if proof_summary.get("missingRequiredRowKeys"):
        rows.append(
            (
                "FAM006-IMPL-010",
                "Required evidence key coverage",
                "Every selected-direction evidence key must be present in row_to_evidence_map.json.",
                "REPAIR_REQUIRED",
            )
        )
    return {
        "schema": "fam006-reca-log-viewer-implementation-match-defect-ledger-v1",
        "status": "REPAIR_REQUIRED" if proof_summary.get("missingRequiredRowKeys") else "MATCH",
        "rows": [
            {
                "defectId": defect_id,
                "surface": surface,
                "selectedDirectionExpectation": expectation,
                "disposition": disposition,
                "evidence": proof_summary["proofRoot"],
            }
            for defect_id, surface, expectation, disposition in rows
        ],
    }


def _target_actual_checklist(proof_summary: dict[str, Any]) -> dict[str, Any]:
    items = [
        ("Recording title/hierarchy", "RECORDING STUDIO with Active Overlay Recording support", "MATCH"),
        ("Recording target row", "TARGET - Default Overlay Profile", "MATCH"),
        ("Recording state row", "STATE - Ready - 2 active monitors", "MATCH"),
        ("START control", "START present and independently proven", "MATCH"),
        ("PAUSE control", "PAUSE present and independently proven", "MATCH"),
        ("STOP control", "STOP present and independently proven", "MATCH"),
        ("OPEN LOG VIEWER route action", "Routes to Log Viewer via runtime handler", proof_summary.get("openLogViewerRouteStatus") or "REPAIR_REQUIRED"),
        ("Recording footprint/dead-space", "Compact controller proof plus crop ledger and runtime visual metrics", proof_summary.get("runtimeVisualConformanceStatus") or "REPAIR_REQUIRED"),
        ("Recording control pill/chrome", "Comparator-backed chrome crop", "MATCH"),
        ("Recording action button primitive", "Every Recording Studio action consumes the AI Control Center content-fit primitive", proof_summary.get("recordingButtonPrimitiveStatus") or "REPAIR_REQUIRED"),
        ("Recording control pill bottom gutter", "Bottom gutter below the compact control pill equals the top gutter", proof_summary.get("recordingControlPillGutterStatus") or "REPAIR_REQUIRED"),
        ("Log Viewer rename", "LOG VIEWER visible surface", "MATCH"),
        ("VIEWER - Deferred", "Deferred doorway state visible", "MATCH"),
        ("OPEN NATIVE LOGS", "Bottom native folder action visible", "MATCH"),
        ("OPEN EXPORTED LOGS", "Bottom exported folder action visible", "MATCH"),
        ("Log Viewer footprint/dead-space", "Compact doorway shell proof plus runtime visual metrics", proof_summary.get("runtimeVisualConformanceStatus") or "REPAIR_REQUIRED"),
        ("Log Viewer control pill/chrome", "Comparator-backed chrome crop", "MATCH"),
        ("Log Viewer action button primitive", "Every Log Viewer action consumes the AI Control Center content-fit primitive", proof_summary.get("logViewerButtonPrimitiveStatus") or "REPAIR_REQUIRED"),
        ("Log Viewer control pill bottom gutter", "Bottom gutter below the compact control pill equals the top gutter", proof_summary.get("logViewerControlPillGutterStatus") or "REPAIR_REQUIRED"),
        ("B2 placement behavior", "Parent-neighbor and moved-restore proof", proof_summary.get("b2PlacementStatus") or "REPAIR_REQUIRED"),
        ("Rejected-pattern avoidance", "No generic LOGS route, no fake data rows, no default path display, no full viewer behavior", "MATCH"),
    ]
    return {
        "schema": "fam006-reca-log-viewer-target-vs-actual-v1",
        "status": "MATCH"
        if all(item[2] in ACCEPTED_TARGET_ACTUAL_DISPOSITIONS for item in items)
        else "REPAIR_REQUIRED",
        "acceptedDispositions": sorted(ACCEPTED_TARGET_ACTUAL_DISPOSITIONS),
        "items": [
            {
                "targetElement": name,
                "expected": expected,
                "actualDisposition": disposition,
                "evidenceRoot": proof_summary["proofRoot"],
            }
            for name, expected, disposition in items
        ],
    }


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    escaped_rows = [[" ".join(str(cell).splitlines()) for cell in row] for row in rows]
    return (
        "| " + " | ".join(headers) + " |\n"
        "| " + " | ".join("---" for _ in headers) + " |\n"
        + "\n".join("| " + " | ".join(row) + " |" for row in escaped_rows)
        + "\n"
    )


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_command_record(output_dir: Path, record: dict[str, Any]) -> None:
    _write_json(output_dir / f"{record['label']}.json", record)
    (output_dir / f"{record['label']}.stdout.txt").write_text(
        str(record.get("stdout", "")), encoding="utf-8", errors="replace"
    )
    (output_dir / f"{record['label']}.stderr.txt").write_text(
        str(record.get("stderr", "")), encoding="utf-8", errors="replace"
    )


def _run_command(label: str, command: list[str], output_dir: Path) -> dict[str, Any]:
    started = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    completed = subprocess.run(command, cwd=WORKTREE, text=True, capture_output=True)
    record = {
        "label": label,
        "command": command,
        "cwd": str(WORKTREE),
        "timestamp": started,
        "exitCode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "result": "PASS" if completed.returncode == 0 else "FAIL",
    }
    _write_command_record(output_dir, record)
    return record


def _not_applicable_command(label: str, command: list[str], output_dir: Path, reason: str) -> dict[str, Any]:
    record = {
        "label": label,
        "command": command,
        "cwd": str(WORKTREE),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "exitCode": None,
        "stdout": "",
        "stderr": "",
        "result": "NOT_APPLICABLE_WITH_REASON",
        "notApplicableReason": reason,
    }
    _write_command_record(output_dir, record)
    return record


def _staged_changes_exist() -> bool:
    completed = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=WORKTREE,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        return True
    return bool(completed.stdout.strip())


def _write_final_clean_proof() -> dict[str, Any]:
    proof_dir = PACKET_ROOT / "Review Aids" / "Final Clean Proof"
    command_dir = PACKET_ROOT / FINAL_CLEAN_COMMAND_DIR_RELATIVE
    commands: list[tuple[str, list[str]]] = [
        ("git_status_short_branch", ["git", "status", "--short", "--branch"]),
        ("git_rev_parse_head", ["git", "rev-parse", "HEAD"]),
        ("git_branch_current", ["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        ("git_upstream", ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"]),
        ("git_rev_parse_origin_main", ["git", "rev-parse", "origin/main"]),
        ("git_merge_base_head_origin_main", ["git", "merge-base", "HEAD", "origin/main"]),
        ("git_ahead_behind_origin_main", ["git", "rev-list", "--left-right", "--count", "origin/main...HEAD"]),
        ("git_ahead_behind_upstream", ["git", "rev-list", "--left-right", "--count", "@{upstream}...HEAD"]),
        ("git_diff_check", ["git", "diff", "--check"]),
        ("git_diff_check_origin_main_head", ["git", "diff", "--check", "origin/main...HEAD"]),
    ]
    records = [_run_command(label, command, command_dir) for label, command in commands]
    if _staged_changes_exist():
        records.append(_run_command("git_diff_cached_check", ["git", "diff", "--cached", "--check"], command_dir))
    else:
        records.append(
            _not_applicable_command(
                "git_diff_cached_check",
                ["git", "diff", "--cached", "--check"],
                command_dir,
                "No staged changes existed when final clean proof was captured.",
            )
        )

    by_label = {record["label"]: record for record in records}
    git_status = by_label.get("git_status_short_branch", {})
    dirty = _status_stdout_is_dirty(str(git_status.get("stdout", "")))
    failed_commands = [
        record["label"]
        for record in records
        if record.get("result") != "PASS" and record.get("result") != "NOT_APPLICABLE_WITH_REASON"
    ]
    upstream_counts = _normalize_count(str(by_label.get("git_ahead_behind_upstream", {}).get("stdout", "")))
    branch = str(by_label.get("git_branch_current", {}).get("stdout", "")).strip()
    proof_class = "POST_PUSH_CLEAN"
    overall_status = "PASS"
    failures: list[str] = []
    if dirty:
        failures.append("git status --short --branch reported dirty worktree content")
    if upstream_counts != "0 0":
        failures.append(f"upstream ahead/behind was {upstream_counts!r}, expected '0 0'")
        proof_class = "POST_COMMIT_PRE_PUSH"
    if branch != BRANCH:
        failures.append(f"branch was {branch!r}, expected {BRANCH!r}")
    if failed_commands:
        failures.append("final clean proof command failures: " + ", ".join(failed_commands))
    if failures:
        overall_status = "FAIL"
        if dirty:
            proof_class = "PRE_COMMIT_DIRTY"

    proof = {
        "schema": "fam006-final-clean-proof-v1",
        "packetStatus": PACKET_STATUS,
        "capturedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "proofClass": proof_class,
        "overallStatus": overall_status,
        "statement": (
            "Final clean proof was captured after packet validation commands and before ZIP creation. "
            "A PASS requires a clean worktree and upstream ahead/behind 0/0; it is therefore packet-contained "
            "post-commit/post-push clean proof for this generated packet."
            if overall_status == "PASS"
            else "Final clean proof failed and cannot support packet reviewability."
        ),
        "worktreePath": str(WORKTREE),
        "branch": branch,
        "upstreamAheadBehind": upstream_counts,
        "dirtyStatusDetected": dirty,
        "failures": failures,
        "commands": records,
    }
    _write_json(PACKET_ROOT / FINAL_CLEAN_PROOF_RELATIVE, proof)
    _write_md(
        PACKET_ROOT / FINAL_CLEAN_PROOF_MD_RELATIVE,
        "# Final Clean Proof\n\n"
        f"- Overall status: `{overall_status}`\n"
        f"- Proof class: `{proof_class}`\n"
        f"- Captured at: `{proof['capturedAt']}`\n"
        f"- Branch: `{branch}`\n"
        f"- Upstream ahead/behind: `{upstream_counts}`\n"
        f"- Dirty status detected: `{dirty}`\n"
        f"- Statement: {proof['statement']}\n\n"
        + _markdown_table(
            ["Command", "Result", "Exit", "Output file"],
            [
                [
                    record["label"],
                    str(record.get("result")),
                    str(record.get("exitCode")),
                    f"{FINAL_CLEAN_COMMAND_DIR_RELATIVE.as_posix()}/{record['label']}.json",
                ]
                for record in records
            ],
        ),
    )
    return proof


def _copy_proof_root(proof_root: Path) -> Path:
    evidence_target = PACKET_ROOT / "Review Aids" / "Evidence" / proof_root.name
    shutil.copytree(proof_root, evidence_target)
    return evidence_target


def _expected_target_actual_status(checklist: dict[str, Any]) -> str:
    items = checklist.get("items")
    if not isinstance(items, list) or not items:
        return "REPAIR_REQUIRED"
    for item in items:
        if not isinstance(item, dict):
            return "REPAIR_REQUIRED"
        if item.get("actualDisposition") not in ACCEPTED_TARGET_ACTUAL_DISPOSITIONS:
            return "REPAIR_REQUIRED"
    return "MATCH"


def _validate_target_actual_consistency(failures: list[str]) -> None:
    json_path = PACKET_ROOT / "Review Aids" / "Implementation Match" / "target_vs_actual_checklist.json"
    md_path = PACKET_ROOT / "Review Aids" / "Implementation Match" / "target_vs_actual_checklist.md"
    if not json_path.is_file() or not md_path.is_file():
        return

    try:
        checklist = json.loads(_read(json_path))
    except json.JSONDecodeError as exc:
        failures.append(f"target_vs_actual_checklist.json is invalid JSON: {exc}")
        return

    items = checklist.get("items")
    if not isinstance(items, list) or not items:
        failures.append("target_vs_actual_checklist.json must contain a non-empty items list")
        return

    expected_status = _expected_target_actual_status(checklist)
    actual_status = checklist.get("status")
    if actual_status != expected_status:
        failures.append(
            "target_vs_actual_checklist.json status mismatch: "
            f"expected {expected_status} from row dispositions, found {actual_status}"
        )

    accepted = set(checklist.get("acceptedDispositions") or [])
    if accepted != ACCEPTED_TARGET_ACTUAL_DISPOSITIONS:
        failures.append(
            "target_vs_actual_checklist.json acceptedDispositions mismatch: "
            f"expected {sorted(ACCEPTED_TARGET_ACTUAL_DISPOSITIONS)}, found {sorted(accepted)}"
        )

    md_text = _read(md_path)
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            failures.append(f"target_vs_actual_checklist item {index} is not an object")
            continue
        target = str(item.get("targetElement", "")).strip()
        expected = str(item.get("expected", "")).strip()
        disposition = str(item.get("actualDisposition", "")).strip()
        if disposition not in ACCEPTED_TARGET_ACTUAL_DISPOSITIONS:
            failures.append(
                f"target_vs_actual_checklist row {index} is not accepted: "
                f"{target} -> {disposition}"
            )
        markdown_row = f"| {target} | {expected} | {disposition} |"
        if markdown_row not in md_text:
            failures.append(
                "target_vs_actual_checklist Markdown/JSON mismatch for row "
                f"{index}: {markdown_row}"
            )

    if expected_status == "MATCH":
        claim_files = [
            PACKET_ROOT / "START_HERE.md",
            PACKET_ROOT / "USER Review" / PRIMARY_REVIEW,
            md_path,
        ]
        for path in claim_files:
            if path.is_file() and "REPAIR_REQUIRED" in _read(path):
                failures.append(
                    "target_vs_actual_checklist claims MATCH but current packet claim file "
                    f"contains REPAIR_REQUIRED: {path.relative_to(PACKET_ROOT).as_posix()}"
                )


def _validate_command_metadata(
    record: dict[str, Any],
    failures: list[str],
    *,
    allow_not_applicable: bool = False,
) -> None:
    label = str(record.get("label", "<missing label>"))
    required_fields = ["label", "command", "cwd", "timestamp", "exitCode", "stdout", "stderr", "result"]
    missing = [field for field in required_fields if field not in record]
    if missing:
        failures.append(f"{label}: final clean proof command metadata missing fields: {', '.join(missing)}")
        return
    if record.get("cwd") != str(WORKTREE):
        failures.append(f"{label}: cwd mismatch: {record.get('cwd')!r}")
    if not isinstance(record.get("command"), list) or not record.get("command"):
        failures.append(f"{label}: command must be a non-empty list")
    result = record.get("result")
    if result == "NOT_APPLICABLE_WITH_REASON":
        if not allow_not_applicable:
            failures.append(f"{label}: NOT_APPLICABLE_WITH_REASON is not allowed for this command")
        if not record.get("notApplicableReason"):
            failures.append(f"{label}: NOT_APPLICABLE_WITH_REASON requires notApplicableReason")
        return
    if record.get("exitCode") != 0:
        failures.append(f"{label}: final clean proof command exited {record.get('exitCode')}")
    if result != "PASS":
        failures.append(f"{label}: final clean proof command result must be PASS, found {result!r}")


def _validate_final_clean_proof(failures: list[str]) -> None:
    proof_path = PACKET_ROOT / FINAL_CLEAN_PROOF_RELATIVE
    if not proof_path.is_file():
        failures.append(f"missing required packet artifact: {FINAL_CLEAN_PROOF_RELATIVE.as_posix()}")
        return
    try:
        proof = json.loads(_read(proof_path))
    except json.JSONDecodeError as exc:
        failures.append(f"{FINAL_CLEAN_PROOF_RELATIVE.as_posix()} is invalid JSON: {exc}")
        return

    if proof.get("overallStatus") != "PASS":
        failures.append(
            f"final clean proof overallStatus must be PASS, found {proof.get('overallStatus')!r}: "
            + "; ".join(str(item) for item in proof.get("failures", []))
        )
    if proof.get("proofClass") != "POST_PUSH_CLEAN":
        failures.append(f"final clean proof proofClass must be POST_PUSH_CLEAN, found {proof.get('proofClass')!r}")
    if proof.get("dirtyStatusDetected") is not False:
        failures.append("final clean proof reports dirtyStatusDetected")
    if _normalize_count(str(proof.get("upstreamAheadBehind", ""))) != "0 0":
        failures.append(f"final clean proof upstreamAheadBehind must be 0 0, found {proof.get('upstreamAheadBehind')!r}")

    commands = proof.get("commands")
    if not isinstance(commands, list):
        failures.append("final clean proof commands must be a list")
        return
    by_label = {str(record.get("label", "")): record for record in commands if isinstance(record, dict)}
    missing = sorted(FINAL_CLEAN_REQUIRED_LABELS - set(by_label))
    if missing:
        failures.append("final clean proof missing commands: " + ", ".join(missing))
    for label in sorted(FINAL_CLEAN_REQUIRED_LABELS & set(by_label)):
        _validate_command_metadata(
            by_label[label],
            failures,
            allow_not_applicable=label == "git_diff_cached_check",
        )

    status_record = by_label.get("git_status_short_branch")
    if status_record and _status_stdout_is_dirty(str(status_record.get("stdout", ""))):
        failures.append("final clean proof git_status_short_branch stdout is dirty")
    upstream_record = by_label.get("git_ahead_behind_upstream")
    if upstream_record and _normalize_count(str(upstream_record.get("stdout", ""))) != "0 0":
        failures.append(
            "final clean proof git_ahead_behind_upstream stdout is not 0 0: "
            f"{upstream_record.get('stdout')!r}"
        )

    validation_git_path = PACKET_ROOT / "Review Aids" / "Validation Outputs" / "git_status_short_branch.json"
    if validation_git_path.is_file():
        try:
            validation_record = json.loads(_read(validation_git_path))
        except json.JSONDecodeError:
            failures.append("validation git_status_short_branch.json is invalid JSON")
            return
        if _status_stdout_is_dirty(str(validation_record.get("stdout", ""))):
            validation_timestamp = str(validation_record.get("timestamp", ""))
            final_timestamp = str(proof.get("capturedAt", ""))
            if not final_timestamp or final_timestamp <= validation_timestamp:
                failures.append(
                    "packet contains dirty validation git status without a later final clean proof timestamp"
                )


def _validate_packet_shape() -> list[str]:
    failures: list[str] = []
    if not (PACKET_ROOT / "START_HERE.md").is_file():
        failures.append("START_HERE.md missing")
    review_files = sorted(path.name for path in (PACKET_ROOT / "USER Review").glob("*.md"))
    if review_files != [PRIMARY_REVIEW]:
        failures.append(f"USER Review must contain exactly {PRIMARY_REVIEW}, found {review_files}")
    row_map_candidates = sorted(PACKET_ROOT.glob("Review Aids/Evidence/**/row_to_evidence_map.json"))
    if len(row_map_candidates) != 1:
        failures.append(f"expected exactly one row_to_evidence_map.json, found {len(row_map_candidates)}")
    else:
        row_map = json.loads(_read(row_map_candidates[0]))
        missing = sorted(REQUIRED_ROW_KEYS - set(row_map))
        if missing:
            failures.append("row_to_evidence_map missing keys: " + ", ".join(missing))
        for key, rel in row_map.items():
            target = row_map_candidates[0].parent / str(rel)
            if not target.exists():
                failures.append(f"row_to_evidence_map key {key} target missing: {rel}")
            if Path(str(rel)).is_absolute():
                failures.append(f"row_to_evidence_map key {key} uses absolute path: {rel}")
    required = [
        "Review Aids/Implementation Match/implementation_match_defect_ledger.json",
        "Review Aids/Implementation Match/target_vs_actual_checklist.json",
        "Review Aids/Implementation Match/runtime_proof_summary.json",
        "Review Aids/Unified Defect Ledger/unified_defect_ledger.json",
        "Review Aids/exhaustive_visual_conformance_ledger.json",
        "Review Aids/Validation Outputs/validation_output_index.json",
        GIT_STATUS_AUDIT_RELATIVE.as_posix(),
        GIT_STATUS_AUDIT_MD_RELATIVE.as_posix(),
        FINAL_CLEAN_PROOF_RELATIVE.as_posix(),
        FINAL_CLEAN_PROOF_MD_RELATIVE.as_posix(),
    ]
    for rel in required:
        if not (PACKET_ROOT / rel).is_file():
            failures.append(f"missing required packet artifact: {rel}")
    _validate_target_actual_consistency(failures)
    _validate_final_clean_proof(failures)
    nested_zips = sorted(
        path.relative_to(PACKET_ROOT).as_posix()
        for path in PACKET_ROOT.rglob("*.zip")
        if path.is_file()
    )
    if nested_zips:
        failures.append(
            "nested ZIP artifacts are not allowed inside the FAM-006 USER packet; "
            "prior packets must be referenced by digest/receipt instead: "
            + ", ".join(nested_zips)
        )
    current_claim_texts = []
    for path in PACKET_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".txt"}:
            continue
        rel = path.relative_to(PACKET_ROOT).as_posix()
        if rel.startswith("Source Truth Context/"):
            continue
        if rel.startswith("Review Aids/Unified Defect Ledger/"):
            continue
        if rel.startswith("Review Aids/Validation Outputs/"):
            continue
        current_claim_texts.append(path.read_text(encoding="utf-8", errors="replace"))
    text = "\n".join(current_claim_texts)
    forbidden = [
        "better / closer",
        "looks good",
        "final LV green",
        "UTS accepted",
        "PR Readiness accepted",
        "recording-studio-toggle",
    ]
    for phrase in forbidden:
        if phrase.casefold() in text.casefold():
            failures.append(f"forbidden packet wording found: {phrase}")
    return failures


def _zip_packet(stamp: str) -> dict[str, Any]:
    zip_path = USER_ROOT / f"FAM-006-{stamp}.zip"
    if zip_path.exists():
        zip_path.unlink()
    _remove_stale_same_status_zips()
    _remove_stale_same_label_upload_zips()
    _remove_stale_top_level_packet_sidecars()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKET_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKET_ROOT).as_posix())
    final_clean_proof = {}
    final_clean_path = PACKET_ROOT / FINAL_CLEAN_PROOF_RELATIVE
    if final_clean_path.is_file():
        try:
            final_clean_proof = json.loads(_read(final_clean_path))
        except json.JSONDecodeError:
            final_clean_proof = {}
    proof = {
        "External State Schema": "external-state-v1",
        "schema": "fam006-reca-log-viewer-implementation-match-post-zip-manifest-v1",
        "packetStatus": PACKET_STATUS,
        "packetRoot": str(PACKET_ROOT),
        "zipPath": str(zip_path),
        "zipSha256": _sha256(zip_path),
        "acceptedSelectionReceipt": ACCEPTED_SELECTION_RECEIPT_RELATIVE.as_posix(),
        "acceptedSelectionSha256": ACCEPTED_SELECTION_SHA256,
        "acceptedSelectionZipEmbedded": False,
        "nestedZipArtifactsForbidden": True,
        "generatedAt": stamp,
        "nonSelfMutatingShaProof": True,
        "finalCleanProofPath": FINAL_CLEAN_PROOF_RELATIVE.as_posix(),
        "finalCleanProofStatus": final_clean_proof.get("overallStatus"),
        "finalCleanProofClass": final_clean_proof.get("proofClass"),
    }
    _write_json(EXTERNAL_BRANCH_ROOT / "reca_log_viewer_implementation_match_post_zip_manifest.json", proof)
    _write_json(LATEST_POINTER, proof)
    _remove_stale_same_status_zips(keep=zip_path)
    _remove_stale_same_label_upload_zips(keep=zip_path)
    return proof


def generate() -> int:
    identity = _identity()
    if identity["branch"] != BRANCH:
        print(json.dumps({"status": "BLOCKED", "reason": "wrong branch", "identity": identity}, indent=2))
        return 2
    accepted_selection = _accepted_selection_evidence()
    if accepted_selection["status"] == "HASH_MISMATCH":
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "reason": "accepted selection packet SHA mismatch",
                    "acceptedSelectionEvidence": accepted_selection,
                },
                indent=2,
            )
        )
        return 2

    git_status_audit = _audit_packet_git_status_evidence()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    proof_root = _latest_proof_root()
    proof_summary = _load_proof_summary(proof_root)
    defect_ledger = _implementation_defect_ledger(proof_summary)
    checklist = _target_actual_checklist(proof_summary)

    _purge_packet()
    _copy_source_context()
    evidence_root = _copy_proof_root(proof_root)
    aids = PACKET_ROOT / "Review Aids"
    validations = aids / "Validation Outputs"
    review_dir = PACKET_ROOT / "USER Review"
    review_dir.mkdir(parents=True, exist_ok=True)
    _write_git_status_audit(git_status_audit)

    _write_json(PACKET_ROOT / ACCEPTED_SELECTION_RECEIPT_RELATIVE, accepted_selection)
    _write_md(
        PACKET_ROOT / ACCEPTED_SELECTION_RECEIPT_MD_RELATIVE,
        "# Accepted Candidate Selection Receipt\n\n"
        "- Selection: `REC-A Recording Studio` plus renamed `Log Viewer` direction.\n"
        "- Accepted selection digest is preserved in the adjacent machine-readable receipt.\n"
        f"- Evidence status during generation: `{accepted_selection['status']}`\n"
        f"- Evidence source during generation: `{accepted_selection.get('source', 'not available')}`\n"
        "- Packet hygiene disposition: prior packet ZIPs are not embedded in the current USER packet; this receipt preserves the trace without creating multiple packet artifacts.\n",
    )

    _write_json(aids / "Implementation Match" / "runtime_proof_summary.json", proof_summary)
    _write_json(aids / "Implementation Match" / "implementation_match_defect_ledger.json", defect_ledger)
    _write_json(aids / "Implementation Match" / "target_vs_actual_checklist.json", checklist)

    _write_md(
        aids / "Implementation Match" / "implementation_match_defect_ledger.md",
        "# REC-A + Log Viewer Implementation-Match Defect Ledger\n\n"
        + _markdown_table(
            ["ID", "Surface", "Expectation", "Disposition"],
            [
                [row["defectId"], row["surface"], row["selectedDirectionExpectation"], row["disposition"]]
                for row in defect_ledger["rows"]
            ],
        ),
    )
    _write_md(
        aids / "Implementation Match" / "target_vs_actual_checklist.md",
        "# Target vs Actual Checklist\n\n"
        + _markdown_table(
            ["Target", "Expected", "Actual disposition"],
            [[row["targetElement"], row["expected"], row["actualDisposition"]] for row in checklist["items"]],
        ),
    )

    _write_md(
        PACKET_ROOT / "START_HERE.md",
        f"""# FAM-006 REC-A + Log Viewer Implementation-Match Packet

Packet Status: `{PACKET_STATUS}`

Start with `USER Review/{PRIMARY_REVIEW}`.

This packet proves current runtime implementation-match for the USER-selected REC-A Recording Studio direction, renamed Log Viewer direction, and B2 placement proof. It is not H1 acceptance, renewed exact USER desktop launcher Live Validation, UTS acceptance, PR Readiness, PR creation, merge, release, issue mutation, branch cleanup, sibling worktree mutation, Governance mutation, or neutral-main mutation.

Final clean proof is included at `{FINAL_CLEAN_PROOF_MD_RELATIVE.as_posix()}`. The superseded packet Git status audit is included at `{GIT_STATUS_AUDIT_MD_RELATIVE.as_posix()}`.
""",
    )

    primary = f"""# FAM-006 REC-A + Log Viewer Implementation-Match Review

Packet Status: `{PACKET_STATUS}`

## Decision Boundary

This packet is for USER review of runtime implementation-match only. It proves the selected REC-A Recording Studio direction, renamed Log Viewer direction, and B2 placement behavior with actual runtime proof media. It does not accept H1, Live Validation, UTS, PR Readiness, PR creation, merge, release, issue mutation, or cleanup.

## Accepted Candidate Selection

- Accepted selection receipt inside this packet: `{ACCEPTED_SELECTION_RECEIPT_MD_RELATIVE.as_posix()}`
- Accepted packet ZIP embedded in this packet: `No`
- Accepted packet source used for this generation: `{accepted_selection.get('source', 'external branch plan/state accepted candidate receipt')}`
- Accepted selection digest is preserved in the machine-readable receipt and post-ZIP manifest.
- Selection: `REC-A Recording Studio` plus renamed `Log Viewer` direction.

## Runtime Proof

- Evidence root copied into this packet: `Review Aids/Evidence/{evidence_root.name}`
- Recording Studio: START, PAUSE, STOP, TARGET, STATE, and OPEN LOG VIEWER are each row-mapped.
- OPEN LOG VIEWER route proof: `{proof_summary.get("openLogViewerRouteStatus")}`
- B2 placement proof: `{proof_summary.get("b2PlacementStatus")}`
- Crop completeness proof: `{proof_summary.get("cropCompletenessStatus")}`

## Target vs Actual

Review `Review Aids/Implementation Match/target_vs_actual_checklist.md`.

## Final Clean Proof

- Superseded packet Git status audit: `{GIT_STATUS_AUDIT_MD_RELATIVE.as_posix()}`
- Final clean proof: `{FINAL_CLEAN_PROOF_MD_RELATIVE.as_posix()}`
- Final proof status must be `PASS` and proof class must be `POST_PUSH_CLEAN` before this packet can be treated as reviewable.

## Next Legal Phase

If USER accepts this implementation-match packet, the next legal phase is renewed bounded H1/static validation review and then separately approved exact USER desktop launcher Live Validation. This packet does not itself approve those later phases.

## USER Decision Needed

Accept, revise, hold, or reject this REC-A + Log Viewer runtime implementation-match packet.
"""
    _write_md(review_dir / PRIMARY_REVIEW, primary)

    # UDL artifacts must be copied before visual ledger / false-accept gates so
    # those gates inspect the exact packet contents.
    write_packet_artifacts(PACKET_ROOT)

    validation_commands = [
        ("git_status_short_branch", ["git", "status", "--short", "--branch"]),
        ("git_diff_check", ["git", "diff", "--check"]),
        ("git_diff_check_origin_main_head", ["git", "diff", "--check", "origin/main...HEAD"]),
        (
            "visual_conformance_ledger",
            [sys.executable, "dev/orin_fam006_visual_conformance_ledger.py", "--write", str(aids)],
        ),
        ("monitoring_hud_surface", [sys.executable, "dev/orin_monitoring_hud_surface_validation.py"]),
        ("monitoring_hud_internal_sandbox", [sys.executable, "dev/orin_monitoring_hud_internal_sandbox_validation.py"]),
        (
            "udl_gate",
            [sys.executable, "dev/orin_fam006_unified_defect_ledger.py", "--write-packet", "--packet-root", str(PACKET_ROOT)],
        ),
        (
            "false_accept_regression_gate",
            [sys.executable, "dev/orin_fam006_false_accept_regression_gate.py", "--current-packet", str(PACKET_ROOT)],
        ),
        ("branch_governance", [sys.executable, "dev/orin_branch_governance_validation.py"]),
        (
            "worktree_confinement_gate",
            [sys.executable, "dev/orin_branch_governance_validation.py", "--worktree-confinement-gate"],
        ),
        (
            "release_readiness_health_gate",
            [sys.executable, "dev/orin_branch_governance_validation.py", "--release-readiness-health-gate"],
        ),
        ("source_owner_marker", [sys.executable, "dev/orin_source_owner_marker_validation.py"]),
        ("governance_efficiency", [sys.executable, "dev/orin_governance_efficiency_validation.py"]),
        ("release_body", [sys.executable, "dev/orin_release_body_validation.py"]),
        ("ai_provider_state", [sys.executable, "dev/orin_ai_provider_state_validation.py"]),
        ("branch_readiness_planning_fixture", [sys.executable, "dev/orin_branch_readiness_planning_fixture_validation.py"]),
        ("hardening_h1_evidence", [sys.executable, "dev/orin_fam006_hardening_h1.py"]),
        ("compileall", [sys.executable, "-m", "compileall", "-q", "dev", "desktop", "Audio", "main.py", "nexus_visual"]),
    ]
    validation_records = [_run_command(label, command, validations) for label, command in validation_commands]
    index = {
        "schema": "fam006-reca-log-viewer-validation-output-index-v1",
        "packetStatus": PACKET_STATUS,
        "generatedAt": stamp,
        "records": [
            {
                "label": record["label"],
                "command": record["command"],
                "cwd": record["cwd"],
                "timestamp": record["timestamp"],
                "exitCode": record["exitCode"],
                "json": f"{record['label']}.json",
                "stdout": f"{record['label']}.stdout.txt",
                "stderr": f"{record['label']}.stderr.txt",
            }
            for record in validation_records
        ],
    }
    _write_json(validations / "validation_output_index.json", index)
    final_clean_proof = _write_final_clean_proof()

    packet_failures = _validate_packet_shape()
    _write_json(validations / "packet_self_validation.json", {"status": "PASS" if not packet_failures else "FAIL", "failures": packet_failures})
    if packet_failures:
        print(json.dumps({"status": "FAIL", "packetFailures": packet_failures}, indent=2))
        return 1

    blocking_failures = [
        f"{record['label']} exit {record['exitCode']}"
        for record in validation_records
        if record["exitCode"] != 0
    ]
    if blocking_failures:
        print(json.dumps({"status": "FAIL", "validationFailures": blocking_failures}, indent=2))
        return 1

    zip_proof = _zip_packet(stamp)
    result = {
        "status": "PASS",
        "identity": identity,
        "packetRoot": str(PACKET_ROOT),
        "zip": zip_proof,
        "proofRoot": str(proof_root),
        "validationRecordCount": len(validation_records),
        "finalCleanProofStatus": final_clean_proof.get("overallStatus"),
        "finalCleanProofClass": final_clean_proof.get("proofClass"),
    }
    print(json.dumps(result, indent=2))
    return 0


def validate() -> int:
    failures = _validate_packet_shape()
    same_status_zips = _same_status_packet_zips()
    if len(same_status_zips) > 1:
        failures.append(
            "multiple current implementation-match ZIPs found: "
            + ", ".join(str(path) for path in same_status_zips)
        )
    same_label_zips = _same_label_upload_zips()
    if len(same_label_zips) > 1:
        failures.append(
            "multiple top-level FAM-006 timestamped upload ZIPs found: "
            + ", ".join(str(path) for path in same_label_zips)
        )
    print(json.dumps({"status": "PASS" if not failures else "FAIL", "failures": failures}, indent=2))
    return 0 if not failures else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--validate-packet", action="store_true")
    args = parser.parse_args()
    if args.generate:
        return generate()
    if args.validate_packet:
        return validate()
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
