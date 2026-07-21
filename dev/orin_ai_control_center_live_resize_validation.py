# Helper Status: Workstream-scoped
# Owner Workstream: FAM-007 AI Dashboard domain-doorway Workstream repair
# Reason Reusable Helper Was Not Extended: the HUD validator is FAM-006-specific; this helper supplies FAM-007 implementation diagnostics and cannot make a governed visible-input gating decision.
# Consolidation Target: future reusable Nexus product-window supporting diagnostic helper
# Promotion Decision Point: before PR Readiness fold-down

from __future__ import annotations

import ctypes
import ctypes.wintypes
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from desktop.ai_provider_state import (  # noqa: E402
    build_default_provider_readiness_config,
    build_provider_setup_completion_foundation_state,
)
from desktop.desktop_renderer import AIControlCenterDialog  # noqa: E402

STATE_TAXONOMY_CONTRACT = "ai-dashboard-ai-control-center-state-taxonomy-v1"
VIEW_MODEL_CONTRACT = "ai-dashboard-provider-state-view-model-v1"
REQUIRED_STATE_TAXONOMY_STATES = {
    "no-provider-fail-closed",
    "provider-unavailable",
    "stale-state-fail-closed",
    "failed-check-fail-closed",
    "retry-local-check-only",
    "recovery-local-only",
    "blocked-action",
    "unavailable-capability",
    "degraded-no-provider",
}

EXACT_FAM007_SHORTCUT = Path(
    os.environ.get("OneDrive", str(Path.home() / "OneDrive"))
) / "Desktop" / "FAM-007 BLUE AI - Nexus Desktop AI Launcher.lnk"
PROOF_CLASSIFICATION_FIXTURE = (
    REPO_ROOT
    / "dev"
    / "fixtures"
    / "fam007_ai_dashboard_lv_proof_contract"
    / "proof_classification_cases.json"
)
GATING_INPUTS_BY_ACTOR = {
    "CODEX_GOVERNED_HUMAN_CLIENT": {"governed-real-os-mouse", "governed-real-os-keyboard"},
}
BANNED_VALIDATION_INPUTS = {"computer-use"}
REPAIR_DEFECT_IDS = (
    "F7-LV1-001",
    "F7-LV1-002",
    "F7-LV1-003-A",
    "F7-LV1-003-B",
    "F7-LV1-003-C",
    "F7-LV1-003-D",
    "F7-LV1-004",
    "F7-LV1-005",
    "F7-LV1-006-A",
    "F7-LV1-007",
    "F7-LV1-008",
    "F7-LV1-009",
)
WINDOW_SURFACES = (
    "AI Dashboard",
    "AI Control Center",
    "AI Readiness & Diagnostics",
    "Capabilities & Maintenance",
)
CHILD_WINDOW_SURFACES = WINDOW_SURFACES[1:]
SUPPORTED_GEOMETRY_STATES = ("minimum", "default", "intermediate", "useful-large")
RESIZE_EDGE_NAMES = ("left", "right", "top", "bottom")
RESIZE_CORNER_NAMES = ("top-left", "top-right", "bottom-left", "bottom-right")
CHILD_NEGATIVE_DRAG_GROUPS = ("description", "controls", "cards", "rows", "actions", "scrollbar")
FAM007_GATING_ACTOR = "CODEX_GOVERNED_HUMAN_CLIENT"
FAM007_GATING_INPUTS = ("governed-real-os-mouse", "governed-real-os-keyboard")


def _proof_classification_fixture_probe() -> dict[str, object]:
    payload = json.loads(PROOF_CLASSIFICATION_FIXTURE.read_text(encoding="utf-8"))
    results = []
    for case in payload.get("cases", []):
        actor = str(case.get("actor") or "")
        input_source = str(case.get("inputSource") or "")
        may_set_gating = bool(case.get("maySetGatingPass"))
        policy_allows_gating = input_source in GATING_INPUTS_BY_ACTOR.get(actor, set())
        input_prohibited = input_source in BANNED_VALIDATION_INPUTS
        actual_valid = not input_prohibited and may_set_gating == policy_allows_gating
        expected_valid = bool(case.get("expectedValid"))
        results.append(
            {
                "id": str(case.get("id") or ""),
                "actor": actor,
                "inputSource": input_source,
                "maySetGatingPass": may_set_gating,
                "policyAllowsGating": policy_allows_gating,
                "inputProhibited": input_prohibited,
                "actualValid": actual_valid,
                "expectedValid": expected_valid,
                "matchedExpected": actual_valid == expected_valid,
            }
        )
    known_bad = [item for item in results if item["expectedValid"] is False]
    return {
        "ok": bool(results)
        and all(item["matchedExpected"] for item in results)
        and bool(known_bad)
        and all(item["actualValid"] is False for item in known_bad),
        "contract": str(payload.get("contract") or ""),
        "fixture": str(PROOF_CLASSIFICATION_FIXTURE),
        "cases": results,
        "knownBadRejected": bool(known_bad) and all(item["actualValid"] is False for item in known_bad),
    }


def _powershell_json(script: str) -> object:
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if completed.returncode != 0:
        return {"error": completed.stderr.strip() or completed.stdout.strip(), "returnCode": completed.returncode}
    output = completed.stdout.strip()
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"error": "invalid-json", "raw": output}


def _read_only_exact_launcher_preflight() -> dict[str, object]:
    shortcut_literal = str(EXACT_FAM007_SHORTCUT).replace("'", "''")
    shortcut = _powershell_json(
        "$ErrorActionPreference='Stop';"
        f"$path='{shortcut_literal}';"
        "if(-not (Test-Path -LiteralPath $path)){[pscustomobject]@{exists=$false;path=$path}|ConvertTo-Json -Compress;exit};"
        "$shell=New-Object -ComObject WScript.Shell;"
        "$link=$shell.CreateShortcut($path);"
        "[pscustomobject]@{exists=$true;path=$path;target=$link.TargetPath;arguments=$link.Arguments;workingDirectory=$link.WorkingDirectory}|ConvertTo-Json -Compress"
    )
    processes = _powershell_json(
        "$items=Get-CimInstance Win32_Process | Where-Object {"
        "($_.Name -match '^(pythonw?|wscript|cscript)(\\.exe)?$') -and "
        "($_.CommandLine -match 'orin_desktop_launcher\\.pyw|launch_orin_desktop\\.vbs')"
        "} | Select-Object ProcessId,Name,CommandLine,CreationDate;"
        "@($items)|ConvertTo-Json -Compress"
    )
    if isinstance(processes, list):
        process_rows = processes
    elif isinstance(processes, dict) and "ProcessId" in processes:
        process_rows = [processes]
    else:
        process_rows = []
    selected = []
    foreign = []
    unknown = []
    for item in process_rows:
        command = str(item.get("CommandLine") or "")
        row = {
            "pid": int(item.get("ProcessId") or 0),
            "name": str(item.get("Name") or ""),
            "commandLine": command,
            "creationDate": str(item.get("CreationDate") or ""),
        }
        if str(REPO_ROOT).lower() in command.lower():
            selected.append(row)
        elif "nexus" in command.lower():
            foreign.append(row)
        else:
            unknown.append(row)
    shortcut_ok = (
        isinstance(shortcut, dict)
        and shortcut.get("exists") is True
        and str(REPO_ROOT).lower() in " ".join(
            str(shortcut.get(key) or "") for key in ("target", "arguments", "workingDirectory")
        ).lower()
    )
    if not shortcut_ok:
        classification = "EXACT_SHORTCUT_MISSING_OR_WRONG_TARGET_STOP"
    elif foreign:
        classification = "FOREIGN_RUNTIME_DETECTED_STOP_ROUTE_REQUIRED"
    elif unknown:
        classification = "UNKNOWN_OWNER_STOP"
    elif selected:
        classification = "FAM007_RUNTIME_ALREADY_ACTIVE_STOP_BEFORE_RELAUNCH"
    else:
        classification = "NO_RELEVANT_RUNTIME_DETECTED_SETUP_PRECONDITION_AVAILABLE"
    activation_permitted = classification == "NO_RELEVANT_RUNTIME_DETECTED_SETUP_PRECONDITION_AVAILABLE"
    return {
        "protocol": "fam007-exact-launcher-read-only-owner-safe-preflight-v2",
        "classification": classification,
        "readOnly": True,
        "processTerminationAttempted": False,
        "launcherActivationAttempted": False,
        "fileExplorerUsed": False,
        "computerUseUsed": False,
        "shortcut": shortcut,
        "processQuery": processes,
        "selectedRuntimeProcesses": selected,
        "foreignRuntimeProcesses": foreign,
        "unknownOwnerProcesses": unknown,
        "stopRequired": not activation_permitted,
        "activationPermitted": activation_permitted,
        "requiredActor": FAM007_GATING_ACTOR,
        "allowedInputSources": list(FAM007_GATING_INPUTS),
        "operationTransferToUserAllowed": False,
        "processMutationAllowed": False,
        "foreignOrUnknownReuseAllowed": False,
        "ownerGuessingAllowed": False,
        "fileExplorerFallbackAllowed": False,
        "directLaunchSubstitutionAllowed": False,
        "computerUseAllowed": False,
        "oneRuntimePerUserSessionPreserved": True,
        "requiredActivationRepetitions": 3,
        "requiredPostActivationEvidence": [
            "exact-shortcut-visible-target-frame",
            "launcher-target-and-working-directory-identity",
            "fam007-runtime-pid-and-command-line-root",
            "stable-process-owner-samples",
            "full-desktop-before-during-after-frames",
        ],
        "nextAction": (
            "Codex may activate the already-visible exact shortcut through the governed real-OS mouse/keyboard path; record FAM-007 PID/root stabilization and ordered visible evidence."
            if activation_permitted
            else "STOP and route the ownership or launcher-identity failure; do not terminate, alter, reuse, activate, or transfer the operation to the USER."
        ),
        "excludedFutureCandidate": "F7-LV1-006-B shared runtime owner attribution; not implemented here",
        "unresolvedSharedOwnerRoute": "F7-LV1-006-B / Issue #301 / future FAM-001 shared-runtime owner",
    }


def _physical_interaction_matrix() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(
        row_id: str,
        surface: str,
        element_group: str,
        claim: str,
        defect_ids: tuple[str, ...],
        *,
        repetitions: int = 1,
        negative_check: bool = False,
    ) -> None:
        rows.append(
            {
                "id": row_id,
                "surface": surface,
                "elementGroup": element_group,
                "claim": claim,
                "defectIds": list(defect_ids),
                "requiredActor": FAM007_GATING_ACTOR,
                "allowedInputSources": list(FAM007_GATING_INPUTS),
                "targetAcquisition": "visible-onscreen-target-before-input",
                "requiredRepetitions": repetitions,
                "negativeCheck": negative_check,
                "requiredEvidence": [
                    "full-desktop-before-frame",
                    "visible-cursor-during-frame",
                    "full-desktop-after-frame",
                    "window-geometry-or-visible-state-trace",
                    "claim-linked-adjudication",
                ],
                "workspaceInventoryRequired": True,
                "unrelatedWindowsMustRemainUntouched": True,
                "computerUseAllowed": False,
                "operationTransferToUserAllowed": False,
                "apiAcceptedByName": False,
                "helperSelfCertificationAllowed": False,
                "prohibitedGatingSubstitutes": [
                    "computer-use",
                    "qt-qtest",
                    "dom-or-direct-handler",
                    "direct-widget-call",
                    "direct-geometry-mutation",
                    "hidden-activation",
                    "helper-only-pass",
                ],
                "legacyEvidenceDisposition": "historical-supporting-only-never-retroactively-promoted",
                "syntheticSubstituteAllowed": False,
                "status": "PENDING_FOCUSED_CLOSURE_VERIFICATION",
            }
        )

    add("PARENT-001", WINDOW_SURFACES[0], "launcher-preflight", "read-only exact-launcher ownership preflight", ("F7-LV1-006-A",))
    add("PARENT-002", WINDOW_SURFACES[0], "launcher", "exact visible Desktop shortcut activation and FAM-007 PID/root stabilization", ("F7-LV1-006-A", "F7-LV1-007"), repetitions=3)
    add("PARENT-003", WINDOW_SURFACES[0], "tray-menu", "notification-area route opens the AI Dashboard parent", ("F7-LV1-005", "F7-LV1-007"))
    add("PARENT-004", WINDOW_SURFACES[0], "workspace", "before-run workspace inventory proves no unrelated window state changes", ("F7-LV1-005", "F7-LV1-007"))
    add("PARENT-005", WINDOW_SURFACES[0], "drag-header", "three valid visible-header move cycles", ("F7-LV1-005", "F7-LV1-007"), repetitions=3)
    for index, group in enumerate(("window-controls", "title-description", "cards", "rows", "buttons", "scrollbar"), start=6):
        add(f"PARENT-{index:03d}", WINDOW_SURFACES[0], group, f"negative drag over parent {group}", ("F7-LV1-005", "F7-LV1-007"), negative_check=True)
    parent_sequence = len(rows) + 1
    for edge in RESIZE_EDGE_NAMES:
        add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], f"resize-edge-{edge}", f"{edge} edge cursor transition, resize delta, release, and immediate outside negative sample", ("F7-LV1-005", "F7-LV1-007"), repetitions=2, negative_check=True)
        parent_sequence += 1
    for corner in RESIZE_CORNER_NAMES:
        add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], f"resize-corner-{corner}", f"{corner} corner cursor transition, resize delta, release, and immediate outside negative sample", ("F7-LV1-005", "F7-LV1-007"), repetitions=2, negative_check=True)
        parent_sequence += 1
    add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], "window-controls", "deliberate in-scope minimize and restore only", ("F7-LV1-005", "F7-LV1-007")); parent_sequence += 1
    add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], "lifecycle", "close and normal tray/menu-route reopen", ("F7-LV1-005", "F7-LV1-007")); parent_sequence += 1
    for domain in ("control-center", "readiness-diagnostics", "capabilities-maintenance"):
        add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], f"doorway-{domain}", f"activate {domain} doorway and verify the named detached window", ("F7-LV1-005", "F7-LV1-007"))
        parent_sequence += 1
    add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], "doorway-buttons", "hover, keyboard focus, pressed, enabled, and returned-focus states", ("F7-LV1-005", "F7-LV1-007")); parent_sequence += 1
    add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], "workspace", "after-run workspace inventory matches the before inventory except named in-scope windows", ("F7-LV1-005", "F7-LV1-007")); parent_sequence += 1
    for geometry in SUPPORTED_GEOMETRY_STATES:
        add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], f"geometry-{geometry}", f"{geometry} parent geometry has intentional composition, stable reflow, and owned scrolling", ("F7-LV1-005", "F7-LV1-007"))
        parent_sequence += 1
    for environment, claim in (
        ("display-scale", "100, 125, 150, and 200 percent display-scale inspection"),
        ("multi-monitor", "monitor transfer and missing-monitor recovery remain onscreen"),
        ("portrait-narrow-monitor", "portrait or narrow-monitor screen-bounded composition"),
        ("restored-state", "restored geometry and controls remain coherent"),
        ("content-overflow", "screen-bounded overflow remains reachable through the owned scrollbar"),
        ("maximize-fullscreen-policy", "maximize and fullscreen are not offered and do not appear as hidden controls"),
    ):
        add(f"PARENT-{parent_sequence:03d}", WINDOW_SURFACES[0], environment, claim, ("F7-LV1-005", "F7-LV1-007"))
        parent_sequence += 1

    for surface_index, surface in enumerate(CHILD_WINDOW_SURFACES, start=1):
        prefix = f"CHILD-{surface_index}"
        sequence = 1
        add(f"{prefix}-{sequence:03d}", surface, "doorway", "open from the matching AI Dashboard doorway and verify title/focus", ("F7-LV1-005", "F7-LV1-007")); sequence += 1
        add(f"{prefix}-{sequence:03d}", surface, "visible-title-drag-strip", "three valid title-strip move cycles with exact pointer/window deltas", ("F7-LV1-001", "F7-LV1-005", "F7-LV1-007"), repetitions=3); sequence += 1
        for group in CHILD_NEGATIVE_DRAG_GROUPS:
            add(f"{prefix}-{sequence:03d}", surface, group, f"negative drag over child {group}", ("F7-LV1-001", "F7-LV1-005", "F7-LV1-007"), repetitions=2, negative_check=True)
            sequence += 1
        add(f"{prefix}-{sequence:03d}", surface, "rounded-shell-boundary", "visible border, mask, inside rail, transparent corner, and immediate outside samples coincide", ("F7-LV1-002", "F7-LV1-003-A", "F7-LV1-005", "F7-LV1-007"), repetitions=2, negative_check=True); sequence += 1
        for edge in RESIZE_EDGE_NAMES:
            add(f"{prefix}-{sequence:03d}", surface, f"resize-edge-{edge}", f"{edge} edge cursor transition, legal resize delta, release, and outside negative sample", ("F7-LV1-002", "F7-LV1-005", "F7-LV1-007"), repetitions=2, negative_check=True)
            sequence += 1
        for corner in RESIZE_CORNER_NAMES:
            add(f"{prefix}-{sequence:03d}", surface, f"resize-corner-{corner}", f"{corner} corner cursor transition, legal resize delta, release, and outside negative sample", ("F7-LV1-002", "F7-LV1-005", "F7-LV1-007"), repetitions=2, negative_check=True)
            sequence += 1
        add(f"{prefix}-{sequence:03d}", surface, "window-controls", "minimize and restore through the named child control only", ("F7-LV1-005", "F7-LV1-007")); sequence += 1
        add(f"{prefix}-{sequence:03d}", surface, "window-controls", "close, return to parent, and normal-doorway reopen", ("F7-LV1-005", "F7-LV1-007")); sequence += 1
        add(f"{prefix}-{sequence:03d}", surface, "singleton-focus", "second doorway activation refocuses the same child object", ("F7-LV1-005", "F7-LV1-007")); sequence += 1
        add(f"{prefix}-{sequence:03d}", surface, "parent-child-lifecycle", "parent close obeys the declared exclusive-child or external-unique lifecycle", ("F7-LV1-005", "F7-LV1-007")); sequence += 1
        for geometry in SUPPORTED_GEOMETRY_STATES:
            add(f"{prefix}-{sequence:03d}", surface, f"geometry-{geometry}", f"{geometry} geometry has intentional composition, stable reflow, and owned scrolling", ("F7-LV1-003-B", "F7-LV1-003-C", "F7-LV1-003-D", "F7-LV1-005", "F7-LV1-007"))
            sequence += 1
        add(f"{prefix}-{sequence:03d}", surface, "scroll-and-actions", "scroll to every lower content row and action, activate only admitted display/local actions, and return to top", ("F7-LV1-003-B", "F7-LV1-003-C", "F7-LV1-003-D", "F7-LV1-005", "F7-LV1-007")); sequence += 1
        add(f"{prefix}-{sequence:03d}", surface, "control-and-action-states", "hover, tooltip, focus, pressed, disabled, and aria-pressed states remain clear and stable", ("F7-LV1-003-A", "F7-LV1-005", "F7-LV1-007")); sequence += 1
        for environment, claim in (
            ("display-scale", "100, 125, 150, and 200 percent display-scale inspection"),
            ("multi-monitor", "monitor transfer and missing-monitor recovery remain onscreen"),
            ("portrait-narrow-monitor", "portrait or narrow-monitor screen-bounded composition"),
            ("restored-state", "restored geometry and controls remain coherent"),
            ("content-overflow", "screen-bounded overflow keeps all rows and actions reachable"),
            ("maximize-fullscreen-policy", "maximize and fullscreen are not offered and do not appear as hidden controls"),
        ):
            add(f"{prefix}-{sequence:03d}", surface, environment, claim, ("F7-LV1-003-B", "F7-LV1-003-C", "F7-LV1-003-D", "F7-LV1-005", "F7-LV1-007"))
            sequence += 1
    return rows


def _interaction_matrix_contract_ok(rows: list[dict[str, object]]) -> bool:
    ids = [str(row.get("id") or "") for row in rows]
    if len(rows) < 100 or len(ids) != len(set(ids)) or not all(ids):
        return False
    if {str(row.get("surface") or "") for row in rows} != set(WINDOW_SURFACES):
        return False
    if not all(
        row.get("requiredActor") == FAM007_GATING_ACTOR
        and tuple(row.get("allowedInputSources") or ()) == FAM007_GATING_INPUTS
        and row.get("computerUseAllowed") is False
        and row.get("operationTransferToUserAllowed") is False
        and row.get("apiAcceptedByName") is False
        and row.get("helperSelfCertificationAllowed") is False
        and len(row.get("prohibitedGatingSubstitutes") or []) == 7
        and row.get("legacyEvidenceDisposition") == "historical-supporting-only-never-retroactively-promoted"
        and row.get("syntheticSubstituteAllowed") is False
        and row.get("status") == "PENDING_FOCUSED_CLOSURE_VERIFICATION"
        and len(row.get("requiredEvidence") or []) == 5
        for row in rows
    ):
        return False
    for surface in WINDOW_SURFACES:
        groups = {str(row.get("elementGroup") or "") for row in rows if row.get("surface") == surface}
        if not {f"resize-edge-{name}" for name in RESIZE_EDGE_NAMES}.issubset(groups):
            return False
        if not {f"resize-corner-{name}" for name in RESIZE_CORNER_NAMES}.issubset(groups):
            return False
        if not {f"geometry-{state}" for state in SUPPORTED_GEOMETRY_STATES}.issubset(groups):
            return False
        if not {
            "display-scale",
            "multi-monitor",
            "portrait-narrow-monitor",
            "restored-state",
            "content-overflow",
            "maximize-fullscreen-policy",
        }.issubset(groups):
            return False
    for surface in CHILD_WINDOW_SURFACES:
        groups = {str(row.get("elementGroup") or "") for row in rows if row.get("surface") == surface}
        if not set(CHILD_NEGATIVE_DRAG_GROUPS).issubset(groups):
            return False
    return True


def _dual_contrast_matrix() -> list[dict[str, object]]:
    return [
        {
            "id": f"DUAL-{surface_index:02d}-{geometry_index:02d}-{background_index:02d}",
            "pairId": f"DUAL-{surface_index:02d}-{geometry_index:02d}",
            "surface": surface,
            "geometryState": geometry,
            "background": background,
            "backgroundHex": color,
            "requiredState": "identical-geometry-state-scale-crop-per-pair",
            "requiredCaptures": ["full-desktop", "full-window", "four-corner-and-four-edge-crops"],
            "requiredAdjudication": [
                "border",
                "rounded-corners",
                "transparency",
                "native-mask",
                "shadow",
                "halo",
                "gaps",
                "clipping",
                "bleed-through",
                "native-frame-exposure",
                "visual-interactive-boundary-alignment",
                "controls",
                "scrollbar",
                "focus",
            ],
            "computerUseAllowed": False,
            "operationTransferToUserAllowed": False,
            "edgeCornerAdjudication": "PENDING_FOCUSED_CLOSURE_VERIFICATION",
            "interactionProofSuppliedByImage": False,
        }
        for surface_index, surface in enumerate(WINDOW_SURFACES, start=1)
        for geometry_index, geometry in enumerate(SUPPORTED_GEOMETRY_STATES, start=1)
        for background_index, (background, color) in enumerate((("solid-black", "#000000"), ("solid-white", "#FFFFFF")), start=1)
    ]


def _dual_contrast_matrix_contract_ok(rows: list[dict[str, object]]) -> bool:
    expected_pairs = {
        (surface, geometry)
        for surface in WINDOW_SURFACES
        for geometry in SUPPORTED_GEOMETRY_STATES
    }
    actual_pairs: dict[tuple[str, str], set[str]] = {}
    for row in rows:
        key = (str(row.get("surface") or ""), str(row.get("geometryState") or ""))
        actual_pairs.setdefault(key, set()).add(str(row.get("background") or ""))
        if (
            row.get("computerUseAllowed") is not False
            or row.get("operationTransferToUserAllowed") is not False
            or row.get("interactionProofSuppliedByImage") is not False
            or len(row.get("requiredCaptures") or []) != 3
            or len(row.get("requiredAdjudication") or []) != 14
        ):
            return False
    return set(actual_pairs) == expected_pairs and all(
        backgrounds == {"solid-black", "solid-white"}
        for backgrounds in actual_pairs.values()
    )


_VISUAL_GRAMMAR_PROBE_SCRIPT = r"""
(() => {
  const surface = document.getElementById("monitoring-hud");
  const cssText = Array.from(document.styleSheets).map((sheet) => {
    try {
      return Array.from(sheet.cssRules || []).map((rule) => rule.cssText || "").join("\n");
    } catch (error) {
      return "";
    }
  }).join("\n");
  const rectFor = (node) => {
    if (!node) return null;
    const rect = node.getBoundingClientRect();
    return {
      left: Math.round(rect.left),
      top: Math.round(rect.top),
      right: Math.round(rect.right),
      bottom: Math.round(rect.bottom),
      width: Math.round(rect.width),
      height: Math.round(rect.height)
    };
  };
  const styleFor = (node) => {
    if (!node) return {};
    const style = getComputedStyle(node);
    return {
      display: style.display,
      position: style.position,
      gridTemplateColumns: style.gridTemplateColumns,
      gap: style.gap,
      columnGap: style.columnGap,
      rowGap: style.rowGap,
      padding: `${style.paddingTop} ${style.paddingRight} ${style.paddingBottom} ${style.paddingLeft}`,
      paddingTop: style.paddingTop,
      paddingRight: style.paddingRight,
      paddingBottom: style.paddingBottom,
      paddingLeft: style.paddingLeft,
      marginTop: style.marginTop,
      minHeight: style.minHeight,
      width: style.width,
      height: style.height,
      maxWidth: style.maxWidth,
      fontSize: style.fontSize,
      lineHeight: style.lineHeight,
      fontWeight: style.fontWeight,
      letterSpacing: style.letterSpacing,
      textTransform: style.textTransform,
      textIndent: style.textIndent,
      color: style.color,
      backgroundColor: style.backgroundColor,
      borderTopWidth: style.borderTopWidth,
      borderTopColor: style.borderTopColor,
      borderRadius: style.borderRadius,
      opacity: style.opacity,
      boxShadow: style.boxShadow,
      overflow: style.overflow,
      whiteSpace: style.whiteSpace,
      flex: style.flex,
      flexGrow: style.flexGrow,
      flexShrink: style.flexShrink,
      flexBasis: style.flexBasis,
      flexWrap: style.flexWrap
    };
  };
  const textFor = (node) => (node?.textContent || "").replace(/\s+/g, " ").trim();
  const group = (selector) => {
    const node = document.querySelector(selector);
    return {
      present: Boolean(node),
      selector,
      rect: rectFor(node),
      style: styleFor(node),
      text: textFor(node).slice(0, 180)
    };
  };
  const all = (selector) => Array.from(document.querySelectorAll(selector)).map((node, index) => ({
    index,
    rect: rectFor(node),
    style: styleFor(node),
    text: textFor(node).slice(0, 180),
    id: node.id || "",
    dataset: Object.assign({}, node.dataset || {})
  }));
  const rowMetrics = all(".monitoring-hud__state-row").map((row) => ({
    index: row.index,
    height: row.rect ? row.rect.height : 0,
    width: row.rect ? row.rect.width : 0,
    padding: row.style.padding,
    gridTemplateColumns: row.style.gridTemplateColumns,
    gap: row.style.gap,
    text: row.text
  }));
  const buttonMetrics = all(".monitoring-hud__hub-action").map((button) => ({
    index: button.index,
    id: button.id,
    text: button.text,
    width: button.rect ? button.rect.width : 0,
    height: button.rect ? button.rect.height : 0,
    fontSize: button.style.fontSize,
    fontWeight: button.style.fontWeight,
    letterSpacing: button.style.letterSpacing,
    padding: button.style.padding,
    borderRadius: button.style.borderRadius,
    disabled: Boolean(document.getElementById(button.id)?.disabled),
    ariaDisabled: document.getElementById(button.id)?.getAttribute("aria-disabled") || "",
    actionState: button.dataset.actionState || "",
    launchKind: button.dataset.launchWindowKind || ""
  }));
  const cardMetrics = all("[data-dashboard-hub-card]").map((card) => {
    const cardNode = document.querySelectorAll("[data-dashboard-hub-card]")[card.index];
    const heading = cardNode?.querySelector(".monitoring-hud__hub-card-topline");
    const rows = cardNode?.querySelectorAll(".monitoring-hud__state-row") || [];
    const rowsBox = cardNode?.querySelector(".ai-control-center-card-rows") || (rows.length ? rows[0].parentElement : null);
    const action = cardNode?.querySelector(".monitoring-hud__hub-actions");
    const actionButton = cardNode?.querySelector(".monitoring-hud__hub-action");
    const cardRect = cardNode?.getBoundingClientRect();
    const actionRect = action?.getBoundingClientRect();
    const buttonRect = actionButton?.getBoundingClientRect();
    const rowRects = Array.from(rows).map((row) => row.getBoundingClientRect());
    const rowUnionRect = rowRects.length ? {
      top: Math.min(...rowRects.map((rect) => rect.top)),
      bottom: Math.max(...rowRects.map((rect) => rect.bottom)),
      left: Math.min(...rowRects.map((rect) => rect.left)),
      right: Math.max(...rowRects.map((rect) => rect.right))
    } : null;
    if (rowUnionRect) {
      rowUnionRect.width = rowUnionRect.right - rowUnionRect.left;
      rowUnionRect.height = rowUnionRect.bottom - rowUnionRect.top;
    }
    const rowsRect = rowsBox && rowsBox.classList.contains("ai-control-center-card-rows")
      ? rowsBox.getBoundingClientRect()
      : rowUnionRect;
    return {
      id: card.dataset.dashboardHubCard || "",
      rect: card.rect,
      style: card.style,
      title: textFor(cardNode?.querySelector(".monitoring-hud__hub-card-title-copy strong")),
      description: textFor(cardNode?.querySelector(".monitoring-hud__hub-card-description")),
      rowCount: rows.length,
      rowHeights: Array.from(rows).map((row) => Math.round(row.getBoundingClientRect().height)),
      rowsHeight: rowsRect ? Math.round(rowsRect.height) : 0,
      topToHeading: cardRect && heading ? Math.round(heading.getBoundingClientRect().top - cardRect.top) : null,
      headingToRows: heading && rowsRect ? Math.round(rowsRect.top - heading.getBoundingClientRect().bottom) : null,
      afterRowsGap: rowsRect && actionRect ? Math.round(actionRect.top - rowsRect.bottom) : null,
      actionBottomGutter: cardRect && actionRect ? Math.round(cardRect.bottom - actionRect.bottom) : null,
      buttonRightGutter: cardRect && buttonRect ? Math.round(cardRect.right - buttonRect.right) : null,
      buttonWidth: buttonRect ? Math.round(buttonRect.width) : 0,
      buttonHeight: buttonRect ? Math.round(buttonRect.height) : 0
    };
  });
  const materialGroups = {
    chrome: group(".monitoring-hud__chrome"),
    titleGroup: group(".monitoring-hud__title-group"),
    header: group(".monitoring-hud__header"),
    kicker: group(".monitoring-hud__kicker"),
    title: group(".monitoring-hud__title"),
    subtitle: group(".monitoring-hud__subtitle"),
    surfaceRole: group(".monitoring-hud__surface-role"),
    surfaceRoleCopy: group(".monitoring-hud__surface-role-copy"),
    surfaceRolePair: group(".monitoring-hud__surface-role-pair"),
    windowControls: group(".monitoring-hud__window-controls"),
    windowControlButton: group(".monitoring-hud__window-control-button"),
    controlHub: group(".monitoring-hud__control-hub"),
    hubCard: group("[data-dashboard-hub-card]"),
    cardTopline: group(".monitoring-hud__hub-card-topline"),
    cardBadge: group(".monitoring-hud__hub-card-topline > span"),
    cardTitle: group(".monitoring-hud__hub-card-title-copy strong"),
    cardDescription: group(".monitoring-hud__hub-card-description"),
    stateRow: group(".monitoring-hud__state-row"),
    rowLabel: group(".monitoring-hud__state-row span"),
    rowValue: group(".monitoring-hud__state-row strong"),
    hubActions: group(".monitoring-hud__hub-actions"),
    hubAction: group(".monitoring-hud__hub-action"),
    buttonLabel: group(".monitoring-hud__button-label"),
    scrollbarTrack: group(".ai-control-center-scrollbar__track"),
    scrollbarThumb: group(".ai-control-center-scrollbar__thumb")
  };
  const missingGroups = Object.entries(materialGroups)
    .filter(([, value]) => !value.present)
    .map(([name]) => name);
  return JSON.stringify({
    ok: true,
    surface: {
      id: surface?.dataset.surfaceId || "",
      productSurfaceRole: surface?.dataset.productSurfaceRole || "",
      defaultWindowWidth: surface?.dataset.defaultWindowWidth || "",
      defaultWindowHeight: surface?.dataset.defaultWindowHeight || "",
      dashboardSurfaceModel: surface?.dataset.dashboardSurfaceModel || "",
      dashboardIaModel: surface?.dataset.dashboardIaModel || "",
      childWindowModel: surface?.dataset.childWindowModel || "",
      rowDensity: surface?.dataset.rowDensity || "",
      cardOrder: surface?.dataset.dashboardCardOrder || "",
      title: textFor(document.querySelector(".monitoring-hud__title")),
      subtitle: textFor(document.querySelector(".monitoring-hud__subtitle"))
    },
    materialGroups,
    rowMetrics,
    buttonMetrics,
    cardMetrics,
    cssStateSelectors: {
      hubActionHover: cssText.includes(".monitoring-hud__hub-action") && (cssText.includes(":hover") || cssText.includes(".is-hovered")),
      hubActionFocus: cssText.includes(".monitoring-hud__hub-action") && cssText.includes(":focus-visible"),
      hubActionPressed: cssText.includes(".monitoring-hud__hub-action") && (cssText.includes(":active") || cssText.includes(".is-pressed")),
      hubActionDisabled: cssText.includes(".monitoring-hud__hub-action:disabled") || cssText.includes("[aria-disabled=\"true\"]"),
      windowControlHover: cssText.includes(".monitoring-hud__window-control-button:hover"),
      windowControlFocus: cssText.includes(".monitoring-hud__window-control-button:focus-visible"),
      windowControlDisabled: cssText.includes(".monitoring-hud__window-control-button:disabled") || cssText.includes("data-window-control-state=\"blocked\""),
      customScrollbar: cssText.includes("ai-control-center-scrollbar__thumb")
    },
    coverage: {
      materialGroupCount: Object.keys(materialGroups).length,
      missingGroups,
      cardCount: cardMetrics.length,
      rowCount: rowMetrics.length,
      buttonCount: buttonMetrics.length
    }
  });
})();
"""


user32 = ctypes.windll.user32
GetWindowRect = user32.GetWindowRect
GetWindowRect.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.RECT)]
GetWindowRect.restype = ctypes.c_bool
SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = [ctypes.wintypes.HWND]
SetForegroundWindow.restype = ctypes.c_bool
BringWindowToTop = user32.BringWindowToTop
BringWindowToTop.argtypes = [ctypes.wintypes.HWND]
BringWindowToTop.restype = ctypes.c_bool
ShowWindow = user32.ShowWindow
ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
ShowWindow.restype = ctypes.c_bool
SetCursorPos = user32.SetCursorPos
SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
SetCursorPos.restype = ctypes.c_bool
mouse_event = user32.mouse_event
mouse_event.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
mouse_event.restype = None
SW_RESTORE = 9
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_MOVE = 0x0001


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def _pump(app: QApplication, duration_ms: int = 80) -> None:
    deadline = time.monotonic() + max(0, duration_ms) / 1000.0
    while time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()


def _run_js(app: QApplication, dialog: AIControlCenterDialog, script: str, timeout_ms: int = 1500):
    box: dict[str, object] = {"done": False, "result": None}

    def _complete(result):
        box["result"] = result
        box["done"] = True

    dialog.webview.page().runJavaScript(script, _complete)
    deadline = time.monotonic() + max(0, timeout_ms) / 1000.0
    while not box["done"] and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    return box.get("result")


def _run_visual_grammar_probe(app: QApplication, dialog: AIControlCenterDialog) -> dict[str, object]:
    raw = _run_js(app, dialog, _VISUAL_GRAMMAR_PROBE_SCRIPT, timeout_ms=2500)
    try:
        parsed = json.loads(raw or "{}")
    except Exception:
        parsed = {"ok": False, "raw": str(raw or "")}
    return parsed if isinstance(parsed, dict) else {"ok": False, "raw": str(parsed)}


def _run_child_js(app: QApplication, window, script: str, timeout_ms: int = 1500):
    box: dict[str, object] = {"done": False, "result": None}

    def _complete(result):
        box["result"] = result
        box["done"] = True

    window.webview.page().runJavaScript(script, _complete)
    deadline = time.monotonic() + max(0, timeout_ms) / 1000.0
    while not box["done"] and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    return box.get("result")


def _rect(hwnd: int) -> dict[str, int]:
    native_rect = ctypes.wintypes.RECT()
    if not hwnd or not GetWindowRect(ctypes.wintypes.HWND(int(hwnd)), ctypes.byref(native_rect)):
        return {"left": 0, "top": 0, "right": 0, "bottom": 0, "width": 0, "height": 0}
    return {
        "left": int(native_rect.left),
        "top": int(native_rect.top),
        "right": int(native_rect.right),
        "bottom": int(native_rect.bottom),
        "width": int(native_rect.right - native_rect.left),
        "height": int(native_rect.bottom - native_rect.top),
    }


def _foreground_window(app: QApplication, window, duration_ms: int = 260) -> None:
    window.showNormal()
    window.raise_()
    window.activateWindow()
    hwnd = int(window.winId()) if window.winId() else 0
    if hwnd:
        ShowWindow(ctypes.wintypes.HWND(hwnd), SW_RESTORE)
        BringWindowToTop(ctypes.wintypes.HWND(hwnd))
        SetForegroundWindow(ctypes.wintypes.HWND(hwnd))
    _pump(app, duration_ms)


def _capture_window(app: QApplication, window, root: Path, label: str) -> dict[str, str]:
    focused_path = root / f"{label}_focused_window.png"
    desktop_path = root / f"{label}_full_desktop.png"
    screen = window.screen() or QApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No screen available for screenshot capture")
    _foreground_window(app, window)
    if not window.grab().save(str(focused_path)):
        raise RuntimeError(f"Failed to save focused screenshot: {focused_path}")
    _pump(app, 80)
    if not screen.grabWindow(0).save(str(desktop_path)):
        raise RuntimeError(f"Failed to save desktop screenshot: {desktop_path}")
    _pump(app, 50)
    return {"focusedWindow": str(focused_path), "fullDesktop": str(desktop_path)}


def _probe_rect_to_qrect(raw: dict[str, object] | None, window) -> QRect:
    source = raw if isinstance(raw, dict) else {}
    try:
        left = int(round(float(source.get("left", 0))))
        top = int(round(float(source.get("top", 0))))
        width = int(round(float(source.get("width", 0))))
        height = int(round(float(source.get("height", 0))))
    except Exception:
        return QRect()
    rect = QRect(max(0, left), max(0, top), max(0, width), max(0, height))
    return rect.intersected(QRect(0, 0, int(window.width()), int(window.height())))


def _capture_window_region(app: QApplication, window, root: Path, label: str, raw_rect: dict[str, object] | None) -> dict[str, object]:
    rect = _probe_rect_to_qrect(raw_rect, window)
    if not rect.isValid() or rect.width() < 16 or rect.height() < 12:
        return {"ok": False, "label": label, "reason": "invalid-rect"}
    path = root / f"{label}.png"
    _foreground_window(app, window, 140)
    if not window.grab(rect).save(str(path)):
        return {"ok": False, "label": label, "reason": "save-failed", "path": str(path)}
    return {
        "ok": True,
        "label": label,
        "path": str(path),
        "rect": {
            "left": rect.left(),
            "top": rect.top(),
            "width": rect.width(),
            "height": rect.height(),
        },
    }


def _copy_reference_image(source: Path, root: Path, label: str) -> dict[str, object]:
    target = root / f"{label}.png"
    if not source.exists():
        return {"ok": False, "label": label, "source": str(source), "reason": "missing-reference"}
    target.write_bytes(source.read_bytes())
    image = QImage(str(target))
    return {
        "ok": not image.isNull(),
        "label": label,
        "source": str(source),
        "path": str(target),
        "width": int(image.width()) if not image.isNull() else 0,
        "height": int(image.height()) if not image.isNull() else 0,
        "reason": "" if not image.isNull() else "unreadable-reference",
    }


def _scaled_for_board(image: QImage, max_width: int = 460, max_height: int = 420) -> QImage:
    if image.isNull():
        return image
    scaled = image
    if scaled.width() > max_width:
        scaled = scaled.scaledToWidth(max_width, Qt.SmoothTransformation)
    if scaled.height() > max_height:
        scaled = scaled.scaledToHeight(max_height, Qt.SmoothTransformation)
    return scaled


def _write_side_by_side_board(
    left_path: Path,
    right_path: Path,
    out_path: Path,
    left_label: str,
    right_label: str,
) -> dict[str, object]:
    left = QImage(str(left_path))
    right = QImage(str(right_path))
    if left.isNull() or right.isNull():
        return {
            "ok": False,
            "path": str(out_path),
            "reason": "source-image-unreadable",
            "left": str(left_path),
            "right": str(right_path),
        }
    left = _scaled_for_board(left)
    right = _scaled_for_board(right)
    padding = 18
    label_height = 32
    width = left.width() + right.width() + (padding * 3)
    height = max(left.height(), right.height()) + label_height + (padding * 2)
    board = QImage(width, height, QImage.Format_ARGB32)
    board.fill(QColor(2, 10, 20))
    painter = QPainter(board)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setPen(QColor(116, 240, 255))
    font = QFont("Segoe UI", 10)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(padding, padding + 14, left_label)
    right_x = left.width() + (padding * 2)
    painter.drawText(right_x, padding + 14, right_label)
    painter.drawImage(padding, padding + label_height, left)
    painter.drawImage(right_x, padding + label_height, right)
    painter.end()
    if not board.save(str(out_path)):
        return {"ok": False, "path": str(out_path), "reason": "save-failed"}
    return {
        "ok": True,
        "path": str(out_path),
        "left": str(left_path),
        "right": str(right_path),
    }


def _write_child_contact_sheet(
    comparator_path: Path,
    child_path: Path,
    out_path: Path,
    comparator_label: str,
    child_label: str,
) -> dict[str, object]:
    return _write_side_by_side_board(
        comparator_path,
        child_path,
        out_path,
        comparator_label,
        child_label,
    )


def _write_settings_option_b_disposition(log_root: Path) -> dict[str, object]:
    manifest_path = log_root / "15_settings_option_b_removal_deferment.json"
    payload = {
        "ok": True,
        "selectedOption": "B",
        "selectedOptionLabel": "Remove And Defer",
        "currentRuntimeSettingsAffordance": "removed-from-current-workstream-exit-path",
        "fam003Dependency": "global-settings-window-required-before-future-settings-entry",
        "activeGlobalSettingsBehavior": False,
        "settingsWindowOpened": False,
        "settingsBehaviorImplementationBlocked": True,
        "implementedRuntimeOption": "B",
        "classification": "option-b-implementation-disposition-only",
    }
    manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payload["jsonPath"] = str(manifest_path)
    return payload


def _drive_ai_dashboard_horizontal_resize(
    app: QApplication,
    dialog: AIControlCenterDialog,
    log_root: Path,
) -> dict[str, object]:
    _foreground_window(app, dialog)
    initial = _rect(int(dialog.winId()))
    if initial["width"] <= 0:
        return {"ok": False, "reason": "missing-window-rect", "before": initial}

    def _read_layout() -> dict[str, object]:
        layout_raw = _run_js(
            app,
            dialog,
            """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          const titleGroup = document.querySelector(".monitoring-hud__title-group");
          const subtitle = document.querySelector(".monitoring-hud__subtitle");
          const settings = document.getElementById("ai-dashboard-settings-action");
          const strip = document.querySelector("[data-dashboard-role='global-ai-strip']");
          const nodes = [...document.querySelectorAll(".monitoring-hud__state-row span, .monitoring-hud__state-row strong, .monitoring-hud__hub-action")];
          const hubRect = hub?.getBoundingClientRect();
          const clipped = nodes.filter((node) => {
            const rect = node.getBoundingClientRect();
            return hubRect && (rect.right > hubRect.right + 2 || rect.left < hubRect.left - 2);
          }).map((node) => node.textContent.trim());
          const stripRect = strip?.getBoundingClientRect();
          const settingsRect = settings?.getBoundingClientRect();
          const rectFor = (node) => {
            if (!node) return { left: 0, top: 0, right: 0, bottom: 0, width: 0, height: 0 };
            const rect = node.getBoundingClientRect();
            return {
              left: Math.round(rect.left),
              top: Math.round(rect.top),
              right: Math.round(rect.right),
              bottom: Math.round(rect.bottom),
              width: Math.round(rect.width),
              height: Math.round(rect.height)
            };
          };
          const pxNumber = (value) => {
            const parsed = Number.parseFloat(String(value || "0"));
            return Number.isFinite(parsed) ? parsed : 0;
          };
          const firstGridColumnWidth = (template) => {
            const match = String(template || "").match(/([\\d.]+)px/);
            return match ? Number(match[1]) : 0;
          };
          const lineHeightNumber = (style, rect) => pxNumber(style?.lineHeight) || Math.max(1, rect.height);
          const titleStatusPillWrap = (() => {
            const copy = document.querySelector(".monitoring-hud__surface-role-copy");
            const copyRect = rectFor(copy);
            const pairMetrics = [...document.querySelectorAll(".monitoring-hud__surface-role-pair")].map((pair) => {
              const rect = rectFor(pair);
              const style = getComputedStyle(pair);
              const childRects = [...pair.children].map((child) => rectFor(child));
              const childTops = childRects.map((rect) => rect.top);
              const childBottoms = childRects.map((rect) => rect.bottom);
              const childTopSpread = childTops.length ? Math.max(...childTops) - Math.min(...childTops) : 0;
              const childBottomSpread = childBottoms.length ? Math.max(...childBottoms) - Math.min(...childBottoms) : 0;
              return {
                text: pair.textContent.replace(/\\s+/g, " ").trim(),
                rect,
                display: style.display,
                flexShrink: style.flexShrink,
                whiteSpace: style.whiteSpace,
                lineTop: rect.top,
                childrenShareLine: childTopSpread <= 2 && childBottomSpread <= 2,
                withinPill: copyRect.width > 0 && rect.left >= copyRect.left - 2 && rect.right <= copyRect.right + 2
              };
            });
            const expectedTexts = ["AI Persona - None", "Status - Not implemented", "Provider - Blocked"];
            return {
              copyRect,
              copyMaxWidth: copy ? getComputedStyle(copy).maxWidth : "",
              pairCount: pairMetrics.length,
              lineCount: new Set(pairMetrics.map((pair) => pair.lineTop)).size,
              expectedTextsPresent: expectedTexts.every((text) => pairMetrics.some((pair) => pair.text === text)),
              groupsAtomic: pairMetrics.every((pair) => pair.display.includes("flex") && pair.whiteSpace === "nowrap" && pair.childrenShareLine),
              clippedPairCount: pairMetrics.filter((pair) => !pair.withinPill).length,
              pairMetrics
            };
          })();
          const titleDescriptionWrap = (() => {
            const description = subtitle;
            const descriptionRect = rectFor(description);
            const descriptionStyle = description ? getComputedStyle(description) : null;
            const titleGroupRect = rectFor(titleGroup);
            const titleGroupStyle = titleGroup ? getComputedStyle(titleGroup) : null;
            const titleGroupInnerWidth = titleGroup
              ? Math.round(
                  titleGroupRect.width
                  - pxNumber(titleGroupStyle?.paddingLeft)
                  - pxNumber(titleGroupStyle?.paddingRight)
                )
              : 0;
            const publishedMaxWidth = pxNumber(description?.dataset.titleDescriptionMaxWidth || "");
            const expectedText = "AI is not implemented; provider/model execution is blocked, and no prompt, file, memory, telemetry, or provider data leaves this machine.";
            const text = (description?.textContent || "").replace(/\\s+/g, " ").trim();
            const rectFromDomRect = (rect) => ({
              left: Math.round(rect.left),
              top: Math.round(rect.top),
              right: Math.round(rect.right),
              bottom: Math.round(rect.bottom),
              width: Math.round(rect.width),
              height: Math.round(rect.height)
            });
            const textNode = description
              ? [...description.childNodes].find((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim())
              : null;
            const wordMetrics = [];
            if (textNode) {
              const rawText = textNode.textContent || "";
              const wordPattern = /\\S+/g;
              let match = null;
              while ((match = wordPattern.exec(rawText)) !== null) {
                const range = document.createRange();
                range.setStart(textNode, match.index);
                range.setEnd(textNode, match.index + match[0].length);
                const rects = [...range.getClientRects()]
                  .filter((rect) => rect.width > 0 && rect.height > 0)
                  .map(rectFromDomRect);
                range.detach();
                const rect = rects[0] || { left: 0, top: 0, right: 0, bottom: 0, width: 0, height: 0 };
                wordMetrics.push({
                  text: match[0],
                  rect,
                  rects,
                  lineTop: rect.top,
                  withinDescription: descriptionRect.width > 0 && rect.left >= descriptionRect.left - 2 && rect.right <= descriptionRect.right + 2
                });
              }
            }
            const groupCount = description ? description.querySelectorAll(".monitoring-hud__subtitle-group").length : 0;
            const lineTops = [...new Set(wordMetrics.map((word) => word.lineTop).filter((top) => top > 0))];
            const lastPhraseMetrics = wordMetrics.slice(-6);
            const lastPhraseLineCount = new Set(lastPhraseMetrics.map((word) => word.lineTop).filter((top) => top > 0)).size;
            const lastPhraseText = lastPhraseMetrics.map((word) => word.text).join(" ");
            return {
              containerRect: descriptionRect,
              display: descriptionStyle?.display || "",
              flexWrap: descriptionStyle?.flexWrap || "",
              whiteSpace: descriptionStyle?.whiteSpace || "",
              overflowWrap: descriptionStyle?.overflowWrap || "",
              wordBreak: descriptionStyle?.wordBreak || "",
              maxWidth: descriptionStyle?.maxWidth || "",
              publishedMaxWidth: Math.round(publishedMaxWidth),
              titleGroupInnerWidth,
              columnSource: description?.dataset.titleDescriptionColumnSource || "",
              metadata: description?.dataset.titleDescriptionWrap || "",
              text,
              expectedTextPresent: text === expectedText,
              groupCount,
              lineCount: lineTops.length,
              wordCount: wordMetrics.length,
              noAtomicPhraseGroups: groupCount === 0,
              wordsCanWrapIndividually: wordMetrics.length > 0 && wordMetrics.every((word) => word.rect.width <= descriptionRect.width + 2),
              clippedWordCount: wordMetrics.filter((word) => !word.withinDescription).length,
              lastPhraseText,
              lastPhraseLineCount,
              lastPhraseWrapsByWord: lastPhraseText === "or provider data leaves this machine." && lastPhraseLineCount >= 2,
              measuredWidthMatchesTitleCardInner: Math.abs(Math.round(publishedMaxWidth) - titleGroupInnerWidth) <= 2,
              fixedLegacyMaxWidthRemoved: descriptionStyle ? descriptionStyle.maxWidth !== "600px" : false,
              containerUsesProseWordWrap: descriptionStyle
                ? !descriptionStyle.display.includes("flex") && descriptionStyle.whiteSpace === "normal"
                : false,
              wordMetrics,
              lastPhraseMetrics
            };
          })();
          const rowTitleSizingProbe = (() => {
            const hub = document.getElementById("ai-control-center-card-hub");
            const hubStyle = hub ? getComputedStyle(hub) : null;
            const derivedGutter = pxNumber(hubStyle?.getPropertyValue("--ai-dashboard-row-gutter"));
            const derivedVerticalGutter = pxNumber(hubStyle?.getPropertyValue("--ai-dashboard-row-vertical-gutter"));
            const declaredLabelColumnWidthRaw = hubStyle?.getPropertyValue("--ai-dashboard-row-label-width") || "";
            const declaredLabelColumnWidthIsPx = /^\\s*\\d+(?:\\.\\d+)?px\\s*$/.test(declaredLabelColumnWidthRaw);
            const declaredLabelColumnWidth = declaredLabelColumnWidthIsPx ? pxNumber(declaredLabelColumnWidthRaw) : 0;
            const rows = [...document.querySelectorAll(".ai-control-center-card-rows .monitoring-hud__state-row")];
            const rowStackMetrics = [...document.querySelectorAll(".ai-control-center-card-rows")].map((stack, stackIndex) => {
              const stackStyle = getComputedStyle(stack);
              const stackRows = [...stack.querySelectorAll(".monitoring-hud__state-row")];
              const pairGaps = stackRows.slice(1).map((row, index) => {
                const previousRect = stackRows[index].getBoundingClientRect();
                const rowRect = row.getBoundingClientRect();
                return Math.round(rowRect.top - previousRect.bottom);
              });
              const rowGapPx = Math.round(pxNumber(stackStyle.rowGap || stackStyle.gap));
              return {
                stackIndex,
                rowCount: stackRows.length,
                rowGapPx,
                expectedRowVerticalGutterPx: Math.round(derivedVerticalGutter),
                pairGaps,
                rowGapMatchesToken: Math.abs(rowGapPx - derivedVerticalGutter) <= 1,
                pairGapsMatchToken: pairGaps.every((gap) => Math.abs(gap - derivedVerticalGutter) <= 1)
              };
            });
            const labelWidths = rows.map((row) => {
              const label = row.querySelector("span");
              const labelRect = rectFor(label);
              return Math.ceil(Math.max(labelRect.width || 0, label?.scrollWidth || 0));
            });
            const measuredMaxLabelWidth = labelWidths.length ? Math.max(...labelWidths) : 0;
            const contractLabelColumnWidth = Math.round(declaredLabelColumnWidth);
            const rowMetrics = rows.map((row, index) => {
              const rowRect = rectFor(row);
              const style = getComputedStyle(row);
              const label = row.querySelector("span");
              const value = row.querySelector("strong");
              const labelRect = rectFor(label);
              const valueRect = rectFor(value);
              const labelStyle = label ? getComputedStyle(label) : null;
              const titleColumnWidth = firstGridColumnWidth(style.gridTemplateColumns);
              const labelWraps = labelRect.height > lineHeightNumber(labelStyle, labelRect) * 1.35;
              const valueColumnOffset = Math.round(valueRect.left - rowRect.left);
              const expectedValueColumnOffset = Math.round(contractLabelColumnWidth + derivedGutter);
              const fixedColumnGutterPx = Math.round(valueColumnOffset - titleColumnWidth);
              const visibleLabelToValueGutterPx = Math.round(valueRect.left - labelRect.right);
              return {
                index,
                key: `${label?.textContent.trim() || ""}|${value?.textContent.trim() || ""}`,
                label: label?.textContent.trim() || "",
                value: value?.textContent.trim() || "",
                labelFontSize: labelStyle?.fontSize || "",
                valueFontSize: value ? getComputedStyle(value).fontSize : "",
                gridTemplateColumns: style.gridTemplateColumns,
                titleColumnWidth: Math.round(titleColumnWidth),
                labelWidth: labelRect.width,
                rowLeft: rowRect.left,
                rowGutterPx: Math.round(derivedGutter),
                fixedColumnGutterPx,
                visibleLabelToValueGutterPx,
                valueColumnOffset,
                expectedValueColumnOffset,
                valueLeft: valueRect.left,
                rowRight: rowRect.right,
                labelWraps,
                titleColumnContentExcessPx: Math.round(titleColumnWidth - labelRect.width),
                titleColumnMatchesContract: Math.abs(titleColumnWidth - contractLabelColumnWidth) <= 2,
                valueColumnOffsetMatchesContract: Math.abs(valueColumnOffset - expectedValueColumnOffset) <= 2,
                fixedColumnGutterMatchesToken: Math.abs(fixedColumnGutterPx - derivedGutter) <= 2,
                visibleGutterAtLeastFixedGutter: visibleLabelToValueGutterPx >= derivedGutter - 2,
                labelWithinRow: labelRect.left >= rowRect.left - 2 && labelRect.right <= rowRect.right + 2,
                valueWithinRow: valueRect.left >= rowRect.left - 2 && valueRect.right <= rowRect.right + 2
              };
            });
            const valueOffsets = rowMetrics.map((row) => row.valueColumnOffset);
            const uniformValueColumnOffset = valueOffsets.length
              ? Math.max(...valueOffsets) - Math.min(...valueOffsets) <= 2
              : false;
            const valueLefts = rowMetrics.map((row) => Math.round(row.valueLeft));
            const uniformValueLeftEdge = valueLefts.length
              ? Math.max(...valueLefts) - Math.min(...valueLefts) <= 2
              : false;
            const maxLabelColumnExcess = Math.abs(contractLabelColumnWidth - measuredMaxLabelWidth);
            const maxTitleColumnExcess = rowMetrics.length
              ? Math.max(...rowMetrics.map((row) => Math.abs(row.titleColumnWidth - contractLabelColumnWidth)))
              : 999;
            const declaredLabelColumnMatchesMeasuredMax = declaredLabelColumnWidthIsPx
              && contractLabelColumnWidth > 0
              && maxLabelColumnExcess <= 2;
            return {
              rowCount: rowMetrics.length,
              labelColumnSource: hub?.dataset.rowLabelColumnSource || "",
              labelColumnUnit: hub?.dataset.rowLabelColumnUnit || "",
              rowValueColumnContract: hub?.dataset.rowValueColumnContract || "",
              measuredMaxLabelWidth: Math.round(measuredMaxLabelWidth),
              declaredLabelColumnWidthRaw: declaredLabelColumnWidthRaw.trim(),
              declaredLabelColumnWidthIsPx,
              declaredLabelColumnWidth: Math.round(declaredLabelColumnWidth),
              contractLabelColumnWidth,
              rowGutterPx: Math.round(derivedGutter),
              rowVerticalGutterPx: Math.round(derivedVerticalGutter),
              rowVerticalGutterRestored: rowStackMetrics.every((stack) => stack.rowCount < 2 || (stack.rowGapMatchesToken && stack.pairGapsMatchToken)),
              rowStackMetrics,
              contentSized: rowMetrics.every((row) => (
                !row.labelWraps
                && row.titleColumnMatchesContract
                && row.valueColumnOffsetMatchesContract
                && row.fixedColumnGutterMatchesToken
                && row.visibleGutterAtLeastFixedGutter
              )) && declaredLabelColumnMatchesMeasuredMax && maxTitleColumnExcess <= 2 && uniformValueColumnOffset && uniformValueLeftEdge,
              noLabelClipping: rowMetrics.every((row) => row.labelWithinRow),
              noValueClipping: rowMetrics.every((row) => row.valueWithinRow),
              labelValueFontSizeParity: rowMetrics.every((row) => row.labelFontSize === row.valueFontSize),
              valueColumnDerivedFromLabelContent: rowMetrics.every((row) => row.valueColumnOffsetMatchesContract),
              valueColumnDerivedFromMaxLabelContent: rowMetrics.every((row) => row.valueColumnOffsetMatchesContract),
              declaredLabelColumnMatchesMeasuredMax,
              fixedColumnGutterRestored: rowMetrics.every((row) => row.fixedColumnGutterMatchesToken),
              uniformValueColumnOffset,
              uniformValueLeftEdge,
              visibleRowGutterAtLeastFixedGutter: rowMetrics.every((row) => row.visibleGutterAtLeastFixedGutter),
              maxTitleColumnExcessPx: maxTitleColumnExcess,
              maxLabelColumnExcessPx: maxLabelColumnExcess,
              rowMetrics
            };
          })();
          return JSON.stringify({
            clippedCount: clipped.length,
            clipped,
            hubClientWidth: hub ? Math.round(hub.clientWidth) : 0,
            titleGroupWidth: titleGroup ? Math.round(titleGroup.getBoundingClientRect().width) : 0,
            settingsVisible: Boolean(settingsRect && settingsRect.width > 0 && settingsRect.height > 0),
            stripSettingsOverlap: Boolean(stripRect && settingsRect && stripRect.right > settingsRect.left - 4 && stripRect.bottom > settingsRect.top && stripRect.top < settingsRect.bottom),
            maxScroll: hub ? Math.round(Math.max(0, hub.scrollHeight - hub.clientHeight)) : 0,
            titleStatusPillWrap,
            titleDescriptionWrap,
            rowTitleSizingProbe
          });
        })();
        """,
        )
        try:
            return json.loads(layout_raw or "{}")
        except Exception:
            return {"raw": str(layout_raw or "")}

    def _drag_to_width(target_width: int, screenshot_name: str, crop_name: str) -> dict[str, object]:
        before = _rect(int(dialog.winId()))
        if before["width"] <= 0:
            return {"ok": False, "reason": "missing-window-rect", "before": before}
        available = dialog._available_desktop_geometry()
        max_target_width = max(dialog.minimumWidth(), available.width() - 20)
        bounded_target_width = max(dialog.minimumWidth(), min(int(target_width), max_target_width))
        if bounded_target_width == before["width"]:
            bounded_target_width = max(dialog.minimumWidth(), min(before["width"] - 20, max_target_width))
        start = QPoint(before["right"] - max(2, dialog.RESIZE_MARGIN // 2), before["top"] + before["height"] // 2)
        end = QPoint(start.x() + (bounded_target_width - before["width"]), start.y())
        SetCursorPos(start.x(), start.y())
        _pump(app, 120)
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        _pump(app, 140)
        started = bool(getattr(dialog, "_resize_active", False))
        cursor_points = [{"x": start.x(), "y": start.y(), "phase": "mouse-down"}]
        for step in range(1, 10):
            x = start.x() + int(round((end.x() - start.x()) * (step / 9)))
            point = QPoint(x, start.y())
            SetCursorPos(point.x(), point.y())
            mouse_event(MOUSEEVENTF_MOVE, 0, 0, 0, 0)
            cursor_points.append({"x": point.x(), "y": point.y(), "phase": f"drag-step-{step}"})
            _pump(app, 45)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        cursor_points.append({"x": end.x(), "y": end.y(), "phase": "mouse-up"})
        _pump(app, 260)
        after = _rect(int(dialog.winId()))
        screenshots = _capture_window(app, dialog, log_root, screenshot_name)
        layout = _read_layout()
        wrap_crop = _capture_window_region(
            app,
            dialog,
            log_root,
            crop_name,
            (layout.get("titleStatusPillWrap") or {}).get("copyRect") if isinstance(layout, dict) else {},
        )
        title_description_wrap_crop = _capture_window_region(
            app,
            dialog,
            log_root,
            f"{crop_name}_title_description",
            (layout.get("titleDescriptionWrap") or {}).get("containerRect") if isinstance(layout, dict) else {},
        )
        return {
            "proofPath": "ai-control-center-right-edge-windows-cursor-drag",
            "hudResizePathSubset": "HUD Dashboard active right-edge cursor drag live resize proof subset",
            "inputMethod": "windows-cursor-left-button-drag",
            "codeForcedGeometry": False,
            "runtimeResizeEventStarted": started,
            "started": started,
            "cursorDragPoints": cursor_points,
            "before": before,
            "after": after,
            "targetWidth": bounded_target_width,
            "minimumWidth": int(dialog.minimumWidth()),
            "minimumHeight": int(dialog.minimumHeight()),
            "widthDelta": after["width"] - before["width"],
            "heightDelta": after["height"] - before["height"],
            "layout": layout,
            "wrapCrop": wrap_crop,
            "titleDescriptionWrapCrop": title_description_wrap_crop,
            "screenshots": screenshots,
        }

    no_early_target_width = max(dialog.minimumWidth(), min(578, dialog._available_desktop_geometry().width() - 20))
    no_early = _drag_to_width(
        no_early_target_width,
        "03_dashboard_horizontal_shrink_no_early_wrap",
        "15_title_status_pill_no_early_wrap_windows_cursor_resize",
    )
    natural = _drag_to_width(
        int(dialog.minimumWidth()),
        "03_dashboard_horizontal_shrink",
        "16_title_status_pill_wrapped_windows_cursor_resize",
    )
    natural_attempts = [natural]

    def _natural_wrap_attempt_ok(proof: object) -> bool:
        if not isinstance(proof, dict):
            return False
        layout = proof.get("layout") if isinstance(proof.get("layout"), dict) else {}
        wrap = layout.get("titleStatusPillWrap") if isinstance(layout.get("titleStatusPillWrap"), dict) else {}
        after = proof.get("after") if isinstance(proof.get("after"), dict) else {}
        crop = proof.get("wrapCrop") if isinstance(proof.get("wrapCrop"), dict) else {}
        return (
            proof.get("started") is True
            and int(after.get("width") or 999) <= 470
            and int(after.get("width") or 0) >= dialog.minimumWidth()
            and int(layout.get("clippedCount") or 0) == 0
            and layout.get("stripSettingsOverlap") is False
            and int(wrap.get("lineCount") or 0) >= 2
            and wrap.get("groupsAtomic") is True
            and int(wrap.get("clippedPairCount", 999)) == 0
            and crop.get("ok") is True
        )

    retry_index = 1
    while not _natural_wrap_attempt_ok(natural) and retry_index <= 2:
        natural = _drag_to_width(
            int(dialog.minimumWidth()),
            f"03_dashboard_horizontal_shrink_retry_{retry_index}",
            f"16_title_status_pill_wrapped_windows_cursor_resize_retry_{retry_index}",
        )
        natural_attempts.append(natural)
        retry_index += 1
    no_early_layout = no_early.get("layout") if isinstance(no_early, dict) else {}
    no_early_layout = no_early_layout if isinstance(no_early_layout, dict) else {}
    no_early_wrap = no_early_layout.get("titleStatusPillWrap") or {}
    natural_layout = natural.get("layout") if isinstance(natural, dict) else {}
    natural_layout = natural_layout if isinstance(natural_layout, dict) else {}
    natural_wrap = natural_layout.get("titleStatusPillWrap") or {}
    natural_after = natural.get("after") if isinstance(natural, dict) else {}
    natural_after = natural_after if isinstance(natural_after, dict) else {}
    no_early_after = no_early.get("after") if isinstance(no_early, dict) else {}
    no_early_after = no_early_after if isinstance(no_early_after, dict) else {}
    natural_crop = natural.get("wrapCrop") if isinstance(natural, dict) else {}
    natural_crop = natural_crop if isinstance(natural_crop, dict) else {}
    return {
        "ok": (
            no_early.get("started") is True
            and natural.get("started") is True
            and 560 <= int(no_early_after.get("width") or 0) <= 590
            and int(natural_after.get("width") or 999) <= 470
            and int(natural_after.get("width") or 0) >= dialog.minimumWidth()
            and int(no_early_layout.get("clippedCount") or 0) == 0
            and int(natural_layout.get("clippedCount") or 0) == 0
            and no_early_layout.get("stripSettingsOverlap") is False
            and natural_layout.get("stripSettingsOverlap") is False
            and int(no_early_wrap.get("lineCount") or 0) == 1
            and no_early_wrap.get("groupsAtomic") is True
            and int(no_early_wrap.get("clippedPairCount", 999)) == 0
            and int(natural_wrap.get("lineCount") or 0) >= 2
            and natural_wrap.get("groupsAtomic") is True
            and int(natural_wrap.get("clippedPairCount", 999)) == 0
            and natural_crop.get("ok") is True
        ),
        "proofPath": "ai-control-center-right-edge-windows-cursor-drag",
        "proofPathVariant": "two-stage-no-early-wrap-then-natural-wrap",
        "hudResizePathSubset": "HUD Dashboard active right-edge cursor drag live resize proof subset",
        "inputMethod": "windows-cursor-left-button-drag",
        "codeForcedGeometry": False,
        "runtimeResizeEventStarted": no_early.get("started") is True and natural.get("started") is True,
        "started": no_early.get("started") is True and natural.get("started") is True,
        "cursorDragPoints": {
            "noEarlyWrap": no_early.get("cursorDragPoints") or [],
            "naturalWrap": natural.get("cursorDragPoints") or [],
        },
        "before": initial,
        "after": natural_after,
        "targetWidth": int(dialog.minimumWidth()),
        "minimumWidth": int(dialog.minimumWidth()),
        "minimumHeight": int(dialog.minimumHeight()),
        "widthDelta": int(natural_after.get("width") or 0) - initial["width"],
        "heightDelta": int(natural_after.get("height") or 0) - initial["height"],
        "layout": natural_layout,
        "wrapCrop": natural_crop,
        "titleDescriptionWrapCrop": natural.get("titleDescriptionWrapCrop") or {},
        "screenshots": natural.get("screenshots") or {},
        "noEarlyWrapProof": no_early,
        "naturalWrapProof": natural,
        "naturalWrapAttempts": natural_attempts,
    }


def _capture_main_runtime_ai_control_center_reference(log_root: Path) -> dict[str, object]:
    main_root = Path("C:/Nexus Desktop AI")
    launcher = Path.home() / "OneDrive" / "Desktop" / "MAIN GREEN - Nexus Desktop AI Launcher.lnk"
    focused_path = log_root / "09_main_runtime_old_ai_control_center_focused_window.png"
    desktop_path = log_root / "10_main_runtime_old_ai_control_center_full_desktop.png"
    script_path = log_root / "_capture_main_runtime_ai_control_center_reference.py"
    metadata_path = log_root / "main_runtime_old_ai_control_center_reference.json"
    state_path = log_root / "main_runtime_ai_control_center_state.json"
    if not main_root.exists():
        return {
            "ok": False,
            "referenceSource": str(main_root),
            "launcher": str(launcher),
            "reason": "main-runtime-root-missing",
        }
    script_path.write_text(
        f"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication

main_root = Path({json.dumps(str(main_root))})
focused_path = Path({json.dumps(str(focused_path))})
desktop_path = Path({json.dumps(str(desktop_path))})
metadata_path = Path({json.dumps(str(metadata_path))})
state_path = Path({json.dumps(str(state_path))})

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["NEXUS_AI_CONTROL_CENTER_STATE_PATH"] = str(state_path)
os.environ.pop("NEXUS_AI_CONTROL_CENTER_ENABLE_GEOMETRY_MEMORY", None)
sys.path.insert(0, str(main_root))

from desktop.ai_provider_state import build_default_provider_readiness_config, build_provider_setup_completion_foundation_state  # noqa: E402
from desktop.desktop_renderer import AIControlCenterDialog  # noqa: E402


def pump(app: QApplication, duration_ms: int = 80) -> None:
    deadline = time.monotonic() + max(0, duration_ms) / 1000.0
    while time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()


def run_js(app: QApplication, dialog: AIControlCenterDialog, script: str, timeout_ms: int = 1500):
    box = {{"done": False, "result": None}}

    def complete(result):
        box["result"] = result
        box["done"] = True

    dialog.webview.page().runJavaScript(script, complete)
    deadline = time.monotonic() + max(0, timeout_ms) / 1000.0
    while not box["done"] and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    return box.get("result")


app = QApplication.instance() or QApplication(sys.argv)
screen = QApplication.primaryScreen()
if screen is None:
    raise RuntimeError("No primary screen available for main runtime reference")
events = []
provider_state = build_provider_setup_completion_foundation_state(
    build_default_provider_readiness_config(),
    surface_role="hud",
)
dialog = AIControlCenterDialog(screen, event_logger=events.append)
dialog.update_provider_state(provider_state.as_renderer_payload())
available = screen.availableGeometry()
dialog.setGeometry(
    QRect(
        available.x() + max(40, available.width() - dialog.DEFAULT_WIDTH - 120),
        available.y() + 80,
        dialog.DEFAULT_WIDTH,
        dialog.DEFAULT_HEIGHT,
    )
)
dialog.show_from_tray()
pump(app, 900)
focused_saved = bool(dialog.grab().save(str(focused_path)))
pump(app, 80)
desktop_saved = bool(screen.grabWindow(0).save(str(desktop_path)))
probe_raw = run_js(
    app,
    dialog,
    \"\"\"
    (() => {{
      const surface = document.getElementById("monitoring-hud");
      return JSON.stringify({{
        title: document.querySelector(".monitoring-hud__title")?.textContent.trim() || "",
        subtitle: document.querySelector(".monitoring-hud__subtitle")?.textContent.replace(/\\\\s+/g, " ").trim() || "",
        surfaceId: surface?.dataset.surfaceId || "",
        productSurfaceRole: surface?.dataset.productSurfaceRole || "",
        defaultWindowWidth: surface?.dataset.defaultWindowWidth || "",
        defaultWindowHeight: surface?.dataset.defaultWindowHeight || "",
        cardTitles: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-card-title-copy strong, .monitoring-hud__hub-card-title-copy strong")].map((node) => node.textContent.trim()),
        bodyTextSample: document.body.innerText.replace(/\\\\s+/g, " ").trim().slice(0, 500)
      }});
    }})();
    \"\"\",
)
try:
    probe = json.loads(probe_raw or "{{}}")
except Exception:
    probe = {{"rawProbe": str(probe_raw or "")}}
visual_grammar_script = {json.dumps(_VISUAL_GRAMMAR_PROBE_SCRIPT)}
visual_grammar_raw = run_js(app, dialog, visual_grammar_script, 2500)
try:
    probe["visualGrammar"] = json.loads(visual_grammar_raw or "{{}}")
except Exception:
    probe["visualGrammar"] = {{"ok": False, "raw": str(visual_grammar_raw or "")}}
metadata = {{
    "ok": bool(focused_saved and desktop_saved and focused_path.exists() and desktop_path.exists()),
    "referenceKind": "main-worktree-old-ai-control-center-runtime",
    "referenceSource": str(main_root),
    "focusedWindow": str(focused_path),
    "fullDesktop": str(desktop_path),
    "windowTitle": dialog.windowTitle(),
    "defaultWidth": int(dialog.DEFAULT_WIDTH),
    "defaultHeight": int(dialog.DEFAULT_HEIGHT),
    "minimumWidth": int(dialog.minimumWidth()),
    "minimumHeight": int(dialog.minimumHeight()),
    "probe": probe,
    "events": events,
}}
metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
print(json.dumps(metadata, sort_keys=True))
dialog.close()
pump(app, 300)
""".strip()
        + "\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["NEXUS_AI_CONTROL_CENTER_STATE_PATH"] = str(state_path)
    env.pop("NEXUS_AI_CONTROL_CENTER_ENABLE_GEOMETRY_MEMORY", None)
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(main_root),
        env=env,
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    stdout_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    metadata: dict[str, object] = {}
    if stdout_lines:
        try:
            metadata = json.loads(stdout_lines[-1])
        except Exception:
            metadata = {}
    ok = bool(metadata.get("ok")) and result.returncode == 0
    return {
        "ok": ok,
        "referenceKind": "main-worktree-old-ai-control-center-runtime",
        "referenceSource": str(main_root),
        "desktopLauncher": str(launcher),
        "launcherExists": launcher.exists(),
        "focusedWindow": str(focused_path),
        "fullDesktop": str(desktop_path),
        "metadataPath": str(metadata_path),
        "captureScript": str(script_path),
        "returnCode": result.returncode,
        "stdoutTail": stdout_lines[-3:],
        "stderrTail": result.stderr.splitlines()[-10:],
        "metadata": metadata,
        "reason": "" if ok else "main-runtime-reference-capture-failed",
    }


def _ai_dashboard_resize_hit_zone_probe(app: QApplication, dialog: AIControlCenterDialog) -> dict[str, object]:
    width = int(dialog.width())
    height = int(dialog.height())
    center_x = width // 2
    center_y = height // 2
    edge_sample_inset = max(4, min(10, int(dialog.RESIZE_MARGIN) // 2))
    corner_sample_inset = max(edge_sample_inset + 12, min(24, int(dialog.RESIZE_MARGIN) + 4))
    right_edge_x = max(0, width - 1 - edge_sample_inset)
    bottom_edge_y = max(0, height - 1 - edge_sample_inset)
    bottom_corner_y = max(0, height - 1 - corner_sample_inset)
    sample_points = {
        "left": QPoint(edge_sample_inset, center_y),
        "right": QPoint(right_edge_x, center_y),
        "top": QPoint(center_x, edge_sample_inset),
        "bottom": QPoint(center_x, bottom_edge_y),
        "topLeft": QPoint(corner_sample_inset, corner_sample_inset),
        "topRight": QPoint(right_edge_x, corner_sample_inset),
        "bottomLeft": QPoint(corner_sample_inset, bottom_corner_y),
        "bottomRight": QPoint(right_edge_x, bottom_corner_y),
        "innerContent": QPoint(max(48, dialog.RESIZE_MARGIN + 28), max(220, dialog.RESIZE_MARGIN + 80)),
        "windowControls": dialog._ai_control_center_close_zone().center(),
    }
    expected_resize_samples = {
        "left",
        "right",
        "top",
        "bottom",
        "topLeft",
        "topRight",
        "bottomLeft",
        "bottomRight",
    }
    samples: dict[str, dict[str, object]] = {}
    for name, point in sample_points.items():
        edges = dialog._ai_control_center_resize_edges_for_local_pos(point)
        hit_test = int(dialog._ai_control_center_resize_hit_test_for_edges(edges))
        global_point = dialog.mapToGlobal(point)
        expected_hover_key = list(dialog._ai_control_center_resize_edge_key(edges)) if edges else None
        dialog._reset_ai_control_center_resize_cursor()
        SetCursorPos(int(global_point.x()), int(global_point.y()))
        _pump(app, 120)
        dialog._poll_ai_control_center_resize_hover_cursor()
        actual_hover_key = (
            list(dialog._resize_cursor_key)
            if isinstance(dialog._resize_cursor_key, tuple)
            else dialog._resize_cursor_key
        )
        samples[name] = {
            "localPoint": {"x": point.x(), "y": point.y()},
            "globalPoint": {"x": global_point.x(), "y": global_point.y()},
            "edges": {
                "left": bool(edges & Qt.LeftEdge),
                "right": bool(edges & Qt.RightEdge),
                "top": bool(edges & Qt.TopEdge),
                "bottom": bool(edges & Qt.BottomEdge),
            },
            "hitTest": hit_test,
            "expectedHoverKey": expected_hover_key,
            "hoverCursorKey": actual_hover_key,
            "hoverCursorMatchesEdges": actual_hover_key == expected_hover_key,
            "expectedResize": name in expected_resize_samples,
        }
    dialog._reset_ai_control_center_resize_cursor()
    expected_ok = all(samples[name]["hitTest"] != 0 for name in expected_resize_samples)
    non_edge_ok = samples["innerContent"]["hitTest"] == 0 and samples["windowControls"]["hitTest"] == 0
    hover_ok = all(samples[name]["hoverCursorMatchesEdges"] is True for name in expected_resize_samples)
    return {
        "ok": expected_ok and non_edge_ok and hover_ok,
        "resizeMarginPx": int(dialog.RESIZE_MARGIN),
        "sampleInsetPx": edge_sample_inset,
        "edgeSampleInsetPx": edge_sample_inset,
        "cornerSampleInsetPx": corner_sample_inset,
        "expectedResizeSamples": sorted(expected_resize_samples),
        "samples": samples,
        "expectedResizeSamplesHit": expected_ok,
        "nonEdgeSamplesClear": non_edge_ok,
        "hoverCursorSamplesStable": hover_ok,
    }


def _button_rect(app: QApplication, web_window, button_id: str) -> dict[str, int | str | bool]:
    raw = _run_child_js(
        app,
        web_window,
        f"""
        (() => {{
          const button = document.getElementById({json.dumps(button_id)});
          if (!button) return JSON.stringify({{ ok: false, reason: "missing-button" }});
          button.scrollIntoView({{ block: "center", inline: "center", behavior: "instant" }});
          const rect = button.getBoundingClientRect();
          return JSON.stringify({{
            ok: true,
            id: button.id || "",
            text: button.textContent.trim(),
            left: Math.round(rect.left),
            top: Math.round(rect.top),
            width: Math.round(rect.width),
            height: Math.round(rect.height)
          }});
        }})();
        """,
    )
    return json.loads(raw or "{}")


def _click_web_button(app: QApplication, web_window, button_id: str) -> dict[str, object]:
    rect = _button_rect(app, web_window, button_id)
    if not rect.get("ok"):
        return {"ok": False, "button": button_id, "reason": rect.get("reason", "missing-button")}
    _foreground_window(app, web_window)
    point = QPoint(int(rect["left"]) + int(rect["width"]) // 2, int(rect["top"]) + int(rect["height"]) // 2)
    global_point = web_window.webview.mapToGlobal(point)
    SetCursorPos(int(global_point.x()), int(global_point.y()))
    _pump(app, 80)
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    _pump(app, 40)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    _pump(app, 500)
    return {
        "ok": True,
        "button": button_id,
        "text": rect.get("text", ""),
        "point": {"x": point.x(), "y": point.y()},
        "globalPoint": {"x": global_point.x(), "y": global_point.y()},
        "clickMode": "os-cursor-webview-coordinate",
    }


def _hover_web_button(app: QApplication, web_window, button_id: str) -> dict[str, object]:
    rect = _button_rect(app, web_window, button_id)
    if not rect.get("ok"):
        return {"ok": False, "button": button_id, "reason": rect.get("reason", "missing-button")}
    _foreground_window(app, web_window)
    point = QPoint(int(rect["left"]) + int(rect["width"]) // 2, int(rect["top"]) + int(rect["height"]) // 2)
    global_point = web_window.webview.mapToGlobal(point)
    SetCursorPos(int(global_point.x()), int(global_point.y()))
    _pump(app, 260)
    return {
        "ok": True,
        "button": button_id,
        "text": rect.get("text", ""),
        "point": {"x": point.x(), "y": point.y()},
        "globalPoint": {"x": global_point.x(), "y": global_point.y()},
        "hoverMode": "os-cursor-webview-coordinate",
    }


def _supporting_qtest_drag_child_window(app: QApplication, window, dx: int = 36, dy: int = 24) -> dict[str, object]:
    _foreground_window(app, window)
    before = _rect(int(window.winId()))
    start = QPoint(min(176, max(80, window.webview.width() // 3)), 46)
    end = QPoint(start.x() + dx, start.y() + dy)
    QTest.mousePress(window.webview, Qt.LeftButton, Qt.NoModifier, start)
    _pump(app, 60)
    QTest.mouseMove(window.webview, end, 120)
    _pump(app, 80)
    QTest.mouseRelease(window.webview, Qt.LeftButton, Qt.NoModifier, end)
    _pump(app, 220)
    after = _rect(int(window.winId()))
    return {
        "before": before,
        "after": after,
        "deltaLeft": after["left"] - before["left"],
        "deltaTop": after["top"] - before["top"],
        "moved": abs(after["left"] - before["left"]) >= 16 and abs(after["top"] - before["top"]) >= 12,
        "mode": "synthetic-qtest-webview-header-drag",
        "actor": "CODEX_AUTOMATION",
        "inputSource": "qt-qtest-direct-widget-event",
        "proofClass": "SUPPORTING_ONLY_SYNTHETIC_DIAGNOSTIC",
        "gatingValid": False,
        "maySetGatingPass": False,
        "closesDefect": False,
    }


def _supporting_qtest_resize_child_window(app: QApplication, window, dx: int = 44, dy: int = 34) -> dict[str, object]:
    _foreground_window(app, window)
    before = _rect(int(window.winId()))
    start = QPoint(max(2, window.webview.width() - 4), max(2, window.webview.height() - 4))
    end = QPoint(start.x() + dx, start.y() + dy)
    QTest.mousePress(window.webview, Qt.LeftButton, Qt.NoModifier, start)
    _pump(app, 60)
    QTest.mouseMove(window.webview, end, 140)
    _pump(app, 80)
    QTest.mouseRelease(window.webview, Qt.LeftButton, Qt.NoModifier, end)
    _pump(app, 260)
    after = _rect(int(window.winId()))
    return {
        "before": before,
        "after": after,
        "widthDelta": after["width"] - before["width"],
        "heightDelta": after["height"] - before["height"],
        "resized": after["width"] - before["width"] >= 22 and after["height"] - before["height"] >= 16,
        "mode": "synthetic-qtest-webview-bottom-right-edge-resize",
        "actor": "CODEX_AUTOMATION",
        "inputSource": "qt-qtest-direct-widget-event",
        "proofClass": "SUPPORTING_ONLY_SYNTHETIC_DIAGNOSTIC",
        "gatingValid": False,
        "maySetGatingPass": False,
        "closesDefect": False,
    }


def _supporting_native_hit_test_contract(window) -> dict[str, object]:
    width = window.width()
    height = window.height()
    drag_region = window._drag_region()
    drag_y = max(16, min(drag_region.bottom() - 2, 46))
    description_y = min(height - 24, max(drag_region.bottom() + 3, int(window._description_region_top) + 3))
    local_cases = {
        "caption": (QPoint(100, drag_y), 2),
        "descriptionExclusion": (QPoint(100, description_y), 1),
        "controlExclusion": (QPoint(max(1, width - 48), 30), 1),
        "content": (QPoint(width // 2, min(height - 24, 180)), 1),
        "transparentTopLeft": (QPoint(0, 0), 0),
        "outsideLeft": (QPoint(-1, height // 2), 0),
        "outsideRight": (QPoint(width, height // 2), 0),
        "outsideTop": (QPoint(width // 2, -1), 0),
        "outsideBottom": (QPoint(width // 2, height), 0),
        "left": (QPoint(2, height // 2), 10),
        "right": (QPoint(max(0, width - 2), height // 2), 11),
        "top": (QPoint(width // 2, 2), 12),
        "topLeft": (QPoint(8, 8), 13),
        "topRight": (QPoint(max(0, width - 8), 8), 14),
        "bottom": (QPoint(width // 2, max(0, height - 2)), 15),
        "bottomLeft": (QPoint(8, max(0, height - 8)), 16),
        "bottomRight": (QPoint(max(0, width - 8), max(0, height - 8)), 17),
    }
    results = {}
    for name, (local_point, expected) in local_cases.items():
        actual = int(window._native_hit_test(window.mapToGlobal(local_point)))
        results[name] = {
            "localPoint": {"x": local_point.x(), "y": local_point.y()},
            "expected": expected,
            "actual": actual,
            "matches": actual == expected,
        }
    boundary = window._boundary_contract_snapshot()
    boundary_samples = boundary.get("samples") if isinstance(boundary.get("samples"), dict) else {}
    boundary_ok = (
        boundary.get("contract") == "single-rounded-shell-mask-hit-rails-coincident-v2"
        and boundary.get("windowBounds") == boundary.get("visibleShellBounds")
        and boundary.get("windowBounds") == boundary.get("maskBounds")
        and boundary.get("boundaryInset") == 0
        and boundary.get("resizeRailsInsideVisibleShell") is True
        and boundary.get("outsideHitBehavior") == "noninteractive"
        and all(
            (boundary_samples.get(name) or {}).get("visibleShell") is False
            and int((boundary_samples.get(name) or {}).get("resizeEdges") or 0) == 0
            for name in ("outsideLeft", "outsideRight", "outsideTop", "outsideBottom", "transparentTopLeft")
        )
        and (boundary_samples.get("visibleTopLeftRail") or {}).get("visibleShell") is True
        and int((boundary_samples.get("visibleTopLeftRail") or {}).get("resizeEdges") or 0) != 0
    )
    return {
        "status": "SUPPORTING_DIAGNOSTIC_PASS"
        if all(item["matches"] for item in results.values()) and boundary_ok
        else "SUPPORTING_DIAGNOSTIC_FAIL",
        "actor": "CODEX_AUTOMATION",
        "inputSource": "direct-native-hit-test-contract-call",
        "proofClass": "SUPPORTING_ONLY_CODE_PATH_DIAGNOSTIC",
        "gatingValid": False,
        "maySetGatingPass": False,
        "closesDefect": False,
        "boundaryContract": boundary,
        "boundaryContractMatches": boundary_ok,
        "dragRegion": {
            "bottom": drag_region.bottom(),
            "descriptionTop": int(window._description_region_top),
        },
        "cases": results,
    }


def _supporting_minimum_geometry_scroll_probe(app: QApplication, window) -> dict[str, object]:
    before = QRect(window.geometry())
    window.resize(window.minimumWidth(), window.minimumHeight())
    _pump(app, 300)
    probe_script = """
        (() => {
          const chrome = document.querySelector('.ai-domain-window__chrome');
          const actions = document.querySelector('.ai-domain-window__actions');
          if (!chrome || !actions) return JSON.stringify({ok:false});
          const chromeRect = chrome.getBoundingClientRect();
          const actionRect = actions.getBoundingClientRect();
          return JSON.stringify({
            ok: true,
            clientHeight: Math.round(chrome.clientHeight),
            scrollHeight: Math.round(chrome.scrollHeight),
            scrollTop: Math.round(chrome.scrollTop),
            actionsFullyVisible: actionRect.top >= chromeRect.top && actionRect.bottom <= chromeRect.bottom
          });
        })();
    """
    before_scroll = _run_js(app, window, probe_script)
    _run_js(
        app,
        window,
        """
        (() => {
          const chrome = document.querySelector('.ai-domain-window__chrome');
          if (!chrome) return false;
          chrome.scrollTop = chrome.scrollHeight;
          return true;
        })();
        """,
    )
    _pump(app, 240)
    after_scroll = _run_js(app, window, probe_script)
    _run_js(
        app,
        window,
        "document.querySelector('.ai-domain-window__chrome') && "
        "(document.querySelector('.ai-domain-window__chrome').scrollTop = 0);",
    )
    window.setGeometry(before)
    _pump(app, 260)
    try:
        before_data = json.loads(before_scroll or "{}")
        after_data = json.loads(after_scroll or "{}")
    except json.JSONDecodeError:
        before_data = {"ok": False, "raw": str(before_scroll or "")}
        after_data = {"ok": False, "raw": str(after_scroll or "")}
    overflow_expected = int(before_data.get("scrollHeight") or 0) > int(before_data.get("clientHeight") or 0)
    reachable = before_data.get("actionsFullyVisible") is True or after_data.get("actionsFullyVisible") is True
    return {
        "status": "SUPPORTING_DIAGNOSTIC_PASS"
        if before_data.get("ok") is True and after_data.get("ok") is True and reachable
        else "SUPPORTING_DIAGNOSTIC_FAIL",
        "actor": "CODEX_AUTOMATION",
        "inputSource": "direct-window-geometry-api-plus-dom-javascript",
        "proofClass": "SUPPORTING_ONLY_SYNTHETIC_DIAGNOSTIC",
        "gatingValid": False,
        "maySetGatingPass": False,
        "closesDefect": False,
        "minimumSize": {"width": window.minimumWidth(), "height": window.minimumHeight()},
        "overflowExpected": overflow_expected,
        "beforeScroll": before_data,
        "afterScroll": after_data,
        "actionsReachable": reachable,
    }


def _open_from_dashboard(app: QApplication, dialog: AIControlCenterDialog, button_id: str, domain_id: str):
    before = set(dialog._domain_windows.keys())
    result = _run_js(
        app,
        dialog,
        f"""
        (() => {{
          const button = document.getElementById({json.dumps(button_id)});
          if (!button) return JSON.stringify({{ ok: false, reason: "missing-button" }});
          return JSON.stringify({{ ok: true, label: button.textContent.trim(), target: button.dataset.launchTarget || "", kind: button.dataset.launchWindowKind || "" }});
        }})();
        """,
    )
    click = _click_web_button(app, dialog, button_id)
    _pump(app, 700)
    window = dialog._domain_windows.get(domain_id)
    dom_click_fallback = {"ok": False, "skipped": True, "reason": "os-cursor-click-opened-window"}
    if window is None:
        raw_fallback = _run_js(
            app,
            dialog,
            f"""
            (() => {{
              const button = document.getElementById({json.dumps(button_id)});
              if (!button) return JSON.stringify({{ ok: false, reason: "missing-button" }});
              button.click();
              return JSON.stringify({{ ok: true, button: {json.dumps(button_id)}, clickMode: "dom-button-click-fallback" }});
            }})();
            """,
        )
        try:
            dom_click_fallback = json.loads(raw_fallback or "{}")
        except Exception:
            dom_click_fallback = {"ok": False, "raw": str(raw_fallback or "")}
        _pump(app, 700)
        window = dialog._domain_windows.get(domain_id)
    return {"probe": json.loads(result or "{}"), "realClick": click, "domClickFallback": dom_click_fallback}, window, before


def _probe_child_window(app: QApplication, window) -> dict[str, object]:
    if window is None:
        return {"ok": False, "reason": "missing-window"}
    raw = _run_child_js(
        app,
        window,
        """
        (() => {
          const surface = document.querySelector("[data-ai-dashboard-child-window]");
          const title = document.querySelector(".ai-domain-window__title");
          const cssText = Array.from(document.styleSheets).map((sheet) => {
            try {
              return Array.from(sheet.cssRules || []).map((rule) => rule.cssText || "").join("\\n");
            } catch (error) {
              return "";
            }
          }).join("\\n");
          const rectFor = (node) => {
            if (!node) return null;
            const rect = node.getBoundingClientRect();
            return {
              left: Math.round(rect.left),
              top: Math.round(rect.top),
              right: Math.round(rect.right),
              bottom: Math.round(rect.bottom),
              width: Math.round(rect.width),
              height: Math.round(rect.height)
            };
          };
          const styleFor = (node) => {
            if (!node) return {};
            const style = getComputedStyle(node);
            return {
              display: style.display,
              gridTemplateColumns: style.gridTemplateColumns,
              gap: style.gap,
              columnGap: style.columnGap,
              rowGap: style.rowGap,
              padding: `${style.paddingTop} ${style.paddingRight} ${style.paddingBottom} ${style.paddingLeft}`,
              fontSize: style.fontSize,
              fontWeight: style.fontWeight,
              letterSpacing: style.letterSpacing,
              color: style.color,
              backgroundColor: style.backgroundColor,
              backgroundImage: style.backgroundImage,
              borderRadius: style.borderRadius,
              borderTopWidth: style.borderTopWidth,
              borderTopColor: style.borderTopColor,
              boxShadow: style.boxShadow,
              overflow: style.overflow,
              whiteSpace: style.whiteSpace
            };
          };
          const textForNode = (node) => (node?.textContent || "").replace(/\\s+/g, " ").trim();
          const group = (name, selector) => {
            const node = document.querySelector(selector);
            return {
              name,
              selector,
              present: Boolean(node),
              rect: rectFor(node),
              style: styleFor(node),
              text: textForNode(node).slice(0, 220)
            };
          };
          const all = (selector) => [...document.querySelectorAll(selector)].map((node, index) => ({
            index,
            rect: rectFor(node),
            style: styleFor(node),
            text: textForNode(node).slice(0, 220),
            id: node.id || "",
            dataset: Object.assign({}, node.dataset || {})
          }));
          const workspaceNodes = [...document.querySelectorAll("[data-domain-workspace]")];
          const controlWorkspace = document.querySelector("[data-domain-workspace='control-center']");
          const readinessWorkspace = document.querySelector("[data-domain-workspace='readiness-diagnostics']");
          const capabilityWorkspace = document.querySelector("[data-domain-workspace='capabilities-maintenance']");
          const controls = [...document.querySelectorAll("[data-domain-command='window-minimize'], [data-domain-command='window-close']")];
          const actionButtons = [...document.querySelectorAll(".ai-domain-window__button")].map((button) => ({
            id: button.id || "",
            text: button.textContent.trim(),
            command: button.dataset.domainCommand || "",
            disabled: Boolean(button.disabled),
            ariaDisabled: button.getAttribute("aria-disabled") || "",
            ariaPressed: button.getAttribute("aria-pressed") || ""
          }));
          const textFor = (id) => document.getElementById(id)?.textContent.trim() || "";
          return JSON.stringify({
            domDomain: surface?.dataset.aiDashboardChildWindow || "",
            domClassification: surface?.dataset.windowClassification || "",
            domLifecycle: surface?.dataset.windowLifecycle || "",
            nativeChrome: surface?.dataset.ndaiNativeChrome || "",
            genericOsChrome: surface?.dataset.genericOsChrome || "",
            shellConformance: surface?.dataset.shellConformance || "",
            boundaryContract: surface?.dataset.windowBoundaryContract || "",
            boundaryInset: surface?.dataset.windowBoundaryInset || "",
            resizeRailLocation: surface?.dataset.windowResizeRailLocation || "",
            outsideHitBehavior: surface?.dataset.windowOutsideHitBehavior || "",
            move: surface?.dataset.windowMove || "",
            descriptionDrag: surface?.dataset.windowDescriptionDrag || "",
            resize: surface?.dataset.windowResize || "",
            defaultGeometryContract: surface?.dataset.windowDefaultGeometryContract || "",
            supportedGeometryContract: surface?.dataset.windowSupportedGeometryContract || "",
            maximumUsefulSize: surface?.dataset.windowMaximumUsefulSize || "",
            maximizeFullscreenPolicy: surface?.dataset.windowMaximizeFullscreenPolicy || "",
            reopenGeometryContract: surface?.dataset.windowReopenGeometryContract || "",
            shellVisualContract: surface?.dataset.windowShellVisualContract || "",
            initialContentFitApplied: surface?.dataset.initialContentFitApplied || "",
            measuredContentHeight: surface?.dataset.measuredContentHeight || "",
            defaultContentFitHeight: surface?.dataset.defaultContentFitHeight || "",
            defaultOverflowContract: surface?.dataset.defaultOverflowContract || "",
            measuredDragRegionBottom: surface?.dataset.measuredDragRegionBottom || "",
            measuredDescriptionTop: surface?.dataset.measuredDescriptionTop || "",
            controlCluster: surface?.dataset.windowControlCluster || "",
            stateTaxonomyContract: surface?.dataset.stateTaxonomyContract || "",
            stateTaxonomySource: surface?.dataset.stateTaxonomySource || "",
            stateTaxonomyScope: surface?.dataset.stateTaxonomyScope || "",
            stateTaxonomyRequiredStates: surface?.dataset.stateTaxonomyRequiredStates || "",
            stateTaxonomyRenderedStates: surface?.dataset.stateTaxonomyRenderedStates || "",
            stateTaxonomyComplete: surface?.dataset.stateTaxonomyComplete || "",
            rowLabelColumnSource: surface?.dataset.rowLabelColumnSource || "",
            rowValueColumnContract: surface?.dataset.rowValueColumnContract || "",
            rowValueGutter: surface?.dataset.rowValueGutter || "",
            rowVerticalGutter: surface?.dataset.rowVerticalGutter || "",
            materialGroups: {
              shell: group("shell", ".ai-domain-window"),
              chrome: group("chrome", ".ai-domain-window__chrome"),
              controls: group("controls", ".ai-domain-window__controls"),
              controlButton: group("controlButton", ".ai-domain-window__control"),
              header: group("header", ".ai-domain-window__header"),
              dragRegion: group("dragRegion", ".ai-domain-window__drag-region"),
              kicker: group("kicker", ".ai-domain-window__kicker"),
              title: group("title", ".ai-domain-window__title"),
              description: group("description", ".ai-domain-window__description"),
              card: group("card", ".ai-domain-window__card"),
              cardHeading: group("cardHeading", ".ai-domain-window__card-heading"),
              cardNumber: group("cardNumber", ".ai-domain-window__card-number"),
              cardTitle: group("cardTitle", ".ai-domain-window__card-title"),
              cardDescription: group("cardDescription", ".ai-domain-window__card-description"),
              rows: group("rows", ".ai-domain-window__rows"),
              row: group("row", ".ai-domain-window__row"),
              rowLabel: group("rowLabel", ".ai-domain-window__row span"),
              rowValue: group("rowValue", ".ai-domain-window__row strong"),
              actions: group("actions", ".ai-domain-window__actions"),
              button: group("button", ".ai-domain-window__button")
            },
            elementInventory: {
              rows: all(".ai-domain-window__row").map((row) => ({
                index: row.index,
                text: row.text,
                rect: row.rect,
                gridTemplateColumns: row.style.gridTemplateColumns,
                columnGap: row.style.columnGap,
                rowGap: row.style.rowGap,
                label: document.querySelectorAll(".ai-domain-window__row")[row.index]?.querySelector("span")?.textContent.trim() || "",
                value: document.querySelectorAll(".ai-domain-window__row")[row.index]?.querySelector("strong")?.textContent.trim() || ""
              })),
              buttons: all(".ai-domain-window__button"),
              controls: all(".ai-domain-window__control")
            },
            cssStateSelectors: {
              buttonHover: cssText.includes(".ai-domain-window__button:hover"),
              buttonFocus: cssText.includes(".ai-domain-window__button:focus-visible"),
              buttonPressed: cssText.includes(".ai-domain-window__button:active"),
              buttonDisabled: cssText.includes(".ai-domain-window__button:disabled"),
              windowControlHover: cssText.includes(".ai-domain-window__control:hover"),
              windowControlFocus: cssText.includes(".ai-domain-window__control:focus-visible"),
              windowControlPressed: cssText.includes(".ai-domain-window__control:active"),
              customScrollbar: cssText.includes(".ai-domain-window__chrome::-webkit-scrollbar-thumb")
            },
            viewModelContract: surface?.dataset.viewModelContract || "",
            viewModelSource: surface?.dataset.viewModelSource || "",
            viewModelState: surface?.dataset.viewModelState || "",
            viewModelProviderRuntimeBlocked: surface?.dataset.viewModelProviderRuntimeBlocked || "",
            viewModelPromptSendDisabled: surface?.dataset.viewModelPromptSendDisabled || "",
            viewModelProviderVisibleDataNone: surface?.dataset.viewModelProviderVisibleDataNone || "",
            viewModelPrivateSetupBlocked: surface?.dataset.viewModelPrivateSetupBlocked || "",
            viewModelOwnerMemoryAgentsBlocked: surface?.dataset.viewModelOwnerMemoryAgentsBlocked || "",
            providerVisibleDataState: surface?.dataset.providerVisibleDataState || "",
            noProviderState: surface?.dataset.noProviderState || "",
            promptExecutionState: surface?.dataset.promptExecutionState || "",
            providerModelRuntimeState: surface?.dataset.providerModelRuntimeState || "",
            trustBoundaryState: surface?.dataset.trustBoundaryState || "",
            controlCount: controls.length,
            controlCommands: controls.map((control) => control.dataset.domainCommand || ""),
            title: title?.textContent.trim() || "",
            workspaceCount: workspaceNodes.length,
            workspaces: workspaceNodes.map((node) => node.dataset.domainWorkspace || ""),
            actionButtons,
            providerVisibleData: textFor("provider-visible-data"),
            providerModel: textFor("provider-model"),
            promptMemory: textFor("prompt-memory"),
            capabilityPacks: textFor("capability-packs"),
            maintenanceUpdates: textFor("maintenance-updates"),
            developerLaneBoundary: textFor("developer-lane-boundary"),
            ownerLaneBoundary: textFor("owner-lane-boundary"),
            privateSetupBoundary: textFor("private-setup-boundary"),
            executionBoundary: textFor("execution-boundary"),
            localResult: textFor("local-result"),
            localDetail: textFor("local-detail"),
            reportState: textFor("report-state"),
            reportSummary: textFor("report-summary"),
            reportBodyHidden: Boolean(document.getElementById("report-body")?.hidden),
            reportBoundary: textFor("report-boundary"),
            copyDisabled: Boolean(document.getElementById("copy-report")?.disabled),
            copyAriaDisabled: document.getElementById("copy-report")?.getAttribute("aria-disabled") || "",
            controlCenterOperationalContract: controlWorkspace?.dataset.controlCenterOperationalContract || "",
            controlCenterMode: controlWorkspace?.dataset.controlCenterMode || "",
            controlCenterGuardClosed: controlWorkspace?.dataset.controlCenterGuardClosed || "",
            controlCenterProviderActionExecuted: controlWorkspace?.dataset.controlCenterProviderActionExecuted || "",
            controlCenterProviderModelExecution: controlWorkspace?.dataset.controlCenterProviderModelExecution || "",
            controlCenterPromptSendExecution: controlWorkspace?.dataset.controlCenterPromptSendExecution || "",
            controlCenterNetworkEgress: controlWorkspace?.dataset.controlCenterNetworkEgress || "",
            controlCenterMemoryIndexing: controlWorkspace?.dataset.controlCenterMemoryIndexing || "",
            controlCenterProviderVisibleData: controlWorkspace?.dataset.controlCenterProviderVisibleData || "",
            controlCenterModeText: textFor("control-center-mode"),
            controlCenterReviewState: textFor("control-center-review-state"),
            controlCenterReviewDetail: textFor("control-center-review-detail"),
            controlCenterRecoveryRoute: textFor("control-center-recovery-route"),
            controlCenterTaxonomy: textFor("control-center-taxonomy"),
            updateExecution: document.querySelector("[data-update-execution]")?.dataset.updateExecution || "",
            downloadExecution: document.querySelector("[data-download-execution]")?.dataset.downloadExecution || "",
            installExecution: document.querySelector("[data-install-execution]")?.dataset.installExecution || "",
            fetchExecution: capabilityWorkspace?.dataset.fetchExecution || "",
            capabilityExecution: capabilityWorkspace?.dataset.capabilityExecution || "",
            packagingExecution: capabilityWorkspace?.dataset.packagingExecution || "",
            capabilitiesBoundaryContract: capabilityWorkspace?.dataset.capabilitiesBoundaryContract || "",
            capabilitiesMaintenanceWorkflowContract: capabilityWorkspace?.dataset.capabilitiesMaintenanceWorkflowContract || "",
            capabilitiesMaintenanceMode: capabilityWorkspace?.dataset.capabilitiesMaintenanceMode || "",
            capabilitiesMaintenanceActionExecuted: capabilityWorkspace?.dataset.capabilitiesMaintenanceActionExecuted || "",
            capabilitiesMaintenanceDownloadExecution: capabilityWorkspace?.dataset.capabilitiesMaintenanceDownloadExecution || "",
            capabilitiesMaintenanceInstallExecution: capabilityWorkspace?.dataset.capabilitiesMaintenanceInstallExecution || "",
            capabilitiesMaintenanceUpdateExecution: capabilityWorkspace?.dataset.capabilitiesMaintenanceUpdateExecution || "",
            capabilitiesMaintenanceFetchExecution: capabilityWorkspace?.dataset.capabilitiesMaintenanceFetchExecution || "",
            capabilitiesMaintenancePackagingExecution: capabilityWorkspace?.dataset.capabilitiesMaintenancePackagingExecution || "",
            capabilitiesMaintenancePrivateSetup: capabilityWorkspace?.dataset.capabilitiesMaintenancePrivateSetup || "",
            capabilitiesModeText: textFor("capabilities-mode"),
            capabilitiesWorkflowState: textFor("capabilities-workflow-state"),
            capabilitiesWorkflowDetail: textFor("capabilities-workflow-detail"),
            capabilitiesWorkflowNext: textFor("capabilities-workflow-next"),
            capabilityPackLifecycleState: capabilityWorkspace?.dataset.capabilityPackLifecycleState || "",
            capabilityPackDownloadState: capabilityWorkspace?.dataset.capabilityPackDownloadState || "",
            installIntentState: capabilityWorkspace?.dataset.installIntentState || "",
            capabilityPackInstallState: capabilityWorkspace?.dataset.capabilityPackInstallState || "",
            capabilityPackUpdateState: capabilityWorkspace?.dataset.capabilityPackUpdateState || "",
            capabilityPackUninstallState: capabilityWorkspace?.dataset.capabilityPackUninstallState || "",
            developerLaneBoundaryState: capabilityWorkspace?.dataset.developerLaneBoundaryState || "",
            ownerLaneBoundaryState: capabilityWorkspace?.dataset.ownerLaneBoundaryState || "",
            privateSetupBoundaryState: capabilityWorkspace?.dataset.privateSetupBoundaryState || "",
            privateSetupAuthorized: capabilityWorkspace?.dataset.privateSetupAuthorized || "",
            privateMaterialVisible: capabilityWorkspace?.dataset.privateMaterialVisible || "",
            ownerMemoryEnabled: capabilityWorkspace?.dataset.ownerMemoryEnabled || "",
            ownerAgentsEnabled: capabilityWorkspace?.dataset.ownerAgentsEnabled || "",
            noProviderDiagnosticsFlow: readinessWorkspace?.dataset.noProviderDiagnosticsFlow || "",
            noProviderFlowState: readinessWorkspace?.dataset.noProviderFlowState || "",
            noProviderFlowProviderVisibleData: readinessWorkspace?.dataset.noProviderFlowProviderVisibleData || "",
            noProviderFlowSentToProvider: readinessWorkspace?.dataset.noProviderFlowSentToProvider || "",
            noProviderFlowCanAcceptPrompts: readinessWorkspace?.dataset.noProviderFlowCanAcceptPrompts || "",
            noProviderFlowPromptSend: readinessWorkspace?.dataset.noProviderFlowPromptSend || "",
            noProviderFlowNetworkEgress: readinessWorkspace?.dataset.noProviderFlowNetworkEgress || "",
            noProviderFlowMemoryIndexing: readinessWorkspace?.dataset.noProviderFlowMemoryIndexing || "",
            noProviderFlowReportState: readinessWorkspace?.dataset.noProviderFlowReportState || "",
            noProviderFlowCopyState: readinessWorkspace?.dataset.noProviderFlowCopyState || "",
            domainViewModel: window.nexusAiDomainCurrentViewModel || null,
            bodyText: document.body.innerText.replace(/\\s+/g, " ").trim()
          });
        })();
        """,
    )
    try:
        dom = json.loads(raw or "{}")
    except Exception:
        dom = {"raw": str(raw or "")}
    rect = _rect(int(window.winId())) if window.winId() else {"width": 0, "height": 0}
    return {
        "ok": True,
        "visible": bool(window.isVisible()),
        "windowTitle": window.windowTitle(),
        "objectName": window.objectName(),
        "propertyDomain": str(window.property("aiDashboardDomainWindow") or ""),
        "propertyClassification": str(window.property("aiDashboardDomainClassification") or ""),
        "propertyLifecycle": str(window.property("aiDashboardDomainLifecycle") or ""),
        "propertyShellConformance": str(window.property("ndaiShellConformance") or ""),
        "propertyBoundaryContract": str(window.property("windowBoundaryContract") or ""),
        "propertyBoundaryInset": str(window.property("windowBoundaryInset") or ""),
        "propertyResizeRailLocation": str(window.property("windowResizeRailLocation") or ""),
        "propertyOutsideHitBehavior": str(window.property("windowOutsideHitBehavior") or ""),
        "propertyMoveBehavior": str(window.property("windowMoveBehavior") or ""),
        "propertyResizeBehavior": str(window.property("windowResizeBehavior") or ""),
        "propertyDefaultGeometryContract": str(window.property("windowDefaultGeometryContract") or ""),
        "propertySupportedGeometryContract": str(window.property("windowSupportedGeometryContract") or ""),
        "propertyMaximumUsefulSize": str(window.property("windowMaximumUsefulSize") or ""),
        "propertyMaximizeFullscreenPolicy": str(window.property("windowMaximizeFullscreenPolicy") or ""),
        "propertyReopenGeometryContract": str(window.property("windowReopenGeometryContract") or ""),
        "propertyShellVisualContract": str(window.property("windowShellVisualContract") or ""),
        "propertyDescriptionDragBehavior": str(window.property("windowDescriptionDragBehavior") or ""),
        "propertyMeasuredDragRegionBottom": str(window.property("windowMeasuredDragRegionBottom") or ""),
        "propertyMeasuredDescriptionTop": str(window.property("windowMeasuredDescriptionTop") or ""),
        "propertyInitialContentFitApplied": str(window.property("windowInitialContentFitApplied") or ""),
        "propertyMeasuredContentHeight": str(window.property("windowMeasuredContentHeight") or ""),
        "propertyDefaultContentFitHeight": str(window.property("windowDefaultContentFitHeight") or ""),
        "propertyDefaultOverflowContract": str(window.property("windowDefaultOverflowContract") or ""),
        "propertyProviderVisibleData": str(window.property("providerVisibleData") or ""),
        "propertyProviderModelExecution": str(window.property("providerModelExecution") or ""),
        "propertyPromptSend": str(window.property("promptSend") or ""),
        "propertyNetworkEgress": str(window.property("networkEgress") or ""),
        "propertyMemoryIndexing": str(window.property("memoryIndexing") or ""),
        "propertyStateTaxonomyContract": str(window.property("aiControlCenterStateTaxonomyContract") or ""),
        "propertyStateTaxonomyComplete": str(window.property("aiControlCenterStateTaxonomyComplete") or ""),
        "propertyDiagnosticState": str(window.property("aiControlCenterDiagnosticState") or ""),
        "propertyStateTaxonomyRenderedStates": str(window.property("aiControlCenterStateTaxonomyRenderedStates") or ""),
        "propertyViewModelContract": str(window.property("aiDashboardProviderStateViewModelContract") or ""),
        "propertyViewModelApplied": str(window.property("aiDashboardProviderStateViewModelApplied") or ""),
        "rect": rect,
        "dom": dom,
    }


def _exercise_readiness_child_window(app: QApplication, window, log_root: Path) -> dict[str, object]:
    if window is None:
        return {"ok": False, "reason": "missing-readiness-window"}
    before = _probe_child_window(app, window)
    visual_proof_screenshots: dict[str, dict[str, str]] = {
        "beforeRun": _capture_window(app, window, log_root, "19_readiness_before_run"),
    }
    local_click = _click_web_button(app, window, "run-local-check")
    _pump(app, 220)
    after_local = _probe_child_window(app, window)
    local_fallback = {"ok": False, "skipped": True, "reason": "os-cursor-click-updated-local-check"}
    if ((after_local.get("dom") or {}).get("localResult") != "No provider configured"):
        raw = _run_child_js(
            app,
            window,
            """
            (() => {
              const button = document.getElementById("run-local-check");
              if (!button) return JSON.stringify({ ok: false, reason: "missing-button" });
              button.click();
              return JSON.stringify({ ok: true, button: "run-local-check", clickMode: "dom-button-click-fallback" });
            })();
            """,
        )
        try:
            local_fallback = json.loads(raw or "{}")
        except Exception:
            local_fallback = {"ok": False, "raw": str(raw or "")}
        _pump(app, 260)
        after_local = _probe_child_window(app, window)
    visual_proof_screenshots["afterLocalCheck"] = _capture_window(
        app,
        window,
        log_root,
        "20_readiness_after_local_check",
    )
    generate_click = _click_web_button(app, window, "generate-report")
    _pump(app, 320)
    after_generate = _probe_child_window(app, window)
    generate_fallback = {"ok": False, "skipped": True, "reason": "os-cursor-click-generated-report"}
    if ((after_generate.get("dom") or {}).get("reportState") != "Generated locally"):
        raw = _run_child_js(
            app,
            window,
            """
            (() => {
              const button = document.getElementById("generate-report");
              if (!button) return JSON.stringify({ ok: false, reason: "missing-button" });
              button.click();
              return JSON.stringify({ ok: true, button: "generate-report", clickMode: "dom-button-click-fallback" });
            })();
            """,
        )
        try:
            generate_fallback = json.loads(raw or "{}")
        except Exception:
            generate_fallback = {"ok": False, "raw": str(raw or "")}
        _pump(app, 360)
        after_generate = _probe_child_window(app, window)
    visual_proof_screenshots["afterReportGeneration"] = _capture_window(
        app,
        window,
        log_root,
        "21_readiness_after_report_generation",
    )
    copy_click = _click_web_button(app, window, "copy-report")
    _pump(app, 360)
    after_copy = _probe_child_window(app, window)
    copy_fallback = {"ok": False, "skipped": True, "reason": "os-cursor-click-copied-report"}
    if ((after_copy.get("dom") or {}).get("reportState") not in {
        "Copied locally",
        "Copying locally",
        "Copy unavailable; report remains visible",
    }):
        raw = _run_child_js(
            app,
            window,
            """
            (() => {
              const button = document.getElementById("copy-report");
              if (!button) return JSON.stringify({ ok: false, reason: "missing-button" });
              button.click();
              return JSON.stringify({ ok: true, button: "copy-report", clickMode: "dom-button-click-fallback" });
            })();
            """,
        )
        try:
            copy_fallback = json.loads(raw or "{}")
        except Exception:
            copy_fallback = {"ok": False, "raw": str(raw or "")}
        _pump(app, 360)
        after_copy = _probe_child_window(app, window)
    visual_proof_screenshots["afterCopyAction"] = _capture_window(
        app,
        window,
        log_root,
        "22_readiness_after_copy_action",
    )
    return {
        "ok": True,
        "before": before,
        "visualProofScreenshots": visual_proof_screenshots,
        "localClick": local_click,
        "localDomClickFallback": local_fallback,
        "afterLocalCheck": after_local,
        "generateClick": generate_click,
        "generateDomClickFallback": generate_fallback,
        "afterGenerate": after_generate,
        "copyClick": copy_click,
        "copyDomClickFallback": copy_fallback,
        "afterCopy": after_copy,
    }


def _click_child_button_with_dom_fallback(
    app: QApplication,
    window,
    button_id: str,
    *,
    expected_field: str,
    expected_value: str,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    click = _click_web_button(app, window, button_id)
    _pump(app, 280)
    after = _probe_child_window(app, window)
    fallback = {"ok": False, "skipped": True, "reason": "os-cursor-click-updated-expected-state"}
    if ((after.get("dom") or {}).get(expected_field) != expected_value):
        raw = _run_child_js(
            app,
            window,
            f"""
            (() => {{
              const button = document.getElementById({json.dumps(button_id)});
              if (!button) return JSON.stringify({{ ok: false, reason: "missing-button" }});
              button.click();
              return JSON.stringify({{ ok: true, button: {json.dumps(button_id)}, clickMode: "dom-button-click-fallback" }});
            }})();
            """,
        )
        try:
            fallback = json.loads(raw or "{}")
        except Exception:
            fallback = {"ok": False, "raw": str(raw or "")}
        _pump(app, 320)
        after = _probe_child_window(app, window)
    return click, fallback, after


def _exercise_control_center_child_window(app: QApplication, window, log_root: Path) -> dict[str, object]:
    if window is None:
        return {"ok": False, "reason": "missing-control-center-window"}
    before = _probe_child_window(app, window)
    visual_proof_screenshots: dict[str, dict[str, str]] = {
        "beforeBoundary": _capture_window(app, window, log_root, "23_control_center_before_boundary_review"),
    }
    boundary_click, boundary_fallback, after_boundary = _click_child_button_with_dom_fallback(
        app,
        window,
        "control-review-boundary",
        expected_field="controlCenterMode",
        expected_value="boundary",
    )
    visual_proof_screenshots["afterBoundaryReview"] = _capture_window(
        app,
        window,
        log_root,
        "24_control_center_after_boundary_review",
    )
    recovery_click, recovery_fallback, after_recovery = _click_child_button_with_dom_fallback(
        app,
        window,
        "control-review-recovery",
        expected_field="controlCenterMode",
        expected_value="recovery",
    )
    visual_proof_screenshots["afterRecoveryRoute"] = _capture_window(
        app,
        window,
        log_root,
        "25_control_center_after_recovery_route",
    )
    taxonomy_click, taxonomy_fallback, after_taxonomy = _click_child_button_with_dom_fallback(
        app,
        window,
        "control-review-taxonomy",
        expected_field="controlCenterMode",
        expected_value="taxonomy",
    )
    visual_proof_screenshots["afterStateTaxonomy"] = _capture_window(
        app,
        window,
        log_root,
        "26_control_center_after_state_taxonomy",
    )
    return {
        "ok": True,
        "before": before,
        "visualProofScreenshots": visual_proof_screenshots,
        "boundaryClick": boundary_click,
        "boundaryDomClickFallback": boundary_fallback,
        "afterBoundary": after_boundary,
        "recoveryClick": recovery_click,
        "recoveryDomClickFallback": recovery_fallback,
        "afterRecovery": after_recovery,
        "taxonomyClick": taxonomy_click,
        "taxonomyDomClickFallback": taxonomy_fallback,
        "afterTaxonomy": after_taxonomy,
    }


def _exercise_capabilities_child_window(app: QApplication, window, log_root: Path) -> dict[str, object]:
    if window is None:
        return {"ok": False, "reason": "missing-capabilities-maintenance-window"}
    before = _probe_child_window(app, window)
    visual_proof_screenshots: dict[str, dict[str, str]] = {
        "beforeLifecycle": _capture_window(app, window, log_root, "27_capabilities_before_lifecycle_review"),
    }
    lifecycle_click, lifecycle_fallback, after_lifecycle = _click_child_button_with_dom_fallback(
        app,
        window,
        "capabilities-review-lifecycle",
        expected_field="capabilitiesMaintenanceMode",
        expected_value="lifecycle",
    )
    visual_proof_screenshots["afterLifecycleReview"] = _capture_window(
        app,
        window,
        log_root,
        "28_capabilities_after_lifecycle_review",
    )
    lanes_click, lanes_fallback, after_lanes = _click_child_button_with_dom_fallback(
        app,
        window,
        "capabilities-review-lanes",
        expected_field="capabilitiesMaintenanceMode",
        expected_value="lanes",
    )
    visual_proof_screenshots["afterEditionGates"] = _capture_window(
        app,
        window,
        log_root,
        "29_capabilities_after_edition_gates",
    )
    maintenance_click, maintenance_fallback, after_maintenance = _click_child_button_with_dom_fallback(
        app,
        window,
        "capabilities-review-maintenance",
        expected_field="capabilitiesMaintenanceMode",
        expected_value="maintenance",
    )
    visual_proof_screenshots["afterMaintenanceHold"] = _capture_window(
        app,
        window,
        log_root,
        "30_capabilities_after_maintenance_hold",
    )
    return {
        "ok": True,
        "before": before,
        "visualProofScreenshots": visual_proof_screenshots,
        "lifecycleClick": lifecycle_click,
        "lifecycleDomClickFallback": lifecycle_fallback,
        "afterLifecycle": after_lifecycle,
        "lanesClick": lanes_click,
        "lanesDomClickFallback": lanes_fallback,
        "afterLanes": after_lanes,
        "maintenanceClick": maintenance_click,
        "maintenanceDomClickFallback": maintenance_fallback,
        "afterMaintenance": after_maintenance,
    }


def _hash_file(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _px(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text.removesuffix("px"))
    except ValueError:
        return None


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[middle])
    return (ordered[middle - 1] + ordered[middle]) / 2.0


def _grammar_group(grammar: dict[str, object], group_name: str) -> dict[str, object]:
    groups = grammar.get("materialGroups") if isinstance(grammar, dict) else {}
    if not isinstance(groups, dict):
        return {}
    group = groups.get(group_name)
    return group if isinstance(group, dict) else {}


def _grammar_style(grammar: dict[str, object], group_name: str, key: str) -> object:
    group = _grammar_group(grammar, group_name)
    style = group.get("style")
    if not isinstance(style, dict):
        return None
    return style.get(key)


def _grammar_rect_value(grammar: dict[str, object], group_name: str, key: str) -> float | None:
    group = _grammar_group(grammar, group_name)
    rect = group.get("rect")
    if not isinstance(rect, dict):
        return None
    raw = rect.get(key)
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _metric_summary(grammar: dict[str, object]) -> dict[str, object]:
    rows = grammar.get("rowMetrics") if isinstance(grammar, dict) else []
    buttons = grammar.get("buttonMetrics") if isinstance(grammar, dict) else []
    cards = grammar.get("cardMetrics") if isinstance(grammar, dict) else []
    rows = rows if isinstance(rows, list) else []
    buttons = buttons if isinstance(buttons, list) else []
    cards = cards if isinstance(cards, list) else []
    row_heights = [
        float(row.get("height") or 0)
        for row in rows
        if isinstance(row, dict) and float(row.get("height") or 0) > 0
    ]
    button_heights = [
        float(button.get("height") or 0)
        for button in buttons
        if isinstance(button, dict) and float(button.get("height") or 0) > 0
    ]
    button_widths = [
        float(button.get("width") or 0)
        for button in buttons
        if isinstance(button, dict) and float(button.get("width") or 0) > 0
    ]
    after_row_gaps = [
        float(card.get("afterRowsGap") or 0)
        for card in cards
        if isinstance(card, dict) and card.get("afterRowsGap") is not None
    ]
    action_bottom_gutters = [
        float(card.get("actionBottomGutter") or 0)
        for card in cards
        if isinstance(card, dict) and card.get("actionBottomGutter") is not None
    ]
    return {
        "rowCount": len(rows),
        "buttonCount": len(buttons),
        "cardCount": len(cards),
        "medianRowHeight": _median(row_heights),
        "minRowHeight": min(row_heights) if row_heights else 0,
        "maxRowHeight": max(row_heights) if row_heights else 0,
        "medianButtonHeight": _median(button_heights),
        "medianButtonWidth": _median(button_widths),
        "medianAfterRowGap": _median(after_row_gaps),
        "medianActionBottomGutter": _median(action_bottom_gutters),
    }


def _write_visual_grammar_audit(
    log_root: Path,
    dashboard_probe: dict[str, object],
    main_runtime_ai_control_center_reference: dict[str, object],
) -> dict[str, object]:
    current_grammar = dashboard_probe.get("visualGrammar")
    if not isinstance(current_grammar, dict):
        current_grammar = {}
    reference_metadata = main_runtime_ai_control_center_reference.get("metadata")
    reference_probe = (
        reference_metadata.get("probe")
        if isinstance(reference_metadata, dict) and isinstance(reference_metadata.get("probe"), dict)
        else {}
    )
    reference_grammar = reference_probe.get("visualGrammar") if isinstance(reference_probe, dict) else {}
    if not isinstance(reference_grammar, dict):
        reference_grammar = {}

    findings: list[dict[str, object]] = []

    def add(
        group: str,
        status: str,
        current: object,
        reference: object,
        note: str,
    ) -> None:
        findings.append(
            {
                "group": group,
                "status": status,
                "current": current,
                "reference": reference,
                "note": note,
            }
        )

    required_groups = [
        "chrome",
        "titleGroup",
        "header",
        "kicker",
        "title",
        "subtitle",
        "surfaceRole",
        "surfaceRoleCopy",
        "surfaceRolePair",
        "windowControls",
        "windowControlButton",
        "controlHub",
        "hubCard",
        "cardTopline",
        "cardBadge",
        "cardTitle",
        "cardDescription",
        "stateRow",
        "rowLabel",
        "rowValue",
        "hubActions",
        "hubAction",
        "buttonLabel",
        "scrollbarTrack",
        "scrollbarThumb",
    ]
    for group_name in required_groups:
        current_present = bool(_grammar_group(current_grammar, group_name).get("present"))
        reference_present = bool(_grammar_group(reference_grammar, group_name).get("present"))
        status = "PASS" if current_present and reference_present else "UNPROVEN"
        add(
            group_name,
            status,
            "present" if current_present else "missing",
            "present" if reference_present else "missing",
            "Material element-group exists in both rendered surfaces." if status == "PASS" else "Required material element-group missing from current or comparator render.",
        )

    current_summary = _metric_summary(current_grammar)
    reference_summary = _metric_summary(reference_grammar)

    def compare_px(
        group_name: str,
        style_key: str,
        tolerance: float,
        note: str,
        status_on_difference: str = "NONCONFORMING",
    ) -> None:
        current = _px(_grammar_style(current_grammar, group_name, style_key))
        reference = _px(_grammar_style(reference_grammar, group_name, style_key))
        if current is None or reference is None:
            add(f"{group_name}.{style_key}", "UNPROVEN", current, reference, "Computed style missing from current or comparator.")
            return
        diff = abs(current - reference)
        add(
            f"{group_name}.{style_key}",
            "PASS" if diff <= tolerance else status_on_difference,
            current,
            reference,
            note if diff <= tolerance else f"{note} Difference {diff:.1f}px exceeds {tolerance:.1f}px tolerance.",
        )

    def compare_text(group_name: str, style_key: str, note: str) -> None:
        current = _grammar_style(current_grammar, group_name, style_key)
        reference = _grammar_style(reference_grammar, group_name, style_key)
        add(
            f"{group_name}.{style_key}",
            "PASS" if str(current) == str(reference) else "NONCONFORMING",
            current,
            reference,
            note,
        )

    compare_px("chrome", "paddingLeft", 0.5, "Outer chrome padding matches the Main comparator.")
    compare_px("titleGroup", "borderRadius", 0.5, "Header capsule radius matches the Main comparator.")
    compare_px("title", "fontSize", 1.0, "Title scale remains in the Main comparator range.")
    compare_px("subtitle", "lineHeight", 1.0, "Subtitle line-height remains in the Main comparator range.")
    compare_px("surfaceRole", "marginTop", 0.5, "Global strip top rhythm matches the Main comparator.")
    compare_px("surfaceRole", "borderRadius", 0.5, "Global strip radius matches the Main comparator.")
    compare_px("windowControlButton", "width", 0.5, "Window control button width matches the Main comparator.")
    compare_px("windowControlButton", "height", 0.5, "Window control button height matches the Main comparator.")
    compare_text("controlHub", "gap", "Control-hub card gap uses the Main comparator rhythm.")
    compare_text("controlHub", "padding", "Control-hub padding uses the Main comparator rhythm.")
    compare_text("hubCard", "padding", "Card padding uses the Main comparator rhythm.")
    compare_px("hubCard", "borderRadius", 0.5, "Card radius uses the Main comparator grammar.")
    compare_px("cardBadge", "width", 0.5, "Card badge width matches the Main comparator.")
    compare_px("cardBadge", "height", 0.5, "Card badge height matches the Main comparator.")
    compare_px("cardTitle", "fontSize", 0.5, "Card title size matches the Main comparator.")
    compare_px("cardDescription", "fontSize", 0.5, "Card description size matches the Main comparator.")
    compare_px(
        "rowLabel",
        "fontSize",
        0.5,
        "Row label size follows the USER row title/status text-size parity rule; Main comparator label size is retained as reference context.",
        status_on_difference="WAIVED_WITH_REASON",
    )
    compare_px("rowValue", "fontSize", 0.5, "Row value size matches the Main comparator.")
    current_row_label_font = _px(_grammar_style(current_grammar, "rowLabel", "fontSize"))
    current_row_value_font = _px(_grammar_style(current_grammar, "rowValue", "fontSize"))
    add(
        "rowTypography.labelValueFontSizeParity",
        "PASS"
        if current_row_label_font is not None
        and current_row_value_font is not None
        and abs(current_row_label_font - current_row_value_font) <= 0.1
        else "NONCONFORMING",
        current_row_label_font,
        current_row_value_font,
        "Current row title and status/value text sizes must be identical per USER visual-grammar direction.",
    )
    compare_px("hubAction", "fontSize", 0.5, "Action button text size matches the Main comparator.")
    compare_px("hubAction", "height", 0.5, "Action button height matches the Main comparator.")
    compare_px("buttonLabel", "fontSize", 0.5, "Button label text size matches the Main comparator.")

    row_height_diff = abs(float(current_summary["medianRowHeight"]) - float(reference_summary["medianRowHeight"]))
    add(
        "rowRhythm.medianHeight",
        "PASS" if row_height_diff <= 2 else "NONCONFORMING",
        current_summary["medianRowHeight"],
        reference_summary["medianRowHeight"],
        "Median row height must stay within 2px of Main-runtime row rhythm.",
    )
    after_row_gap_diff = abs(float(current_summary["medianAfterRowGap"]) - float(reference_summary["medianAfterRowGap"]))
    add(
        "afterRowSpacing.medianGap",
        "PASS" if after_row_gap_diff <= 2 else "NONCONFORMING",
        current_summary["medianAfterRowGap"],
        reference_summary["medianAfterRowGap"],
        "Rows-to-action spacing must stay within 2px of Main-runtime rhythm.",
    )
    button_height_diff = abs(float(current_summary["medianButtonHeight"]) - float(reference_summary["medianButtonHeight"]))
    add(
        "buttonSize.medianHeight",
        "PASS" if button_height_diff <= 1 else "NONCONFORMING",
        current_summary["medianButtonHeight"],
        reference_summary["medianButtonHeight"],
        "Median action button height must match the Main-runtime control grammar.",
    )
    add(
        "surfaceRole.defaultWindowSize",
        "WAIVED_WITH_REASON",
        f'{dashboard_probe.get("defaultWindowWidth")}x{dashboard_probe.get("defaultWindowHeight")}',
        f'{reference_probe.get("defaultWindowWidth")}x{reference_probe.get("defaultWindowHeight")}',
        "AI Dashboard is the wider parent hub; Main AI Control Center remains the focused comparator, not an identical surface footprint.",
    )
    add(
        "cardSet.countAndPurpose",
        "WAIVED_WITH_REASON",
        current_summary["cardCount"],
        reference_summary["cardCount"],
        "Current parent Dashboard has three doorway cards; Main old AI Control Center has two focused cards.",
    )
    add(
        "buttonState.affordance",
        "WAIVED_WITH_REASON",
        dashboard_probe.get("doorwayButtons"),
        reference_grammar.get("buttonMetrics"),
        "Current Dashboard doorway controls open detached domain windows; Main comparator has a focused local-check action. Geometry and typography remain same-family.",
    )

    current_css = current_grammar.get("cssStateSelectors") if isinstance(current_grammar, dict) else {}
    reference_css = reference_grammar.get("cssStateSelectors") if isinstance(reference_grammar, dict) else {}
    if not isinstance(current_css, dict):
        current_css = {}
    if not isinstance(reference_css, dict):
        reference_css = {}
    for key in [
        "hubActionHover",
        "hubActionFocus",
        "hubActionPressed",
        "hubActionDisabled",
        "windowControlHover",
        "windowControlFocus",
        "windowControlDisabled",
        "customScrollbar",
    ]:
        add(
            f"stateCoverage.{key}",
            "PASS" if current_css.get(key) and reference_css.get(key) else "UNPROVEN",
            current_css.get(key),
            reference_css.get(key),
            "CSS state selector coverage exists in both current and comparator surfaces.",
        )

    blocking_statuses = {"NONCONFORMING", "PARTIAL", "SOURCE-TRUTH GAP", "REFERENCE GAP", "UNPROVEN"}
    blocking_findings = [finding for finding in findings if str(finding.get("status")) in blocking_statuses]
    status = "PASS" if not blocking_findings else "FAIL"
    audit = {
        "status": status,
        "auditKind": "exhaustive-main-runtime-visual-grammar-comparison",
        "currentSummary": current_summary,
        "referenceSummary": reference_summary,
        "blockingFindingCount": len(blocking_findings),
        "findings": findings,
        "blockingFindings": blocking_findings,
    }
    json_path = log_root / "14_exhaustive_visual_grammar_audit.json"
    md_path = log_root / "14_exhaustive_visual_grammar_audit.md"
    json_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows = [
        "# Exhaustive Main Runtime Visual Grammar Audit",
        "",
        f"Status: `{status}`",
        "",
        "| Group | Status | Current | Reference | Note |",
        "| --- | --- | --- | --- | --- |",
    ]
    for finding in findings:
        current = str(finding.get("current", "")).replace("|", "/")
        reference = str(finding.get("reference", "")).replace("|", "/")
        note = str(finding.get("note", "")).replace("|", "/")
        if len(current) > 140:
            current = current[:137] + "..."
        if len(reference) > 140:
            reference = reference[:137] + "..."
        rows.append(
            f"| {finding.get('group')} | `{finding.get('status')}` | {current} | {reference} | {note} |"
        )
    md_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    audit["jsonPath"] = str(json_path)
    audit["markdownPath"] = str(md_path)
    return audit


def _copy_user_evidence(local_root: Path, stamp: str) -> Path:
    user_root = (
        Path.home()
        / "OneDrive"
        / "Pictures"
        / "Screenshots"
        / "Nexus Desktop AI"
        / "FAM-007-H4"
        / f"{stamp}-parent-dashboard"
    )
    if user_root.exists():
        shutil.rmtree(user_root)
    user_root.mkdir(parents=True, exist_ok=True)
    for png in sorted(local_root.glob("*.png")):
        (user_root / png.name).write_bytes(png.read_bytes())
    return user_root


def main() -> int:
    stamp = _timestamp()
    log_root = REPO_ROOT / "dev" / "logs" / "fam_007_ai_control_center_live_resize" / stamp
    log_root.mkdir(parents=True, exist_ok=True)
    proof_classification_fixture_probe = _proof_classification_fixture_probe()
    exact_launcher_preflight = _read_only_exact_launcher_preflight()
    physical_interaction_matrix = _physical_interaction_matrix()
    dual_contrast_matrix = _dual_contrast_matrix()
    isolated_state_path = log_root / "isolated_ai_dashboard_window_state.json"
    os.environ["NEXUS_AI_CONTROL_CENTER_STATE_PATH"] = str(isolated_state_path)
    os.environ.pop("NEXUS_AI_CONTROL_CENTER_ENABLE_GEOMETRY_MEMORY", None)

    app = QApplication.instance() or QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No primary screen available for parent-dashboard validation")

    events: list[str] = []
    provider_state = build_provider_setup_completion_foundation_state(
        build_default_provider_readiness_config(),
        surface_role="hud",
    )
    dialog = AIControlCenterDialog(screen, event_logger=events.append)
    dialog.update_provider_state(provider_state.as_renderer_payload())
    available = screen.availableGeometry()
    dialog.setGeometry(
        QRect(
            available.x() + max(40, available.width() - dialog.DEFAULT_WIDTH - 120),
            available.y() + 80,
            dialog.DEFAULT_WIDTH,
            dialog.DEFAULT_HEIGHT,
        )
    )
    dialog.show_from_tray()
    _pump(app, 900)

    screenshots: dict[str, dict[str, str]] = {
        "dashboard_initial": _capture_window(app, dialog, log_root, "01_dashboard_initial"),
    }
    dashboard_probe = json.loads(
        _run_js(
            app,
            dialog,
            """
            (() => {
              const surface = document.getElementById("monitoring-hud");
              const cardNames = Array.from(document.querySelectorAll("[data-dashboard-hub-card]")).map((card) => card.dataset.dashboardHubCard || "");
              const launchers = Array.from(document.querySelectorAll("[data-category-launcher]")).map((button) => ({
                id: button.id || "",
                text: button.textContent.trim(),
                launcher: button.dataset.categoryLauncher || "",
                target: button.dataset.launchTarget || "",
                kind: button.dataset.launchWindowKind || ""
              }));
              const doorwayButtons = Array.from(document.querySelectorAll("[data-category-doorway]")).map((button) => {
                const rect = button.getBoundingClientRect();
                const style = getComputedStyle(button);
                const label = button.querySelector(".monitoring-hud__button-label");
                const labelRect = label?.getBoundingClientRect();
                const labelStyle = label ? getComputedStyle(label) : null;
                const horizontalPadding = Math.round(parseFloat(style.paddingLeft || "0") + parseFloat(style.paddingRight || "0"));
                return {
                  id: button.id || "",
                  text: button.textContent.trim(),
                  doorway: button.dataset.categoryDoorway || "",
                  actionState: button.dataset.actionState || "",
                  control: button.dataset.control || "",
                  command: button.dataset.launchCommand || "",
                  disabled: Boolean(button.disabled),
                  ariaDisabled: button.getAttribute("aria-disabled") || "",
                  launchTarget: button.dataset.launchTarget || "",
                  launchKind: button.dataset.launchWindowKind || "",
                  lifecycle: button.dataset.windowLifecycle || "",
                  width: Math.round(rect.width),
                  height: Math.round(rect.height),
                  horizontalPadding,
                  labelWidth: labelRect ? Math.round(labelRect.width) : 0,
                  labelOverflow: labelStyle ? labelStyle.overflow : "",
                  labelTextOverflow: labelStyle ? labelStyle.textOverflow : "",
                  fontSize: style.fontSize,
                  fontWeight: style.fontWeight
                };
              });
              const surfaceRect = surface?.getBoundingClientRect();
              const chrome = document.querySelector(".monitoring-hud__chrome");
              const header = document.querySelector(".monitoring-hud__title-group");
              const headerCopy = document.querySelector(".monitoring-hud__header");
              const title = document.querySelector(".monitoring-hud__title");
              const subtitle = document.querySelector(".monitoring-hud__subtitle");
              const windowControls = document.querySelector(".monitoring-hud__window-controls");
              const hub = document.getElementById("ai-control-center-card-hub");
              const firstCard = document.querySelector("[data-dashboard-hub-card]");
              const thirdCard = document.querySelector('[data-dashboard-hub-card="capabilities-maintenance"]');
              const chromeStyle = chrome ? getComputedStyle(chrome) : null;
              const headerCopyStyle = headerCopy ? getComputedStyle(headerCopy) : null;
              const titleBackingStyle = header ? getComputedStyle(header, "::before") : null;
              const subtitleStyle = subtitle ? getComputedStyle(subtitle) : null;
              const hubStyle = hub ? getComputedStyle(hub) : null;
              const rectFor = (node, extra = 0) => {
                if (!node) return { left: 0, top: 0, width: 0, height: 0, right: 0, bottom: 0 };
                const rect = node.getBoundingClientRect();
                return {
                  left: Math.round(rect.left - extra),
                  top: Math.round(rect.top - extra),
                  width: Math.round(rect.width + (extra * 2)),
                  height: Math.round(rect.height + (extra * 2)),
                  right: Math.round(rect.right + extra),
                  bottom: Math.round(rect.bottom + extra)
                };
              };
              const intersects = (a, b) => Boolean(a && b && a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top);
              const pxNumber = (value) => {
                const parsed = Number.parseFloat(String(value || "0"));
                return Number.isFinite(parsed) ? parsed : 0;
              };
              const firstGridColumnWidth = (template) => {
                const match = String(template || "").match(/([\\d.]+)px/);
                return match ? Number(match[1]) : 0;
              };
              const lineHeightNumber = (style, rect) => pxNumber(style?.lineHeight) || Math.max(1, rect.height);
              const titleStatusPillWrap = (() => {
                const copy = document.querySelector(".monitoring-hud__surface-role-copy");
                const copyRect = rectFor(copy);
                const pairMetrics = [...document.querySelectorAll(".monitoring-hud__surface-role-pair")].map((pair) => {
                  const rect = rectFor(pair);
                  const style = getComputedStyle(pair);
                  const childRects = [...pair.children].map((child) => rectFor(child));
                  const childTops = childRects.map((rect) => rect.top);
                  const childBottoms = childRects.map((rect) => rect.bottom);
                  const childTopSpread = childTops.length ? Math.max(...childTops) - Math.min(...childTops) : 0;
                  const childBottomSpread = childBottoms.length ? Math.max(...childBottoms) - Math.min(...childBottoms) : 0;
                  return {
                    text: pair.textContent.replace(/\\s+/g, " ").trim(),
                    rect,
                    display: style.display,
                    flexShrink: style.flexShrink,
                    whiteSpace: style.whiteSpace,
                    lineTop: rect.top,
                    childrenShareLine: childTopSpread <= 2 && childBottomSpread <= 2,
                    withinPill: copyRect.width > 0 && rect.left >= copyRect.left - 2 && rect.right <= copyRect.right + 2
                  };
                });
                const expectedTexts = ["AI Persona - None", "Status - Not implemented", "Provider - Blocked"];
                return {
                  copyMaxWidth: copy ? getComputedStyle(copy).maxWidth : "",
                  pairCount: pairMetrics.length,
                  lineCount: new Set(pairMetrics.map((pair) => pair.lineTop)).size,
                  expectedTextsPresent: expectedTexts.every((text) => pairMetrics.some((pair) => pair.text === text)),
                  groupsAtomic: pairMetrics.every((pair) => pair.display.includes("flex") && pair.whiteSpace === "nowrap" && pair.childrenShareLine),
                  clippedPairCount: pairMetrics.filter((pair) => !pair.withinPill).length,
                  pairMetrics
                };
              })();
              const titleDescriptionWrap = (() => {
                const description = subtitle;
                const descriptionRect = rectFor(description);
                const descriptionStyle = description ? getComputedStyle(description) : null;
                const titleGroupRectForWrap = rectFor(header);
                const titleGroupStyleForWrap = header ? getComputedStyle(header) : null;
                const titleGroupInnerWidth = header
                  ? Math.round(
                      titleGroupRectForWrap.width
                      - pxNumber(titleGroupStyleForWrap?.paddingLeft)
                      - pxNumber(titleGroupStyleForWrap?.paddingRight)
                    )
                  : 0;
                const publishedMaxWidth = pxNumber(description?.dataset.titleDescriptionMaxWidth || "");
                const expectedText = "AI is not implemented; provider/model execution is blocked, and no prompt, file, memory, telemetry, or provider data leaves this machine.";
                const text = (description?.textContent || "").replace(/\\s+/g, " ").trim();
                const rectFromDomRect = (rect) => ({
                  left: Math.round(rect.left),
                  top: Math.round(rect.top),
                  right: Math.round(rect.right),
                  bottom: Math.round(rect.bottom),
                  width: Math.round(rect.width),
                  height: Math.round(rect.height)
                });
                const textNode = description
                  ? [...description.childNodes].find((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim())
                  : null;
                const wordMetrics = [];
                if (textNode) {
                  const rawText = textNode.textContent || "";
                  const wordPattern = /\\S+/g;
                  let match = null;
                  while ((match = wordPattern.exec(rawText)) !== null) {
                    const range = document.createRange();
                    range.setStart(textNode, match.index);
                    range.setEnd(textNode, match.index + match[0].length);
                    const rects = [...range.getClientRects()]
                      .filter((rect) => rect.width > 0 && rect.height > 0)
                      .map(rectFromDomRect);
                    range.detach();
                    const rect = rects[0] || { left: 0, top: 0, right: 0, bottom: 0, width: 0, height: 0 };
                    wordMetrics.push({
                      text: match[0],
                      rect,
                      rects,
                      lineTop: rect.top,
                      withinDescription: descriptionRect.width > 0 && rect.left >= descriptionRect.left - 2 && rect.right <= descriptionRect.right + 2
                    });
                  }
                }
                const groupCount = description ? description.querySelectorAll(".monitoring-hud__subtitle-group").length : 0;
                const lineTops = [...new Set(wordMetrics.map((word) => word.lineTop).filter((top) => top > 0))];
                const lastPhraseMetrics = wordMetrics.slice(-6);
                const lastPhraseLineCount = new Set(lastPhraseMetrics.map((word) => word.lineTop).filter((top) => top > 0)).size;
                const lastPhraseText = lastPhraseMetrics.map((word) => word.text).join(" ");
                return {
                  containerRect: descriptionRect,
                  display: descriptionStyle?.display || "",
                  flexWrap: descriptionStyle?.flexWrap || "",
                  whiteSpace: descriptionStyle?.whiteSpace || "",
                  overflowWrap: descriptionStyle?.overflowWrap || "",
                  wordBreak: descriptionStyle?.wordBreak || "",
                  maxWidth: descriptionStyle?.maxWidth || "",
                  publishedMaxWidth: Math.round(publishedMaxWidth),
                  titleGroupInnerWidth,
                  columnSource: description?.dataset.titleDescriptionColumnSource || "",
                  metadata: description?.dataset.titleDescriptionWrap || "",
                  text,
                  expectedTextPresent: text === expectedText,
                  groupCount,
                  lineCount: lineTops.length,
                  wordCount: wordMetrics.length,
                  noAtomicPhraseGroups: groupCount === 0,
                  wordsCanWrapIndividually: wordMetrics.length > 0 && wordMetrics.every((word) => word.rect.width <= descriptionRect.width + 2),
                  clippedWordCount: wordMetrics.filter((word) => !word.withinDescription).length,
                  lastPhraseText,
                  lastPhraseLineCount,
                  lastPhraseWrapsByWord: lastPhraseText === "or provider data leaves this machine." && lastPhraseLineCount >= 2,
                  measuredWidthMatchesTitleCardInner: Math.abs(Math.round(publishedMaxWidth) - titleGroupInnerWidth) <= 2,
                  fixedLegacyMaxWidthRemoved: descriptionStyle ? descriptionStyle.maxWidth !== "600px" : false,
                  containerUsesProseWordWrap: descriptionStyle
                    ? !descriptionStyle.display.includes("flex") && descriptionStyle.whiteSpace === "normal"
                    : false,
                  wordMetrics,
                  lastPhraseMetrics
                };
              })();
              const rowTitleSizingProbe = (() => {
                const hub = document.getElementById("ai-control-center-card-hub");
                const hubStyle = hub ? getComputedStyle(hub) : null;
                const derivedGutter = pxNumber(hubStyle?.getPropertyValue("--ai-dashboard-row-gutter"));
                const derivedVerticalGutter = pxNumber(hubStyle?.getPropertyValue("--ai-dashboard-row-vertical-gutter"));
                const declaredLabelColumnWidthRaw = hubStyle?.getPropertyValue("--ai-dashboard-row-label-width") || "";
                const declaredLabelColumnWidthIsPx = /^\\s*\\d+(?:\\.\\d+)?px\\s*$/.test(declaredLabelColumnWidthRaw);
                const declaredLabelColumnWidth = declaredLabelColumnWidthIsPx ? pxNumber(declaredLabelColumnWidthRaw) : 0;
                const rows = [...document.querySelectorAll(".ai-control-center-card-rows .monitoring-hud__state-row")];
                const rowStackMetrics = [...document.querySelectorAll(".ai-control-center-card-rows")].map((stack, stackIndex) => {
                  const stackStyle = getComputedStyle(stack);
                  const stackRows = [...stack.querySelectorAll(".monitoring-hud__state-row")];
                  const pairGaps = stackRows.slice(1).map((row, index) => {
                    const previousRect = stackRows[index].getBoundingClientRect();
                    const rowRect = row.getBoundingClientRect();
                    return Math.round(rowRect.top - previousRect.bottom);
                  });
                  const rowGapPx = Math.round(pxNumber(stackStyle.rowGap || stackStyle.gap));
                  return {
                    stackIndex,
                    rowCount: stackRows.length,
                    rowGapPx,
                    expectedRowVerticalGutterPx: Math.round(derivedVerticalGutter),
                    pairGaps,
                    rowGapMatchesToken: Math.abs(rowGapPx - derivedVerticalGutter) <= 1,
                    pairGapsMatchToken: pairGaps.every((gap) => Math.abs(gap - derivedVerticalGutter) <= 1)
                  };
                });
                const labelWidths = rows.map((row) => {
                  const label = row.querySelector("span");
                  const labelRect = rectFor(label);
                  return Math.ceil(Math.max(labelRect.width || 0, label?.scrollWidth || 0));
                });
                const measuredMaxLabelWidth = labelWidths.length ? Math.max(...labelWidths) : 0;
                const contractLabelColumnWidth = Math.round(declaredLabelColumnWidth);
                const rowMetrics = rows.map((row, index) => {
                  const rowRect = rectFor(row);
                  const style = getComputedStyle(row);
                  const label = row.querySelector("span");
                  const value = row.querySelector("strong");
                  const labelRect = rectFor(label);
                  const valueRect = rectFor(value);
                  const labelStyle = label ? getComputedStyle(label) : null;
                  const titleColumnWidth = firstGridColumnWidth(style.gridTemplateColumns);
                  const labelWraps = labelRect.height > lineHeightNumber(labelStyle, labelRect) * 1.35;
                  const valueColumnOffset = Math.round(valueRect.left - rowRect.left);
                  const expectedValueColumnOffset = Math.round(contractLabelColumnWidth + derivedGutter);
                  const fixedColumnGutterPx = Math.round(valueColumnOffset - titleColumnWidth);
                  const visibleLabelToValueGutterPx = Math.round(valueRect.left - labelRect.right);
                  return {
                    index,
                    key: `${label?.textContent.trim() || ""}|${value?.textContent.trim() || ""}`,
                    label: label?.textContent.trim() || "",
                    value: value?.textContent.trim() || "",
                    labelFontSize: labelStyle?.fontSize || "",
                    valueFontSize: value ? getComputedStyle(value).fontSize : "",
                    gridTemplateColumns: style.gridTemplateColumns,
                    titleColumnWidth: Math.round(titleColumnWidth),
                    labelWidth: labelRect.width,
                    rowLeft: rowRect.left,
                    rowGutterPx: Math.round(derivedGutter),
                    fixedColumnGutterPx,
                    visibleLabelToValueGutterPx,
                    valueColumnOffset,
                    expectedValueColumnOffset,
                    valueLeft: valueRect.left,
                    rowRight: rowRect.right,
                    labelWraps,
                    titleColumnContentExcessPx: Math.round(titleColumnWidth - labelRect.width),
                    titleColumnMatchesContract: Math.abs(titleColumnWidth - contractLabelColumnWidth) <= 2,
                    valueColumnOffsetMatchesContract: Math.abs(valueColumnOffset - expectedValueColumnOffset) <= 2,
                    fixedColumnGutterMatchesToken: Math.abs(fixedColumnGutterPx - derivedGutter) <= 2,
                    visibleGutterAtLeastFixedGutter: visibleLabelToValueGutterPx >= derivedGutter - 2,
                    labelWithinRow: labelRect.left >= rowRect.left - 2 && labelRect.right <= rowRect.right + 2,
                    valueWithinRow: valueRect.left >= rowRect.left - 2 && valueRect.right <= rowRect.right + 2
                  };
                });
                const valueOffsets = rowMetrics.map((row) => row.valueColumnOffset);
                const uniformValueColumnOffset = valueOffsets.length
                  ? Math.max(...valueOffsets) - Math.min(...valueOffsets) <= 2
                  : false;
                const valueLefts = rowMetrics.map((row) => Math.round(row.valueLeft));
                const uniformValueLeftEdge = valueLefts.length
                  ? Math.max(...valueLefts) - Math.min(...valueLefts) <= 2
                  : false;
                const maxLabelColumnExcess = Math.abs(contractLabelColumnWidth - measuredMaxLabelWidth);
                const maxTitleColumnExcess = rowMetrics.length
                  ? Math.max(...rowMetrics.map((row) => Math.abs(row.titleColumnWidth - contractLabelColumnWidth)))
                  : 999;
                const declaredLabelColumnMatchesMeasuredMax = declaredLabelColumnWidthIsPx
                  && contractLabelColumnWidth > 0
                  && maxLabelColumnExcess <= 2;
                return {
                  rowCount: rowMetrics.length,
                  labelColumnSource: hub?.dataset.rowLabelColumnSource || "",
                  labelColumnUnit: hub?.dataset.rowLabelColumnUnit || "",
                  rowValueColumnContract: hub?.dataset.rowValueColumnContract || "",
                  measuredMaxLabelWidth: Math.round(measuredMaxLabelWidth),
                  declaredLabelColumnWidthRaw: declaredLabelColumnWidthRaw.trim(),
                  declaredLabelColumnWidthIsPx,
                  declaredLabelColumnWidth: Math.round(declaredLabelColumnWidth),
                  contractLabelColumnWidth,
                  rowGutterPx: Math.round(derivedGutter),
                  rowVerticalGutterPx: Math.round(derivedVerticalGutter),
                  rowVerticalGutterRestored: rowStackMetrics.every((stack) => stack.rowCount < 2 || (stack.rowGapMatchesToken && stack.pairGapsMatchToken)),
                  rowStackMetrics,
                  contentSized: rowMetrics.every((row) => (
                    !row.labelWraps
                    && row.titleColumnMatchesContract
                    && row.valueColumnOffsetMatchesContract
                    && row.fixedColumnGutterMatchesToken
                    && row.visibleGutterAtLeastFixedGutter
                  )) && declaredLabelColumnMatchesMeasuredMax && maxTitleColumnExcess <= 2 && uniformValueColumnOffset && uniformValueLeftEdge,
                  noLabelClipping: rowMetrics.every((row) => row.labelWithinRow),
                  noValueClipping: rowMetrics.every((row) => row.valueWithinRow),
                  labelValueFontSizeParity: rowMetrics.every((row) => row.labelFontSize === row.valueFontSize),
                  valueColumnDerivedFromLabelContent: rowMetrics.every((row) => row.valueColumnOffsetMatchesContract),
                  valueColumnDerivedFromMaxLabelContent: rowMetrics.every((row) => row.valueColumnOffsetMatchesContract),
                  declaredLabelColumnMatchesMeasuredMax,
                  fixedColumnGutterRestored: rowMetrics.every((row) => row.fixedColumnGutterMatchesToken),
                  uniformValueColumnOffset,
                  uniformValueLeftEdge,
                  visibleRowGutterAtLeastFixedGutter: rowMetrics.every((row) => row.visibleGutterAtLeastFixedGutter),
                  maxTitleColumnExcessPx: maxTitleColumnExcess,
                  maxLabelColumnExcessPx: maxLabelColumnExcess,
                  rowMetrics
                };
              })();
              const belowTitleTextWeightProbe = (() => {
                const hub = document.getElementById("ai-control-center-card-hub");
                const nodes = hub
                  ? [...hub.querySelectorAll("span, strong, p, button, .monitoring-hud__button-label")]
                  : [];
                const textNodes = nodes.filter((node) => {
                  const rect = node.getBoundingClientRect();
                  const style = getComputedStyle(node);
                  return node.textContent.trim()
                    && style.display !== "none"
                    && style.visibility !== "hidden"
                    && Number(style.opacity || 1) > 0
                    && rect.width > 0
                    && rect.height > 0;
                }).map((node) => ({
                  text: node.textContent.replace(/\\s+/g, " ").trim(),
                  tagName: node.tagName.toLowerCase(),
                  className: node.className || "",
                  fontWeight: getComputedStyle(node).fontWeight
                }));
                const non720 = textNodes.filter((node) => node.fontWeight !== "720");
                return {
                  targetWeight: "720",
                  nodeCount: textNodes.length,
                  all720: textNodes.length > 0 && non720.length === 0,
                  non720
                };
              })();
              const rowMetrics = [...document.querySelectorAll(".ai-control-center-card-rows .monitoring-hud__state-row")].map((row) => {
                const rect = row.getBoundingClientRect();
                const style = getComputedStyle(row);
                return {
                  height: Math.round(rect.height),
                  paddingTop: style.paddingTop,
                  paddingBottom: style.paddingBottom
                };
              });
              const cardVisualMetrics = [...document.querySelectorAll("[data-dashboard-hub-card]")].map((card) => {
                const cardRect = card.getBoundingClientRect();
                const rows = card.querySelector(".ai-control-center-card-rows");
                const rowsRect = rows?.getBoundingClientRect();
                const action = card.querySelector(".monitoring-hud__hub-actions");
                const actionRect = action?.getBoundingClientRect();
                const button = card.querySelector("[data-category-doorway]");
                const buttonRect = button?.getBoundingClientRect();
                const descriptions = card.querySelector(".monitoring-hud__hub-card-description");
                const descriptionStyle = descriptions ? getComputedStyle(descriptions) : null;
                return {
                  card: card.dataset.dashboardHubCard || "",
                  height: Math.round(cardRect.height),
                  rowsHeight: rowsRect ? Math.round(rowsRect.height) : 0,
                  actionGapFromRows: rowsRect && actionRect ? Math.round(actionRect.top - rowsRect.bottom) : 0,
                  actionHeight: actionRect ? Math.round(actionRect.height) : 0,
                  rightGutterToButton: buttonRect ? Math.round(cardRect.right - buttonRect.right) : 0,
                  buttonWidth: buttonRect ? Math.round(buttonRect.width) : 0,
                  buttonHeight: buttonRect ? Math.round(buttonRect.height) : 0,
                  descriptionTextIndent: descriptionStyle ? descriptionStyle.textIndent : "",
                  descriptionTop: descriptions ? Math.round(descriptions.getBoundingClientRect().top - cardRect.top) : 0
                };
              });
              const headerRect = rectFor(header, 3);
              const subtitleRect = rectFor(subtitle, 4);
              const windowControlRect = rectFor(windowControls, 0);
              const titleGroupRect = rectFor(header, 0);
              const chromeRect = rectFor(chrome, 0);
              const firstRows = firstCard?.querySelector(".ai-control-center-card-rows");
              const firstAction = firstCard?.querySelector(".monitoring-hud__hub-actions");
              return JSON.stringify({
                title: document.querySelector(".monitoring-hud__title")?.textContent.trim() || "",
                subtitle: document.querySelector(".monitoring-hud__subtitle")?.textContent.replace(/\\s+/g, " ").trim() || "",
                surfaceRole: surface?.dataset.productSurfaceRole || "",
                aiControlCenterPlacement: surface?.dataset.aiControlCenterPlacement || "",
                dashboardIaModel: surface?.dataset.dashboardIaModel || "",
                dashboardSurfaceModel: surface?.dataset.dashboardSurfaceModel || "",
                childWindowModel: surface?.dataset.childWindowModel || "",
                sameWindowFocusedSectionPolicy: surface?.dataset.sameWindowFocusedSectionPolicy || "",
                defaultWindowWidth: surface?.dataset.defaultWindowWidth || "",
                defaultWindowHeight: surface?.dataset.defaultWindowHeight || "",
                titleBackingLayer: surface?.dataset.titleBackingLayer || "",
                cardOrder: surface?.dataset.dashboardCardOrder || "",
                cardNames,
                launchers,
                doorwayButtons,
                designProcessCopyPresent: /Refined|Option\\s+[A-Z]|target/i.test(document.body.innerText || ""),
                detachedWindowOpenCopyPresent: [...document.querySelectorAll(".monitoring-hud__button-label")]
                  .some((node) => ["Open", "Open Diagnostics", "Open Capabilities"].includes(node.textContent.trim())),
                cardTitles: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-card-title-copy strong")].map((node) => node.textContent.trim()),
                cardDescriptions: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-card-description")].map((node) => node.textContent.trim()),
                stripText: document.querySelector("[data-dashboard-role='global-ai-strip']")?.textContent.replace(/\\s+/g, " ").trim() || "",
                launcherActionRows: [...document.querySelectorAll("[data-dashboard-hub-card] .monitoring-hud__hub-actions")].map((row) => ({
                  contract: row.dataset.actionRowContract || "",
                  buttonCount: row.querySelectorAll("[data-category-doorway]").length,
                  followsRows: Boolean(row.previousElementSibling?.classList.contains("ai-control-center-card-rows")),
                  insideRows: Boolean(row.closest(".ai-control-center-card-rows"))
                })),
                layoutMetrics: {
                  surfaceWidth: surfaceRect ? Math.round(surfaceRect.width) : 0,
                  chromePaddingLeft: chromeStyle ? chromeStyle.paddingLeft : "",
                  chromePaddingRight: chromeStyle ? chromeStyle.paddingRight : "",
                  headerWidth: header ? Math.round(header.getBoundingClientRect().width) : 0,
                  hubPaddingTop: hubStyle ? hubStyle.paddingTop : "",
                  hubPaddingLeft: hubStyle ? hubStyle.paddingLeft : "",
                  hubPaddingRight: hubStyle ? hubStyle.paddingRight : "",
                  headerPaddingRight: headerCopyStyle ? headerCopyStyle.paddingRight : "",
                  titleBackingDisplay: titleBackingStyle ? titleBackingStyle.display : "",
                  titleBackingContent: titleBackingStyle ? titleBackingStyle.content : "",
                  titleBackingOpacity: titleBackingStyle ? titleBackingStyle.opacity : "",
                  titleBackingLayerRemoved: Boolean(titleBackingStyle && titleBackingStyle.display === "none"),
                  subtitleHeight: subtitle ? Math.round(subtitle.getBoundingClientRect().height) : 0,
                  subtitleLineHeight: subtitleStyle ? subtitleStyle.lineHeight : "",
                  subtitleLineCount: titleDescriptionWrap.lineCount,
                  subtitlePublishedMaxWidth: titleDescriptionWrap.publishedMaxWidth,
                  subtitleTitleCardInnerWidth: titleDescriptionWrap.titleGroupInnerWidth,
                  subtitleOverlapsWindowControls: intersects(subtitleRect, windowControlRect),
                  windowControlOuterTopOffset: windowControls && chrome ? Math.round(windowControlRect.top - chromeRect.top) : 0,
                  windowControlOuterRightOffset: windowControls && chrome ? Math.round(chromeRect.right - windowControlRect.right) : 0,
                  topGutter: firstCard && hub ? Math.round(firstCard.getBoundingClientRect().top - hub.getBoundingClientRect().top) : 0,
                  scrollbarVisible: surface?.dataset.customScrollbarVisible || "false",
                  rowMetrics,
                  cardVisualMetrics
                },
                proofRects: {
                  header: headerRect,
                  subtitleWrap: subtitleRect,
                  rowGutterCardDensity: rectFor(firstRows, 8),
                  buttonPlacement: rectFor(firstAction, 8),
                  firstCard: rectFor(firstCard, 4)
                },
                defaultScrollMetrics: (() => {
                  const hubRect = hub?.getBoundingClientRect();
                  const thirdRect = thirdCard?.getBoundingClientRect();
                  return {
                    clientHeight: hub ? Math.round(hub.clientHeight) : 0,
                    scrollHeight: hub ? Math.round(hub.scrollHeight) : 0,
                    maxScroll: hub ? Math.round(Math.max(0, hub.scrollHeight - hub.clientHeight)) : 0,
                    scrollTop: hub ? Math.round(hub.scrollTop) : 0,
                    thirdCardFullyVisibleAtDefault: Boolean(hubRect && thirdRect && thirdRect.top >= hubRect.top && thirdRect.bottom <= hubRect.bottom),
                    thirdCardPartiallyVisibleAtDefault: Boolean(hubRect && thirdRect && thirdRect.bottom > hubRect.top && thirdRect.top < hubRect.bottom)
                  };
                })(),
                rowGroups: Object.fromEntries([...document.querySelectorAll("[data-dashboard-hub-card]")].map((card) => [
                  card.dataset.dashboardHubCard || "",
                  [...card.querySelectorAll(".monitoring-hud__state-row")].map((row) => ({
                    label: row.querySelector("span")?.textContent.trim() || "",
                    value: row.querySelector("strong")?.textContent.trim() || ""
                  }))
                ])),
                stateTaxonomyRows: Object.fromEntries([...document.querySelectorAll("[data-dashboard-hub-card]")].map((card) => [
                  card.dataset.dashboardHubCard || "",
                  [...card.querySelectorAll(".monitoring-hud__state-row")].map((row) => ({
                    label: row.querySelector("span")?.textContent.trim() || "",
                    value: row.querySelector("strong")?.textContent.trim() || "",
                    taxonomyKey: row.dataset.stateTaxonomyKey || "",
                    taxonomyValue: row.dataset.stateTaxonomyValue || "",
                    viewModelKey: row.dataset.viewModelKey || "",
                    viewModelContract: row.dataset.viewModelContract || "",
                    viewModelBound: row.dataset.viewModelBound || ""
                  }))
                ])),
                stateTaxonomyContract: surface?.dataset.stateTaxonomyContract || "",
                stateTaxonomySource: surface?.dataset.stateTaxonomySource || "",
                stateTaxonomyRendering: surface?.dataset.stateTaxonomyRendering || "",
                viewModelContract: surface?.dataset.viewModelContract || "",
                viewModelSource: surface?.dataset.viewModelSource || "",
                viewModelState: surface?.dataset.viewModelState || "",
                viewModelProviderRuntimeBlocked: surface?.dataset.viewModelProviderRuntimeBlocked || "",
                viewModelPromptSendDisabled: surface?.dataset.viewModelPromptSendDisabled || "",
                viewModelProviderVisibleDataNone: surface?.dataset.viewModelProviderVisibleDataNone || "",
                viewModelRecoveryGuidance: surface?.dataset.viewModelRecoveryGuidance || "",
                dashboardViewModel: window.nexusAiControlCenterCurrentViewModel || null,
                stateTaxonomyRequiredStates: surface?.dataset.stateTaxonomyRequiredStates || "",
                stateTaxonomyRenderedStates: surface?.dataset.stateTaxonomyRenderedStates || "",
                stateTaxonomyComplete: surface?.dataset.stateTaxonomyComplete || "",
                aiPersonaState: surface?.dataset.aiPersonaState || "",
                aiStatusState: surface?.dataset.aiStatusState || "",
                providerModelRuntimeState: surface?.dataset.providerModelRuntimeState || "",
                providerVisibleDataState: surface?.dataset.providerVisibleDataState || "",
                noProviderState: surface?.dataset.noProviderState || "",
                promptExecutionState: surface?.dataset.promptExecutionState || "",
                trustBoundaryState: surface?.dataset.trustBoundaryState || "",
                stateTaxonomyCards: Object.fromEntries([...document.querySelectorAll("[data-dashboard-hub-card]")].map((card) => [
                  card.dataset.dashboardHubCard || "",
                  {
                    contract: card.dataset.stateTaxonomyContract || "",
                    scope: card.dataset.stateTaxonomyScope || "",
                    renderedStates: card.dataset.stateTaxonomyRenderedStates || "",
                    complete: card.dataset.stateTaxonomyComplete || "",
                    aiPersonaState: card.dataset.aiPersonaState || "",
                    providerModelRuntimeState: card.dataset.providerModelRuntimeState || "",
                    providerVisibleDataState: card.dataset.providerVisibleDataState || "",
                    noProviderState: card.dataset.noProviderState || "",
                    retryState: card.dataset.retryState || "",
                    recoveryState: card.dataset.recoveryState || "",
                    promptExecutionState: card.dataset.promptExecutionState || "",
                    noProviderDiagnosticsFlow: card.dataset.noProviderDiagnosticsFlow || "",
                    noProviderFlowState: card.dataset.noProviderFlowState || "",
                    unavailableCapabilityState: card.dataset.unavailableCapabilityState || "",
                    blockedActionState: card.dataset.blockedActionState || "",
                    capabilitiesBoundaryContract: card.dataset.capabilitiesBoundaryContract || "",
                    capabilityPackLifecycleState: card.dataset.capabilityPackLifecycleState || "",
                    capabilityPackDownloadState: card.dataset.capabilityPackDownloadState || "",
                    installIntentState: card.dataset.installIntentState || "",
                    capabilityPackInstallState: card.dataset.capabilityPackInstallState || "",
                    capabilityPackUpdateState: card.dataset.capabilityPackUpdateState || "",
                    capabilityPackUninstallState: card.dataset.capabilityPackUninstallState || "",
                    developerLaneBoundaryState: card.dataset.developerLaneBoundaryState || "",
                    ownerLaneBoundaryState: card.dataset.ownerLaneBoundaryState || "",
                    privateSetupBoundaryState: card.dataset.privateSetupBoundaryState || "",
                    privateSetupAuthorized: card.dataset.privateSetupAuthorized || "",
                    privateMaterialVisible: card.dataset.privateMaterialVisible || "",
                    ownerMemoryEnabled: card.dataset.ownerMemoryEnabled || "",
                    ownerAgentsEnabled: card.dataset.ownerAgentsEnabled || "",
                    downloadExecution: card.dataset.downloadExecution || "",
                    installExecution: card.dataset.installExecution || "",
                    updateExecution: card.dataset.updateExecution || "",
                    fetchExecution: card.dataset.fetchExecution || "",
                    capabilityExecution: card.dataset.capabilityExecution || "",
                    packagingExecution: card.dataset.packagingExecution || "",
                    viewModelPrivateSetupBlocked: card.dataset.viewModelPrivateSetupBlocked || "",
                    viewModelOwnerMemoryAgentsBlocked: card.dataset.viewModelOwnerMemoryAgentsBlocked || ""
                  }
                ])),
                stateTaxonomyStripPairs: [...document.querySelectorAll("[data-dashboard-role='global-ai-strip'] .monitoring-hud__surface-role-pair")].map((pair) => ({
                  text: pair.textContent.replace(/\\s+/g, " ").trim(),
                  key: pair.dataset.stateTaxonomyKey || "",
                  value: pair.dataset.stateTaxonomyValue || ""
                })),
                capabilityHubRows: document.querySelectorAll('[data-dashboard-hub-card="capabilities-maintenance"] .monitoring-hud__state-row').length,
                settingsRouteMetadata: document.getElementById("monitoring-hud")?.dataset.settingsRoute || "",
                titleStatusWrapMetadata: document.getElementById("monitoring-hud")?.dataset.titleStatusWrap || "",
                titleDescriptionWrapMetadata: document.getElementById("monitoring-hud")?.dataset.titleDescriptionWrap || "",
                rowTitleSizingMetadata: document.getElementById("monitoring-hud")?.dataset.rowTitleSizing || "",
                titleStatusPillWrap,
                titleDescriptionWrap,
                rowTitleSizingProbe,
                belowTitleTextWeightProbe,
                settingsTooltipText: document.getElementById("ai-dashboard-settings-tooltip")?.textContent.trim() || "",
                settingsRoutePresent: Boolean(document.querySelector("[data-dashboard-utility-row='settings-route']")),
                settingsVisualAcceptance: document.querySelector("[data-dashboard-utility-row='settings-route']")?.dataset.settingsVisualAcceptance || "",
                settingsBehavior: document.querySelector("[data-dashboard-utility-row='settings-route']")?.dataset.settingsBehavior || "",
                settingsButtonState: document.getElementById("ai-dashboard-settings-action")?.dataset.settingsState || "",
                settingsWindowOpened: document.getElementById("ai-dashboard-settings-action")?.dataset.settingsWindowOpened || "",
                settingsRouteVisible: (() => {
                  const row = document.querySelector("[data-dashboard-utility-row='settings-route']");
                  if (!row) return false;
                  const style = getComputedStyle(row);
                  const rect = row.getBoundingClientRect();
                  return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
                })(),
                settingsButtonPresent: Boolean(document.getElementById("ai-dashboard-settings-action")),
                settingsButtonVisible: (() => {
                  const button = document.getElementById("ai-dashboard-settings-action");
                  if (!button) return false;
                  const style = getComputedStyle(button);
                  const rect = button.getBoundingClientRect();
                  return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
                })(),
                focusedSurfaceCount: document.querySelectorAll("[data-focused-surface]").length,
                domainSurfaceCount: document.querySelectorAll("[data-domain-surface]").length,
                localCheckInline: Boolean(document.getElementById("ai-control-center-local-check-action")),
                generateInline: Boolean(document.getElementById("ai-control-center-generate-report-action")),
                copyInline: Boolean(document.getElementById("ai-control-center-copy-report-action")),
                visibleSettingsFutureText: document.body.innerText.includes("Settings future-gated"),
                activeAiText: document.body.innerText.includes("Active AI"),
                trustProviderText: document.body.innerText.includes("Trust & Provider"),
                nativeTitleTooltipCount: document.querySelectorAll("[title]").length
              });
            })();
            """,
        )
    )
    dashboard_probe["visualGrammar"] = _run_visual_grammar_probe(app, dialog)
    settings_option_b_disposition = _write_settings_option_b_disposition(log_root)
    settings_tooltip_probe = json.loads(
        _run_js(
            app,
            dialog,
            """
            (() => {
              const tooltip = document.getElementById("ai-dashboard-settings-tooltip");
              const style = tooltip ? getComputedStyle(tooltip) : null;
              const rect = tooltip ? tooltip.getBoundingClientRect() : null;
              return JSON.stringify({
                present: Boolean(tooltip),
                text: tooltip?.textContent.trim() || "",
                opacity: style ? Number(style.opacity) : 0,
                display: style ? style.display : "",
                visibility: style ? style.visibility : "",
                visible: style && rect ? style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0 : false,
                label: document.getElementById("ai-dashboard-settings-action")?.getAttribute("aria-label") || "",
                state: document.getElementById("ai-dashboard-settings-action")?.dataset.settingsState || "",
                windowOpened: document.getElementById("ai-dashboard-settings-action")?.dataset.settingsWindowOpened || "",
                route: document.getElementById("ai-dashboard-settings-action")?.dataset.settingsRoute || "",
                titleCount: document.querySelectorAll("[title]").length
              });
            })();
            """,
        )
    )
    proof_rects = dashboard_probe.get("proofRects") if isinstance(dashboard_probe.get("proofRects"), dict) else {}
    proof_crops = {
        "focusedTitleHeader": _capture_window_region(app, dialog, log_root, "04_focused_title_header", proof_rects.get("header")),
        "subtitleWrap": _capture_window_region(app, dialog, log_root, "05_subtitle_wrap", proof_rects.get("subtitleWrap")),
        "rowGutterCardDensity": _capture_window_region(app, dialog, log_root, "06_row_gutter_card_density", proof_rects.get("rowGutterCardDensity")),
        "buttonPlacement": _capture_window_region(app, dialog, log_root, "07_button_placement", proof_rects.get("buttonPlacement")),
        "firstCardDensity": _capture_window_region(app, dialog, log_root, "08_first_card_density", proof_rects.get("firstCard")),
    }
    fam007_h4_root = Path.home() / "OneDrive" / "Pictures" / "Screenshots" / "Nexus Desktop AI" / "FAM-007-H4"
    main_runtime_ai_control_center_reference = _capture_main_runtime_ai_control_center_reference(log_root)
    previous_parent_dashboard_reference = _copy_reference_image(
        fam007_h4_root
        / "20260624-214952-parent-dashboard"
        / "01_dashboard_initial_focused_window.png",
        log_root,
        "11_before_parent_dashboard_density_reference",
    )
    visual_comparison_boards = {
        "currentVsMainRuntimeOldAiControlCenter": _write_side_by_side_board(
            Path(screenshots["dashboard_initial"]["focusedWindow"]),
            Path(str(main_runtime_ai_control_center_reference.get("focusedWindow", ""))),
            log_root / "12_current_vs_main_runtime_old_ai_control_center.png",
            "Current repaired parent AI Dashboard",
            "Main runtime old AI Control Center",
        ) if main_runtime_ai_control_center_reference.get("ok") else {
            "ok": False,
            "reason": main_runtime_ai_control_center_reference.get("reason", "missing-reference"),
        },
        "beforeAfterParentDensity": _write_side_by_side_board(
            Path(str(previous_parent_dashboard_reference.get("path", ""))),
            Path(screenshots["dashboard_initial"]["focusedWindow"]),
            log_root / "13_before_after_parent_dashboard_density.png",
            "Before returned defect proof",
            "Current repaired parent AI Dashboard",
        ) if previous_parent_dashboard_reference.get("ok") else {
            "ok": False,
            "reason": previous_parent_dashboard_reference.get("reason", "missing-reference"),
        },
    }
    visual_grammar_audit = _write_visual_grammar_audit(
        log_root,
        dashboard_probe,
        main_runtime_ai_control_center_reference,
    )
    resize_edge_hit_zone_probe = _ai_dashboard_resize_hit_zone_probe(app, dialog)

    child_windows_visible_before_close = {
        "control-center": False,
        "readiness-diagnostics": False,
        "capabilities-maintenance": False,
    }
    child_chrome_probe = {}
    child_geometry_behavior = {}
    child_native_hit_test_diagnostic = {}
    child_minimum_geometry_scroll_diagnostic = {}
    child_comparison_boards = {}
    control_center_result = {}
    readiness_result = {}
    capabilities_result = {}
    singleton_focus = {}
    child_control_behavior = {}
    opened_desktop_hashes = {}
    domain_launch_probe = {
        "domainWindowCount": len(dialog._domain_windows),
        "domainWindowKeys": sorted(dialog._domain_windows.keys()),
        "acceptedScope": "SLC-001-active-domain-doorways",
        "detachedChildWindowDisposition": "active-domain-window-route-lifecycle",
        "launches": {},
    }

    dashboard_rect_before_resize = _rect(int(dialog.winId()))
    _run_js(
        app,
        dialog,
        """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          if (hub) {
            hub.scrollTop = hub.scrollHeight;
            if (window.nexusAiControlCenterSyncScrollbar) {
              window.nexusAiControlCenterSyncScrollbar();
            }
          }
          return "true";
        })();
        """,
    )
    _pump(app, 250)
    scrolled_probe = json.loads(
        _run_js(
            app,
            dialog,
            """
            (() => {
              const hub = document.getElementById("ai-control-center-card-hub");
              const thirdCard = document.querySelector('[data-dashboard-hub-card="capabilities-maintenance"]');
              const hubRect = hub?.getBoundingClientRect();
              const thirdRect = thirdCard?.getBoundingClientRect();
              return JSON.stringify({
                scrollTop: hub ? Math.round(hub.scrollTop) : 0,
                maxScroll: hub ? Math.round(Math.max(0, hub.scrollHeight - hub.clientHeight)) : 0,
                thirdCardFullyVisibleAfterScroll: Boolean(hubRect && thirdRect && thirdRect.top >= hubRect.top && thirdRect.bottom <= hubRect.bottom),
                thirdCardPartiallyVisibleAfterScroll: Boolean(hubRect && thirdRect && thirdRect.bottom > hubRect.top && thirdRect.top < hubRect.bottom)
              });
            })();
            """,
        )
    )
    screenshots["dashboard_scrolled_bottom"] = _capture_window(
        app,
        dialog,
        log_root,
        "02_dashboard_scrolled_bottom",
    )
    _run_js(
        app,
        dialog,
        """
        (() => {
          const hub = document.getElementById("ai-control-center-card-hub");
          if (hub) {
            hub.scrollTop = 0;
            if (window.nexusAiControlCenterSyncScrollbar) {
              window.nexusAiControlCenterSyncScrollbar();
            }
          }
          return "true";
        })();
        """,
    )
    _pump(app, 180)
    horizontal_resize_proof = _drive_ai_dashboard_horizontal_resize(app, dialog, log_root)
    screenshots["dashboard_horizontal_shrink"] = horizontal_resize_proof.get("screenshots", {})
    dialog.resize(dialog.DEFAULT_WIDTH, dialog.DEFAULT_HEIGHT)
    _pump(app, 260)
    dialog.resize(dialog.width() + 42, dialog.height() + 28)
    _pump(app, 300)
    dashboard_rect_after_resize = _rect(int(dialog.winId()))
    screenshots["dashboard_resized"] = _capture_window(
        app,
        dialog,
        log_root,
        "03_dashboard_resized",
    )
    dashboard_resize_proof = {
        "before": dashboard_rect_before_resize,
        "after": dashboard_rect_after_resize,
        "widthDelta": dashboard_rect_after_resize["width"] - dashboard_rect_before_resize["width"],
        "heightDelta": dashboard_rect_after_resize["height"] - dashboard_rect_before_resize["height"],
    }

    doorway_launch_contract = {
        "control-center": {
            "buttonId": "ai-control-center-open-control-surface-action",
            "classification": "exclusive-child",
            "lifecycle": "closes-with-dashboard",
            "title": "AI Control Center",
        },
        "readiness-diagnostics": {
            "buttonId": "ai-control-center-open-readiness-surface-action",
            "classification": "external-unique",
            "lifecycle": "stays-open-if-dashboard-closes",
            "title": "AI Readiness & Diagnostics",
        },
        "capabilities-maintenance": {
            "buttonId": "ai-control-center-open-maintenance-surface-action",
            "classification": "exclusive-child",
            "lifecycle": "closes-with-dashboard",
            "title": "Capabilities & Maintenance",
        },
    }
    for domain_id, contract in doorway_launch_contract.items():
        launch, window, previous_keys = _open_from_dashboard(
            app,
            dialog,
            str(contract["buttonId"]),
            domain_id,
        )
        _pump(app, 500)
        probe = _probe_child_window(app, window)
        child_chrome_probe[domain_id] = probe
        if window is not None:
            child_native_hit_test_diagnostic[domain_id] = _supporting_native_hit_test_contract(window)
            child_minimum_geometry_scroll_diagnostic[domain_id] = _supporting_minimum_geometry_scroll_probe(
                app,
                window,
            )
            child_geometry_behavior[domain_id] = {
                "move": _supporting_qtest_drag_child_window(app, window),
                "resize": _supporting_qtest_resize_child_window(app, window),
            }
            screenshots[f"child_{domain_id}"] = _capture_window(
                app,
                window,
                log_root,
                f"17_child_{domain_id}",
            )
            reference_focus = Path(str(main_runtime_ai_control_center_reference.get("focusedWindow", "")))
            child_focus = Path(screenshots[f"child_{domain_id}"]["focusedWindow"])
            child_comparison_boards[domain_id] = _write_child_contact_sheet(
                reference_focus,
                child_focus,
                log_root / f"18_child_{domain_id}_purpose_contact_sheet.png",
                "Main runtime old AI Control Center",
                f"{contract['title']} child/domain",
            ) if reference_focus.exists() else {
                "ok": False,
                "reason": "missing-main-runtime-comparator",
                "domain": domain_id,
            }
            opened_desktop_hashes[domain_id] = _hash_file(
                screenshots[f"child_{domain_id}"]["fullDesktop"]
            )
        domain_launch_probe["launches"][domain_id] = {
            **launch,
            "previousDomainWindowKeys": sorted(previous_keys),
            "windowPresent": window is not None,
            "visible": bool(window and window.isVisible()),
            "windowObjectId": id(window) if window is not None else 0,
            "domainWindowKeysAfterLaunch": sorted(dialog._domain_windows.keys()),
            "expectedClassification": contract["classification"],
            "expectedLifecycle": contract["lifecycle"],
            "expectedTitle": contract["title"],
        }
    domain_launch_probe["domainWindowCountAfterLaunch"] = len(dialog._domain_windows)
    domain_launch_probe["domainWindowKeysAfterLaunch"] = sorted(dialog._domain_windows.keys())

    control_window = dialog._domain_windows.get("control-center")
    singleton_before_keys = sorted(dialog._domain_windows.keys())
    singleton_before_id = id(control_window) if control_window is not None else 0
    singleton_launch, singleton_after_window, singleton_previous_keys = _open_from_dashboard(
        app,
        dialog,
        "ai-control-center-open-control-surface-action",
        "control-center",
    )
    _pump(app, 400)
    singleton_focus = {
        "domain": "control-center",
        "beforeKeys": singleton_before_keys,
        "previousKeysForSecondLaunch": sorted(singleton_previous_keys),
        "afterKeys": sorted(dialog._domain_windows.keys()),
        "beforeObjectId": singleton_before_id,
        "afterObjectId": id(singleton_after_window) if singleton_after_window is not None else 0,
        "sameWindowObject": bool(
            singleton_before_id
            and singleton_after_window is not None
            and singleton_before_id == id(singleton_after_window)
        ),
        "secondLaunch": singleton_launch,
        "visibleAfterSecondLaunch": bool(singleton_after_window and singleton_after_window.isVisible()),
    }

    readiness_window = dialog._domain_windows.get("readiness-diagnostics")
    readiness_result = _exercise_readiness_child_window(app, readiness_window, log_root)
    readiness_visual_state_names = {
        "beforeRun": "readiness_before_run",
        "afterLocalCheck": "readiness_after_local_check",
        "afterReportGeneration": "readiness_after_report_generation",
        "afterCopyAction": "readiness_after_copy_action",
    }
    readiness_visual_screenshots = (
        readiness_result.get("visualProofScreenshots")
        if isinstance(readiness_result, dict)
        else {}
    )
    if isinstance(readiness_visual_screenshots, dict):
        for state_key, screenshot_key in readiness_visual_state_names.items():
            screenshot_paths = readiness_visual_screenshots.get(state_key)
            if isinstance(screenshot_paths, dict):
                screenshots[screenshot_key] = screenshot_paths
    control_window = dialog._domain_windows.get("control-center")
    control_center_result = _exercise_control_center_child_window(app, control_window, log_root)
    control_visual_state_names = {
        "beforeBoundary": "control_before_boundary_review",
        "afterBoundaryReview": "control_after_boundary_review",
        "afterRecoveryRoute": "control_after_recovery_route",
        "afterStateTaxonomy": "control_after_state_taxonomy",
    }
    control_visual_screenshots = (
        control_center_result.get("visualProofScreenshots")
        if isinstance(control_center_result, dict)
        else {}
    )
    if isinstance(control_visual_screenshots, dict):
        for state_key, screenshot_key in control_visual_state_names.items():
            screenshot_paths = control_visual_screenshots.get(state_key)
            if isinstance(screenshot_paths, dict):
                screenshots[screenshot_key] = screenshot_paths
    capabilities_window = dialog._domain_windows.get("capabilities-maintenance")
    capabilities_result = _exercise_capabilities_child_window(app, capabilities_window, log_root)
    capabilities_visual_state_names = {
        "beforeLifecycle": "capabilities_before_lifecycle_review",
        "afterLifecycleReview": "capabilities_after_lifecycle_review",
        "afterEditionGates": "capabilities_after_edition_gates",
        "afterMaintenanceHold": "capabilities_after_maintenance_hold",
    }
    capabilities_visual_screenshots = (
        capabilities_result.get("visualProofScreenshots")
        if isinstance(capabilities_result, dict)
        else {}
    )
    if isinstance(capabilities_visual_screenshots, dict):
        for state_key, screenshot_key in capabilities_visual_state_names.items():
            screenshot_paths = capabilities_visual_screenshots.get(state_key)
            if isinstance(screenshot_paths, dict):
                screenshots[screenshot_key] = screenshot_paths
    child_control_behavior = {
        "controlCenterLocalBoundaryReview": control_center_result,
        "readinessLocalCheckReportCopy": readiness_result,
        "capabilitiesMaintenanceDisplayWorkflow": capabilities_result,
        "providerExecutionEvents": [
            event for event in events
            if "AI_DASHBOARD_DOMAIN_WINDOW_COMMAND" in event
            or "AI_DASHBOARD_CATEGORY_LAUNCHER_OPENED_WINDOW" in event
            or "AI_DASHBOARD_DOMAIN_WINDOW_VISIBLE" in event
        ],
    }
    for domain_id, window in list(dialog._domain_windows.items()):
        child_windows_visible_before_close[domain_id] = bool(window and window.isVisible())

    dialog.close()
    _pump(app, 500)
    post_close_windows = {
        domain_id: window
        for domain_id, window in list(dialog._domain_windows.items())
    }
    lifecycle_after_dashboard_close = {
        "controlVisible": bool(post_close_windows.get("control-center") and post_close_windows["control-center"].isVisible()),
        "maintenanceVisible": bool(post_close_windows.get("capabilities-maintenance") and post_close_windows["capabilities-maintenance"].isVisible()),
        "readinessVisible": bool(post_close_windows.get("readiness-diagnostics") and post_close_windows["readiness-diagnostics"].isVisible()),
    }
    for window in list(post_close_windows.values()):
        try:
            window.close()
        except RuntimeError:
            pass
    _pump(app, 220)

    duplicate_full_desktop_proof = len(set(opened_desktop_hashes.values())) != len(opened_desktop_hashes)
    actual_doorway_labels = [button.get("text") for button in dashboard_probe.get("doorwayButtons") or []]
    expected_option_g_rows = {
        "control-center": [
            {"label": "AI Persona", "value": "None; ORIN persona not implemented"},
            {"label": "Provider", "value": "Blocked; no model path active"},
            {"label": "Privacy", "value": "Protected; no provider or third-party tracking"},
        ],
        "readiness-diagnostics": [
            {"label": "Check", "value": "Waiting for USER action"},
            {"label": "Report", "value": "Local decision aid behind diagnostics"},
            {"label": "Prompt", "value": "Not accepted, sent, stored, or indexed"},
        ],
        "capabilities-maintenance": [
            {"label": "Packs", "value": "Install blocked; downloads disabled"},
            {"label": "Updates", "value": "Future-gated; no install execution"},
        ],
    }
    row_label_lengths = [
        len(str(row.get("label") or ""))
        for rows in expected_option_g_rows.values()
        for row in rows
    ]
    title_status_pill_wrap = dashboard_probe.get("titleStatusPillWrap") or {}
    title_description_wrap = dashboard_probe.get("titleDescriptionWrap") or {}
    horizontal_layout = horizontal_resize_proof.get("layout") if isinstance(horizontal_resize_proof, dict) else {}
    horizontal_layout = horizontal_layout if isinstance(horizontal_layout, dict) else {}
    horizontal_title_status_pill_wrap = horizontal_layout.get("titleStatusPillWrap") or {}
    horizontal_title_description_wrap = horizontal_layout.get("titleDescriptionWrap") or {}
    no_early_wrap_proof = horizontal_resize_proof.get("noEarlyWrapProof") if isinstance(horizontal_resize_proof, dict) else {}
    no_early_wrap_proof = no_early_wrap_proof if isinstance(no_early_wrap_proof, dict) else {}
    no_early_wrap_layout = no_early_wrap_proof.get("layout") if isinstance(no_early_wrap_proof, dict) else {}
    no_early_wrap_layout = no_early_wrap_layout if isinstance(no_early_wrap_layout, dict) else {}
    no_early_title_status_pill_wrap = no_early_wrap_layout.get("titleStatusPillWrap") or {}
    no_early_title_description_wrap = no_early_wrap_layout.get("titleDescriptionWrap") or {}
    row_title_sizing_probe = dashboard_probe.get("rowTitleSizingProbe") or {}
    horizontal_row_title_sizing_probe = horizontal_layout.get("rowTitleSizingProbe") or {}
    horizontal_wrap_crop = horizontal_resize_proof.get("wrapCrop") if isinstance(horizontal_resize_proof, dict) else {}
    horizontal_wrap_crop = horizontal_wrap_crop if isinstance(horizontal_wrap_crop, dict) else {}
    horizontal_title_description_wrap_crop = horizontal_resize_proof.get("titleDescriptionWrapCrop") if isinstance(horizontal_resize_proof, dict) else {}
    horizontal_title_description_wrap_crop = horizontal_title_description_wrap_crop if isinstance(horizontal_title_description_wrap_crop, dict) else {}
    below_title_text_weight_probe = dashboard_probe.get("belowTitleTextWeightProbe") or {}

    def _title_column_map(probe: object) -> dict[str, int]:
        if not isinstance(probe, dict):
            return {}
        rows = probe.get("rowMetrics")
        if not isinstance(rows, list):
            return {}
        mapped: dict[str, int] = {}
        for row in rows:
            if not isinstance(row, dict):
                continue
            key = str(row.get("key") or "")
            if not key:
                continue
            mapped[key] = int(row.get("titleColumnWidth") or 0)
        return mapped

    default_title_columns = _title_column_map(row_title_sizing_probe)
    horizontal_title_columns = _title_column_map(horizontal_row_title_sizing_probe)
    title_columns_stable_across_resize = (
        bool(default_title_columns)
        and default_title_columns.keys() == horizontal_title_columns.keys()
        and all(
            abs(int(default_title_columns[key]) - int(horizontal_title_columns[key])) <= 1
            for key in default_title_columns
        )
    )

    layout_metrics = dashboard_probe.get("layoutMetrics") or {}
    row_heights = [
        int(row.get("height") or 0)
        for row in layout_metrics.get("rowMetrics") or []
    ]
    card_visual_metrics = layout_metrics.get("cardVisualMetrics") or []
    card_heights = [
        int(card.get("height") or 0)
        for card in card_visual_metrics
    ]
    action_gaps = [
        int(card.get("actionGapFromRows") or 0)
        for card in card_visual_metrics
    ]
    button_right_gutters = [
        int(card.get("rightGutterToButton") or 0)
        for card in card_visual_metrics
    ]
    description_indents = [
        str(card.get("descriptionTextIndent") or "")
        for card in card_visual_metrics
    ]
    proof_crops_ok = all(item.get("ok") is True for item in proof_crops.values())
    required_reference_images_ok = (
        main_runtime_ai_control_center_reference.get("ok") is True
    )
    visual_boards_ok = (
        visual_comparison_boards["currentVsMainRuntimeOldAiControlCenter"].get("ok") is True
        and visual_comparison_boards["beforeAfterParentDensity"].get("ok") is True
    )
    doorway_buttons = dashboard_probe.get("doorwayButtons") or []

    def _int_or(value: object, fallback: int = -999) -> int:
        try:
            return int(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return fallback

    def _row_stack_vertical_gutter_ok(probe: object) -> bool:
        if not isinstance(probe, dict):
            return False
        if probe.get("rowCount") != 8:
            return False
        if _int_or(probe.get("rowVerticalGutterPx")) != 6:
            return False
        if probe.get("rowVerticalGutterRestored") is not True:
            return False
        stacks = probe.get("rowStackMetrics")
        if not isinstance(stacks, list) or len(stacks) != 3:
            return False
        for stack, expected_count in zip(stacks, [3, 3, 2]):
            if not isinstance(stack, dict):
                return False
            if _int_or(stack.get("rowCount")) != expected_count:
                return False
            if _int_or(stack.get("rowGapPx")) != 6:
                return False
            if _int_or(stack.get("expectedRowVerticalGutterPx")) != 6:
                return False
            if stack.get("rowGapMatchesToken") is not True:
                return False
            if stack.get("pairGapsMatchToken") is not True:
                return False
            pair_gaps = stack.get("pairGaps")
            if not isinstance(pair_gaps, list) or len(pair_gaps) != expected_count - 1:
                return False
            if any(abs(_int_or(gap) - 6) > 1 for gap in pair_gaps):
                return False
        return True

    def _shared_status_value_column_ok(probe: object) -> bool:
        if not isinstance(probe, dict):
            return False
        if probe.get("rowCount") != 8:
            return False
        if probe.get("labelColumnSource") != "measured-max-visible-label-content-px":
            return False
        if probe.get("labelColumnUnit") != "px":
            return False
        if probe.get("rowValueColumnContract") != "shared-max-label-content-plus-fixed-gutter":
            return False
        if probe.get("declaredLabelColumnWidthIsPx") is not True:
            return False
        if probe.get("declaredLabelColumnMatchesMeasuredMax") is not True:
            return False
        if _int_or(probe.get("declaredLabelColumnWidth")) <= 0:
            return False
        if _int_or(probe.get("contractLabelColumnWidth")) != _int_or(probe.get("declaredLabelColumnWidth")):
            return False
        if abs(_int_or(probe.get("maxLabelColumnExcessPx"), 999)) > 2:
            return False
        if abs(_int_or(probe.get("maxTitleColumnExcessPx"), 999)) > 2:
            return False
        if _int_or(probe.get("rowGutterPx")) != 8:
            return False
        if probe.get("contentSized") is not True:
            return False
        if probe.get("valueColumnDerivedFromLabelContent") is not True:
            return False
        if probe.get("valueColumnDerivedFromMaxLabelContent") is not True:
            return False
        if probe.get("fixedColumnGutterRestored") is not True:
            return False
        if probe.get("uniformValueColumnOffset") is not True:
            return False
        if probe.get("uniformValueLeftEdge") is not True:
            return False
        rows = probe.get("rowMetrics")
        if not isinstance(rows, list) or len(rows) != 8:
            return False
        contract_width = _int_or(probe.get("contractLabelColumnWidth"))
        expected_offset = contract_width + 8
        for row in rows:
            if not isinstance(row, dict):
                return False
            if abs(_int_or(row.get("titleColumnWidth")) - contract_width) > 2:
                return False
            if abs(_int_or(row.get("fixedColumnGutterPx")) - 8) > 2:
                return False
            if abs(_int_or(row.get("valueColumnOffset")) - expected_offset) > 2:
                return False
            if row.get("titleColumnMatchesContract") is not True:
                return False
            if row.get("valueColumnOffsetMatchesContract") is not True:
                return False
            if row.get("fixedColumnGutterMatchesToken") is not True:
                return False
        return True

    def _title_description_wrap_ok(probe: object, *, min_lines: int = 1, max_lines: int | None = None) -> bool:
        if not isinstance(probe, dict):
            return False
        if probe.get("metadata") != "measured-title-card-prose-word-wrap":
            return False
        if probe.get("columnSource") != "title-card-inner-content-width-px":
            return False
        if probe.get("groupCount") != 0:
            return False
        if probe.get("expectedTextPresent") is not True:
            return False
        if probe.get("noAtomicPhraseGroups") is not True:
            return False
        if probe.get("containerUsesProseWordWrap") is not True:
            return False
        if probe.get("fixedLegacyMaxWidthRemoved") is not True:
            return False
        if probe.get("measuredWidthMatchesTitleCardInner") is not True:
            return False
        if probe.get("wordsCanWrapIndividually") is not True:
            return False
        if _int_or(probe.get("publishedMaxWidth")) <= 0:
            return False
        if _int_or(probe.get("titleGroupInnerWidth")) <= 0:
            return False
        if _int_or(probe.get("clippedWordCount"), 999) != 0:
            return False
        if _int_or(probe.get("wordCount")) < 14:
            return False
        line_count = _int_or(probe.get("lineCount"))
        if line_count < min_lines:
            return False
        if max_lines is not None and line_count > max_lines:
            return False
        return True

    expected_doorway_buttons = {
        "control-center": {
            "target": "control-center",
            "kind": "exclusive-child",
            "command": "open-control-center-child-window",
            "lifecycle": "closes-with-dashboard",
        },
        "readiness-diagnostics": {
            "target": "readiness-diagnostics",
            "kind": "external-unique",
            "command": "open-readiness-diagnostics-child-window",
            "lifecycle": "stays-open-if-dashboard-closes",
        },
        "capabilities-maintenance": {
            "target": "capabilities-maintenance",
            "kind": "exclusive-child",
            "command": "open-maintenance-lifecycle-child-window",
            "lifecycle": "closes-with-dashboard",
        },
    }
    doorway_buttons_by_id = {
        str(button.get("doorway") or ""): button
        for button in doorway_buttons
        if isinstance(button, dict)
    }
    provider_payload = provider_state.as_renderer_payload()
    provider_taxonomy_states = {
        str(item.get("state") or "")
        for item in provider_payload.get("aiControlCenterStateTaxonomy", [])
        if isinstance(item, dict)
    }

    def _states_from_text(value: object) -> set[str]:
        return {part for part in str(value or "").split() if part}

    def _dashboard_state_taxonomy_ok() -> bool:
        cards = dashboard_probe.get("stateTaxonomyCards")
        rows = dashboard_probe.get("stateTaxonomyRows")
        pairs = dashboard_probe.get("stateTaxonomyStripPairs")
        if not isinstance(cards, dict) or not isinstance(rows, dict) or not isinstance(pairs, list):
            return False
        control_card = cards.get("control-center")
        readiness_card = cards.get("readiness-diagnostics")
        capabilities_card = cards.get("capabilities-maintenance")
        if not isinstance(control_card, dict) or not isinstance(readiness_card, dict) or not isinstance(capabilities_card, dict):
            return False
        if dashboard_probe.get("stateTaxonomyContract") != STATE_TAXONOMY_CONTRACT:
            return False
        if dashboard_probe.get("stateTaxonomySource") != "AIProviderStateSnapshot.aiControlCenterStateTaxonomy":
            return False
        if dashboard_probe.get("stateTaxonomyComplete") != "true":
            return False
        if not REQUIRED_STATE_TAXONOMY_STATES.issubset(_states_from_text(dashboard_probe.get("stateTaxonomyRequiredStates"))):
            return False
        if not REQUIRED_STATE_TAXONOMY_STATES.issubset(_states_from_text(dashboard_probe.get("stateTaxonomyRenderedStates"))):
            return False
        if not REQUIRED_STATE_TAXONOMY_STATES.issubset(provider_taxonomy_states):
            return False
        if dashboard_probe.get("aiPersonaState") != "none-orin-persona-not-implemented":
            return False
        if dashboard_probe.get("aiStatusState") != "not-implemented":
            return False
        if dashboard_probe.get("providerModelRuntimeState") != "blocked-no-model-path":
            return False
        if dashboard_probe.get("providerVisibleDataState") != "none":
            return False
        if dashboard_probe.get("noProviderState") != "no-provider-fail-closed":
            return False
        if dashboard_probe.get("promptExecutionState") != "prompt-send-disabled":
            return False
        if dashboard_probe.get("trustBoundaryState") != "local-only-no-egress-no-memory-no-cache":
            return False
        if any(pair.get("key") == "" or pair.get("value") == "" for pair in pairs if isinstance(pair, dict)):
            return False
        expected_control_taxonomy_rows = [
            {
                "label": "AI Persona",
                "value": "None; ORIN persona not implemented",
                "taxonomyKey": "ai-persona",
                "taxonomyValue": "none-orin-persona-not-implemented",
            },
            {
                "label": "Provider",
                "value": "Blocked; no model path active",
                "taxonomyKey": "provider-model-runtime",
                "taxonomyValue": "blocked-no-model-path",
            },
            {
                "label": "Privacy",
                "value": "Protected; no provider or third-party tracking",
                "taxonomyKey": "provider-visible-data",
                "taxonomyValue": "none",
            },
        ]
        control_rows = rows.get("control-center")
        control_rows_ok = (
            isinstance(control_rows, list)
            and len(control_rows) == len(expected_control_taxonomy_rows)
            and all(
                isinstance(actual, dict)
                and all(actual.get(key) == value for key, value in expected.items())
                for actual, expected in zip(control_rows, expected_control_taxonomy_rows)
            )
        )
        return (
            control_card.get("contract") == STATE_TAXONOMY_CONTRACT
            and control_card.get("scope") == "ai-control-center-card-1"
            and control_card.get("complete") == "true"
            and control_card.get("aiPersonaState") == "none-orin-persona-not-implemented"
            and control_card.get("providerModelRuntimeState") == "blocked-no-model-path"
            and control_card.get("providerVisibleDataState") == "none"
            and control_card.get("noProviderState") == "no-provider-fail-closed"
            and readiness_card.get("retryState") == "retry-local-check-only"
            and readiness_card.get("recoveryState") == "recovery-local-only"
            and readiness_card.get("promptExecutionState") == "prompt-send-disabled"
            and capabilities_card.get("unavailableCapabilityState") == "unavailable-capability"
            and capabilities_card.get("blockedActionState") == "blocked-action"
            and control_rows_ok
        )

    def _dashboard_view_model_ok() -> bool:
        view_model = dashboard_probe.get("dashboardViewModel")
        rows = dashboard_probe.get("stateTaxonomyRows")
        if not isinstance(view_model, dict) or not isinstance(rows, dict):
            return False
        source_fields = view_model.get("sourceFields")
        disabled_actions = view_model.get("disabledActions")
        model_rows = view_model.get("rows")
        recovery = view_model.get("recoveryGuidance")
        if not isinstance(source_fields, dict) or not isinstance(disabled_actions, dict):
            return False
        if not isinstance(model_rows, dict) or not isinstance(recovery, dict):
            return False
        expected_values = {
            "aiPersona": "None; ORIN persona not implemented",
            "providerRuntime": "Blocked; no model path active",
            "privacy": "Protected; no provider or third-party tracking",
            "readinessCheck": "Waiting for USER action",
            "readinessReport": "Local decision aid behind diagnostics",
            "prompt": "Not accepted, sent, stored, or indexed",
            "capabilityPacks": "Install blocked; downloads disabled",
            "maintenanceUpdates": "Future-gated; no install execution",
        }
        flattened_values = {
            "aiPersona": (model_rows.get("controlCenter") or {}).get("aiPersona"),
            "providerRuntime": (model_rows.get("controlCenter") or {}).get("providerRuntime"),
            "privacy": (model_rows.get("controlCenter") or {}).get("privacy"),
            "readinessCheck": (model_rows.get("readinessDiagnostics") or {}).get("readinessCheck"),
            "readinessReport": (model_rows.get("readinessDiagnostics") or {}).get("readinessReport"),
            "prompt": (model_rows.get("readinessDiagnostics") or {}).get("prompt"),
            "capabilityPacks": (model_rows.get("capabilitiesMaintenance") or {}).get("capabilityPacks"),
            "maintenanceUpdates": (model_rows.get("capabilitiesMaintenance") or {}).get("maintenanceUpdates"),
        }
        row_key_to_value = {}
        for grouped_rows in rows.values():
            if not isinstance(grouped_rows, list):
                return False
            for row in grouped_rows:
                if isinstance(row, dict):
                    row_key_to_value[str(row.get("viewModelKey") or "")] = row
        return (
            dashboard_probe.get("viewModelContract") == VIEW_MODEL_CONTRACT
            and dashboard_probe.get("viewModelSource") == "AIProviderStateSnapshot.as_renderer_payload"
            and dashboard_probe.get("viewModelState") == "provider-payload-applied"
            and dashboard_probe.get("viewModelProviderRuntimeBlocked") == "true"
            and dashboard_probe.get("viewModelPromptSendDisabled") == "true"
            and dashboard_probe.get("viewModelProviderVisibleDataNone") == "true"
            and dashboard_probe.get("viewModelRecoveryGuidance") == "Retry local check only"
            and view_model.get("contract") == VIEW_MODEL_CONTRACT
            and view_model.get("source") == "AIProviderStateSnapshot.as_renderer_payload"
            and source_fields.get("providerExecutionGateState") == "provider-execution-disabled"
            and source_fields.get("modelExecutionGateState") == "model-execution-disabled"
            and source_fields.get("providerVisibleData") == "none"
            and source_fields.get("sentToProvider") == "false"
            and source_fields.get("networkEgressState") == "network-egress-blocked"
            and source_fields.get("promptSendPosture") == "prompt-send-disabled"
            and source_fields.get("memoryIndexingState") == "memory-indexing-disabled"
            and disabled_actions == {
                "providerModelExecution": True,
                "promptSend": True,
                "providerVisibleDataEgress": True,
                "capabilityInstallDownload": True,
                "maintenanceUpdateExecution": True,
                "privateSetup": True,
                "ownerMemoryAgents": True,
            }
            and recovery.get("label") == "Retry local check only"
            and flattened_values == expected_values
            and set(row_key_to_value.keys()) == set(expected_values.keys())
            and all(
                row_key_to_value[key].get("value") == value
                and row_key_to_value[key].get("viewModelContract") == VIEW_MODEL_CONTRACT
                and row_key_to_value[key].get("viewModelBound") == "provider-payload"
                for key, value in expected_values.items()
            )
        )

    def _domain_launch_ok(domain_id: str) -> bool:
        launch = (domain_launch_probe.get("launches") or {}).get(domain_id)
        if not isinstance(launch, dict):
            return False
        probe = launch.get("probe") if isinstance(launch.get("probe"), dict) else {}
        click = launch.get("realClick") if isinstance(launch.get("realClick"), dict) else {}
        expected = expected_doorway_buttons.get(domain_id, {})
        return (
            probe.get("ok") is True
            and click.get("ok") is True
            and probe.get("target") == expected.get("target")
            and probe.get("kind") == expected.get("kind")
            and launch.get("windowPresent") is True
            and launch.get("visible") is True
            and domain_id in (launch.get("domainWindowKeysAfterLaunch") or [])
        )

    def _child_probe_ok(domain_id: str, *, title: str, classification: str, lifecycle: str) -> bool:
        probe = child_chrome_probe.get(domain_id)
        if not isinstance(probe, dict):
            return False
        dom = probe.get("dom") if isinstance(probe.get("dom"), dict) else {}
        return (
            probe.get("ok") is True
            and probe.get("visible") is True
            and probe.get("windowTitle") == title
            and probe.get("propertyDomain") == domain_id
            and probe.get("propertyClassification") == classification
            and probe.get("propertyLifecycle") == lifecycle
            and probe.get("propertyShellConformance") == "ndai-webview-rounded-window-shell"
            and probe.get("propertyBoundaryContract") == "single-rounded-shell-mask-hit-rails-coincident-v2"
            and probe.get("propertyBoundaryInset") == "0"
            and probe.get("propertyResizeRailLocation") == "inside-visible-rounded-shell"
            and probe.get("propertyOutsideHitBehavior") == "noninteractive"
            and probe.get("propertyMoveBehavior") == "measured-visible-title-strip-native-and-fallback-v2"
            and probe.get("propertyResizeBehavior") == "windows-native-edge-corner-hit-test-with-webview-fallback"
            and probe.get("propertyDefaultGeometryContract") == "settled-dom-content-measured-screen-bounded-v2"
            and probe.get("propertySupportedGeometryContract") == "minimum-default-intermediate-useful-large-screen-bounded"
            and "x" in str(probe.get("propertyMaximumUsefulSize") or "")
            and probe.get("propertyMaximizeFullscreenPolicy") == "not-offered-compact-detached-window"
            and probe.get("propertyReopenGeometryContract") == "preserve-last-user-geometry-until-destroyed"
            and probe.get("propertyShellVisualContract") == "single-border-no-outer-halo"
            and probe.get("propertyDescriptionDragBehavior") == "client-content-never-caption"
            and probe.get("propertyInitialContentFitApplied") == "true"
            and int(probe.get("propertyMeasuredContentHeight") or 0) > 0
            and int(probe.get("propertyDefaultContentFitHeight") or 0) >= 360
            and int(probe.get("propertyMeasuredDragRegionBottom") or 0) > 0
            and int(probe.get("propertyMeasuredDescriptionTop") or 0)
            >= int(probe.get("propertyMeasuredDragRegionBottom") or 0)
            and probe.get("propertyDefaultOverflowContract") in {"content-fit", "screen-bounded-scroll"}
            and probe.get("propertyProviderVisibleData") == "none"
            and probe.get("propertyProviderModelExecution") == "blocked"
            and probe.get("propertyPromptSend") == "prompt-send-disabled"
            and probe.get("propertyNetworkEgress") == "network-egress-blocked"
            and probe.get("propertyMemoryIndexing") == "memory-indexing-disabled"
            and probe.get("propertyStateTaxonomyContract") == STATE_TAXONOMY_CONTRACT
            and probe.get("propertyStateTaxonomyComplete") == "true"
            and probe.get("propertyDiagnosticState") == "no-provider-fail-closed"
            and REQUIRED_STATE_TAXONOMY_STATES.issubset(_states_from_text(probe.get("propertyStateTaxonomyRenderedStates")))
            and probe.get("propertyViewModelContract") == VIEW_MODEL_CONTRACT
            and probe.get("propertyViewModelApplied") == "true"
            and dom.get("domDomain") == domain_id
            and dom.get("domClassification") == classification
            and dom.get("domLifecycle") == lifecycle
            and dom.get("nativeChrome") == "true"
            and dom.get("genericOsChrome") == "rejected"
            and dom.get("shellConformance") == "ndai-webview-rounded-window-shell"
            and dom.get("boundaryContract") == "single-rounded-shell-mask-hit-rails-coincident-v2"
            and dom.get("boundaryInset") == "0"
            and dom.get("resizeRailLocation") == "inside-visible-rounded-shell"
            and dom.get("outsideHitBehavior") == "noninteractive"
            and dom.get("move") == "measured-visible-title-strip-native-and-fallback-v2"
            and dom.get("descriptionDrag") == "client-content-never-caption"
            and dom.get("resize") == "windows-native-edge-corner-hit-test-with-webview-fallback"
            and dom.get("defaultGeometryContract") == "settled-dom-content-measured-screen-bounded-v2"
            and dom.get("supportedGeometryContract") == "minimum-default-intermediate-useful-large-screen-bounded"
            and dom.get("maximumUsefulSize") == probe.get("propertyMaximumUsefulSize")
            and dom.get("maximizeFullscreenPolicy") == "not-offered-compact-detached-window"
            and dom.get("reopenGeometryContract") == "preserve-last-user-geometry-until-destroyed"
            and dom.get("shellVisualContract") == "single-border-no-outer-halo"
            and dom.get("initialContentFitApplied") == "true"
            and int(dom.get("measuredDragRegionBottom") or 0) > 0
            and int(dom.get("measuredDescriptionTop") or 0) >= int(dom.get("measuredDragRegionBottom") or 0)
            and dom.get("defaultOverflowContract") in {"content-fit", "screen-bounded-scroll"}
            and dom.get("controlCluster") == "compact-minimize-close"
            and dom.get("stateTaxonomyContract") == STATE_TAXONOMY_CONTRACT
            and dom.get("stateTaxonomySource") == "AIProviderStateSnapshot.aiControlCenterStateTaxonomy"
            and dom.get("stateTaxonomyScope") == domain_id
            and dom.get("stateTaxonomyComplete") == "true"
            and dom.get("viewModelContract") == VIEW_MODEL_CONTRACT
            and dom.get("viewModelSource") == "AIProviderStateSnapshot.as_renderer_payload"
            and dom.get("viewModelState") == "provider-payload-applied"
            and dom.get("viewModelProviderRuntimeBlocked") == "true"
            and dom.get("viewModelPromptSendDisabled") == "true"
            and dom.get("viewModelProviderVisibleDataNone") == "true"
            and (dom.get("domainViewModel") or {}).get("contract") == VIEW_MODEL_CONTRACT
            and REQUIRED_STATE_TAXONOMY_STATES.issubset(_states_from_text(dom.get("stateTaxonomyRequiredStates")))
            and REQUIRED_STATE_TAXONOMY_STATES.issubset(_states_from_text(dom.get("stateTaxonomyRenderedStates")))
            and dom.get("providerVisibleDataState") == "none"
            and dom.get("noProviderState") == "no-provider-fail-closed"
            and dom.get("promptExecutionState") == "prompt-send-disabled"
            and dom.get("providerModelRuntimeState") == "blocked-no-model-path"
            and dom.get("trustBoundaryState") == "local-only-no-egress-no-memory-no-cache"
            and dom.get("controlCount") == 2
            and dom.get("workspaceCount") == 1
            and domain_id in (dom.get("workspaces") or [])
        )

    def _child_geometry_supporting_diagnostic_ok(domain_id: str) -> bool:
        behavior = child_geometry_behavior.get(domain_id)
        if not isinstance(behavior, dict):
            return False
        move = behavior.get("move") if isinstance(behavior.get("move"), dict) else {}
        resize = behavior.get("resize") if isinstance(behavior.get("resize"), dict) else {}
        return move.get("moved") is True and resize.get("resized") is True

    def _child_boundary_content_fit_ok(domain_id: str) -> bool:
        probe = child_chrome_probe.get(domain_id)
        if not isinstance(probe, dict):
            return False
        dom = probe.get("dom") if isinstance(probe.get("dom"), dict) else {}
        groups = dom.get("materialGroups") if isinstance(dom.get("materialGroups"), dict) else {}
        shell = groups.get("shell") if isinstance(groups.get("shell"), dict) else {}
        chrome = groups.get("chrome") if isinstance(groups.get("chrome"), dict) else {}
        actions = groups.get("actions") if isinstance(groups.get("actions"), dict) else {}
        drag_region = groups.get("dragRegion") if isinstance(groups.get("dragRegion"), dict) else {}
        description = groups.get("description") if isinstance(groups.get("description"), dict) else {}
        shell_rect = shell.get("rect") if isinstance(shell.get("rect"), dict) else {}
        chrome_rect = chrome.get("rect") if isinstance(chrome.get("rect"), dict) else {}
        actions_rect = actions.get("rect") if isinstance(actions.get("rect"), dict) else {}
        drag_rect = drag_region.get("rect") if isinstance(drag_region.get("rect"), dict) else {}
        description_rect = description.get("rect") if isinstance(description.get("rect"), dict) else {}
        chrome_style = chrome.get("style") if isinstance(chrome.get("style"), dict) else {}
        window_rect = probe.get("rect") if isinstance(probe.get("rect"), dict) else {}
        return (
            shell_rect == chrome_rect
            and int(chrome_rect.get("left", -1)) == 0
            and int(chrome_rect.get("top", -1)) == 0
            and int(chrome_rect.get("width") or 0) == int(window_rect.get("width") or -1)
            and int(chrome_rect.get("height") or 0) == int(window_rect.get("height") or -1)
            and int(actions_rect.get("bottom") or 99999) <= int(chrome_rect.get("bottom") or -1)
            and int(drag_rect.get("bottom") or 0) <= int(description_rect.get("top") or -1)
            and str(chrome_style.get("boxShadow") or "") == "none"
            and "radial-gradient" not in str(chrome_style.get("backgroundImage") or "")
            and "linear-gradient" in str(chrome_style.get("backgroundImage") or "")
            and int(probe.get("propertyDefaultContentFitHeight") or 0) == int(window_rect.get("height") or -1)
        )

    def _readiness_actions_ok(result: object) -> bool:
        if not isinstance(result, dict) or result.get("ok") is not True:
            return False
        local = result.get("afterLocalCheck") if isinstance(result.get("afterLocalCheck"), dict) else {}
        generated = result.get("afterGenerate") if isinstance(result.get("afterGenerate"), dict) else {}
        copied = result.get("afterCopy") if isinstance(result.get("afterCopy"), dict) else {}
        before = result.get("before") if isinstance(result.get("before"), dict) else {}
        before_dom = before.get("dom") if isinstance(before.get("dom"), dict) else {}
        local_dom = local.get("dom") if isinstance(local.get("dom"), dict) else {}
        generated_dom = generated.get("dom") if isinstance(generated.get("dom"), dict) else {}
        copied_dom = copied.get("dom") if isinstance(copied.get("dom"), dict) else {}
        def _flow_boundary_ok(dom: dict[str, object]) -> bool:
            return (
                dom.get("noProviderDiagnosticsFlow") == "local-only-no-provider-readiness-v1"
                and dom.get("noProviderFlowProviderVisibleData") == "none"
                and dom.get("noProviderFlowSentToProvider") == "false"
                and dom.get("noProviderFlowCanAcceptPrompts") == "false"
                and dom.get("noProviderFlowPromptSend") == "prompt-send-disabled"
                and dom.get("noProviderFlowNetworkEgress") == "network-egress-blocked"
                and dom.get("noProviderFlowMemoryIndexing") == "memory-indexing-disabled"
            )
        return (
            (result.get("localClick") or {}).get("ok") is True
            and (result.get("generateClick") or {}).get("ok") is True
            and (result.get("copyClick") or {}).get("ok") is True
            and _flow_boundary_ok(before_dom)
            and before_dom.get("noProviderFlowState") == "waiting-for-user-action"
            and before_dom.get("noProviderFlowReportState") == "not-generated"
            and before_dom.get("noProviderFlowCopyState") == "not-ready"
            and _flow_boundary_ok(local_dom)
            and local_dom.get("noProviderFlowState") == "local-check-complete-no-provider"
            and local_dom.get("noProviderFlowReportState") == "not-generated"
            and local_dom.get("localResult") == "No provider configured"
            and "no prompt" in str(local_dom.get("localDetail") or "").lower()
            and _flow_boundary_ok(generated_dom)
            and generated_dom.get("noProviderFlowState") == "report-generated-local-only"
            and generated_dom.get("noProviderFlowReportState") == "generated-locally"
            and generated_dom.get("noProviderFlowCopyState") == "ready-user-initiated-only"
            and generated_dom.get("reportState") == "Generated locally"
            and generated_dom.get("reportBodyHidden") is False
            and generated_dom.get("copyDisabled") is False
            and "No provider/model execution" in str(generated_dom.get("reportBoundary") or "")
            and _flow_boundary_ok(copied_dom)
            and copied_dom.get("noProviderFlowState") in {
                "report-copied-locally",
                "copy-unavailable-report-visible",
            }
            and copied_dom.get("noProviderFlowCopyState") in {
                "copied-locally",
                "copy-unavailable-report-visible",
            }
            and copied_dom.get("copyDisabled") is False
            and copied_dom.get("reportState") in {
                "Copied locally",
                "Copying locally",
                "Copy unavailable; report remains visible",
            }
        )

    def _visual_proof_screenshots_exist(result: object, required_states: tuple[str, ...]) -> bool:
        if not isinstance(result, dict):
            return False
        screenshots_by_state = result.get("visualProofScreenshots")
        if not isinstance(screenshots_by_state, dict):
            return False
        for state_name in required_states:
            screenshots_for_state = screenshots_by_state.get(state_name)
            if not isinstance(screenshots_for_state, dict):
                return False
            for key in ("focusedWindow", "fullDesktop"):
                image_path = Path(str(screenshots_for_state.get(key) or ""))
                if not image_path.is_file():
                    return False
        return True

    def _control_center_actions_ok(result: object) -> bool:
        if not isinstance(result, dict) or result.get("ok") is not True:
            return False
        if not _visual_proof_screenshots_exist(
            result,
            ("beforeBoundary", "afterBoundaryReview", "afterRecoveryRoute", "afterStateTaxonomy"),
        ):
            return False
        expected_active = {
            "boundary": "show-control-boundary",
            "recovery": "show-control-recovery",
            "taxonomy": "show-control-taxonomy",
        }
        states = {
            "boundary": result.get("afterBoundary"),
            "recovery": result.get("afterRecovery"),
            "taxonomy": result.get("afterTaxonomy"),
        }
        for mode, probe in states.items():
            if not isinstance(probe, dict):
                return False
            dom = probe.get("dom") if isinstance(probe.get("dom"), dict) else {}
            buttons = dom.get("actionButtons") if isinstance(dom.get("actionButtons"), list) else []
            active_buttons = [
                button for button in buttons
                if isinstance(button, dict) and button.get("ariaPressed") == "true"
            ]
            if not (
                dom.get("controlCenterOperationalContract") == "ai-control-center-local-boundary-control-v1"
                and dom.get("controlCenterMode") == mode
                and dom.get("controlCenterGuardClosed") == "true"
                and dom.get("controlCenterProviderActionExecuted") == "false"
                and dom.get("controlCenterProviderModelExecution") == "blocked"
                and dom.get("controlCenterPromptSendExecution") == "blocked"
                and dom.get("controlCenterNetworkEgress") == "network-egress-blocked"
                and dom.get("controlCenterMemoryIndexing") == "memory-indexing-disabled"
                and dom.get("controlCenterProviderVisibleData") == "none"
                and dom.get("providerVisibleData") == "None"
                and dom.get("providerModel") == "Disabled and blocked"
                and dom.get("promptMemory") == "Not accepted, sent, stored, or indexed"
                and dom.get("controlCenterModeText")
                and dom.get("controlCenterReviewState")
                and dom.get("controlCenterReviewDetail")
                and dom.get("controlCenterRecoveryRoute")
                and dom.get("controlCenterTaxonomy")
                and len(active_buttons) == 1
                and active_buttons[0].get("command") == expected_active[mode]
            ):
                return False
        return True

    def _capabilities_workflow_ok(result: object) -> bool:
        if not isinstance(result, dict) or result.get("ok") is not True:
            return False
        if not _visual_proof_screenshots_exist(
            result,
            ("beforeLifecycle", "afterLifecycleReview", "afterEditionGates", "afterMaintenanceHold"),
        ):
            return False
        expected_active = {
            "lifecycle": "show-capability-lifecycle",
            "lanes": "show-capability-lanes",
            "maintenance": "show-capability-maintenance",
        }
        states = {
            "lifecycle": result.get("afterLifecycle"),
            "lanes": result.get("afterLanes"),
            "maintenance": result.get("afterMaintenance"),
        }
        for mode, probe in states.items():
            if not isinstance(probe, dict):
                return False
            dom = probe.get("dom") if isinstance(probe.get("dom"), dict) else {}
            buttons = dom.get("actionButtons") if isinstance(dom.get("actionButtons"), list) else []
            active_buttons = [
                button for button in buttons
                if isinstance(button, dict) and button.get("ariaPressed") == "true"
            ]
            if not (
                dom.get("capabilitiesBoundaryContract") == "capabilities-maintenance-developer-owner-boundary-v1"
                and dom.get("capabilitiesMaintenanceWorkflowContract") == "capabilities-maintenance-display-workflow-v1"
                and dom.get("capabilitiesMaintenanceMode") == mode
                and dom.get("capabilitiesMaintenanceActionExecuted") == "false"
                and dom.get("capabilitiesMaintenanceDownloadExecution") == "blocked"
                and dom.get("capabilitiesMaintenanceInstallExecution") == "blocked"
                and dom.get("capabilitiesMaintenanceUpdateExecution") == "blocked"
                and dom.get("capabilitiesMaintenanceFetchExecution") == "blocked"
                and dom.get("capabilitiesMaintenancePackagingExecution") == "blocked"
                and dom.get("downloadExecution") == "blocked"
                and dom.get("installExecution") == "blocked"
                and dom.get("updateExecution") == "blocked"
                and dom.get("fetchExecution") == "blocked"
                and dom.get("capabilityExecution") == "blocked"
                and dom.get("packagingExecution") == "blocked"
                and dom.get("capabilityPacks") == "Install blocked; downloads disabled"
                and dom.get("maintenanceUpdates") == "Lifecycle placement only; update execution blocked"
                and dom.get("capabilitiesModeText")
                and dom.get("capabilitiesWorkflowState")
                and dom.get("capabilitiesWorkflowDetail")
                and dom.get("capabilitiesWorkflowNext")
                and len(active_buttons) == 1
                and active_buttons[0].get("command") == expected_active[mode]
            ):
                return False
        return True

    def _readiness_after_action_visual_proof_ok(result: object) -> bool:
        if not isinstance(result, dict) or result.get("ok") is not True:
            return False
        return _visual_proof_screenshots_exist(
            result,
            (
            "beforeRun",
            "afterLocalCheck",
            "afterReportGeneration",
            "afterCopyAction",
            ),
        ) and _readiness_actions_ok(result)

    def _dashboard_readiness_flow_contract_ok() -> bool:
        cards = dashboard_probe.get("stateTaxonomyCards") if isinstance(dashboard_probe.get("stateTaxonomyCards"), dict) else {}
        readiness_card = cards.get("readiness-diagnostics") if isinstance(cards.get("readiness-diagnostics"), dict) else {}
        return (
            readiness_card.get("noProviderDiagnosticsFlow") == "local-only-no-provider-readiness-v1"
            and readiness_card.get("noProviderFlowState") == "waiting-for-user-action"
            and readiness_card.get("retryState") == "retry-local-check-only"
            and readiness_card.get("recoveryState") == "recovery-local-only"
            and readiness_card.get("promptExecutionState") == "prompt-send-disabled"
        )

    def _capabilities_boundary_ok() -> bool:
        cards = dashboard_probe.get("stateTaxonomyCards") if isinstance(dashboard_probe.get("stateTaxonomyCards"), dict) else {}
        capabilities_card = cards.get("capabilities-maintenance") if isinstance(cards.get("capabilities-maintenance"), dict) else {}
        capability_child = child_chrome_probe.get("capabilities-maintenance") if isinstance(child_chrome_probe.get("capabilities-maintenance"), dict) else {}
        capability_dom = capability_child.get("dom") if isinstance(capability_child.get("dom"), dict) else {}
        view_model = dashboard_probe.get("dashboardViewModel") if isinstance(dashboard_probe.get("dashboardViewModel"), dict) else {}
        source_fields = view_model.get("sourceFields") if isinstance(view_model.get("sourceFields"), dict) else {}
        disabled_actions = view_model.get("disabledActions") if isinstance(view_model.get("disabledActions"), dict) else {}

        expected_states = {
            "capabilitiesBoundaryContract": "capabilities-maintenance-developer-owner-boundary-v1",
            "capabilityPackLifecycleState": "capability-pack-lifecycle-planned",
            "capabilityPackDownloadState": "capability-pack-downloads-blocked",
            "installIntentState": "install-intent-blocked",
            "capabilityPackInstallState": "install-blocked",
            "capabilityPackUpdateState": "update-blocked",
            "capabilityPackUninstallState": "uninstall-blocked",
            "developerLaneBoundaryState": "developer-lane-private-setup-blocked",
            "ownerLaneBoundaryState": "owner-lane-private-setup-blocked",
            "privateSetupBoundaryState": "private-setup-blocked",
            "privateSetupAuthorized": "false",
            "privateMaterialVisible": "false",
            "ownerMemoryEnabled": "false",
            "ownerAgentsEnabled": "false",
            "downloadExecution": "blocked",
            "installExecution": "blocked",
            "updateExecution": "blocked",
            "fetchExecution": "blocked",
            "capabilityExecution": "blocked",
            "packagingExecution": "blocked",
            "viewModelPrivateSetupBlocked": "true",
            "viewModelOwnerMemoryAgentsBlocked": "true",
        }
        provider_expected = {
            "capabilityPackLifecycleState": "capability-pack-lifecycle-planned",
            "capabilityPackDownloadState": "capability-pack-downloads-blocked",
            "installIntentState": "install-intent-blocked",
            "capabilityPackInstallState": "install-blocked",
            "capabilityPackUpdateState": "update-blocked",
            "capabilityPackUninstallState": "uninstall-blocked",
            "developerLaneBoundaryState": "developer-lane-private-setup-blocked",
            "ownerLaneBoundaryState": "owner-lane-private-setup-blocked",
            "privateSetupBoundaryState": "private-setup-blocked",
        }
        return (
            all(capabilities_card.get(key) == value for key, value in expected_states.items())
            and all(capability_dom.get(key) == value for key, value in expected_states.items())
            and all(source_fields.get(key) == value for key, value in provider_expected.items())
            and all(provider_payload.get(key) == value for key, value in provider_expected.items())
            and source_fields.get("privateSetupAuthorized") == "false"
            and source_fields.get("privateMaterialVisible") == "false"
            and source_fields.get("ownerMemoryEnabled") == "false"
            and source_fields.get("ownerAgentsEnabled") == "false"
            and provider_payload.get("privateSetupAuthorized") is False
            and provider_payload.get("privateMaterialVisible") is False
            and provider_payload.get("ownerMemoryEnabled") is False
            and provider_payload.get("ownerAgentsEnabled") is False
            and disabled_actions.get("capabilityInstallDownload") is True
            and disabled_actions.get("maintenanceUpdateExecution") is True
            and disabled_actions.get("privateSetup") is True
            and disabled_actions.get("ownerMemoryAgents") is True
            and capability_dom.get("capabilityPacks") == "Install blocked; downloads disabled"
            and capability_dom.get("maintenanceUpdates") == "Lifecycle placement only; update execution blocked"
            and capability_dom.get("developerLaneBoundary") == "Developer lane: gated; private setup not configured"
            and capability_dom.get("ownerLaneBoundary") == "Owner lane: gated; private setup not configured"
            and capability_dom.get("privateSetupBoundary") == "Private setup blocked; no private material visible"
            and "No update, download, install, fetch, provider/model, private setup, packaging, or capability execution is approved."
            in str(capability_dom.get("executionBoundary") or "")
        )

    def _singleton_focus_ok(probe: object) -> bool:
        if not isinstance(probe, dict):
            return False
        return (
            probe.get("sameWindowObject") is True
            and probe.get("visibleAfterSecondLaunch") is True
            and probe.get("beforeKeys") == probe.get("afterKeys")
            and (probe.get("secondLaunch") or {}).get("realClick", {}).get("ok") is True
        )

    checks = {
        "proofClassificationFalseGreenFixture": (
            proof_classification_fixture_probe.get("ok") is True
            and proof_classification_fixture_probe.get("knownBadRejected") is True
        ),
        "exactLauncherReadOnlyPreflightProtocolImplemented": (
            exact_launcher_preflight.get("protocol") == "fam007-exact-launcher-read-only-owner-safe-preflight-v2"
            and exact_launcher_preflight.get("readOnly") is True
            and exact_launcher_preflight.get("processTerminationAttempted") is False
            and exact_launcher_preflight.get("launcherActivationAttempted") is False
            and exact_launcher_preflight.get("fileExplorerUsed") is False
            and exact_launcher_preflight.get("computerUseUsed") is False
            and exact_launcher_preflight.get("operationTransferToUserAllowed") is False
            and exact_launcher_preflight.get("processMutationAllowed") is False
            and exact_launcher_preflight.get("foreignOrUnknownReuseAllowed") is False
            and exact_launcher_preflight.get("ownerGuessingAllowed") is False
            and exact_launcher_preflight.get("fileExplorerFallbackAllowed") is False
            and exact_launcher_preflight.get("directLaunchSubstitutionAllowed") is False
            and exact_launcher_preflight.get("computerUseAllowed") is False
            and exact_launcher_preflight.get("oneRuntimePerUserSessionPreserved") is True
            and exact_launcher_preflight.get("requiredActor") == FAM007_GATING_ACTOR
            and tuple(exact_launcher_preflight.get("allowedInputSources") or ()) == FAM007_GATING_INPUTS
            and exact_launcher_preflight.get("requiredActivationRepetitions") == 3
            and len(exact_launcher_preflight.get("requiredPostActivationEvidence") or []) == 5
            and exact_launcher_preflight.get("classification") in {
                "NO_RELEVANT_RUNTIME_DETECTED_SETUP_PRECONDITION_AVAILABLE",
                "FAM007_RUNTIME_ALREADY_ACTIVE_STOP_BEFORE_RELAUNCH",
                "FOREIGN_RUNTIME_DETECTED_STOP_ROUTE_REQUIRED",
                "UNKNOWN_OWNER_STOP",
                "EXACT_SHORTCUT_MISSING_OR_WRONG_TARGET_STOP",
            }
            and exact_launcher_preflight.get("excludedFutureCandidate")
            == "F7-LV1-006-B shared runtime owner attribution; not implemented here"
            and exact_launcher_preflight.get("unresolvedSharedOwnerRoute")
            == "F7-LV1-006-B / Issue #301 / future FAM-001 shared-runtime owner"
        ),
        "returnedDefectCoverageContractComplete": (
            len(REPAIR_DEFECT_IDS) == 12
            and _interaction_matrix_contract_ok(physical_interaction_matrix)
            and _dual_contrast_matrix_contract_ok(dual_contrast_matrix)
        ),
        "childVisibleNativeBoundaryAndDefaultContentFitImplemented": (
            set(child_chrome_probe) == set(expected_doorway_buttons)
            and all(_child_boundary_content_fit_ok(domain_id) for domain_id in expected_doorway_buttons)
        ),
        "childNativeHitTestSupportingDiagnosticImplemented": (
            set(child_native_hit_test_diagnostic) == set(expected_doorway_buttons)
            and all(
                child_native_hit_test_diagnostic[domain_id].get("status") == "SUPPORTING_DIAGNOSTIC_PASS"
                and child_native_hit_test_diagnostic[domain_id].get("gatingValid") is False
                and child_native_hit_test_diagnostic[domain_id].get("closesDefect") is False
                for domain_id in expected_doorway_buttons
            )
        ),
        "childMinimumGeometryScrollSupportingDiagnosticImplemented": (
            set(child_minimum_geometry_scroll_diagnostic) == set(expected_doorway_buttons)
            and all(
                child_minimum_geometry_scroll_diagnostic[domain_id].get("status") == "SUPPORTING_DIAGNOSTIC_PASS"
                and child_minimum_geometry_scroll_diagnostic[domain_id].get("actionsReachable") is True
                and child_minimum_geometry_scroll_diagnostic[domain_id].get("gatingValid") is False
                and child_minimum_geometry_scroll_diagnostic[domain_id].get("closesDefect") is False
                for domain_id in expected_doorway_buttons
            )
        ),
        "dashboardHubActiveDoorwayLifecycle": (
            dashboard_probe.get("title") == "AI Dashboard"
            and dashboard_probe.get("dashboardIaModel") == "ai-dashboard-parent-global-strip-category-cards-detached-domain-windows-active"
            and dashboard_probe.get("dashboardSurfaceModel") == "hub-only-cards-are-doorways"
            and dashboard_probe.get("childWindowModel") == "detached-domain-window-route-lifecycle-active"
            and dashboard_probe.get("sameWindowFocusedSectionPolicy") == "blocked-as-dashboard-workspace-substitute"
            and dashboard_probe.get("cardNames") == ["control-center", "readiness-diagnostics", "capabilities-maintenance"]
            and dashboard_probe.get("cardTitles") == [
                "AI Control Center",
                "AI Readiness & Diagnostics",
                "Capabilities & Maintenance",
            ]
            and dashboard_probe.get("cardDescriptions") == [
                "Persona and provider boundary doorway.",
                "Local checks and diagnostics doorway.",
                "Packs and updates stay blocked.",
            ]
            and all(part in dashboard_probe.get("stripText", "") for part in ["AI Persona - None", "Status - Not implemented", "Provider - Blocked"])
            and "Data -" not in dashboard_probe.get("stripText", "")
            and len(dashboard_probe.get("launcherActionRows") or []) == 3
            and all(
                row.get("contract") == "separate-from-state-rows"
                and row.get("buttonCount") == 1
                and row.get("followsRows") is True
                and row.get("insideRows") is False
                for row in dashboard_probe.get("launcherActionRows") or []
            )
            and dashboard_probe.get("rowGroups") == expected_option_g_rows
            and dashboard_probe.get("focusedSurfaceCount") == 0
            and dashboard_probe.get("domainSurfaceCount") == 0
        ),
        "aiDashboardStateTaxonomyContractProven": _dashboard_state_taxonomy_ok(),
        "aiDashboardProviderStateViewModelProven": _dashboard_view_model_ok(),
        "doorwayButtonsOpenDomainWindowsNoInlineActions": (
            actual_doorway_labels == [
                "Open Control Center",
                "Open Readiness & Diagnostics",
                "Open Capabilities & Maintenance",
            ]
            and len(dashboard_probe.get("launchers") or []) == 0
            and len(doorway_buttons) == 3
            and set(doorway_buttons_by_id.keys()) == set(expected_doorway_buttons.keys())
            and all(button.get("disabled") is False for button in doorway_buttons)
            and all(button.get("ariaDisabled") == "false" for button in doorway_buttons)
            and all(button.get("actionState") == "ready" for button in doorway_buttons)
            and all(
                doorway_buttons_by_id[doorway].get("launchTarget") == contract["target"]
                and doorway_buttons_by_id[doorway].get("launchKind") == contract["kind"]
                and doorway_buttons_by_id[doorway].get("command") == contract["command"]
                and doorway_buttons_by_id[doorway].get("lifecycle") == contract["lifecycle"]
                for doorway, contract in expected_doorway_buttons.items()
            )
            and domain_launch_probe.get("domainWindowCount") == 0
            and domain_launch_probe.get("domainWindowCountAfterLaunch") == 3
            and set(domain_launch_probe.get("domainWindowKeysAfterLaunch") or []) == set(expected_doorway_buttons.keys())
        ),
        "activeDomainWindowLaunchChromeStructure": (
            all(_domain_launch_ok(domain_id) for domain_id in expected_doorway_buttons)
            and _child_probe_ok(
                "control-center",
                title="AI Control Center",
                classification="exclusive-child",
                lifecycle="closes-with-dashboard",
            )
            and _child_probe_ok(
                "readiness-diagnostics",
                title="AI Readiness & Diagnostics",
                classification="external-unique",
                lifecycle="stays-open-if-dashboard-closes",
            )
            and _child_probe_ok(
                "capabilities-maintenance",
                title="Capabilities & Maintenance",
                classification="exclusive-child",
                lifecycle="closes-with-dashboard",
            )
            and _singleton_focus_ok(singleton_focus)
        ),
        "readinessDiagnosticsLocalActionsStayInsideChild": (
            _readiness_actions_ok(readiness_result)
            and provider_state.as_renderer_payload().get("sentToProvider") is False
            and provider_state.as_renderer_payload().get("canAcceptPrompts") is False
            and provider_state.as_renderer_payload().get("providerVisibleData") == "none"
        ),
        "readinessAfterActionVisualProofProven": _readiness_after_action_visual_proof_ok(readiness_result),
        "readinessDiagnosticsNoProviderLocalOnlyFlowProven": (
            _dashboard_readiness_flow_contract_ok()
            and _readiness_actions_ok(readiness_result)
            and provider_state.as_renderer_payload().get("sentToProvider") is False
            and provider_state.as_renderer_payload().get("canAcceptPrompts") is False
            and provider_state.as_renderer_payload().get("providerVisibleData") == "none"
            and provider_state.as_renderer_payload().get("networkEgressState") == "network-egress-blocked"
            and provider_state.as_renderer_payload().get("memoryIndexingState") == "memory-indexing-disabled"
        ),
        "controlCenterLocalBoundaryControlProven": _control_center_actions_ok(control_center_result),
        "capabilitiesMaintenanceDeveloperOwnerBoundaryDisplayProven": _capabilities_boundary_ok(),
        "capabilitiesMaintenanceDisplayWorkflowProven": _capabilities_workflow_ok(capabilities_result),
        "parentVisualMetrics": (
            dashboard_probe.get("defaultWindowWidth") == "471"
            and dashboard_probe.get("defaultWindowHeight") == "598"
            and str(layout_metrics.get("chromePaddingLeft")) == str(layout_metrics.get("chromePaddingRight"))
            and int(layout_metrics.get("topGutter") or 0) >= 8
            and len(row_heights) == 8
            and min(row_heights or [0]) >= 18
            and max(row_heights or [999]) <= 28
            and all(30 <= int(button.get("height") or 0) <= 32 for button in doorway_buttons)
            and all(
                int(button.get("labelWidth") or 0) > 0
                and int(button.get("horizontalPadding") or 0) == 28
                and 0 <= (
                    int(button.get("width") or 0)
                    - int(button.get("labelWidth") or 0)
                    - int(button.get("horizontalPadding") or 0)
                ) <= 4
                and button.get("labelOverflow") == "visible"
                and button.get("labelTextOverflow") == "clip"
                for button in doorway_buttons
            )
            and all(str(button.get("fontWeight") or "").isdigit() and int(button.get("fontWeight")) >= 700 for button in doorway_buttons)
            and int(layout_metrics.get("headerWidth") or 0) >= int(layout_metrics.get("surfaceWidth") or 0) - 32
        ),
        "deterministicStatusRowsAndTitlePill": (
            dashboard_probe.get("rowGroups") == expected_option_g_rows
            and max(row_label_lengths or [999]) <= 10
            and "Downloads/updates" not in str(dashboard_probe.get("rowGroups"))
            and "Visible data" not in str(dashboard_probe.get("rowGroups"))
            and "Capability packs" not in str(dashboard_probe.get("rowGroups"))
            and "AI - ORIN" not in dashboard_probe.get("stripText", "")
            and "Data - None" not in dashboard_probe.get("stripText", "")
            and "AI Persona - None" in dashboard_probe.get("stripText", "")
            and "Protected; no provider or third-party tracking" in str(dashboard_probe.get("rowGroups"))
        ),
        "titleStatusPillGroupWrapProven": (
            dashboard_probe.get("titleStatusWrapMetadata") == "group-preserving-atomic-flex-wrap"
            and title_status_pill_wrap.get("pairCount") == 3
            and title_status_pill_wrap.get("expectedTextsPresent") is True
            and title_status_pill_wrap.get("groupsAtomic") is True
            and int(title_status_pill_wrap.get("clippedPairCount", 999)) == 0
            and int(title_status_pill_wrap.get("lineCount", 0)) >= 1
            and no_early_title_status_pill_wrap.get("pairCount") == 3
            and no_early_title_status_pill_wrap.get("expectedTextsPresent") is True
            and no_early_title_status_pill_wrap.get("groupsAtomic") is True
            and int(no_early_title_status_pill_wrap.get("clippedPairCount", 999)) == 0
            and int(no_early_title_status_pill_wrap.get("lineCount", 0)) == 1
            and horizontal_title_status_pill_wrap.get("pairCount") == 3
            and horizontal_title_status_pill_wrap.get("expectedTextsPresent") is True
            and horizontal_title_status_pill_wrap.get("groupsAtomic") is True
            and int(horizontal_title_status_pill_wrap.get("clippedPairCount", 999)) == 0
            and int(horizontal_title_status_pill_wrap.get("lineCount", 0)) >= 2
        ),
        "titleStatusPillNoEarlyWrapAt580Proven": (
            no_early_wrap_proof.get("proofPath") == "ai-control-center-right-edge-windows-cursor-drag"
            and no_early_wrap_proof.get("inputMethod") == "windows-cursor-left-button-drag"
            and no_early_wrap_proof.get("codeForcedGeometry") is False
            and no_early_wrap_proof.get("runtimeResizeEventStarted") is True
            and 560 <= int((no_early_wrap_proof.get("after") or {}).get("width") or 0) <= 590
            and no_early_title_status_pill_wrap.get("copyMaxWidth") == "100%"
            and no_early_title_status_pill_wrap.get("pairCount") == 3
            and no_early_title_status_pill_wrap.get("expectedTextsPresent") is True
            and no_early_title_status_pill_wrap.get("groupsAtomic") is True
            and int(no_early_title_status_pill_wrap.get("clippedPairCount", 999)) == 0
            and int(no_early_title_status_pill_wrap.get("lineCount", 0)) == 1
        ),
        "titleStatusPillWindowsCursorWrapProven": (
            horizontal_resize_proof.get("proofPath") == "ai-control-center-right-edge-windows-cursor-drag"
            and horizontal_resize_proof.get("inputMethod") == "windows-cursor-left-button-drag"
            and horizontal_resize_proof.get("codeForcedGeometry") is False
            and horizontal_resize_proof.get("runtimeResizeEventStarted") is True
            and horizontal_title_status_pill_wrap.get("pairCount") == 3
            and horizontal_title_status_pill_wrap.get("expectedTextsPresent") is True
            and horizontal_title_status_pill_wrap.get("groupsAtomic") is True
            and int(horizontal_title_status_pill_wrap.get("clippedPairCount", 999)) == 0
            and int(horizontal_title_status_pill_wrap.get("lineCount", 0)) >= 2
            and horizontal_wrap_crop.get("ok") is True
            and Path(str(horizontal_wrap_crop.get("path") or "")).name.startswith(
                "16_title_status_pill_wrapped_windows_cursor_resize"
            )
        ),
        "titleDescriptionProseWordWrapProven": (
            dashboard_probe.get("titleDescriptionWrapMetadata") == "measured-title-card-prose-word-wrap"
            and _title_description_wrap_ok(title_description_wrap, min_lines=1, max_lines=2)
            and _title_description_wrap_ok(no_early_title_description_wrap, min_lines=1, max_lines=2)
            and _title_description_wrap_ok(horizontal_title_description_wrap, min_lines=2)
        ),
        "titleDescriptionWindowsCursorProseWrapProven": (
            horizontal_resize_proof.get("proofPath") == "ai-control-center-right-edge-windows-cursor-drag"
            and horizontal_resize_proof.get("inputMethod") == "windows-cursor-left-button-drag"
            and horizontal_resize_proof.get("codeForcedGeometry") is False
            and horizontal_resize_proof.get("runtimeResizeEventStarted") is True
            and _title_description_wrap_ok(no_early_title_description_wrap, min_lines=1, max_lines=2)
            and _title_description_wrap_ok(horizontal_title_description_wrap, min_lines=3)
            and int(horizontal_title_description_wrap.get("lineCount") or 0) > int(no_early_title_description_wrap.get("lineCount") or 0)
            and horizontal_title_description_wrap.get("lastPhraseWrapsByWord") is True
            and horizontal_title_description_wrap_crop.get("ok") is True
            and Path(str(horizontal_title_description_wrap_crop.get("path") or "")).name.startswith(
                "16_title_status_pill_wrapped_windows_cursor_resize"
            )
        ),
        "deterministicTitleColumnSizingProven": (
            dashboard_probe.get("rowTitleSizingMetadata") == "shared-max-label-content-fixed-gutter"
            and row_title_sizing_probe.get("rowCount") == 8
            and row_title_sizing_probe.get("labelColumnSource") == "measured-max-visible-label-content-px"
            and int(row_title_sizing_probe.get("rowGutterPx") or 0) == 8
            and row_title_sizing_probe.get("contentSized") is True
            and row_title_sizing_probe.get("valueColumnDerivedFromLabelContent") is True
            and row_title_sizing_probe.get("valueColumnDerivedFromMaxLabelContent") is True
            and row_title_sizing_probe.get("declaredLabelColumnMatchesMeasuredMax") is True
            and row_title_sizing_probe.get("fixedColumnGutterRestored") is True
            and row_title_sizing_probe.get("uniformValueColumnOffset") is True
            and row_title_sizing_probe.get("uniformValueLeftEdge") is True
            and row_title_sizing_probe.get("noLabelClipping") is True
            and row_title_sizing_probe.get("noValueClipping") is True
            and row_title_sizing_probe.get("labelValueFontSizeParity") is True
            and int(row_title_sizing_probe.get("maxTitleColumnExcessPx", 999)) <= 2
            and int(row_title_sizing_probe.get("maxLabelColumnExcessPx", 999)) <= 2
            and horizontal_row_title_sizing_probe.get("rowCount") == 8
            and horizontal_row_title_sizing_probe.get("labelColumnSource") == "measured-max-visible-label-content-px"
            and int(horizontal_row_title_sizing_probe.get("rowGutterPx") or 0) == 8
            and horizontal_row_title_sizing_probe.get("contentSized") is True
            and horizontal_row_title_sizing_probe.get("valueColumnDerivedFromLabelContent") is True
            and horizontal_row_title_sizing_probe.get("valueColumnDerivedFromMaxLabelContent") is True
            and horizontal_row_title_sizing_probe.get("declaredLabelColumnMatchesMeasuredMax") is True
            and horizontal_row_title_sizing_probe.get("fixedColumnGutterRestored") is True
            and horizontal_row_title_sizing_probe.get("uniformValueColumnOffset") is True
            and horizontal_row_title_sizing_probe.get("uniformValueLeftEdge") is True
            and horizontal_row_title_sizing_probe.get("noLabelClipping") is True
            and horizontal_row_title_sizing_probe.get("noValueClipping") is True
            and horizontal_row_title_sizing_probe.get("labelValueFontSizeParity") is True
            and int(horizontal_row_title_sizing_probe.get("maxTitleColumnExcessPx", 999)) <= 2
            and int(horizontal_row_title_sizing_probe.get("maxLabelColumnExcessPx", 999)) <= 2
            and title_columns_stable_across_resize is True
        ),
        "fixedColumnGutterAndUniformValueColumnProven": (
            row_title_sizing_probe.get("rowCount") == 8
            and row_title_sizing_probe.get("fixedColumnGutterRestored") is True
            and row_title_sizing_probe.get("uniformValueColumnOffset") is True
            and horizontal_row_title_sizing_probe.get("rowCount") == 8
            and horizontal_row_title_sizing_probe.get("fixedColumnGutterRestored") is True
            and horizontal_row_title_sizing_probe.get("uniformValueColumnOffset") is True
            and int(row_title_sizing_probe.get("rowGutterPx") or 0) == 8
            and int(horizontal_row_title_sizing_probe.get("rowGutterPx") or 0) == 8
        ),
        "sharedStatusValueColumnProven": (
            _shared_status_value_column_ok(row_title_sizing_probe)
            and _shared_status_value_column_ok(horizontal_row_title_sizing_probe)
        ),
        "rowStackVerticalGutterProven": (
            _row_stack_vertical_gutter_ok(row_title_sizing_probe)
            and _row_stack_vertical_gutter_ok(horizontal_row_title_sizing_probe)
        ),
        "windowControlEdgeGutterProven": (
            14 <= int(layout_metrics.get("windowControlOuterTopOffset") or 0) <= 17
            and 14 <= int(layout_metrics.get("windowControlOuterRightOffset") or 0) <= 17
        ),
        "titleCardBackingLayerRemoved": (
            dashboard_probe.get("titleBackingLayer") == "single-title-card-no-secondary-backing"
            and layout_metrics.get("titleBackingLayerRemoved") is True
            and layout_metrics.get("titleBackingDisplay") == "none"
        ),
        "rowTitleStatusTextSizeParityProven": (
            row_title_sizing_probe.get("rowCount") == 8
            and row_title_sizing_probe.get("labelValueFontSizeParity") is True
            and horizontal_row_title_sizing_probe.get("rowCount") == 8
            and horizontal_row_title_sizing_probe.get("labelValueFontSizeParity") is True
        ),
        "belowTitleTextWeights720Proven": (
            dashboard_probe.get("settingsRouteMetadata") == "option-b-deferred-until-fam003-global-settings-window"
            and dashboard_probe.get("focusedSurfaceCount") == 0
            and dashboard_probe.get("domainSurfaceCount") == 0
            and below_title_text_weight_probe.get("targetWeight") == "720"
            and int(below_title_text_weight_probe.get("nodeCount") or 0) >= 20
            and below_title_text_weight_probe.get("all720") is True
            and not below_title_text_weight_probe.get("non720")
        ),
        "returnedDensityAndButtonPlacementRepaired": (
            len(card_heights) == 3
            and max(card_heights or [999]) <= 205
            and min(card_heights or [0]) >= 118
            and all(4 <= gap <= 8 for gap in action_gaps)
            and all(9 <= gutter <= 22 for gutter in button_right_gutters)
            and all(indent in ("0px", "0") for indent in description_indents)
        ),
        "returnedTitleSubtitleWrapRepaired": (
            str(layout_metrics.get("headerPaddingRight") or "").startswith("108")
            and int(layout_metrics.get("subtitleHeight") or 0) <= 42
            and layout_metrics.get("subtitleOverlapsWindowControls") is False
            and _title_description_wrap_ok(title_description_wrap, min_lines=1, max_lines=2)
        ),
        "acceptedReferenceComparisonProven": (
            dashboard_probe.get("surfaceRole") == "ai-dashboard-top-most-hub"
            and dashboard_probe.get("aiControlCenterPlacement") == "focused-domain-card-inside-ai-dashboard"
            and required_reference_images_ok
            and visual_boards_ok
            and proof_crops_ok
        ),
        "exhaustiveMainRuntimeVisualGrammarComparisonProven": (
            visual_grammar_audit.get("status") == "PASS"
            and int(visual_grammar_audit.get("blockingFindingCount") or 0) == 0
        ),
        "resizeEdgeHitZoneProven": (
            resize_edge_hit_zone_probe.get("ok") is True
            and int(resize_edge_hit_zone_probe.get("resizeMarginPx") or 0) >= 16
        ),
        "defaultScrollIntentProven": (
            dashboard_probe.get("defaultWindowHeight") == "598"
            and (
                (
                    int((dashboard_probe.get("defaultScrollMetrics") or {}).get("maxScroll") or 0) == 0
                    and (dashboard_probe.get("defaultScrollMetrics") or {}).get("thirdCardFullyVisibleAtDefault") is True
                    and str(layout_metrics.get("scrollbarVisible")) in {"false", ""}
                )
                or (
                    str(layout_metrics.get("scrollbarVisible")) == "true"
                    and int((dashboard_probe.get("defaultScrollMetrics") or {}).get("maxScroll") or 0) > 20
                    and (dashboard_probe.get("defaultScrollMetrics") or {}).get("thirdCardFullyVisibleAtDefault") is False
                    and scrolled_probe.get("thirdCardFullyVisibleAfterScroll") is True
                    and int(scrolled_probe.get("scrollTop") or 0) >= int(scrolled_probe.get("maxScroll") or 0) - 2
                )
            )
        ),
        "runtimeCopyIsProductFacing": (
            "provider/model execution is blocked" in str(dashboard_probe.get("subtitle") or "")
            and "no prompt, file, memory, telemetry, or provider data leaves this machine" in str(dashboard_probe.get("subtitle") or "")
            and dashboard_probe.get("designProcessCopyPresent") is False
            and dashboard_probe.get("detachedWindowOpenCopyPresent") is False
        ),
        "noInlineWorkspaceActions": (
            dashboard_probe.get("localCheckInline") is False
            and dashboard_probe.get("generateInline") is False
            and dashboard_probe.get("copyInline") is False
        ),
        "capabilitiesCardCompactDoorway": (
            dashboard_probe.get("capabilityHubRows") == 2
        ),
        "redundantCardsRemoved": (
            dashboard_probe.get("activeAiText") is False
            and dashboard_probe.get("trustProviderText") is False
        ),
        "settingsCogRemovedAndDeferred": (
            dashboard_probe.get("visibleSettingsFutureText") is False
            and dashboard_probe.get("nativeTitleTooltipCount") == 0
            and dashboard_probe.get("settingsRouteMetadata") == "option-b-deferred-until-fam003-global-settings-window"
            and dashboard_probe.get("settingsRoutePresent") is False
            and dashboard_probe.get("settingsRouteVisible") is False
            and dashboard_probe.get("settingsButtonPresent") is False
            and dashboard_probe.get("settingsButtonVisible") is False
            and dashboard_probe.get("settingsTooltipText") == ""
            and settings_tooltip_probe.get("present") is False
            and settings_tooltip_probe.get("visible") is False
            and settings_tooltip_probe.get("titleCount") == 0
        ),
        "settingsOptionBSelectionDispositionProven": (
            settings_option_b_disposition.get("ok") is True
            and settings_option_b_disposition.get("selectedOption") == "B"
            and settings_option_b_disposition.get("currentRuntimeSettingsAffordance") == "removed-from-current-workstream-exit-path"
            and settings_option_b_disposition.get("activeGlobalSettingsBehavior") is False
            and settings_option_b_disposition.get("settingsWindowOpened") is False
            and settings_option_b_disposition.get("implementedRuntimeOption") == "B"
        ),
        "fullDesktopProofNotDuplicated": (
            set(opened_desktop_hashes.keys()) == set(expected_doorway_buttons.keys())
            and len(opened_desktop_hashes) == 3
            and duplicate_full_desktop_proof is False
        ),
        "childPurposeMatchedContactSheetsProven": (
            set(child_comparison_boards.keys()) == set(expected_doorway_buttons.keys())
            and all(board.get("ok") is True for board in child_comparison_boards.values())
        ),
        "dashboardResizeStillWorks": (
            dashboard_resize_proof["widthDelta"] >= 30
            and dashboard_resize_proof["heightDelta"] >= 20
        ),
        "dashboardHorizontalResizeMinimumWorks": (
            horizontal_resize_proof.get("ok") is True
            and horizontal_resize_proof.get("proofPath") == "ai-control-center-right-edge-windows-cursor-drag"
            and horizontal_resize_proof.get("inputMethod") == "windows-cursor-left-button-drag"
            and horizontal_resize_proof.get("codeForcedGeometry") is False
            and horizontal_resize_proof.get("runtimeResizeEventStarted") is True
            and int(horizontal_resize_proof.get("minimumWidth") or 999) <= 430
            and int(horizontal_resize_proof.get("widthDelta") or 0) <= 0
            and int(((horizontal_resize_proof.get("noEarlyWrapProof") or {}).get("widthDelta") or 0)) >= 80
            and int(((horizontal_resize_proof.get("naturalWrapProof") or {}).get("widthDelta") or 0)) <= -100
            and int((horizontal_resize_proof.get("after") or {}).get("width") or 999) <= 470
            and "HUD Dashboard" in str(horizontal_resize_proof.get("hudResizePathSubset") or "")
        ),
        "childLifecycleBehavior": (
            lifecycle_after_dashboard_close["controlVisible"] is False
            and lifecycle_after_dashboard_close["maintenanceVisible"] is False
            and lifecycle_after_dashboard_close["readinessVisible"] is True
            and child_windows_visible_before_close == {
                "control-center": True,
                "readiness-diagnostics": True,
                "capabilities-maintenance": True,
            }
        ),
        "providerExecutionStillBlocked": (
            all("PROVIDER" not in event or "provider_visible_data=none" in event.lower() or "provider/model" not in event.lower() for event in events)
            and provider_state.as_renderer_payload().get("sentToProvider") is False
            and provider_state.as_renderer_payload().get("canAcceptPrompts") is False
            and provider_state.as_renderer_payload().get("networkEgressState") == "network-egress-blocked"
            and provider_state.as_renderer_payload().get("memoryIndexingState") == "memory-indexing-disabled"
        ),
    }

    implementation_checks_status = "PASS" if all(checks.values()) else "FAIL"
    status = (
        "SUPPORTING_DIAGNOSTIC_PASS"
        if implementation_checks_status == "PASS"
        else "SUPPORTING_DIAGNOSTIC_FAIL"
    )
    synthetic_child_geometry_diagnostic = {
        "status": "SUPPORTING_DIAGNOSTIC_PASS"
        if all(_child_geometry_supporting_diagnostic_ok(domain_id) for domain_id in expected_doorway_buttons)
        else "SUPPORTING_DIAGNOSTIC_FAIL",
        "gatingValid": False,
        "maySetGatingPass": False,
        "closesDefect": False,
        "results": child_geometry_behavior,
    }
    user_evidence_root = _copy_user_evidence(log_root, stamp)
    manifest = {
        "status": status,
        "implementationChecksStatus": implementation_checks_status,
        "stamp": stamp,
        "helper": "dev/orin_ai_control_center_live_resize_validation.py",
        "proofClass": "supporting-only FAM-007 implementation diagnostic; not Live Validation proof",
        "gatingDecision": "NOT_EVALUATED_REQUIRES_SEPARATELY_APPROVED_CODEX_OWNED_GOVERNED_VISIBLE_INPUT_FOCUSED_CLOSURE_VERIFICATION",
        "liveValidationStatus": "LV_BLOCKED_REPAIR_FIRST_NOT_GREEN",
        "utsStatus": "BLOCKED_NOT_CREATED",
        "defectImplementationStatus": "REPAIR_IMPLEMENTED_PENDING_FOCUSED_CLOSURE_PROOF",
        "defectsRemainOpen": list(REPAIR_DEFECT_IDS),
        "syntheticEvidencePolicy": {
            "contract": "fam007-codex-owned-governed-visible-input-computer-use-prohibited-proof-classification-v4",
            "allHelperGeneratedInteraction": "SUPPORTING_ONLY",
            "qtest": "SUPPORTING_ONLY",
            "directGeometry": "SUPPORTING_ONLY",
            "domJavascript": "SUPPORTING_ONLY",
            "setCursorPosMouseEvent": "SUPPORTING_ONLY",
            "computerUse": "PROHIBITED_NOT_INVOKED",
            "governedHumanClientMouseKeyboard": "GATING_CANDIDATE_DURING_SEPARATELY_APPROVED_CLOSURE_GATE",
            "physicalUserMouseKeyboard": "HISTORICAL_ONLY_NOT_CURRENT_FAM007_GATING",
            "unknownActor": "STOP_NOT_GATING_VALID",
        },
        "proofClassificationFixture": proof_classification_fixture_probe,
        "exactLauncherReadOnlyPreflight": exact_launcher_preflight,
        "focusedGovernedVisibleInputMatrix": physical_interaction_matrix,
        "focusedHumanClientInteractionMatrix": physical_interaction_matrix,
        "dualContrastPerimeterMatrix": dual_contrast_matrix,
        "workspacePreservationContract": {
            "status": "PENDING_FOCUSED_CLOSURE_VERIFICATION",
            "beforeAfterInventoryRequired": True,
            "unrelatedWindowsMustRemainUntouched": True,
            "showDesktopForbidden": True,
            "minimizeAllForbidden": True,
            "fileExplorerLauncherFallbackForbidden": True,
            "desktopFolderLauncherFallbackForbidden": True,
            "nexusFolderLauncherFallbackForbidden": True,
            "onlyNamedInScopeMinimizeRestoreMayChangeWindowState": True,
        },
        "worktree": str(REPO_ROOT),
        "window": "AI Dashboard",
        "dashboardProbe": dashboard_probe,
        "proofCrops": proof_crops,
        "acceptedReferenceImages": {
            "mainRuntimeOldAiControlCenter": main_runtime_ai_control_center_reference,
            "beforeParentDashboard": previous_parent_dashboard_reference,
        },
        "visualComparisonBoards": visual_comparison_boards,
        "visualGrammarAudit": visual_grammar_audit,
        "resizeEdgeHitZoneProbe": resize_edge_hit_zone_probe,
        "surfaceClassification": {
            "currentSurface": "parent AI Dashboard top-most hub",
            "currentSurfaceRole": dashboard_probe.get("surfaceRole"),
            "aiControlCenterPlacement": dashboard_probe.get("aiControlCenterPlacement"),
            "detachedChildWindowDisposition": "active-domain-window-route-lifecycle",
            "acceptedComparatorUse": "Main worktree old AI Control Center runtime is comparator proof only, not global UIREF promotion",
            "acceptedComparatorSource": main_runtime_ai_control_center_reference.get("referenceSource"),
            "acceptedComparatorDesktopLauncher": main_runtime_ai_control_center_reference.get("desktopLauncher"),
        },
        "domainLaunchProbe": domain_launch_probe,
        "settingsTooltipProbe": settings_tooltip_probe,
        "settingsOptionBDisposition": settings_option_b_disposition,
        "defaultScrollIntentProbe": scrolled_probe,
        "childChromeProbe": child_chrome_probe,
        "childNativeHitTestDiagnostic": child_native_hit_test_diagnostic,
        "childMinimumGeometryScrollDiagnostic": child_minimum_geometry_scroll_diagnostic,
        "childControlBehavior": child_control_behavior,
        "childPurposeMatchedContactSheets": child_comparison_boards,
        "controlCenterResult": control_center_result,
        "capabilitiesResult": capabilities_result,
        "fullDesktopHashes": opened_desktop_hashes,
        "duplicateFullDesktopProof": duplicate_full_desktop_proof,
        "childWindowClassificationLedger": {
            "control-center": {
                "sourceCategoryCard": "AI Control Center",
                "launcherLabel": "Open Control Center",
                "classification": "exclusive-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": True,
                "moveBehavior": "measured-visible-title-strip-native-and-fallback-v2",
                "resizeBehavior": "windows-native-edge-corner-hit-test-with-webview-fallback",
                "boundaryContract": "single-rounded-shell-mask-hit-rails-coincident-v2",
                "shellConformance": "ndai-webview-rounded-window-shell",
                "focusBehavior": "bring-to-front-existing-singleton",
            },
            "readiness-diagnostics": {
                "sourceCategoryCard": "AI Readiness & Diagnostics",
                "launcherLabel": "Open Readiness & Diagnostics",
                "classification": "external-unique",
                "remainsOpenIfDashboardCloses": True,
                "singleton": True,
                "moveBehavior": "measured-visible-title-strip-native-and-fallback-v2",
                "resizeBehavior": "windows-native-edge-corner-hit-test-with-webview-fallback",
                "boundaryContract": "single-rounded-shell-mask-hit-rails-coincident-v2",
                "shellConformance": "ndai-webview-rounded-window-shell",
                "focusBehavior": "bring-to-front-existing-singleton",
            },
            "capabilities-maintenance": {
                "sourceCategoryCard": "Capabilities & Maintenance",
                "launcherLabel": "Open Capabilities & Maintenance",
                "classification": "exclusive-child",
                "remainsOpenIfDashboardCloses": False,
                "singleton": True,
                "moveBehavior": "measured-visible-title-strip-native-and-fallback-v2",
                "resizeBehavior": "windows-native-edge-corner-hit-test-with-webview-fallback",
                "boundaryContract": "single-rounded-shell-mask-hit-rails-coincident-v2",
                "shellConformance": "ndai-webview-rounded-window-shell",
                "focusBehavior": "bring-to-front-existing-singleton",
            },
        },
        "readinessResult": readiness_result,
        "singletonFocus": singleton_focus,
        "dashboardResizeProof": dashboard_resize_proof,
        "dashboardHorizontalResizeProof": horizontal_resize_proof,
        "lifecycleAfterDashboardClose": lifecycle_after_dashboard_close,
        "childWindowsVisibleBeforeDashboardClose": child_windows_visible_before_close,
        "childGeometryBehavior": child_geometry_behavior,
        "syntheticChildGeometryDiagnostic": synthetic_child_geometry_diagnostic,
        "providerBoundary": {
            "sentToProvider": provider_payload.get("sentToProvider"),
            "canAcceptPrompts": provider_payload.get("canAcceptPrompts"),
            "providerVisibleData": provider_payload.get("providerVisibleData"),
            "networkEgressState": provider_payload.get("networkEgressState"),
            "memoryIndexingState": provider_payload.get("memoryIndexingState"),
            "stateTaxonomyContract": STATE_TAXONOMY_CONTRACT,
            "requiredStateTaxonomyStates": sorted(REQUIRED_STATE_TAXONOMY_STATES),
            "providerTaxonomyStates": sorted(provider_taxonomy_states),
            "dashboardTaxonomyComplete": dashboard_probe.get("stateTaxonomyComplete"),
            "dashboardTaxonomyRenderedStates": dashboard_probe.get("stateTaxonomyRenderedStates"),
            "viewModelContract": VIEW_MODEL_CONTRACT,
            "dashboardViewModelState": dashboard_probe.get("viewModelState"),
            "dashboardViewModelRecoveryGuidance": dashboard_probe.get("viewModelRecoveryGuidance"),
            "capabilitiesBoundaryContract": "capabilities-maintenance-developer-owner-boundary-v1",
            "capabilityPackLifecycleState": provider_payload.get("capabilityPackLifecycleState"),
            "capabilityPackDownloadState": provider_payload.get("capabilityPackDownloadState"),
            "installIntentState": provider_payload.get("installIntentState"),
            "capabilityPackInstallState": provider_payload.get("capabilityPackInstallState"),
            "capabilityPackUpdateState": provider_payload.get("capabilityPackUpdateState"),
            "capabilityPackUninstallState": provider_payload.get("capabilityPackUninstallState"),
            "developerLaneBoundaryState": provider_payload.get("developerLaneBoundaryState"),
            "ownerLaneBoundaryState": provider_payload.get("ownerLaneBoundaryState"),
            "privateSetupBoundaryState": provider_payload.get("privateSetupBoundaryState"),
            "privateSetupAuthorized": provider_payload.get("privateSetupAuthorized"),
            "privateMaterialVisible": provider_payload.get("privateMaterialVisible"),
            "ownerMemoryEnabled": provider_payload.get("ownerMemoryEnabled"),
            "ownerAgentsEnabled": provider_payload.get("ownerAgentsEnabled"),
        },
        "events": events,
        "checks": checks,
        "screenshots": screenshots,
        "userInspectableEvidenceRoot": str(user_evidence_root),
        "localLogRoot": str(log_root),
    }
    manifest_path = log_root / "live_resize_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (user_evidence_root / "live_resize_manifest.json").write_bytes(manifest_path.read_bytes())
    for audit_key in ("jsonPath", "markdownPath"):
        audit_source = Path(str(visual_grammar_audit.get(audit_key, "")))
        if audit_source.exists():
            (user_evidence_root / audit_source.name).write_bytes(audit_source.read_bytes())
    settings_disposition_json = Path(str(settings_option_b_disposition.get("jsonPath", "")))
    if settings_disposition_json.exists():
        (user_evidence_root / settings_disposition_json.name).write_bytes(settings_disposition_json.read_bytes())

    if implementation_checks_status != "PASS":
        print(f"SUPPORTING_DIAGNOSTIC_FAIL: FAM-007 implementation diagnostics failed. Manifest: {manifest_path}")
        return 1
    print(f"SUPPORTING_DIAGNOSTIC_PASS: FAM-007 implementation diagnostics passed. Manifest: {manifest_path}")
    print("GATING_DECISION: NOT_EVALUATED; Codex-owned governed-visible-input focused closure verification remains pending and unapproved.")
    print(f"USER_EVIDENCE_ROOT: {user_evidence_root}")
    return 0


if __name__ == "__main__":
    if "--launcher-preflight-only" in sys.argv:
        preflight = _read_only_exact_launcher_preflight()
        print(json.dumps(preflight, indent=2, sort_keys=True))
        raise SystemExit(0 if preflight.get("stopRequired") is False else 2)
    raise SystemExit(main())
