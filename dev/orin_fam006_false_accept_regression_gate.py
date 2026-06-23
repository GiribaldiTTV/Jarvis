"""FAM-006 false-ACCEPT regression gate.

This branch-local gate prevents the specific returned-UTS failure loop where a
packet claims Studio visual ACCEPT while the packet evidence still contains
summary-only root cause, assertion-only red-team rows, local-only proof, weak
resize proof, clipped crops, or progress-language green claims.
"""

from __future__ import annotations

import argparse
import json
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image


USER_ROOT = Path("C:/Nexus USER")
DEFAULT_CURRENT_PACKET = USER_ROOT / "FAM-006"
EXTERNAL_BRANCH_ROOT = Path(
    "C:/Nexus Governance State/branches/feature_fam_006_dashboard_recording_start_stop_local_file"
)
KNOWN_BAD_CORPUS_ROOT = EXTERNAL_BRANCH_ROOT / "false_accept_regression_corpus"
KNOWN_BAD_ZIPS = [
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-173545.zip",
    USER_ROOT / "FAM-006-20260622-173545.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-170147.zip",
    USER_ROOT / "FAM-006-20260622-170147.zip",
]

REQUIRED_RED_TEAM_FIELDS = {
    "rowId",
    "surface",
    "elementGroup",
    "sourceTruthRequirement",
    "screenshotEvidenceFile",
    "negativeQuestion",
    "defectLookedFor",
    "observedFinding",
    "finalDisposition",
    "whyDefectAbsentIfPass",
    "exactRepairIfRequired",
    "checkThatWouldFailIfAppearsAgain",
}

REQUIRED_ROOT_CAUSE_FIELDS = {
    "defectId",
    "falseAcceptPacketOrEvidence",
    "visibleDefectDescription",
    "whyCodexMissedIt",
    "failedStep",
    "missingCheck",
    "repairMade",
    "proofNewCheckRejectsKnownBadExample",
    "currentStatus",
    "disposition",
}

REQUIRED_EVIDENCE_KEYS = {
    "recording-full-window",
    "recording-window-chrome",
    "recording-primary-action",
    "recording-target-truth",
    "recording-log-route",
    "log-viewer-full-window",
    "log-viewer-window-chrome",
    "native-log-destination-action",
    "exported-log-destination-action",
    "log-viewer-action-status",
    "log-viewer-resize-before",
    "log-viewer-resize-during",
    "log-viewer-resize-after",
    "full-desktop-combined",
    "contact-sheet",
}

FORBIDDEN_GREEN_WORDS = (
    "better",
    "closer",
    "improved",
    "mostly",
    "cleaner",
    "good enough",
    "clean enough",
    "green enough",
    "looks okay",
    "looks acceptable",
)

FORBIDDEN_PRODUCT_COPY = (
    "ready when user exports",
    "user exports",
)

REQUIRED_RED_TEAM_DEFECT_CLASSES = {
    "log-viewer-user-export-copy",
    "log-viewer-card-footer-contradiction",
    "recording-action-hierarchy",
    "recording-status-panel-feel",
    "local-absolute-primary-proof",
    "broad-row-evidence-map",
    "visual-ledger-overcredit",
}

MIN_ROOT_CAUSE_UNIQUE_FIELDS = (
    "whyCodexMissedIt",
    "failedStep",
    "missingCheck",
    "repairMade",
    "proofNewCheckRejectsKnownBadExample",
)


@dataclass
class PacketInspection:
    label: str
    path: str
    accepted: bool
    failures: list[str]
    artifactSummary: dict[str, Any]


def _read_json(path: Path) -> tuple[dict[str, Any] | list[Any] | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:  # noqa: BLE001 - validation reports exact parse failure
        return None, str(exc)


def _find_one(root: Path, pattern: str) -> Path | None:
    matches = sorted(root.glob(pattern))
    return matches[0] if matches else None


def _image_size(path: Path) -> tuple[int, int] | None:
    try:
        with Image.open(path) as image:
            return image.size
    except Exception:
        return None


def _inspect_packet_root(root: Path, label: str) -> PacketInspection:
    failures: list[str] = []
    evidence_roots = sorted((root / "Review Aids" / "Evidence").glob("*")) if (root / "Review Aids" / "Evidence").exists() else []
    evidence_root = next((path for path in evidence_roots if path.is_dir()), None)
    if evidence_root is None:
        failures.append("missing Review Aids/Evidence proof root")
        evidence_root = root

    row_map_path = _find_one(root, "Review Aids/Evidence/**/row_to_evidence_map.json")
    manifest_path = _find_one(root, "Review Aids/Evidence/**/visual_capture_manifest.json")
    red_team_path = _find_one(root, "Review Aids/Evidence/**/internal_visual_red_team_ledger.json")
    root_cause_path = _find_one(root, "Review Aids/Evidence/**/adjudication_failure_root_cause_ledger.json")
    visual_ledger_path = _find_one(root, "Review Aids/exhaustive_visual_conformance_ledger.json")
    is_known_bad = label.startswith("known-bad:")

    row_map: dict[str, Any] = {}
    if row_map_path is None:
        failures.append("missing row_to_evidence_map.json")
    else:
        data, error = _read_json(row_map_path)
        if error or not isinstance(data, dict):
            failures.append(f"invalid row_to_evidence_map.json: {error}")
        else:
            row_map = data
            missing = sorted(REQUIRED_EVIDENCE_KEYS - set(row_map))
            if missing:
                failures.append(f"row_to_evidence_map missing keys: {', '.join(missing)}")
            for key, value in sorted(row_map.items()):
                text = str(value or "").strip()
                if not text:
                    failures.append(f"row_to_evidence_map key {key} has empty path")
                    continue
                if Path(text).is_absolute():
                    failures.append(f"row_to_evidence_map key {key} uses local absolute path")
                    continue
                target = row_map_path.parent / text
                if not target.exists():
                    failures.append(f"row_to_evidence_map key {key} target missing: {text}")
                    continue
                if target.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                    size = _image_size(target)
                    if size is None:
                        failures.append(f"row_to_evidence_map key {key} image unreadable")
                    elif key != "contact-sheet" and (size[0] < 220 or size[1] < 60):
                        failures.append(f"row_to_evidence_map key {key} image too small/clipped: {size[0]}x{size[1]}")

    if manifest_path is None:
        failures.append("missing visual_capture_manifest.json")
    else:
        data, error = _read_json(manifest_path)
        if error or not isinstance(data, dict):
            failures.append(f"invalid visual_capture_manifest.json: {error}")
        else:
            resize = data.get("resizeProof", {})
            if not isinstance(resize, dict):
                failures.append("resizeProof missing object")
            else:
                method = str(resize.get("method", ""))
                runtime_truth = str(resize.get("runtimeTruth", ""))
                if "runtime-widget-edge" not in method and "fixed-size-source-truth" not in method:
                    failures.append(f"resize proof method is not runtime-edge or fixed-size source-truth: {method}")
                if resize.get("directGeometrySetUsed") is True or method in {"setGeometry-only", "scripted-resize-call"}:
                    failures.append("resize proof uses direct/scripted geometry as primary proof")
                if method.startswith("runtime-widget-edge") and not resize.get("widthIncreased"):
                    failures.append("resize proof does not prove width increased")
                if "exact-desktop-launcher-live-validation-still-required" not in runtime_truth:
                    failures.append("resize proof does not preserve exact desktop launcher LV boundary")

    if red_team_path is None:
        failures.append("missing internal_visual_red_team_ledger.json")
    else:
        data, error = _read_json(red_team_path)
        rows = data.get("rows", []) if isinstance(data, dict) else []
        if error or not isinstance(data, dict) or not isinstance(rows, list):
            failures.append(f"invalid internal_visual_red_team_ledger.json: {error}")
        else:
            if len(rows) < 12:
                failures.append(f"internal red-team ledger row count too low: {len(rows)}")
            dispositions = [str(row.get("finalDisposition", "")) for row in rows if isinstance(row, dict)]
            known_bad_proven = data.get("knownBadRegressionRejected") is True
            if rows and all(disposition == "PERFECT_PASS" for disposition in dispositions) and not known_bad_proven:
                failures.append("internal red-team ledger is all PERFECT_PASS and lacks negative repair/adjudication branches")
            defect_classes = {
                str(row.get("defectClass", "")).strip()
                for row in rows
                if isinstance(row, dict) and str(row.get("defectClass", "")).strip()
            }
            missing_classes = sorted(REQUIRED_RED_TEAM_DEFECT_CLASSES - defect_classes)
            if missing_classes:
                failures.append(f"internal red-team ledger missing defect classes: {', '.join(missing_classes)}")
            for index, row in enumerate(rows, start=1):
                if not isinstance(row, dict):
                    failures.append(f"internal red-team row {index} is not an object")
                    continue
                missing = REQUIRED_RED_TEAM_FIELDS - set(row)
                if missing:
                    failures.append(f"internal red-team row {index} missing fields: {', '.join(sorted(missing))}")
                if row.get("finalDisposition") == "REPAIR_REQUIRED":
                    failures.append(f"internal red-team row {index} remains REPAIR_REQUIRED")
                adjudicated_text = " ".join(
                    str(row.get(field, ""))
                    for field in ("observedFinding", "whyDefectAbsentIfPass", "exactRepairIfRequired")
                ).casefold()
                if any(term in adjudicated_text for term in FORBIDDEN_PRODUCT_COPY) and row.get("finalDisposition") == "PERFECT_PASS":
                    failures.append(f"internal red-team row {index} marks forbidden product copy as PERFECT_PASS")
                if "could not be opened" in adjudicated_text and "ready" in adjudicated_text and row.get("finalDisposition") == "PERFECT_PASS":
                    failures.append(f"internal red-team row {index} marks card/footer ready-vs-blocked contradiction as PERFECT_PASS")

    if root_cause_path is None:
        failures.append("missing adjudication_failure_root_cause_ledger.json")
    else:
        data, error = _read_json(root_cause_path)
        defects = data.get("defects", []) if isinstance(data, dict) else []
        if error or not isinstance(data, dict) or not isinstance(defects, list):
            failures.append(f"invalid adjudication_failure_root_cause_ledger.json: {error}")
        else:
            if len(defects) < 10:
                failures.append(f"root-cause defect row count too low: {len(defects)}")
            if len(defects) >= 2:
                for field in MIN_ROOT_CAUSE_UNIQUE_FIELDS:
                    unique = {
                        str(row.get(field, "")).strip()
                        for row in defects
                        if isinstance(row, dict) and str(row.get(field, "")).strip()
                    }
                    minimum = min(5, len(defects))
                    if len(unique) < minimum:
                        failures.append(
                            f"root-cause field {field} is too generic/repeated: {len(unique)} unique values for {len(defects)} defects"
                        )
            for index, row in enumerate(defects, start=1):
                if not isinstance(row, dict):
                    failures.append(f"root-cause defect row {index} is not an object")
                    continue
                missing = REQUIRED_ROOT_CAUSE_FIELDS - set(row)
                if missing:
                    failures.append(f"root-cause defect row {index} missing fields: {', '.join(sorted(missing))}")
                proof = str(row.get("proofNewCheckRejectsKnownBadExample", ""))
                if "FAM-006-20260622-173545.zip" not in proof and is_known_bad:
                    failures.append(f"root-cause defect row {index} does not cite the current known-bad rejection proof")

    if visual_ledger_path is None:
        failures.append("missing exhaustive_visual_conformance_ledger.json")
    else:
        data, error = _read_json(visual_ledger_path)
        rows = data.get("rows", []) if isinstance(data, dict) else []
        if error or not isinstance(data, dict) or not isinstance(rows, list):
            failures.append(f"invalid exhaustive_visual_conformance_ledger.json: {error}")
        else:
            joined_green_text = []
            for row in rows:
                if isinstance(row, dict) and row.get("final_disposition") == "PERFECT_PASS":
                    joined_green_text.append(" ".join(str(value) for value in row.values()))
                    if row.get("surface") in {"Recording Studio", "Log Viewer Studio", "Native/export folder shell"} and not row.get("packet_evidence_key"):
                        failures.append(f"{row.get('row_id')}: green Studio row lacks packet evidence key")
            green_text = " ".join(joined_green_text).casefold()
            for word in FORBIDDEN_GREEN_WORDS:
                if word in green_text:
                    failures.append(f"visual ledger green row contains forbidden progress wording: {word}")
            if any(term in green_text for term in FORBIDDEN_PRODUCT_COPY):
                failures.append("visual ledger green row contains forbidden internal/governance product copy")

    artifact_summary = {
        "evidenceRoot": str(evidence_root),
        "rowMap": str(row_map_path) if row_map_path else "",
        "visualManifest": str(manifest_path) if manifest_path else "",
        "redTeam": str(red_team_path) if red_team_path else "",
        "rootCause": str(root_cause_path) if root_cause_path else "",
        "visualLedger": str(visual_ledger_path) if visual_ledger_path else "",
        "rowMapKeys": sorted(row_map),
    }
    return PacketInspection(
        label=label,
        path=str(root),
        accepted=not failures,
        failures=failures,
        artifactSummary=artifact_summary,
    )


def _inspect_zip(path: Path, label: str) -> PacketInspection:
    with tempfile.TemporaryDirectory(prefix="fam006_false_accept_") as temp:
        temp_root = Path(temp)
        with zipfile.ZipFile(path, "r") as archive:
            archive.extractall(temp_root)
        return _inspect_packet_root(temp_root, label)


def _known_bad_results(paths: list[Path]) -> tuple[list[PacketInspection], list[str]]:
    results: list[PacketInspection] = []
    missing: list[str] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if not path.exists():
            missing.append(str(path))
            continue
        result = _inspect_zip(path, f"known-bad:{path.name}")
        results.append(result)
    return results, missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-packet", type=Path, default=DEFAULT_CURRENT_PACKET)
    parser.add_argument("--known-bad", action="append", type=Path, default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--known-bad-only", action="store_true")
    args = parser.parse_args()

    known_bad_paths = [*args.known_bad, *KNOWN_BAD_ZIPS]
    known_bad, missing = _known_bad_results(known_bad_paths)
    failures: list[str] = []
    if not known_bad:
        failures.append("no known-bad packet artifact available for false-ACCEPT regression corpus")
    for result in known_bad:
        if result.accepted:
            failures.append(f"known-bad packet was not rejected: {result.path}")

    current: PacketInspection | None = None
    if not args.known_bad_only:
        if not args.current_packet.exists():
            failures.append(f"current packet root missing: {args.current_packet}")
        else:
            current = _inspect_packet_root(args.current_packet, "current-packet")
            if not current.accepted:
                failures.extend(f"current packet: {failure}" for failure in current.failures)

    output = {
        "status": "PASS" if not failures else "FAIL",
        "gate": "FAM-006 false-ACCEPT regression gate",
        "knownBadRejected": all(not result.accepted for result in known_bad) and bool(known_bad),
        "knownBadResults": [result.__dict__ for result in known_bad],
        "missingPriorArtifacts": missing,
        "currentPacketResult": current.__dict__ if current else None,
        "failures": failures,
    }
    text = json.dumps(output, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
