# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=RRI-20260727-001; surface=current-gate-autonomous-repair; status=shared
"""Compile gate contracts and enforce bounded same-gate repair behavior."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable, Mapping, Sequence


BR1_SECTION_HEADING = "BR1 Candidate Viability / Grouping Matrix"
BR1_MATRIX_ARTIFACT = "BR1_CANDIDATE_VIABILITY_GROUPING_MATRIX.md"
SOURCE_TRUTH_CONTEXT_PREFIX = "Source Truth Context/"


class FindingClass(str, Enum):
    """Exact governed top-level finding classes."""

    SELF_REPAIRABLE_CURRENT_GATE = "SELF_REPAIRABLE_CURRENT_GATE"
    USER_DECISION_REQUIRED = "USER_DECISION_REQUIRED"
    EXTERNAL_SAFETY_BLOCKER = "EXTERNAL_SAFETY_BLOCKER"
    REUSABLE_ENFORCEMENT_GAP = "REUSABLE_ENFORCEMENT_GAP"


class GateContractError(RuntimeError):
    """Raised when a source-owned gate contract cannot be compiled safely."""


class CanonicalPublishError(RuntimeError):
    """Raised when transactional canonical publication fails or rolls back."""


@dataclass(frozen=True)
class GateFinding:
    code: str
    finding_class: FindingClass
    message: str
    artifact: str = ""
    root_cause_owner: str = ""

    @property
    def signature(self) -> str:
        normalized = "|".join(
            (
                self.code.casefold().strip(),
                self.finding_class.value.casefold(),
                self.artifact.replace("\\", "/").casefold().strip(),
                self.root_cause_owner.replace("\\", "/").casefold().strip(),
            )
        )
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:20]


@dataclass(frozen=True)
class ManualContractRow:
    field_name: str
    artifact: str
    status: str
    reason: str


@dataclass(frozen=True)
class CompiledGateContract:
    phase: str
    stage: str
    rule_name: str
    owner_path: Path
    owner_sha256: str
    source_section_sha256: str
    required_artifacts: tuple[str, ...]
    required_fields: tuple[str, ...]
    conditional_fields: tuple[str, ...]
    allowed_route_classes: tuple[str, ...]
    manual_review_fields: tuple[str, ...]
    invalid_candidate_shapes: tuple[str, ...]
    blocking_conditions: tuple[str, ...]


@dataclass(frozen=True)
class PacketContractValidation:
    contract: CompiledGateContract
    applies: bool
    findings: tuple[GateFinding, ...]
    manual_rows: tuple[ManualContractRow, ...]

    @property
    def is_machine_green(self) -> bool:
        return not self.findings


@dataclass(frozen=True)
class GateBoundary:
    candidate: str
    scope_fingerprint: str
    owner: str
    worktree: str
    branch: str
    phase: str
    stage: str
    selected_next: str

    def changed_axes(self, other: "GateBoundary") -> tuple[str, ...]:
        return tuple(
            name
            for name in (
                "candidate",
                "scope_fingerprint",
                "owner",
                "worktree",
                "branch",
                "phase",
                "stage",
                "selected_next",
            )
            if getattr(self, name) != getattr(other, name)
        )


@dataclass(frozen=True)
class LatchDisposition:
    action: str
    signature: str
    occurrence: int
    may_return: bool
    root_cause_repair_required: bool


@dataclass
class InternalRepairContinuationLatch:
    """Keep deterministic same-gate repair active until closure or a real stop."""

    occurrences: dict[str, int] = field(default_factory=dict)
    unresolved: dict[str, GateFinding] = field(default_factory=dict)
    root_cause_repaired: set[str] = field(default_factory=set)

    def observe(self, finding: GateFinding) -> LatchDisposition:
        signature = finding.signature
        occurrence = self.occurrences.get(signature, 0) + 1
        self.occurrences[signature] = occurrence
        self.unresolved[signature] = finding

        if finding.finding_class == FindingClass.SELF_REPAIRABLE_CURRENT_GATE:
            repeated = occurrence > 1
            return LatchDisposition(
                action=(
                    "REPAIR_ROOT_CAUSE_AND_CONTINUE"
                    if repeated
                    else "REPAIR_DRAFT_AND_CONTINUE"
                ),
                signature=signature,
                occurrence=occurrence,
                may_return=False,
                root_cause_repair_required=repeated,
            )
        if finding.finding_class == FindingClass.REUSABLE_ENFORCEMENT_GAP:
            return LatchDisposition(
                action="RECORD_NON_BLOCKING_GOVERNANCE_HANDOFF",
                signature=signature,
                occurrence=occurrence,
                may_return=True,
                root_cause_repair_required=False,
            )
        if finding.finding_class == FindingClass.USER_DECISION_REQUIRED:
            return LatchDisposition(
                action="CONSOLIDATE_USER_DECISIONS_AND_STOP",
                signature=signature,
                occurrence=occurrence,
                may_return=True,
                root_cause_repair_required=False,
            )
        return LatchDisposition(
            action="STOP_WITH_EXTERNAL_SAFETY_BLOCKER",
            signature=signature,
            occurrence=occurrence,
            may_return=True,
            root_cause_repair_required=False,
        )

    def resolve(self, finding: GateFinding, *, root_cause_repaired: bool = False) -> None:
        signature = finding.signature
        if self.occurrences.get(signature, 0) > 1 and not root_cause_repaired:
            raise GateContractError(
                "Repeated defect signature requires generator/schema/helper/validator "
                f"root-cause repair before closure: {signature}"
            )
        if root_cause_repaired:
            self.root_cause_repaired.add(signature)
        self.unresolved.pop(signature, None)

    def assert_green_return_allowed(self) -> None:
        blocking = [
            finding
            for finding in self.unresolved.values()
            if finding.finding_class
            in {
                FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                FindingClass.USER_DECISION_REQUIRED,
                FindingClass.EXTERNAL_SAFETY_BLOCKER,
            }
        ]
        if blocking:
            classes = ", ".join(sorted({item.finding_class.value for item in blocking}))
            raise GateContractError(
                "Final digest blocked while current-gate findings remain unresolved: "
                + classes
            )


@dataclass(frozen=True)
class CanonicalPublishResult:
    canonical_folder: Path
    canonical_zip: Path
    superseded_count: int
    rollback_performed: bool


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def _extract_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|\Z)"
    )
    match = pattern.search(text)
    if not match:
        raise GateContractError(f"Gate contract owner is missing section: {heading}")
    return match.group(1)


def _line_value(section: str, marker: str) -> str:
    match = re.search(rf"(?mi)^{re.escape(marker)}\s*(.+)$", section)
    if not match:
        raise GateContractError(f"Gate contract section is missing marker: {marker}")
    return match.group(1).strip()


def _backtick_values(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in re.findall(r"`([^`]+)`", value) if item.strip())


def _comma_values(value: str) -> tuple[str, ...]:
    normalized = re.sub(r"\s+and\s+", ", ", value.strip().rstrip("."), flags=re.I)
    return tuple(item.strip() for item in normalized.split(",") if item.strip())


def compile_br1_stage1_contract(
    owner_path: str | Path,
    *,
    expected_owner_sha256: str | None = None,
) -> CompiledGateContract:
    """Compile the live BR1 Stage 1 contract directly from its source owner."""

    owner = Path(owner_path).resolve()
    owner_bytes = owner.read_bytes()
    owner_sha256 = _sha256_bytes(owner_bytes)
    if expected_owner_sha256 and owner_sha256 != expected_owner_sha256.upper():
        raise GateContractError(
            "Compiled gate contract is stale after source-owner change: "
            f"expected {expected_owner_sha256.upper()} actual {owner_sha256}"
        )
    text = owner_bytes.decode("utf-8")
    section = _extract_section(text, BR1_SECTION_HEADING)
    required_fields = _backtick_values(_line_value(section, "Required Matrix Fields:"))
    allowed_route_classes = _backtick_values(
        _line_value(section, "Allowed Implementation-Bearing Route Classes:")
    )
    invalid_shapes = _comma_values(_line_value(section, "Invalid Candidate Shapes:"))
    blocking_conditions = _backtick_values(_line_value(section, "Blocking Conditions:"))
    if not required_fields or not allowed_route_classes:
        raise GateContractError("Compiled BR1 contract has empty fields or enum values")
    conditional_fields = tuple(
        item for item in required_fields if "when applicable" in item.casefold()
    )
    manual_review_fields = tuple(
        item
        for item in required_fields
        if item.casefold() != "implementation-bearing route class"
    )
    return CompiledGateContract(
        phase="Branch Readiness",
        stage="Stage 1",
        rule_name=BR1_SECTION_HEADING,
        owner_path=owner,
        owner_sha256=owner_sha256,
        source_section_sha256=_sha256_bytes(section.encode("utf-8")),
        required_artifacts=(BR1_MATRIX_ARTIFACT,),
        required_fields=required_fields,
        conditional_fields=conditional_fields,
        allowed_route_classes=allowed_route_classes,
        manual_review_fields=manual_review_fields,
        invalid_candidate_shapes=invalid_shapes,
        blocking_conditions=blocking_conditions,
    )


def _packet_basename(path: str) -> str:
    return PurePosixPath(path.replace("\\", "/")).name


def _active_packet_files(packet_files: Mapping[str, str]) -> dict[str, str]:
    return {
        name.replace("\\", "/"): text
        for name, text in packet_files.items()
        if not name.replace("\\", "/").startswith(SOURCE_TRUTH_CONTEXT_PREFIX)
    }


def _is_br1_stage1_packet(packet_files: Mapping[str, str]) -> bool:
    active = _active_packet_files(packet_files)
    if any(_packet_basename(name) == BR1_MATRIX_ARTIFACT for name in active):
        return True
    combined = "\n".join(active.values()).casefold()
    return (
        "branch readiness stage 1" in combined
        and (
            "candidate viability" in combined
            or "implementation-bearing route class" in combined
        )
    )


def _normalize_field_name(value: str) -> str:
    value = value.strip().strip("`*_ ")
    value = re.sub(r"\s+", " ", value)
    return value.casefold()


def _field_values(text: str) -> dict[str, list[str]]:
    fields: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*(?:[-*]\s+)?([^|:#][^:]{1,120}):\s*(.*?)\s*$", line)
        if not match:
            continue
        name = _normalize_field_name(match.group(1))
        value = match.group(2).strip().strip("`*_ ")
        fields.setdefault(name, []).append(value)
    return fields


def _is_placeholder(value: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()
    return normalized in {
        "",
        "tbd",
        "todo",
        "pending",
        "unknown",
        "not set",
        "fill in",
        "placeholder",
    }


def _candidate_matrix_fields(text: str) -> list[tuple[str, dict[str, list[str]]]]:
    lines = text.splitlines()
    candidate_starts: list[int] = []
    for index, line in enumerate(lines):
        match = re.match(r"^\s*(?:[-*]\s+)?([^|:#][^:]{1,120}):\s*(.*?)\s*$", line)
        if match and _normalize_field_name(match.group(1)) == "option name":
            candidate_starts.append(index)
    if not candidate_starts:
        return [("candidate 1", _field_values(text))]

    candidates: list[tuple[str, dict[str, list[str]]]] = []
    for candidate_index, start in enumerate(candidate_starts):
        end = (
            candidate_starts[candidate_index + 1]
            if candidate_index + 1 < len(candidate_starts)
            else len(lines)
        )
        fields = _field_values("\n".join(lines[start:end]))
        option_values = fields.get("option name", [])
        option_name = next(
            (value for value in option_values if not _is_placeholder(value)),
            f"candidate {candidate_index + 1}",
        )
        candidates.append((option_name, fields))
    return candidates


def validate_br1_stage1_packet(
    packet_files: Mapping[str, str],
    contract: CompiledGateContract,
) -> PacketContractValidation:
    """Validate BR1 artifacts and exact route-class values before publication."""

    if not _is_br1_stage1_packet(packet_files):
        return PacketContractValidation(contract, False, (), ())

    active = _active_packet_files(packet_files)
    findings: list[GateFinding] = []
    matrix_items = [
        (name, text)
        for name, text in active.items()
        if _packet_basename(name) == BR1_MATRIX_ARTIFACT
    ]
    if not matrix_items:
        findings.append(
            GateFinding(
                code="BR1_REQUIRED_ARTIFACT_MISSING",
                finding_class=FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                message=f"Required BR1 artifact is missing: {BR1_MATRIX_ARTIFACT}",
                artifact=BR1_MATRIX_ARTIFACT,
                root_cause_owner="dev/orin_user_review_bundle.py",
            )
        )
        return PacketContractValidation(contract, True, tuple(findings), ())
    if len(matrix_items) > 1:
        findings.append(
            GateFinding(
                code="BR1_REQUIRED_ARTIFACT_DUPLICATE",
                finding_class=FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                message=f"BR1 packet contains {len(matrix_items)} matrix artifacts; expected one",
                artifact=BR1_MATRIX_ARTIFACT,
                root_cause_owner="dev/orin_user_review_bundle.py",
            )
        )

    matrix_name, matrix_text = matrix_items[0]
    matrix_candidates = _candidate_matrix_fields(matrix_text)
    manual_rows: list[ManualContractRow] = []
    candidate_route_fields: list[tuple[str, str, str]] = []
    for option_name, candidate_fields in matrix_candidates:
        for required_field in contract.required_fields:
            normalized = _normalize_field_name(required_field)
            values = candidate_fields.get(normalized, [])
            if not values or all(_is_placeholder(value) for value in values):
                findings.append(
                    GateFinding(
                        code="BR1_REQUIRED_FIELD_MISSING",
                        finding_class=FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                        message=(
                            f"Required BR1 matrix field is missing or placeholder for "
                            f"{option_name!r}: {required_field}"
                        ),
                        artifact=matrix_name,
                        root_cause_owner="dev/orin_user_review_bundle.py",
                    )
                )
                continue
            if required_field in contract.manual_review_fields:
                manual_rows.append(
                    ManualContractRow(
                        field_name=required_field,
                        artifact=matrix_name,
                        status="PRESENT_MANUAL_REVIEW_REQUIRED",
                        reason=(
                            f"{option_name}: presence is machine-checked; substantive truth "
                            "remains a Codex/USER review row."
                        ),
                    )
                )
        candidate_route_fields.extend(
            (matrix_name, option_name, value)
            for value in candidate_fields.get("implementation-bearing route class", [])
        )

    route_fields: list[tuple[str, str, str]] = list(candidate_route_fields)
    for name, text in active.items():
        if name == matrix_name:
            continue
        fields = _field_values(text)
        route_fields.extend(
            (name, _packet_basename(name), value)
            for value in fields.get("implementation-bearing route class", [])
        )
    if not route_fields:
        findings.append(
            GateFinding(
                code="BR1_ROUTE_CLASS_MISSING",
                finding_class=FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                message="No active BR1 artifact contains Implementation-bearing route class",
                artifact=matrix_name,
                root_cause_owner="dev/orin_user_review_bundle.py",
            )
        )
    for name, option_name, value in route_fields:
        if value not in contract.allowed_route_classes:
            findings.append(
                GateFinding(
                    code="BR1_ROUTE_CLASS_ENUM_INVALID",
                    finding_class=FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                    message=(
                        f"Implementation-bearing route class {value!r} for {option_name!r} is not one of "
                        + ", ".join(contract.allowed_route_classes)
                    ),
                    artifact=name,
                    root_cause_owner="dev/orin_user_review_bundle.py",
                )
            )

    return PacketContractValidation(
        contract=contract,
        applies=True,
        findings=tuple(findings),
        manual_rows=tuple(manual_rows),
    )


def classify_boundary_transition(
    before: GateBoundary,
    after: GateBoundary,
) -> FindingClass:
    """Classify whether a proposed repair remains within the approved gate."""

    if not before.changed_axes(after):
        return FindingClass.SELF_REPAIRABLE_CURRENT_GATE
    return FindingClass.USER_DECISION_REQUIRED


def consolidate_user_decisions(findings: Iterable[GateFinding]) -> tuple[GateFinding, ...]:
    """Return all unique material USER decisions in one deterministic packet order."""

    unique: dict[str, GateFinding] = {}
    for finding in findings:
        if finding.finding_class == FindingClass.USER_DECISION_REQUIRED:
            unique.setdefault(finding.signature, finding)
    return tuple(sorted(unique.values(), key=lambda item: (item.code, item.artifact, item.message)))


def _remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


class CanonicalPacketPublisher:
    """Publish one folder/ZIP pair only after draft validation, with rollback."""

    def __init__(self, canonical_root: str | Path) -> None:
        self.canonical_root = Path(canonical_root).resolve()

    def _inside_root(self, path: Path) -> bool:
        resolved = path.resolve()
        return resolved == self.canonical_root or self.canonical_root in resolved.parents

    def publish(
        self,
        *,
        draft_folder: str | Path,
        draft_zip: str | Path,
        canonical_folder: str | Path,
        canonical_zip: str | Path,
        superseded_paths: Sequence[str | Path] = (),
        validate_draft: Callable[[], None],
        validate_final: Callable[[], None],
    ) -> CanonicalPublishResult:
        draft_folder_path = Path(draft_folder).resolve()
        draft_zip_path = Path(draft_zip).resolve()
        canonical_folder_path = Path(canonical_folder).resolve()
        canonical_zip_path = Path(canonical_zip).resolve()
        for path in (canonical_folder_path, canonical_zip_path):
            if not self._inside_root(path):
                raise CanonicalPublishError(f"Canonical publish target escapes root: {path}")
        if not draft_folder_path.is_dir() or not draft_zip_path.is_file():
            raise CanonicalPublishError("Canonical publish draft folder/ZIP pair is incomplete")

        validate_draft()
        self.canonical_root.mkdir(parents=True, exist_ok=True)
        candidates = [canonical_folder_path, canonical_zip_path]
        candidates.extend(Path(path).resolve() for path in superseded_paths)
        unique_candidates: list[Path] = []
        for candidate in candidates:
            if candidate in unique_candidates:
                continue
            if not self._inside_root(candidate):
                raise CanonicalPublishError(
                    f"Superseded canonical path escapes root: {candidate}"
                )
            unique_candidates.append(candidate)

        transaction_root = self.canonical_root / (
            f".canonical-publish-{os.getpid()}-{uuid.uuid4().hex}"
        )
        transaction_root.mkdir(parents=False, exist_ok=False)
        backups: list[tuple[Path, Path]] = []
        published: list[Path] = []
        rollback_performed = False

        try:
            for index, candidate in enumerate(unique_candidates):
                if not candidate.exists():
                    continue
                backup = transaction_root / f"{index:04d}-{candidate.name}"
                shutil.move(str(candidate), str(backup))
                backups.append((candidate, backup))

            shutil.move(str(draft_folder_path), str(canonical_folder_path))
            published.append(canonical_folder_path)
            shutil.move(str(draft_zip_path), str(canonical_zip_path))
            published.append(canonical_zip_path)
            validate_final()
        except Exception as exc:
            rollback_performed = True
            for path in reversed(published):
                _remove_path(path)
            for original, backup in reversed(backups):
                if backup.exists():
                    shutil.move(str(backup), str(original))
            _remove_path(transaction_root)
            raise CanonicalPublishError(
                f"Canonical publication failed and rollback was attempted: {exc}"
            ) from exc

        superseded_count = len(backups)
        _remove_path(transaction_root)
        return CanonicalPublishResult(
            canonical_folder=canonical_folder_path,
            canonical_zip=canonical_zip_path,
            superseded_count=superseded_count,
            rollback_performed=rollback_performed,
        )
