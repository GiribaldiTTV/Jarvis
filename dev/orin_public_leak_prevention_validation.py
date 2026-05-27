# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=SRCOWN-FIRSTPASS-FAM007-AI-007; surface=fam007-public-leak-prevention-validator; status=shared
"""Validate FAM-007 AI Edition public leak-prevention proof surfaces."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import desktop.ai_provider_state as ai_provider_state  # noqa: E402
import dev.orin_user_review_bundle as user_review_bundle  # noqa: E402


AI_EDITION_PLAN = Path(
    "Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md"
)
FAM007_BRANCH_PLAN = Path(
    "Docs/branch_plans/feature_fam_007_ai_edition_public_leak_prevention_foundation.md"
)
FAM007_BRANCH_RECORD = Path(
    "Docs/branch_records/feature_fam_007_ai_edition_public_leak_prevention_foundation.md"
)
FAM007_DEV_OWNER_BRANCH_PLAN = Path(
    "Docs/branch_plans/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md"
)
FAM007_DEV_OWNER_BRANCH_RECORD = Path(
    "Docs/branch_records/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md"
)
FAM007_AI_RUNTIME_TRUST_BRANCH_PLAN = Path(
    "Docs/branch_plans/feature_fam_007_ai_runtime_trust_boundary_readiness.md"
)
FAM007_AI_RUNTIME_TRUST_BRANCH_RECORD = Path(
    "Docs/branch_records/feature_fam_007_ai_runtime_trust_boundary_readiness.md"
)
FAM007_BREAKPOINT2_BRANCH_PLAN = Path(
    "Docs/branch_plans/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md"
)
FAM007_BREAKPOINT2_BRANCH_RECORD = Path(
    "Docs/branch_records/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md"
)
VALIDATION_REGISTRY = Path("Docs/validation_helper_registry.md")
REVIEW_BUNDLE_HELPER = Path("dev/orin_user_review_bundle.py")
FIXTURE_DIR = ROOT / "dev" / "fixtures" / "fam007_public_leak_prevention"
FIXTURE_SET = FIXTURE_DIR / "public_leak_prevention_fixture_set.json"

REQUIRED_AI_PLAN_PHRASES = (
    "Protected Assets Table",
    "Public-Safe Fixture Rule",
    "Public Review-Bundle Leak-Prevention Rule",
    "Owner-As-Private-Test-Person Rule",
    "Edition Boundary Manifest Planning",
    "Private-To-Public Sanitization Gate",
    "Public Build Exclusion Requirement",
    "Off-Boot Backup And Recovery Planning",
    "USER Action Gate Registry",
    "USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE",
    "USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE",
    "USER-ACTION-FAM007-GITHUB-DESKTOP-PRIVATE-REMOTE-SETUP",
    "USER-ACTION-FAM007-AI-DATA-BACKUP-RECOVERY",
    "USER-ACTION-FAM007-PRIVATE-TO-PUBLIC-SANITIZATION",
    "USER-ACTION-FAM007-PROVIDER-MODEL-EXECUTION",
    "Breakpoint 1: Public Leak-Prevention Foundation",
    "Breakpoint 2: Private Dev And Owner Skeleton Creation",
    "Breakpoint 2 Readiness Proof Contract",
    "Dev skeleton readiness proof must show",
    "Owner skeleton readiness proof must show",
    "GitHub Desktop private remote safety proof must show",
    "Private release notes, private tags, private builds, private capability packs",
)

REQUIRED_BRANCH_PLAN_PHRASES = (
    "Public Protected-Asset Leak Checklist And Public-Safe Fixture Contract",
    "Edition Boundary Manifest Planning / Public-Safe Schema Direction",
    "Public Build Exclusion Requirement And Audit Posture",
    "Public Review-Bundle Leak Prevention And Source-Truth Routing",
    "Dev/Owner Skeleton Handoff Criteria And Provider-Execution Continuation",
    "PR Readiness Stage 1 Record",
    "Stage 2 PR Creation: `Historical completed",
    "FAM-007 USER Action Gate Identifiers",
    "USER-ACTION-FAM007-AI-DATA-BACKUP-RECOVERY",
    "USER-ACTION-FAM007-PUBLIC-TO-DEV-MIGRATION-CONSENT",
    "USER-ACTION-FAM007-MEMORY-LEARNING-PERSONALIZATION",
    "Provider-boundary preservation",
    "Workstream Green",
)

REQUIRED_RECORD_PHRASES = (
    "Phase: `Historical Traceability`",
    "Workstream Status: `Historical green",
    "Stage: `Released in v1.7.22-prebeta`",
    "PR Readiness Stage 1 Result: `Historical pre-PR snapshot",
    "Stage 2 PR Creation: `Historical completed",
    "Live Validation LV1 Result: `Green",
    "Hardening H1 Result: `Green",
    "Next Legal Phase: `Release Readiness`",
    "Release Readiness Health Pass: PASS",
    "Governance Drift Found:",
    "Release Window Audit: PASS",
    "FAM-007 USER Action Gate Identifiers",
    "USER-ACTION-FAM007-PACKAGING-EDITION-IDENTITY",
    "USER-ACTION-FAM007-AI-DATA-BACKUP-RECOVERY",
    "No visible runtime UI change",
    "Provider Execution State: `Blocked",
)

REQUIRED_DEV_OWNER_PLAN_PHRASES = (
    "First Seam Group Implementation Receipt",
    "Remaining Workstream Seam Group Implementation Receipt",
    "Dev Skeleton Readiness Gate Proof: `Implemented - public-safe planning proof only`",
    "Owner Skeleton Readiness Gate Proof: `Implemented - public-safe planning proof only`",
    "Private Repo / Local-Only Action-Gate Proof: `Implemented - private setup remains pending USER decision`",
    "GitHub Desktop Private Remote Safety Proof: `Implemented - planning-only remote safety proof`",
    "Off-Boot Backup / Recovery Planning Proof: `Implemented - public-safe planning proof only`",
    "Public-To-Private Separation Proof: `Implemented - public-safe planning proof only`",
    "Provider / Model Execution Deferral Hardening Proof: `Implemented - provider boundary remains closed`",
    "Future Handoff Criteria Proof: `Implemented - Hardening H1 handoff criteria are recorded`",
    "Workstream Green Candidate: `YES - all admitted Workstream seams have public-safe proof",
    "No private Dev repository was created",
    "No private Owner repository or local-only Owner root was created",
    "No GitHub Desktop private remote was configured",
    "No off-boot backup root was created or written",
    "No Public-to-Dev import was implemented",
    "No provider SDK or model execution was enabled",
)

REQUIRED_DEV_OWNER_RECORD_PHRASES = (
    "First Seam Group Implementation Receipt",
    "Remaining Workstream Seam Group Implementation Receipt",
    "Dev Skeleton Readiness Gate Proof: `Implemented - public-safe planning proof only`",
    "Owner Skeleton Readiness Gate Proof: `Implemented - public-safe planning proof only`",
    "Private Repo / Local-Only Action-Gate Proof: `Implemented - private setup remains pending USER decision`",
    "GitHub Desktop Private Remote Safety Proof: `Implemented - planning-only remote safety proof`",
    "Off-Boot Backup / Recovery Planning Proof: `Implemented - public-safe planning proof only`",
    "Public-To-Private Separation Proof: `Implemented - public-safe planning proof only`",
    "Provider / Model Execution Deferral Hardening Proof: `Implemented - provider boundary remains closed`",
    "Future Handoff Criteria Proof: `Implemented - Hardening H1 handoff criteria are recorded`",
    "Workstream Green Candidate: `YES - all admitted Workstream seams have public-safe proof",
    "No provider/model execution, memory, downloads, external calls, voice/Core sync, backup implementation, private repo creation, private remote configuration, PR, merge, release, cleanup, or v1.8.0 work was performed.",
)

REQUIRED_AI_RUNTIME_TRUST_PLAN_PHRASES = (
    "Workstream Implementation Receipt",
    "Option 1 Permission-State And Provider Boundary Readiness Proof: `Implemented - public-safe planning proof only`",
    "Option 2 Deterministic Routing And Reliability Readiness Proof: `Implemented - direct deterministic-policy fixture proof only`",
    "Option 3 Trust Journal And AI Operational Cache Governance Readiness Proof: `Implemented - cache is not memory and runtime cache behavior remains blocked`",
    "Option 4 Capability-Pack And Local-Only Handoff Readiness Proof: `Implemented - capability-pack/local-only handoff criteria recorded without install or execution`",
    "Workstream Green Candidate: `YES - Options 1 through 4 have direct validator and fixture proof`",
    "Hardening H1 Result: `Green - H1 compared Options 1 through 4",
    "Live Validation LV1 Result: `Green - no visible runtime surface changed",
    "User Test Summary Results: `WAIVED`",
    "No provider SDK/model execution, runtime provider execution, runtime cache behavior, memory/learning/personalization, downloads, external calls, private repo creation, private remote configuration, backup/import implementation, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, or v1.8.0 work was performed.",
)

REQUIRED_AI_RUNTIME_TRUST_RECORD_PHRASES = (
    "Workstream Implementation Receipt",
    "Option 1 Permission-State And Provider Boundary Readiness Proof: `Implemented - public-safe planning proof only`",
    "Option 2 Deterministic Routing And Reliability Readiness Proof: `Implemented - direct deterministic-policy fixture proof only`",
    "Option 3 Trust Journal And AI Operational Cache Governance Readiness Proof: `Implemented - cache is not memory and runtime cache behavior remains blocked`",
    "Option 4 Capability-Pack And Local-Only Handoff Readiness Proof: `Implemented - capability-pack/local-only handoff criteria recorded without install or execution`",
    "Backlog Completion State: Implemented Complete Except Future Dependency",
    "Completion Status: Green",
    "Continue Decision: Stop",
    "Hardening H1 Result: `Green - H1 compared Options 1 through 4",
    "Live Validation LV1 Result: `Green - no visible runtime surface changed",
    "User Test Summary Results: `WAIVED`",
    "No provider SDK/model execution, runtime provider execution, runtime cache behavior, memory/learning/personalization, downloads, external calls, private repo creation, private remote configuration, backup/import implementation, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, or v1.8.0 work was performed.",
)

REQUIRED_BREAKPOINT2_PLAN_PHRASES = (
    "Seam 1 Action-Gate Registry Implementation Receipt",
    "Seam 1 Status: `Implemented - public-safe action-gate registry and exact USER decision proof only`",
    "Action-Gate Registry Proof: `Implemented - every Breakpoint 2 gated action remains pending USER decision`",
    "Direct Validation Surface: `dev/orin_public_leak_prevention_validation.py validates breakpoint2Seam1ActionGateRegistry`",
    "Remaining Workstream Seam Group Implementation Receipt",
    "Seam 2 Private/Public Boundary And Private Remote Safety Proof: `Implemented - public-safe metadata and private remote safety proof only`",
    "Seam 3 Backup/Recovery And Public-To-Dev Import Planning Proof: `Implemented - planning-only gate proof`",
    "Seam 4 Provider/Model/Runtime/Cache/Memory Deferral And Local-Only Handoff Proof: `Implemented - provider/runtime/cache/memory remains blocked`",
    "Direct Validation Surface: `dev/orin_public_leak_prevention_validation.py validates breakpoint2RemainingWorkstreamReadiness`",
    "Workstream Green Candidate: `YES - all admitted Breakpoint 2 seams have direct validator and fixture proof`",
    "Next Legal Phase: `Hardening`",
    "Hardening H1 Result: `Green - H1 compared Seams 1 through 4",
    "H1 Drift Found: `YES - older duplicate ledger wording still described Seams 2 through 4 as planned or pending Workstream approval.`",
    "H1 Direct Validation Surface: `dev/orin_public_leak_prevention_validation.py rejects stale Breakpoint 2 Workstream-pending ledger phrases after H1.`",
    "Next Legal Phase: `Live Validation`",
    "Exact Next USER Decision Needed: `Approve bounded Live Validation LV1/no-visible-runtime proof",
    "No private Dev repo, private Owner repo, local-only private root, private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006/Governance mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0 work was performed.",
    "Exact Next USER Decision Needed: `Approve bounded Hardening H1",
)

REQUIRED_BREAKPOINT2_RECORD_PHRASES = (
    "Seam 1 Action-Gate Registry Implementation Receipt",
    "Seam 1 Status: `Implemented - public-safe action-gate registry and exact USER decision proof only`",
    "Action-Gate Registry Proof: `Implemented - every Breakpoint 2 gated action remains pending USER decision`",
    "Direct Validation Surface: `dev/orin_public_leak_prevention_validation.py validates breakpoint2Seam1ActionGateRegistry`",
    "Remaining Workstream Seam Group Implementation Receipt",
    "Seam 2 Private/Public Boundary And Private Remote Safety Proof: `Implemented - public-safe metadata and private remote safety proof only`",
    "Seam 3 Backup/Recovery And Public-To-Dev Import Planning Proof: `Implemented - planning-only gate proof`",
    "Seam 4 Provider/Model/Runtime/Cache/Memory Deferral And Local-Only Handoff Proof: `Implemented - provider/runtime/cache/memory remains blocked`",
    "Direct Validation Surface: `dev/orin_public_leak_prevention_validation.py validates breakpoint2RemainingWorkstreamReadiness`",
    "Workstream Green Candidate: `YES - all admitted Breakpoint 2 seams have direct validator and fixture proof`",
    "Backlog Completion State: Implemented Complete Except Future Dependency",
    "Completion Status: Green",
    "Continue Decision: Stop",
    "Next Legal Phase: `Hardening`",
    "Hardening H1 Result: `Green - H1 compared Seams 1 through 4",
    "H1 Drift Found: `YES - older duplicate ledger wording still described Seams 2 through 4 as planned or pending Workstream approval.`",
    "H1 Direct Validation Surface: `dev/orin_public_leak_prevention_validation.py rejects stale Breakpoint 2 Workstream-pending ledger phrases after H1.`",
    "Next Legal Phase: `Live Validation`",
    "Exact Next USER Decision Needed: `Approve bounded Live Validation LV1/no-visible-runtime proof",
    "No private Dev repo, private Owner repo, local-only private root, private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006/Governance mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0 work was performed.",
    "Exact Next USER Decision Needed: `Approve bounded Hardening H1",
)

BREAKPOINT2_STALE_WORKSTREAM_PHRASES = (
    "Workstream implementation is pending",
    "Pending Workstream approval",
    "Seam 2 pending USER approval",
    "Seam 2 and all private/runtime actions remain pending USER decision",
    "USER reviews refreshed packet before Seam 2",
    "Approve Workstream Entry analysis next",
    "USER approved Branch Readiness Stage 2 setup only",
    "Hardening H1 remains pending USER approval",
    "Hardening H1 remains blocked pending exact USER approval",
    "Hardening H1 remains blocked until USER approval",
    "Hardening H1 approval is pending USER decision",
    "Hardening H1 is blocked until USER approves",
)

REQUIRED_REGISTRY_PHRASES = (
    "dev/orin_public_leak_prevention_validation.py",
    "FAM-007 public leak-prevention validator",
    "protected assets",
    "public-safe fixtures",
    "review-bundle leak prevention",
    "edition-boundary manifest",
    "public build exclusion",
    "Dev/Owner skeleton readiness action-gate proof",
    "GitHub Desktop private remote safety remains planning-only",
    "off-boot backup/recovery planning remains USER-gated",
    "public-to-private separation remains planning-only",
    "provider/model deferral hardening",
    "future handoff criteria",
    "AI runtime/trust-boundary readiness",
    "Options 1 through 4",
    "AI Operational Cache Governance readiness",
    "Breakpoint 2 Seam 1 action-gate registry proof",
    "Breakpoint 2 remaining Workstream readiness proof",
    "private/public boundary and private remote safety proof",
    "exact USER decision proof",
)

PROTECTED_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private-path",
        re.compile(
            r"(?:[A-Z]:[\\/][^\n\r]*"
            r"(?:Owner(?:[\\/ _.-]|$)|Private(?:[\\/ _.-]|$)|\.codex[\\/](?:private|owner|dev)))|"
            r"(?:^|[\\/ _.-])(?:owner[-_ ]?private|private[-_ ]?owner|owner[-_ ]?repo|dev[-_ ]?repo)"
            r"(?:[\\/ _.-]|$)",
            re.IGNORECASE,
        ),
    ),
    (
        "private-prompt",
        re.compile(r"(?:owner|dev|private)[-_ ]?(?:prompt|instruction)", re.IGNORECASE),
    ),
    (
        "private-memory",
        re.compile(r"(?:owner|dev|private)[-_ ]?(?:memory|personalization)", re.IGNORECASE),
    ),
    (
        "private-log-or-eval",
        re.compile(r"(?:owner|dev|private)[-_ ]?(?:log|eval|transcript)", re.IGNORECASE),
    ),
    (
        "private-screenshot-or-model-output",
        re.compile(r"(?:owner|dev|private)[-_ ]?(?:screenshot|model[-_ ]?output)", re.IGNORECASE),
    ),
    (
        "private-automation-or-handoff",
        re.compile(r"(?:owner|dev|private)[-_ ]?(?:automation|codex[-_ ]?handoff)", re.IGNORECASE),
    ),
    (
        "secret-or-token",
        re.compile(
            r"(?:BEGIN (?:RSA |OPENSSH |EC |)PRIVATE KEY|gh[pousr]_[A-Za-z0-9_]{20,}|"
            r"sk-[A-Za-z0-9]{20,}|(?:token|secret|password|credential)\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{8,})",
            re.IGNORECASE,
        ),
    ),
    (
        "private-model-or-capability",
        re.compile(
            r"(?:owner|dev|private)[-_ ]?(?:model|capability[-_ ]?pack|weights|artifact)",
            re.IGNORECASE,
        ),
    ),
    (
        "private-edition-runtime",
        re.compile(
            r"(?:owner|dev)[-_ ]?(?:runtime|edition[-_ ]?runtime|manifest[-_ ]?runtime)",
            re.IGNORECASE,
        ),
    ),
    (
        "provider-execution",
        re.compile(
            r"(?:provider|model|sdk)[-_ ]?(?:execution|enabled|ready)|canAcceptPrompts\s*[:=]\s*true",
            re.IGNORECASE,
        ),
    ),
    (
        "network-or-download",
        re.compile(r"(?:network|external[-_ ]?call|download)[-_ ]?(?:enabled|allowed|ready)", re.IGNORECASE),
    ),
    (
        "public-to-dev-import",
        re.compile(r"public[-_ ]?to[-_ ]?dev[-_ ]?import[-_ ]?(?:enabled|implementation)", re.IGNORECASE),
    ),
)

SAFE_FIXTURE_BOOLEAN_FIELDS = (
    "synthetic",
    "nonSecret",
    "nonOwnerSpecific",
    "nonMemoryDerived",
    "nonTokenDerived",
    "notCopiedFromPrivateLogs",
)

PUBLIC_MANIFEST_FALSE_FIELDS = (
    "ownerPrivateAllowed",
    "devPrivateAllowed",
    "providerExecutionAllowed",
    "modelExecutionAllowed",
    "memoryAllowed",
    "networkAllowed",
    "downloadsAllowed",
    "privateRepoAllowed",
    "publicToDevImportImplementationAllowed",
    "voiceCoreSyncAllowed",
)

PROVIDER_PAYLOAD_EXPECTATIONS = {
    "providerVisibleData": "none",
    "providerVisibleDataGuarantee": "provider-visible-data-none-guaranteed",
    "sentToProvider": False,
    "canAcceptPrompts": False,
    "modelExecutionStatus": "model-execution-disabled",
    "modelWorkloadReadinessPosture": "model-workload-readiness-disabled",
    "networkEgressState": "network-egress-blocked",
    "memoryContextState": "memory-context-disabled",
    "memoryIndexingState": "memory-indexing-disabled",
    "retrievalState": "retrieval-disabled",
    "learningState": "learning-disabled",
    "voiceRuntimeState": "voice-runtime-disabled",
}


def _read(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _load_fixture_set() -> dict[str, Any]:
    return json.loads(FIXTURE_SET.read_text(encoding="utf-8"))


def _flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for _key, nested in value.items():
            strings.extend(_flatten_strings(nested))
        return strings
    if isinstance(value, list):
        strings = []
        for nested in value:
            strings.extend(_flatten_strings(nested))
        return strings
    return [str(value)] if value is not None else []


def _scan_reasons(value: Any) -> set[str]:
    payload = "\n".join(_flatten_strings(value))
    return {reason for reason, pattern in PROTECTED_PATTERNS if pattern.search(payload)}


def _require(condition: bool, failures: list[str], message: str) -> None:
    if not condition:
        failures.append(message)


def _is_public_review_bundle_relative_path(path: str) -> bool:
    if not isinstance(path, str) or not path:
        return False
    if "://" in path or path.startswith("~"):
        return False
    if Path(path).is_absolute() or PurePosixPath(path).is_absolute():
        return False
    windows_path = PureWindowsPath(path)
    if windows_path.is_absolute() or windows_path.drive or windows_path.root:
        return False
    parts = set(PurePosixPath(path).parts) | set(windows_path.parts)
    return ".." not in parts


def _validate_required_source_truth(failures: list[str]) -> None:
    ai_plan = _read(AI_EDITION_PLAN)
    branch_plan = _read(FAM007_BRANCH_PLAN)
    branch_record = _read(FAM007_BRANCH_RECORD)
    dev_owner_plan = _read(FAM007_DEV_OWNER_BRANCH_PLAN)
    dev_owner_record = _read(FAM007_DEV_OWNER_BRANCH_RECORD)
    runtime_trust_plan = _read(FAM007_AI_RUNTIME_TRUST_BRANCH_PLAN)
    runtime_trust_record = _read(FAM007_AI_RUNTIME_TRUST_BRANCH_RECORD)
    breakpoint2_plan = _read(FAM007_BREAKPOINT2_BRANCH_PLAN)
    breakpoint2_record = _read(FAM007_BREAKPOINT2_BRANCH_RECORD)
    registry = _read(VALIDATION_REGISTRY)
    helper = _read(REVIEW_BUNDLE_HELPER)
    for phrase in REQUIRED_AI_PLAN_PHRASES:
        _require(phrase in ai_plan, failures, f"{AI_EDITION_PLAN}: missing {phrase!r}")
    for phrase in REQUIRED_BRANCH_PLAN_PHRASES:
        _require(phrase in branch_plan, failures, f"{FAM007_BRANCH_PLAN}: missing {phrase!r}")
    for phrase in REQUIRED_RECORD_PHRASES:
        _require(phrase in branch_record, failures, f"{FAM007_BRANCH_RECORD}: missing {phrase!r}")
    for phrase in REQUIRED_DEV_OWNER_PLAN_PHRASES:
        _require(
            phrase in dev_owner_plan,
            failures,
            f"{FAM007_DEV_OWNER_BRANCH_PLAN}: missing {phrase!r}",
        )
    for phrase in REQUIRED_DEV_OWNER_RECORD_PHRASES:
        _require(
            phrase in dev_owner_record,
            failures,
            f"{FAM007_DEV_OWNER_BRANCH_RECORD}: missing {phrase!r}",
        )
    for phrase in REQUIRED_AI_RUNTIME_TRUST_PLAN_PHRASES:
        _require(
            phrase in runtime_trust_plan,
            failures,
            f"{FAM007_AI_RUNTIME_TRUST_BRANCH_PLAN}: missing {phrase!r}",
        )
    for phrase in REQUIRED_AI_RUNTIME_TRUST_RECORD_PHRASES:
        _require(
            phrase in runtime_trust_record,
            failures,
            f"{FAM007_AI_RUNTIME_TRUST_BRANCH_RECORD}: missing {phrase!r}",
        )
    for phrase in REQUIRED_BREAKPOINT2_PLAN_PHRASES:
        _require(
            phrase in breakpoint2_plan,
            failures,
            f"{FAM007_BREAKPOINT2_BRANCH_PLAN}: missing {phrase!r}",
        )
    for phrase in REQUIRED_BREAKPOINT2_RECORD_PHRASES:
        _require(
            phrase in breakpoint2_record,
            failures,
            f"{FAM007_BREAKPOINT2_BRANCH_RECORD}: missing {phrase!r}",
        )
    for phrase in BREAKPOINT2_STALE_WORKSTREAM_PHRASES:
        _require(
            phrase not in breakpoint2_plan,
            failures,
            f"{FAM007_BREAKPOINT2_BRANCH_PLAN}: stale post-H1 Workstream phrase remains {phrase!r}",
        )
        _require(
            phrase not in breakpoint2_record,
            failures,
            f"{FAM007_BREAKPOINT2_BRANCH_RECORD}: stale post-H1 Workstream phrase remains {phrase!r}",
        )
    for phrase in REQUIRED_REGISTRY_PHRASES:
        _require(phrase in registry, failures, f"{VALIDATION_REGISTRY}: missing {phrase!r}")
    for phrase in (
        "PUBLIC_REVIEW_BUNDLE_LEAK_PREVENTION_STATUS",
        "PRIVATE_REVIEW_BUNDLE_PATH_PATTERNS",
        "_public_review_bundle_file_list_failures",
        "WORKSTREAM_ENTRY_PACKET_REQUIRED_FILES",
        "_validate_workstream_entry_packet_decision_path",
        "validate_workstream_entry_packet_folder",
    ):
        _require(phrase in helper, failures, f"{REVIEW_BUNDLE_HELPER}: missing {phrase!r}")


def _validate_public_safe_fixture(fixture_set: dict[str, Any], failures: list[str]) -> None:
    fixture = fixture_set.get("publicSafeFixture", {})
    _require(fixture.get("schema") == "fam007-public-safe-fixture-v1", failures, "public-safe fixture schema mismatch")
    for field in SAFE_FIXTURE_BOOLEAN_FIELDS:
        _require(fixture.get(field) is True, failures, f"public-safe fixture must set {field}=true")
    _require(
        fixture.get("sanitizationApproval") == "not-required-synthetic",
        failures,
        "public-safe fixture must be synthetic instead of sanitizer-dependent",
    )
    reasons = _scan_reasons(fixture)
    _require(not reasons, failures, f"public-safe fixture contains protected patterns: {sorted(reasons)}")


def _validate_public_review_bundle(fixture_set: dict[str, Any], failures: list[str]) -> None:
    bundle = fixture_set.get("publicReviewBundle", {})
    _require(bundle.get("schema") == "fam007-public-review-bundle-v1", failures, "public review bundle schema mismatch")
    _require(bundle.get("bundleType") == "public", failures, "public review bundle must declare bundleType=public")
    _require(bundle.get("privateReviewBundle") is False, failures, "public review bundle must not be private")
    _require(
        bundle.get("containsOwnerDevPrivateMaterial") is False,
        failures,
        "public review bundle must exclude Owner/Dev private material",
    )
    for file_entry in bundle.get("files", []):
        path = file_entry.get("path", "")
        _require(_is_public_review_bundle_relative_path(path), failures, f"public review bundle path must be repo-relative: {path!r}")
    reasons = _scan_reasons(bundle)
    _require(not reasons, failures, f"public review bundle contains protected patterns: {sorted(reasons)}")


def _validate_review_bundle_path_canaries(fixture_set: dict[str, Any], failures: list[str]) -> None:
    canaries = fixture_set.get("reviewBundlePathCanaries", [])
    _require(len(canaries) >= 6, failures, "review bundle path canaries must cover relative and absolute path forms")
    seen_cases: set[str] = set()
    for canary in canaries:
        case_id = str(canary.get("caseId", ""))
        path = canary.get("path", "")
        expected = canary.get("expectedRepoRelative")
        actual = _is_public_review_bundle_relative_path(path)
        seen_cases.add(case_id)
        _require(
            actual is expected,
            failures,
            f"review bundle path canary {case_id} expected repo-relative={expected!r}, got {actual!r} for {path!r}",
        )
        helper_failures = user_review_bundle._public_review_bundle_file_list_failures([path])
        helper_actual = not helper_failures
        _require(
            helper_actual is expected,
            failures,
            f"review bundle helper canary {case_id} expected repo-relative={expected!r}, got {helper_actual!r} for {path!r}",
        )
    for required_case in (
        "repo-relative-root-file",
        "repo-relative-nested-file",
        "windows-drive-absolute",
        "windows-drive-relative",
        "windows-rooted-path",
        "windows-unc-path",
        "posix-absolute",
        "parent-traversal",
        "url-path",
    ):
        _require(required_case in seen_cases, failures, f"review bundle path canaries missing {required_case}")


def _validate_edition_manifest(fixture_set: dict[str, Any], failures: list[str]) -> None:
    manifest = fixture_set.get("editionBoundaryManifest", {})
    _require(manifest.get("schema") == "fam007-edition-boundary-manifest-v1", failures, "edition manifest schema mismatch")
    _require(manifest.get("edition") == "Public", failures, "edition manifest must be Public")
    _require(manifest.get("repoRole") == "public", failures, "edition manifest repoRole must be public")
    for field in PUBLIC_MANIFEST_FALSE_FIELDS:
        _require(manifest.get(field) is False, failures, f"public edition manifest must set {field}=false")
    blocked = set(manifest.get("blockedCapabilityClasses", []))
    for capability in (
        "owner_private_memory",
        "dev_private_tools",
        "provider_execution",
        "model_execution",
        "downloads",
        "external_calls",
        "memory_learning_personalization",
        "voice_core_sync",
    ):
        _require(capability in blocked, failures, f"public edition manifest must block {capability}")
    scan_manifest = dict(manifest)
    scan_manifest["blockedCapabilityClasses"] = []
    reasons = _scan_reasons(scan_manifest)
    _require(not reasons, failures, f"public edition manifest contains protected patterns: {sorted(reasons)}")


def _validate_public_build_audit(fixture_set: dict[str, Any], failures: list[str]) -> None:
    audit = fixture_set.get("publicBuildAudit", {})
    _require(audit.get("schema") == "fam007-public-build-audit-v1", failures, "public build audit schema mismatch")
    _require(audit.get("failClosedOnPrivateAsset") is True, failures, "public build audit must fail closed")
    _require(audit.get("privateOverlayIncluded") is False, failures, "public build audit must exclude private overlays")
    _require(audit.get("privateCapabilityReferenceIncluded") is False, failures, "public build audit must exclude private capability references")
    _require(audit.get("privateModelReferenceIncluded") is False, failures, "public build audit must exclude private model references")
    reasons = _scan_reasons(audit)
    _require(not reasons, failures, f"public build audit contains protected patterns: {sorted(reasons)}")


def _validate_dev_owner_skeleton_readiness(fixture_set: dict[str, Any], failures: list[str]) -> None:
    readiness = fixture_set.get("devOwnerSkeletonReadiness", {})
    _require(
        readiness.get("schema") == "fam007-dev-owner-skeleton-readiness-fixture-v1",
        failures,
        "Dev/Owner skeleton readiness fixture schema mismatch",
    )
    _require(readiness.get("planningOnly") is True, failures, "Dev/Owner readiness must be planning-only")
    _require(
        readiness.get("publicSafeProofOnly") is True,
        failures,
        "Dev/Owner readiness must be public-safe proof only",
    )

    action_gates = readiness.get("actionGates", {})
    _require(
        action_gates.get("dev") == "USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE",
        failures,
        "Dev skeleton readiness must cite the Dev private repo action gate",
    )
    _require(
        action_gates.get("owner") == "USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE",
        failures,
        "Owner skeleton readiness must cite the Owner private repo action gate",
    )
    _require(
        action_gates.get("githubDesktop") == "USER-ACTION-FAM007-GITHUB-DESKTOP-PRIVATE-REMOTE-SETUP",
        failures,
        "GitHub Desktop readiness must cite the private remote setup action gate",
    )

    setup_state = readiness.get("setupState", {})
    for field in (
        "privateDevRepositoryCreated",
        "privateOwnerRepositoryCreated",
        "ownerLocalOnlyRootCreated",
        "githubDesktopPrivateRemoteConfigured",
        "providerModelExecutionEnabled",
        "memoryPersonalizationEnabled",
        "downloadsNetworkExternalCallsEnabled",
        "voiceCoreSyncEnabled",
    ):
        _require(setup_state.get(field) is False, failures, f"Dev/Owner readiness must set {field}=false")

    dev = readiness.get("devSkeleton", {})
    _require(dev.get("trustedButNotOwnerPrivate") is True, failures, "Dev skeleton must remain trusted but not owner-private")
    _require(dev.get("ownerPrivateInheritanceAllowed") is False, failures, "Dev skeleton must block owner-private inheritance")
    _require(dev.get("privateSetupState") == "pending-user-action", failures, "Dev private setup must remain pending USER action")
    _require(
        dev.get("publicSourceScope") == "readiness-proof-only",
        failures,
        "Dev public source scope must be readiness-proof-only",
    )

    owner = readiness.get("ownerSkeleton", {})
    _require(owner.get("editionName") == "Nexus Desktop AI Owner", failures, "Owner skeleton must preserve accepted edition name")
    _require(owner.get("ownerOnly") is True, failures, "Owner skeleton must be owner-only")
    _require(owner.get("privateSetupState") == "pending-user-action", failures, "Owner private setup must remain pending USER action")
    _require(owner.get("devPublicInheritanceAllowed") is False, failures, "Owner material must not flow to Dev/Public by default")
    _require(
        owner.get("localOnlyAllowedBeforePrivateHosting") is True,
        failures,
        "Owner skeleton must preserve local-only option before private hosting",
    )

    remote_safety = readiness.get("githubDesktopPrivateRemoteSafety", {})
    _require(remote_safety.get("configurationState") == "planning-only", failures, "GitHub Desktop setup must remain planning-only")
    _require(remote_safety.get("privateOriginRequired") is True, failures, "private origin must be required for hosted Dev/Owner repos")
    _require(remote_safety.get("publicRemoteName") == "public-upstream", failures, "public remote must be named public-upstream")
    _require(remote_safety.get("publicUpstreamPushAllowed") is False, failures, "public-upstream push must remain blocked")
    _require(remote_safety.get("publicRemoteAsOriginAllowed") is False, failures, "public remote must not be origin in private roots")

    forbidden = readiness.get("forbiddenMaterialPresence", {})
    for field in (
        "privateRemoteUrl",
        "tokenOrCredential",
        "ownerSecret",
        "privatePath",
        "promptPayload",
        "memoryPayload",
        "privateAutomation",
        "modelArtifact",
        "capabilityPackAsset",
        "privateHostingSecret",
    ):
        _require(forbidden.get(field) is False, failures, f"Dev/Owner readiness must set forbidden {field}=false")

    provider_boundary = readiness.get("providerBoundary", {})
    for field in ("sentToProvider", "canAcceptPrompts"):
        _require(provider_boundary.get(field) is False, failures, f"provider boundary must set {field}=false")
    _require(provider_boundary.get("providerVisibleData") == "none", failures, "provider visible data must remain none")
    _require(
        provider_boundary.get("providerModelExecution") == "deferred",
        failures,
        "provider/model execution must remain deferred",
    )


def _validate_remaining_workstream_readiness(fixture_set: dict[str, Any], failures: list[str]) -> None:
    readiness = fixture_set.get("remainingWorkstreamReadiness", {})
    _require(
        readiness.get("schema") == "fam007-remaining-workstream-readiness-fixture-v1",
        failures,
        "remaining Workstream readiness fixture schema mismatch",
    )
    _require(readiness.get("planningOnly") is True, failures, "remaining Workstream readiness must be planning-only")
    _require(
        readiness.get("publicSafeProofOnly") is True,
        failures,
        "remaining Workstream readiness must be public-safe proof only",
    )
    _require(
        readiness.get("workstreamGreenReady") is True,
        failures,
        "remaining Workstream readiness must mark Workstream Green readiness",
    )

    action_gates = readiness.get("actionGates", {})
    expected_gates = {
        "backupRecovery": "USER-ACTION-FAM007-AI-DATA-BACKUP-RECOVERY",
        "publicToDevMigration": "USER-ACTION-FAM007-PUBLIC-TO-DEV-MIGRATION-CONSENT",
        "privateToPublicSanitization": "USER-ACTION-FAM007-PRIVATE-TO-PUBLIC-SANITIZATION",
        "providerModelExecution": "USER-ACTION-FAM007-PROVIDER-MODEL-EXECUTION",
        "memoryLearningPersonalization": "USER-ACTION-FAM007-MEMORY-LEARNING-PERSONALIZATION",
    }
    for field, expected in expected_gates.items():
        _require(action_gates.get(field) == expected, failures, f"remaining Workstream action gate {field} mismatch")

    setup_state = readiness.get("setupState", {})
    for field in (
        "offBootBackupRootCreated",
        "backupRestoreImplemented",
        "publicToDevImportImplemented",
        "providerSdkIntegrated",
        "modelExecutionEnabled",
        "modelDownloadsEnabled",
        "externalCallsEnabled",
        "memoryLearningPersonalizationEnabled",
        "voiceCoreSyncEnabled",
        "privateDevOwnerReposCreated",
    ):
        _require(setup_state.get(field) is False, failures, f"remaining Workstream must set {field}=false")

    backup = readiness.get("backupRecoveryPlanning", {})
    _require(backup.get("state") == "planning-only", failures, "backup/recovery planning must remain planning-only")
    _require(backup.get("offBootRequired") is True, failures, "backup/recovery planning must require off-boot roots")
    _require(backup.get("bootDriveOnlyAllowed") is False, failures, "backup/recovery planning must reject boot-drive-only backup")
    _require(
        backup.get("restoreProofRequiredBeforeImplementation") is True,
        failures,
        "backup/recovery planning must require restore proof before implementation",
    )
    _require(
        backup.get("editionSeparatedRecoveryRequired") is True,
        failures,
        "backup/recovery planning must require edition-separated recovery",
    )
    _require(
        backup.get("privateMaterialRequiresEncryptionOrVaultPlan") is True,
        failures,
        "backup/recovery planning must require encryption/vault planning for private material",
    )
    _require(
        backup.get("publicRepoBackupStorageAllowed") is False,
        failures,
        "backup/recovery planning must block public repo backup storage",
    )

    separation = readiness.get("publicToPrivateSeparation", {})
    _require(separation.get("state") == "planning-only", failures, "public-to-private separation must remain planning-only")
    _require(separation.get("copyOnlyImportRequired") is True, failures, "public-to-private separation must require copy-only import")
    for field in ("secretsTokensImportedByDefault", "ownerPrivateDataImportedToDevOrPublic", "noExportDataImportedByDefault"):
        _require(separation.get(field) is False, failures, f"public-to-private separation must set {field}=false")
    _require(
        separation.get("privateToPublicSanitizationGateRequired") is True,
        failures,
        "public-to-private separation must require private-to-public sanitization gate",
    )
    _require(
        separation.get("protectedAssetsExcluded") is True,
        failures,
        "public-to-private separation must exclude protected assets",
    )

    provider = readiness.get("providerModelDeferral", {})
    _require(provider.get("state") == "deferred", failures, "provider/model deferral must remain deferred")
    for field in ("providerSdkExecutionAllowed", "modelExecutionAllowed", "modelDownloadsAllowed", "externalCallsAllowed"):
        _require(provider.get(field) is False, failures, f"provider/model deferral must set {field}=false")
    _require(provider.get("providerVisibleData") == "none", failures, "provider/model deferral must keep providerVisibleData=none")
    for field in ("sentToProvider", "canAcceptPrompts"):
        _require(provider.get(field) is False, failures, f"provider/model deferral must set {field}=false")

    handoff = readiness.get("futureHandoffCriteria", {})
    _require(handoff.get("state") == "ready-for-hardening-review", failures, "future handoff must point to Hardening review")
    _require(handoff.get("planningOnly") is True, failures, "future handoff criteria must remain planning-only")
    for field in (
        "privateRepoCreationAuthorized",
        "privateRemoteConfigurationAuthorized",
        "backupImplementationAuthorized",
        "publicToDevImportAuthorized",
        "providerModelExecutionAuthorized",
    ):
        _require(handoff.get(field) is False, failures, f"future handoff criteria must set {field}=false")
    _require(handoff.get("nextLegalPhase") == "Hardening H1", failures, "future handoff must name Hardening H1")

    forbidden = readiness.get("forbiddenMaterialPresence", {})
    for field in (
        "privateRemoteUrl",
        "tokenOrCredential",
        "ownerSecret",
        "privatePath",
        "promptPayload",
        "memoryPayload",
        "privateAutomation",
        "modelArtifact",
        "capabilityPackAsset",
        "privateHostingSecret",
    ):
        _require(forbidden.get(field) is False, failures, f"remaining Workstream must set forbidden {field}=false")


def _validate_ai_runtime_trust_boundary_readiness(fixture_set: dict[str, Any], failures: list[str]) -> None:
    readiness = fixture_set.get("aiRuntimeTrustBoundaryReadiness", {})
    _require(
        readiness.get("schema") == "fam007-ai-runtime-trust-boundary-readiness-fixture-v1",
        failures,
        "AI runtime/trust-boundary readiness fixture schema mismatch",
    )
    _require(readiness.get("planningOnly") is True, failures, "AI runtime/trust-boundary readiness must be planning-only")
    _require(
        readiness.get("publicSafeProofOnly") is True,
        failures,
        "AI runtime/trust-boundary readiness must be public-safe proof only",
    )
    _require(
        readiness.get("workstreamGreenReady") is True,
        failures,
        "AI runtime/trust-boundary readiness must mark Workstream Green readiness",
    )

    options = readiness.get("options", {})
    for option_id in ("option1", "option2", "option3", "option4"):
        option = options.get(option_id, {})
        _require(
            option.get("status") == "implemented-public-safe-proof-only",
            failures,
            f"AI runtime/trust-boundary {option_id} must be implemented as public-safe proof only",
        )

    option1 = options.get("option1", {})
    required_states = {
        "Installed",
        "Available",
        "Enabled",
        "Disabled",
        "Denied",
        "Suspended",
        "Revoked",
        "Requires Setup",
        "Requires Hardware",
        "Requires Consent",
        "Blocked By Privacy Mode",
        "Blocked By Safety Policy",
        "Blocked By Competitive Integrity Mode",
        "Blocked By Provider State",
    }
    _require(
        required_states.issubset(set(option1.get("permissionStates", []))),
        failures,
        "Option 1 permission-state proof is missing required capability states",
    )
    _require(
        {"ai-layer", "tool-capability-layer"}.issubset(set(option1.get("enforcedAtLayers", []))),
        failures,
        "Option 1 must enforce permission state at AI and tool/capability layers",
    )
    provider_boundary = option1.get("providerBoundary", {})
    _require(provider_boundary.get("providerVisibleData") == "none", failures, "Option 1 providerVisibleData must remain none")
    for field in ("sentToProvider", "canAcceptPrompts"):
        _require(provider_boundary.get(field) is False, failures, f"Option 1 provider boundary must set {field}=false")
    for field, expected in {
        "promptExecution": "disabled",
        "providerExecution": "disabled",
        "modelExecution": "disabled",
        "downloadsNetworkExternalCalls": "blocked",
    }.items():
        _require(provider_boundary.get(field) == expected, failures, f"Option 1 provider boundary {field} mismatch")
    _require(
        provider_boundary.get("localOnlyPosturePreserved") is True,
        failures,
        "Option 1 must preserve local-only posture",
    )

    option2 = options.get("option2", {})
    _require(
        option2.get("objectiveAnswerPolicy") == "deterministic-or-tool-backed-required",
        failures,
        "Option 2 objective-answer policy must require deterministic/tool-backed paths",
    )
    _require(option2.get("calculatorMathRouting") == "deterministic-required", failures, "Option 2 calculator/math routing mismatch")
    _require(option2.get("sourceCitationRouting") == "required-when-source-backed", failures, "Option 2 source/citation routing mismatch")
    _require(
        option2.get("windowsHealthRouting") == "observed-versus-inferred-separated",
        failures,
        "Option 2 Windows Health routing must separate observed and inferred evidence",
    )
    _require(
        {"Deterministic", "High Confidence", "Advisory", "Creative/Open-ended"}.issubset(
            set(option2.get("confidenceTiers", []))
        ),
        failures,
        "Option 2 confidence tiers are incomplete",
    )
    _require(option2.get("refusalBehavior") == "refuse-to-pretend-certainty", failures, "Option 2 refusal behavior mismatch")
    _require(option2.get("runtimeRouterImplemented") is False, failures, "Option 2 must not implement a runtime router")
    _require(
        option2.get("providerRecommendationExecutionAllowed") is False,
        failures,
        "Option 2 provider recommendation execution must remain blocked",
    )

    option3 = options.get("option3", {})
    _require(option3.get("cacheIsNotMemory") is True, failures, "Option 3 must preserve cache-is-not-memory")
    for field in ("runtimeCacheImplementation", "memoryWriteEnabled", "trustJournalRuntimeImplemented", "telemetryEnabled"):
        _require(option3.get(field) is False, failures, f"Option 3 must set {field}=false")
    required_scope_classes = {
        "Session cache",
        "Operational cache",
        "Deterministic validation cache",
        "Advisory cache",
        "Provider-response cache",
        "Capability-pack index cache",
        "Windows Health analysis cache",
        "Temporary routine-context cache",
    }
    _require(
        required_scope_classes.issubset(set(option3.get("cacheScopeClasses", []))),
        failures,
        "Option 3 cache scope classes are incomplete",
    )
    _require(
        {"Low", "Medium", "High", "Very High", "Critical"}.issubset(set(option3.get("cacheSensitivityClasses", []))),
        failures,
        "Option 3 cache sensitivity classes are incomplete",
    )
    replay = option3.get("replaySafety", {})
    for field in (
        "deterministicReplayRequiresInputToolSourcePermissionPolicyMatch",
        "advisoryProviderCacheCannotReplayAsCurrentTruth",
        "safetySensitiveCacheRequiresFreshnessRevalidation",
        "replayDecisionsJournalable",
    ):
        _require(replay.get(field) is True, failures, f"Option 3 replay safety must set {field}=true")
    sanitization = option3.get("providerCacheSanitization", {})
    for field in (
        "privatePromptAllowed",
        "secretAllowed",
        "privatePathAllowed",
        "memoryPayloadAllowed",
        "identityDataAllowed",
        "protectedRepoMaterialAllowed",
    ):
        _require(sanitization.get(field) is False, failures, f"Option 3 provider-cache sanitization must set {field}=false")
    privacy_modes = option3.get("privacyModes", {})
    for field in (
        "localOnlyBlocksProviderCache",
        "privacyLockdownBlocksSensitiveCacheWrites",
        "clearOperationalCacheDoesNotDeleteMemoryLogsOrBackups",
    ):
        _require(privacy_modes.get(field) is True, failures, f"Option 3 privacy mode proof must set {field}=true")

    option4 = options.get("option4", {})
    required_manifest = {
        "declares-capability",
        "declares-limits",
        "declares-source-provenance",
        "declares-hardware-storage-provider-requirements",
        "declares-cache-ownership",
        "declares-local-only-or-provider-assisted-mode",
    }
    _require(
        required_manifest.issubset(set(option4.get("capabilityPackManifestExpectations", []))),
        failures,
        "Option 4 capability-pack manifest expectations are incomplete",
    )
    for field in (
        "capabilityPackInstalled",
        "capabilityPackExecuted",
        "modelOrCapabilityDownloadsEnabled",
        "storageRootCreated",
        "privateEditionSkeletonSetup",
    ):
        _require(option4.get(field) is False, failures, f"Option 4 must set {field}=false")
    local_only = option4.get("localOnlyHandoff", {})
    _require(local_only.get("providerCallsBlocked") is True, failures, "Option 4 local-only handoff must block provider calls")
    _require(local_only.get("providerCacheBlocked") is True, failures, "Option 4 local-only handoff must block provider cache")
    _require(
        local_only.get("hiddenExternalDependenciesAllowed") is False,
        failures,
        "Option 4 local-only handoff must block hidden external dependencies",
    )
    _require(local_only.get("providerVisibleData") == "none", failures, "Option 4 local-only handoff providerVisibleData must remain none")
    _require(
        local_only.get("localOnlyRuntimeGuaranteeImplemented") is False,
        failures,
        "Option 4 must not claim a runtime local-only guarantee implementation",
    )

    setup_state = readiness.get("setupState", {})
    for field in (
        "privateDevRepositoryCreated",
        "privateOwnerRepositoryCreated",
        "githubDesktopPrivateRemoteConfigured",
        "offBootBackupRootCreated",
        "publicToDevImportImplemented",
        "providerSdkIntegrated",
        "modelExecutionEnabled",
        "modelDownloadsEnabled",
        "runtimeProviderExecutionEnabled",
        "runtimeCacheBehaviorEnabled",
        "externalCallsEnabled",
        "memoryLearningPersonalizationEnabled",
        "voiceCoreSyncEnabled",
    ):
        _require(setup_state.get(field) is False, failures, f"AI runtime/trust-boundary setupState must set {field}=false")

    gates = readiness.get("globalActionGates", {})
    expected_gates = {
        "providerModelExecution": "USER-ACTION-FAM007-PROVIDER-MODEL-EXECUTION",
        "memoryLearningPersonalization": "USER-ACTION-FAM007-MEMORY-LEARNING-PERSONALIZATION",
        "backupRecovery": "USER-ACTION-FAM007-AI-DATA-BACKUP-RECOVERY",
        "publicToDevMigration": "USER-ACTION-FAM007-PUBLIC-TO-DEV-MIGRATION-CONSENT",
        "privateDevRepository": "USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE",
        "privateOwnerRepository": "USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE",
        "githubDesktopPrivateRemote": "USER-ACTION-FAM007-GITHUB-DESKTOP-PRIVATE-REMOTE-SETUP",
    }
    for field, expected in expected_gates.items():
        _require(gates.get(field) == expected, failures, f"AI runtime/trust-boundary action gate {field} mismatch")

    forbidden = readiness.get("forbiddenMaterialPresence", {})
    for field in (
        "privateRemoteUrl",
        "tokenOrCredential",
        "ownerSecret",
        "privatePath",
        "promptPayload",
        "memoryPayload",
        "privateAutomation",
        "modelArtifact",
        "capabilityPackAsset",
        "privateHostingSecret",
    ):
        _require(forbidden.get(field) is False, failures, f"AI runtime/trust-boundary must set forbidden {field}=false")


def _validate_breakpoint2_seam1_action_gate_registry(fixture_set: dict[str, Any], failures: list[str]) -> None:
    registry = fixture_set.get("breakpoint2Seam1ActionGateRegistry", {})
    _require(
        registry.get("schema") == "fam007-breakpoint2-seam1-action-gate-registry-v1",
        failures,
        "Breakpoint 2 Seam 1 action-gate registry schema mismatch",
    )
    _require(
        registry.get("branch") == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness",
        failures,
        "Breakpoint 2 Seam 1 registry branch mismatch",
    )
    _require(registry.get("seam") == "Seam 1", failures, "Breakpoint 2 Seam 1 registry seam mismatch")
    _require(registry.get("planningOnly") is True, failures, "Breakpoint 2 Seam 1 registry must be planning-only")
    _require(
        registry.get("publicSafeProofOnly") is True,
        failures,
        "Breakpoint 2 Seam 1 registry must be public-safe proof only",
    )
    _require(
        registry.get("directValidationRequired") is True,
        failures,
        "Breakpoint 2 Seam 1 registry must require direct validation",
    )
    _require(
        registry.get("allGatesRemainPending") is True,
        failures,
        "Breakpoint 2 Seam 1 registry must keep all gates pending",
    )

    expected_gate_ids = {
        "USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE",
        "USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE",
        "USER-ACTION-FAM007-GITHUB-DESKTOP-PRIVATE-REMOTE-SETUP",
        "USER-ACTION-FAM007-AI-DATA-BACKUP-RECOVERY",
        "USER-ACTION-FAM007-PUBLIC-TO-DEV-MIGRATION-CONSENT",
        "USER-ACTION-FAM007-PRIVATE-TO-PUBLIC-SANITIZATION",
        "USER-ACTION-FAM007-OWNER-VAULT-OR-PRIVATE-HOSTING",
        "USER-ACTION-FAM007-PROVIDER-MODEL-EXECUTION",
        "USER-ACTION-FAM007-MEMORY-LEARNING-PERSONALIZATION",
        "USER-ACTION-FAM007-PACKAGING-EDITION-IDENTITY",
        "USER-GATE-FAM007-LOCAL-ONLY-PRIVATE-ROOT-CREATE",
        "USER-GATE-FAM007-MODEL-DOWNLOADS",
        "USER-GATE-FAM007-RUNTIME-PROVIDER-EXECUTION",
        "USER-GATE-FAM007-RUNTIME-CACHE-BEHAVIOR",
        "USER-GATE-FAM007-VOICE-CORE-SYNC",
        "USER-GATE-FAM007-SHORTCUT-INSTALLER-WORK",
        "USER-GATE-FAM007-PR-CREATION",
        "USER-GATE-FAM007-MERGE",
        "USER-GATE-FAM007-RELEASE-TAG-ARTIFACT",
        "USER-GATE-FAM007-BRANCH-WORKTREE-CLEANUP",
        "USER-GATE-FAM007-FAM006-GOVERNANCE-MUTATION",
        "USER-GATE-FAM007-AI-PRODUCT-CONTRACT-IMPORT",
        "USER-GATE-FAM007-PRIVATE-DEV-ORIN-IMPORT",
        "USER-GATE-FAM007-V1-8-0-PREBETA",
    }
    gates = registry.get("pendingUserDecisionGates", [])
    _require(isinstance(gates, list), failures, "Breakpoint 2 Seam 1 gates must be a list")
    gates_by_id = {gate.get("id"): gate for gate in gates if isinstance(gate, dict)}
    for gate_id in sorted(expected_gate_ids):
        gate = gates_by_id.get(gate_id)
        _require(gate is not None, failures, f"Breakpoint 2 Seam 1 registry missing gate {gate_id}")
        if gate is None:
            continue
        _require(
            gate.get("status") == "pending-user-decision",
            failures,
            f"Breakpoint 2 Seam 1 gate {gate_id} must remain pending-user-decision",
        )
        _require(gate.get("executed") is False, failures, f"Breakpoint 2 Seam 1 gate {gate_id} must set executed=false")
        _require(
            gate.get("authorizedBySeam1") is False,
            failures,
            f"Breakpoint 2 Seam 1 gate {gate_id} must set authorizedBySeam1=false",
        )

    public_safety = registry.get("publicSafetyProof", {})
    expected_false_fields = (
        "privateDevRepositoryCreated",
        "privateOwnerRepositoryCreated",
        "localOnlyPrivateRootCreated",
        "githubDesktopPrivateRemoteConfigured",
        "offBootBackupRootCreated",
        "publicToDevImportImplemented",
        "providerSdkIntegrated",
        "modelDownloadsEnabled",
        "runtimeProviderExecutionEnabled",
        "runtimeCacheBehaviorEnabled",
        "externalCallsEnabled",
        "memoryLearningIndexingRetrievalPersonalizationEnabled",
        "voiceCoreSyncEnabled",
        "shortcutInstallerWorkPerformed",
        "prCreated",
        "merged",
        "releaseTagArtifactExecuted",
        "cleanupPerformed",
        "fam006GovernanceMutationPerformed",
        "aiProductContractImported",
        "privateDevOrinImported",
        "v180PrebetaExecuted",
    )
    for field in expected_false_fields:
        _require(public_safety.get(field) is False, failures, f"Breakpoint 2 Seam 1 public safety must set {field}=false")

    provider_boundary = registry.get("providerBoundary", {})
    _require(provider_boundary.get("providerVisibleData") == "none", failures, "Breakpoint 2 Seam 1 providerVisibleData must be none")
    for field in ("sentToProvider", "canAcceptPrompts"):
        _require(provider_boundary.get(field) is False, failures, f"Breakpoint 2 Seam 1 provider boundary must set {field}=false")
    for field, expected in {
        "promptProviderModelExecution": "disabled",
        "downloadsNetworkExternalCalls": "blocked",
        "memoryLearningPersonalization": "inactive",
        "voiceCoreSync": "gated",
    }.items():
        _require(provider_boundary.get(field) == expected, failures, f"Breakpoint 2 Seam 1 provider boundary {field} mismatch")

    forbidden = registry.get("forbiddenMaterialPresence", {})
    for field in (
        "privateRemoteUrl",
        "tokenOrCredential",
        "ownerSecret",
        "privatePath",
        "modelArtifact",
        "promptPayload",
        "memoryPayload",
        "privateAutomationContent",
    ):
        _require(forbidden.get(field) is False, failures, f"Breakpoint 2 Seam 1 must set forbidden {field}=false")

    exact_decision = str(registry.get("exactUserDecisionProof", ""))
    for phrase in (
        "Seam 1",
        "Action-gate registry and exact USER decision proof",
        "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness",
        "public-safe proof",
    ):
        _require(phrase in exact_decision, failures, f"Breakpoint 2 Seam 1 exact USER decision proof missing {phrase!r}")

    next_decision = str(registry.get("exactNextUserDecision", ""))
    for phrase in (
        "Seam 2",
        "Private/public boundary and private remote safety proof",
        "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness",
    ):
        _require(phrase in next_decision, failures, f"Breakpoint 2 Seam 1 exact next USER decision missing {phrase!r}")


def _validate_breakpoint2_remaining_workstream_readiness(fixture_set: dict[str, Any], failures: list[str]) -> None:
    readiness = fixture_set.get("breakpoint2RemainingWorkstreamReadiness", {})
    _require(
        readiness.get("schema") == "fam007-breakpoint2-remaining-workstream-readiness-v1",
        failures,
        "Breakpoint 2 remaining Workstream readiness schema mismatch",
    )
    _require(
        readiness.get("branch") == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness",
        failures,
        "Breakpoint 2 remaining Workstream branch mismatch",
    )
    _require(
        readiness.get("seamGroup") == "Seams 2 through 4",
        failures,
        "Breakpoint 2 remaining Workstream seam group mismatch",
    )
    for field in ("planningOnly", "publicSafeProofOnly", "directValidationRequired", "workstreamGreenReady", "allFutureGatesRemainPending"):
        _require(readiness.get(field) is True, failures, f"Breakpoint 2 remaining Workstream must set {field}=true")

    implemented = readiness.get("implementedSeams", {})
    seam2 = implemented.get("seam2", {})
    _require(seam2.get("name") == "Private/public boundary and private remote safety proof", failures, "Breakpoint 2 Seam 2 name mismatch")
    _require(seam2.get("status") == "implemented-public-safe-proof-only", failures, "Breakpoint 2 Seam 2 status mismatch")
    _require(seam2.get("githubDesktopPrivateRemoteConfigured") is False, failures, "Breakpoint 2 Seam 2 must not configure GitHub Desktop private remote")
    _require(seam2.get("privateRemoteConfigurationState") == "planning-only", failures, "Breakpoint 2 Seam 2 private remote state must be planning-only")
    _require(seam2.get("publicRemoteName") == "public-upstream", failures, "Breakpoint 2 Seam 2 public remote name mismatch")
    for field in ("privateRemoteUrlAllowed", "tokenOrCredentialAllowed", "ownerSecretAllowed", "privatePathAllowed", "modelArtifactAllowed", "promptPayloadAllowed", "memoryPayloadAllowed", "privateAutomationContentAllowed", "publicUpstreamPushAllowed", "publicRemoteAsOriginAllowed"):
        _require(seam2.get(field) is False, failures, f"Breakpoint 2 Seam 2 must set {field}=false")

    seam3 = implemented.get("seam3", {})
    _require(seam3.get("name") == "Backup/recovery and Public-to-Dev import planning proof", failures, "Breakpoint 2 Seam 3 name mismatch")
    _require(seam3.get("status") == "implemented-planning-proof-only", failures, "Breakpoint 2 Seam 3 status mismatch")
    _require(seam3.get("backupRecoveryPlanningState") == "planning-only", failures, "Breakpoint 2 Seam 3 backup state must be planning-only")
    _require(seam3.get("offBootRequired") is True, failures, "Breakpoint 2 Seam 3 must require off-boot planning")
    _require(seam3.get("restoreProofRequiredBeforeImplementation") is True, failures, "Breakpoint 2 Seam 3 must require restore proof before implementation")
    _require(seam3.get("privateMaterialRequiresEncryptionOrVaultPlan") is True, failures, "Breakpoint 2 Seam 3 must require encryption/vault planning")
    for field in ("offBootBackupRootCreated", "backupRestoreImplemented", "publicToDevImportImplemented", "publicRepoBackupStorageAllowed", "secretsTokensImportedByDefault", "ownerPrivateDataImportedToDevOrPublic", "noExportDataImportedByDefault"):
        _require(seam3.get(field) is False, failures, f"Breakpoint 2 Seam 3 must set {field}=false")

    seam4 = implemented.get("seam4", {})
    _require(seam4.get("name") == "Provider/model/runtime/cache/memory deferral and local-only handoff proof", failures, "Breakpoint 2 Seam 4 name mismatch")
    _require(seam4.get("status") == "implemented-public-safe-deferral-proof-only", failures, "Breakpoint 2 Seam 4 status mismatch")
    _require(seam4.get("providerVisibleData") == "none", failures, "Breakpoint 2 Seam 4 providerVisibleData must be none")
    _require(seam4.get("promptProviderModelExecution") == "disabled", failures, "Breakpoint 2 Seam 4 prompt/provider/model execution must be disabled")
    _require(seam4.get("downloadsNetworkExternalCalls") == "blocked", failures, "Breakpoint 2 Seam 4 downloads/network/external calls must be blocked")
    _require(seam4.get("runtimeCacheState") == "inactive", failures, "Breakpoint 2 Seam 4 runtime cache must be inactive")
    _require(seam4.get("memoryLearningPersonalization") == "inactive", failures, "Breakpoint 2 Seam 4 memory/learning/personalization must be inactive")
    _require(seam4.get("voiceCoreSync") == "gated", failures, "Breakpoint 2 Seam 4 voice/Core sync must be gated")
    _require(seam4.get("cacheIsNotMemory") is True, failures, "Breakpoint 2 Seam 4 must preserve cache-is-not-memory")
    _require(seam4.get("localOnlyHandoffReady") is True, failures, "Breakpoint 2 Seam 4 must be ready for local-only handoff review")
    for field in ("sentToProvider", "canAcceptPrompts", "providerSdkIntegrated", "modelExecutionEnabled", "modelDownloadsEnabled", "runtimeProviderExecutionEnabled", "runtimeCacheBehaviorEnabled", "externalCallsEnabled", "memoryLearningIndexingRetrievalPersonalizationEnabled", "trustJournalRuntimeImplemented", "telemetryEnabled"):
        _require(seam4.get(field) is False, failures, f"Breakpoint 2 Seam 4 must set {field}=false")

    gate_states = readiness.get("futureActionGateStates", {})
    expected_gates = {
        "privateDevRepo": "USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE",
        "privateOwnerRepo": "USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE",
        "githubDesktopPrivateRemote": "USER-ACTION-FAM007-GITHUB-DESKTOP-PRIVATE-REMOTE-SETUP",
        "backupRecovery": "USER-ACTION-FAM007-AI-DATA-BACKUP-RECOVERY",
        "publicToDevMigration": "USER-ACTION-FAM007-PUBLIC-TO-DEV-MIGRATION-CONSENT",
        "privateToPublicSanitization": "USER-ACTION-FAM007-PRIVATE-TO-PUBLIC-SANITIZATION",
        "providerModelExecution": "USER-ACTION-FAM007-PROVIDER-MODEL-EXECUTION",
        "memoryLearningPersonalization": "USER-ACTION-FAM007-MEMORY-LEARNING-PERSONALIZATION",
        "runtimeCacheBehavior": "USER-GATE-FAM007-RUNTIME-CACHE-BEHAVIOR",
    }
    for field, expected in expected_gates.items():
        gate = gate_states.get(field, {})
        _require(gate.get("id") == expected, failures, f"Breakpoint 2 remaining gate {field} id mismatch")
        _require(gate.get("status") == "pending-user-decision", failures, f"Breakpoint 2 remaining gate {field} must remain pending")
        _require(gate.get("executed") is False, failures, f"Breakpoint 2 remaining gate {field} must set executed=false")
        _require(gate.get("authorizedByWorkstream") is False, failures, f"Breakpoint 2 remaining gate {field} must set authorizedByWorkstream=false")

    forbidden = readiness.get("forbiddenMaterialPresence", {})
    for field in (
        "privateRemoteUrl",
        "tokenOrCredential",
        "ownerSecret",
        "privatePath",
        "modelArtifact",
        "promptPayload",
        "memoryPayload",
        "privateAutomationContent",
        "privateHostingSecret",
    ):
        _require(forbidden.get(field) is False, failures, f"Breakpoint 2 remaining Workstream must set forbidden {field}=false")

    handoff = readiness.get("hardeningHandoff", {})
    _require(handoff.get("state") == "ready-for-hardening-review", failures, "Breakpoint 2 handoff must be ready for Hardening review")
    _require(handoff.get("nextLegalPhase") == "Hardening H1", failures, "Breakpoint 2 handoff next legal phase must be Hardening H1")
    _require(handoff.get("workstreamGreenCandidate") is True, failures, "Breakpoint 2 handoff must mark Workstream green candidate")
    for field in ("privateRepoCreationAuthorized", "privateRemoteConfigurationAuthorized", "backupImplementationAuthorized", "publicToDevImportAuthorized", "providerModelExecutionAuthorized", "runtimeCacheBehaviorAuthorized", "memoryLearningPersonalizationAuthorized"):
        _require(handoff.get(field) is False, failures, f"Breakpoint 2 handoff must set {field}=false")

    next_decision = str(readiness.get("exactNextUserDecision", ""))
    for phrase in (
        "Hardening H1",
        "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness",
        "all admitted Workstream seams",
    ):
        _require(phrase in next_decision, failures, f"Breakpoint 2 remaining exact next USER decision missing {phrase!r}")


def _validate_blocked_canaries(fixture_set: dict[str, Any], failures: list[str]) -> None:
    canaries = fixture_set.get("blockedCanaries", [])
    _require(len(canaries) >= 10, failures, "blocked canaries must cover all major private/leak classes")
    seen_expected: set[str] = set()
    for canary in canaries:
        expected = canary.get("expectedReason")
        reasons = _scan_reasons(canary.get("payload"))
        seen_expected.add(str(expected))
        _require(expected in reasons, failures, f"blocked canary {canary.get('caseId')} did not trigger {expected}; got {sorted(reasons)}")
    for required_reason in (
        "private-path",
        "private-prompt",
        "private-memory",
        "private-log-or-eval",
        "private-screenshot-or-model-output",
        "private-automation-or-handoff",
        "secret-or-token",
        "private-model-or-capability",
        "private-edition-runtime",
        "provider-execution",
        "network-or-download",
        "public-to-dev-import",
    ):
        _require(required_reason in seen_expected, failures, f"blocked canaries missing {required_reason}")


def _validate_provider_boundary(failures: list[str]) -> None:
    state = ai_provider_state.build_provider_setup_completion_foundation_state(
        ai_provider_state.build_default_provider_readiness_config()
    )
    payload = state.as_renderer_payload()
    for key, expected in PROVIDER_PAYLOAD_EXPECTATIONS.items():
        _require(payload.get(key) == expected, failures, f"provider payload {key}={payload.get(key)!r}, expected {expected!r}")


def _validate_workstream_entry_packet_decision_canaries(fixture_set: dict[str, Any], failures: list[str]) -> None:
    canaries = fixture_set.get("workstreamEntryPacketDecisionCanaries", [])
    _require(len(canaries) >= 6, failures, "workstream entry packet decision canaries must cover pass and failure cases")
    seen_cases: set[str] = set()
    for canary in canaries:
        case_id = str(canary.get("caseId", ""))
        seen_cases.add(case_id)
        result = user_review_bundle._validate_workstream_entry_packet_decision_path(
            canary.get("files", {}),
            expected_branch=canary.get("expectedBranch", ""),
            expected_head=canary.get("expectedHead", ""),
            expected_origin_main=canary.get("expectedOriginMain", ""),
            require_implementation_ready=canary.get("requireImplementationReady", False),
        )
        expected_valid = canary.get("expectedValid")
        expected_status = canary.get("expectedStatus")
        if expected_valid is True:
            _require(not result.failures, failures, f"packet decision canary {case_id} unexpectedly failed: {result.failures}")
        elif expected_valid is False:
            _require(bool(result.failures), failures, f"packet decision canary {case_id} unexpectedly passed")
        else:
            failures.append(f"packet decision canary {case_id} missing expectedValid boolean")
        _require(
            result.status == expected_status,
            failures,
            f"packet decision canary {case_id} expected status {expected_status!r}, got {result.status!r}",
        )
        expected_failure_contains = canary.get("expectedFailureContains")
        if expected_failure_contains:
            joined_failures = "\n".join(result.failures)
            _require(
                expected_failure_contains in joined_failures,
                failures,
                f"packet decision canary {case_id} did not report expected failure fragment {expected_failure_contains!r}",
            )
    for required_case in (
        "branch-correct-implementation-ready",
        "branch-correct-repair-revalidation",
        "stale-branch-packet",
        "missing-required-digest-file",
        "conflicting-next-legal-phase",
        "chat-only-decision-missing-packet-evidence",
        "unresolved-template-placeholder",
        "packet-count-mismatch",
    ):
        _require(required_case in seen_cases, failures, f"packet decision canaries missing {required_case}")


def validate() -> list[str]:
    failures: list[str] = []
    _require(FIXTURE_SET.is_file(), failures, f"{FIXTURE_SET.relative_to(ROOT)} is missing")
    if failures:
        return failures
    fixture_set = _load_fixture_set()
    _validate_required_source_truth(failures)
    _validate_public_safe_fixture(fixture_set, failures)
    _validate_public_review_bundle(fixture_set, failures)
    _validate_review_bundle_path_canaries(fixture_set, failures)
    _validate_edition_manifest(fixture_set, failures)
    _validate_public_build_audit(failures=failures, fixture_set=fixture_set)
    _validate_dev_owner_skeleton_readiness(fixture_set, failures)
    _validate_remaining_workstream_readiness(fixture_set, failures)
    _validate_ai_runtime_trust_boundary_readiness(fixture_set, failures)
    _validate_breakpoint2_seam1_action_gate_registry(fixture_set, failures)
    _validate_breakpoint2_remaining_workstream_readiness(fixture_set, failures)
    _validate_blocked_canaries(fixture_set, failures)
    _validate_provider_boundary(failures)
    _validate_workstream_entry_packet_decision_canaries(fixture_set, failures)
    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("FAIL: FAM-007 public leak-prevention validation failed.")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: FAM-007 public leak-prevention validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
