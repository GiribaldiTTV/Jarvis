"""FAM-006 branch-local Unified Defect Ledger gate.

This helper is intentionally branch-local. It turns the repeated FAM-006
false-green history into a persistent external-state ledger and a packet gate
without claiming global Governance enforcement exists yet.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


USER_ROOT = Path("C:/Nexus USER")
PACKET_ROOT = USER_ROOT / "FAM-006"
EXTERNAL_BRANCH_ROOT = Path(
    "C:/Nexus Governance State/branches/feature_fam_006_dashboard_recording_start_stop_local_file"
)
KNOWN_BAD_CORPUS_ROOT = EXTERNAL_BRANCH_ROOT / "false_accept_regression_corpus"
UDL_JSON = EXTERNAL_BRANCH_ROOT / "unified_defect_ledger.json"
UDL_MD = EXTERNAL_BRANCH_ROOT / "UNIFIED_DEFECT_LEDGER.md"
INCIDENT_JSON = EXTERNAL_BRANCH_ROOT / "false_green_incident_ledger.json"
INCIDENT_MD = EXTERNAL_BRANCH_ROOT / "FALSE_GREEN_INCIDENT_LEDGER.md"
UDL_GATE_JSON = EXTERNAL_BRANCH_ROOT / "unified_defect_ledger_gate.json"
EXTERNAL_STATE_SCHEMA = "external-state-v1"

ALLOWED_STATUSES = {
    "OPEN",
    "REPRODUCED",
    "IN_REPAIR",
    "FIXED_PENDING_PROOF",
    "PROOF_FAILED",
    "REOPENED",
    "CLOSED_WITH_PROOF",
    "BLOCKED_SOURCE_TRUTH",
    "OUT_OF_SCOPE_USER_APPROVAL_REQUIRED",
}
BLOCKING_STATUSES = {
    "OPEN",
    "REPRODUCED",
    "IN_REPAIR",
    "FIXED_PENDING_PROOF",
    "PROOF_FAILED",
    "REOPENED",
}
PACKET_REQUIRED_FILES = {
    "Review Aids/Unified Defect Ledger/unified_defect_ledger.json",
    "Review Aids/Unified Defect Ledger/UNIFIED_DEFECT_LEDGER.md",
    "Review Aids/Unified Defect Ledger/false_green_incident_ledger.json",
    "Review Aids/Unified Defect Ledger/FALSE_GREEN_INCIDENT_LEDGER.md",
    "Review Aids/Unified Defect Ledger/unified_defect_ledger_gate.json",
}
EXPECTED_KNOWN_BAD = {
    "FAM-006-20260622-170147.zip",
    "FAM-006-20260622-173545.zip",
    "FAM-006-20260622-175717.zip",
    "FAM-006-20260622-182112.zip",
    "FAM-006-20260622-192100.zip",
    "FAM-006-20260622-194848.zip",
    "FAM-006-20260622-202600.zip",
    "FAM-006-20260623-050502.zip",
    "FAM-006-20260623-060525.zip",
    "FAM-006-20260623-063715.zip",
}


def _defect(
    defect_id: str,
    *,
    origin: str,
    title: str,
    exact_user_wording: str,
    expected: str,
    actual: str,
    evidence: str,
    surfaces: str,
    root_cause: str,
    validator_gap: str,
    repair_target: str,
    acceptance: str,
    proof: str,
    status: str,
    closure: str,
    current_owned: bool = True,
    governance_candidate: str = "",
) -> dict[str, Any]:
    return {
        "defectId": defect_id,
        "origin": origin,
        "title": title,
        "exactUserWording": exact_user_wording,
        "sourceTruthBasis": "Docs/Main.md -> FAM-006 external branch plan, FAM-002, FAM-006 vision, UIREF-001..006, UTS guidance, validation registry",
        "expectedBehavior": expected,
        "actualBehavior": actual,
        "evidencePathOrReference": evidence,
        "affectedFilesOrSurfaces": surfaces,
        "ownerFamilyWorkstreamBoundary": "FAM-006 branch-local unless governanceCandidate is populated",
        "impact": "Blocks FAM-006 from returning REPAIRED/LV-green/UTS-ready/PR-ready on shape-only proof.",
        "rootCause": root_cause,
        "validatorProofGapThatAllowedIt": validator_gap,
        "adjacentDefectSweepResult": "Adjacent proof path inspected: packet evidence, crop/overlay/text/scope, visual ledger, red-team/root-cause row, false-ACCEPT gate.",
        "exactRepairTarget": repair_target,
        "acceptanceCriteria": acceptance,
        "requiredProof": proof,
        "validationRequired": "python dev\\orin_fam006_false_accept_regression_gate.py; python dev\\orin_fam006_visual_conformance_ledger.py; python dev\\orin_fam006_unified_defect_ledger.py",
        "status": status,
        "closureProof": closure,
        "currentOwned": current_owned,
        "governanceCandidate": governance_candidate,
    }


def seed_defects() -> list[dict[str, Any]]:
    return [
        _defect(
            "FAM006-UDL-001",
            origin="USER/ChatGPT",
            title="USER packet evidence referenced local paths instead of containing proof",
            exact_user_wording="Packet evidence being local-path-based or only partially self-contained.",
            expected="USER packet contains actual evidence media, packet-relative manifests, and source-truth context.",
            actual="Earlier packet referenced proof by local path or included incomplete media.",
            evidence="Rejected packets FAM-006-20260622-141036.zip and FAM-006-20260622-145536.zip; external plan lines 1523-1538.",
            surfaces="C:/Nexus USER/FAM-006 packet; dev/orin_fam006_false_accept_regression_gate.py",
            root_cause="Packet validation accepted path references and artifact presence before checking self-contained packet evidence.",
            validator_gap="No packet-contained evidence file parity gate for every green proof row.",
            repair_target="Require packet-relative evidence map and packet-contained media.",
            acceptance="Current packet gate fails when primary proof is absolute/local-only or missing from packet.",
            proof="Current false-ACCEPT gate validates row_to_evidence_map targets and source-truth context.",
            status="CLOSED_WITH_PROOF",
            closure="Known-bad corpus rejects older packets; current packet contains evidence under Review Aids/Evidence.",
        ),
        _defect(
            "FAM006-UDL-002",
            origin="USER/ChatGPT",
            title="Root-cause and red-team ledgers were generic or pass-biased",
            exact_user_wording="Root-cause ledgers using generic repeated language; internal red-team ledgers becoming pass-biased.",
            expected="Every root-cause/red-team row names the exact defect class, negative question, observed finding, and repair.",
            actual="Earlier rows repeated broad language and could pass while missing the defect class.",
            evidence="Known-bad FAM-006-20260622-192100.zip; external plan Loop V receipt.",
            surfaces="internal_visual_red_team_ledger.json; adjudication_failure_root_cause_ledger.json",
            root_cause="The gate counted rows and PASS values instead of enforcing unique defect-class content.",
            validator_gap="No uniqueness/minimum-specificity check for root-cause fields.",
            repair_target="Require named defect classes, unique root-cause fields, and known-bad rejection proof.",
            acceptance="Gate fails generic repeated fields and missing required red-team defect classes.",
            proof="Current FAM-006 false-ACCEPT gate enforces required defect classes and unique root-cause fields.",
            status="CLOSED_WITH_PROOF",
            closure="Known-bad Loop V packet is rejected for generic/pass-biased ledgers.",
        ),
        _defect(
            "FAM006-UDL-003",
            origin="ChatGPT",
            title="Crop completeness rows missing or self-attested",
            exact_user_wording="Crop rows missing, clipped, misframed, self-attested, or contradicted by overlay.",
            expected="Every required crop has target bounds, overlay, expected text, content/scope method, and PASS verdict.",
            actual="Earlier crop rows lacked the fields needed to prove completeness.",
            evidence="Known-bad FAM-006-20260622-194848.zip.",
            surfaces="crop_completeness_ledger.json; visual_capture_manifest.json",
            root_cause="The helper trusted completeness booleans without independent crop metadata.",
            validator_gap="Missing crop ledger field enforcement.",
            repair_target="Require crop ledger rows and overlay/text/scope/content checks.",
            acceptance="Gate rejects missing crop rows or incomplete crop-content fields.",
            proof="Current crop ledger validation rejects Loop VI known-bad packet.",
            status="CLOSED_WITH_PROOF",
            closure="Loop VI known-bad artifact rejected by current false-ACCEPT gate.",
        ),
        _defect(
            "FAM006-UDL-004",
            origin="ChatGPT",
            title="Crop overlay contradicted ledger claims",
            exact_user_wording="Crop overlay/ledger contradiction defect.",
            expected="Overlay rectangle, target rectangle, DOM sibling bounds, and ledger adjacent-content fields agree.",
            actual="Earlier overlays showed sibling geometry while the ledger claimed clean element crops.",
            evidence="Known-bad FAM-006-20260622-202600.zip.",
            surfaces="crop_overlays; crop_completeness_ledger.json",
            root_cause="Overlay existence was accepted without comparing overlay geometry to target/sibling bounds.",
            validator_gap="No DOM sibling intersection check for element crops.",
            repair_target="Reject undeclared adjacent geometry/text for element crops.",
            acceptance="Element crops fail if sibling geometry intersects the crop outside the target rectangle.",
            proof="Current false-ACCEPT gate rejects Loop VII known-bad packet.",
            status="CLOSED_WITH_PROOF",
            closure="Loop VII known-bad artifact rejected by overlay/ledger contradiction checks.",
        ),
        _defect(
            "FAM006-UDL-005",
            origin="ChatGPT",
            title="Expected-text and crop-scope audit incomplete",
            exact_user_wording="Expected-text lists incomplete; crop scope/type mismatch.",
            expected="Full-window/state/resize crops declare scope and list all required visible text.",
            actual="Earlier crops passed while omitting visible body/action/status text.",
            evidence="Known-bad FAM-006-20260623-050502.zip.",
            surfaces="crop_completeness_ledger.json; visual_capture_manifest.json",
            root_cause="The gate checked only listed text, not whether all required visible scope text was listed.",
            validator_gap="No crop-type-specific required text inventory.",
            repair_target="Require cropType and required scope text for full-window/state/resize crops.",
            acceptance="Gate fails omitted visible scope text or mismatched crop type.",
            proof="Current false-ACCEPT gate rejects Loop VIII known-bad packet.",
            status="CLOSED_WITH_PROOF",
            closure="Loop VIII known-bad artifact rejected by expected-text/scope audit.",
        ),
        _defect(
            "FAM006-UDL-006",
            origin="ChatGPT",
            title="Comparator proof not row-bound",
            exact_user_wording="Comparator proof missing, broad, duplicated, uncited, or not row-bound.",
            expected="Every green comparator row cites a packet-contained comparator key/path and row-specific finding.",
            actual="Earlier green rows cited AI Control Center generally and reused contact-sheet context.",
            evidence="Known-bad FAM-006-20260623-060525.zip.",
            surfaces="exhaustive_visual_conformance_ledger.json; row_to_evidence_map.json",
            root_cause="Accepted comparator prose was treated as proof without a row-bound comparator artifact.",
            validator_gap="No comparator_evidence_key/path/finding requirement for green rows.",
            repair_target="Require row-bound comparator evidence fields for green comparator rows.",
            acceptance="Gate rejects missing comparator keys or broad contact-sheet-only proof.",
            proof="Current false-ACCEPT gate rejects Loop IX known-bad packet.",
            status="CLOSED_WITH_PROOF",
            closure="Loop IX known-bad artifact rejected for missing comparator row-map keys and green-row fields.",
        ),
        _defect(
            "FAM006-UDL-007",
            origin="ChatGPT",
            title="Comparator crops broad/duplicated/mismatched",
            exact_user_wording="Comparator crops having undeclared adjacent text or wrong proof scope.",
            expected="Focused comparator keys use focused crops with overlay/source/target primitive proof and unique compatible hashes.",
            actual="Loop X packet reused broad AI Control Center screenshots under focused proof names.",
            evidence="Known-bad FAM-006-20260623-063715.zip SHA32BD9A6D2A0C9D70F62892E9A14E7E9FD43678785724381089CF4A118F97932D.",
            surfaces="comparator_crop_ledger.json; focused_comparator_crops; exhaustive_visual_conformance_ledger.json",
            root_cause="Key presence was checked before key content and crop focus were adjudicated.",
            validator_gap="No comparator crop ledger or duplicate hash/scope/content validation.",
            repair_target="Require comparator_crop_ledger.json and key-specific crop size/scope/content checks.",
            acceptance="Gate rejects missing comparator ledger, broad/full reuse, duplicate media misuse, and key/content mismatch.",
            proof="Current false-ACCEPT gate rejects Loop X known-bad packet and current packet includes comparator crop ledger.",
            status="CLOSED_WITH_PROOF",
            closure="Loop X known-bad artifact rejected by current comparator crop gate.",
        ),
        _defect(
            "FAM006-UDL-008",
            origin="USER",
            title="Runtime resize proof mismatch must stay scoped",
            exact_user_wording="Log Viewer resize proof not matching USER runtime behavior.",
            expected="Pre-LV resize proof is accurately labeled and exact desktop launcher LV remains pending.",
            actual="Earlier repair risked overclaiming pre-LV widget proof as USER-runtime proof.",
            evidence="visual_capture_manifest.json resizeProof.runtimeTruth.",
            surfaces="MonitoringHudLogViewerStudioWindow; visual_capture_manifest.json",
            root_cause="Proof class boundary was not explicit enough.",
            validator_gap="No required exact-desktop-launcher-live-validation-still-required marker.",
            repair_target="Keep pre-LV resize/fixed-size proof scoped and block renewed LV until USER approval.",
            acceptance="Gate requires runtimeTruth to preserve exact desktop launcher LV boundary.",
            proof="Current false-ACCEPT and visual ledger validators require exact desktop launcher LV boundary text.",
            status="CLOSED_WITH_PROOF",
            closure="Current packet proof remains pre-LV only; no renewed LV/UTS acceptance is claimed.",
        ),
        _defect(
            "FAM006-UDL-009",
            origin="USER",
            title="UI visual quality/product judgment remains controlling",
            exact_user_wording="UI visually improved but not complete/perfect; Codex stopping at better / closer / improved.",
            expected="FAM-006 cannot claim visual/product acceptance unless USER accepts or proof satisfies source-truth acceptance path.",
            actual="Repeated ACCEPT claims were rejected by USER visual judgment.",
            evidence="Returned UTS and false-ACCEPT receipts in external branch_plan.md.",
            surfaces="Recording Studio; Log Viewer Studio; USER packets",
            root_cause="Codex treated improvement and helper green as acceptance.",
            validator_gap="No UDL hard stop preserving USER visual/product override.",
            repair_target="UDL gate blocks green wording while USER review remains pending and forbids progress-language green.",
            acceptance="Current packet may be reviewable but not LV/UTS/PR green; USER decision remains pending.",
            proof="UDL marks this as OUT_OF_SCOPE_USER_APPROVAL_REQUIRED until USER accepts/revises/rejects visual result.",
            status="OUT_OF_SCOPE_USER_APPROVAL_REQUIRED",
            closure="Pending USER review of FAM-006 packet; no green/PR-ready/LV-ready claim allowed.",
            current_owned=False,
            governance_candidate="Global proof-verdict vocabulary should be promoted by Governance after FAM-006 branch-local proof.",
        ),
        _defect(
            "FAM006-UDL-010",
            origin="Codex",
            title="Branch-local UDL was missing before packet green claims",
            exact_user_wording="Create FAM-006-local Unified Defect Ledger process and artifacts.",
            expected="Persistent UDL exists in FAM-006 external state and packet before FAM-006 can report repaired/green.",
            actual="Before this task, defects existed across packet/helper outputs but no single branch-local UDL gate controlled packet generation.",
            evidence="This helper and external UDL files.",
            surfaces="C:/Nexus Governance State/branches/.../unified_defect_ledger.json; dev/orin_fam006_unified_defect_ledger.py",
            root_cause="False-green repairs were stored as sequential receipts instead of a single carry-forward gate.",
            validator_gap="Existing FAM-006 gates did not require UDL status closure.",
            repair_target="Create UDL helper and wire FAM-006 packet gates to require it.",
            acceptance="UDL helper passes; FAM-006 false-ACCEPT gate and visual ledger read the UDL.",
            proof="python dev\\orin_fam006_unified_defect_ledger.py and packet-contained UDL gate output.",
            status="CLOSED_WITH_PROOF",
            closure="UDL helper writes external ledgers and validates packet-contained UDL artifacts.",
        ),
        _defect(
            "FAM006-UDL-011",
            origin="Codex",
            title="Global false-green prevention remains a Governance candidate",
            exact_user_wording="Global/Governance prevention may require Governance carrier and separate USER approval.",
            expected="FAM-006 records global promotion need without mutating Governance from this branch.",
            actual="Global reusable enforcement still lives as guidance/future-gated source truth outside this branch-local implementation.",
            evidence="Docs/ui_reference_catalog/UIREF-006_negative_example_and_enforcement_contract.md known limitations.",
            surfaces="Docs/phase_governance.md; Docs/validation_helper_registry.md; dev/orin_user_review_bundle.py; future global false-accept helper",
            root_cause="UIREF-006 accepted the enforcement contract but deferred executable global fixtures/helpers.",
            validator_gap="No project-wide known-bad corpus/gate outside FAM-006.",
            repair_target="Route global promotion to Governance intake with exact approval.",
            acceptance="FAM-006 packet lists Governance candidate and does not block branch-local UDL implementation.",
            proof="UDL row is OUT_OF_SCOPE_USER_APPROVAL_REQUIRED with exact candidate file list.",
            status="OUT_OF_SCOPE_USER_APPROVAL_REQUIRED",
            closure="Governance candidate recorded; no Governance mutation performed.",
            current_owned=False,
            governance_candidate="Governance intake should generalize FAM-006 UDL/known-bad gate into project-wide proof acceptance contract.",
        ),
    ]


def seed_incidents(defects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    defect_ids = [row["defectId"] for row in defects]
    return [
        {
            "incidentId": "FAM006-FGI-001",
            "codexClaim": "Prior packets were returned as ACCEPT / REPAIRED / review-ready after helper green.",
            "userOrChatGPTRejection": "USER/ChatGPT repeatedly found visible UI/proof/packet defects after the claim.",
            "validatorFailed": "FAM-006 visual conformance and false-ACCEPT gates before UDL hardening.",
            "insufficientProofArtifact": "Known-bad packet series FAM-006-20260622-170147.zip through FAM-006-20260623-063715.zip.",
            "overclaimedLedgerRow": "Sequential repair receipts without one carry-forward UDL status gate.",
            "missedOrMisusedComparator": "AI Control Center/UIREF comparator evidence was used as broad context before row-bound focused crops were required.",
            "fam006PreventionAdded": "FAM-006 UDL plus packet gate, known-bad rejection, crop/comparator ledgers, red-team/root-cause specificity checks.",
            "globalGovernanceCandidate": "Project-wide UDL/false-green corpus and reusable packet/proof acceptance gate.",
            "linkedDefectIds": defect_ids,
        }
    ]


def _required_fields() -> set[str]:
    return {
        "defectId",
        "origin",
        "title",
        "exactUserWording",
        "sourceTruthBasis",
        "expectedBehavior",
        "actualBehavior",
        "evidencePathOrReference",
        "affectedFilesOrSurfaces",
        "ownerFamilyWorkstreamBoundary",
        "impact",
        "rootCause",
        "validatorProofGapThatAllowedIt",
        "adjacentDefectSweepResult",
        "exactRepairTarget",
        "acceptanceCriteria",
        "requiredProof",
        "validationRequired",
        "status",
        "closureProof",
        "currentOwned",
        "governanceCandidate",
    }


def _packet_rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def validate_udl_state(packet_root: Path | None = None) -> dict[str, Any]:
    defects = seed_defects()
    incidents = seed_incidents(defects)
    failures: list[str] = []
    ids = [str(row.get("defectId", "")) for row in defects]
    duplicate_ids = sorted(item for item, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        failures.append(f"duplicate UDL defect IDs: {', '.join(duplicate_ids)}")
    if len(defects) < 10:
        failures.append("UDL contains fewer than 10 seeded FAM-006 false-green defects")
    required = _required_fields()
    for row in defects:
        defect_id = str(row.get("defectId", "<missing>"))
        missing = sorted(required - set(row))
        if missing:
            failures.append(f"{defect_id}: missing fields: {', '.join(missing)}")
        status = str(row.get("status", ""))
        if status not in ALLOWED_STATUSES:
            failures.append(f"{defect_id}: invalid status {status!r}")
        if status in BLOCKING_STATUSES:
            failures.append(f"{defect_id}: blocking status remains {status}")
        if status == "CLOSED_WITH_PROOF" and not str(row.get("closureProof", "")).strip():
            failures.append(f"{defect_id}: CLOSED_WITH_PROOF missing closureProof")
        if status == "OUT_OF_SCOPE_USER_APPROVAL_REQUIRED" and not str(row.get("governanceCandidate", "")).strip():
            failures.append(f"{defect_id}: out-of-scope row missing governanceCandidate")
        for banned in ("improved", "mostly", "acceptable", "looks good", "good enough", "green enough"):
            if banned in status.casefold():
                failures.append(f"{defect_id}: soft status wording is forbidden: {status}")
    known_bad = {path.name for path in KNOWN_BAD_CORPUS_ROOT.glob("FAM-006-*.zip")} if KNOWN_BAD_CORPUS_ROOT.exists() else set()
    missing_known_bad = sorted(EXPECTED_KNOWN_BAD - known_bad)
    if missing_known_bad:
        failures.append(f"known-bad corpus missing artifacts: {', '.join(missing_known_bad)}")
    if not incidents:
        failures.append("false-green incident ledger is empty")
    for incident in incidents:
        for field in (
            "incidentId",
            "codexClaim",
            "userOrChatGPTRejection",
            "validatorFailed",
            "insufficientProofArtifact",
            "overclaimedLedgerRow",
            "missedOrMisusedComparator",
            "fam006PreventionAdded",
            "globalGovernanceCandidate",
            "linkedDefectIds",
        ):
            if field not in incident or incident[field] in ("", []):
                failures.append(f"{incident.get('incidentId', '<missing>')}: missing {field}")
    packet_files: list[str] = []
    if packet_root is not None:
        if not packet_root.exists():
            failures.append(f"packet root missing: {packet_root}")
        else:
            packet_files = [
                _packet_rel(path, packet_root)
                for path in packet_root.rglob("*")
                if path.is_file()
            ]
            present = set(packet_files)
            missing_packet = sorted(PACKET_REQUIRED_FILES - present)
            if missing_packet:
                failures.append(f"packet missing UDL files: {', '.join(missing_packet)}")
    status_counts = Counter(str(row["status"]) for row in defects)
    current_owned_blockers = [
        row["defectId"]
        for row in defects
        if row.get("currentOwned") is True and row.get("status") in BLOCKING_STATUSES
    ]
    if current_owned_blockers:
        failures.append(f"current-owned UDL blockers remain: {', '.join(current_owned_blockers)}")
    return {
        "External State Schema": EXTERNAL_STATE_SCHEMA,
        "status": "PASS" if not failures else "FAIL",
        "gate": "FAM-006 Unified Defect Ledger packet gate",
        "allowedStatuses": sorted(ALLOWED_STATUSES),
        "blockingStatuses": sorted(BLOCKING_STATUSES),
        "defectCount": len(defects),
        "statusCounts": dict(sorted(status_counts.items())),
        "currentOwnedBlockingDefects": current_owned_blockers,
        "knownBadCorpusRoot": str(KNOWN_BAD_CORPUS_ROOT),
        "knownBadCorpusCount": len(known_bad),
        "knownBadMissing": missing_known_bad,
        "packetRoot": str(packet_root) if packet_root else "",
        "packetFilesChecked": packet_files,
        "failures": failures,
    }


def _ledger_payload() -> dict[str, Any]:
    defects = seed_defects()
    return {
        "External State Schema": EXTERNAL_STATE_SCHEMA,
        "schema": "fam006-unified-defect-ledger-v1",
        "branch": "feature/fam-006-dashboard-recording-start-stop-local-file",
        "worktree": "C:/Nexus Worktrees/FAM-006",
        "statusVocabulary": sorted(ALLOWED_STATUSES),
        "hardRule": "No FAM-006 REPAIRED/LV-green/UTS-ready/PR-ready claim is legal while a current-owned UDL defect remains in a blocking status.",
        "defects": defects,
    }


def _incidents_payload() -> dict[str, Any]:
    defects = seed_defects()
    return {
        "External State Schema": EXTERNAL_STATE_SCHEMA,
        "schema": "fam006-false-green-incident-ledger-v1",
        "branch": "feature/fam-006-dashboard-recording-start-stop-local-file",
        "incidents": seed_incidents(defects),
    }


def _write_markdown(defects: list[dict[str, Any]], incidents: list[dict[str, Any]]) -> None:
    UDL_MD.write_text(
        "# FAM-006 Unified Defect Ledger\n\n"
        "This is the branch-local carry-forward ledger for FAM-006 false-green prevention. "
        "It is evidence and branch-local gate material, not global Governance law.\n\n"
        "| Defect ID | Origin | Title | Status | Current Owned | Proof / Decision |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(
            f"| {row['defectId']} | {row['origin']} | {row['title']} | {row['status']} | {row['currentOwned']} | {row['closureProof'] or row['governanceCandidate']} |"
            for row in defects
        )
        + "\n",
        encoding="utf-8",
    )
    INCIDENT_MD.write_text(
        "# FAM-006 False-Green Incident Ledger\n\n"
        "| Incident ID | Codex Claim | Rejection | Prevention Added | Linked Defects |\n"
        "| --- | --- | --- | --- | --- |\n"
        + "\n".join(
            f"| {row['incidentId']} | {row['codexClaim']} | {row['userOrChatGPTRejection']} | {row['fam006PreventionAdded']} | {', '.join(row['linkedDefectIds'])} |"
            for row in incidents
        )
        + "\n",
        encoding="utf-8",
    )


def write_external_state() -> dict[str, Any]:
    EXTERNAL_BRANCH_ROOT.mkdir(parents=True, exist_ok=True)
    ledger = _ledger_payload()
    incidents = _incidents_payload()
    UDL_JSON.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    INCIDENT_JSON.write_text(json.dumps(incidents, indent=2) + "\n", encoding="utf-8")
    _write_markdown(ledger["defects"], incidents["incidents"])
    gate = validate_udl_state()
    UDL_GATE_JSON.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")
    return gate


def write_packet_artifacts(packet_root: Path = PACKET_ROOT) -> dict[str, Any]:
    if not UDL_JSON.exists() or not INCIDENT_JSON.exists():
        write_external_state()
    target = packet_root / "Review Aids" / "Unified Defect Ledger"
    target.mkdir(parents=True, exist_ok=True)
    files = [
        (UDL_JSON, target / "unified_defect_ledger.json"),
        (UDL_MD, target / "UNIFIED_DEFECT_LEDGER.md"),
        (INCIDENT_JSON, target / "false_green_incident_ledger.json"),
        (INCIDENT_MD, target / "FALSE_GREEN_INCIDENT_LEDGER.md"),
    ]
    for source, destination in files:
        destination.write_bytes(source.read_bytes())
    initial_gate = validate_udl_state(None)
    (target / "unified_defect_ledger_gate.json").write_text(
        json.dumps(initial_gate, indent=2) + "\n",
        encoding="utf-8",
    )
    gate = validate_udl_state(packet_root)
    (target / "unified_defect_ledger_gate.json").write_text(
        json.dumps(gate, indent=2) + "\n",
        encoding="utf-8",
    )
    UDL_GATE_JSON.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")
    return gate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-external", action="store_true")
    parser.add_argument("--write-packet", action="store_true")
    parser.add_argument("--packet-root", type=Path, default=None)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    packet_root = args.packet_root
    if args.write_external:
        gate = write_external_state()
    else:
        gate = validate_udl_state(packet_root)
    if args.write_packet:
        gate = write_packet_artifacts(packet_root or PACKET_ROOT)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(gate, indent=2))
    return 0 if gate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
