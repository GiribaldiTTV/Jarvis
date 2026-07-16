"""Fail-closed Git-to-ledger audit for FAM-003 R2 Workstream completion.

Helper Status: Workstream-scoped
Owner Workstream: FAM-003 R2 HUD baseline access completion audit
Reason Reusable Helper Was Not Extended: The audit is bound to the accepted
    FAM-003 R2 base commit, branch file set, Slice/SLC/seam contract, and
    completion-packet schema.
Consolidation Target: A reusable Git-to-packet scope-audit helper after a
    second branch needs the same exact changed-file and commit inventory gate.
Promotion Decision Point: PR Readiness for this branch or the next consumer.
"""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKSTREAM_BASE = "1806927765013f0c7d1a13335af2ca5cfce5325e"
FIXTURE_PATH = ROOT / "dev" / "fixtures" / "fam003_r2_scope_audit_negative_cases.json"
SCHEMA_VERSION = "fam003-r2-workstream-scope-audit-v1"

REQUIRED_ROW_FIELDS = (
    "path",
    "status",
    "commits",
    "changeCategory",
    "sourceTruthOwner",
    "legalCarrierBasis",
    "whyChanged",
    "sliceSlcSeamTraceability",
    "behaviorAffected",
    "overlapRisk",
    "validationPerformed",
    "rollbackConsideration",
    "deltaMembership",
    "disposition",
)

SHARED_AUDIT_FIELDS = (
    "legalCarrier",
    "repairsStaleFam003Only",
    "altersFam006Expectation",
    "weakensFailure",
    "crossFamilyDrift",
    "falseGreenPrevention",
    "fam006Carryforward",
)

GROUPED_PATH_MARKERS = (
    "shared validators",
    "existing helpers",
    "runtime files",
    "proof artifacts",
    "etc.",
)


def _shared_audit(*, carryforward: str, detail: str) -> dict[str, str]:
    return {
        "legalCarrier": "YES - FAM-003 may repair its own stale expectations in a registered shared validator.",
        "repairsStaleFam003Only": detail,
        "altersFam006Expectation": "NO - no FAM-006 product state, runtime contract, schema, or target behavior is redefined.",
        "weakensFailure": "NO - the change is fail-closed or replaces a retired FAM-003 expectation with the accepted current route.",
        "crossFamilyDrift": "NO - current FAM-003 behavior is isolated from retained FAM-006 ownership.",
        "falseGreenPrevention": "YES - stale, grouped, omitted, or mismatched FAM-003 proof is rejected.",
        "fam006Carryforward": carryforward,
    }


def _meta(
    category: str,
    owner: str,
    carrier: str,
    why: str,
    trace: str,
    behavior: str,
    overlap: str,
    validation: str,
    rollback: str,
    *,
    disposition: str = "IN_SCOPE",
    shared: dict[str, str] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "changeCategory": category,
        "sourceTruthOwner": owner,
        "legalCarrierBasis": carrier,
        "whyChanged": why,
        "sliceSlcSeamTraceability": trace,
        "behaviorAffected": behavior,
        "overlapRisk": overlap,
        "validationPerformed": validation,
        "rollbackConsideration": rollback,
        "disposition": disposition,
    }
    if shared is not None:
        result["sharedValidatorAudit"] = shared
    return result


FILE_METADATA: dict[str, dict[str, Any]] = {
    "Docs/branch_records/feature_fam_003_settings_resize_proof.md": _meta(
        "documentation/source truth",
        "Branch-record authority for feature/fam-003-settings-resize-proof",
        "FAM-003 BR2 carrier setup on the assigned branch",
        "Created the durable branch record and legal carrier pointer.",
        "Historical BR2/BP1 carrier setup; no R2 Workstream code seam.",
        "Branch identity, confinement, and routed authority.",
        "None; records FAM-003 only.",
        "Branch governance, confinement, source-owner, and readiness fixture validation.",
        "Retire only through the governed branch-record fold-down after merge; do not delete during Workstream.",
        disposition="ADJACENT_REQUIRED",
    ),
    "Docs/branch_records/index.md": _meta(
        "documentation/source truth",
        "Branch-record index",
        "Required router update for the admitted FAM-003 carrier",
        "Added the exact active branch-record route.",
        "Historical BR2 carrier routing; no R2 Workstream code seam.",
        "Source-truth discoverability for the current branch.",
        "None; index-only pointer.",
        "Branch governance, source-owner, and readiness fixture validation.",
        "Remove or fold the pointer only with the branch-record lifecycle action.",
        disposition="ADJACENT_REQUIRED",
    ),
    "Docs/governance_docs_full_inventory_reform_audit.md": _meta(
        "documentation/source truth",
        "Governance docs inventory manifest",
        "Mechanical manifest synchronization required when the branch record was added",
        "Updated Docs counts and the generated inventory row sequence for the new branch record.",
        "Historical branch setup manifest synchronization; no R2 Workstream seam.",
        "Docs inventory parity only; no product or phase authority change.",
        "Low; generated inventory can drift if edited independently.",
        "Governance efficiency and source-owner validation.",
        "Rebuild the inventory from current Docs state; never hand-delete unrelated rows.",
        disposition="ADJACENT_REQUIRED",
    ),
    "Docs/governance_docs_reform_user_review_index.md": _meta(
        "documentation/source truth",
        "Governance docs inventory review index",
        "Mechanical companion synchronization for the added branch record",
        "Updated Docs totals and ambiguity counts to match the inventory owner.",
        "Historical branch setup manifest synchronization; no R2 Workstream seam.",
        "Inventory-review counts only.",
        "Low; must remain synchronized with the full inventory dossier.",
        "Governance efficiency validation.",
        "Regenerate from the full inventory owner if counts drift.",
        disposition="ADJACENT_REQUIRED",
    ),
    "Docs/validation_helper_registry.md": _meta(
        "documentation/source truth",
        "Validation helper registry",
        "Registered FAM-003 Workstream-scoped helpers and their retention/consolidation contract",
        "Recorded helper ownership, proof limits, reuse posture, and this exact-scope completion gate.",
        "Slice E / SLC-R2-009 and SLC-R2-010 / R2-WS09 and R2-WS10.",
        "Validator ownership and packet false-green prevention.",
        "No product overlap; future branches must respect helper status rather than infer shared product ownership.",
        "Source-owner marker, governance efficiency, branch governance, and scope-audit validation.",
        "Revert only the FAM-003 rows together with the helpers they register.",
    ),
    "desktop/desktop_renderer.py": _meta(
        "Global Settings UI",
        "FAM-003 Settings doorway consuming FAM-002 grammar and FAM-006 state truth",
        "Accepted BP1-R2/BP2-R2/BP3-R2 bounded FAM-003 integration surface",
        "Added the persistent HUD parent/child, owner-backed enable/disable/open/retry UI, and result-bearing HUD access callbacks.",
        "Slices A/B/D / SLC-R2-002,003,004,007,008 / R2-WS02,03,04,07,08.",
        "Global Settings HUD navigation, status, failure/retry, lifecycle, and responsive visual behavior.",
        "Medium: shared renderer contains FAM-006 runtime methods, but the delta preserves FAM-006 semantics behind the adapter.",
        "HUD access state matrix, HUD visual, Settings regression, desktop entrypoint, resident, and aggregate validators.",
        "Revert the R2 HUD Settings and adapter wiring while preserving prior Quick Access/Settings implementation.",
    ),
    "desktop/monitoring_hud_access.py": _meta(
        "adapter/state integration",
        "FAM-003 owner-bounded access adapter; FAM-006 retains state/runtime semantics",
        "Accepted public integration boundary in BP2-R2/BP3-R2",
        "Added the public query/action/result, retry, generation, coalescing, and shutdown contract used by FAM-003 consumers.",
        "Slice A/D / SLC-R2-001,002,007,008 / R2-WS01,02,07,08.",
        "Deterministic owner-backed state access and action results without direct consumer JSON writes.",
        "Medium: future FAM-006 state evolution must continue through this boundary or an approved replacement.",
        "Exact 26-state HUD access validator, bypass negatives, entrypoint, resident, and aggregate proof.",
        "Remove adapter construction and consumers together; do not migrate or erase the FAM-006-owned state file.",
    ),
    "desktop/orin_desktop_main.py": _meta(
        "product/runtime",
        "Desktop composition root with FAM-003 bounded integration",
        "Accepted R2 startup/shutdown composition seam",
        "Constructed the real or unavailable HUD adapter and bound startup, route refresh, and shutdown lifecycle.",
        "Slice D / SLC-R2-007,008 / R2-WS07,08.",
        "Startup owner-state read, adapter availability, and shutdown suppression.",
        "Low to medium: composition touches the FAM-006 runtime object but does not change its ownership or internals.",
        "Desktop entrypoint, HUD access, resident, and aggregate validators.",
        "Remove the adapter construction/binding and fall back to the pre-R2 unavailable path.",
    ),
    "desktop/resident_access.py": _meta(
        "tray/resident access",
        "FAM-003 resident access model",
        "Existing accepted Option C resident carrier predating the R2 implementation range",
        "Added HUD menu structure/model vocabulary that the R2 tray synchronization consumes.",
        "Slice C / SLC-R2-005 / R2-WS05 supporting model present at Workstream entry; historical pre-R2 delta.",
        "Resident menu-plan HUD submenu declaration.",
        "Low: target remains FAM-006-owned, while visibility/routing remains FAM-003-owned.",
        "Resident access and tray/aggregate validators.",
        "Remove the HUD menu plan only with the tray route; preserve other resident entries.",
    ),
    "desktop/tray_controller.py": _meta(
        "tray/resident access",
        "FAM-003 resident tray doorway",
        "Accepted BP1-R2/BP2-R2/BP3-R2 tray synchronization and open/restore seam",
        "Bound the compact HUD submenu to confirmed adapter truth and made Open HUD Dashboard open or restore rather than toggle closed.",
        "Slice C / SLC-R2-005,006 / R2-WS05,06.",
        "Resident menu visibility, enabled/blocked states, route refresh, and target action.",
        "Medium: FAM-006 owns the target runtime; FAM-003 only owns route presentation and request dispatch.",
        "Resident, desktop entrypoint, shared HUD regression, HUD access, and aggregate validators.",
        "Hide/remove only the HUD submenu and adapter callbacks; preserve Global Settings, Quick Access, AI, and Exit.",
    ),
    "dev/fixtures/branch_readiness_planning/fam003_bp3_orchestration_consistency.json": _meta(
        "fixture",
        "Reusable branch-planning fixture suite with FAM-003 case ownership",
        "FAM-003 BP3 packet consistency repair before R2 Workstream entry",
        "Added positive and negative BP3 phase/visual-decision fixtures.",
        "Historical BP3 orchestration gate; supports Slice E planning but is outside R2-WS01..10 execution delta.",
        "Prevents BP3 from executing H1/LV/UTS or using a pending visual target.",
        "None; fixture is FAM-003-specific inside a shared suite.",
        "Branch readiness planning fixture validation.",
        "Remove with the matching fixture-validation case only if the BP3 contract is retired.",
        disposition="ADJACENT_REQUIRED",
    ),
    "dev/fixtures/fam003_hud_access_state_matrix.json": _meta(
        "fixture",
        "FAM-003 R2 HUD access Workstream",
        "Accepted 26-state BP2/BP3 proof contract",
        "Encoded every accepted normal, failure, retry, concurrency, lifecycle, and accessibility state.",
        "Slices A-E / SLC-R2-001 through 010 / R2-WS01 through 10.",
        "Expected owner result, Settings, tray, persistence, and retry behavior for states 01-26.",
        "None; fixture consumes but does not redefine FAM-006 state semantics.",
        "HUD access Workstream validator and aggregate proof.",
        "Remove with the R2 validator only; do not retain a validator that silently loses state coverage.",
    ),
    "dev/fixtures/fam003_r2_scope_audit_negative_cases.json": _meta(
        "fixture",
        "FAM-003 R2 completion scope-audit helper",
        "Current USER-approved packet false-green repair",
        "Adds fail-capable omissions, grouping, commit, owner, range, traceability, rename/delete, and HEAD mismatch cases.",
        "Slice E / SLC-R2-010 / R2-WS10 completion packet audit repair.",
        "Proves the exact-scope validator rejects the packet defect class found in review.",
        "None; packet/Git evidence only.",
        "Scope-audit validator self-test and USER packet guard self-test.",
        "Remove only with the scope-audit helper and replacement equivalent negative coverage.",
    ),
    "dev/orin_branch_readiness_planning_fixture_validation.py": _meta(
        "shared validator",
        "Reusable branch-planning fixture validator; FAM-003 owns its added case",
        "Legal FAM-003 BP3 consistency case in the registered reusable validator",
        "Added the FAM-003 BP3 phase-boundary and visual-decision fixture checks.",
        "Historical BP3 orchestration gate; no R2 Workstream execution seam.",
        "Rejects stale/premature FAM-003 planning state.",
        "None; no FAM-006 fixture or expectation changed.",
        "Direct branch readiness planning fixture validation.",
        "Revert the FAM-003 case and fixture together.",
        disposition="ADJACENT_REQUIRED",
        shared=_shared_audit(
            carryforward="NONE - no FAM-006 row changed.",
            detail="YES - only the FAM-003 BP3 orchestration fixture and invocation were added.",
        ),
    ),
    "dev/orin_desktop_entrypoint_validation.py": _meta(
        "shared validator",
        "Reusable desktop entrypoint validator; FAM-003 owns its resident/HUD expectation delta",
        "BP3-R2 names this registered helper as the existing extension point",
        "Replaced retired FAM-003 toggle/private-path expectations with public adapter and open/restore checks.",
        "Slices A/C/D/E / SLC-R2-001,005,006,007,008,009 / R2-WS01,05,06,07,08,09.",
        "Desktop composition, route state, startup/shutdown, and no-bypass regression proof.",
        "Low: shared helper observes FAM-006 target availability but does not redefine target semantics.",
        "Direct desktop entrypoint validation and aggregate child result.",
        "Revert only the FAM-003 HUD assertions if the R2 route is rolled back.",
        shared=_shared_audit(
            carryforward="NONE beyond normal post-main regression rerun by FAM-006.",
            detail="YES - all changed assertions describe the accepted FAM-003 adapter and resident route.",
        ),
    ),
    "dev/orin_fam003_hud_access_workstream_validation.py": _meta(
        "FAM-003 validator",
        "FAM-003 R2 HUD access Workstream",
        "New fail-capable validator admitted by BP2-R2/BP3-R2",
        "Validates 26 states, owner persistence, retries, generations, concurrency, shutdown, accessibility, and direct-bypass negatives.",
        "Slices A-E / SLC-R2-001 through 010 / R2-WS01 through 10.",
        "Adapter/state behavior and static consumer-boundary proof.",
        "None; fake owner fixtures isolate FAM-003 integration behavior.",
        "Direct validator and aggregate required child.",
        "Remove only with adapter/fixture rollback or replace with equivalent fail-capable coverage.",
    ),
    "dev/orin_fam003_hud_settings_visual_validation.py": _meta(
        "FAM-003 validator",
        "FAM-003 Settings visual proof consuming the accepted target",
        "BP3-R2 visual implementation-match obligation",
        "Renders disabled, enabled, progress, unavailable, partial, failure/retry, minimum, wide, focus, and Quick Access regression states.",
        "Slices B/E / SLC-R2-003,004,009,010 / R2-WS03,04,09,10.",
        "Settings HUD element/state visual evidence and accepted-target comparison.",
        "None; target/runtime proof does not transfer FAM-006 ownership.",
        "Direct HUD visual validation and aggregate child; final target source is external accepted state.",
        "Remove HUD-specific proof with the HUD page; preserve the broader Settings validator.",
    ),
    "dev/orin_fam003_human_client_live_validation.ps1": _meta(
        "proof helper",
        "FAM-003 normal USER-path live helper",
        "Historical Option C LV readiness work retained as downstream helper availability",
        "Added exact launcher/tray/Settings/NCP visible-control proof support without executing formal LV in R2.",
        "Slice E / SLC-R2-010 / R2-WS10 helper-readiness input; historical pre-R2 delta.",
        "Future normal USER-path evidence production only.",
        "Low; optional FAM-006 integration remains explicitly separate and owner-bound.",
        "PowerShell parser and historical helper validation; formal LV not run in this task.",
        "Retain for later separately approved LV or remove with an approved replacement.",
        disposition="ADJACENT_REQUIRED",
    ),
    "dev/orin_fam003_lv1_real_live_validation.py": _meta(
        "FAM-003 validator",
        "FAM-003 LV1 adjudicator",
        "Historical Option C LV readiness work retained for downstream gate readiness",
        "Added fail-closed adjudication for exact launcher, visible input, optional-route state, and owner-integration separation.",
        "Slice E / SLC-R2-010 / R2-WS10 helper-readiness input; historical pre-R2 delta.",
        "Future LV evidence adjudication; no LV execution in this audit.",
        "Low; explicitly refuses to overclaim FAM-006 end-to-end integration.",
        "Python compile and historical gate fixtures; formal LV not run.",
        "Retain for later separately approved LV or remove with an approved replacement.",
        disposition="ADJACENT_REQUIRED",
    ),
    "dev/orin_fam003_option_c_workstream_proof_validation.py": _meta(
        "proof helper",
        "FAM-003 Option C/R2 aggregate proof",
        "Accepted existing aggregate extension point in BP3-R2",
        "Made HUD access, HUD visual, Settings, resident-adjacent, NCP, and entrypoint children fail closed and emitted current packet evidence.",
        "Slice E / SLC-R2-009,010 / R2-WS09,10.",
        "Whole-package cumulative proof and required-child propagation.",
        "Low; shared HUD children remain regression evidence, not FAM-006 product authority.",
        "Direct aggregate final PASS with all required child results.",
        "Revert only R2 child registration/evidence rows if the R2 package is rolled back.",
    ),
    "dev/orin_fam003_resident_access_validation.py": _meta(
        "FAM-003 validator",
        "FAM-003 resident access Workstream",
        "Accepted resident/tray regression validator extension",
        "Adopted Tray-plus-HUD parent/child IA, adapter-backed open/restore, and no-retired-toggle expectations.",
        "Slices C/E / SLC-R2-005,006,009 / R2-WS05,06,09.",
        "Resident structure, exact labels, route availability, and preserved non-HUD entries.",
        "Low; validates the FAM-003 doorway and only references the FAM-006 target contract.",
        "Direct resident validation and cumulative aggregate coverage.",
        "Revert HUD-specific assertions with the resident route; preserve all earlier resident checks.",
    ),
    "dev/orin_fam003_r2_workstream_scope_audit_validation.py": _meta(
        "packet helper",
        "FAM-003 R2 completion scope audit",
        "Current USER-approved exact changed-file and packet false-green repair",
        "Adds deterministic Git inventories, one-row-per-file ledger generation, commit audit, shared-validator review, parity validation, and negative self-tests.",
        "Slice E / SLC-R2-010 / R2-WS10 completion packet audit repair.",
        "Completion packet scope truth and Git-to-ledger parity.",
        "None; read-only Git and packet evidence generation.",
        "Direct validator, negative self-test, packet guard, and folder/ZIP parity.",
        "Remove only with a replacement that preserves exact Git, commit, owner, and range parity checks.",
    ),
    "dev/orin_fam003_settings_repair_visual_validation.py": _meta(
        "FAM-003 validator",
        "FAM-003 Settings visual regression proof",
        "Accepted existing Settings validator extension point",
        "Added the persistent HUD parent/child to IA, stress, geometry, state, and visual regression expectations.",
        "Slices B/E / SLC-R2-003,004,009 / R2-WS03,04,09.",
        "Global Settings rail, content, responsive geometry, dirty guard, and Quick Access regression behavior.",
        "None; no FAM-006 surface internals are rendered or changed.",
        "Direct Settings regression and aggregate required child.",
        "Remove only HUD-specific expectations if the HUD page is rolled back.",
    ),
    "dev/orin_monitoring_hud_internal_sandbox_validation.py": _meta(
        "shared validator",
        "Reusable monitoring/HUD internal sandbox validator; FAM-003 owns changed resident-route assertions",
        "BP3-R2 allows shared validator maintenance needed for current FAM-003 route truth",
        "Removed retired FAM-003 tray-toggle/close/unanchor labels and required current open/restore redirect/request vocabulary.",
        "Slices C/E / SLC-R2-005,006,009 / R2-WS05,06,09.",
        "Cross-surface static regression expectations for the FAM-003 doorway.",
        "Medium: file is monitoring/HUD shared, so later FAM-006 work must rerun it after rebasing without restoring retired FAM-003 assumptions.",
        "Direct internal sandbox validation and aggregate/shared regression suite.",
        "Revert only the bounded FAM-003 token list if the resident route is rolled back.",
        shared=_shared_audit(
            carryforward="FAM-006 should fetch current main, reconcile, and rerun this helper before H1; it must not restore retired FAM-003 toggle/close expectations.",
            detail="YES - changed tokens are solely the FAM-003 resident route vocabulary consumed by this shared regression helper.",
        ),
    ),
    "dev/orin_monitoring_hud_surface_validation.py": _meta(
        "shared validator",
        "Reusable monitoring/HUD surface validator; FAM-003 owns changed command-overlay assertion",
        "BP3-R2 preserves command-overlay behavior as a FAM-003 regression",
        "Replaced the stale visible Close Command Overlay wording with the current Command Overlay surface label.",
        "Slices C/E / SLC-R2-005,009 / R2-WS05,09.",
        "Shared HUD surface regression vocabulary for the FAM-003 command-overlay doorway.",
        "Low: no FAM-006 Dashboard, telemetry, profile, or runtime expectation changed.",
        "Direct monitoring HUD surface validation and aggregate/shared regression suite.",
        "Revert only if the source-owned FAM-003 command-overlay label is itself rolled back.",
        shared=_shared_audit(
            carryforward="FAM-006 should rerun after current-main reconciliation; no product carryforward change is required.",
            detail="YES - one stale FAM-003 visible label was updated; all FAM-006 expectations remain intact.",
        ),
    ),
    "dev/orin_user_review_bundle.py": _meta(
        "packet helper",
        "Reusable USER packet helper with FAM-003 completion-packet guard",
        "Current USER-approved repair of a packet false-green admitted on this FAM-003 carrier",
        "Adds exact full-branch/Workstream ledger, commit, owner, traceability, and pushed-HEAD consistency checks for this packet class.",
        "Slice E / SLC-R2-010 / R2-WS10 completion packet audit repair; earlier changes are historical packet guards.",
        "USER packet reviewability and false-green rejection.",
        "None; the new branch-specific guard does not change other packet families.",
        "Scope-audit negative fixtures plus active-review folder/ZIP validation.",
        "Revert only the FAM-003 R2 completion guard if replaced by equivalent reusable coverage.",
        shared=_shared_audit(
            carryforward="NONE - guard activates only for FAM003_R2_WORKSTREAM_COMPLETION_REVIEW.md.",
            detail="YES - the new logic is branch-packet-specific and leaves other family packet modes unchanged.",
        ),
    ),
}


WORKSTREAM_COMMIT_AUDIT_BY_SUBJECT = {
    "Implement FAM-003 HUD resident access loop": {
        "reason": "Implemented the public adapter and bound Settings, tray, and desktop composition.",
        "traceability": "R2-WS01 through R2-WS08 / SLC-R2-001 through 008.",
        "coherent": "YES - one product integration loop.",
        "unrelatedChanges": "NO.",
        "validation": "Cumulative HUD state, Settings, resident, entrypoint, shared regression, and aggregate proof.",
        "supersession": "Later proof commits repaired validators; product implementation remains current.",
    },
    "Harden FAM-003 HUD Workstream proof": {
        "reason": "Added the 26-state fixture, direct/visual validators, aggregate children, and shared stale-expectation repairs.",
        "traceability": "R2-WS09 and R2-WS10 / SLC-R2-009 and 010.",
        "coherent": "YES - one fail-closed proof package.",
        "unrelatedChanges": "NO.",
        "validation": "Direct child validators and aggregate proof; later commit repaired two residual false-green gaps.",
        "supersession": "Partially superseded by c351a14c for target-source and IA-token proof defects.",
    },
    "Harden FAM-003 completion proof sources": {
        "reason": "Moved visual target proof to immutable accepted external state and corrected stale resident IA vocabulary.",
        "traceability": "R2-WS09 and R2-WS10 / SLC-R2-009 and 010.",
        "coherent": "YES - two closure repairs for the cumulative proof package.",
        "unrelatedChanges": "NO.",
        "validation": "Direct HUD visual, resident, and final aggregate PASS.",
        "supersession": "Current proof-source baseline.",
    },
    "Harden FAM-003 R2 completion scope audit": {
        "reason": "Repaired the non-exhaustive changed-file packet ledger and added fail-closed Git/commit/owner parity.",
        "traceability": "R2-WS10 / SLC-R2-010 completion packet audit repair.",
        "coherent": "YES - validator, fixtures, packet guard, and registry only.",
        "unrelatedChanges": "NO.",
        "validation": "Scope-audit self-test, packet active-review validation, compileall, governance, and final parity.",
        "supersession": "Supersedes the grouped changed-file ledger in the prior completion packet.",
    },
    "Fix FAM-003 R2 packet classification": {
        "reason": "Kept exact Git evidence legal in the R2 completion packet, prevented next-phase H1 wording from misclassifying the packet, and restored referenced comparator-image parity.",
        "traceability": "R2-WS10 / SLC-R2-010 completion packet validation repair.",
        "coherent": "YES - packet classifier and proof-integrity repair only.",
        "unrelatedChanges": "NO.",
        "validation": "Packet-specific classifier probes and active-review folder/ZIP validation.",
        "supersession": "Extends the R2 completion scope-audit packet guard without weakening other packet classes.",
    },
}


def _run_git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.rstrip("\n")


def _parse_name_status(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        code = parts[0]
        kind = code[0]
        if kind in {"R", "C"}:
            if len(parts) != 3:
                raise ValueError(f"Malformed rename/copy name-status row: {line}")
            rows.append({"code": code, "previousPath": parts[1], "path": parts[2]})
        else:
            if len(parts) != 2:
                raise ValueError(f"Malformed name-status row: {line}")
            rows.append({"code": code, "path": parts[1]})
    return rows


def _status_name(code: str) -> str:
    return {
        "A": "added",
        "M": "modified",
        "D": "deleted",
        "R": "renamed",
        "C": "copied",
        "T": "modified",
    }.get(code[0], "modified")


def _range_inventory(range_spec: str, *, diff_spec: str) -> dict[str, Any]:
    name_status_text = _run_git("diff", "--name-status", "-M", "-C", diff_spec)
    changed_files = _parse_name_status(name_status_text)
    log_text = _run_git("log", "--reverse", "--format=%H%x1f%s", range_spec)
    commits: list[dict[str, Any]] = []
    for line in log_text.splitlines():
        if not line:
            continue
        commit_hash, subject = line.split("\x1f", 1)
        show_text = _run_git("show", "--format=", "--name-status", "-M", "-C", commit_hash)
        commits.append(
            {
                "hash": commit_hash,
                "subject": subject,
                "files": _parse_name_status(show_text),
            }
        )
    return {
        "range": range_spec,
        "diffSpec": diff_spec,
        "changedFiles": changed_files,
        "changedFileCount": len(changed_files),
        "stat": _run_git("diff", "--stat", diff_spec),
        "logFuller": _run_git("log", "--reverse", "--format=fuller", range_spec),
        "nameStatusText": name_status_text,
        "commits": commits,
        "commitCount": len(commits),
    }


def _commit_hashes_for_path(commits: list[dict[str, Any]], path: str) -> list[str]:
    result: list[str] = []
    for commit in commits:
        touched = {
            item.get("path", "")
            for item in commit["files"]
        } | {
            item.get("previousPath", "")
            for item in commit["files"]
        }
        if path in touched:
            result.append(commit["hash"])
    return result


def build_ledger(*, full_base: str, workstream_base: str, expected_head: str | None = None) -> dict[str, Any]:
    branch = _run_git("branch", "--show-current")
    head = _run_git("rev-parse", "HEAD")
    if expected_head and head != expected_head:
        raise ValueError(f"Expected HEAD {expected_head} but Git reports {head}")
    upstream = _run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    full_base_commit = _run_git("rev-parse", full_base)
    workstream_base_commit = _run_git("rev-parse", workstream_base)
    merge_base = _run_git("merge-base", "HEAD", full_base)

    full = _range_inventory(f"{full_base}..HEAD", diff_spec=f"{full_base}...HEAD")
    workstream = _range_inventory(
        f"{workstream_base}..HEAD",
        diff_spec=f"{workstream_base}..HEAD",
    )
    full["head"] = head
    workstream["head"] = head
    workstream_paths = {item["path"] for item in workstream["changedFiles"]}

    rows: list[dict[str, Any]] = []
    missing_metadata: list[str] = []
    for item in full["changedFiles"]:
        path = item["path"]
        metadata = FILE_METADATA.get(path)
        if metadata is None:
            missing_metadata.append(path)
            continue
        row = {
            "path": path,
            "status": _status_name(item["code"]),
            "statusCode": item["code"],
            "commits": _commit_hashes_for_path(full["commits"], path),
            "inFullBranchDelta": True,
            "inWorkstreamDelta": path in workstream_paths,
            "deltaMembership": (
                "R2_WORKSTREAM_DELTA"
                if path in workstream_paths
                else "HISTORICAL_PRE_R2_BRANCH_DELTA"
            ),
            **copy.deepcopy(metadata),
        }
        if "previousPath" in item:
            row["previousPath"] = item["previousPath"]
        rows.append(row)
    if missing_metadata:
        raise ValueError(f"Changed paths lack audit metadata: {missing_metadata}")

    workstream_commit_rows: list[dict[str, Any]] = []
    for commit in workstream["commits"]:
        audit = WORKSTREAM_COMMIT_AUDIT_BY_SUBJECT.get(commit["subject"])
        if audit is None:
            raise ValueError(
                "Workstream commit lacks exact audit metadata: "
                f"{commit['hash']} {commit['subject']}"
            )
        workstream_commit_rows.append({**commit, **copy.deepcopy(audit)})

    full["baseRef"] = full_base
    full["baseCommit"] = full_base_commit
    workstream["baseRef"] = workstream_base
    workstream["baseCommit"] = workstream_base_commit
    workstream["commits"] = workstream_commit_rows

    return {
        "schemaVersion": SCHEMA_VERSION,
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "originMain": full_base_commit,
        "mergeBase": merge_base,
        "workstreamBase": workstream_base_commit,
        "fullBranchChangedFileCount": len(rows),
        "workstreamChangedFileCount": len(workstream_paths),
        "files": rows,
        "fullBranch": full,
        "workstream": workstream,
    }


def validate_ledger(
    ledger: dict[str, Any],
    *,
    full_base: str,
    workstream_base: str,
    expected_head: str | None = None,
) -> list[str]:
    failures: list[str] = []
    try:
        actual = build_ledger(
            full_base=full_base,
            workstream_base=workstream_base,
            expected_head=expected_head,
        )
    except (RuntimeError, ValueError) as exc:
        return [str(exc)]

    if ledger.get("schemaVersion") != SCHEMA_VERSION:
        failures.append("schemaVersion mismatch")
    for field in ("branch", "head", "upstream", "originMain", "mergeBase", "workstreamBase"):
        if ledger.get(field) != actual.get(field):
            failures.append(f"{field} mismatch: ledger={ledger.get(field)!r} git={actual.get(field)!r}")

    rows = ledger.get("files")
    if not isinstance(rows, list):
        return failures + ["files must be a list"]
    actual_rows = {row["path"]: row for row in actual["files"]}
    ledger_rows: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"files[{index}] must be an object")
            continue
        path = row.get("path")
        if not isinstance(path, str) or not path:
            failures.append(f"files[{index}] path is missing")
            continue
        if path in ledger_rows:
            failures.append(f"duplicate changed-file ledger path: {path}")
        ledger_rows[path] = row
        if any(marker in path.casefold() for marker in GROUPED_PATH_MARKERS):
            failures.append(f"grouped changed-file label is forbidden: {path}")
        for field in REQUIRED_ROW_FIELDS:
            value = row.get(field)
            if value is None or value == "" or value == []:
                failures.append(f"{path}: required field {field} is missing or empty")
        if row.get("status") in {"renamed", "copied"} and not row.get("previousPath"):
            failures.append(f"{path}: renamed/copied row lacks previousPath")
        shared = row.get("sharedValidatorAudit")
        if row.get("changeCategory") == "shared validator":
            if not isinstance(shared, dict):
                failures.append(f"{path}: shared validator row lacks sharedValidatorAudit")
            else:
                for field in SHARED_AUDIT_FIELDS:
                    if not shared.get(field):
                        failures.append(f"{path}: sharedValidatorAudit.{field} is missing")

    actual_paths = set(actual_rows)
    ledger_paths = set(ledger_rows)
    if ledger_paths != actual_paths:
        failures.append(
            "Git-to-ledger path mismatch: "
            f"missing={sorted(actual_paths - ledger_paths)} extra={sorted(ledger_paths - actual_paths)}"
        )
    if ledger.get("fullBranchChangedFileCount") != len(actual_paths):
        failures.append("fullBranchChangedFileCount does not match Git")

    for path in sorted(actual_paths & ledger_paths):
        row = ledger_rows[path]
        expected = actual_rows[path]
        for field in ("status", "statusCode", "commits", "inFullBranchDelta", "inWorkstreamDelta", "deltaMembership"):
            if row.get(field) != expected.get(field):
                failures.append(f"{path}: {field} mismatch")
        if row.get("sliceSlcSeamTraceability") != expected.get("sliceSlcSeamTraceability"):
            failures.append(f"{path}: Slice/SLC/seam traceability differs from the audited classification")

    ledger_workstream_paths = {
        path for path, row in ledger_rows.items() if row.get("inWorkstreamDelta") is True
    }
    actual_workstream_paths = {row["path"] for row in actual["workstream"]["changedFiles"]}
    if ledger_workstream_paths != actual_workstream_paths:
        failures.append(
            "Workstream/full-branch delta conflation: "
            f"missing={sorted(actual_workstream_paths - ledger_workstream_paths)} "
            f"extra={sorted(ledger_workstream_paths - actual_workstream_paths)}"
        )
    if ledger.get("workstreamChangedFileCount") != len(actual_workstream_paths):
        failures.append("workstreamChangedFileCount does not match Git")

    for range_key in ("fullBranch", "workstream"):
        supplied = ledger.get(range_key)
        expected = actual[range_key]
        if not isinstance(supplied, dict):
            failures.append(f"{range_key} inventory is missing")
            continue
        supplied_paths = supplied.get("changedFiles")
        if supplied_paths != expected.get("changedFiles"):
            failures.append(f"{range_key} changed-file inventory differs from Git")
        supplied_commits = supplied.get("commits")
        if supplied_commits != expected.get("commits"):
            failures.append(f"{range_key} commit-by-commit inventory differs from Git")

    return failures


def _escape(value: Any) -> str:
    if isinstance(value, list):
        value = ", ".join(str(item)[:12] for item in value)
    text = str(value).replace("|", "\\|").replace("\n", " ")
    return text


def _ledger_markdown(ledger: dict[str, Any], *, workstream_only: bool) -> str:
    title = "R2 Workstream Changed-File Ledger" if workstream_only else "Full Branch Changed-File Ledger"
    rows = [row for row in ledger["files"] if not workstream_only or row["inWorkstreamDelta"]]
    lines = [
        f"# {title}",
        "",
        f"Branch: `{ledger['branch']}`",
        f"HEAD: `{ledger['head']}`",
        f"Rows: `{len(rows)}`",
        "",
        "Every row is an exact repository-relative path. The canonical machine-readable record is `EXACT_CHANGED_FILE_LEDGER.json`.",
        "",
        "| Path | Status | Commit(s) | Category | Owner | Legal carrier | Why | Slice / SLC / seam | Behavior | Overlap risk | Validation | Rollback | Delta | Disposition |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        values = (
            f"`{row['path']}`",
            row["status"],
            _escape(row["commits"]),
            row["changeCategory"],
            row["sourceTruthOwner"],
            row["legalCarrierBasis"],
            row["whyChanged"],
            row["sliceSlcSeamTraceability"],
            row["behaviorAffected"],
            row["overlapRisk"],
            row["validationPerformed"],
            row["rollbackConsideration"],
            row["deltaMembership"],
            row["disposition"],
        )
        lines.append("| " + " | ".join(_escape(value) for value in values) + " |")
    lines.append("")
    return "\n".join(lines)


def _commit_audit_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "# Commit-By-Commit Audit",
        "",
        "## Full Branch Commit Inventory",
        "",
        f"Range: `{ledger['fullBranch']['range']}`",
        "",
        "| # | Commit | Subject | Exact files reported by git show | Range class |",
        "| ---: | --- | --- | --- | --- |",
    ]
    workstream_hashes = {row["hash"] for row in ledger["workstream"]["commits"]}
    for index, commit in enumerate(ledger["fullBranch"]["commits"], 1):
        files = ", ".join(item["path"] for item in commit["files"]) or "None reported by git show"
        range_class = "R2 Workstream" if commit["hash"] in workstream_hashes else "Historical pre-R2 branch"
        lines.append(
            f"| {index} | `{commit['hash']}` | {_escape(commit['subject'])} | {_escape(files)} | {range_class} |"
        )
    lines.extend(
        [
            "",
            "## R2 Workstream Commit Adjudication",
            "",
        ]
    )
    for commit in ledger["workstream"]["commits"]:
        files = ", ".join(f"`{item['path']}` ({_status_name(item['code'])})" for item in commit["files"])
        lines.extend(
            [
                f"### {commit['hash']} - {commit['subject']}",
                "",
                f"- Files: {files}",
                f"- Reason: {commit['reason']}",
                f"- Slice/SLC/seam: {commit['traceability']}",
                f"- Internally coherent: {commit['coherent']}",
                f"- Unrelated changes: {commit['unrelatedChanges']}",
                f"- Validation: {commit['validation']}",
                f"- Later supersession/repair: {commit['supersession']}",
                "",
            ]
        )
    return "\n".join(lines)


def _shared_audit_markdown(ledger: dict[str, Any]) -> str:
    rows = [row for row in ledger["files"] if row.get("sharedValidatorAudit")]
    lines = [
        "# Shared Validator Ownership Audit",
        "",
        "No sibling worktree was inspected. This review uses current FAM-003 files and routed source truth only.",
        "",
        "| Exact path | Legal carrier | Stale FAM-003 only | Alters FAM-006 expectation | Weakens failure | Cross-family drift | False-green prevention | FAM-006 carryforward |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        audit = row["sharedValidatorAudit"]
        lines.append(
            "| "
            + " | ".join(
                _escape(value)
                for value in (
                    f"`{row['path']}`",
                    audit["legalCarrier"],
                    audit["repairsStaleFam003Only"],
                    audit["altersFam006Expectation"],
                    audit["weakensFailure"],
                    audit["crossFamilyDrift"],
                    audit["falseGreenPrevention"],
                    audit["fam006Carryforward"],
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Disposition: all listed shared-validator changes are legal, bounded, fail-closed, and preserve FAM-006 product/runtime ownership.",
            "",
        ]
    )
    return "\n".join(lines)


def _write_outputs(output_dir: Path, ledger: dict[str, Any], failures: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "EXACT_CHANGED_FILE_LEDGER.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "FULL_BRANCH_CHANGED_FILE_LEDGER.md").write_text(
        _ledger_markdown(ledger, workstream_only=False), encoding="utf-8"
    )
    (output_dir / "WORKSTREAM_CHANGED_FILE_LEDGER.md").write_text(
        _ledger_markdown(ledger, workstream_only=True), encoding="utf-8"
    )
    (output_dir / "COMMIT_BY_COMMIT_AUDIT.md").write_text(
        _commit_audit_markdown(ledger), encoding="utf-8"
    )
    (output_dir / "SHARED_VALIDATOR_OWNERSHIP_AUDIT.md").write_text(
        _shared_audit_markdown(ledger), encoding="utf-8"
    )
    for key, filename in (
        ("fullBranch", "full_branch_delta.json"),
        ("workstream", "workstream_delta.json"),
    ):
        (output_dir / filename).write_text(
            json.dumps(ledger[key], indent=2) + "\n", encoding="utf-8"
        )
    commit_payload = {
        "schemaVersion": SCHEMA_VERSION,
        "branch": ledger["branch"],
        "head": ledger["head"],
        "fullBranchCommits": ledger["fullBranch"]["commits"],
        "workstreamCommits": ledger["workstream"]["commits"],
    }
    (output_dir / "commit_by_commit.json").write_text(
        json.dumps(commit_payload, indent=2) + "\n", encoding="utf-8"
    )
    raw_outputs = {
        "full_branch_name_status.txt": ledger["fullBranch"]["nameStatusText"],
        "full_branch_stat.txt": ledger["fullBranch"]["stat"],
        "full_branch_log_fuller.txt": ledger["fullBranch"]["logFuller"],
        "workstream_name_status.txt": ledger["workstream"]["nameStatusText"],
        "workstream_stat.txt": ledger["workstream"]["stat"],
        "workstream_log_fuller.txt": ledger["workstream"]["logFuller"],
    }
    for filename, text in raw_outputs.items():
        (output_dir / filename).write_text(text + "\n", encoding="utf-8")
    status = "PASS" if not failures else "FAIL"
    report = [
        "# FAM-003 R2 Scope Audit Validation",
        "",
        f"Status: `{status}`",
        f"HEAD: `{ledger['head']}`",
        f"Full branch changed files: `{ledger['fullBranchChangedFileCount']}`",
        f"R2 Workstream changed files: `{ledger['workstreamChangedFileCount']}`",
        f"Full branch commits: `{ledger['fullBranch']['commitCount']}`",
        f"R2 Workstream commits: `{ledger['workstream']['commitCount']}`",
        "",
    ]
    if failures:
        report.extend(f"- FAIL: {failure}" for failure in failures)
    else:
        report.extend(
            [
                "- PASS: exact Git-to-ledger path and status parity.",
                "- PASS: commit-by-commit inventory parity.",
                "- PASS: full-branch and Workstream ranges remain distinct.",
                "- PASS: every row carries owner, carrier, traceability, validation, rollback, overlap, and disposition.",
                "- PASS: every shared-validator row carries the cross-family ownership audit.",
            ]
        )
    (output_dir / "SCOPE_AUDIT_VALIDATION.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def _packet_files_for_self_test(ledger: dict[str, Any]) -> dict[str, str]:
    return {
        "START_HERE.md": "Primary USER Review File: `USER Review/FAM003_R2_WORKSTREAM_COMPLETION_REVIEW.md`",
        "USER Review/FAM003_R2_WORKSTREAM_COMPLETION_REVIEW.md": "# FAM-003 R2 Workstream Completion Review",
        "Review Aids/EXACT_CHANGED_FILE_LEDGER.json": json.dumps(ledger),
        "Review Aids/FULL_BRANCH_CHANGED_FILE_LEDGER.md": _ledger_markdown(ledger, workstream_only=False),
        "Review Aids/WORKSTREAM_CHANGED_FILE_LEDGER.md": _ledger_markdown(ledger, workstream_only=True),
        "Review Aids/COMMIT_BY_COMMIT_AUDIT.md": _commit_audit_markdown(ledger),
        "Review Aids/SHARED_VALIDATOR_OWNERSHIP_AUDIT.md": _shared_audit_markdown(ledger),
        "Source Truth Context/Git Audit/full_branch_delta.json": json.dumps(ledger["fullBranch"]),
        "Source Truth Context/Git Audit/workstream_delta.json": json.dumps(ledger["workstream"]),
        "Source Truth Context/Git Audit/commit_by_commit.json": json.dumps(
            {
                "schemaVersion": SCHEMA_VERSION,
                "branch": ledger["branch"],
                "head": ledger["head"],
                "fullBranchCommits": ledger["fullBranch"]["commits"],
                "workstreamCommits": ledger["workstream"]["commits"],
            }
        ),
    }


def _apply_negative_case(ledger: dict[str, Any], case_id: str) -> dict[str, Any]:
    mutated = copy.deepcopy(ledger)
    if case_id == "missing_changed_file":
        mutated["files"].pop()
    elif case_id == "grouped_path_label":
        mutated["files"][0]["path"] = "Existing FAM-003/shared validators"
    elif case_id == "missing_commit_mapping":
        mutated["files"][0]["commits"] = []
    elif case_id == "missing_shared_owner_classification":
        row = next(item for item in mutated["files"] if item["changeCategory"] == "shared validator")
        row.pop("sharedValidatorAudit", None)
    elif case_id == "full_workstream_range_conflation":
        row = next(item for item in mutated["files"] if not item["inWorkstreamDelta"])
        row["inWorkstreamDelta"] = True
        row["deltaMembership"] = "R2_WORKSTREAM_DELTA"
    elif case_id == "missing_slice_slc_seam_traceability":
        mutated["files"][0]["sliceSlcSeamTraceability"] = ""
    elif case_id == "silent_rename_delete_omission":
        mutated["files"][0]["status"] = "renamed"
        mutated["files"][0]["statusCode"] = "R100"
        mutated["files"][0].pop("previousPath", None)
    elif case_id == "wrong_final_head":
        mutated["head"] = "0" * 40
    else:
        raise ValueError(f"Unknown negative case: {case_id}")
    return mutated


def run_self_test(*, full_base: str, workstream_base: str) -> list[str]:
    failures: list[str] = []
    ledger = build_ledger(full_base=full_base, workstream_base=workstream_base)
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if validate_ledger(ledger, full_base=full_base, workstream_base=workstream_base):
        failures.append("valid scope ledger failed direct validation")

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from dev import orin_user_review_bundle as review_bundle

    valid_packet = _packet_files_for_self_test(ledger)
    packet_failures = review_bundle._fam003_r2_workstream_completion_scope_failures(valid_packet)
    if packet_failures:
        failures.append("valid completion packet fixture failed: " + "; ".join(packet_failures))

    for case in fixture["cases"]:
        case_id = case["id"]
        mutated = _apply_negative_case(ledger, case_id)
        direct_failures = validate_ledger(
            mutated,
            full_base=full_base,
            workstream_base=workstream_base,
        )
        packet_files = _packet_files_for_self_test(mutated)
        packet_case_failures = review_bundle._fam003_r2_workstream_completion_scope_failures(packet_files)
        if not direct_failures:
            failures.append(f"negative case {case_id} did not fail direct validation")
        if not packet_case_failures:
            failures.append(f"negative case {case_id} did not fail packet validation")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-base", default="origin/main")
    parser.add_argument("--workstream-base", default=WORKSTREAM_BASE)
    parser.add_argument("--expected-head")
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--write-output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    ledger = build_ledger(
        full_base=args.full_base,
        workstream_base=args.workstream_base,
        expected_head=args.expected_head,
    )
    if args.ledger:
        supplied = json.loads(args.ledger.read_text(encoding="utf-8"))
    else:
        supplied = ledger
    failures = validate_ledger(
        supplied,
        full_base=args.full_base,
        workstream_base=args.workstream_base,
        expected_head=args.expected_head,
    )
    if args.self_test:
        failures.extend(run_self_test(full_base=args.full_base, workstream_base=args.workstream_base))
    failures = list(dict.fromkeys(failures))
    if args.write_output_dir:
        _write_outputs(args.write_output_dir, supplied, failures)

    if failures:
        print("FAM-003 R2 WORKSTREAM SCOPE AUDIT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("FAM-003 R2 WORKSTREAM SCOPE AUDIT: PASS")
    print(f"HEAD: {supplied['head']}")
    print(f"Full branch changed files: {supplied['fullBranchChangedFileCount']}")
    print(f"R2 Workstream changed files: {supplied['workstreamChangedFileCount']}")
    print(f"Full branch commits: {supplied['fullBranch']['commitCount']}")
    print(f"R2 Workstream commits: {supplied['workstream']['commitCount']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
