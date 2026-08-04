"""Guarded deletion gate for the three superseded C workspace roots."""
# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-RELOCATION-CLOSURE-015; surface=guarded-c-root-cleanup-gate; status=canonical
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

from nexus_paths import EXTERNAL_STATE_ROOT, USER_HUB_ROOT, WORKTREES_ROOT

NEUTRAL_MAIN = Path(r"C:\Nexus Desktop AI")
SUPERSEDED_ROOTS = (
    Path(r"C:\Nexus Worktrees"),
    Path(r"C:\Nexus USER"),
    Path(r"C:\Nexus Governance State"),
)
ROOT_PAIRS = (
    (SUPERSEDED_ROOTS[0], WORKTREES_ROOT),
    (SUPERSEDED_ROOTS[1], USER_HUB_ROOT),
    (SUPERSEDED_ROOTS[2], EXTERNAL_STATE_ROOT),
)
ZIP_NAME = re.compile(r"^Governance-(\d{8})-(\d{6})\.zip$")
MANIFEST_SCHEMA = "nexus-relocation-parity-v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def is_reparse_point(path: Path) -> bool:
    junction_check = getattr(path, "is_junction", None)
    return path.is_symlink() or bool(junction_check and junction_check())


def folder_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)).replace("\\", "/"): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def zip_hashes(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("duplicate ZIP members")
        for name in names:
            if "\\" in name or name.endswith("/"):
                raise ValueError(f"non-file or backslash ZIP member: {name!r}")
            result[name] = hashlib.sha256(archive.read(name)).hexdigest()
    return result


def _digest_entry(relative: str, size: int, digest: str) -> bytes:
    return f"{relative.replace(chr(92), '/') }\0{size}\0{digest}\n".encode("utf-8")


def relocation_parity() -> list[dict[str, object]]:
    """Prove every source-root file exists identically under the D root.

    D roots may contain additional current material, but no file present in a
    superseded C root may be missing or changed at its corresponding D path.
    The aggregate digest is content-bound to relative path, size, and SHA-256.
    """

    results: list[dict[str, object]] = []
    for source_root, destination_root in ROOT_PAIRS:
        failures: list[str] = []
        source_digest = hashlib.sha256()
        matched_digest = hashlib.sha256()
        source_count = 0
        matched_count = 0
        missing_count = 0
        mismatch_count = 0
        unreadable_count = 0
        if not source_root.is_dir() or not destination_root.is_dir():
            failures.append("source or destination root is missing")
        elif is_reparse_point(source_root) or is_reparse_point(destination_root):
            failures.append("source or destination root is a reparse point")
        else:
            for source_file in sorted(source_root.rglob("*")):
                if not source_file.is_file():
                    continue
                if is_reparse_point(source_file):
                    failures.append(f"source file is a reparse point: {source_file}")
                    continue
                relative = source_file.relative_to(source_root)
                destination_file = destination_root / relative
                source_count += 1
                try:
                    source_size = source_file.stat().st_size
                    source_hash = sha256(source_file)
                    source_digest.update(_digest_entry(str(relative), source_size, source_hash))
                except OSError:
                    unreadable_count += 1
                    failures.append(f"source file is unreadable: {source_file}")
                    continue
                if not destination_file.is_file() or is_reparse_point(destination_file):
                    missing_count += 1
                    failures.append(f"destination file is missing or unsafe: {relative}")
                    continue
                try:
                    destination_size = destination_file.stat().st_size
                    destination_hash = sha256(destination_file)
                except OSError:
                    unreadable_count += 1
                    failures.append(f"destination file is unreadable: {relative}")
                    continue
                if source_size != destination_size or source_hash != destination_hash:
                    mismatch_count += 1
                    failures.append(f"destination file differs: {relative}")
                    continue
                matched_count += 1
                matched_digest.update(_digest_entry(str(relative), destination_size, destination_hash))
        results.append(
            {
                "source_root": str(source_root),
                "destination_root": str(destination_root),
                "source_file_count": source_count,
                "matched_file_count": matched_count,
                "missing_count": missing_count,
                "mismatch_count": mismatch_count,
                "unreadable_count": unreadable_count,
                "source_aggregate_sha256": source_digest.hexdigest(),
                "matched_aggregate_sha256": matched_digest.hexdigest(),
                "status": "PASS" if not failures and matched_count == source_count else "FAIL",
                "failure_sample": failures[:20],
            }
        )
    return results


def _parse_packet_timestamp(name: str) -> dt.datetime | None:
    match = ZIP_NAME.fullmatch(name)
    if not match:
        return None
    try:
        return dt.datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S").replace(
            tzinfo=dt.timezone.utc
        )
    except ValueError:
        return None


def _packet_freshness(packet: Path, archive: Path, receipt: Path, failures: list[str]) -> None:
    candidates = sorted(USER_HUB_ROOT.glob("Governance-*.zip"))
    if candidates != [archive]:
        failures.append("there must be exactly one current Governance ZIP beside the packet")
    timestamp = _parse_packet_timestamp(archive.name)
    if timestamp is None:
        failures.append("packet ZIP timestamp is invalid")
    if not receipt.is_file():
        return
    text = receipt.read_text(encoding="utf-8", errors="ignore")
    if f"Packet ZIP Name: {archive.name}" not in text:
        failures.append("audit receipt does not bind the supplied ZIP name")
    marker = re.search(r"Packet Generation Timestamp UTC:\s*([^\r\n]+)", text)
    if not marker:
        failures.append("audit receipt does not contain packet generation timestamp")
    elif timestamp is not None:
        try:
            generated = dt.datetime.fromisoformat(marker.group(1).strip().replace("Z", "+00:00"))
            if generated.astimezone(dt.timezone.utc).strftime("%Y%m%d-%H%M%S") != archive.stem.removeprefix("Governance-"):
                failures.append("packet ZIP timestamp does not match receipt generation timestamp")
        except ValueError:
            failures.append("audit receipt packet generation timestamp is invalid")
    if archive.is_file() and receipt.is_file() and archive.stat().st_mtime < receipt.stat().st_mtime:
        failures.append("packet ZIP predates the receipt it is supposed to contain")


def _load_manifest(path: Path, parity: list[dict[str, object]], failures: list[str]) -> None:
    if not path.is_file():
        failures.append("relocation parity manifest is missing")
        return
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"relocation parity manifest is unreadable: {exc}")
        return
    if payload.get("schema") != MANIFEST_SCHEMA:
        failures.append("relocation parity manifest schema is invalid")
        return
    expected = payload.get("roots")
    if expected != parity:
        failures.append("relocation parity manifest does not match the current source/D proof")


def verify(args: argparse.Namespace) -> dict[str, object]:
    packet = Path(args.packet_root).resolve()
    archive = Path(args.packet_zip).resolve()
    receipt = Path(args.audit_receipt).resolve()
    manifest = Path(args.relocation_manifest).resolve() if args.relocation_manifest else None
    failures: list[str] = []
    if packet.parent != USER_HUB_ROOT.resolve() or packet.name != "Governance":
        failures.append("packet root is not the canonical D Governance packet folder")
    if archive.parent != USER_HUB_ROOT.resolve() or not ZIP_NAME.fullmatch(archive.name):
        failures.append("packet ZIP is not a timestamped Governance ZIP beside the folder")
    if receipt.parent != packet.resolve() and not receipt.is_relative_to(packet):
        failures.append("audit receipt is not inside the canonical packet")
    if manifest is None or (manifest.parent != packet.resolve() and not manifest.is_relative_to(packet)):
        failures.append("relocation parity manifest must be inside the canonical packet")
    if not packet.is_dir() or not archive.is_file() or not receipt.is_file():
        failures.append("packet folder, ZIP, or audit receipt is missing")
    for root in (WORKTREES_ROOT, USER_HUB_ROOT, EXTERNAL_STATE_ROOT):
        if not root.is_dir():
            failures.append(f"canonical D root is missing: {root}")
    if not NEUTRAL_MAIN.is_dir():
        failures.append("neutral main C root is missing")
    if receipt.is_file():
        receipt_text = receipt.read_text(encoding="utf-8", errors="ignore")
        if "Non-Restorable Relocation Audit Receipt: YES" not in receipt_text:
            failures.append("audit receipt is not explicitly non-restorable")
        if "Final D-Root Verification: PASS" not in receipt_text:
            failures.append("audit receipt does not prove final D-root verification")
    _packet_freshness(packet, archive, receipt, failures)
    parity = relocation_parity()
    if any(item["status"] != "PASS" for item in parity):
        failures.append("C-to-D relocation parity proof failed")
    if manifest is not None:
        _load_manifest(manifest, parity, failures)
    archive_hash: str | None = None
    if packet.is_dir() and archive.is_file():
        try:
            folder = folder_hashes(packet)
            zipped = zip_hashes(archive)
            if folder != zipped:
                failures.append("packet folder and ZIP content hashes differ")
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            failures.append(f"packet ZIP parity failed: {exc}")
        try:
            archive_hash = sha256(archive)
        except OSError as exc:
            failures.append(f"packet ZIP SHA-256 is unreadable: {exc}")
    target_preflight: list[str] = []
    for target in SUPERSEDED_ROOTS:
        if target == NEUTRAL_MAIN or target not in SUPERSEDED_ROOTS:
            failures.append(f"refusing non-allowlisted cleanup target: {target}")
        elif target.exists() and (not target.is_dir() or is_reparse_point(target)):
            failures.append(f"cleanup target is not a normal directory: {target}")
        elif target.exists():
            target_preflight.append(str(target))
    return {
        "canonical_d_roots": [str(WORKTREES_ROOT), str(USER_HUB_ROOT), str(EXTERNAL_STATE_ROOT)],
        "neutral_main": str(NEUTRAL_MAIN),
        "superseded_exact_targets": [str(path) for path in SUPERSEDED_ROOTS],
        "packet": str(packet),
        "packet_zip": str(archive),
        "packet_zip_sha256": archive_hash,
        "relocation_parity": parity,
        "cleanup_target_preflight": target_preflight,
        "failures": failures,
        "ready": not failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-root", required=True)
    parser.add_argument("--packet-zip", required=True)
    parser.add_argument("--audit-receipt", required=True)
    parser.add_argument("--relocation-manifest", required=True)
    parser.add_argument("--write-relocation-manifest", action="store_true")
    parser.add_argument("--confirm-cleanup", action="store_true", help="Delete only after every guard passes.")
    args = parser.parse_args()
    manifest = Path(args.relocation_manifest).resolve()
    if args.write_relocation_manifest:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "schema": MANIFEST_SCHEMA,
                    "roots": relocation_parity(),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    report = verify(args)
    report["cleanup_executed"] = False
    if args.confirm_cleanup and report["ready"]:
        # Every target is preflighted before the first destructive operation.
        for target in SUPERSEDED_ROOTS:
            if target.exists():
                shutil.rmtree(target)
        report["cleanup_executed"] = True
        remaining = [str(target) for target in SUPERSEDED_ROOTS if target.exists()]
        if remaining:
            report["failures"].append(f"cleanup targets remain after deletion: {remaining}")
            report["ready"] = False
    print(json.dumps(report, indent=2))
    return 0 if report["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
