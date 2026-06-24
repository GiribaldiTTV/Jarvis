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
    "FAM-006-20260623-121602.zip",
    "FAM-006-20260623-123110.zip",
    "FAM-006-20260624-121535.zip",
    "FAM-006-20260624-130151.zip",
    "FAM-006-20260624-132551.zip",
    "FAM-006-20260624-135010.zip",
}
KNOWN_BAD_SHA256 = {
    "FAM-006-20260623-071500.reconstructed-known-bad.json": "5605463897BAC7597DE6755DFB824EB7E9BA0B84B6F82A703DEF5FB5679BB373",
    "FAM-006-20260623-113615.zip": "CFBBFA0CDAC9A6A190DF22F4811BC7E959C3A32C58E5514AF025ED18FB289086",
    "FAM-006-20260623-120234.zip": "D93AADB19ABBDD0973412D301AB14ABF8B115349A352E75868607A32F3CC20FE",
    "FAM-006-20260623-121602.zip": "284D92B4DD0F9F7977018B6B10D3E3550B14FAFAD1026DF5CF9E5DFDEED82CB6",
    "FAM-006-20260623-123110.zip": "5DB6C953EFD4A120122B623A0713C8CB106117C21CC4C27B4DDE171DE796628C",
    "FAM-006-20260624-121535.zip": "1ED2108CD4EC129476303C0E267D5B0F2D8A573770675B5BD57157534B65A6D3",
    "FAM-006-20260624-130151.zip": "0929BF53FCAD8F5BC3751BF51CC053351C1103C97D6C8776C288B870FE9BE73F",
    "FAM-006-20260624-132551.zip": "DC225DD9AA20EEB84D4FA2B8185205359D6AA786333CFFFA4E1EA6CF765529DE",
    "FAM-006-20260624-135010.zip": "46008863B7BFE9E4D3B0028AC84A5B62DED4CC30621FAA0BB9311BEEB53F396D",
}
PACKET_REQUIRED_SOURCE_TRUTH_CONTEXT_FILES = {
    "Docs_Main.md",
    "Docs_nexus_startup_contract.md",
    "Docs_phase_governance.md",
    "Docs_branch_plans_README.md",
    "Docs_nexus_vision.md",
    "FAM-002_desktop_interface.md",
    "FAM-006_monitoring_and_hud.md",
    "FAM-006_recording.md",
    "ui_reference_catalog_index.md",
    "UIREF-001_top_level_window_frame.md",
    "UIREF-002_window_control_cluster.md",
    "UIREF-003_control_state_and_selector_grammar.md",
    "UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
    "UIREF-005_design_token_and_shared_rule_baseline.md",
    "UIREF-006_negative_example_and_enforcement_contract.md",
    "Docs_user_test_summary_guidance.md",
    "Docs_validation_helper_registry.md",
    "Docs_incident_patterns.md",
    "Docs_external_operational_state_store_reform_plan.md",
    "feature_fam_006_dashboard_recording_start_stop_local_file.md",
    "external_branch_plan.md",
}
TEXT_HYGIENE_EXTENSIONS = {".json", ".md"}
TEXT_HYGIENE_ROOTS = (
    "START_HERE.md",
    "USER Review",
    "Review Aids",
    "Source Truth Context",
)
CANONICAL_TEXT_REFERENCES = (
    "FAM-006-20260623-071500.zip",
    "071500",
    "the reconstructed 071500 record",
    "FAM-006-20260623-120234.zip",
    "FAM-006-20260623-121602.zip",
    "FAM-006-20260623-123110.zip",
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
        if "\the reconstructed 071500 record" in text:
            failures.append(f"{rel}: tab-corrupted prose `\\the reconstructed 071500 record`")
        if path.suffix.lower() == ".md":
            in_fence = False
            for line_number, line in enumerate(text.splitlines(), start=1):
                stripped = line.lstrip()
                if stripped.startswith("```") or stripped.startswith("~~~"):
                    in_fence = not in_fence
                    continue
                if "\t" not in line:
                    continue
                is_table = stripped.startswith("|")
                if not in_fence and not is_table:
                    failures.append(f"{rel}: tab character in USER-facing prose at line {line_number}")
        elif "\t" in text:
            failures.append(f"{rel}: tab character is not allowed in USER-facing JSON/text")
        control_stripped = "".join(char for char in text if ord(char) >= 32 or char in "\r\n")
        for expected in CANONICAL_TEXT_REFERENCES:
            if expected in control_stripped and expected not in text:
                failures.append(f"{rel}: canonical reference corrupted by hidden control characters: {expected}")
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
    adjacent_sweep: str = "",
) -> dict[str, Any]:
    sweep = adjacent_sweep or (
        f"Row-specific adjacent sweep for {defect_id}: inspected adjacent surfaces/files `{surfaces}`; "
        f"inspected adjacent behavior/proof through `{proof}`; inspected adjacent validator gap `{validator_gap}`; "
        "additional adjacent defects found: none for this row beyond separately linked UDL rows; "
        "repair scope changed: no."
    )
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
        "adjacentDefectSweepResult": sweep,
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
        _defect(
            "FAM006-UDL-015",
            origin="ChatGPT",
            title="USER-facing Markdown prose contains escape-generated tab and corrupted expected phrase",
            exact_user_wording="USER Review/FAM006_UDL_TEXT_HYGIENE_REPAIR_REVIEW.md contains `should read \\the reconstructed 071500 record` instead of `should read the reconstructed 071500 record`.",
            expected="USER-facing Markdown prose must render artifact explanations as normal readable text; tabs/control characters may not replace letters, split canonical references, or corrupt expected phrases outside explicitly allowed code/table contexts.",
            actual="FAM-006-20260623-121602.zip passed validation while the primary USER review Markdown contained a literal tab before `he reconstructed 071500 record`, replacing the leading `t` in `the`.",
            evidence="Known-bad packet FAM-006-20260623-121602.zip SHA 284D92B4DD0F9F7977018B6B10D3E3550B14FAFAD1026DF5CF9E5DFDEED82CB6; exact failing file USER Review/FAM006_UDL_TEXT_HYGIENE_REPAIR_REVIEW.md.",
            surfaces="START_HERE.md; USER Review/*.md; Review Aids/**/*.md; Review Aids/**/*.json; Source Truth Context/**/*.md; generated USER review prose",
            root_cause="The text-hygiene scanner allowed tab characters globally, so a generated escape sequence in prose corrupted the review sentence while still passing the packet gate.",
            validator_gap="No Markdown context-aware tab rule and no canonical phrase/reference integrity check for `the reconstructed 071500 record` and the active known-bad packet IDs.",
            repair_target="Add 121602 to known-bad, reject tabs in Markdown prose outside fenced code or table rows, and require canonical artifact/phrase integrity for known-bad references.",
            acceptance="FAM-006 gates reject 121602 for the exact tab-corrupted phrase; regenerated packet has no prose tabs and renders `the reconstructed 071500 record` correctly.",
            proof="false-ACCEPT gate rejects FAM-006-20260623-121602.zip for packet text hygiene and current packet text hygiene scan passes with canonical references intact.",
            status="CLOSED_WITH_PROOF",
            closure="121602 is admitted as known-bad, the packet text hygiene gate rejects its prose tab corruption, and the regenerated USER packet scans clean for tabs/control characters in prose.",
        ),
        _defect(
            "FAM006-UDL-016",
            origin="ChatGPT",
            title="Required startup contract missing from packet Source Truth Context",
            exact_user_wording="FAM-006-20260623-123110.zip omitted Docs/nexus_startup_contract.md from Source Truth Context even though the task required it for false-green prevention, ChatGPT/Codex behavior, prompt workflow, loader alignment, and self-adjudication.",
            expected="When startup contract, prompt workflow, loader continuity, ChatGPT/Codex behavior, or self-adjudication are in scope, the USER packet must include Docs/nexus_startup_contract.md in Source Truth Context or include a source-truth-backed omission reason.",
            actual="FAM-006-20260623-123110.zip passed validation while Source Truth Context lacked Docs_nexus_startup_contract.md and contained no omission reason.",
            evidence="Known-bad packet FAM-006-20260623-123110.zip SHA 5DB6C953EFD4A120122B623A0713C8CB106117C21CC4C27B4DDE171DE796628C; Source Truth Context listing omitted Docs_nexus_startup_contract.md.",
            surfaces="Source Truth Context/Docs_nexus_startup_contract.md; START_HERE.md; USER Review/FAM006_UDL_TEXT_HYGIENE_REPAIR_II_REVIEW.md; UDL packet context manifest.",
            root_cause="The packet gate required common governance and UI context files but did not encode startup contract as required when false-green/self-adjudication prompt behavior was explicitly in scope.",
            validator_gap="No FAM-006-local packet source-truth context completeness rule for Docs_nexus_startup_contract.md.",
            repair_target="Add 123110 to known-bad, require Docs_nexus_startup_contract.md in packet Source Truth Context, and include it in regenerated UDL repair packets.",
            acceptance="FAM-006 gates reject 123110 for missing startup contract context and pass only when regenerated packet context includes Docs_nexus_startup_contract.md.",
            proof="false-ACCEPT gate rejects FAM-006-20260623-123110.zip for missing startup contract context; current packet source context includes Docs_nexus_startup_contract.md.",
            status="CLOSED_WITH_PROOF",
            closure="123110 is admitted as known-bad, the packet source-context gate rejects its missing startup contract context, and the regenerated USER packet includes Docs_nexus_startup_contract.md.",
        ),
        _defect(
            "FAM006-UDL-017",
            origin="ChatGPT",
            title="UDL adjacent-defect sweep fields are generic and repeated",
            exact_user_wording="Every UDL row repeated `Adjacent proof path inspected: packet evidence, crop/overlay/text/scope, visual ledger, red-team/root-cause row, false-ACCEPT gate.` instead of a row-specific adjacent-defect sweep.",
            expected="Every UDL defect row must name row-specific adjacent surfaces/files, adjacent behavior, adjacent proof artifacts, adjacent validators or ledger rows, additional defects found or exact reason none were found, linked UDL IDs added or reopened, and whether repair scope changed.",
            actual="FAM-006-20260623-123110.zip passed validation even though adjacentDefectSweepResult was copied across unrelated UDL rows and did not substantively sweep adjacent defects row by row.",
            evidence="Known-bad packet FAM-006-20260623-123110.zip SHA 5DB6C953EFD4A120122B623A0713C8CB106117C21CC4C27B4DDE171DE796628C; embedded Review Aids/Unified Defect Ledger/unified_defect_ledger.json.",
            surfaces="unified_defect_ledger.json; UNIFIED_DEFECT_LEDGER.md; false-ACCEPT gate; UDL packet gate.",
            root_cause="The UDL helper generated one boilerplate adjacent sweep string inside the shared defect constructor and the gate checked field presence instead of row-specific content.",
            validator_gap="No duplicate/generic adjacentDefectSweepResult rejection and no minimum row-specific token checks.",
            repair_target="Generate row-specific adjacent sweep text and reject duplicated or category-list-only adjacent sweeps.",
            acceptance="FAM-006 gates reject 123110 for generic repeated adjacent sweeps and pass only when all current UDL rows have unique, substantive adjacent sweep results.",
            proof="UDL gate reports no duplicate adjacentDefectSweepResult values and false-ACCEPT gate rejects 123110 for the embedded generic sweep recurrence.",
            status="CLOSED_WITH_PROOF",
            closure="123110 is admitted as known-bad, generic repeated adjacent sweeps are rejected, and regenerated UDL rows carry row-specific adjacent sweep results.",
            adjacent_sweep=(
                "Row-specific adjacent sweep for FAM006-UDL-017: inspected adjacent surfaces/files `unified_defect_ledger.json`, "
                "`UNIFIED_DEFECT_LEDGER.md`, the shared `_defect` constructor, and packet-embedded UDL rows; "
                "adjacent behavior inspected: row-specific defect closure versus copied category-list proof; "
                "adjacent proof artifacts inspected: FAM-006-20260623-123110.zip embedded UDL, current regenerated UDL JSON, "
                "and false-ACCEPT validator gate output; additional adjacent defects found: FAM006-UDL-016 for missing startup contract context; "
                "linked UDL IDs added/reopened: FAM006-UDL-016 and FAM006-UDL-017; repair scope changed: yes, packet source-context and adjacent-sweep gates both hardened."
            ),
        ),
        _defect(
            "FAM006-UDL-018",
            origin="USER/ChatGPT",
            title="Full-desktop proof contradicted focused visual ACCEPT packet",
            exact_user_wording="FAM-006-20260624-121535.zip claimed ACCEPT, but full-desktop evidence showed Log Viewer Studio scale/dead-space and child-window placement/composition failures that focused crops hid.",
            expected="Material Recording Studio / Log Viewer Studio visual packets must treat full-desktop or full-window context as controlling evidence for scale, placement, dead space, parent/child relationship, and composition; a focused crop cannot green-light a contradicted visual claim.",
            actual="The 121535 packet passed focused row-grammar and comparator gates while the included full-desktop screenshot exposed obvious visual contradictions.",
            evidence="Known-bad packet FAM-006-20260624-121535.zip SHA 1ED2108CD4EC129476303C0E267D5B0F2D8A573770675B5BD57157534B65A6D3; full_desktop_recording_and_log_viewer_after_repair.png.",
            surfaces="Recording Studio; Log Viewer Studio; full-desktop proof; visual conformance packet; child-window placement/options.",
            root_cause="The branch-local visual gates required focused evidence and crop/comparator completeness but did not require a full-desktop red-team contradiction ledger before accepting visual readiness.",
            validator_gap="No full-context visual false-green packet gate, no child-window placement doctrine check, and no requirement to classify USER-reported full-desktop defects before renewed LV.",
            repair_target="Admit 121535 as known-bad, require full-desktop false-green packet validation, add branch-local source-truth carrydown, and packet visual/placement options for USER review.",
            acceptance="FAM-006 full-desktop false-green helper rejects missing full-context evidence, missing USER defect rows, generic root-cause rows, missing placement doctrine, and missing visual options.",
            proof="dev/orin_fam006_full_desktop_false_green_review.py validates the regenerated false-green packet and external state records the known-bad 121535 corpus copy.",
            status="CLOSED_WITH_PROOF",
            closure="121535 is admitted as known-bad, full-desktop contradiction handling is packeted with media and source-truth carrydown, and renewed LV remains blocked pending USER review.",
            adjacent_sweep=(
                "Row-specific adjacent sweep for FAM006-UDL-018: inspected adjacent surfaces/files `Docs/family_feature_visions/FAM-006_recording.md`, "
                "`Docs/validation_helper_registry.md`, `dev/orin_fam006_full_desktop_false_green_review.py`, the 121535 rejected packet media, "
                "and external branch_plan.md; adjacent behavior inspected: crop-only acceptance, full-desktop contradiction, child-window placement options, "
                "USER packet media inclusion, proof artifact completeness, and validator/helper full-context enforcement; additional adjacent defects found: none beyond this full-context false-green class; linked UDL IDs added/reopened: "
                "FAM006-UDL-018; repair scope changed: yes, branch-local FFV, helper registry, helper, external state, and USER packet were updated."
            ),
        ),
        _defect(
            "FAM006-UDL-019",
            origin="USER/ChatGPT",
            title="Visual option packet used clipped text cards instead of rendered option evidence",
            exact_user_wording="FAM-006-20260624-130151.zip had the right false-green direction, but the visual/placement option packet was not reviewable enough because the options board was mostly clipped text cards and validation-output evidence was incomplete.",
            expected="When visual, spatial, placement, nested-card, or doorway-layout decisions are under USER review, the packet must include actual rendered option media, full desktop/context renders where placement matters, and command/cwd/timestamp/exit-code/stdout/stderr validation output evidence for claimed validations.",
            actual="The 130151 packet contained a mostly text-card options board, several clipped option cards, no separate rendered A/B/C option media, and incomplete in-packet validation outputs.",
            evidence="Known-bad packet FAM-006-20260624-130151.zip SHA 0929BF53FCAD8F5BC3751BF51CC053351C1103C97D6C8776C288B870FE9BE73F; USER/ChatGPT REPAIR verdict on full-desktop option packet.",
            surfaces="FAM-006 USER packet; visual/placement options board; nested-card inheritance options; child-window placement diagrams; Log Viewer doorway layout options; validation output evidence.",
            root_cause="The helper generated a text-summary contact sheet for decisions that were inherently visual/spatial, and the packet gate accepted the presence of an options board without requiring option-specific rendered media or validation-output records.",
            validator_gap="No hard failure for text-only visual options, clipped/unreadable option cards, missing B placement diagrams, missing A/C rendered comparisons, or validation-output summaries without command/cwd/timestamp/exit-code/stdout/stderr.",
            repair_target="Admit 130151 as known-bad, require A1/A2/A3, B1/B2/B3, and C1/C2/C3 rendered media, require in-packet validation-output records, and regenerate the USER packet from a purged folder.",
            acceptance="FAM-006 gates fail when rendered option media or validation-output evidence is missing and pass only when the regenerated packet includes actual media for every required option.",
            proof="dev/orin_fam006_full_desktop_false_green_review.py validates individual option renders, packet-contained validation outputs, and the 130151 known-bad corpus copy.",
            status="CLOSED_WITH_PROOF",
            closure="130151 is admitted as known-bad; the repaired packet helper generates actual A/B/C option renders, full placement diagrams, validation-output evidence, and a new timestamped USER packet.",
            adjacent_sweep=(
                "Row-specific adjacent sweep for FAM006-UDL-019: inspected adjacent surfaces/files `dev/orin_fam006_full_desktop_false_green_review.py`, "
                "`Docs/family_feature_visions/FAM-006_recording.md`, `Docs/validation_helper_registry.md`, 130151 rejected packet output, and active USER packet layout; "
                "adjacent behavior inspected: text-only option cards, clipped visual decision evidence, missing placement diagrams, missing option-specific renders, missing validation-output records, and stale ZIP purge behavior; "
                "adjacent proof artifacts inspected: regenerated option PNGs, packet media manifest, validation output JSON/TXT files, known-bad corpus SHA proof, validator gate output, and external full_desktop_false_green_review_manifest.json; "
                "additional adjacent defects found: none beyond the 130151 option-packet false-green class and already linked FAM006-UDL-018 full-desktop contradiction; "
                "linked UDL IDs added/reopened: FAM006-UDL-018 and FAM006-UDL-019; repair scope changed: yes, packet helper, known-bad expectations, false-green incident ledger, and external packet receipt were hardened."
            ),
        ),
        _defect(
            "FAM006-UDL-020",
            origin="USER/ChatGPT",
            title="Selected option packet failed to preserve USER-selected semantics",
            exact_user_wording="FAM-006-20260624-132551.zip was improved, but the selected direction needed to be recorded with revisions before runtime repair: A2 revised, B2, and C2 revised with exact labels and no superseded helper/open-option wording.",
            expected="Once USER selects A2 revised / B2 / C2 revised, the packet must preserve exact selected semantics, exact Recording Studio ACTION-002 label `OPEN LOG VIEWER STUDIO`, A2 TARGET/STATE separation with no bottom helper copy, C2 explicit `OPEN NATIVE LOGS` and `OPEN EXPORTED LOGS` labels, rejected/deferred option dispositions, and clean post-commit/post-push proof.",
            actual="The 132551 packet still behaved partly like an option-recommendation packet, selected renders/text could regress labels, C2 could use generic OPEN labels, and in-packet Git proof could remain pre-commit/dirty if generated before durability.",
            evidence="Known-bad packet FAM-006-20260624-132551.zip SHA DC225DD9AA20EEB84D4FA2B8185205359D6AA786333CFFFA4E1EA6CF765529DE; USER/ChatGPT REPAIR verdict on full-desktop option selection / packet evidence repair.",
            surfaces="FAM-006 USER packet; selected A2 render; selected B2 placement render; selected C2 render; selected-direction summary; validation output evidence; external full_desktop_false_green_review_manifest.json.",
            root_cause="The packet helper validated that rendered media existed but did not distinguish open option recommendation evidence from a USER-selected direction contract with exact semantic labels and post-push clean proof.",
            validator_gap="No hard failure for missing selected-direction JSON/Markdown, superseded open-option recommendation wording, missing rejected/deferred dispositions, A2 helper-copy regression, C2 generic OPEN labels, ACTION-002 label drift, or dirty git-status proof captured inside validation outputs.",
            repair_target="Admit 132551 as known-bad, require selected-direction summary files, require exact A2/B2/C2 revised semantics, require rejected/deferred dispositions, require clean post-push Git validation output, and regenerate the USER packet from a purged folder after helper commit/push.",
            acceptance="FAM-006 gates fail when selected-direction files, exact semantic labels, post-push clean proof, or packet-contained validation outputs are missing or superseded recommendation wording remains.",
            proof="dev/orin_fam006_full_desktop_false_green_review.py validates selected-direction summary, A2/B2/C2 text, exact labels, known-bad 132551 corpus copy, packet-contained validation outputs, and clean upstream proof.",
            status="CLOSED_WITH_PROOF",
            closure="132551 is admitted as known-bad; the repaired helper records selected A2 revised / B2 / C2 revised direction, validates exact labels and dispositions, and requires clean post-push status proof inside the regenerated packet.",
            adjacent_sweep=(
                "Row-specific adjacent sweep for FAM006-UDL-020: inspected adjacent surfaces/files `dev/orin_fam006_full_desktop_false_green_review.py`, "
                "`dev/orin_fam006_unified_defect_ledger.py`, `dev/orin_fam006_false_accept_regression_gate.py`, active USER packet layout, and external manifest receipt; "
                "adjacent behavior inspected: selected-direction semantics, exact A2 ACTION-002 label, A2 TARGET/STATE separation, A2 bottom helper copy exclusion, B2 placement doctrine, C2 explicit row action labels, rejected/deferred option dispositions, post-push clean Git proof, and packet-contained validation-output evidence; "
                "additional adjacent defects found by validator gate output: none beyond the selected-direction false-green class and already linked FAM006-UDL-018 / FAM006-UDL-019; "
                "linked UDL IDs added/reopened: FAM006-UDL-018, FAM006-UDL-019, and FAM006-UDL-020; repair scope changed: yes, packet helper, known-bad expectations, false-green incident ledger, and external packet receipt were hardened."
            ),
        ),
        _defect(
            "FAM006-UDL-021",
            origin="USER/ChatGPT",
            title="Selected-direction packet chose fake Log Viewer row-action semantics",
            exact_user_wording="FAM-006-20260624-135010.zip correctly recorded A2 revised and B2, but Log Viewer C2 revised is rejected because inline/right-aligned row actions make the deferred Log Viewer Studio look like it has row-level data/actions before a real viewer exists.",
            expected="The selected Log Viewer direction must be a LOG-A-derived doorway shell: one middle/status row `VIEWER - Deferred`, bottom `OPEN NATIVE LOGS` and `OPEN EXPORTED LOGS` actions, no fake native/export information rows, no local path display by default, no graph/export customization, no previous-log selection, no native-log reading from Recording Studio, no direct exported-log opening from Recording Studio, and no fake full-viewer workspace behavior.",
            actual="The 135010 packet treated C2 revised inline/right-aligned native/export row actions as selected, which implied row-level viewer data/functionality before current-branch scope includes a real Log Viewer data surface.",
            evidence="Known-bad packet FAM-006-20260624-135010.zip SHA 46008863B7BFE9E4D3B0028AC84A5B62DED4CC30621FAA0BB9311BEEB53F396D; USER/ChatGPT REPAIR verdict on selected-direction Log Viewer doorway correction.",
            surfaces="FAM-006 USER packet; selected-direction summary; Log Viewer selected render; visual/placement options board; external full_desktop_false_green_review_manifest.json.",
            root_cause="The packet helper allowed an option selected for visual row/action proximity to override the source-truth boundary that current Log Viewer Studio is only a doorway shell, not a data-row/action surface.",
            validator_gap="No hard failure for C2-selected drift, missing `VIEWER - Deferred`, bottom action row absence, fake native/export data rows, local-path default display, or Recording Studio implying direct native/export log actions.",
            repair_target="Admit 135010 as known-bad, reject C2 revised as selected, require corrected Log Viewer doorway shell media and selected-direction JSON/Markdown, and regenerate the USER packet from a purged folder after helper commit/push.",
            acceptance="FAM-006 gates fail when the selected Log Viewer direction lacks `VIEWER - Deferred`, uses inline/right-aligned row actions as selected, displays fake data rows, or implies full-viewer/native-export functionality before source truth admits it.",
            proof="dev/orin_fam006_full_desktop_false_green_review.py validates the corrected doorway shell render, selected-direction summary, 135010 known-bad corpus copy, packet-contained validation outputs, and clean upstream proof.",
            status="CLOSED_WITH_PROOF",
            closure="135010 is admitted as known-bad; the repaired helper records A2 revised / B2 / corrected Log Viewer doorway shell, rejects C2 revised, validates `VIEWER - Deferred` and bottom action labels, and requires clean post-push status proof inside the regenerated packet.",
            adjacent_sweep=(
                "Row-specific adjacent sweep for FAM006-UDL-021: inspected adjacent surfaces/files `dev/orin_fam006_full_desktop_false_green_review.py`, "
                "`dev/orin_fam006_unified_defect_ledger.py`, `dev/orin_fam006_false_accept_regression_gate.py`, `Docs/family_feature_visions/FAM-006_recording.md`, "
                "`Docs/validation_helper_registry.md`, active USER packet layout, and external manifest receipt; adjacent behavior inspected: selected Log Viewer semantics, C2 rejection, "
                "`VIEWER - Deferred` status row, bottom `OPEN NATIVE LOGS` / `OPEN EXPORTED LOGS` actions, fake native/export row exclusion, local path display exclusion, "
                "Recording Studio direct native/export action exclusion, rejected/deferred option disposition, post-push clean Git proof, and packet-contained validation-output evidence; "
                "additional adjacent defects found: none beyond the selected-direction doorway false-green class and already linked FAM006-UDL-018 / FAM006-UDL-019 / FAM006-UDL-020; "
                "linked UDL IDs added/reopened: FAM006-UDL-018, FAM006-UDL-019, FAM006-UDL-020, and FAM006-UDL-021; repair scope changed: yes, packet helper, known-bad expectations, false-green incident ledger, and external packet receipt were hardened."
            ),
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
        _incident(
            "FAM006-FGI-011",
            packet="FAM-006-20260623-121602.zip",
            sha256="284D92B4DD0F9F7977018B6B10D3E3550B14FAFAD1026DF5CF9E5DFDEED82CB6",
            head="65e420fc8a214df35ae84de29ee39f8687e166bf",
            codex_claim="FAM-006 UDL packet text-hygiene repair was ACCEPT / complete after null-byte prevention.",
            rejection="USER/ChatGPT rejected USER-facing Markdown prose corruption because a literal tab replaced the leading `t` in `the reconstructed 071500 record`.",
            validator_failed="FAM-006 packet text hygiene gate before Markdown prose tab-context and canonical phrase integrity checks.",
            artifact="USER Review/FAM006_UDL_TEXT_HYGIENE_REPAIR_REVIEW.md inside FAM-006-20260623-121602.zip",
            ledger_row="FAM006-UDL-015",
            comparator="No visual comparator issue; text hygiene false green corrupted prose and the canonical 071500 phrase.",
            prevention="Reject tabs in USER-facing Markdown prose outside code fences/tables and require canonical known-bad artifact/phrase integrity.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-015"],
        ),
        _incident(
            "FAM006-FGI-012",
            packet="FAM-006-20260623-123110.zip",
            sha256="5DB6C953EFD4A120122B623A0713C8CB106117C21CC4C27B4DDE171DE796628C",
            head="c4a4b54585a82235cc7dc13ed249a4c107a5a4c7",
            codex_claim="FAM-006 UDL text-hygiene repair II was ACCEPT / complete after fixing the tab-corrupted phrase.",
            rejection="USER/ChatGPT rejected missing Docs/nexus_startup_contract.md packet context and generic repeated adjacent-defect sweep fields.",
            validator_failed="FAM-006 UDL and false-ACCEPT gates before startup-contract source-context and row-specific adjacent-sweep enforcement.",
            artifact="Source Truth Context inside FAM-006-20260623-123110.zip; embedded Review Aids/Unified Defect Ledger/unified_defect_ledger.json.",
            ledger_row="FAM006-UDL-016,FAM006-UDL-017",
            comparator="No visual comparator issue; UDL packet false green came from missing required source-truth context and copied adjacent-sweep prose.",
            prevention="Require Docs_nexus_startup_contract.md in this scope and reject duplicated/generic adjacentDefectSweepResult fields.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-016", "FAM006-UDL-017"],
        ),
        _incident(
            "FAM006-FGI-013",
            packet="FAM-006-20260624-121535.zip",
            sha256="1ED2108CD4EC129476303C0E267D5B0F2D8A573770675B5BD57157534B65A6D3",
            head="9c487aef9240a648183acf519b6cd95dfdd4caa7",
            codex_claim="FAM-006 row-grammar / footprint repair packet was ACCEPT and ready for USER review.",
            rejection="USER/ChatGPT rejected the packet because full-desktop evidence exposed Log Viewer scale/dead-space, disconnected composition, and placement/context issues hidden by focused crops.",
            validator_failed="FAM-006 visual conformance and false-ACCEPT gates before full-desktop contradiction and child-window placement option enforcement.",
            artifact="Review Aids/Evidence/20260624_121443_feature_studio_visual_fail_repair/full_desktop_recording_and_log_viewer_after_repair.png inside FAM-006-20260624-121535.zip.",
            ledger_row="FAM006-UDL-018",
            comparator="Full-desktop proof contradicted focused crop/comparator proof for material visual acceptance.",
            prevention="Require branch-local full-desktop false-green review packet, row-specific root-cause ledger, USER defect classification, placement doctrine, and visual options before renewed LV.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-018"],
        ),
        _incident(
            "FAM006-FGI-014",
            packet="FAM-006-20260624-130151.zip",
            sha256="0929BF53FCAD8F5BC3751BF51CC053351C1103C97D6C8776C288B870FE9BE73F",
            head="1e6f99cfc7dd02b37da77010b22cbdf2085042b6",
            codex_claim="FAM-006 full-desktop false-green review packet was ACCEPT / reviewable after adding an options board.",
            rejection="USER/ChatGPT rejected the packet because visual/placement options were mostly text cards, cards were clipped, actual rendered option media were missing, and validation-output evidence was incomplete.",
            validator_failed="FAM-006 full-desktop false-green packet helper before rendered option media and validation-output evidence gates.",
            artifact="Review Aids/Evidence/Options/visual_and_placement_options_board.png inside FAM-006-20260624-130151.zip.",
            ledger_row="FAM006-UDL-019",
            comparator="The packet described A/B/C decisions instead of showing rendered nested-card, placement, and Log Viewer doorway alternatives.",
            prevention="Require actual rendered A1/A2/A3, B1/B2/B3, and C1/C2/C3 media plus command/cwd/timestamp/exit-code/stdout/stderr validation output records.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-019", "FAM006-UDL-018"],
        ),
        _incident(
            "FAM006-FGI-015",
            packet="FAM-006-20260624-132551.zip",
            sha256="DC225DD9AA20EEB84D4FA2B8185205359D6AA786333CFFFA4E1EA6CF765529DE",
            head="a125b162265a8d8c0bdb9b6e4b614a1409987e41",
            codex_claim="FAM-006 full-desktop option packet repair was ACCEPT / reviewable after rendered option media were added.",
            rejection="USER/ChatGPT rejected the packet because USER-selected A2 revised / B2 / C2 revised direction and exact selected semantics were not durably recorded before runtime repair.",
            validator_failed="FAM-006 full-desktop false-green packet helper before selected-direction semantic contract and post-push clean-proof gates.",
            artifact="Review Aids/VISUAL_AND_PLACEMENT_OPTIONS.md and rendered selected option media inside FAM-006-20260624-132551.zip.",
            ledger_row="FAM006-UDL-020",
            comparator="The packet showed improved option renders but still behaved like open recommendation evidence rather than a selected-direction contract.",
            prevention="Require selected-direction JSON/Markdown, exact A2/B2/C2 revised labels and dispositions, known-bad 132551 replay, and clean post-push validation-output proof.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-020", "FAM006-UDL-019", "FAM006-UDL-018"],
        ),
        _incident(
            "FAM006-FGI-016",
            packet="FAM-006-20260624-135010.zip",
            sha256="46008863B7BFE9E4D3B0028AC84A5B62DED4CC30621FAA0BB9311BEEB53F396D",
            head="98092b3aa831ad9a8077c6c87c68973c31355cae",
            codex_claim="FAM-006 selected-direction packet was ACCEPT / reviewable after A2 revised, B2, and C2 revised were recorded.",
            rejection="USER/ChatGPT rejected the packet because C2 revised inline/right-aligned row actions imply Log Viewer row-level data/functionality before the current branch implements a real Log Viewer data surface.",
            validator_failed="FAM-006 full-desktop false-green packet helper before corrected Log Viewer doorway-shell semantic gate.",
            artifact="Review Aids/SELECTED_DIRECTION_SUMMARY.md, Review Aids/VISUAL_AND_PLACEMENT_OPTIONS.md, and rendered C2 selected media inside FAM-006-20260624-135010.zip.",
            ledger_row="FAM006-UDL-021",
            comparator="The packet selected a row-action design when the source-truth-correct current branch direction is a simple doorway shell with `VIEWER - Deferred` and bottom actions.",
            prevention="Require corrected Log Viewer doorway shell media, `VIEWER - Deferred`, bottom `OPEN NATIVE LOGS` / `OPEN EXPORTED LOGS` actions, C2 rejection, fake-row exclusion, and known-bad 135010 replay.",
            scope="FAM-006-local",
            linked=["FAM006-UDL-021", "FAM006-UDL-020", "FAM006-UDL-019", "FAM006-UDL-018"],
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
    sweep_values: dict[str, list[str]] = {}
    generic_sweep = (
        "Adjacent proof path inspected: packet evidence, crop/overlay/text/scope, "
        "visual ledger, red-team/root-cause row, false-ACCEPT gate."
    )
    for row in defects:
        defect_id = str(row.get("defectId", "<missing>"))
        sweep = str(row.get("adjacentDefectSweepResult", "")).strip()
        sweep_values.setdefault(sweep, []).append(defect_id)
        if sweep == generic_sweep:
            failures.append(f"{defect_id}: adjacentDefectSweepResult is the rejected generic copied sweep")
        required_tokens = (
            "adjacent",
            "surfaces",
            "proof",
            "validator",
            "additional",
            "defects",
            "repair scope",
        )
        missing_tokens = [token for token in required_tokens if token not in sweep.casefold()]
        if missing_tokens:
            failures.append(
                f"{defect_id}: adjacentDefectSweepResult missing row-specific tokens: {', '.join(missing_tokens)}"
            )
    for sweep, defect_ids in sweep_values.items():
        if sweep and len(defect_ids) > 1:
            failures.append(
                "duplicate adjacentDefectSweepResult across unrelated defects: "
                f"{', '.join(defect_ids)}"
            )
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
    if len(incidents) < 11:
        failures.append(f"false-green incident ledger is too generic: expected at least 11 event-specific rows, found {len(incidents)}")
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
            context_root = packet_root / "Source Truth Context"
            if not context_root.exists():
                failures.append("packet missing Source Truth Context folder")
            else:
                context_present = {
                    path.name
                    for path in context_root.glob("*")
                    if path.is_file()
                }
                missing_context = sorted(PACKET_REQUIRED_SOURCE_TRUTH_CONTEXT_FILES - context_present)
                if missing_context:
                    failures.append(
                        "packet Source Truth Context missing required files: "
                        + ", ".join(missing_context)
                    )
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
