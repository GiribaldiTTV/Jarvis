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
    "FAM-006-20260623-071500.reconstructed-known-bad.json",
    "FAM-006-20260623-113615.zip",
    "FAM-006-20260623-120234.zip",
}
KNOWN_BAD_SHA256 = {
    "FAM-006-20260623-071500.reconstructed-known-bad.json": "5605463897BAC7597DE6755DFB824EB7E9BA0B84B6F82A703DEF5FB5679BB373",
    "FAM-006-20260623-113615.zip": "CFBBFA0CDAC9A6A190DF22F4811BC7E959C3A32C58E5514AF025ED18FB289086",
    "FAM-006-20260623-120234.zip": "D93AADB19ABBDD0973412D301AB14ABF8B115349A352E75868607A32F3CC20FE",
}
TEXT_HYGIENE_EXTENSIONS = {".json", ".md"}
TEXT_HYGIENE_ROOTS = (
    "START_HERE.md",
    "USER Review",
    "Review Aids",
    "Source Truth Context",
)


def _is_text_hygiene_target(path: Path, root: Path) -> bool:
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    if not path.is_file():
        return False
    if rel.as_posix() == "START_HERE.md":
        return True
    if path.suffix.lower() not in TEXT_HYGIENE_EXTENSIONS:
        return False
    if not rel.parts:
        return False
    return rel.parts[0] in {"USER Review", "Review Aids", "Source Truth Context"}


def scan_packet_text_hygiene(packet_root: Path) -> list[str]:
    failures: list[str] = []
    if not packet_root.exists():
        return [f"packet root missing for text hygiene scan: {packet_root}"]
    for path in sorted(packet_root.rglob("*")):
        if not _is_text_hygiene_target(path, packet_root):
            continue
        rel = _packet_rel(path, packet_root)
        data = path.read_bytes()
        for index, byte in enumerate(data):
            if byte < 32 and byte not in (9, 10, 13):
                failures.append(f"{rel}: non-printable control byte 0x{byte:02X} at byte {index}")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"{rel}: invalid UTF-8 text: {exc}")
            continue
        if "\ufffd" in text:
            failures.append(f"{rel}: replacement character U+FFFD indicates decoding corruption")
        if "\x00" in text:
            failures.append(f"{rel}: null character corrupts USER-facing text")
        if "reconstructed \x0071500 record" in text:
            failures.append(f"{rel}: corrupted known-bad identifier `reconstructed \\x0071500 record`")
    return failures


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
        _defect(
            "FAM006-UDL-012",
            origin="USER/ChatGPT",
            title="Loop XI comparator crop content and scope recurrence",
            exact_user_wording="FAM-006-20260623-071500.zip was rejected for comparator crop content/scope defects that the UDL omitted.",
            expected="Latest USER/ChatGPT-rejected comparator crop content/scope recurrence must be represented as known-bad and tied to a UDL defect before closure.",
            actual="The first UDL implementation closed the comparator-crop class while omitting the 071500 recurrence.",
            evidence="Reconstructed known-bad record FAM-006-20260623-071500.reconstructed-known-bad.json; branch plan Loop X receipt naming C:/Nexus USER/FAM-006-20260623-071500.zip and SHA 5605463897BAC7597DE6755DFB824EB7E9BA0B84B6F82A703DEF5FB5679BB373.",
            surfaces="focused_comparator_crops; comparator_crop_ledger.json; exhaustive_visual_conformance_ledger.json; USER packet evidence root 20260623_071352_feature_studio_visual_fail_repair",
            root_cause="UDL closure used Loop X broad/duplicate comparator proof but did not carry forward the later comparator content/scope rejection.",
            validator_gap="Expected known-bad corpus omitted reconstructed known-bad records and did not require latest recurrence closure proof.",
            repair_target="Admit or reconstruct 071500 as known-bad, link it to this UDL ID, and require false-ACCEPT rejection coverage.",
            acceptance="UDL gate fails if the 071500 reconstructed known-bad record is missing or not linked to this defect; false-ACCEPT gate reports it rejected for comparator crop content/scope recurrence.",
            proof="FAM-006 UDL gate includes FAM-006-20260623-071500.reconstructed-known-bad.json and false-ACCEPT gate reports reconstructed-known-bad:FAM-006-20260623-071500.",
            status="CLOSED_WITH_PROOF",
            closure="071500 is reconstructed in the known-bad corpus and rejected by the FAM-006 false-ACCEPT regression gate for Loop XI comparator crop content/scope recurrence.",
        ),
        _defect(
            "FAM006-UDL-013",
            origin="USER/ChatGPT",
            title="UDL packet omitted latest known-bad and used generic incident ledger",
            exact_user_wording="FAM-006-20260623-113615.zip was rejected because the UDL missed 071500, left one generic false-green incident, and closed comparator crop recurrence too early.",
            expected="A UDL packet cannot pass when latest known-bad artifacts are missing, incidents are generic, or recurring defect classes are closed before latest recurrence rejection proof.",
            actual="The 113615 UDL packet passed despite missing 071500, aggregating false-green incidents, and not representing Loop XI as a current-owned defect.",
            evidence="Known-bad packet FAM-006-20260623-113615.zip SHA CFBBFA0CDAC9A6A190DF22F4811BC7E959C3A32C58E5514AF025ED18FB289086.",
            surfaces="unified_defect_ledger.json; false_green_incident_ledger.json; unified_defect_ledger_gate.json; FAM006_UNIFIED_DEFECT_LEDGER_REVIEW.md",
            root_cause="The first UDL gate counted expected old corpus artifacts and required any incident row, but not latest rejected-packet admission or event-specific incidents.",
            validator_gap="No failure for missing latest rejected packet, no incident-count/detail floor, and no recurrence-vs-closure proof check.",
            repair_target="Add 113615 to known-bad, require event-specific incident rows, require latest recurrence records, and reject generic incident ledgers.",
            acceptance="UDL gate fails if 113615 is absent; false-ACCEPT gate reports 113615 rejected as a UDL implementation false green.",
            proof="FAM-006 known-bad corpus includes FAM-006-20260623-113615.zip and current gates reject it while accepting only the regenerated packet.",
            status="CLOSED_WITH_PROOF",
            closure="113615 is admitted as known-bad and rejected by the repaired false-ACCEPT gate for missing latest known-bad, generic incident ledger, and premature UDL closure.",
        ),
        _defect(
            "FAM006-UDL-014",
            origin="ChatGPT",
            title="USER-facing packet text contains non-printable control character",
            exact_user_wording="USER Review/FAM006_UNIFIED_DEFECT_LEDGER_REPAIR_REVIEW.md contains `the reconstructed \\x0071500 record` instead of `the reconstructed 071500 record`.",
            expected="USER-facing packet text, known-bad identifiers, artifact IDs, and paths must be readable UTF-8 text with no null bytes, non-printable control characters, replacement characters, or corrupted IDs.",
            actual="FAM-006-20260623-120234.zip passed validation while its primary USER review Markdown contained a literal null byte that corrupted the 071500 known-bad identifier.",
            evidence="Known-bad packet FAM-006-20260623-120234.zip SHA D93AADB19ABBDD0973412D301AB14ABF8B115349A352E75868607A32F3CC20FE; exact failing file USER Review/FAM006_UNIFIED_DEFECT_LEDGER_REPAIR_REVIEW.md.",
            surfaces="START_HERE.md; USER Review/*.md; Review Aids/**/*.md; Review Aids/**/*.json; Source Truth Context/**/*.md; packet generated review text",
            root_cause="Packet generation wrote USER-facing text without a final binary/text hygiene scan, so an accidental null byte survived into the upload artifact and the helper still reported green.",
            validator_gap="UDL and false-ACCEPT gates checked structure, known-bad corpus coverage, and proof files but did not reject non-printable control characters or corrupted artifact IDs in USER-facing packet files.",
            repair_target="Add 120234 to known-bad, add packet text hygiene scanning to FAM-006 packet gates, repair the generated review text, and reject the known-bad packet for the control-character defect.",
            acceptance="FAM-006 gates fail for non-printable control bytes, U+FFFD replacement characters, invalid UTF-8, or the corrupted `reconstructed \\x0071500 record` phrase; regenerated packet renders `071500` correctly everywhere.",
            proof="false-ACCEPT gate rejects FAM-006-20260623-120234.zip for packet text hygiene and current UDL gate reports packet text hygiene clean for the regenerated packet.",
            status="CLOSED_WITH_PROOF",
            closure="120234 is admitted as known-bad, the packet text hygiene gate rejects its null byte, and the regenerated USER packet scans clean for non-printable control characters.",
        ),
    ]


def _incident(
    incident_id: str,
    *,
    packet: str,
    sha256: str,
    head: str,
    codex_claim: str,
    rejection: str,
    validator_failed: str,
    artifact: str,
    ledger_row: str,
    comparator: str,
    prevention: str,
    scope: str,
    linked: list[str],
    status: str = "CLOSED_WITH_PROOF",
) -> dict[str, Any]:
    return {
        "incidentId": incident_id,
        "packetPathOrReconstructedRecord": packet,
        "packetSha256": sha256,
        "head": head,
        "codexClaim": codex_claim,
        "userOrChatGPTRejection": rejection,
        "validatorFailed": validator_failed,
        "insufficientProofArtifact": artifact,
        "overclaimedLedgerRow": ledger_row,
        "missedOrMisusedComparator": comparator,
        "fam006PreventionAdded": prevention,
        "preventionScope": scope,
        "globalGovernanceCandidate": (
            "Governance candidate only: promote branch-local UDL, known-bad corpus, "
            "and event-specific false-green incident enforcement into reusable project-wide proof law."
        ),
        "linkedDefectIds": linked,
        "finalIncidentStatus": status,
    }


def seed_incidents(defects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    known_ids = {row["defectId"] for row in defects}
    rows = [
        _incident(
            "FAM006-FGI-001",
            packet="FAM-006-20260622-170147.zip",
            sha256="unknown-preserved-corpus-artifact",
            head="pre-UDL-loop",
            codex_claim="Packet was reviewable/acceptable while evidence was referenced by local paths or missing media.",
            rejection="USER/ChatGPT rejected local-path and missing-media packet proof.",
            validator_failed="Packet hygiene and evidence containment checks before FAM-006 false-ACCEPT hardening.",
            artifact="USER packet Review Aids evidence paths and row_to_evidence_map entries.",
            ledger_row="FAM006-UDL-001",
            comparator="No comparator-specific issue; packet self-containment proof was missing.",
            prevention="Require packet-contained media and packet-relative evidence map entries for green rows.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-001"],
        ),
        _incident(
            "FAM006-FGI-002",
            packet="FAM-006-20260622-192100.zip",
            sha256="unknown-preserved-corpus-artifact",
            head="pre-UDL-loop",
            codex_claim="Root-cause and red-team ledgers were substantive enough for USER review.",
            rejection="USER/ChatGPT rejected generic repeated root-cause/red-team rows.",
            validator_failed="Root-cause/red-team specificity validator before unique-field and defect-class checks.",
            artifact="adjudication_failure_root_cause_ledger.json; internal_visual_red_team_ledger.json",
            ledger_row="FAM006-UDL-002",
            comparator="Comparator not primary; issue was generic evidence adjudication.",
            prevention="Require named defect classes, unique root-cause fields, and known-bad rejection proof.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-002"],
        ),
        _incident(
            "FAM006-FGI-003",
            packet="FAM-006-20260622-194848.zip",
            sha256="unknown-preserved-corpus-artifact",
            head="pre-UDL-loop",
            codex_claim="Crop completeness proof was sufficient.",
            rejection="USER/ChatGPT rejected missing crop rows and self-attested crop proof.",
            validator_failed="Crop completeness validator before required crop-row field enforcement.",
            artifact="crop_completeness_ledger.json; visual_capture_manifest.json",
            ledger_row="FAM006-UDL-003",
            comparator="No comparator-specific issue; crop proof rows were incomplete.",
            prevention="Require crop ledger rows, overlay paths, expected text, and content/scope validation method fields.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-003"],
        ),
        _incident(
            "FAM006-FGI-004",
            packet="FAM-006-20260622-202600.zip",
            sha256="unknown-preserved-corpus-artifact",
            head="pre-UDL-loop",
            codex_claim="Crop overlay proof matched ledger claims.",
            rejection="USER/ChatGPT rejected overlay/ledger contradictions.",
            validator_failed="Crop geometry validator before DOM sibling intersection and adjacent-content checks.",
            artifact="crop_overlays; crop_completeness_ledger.json",
            ledger_row="FAM006-UDL-004",
            comparator="No comparator-specific issue; crop overlay contradicted the ledger.",
            prevention="Reject element crops with undeclared adjacent geometry/text and require relationship crop classification.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-004"],
        ),
        _incident(
            "FAM006-FGI-005",
            packet="FAM-006-20260623-050502.zip",
            sha256="47869093641E2D1432445AD4226F8C1FA60E26B2502E22D9B47D4C7CBBF39A4D",
            head="pre-UDL-loop",
            codex_claim="Expected-text and crop-scope proof was sufficient.",
            rejection="USER/ChatGPT rejected incomplete visible-text and crop-scope/type proof.",
            validator_failed="Expected-text validator before crop-type-specific scope inventory.",
            artifact="crop_completeness_ledger.json; visual_capture_manifest.json",
            ledger_row="FAM006-UDL-005",
            comparator="No comparator-specific issue; crop scope and visible text were incomplete.",
            prevention="Require cropType, declared target scope, visible text audit, and final text verdict.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-005"],
        ),
        _incident(
            "FAM006-FGI-006",
            packet="FAM-006-20260623-060525.zip",
            sha256="D0C45ACAB585541FA0B3A2AB10315B92AA38A789E748B5E0C3CD43F70E1DB69D",
            head="pre-UDL-loop",
            codex_claim="AI Control Center comparator proof was sufficient through broad/context evidence.",
            rejection="USER/ChatGPT rejected comparator proof that was not row-bound.",
            validator_failed="Visual conformance comparator gate before row-bound comparator key/path/finding requirements.",
            artifact="exhaustive_visual_conformance_ledger.json; row_to_evidence_map.json",
            ledger_row="FAM006-UDL-006",
            comparator="AI Control Center/UIREF comparator cited as broad context instead of row-bound focused proof.",
            prevention="Require comparator_evidence_key, comparator path, comparator crop key, owner, proof scope, source-truth rule, and row-specific finding for every green comparator row.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-006"],
        ),
        _incident(
            "FAM006-FGI-007",
            packet="FAM-006-20260623-063715.zip",
            sha256="32BD9A6D2A0C9D70F62892E9A14E7E9FD43678785724381089CF4A118F97932D",
            head="pre-UDL-loop",
            codex_claim="Focused AI Control Center comparator crops were sufficient.",
            rejection="USER/ChatGPT rejected broad, duplicated, mismatched comparator crops.",
            validator_failed="Comparator crop validator before comparator_crop_ledger and hash/scope/content checks.",
            artifact="focused_comparator_crops; comparator_crop_ledger.json missing in known-bad packet.",
            ledger_row="FAM006-UDL-007",
            comparator="AI Control Center focused crop keys reused broad/full screenshot content.",
            prevention="Require comparator_crop_ledger.json with source screenshot, crop rect, target primitive, overlay proof, uniqueness/hash, and final comparator verdict.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-007"],
        ),
        _incident(
            "FAM006-FGI-008",
            packet="FAM-006-20260623-071500.reconstructed-known-bad.json",
            sha256="5605463897BAC7597DE6755DFB824EB7E9BA0B84B6F82A703DEF5FB5679BB373",
            head="pre-UDL-loop",
            codex_claim="Comparator crop proof was complete after Loop X repair.",
            rejection="USER/ChatGPT rejected Loop XI comparator crop content/scope defects.",
            validator_failed="UDL/false-ACCEPT gate before reconstructed latest-known-bad and comparator content/scope recurrence checks.",
            artifact="Review Aids/Evidence/20260623_071352_feature_studio_visual_fail_repair comparator crops and crop ledger.",
            ledger_row="FAM006-UDL-012",
            comparator="AI Control Center comparator crop content included wrong/undeclared adjacent content or wrong proof scope.",
            prevention="Admit reconstructed 071500 known-bad record, link to FAM006-UDL-012, and reject the recurrence by false-ACCEPT gate.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-012", "FAM006-UDL-007"],
        ),
        _incident(
            "FAM006-FGI-009",
            packet="FAM-006-20260623-113615.zip",
            sha256="CFBBFA0CDAC9A6A190DF22F4811BC7E959C3A32C58E5514AF025ED18FB289086",
            head="1e0e927c4aea2d0db31aa5569920e69f799f8f9d",
            codex_claim="FAM-006 UDL packet was ACCEPT / complete after branch-local UDL implementation.",
            rejection="USER/ChatGPT rejected missing latest known-bad, generic false-green incident ledger, and premature comparator defect closure.",
            validator_failed="FAM-006 UDL gate before latest-known-bad admission, event-specific incident count, and recurrence-vs-closure checks.",
            artifact="unified_defect_ledger.json; false_green_incident_ledger.json; unified_defect_ledger_gate.json",
            ledger_row="FAM006-UDL-013",
            comparator="Comparator crop recurrence from 071500 was omitted while UDL-007 remained closed.",
            prevention="Add 113615 to known-bad corpus, require event-specific incidents, require 071500 reconstruction, and require closure proof tied to latest recurrence.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-013", "FAM006-UDL-012"],
        ),
        _incident(
            "FAM006-FGI-010",
            packet="FAM-006-20260623-120234.zip",
            sha256="D93AADB19ABBDD0973412D301AB14ABF8B115349A352E75868607A32F3CC20FE",
            head="dbe5b2903a0ef5a3dfdac1d1d52477aa4d5366f8",
            codex_claim="FAM-006 UDL packet was ACCEPT / complete after latest known-bad coverage repair.",
            rejection="USER/ChatGPT rejected USER-facing packet text hygiene because the primary review file contained `the reconstructed \\x0071500 record`.",
            validator_failed="FAM-006 UDL and false-ACCEPT gates before packet text hygiene scanning of USER-facing Markdown/JSON files.",
            artifact="USER Review/FAM006_UNIFIED_DEFECT_LEDGER_REPAIR_REVIEW.md inside FAM-006-20260623-120234.zip",
            ledger_row="FAM006-UDL-014",
            comparator="No visual comparator issue; text hygiene false green corrupted a known-bad artifact identifier.",
            prevention="Scan packet USER-facing Markdown/JSON for invalid UTF-8, null bytes, non-printable controls, U+FFFD, and corrupted known-bad IDs.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-014"],
        ),
    ]
    for row in rows:
        unknown = sorted(set(row["linkedDefectIds"]) - known_ids)
        if unknown:
            row["finalIncidentStatus"] = "BROKEN_LINK"
            row["brokenLinkedDefectIds"] = unknown
    return rows


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
    known_bad = set()
    if KNOWN_BAD_CORPUS_ROOT.exists():
        known_bad.update(path.name for path in KNOWN_BAD_CORPUS_ROOT.glob("FAM-006-*.zip"))
        known_bad.update(path.name for path in KNOWN_BAD_CORPUS_ROOT.glob("FAM-006-*.reconstructed-known-bad.json"))
    missing_known_bad = sorted(EXPECTED_KNOWN_BAD - known_bad)
    if missing_known_bad:
        failures.append(f"known-bad corpus missing artifacts: {', '.join(missing_known_bad)}")
    for artifact_name, expected_sha in KNOWN_BAD_SHA256.items():
        artifact_path = KNOWN_BAD_CORPUS_ROOT / artifact_name
        if not artifact_path.exists():
            continue
        if artifact_path.suffix.lower() == ".zip":
            import hashlib

            actual_sha = hashlib.sha256(artifact_path.read_bytes()).hexdigest().upper()
            if actual_sha != expected_sha:
                failures.append(f"{artifact_name}: SHA256 mismatch; expected {expected_sha}, found {actual_sha}")
        else:
            try:
                record = json.loads(artifact_path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001 - corrupt known-bad record is a validation failure
                failures.append(f"{artifact_name}: reconstructed known-bad record is unreadable: {exc}")
                continue
            if record.get("External State Schema") != EXTERNAL_STATE_SCHEMA:
                failures.append(f"{artifact_name}: missing External State Schema {EXTERNAL_STATE_SCHEMA}")
            if record.get("originalPacketSha256") != expected_sha:
                failures.append(f"{artifact_name}: reconstructed SHA mismatch")
            if "FAM006-UDL-012" not in record.get("linkedDefectIds", []):
                failures.append(f"{artifact_name}: reconstructed record missing FAM006-UDL-012 link")
            if not record.get("exactRejectionReasons"):
                failures.append(f"{artifact_name}: reconstructed record missing exactRejectionReasons")
    if not incidents:
        failures.append("false-green incident ledger is empty")
    if len(incidents) < 10:
        failures.append(f"false-green incident ledger is too generic: expected at least 10 event-specific rows, found {len(incidents)}")
    for incident in incidents:
        for field in (
            "incidentId",
            "packetPathOrReconstructedRecord",
            "packetSha256",
            "head",
            "codexClaim",
            "userOrChatGPTRejection",
            "validatorFailed",
            "insufficientProofArtifact",
            "overclaimedLedgerRow",
            "missedOrMisusedComparator",
            "fam006PreventionAdded",
            "preventionScope",
            "globalGovernanceCandidate",
            "linkedDefectIds",
            "finalIncidentStatus",
        ):
            if field not in incident or incident[field] in ("", []):
                failures.append(f"{incident.get('incidentId', '<missing>')}: missing {field}")
        if len(incident.get("linkedDefectIds", [])) > 3:
            failures.append(f"{incident.get('incidentId', '<missing>')}: generic incident links too many defects")
        if incident.get("finalIncidentStatus") not in {"CLOSED_WITH_PROOF", "OUT_OF_SCOPE_USER_APPROVAL_REQUIRED"}:
            failures.append(f"{incident.get('incidentId', '<missing>')}: invalid finalIncidentStatus {incident.get('finalIncidentStatus')!r}")
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
            failures.extend(f"packet text hygiene: {failure}" for failure in scan_packet_text_hygiene(packet_root))
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


def _write_reconstructed_known_bad_records() -> None:
    KNOWN_BAD_CORPUS_ROOT.mkdir(parents=True, exist_ok=True)
    record = {
        "External State Schema": EXTERNAL_STATE_SCHEMA,
        "schema": "fam006-reconstructed-known-bad-v1",
        "artifactName": "FAM-006-20260623-071500.zip",
        "reconstructedRecordName": "FAM-006-20260623-071500.reconstructed-known-bad.json",
        "originalPacketPath": "C:/Nexus USER/FAM-006-20260623-071500.zip",
        "originalPacketSha256": "5605463897BAC7597DE6755DFB824EB7E9BA0B84B6F82A703DEF5FB5679BB373",
        "reconstructionReason": "Original ZIP was purged before this repair; external branch-plan receipt and USER/ChatGPT rejection text preserve enough evidence to admit it as known-bad.",
        "userOrChatGPTDisposition": "REPAIR",
        "falseGreenClass": "Loop XI comparator crop content/scope recurrence",
        "proofRoot": "Review Aids/Evidence/20260623_071352_feature_studio_visual_fail_repair",
        "exactRejectionReasons": [
            "Comparator crops still contained undeclared adjacent text or wrong proof-scope content.",
            "The active proof root was later reused by the UDL packet without admitting the 071500 known-bad recurrence.",
            "UDL-007 remained closed on Loop X proof while the Loop XI comparator crop content/scope recurrence was unresolved.",
        ],
        "linkedDefectIds": ["FAM006-UDL-012", "FAM006-UDL-007"],
        "linkedIncidentIds": ["FAM006-FGI-008"],
        "branchPlanReceipt": "C:/Nexus Governance State/branches/feature_fam_006_dashboard_recording_start_stop_local_file/branch_plan.md#FAM-006-Loop-X-Comparator-Media-Proof-Repair-Receipt---2026-06-23",
        "reconstructedKnownBadStatus": "REJECTED_BY_CURRENT_GATE",
    }
    (KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-071500.reconstructed-known-bad.json").write_text(
        json.dumps(record, indent=2) + "\n",
        encoding="utf-8",
    )


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
        "| Incident ID | Packet / Record | SHA256 | Codex Claim | Rejection | Failed Validator / Proof | Overclaimed Row | Prevention Added | Linked Defects | Status |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(
            f"| {row['incidentId']} | {row['packetPathOrReconstructedRecord']} | {row['packetSha256']} | {row['codexClaim']} | {row['userOrChatGPTRejection']} | {row['validatorFailed']} / {row['insufficientProofArtifact']} | {row['overclaimedLedgerRow']} | {row['fam006PreventionAdded']} | {', '.join(row['linkedDefectIds'])} | {row['finalIncidentStatus']} |"
            for row in incidents
        )
        + "\n",
        encoding="utf-8",
    )


def write_external_state() -> dict[str, Any]:
    EXTERNAL_BRANCH_ROOT.mkdir(parents=True, exist_ok=True)
    _write_reconstructed_known_bad_records()
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
