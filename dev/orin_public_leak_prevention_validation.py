# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=SRCOWN-FIRSTPASS-FAM007-AI-007; surface=fam007-public-leak-prevention-validator; status=shared
"""Validate FAM-007 AI Edition public leak-prevention proof surfaces."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import desktop.ai_provider_state as ai_provider_state  # noqa: E402


AI_EDITION_PLAN = Path(
    "Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md"
)
FAM007_BRANCH_PLAN = Path(
    "Docs/branch_plans/feature_fam_007_ai_edition_public_leak_prevention_foundation.md"
)
FAM007_BRANCH_RECORD = Path(
    "Docs/branch_records/feature_fam_007_ai_edition_public_leak_prevention_foundation.md"
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
    "Breakpoint 1: Public Leak-Prevention Foundation",
    "Breakpoint 2: Private Dev And Owner Skeleton Creation",
    "Private release notes, private tags, private builds, private capability packs",
)

REQUIRED_BRANCH_PLAN_PHRASES = (
    "Public Protected-Asset Leak Checklist And Public-Safe Fixture Contract",
    "Edition Boundary Manifest Planning / Public-Safe Schema Direction",
    "Public Build Exclusion Requirement And Audit Posture",
    "Public Review-Bundle Leak Prevention And Source-Truth Routing",
    "Dev/Owner Skeleton Handoff Criteria And Provider-Execution Continuation",
    "Provider-boundary preservation",
    "Workstream Green",
)

REQUIRED_RECORD_PHRASES = (
    "Phase: `Hardening`",
    "Workstream Status: `Green",
    "Stage: `H1 Green`",
    "Hardening H1 Result: `Green",
    "Next Legal Phase: `Live Validation`",
    "No visible runtime UI change",
    "Provider Execution State: `Blocked",
)

REQUIRED_REGISTRY_PHRASES = (
    "dev/orin_public_leak_prevention_validation.py",
    "FAM-007 public leak-prevention validator",
    "protected assets",
    "public-safe fixtures",
    "review-bundle leak prevention",
    "edition-boundary manifest",
    "public build exclusion",
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


def _validate_required_source_truth(failures: list[str]) -> None:
    ai_plan = _read(AI_EDITION_PLAN)
    branch_plan = _read(FAM007_BRANCH_PLAN)
    branch_record = _read(FAM007_BRANCH_RECORD)
    registry = _read(VALIDATION_REGISTRY)
    helper = _read(REVIEW_BUNDLE_HELPER)
    for phrase in REQUIRED_AI_PLAN_PHRASES:
        _require(phrase in ai_plan, failures, f"{AI_EDITION_PLAN}: missing {phrase!r}")
    for phrase in REQUIRED_BRANCH_PLAN_PHRASES:
        _require(phrase in branch_plan, failures, f"{FAM007_BRANCH_PLAN}: missing {phrase!r}")
    for phrase in REQUIRED_RECORD_PHRASES:
        _require(phrase in branch_record, failures, f"{FAM007_BRANCH_RECORD}: missing {phrase!r}")
    for phrase in REQUIRED_REGISTRY_PHRASES:
        _require(phrase in registry, failures, f"{VALIDATION_REGISTRY}: missing {phrase!r}")
    for phrase in (
        "PUBLIC_REVIEW_BUNDLE_LEAK_PREVENTION_STATUS",
        "PRIVATE_REVIEW_BUNDLE_PATH_PATTERNS",
        "_public_review_bundle_file_list_failures",
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
        _require(path and not Path(path).is_absolute(), failures, f"public review bundle path must be relative: {path!r}")
    reasons = _scan_reasons(bundle)
    _require(not reasons, failures, f"public review bundle contains protected patterns: {sorted(reasons)}")


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


def validate() -> list[str]:
    failures: list[str] = []
    _require(FIXTURE_SET.is_file(), failures, f"{FIXTURE_SET.relative_to(ROOT)} is missing")
    if failures:
        return failures
    fixture_set = _load_fixture_set()
    _validate_required_source_truth(failures)
    _validate_public_safe_fixture(fixture_set, failures)
    _validate_public_review_bundle(fixture_set, failures)
    _validate_edition_manifest(fixture_set, failures)
    _validate_public_build_audit(failures=failures, fixture_set=fixture_set)
    _validate_blocked_canaries(fixture_set, failures)
    _validate_provider_boundary(failures)
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
