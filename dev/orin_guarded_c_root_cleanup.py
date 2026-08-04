"""Guarded deletion gate for the three superseded C workspace roots."""
# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-RELOCATION-CLOSURE-015; surface=guarded-c-root-cleanup-gate; status=canonical
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

from nexus_paths import EXTERNAL_STATE_ROOT, USER_HUB_ROOT, WORKTREES_ROOT

DATA_ROOT = Path(r"D:\Nexus Desktop AI Data")
NEUTRAL_MAIN = Path(r"C:\Nexus Desktop AI")
SUPERSEDED_ROOTS = (
    Path(r"C:\Nexus Worktrees"),
    Path(r"C:\Nexus USER"),
    Path(r"C:\Nexus Governance State"),
)
ZIP_NAME = re.compile(r"^Governance-\d{8}-\d{6}\.zip$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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


def verify(args: argparse.Namespace) -> dict[str, object]:
    packet = Path(args.packet_root).resolve()
    archive = Path(args.packet_zip).resolve()
    receipt = Path(args.audit_receipt).resolve()
    failures: list[str] = []
    if packet.parent != USER_HUB_ROOT.resolve() or packet.name != "Governance":
        failures.append("packet root is not the canonical D Governance packet folder")
    if archive.parent != USER_HUB_ROOT.resolve() or not ZIP_NAME.fullmatch(archive.name):
        failures.append("packet ZIP is not a timestamped Governance ZIP beside the folder")
    if receipt.parent != packet.resolve() and not receipt.is_relative_to(packet):
        failures.append("audit receipt is not inside the canonical packet")
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
    if packet.is_dir() and archive.is_file():
        try:
            folder = folder_hashes(packet)
            zipped = zip_hashes(archive)
            if folder != zipped:
                failures.append("packet folder and ZIP content hashes differ")
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            failures.append(f"packet ZIP parity failed: {exc}")
    return {
        "canonical_d_roots": [str(WORKTREES_ROOT), str(USER_HUB_ROOT), str(EXTERNAL_STATE_ROOT)],
        "neutral_main": str(NEUTRAL_MAIN),
        "superseded_exact_targets": [str(path) for path in SUPERSEDED_ROOTS],
        "packet": str(packet),
        "packet_zip": str(archive),
        "packet_zip_sha256": sha256(archive) if archive.is_file() else None,
        "failures": failures,
        "ready": not failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-root", required=True)
    parser.add_argument("--packet-zip", required=True)
    parser.add_argument("--audit-receipt", required=True)
    parser.add_argument("--confirm-cleanup", action="store_true", help="Delete only after every guard passes.")
    args = parser.parse_args()
    report = verify(args)
    if args.confirm_cleanup and report["ready"]:
        for target in SUPERSEDED_ROOTS:
            if target == NEUTRAL_MAIN or target not in SUPERSEDED_ROOTS:
                raise RuntimeError(f"refusing non-allowlisted cleanup target: {target}")
            if target.exists():
                if target.is_symlink():
                    raise RuntimeError(f"refusing reparse/symlink cleanup target: {target}")
                shutil.rmtree(target)
        report["cleanup_executed"] = True
    else:
        report["cleanup_executed"] = False
    print(json.dumps(report, indent=2))
    return 0 if report["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
