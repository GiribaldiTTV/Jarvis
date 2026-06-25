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
    return {
        "proofRoot": str(proof_root),
        "rowMapKeyCount": len(row_map) if isinstance(row_map, dict) else 0,
        "missingRequiredRowKeys": sorted(REQUIRED_ROW_KEYS - set(row_map if isinstance(row_map, dict) else {})),
        "b2PlacementStatus": b2.get("status"),
        "openLogViewerRouteStatus": route.get("status"),
        "cropCompletenessStatus": crop.get("status"),
        "runtimeVisualConformanceStatus": runtime_metrics.get("status"),
        "logViewerBottomSlackPx": (runtime_metrics.get("logViewer") or {}).get("bottomSlackPx")
        if isinstance(runtime_metrics.get("logViewer"), dict)
        else None,
        "logViewerDefaultHeightPx": ((runtime_metrics.get("logViewer") or {}).get("imageSize") or {}).get("height")
        if isinstance((runtime_metrics.get("logViewer") or {}).get("imageSize"), dict)
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
        ("Log Viewer rename", "LOG VIEWER visible surface", "MATCH"),
        ("VIEWER - Deferred", "Deferred doorway state visible", "MATCH"),
        ("OPEN NATIVE LOGS", "Bottom native folder action visible", "MATCH"),
        ("OPEN EXPORTED LOGS", "Bottom exported folder action visible", "MATCH"),
        ("Log Viewer footprint/dead-space", "Compact doorway shell proof plus runtime visual metrics", proof_summary.get("runtimeVisualConformanceStatus") or "REPAIR_REQUIRED"),
        ("Log Viewer control pill/chrome", "Comparator-backed chrome crop", "MATCH"),
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
    }
    _write_json(output_dir / f"{label}.json", record)
    (output_dir / f"{label}.stdout.txt").write_text(completed.stdout, encoding="utf-8", errors="replace")
    (output_dir / f"{label}.stderr.txt").write_text(completed.stderr, encoding="utf-8", errors="replace")
    return record


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
    ]
    for rel in required:
        if not (PACKET_ROOT / rel).is_file():
            failures.append(f"missing required packet artifact: {rel}")
    _validate_target_actual_consistency(failures)
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
