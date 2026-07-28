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

from orin_external_state_common import atomic_write_json, load_json
from orin_external_state_lock_lifecycle import process_is_running


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
    defect_key: str = ""

    @property
    def signature(self) -> str:
        discriminator = self.defect_key
        if not discriminator and self.finding_class == FindingClass.USER_DECISION_REQUIRED:
            discriminator = self.message
        normalized = "|".join(
            (
                self.code.casefold().strip(),
                self.finding_class.value.casefold(),
                self.artifact.replace("\\", "/").casefold().strip(),
                self.root_cause_owner.replace("\\", "/").casefold().strip(),
                discriminator.casefold().strip(),
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
    for text in active.values():
        if re.search(
            r"(?im)^\s{0,3}#{1,6}\s+branch readiness stage 1\b",
            text,
        ):
            return True
        fields = _field_values(text)
        direct_gate_values = [
            value
            for name in (
                "current gate",
                "current phase",
                "decision phase",
                "review phase",
            )
            for value in fields.get(name, [])
        ]
        if any(
            re.match(r"(?i)^branch readiness stage 1\b", value)
            for value in direct_gate_values
        ):
            return True
        phase_values = fields.get("phase", []) + fields.get("current phase", [])
        stage_values = fields.get("stage", []) + fields.get("current stage", [])
        if any(value.casefold() == "branch readiness" for value in phase_values) and any(
            re.match(r"(?i)^stage 1\b", value) for value in stage_values
        ):
            return True
    return False


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


def _candidate_matrix_fields(
    text: str,
    candidate_field_names: set[str],
) -> list[tuple[str, str, dict[str, list[str]]]]:
    lines = text.splitlines()
    candidate_starts: list[int] = []
    for index, line in enumerate(lines):
        match = re.match(r"^\s*(?:[-*]\s+)?([^|:#][^:]{1,120}):\s*(.*?)\s*$", line)
        if match and _normalize_field_name(match.group(1)) == "option name":
            candidate_starts.append(index)
    if not candidate_starts:
        return [("candidate 1", "candidate 1", _field_values(text))]

    candidates: list[tuple[str, str, dict[str, list[str]]]] = []
    prefix_fields = _field_values("\n".join(lines[: candidate_starts[0]]))
    if any(name in candidate_field_names for name in prefix_fields):
        candidates.append(("candidate 1", "candidate 1", prefix_fields))

    candidate_offset = len(candidates)
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
            f"candidate {candidate_index + candidate_offset + 1}",
        )
        candidate_key = f"candidate {candidate_index + candidate_offset + 1}"
        candidates.append((candidate_key, option_name, fields))
    return candidates


CONDITIONAL_FIELD_APPLICABILITY_TERMS = {
    "platform contract adoption matrix when applicable": "platform contract",
    "repo-wide migration neutralization proof when applicable": "repo-wide migration",
}


def _affirmatively_mentions(values: list[str], term: str) -> bool:
    for value in values:
        for clause in re.split(r"[.;\n]+", value.casefold()):
            if term not in clause:
                continue
            prefix = clause.split(term, 1)[0]
            if re.search(r"\b(?:no|not|without)\b(?:\s+\w+){0,4}\s*$", prefix):
                continue
            suffix = clause.split(term, 1)[1]
            if re.match(r"^\s*(?:\w+\s+){0,4}(?:no|not|without)\b", suffix):
                continue
            return True
    return False


def _conditional_field_applies(
    required_field: str,
    candidate_fields: Mapping[str, list[str]],
) -> bool:
    normalized_field = _normalize_field_name(required_field)
    term = CONDITIONAL_FIELD_APPLICABILITY_TERMS.get(normalized_field)
    if term is None:
        return False
    conditional_names = set(CONDITIONAL_FIELD_APPLICABILITY_TERMS)
    evidence_values = [
        value
        for field_name, values in candidate_fields.items()
        if field_name not in conditional_names
        for value in values
    ]
    return _affirmatively_mentions(evidence_values, term)


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
                defect_key=BR1_MATRIX_ARTIFACT,
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
                defect_key="duplicate-matrix-artifact",
            )
        )

    matrix_name, matrix_text = matrix_items[0]
    matrix_candidates = _candidate_matrix_fields(
        matrix_text,
        {_normalize_field_name(field) for field in contract.required_fields},
    )
    manual_rows: list[ManualContractRow] = []
    candidate_route_fields: list[tuple[str, str, str, str]] = []
    for candidate_key, option_name, candidate_fields in matrix_candidates:
        for required_field in contract.required_fields:
            if (
                required_field in contract.conditional_fields
                and not _conditional_field_applies(required_field, candidate_fields)
            ):
                continue
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
                        defect_key=f"{candidate_key}|{required_field}",
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
        candidate_route_values = candidate_fields.get(
            "implementation-bearing route class",
            [],
        )
        if len(candidate_route_values) > 1:
            findings.append(
                GateFinding(
                    code="BR1_ROUTE_CLASS_DUPLICATE",
                    finding_class=FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                    message=(
                        f"BR1 candidate {option_name!r} contains "
                        f"{len(candidate_route_values)} route-class values; expected exactly one"
                    ),
                    artifact=matrix_name,
                    root_cause_owner="dev/orin_user_review_bundle.py",
                    defect_key=f"{candidate_key}|implementation-bearing route class",
                )
            )
        candidate_route_fields.extend(
            (matrix_name, candidate_key, option_name, value)
            for value in candidate_route_values
        )

    route_fields: list[tuple[str, str, str, str]] = list(candidate_route_fields)
    for name, text in active.items():
        if name == matrix_name:
            continue
        fields = _field_values(text)
        artifact_route_values = fields.get("implementation-bearing route class", [])
        if len(artifact_route_values) > 1:
            findings.append(
                GateFinding(
                    code="BR1_ROUTE_CLASS_DUPLICATE",
                    finding_class=FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                    message=(
                        f"Active BR1 artifact {name!r} contains "
                        f"{len(artifact_route_values)} route-class values; expected one"
                    ),
                    artifact=name,
                    root_cause_owner="dev/orin_user_review_bundle.py",
                    defect_key="implementation-bearing route class",
                )
            )
        route_fields.extend(
            (name, _packet_basename(name), _packet_basename(name), value)
            for value in artifact_route_values
        )
    if not route_fields:
        findings.append(
            GateFinding(
                code="BR1_ROUTE_CLASS_MISSING",
                finding_class=FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
                message="No active BR1 artifact contains Implementation-bearing route class",
                artifact=matrix_name,
                root_cause_owner="dev/orin_user_review_bundle.py",
                defect_key="implementation-bearing route class",
            )
        )
    for name, candidate_key, option_name, value in route_fields:
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
                    defect_key=f"{candidate_key}|implementation-bearing route class",
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
    """Publish one folder/ZIP pair after draft validation with durable recovery."""

    TRANSACTION_PREFIX = ".canonical-publish-"
    TRANSACTION_MANIFEST = "transaction.json"

    def __init__(
        self,
        canonical_root: str | Path,
        *,
        process_checker: Callable[[int], bool | None] = process_is_running,
        after_move: Callable[[str, Path, Path], None] | None = None,
    ) -> None:
        self.canonical_root = Path(canonical_root).resolve()
        self.process_checker = process_checker
        self.after_move = after_move or (lambda _stage, _source, _destination: None)

    def _inside_root(self, path: Path) -> bool:
        resolved = path.resolve()
        return resolved == self.canonical_root or self.canonical_root in resolved.parents

    def _relative_canonical_path(self, path: Path) -> str:
        if not self._inside_root(path):
            raise CanonicalPublishError(f"Canonical transaction path escapes root: {path}")
        return path.resolve().relative_to(self.canonical_root).as_posix()

    def _resolve_manifest_path(self, raw: object, *, base: Path, label: str) -> Path:
        relative = PurePosixPath(str(raw))
        if relative.is_absolute() or not relative.parts or any(
            part in {"", ".", ".."} for part in relative.parts
        ):
            raise CanonicalPublishError(f"Canonical transaction {label} is invalid: {raw!r}")
        candidate = base.joinpath(*relative.parts).resolve()
        if candidate != base and base not in candidate.parents:
            raise CanonicalPublishError(f"Canonical transaction {label} escapes its root: {raw!r}")
        return candidate

    def _owner_is_inactive(self, owner_process_id: object) -> bool:
        if not isinstance(owner_process_id, int) or owner_process_id <= 0:
            raise CanonicalPublishError("Canonical transaction owner process identity is invalid")
        running = self.process_checker(owner_process_id)
        if running is not False:
            state = "active" if running else "unknown"
            raise CanonicalPublishError(
                f"Canonical transaction owner process is still {state}: {owner_process_id}"
            )
        return True

    def _recover_transaction(
        self,
        transaction_root: Path,
        *,
        ignore_owner: bool = False,
    ) -> None:
        manifest_path = transaction_root / self.TRANSACTION_MANIFEST
        if not manifest_path.is_file():
            match = re.fullmatch(r"\.canonical-publish-(\d+)-[0-9a-f]+", transaction_root.name)
            if not match:
                raise CanonicalPublishError(
                    f"Unrecognized canonical transaction directory: {transaction_root}"
                )
            if not ignore_owner:
                self._owner_is_inactive(int(match.group(1)))
            # No canonical move occurs until the manifest write returns. A dead
            # owner with no manifest can therefore leave only setup residue.
            residue = list(transaction_root.iterdir())
            if any(
                not re.fullmatch(r"\.transaction\.json\..+\.tmp", item.name)
                for item in residue
            ):
                raise CanonicalPublishError(
                    f"Manifest-free canonical transaction contains unknown residue: {transaction_root}"
                )
            _remove_path(transaction_root)
            return

        try:
            manifest = load_json(manifest_path)
        except Exception as exc:
            raise CanonicalPublishError(
                f"Canonical transaction recovery manifest is unreadable: {manifest_path}: {exc}"
            ) from exc
        if not ignore_owner:
            self._owner_is_inactive(manifest.get("Owner Process ID"))
        directory_match = re.fullmatch(
            r"\.canonical-publish-(\d+)-[0-9a-f]+",
            transaction_root.name,
        )
        if not directory_match or manifest.get("Owner Process ID") != int(
            directory_match.group(1)
        ):
            raise CanonicalPublishError(
                "Canonical transaction directory and manifest owner identities differ"
            )
        if manifest.get("Transaction Version") != 1:
            raise CanonicalPublishError("Canonical transaction recovery version is unsupported")
        state = manifest.get("Transaction State")
        rows = manifest.get("Candidates")
        if state not in {"Prepared", "Committed"} or not isinstance(rows, list) or not rows:
            raise CanonicalPublishError("Canonical transaction recovery manifest is malformed")

        recovered_rows: list[tuple[Path, Path, bool]] = []
        original_paths: set[Path] = set()
        backup_paths: set[Path] = set()
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("Had Original"), bool):
                raise CanonicalPublishError("Canonical transaction candidate row is malformed")
            original = self._resolve_manifest_path(
                row.get("Original"),
                base=self.canonical_root,
                label="original path",
            )
            backup = self._resolve_manifest_path(
                row.get("Backup"),
                base=transaction_root,
                label="backup path",
            )
            if original in original_paths or backup in backup_paths:
                raise CanonicalPublishError(
                    "Canonical transaction candidate rows contain duplicate paths"
                )
            original_paths.add(original)
            backup_paths.add(backup)
            recovered_rows.append((original, backup, row["Had Original"]))

        if state == "Committed":
            for key in ("Canonical Folder", "Canonical ZIP"):
                published = self._resolve_manifest_path(
                    manifest.get(key),
                    base=self.canonical_root,
                    label=key.casefold(),
                )
                if not published.exists():
                    raise CanonicalPublishError(
                        f"Committed canonical transaction is missing {key}: {published}"
                    )
            _remove_path(transaction_root)
            return

        for original, backup, had_original in reversed(recovered_rows):
            if backup.exists():
                _remove_path(original)
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(backup), str(original))
            elif had_original and not original.exists():
                raise CanonicalPublishError(
                    f"Prepared canonical transaction lost original and backup: {original}"
                )
            elif not had_original:
                _remove_path(original)
        _remove_path(transaction_root)

    def _recover_orphaned_transactions(self) -> None:
        transactions = sorted(
            path
            for path in self.canonical_root.glob(f"{self.TRANSACTION_PREFIX}*")
            if path.is_dir()
        )
        if len(transactions) > 1:
            raise CanonicalPublishError(
                "Multiple canonical transactions make recovery order ambiguous: "
                + ", ".join(str(path) for path in transactions)
            )
        for transaction_root in transactions:
            if transaction_root.is_symlink() or not self._inside_root(transaction_root):
                raise CanonicalPublishError(
                    f"Canonical transaction directory escapes root: {transaction_root}"
                )
            self._recover_transaction(transaction_root)

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
        self.canonical_root.mkdir(parents=True, exist_ok=True)
        self._recover_orphaned_transactions()
        if not draft_folder_path.is_dir() or not draft_zip_path.is_file():
            raise CanonicalPublishError("Canonical publish draft folder/ZIP pair is incomplete")

        validate_draft()
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
        competing_transactions = [
            path
            for path in self.canonical_root.glob(f"{self.TRANSACTION_PREFIX}*")
            if path.is_dir() and path != transaction_root
        ]
        if competing_transactions:
            _remove_path(transaction_root)
            raise CanonicalPublishError(
                "Concurrent canonical publication transaction detected: "
                + ", ".join(str(path) for path in competing_transactions)
            )
        candidate_rows = [
            {
                "Original": self._relative_canonical_path(candidate),
                "Backup": f"backups/{index:04d}-{candidate.name}",
                "Had Original": candidate.exists(),
            }
            for index, candidate in enumerate(unique_candidates)
        ]
        manifest = {
            "Transaction Version": 1,
            "Transaction State": "Prepared",
            "Owner Process ID": os.getpid(),
            "Canonical Folder": self._relative_canonical_path(canonical_folder_path),
            "Canonical ZIP": self._relative_canonical_path(canonical_zip_path),
            "Candidates": candidate_rows,
        }
        atomic_write_json(transaction_root / self.TRANSACTION_MANIFEST, manifest)
        (transaction_root / "backups").mkdir(parents=False, exist_ok=False)

        try:
            for candidate, row in zip(unique_candidates, candidate_rows, strict=True):
                if not row["Had Original"]:
                    continue
                backup = transaction_root.joinpath(*PurePosixPath(row["Backup"]).parts)
                shutil.move(str(candidate), str(backup))
                self.after_move("backup", candidate, backup)

            shutil.move(str(draft_folder_path), str(canonical_folder_path))
            self.after_move("publish", draft_folder_path, canonical_folder_path)
            shutil.move(str(draft_zip_path), str(canonical_zip_path))
            self.after_move("publish", draft_zip_path, canonical_zip_path)
            validate_final()
            manifest["Transaction State"] = "Committed"
            atomic_write_json(transaction_root / self.TRANSACTION_MANIFEST, manifest)
            self.after_move(
                "commit",
                transaction_root / self.TRANSACTION_MANIFEST,
                transaction_root,
            )
        except Exception as exc:
            recovery_error = ""
            try:
                self._recover_transaction(transaction_root, ignore_owner=True)
            except Exception as recovery_exc:  # noqa: BLE001 - report both publication failures
                recovery_error = f"; durable recovery failed: {recovery_exc}"
            raise CanonicalPublishError(
                f"Canonical publication failed and rollback was attempted: {exc}{recovery_error}"
            ) from exc

        superseded_count = sum(bool(row["Had Original"]) for row in candidate_rows)
        _remove_path(transaction_root)
        return CanonicalPublishResult(
            canonical_folder=canonical_folder_path,
            canonical_zip=canonical_zip_path,
            superseded_count=superseded_count,
            rollback_performed=False,
        )
