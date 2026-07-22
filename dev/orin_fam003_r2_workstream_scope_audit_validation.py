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
        "Recorded helper ownership, proof limits, reuse posture, the exact-scope completion gate, and the Option D sustained-performance methodology contract.",
        "Slice E / SLC-R2-009 and SLC-R2-010 / R2-WS09 and R2-WS10.",
        "Validator ownership and packet false-green prevention.",
        "No product overlap; future branches must respect helper status rather than infer shared product ownership.",
        "Source-owner marker, governance efficiency, branch governance, and scope-audit validation.",
        "Revert only the FAM-003 rows together with the helpers they register.",
    ),
    "desktop/core_visualization_renderer.py": _meta(
        "product/runtime lifecycle",
        "FAM-003 desktop visualization renderer lifecycle",
        "USER-approved bounded mixed decline-then-accept relaunch lifecycle repair",
        "Added idempotent staged Qt WebEngine teardown so the visualization page releases before application quit.",
        "R2 Workstream completion lifecycle repair / R2-EVIDENCE-004.",
        "WebEngine page shutdown, deferred deletion, and native-surface release ordering.",
        "Low: the repair is confined to FAM-003 desktop shutdown and does not alter FAM-006 ownership or behavior.",
        "Desktop-entrypoint validation, repeated relaunch lifecycle stress, Option C aggregate, and Python compileall.",
        "Revert together with the coordinated desktop shutdown repair; never retain the stricter clean-exit proof without the product fix.",
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
        "Accepted R2 startup/shutdown composition seam plus explicit USER-approved Option D Workstream proof hook",
        "Constructed the real or unavailable HUD adapter, bound startup/route/shutdown lifecycle, and added a dormant environment-gated in-process all-surface proof hook used only by the exact normal launcher.",
        "Slice D/E / SLC-R2-007,008,009,010 / R2-WS07,08,09,10 and Option D renderer-backend completion proof.",
        "Startup owner-state read, adapter availability, shutdown suppression, and normal-launcher Workstream proof orchestration.",
        "Medium: the composition root creates current-carrier FAM-006/FAM-007-owned surfaces, but the hook does not change their product ownership or sibling worktrees.",
        "Desktop entrypoint, renderer-backend negative fixtures and three-session proof, HUD access, resident, and Option C aggregate.",
        "Remove the environment-gated proof hook independently; remove adapter construction/binding only with the R2 HUD access rollback.",
    ),
    "desktop/orin_desktop_launcher.pyw": _meta(
        "product launcher lifecycle",
        "FAM-003 normal desktop launcher and relaunch outcome classification",
        "USER-approved bounded mixed decline-then-accept lifecycle repair plus temporary Option D shared-runtime safety policy",
        "Normalizes the process-wide software-compositor flag to one token, records parent/effective flags and temporary shared-runtime provenance, propagates launcher failure codes, and classifies every post-settled nonzero first-session exit as abnormal.",
        "R2 Workstream completion lifecycle repair / R2-EVIDENCE-004 plus Option D renderer-backend completion proof.",
        "Normal launcher child environment, shared WebEngine backend classification, first/replacement outcome separation, and fail-closed process result propagation.",
        "High overlap: every current-carrier WebEngine surface inherits the process-wide flag; this is temporary shared runtime behavior, not FAM-003-only or permanent policy.",
        "Renderer-backend contract fixtures, exact Desktop launcher sessions, desktop-entrypoint lifecycle stress, and Option C aggregate.",
        "Remove the flag through desktop/renderer_backend.py only after approved replacement architecture and full lifecycle/all-surface reproof; never restore crash masking.",
    ),
    "desktop/renderer_backend.py": _meta(
        "product launcher policy",
        "Temporary shared desktop WebEngine backend policy",
        "Explicit USER-approved Option D execution in the current R2 Workstream",
        "Centralizes environment copying, token de-duplication, the single --disable-gpu safety flag, and explicit temporary/shared-runtime provenance.",
        "Slice E / SLC-R2-009,010 / R2-WS09,10 renderer-backend completion proof.",
        "One auditable environment-policy point inherited by first, replacement, and recovery renderer children.",
        "High overlap by design: current-carrier FAM-006/FAM-007-owned WebEngine surfaces inherit the flag; no sibling source or state is inspected or mutated.",
        "Four contract cases, 15 negative fixtures, exact normal-launcher sessions, lifecycle proof, and aggregate consumption.",
        "Remove only after approved shared renderer architecture and rerun every invalidated lifecycle, surface, and performance proof.",
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
    "dev/fixtures/fam003_resize_cursor_proof_negative_cases.json": _meta(
        "fixture",
        "FAM-003 R2 resize-cursor Workstream proof",
        "Current USER-approved cursor-proof false-green repair",
        "Adds geometry-only, telemetry-only, hit-zone, event-order, missing-frame, non-composited-frame, stale-HEAD, and hidden-child-failure cases.",
        "Slice E / SLC-R2-010 / R2-WS10 completion proof repair.",
        "Proves visible cursor evidence cannot be replaced by internal diagnostics or geometry-only success.",
        "None; evidence-gate fixture only.",
        "Settings cursor self-test, aggregate proof, and packet active-review validation.",
        "Remove only with a replacement that preserves the same fail-closed cursor-proof cases.",
    ),
    "dev/fixtures/fam003_renderer_backend_negative_cases.json": _meta(
        "fixture",
        "FAM-003 R2 Option D renderer-backend proof",
        "Explicit USER-approved temporary shared WebEngine policy validation",
        "Carries 39 fail-capable mutations, including sustained resident-state inventory, interval duration, per-process CPU/memory attribution, truthful first-visible timing, raw-summary parity, baseline comparability, complete performance adjudication, and preserved-proof currentness.",
        "Slice E / SLC-R2-009,010 / R2-WS09,10 renderer-backend completion proof.",
        "Renderer-backend proof false-green prevention.",
        "None; fixture-only mutations do not execute sibling runtime or alter product state.",
        "Renderer-backend self-test and aggregate required-child validation.",
        "Remove only with the renderer-backend adjudicator or an equivalent replacement fixture set.",
    ),
    "dev/fixtures/fam003_option_d_nonintrusive_performance_negative_cases.json": _meta(
        "fixture",
        "FAM-003 R2 Option D nonintrusive performance proof",
        "Explicit USER-approved performance-observation methodology repair",
        "Adds 20 fail-capable mutations for nested event loops, GUI-thread sampling, observer attribution, PID/role CPU, CPU denominators, private/shared memory, idle and post-use state, meaningful workload, timing, baseline, external-state, release-health, and raw-summary parity.",
        "Slice E / SLC-R2-010 / R2-WS10 performance-methodology repair.",
        "Nonintrusive performance false-green prevention.",
        "None; fixture-only mutations do not execute sibling runtime or alter product state.",
        "Nonintrusive validator self-test and Option C aggregate fixture parity.",
        "Remove only with an equivalent nonintrusive observation fixture set.",
    ),
    "dev/fixtures/desktop_relaunch_lifecycle_cases.json": _meta(
        "fixture",
        "FAM-003 desktop-entrypoint relaunch lifecycle proof",
        "USER-approved bounded mixed decline-then-accept relaunch lifecycle repair",
        "Adds ten explicit clean, decline, mixed, guard-order, native-crash, forced-kill, missing-exit, overlap, and replacement-masking cases.",
        "R2 Workstream completion lifecycle repair / R2-EVIDENCE-004.",
        "Fail-closed first-session and replacement-session lifecycle classification.",
        "None; deterministic validator fixture only.",
        "Desktop-entrypoint fixture validation, direct lifecycle stress, and Option C aggregate.",
        "Remove only with equivalent negative and positive lifecycle coverage.",
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
        "Validates 26 states, owner persistence, retries, generations, concurrency, shutdown, accessibility, and direct-bypass negatives, then emits complete row-level JSON/Markdown evidence with current-HEAD provenance.",
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
        "Renders disabled, enabled, progress, unavailable, partial, failure/retry, minimum, wide, focus, and Quick Access regression states with source-HEAD/timestamp/proof-root provenance.",
        "Slices B/E / SLC-R2-003,004,009,010 / R2-WS03,04,09,10.",
        "Settings HUD element/state visual evidence and accepted-target comparison.",
        "None; target/runtime proof does not transfer FAM-006 ownership.",
        "Direct HUD visual validation and aggregate child; final target source is external accepted state.",
        "Remove HUD-specific proof with the HUD page; preserve the broader Settings validator.",
    ),
    "dev/orin_fam003_human_client_live_validation.ps1": _meta(
        "proof helper",
        "FAM-003 normal USER-path live helper",
        "Accepted existing helper extended by the current bounded R2 cursor-proof repair",
        "Added an isolated non-LV cursor-proof mode that uses the exact Desktop launcher, real Windows pointer input, GetCursorInfo, DrawIconEx, and ordered pre-drag/held-drag/post-edge frames.",
        "Slice E / SLC-R2-010 / R2-WS10 completion proof repair.",
        "Current Settings resize-cursor evidence plus future normal USER-path evidence production.",
        "Low; optional FAM-006 integration remains explicitly separate and owner-bound.",
        "PowerShell parser, focused normal-launcher cursor run, Settings/Option C aggregate, and packet proof; formal LV not run.",
        "Retain bounded cursor mode with the Settings proof gate and preserve full LV mode for later separate approval.",
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
        "Makes HUD access, HUD visual, resident-adjacent, NCP, desktop-entrypoint, and Option D renderer-backend children fail closed; preserves Settings/cursor evidence only through exact Git-diff currentness; selects exact current child roots; copies complete 26-state and renderer evidence; and propagates USER_DECISION_REQUIRED when performance has no safe equivalent baseline.",
        "Slice E / SLC-R2-009,010 / R2-WS09,10.",
        "Whole-package cumulative proof and required-child propagation.",
        "High overlap is recorded for the temporary shared renderer flag; current-carrier FAM-006/FAM-007 surfaces remain proof dependencies, not transferred product authority.",
        "Direct aggregate result with all required child results; performance ambiguity blocks PASS as USER_DECISION_REQUIRED.",
        "Revert only R2 child registration/evidence rows if the R2 package is rolled back.",
    ),
    "dev/fam003_renderer_backend_runtime_probe.py": _meta(
        "proof helper",
        "FAM-003 R2 Option D product-side proof entry",
        "Explicit USER-approved Option D nonintrusive performance-methodology repair",
        "Routes the active environment-gated entry to the nonblocking controller and immediately returns to the normal Qt event loop; the earlier intrusive implementation remains superseded historical code and is not callable through the active entry.",
        "Slice E / SLC-R2-009,010 / R2-WS09,10 renderer-backend completion proof.",
        "Direct current-carrier backend-to-visual and backend-to-functional truth under the exact normal launcher.",
        "High overlap is explicit because sibling-owned product surfaces in the current carrier inherit the process flag; no sibling source or state is inspected or mutated.",
        "Active-entry source checks, three normal-launcher sessions, external process observations, preserved-current non-performance proof, and aggregate consumption.",
        "Remove the dormant environment hook and probe together; generated evidence becomes stale after any affected surface or backend change.",
    ),
    "dev/fam003_option_d_performance_controller.py": _meta(
        "proof helper",
        "FAM-003 R2 Option D nonintrusive product-side controller",
        "Explicit USER-approved performance-observation methodology repair",
        "Uses ordinary QTimer callbacks under QApplication.exec to coordinate startup idle, meaningful multi-surface active work, three normal close/hide and post-use-idle cycles, surface inventory, truthful timing labels, and normal shutdown without nested event pumping or GUI-thread sleep.",
        "Slice E / SLC-R2-010 / R2-WS10 performance-methodology repair.",
        "Validation-only state coordination; normal product behavior is unchanged outside the environment-gated proof entry.",
        "High overlap is measured on current-carrier shared surfaces without sibling worktree inspection or mutation.",
        "Source checks, three normal-launcher sessions, event-dispatch timing, state inventory, and observer request/result parity.",
        "Remove with the observer and nonintrusive adjudicator if the Option D proof path is retired.",
    ),
    "dev/fam003_option_d_performance_observer.py": _meta(
        "proof helper",
        "FAM-003 R2 Option D external observer",
        "Explicit USER-approved performance-observation methodology repair",
        "Runs outside the product tree and records PID/parent/role CPU, CPU denominators, RSS/working set, USS/private, shared estimates, process persistence, launcher ancestry, raw samples, and its own excluded overhead.",
        "Slice E / SLC-R2-010 / R2-WS10 performance-methodology repair.",
        "External nonintrusive process/resource evidence only.",
        "None; it observes only the current FAM-003 validation-owned process tree.",
        "Twenty negative fixtures, three normal-launcher sessions, raw-summary reproduction, and process-ledger validation.",
        "Remove with the controller and nonintrusive adjudicator if the Option D proof path is retired.",
    ),
    "dev/orin_fam003_option_d_nonintrusive_performance_validation.py": _meta(
        "proof helper",
        "FAM-003 R2 Option D nonintrusive performance adjudicator",
        "Explicit USER-approved performance-observation methodology repair",
        "Launches the external observer and exact Desktop shortcut, validates three normal event-loop sessions, reproduces summaries from raw samples, preserves only Git-current non-performance proof, supersedes intrusive performance evidence, and returns USER_DECISION_REQUIRED without a valid baseline or governed threshold.",
        "Slice E / SLC-R2-010 / R2-WS10 performance-methodology repair.",
        "Fail-closed measurement, currentness, attribution, external-state, release-health, and decision proof.",
        "High overlap is classified through current-carrier shared runtime evidence; no sibling worktree is inspected or mutated.",
        "Fifty-nine combined fixtures, Python compile, three exact-launcher sessions, Option C aggregate, scope audit, governance, and packet parity.",
        "Retire only after an approved replacement supplies equivalent nonintrusive evidence and currentness controls.",
    ),
    "dev/orin_fam003_renderer_backend_workstream_validation.py": _meta(
        "proof helper",
        "FAM-003 R2 Option D renderer-backend adjudicator",
        "Explicit USER-approved temporary shared WebEngine policy proof",
        "Compatibility entrypoint routes active execution to the external-observer adjudicator, preserves the historical visual/lifecycle support functions, refuses unsupported equivalence without a safe baseline, and enforces 59 combined negative fixtures.",
        "Slice E / SLC-R2-009,010 / R2-WS09,10 renderer-backend completion proof.",
        "Fail-closed shared-backend, all-surface, lifecycle, performance, approval, and evidence-currentness adjudication.",
        "High overlap is classified rather than hidden; no sibling worktree inspection/mutation or unmerged sibling claim is allowed.",
        "Direct self-test, three-session proof, lifecycle ingestion, and Option C aggregate required-child propagation.",
        "Retire only after an approved permanent renderer architecture supplies equivalent or stronger proof.",
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
        "Adds deterministic Git inventories, one-row-per-file ledger generation, commit audit, shared-validator review, parity validation, 26-state/root-currentness packet guards, and negative self-tests.",
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
        "Added the persistent HUD parent/child to IA/stress/geometry/state expectations and now requires current-HEAD normal-launcher cursor frames before closing resize/cursor rows.",
        "Slices B/E / SLC-R2-003,004,009 / R2-WS03,04,09.",
        "Global Settings rail, content, responsive geometry, dirty guard, and Quick Access regression behavior.",
        "None; no FAM-006 surface internals are rendered or changed.",
        "Direct Settings regression, eight fail-closed cursor fixtures, and aggregate required child.",
        "Remove only HUD-specific expectations if the HUD page is rolled back; retain cursor proof unless replaced equivalently.",
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
        "Adds exact full-branch/Workstream ledger checks plus current Settings, Option C, complete 26-state, unambiguous HUD child-root, and actual-cursor-composited proof requirements so stale, summary-only, ambiguous, or telemetry-only evidence cannot carry completion.",
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
    "Harden FAM-003 R2 packet identity validation": {
        "reason": "Repaired the duplicate active external-state snapshot false-green path and made the Workstream scope audit merge-aware after rebaseline.",
        "traceability": "R2 Workstream completion packet identity reconciliation / SLC-R2-010 packet traceability repair.",
        "coherent": "YES - packet validator, scope-audit helper, and negative fixtures only.",
        "unrelatedChanges": "NO.",
        "validation": "Scope-audit self-test, old-packet negative validation, packet active-review validation, and final parity.",
        "supersession": "Supersedes the stale duplicate External Operational State snapshot shape in the 20260716-112604 packet.",
    },
    "Harden FAM-003 R2 completion packet integrity": {
        "reason": "Repaired current-gate packet integrity false-green paths for stale review aids, control characters, missing self-contained evidence, and commit-classification ambiguity.",
        "traceability": "R2 Workstream completion packet integrity repair / SLC-R2-010 packet reviewability repair.",
        "coherent": "YES - packet validator, negative fixtures, and scope-audit helper only.",
        "unrelatedChanges": "NO.",
        "validation": "Scope-audit negative fixtures, old-packet negative validation, packet active-review validation, and final parity.",
        "supersession": "Supersedes the stale, non-self-contained 20260717-122104 completion packet shape.",
    },
    "Harden FAM-003 resize cursor proof": {
        "reason": "Repaired geometry-only and telemetry-only cursor false greens with real normal-launcher pointer capture, current-child aggregation, and packet fail-closed checks.",
        "traceability": "R2-WS10 / SLC-R2-010 resize-cursor completion proof repair.",
        "coherent": "YES - bounded proof helper, validators, fixtures, registry, and packet guard only.",
        "unrelatedChanges": "NO.",
        "validation": "Cursor negative fixtures, Settings/Option C fail-closed paths, packet guard, compileall, and PowerShell parse.",
        "supersession": "Supersedes the telemetry-promoted 122222 cursor proof and omitted 165501 non-green result.",
    },
    "Fix cursor proof compiler reference": {
        "reason": "Added the explicit Windows PowerShell System.Drawing compiler reference required by the actual-cursor renderer.",
        "traceability": "R2-WS10 / SLC-R2-010 resize-cursor proof-helper finalization.",
        "coherent": "YES - one proof-helper compiler repair.",
        "unrelatedChanges": "NO.",
        "validation": "PowerShell parse and bounded normal-launcher cursor proof.",
        "supersession": "Completes the prior proof-helper commit without changing product behavior.",
    },
    "Make FAM-003 cursor proof reviewable": {
        "reason": "Aligned packet filenames to actual ordered frame indices, separated launcher frames from cursor-requested frames, and added focused crops for human review.",
        "traceability": "R2-WS10 / SLC-R2-010 cursor-proof packet reviewability repair.",
        "coherent": "YES - proof/packet readability and exact audit metadata only.",
        "unrelatedChanges": "NO.",
        "validation": "Cursor proof rerun, Settings/Option C aggregate, scope-audit self-test, active-review packet validation, and image integrity.",
        "supersession": "Final reviewable cursor evidence shape for the replacement Workstream packet.",
    },
    "Make FAM-003 HUD completion evidence self-contained": {
        "reason": "Added complete 26-state row artifacts, exact aggregate child-root provenance, packet false-green guards, and routed registry ownership.",
        "traceability": "R2-WS10 / SLC-R2-010 Workstream completion evidence repair.",
        "coherent": "YES - Workstream evidence helpers, packet guard, fixture cases, and registry only.",
        "unrelatedChanges": "NO.",
        "validation": "26-state direct helper, HUD visual helper, Option C aggregate, scope-audit self-test, packet validation, and final parity.",
        "supersession": "Supersedes the summary-only 26-state packet shape and ambiguous 053038/054537 HUD root selection.",
    },
    "Classify FAM-003 HUD evidence repair": {
        "reason": "Added exact audit metadata for the self-contained HUD evidence repair commit and this bounded classifier follow-up.",
        "traceability": "R2-WS10 / SLC-R2-010 Workstream completion evidence audit repair.",
        "coherent": "YES - exact commit-classification metadata only.",
        "unrelatedChanges": "NO.",
        "validation": "Scope-audit self-test and final Git-to-ledger parity.",
        "supersession": "Completes the prior evidence repair without changing product or proof semantics.",
    },
    "Classify FAM-003 evidence helper references": {
        "reason": "Repeated existing Helper Status classifications in the HUD evidence addendum so reusable governance validation can classify every helper reference deterministically.",
        "traceability": "R2-WS10 / SLC-R2-010 Workstream completion evidence audit repair.",
        "coherent": "YES - registry helper-classification markers only.",
        "unrelatedChanges": "NO.",
        "validation": "Branch governance modes, scope-audit self-test, and final Git-to-ledger parity.",
        "supersession": "Completes the registry classification repair without changing product or proof semantics.",
    },
    "Repair resident relaunch shutdown lifecycle": {
        "reason": "Repaired the Windows Qt WebEngine native shutdown order and made abnormal first-session exits fail closed even when a replacement session settles.",
        "traceability": "R2 Workstream completion lifecycle repair / R2-EVIDENCE-004.",
        "coherent": "YES - coordinated product lifecycle, launcher, validator, fixture, and registry repair.",
        "unrelatedChanges": "NO.",
        "validation": "Desktop-entrypoint validation, ten-case lifecycle fixture, repeated mixed-cycle stress, resident access, Settings/cursor/HUD children, and Option C aggregate.",
        "supersession": "Supersedes the post-settled recoverable-completion behavior that masked Windows exit 0xC0000409.",
    },
    "Bound FAM-003 visible control lookup": {
        "reason": "Bound UI Automation searches to exact names, control types, and FAM-003 process IDs so the current resize-cursor dependency completes without scanning the full desktop tree.",
        "traceability": "R2 Workstream completion lifecycle repair / current cursor dependency finalization.",
        "coherent": "YES - one proof-helper reliability repair.",
        "unrelatedChanges": "NO.",
        "validation": "PowerShell parse, normal-launcher cursor proof, Settings visual proof, and Option C aggregate.",
        "supersession": "Supersedes the timed-out unbounded UI Automation lookup; it does not change product behavior.",
    },
    "Classify FAM-003 relaunch lifecycle repair": {
        "reason": "Added exact file and commit audit metadata required to include the lifecycle repair in the one-row-per-file completion packet ledger.",
        "traceability": "R2 Workstream completion lifecycle repair / SLC-R2-010 exact-scope packet audit.",
        "coherent": "YES - exact audit metadata only.",
        "unrelatedChanges": "NO.",
        "validation": "Scope-audit self-test, packet active-review validation, and Git-to-ledger parity.",
        "supersession": "Completes lifecycle-repair packet traceability without changing runtime or proof semantics.",
    },
    "Scope FAM-003 packet focus checks to decision aids": {
        "reason": "Prevented legitimate dependency-owner and accepted-reference text inside current proof evidence from being misclassified as a wrong-family active packet focus while preserving the check on decision aids.",
        "traceability": "R2 Workstream completion packet validation / SLC-R2-010 false-blocker repair.",
        "coherent": "YES - packet classifier and exact audit metadata only.",
        "unrelatedChanges": "NO.",
        "validation": "FAM-003 packet scope guard, negative self-test, active-review folder/ZIP validation, and Git-to-ledger parity.",
        "supersession": "Narrows one over-broad stale-focus scan without weakening active decision-surface family checks.",
    },
    "Prove FAM-003 shared renderer backend": {
        "reason": "Executed the USER-approved temporary Option D shared WebEngine safety policy with centralized flag provenance, exhaustive current-carrier surface inventory, exact normal-launcher runtime proof, lifecycle/performance/rollback evidence, negative fixtures, aggregate consumption, and packet traceability.",
        "traceability": "R2-WS09 and R2-WS10 / SLC-R2-009 and 010 renderer-backend completion proof.",
        "coherent": "YES - one temporary shared-backend execution and proof package.",
        "unrelatedChanges": "NO.",
        "validation": "Renderer contract and 18 negative fixtures, three exact normal-launcher sessions, desktop lifecycle suite, affected-surface proof, Option C aggregate, scope audit, governance, compileall, and packet parity.",
        "supersession": "Current temporary Option D proof baseline; permanent renderer architecture remains unapproved and open.",
    },
    "Harden FAM-003 WebEngine proof callbacks": {
        "reason": "Added bounded retry and explicit exhaustion evidence after one of three exact normal-launcher sessions reached WebEngine readiness but failed to return a JavaScript callback.",
        "traceability": "R2-WS10 / SLC-R2-010 renderer-backend false-green closure.",
        "coherent": "YES - one Workstream probe reliability and fail-capable validation repair.",
        "unrelatedChanges": "NO.",
        "validation": "Renderer contract, callback-2 recovery unit fixture, and 20 negative fixtures; three exact normal-launcher sessions; affected-surface proof; Option C aggregate; scope audit; governance; and compileall.",
        "supersession": "Supersedes single-attempt JavaScript callback proof behavior; it does not change product runtime behavior outside the dormant Workstream probe.",
    },
    "Harden FAM-003 cursor mouse-down anchoring": {
        "reason": "Re-established and verified the real pointer edge coordinate and resize-cursor fingerprint immediately before mouse-down after a current-HEAD proof showed pointer displacement between the pre-drag frame and mouse-down.",
        "traceability": "R2-WS10 / SLC-R2-010 exact normal-launcher resize-cursor closure.",
        "coherent": "YES - one visible pointer proof reliability and fail-capable fixture repair.",
        "unrelatedChanges": "NO.",
        "validation": "PowerShell parse, ten cursor negative fixtures, exact Desktop-launcher cursor proof, Settings child, Option C aggregate, scope audit, and governance.",
        "supersession": "Supersedes the unanchored gap between pre-drag cursor proof and mouse-down; product resize behavior is unchanged.",
    },
    "Harden FAM-003 restored WebEngine visual proof": {
        "reason": "Added surface-relative restored-frame coverage and bounded recapture after tray-restored HUD and AI Command Center screenshots exposed large partial-black WebEngine regions that generic nonblank checks accepted.",
        "traceability": "R2-WS10 / SLC-R2-010 affected-surface visual proof closure.",
        "coherent": "YES - restored and reopened WebEngine evidence plus fail-capable fixture repair.",
        "unrelatedChanges": "NO.",
        "validation": "Three exact normal-launcher surface sessions, 22 renderer negative fixtures, visual contact-sheet adjudication, Option C aggregate, scope audit, and governance.",
        "supersession": "Supersedes generic nonblank acceptance for restored and reopened WebEngine evidence; product behavior is unchanged.",
    },
    "Repair FAM-003 Option D performance proof": {
        "reason": "Replaced short, ambiguous renderer-tree samples and contaminated timing labels with three exact-launcher sustained startup-idle, active, and post-use measurements; added process attribution, raw-summary parity, baseline truth, and fail-closed adjudication.",
        "traceability": "R2-WS10 / SLC-R2-010 Option D performance-methodology repair.",
        "coherent": "YES - performance probe, validator, negative fixtures, aggregate propagation, and helper registry only.",
        "unrelatedChanges": "NO.",
        "validation": "39 negative fixtures, Python compile, three exact normal-launcher sustained sessions, Option C aggregate, scope audit, governance, and packet parity.",
        "supersession": "Supersedes the sub-second, non-attributed measurements and unsupported NO_MATERIAL_REGRESSION_OBSERVED verdict; Option D remains temporary and performance acceptance requires USER decision.",
    },
    "Repair FAM-003 Option D nonintrusive performance proof": {
        "reason": "Superseded the validation-controlled nested Qt event-pump sampler with a separate external observer plus ordinary QTimer state controller; added observer overhead exclusion, PID/role CPU, RSS/USS/private memory, three lifecycle cycles, meaningful workload, truthful timing, raw parity, and external/release routing proof.",
        "traceability": "R2-WS10 / SLC-R2-010 Option D nonintrusive performance-methodology repair.",
        "coherent": "YES - performance observer/controller, compatibility entry, validator, fixtures, aggregate currentness, scope audit, and helper registry only.",
        "unrelatedChanges": "NO.",
        "validation": "59 negative fixtures, Python compile, three exact Desktop-launcher sessions, Option C aggregate, scope audit, governance, external-state validation, release-health supporting gate, and packet parity.",
        "supersession": "Supersedes contaminated v2 CPU, memory, and timing conclusions; preserved non-performance evidence remains current only through exact Git-diff proof. Option D remains temporary and performance disposition remains USER_DECISION_REQUIRED unless source truth supports another result.",
    },
    "Preserve FAM-003 proof currentness after performance repair": {
        "reason": "Prevented a performance-helper-only HEAD change from forcing unrelated Settings/cursor recapture while retaining a fail-closed exact Git-diff currentness receipt and the failed-before-final-pass report.",
        "traceability": "R2-WS10 / SLC-R2-010 aggregate currentness and exact-scope repair.",
        "coherent": "YES - aggregate currentness logic and exact audit metadata only.",
        "unrelatedChanges": "NO.",
        "validation": "Python compile, preserved-proof Git currentness receipt, final Option C aggregate, scope audit, governance, and packet parity.",
        "supersession": "Supersedes strict same-HEAD rejection for proof whose product/runtime inputs are Git-proven unchanged; any product/runtime delta still fails preservation.",
    },
    "Classify FAM-003 performance proof registry": {
        "reason": "Added exact Helper Status markers to the sustained-performance addendum, updated the canonical renderer helper row from 22 to 39 negative fixtures, and classified this source-truth follow-up in the exact commit audit.",
        "traceability": "R2-WS10 / SLC-R2-010 performance-helper ownership and exact-scope repair.",
        "coherent": "YES - helper registry and exact audit metadata only.",
        "unrelatedChanges": "NO.",
        "validation": "Branch governance modes, source-owner validation, scope audit, final aggregate, and packet parity.",
        "supersession": "Supersedes stale duplicate helper prose and the prior 22-fixture registry description without changing product/runtime behavior.",
    },
}

WORKSTREAM_COMMIT_EXCLUDED_SUBJECTS = {
    "Classify FAM-003 R2 packet identity repair commit",
}


def _excluded_from_workstream_commit_audit(subject: str) -> bool:
    return subject in WORKSTREAM_COMMIT_EXCLUDED_SUBJECTS or subject.startswith("Packet audit meta:")


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


def _range_inventory(
    range_spec: str,
    *,
    diff_spec: str,
    exclude_ref: str | None = None,
    no_merges: bool = False,
    changed_files_from_commits: bool = False,
) -> dict[str, Any]:
    name_status_text = _run_git("diff", "--name-status", "-M", "-C", diff_spec)
    log_args = ["log", "--reverse", "--format=%H%x1f%s"]
    if no_merges:
        log_args.append("--no-merges")
    log_args.append(range_spec)
    if exclude_ref:
        log_args.extend(["--not", exclude_ref])
    changed_files = _parse_name_status(name_status_text)
    log_text = _run_git(*log_args)
    commits: list[dict[str, Any]] = []
    for line in log_text.splitlines():
        if not line:
            continue
        commit_hash, subject = line.split("\x1f", 1)
        show_text = _run_git("show", "--format=", "--name-status", "-M", "-C", commit_hash)
        if changed_files_from_commits and _excluded_from_workstream_commit_audit(subject):
            continue
        commits.append(
            {
                "hash": commit_hash,
                "subject": subject,
                "files": _parse_name_status(show_text),
            }
        )
    if changed_files_from_commits:
        by_path: dict[str, dict[str, str]] = {}
        for commit in commits:
            for item in commit["files"]:
                path = item.get("path")
                if path:
                    by_path[path] = item
        changed_files = [by_path[path] for path in sorted(by_path)]
        name_status_text = "\n".join(
            "\t".join(
                value
                for value in (item.get("code", ""), item.get("previousPath", ""), item.get("path", ""))
                if value
            )
            for item in changed_files
        )
    return {
        "range": range_spec,
        "diffSpec": diff_spec,
        "excludeRef": exclude_ref,
        "noMerges": no_merges,
        "changedFilesFromCommits": changed_files_from_commits,
        "changedFiles": changed_files,
        "changedFileCount": len(changed_files),
        "stat": _run_git("diff", "--stat", diff_spec),
        "logFuller": _run_git(
            *(
                [
                    "log",
                    "--reverse",
                    *(["--no-merges"] if no_merges else []),
                    "--format=fuller",
                    range_spec,
                    *(["--not", exclude_ref] if exclude_ref else []),
                ]
            )
        ),
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
        exclude_ref=full_base,
        no_merges=True,
        changed_files_from_commits=True,
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
    full_commits = ledger["fullBranch"]["commitCount"]
    workstream_commits = ledger["workstream"]["commitCount"]
    cursor_steps = [
        {"id": "pointer_outside_resize_zone", "status": "PASS", "evidence": {}},
        {
            "id": "visible_cursor_transition_pre_drag",
            "status": "PASS",
            "evidence": {"classification": "VISIBLE_CURSOR_TRANSITION_PROVEN"},
        },
        {"id": "mouse_down_with_visible_resize_cursor", "status": "PASS", "evidence": {}},
        {"id": "held_drag_and_completed_resize", "status": "PASS", "evidence": {}},
        {"id": "pointer_leaves_resize_zone", "status": "PASS", "evidence": {}},
        {
            "id": "resize_cursor_workstream_proof",
            "status": "PASS",
            "evidence": {
                "visibleCursorClassification": "VISIBLE_CURSOR_TRANSITION_PROVEN",
                "internalCursorClassification": "INTERNAL_CURSOR_STATE_SUPPORTING_ONLY",
            },
        },
    ]
    cursor_manifest = {
        "schema": "fam003-r2-workstream-resize-cursor-proof-v1",
        "status": "PASS",
        "proofMode": "R2_WORKSTREAM_RESIZE_CURSOR_ONLY",
        "head": ledger["head"],
        "formalHardening": False,
        "formalLiveValidation": False,
        "cursorFabrication": False,
        "steps": cursor_steps,
        "orderedFrames": [
            {"cursorRequested": True, "cursorComposited": True, "virtualBounds": [0, 0, 1920, 1080]}
            for _ in range(6)
        ],
    }
    settings_manifest = {
        "allChecksPass": True,
        "sourceHead": ledger["head"],
        "visibleCursorProofPass": True,
    }
    hud_access_root = "C:/proof/fam003-hud-access-final"
    hud_settings_root = "C:/proof/fam003-hud-settings-final"
    hud_state_rows = [
        {
            "stateId": state_id,
            "title": f"state {state_id:02d}",
            "entryCondition": "fixture entry condition",
            "expectedAdapterBehavior": "fixture expected behavior",
            "actualAdapterResult": "fixture observed behavior",
            "persistenceResult": "fixture persistence result",
            "globalSettingsState": "fixture Settings state",
            "trayState": "fixture tray state",
            "dashboardState": "fixture Dashboard state",
            "userFacingState": "fixture USER-facing state",
            "retryOrRollbackResult": "fixture recovery result",
            "automatedEvidence": "fixture assertion",
            "workstreamVisualEvidence": ["fixture_visual"],
            "finalVerdict": "PASS",
            "evidencePaths": ["fixture.json"],
            "head": ledger["head"],
            "timestamp": "20260721-120000",
            "proofRoot": hud_access_root,
        }
        for state_id in range(1, 27)
    ]
    hud_state_manifest = {
        "schema": "fam003-hud-access-26-state-results-v2",
        "status": "PASS",
        "sourceHead": ledger["head"],
        "timestamp": "20260721-120000",
        "proofRoot": hud_access_root,
        "stateCount": 26,
        "states": hud_state_rows,
    }
    hud_access_manifest = {
        "schemaVersion": 2,
        "status": "PASS",
        "sourceHead": ledger["head"],
        "proofRoot": hud_access_root,
        "stateCount": 26,
        "stateResults": hud_state_rows,
    }
    hud_settings_manifest = {
        "schemaVersion": 2,
        "status": "PASS",
        "sourceHead": ledger["head"],
        "proofRoot": hud_settings_root,
    }
    option_manifest = {
        "status": "PASS",
        "head": ledger["head"],
        "settingsManifest": settings_manifest,
        "visibleCursorProof": cursor_manifest,
        "visibleCursorArtifacts": ["cursor-proof.png"],
        "visibleCursorFocusedArtifacts": ["focus-cursor-proof.png"],
        "hudAccessManifest": hud_access_manifest,
        "hudSettingsManifest": hud_settings_manifest,
        "childProofRoots": {
            "hudAccessWorkstream": {"root": hud_access_root, "role": "CURRENT_AGGREGATE_CHILD", "head": ledger["head"]},
            "hudSettingsVisual": {"root": hud_settings_root, "role": "CURRENT_AGGREGATE_CHILD_AND_PACKET_EVIDENCE", "head": ledger["head"]},
            "settingsVisualRegression": {"root": "C:/proof/settings-final", "role": "CURRENT_AGGREGATE_CHILD_AND_PACKET_EVIDENCE", "head": ledger["head"]},
            "resizeCursor": {"root": "C:/proof/cursor-final", "role": "CURRENT_AGGREGATE_DEPENDENCY", "head": ledger["head"]},
        },
        "helperRuns": {"settingsVisualRegression": {"ok": True, "returncode": 0}},
    }
    packet = {
        "START_HERE.md": "Primary USER Review File: `USER Review/FAM003_R2_WORKSTREAM_COMPLETION_REVIEW.md`",
        "USER Review/FAM003_R2_WORKSTREAM_COMPLETION_REVIEW.md": "\n".join(
            [
                "# FAM-003 R2 Workstream Completion Review",
                "",
                f"| HEAD | `{ledger['head']}` |",
                f"| origin/main...HEAD | `{full_commits}` branch commits |",
                f"| Workstream range | `{workstream_commits}` Workstream commits |",
                "Complete 26-state row artifact: `PASS`.",
                "Final aggregate child-root matrix: `PASS`.",
            ]
        ),
        "Review Aids/PACKET_MANIFEST.md": "Packet Purpose: `FAM-003 R2 Workstream completion exact-scope USER review`",
        "Review Aids/FILES_LOADED_AND_AUTHORITY_FINDINGS.md": "Conflicting current authority: `NONE after repair`",
        "Review Aids/EXACT_CHANGED_FILE_LEDGER.json": json.dumps(ledger),
        "Review Aids/FULL_BRANCH_CHANGED_FILE_LEDGER.md": _ledger_markdown(ledger, workstream_only=False),
        "Review Aids/WORKSTREAM_CHANGED_FILE_LEDGER.md": _ledger_markdown(ledger, workstream_only=True),
        "Review Aids/COMMIT_BY_COMMIT_AUDIT.md": _commit_audit_markdown(ledger),
        "Review Aids/COMMIT_CLASSIFICATION_LEDGER.md": "\n".join(
            [
                "# Commit Classification Ledger",
                "",
                "## R2 product implementation commits",
                "",
                "- Implement product behavior.",
                "",
                "## R2 Workstream proof/completion-audit commits",
                "",
                "- Prove Workstream completion.",
                "",
                "## Post-Workstream packet and validator repair commits",
                "",
                "- Repair packet and validator traceability.",
                "",
                "## Rebaseline or merge commits",
                "",
                "- Reconcile origin/main.",
                "",
                "## Historical pre-R2 branch commits",
                "",
                "- Branch setup and earlier gated history.",
            ]
        ),
        "Review Aids/CONTROL_CHARACTER_SCAN.md": "Control-character scan result: PASS.",
        "Review Aids/CURRENT_GATE_CONSISTENCY_REPORT.md": "Current Gate: R2 Workstream completion USER review pending.",
        "Review Aids/DEFECT_LEDGER.md": "All packet-integrity defects are CLOSED_WITH_PROOF.",
        "Review Aids/PACKET_CONTENT_MANIFEST.md": "Packet content manifest: all required evidence classes present.",
        "Review Aids/VALIDATION_RESULTS.md": "Validation result: PASS.",
        "Review Aids/SHARED_VALIDATOR_OWNERSHIP_AUDIT.md": _shared_audit_markdown(ledger),
        "Review Aids/Evidence/Option C Workstream Proof/fam003_option_c_workstream_proof_manifest.json": json.dumps(option_manifest),
        "Review Aids/Evidence/Option C Workstream Proof/fam003_hud_access_workstream_manifest.json": json.dumps(hud_access_manifest),
        "Review Aids/Evidence/Option C Workstream Proof/fam003_hud_access_26_state_results.json": json.dumps(hud_state_manifest),
        "Review Aids/Evidence/Option C Workstream Proof/fam003_hud_access_26_state_results.md": "26 state rows PASS.",
        "Review Aids/Evidence/HUD Access 26-State Proof/fam003_hud_access_workstream_manifest.json": json.dumps(hud_access_manifest),
        "Review Aids/Evidence/HUD Access 26-State Proof/fam003_hud_access_26_state_results.json": json.dumps(hud_state_manifest),
        "Review Aids/Evidence/HUD Access 26-State Proof/fam003_hud_access_26_state_results.md": "26 state rows PASS.",
        "Review Aids/HUD_PROOF_ROOT_RECONCILIATION.md": "20260721-053038 HISTORICAL_SUPPORTING_SUPERSEDED; 20260721-054537 HISTORICAL_SUPPORTING_SUPERSEDED; final root FINAL_CURRENT_AGGREGATE_CHILD; roots are not both current.",
        "Review Aids/ACTIVE_CHILD_PROOF_ROOT_MATRIX.md": "All final roots have exactly one current role.",
        "Review Aids/STATE_TO_EVIDENCE_MATRIX.md": "All 26 state rows map to evidence.",
        "Review Aids/Evidence/Option C Workstream Proof/fam003_resize_cursor_workstream_proof_manifest.json": json.dumps(cursor_manifest),
        "Review Aids/Evidence/Option C Workstream Proof/00_option_c_workstream_contact_sheet.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/01_tray_styled_popup_focused.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/03_tray_quick_access_submenu_focused.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/04_tray_hud_submenu_focused.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/10_ncp_entry_typed_request.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/11_ncp_choose_visible_choices.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/12_ncp_confirm_selected_action.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/13_ncp_result_launch_requested.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/cursor_004_pointer_outside_resize_zone_normal.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/cursor_005_pointer_right_edge_visible_resize_cursor_pre_drag.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/cursor_006_mouse_down_with_visible_resize_cursor.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/cursor_007_held_drag_mid_resize.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/cursor_008_mouse_up_completed_resize.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/cursor_009_pointer_left_resize_zone_normal_cursor.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/focus_cursor_004_pointer_outside_resize_zone_normal.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/focus_cursor_005_pointer_right_edge_visible_resize_cursor_pre_drag.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/focus_cursor_006_mouse_down_with_visible_resize_cursor.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/focus_cursor_007_held_drag_mid_resize.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/focus_cursor_008_mouse_up_completed_resize.png": "png",
        "Review Aids/Evidence/Option C Workstream Proof/focus_cursor_009_pointer_left_resize_zone_normal_cursor.png": "png",
        "Review Aids/Evidence/HUD Settings Visual Proof/fam003_hud_settings_visual_manifest.json": json.dumps(hud_settings_manifest),
        "Review Aids/Evidence/HUD Settings Visual Proof/01_disabled_default.png": "png",
        "Review Aids/Evidence/HUD Settings Visual Proof/02_enabled_default.png": "png",
        "Review Aids/Evidence/HUD Settings Visual Proof/06_partial_retry.png": "png",
        "Review Aids/Evidence/HUD Settings Visual Proof/07_failure_retry.png": "png",
        "Review Aids/Evidence/HUD Settings Visual Proof/FAM003_HUD_SETTINGS_IMPLEMENTATION_CONTACT_SHEET.png": "png",
        "Review Aids/Evidence/HUD Settings Visual Proof/FAM003_HUD_TARGET_IMPLEMENTATION_COMPARISON.png": "png",
        "Review Aids/Evidence/Settings Visual Proof/fam003_settings_visual_fail_repair_manifest.json": json.dumps(settings_manifest),
        "Review Aids/Evidence/Settings Visual Proof/03e_live_user_drag_resized.png": "png",
        "Review Aids/Evidence/Settings Visual Proof/07_dropdown_list_state.png": "png",
        "Review Aids/Evidence/Settings Visual Proof/08_close_guard.png": "png",
        "Review Aids/Evidence/Settings Visual Proof/16_defect_closure_contact_sheet.png": "png",
        "Review Aids/Evidence/Settings Visual Proof/17_red_team_review_sheet.png": "png",
        "Source Truth Context/branch_state.md": "\n".join(
            [
                "## FAM-003 R2 Workstream Completion Scope Audit Repair",
                "",
                "Current Gate: `R2 Workstream completion USER review pending`",
                f"Source Repo HEAD: `{ledger['head']}`",
                f"Full Branch Audit: `26 exact changed files / {full_commits} commits for origin/main...HEAD`",
                f"R2 Workstream Audit: `17 exact changed files / {workstream_commits} commits for 1806927765013f0c7d1a13335af2ca5cfce5325e..HEAD`",
            ]
        ),
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
    return packet


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
    elif case_id in {
        "duplicate_active_external_state_snapshot",
        "historical_snapshot_with_active_completion_head",
        "control_character_in_external_snapshot",
        "stale_workstream_entry_review_aid",
        "missing_self_contained_evidence",
        "packet_repair_commit_mislabeled_historical",
        "newer_non_green_settings_omitted",
        "telemetry_only_cursor_false_green",
        "stale_settings_evidence_selected",
        "child_failure_hidden_by_top_level_pass",
        "missing_26_state_artifact",
        "missing_26_state_row",
        "non_green_26_state_row",
        "ambiguous_hud_root_roles",
        "aggregate_packet_hud_root_mismatch",
    }:
        return mutated
    else:
        raise ValueError(f"Unknown negative case: {case_id}")
    return mutated


def _apply_packet_negative_case(packet_files: dict[str, str], case_id: str) -> dict[str, str]:
    mutated = copy.deepcopy(packet_files)
    if case_id == "duplicate_active_external_state_snapshot":
        mutated[
            "Source Truth Context/External Operational State/branch_state.md"
        ] = "\n".join(
            [
                "## FAM-003 R2 Workstream Completion Scope Audit Repair",
                "",
                "Current Gate: `R2 Workstream completion USER review pending`",
                "Source Repo HEAD: `0000000000000000000000000000000000000000`",
                "Ahead / Behind vs origin/main: `38 / 0`",
                "Full Branch Audit: `26 exact changed files / 38 commits for origin/main...HEAD`",
                "R2 Workstream Audit: `17 exact changed files / 4 commits for 1806927765013f0c7d1a13335af2ca5cfce5325e..HEAD`",
            ]
        )
    elif case_id == "historical_snapshot_with_active_completion_head":
        mutated[
            "Source Truth Context/External Operational State/r2_workstream_execution_ledger_20260716.md"
        ] = "\n".join(
            [
                "HISTORICAL MILESTONE - SUPERSEDED",
                "",
                "Completion HEAD: `0000000000000000000000000000000000000000`",
                "Current Gate: `Workstream completion USER review pending`",
            ]
        )
    elif case_id == "control_character_in_external_snapshot":
        mutated[
            "Source Truth Context/Active External Snapshot/r2_workstream_execution_ledger_20260716.md"
        ] = "Current Branch HEAD: \f1e9d76bf98394aa40d009a14ccbf14a89cca378\n"
    elif case_id == "stale_workstream_entry_review_aid":
        mutated[
            "Review Aids/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md"
        ] = "Decision Path: Workstream Entry final decision review - Workstream implementation remains pending USER approval.\n"
    elif case_id == "missing_self_contained_evidence":
        mutated.pop(
            "Review Aids/Evidence/Option C Workstream Proof/00_option_c_workstream_contact_sheet.png",
            None,
        )
    elif case_id == "packet_repair_commit_mislabeled_historical":
        mutated["Review Aids/COMMIT_CLASSIFICATION_LEDGER.md"] = "\n".join(
            [
                "# Commit Classification Ledger",
                "",
                "## R2 product implementation commits",
                "",
                "## R2 Workstream proof/completion-audit commits",
                "",
                "## Post-Workstream packet and validator repair commits",
                "",
                "## Rebaseline or merge commits",
                "",
                "## Historical pre-R2 branch commits",
                "",
                "- Packet audit meta: allow active external snapshot context.",
            ]
        )
    elif case_id == "newer_non_green_settings_omitted":
        path = "Review Aids/Evidence/Settings Visual Proof/fam003_settings_visual_fail_repair_manifest.json"
        payload = json.loads(mutated[path])
        payload["allChecksPass"] = False
        mutated[path] = json.dumps(payload)
    elif case_id == "telemetry_only_cursor_false_green":
        path = "Review Aids/Evidence/Option C Workstream Proof/fam003_resize_cursor_workstream_proof_manifest.json"
        payload = json.loads(mutated[path])
        step = next(item for item in payload["steps"] if item["id"] == "resize_cursor_workstream_proof")
        step["evidence"]["visibleCursorClassification"] = "INTERNAL_CURSOR_STATE_SUPPORTING_ONLY"
        mutated[path] = json.dumps(payload)
    elif case_id == "stale_settings_evidence_selected":
        path = "Review Aids/Evidence/Settings Visual Proof/fam003_settings_visual_fail_repair_manifest.json"
        payload = json.loads(mutated[path])
        payload["sourceHead"] = "0" * 40
        mutated[path] = json.dumps(payload)
    elif case_id == "child_failure_hidden_by_top_level_pass":
        path = "Review Aids/Evidence/Option C Workstream Proof/fam003_option_c_workstream_proof_manifest.json"
        payload = json.loads(mutated[path])
        payload["helperRuns"]["settingsVisualRegression"] = {"ok": False, "returncode": 1}
        mutated[path] = json.dumps(payload)
    elif case_id == "missing_26_state_artifact":
        mutated.pop(
            "Review Aids/Evidence/HUD Access 26-State Proof/fam003_hud_access_26_state_results.json",
            None,
        )
    elif case_id == "missing_26_state_row":
        path = "Review Aids/Evidence/HUD Access 26-State Proof/fam003_hud_access_26_state_results.json"
        payload = json.loads(mutated[path])
        payload["states"].pop()
        payload["stateCount"] = 25
        mutated[path] = json.dumps(payload)
    elif case_id == "non_green_26_state_row":
        path = "Review Aids/Evidence/HUD Access 26-State Proof/fam003_hud_access_26_state_results.json"
        payload = json.loads(mutated[path])
        payload["states"][10]["finalVerdict"] = "FAIL"
        mutated[path] = json.dumps(payload)
    elif case_id == "ambiguous_hud_root_roles":
        mutated["Review Aids/HUD_PROOF_ROOT_RECONCILIATION.md"] = (
            "20260721-053038 current; 20260721-054537 current."
        )
    elif case_id == "aggregate_packet_hud_root_mismatch":
        path = "Review Aids/Evidence/HUD Settings Visual Proof/fam003_hud_settings_visual_manifest.json"
        payload = json.loads(mutated[path])
        payload["proofRoot"] = "C:/proof/unconsumed-later-rerun"
        mutated[path] = json.dumps(payload)
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
        packet_files = _apply_packet_negative_case(
            _packet_files_for_self_test(mutated),
            case_id,
        )
        packet_case_failures = review_bundle._fam003_r2_workstream_completion_scope_failures(packet_files)
        packet_only_case = case_id in {
            "duplicate_active_external_state_snapshot",
            "historical_snapshot_with_active_completion_head",
            "control_character_in_external_snapshot",
            "stale_workstream_entry_review_aid",
            "missing_self_contained_evidence",
            "packet_repair_commit_mislabeled_historical",
            "newer_non_green_settings_omitted",
            "telemetry_only_cursor_false_green",
            "stale_settings_evidence_selected",
            "child_failure_hidden_by_top_level_pass",
            "missing_26_state_artifact",
            "missing_26_state_row",
            "non_green_26_state_row",
            "ambiguous_hud_root_roles",
            "aggregate_packet_hud_root_mismatch",
        }
        if not direct_failures and not packet_only_case:
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
