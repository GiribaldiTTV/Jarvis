"""FAM-006 Workstream proof-readiness contract.

This helper records SLC-055 readiness only. It does not run Hardening H1,
Live Validation LV1, UTS, runtime recording, file writing, or PR readiness.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from desktop.recording_output_contract import validate_recording_output_contract


WORKSTREAM_READINESS_ID = "slc-055-fam006-validation-live-proof-readiness"
WORKSTREAM_PACKAGE_ID = "pkg-006-active-overlay-recording-runtime-foundation"
WORKSTREAM_SEAMS = (
    "SLC-051 target-session-truth",
    "SLC-052 hud-overlay-target-preview",
    "SLC-053 recording-control-window-foundation",
    "SLC-054 output-contract-schema-readback",
    "SLC-055 validation-live-proof-readiness",
)


def build_fam006_workstream_readiness_proof() -> dict[str, Any]:
    output_contract = validate_recording_output_contract()
    seams = [
        {
            "slice": "SLC-051",
            "status": "complete",
            "proof": "active Overlay Profile target/session truth validator coverage",
            "futureGate": "recording execution and file writing blocked",
        },
        {
            "slice": "SLC-052",
            "status": "complete",
            "proof": "HUD Overlay target preview and launcher transparency validator coverage",
            "futureGate": "real Start/Stop, tray, export/share, and provider/model work blocked",
        },
        {
            "slice": "SLC-053",
            "status": "complete",
            "proof": "standalone Recording Control window foundation validator coverage",
            "futureGate": "Start/Stop controls disabled and future-gated",
        },
        {
            "slice": "SLC-054",
            "status": "complete",
            "proof": "durable output contract schema/readback proof",
            "futureGate": "file writing and recording execution blocked",
        },
        {
            "slice": "SLC-055",
            "status": "complete",
            "proof": "validation, H1, LV1, UTS, null/stress, and boundary route declared",
            "futureGate": "H1/LV1/UTS not claimed complete inside Workstream",
        },
    ]
    validators = [
        "git diff --check",
        "git diff --check origin/main...HEAD",
        "python dev\\orin_branch_governance_validation.py",
        "python dev\\orin_branch_governance_validation.py --worktree-confinement-gate",
        "python dev\\orin_branch_governance_validation.py --release-readiness-health-gate",
        "python dev\\orin_monitoring_hud_surface_validation.py",
        "python dev\\orin_monitoring_hud_internal_sandbox_validation.py",
        "python dev\\orin_branch_readiness_planning_fixture_validation.py",
        "python dev\\orin_validation_suite.py --phase runtime-fam006 --format text",
        "python dev\\orin_release_body_validation.py",
        "python dev\\orin_ai_provider_state_validation.py",
        "python dev\\orin_source_owner_marker_validation.py",
        "python -m compileall -q dev desktop Audio main.py nexus_visual",
    ]
    proof = {
        "readinessId": WORKSTREAM_READINESS_ID,
        "packageId": WORKSTREAM_PACKAGE_ID,
        "workstreamGreenCandidate": True,
        "packageSlicesComplete": all(item["status"] == "complete" for item in seams),
        "seams": seams,
        "requiredValidators": validators,
        "hardeningH1State": "pending-after-workstream-green",
        "hardeningH1Expectations": [
            "compare SLC-051 through SLC-055 against accepted BP1/BP2/BP3",
            "stress null active profile, stale profile, high-volume membership, compact/default UI, output contract, and blocked execution boundaries",
            "verify no file writing, recording execution, tray controls, export/share, provider/model, or FAM-007 scope slipped into Workstream",
        ],
        "liveValidationLV1State": "pending-after-h1",
        "liveValidationLV1Expectations": [
            "real user-level mouse and keyboard proof for HUD Overlay launcher and Recording Control window surfaces",
            "focused screenshots or photo comparison for default and compact layouts",
            "explicit waiver or blocker if real input proof cannot be produced",
        ],
        "utsState": "pending-after-lv1",
        "utsExpectations": [
            "USER-facing summary covers HUD target preview, Recording Control window, blocked execution, and future-gated file writing",
            "no UTS is exported until Live Validation authority is active or waived",
        ],
        "futureGatedBoundaries": [
            "recording execution",
            "file writing",
            "real Start/Stop controls",
            "tray controls",
            "export/share",
            "provider/model work",
            "Native Log Loader implementation",
            "FAM-007 mutation",
        ],
        "outputContractProofPassed": output_contract["passed"],
        "fileWritingBlocked": output_contract["fileWritingBlocked"],
        "recordingExecutionBlocked": output_contract["recordingExecutionBlocked"],
        "workstreamGreen": False,
    }
    proof["workstreamGreen"] = (
        proof["workstreamGreenCandidate"]
        and proof["packageSlicesComplete"]
        and proof["outputContractProofPassed"]
        and proof["fileWritingBlocked"]
        and proof["recordingExecutionBlocked"]
        and proof["hardeningH1State"] == "pending-after-workstream-green"
        and proof["liveValidationLV1State"] == "pending-after-h1"
        and proof["utsState"] == "pending-after-lv1"
    )
    return deepcopy(proof)
