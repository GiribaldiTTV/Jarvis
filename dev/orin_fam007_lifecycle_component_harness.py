from __future__ import annotations

# Helper Status: Workstream-scoped
# Owner Workstream: FAM-007 detached child lifecycle Workstream repair
# Consolidation Target: future reusable product-window lifecycle component harness
# Promotion Decision Point: before PR Readiness fold-down

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu")

from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from desktop.desktop_renderer import AIDashboardDomainWindow, AIControlCenterDialog  # noqa: E402
from dev.orin_ai_control_center_live_resize_validation import (  # noqa: E402
    LIFECYCLE_CONTRACT_FIXTURE,
    _evaluate_lifecycle_contract_record,
)


def _utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
    ).strip()


def _drain_events() -> None:
    QApplication.processEvents()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    QApplication.processEvents()


def _wait_until(predicate, timeout_ms: int) -> bool:
    deadline = time.monotonic() + (timeout_ms / 1000.0)
    while time.monotonic() < deadline:
        _drain_events()
        if predicate():
            return True
        time.sleep(0.012)
    _drain_events()
    return bool(predicate())


def _runtime_record(
    dashboard: AIControlCenterDialog,
    window: AIDashboardDomainWindow,
    *,
    head_matches: bool,
) -> dict[str, object]:
    debug = window.lifecycle_debug_state()
    records = debug.get("records") if isinstance(debug.get("records"), list) else []
    latest = dict(records[-1]) if records else {}
    native = debug["native"]
    inventory = AIDashboardDomainWindow.runtime_lifecycle_inventory(window.domain_id, dashboard)
    latest.update(inventory)
    latest.update(
        {
            "instrumentationRootCurrent": True,
            "headMatches": head_matches,
            "supportingDiagnosticOnly": True,
            "gatingDecision": "UNEVALUATED_REQUIRES_SEPARATE_FOCUSED_CLOSURE",
            "mappedDefect": "F7-LV1-010/#307",
            "mappedIssueState": "OPEN_BLOCKING",
            "directImplementationDefects": ["F7-LV1-010/#307"],
            "launcherPreflightOwner": "F7-LV1-006-A/#300",
            "launcherPreflightIssueState": "OPEN_BLOCKING",
            "workspacePreservationOwner": "F7-LV1-009/#304",
            "workspacePreservationIssueState": "CLOSED_COMPLETED",
            "recordOrigin": "production-component-harness",
            "runtimeEvidenceEligible": True,
            "componentHarnessCommandPresent": True,
            "componentHarnessHeadMatches": head_matches,
            "componentHarnessImportsProductionLogic": True,
            "componentHarnessOutputContract": "current-head-json-and-markdown-v1",
            "taskbarGroupingAccepted": True,
            "iconicArtifactNativeFacts": native["iconicArtifactNativeFacts"],
            "iconicArtifactStatus": native["iconicArtifactStatus"],
            "iconicArtifactVisibleProof": None,
            "visualEvidenceScope": "component-no-visible-proof",
            "unexpectedIconicArtifactDetected": native["unexpectedIconicArtifactDetected"],
            "unexpectedIconicArtifactObservationComplete": native["unexpectedIconicArtifactObservationComplete"],
        }
    )
    return latest


def _add_case(cases: list[dict[str, object]], case_id: str, checks: dict[str, bool], **details) -> None:
    failed = sorted(name for name, passed in checks.items() if not passed)
    cases.append(
        {
            "id": case_id,
            "status": "PASS" if not failed else "FAIL",
            "checks": checks,
            "failedChecks": failed,
            **details,
        }
    )


def _write_outputs(output_root: Path, manifest: dict[str, object]) -> tuple[Path, Path]:
    output_root.mkdir(parents=True, exist_ok=True)
    json_path = output_root / "FAM007_LIFECYCLE_COMPONENT_HARNESS.json"
    md_path = output_root / "FAM007_LIFECYCLE_COMPONENT_HARNESS.md"
    json_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows = [
        "# FAM-007 Lifecycle Component Harness",
        "",
        f"- Result: `{manifest['result']}`",
        f"- Classification: `{manifest['classification']}`",
        f"- HEAD: `{manifest['head']}`",
        f"- Expected HEAD: `{manifest['expectedHead']}`",
        f"- Command: `{manifest['invocation']['commandLine']}`",
        f"- CWD: `{manifest['invocation']['cwd']}`",
        f"- Started: `{manifest['invocation']['startedAt']}`",
        f"- Finished: `{manifest['invocation']['finishedAt']}`",
        f"- Exit code: `{manifest['invocation']['exitCode']}`",
        "",
        "| Case | Status | Failed checks |",
        "| --- | --- | --- |",
    ]
    for case in manifest["cases"]:
        failed = ", ".join(case["failedChecks"]) or "none"
        rows.append(f"| `{case['id']}` | `{case['status']}` | {failed} |")
    rows.extend(
        [
            "",
            "This is supporting direct-component evidence only. It does not operate the launcher or taskbar, does not use generated input or Computer Use, and cannot close F7-LV1-010 or make H1/LV green.",
            "",
        ]
    )
    md_path.write_text("\n".join(rows), encoding="utf-8")
    return json_path, md_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the tracked FAM-007 production lifecycle component harness."
    )
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--timeout-ms", type=int, default=6000)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    output_root = Path(args.output_root).resolve()
    started_at = _utc_now()
    started_monotonic = time.monotonic()
    head = _git_head()
    head_matches = head == args.expected_head
    command = [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]]
    cases: list[dict[str, object]] = []
    logs: list[str] = []
    fatal_error = ""
    app = QApplication.instance() or QApplication(sys.argv[:1])
    dashboard = None
    try:
        screen = app.primaryScreen()
        dashboard = AIControlCenterDialog(screen, event_logger=logs.append)

        for domain_id, definition in AIDashboardDomainWindow.DOMAIN_DEFINITIONS.items():
            open_result = dashboard._show_ai_dashboard_domain_window(domain_id)
            _drain_events()
            window = dashboard._domain_windows[domain_id]
            record = _runtime_record(dashboard, window, head_matches=head_matches)
            errors = _evaluate_lifecycle_contract_record(record)
            _add_case(
                cases,
                f"production-open-{domain_id}",
                {
                    "window-visible": open_result.get("visible") is True,
                    "production-record-valid": not errors,
                    "one-live-object": record["liveObjectCount"] == 1,
                    "one-live-hwnd": record["liveSameDomainHwndCount"] == 1,
                    "no-duplicate": record["duplicateCount"] == 0,
                    "visual-adjudication-remains-required": record["iconicArtifactStatus"] == "VISUAL_ADJUDICATION_REQUIRED",
                },
                surface=definition["title"],
                record=record,
                evaluatorErrors=errors,
            )

        duplicate = AIDashboardDomainWindow(
            "control-center",
            screen,
            parent=dashboard,
            event_logger=logs.append,
        )
        duplicate.show_domain_window(dashboard.geometry(), requested_route="component-duplicate-probe")
        _drain_events()
        duplicate_inventory = AIDashboardDomainWindow.runtime_lifecycle_inventory("control-center", dashboard)
        _add_case(
            cases,
            "production-inventory-detects-outside-registry-duplicate",
            {
                "registered-count-remains-one": duplicate_inventory["registeredObjectCount"] == 1,
                "live-object-count-two": duplicate_inventory["liveObjectCount"] == 2,
                "live-hwnd-count-two": duplicate_inventory["liveSameDomainHwndCount"] == 2,
                "duplicate-object-detected": duplicate_inventory["duplicateObjectCount"] == 1,
                "duplicate-hwnd-detected": duplicate_inventory["duplicateHwndCount"] == 1,
            },
            lifecycleInventory=duplicate_inventory,
        )
        duplicate.close_domain_window("component-duplicate-cleanup")
        _wait_until(
            lambda: AIDashboardDomainWindow.runtime_lifecycle_inventory("control-center", dashboard)["liveObjectCount"] == 1,
            args.timeout_ms,
        )

        original = dashboard._domain_windows["control-center"]
        original_identity = id(original)
        original_generation = original._lifecycle_generation
        close_accepted = original.close_domain_window("component-close-doorway-sequence")
        deferred_results = [
            dashboard._show_ai_dashboard_domain_window("control-center")
            for _ in range(3)
        ]
        deferred = deferred_results[0]
        pending_inventory = AIDashboardDomainWindow.runtime_lifecycle_inventory("control-center", dashboard)
        replacement_ready = _wait_until(
            lambda: (
                "control-center" in dashboard._domain_windows
                and id(dashboard._domain_windows["control-center"]) != original_identity
                and not dashboard._domain_closing_identities.get("control-center")
            ),
            args.timeout_ms,
        )
        replacement = dashboard._domain_windows.get("control-center")
        final_inventory = AIDashboardDomainWindow.runtime_lifecycle_inventory("control-center", dashboard)
        _add_case(
            cases,
            "production-close-doorway-deferred-one-shot-reopen",
            {
                "close-accepted": close_accepted,
                "all-doorway-requests-deferred": all(
                    result.get("reason") == "close-in-progress-reopen-deferred"
                    for result in deferred_results
                ),
                "pending-close-count-one": pending_inventory["pendingClosingCount"] == 1,
                "registry-retained-while-closing": pending_inventory["registeredObjectCount"] == 1,
                "no-duplicate-while-closing": pending_inventory["duplicateCount"] == 0,
                "replacement-created-after-destruction": replacement_ready and replacement is not None,
                "generation-advanced-once": bool(replacement and replacement._lifecycle_generation == original_generation + 1),
                "final-one-live-object": final_inventory["liveObjectCount"] == 1,
                "final-one-live-hwnd": final_inventory["liveSameDomainHwndCount"] == 1,
                "final-no-pending-close": final_inventory["pendingClosingCount"] == 0,
                "final-no-duplicate": final_inventory["duplicateCount"] == 0,
                "final-no-stale-registry": final_inventory["staleRegistryCount"] == 0,
            },
            deferredResults=deferred_results,
            pendingInventory=pending_inventory,
            finalInventory=final_inventory,
        )

        readiness = dashboard._domain_windows["readiness-diagnostics"]
        readiness_identity = id(readiness)
        parent_close_control = dashboard._domain_windows["control-center"]
        parent_close_control.close_domain_window("component-close-before-parent-close")
        parent_close_deferred = dashboard._show_ai_dashboard_domain_window("control-center")
        dashboard.close()
        exclusive_destroyed = _wait_until(
            lambda: all(
                key not in dashboard._domain_windows
                for key in ("control-center", "capabilities-maintenance")
            ),
            args.timeout_ms,
        )
        readiness_inventory = AIDashboardDomainWindow.runtime_lifecycle_inventory("readiness-diagnostics", dashboard)
        _add_case(
            cases,
            "production-parent-close-class-lifetimes",
            {
                "exclusive-children-destroyed": exclusive_destroyed,
                "pre-parent-doorway-was-deferred": parent_close_deferred.get("reason") == "close-in-progress-reopen-deferred",
                "parent-close-suppressed-deferred-reopen": "control-center" not in dashboard._domain_windows,
                "readiness-object-preserved": id(dashboard._domain_windows.get("readiness-diagnostics")) == readiness_identity,
                "readiness-one-live-object": readiness_inventory["liveObjectCount"] == 1,
                "readiness-one-live-hwnd": readiness_inventory["liveSameDomainHwndCount"] == 1,
                "readiness-no-duplicate": readiness_inventory["duplicateCount"] == 0,
            },
            parentCloseDeferredResult=parent_close_deferred,
            readinessInventory=readiness_inventory,
        )
    except Exception as exc:
        fatal_error = f"{type(exc).__name__}: {exc}"
        _add_case(cases, "harness-fatal-error", {"no-fatal-error": False}, error=fatal_error)
    finally:
        if dashboard is not None:
            for window in list(dashboard._domain_windows.values()):
                try:
                    window.close_domain_window("component-harness-cleanup")
                except RuntimeError:
                    pass
            try:
                dashboard.close()
            except RuntimeError:
                pass
        _wait_until(
            lambda: all(
                not AIDashboardDomainWindow.runtime_lifecycle_inventory(domain_id, dashboard)["liveSameDomainHwndCount"]
                for domain_id in AIDashboardDomainWindow.DOMAIN_DEFINITIONS
            ),
            args.timeout_ms,
        )

    failed_cases = [case for case in cases if case["status"] != "PASS"]
    exit_code = 0 if head_matches and not fatal_error and not failed_cases else 1
    finished_at = _utc_now()
    manifest = {
        "schemaVersion": "fam007-production-lifecycle-component-harness-v1",
        "classification": "SUPPORTING_DIRECT_COMPONENT_EVIDENCE_ONLY",
        "gatingDecision": "UNEVALUATED_REQUIRES_SEPARATE_FOCUSED_CLOSURE",
        "result": "PASS_SUPPORTING_ONLY" if exit_code == 0 else "FAIL_SUPPORTING_COMPONENT",
        "head": head,
        "expectedHead": args.expected_head,
        "headMatches": head_matches,
        "invocation": {
            "command": command,
            "commandLine": subprocess.list2cmdline(command),
            "arguments": vars(args),
            "cwd": str(Path.cwd()),
            "environment": {
                "QTWEBENGINE_DISABLE_SANDBOX": os.environ.get("QTWEBENGINE_DISABLE_SANDBOX", ""),
                "QTWEBENGINE_CHROMIUM_FLAGS": os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", ""),
            },
            "startedAt": started_at,
            "finishedAt": finished_at,
            "durationSeconds": round(time.monotonic() - started_monotonic, 3),
            "exitCode": exit_code,
            "outputRoot": str(output_root),
        },
        "fixtures": [str(LIFECYCLE_CONTRACT_FIXTURE)],
        "productionImports": [
            "desktop.desktop_renderer.AIDashboardDomainWindow",
            "desktop.desktop_renderer.AIControlCenterDialog",
            "dev.orin_ai_control_center_live_resize_validation._evaluate_lifecycle_contract_record",
        ],
        "constraints": {
            "exactLauncherOperated": False,
            "taskbarClicked": False,
            "generatedUserInputUsed": False,
            "computerUseUsed": False,
            "focusedClosurePerformed": False,
            "h1OrLiveValidationPerformed": False,
        },
        "caseCount": len(cases),
        "failedCaseCount": len(failed_cases),
        "cases": cases,
        "eventLogCount": len(logs),
        "fatalError": fatal_error or None,
    }
    json_path, md_path = _write_outputs(output_root, manifest)
    print(json.dumps({"result": manifest["result"], "json": str(json_path), "markdown": str(md_path)}, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
