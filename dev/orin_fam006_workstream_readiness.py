"""FAM-006 Workstream proof-readiness contract."""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.recording_output_contract import validate_recording_output_contract


WORKSTREAM_READINESS_ID = "slc-055-fam006-validation-live-proof-readiness"
WORKSTREAM_PACKAGE_ID = "pkg-006-dashboard-recording-studio-log-viewer-option-c"
WORKSTREAM_SEAMS = (
    "SLC-051 target-session-truth",
    "SLC-052 dashboard-recording-card-target-status",
    "SLC-053 dashboard-quick-access-start-stop",
    "SLC-054 output-contract-write-readback",
    "SLC-055 validation-live-proof-readiness",
)


def build_fam006_workstream_readiness_proof() -> dict[str, Any]:
    output_contract = validate_recording_output_contract()
    seams = [
        {
            "slice": "SLC-051",
            "status": "complete",
            "proof": "active Overlay Profile target/session truth validator coverage",
            "runtime": "snapshot-at-start target truth feeds Dashboard Start/Stop",
        },
        {
            "slice": "SLC-052",
            "status": "complete",
            "proof": "Dashboard Recording card target/status, Dashboard Quick Access Start/Stop, recording execution, and active-monitor transparency validator coverage",
            "futureGate": "tray, export/share, provider/model, and Native Log Loader work blocked",
        },
        {
            "slice": "SLC-053",
            "status": "complete",
            "proof": "Dashboard quick-access Start/Stop is active and the standalone/native Recording Studio opens as the focused control/status surface",
            "futureGate": "tray controls, keybinds, export/share customization, and provider/model work remain future-gated",
        },
        {
            "slice": "SLC-054",
            "status": "complete",
            "proof": "durable local file writing output contract writes native NDAI log output and proves readback; minimal Log Viewer Studio shell opens native/export folders before an active-session recording exists",
            "futureGate": "full Log Viewer Studio, previous-log selection, export customization, Native Log Loader, export/share, and provider/model work remain future-gated",
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
            "stress null active profile, stale profile, high-volume membership, compact/default UI, output contract, and Start/Stop states",
            "verify file writing stays in the runtime-owned local output root, Log Viewer Studio opens native/export roots pre-session, and tray/export customization/provider/model/FAM-007 scope does not slip into Workstream",
        ],
        "liveValidationLV1State": "pending-after-h1",
        "liveValidationLV1Expectations": [
            "real user-level mouse and keyboard proof for Dashboard Recording card target/status surface",
            "focused screenshots or photo comparison for default and compact Dashboard Recording card layouts",
            "explicit waiver or blocker if real input proof cannot be produced",
        ],
        "utsState": "pending-after-lv1",
        "utsExpectations": [
            "USER-facing summary covers Dashboard Quick Access Start/Stop, Recording card target/status, Recording Studio, minimal Log Viewer Studio shell, saved output result, readback proof, and future-gated tray/keybind/export customization",
            "no UTS is exported until Live Validation authority is active or waived",
        ],
        "futureGatedBoundaries": [
            "tray controls",
            "keybinds",
            "export/share customization",
            "full Log Viewer Studio",
            "previous-log selection",
            "provider/model work",
            "Native Log Loader implementation",
            "FAM-007 mutation",
        ],
        "outputContractProofPassed": output_contract["passed"],
        "fileWritingEnabled": output_contract["fileWritingEnabled"],
        "recordingExecutionEnabled": output_contract["recordingExecutionEnabled"],
        "writeReadbackPassed": output_contract["writeReadbackPassed"],
        "profileLogConsistencyPassed": output_contract["profileLogConsistencyPassed"],
        "twoProfileLogConsistencyPassed": output_contract["twoProfileLogConsistencyPassed"],
        "workstreamGreen": False,
    }
    proof["workstreamGreen"] = (
        proof["workstreamGreenCandidate"]
        and proof["packageSlicesComplete"]
        and proof["outputContractProofPassed"]
        and proof["fileWritingEnabled"]
        and proof["recordingExecutionEnabled"]
        and proof["writeReadbackPassed"]
        and proof["profileLogConsistencyPassed"]
        and proof["twoProfileLogConsistencyPassed"]
        and proof["hardeningH1State"] == "pending-after-workstream-green"
        and proof["liveValidationLV1State"] == "pending-after-h1"
        and proof["utsState"] == "pending-after-lv1"
    )
    return deepcopy(proof)
