"""Build and validate the FAM-003 Option D performance decision packet.

Helper Status: Workstream-scoped
Owner Workstream: FAM-003 R2 Option D performance decision review
Reason Reusable Helper Was Not Extended: The migration-first decision sequence,
    temporary Option D posture, and exact FAM-003 external-state targets are
    specific to this Workstream completion gate.
Consolidation Target: Generic multi-decision packet semantic validation after a
    second branch needs the same external-state migration ordering contract.
Promotion Decision Point: Before any cross-family performance decision packet
    reuses this decision structure.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "dev" / "fixtures" / "fam003_performance_decision_packet_negative_cases.json"
USER_ROOT = Path(r"C:\Nexus USER")
PACKET_FOLDER = USER_ROOT / "FAM-003"
EXTERNAL_ROOT = Path(r"C:\Nexus Governance State")
BRANCH_KEY = "feature_fam_003_settings_resize_proof"
BRANCH_EXTERNAL = EXTERNAL_ROOT / "branches" / BRANCH_KEY
WORKTREE_EXTERNAL = EXTERNAL_ROOT / "worktrees" / "FAM-003" / "worktree_state.md"

CURRENT_GATE = "R2 Workstream completion USER review pending - performance decision required"
WORKSTREAM_RESULT = "USER_DECISION_REQUIRED"
STAGE_STATES = "NOT_ENTERED / NOT_ENTERED / NOT_REQUESTED"
TARGET_RESULT = "BLOCKED_LEGACY_SCHEMA"
ROOT_RESULT = "PASS"
FOREIGN_LOCK_RESULT = "ABSENT / ROOT PREFLIGHT PASS"
SCHEMA_VALUE = "external-state-v1"
STATE_VERSION = "1"
WORKTREE_LABEL = "FAM-003"
WORKTREE_PATH = r"C:\Nexus Worktrees\FAM-003"
SLOT_ID = "runtime-active-3"
BRANCH_NAME = "feature/fam-003-settings-resize-proof"
RAW_SAMPLE_COUNT = 780
PRIMARY_RELATIVE = Path("USER Review") / "FAM003_OPTION_D_PERFORMANCE_FINAL_DECISION_REVIEW.md"
CORE_RELATIVES = (
    Path("START_HERE.md"),
    PRIMARY_RELATIVE,
    Path("Review Aids") / "02_FINAL_EXTERNAL_VALIDATION_CHRONOLOGY.md",
    Path("Review Aids") / "03_TARGET_CURRENTNESS_AND_MIGRATION_SPEC.md",
    Path("Review Aids") / "04_REFINED_OPTION_G_SCOPE.md",
    Path("Review Aids") / "05_HUD_FAIL_CLOSED_ENVELOPE.md",
    Path("Review Aids") / "06_ORIN_CORE_OWNER_VISION_CARRYFORWARD.md",
    Path("Review Aids") / "07_OWNERSHIP_AND_CARRIER_MATRIX.md",
    Path("Review Aids") / "08_DECISION_SEQUENCE_AND_BOUNDARIES.md",
    Path("Review Aids") / "09_VALIDATION_PROOF_ROLLBACK_AND_STALENESS.md",
    Path("Review Aids") / "11_ARTIFACT_MANIFEST.md",
    Path("Source Truth Context") / "Git Audit" / "TARGET_CURRENTNESS_AND_MIGRATION_SPEC.md",
)

MIGRATION_TARGETS = (
    (
        "branch_plan.md",
        BRANCH_EXTERNAL / "branch_plan.md",
        "Live Branch Plan",
        "Current active branch engineering plan fields",
    ),
    (
        "branch_state.md",
        BRANCH_EXTERNAL / "branch_state.md",
        "Live Branch Projection",
        "Current active branch phase, blocker, and next legal phase fields",
    ),
    (
        "worktree_state.md",
        WORKTREE_EXTERNAL,
        "Live Worktree Projection",
        "Current assignment and acknowledgement fields for one worktree",
    ),
)

EXTERNAL_FILES = (
    BRANCH_EXTERNAL / "branch_plan.md",
    BRANCH_EXTERNAL / "branch_state.md",
    BRANCH_EXTERNAL / "r2_workstream_execution_ledger_20260716.md",
    BRANCH_EXTERNAL / "r2_option_d_nonintrusive_performance_repair_20260721.md",
    BRANCH_EXTERNAL / "r2_option_d_performance_methodology_repair_20260721.md",
    BRANCH_EXTERNAL / "r2_option_d_performance_investigation_plan_20260722.md",
    BRANCH_EXTERNAL / "r2_renderer_backend_option_d_completion_20260721.md",
    BRANCH_EXTERNAL / "r2_renderer_backend_scope_reconciliation_20260721.md",
    BRANCH_EXTERNAL / "r2_renderer_backend_user_decision_20260721.md",
    BRANCH_EXTERNAL / "r2_workstream_completion_evidence_repair_defect_ledger_20260721.md",
    WORKTREE_EXTERNAL,
)


class PacketValidationError(RuntimeError):
    """Raised when the active decision packet is semantically unsafe."""


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _safe_seed_members(seed_zip: Path) -> dict[str, bytes]:
    retained: dict[str, bytes] = {}
    with zipfile.ZipFile(seed_zip) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            relative = PurePosixPath(info.filename)
            if relative.is_absolute() or ".." in relative.parts:
                raise PacketValidationError(f"unsafe seed ZIP member: {info.filename}")
            key = relative.as_posix()
            if key == "START_HERE.md":
                continue
            if key.startswith("USER Review/") or key.startswith("Review Aids/"):
                continue
            if key.startswith("Source Truth Context/External State Snapshots/"):
                continue
            if key.startswith("Source Truth Context/Active External Snapshot/"):
                continue
            if key.startswith("Source Truth Context/Validation Outputs/"):
                continue
            if key.startswith("Source Truth Context/Git Audit/"):
                continue
            retained[key] = archive.read(info)
    return retained


def _safe_seed_folder(seed_folder: Path) -> dict[str, bytes]:
    retained: dict[str, bytes] = {}
    for source in sorted(seed_folder.rglob("*")):
        if not source.is_file():
            continue
        key = source.relative_to(seed_folder).as_posix()
        if key == "START_HERE.md":
            continue
        if key.startswith("USER Review/") or key.startswith("Review Aids/"):
            continue
        if key.startswith("Source Truth Context/External State Snapshots/"):
            continue
        if key.startswith("Source Truth Context/Active External Snapshot/"):
            continue
        if key.startswith("Source Truth Context/Validation Outputs/"):
            continue
        if key.startswith("Source Truth Context/Git Audit/"):
            continue
        retained[key] = source.read_bytes()
    return retained


def _extract_seed(seed_members: dict[str, bytes], packet_folder: Path) -> None:
    for relative, payload in seed_members.items():
        destination = packet_folder / Path(*PurePosixPath(relative).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)


def _copy_external_snapshots(packet_folder: Path) -> None:
    destination = packet_folder / "Source Truth Context" / "Active External Snapshot"
    destination.mkdir(parents=True, exist_ok=True)
    for source in EXTERNAL_FILES:
        if not source.is_file():
            raise PacketValidationError(f"required external record missing: {source}")
        shutil.copy2(source, destination / source.name)


def _refresh_repo_context(packet_folder: Path) -> dict[str, str]:
    context_root = packet_folder / "Source Truth Context"
    implementation = context_root / "Implementation Snapshots"
    implementation.mkdir(parents=True, exist_ok=True)
    additions = {
        "dev/orin_fam003_performance_decision_packet_validation.py": (
            implementation / "orin_fam003_performance_decision_packet_validation.py"
        ),
        "dev/fixtures/fam003_performance_decision_packet_negative_cases.json": (
            implementation / "fam003_performance_decision_packet_negative_cases.json"
        ),
    }
    for source, destination in additions.items():
        shutil.copy2(ROOT / source, destination)

    tracked = subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True
    ).splitlines()
    by_name: dict[str, list[str]] = {}
    for source in tracked:
        by_name.setdefault(PurePosixPath(source).name, []).append(source)
    special = {
        "Source Truth Context/Repo Owners/branch_plans_README.md": "Docs/branch_plans/README.md",
        "Source Truth Context/Repo Owners/workstreams_index.md": "Docs/workstreams/index.md",
    }
    mappings: dict[str, str] = {}
    for area in (context_root / "Repo Owners", implementation):
        for copied in sorted(area.rglob("*")):
            if not copied.is_file():
                continue
            copied_relative = copied.relative_to(packet_folder).as_posix()
            source = special.get(copied_relative)
            if source is None:
                candidates = by_name.get(copied.name, [])
                if len(candidates) == 1:
                    source = candidates[0]
                else:
                    matching = [
                        candidate
                        for candidate in candidates
                        if (ROOT / candidate).is_file()
                        and (ROOT / candidate).read_bytes() == copied.read_bytes()
                    ]
                    if len(matching) == 1:
                        source = matching[0]
            if source is None or not (ROOT / source).is_file():
                raise PacketValidationError(
                    f"repo source mapping is ambiguous or missing for {copied_relative}"
                )
            copied.write_bytes(
                subprocess.check_output(["git", "show", f"HEAD:{source}"], cwd=ROOT)
            )
            mappings[source] = copied_relative
    return mappings


def _performance_facts() -> str:
    return """# Current Performance Evidence

Evidence Status: `DECISION_QUALITY_ABSOLUTE_MEASUREMENT / NOT PERFORMANCE ACCEPTANCE`

| Fact | Current evidence | Boundary |
| --- | --- | --- |
| Sustained resident CPU | Startup / active / post-use medians are `195.546% / 243.973% / 201.863%` of one logical core, or `12.222% / 15.248% / 12.616%` of the measured 16-logical-processor machine. | Absolute Option D posture only; no safe equivalent hardware baseline exists. |
| Memory | USS medians are `269.819 / 410.777 / 417.486 MiB`; post-use private commit remains near `1022.984 MiB`. | Retention is proven; a leak is not proven. |
| Process posture | Startup has five product processes and post-use has six. | Retained process/surface attribution requires a later bounded plan. |
| ORIN Core | One continuous `requestAnimationFrame` loop and 14 base infinite CSS animations are present. | Major persistent contributor; exact causal share and durable animation-policy owner remain unresolved. |
| Native polling | Hidden HUD native polling and `Log Viewer Studio resize-hover polling` remain scheduled candidates. | Recording Studio polling is not admitted by this wording. |
| Repeated cycles | The HUD renderer dominates monotonic USS growth over three cycles in all three measured sessions. | Longer-cycle attribution is required before repair authority. |
| Evidence volume | Three normal-launcher sessions, 21 intervals, and `780` raw samples. | `573` is stale and invalid for this packet. |
| Option D | Temporary shared-runtime `--disable-gpu` safety policy. | Not permanent architecture and not accepted performance equivalence. |

No governed numeric performance threshold exists. No product-performance defect,
safe equivalence, no-regression result, improvement claim, or memory leak is
asserted. Workstream completion therefore remains `USER_DECISION_REQUIRED`.
"""


def _chronology() -> str:
    return f"""# Final External Validation Chronology

Final Root-Wide Result: `{ROOT_RESULT}`
Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`
Foreign Lock Mutation: `NONE`

| Order | Validation class | Result | Role |
| --- | --- | --- | --- |
| 1 | Historical evidence-time root validation | `PASS` | Historical supporting evidence only. |
| 2 | Prior packet final root/Stage 4 validation | `BLOCKED_BY_FOREIGN_LIVE_LOCK` | Superseded currentness result; preserved to explain the earlier blocker. |
| 3 | Initial current root/Stage 4 validation | `{ROOT_RESULT}` | Fresh task-start attempt; the prior foreign lock cleared naturally. |
| 4 | FAM-003 target-currentness, branch plan | `{TARGET_RESULT}` | Current blocker; complete live-header migration remains unexecuted. |
| 5 | FAM-003 target-currentness, branch state | `{TARGET_RESULT}` | Current blocker; complete live-header migration remains unexecuted. |
| 6 | FAM-003 target-currentness, worktree state | `{TARGET_RESULT}` | Current blocker; complete live-header migration remains unexecuted. |
| 7 | Final current root/Stage 4 validation | `{ROOT_RESULT}` | Final post-repair attempt; no foreign lock was active. |

The root result is green now, but target currentness remains blocked. The prior
foreign lock was not cleared, edited, bypassed, adopted, or mutated by FAM-003.
Any foreign or conflicting live lock observed at future migration preflight is
a no-write blocker, not permission to recover or clear that lock.
"""


def _target_hash_rows(target_hashes: dict[str, str]) -> str:
    return "\n".join(
        f"| `{name}` | `{target_hashes[name]}` | Must match before any lock-backed staging or write. |"
        for name, _path, _record_class, _record_role in MIGRATION_TARGETS
    )


def _migration_review_aid() -> str:
    return f"""# Target Currentness And FAM-003-Local Migration Review Aid

Target Currentness Result: `{TARGET_RESULT}`
Planning Route While Blocked: `SCHEMA_MIGRATION_DECISION_ONLY / NO BP2_BP3_WORKSTREAM_REVISION`

This review aid summarizes the decision in USER-readable form. The complete
execution contract, exact source/base identities, and approved three-target byte
digests are under
`Source Truth Context/Git Audit/TARGET_CURRENTNESS_AND_MIGRATION_SPEC.md`.

## Exact Targets And Roles

| Target | Record Class | Record Role |
| --- | --- | --- |
| `branch_plan.md` | `Live Branch Plan` | `Current active branch engineering plan fields` |
| `branch_state.md` | `Live Branch Projection` | `Current active branch phase, blocker, and next legal phase fields` |
| `worktree_state.md` | `Live Worktree Projection` | `Current assignment and acknowledgement fields for one worktree` |

The complete live header includes schema/version, class/role, branch and source
identity, worktree label and canonical path, slot, one transition timestamp and
updater, current gate/stage posture, transition status, and the historical
receipt boundary. `Worktree` means label `{WORKTREE_LABEL}`; `Worktree Path`
means `{WORKTREE_PATH}`. The first migrated version is `1` because the legacy
targets have no version field.

The historical boundary is the final live-header field before the existing
first section heading. Every existing byte below it remains historical evidence
and cannot satisfy current live-header validation.

No write begins unless fresh external-state validation has no foreign or
conflicting lock, identity and approval remain current, all three target bytes
match the approved context, all routed locks are available, and a verified
snapshot plus rollback path exists. Lock order is `state-root -> migration ->
worktree -> branch`; release is reversed. FAM-003 never clears a foreign lock.

All three candidates are staged and validated first. Each file replacement is
atomic; completion is logical all-or-none, with one transaction audit and
restoration of every replaced target on failure. Migration completes only after
all three target checks, FAM-003-scoped validation, and root validation pass.
Central, sibling, Governance, selected-next, repo, and other targets are not
admitted. Decision 2 planning preparation remains separately USER-gated after
green migration completion; Decision 3 Core routing remains separate.
"""


def _migration_spec(
    head: str,
    origin_main: str,
    target_hashes: dict[str, str],
) -> str:
    hash_rows = _target_hash_rows(target_hashes)
    return f"""# Target Currentness And FAM-003-Local Migration Specification

Target Currentness Result: `{TARGET_RESULT}`
Planning Route While Blocked: `SCHEMA_MIGRATION_DECISION_ONLY / NO BP2_BP3_WORKSTREAM_REVISION`

## Exact Targets

1. `C:\\Nexus Governance State\\branches\\{BRANCH_KEY}\\branch_plan.md`
2. `C:\\Nexus Governance State\\branches\\{BRANCH_KEY}\\branch_state.md`
3. `C:\\Nexus Governance State\\worktrees\\FAM-003\\worktree_state.md`

## Complete Live-Header Field Union

| Exact label | Exact value or derivation | Applies to | Update / validation / rollback rule |
| --- | --- | --- | --- |
| `External State Schema` | `{SCHEMA_VALUE}` | all three | Immutable during this migration; target and root validators must accept it; rollback restores field absence. |
| `State Version` | `{STATE_VERSION}` | all three | Legacy pre-state is `ABSENT`; first migrated projection initializes at 1. All three commit at version 1. A later successful write increments only its target by one; read/write drift is `External State Version Conflict`; rollback restores absence. |
| `Record Class` | target-specific table below | all three | Exact governed class; placeholders and historical classes fail. |
| `Record Role` | target-specific source phrase below | all three | Exact semantic role; placeholders fail. |
| `Branch` | `{BRANCH_NAME}` | all three | Derived from proven Git identity; exact match required; rollback restores absence. |
| `Source Repo HEAD` | `{head}` | all three | Frozen pushed migration-source commit; all three must agree. Newer HEAD requires reconciliation and a replacement decision packet. |
| `Origin/Main` | `{origin_main}` | all three | Frozen fetched base commit and merge base; newer origin/main triggers pre-rebaseline impact audit and packet reconciliation. |
| `Worktree` | `{WORKTREE_LABEL}` | all three | Stable worktree label, not a filesystem path. |
| `Worktree Path` | `{WORKTREE_PATH}` | all three | Absolute canonical Git worktree path; compared case-insensitively and slash-normalized. |
| `Slot ID` | `{SLOT_ID}` | all three | USER-approved reusable runtime slot from current FAM-003 receipt. |
| `Last Updated` | one transition-wide UTC timestamp captured immediately before staging, RFC 3339 seconds such as `2026-07-22T20:15:30+00:00` | all three | Identical in all three migrated headers; packet timestamps may differ; rollback restores absence. |
| `Last Updated By` | `Codex` | all three | Exact migration writer identity used by the routed helper/audit contract; rollback restores absence. |
| `Current Gate` | `{CURRENT_GATE}` | all three | Copied from current FAM-003 external decision authority; all three must agree. |
| `Workstream Result` | `{WORKSTREAM_RESULT}` | all three | Remains unaccepted; all three must agree. |
| `H1 / LV / UTS` | `{STAGE_STATES}` | all three | No downstream phase advancement; all three must agree. |
| `Next Legal Phase` | `USER Decision 1 on this bounded migration; after green completion, Decision 2 preparation only if separately approved` | all three | Must not imply automatic BP2/BP3/Workstream preparation. |
| `Transition Status` | `MIGRATED_CURRENT_PENDING_USER_PERFORMANCE_DECISION` | all three | Written only by approved execution; completion still requires all validation. |
| `Historical Receipt Boundary` | `Existing record body below this boundary is immutable historical receipt evidence and does not redefine the live header.` | all three | Final live-header field immediately before the first existing `##` heading. |

`Worktree` and `Worktree Path` are both required: the first is the stable label;
the second is the canonical absolute path. They must never be collapsed into one
field or populated with the same path value.

## Exact Per-Target Assignments

| Target | Record Class | Record Role | Live purpose / current gate source | Historical boundary placement |
| --- | --- | --- | --- | --- |
| `branch_plan.md` | `Live Branch Plan` | `Current active branch engineering plan fields` | Active performance-decision and future Option G planning route; current gate comes from the latest FAM-003 decision receipt. | After all live fields and immediately before the existing first heading. |
| `branch_state.md` | `Live Branch Projection` | `Current active branch phase, blocker, and next legal phase fields` | Active branch gate, blockers, and next legal phase; current gate comes from the latest FAM-003 decision receipt. | After all live fields and immediately before the existing first heading. |
| `worktree_state.md` | `Live Worktree Projection` | `Current assignment and acknowledgement fields for one worktree` | FAM-003 assignment, acknowledgement, and gate projection; current gate comes from the latest FAM-003 decision receipt. | After all live fields and immediately before the existing first heading. |

Common identity values are exactly `{BRANCH_NAME}`, `{WORKTREE_LABEL}` (`Worktree`),
`{WORKTREE_PATH}` (`Worktree Path`), and `{SLOT_ID}`. No additional FAM-003
record is required: the plan, branch projection, and worktree projection are the
complete bounded target set.

## Live Versus Historical Content Map

For every target, the new live header begins at byte 0 and ends with the
`Historical Receipt Boundary` field. The complete pre-migration file body,
starting with its existing first `##` heading and including every prior current-
looking receipt, remains byte-for-byte below that boundary as historical
evidence. None of those older fields may satisfy live-header validation or
redefine HEAD, base, gate, version, or role. No old heading is deleted, moved,
or promoted; the boundary supersedes old currentness semantics without erasing
chronology. The live header contains exactly one current gate.

## Approved Pre-Write Hash Model

| Target | Approved decision-packet SHA256 | Rule |
| --- | --- | --- |
{hash_rows}

The later execution rereads and hashes all three files before lock-backed
staging. A mismatch requires a reconciled current snapshot and replacement USER
decision packet; it may not be accepted silently. Encoding remains strict UTF-8
and source newline bytes are preserved. The snapshot must preserve file bytes,
relative paths, hashes, and ordinary file metadata needed for restoration.

## No-Write Preconditions

No mutation, temp-file staging, or later lock acquisition may begin until all
earlier checks pass:

1. fresh root/Stage 4 validation is PASS and no foreign, stale, expired-unrecovered, or conflicting live lock exists;
2. worktree, Git root, branch, upstream, HEAD, origin/main, merge base, cleanliness, ahead/behind, carrier, approval, and RAR posture match this packet;
3. target-currentness still selects exactly these three legacy targets and no additional target is required;
4. all three approved SHA256 values above match current bytes;
5. the routed helper versions equal the pushed packet copies and the complete field union validates in dry-run projections;
6. state-root, migration, worktree, and branch locks can be acquired legally by `Codex` for `{WORKTREE_LABEL}` / `{BRANCH_NAME}`;
7. a complete pre-migration snapshot and manifest cover all three exact targets with matching file count and hashes;
8. rollback temp paths, snapshot bytes, release commands, and receipt location are ready;
9. no central, sibling, Governance, selected-next, issue, PR, release, or repo source mutation is required;
10. no newer origin/main, overlap, approval, carrier, or RAR trigger invalidates the packet.

Failure of any item means no write, no later lock acquisition, reverse release
of every legally acquired FAM-003 lock, and a blocker packet. A foreign lock is
never cleared, recovered, adopted, bypassed, or mutated by this execution.

## Exact Lock Sequence

Preflight first checks the root and every current lock read-only. The Stage 4C
state-root requirement is the outer prerequisite to the ordered concurrency
contract. Acquire in this exact order: `state-root -> migration -> worktree ->
branch`. `Codex` owns all four under `{WORKTREE_LABEL}` / `{BRANCH_NAME}`. The
state-root and migration intended write sets name all three targets; the
worktree lock names only `worktrees/FAM-003/worktree_state.md`; the branch lock
names only the two branch targets. Stop on timeout, expiry, changed payload,
owner mismatch, missing intended-write entry, or stale-lock state. Stale-lock
recovery requires its own USER-reviewed recovery packet. Release only after
completion or verified rollback, in reverse order: `branch -> worktree ->
migration -> state-root`.

## Snapshot And Transaction Contract

After all locks are held, create
`C:\\Nexus Governance State\\snapshots\\snapshot-<UTC-id>` with
`dev/orin_external_state_snapshot.py`. Its manifest must name `{SCHEMA_VALUE}`,
the reason, root, `{WORKTREE_LABEL}`, `{BRANCH_NAME}`, creator `Codex`, timestamp,
every copied relative path, file count, and SHA256. Verify the three target
copies against the approved hashes before staging.
Snapshot contract covers all three exact target bytes, relative paths, file
count, and hashes.

Build all three UTF-8 temporary candidates first, preserve source newline bytes,
validate every complete live header, boundary, class/role, common identity,
version, timestamp, gate, and unchanged historical body, then dry-run the routed
target reconcile contract. Individual replacement is atomic; Windows does not
provide one physical three-file rename transaction. The governed all-three
contract is therefore logical all-or-none completion: no completion audit or
lock release may occur until all three replacements and rereads pass, and any
failure restores every target already replaced from the same snapshot via
atomic per-file restoration. A transaction journal/audit must record all three
before/after hashes and may declare success only once, for the complete set.

## Post-Write Validation And Rollback

After replacement, reread and hash all three, compare headers and historical
bodies, run each target-currentness check, FAM-003-scoped external validation,
then root/Stage 4 validation. Record completion only if every result is PASS.
Planning revision remains blocked until that completion receipt exists.

Rollback triggers are write/partial-write failure, hash drift, schema/header or
boundary failure, cross-file identity/gate mismatch, target/scoped validation
failure, migration-caused root failure, lock loss/change, or audit failure.
Restore all three approved snapshot bytes atomically per file, verify original
hashes and legacy target-currentness posture, run scoped/root validation, write
a rollback receipt, and reverse-release locks. Successful rollback returns to
this unchanged performance-decision gate with migration unexecuted. Failed
rollback is `External State Corrupt / USER recovery decision required` and
locks remain held or explicitly marked for recovery.

If all migrated records pass but a new unrelated foreign lock appears before
the final root check, preserve migrated bytes and all locks, record
`POST_WRITE_ROOT_BLOCKED_BY_NEW_FOREIGN_LOCK`, and stop for USER adjudication;
do not label migration complete and do not roll back otherwise valid FAM-003
bytes merely because unrelated root validation is temporarily blocked.

## Completion Criteria And Mutation Boundary

Completion requires all three complete version-1 headers, exact classes/roles,
valid boundaries, current identities/gate, all-three audit, preserved snapshot
and rollback evidence, three target PASS results, FAM-003-scoped PASS, root PASS,
no relevant foreign lock, packet/external-state agreement, and proof that no
central, sibling, Governance, selected-next, repo, or other target changed.

Migration Ownership / Carrier: `FAM-003 external operational state only`.
This packet specifies but does not perform the migration.
"""


def _option_g_scope() -> str:
    return """# Refined Option G Scope

Recommendation: `OPTION G / MIGRATION FIRST / PLANNING REVISION SECOND`

## Required Sequence

`Decision 1 migration approval -> FAM-003-local migration -> target-currentness green -> root-wide validation green -> Decision 2 planning-revision preparation -> revised BP2/BP3/Workstream packet -> later USER implementation decision`

## Stage 1 Planning Candidates

* hidden HUD native polling lifecycle gating;
* `Log Viewer Studio resize-hover polling` lifecycle gating;
* longer-cycle HUD renderer retention attribution;
* a targeted HUD retention repair only if current-carrier attribution and
  ownership are proven inside the fail-closed envelope.

## Stage 1 Exclusions

* Recording Studio polling unless separately proven and admitted;
* ORIN Core animation changes;
* AI surface-lifetime changes;
* generic WebEngine destruction or lazy-creation policy;
* renderer-backend changes;
* permanent Option D adoption;
* advanced FAM-006 runtime behavior;
* unbounded HUD JavaScript or state-semantic changes;
* sibling-worktree mutation.

The exact Studio row is limited to `Log Viewer Studio resize-hover polling`.
Broader generic Studio polling wording is rejected as ambiguous.
"""


def _hud_envelope() -> str:
    return """# HUD Retention Fail-Closed Envelope

Future planning may enumerate only these later repair classes:

* FAM-003-owned native timer start/stop lifecycle;
* FAM-003-owned visibility-to-polling coordination;
* current-carrier owner-object release or retention behavior only where
  FAM-003 ownership is proved;
* diagnostic attribution and bounded validation/proof.

Mandatory Stop Boundary: `STOP_AND_RETURN_FOR_USER_DECISION`

The later Workstream must stop if attribution reaches FAM-006-owned JavaScript,
FAM-006 state semantics, FAM-006 WebEngine owner lifetime, shared profile/runtime
ownership, another owner's files, or shared architecture beyond the accepted
revision. Current carrier access does not transfer ownership. No open-ended HUD
repair authority is created by this packet.
"""


def _core_carryforward() -> str:
    return """# ORIN Core Owner / Vision Decision Carryforward

Carryforward Status: `SEPARATE_OWNER_VISION_DECISION_PACKET_REQUIRED`

The future planning-revision preparation must also produce a separate ORIN Core
owner/vision decision packet. It must cover the governing source-truth owner,
current animation and idle behavior, continuous `requestAnimationFrame`, the 14
base infinite CSS animations, visible/background behavior, whether throttling
is product vision/performance policy/visualization-owner work, possible legal
carriers, options/tradeoffs, proof obligations, and the exact later USER
decision. This is planning only. It does not silently enter Stage 1, mutate Core,
or assign an owner by inference.
"""


def _ownership_matrix() -> str:
    return """# Ownership And Carrier Matrix

| Surface / concern | Source owner | Current evidence carrier | Disposition |
| --- | --- | --- | --- |
| Resident/tray doorway | FAM-003 / F3-FF01 | FAM-003 current branch | FAM-003 may plan its owned lifecycle/routing behavior. |
| Desktop visual grammar | Project Vision and FAM-002 | Consumed by FAM-003 | Presentation dependency; no sibling mutation. |
| HUD Dashboard, HUD runtime state, Recording Studio, Log Viewer Studio | FAM-006 | Shared current-carrier runtime evidence only | Runtime/state ownership remains FAM-006; current carrier access does not transfer ownership. |
| AI surface/state/runtime trust | FAM-007 plus AI Runtime And Trust Architecture | Shared current-carrier evidence only | No AI lifecycle or provider/runtime work is admitted. |
| ORIN Core animation policy | `SOURCE_TRUTH GAP / OWNER DECISION REQUIRED` | FAM-003 evidence identifies behavior only | Route through a separate owner/vision decision packet. |
| External projection migration | FAM-003 external operational state | Three exact FAM-003 targets | Requires Decision 1 and routed lock/snapshot/atomic helpers. |
| Option G planning revision | FAM-003 branch planning carrier after migration green | Current branch only if separately approved | Preparation only; no implementation. |
"""


def _decision_sequence() -> str:
    return f"""# Decision Sequence And Approval Boundaries

Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`

## Decision 1 - FAM-003-Local External-State Schema Migration

Exact future approval text:

> I approve the bounded FAM-003-local external-state schema migration for
> `branch_plan.md`, `branch_state.md`, and `worktree_state.md` on
> `{BRANCH_NAME}`, subject to every no-write precondition in
> `03_TARGET_CURRENTNESS_AND_MIGRATION_SPEC.md`, using the exact
> `state-root -> migration -> worktree -> branch` lock order, the approved
> three-target pre-write hashes, one verified snapshot, complete version-1 live
> headers, logical all-three completion with atomic per-file replacement and
> mandatory rollback, historical-boundary preservation, one all-three audit,
> and target/scoped/root validation. Any foreign or conflicting lock blocks all
> writes and is not cleared by FAM-003. This approval excludes central or sibling records, repo
> Governance mutation, product/runtime work, BP2/BP3/Workstream revision,
> implementation, H1, LV, UTS, issue, PR, merge, release, and cleanup.

## Decision 2 - Refined Option G Planning-Revision Preparation

This decision is not actionable until Decision 1 is executed and both target
currentness and root-wide external-state validation are green.

Exact future approval text:

> After the approved FAM-003-local migration is complete and target-currentness
> plus root-wide external-state validation are green, I approve preparation
> only of a revised BP2/BP3/Workstream planning packet for Option G Stage 1:
> hidden HUD native polling lifecycle gating, Log Viewer Studio resize-hover
> polling lifecycle gating, longer-cycle HUD renderer retention attribution,
> and only a fail-closed FAM-003-owned targeted HUD retention repair class when
> ownership is proven. Return the revised packet for USER review before any
> implementation. Recording Studio polling, ORIN Core/AI changes, generic
> WebEngine policy, renderer changes, permanent Option D, FAM-006-owned runtime
> behavior, sibling mutation, H1, LV, UTS, issue, PR, merge, release, and
> cleanup remain blocked.

## Decision 3 - Future ORIN Core Owner / Vision Routing

Exact future approval text:

> I approve preparation only of a separate ORIN Core owner/vision decision
> packet covering current animation/idle behavior, continuous RAF and CSS
> animation policy, visible/background behavior, possible owners/carriers,
> tradeoffs, and proof obligations. This does not approve Core behavior changes,
> source-truth owner mutation, Stage 1 inclusion, implementation, H1, LV, UTS,
> issue, PR, merge, release, or sibling/Governance mutation.

The three decisions are separate. Decision 1 is the only current executable
decision. Decisions 2 and 3 remain preparation-only gates and cannot be combined
into implementation authority.
"""


def _validation_and_staleness() -> str:
    return f"""# Validation, Proof, Rollback, And Staleness

Current initial and final root result: `{ROOT_RESULT}`.
Current foreign lock result: `{FOREIGN_LOCK_RESULT}`.
The prior packet's foreign-lock blocker is historical supporting evidence only.
Target currentness remains `{TARGET_RESULT}` for all three FAM-003 projections.

Evidence currentness:

* the source commit and upstream are identical;
* the base branch equals the branch point;
* tracked files were clean before this packet-only validator repair;
* the preserved local launcher remains outside tracked source;
* v4 performance evidence has three sessions, 21 intervals, and 780 raw samples;
* Option D remains temporary;
* Workstream is not accepted;
* H1/LV/UTS remain `NOT_ENTERED / NOT_ENTERED / NOT_REQUESTED`.

The final archive digest is recorded outside the archive after generation. Any
later foreign/conflicting lock, source revision change,
base-branch advance, target migration, performance-bearing code change, or
evidence replacement makes the applicable packet claim stale and requires a
fresh validation/packet cycle.
"""


def _authority() -> str:
    loaded = [
        "Docs/Main.md (loaded first)",
        "Docs/governance_efficiency_operating_model.md",
        "Docs/external_operational_state_store_reform_plan.md",
        "Docs/phase_governance.md",
        "Docs/development_rules.md",
        "Docs/branch_plans/README.md",
        "Docs/validation_helper_registry.md",
        "Docs/branch_records/feature_fam_003_settings_resize_proof.md",
        "Docs/worktree_slots.md",
        "Docs/nexus_vision.md",
        "Docs/family_visions/FAM-002_desktop_interface.md",
        "Docs/family_visions/FAM-003_interaction_and_actions.md",
        "Docs/family_visions/FAM-006_monitoring_and_hud.md",
        "Docs/family_visions/FAM-007_local_ai_and_capability_packs.md",
        "Docs/family_feature_visions/F3-FF01.md",
        "Docs/ai_runtime_and_trust_architecture.md",
        "Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md",
        "Docs/workstreams/FB-040_monitoring_thermals_performance_hud_surface.md",
        "Docs/workstreams/index.md",
        "Docs/incident_patterns.md",
        "dev/orin_external_state_validation.py",
        "dev/orin_external_state_target_reconcile.py",
        "dev/orin_external_state_lock.py",
        "dev/orin_external_state_lock_release.py",
        "dev/orin_external_state_snapshot.py",
        "dev/orin_external_state_report.py",
        "dev/orin_user_review_bundle.py",
        "dev/orin_fam003_option_d_nonintrusive_performance_validation.py",
        *[str(path) for path in EXTERNAL_FILES],
        "C:\\Nexus USER\\FAM-003-20260722-113210.zip",
    ]
    rows = "\n".join(f"* `{item}`" for item in loaded)
    return f"""# Files Loaded And Authority

{rows}

`Docs/nexus_startup_contract.md` was not loaded because the task explicitly
excluded ChatGPT continuity/bootstrap authority.

## Missing / Stale / Conflicting / Superseded Authority

* The three live FAM-003 external projections are legacy records and lack the
  complete governed live-header union; they remain authority for their
  historical content but fail current target validation.
* The old packet's nine-field-only migration sketch and combined migration /
  planning language are superseded by this specification.
* The prior foreign-lock result is historical. Fresh initial and final root
  validation pass because that lock cleared naturally; FAM-003 did not mutate it.
* Historical performance/root PASS receipts remain evidence only.
* Durable ORIN Core animation-policy ownership is not explicit enough for
  mutation and is routed as a source-truth/owner decision gap.
* Source truth defines the state-root prerequisite and then lists migration as
  the first ordered concurrency lock. This packet reconciles them as
  `state-root -> migration -> worktree -> branch`; no competing order remains.
* Current source truth defines per-target atomic replacement, not a physical
  three-file filesystem transaction. This packet requires logical all-or-none
  completion, one transaction audit, and mandatory snapshot rollback.
"""


def _primary() -> str:
    return f"""# FAM-003 Option D Performance Final Decision Review

Packet Status: `READY_FOR_USER_DECISION`

Current Gate: `{CURRENT_GATE}`
Workstream Result: `{WORKSTREAM_RESULT}`
H1 / LV / UTS: `{STAGE_STATES}`
Final Root-Wide Result: `{ROOT_RESULT}`
Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`
Target Currentness: `{TARGET_RESULT}`

## Decision Summary

The nonintrusive Option D investigation remains useful decision-quality
evidence. It proves a high absolute resident CPU posture, persistent Core
animation activity, native polling candidates, retained WebEngine process and
private-memory posture, and monotonic HUD-renderer USS growth. It does not prove
a memory leak, safe renderer equivalence, a numeric regression, permanent
Option D suitability, or a legal ORIN Core animation-policy owner.

Option G remains the recommended direction, but it is migration-first. The
current actionable decision is only Decision 1. Decision 2 cannot begin until
the migration is complete and target plus root validation are green. Decision 3
is a separate planning-only owner/vision route.

## USER Decisions

Read `Review Aids/08_DECISION_SEQUENCE_AND_BOUNDARIES.md` for the three exact,
separate approval texts:

1. FAM-003-local external-state schema migration.
2. Option G BP2/BP3/Workstream revision preparation only after migration
   validation is green.
3. Separate future ORIN Core owner/vision decision-packet preparation.

This packet does not authorize any of them automatically and never combines
them into implementation authority.

## Current Boundaries

No schema migration, BP2/BP3/Workstream revision, product implementation,
optimization, ORIN Core change, animation/timer/polling change, renderer change,
permanent Option D adoption, H1, LV, UTS, foreign-lock mutation, sibling or
Governance mutation, issue, PR, merge, release, or cleanup occurred.
"""


def _start_here(mappings: dict[str, str]) -> str:
    mapping_rows = "\n".join(
        f"| `{source}` | `{copied}` |" for source, copied in sorted(mappings.items())
    )
    return f"""# FAM-003 Option D Performance Final Decision Packet

Packet Reviewability State: `READY_FOR_USER_DECISION`

Current Gate: `{CURRENT_GATE}`
Workstream Result: `{WORKSTREAM_RESULT}`
H1 / LV / UTS: `{STAGE_STATES}`
Final Root-Wide Result: `{ROOT_RESULT}`
Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`
Target Currentness: `{TARGET_RESULT}`

Primary USER Review: `USER Review/FAM003_OPTION_D_PERFORMANCE_FINAL_DECISION_REVIEW.md`

## Review Order

1. Read the primary USER review.
2. Read `Review Aids/01_CURRENT_PERFORMANCE_EVIDENCE.md` through
   `Review Aids/09_VALIDATION_PROOF_ROLLBACK_AND_STALENESS.md`.
3. Inspect the loaded-authority and artifact manifests.
4. Treat Decision 1, Decision 2, and Decision 3 as separate gates.

The final archive path and digest are recorded outside the archive after generation.
This is not a migration, planning-revision, implementation, H1, LV, or UTS
packet. Root validation is green, but all three target-currentness checks remain
blocked until a separately approved migration is executed.

## Source / Copy File Mapping

| Repo source | Packet copy |
| --- | --- |
{mapping_rows}
"""


def _identity_context(head: str, origin_main: str) -> str:
    return f"""# Packet Identity And Final Validation Context

Source Branch: `feature/fam-003-settings-resize-proof`
Source HEAD / Upstream: `{head}`
origin/main / Merge Base: `{origin_main}`
Final Root-Wide Result: `{ROOT_RESULT}`
Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`
Target Currentness Result: `{TARGET_RESULT}`

This generated proof-context file owns technical Git and validation identity.
The USER-facing files intentionally contain decision substance rather than
generator metadata.
"""


def _technical_migration_context(
    head: str,
    origin_main: str,
    target_hashes: dict[str, str],
) -> str:
    return _migration_spec(head, origin_main, target_hashes)


def _semantic_document() -> str:
    return "\n".join(
        (
            f"Final Root-Wide Result: `{ROOT_RESULT}`",
            f"Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`",
            "Prior packet final root/Stage 4 validation: `BLOCKED_BY_FOREIGN_LIVE_LOCK` is historical evidence only.",
            "A foreign lock is never cleared, recovered, adopted, bypassed, or mutated by this execution.",
            f"Target Currentness Result: `{TARGET_RESULT}`",
            "Planning Route While Blocked: `SCHEMA_MIGRATION_DECISION_ONLY / NO BP2_BP3_WORKSTREAM_REVISION`",
            "Decision 1 - FAM-003-Local External-State Schema Migration",
            "Decision 2 - Refined Option G Planning-Revision Preparation",
            "Decision 3 - Future ORIN Core Owner / Vision Routing",
            "Decision 1 migration approval -> FAM-003-local migration -> target-currentness green -> root-wide validation green -> Decision 2 planning-revision preparation",
            "Log Viewer Studio resize-hover polling",
            "Recording Studio polling unless separately proven and admitted",
            "Mandatory Stop Boundary: `STOP_AND_RETURN_FOR_USER_DECISION`",
            "Current carrier access does not transfer ownership.",
            "Carryforward Status: `SEPARATE_OWNER_VISION_DECISION_PACKET_REQUIRED`",
            "## Complete Live-Header Field Union",
            "`External State Schema` `State Version` `Record Class` `Record Role` `Branch` `Source Repo HEAD` `Origin/Main` `Worktree` `Worktree Path` `Slot ID` `Last Updated` `Last Updated By` `Historical Receipt Boundary`",
            "Legacy pre-state is `ABSENT`; first migrated projection initializes at 1. All three commit at version 1.",
            "`Last Updated` uses one transition-wide UTC timestamp in RFC 3339 seconds and `Last Updated By` is `Codex`.",
            "`Worktree` and `Worktree Path` are both required: `FAM-003` and `C:\\Nexus Worktrees\\FAM-003`.",
            "| `branch_plan.md` | `Live Branch Plan` | `Current active branch engineering plan fields` |",
            "| `branch_state.md` | `Live Branch Projection` | `Current active branch phase, blocker, and next legal phase fields` |",
            "| `worktree_state.md` | `Live Worktree Projection` | `Current assignment and acknowledgement fields for one worktree` |",
            "None of those older fields may satisfy live-header validation.",
            "The `Historical Receipt Boundary` is the final live-header field immediately before the first existing `##` heading.",
            "Lock order: `state-root -> migration -> worktree -> branch`; release is `branch -> worktree -> migration -> state-root`.",
            "Foreign-lock no-write rule: any foreign or conflicting live lock blocks mutation.",
            "| `branch_plan.md` | `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` | Must match before any lock-backed staging or write. |",
            "| `branch_state.md` | `BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB` | Must match before any lock-backed staging or write. |",
            "| `worktree_state.md` | `CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC` | Must match before any lock-backed staging or write. |",
            "Snapshot contract covers all three exact target bytes, relative paths, file count, and hashes; logical all-or-none completion applies.",
            "Logical all-or-none completion requires all three replacements; any failure restores every target already replaced.",
            "Root/Stage 4 validation must reach root PASS before migration completion.",
            "Completion proves no central, sibling, Governance, selected-next, repo, or other target changed.",
            f"Evidence volume: `{RAW_SAMPLE_COUNT}` raw samples.",
            f"Current Gate: `{CURRENT_GATE}`",
            f"Workstream Result: `{WORKSTREAM_RESULT}`",
            f"H1 / LV / UTS: `{STAGE_STATES}`",
        )
    )


def _semantic_failures(text: str) -> list[str]:
    failures: list[str] = []
    normalized_text = re.sub(r"\s+", " ", text)
    required = {
        "root-current-result-misreported": f"Final Root-Wide Result: `{ROOT_RESULT}`",
        "foreign-lock-result-missing": f"Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`",
        "historical-foreign-lock-currentness-missing": "Prior packet final root/Stage 4 validation",
        "foreign-lock-write-precondition-missing": "foreign lock is never cleared, recovered, adopted, bypassed, or mutated",
        "target-currentness-blocker-missing": f"Target Currentness Result: `{TARGET_RESULT}`",
        "blocked-target-routes-directly-to-planning": "Planning Route While Blocked: `SCHEMA_MIGRATION_DECISION_ONLY / NO BP2_BP3_WORKSTREAM_REVISION`",
        "decision-1-missing": "Decision 1 - FAM-003-Local External-State Schema Migration",
        "decision-2-missing": "Decision 2 - Refined Option G Planning-Revision Preparation",
        "decision-3-missing": "Decision 3 - Future ORIN Core Owner / Vision Routing",
        "migration-planning-order-invalid": "Decision 1 migration approval -> FAM-003-local migration -> target-currentness green -> root-wide validation green -> Decision 2 planning-revision preparation",
        "log-viewer-scope-missing": "Log Viewer Studio resize-hover polling",
        "recording-studio-exclusion-missing": "Recording Studio polling unless separately proven and admitted",
        "hud-authority-open-ended": "Mandatory Stop Boundary: `STOP_AND_RETURN_FOR_USER_DECISION`",
        "carrier-access-treated-as-ownership": "Current carrier access does not transfer ownership.",
        "orin-core-routing-missing": "Carryforward Status: `SEPARATE_OWNER_VISION_DECISION_PACKET_REQUIRED`",
        "live-schema-union-missing": "## Complete Live-Header Field Union",
        "state-version-transition-missing": "Legacy pre-state is `ABSENT`; first migrated projection initializes at 1. All three commit at version 1.",
        "timestamp-updater-rule-missing": "one transition-wide UTC timestamp",
        "worktree-label-path-rule-missing": "`Worktree` and `Worktree Path` are both required",
        "branch-plan-assignment-missing": "| `branch_plan.md` | `Live Branch Plan` | `Current active branch engineering plan fields` |",
        "branch-state-assignment-missing": "| `branch_state.md` | `Live Branch Projection` | `Current active branch phase, blocker, and next legal phase fields` |",
        "worktree-state-assignment-missing": "| `worktree_state.md` | `Live Worktree Projection` | `Current assignment and acknowledgement fields for one worktree` |",
        "historical-live-separation-missing": "None of those older fields may satisfy live-header validation",
        "historical-boundary-placement-missing": "final live-header field immediately before the first existing `##` heading",
        "lock-order-missing": "state-root -> migration -> worktree -> branch",
        "snapshot-rollback-incomplete": "Snapshot contract covers all three exact target bytes, relative paths, file count, and hashes",
        "atomic-all-three-missing": "any failure restores every target already replaced",
        "root-completion-gate-missing": "root PASS",
        "mutation-boundary-ambiguous": "no central, sibling, Governance, selected-next, repo, or other target changed",
        "raw-evidence-count-mismatch": f"`{RAW_SAMPLE_COUNT}` raw samples",
        "gate-drift": f"Current Gate: `{CURRENT_GATE}`",
        "workstream-result-drift": f"Workstream Result: `{WORKSTREAM_RESULT}`",
        "stage-state-drift": f"H1 / LV / UTS: `{STAGE_STATES}`",
    }
    for code, marker in required.items():
        if re.sub(r"\s+", " ", marker).casefold() not in normalized_text.casefold():
            failures.append(code)
    union_fields = (
        "External State Schema", "State Version", "Record Class", "Record Role",
        "Branch", "Source Repo HEAD", "Origin/Main", "Worktree", "Worktree Path",
        "Slot ID", "Last Updated", "Last Updated By", "Historical Receipt Boundary",
    )
    if any(f"`{field}`" not in text for field in union_fields):
        failures.append("live-schema-union-missing")
    hash_rows = re.findall(
        r"\| `(branch_plan\.md|branch_state\.md|worktree_state\.md)` \| `([A-Fa-f0-9]{64})` \|",
        text,
    )
    if {name for name, _digest in hash_rows} != {
        "branch_plan.md", "branch_state.md", "worktree_state.md"
    }:
        failures.append("pre-write-hashes-missing")
    if re.search(
        r"(?:Record (?:Class|Role)[^\n]{0,40}|\| `Live [^`]+` \| `?)(?:TBD|appropriate|current value|as routed)",
        text,
        re.IGNORECASE,
    ):
        failures.append("record-class-role-placeholder")
    if "resizable Studio native polling" in text:
        failures.append("ambiguous-studio-scope")
    if "`573` raw samples" in text or "573 raw samples" in text:
        failures.append("raw-evidence-count-mismatch")
    return sorted(set(failures))


def _raw_sample_count(packet_folder: Path) -> int:
    root = packet_folder / "Source Truth Context" / "Proof Artifacts" / "Raw Observer Results"
    total = 0
    result_files = sorted(root.glob("session_*/observer_results/*.json"))
    if len(result_files) != 21:
        raise PacketValidationError(f"expected 21 raw interval files, found {len(result_files)}")
    for path in result_files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        count = int(payload.get("rawSampleCount", -1))
        samples = payload.get("rawSamples")
        if not isinstance(samples, list) or len(samples) != count:
            raise PacketValidationError(f"raw sample parity failed: {path}")
        total += count
    return total


def _folder_hashes(packet_folder: Path) -> dict[str, str]:
    return {
        path.relative_to(packet_folder).as_posix(): _sha256(path)
        for path in sorted(packet_folder.rglob("*"))
        if path.is_file()
    }


def _zip_hashes(packet_zip: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    with zipfile.ZipFile(packet_zip) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            hashes[PurePosixPath(info.filename).as_posix()] = hashlib.sha256(
                archive.read(info)
            ).hexdigest().upper()
    return hashes


def validate_packet(packet_folder: Path, packet_zip: Path | None) -> dict[str, Any]:
    if not packet_folder.is_dir():
        raise PacketValidationError(f"packet folder missing: {packet_folder}")
    primary_files = sorted((packet_folder / "USER Review").glob("*.md"))
    if primary_files != [packet_folder / PRIMARY_RELATIVE]:
        raise PacketValidationError(
            f"expected one current primary {PRIMARY_RELATIVE}, found {primary_files}"
        )
    missing = [str(path) for path in CORE_RELATIVES if not (packet_folder / path).is_file()]
    if missing:
        raise PacketValidationError(f"required packet files missing: {missing}")
    active_text = "\n".join(
        (packet_folder / path).read_text(encoding="utf-8") for path in CORE_RELATIVES
    )
    failures = _semantic_failures(active_text)
    if failures:
        raise PacketValidationError("semantic validation failed: " + ", ".join(failures))
    raw_count = _raw_sample_count(packet_folder)
    if raw_count != RAW_SAMPLE_COUNT:
        raise PacketValidationError(
            f"raw-evidence-count-mismatch: expected {RAW_SAMPLE_COUNT}, found {raw_count}"
        )
    folder_hashes = _folder_hashes(packet_folder)
    if packet_zip is not None:
        zip_hashes = _zip_hashes(packet_zip)
        if folder_hashes != zip_hashes:
            missing_zip = sorted(set(folder_hashes) - set(zip_hashes))
            extra_zip = sorted(set(zip_hashes) - set(folder_hashes))
            mismatched = sorted(
                key for key in set(folder_hashes) & set(zip_hashes)
                if folder_hashes[key] != zip_hashes[key]
            )
            raise PacketValidationError(
                f"folder/ZIP parity failed: missing={missing_zip}, extra={extra_zip}, "
                f"mismatched={mismatched}"
            )
    return {
        "status": "PASS",
        "fileCount": len(folder_hashes),
        "rawSampleCount": raw_count,
        "rootWideResult": ROOT_RESULT,
        "targetCurrentness": TARGET_RESULT,
        "foreignLockResult": FOREIGN_LOCK_RESULT,
    }


def _manifest(packet_folder: Path) -> str:
    files = sorted(
        path.relative_to(packet_folder).as_posix()
        for path in packet_folder.rglob("*")
        if path.is_file()
    )
    category_counts: dict[str, int] = {}
    for relative in files:
        category = relative.split("/", 1)[0]
        category_counts[category] = category_counts.get(category, 0) + 1
    rows = "\n".join(
        f"| `{category}` | {count} |" for category, count in sorted(category_counts.items())
    )
    return f"""# Artifact Manifest

Manifest Status: `CURRENT_DECISION_PACKET`
Final Root-Wide Result: `{ROOT_RESULT}`
Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`
Target Currentness Result: `{TARGET_RESULT}`
Raw Evidence: `{RAW_SAMPLE_COUNT}` raw samples across 21 intervals and three sessions.

| Packet area | Files before this manifest |
| --- | ---: |
{rows}

The final exact folder/archive file count and archive digest are computed after all
packet files, including this manifest, are written. The final archive digest remains
outside the ZIP to avoid self-hash contradiction.
"""


def generate_packet(
    seed_zip: Path | None,
    seed_folder: Path | None,
    packet_folder: Path,
    output_zip: Path,
    head: str,
    origin_main: str,
) -> dict[str, Any]:
    if seed_zip is not None:
        if not seed_zip.is_file():
            raise PacketValidationError(f"seed packet missing: {seed_zip}")
        seed_members = _safe_seed_members(seed_zip)
    elif seed_folder is not None:
        if not seed_folder.is_dir():
            raise PacketValidationError(f"seed packet folder missing: {seed_folder}")
        seed_members = _safe_seed_folder(seed_folder)
    else:
        raise PacketValidationError("one seed packet source is required")
    if packet_folder.exists():
        shutil.rmtree(packet_folder)
    packet_folder.mkdir(parents=True)
    for stale in USER_ROOT.glob("FAM-003*.zip"):
        stale.unlink()
    for stale in USER_ROOT.glob("FAM-003*.sha*"):
        stale.unlink()

    _extract_seed(seed_members, packet_folder)
    _copy_external_snapshots(packet_folder)
    mappings = _refresh_repo_context(packet_folder)
    target_hashes = {
        name: _sha256(path)
        for name, path, _record_class, _record_role in MIGRATION_TARGETS
    }

    documents = {
        Path("START_HERE.md"): _start_here(mappings),
        PRIMARY_RELATIVE: _primary(),
        Path("Review Aids/01_CURRENT_PERFORMANCE_EVIDENCE.md"): _performance_facts(),
        Path("Review Aids/02_FINAL_EXTERNAL_VALIDATION_CHRONOLOGY.md"): _chronology(),
        Path("Review Aids/03_TARGET_CURRENTNESS_AND_MIGRATION_SPEC.md"): _migration_review_aid(),
        Path("Review Aids/04_REFINED_OPTION_G_SCOPE.md"): _option_g_scope(),
        Path("Review Aids/05_HUD_FAIL_CLOSED_ENVELOPE.md"): _hud_envelope(),
        Path("Review Aids/06_ORIN_CORE_OWNER_VISION_CARRYFORWARD.md"): _core_carryforward(),
        Path("Review Aids/07_OWNERSHIP_AND_CARRIER_MATRIX.md"): _ownership_matrix(),
        Path("Review Aids/08_DECISION_SEQUENCE_AND_BOUNDARIES.md"): _decision_sequence(),
        Path("Review Aids/09_VALIDATION_PROOF_ROLLBACK_AND_STALENESS.md"): _validation_and_staleness(),
        Path("Review Aids/10_FILES_LOADED_AND_AUTHORITY.md"): _authority(),
        Path("Source Truth Context/Git Audit/PACKET_IDENTITY.md"): _identity_context(
            head, origin_main
        ),
        Path("Source Truth Context/Git Audit/FINAL_EXTERNAL_VALIDATION_CHRONOLOGY.md"): _chronology(),
        Path("Source Truth Context/Git Audit/TARGET_CURRENTNESS_AND_MIGRATION_SPEC.md"): _technical_migration_context(
            head, origin_main, target_hashes
        ),
    }
    for relative, content in documents.items():
        _write_text(packet_folder / relative, content)
    _write_text(
        packet_folder / "Review Aids/11_ARTIFACT_MANIFEST.md",
        _manifest(packet_folder),
    )

    pre_zip = validate_packet(packet_folder, None)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(packet_folder.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(packet_folder).as_posix())
    final = validate_packet(packet_folder, output_zip)
    final["zipPath"] = str(output_zip)
    final["zipSha256"] = _sha256(output_zip)
    final["preZipValidation"] = pre_zip["status"]
    return final


def self_test() -> dict[str, Any]:
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    base = _semantic_document()
    passed = 0
    details: list[dict[str, str]] = []
    replacements = {
        "root_not_pass": ("Final Root-Wide Result: `PASS`", "Final Root-Wide Result: `BLOCKED`"),
        "historical_foreign_blocker_omitted": ("Prior packet final root/Stage 4 validation: `BLOCKED_BY_FOREIGN_LIVE_LOCK` is historical evidence only.", ""),
        "direct_planning_from_blocked_target": ("Planning Route While Blocked: `SCHEMA_MIGRATION_DECISION_ONLY / NO BP2_BP3_WORKSTREAM_REVISION`", "Planning Route While Blocked: `BP2 REVISION`"),
        "planning_before_migration_green": ("Decision 1 migration approval -> FAM-003-local migration -> target-currentness green -> root-wide validation green -> Decision 2 planning-revision preparation", "Decision 2 planning-revision preparation -> Decision 1 migration approval"),
        "ambiguous_studio_scope": ("Log Viewer Studio resize-hover polling", "resizable Studio native polling"),
        "open_ended_hud_authority": ("Mandatory Stop Boundary: `STOP_AND_RETURN_FOR_USER_DECISION`", ""),
        "carrier_access_claims_ownership": ("Current carrier access does not transfer ownership.", "Current carrier access transfers ownership."),
        "orin_core_routing_omitted": ("Carryforward Status: `SEPARATE_OWNER_VISION_DECISION_PACKET_REQUIRED`", ""),
        "foreign_lock_result_omitted": (f"Current Foreign Lock Result: `{FOREIGN_LOCK_RESULT}`", ""),
        "raw_count_573": ("`780` raw samples", "`573` raw samples"),
        "live_schema_union_omitted": ("## Complete Live-Header Field Union", "## Partial Target Fields"),
        "state_metadata_omitted": ("`Last Updated` uses one transition-wide UTC timestamp in RFC 3339 seconds and `Last Updated By` is `Codex`.", ""),
        "per_target_values_absent": ("| `branch_plan.md` | `Live Branch Plan` | `Current active branch engineering plan fields` |", ""),
        "placeholder_record_role": ("Current active branch engineering plan fields", "TBD"),
        "historical_fields_treated_live": ("None of those older fields may satisfy live-header validation.", "Historical fields may satisfy live-header validation."),
        "historical_boundary_unspecified": ("The `Historical Receipt Boundary` is the final live-header field immediately before the first existing `##` heading.", ""),
        "state_version_transition_unspecified": ("Legacy pre-state is `ABSENT`; first migrated projection initializes at 1. All three commit at version 1.", ""),
        "lock_order_unspecified": ("Lock order: `state-root -> migration -> worktree -> branch`; release is `branch -> worktree -> migration -> state-root`.", ""),
        "foreign_lock_allows_write": ("A foreign lock is never cleared, recovered, adopted, bypassed, or mutated by this execution.", "A foreign lock may be cleared so the write can continue."),
        "snapshot_rollback_incomplete": ("Snapshot contract covers all three exact target bytes, relative paths, file count, and hashes; logical all-or-none completion applies.", "Snapshot contract is unspecified."),
        "atomic_all_three_not_required": ("Logical all-or-none completion requires all three replacements; any failure restores every target already replaced.", "Individual target success may be accepted."),
        "planning_authorized_before_green": ("Decision 1 migration approval -> FAM-003-local migration -> target-currentness green -> root-wide validation green -> Decision 2 planning-revision preparation", "Decision 2 planning-revision preparation is immediately authorized"),
        "root_completion_omitted": ("Root/Stage 4 validation must reach root PASS before migration completion.", "Root validation is optional."),
        "mutation_boundaries_ambiguous": ("Completion proves no central, sibling, Governance, selected-next, repo, or other target changed.", "Mutation scope is flexible."),
    }
    for case in fixtures["cases"]:
        mutation = case["mutation"]
        text = base
        if mutation == "prewrite_hashes_unspecified":
            text = re.sub(
                r"^\| `(branch_plan\.md|branch_state\.md|worktree_state\.md)` \| `[A-Fa-f0-9]{64}` \|.*$",
                "",
                text,
                flags=re.MULTILINE,
            )
        elif mutation in replacements:
            old, new = replacements[mutation]
            text = text.replace(old, new)
        else:
            raise PacketValidationError(f"unknown negative fixture mutation: {mutation}")
        failures = _semantic_failures(text)
        expected = case["expectedFailure"]
        if expected not in failures:
            raise PacketValidationError(
                f"negative fixture {case['id']} did not fail as expected: {expected}; {failures}"
            )
        passed += 1
        details.append({"id": case["id"], "result": "PASS", "failure": expected})
    return {"status": "PASS", "passed": passed, "total": len(fixtures["cases"]), "cases": details}


def _default_zip() -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return USER_ROOT / f"FAM-003-{stamp}.zip"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--validate", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--seed-zip", type=Path)
    parser.add_argument("--seed-folder", type=Path)
    parser.add_argument("--packet-folder", type=Path, default=PACKET_FOLDER)
    parser.add_argument("--packet-zip", type=Path)
    parser.add_argument("--head")
    parser.add_argument("--origin-main")
    args = parser.parse_args()
    try:
        if args.self_test:
            result = self_test()
        elif args.generate:
            required = {
                "--head": args.head,
                "--origin-main": args.origin_main,
            }
            missing = [name for name, value in required.items() if not value]
            if bool(args.seed_zip) == bool(args.seed_folder):
                missing.append("exactly one of --seed-zip or --seed-folder")
            if missing:
                raise PacketValidationError(f"generate arguments missing: {missing}")
            output_zip = args.packet_zip or _default_zip()
            result = generate_packet(
                args.seed_zip,
                args.seed_folder,
                args.packet_folder,
                output_zip,
                args.head,
                args.origin_main,
            )
        else:
            if not args.packet_zip:
                raise PacketValidationError("--packet-zip is required with --validate")
            result = validate_packet(args.packet_folder, args.packet_zip)
            result["zipPath"] = str(args.packet_zip)
            result["zipSha256"] = _sha256(args.packet_zip)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, PacketValidationError) as exc:
        print(f"FAM-003 PERFORMANCE DECISION PACKET: FAIL - {exc}")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    print("FAM-003 PERFORMANCE DECISION PACKET: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
