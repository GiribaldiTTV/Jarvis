from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Callable

import orin_external_state_validation as validation


RECEIPT_NAMES = ("legacy-one.json", "legacy-two.json", "legacy-three.json")


def _json_bytes(payload: object) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _receipt_payload(index: int) -> dict[str, object]:
    return {
        "External State Schema": "external-state-v1",
        "Last Updated": f"2026-07-2{index}T00:00:00+00:00",
        "Last Updated By": "Fixture",
        "Lock ID": f"fixture-lock-{index}",
        "Snapshot": f"snapshots/fixture-{index}",
        "Targets": [
            {
                "Target": f"branches/fixture-{index}/branch_state.md",
                "Before SHA256": "A" * 64,
                "After SHA256": "B" * 64,
            }
        ],
        "Transition": validation.LEGACY_AUDIT_TRANSITION,
        "Workload ID": f"fixture-workload-{index}",
    }


def _registry_payload(receipt_bytes: list[bytes]) -> dict[str, object]:
    return {
        "schema": validation.LEGACY_AUDIT_COMPATIBILITY_SCHEMA,
        "compatibilityClass": validation.LEGACY_AUDIT_COMPATIBILITY_CLASS,
        "externalStateSchema": "external-state-v1",
        "transition": validation.LEGACY_AUDIT_TRANSITION,
        "receipts": [
            {
                "path": f"audit_log/{name}",
                "sha256": hashlib.sha256(raw).hexdigest().upper(),
                "profile": f"fixture-profile-{index}",
            }
            for index, (name, raw) in enumerate(zip(RECEIPT_NAMES, receipt_bytes, strict=True), start=1)
        ],
    }


def _write_baseline(root: Path) -> tuple[Path, str]:
    audit_root = root / "audit_log"
    audit_root.mkdir(parents=True)
    receipts = [_json_bytes(_receipt_payload(index)) for index in range(1, 4)]
    for name, raw in zip(RECEIPT_NAMES, receipts, strict=True):
        (audit_root / name).write_bytes(raw)
    registry_path = root / "registry.json"
    registry_path.write_bytes(_json_bytes(_registry_payload(receipts)))
    return registry_path, hashlib.sha256(registry_path.read_bytes()).hexdigest().upper()


def _rewrite_registry(
    registry_path: Path,
    mutate: Callable[[dict[str, object]], None],
) -> str:
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    mutate(payload)
    registry_path.write_bytes(_json_bytes(payload))
    return hashlib.sha256(registry_path.read_bytes()).hexdigest().upper()


def _rewrite_receipt(
    root: Path,
    registry_path: Path,
    index: int,
    mutate: Callable[[dict[str, object]], None],
) -> str:
    path = root / "audit_log" / RECEIPT_NAMES[index]
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutate(payload)
    path.write_bytes(_json_bytes(payload))

    def update_hash(registry: dict[str, object]) -> None:
        rows = registry["receipts"]
        assert isinstance(rows, list) and isinstance(rows[index], dict)
        rows[index]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest().upper()

    return _rewrite_registry(registry_path, update_hash)


def _validate(root: Path, registry_path: Path, expected_sha: str) -> list[str]:
    return validation.validate_legacy_audit_compatibility(root, registry_path, expected_sha)


def _expect_failure(
    label: str,
    mutate: Callable[[Path, Path, str], str | None],
    expected_fragment: str,
) -> None:
    with tempfile.TemporaryDirectory(prefix="n0-legacy-negative-") as temp:
        root = Path(temp)
        registry_path, registry_sha = _write_baseline(root)
        replacement_sha = mutate(root, registry_path, registry_sha)
        issues = _validate(root, registry_path, replacement_sha or registry_sha)
        if not any(expected_fragment.casefold() in issue.casefold() for issue in issues):
            raise AssertionError(f"{label}: expected {expected_fragment!r}, found {issues!r}")


def _load_mutant(
    temp_root: Path,
    label: str,
    replacements: tuple[tuple[str, str], ...],
) -> ModuleType:
    source_path = Path(validation.__file__)
    source = source_path.read_text(encoding="utf-8")
    for original, replacement in replacements:
        count = source.count(original)
        if count != 1:
            raise AssertionError(
                f"{label}: mutation anchor must occur exactly once; {original!r} occurred {count} times"
            )
        source = source.replace(original, replacement, 1)
    mutant_path = temp_root / f"mutant-{label}.py"
    mutant_path.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(f"n0_mutant_{label}", mutant_path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"{label}: mutant module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expect_mutant_escape(
    label: str,
    replacements: tuple[tuple[str, str], ...],
    mutate: Callable[[Path, Path, str], str | None],
) -> None:
    with tempfile.TemporaryDirectory(prefix="n0-legacy-mutant-") as temp:
        temp_root = Path(temp)
        state_root = temp_root / "state"
        registry_path, registry_sha = _write_baseline(state_root)
        replacement_sha = mutate(state_root, registry_path, registry_sha)
        expected_sha = replacement_sha or registry_sha
        baseline_issues = _validate(state_root, registry_path, expected_sha)
        if not baseline_issues:
            raise AssertionError(f"{label}: baseline validator did not reject the adversarial input")
        mutant = _load_mutant(temp_root, label, replacements)
        mutant_issues = mutant.validate_legacy_audit_compatibility(
            state_root,
            registry_path,
            expected_sha,
        )
        if mutant_issues:
            raise AssertionError(
                f"{label}: mutant was not killed by the targeted fixture; found {mutant_issues!r}"
            )


def _copy_receipt(root: Path, _registry: Path, _sha: str) -> None:
    source = root / "audit_log" / RECEIPT_NAMES[0]
    (root / "audit_log" / "copied-receipt.json").write_bytes(source.read_bytes())


def _tamper_receipt(root: Path, _registry: Path, _sha: str) -> None:
    path = root / "audit_log" / RECEIPT_NAMES[0]
    path.write_bytes(path.read_bytes().replace(b"Fixture", b"Fixturf", 1))


def _synthetic_receipt(root: Path, _registry: Path, _sha: str) -> None:
    (root / "audit_log" / "synthetic.json").write_bytes(_json_bytes(_receipt_payload(9)))


def _named_receipt(name: str) -> Callable[[Path, Path, str], None]:
    def mutate(root: Path, _registry: Path, _sha: str) -> None:
        (root / "audit_log" / name).write_bytes(_json_bytes(_receipt_payload(8)))

    return mutate


def _nested_receipt(root: Path, _registry: Path, _sha: str) -> None:
    directory = root / "audit_log" / "nested"
    directory.mkdir()
    (directory / "copied-receipt.json").write_bytes(
        (root / "audit_log" / RECEIPT_NAMES[0]).read_bytes()
    )


def _registry_field(
    field: str,
    value: object,
) -> Callable[[Path, Path, str], str]:
    def mutate(_root: Path, registry: Path, _sha: str) -> str:
        return _rewrite_registry(registry, lambda payload: payload.__setitem__(field, value))

    return mutate


def _registry_row_path(value: str) -> Callable[[Path, Path, str], str]:
    def mutate(_root: Path, registry: Path, _sha: str) -> str:
        def update(payload: dict[str, object]) -> None:
            rows = payload["receipts"]
            assert isinstance(rows, list) and isinstance(rows[0], dict)
            rows[0]["path"] = value

        return _rewrite_registry(registry, update)

    return mutate


def _raw_registry_insertion(fragment: bytes) -> Callable[[Path, Path, str], str]:
    def mutate(_root: Path, registry: Path, _sha: str) -> str:
        raw = registry.read_bytes().replace(b"{\n", b"{\n" + fragment, 1)
        registry.write_bytes(raw)
        return hashlib.sha256(raw).hexdigest().upper()

    return mutate


def _raw_receipt(root: Path, registry: Path, raw: bytes) -> str:
    path = root / "audit_log" / RECEIPT_NAMES[0]
    path.write_bytes(raw)

    def update(payload: dict[str, object]) -> None:
        rows = payload["receipts"]
        assert isinstance(rows, list) and isinstance(rows[0], dict)
        rows[0]["sha256"] = hashlib.sha256(raw).hexdigest().upper()

    return _rewrite_registry(registry, update)


def _tamper_registry_identity(_root: Path, registry: Path, original_sha: str) -> str:
    registry.write_bytes(registry.read_bytes() + b"\n")
    return original_sha


def _wrong_profile(_root: Path, registry: Path, original_sha: str) -> str:
    _rewrite_registry(
        registry,
        lambda payload: payload["receipts"][0].__setitem__("profile", "wrong-profile"),
    )
    return original_sha


def _wrong_class(_root: Path, registry: Path, _original_sha: str) -> str:
    return _rewrite_registry(
        registry,
        lambda payload: payload.__setitem__("compatibilityClass", "unapproved-class"),
    )


def _add_fourth_receipt(root: Path, registry: Path, _original_sha: str) -> str:
    raw = _json_bytes(_receipt_payload(4))
    path = root / "audit_log" / "legacy-four.json"
    path.write_bytes(raw)

    def update(payload: dict[str, object]) -> None:
        rows = payload["receipts"]
        assert isinstance(rows, list)
        rows.append(
            {
                "path": "audit_log/legacy-four.json",
                "sha256": hashlib.sha256(raw).hexdigest().upper(),
                "profile": "fixture-profile-4",
            }
        )

    return _rewrite_registry(registry, update)


def _run_positive_matrix() -> int:
    with tempfile.TemporaryDirectory(prefix="n0-legacy-positive-") as temp:
        root = Path(temp)
        registry_path, registry_sha = _write_baseline(root)
        if _validate(root, registry_path, registry_sha):
            raise AssertionError("exact three-receipt baseline failed")
        for name in RECEIPT_NAMES:
            if not (root / "audit_log" / name).is_file():
                raise AssertionError(f"exact registered receipt missing: {name}")
        (root / "audit_log" / "unrelated.json").write_text(
            '{"External State Schema":"external-state-v1","Record Class":"Audit Note"}\n',
            encoding="utf-8",
        )
        (root / "audit_log" / "modern.json").write_text(
            '{"External State Schema":"external-state-v1","Transaction State":"Completed"}\n',
            encoding="utf-8",
        )
        nested = root / "audit_log" / "nested"
        nested.mkdir()
        (nested / "modern.json").write_text(
            '{"External State Schema":"external-state-v1","Transaction State":"Completed"}\n',
            encoding="utf-8",
        )
        if _validate(root, registry_path, registry_sha):
            raise AssertionError("unrelated audit or modern journal changed current-main behavior")
    return 5


def _run_negative_matrix() -> int:
    cases: list[tuple[str, Callable[[Path, Path, str], str | None], str]] = [
        ("copied bytes", _copy_receipt, "unregistered state-less"),
        ("changed byte", _tamper_receipt, "identity mismatch"),
        (
            "another registered hash",
            lambda _r, p, _s: _rewrite_registry(
                p,
                lambda payload: payload["receipts"][0].__setitem__(
                    "sha256", payload["receipts"][1]["sha256"]
                ),
            ),
            "duplicates SHA256",
        ),
        ("wrong class", _registry_field("compatibilityClass", "wrong-class"), "class is invalid"),
        ("wrong profile", _wrong_profile, "registry identity mismatch"),
        ("synthetic old shape", _synthetic_receipt, "unregistered state-less"),
        ("nested copied receipt", _nested_receipt, "unregistered state-less"),
        ("historical filename", _named_receipt("rri-19990101-final.json"), "unregistered state-less"),
        ("modern filename", _named_receipt("transaction-20990101.json"), "unregistered state-less"),
        (
            "fourth entry",
            lambda _r, p, _s: _rewrite_registry(
                p, lambda payload: payload["receipts"].append(copy.deepcopy(payload["receipts"][0]))
            ),
            "exactly three",
        ),
        (
            "duplicate path",
            lambda _r, p, _s: _rewrite_registry(
                p,
                lambda payload: payload["receipts"][1].__setitem__(
                    "path", payload["receipts"][0]["path"]
                ),
            ),
            "duplicates path",
        ),
        ("duplicate registry field", _raw_registry_insertion(b'  "schema": "duplicate",\n'), "duplicate JSON"),
        ("case alias registry field", _raw_registry_insertion(b'  "Schema": "alias",\n'), "case-ambiguous"),
        ("wildcard path", _registry_row_path("audit_log/*.json"), "not exact"),
        ("absolute path", _registry_row_path("C:/outside.json"), "outside audit_log"),
        ("traversal path", _registry_row_path("audit_log/../outside.json"), "not canonical"),
        ("off-root path", _registry_row_path("outside/receipt.json"), "outside audit_log"),
        ("malformed receipt", lambda r, p, _s: _raw_receipt(r, p, b"{\n"), "authoritative audit JSON is invalid"),
        (
            "duplicate receipt keys",
            lambda r, p, _s: _raw_receipt(
                r,
                p,
                _json_bytes(_receipt_payload(1)).replace(
                    b'  "Transition":', b'  "Transition": "duplicate",\n  "Transition":', 1
                ),
            ),
            "duplicate JSON",
        ),
        (
            "case-aliased receipt field",
            lambda r, p, _s: _raw_receipt(
                r,
                p,
                _json_bytes(_receipt_payload(1)).replace(b'"Lock ID"', b'"lock id"', 1),
            ),
            "case-aliased JSON object key",
        ),
        (
            "wrong schema",
            lambda r, p, _s: _rewrite_receipt(
                r,
                p,
                0,
                lambda payload: payload.__setitem__("External State Schema", "v0"),
            ),
            "schema is invalid",
        ),
        (
            "wrong transition",
            lambda r, p, _s: _rewrite_receipt(r, p, 0, lambda payload: payload.__setitem__("Transition", "wrong")),
            "transition is invalid",
        ),
        (
            "added transaction state",
            lambda r, p, _s: _rewrite_receipt(r, p, 0, lambda payload: payload.__setitem__("Transaction State", [])),
            "shape is invalid",
        ),
        (
            "missing legacy field",
            lambda r, p, _s: _rewrite_receipt(r, p, 0, lambda payload: payload.pop("Lock ID")),
            "shape is invalid",
        ),
        (
            "registry identity changed",
            _tamper_registry_identity,
            "registry identity mismatch",
        ),
        (
            "malformed unrelated audit",
            lambda r, _p, _s: (r / "audit_log" / "malformed.json").write_bytes(b"[") and None,
            "authoritative audit JSON is invalid",
        ),
        (
            "non-standard numeric constant",
            lambda r, _p, _s: (
                (r / "audit_log" / "constant.json").write_text(
                    '{"value":NaN}', encoding="utf-8"
                )
                and None
            ),
            "non-standard JSON numeric constant",
        ),
        (
            "non-object audit root",
            lambda r, _p, _s: (r / "audit_log" / "array.json").write_text('[]', encoding="utf-8") and None,
            "JSON root must be an object",
        ),
        (
            "malformed UTF-8",
            lambda r, _p, _s: (r / "audit_log" / "utf8.json").write_bytes(b"\xff") and None,
            "utf-8",
        ),
    ]
    for label, mutate, expected in cases:
        _expect_failure(label, mutate, expected)

    if validation._has_legacy_audit_signature(
        {"Last Updated": "1999-01-01", "Age": "old"}
    ):
        raise AssertionError("age-only evidence was classified as legacy")
    if validation._has_legacy_audit_signature(
        {"Final Disposition": "complete", "Current Validation State": "PASS"}
    ):
        raise AssertionError("completion prose was classified as legacy")
    return len(cases) + 2


def _run_mutation_and_generated_proof() -> tuple[int, int]:
    loader_source = inspect.getsource(validation._read_strict_json_bytes)
    if loader_source.count("path.read_bytes()") != 1:
        raise AssertionError("strict loader must read candidate bytes exactly once")

    path_lookup = "        entry = registry.get(relative)"
    hash_guard = '        if actual_digest != entry["sha256"]:'
    registry_identity_guard = "    if actual_registry_sha != expected_registry_sha256:"
    class_guard = (
        '    if payload.get("compatibilityClass") '
        "!= LEGACY_AUDIT_COMPATIBILITY_CLASS:"
    )
    state_less_guard = "        if entry is None:\n            if legacy_signature:"
    cardinality_guard = "    if not isinstance(rows, list) or len(rows) != 3:"
    strict_object_hook = "        object_pairs_hook=_strict_json_object,"
    one_read_anchor = (
        "    raw = path.read_bytes()\n"
        "    payload = json.loads(\n"
        '        raw.decode("utf-8"),'
    )
    malformed_guard = (
        '            issues.append(f"Authoritative audit JSON is invalid: '
        '{relative}: {exc}")\n            continue'
    )
    digest_assignment = "        actual_digest = hashlib.sha256(raw).hexdigest().upper()"

    mutants: list[
        tuple[
            str,
            tuple[tuple[str, str], ...],
            Callable[[Path, Path, str], str | None],
        ]
    ] = [
        (
            "path-match-removed",
            ((
                path_lookup,
                path_lookup
                + "\n        if entry is None:\n"
                + "            entry = next((row for row in registry.values() "
                + "if row['sha256'] == hashlib.sha256(raw).hexdigest().upper()), None)",
            ),),
            _copy_receipt,
        ),
        (
            "hash-check-removed",
            ((hash_guard, '        if False and actual_digest != entry["sha256"]:'),),
            _tamper_receipt,
        ),
        (
            "class-check-removed",
            ((class_guard, "    if False:"),),
            _wrong_class,
        ),
        (
            "profile-identity-removed",
            ((registry_identity_guard, "    if False:"),),
            _wrong_profile,
        ),
        (
            "state-less-block-removed",
            ((state_less_guard, "        if entry is None:\n            if False and legacy_signature:"),),
            _synthetic_receipt,
        ),
        (
            "age-filename-heuristic-added",
            ((
                state_less_guard,
                "        if entry is None:\n"
                "            if legacy_signature and 'Last Updated' not in payload "
                "and 'old' not in path.name:",
            ),),
            _named_receipt("old-looking-receipt.json"),
        ),
        (
            "fourth-entry-accepted",
            ((
                cardinality_guard,
                "    if not isinstance(rows, list) or len(rows) < 3:",
            ),),
            _add_fourth_receipt,
        ),
        (
            "duplicate-keys-accepted",
            ((strict_object_hook, "        object_pairs_hook=dict,"),),
            lambda r, p, _s: _raw_receipt(
                r,
                p,
                _json_bytes(_receipt_payload(1)).replace(
                    b'  "Transition":',
                    b'  "Transition": "discarded duplicate",\n  "Transition":',
                    1,
                ),
            ),
        ),
        (
            "malformed-audit-ignored",
            ((malformed_guard, "            continue"),),
            lambda r, _p, _s: (
                (r / "audit_log" / "malformed-mutant.json").write_bytes(b"{") and None
            ),
        ),
        (
            "copied-receipt-accepted",
            ((
                path_lookup,
                path_lookup
                + "\n        if entry is None and path.name == 'copied-receipt.json':\n"
                + "            entry = registry['audit_log/legacy-one.json']",
            ),),
            _copy_receipt,
        ),
        (
            "tampered-receipt-accepted",
            ((
                digest_assignment,
                '        actual_digest = entry["sha256"]',
            ),),
            _tamper_receipt,
        ),
        (
            "modern-missing-state-accepted",
            ((
                state_less_guard,
                "        if entry is None:\n"
                "            if legacy_signature and not path.name.startswith('transaction-'):",
            ),),
            _named_receipt("transaction-20990101.json"),
        ),
    ]
    for label, replacements, mutate in mutants:
        _expect_mutant_escape(label, replacements, mutate)

    with tempfile.TemporaryDirectory(prefix="n0-legacy-mutant-") as temp:
        mutant = _load_mutant(
            Path(temp),
            "one-read-removed",
            ((
                one_read_anchor,
                "    raw = path.read_bytes()\n"
                "    second_read = path.read_bytes()\n"
                "    payload = json.loads(\n"
                '        second_read.decode("utf-8"),',
            ),),
        )
        if inspect.getsource(mutant._read_strict_json_bytes).count("path.read_bytes()") == 1:
            raise AssertionError("one-read-removed: parse/hash TOCTOU mutation survived")

    generated = 0
    for suffix in ("copy", "old", "modern"):
        _expect_failure(
            f"generated path {suffix}",
            _named_receipt(f"generated-{suffix}.json"),
            "unregistered state-less",
        )
        generated += 1
    for offset in (0, 1, 2):
        def tamper(root: Path, _registry: Path, _sha: str, index: int = offset) -> None:
            path = root / "audit_log" / RECEIPT_NAMES[index]
            path.write_bytes(path.read_bytes().replace(b"Fixture", b"Fixturf", 1))

        _expect_failure(f"generated hash {offset}", tamper, "identity mismatch")
        generated += 1
    generated_cases: list[
        tuple[str, Callable[[Path, Path, str], str | None], str]
    ] = [
        (
            "generated missing registry row",
            lambda _r, p, _s: _rewrite_registry(
                p, lambda payload: payload["receipts"].pop()
            ),
            "exactly three",
        ),
        ("generated fourth registry row", _add_fourth_receipt, "exactly three"),
        (
            "generated registry case alias",
            _raw_registry_insertion(b'  "Schema": "alias",\n'),
            "case-ambiguous",
        ),
        (
            "generated receipt case alias",
            lambda r, p, _s: _raw_receipt(
                r,
                p,
                _json_bytes(_receipt_payload(1)).replace(b'"Lock ID"', b'"lock id"', 1),
            ),
            "case-aliased",
        ),
        (
            "generated duplicate registry key",
            _raw_registry_insertion(b'  "schema": "duplicate",\n'),
            "duplicate JSON",
        ),
        (
            "generated duplicate receipt key",
            lambda r, p, _s: _raw_receipt(
                r,
                p,
                _json_bytes(_receipt_payload(1)).replace(
                    b'  "Transition":',
                    b'  "Transition": "duplicate",\n  "Transition":',
                    1,
                ),
            ),
            "duplicate JSON",
        ),
        (
            "generated truncated JSON",
            lambda r, _p, _s: (
                (r / "audit_log" / "generated-truncated.json").write_bytes(b"{") and None
            ),
            "authoritative audit JSON is invalid",
        ),
        (
            "generated invalid UTF-8",
            lambda r, _p, _s: (
                (r / "audit_log" / "generated-utf8.json").write_bytes(b"\xff") and None
            ),
            "utf-8",
        ),
        (
            "generated non-standard number",
            lambda r, _p, _s: (
                (r / "audit_log" / "generated-nan.json").write_text(
                    '{"value":NaN}', encoding="utf-8"
                )
                and None
            ),
            "non-standard JSON numeric constant",
        ),
        ("generated wildcard path", _registry_row_path("audit_log/*.json"), "not exact"),
        (
            "generated traversal path",
            _registry_row_path("audit_log/../outside.json"),
            "not canonical",
        ),
        ("generated nested receipt copy", _nested_receipt, "unregistered state-less"),
        ("generated registry byte drift", _tamper_registry_identity, "identity mismatch"),
    ]
    for label, mutate, expected in generated_cases:
        _expect_failure(label, mutate, expected)
        generated += 1
    return len(mutants) + 1, generated


def main() -> int:
    positive = _run_positive_matrix()
    negative = _run_negative_matrix()
    mutations, generated = _run_mutation_and_generated_proof()
    print("Legacy Audit Compatibility Fixture Validation")
    print(f"Positive Matrix: PASS ({positive}/5)")
    print(f"Negative Matrix: PASS ({negative}/31)")
    print(f"Mutation Proof: PASS ({mutations}/13 killed)")
    print(f"Generated Variants: PASS ({generated}/19)")
    print("Validation Result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
