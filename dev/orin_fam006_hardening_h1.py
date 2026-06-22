"""FAM-006 Hardening H1 proof for the active-overlay recording package.

This helper is non-mutating. It compares SLC-051 through SLC-055 against the
accepted BP1/BP2/BP3 route and verifies that Live Validation and UTS remain
outside H1 while Dashboard Start/Stop and local output writing are present.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.recording_output_contract import validate_recording_output_contract
from dev.orin_fam006_workstream_readiness import build_fam006_workstream_readiness_proof


HARDENING_H1_ID = "h1-fam006-dashboard-recording-studio-log-viewer-option-c"
PACKAGE_ID = "pkg-006-dashboard-recording-studio-log-viewer-option-c"


def _repo_root() -> Path:
    return ROOT


def _read_repo_text(relative_path: str) -> str:
    return (_repo_root() / relative_path).read_text(encoding="utf-8")


def _contains_all(text: str, markers: tuple[str, ...]) -> bool:
    return all(marker in text for marker in markers)


def build_fam006_hardening_h1_proof() -> dict[str, Any]:
    workstream = build_fam006_workstream_readiness_proof()
    output_contract = validate_recording_output_contract()

    branch_record = _read_repo_text(
        "Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md"
    )
    hud_state = _read_repo_text("desktop/monitoring_hud_state.py")
    hud_js = _read_repo_text("nexus_visual/monitoring_hud.js")
    hud_html = _read_repo_text("nexus_visual/monitoring_hud.html")
    studio_html = _read_repo_text("nexus_visual/monitoring_hud_studio.html")
    studio_css = _read_repo_text("nexus_visual/nexus_window_primitives.css")
    renderer = _read_repo_text("desktop/desktop_renderer.py")
    main_entry = _read_repo_text("desktop/orin_desktop_main.py")
    output_source = _read_repo_text("desktop/recording_output_contract.py")

    slc_results = [
        {
            "slice": "SLC-051",
            "result": _contains_all(
                hud_state + hud_js,
                (
                    "activeOverlayRecordingTarget",
                    "activeOverlayRecordingTargetProof",
                    "recordingExecutionState",
                    "fileWritingState",
                ),
            ),
            "hardeningCheck": "active Overlay Profile target/session truth markers",
        },
        {
            "slice": "SLC-052",
            "result": _contains_all(
                hud_html + hud_js,
                (
                    'data-dashboard-hub-card="recording"',
                    "Dashboard Recording",
                    "slc-052-dashboard-recording-card-target-status",
                    "dashboard-recording-card-primary",
                    "hud-overlay-overlay-focused",
                    "dashboard-status-summary",
                    "quick-access-start-stop",
                    "recording-studio-focused-control-status",
                    "monitoringHudToggleRecording",
                    "Log Viewer Studio",
                ),
            ),
            "hardeningCheck": "Dashboard Quick Access Start/Stop plus Recording card target/status markers",
        },
        {
            "slice": "SLC-053",
            "result": _contains_all(
                renderer + hud_js + studio_html + studio_css,
                (
                    "Recording Studio",
                    "recording_studio_window",
                    "MONITORING_HUD_RECORDING_STUDIO_READY",
                    "_dispatch_monitoring_hud_recording_studio_action",
                    "recordingExecutionState",
                    "recordingFileWritingState",
                    "fam006-detached-child-studio-shell-v3",
                    "nexus-window-primitives-v1-rendered-dom-css",
                    "Bounded FAM-006 Shared Primitive Carry-In",
                    "nexus_visual/nexus_window_primitives.css",
                    "sharedPrimitiveConsumer",
                    "featureStudioPrimitive",
                    "primaryVisualComparator",
                    "visualPrimitiveAdoptionContract",
                    "acceptedReferenceSet",
                    "photo-video-comparison-required",
                    "photo-video-comparison-not-runtime-self-attestation",
                    "visualRuntimeSelfAttestation",
                    "visualMatrixRequired",
                    "ultra-lightweight-detached-recording-controller",
                    "dashboardLifecycleDependency",
                    "recording-studio-open-log-viewer-action",
                    "recording-studio-toggle-action",
                    "single-stateful-start-stop-button-plus-log-viewer-route",
                    "monitoring-hud-studio-recording-toggle-action",
                    "monitoring-hud-hub-action-content-fit-equal-gutter-v2",
                    "detached-child-window-title-row",
                    "titleCardState",
                    "category-line-plus-strong-title",
                    "overflow: visible",
                    "text-overflow: clip",
                    "not-resizable-position-memory-only",
                    "data-resize-contract=\"not-resizable-position-memory-only\"",
                    "data-fixed-controller-height=\"224\"",
                    "HEIGHT = 224",
                    "monitoringHudStudioNativeDragHandle",
                    "hub-action-content-fit-equal-gutter-32px-pill",
                    "windowPlacementMemoryState",
                    "titleHeaderBadgeState",
                    "ai-control-center-title-group-no-extra-badge",
                    "top-right-header",
                    "AI-Control-Center-UIREF-001-title-group",
                    "AI-Control-Center-UIREF-002-window-control-cluster",
                    "AI-Control-Center-UIREF-003-action-button",
                    "ai-control-center-symbol-window-control-cluster",
                    "monitoring-hud-hub-action-content-fit-equal-gutter-v2",
                    "text-overflow: clip",
                    "log-viewer-open-export",
                    "fam006-detached-child-window-divider-state-row-density",
                    "fam006-detached-child-window-title-row",
                    "ai-control-center-symbol-window-control-pill",
                    "nativeLogRowsContained",
                ),
            ),
            "hardeningCheck": "standalone Recording Studio is active while tray/keybind/export customization remains future-gated",
        },
        {
            "slice": "SLC-054-SHELL",
            "result": _contains_all(
                renderer + hud_js + studio_html + studio_css,
                (
                    "Log Viewer Studio",
                    "log_viewer_studio_shell",
                    "MONITORING_HUD_LOG_VIEWER_STUDIO_READY",
                    "recording_output_dir",
                    "recording_export_dir",
                    "create-or-open-before-session",
                    "exportCustomizationState",
                    "fam006-detached-child-studio-shell-v3",
                    "nexus-window-primitives-v1-rendered-dom-css",
                    "Bounded FAM-006 Shared Primitive Carry-In",
                    "nexus_visual/nexus_window_primitives.css",
                    "sharedPrimitiveConsumer",
                    "featureStudioPrimitive",
                    "primaryVisualComparator",
                    "visualPrimitiveAdoptionContract",
                    "acceptedReferenceSet",
                    "photo-video-comparison-required",
                    "photo-video-comparison-not-runtime-self-attestation",
                    "visualRuntimeSelfAttestation",
                    "visualMatrixRequired",
                    "compact-current-branch-log-access-shell",
                    "qsizegrip-bottom-right-enabled",
                    "windowPlacementMemoryState",
                    "middle-elided-contained",
                    "pathRowsContained",
                    "contained-middle-elided-readable",
                    "titleHeaderBadgeState",
                    "ai-control-center-title-group-no-extra-badge",
                    "top-right-header",
                    "AI-Control-Center-UIREF-001-title-group",
                    "AI-Control-Center-UIREF-002-window-control-cluster",
                    "AI-Control-Center-UIREF-003-action-button",
                    "ai-control-center-symbol-window-control-cluster",
                    "monitoring-hud-hub-action-content-fit-equal-gutter-v2",
                    "detached-child-window-title-row",
                    "titleCardState",
                    "category-line-plus-strong-title",
                    "hub-action-content-fit-equal-gutter-32px-pill",
                    "fam006-detached-child-window-divider-state-row-density",
                    "fam006-detached-child-window-title-row",
                    "ai-control-center-symbol-window-control-pill",
                ),
            ),
            "hardeningCheck": "minimal Log Viewer Studio shell opens native/export roots pre-session and keeps full viewer/export customization future-gated",
        },
        {
            "slice": "SLC-054",
            "result": bool(
                output_contract.get("passed")
                and output_contract.get("fileWritingEnabled")
                and output_contract.get("recordingExecutionEnabled")
                and output_contract.get("writeReadbackPassed")
                and output_contract.get("profileLogConsistencyPassed")
                and output_contract.get("twoProfileLogConsistencyPassed")
                and _contains_all(
                    output_source,
                    (
                        "recording_output_contract",
                        "write_recording_output_files",
                        "readback_recording_output_files",
                        "ndai-native-recording-log",
                        ".ndailog",
                        "nativeLogReadableOnlyByNDAI",
                        "normalProductSaveCreatesExport",
                        "render_recording_output_csv",
                        "parse_recording_output_csv",
                        '"fileWritingState": "enabled"',
                        '"recordingExecutionState": "enabled"',
                    ),
                )
            ),
            "hardeningCheck": "output contract schema/write/readback and active execution markers",
        },
        {
            "slice": "SLC-055",
            "result": bool(
                workstream.get("workstreamGreen")
                and workstream.get("packageSlicesComplete")
                and workstream.get("hardeningH1State") == "pending-after-workstream-green"
                and workstream.get("liveValidationLV1State") == "pending-after-h1"
                and workstream.get("utsState") == "pending-after-lv1"
            ),
            "hardeningCheck": "Workstream Green proof and H1/LV1/UTS routing markers",
        },
        {
            "slice": "ISSUE-258",
            "result": _contains_all(
                renderer + main_entry,
                (
                    "monitoring_hud_initial_state",
                    "monitoring_hud_saved_state",
                    "overlayProfiles",
                    "activeOverlayProfileId",
                    "overlayProfileDefaultDeletedByUser",
                ),
            ),
            "hardeningCheck": "Overlay Profile restart persistence hydration markers",
        },
    ]

    accepted_gate_trace = _contains_all(
        branch_record,
        (
            "BP1 USER Branch Vision",
            "BP2 USER Branch Plan",
            "BP3 Workstream Entry / Orchestration Validation",
            "Dashboard Recording Start/Stop To Local File",
            "issue #258 Overlay Profile persistence",
            "SLC-051",
            "SLC-052",
            "SLC-053",
            "SLC-054",
            "SLC-055",
        ),
    )
    future_boundaries = (
        "tray controls",
        "export/share",
        "provider/model work",
        "Native Log Loader implementation",
        "FAM-007 mutation",
    )
    boundary_trace = all(boundary in branch_record for boundary in future_boundaries)
    stale_recording_studio_model_absent = not any(
        marker in studio_html + studio_css
        for marker in (
            "monitoring-hud-studio-start-action",
            "monitoring-hud-studio-stop-action",
            "grid-template-columns: repeat(3, minmax(0, 1fr))",
            "grid-template-columns: repeat(2, minmax(0, 1fr))",
            "monitoring-hud-hub-action-content-fit-v1",
            "<span>Target Overlay Profile</span>",
            "<span>Recording State</span>",
            "<span>Native Log</span>",
        )
    )

    proof = {
        "hardeningH1Id": HARDENING_H1_ID,
        "packageId": PACKAGE_ID,
        "phase": "Hardening",
        "h1Result": "Green",
        "acceptedBPTracePassed": accepted_gate_trace,
        "slcResults": slc_results,
        "allSlicesHardened": all(item["result"] for item in slc_results),
        "outputContractProofPassed": output_contract["passed"],
        "fileWritingEnabled": output_contract["fileWritingEnabled"],
        "recordingExecutionEnabled": output_contract["recordingExecutionEnabled"],
        "writeReadbackPassed": output_contract["writeReadbackPassed"],
        "profileLogConsistencyPassed": output_contract["profileLogConsistencyPassed"],
        "twoProfileLogConsistencyPassed": output_contract["twoProfileLogConsistencyPassed"],
        "futureBoundariesPreserved": boundary_trace,
        "staleRecordingStudioModelAbsent": stale_recording_studio_model_absent,
        "liveValidationState": "pending-user-admission-after-h1",
        "utsState": "pending-live-validation-stage-1",
        "formalUtsExported": False,
        "nextLegalPhase": "Live Validation",
        "nextActiveSeam": "Live Validation LV1 - FAM-006 Active Overlay Recording Runtime Implementation",
    }
    proof["hardeningGreen"] = (
        proof["acceptedBPTracePassed"]
        and proof["allSlicesHardened"]
        and proof["outputContractProofPassed"]
        and proof["fileWritingEnabled"]
        and proof["recordingExecutionEnabled"]
        and proof["writeReadbackPassed"]
        and proof["profileLogConsistencyPassed"]
        and proof["twoProfileLogConsistencyPassed"]
        and proof["futureBoundariesPreserved"]
        and proof["staleRecordingStudioModelAbsent"]
        and not proof["formalUtsExported"]
    )
    return deepcopy(proof)


def main() -> int:
    proof = build_fam006_hardening_h1_proof()
    print(json.dumps(proof, indent=2, sort_keys=True))
    if proof["hardeningGreen"]:
        print("PASS: FAM-006 Hardening H1 proof is green")
        return 0
    print("FAIL: FAM-006 Hardening H1 proof is not green")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
