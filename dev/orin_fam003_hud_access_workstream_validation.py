"""Fail-capable validation for the FAM-003 HUD resident access Workstream."""

from __future__ import annotations

import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.monitoring_hud_access import (
    HUD_ACCESS_BLOCKED,
    HUD_ACCESS_FAILED,
    HUD_ACCESS_PARTIAL,
    HUD_ACCESS_SUCCESS,
    HUD_ACCESS_SUPERSEDED,
    MonitoringHudAccessAdapter,
)
from desktop.monitoring_hud_state import load_monitoring_hud_state, save_monitoring_hud_state


MATRIX_PATH = ROOT / "dev" / "fixtures" / "fam003_hud_access_state_matrix.json"

STATE_PROOF_FIELDS = (
    "entryCondition",
    "expectedAdapterBehavior",
    "persistenceResult",
    "globalSettingsState",
    "trayState",
    "dashboardState",
    "userFacingState",
    "retryOrRollbackResult",
)

# Each tuple is ordered by STATE_PROOF_FIELDS, followed by applicable rendered
# HUD Settings artifact IDs. Runtime observations remain in actualAdapterResult.
STATE_PROOF_PROFILES = {
    1: ("Feature disabled and stable.", "Fresh query reports disabled without side effects.", "UNCHANGED_DISABLED", "Recovery control visible; toggle off.", "HUD route hidden.", "Closed.", "Disabled state is truthful.", "Not required.", ["01_disabled_default"]),
    2: ("USER requests enable.", "Emit request before persistence; do not report success early.", "PENDING", "Enable progress shown; controls guarded.", "No premature visible route.", "No premature open.", "Enabling...", "Rollback remains available until confirmation.", ["03_enable_in_progress"]),
    3: ("Enable request with available owner.", "Persist, refresh tray, open Dashboard, then confirm fresh state.", "SUCCEEDED_ENABLED", "Enabled and actionable.", "HUD route visible.", "Open.", "Enabled confirmation.", "Not required.", ["02_enabled_default"]),
    4: ("Enable persists but open fails.", "Return PARTIAL with confirmed enabled truth and targeted retry.", "SUCCEEDED_ENABLED", "Enabled with retry state.", "HUD route visible.", "Closed after failed open.", "Enabled; Dashboard did not open.", "Retry open succeeds when owner recovers.", ["06_partial_retry"]),
    5: ("Enable persistence fails.", "Return FAILED without optimistic enabled drift.", "FAILED_UNCHANGED_DISABLED", "Disabled with failure/retry state.", "HUD route hidden.", "Closed.", "Could not enable.", "Rollback is implicit; retry remains available.", ["07_failure_retry"]),
    6: ("Feature enabled; Dashboard closed.", "Fresh query preserves enabled truth and available open route.", "UNCHANGED_ENABLED", "Enabled; Open HUD Dashboard available.", "HUD route visible.", "Closed.", "Enabled and ready.", "Open is available.", ["02_enabled_default"]),
    7: ("Feature enabled; Dashboard open.", "Open/restore remains idempotent and never toggles closed.", "UNCHANGED_ENABLED", "Enabled.", "HUD route visible.", "Open.", "Dashboard open.", "Not required.", ["02_enabled_default"]),
    8: ("Feature enabled; Dashboard hidden or minimized.", "Open/restore raises and activates the existing Dashboard.", "UNCHANGED_ENABLED", "Enabled.", "HUD route visible.", "Restored open.", "Dashboard restored.", "Not required.", ["02_enabled_default"]),
    9: ("Open requested while already open.", "Remain open; never reinterpret open as close.", "UNCHANGED_ENABLED", "Enabled.", "HUD route visible.", "Remains open.", "Dashboard already open.", "Not required.", ["02_enabled_default"]),
    10: ("Feature enabled; runtime unavailable.", "Return retryable BLOCKED without calling open.", "UNCHANGED_ENABLED", "Unavailable/recovery state visible.", "Route reflects unavailable owner truth.", "Closed.", "HUD Dashboard unavailable.", "Retry remains visible.", ["05_enabled_unavailable"]),
    11: ("Enable succeeds but tray refresh fails.", "Return PARTIAL; never aggregate to success.", "SUCCEEDED_ENABLED", "Enabled with partial result.", "Refresh failed; current menu may be stale.", "Open according to owner result.", "Resident menu refresh failed.", "Targeted retry remains available.", ["06_partial_retry"]),
    12: ("Prior retryable operation failed.", "Retry the recorded operation and confirm fresh owner state.", "SUCCEEDED_ENABLED", "Recovered enabled state.", "HUD route visible.", "Open.", "Retry succeeded.", "Completed.", ["02_enabled_default", "06_partial_retry"]),
    13: ("Prior retryable operation still fails.", "Return FAILED with confirmed truth and retryability preserved.", "UNCHANGED_CONFIRMED", "Failure/retry state remains.", "Matches confirmed owner truth.", "Closed.", "Retry failed.", "Retry remains available.", ["07_failure_retry"]),
    14: ("USER requests disable.", "Emit request before persistence; do not close or hide early.", "PENDING", "Disable progress shown; controls guarded.", "No premature hide.", "No premature close.", "Disabling...", "Rollback remains available until confirmation.", ["04_disable_in_progress"]),
    15: ("Disable request succeeds.", "Persist disabled, close Dashboard, refresh tray, confirm fresh state.", "SUCCEEDED_DISABLED", "Recovery control remains visible; toggle off.", "HUD route hidden.", "Closed.", "Disabled confirmation.", "Not required.", ["01_disabled_default"]),
    16: ("Disable persistence fails.", "Return FAILED and preserve enabled/open state.", "FAILED_ROLLED_BACK_ENABLED", "Enabled with failure/retry state.", "HUD route remains visible.", "Remains open.", "Could not disable.", "Rollback confirmed; retry available.", ["07_failure_retry"]),
    17: ("Disable persists but close fails.", "Return PARTIAL with disabled truth and targeted close retry.", "SUCCEEDED_DISABLED", "Disabled with partial retry state.", "HUD route hidden.", "Still open after failed close.", "Disabled; close needs retry.", "Retry close remains available.", ["06_partial_retry"]),
    18: ("Owner state file missing.", "Load safe disabled default without writing on view.", "SOURCE_MISSING_NO_WRITE", "Disabled recovery state visible.", "HUD route hidden.", "Closed.", "Safe disabled state.", "Not required.", ["01_disabled_default"]),
    19: ("Owner state file malformed or unreadable.", "Load safe disabled degraded state without crashing.", "SOURCE_INVALID_NO_WRITE", "Degraded recovery state visible.", "HUD route hidden.", "Closed.", "State unavailable; safe disabled fallback.", "Repair source or retry after recovery.", ["05_enabled_unavailable"]),
    20: ("Runtime reports state different from request.", "Fresh owner truth wins and mismatch is FAILED.", "REQUEST_REJECTED_BY_CONFIRMED_TRUTH", "Shows confirmed owner state.", "Matches confirmed owner state.", "Matches confirmed owner state.", "Requested state was not confirmed.", "Retry remains available when appropriate.", ["07_failure_retry"]),
    21: ("Startup with feature enabled.", "Query enabled state without forcing Dashboard open.", "LOADED_ENABLED", "Enabled and actionable.", "HUD route visible.", "Closed until USER opens it.", "Enabled at startup.", "Open is available.", ["02_enabled_default"]),
    22: ("Startup with feature disabled.", "Query disabled state without side effects.", "LOADED_DISABLED", "Recovery control visible; toggle off.", "HUD route hidden.", "Closed.", "Disabled at startup.", "Not required.", ["01_disabled_default"]),
    23: ("Shutdown begins during operation lifetime.", "Block new requests and prevent late mutation.", "NO_NEW_WRITE", "Controls become non-actionable for shutdown.", "No late refresh mutation.", "No late open.", "Operation blocked during shutdown.", "No retry during shutdown.", ["05_enabled_unavailable"]),
    24: ("Global Settings reopens after state changed.", "Run a fresh query; do not reuse cached banner/state.", "FRESH_OWNER_READ", "Fresh enabled/disabled state rendered.", "Matches fresh owner truth.", "Matches fresh owner truth.", "Current state shown without stale banner.", "Not required.", ["01_disabled_default", "02_enabled_default"]),
    25: ("Repeated rapid enable/disable input.", "Coalesce duplicate request; latest opposite generation wins.", "LATEST_GENERATION_ONLY", "Latest request state shown.", "Matches latest confirmed state.", "Matches latest confirmed state.", "Superseded work is not reported as current success.", "Stale generation superseded; latest result retained.", ["03_enable_in_progress", "04_disable_in_progress"]),
    26: ("Keyboard/focus interaction and owner-thread guard.", "Expose accessible labels/tab order and block off-owner-thread mutation.", "NO_OFF_OWNER_THREAD_WRITE", "Named controls and deterministic focus remain usable.", "No interaction-induced drift.", "No interaction-induced drift.", "Blocked mutation is truthful; focus remains visible.", "Normal USER action remains available on owner thread.", ["10_keyboard_focus", "11_quick_access_regression"]),
}


def _git_value(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()


class FakeOwner:
    def __init__(self):
        self.enabled = False
        self.dashboard_open = False
        self.available = True
        self.runtime_available = True
        self.reason = ""
        self.source = "fixture"
        self.persist_ok = True
        self.open_ok = True
        self.close_ok = True
        self.tray_ok = True
        self.force_mismatch = False
        self.persist_calls = 0
        self.open_calls = 0
        self.close_calls = 0
        self.tray_calls = 0

    def query(self):
        return {
            "feature_enabled": self.enabled,
            "dashboard_visible": self.dashboard_open,
            "dashboard_available": self.available,
            "runtime_available": self.runtime_available,
            "availability_reason": self.reason,
            "resident_route_state": (
                "enabled_available"
                if self.enabled and self.available
                else "enabled_not_ready"
                if self.enabled
                else "disabled_by_user"
            ),
            "source": self.source,
        }

    def persist(self, enabled, _source):
        self.persist_calls += 1
        if not self.persist_ok:
            return False
        if not self.force_mismatch:
            self.enabled = bool(enabled)
        return True

    def open(self, _source):
        self.open_calls += 1
        if not self.open_ok:
            return False
        self.dashboard_open = True
        return True

    def close(self, _source):
        self.close_calls += 1
        if not self.close_ok:
            return False
        self.dashboard_open = False
        return True

    def tray(self, _source):
        self.tray_calls += 1
        return self.tray_ok

    def adapter(self, *, event_logger=None):
        return MonitoringHudAccessAdapter(
            query_state=self.query,
            persist_enabled=self.persist,
            open_or_restore_dashboard=self.open,
            close_dashboard=self.close,
            refresh_tray=self.tray,
            event_logger=event_logger,
        )


def _row(rows, name, passed, detail):
    rows.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})


def _scenario_rows():
    rows = []
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    ids = [entry.get("id") for entry in matrix.get("states", [])]
    _row(rows, "complete 26-state fixture", ids == list(range(1, 27)), f"ids={ids}")

    owner = FakeOwner()
    adapter = owner.adapter()
    state = adapter.query_state()
    _row(rows, "state 1 disabled stable", not state.enabled and not state.dashboard_open, str(state.as_dict()))

    enabled = adapter.set_enabled(True, "fixture_enable")
    _row(
        rows,
        "states 2-3 enable confirmation",
        enabled.status == HUD_ACCESS_SUCCESS
        and enabled.persistence_succeeded is True
        and enabled.tray_refresh_succeeded is True
        and enabled.dashboard_action_succeeded is True
        and owner.enabled
        and owner.dashboard_open,
        str(enabled.as_dict()),
    )

    owner = FakeOwner()
    owner.open_ok = False
    adapter = owner.adapter()
    partial = adapter.set_enabled(True, "fixture_open_fail")
    owner.open_ok = True
    retried = adapter.retry_last_operation("fixture_retry_open")
    _row(
        rows,
        "states 4 and 12 targeted open retry",
        partial.status == HUD_ACCESS_PARTIAL
        and partial.confirmed_enabled
        and partial.dashboard_action_succeeded is False
        and "did not open" in partial.message
        and retried.status == HUD_ACCESS_SUCCESS
        and owner.dashboard_open,
        f"partial={partial.as_dict()}; retry={retried.as_dict()}",
    )

    owner = FakeOwner()
    owner.persist_ok = False
    failed = owner.adapter().set_enabled(True, "fixture_persist_fail")
    _row(
        rows,
        "state 5 persistence failure has no optimistic drift",
        failed.status == HUD_ACCESS_FAILED and failed.persistence_succeeded is False and not owner.enabled,
        str(failed.as_dict()),
    )

    owner = FakeOwner()
    owner.tray_ok = False
    partial = owner.adapter().set_enabled(True, "fixture_tray_fail")
    _row(
        rows,
        "state 11 tray failure is partial",
        partial.status == HUD_ACCESS_PARTIAL
        and partial.persistence_succeeded is True
        and partial.tray_refresh_succeeded is False
        and "Resident menu" in partial.message,
        str(partial.as_dict()),
    )

    owner = FakeOwner()
    owner.enabled = True
    owner.dashboard_open = True
    adapter = owner.adapter()
    opened = adapter.open_or_restore_dashboard("fixture_already_open")
    _row(
        rows,
        "states 7-9 open-or-restore never toggles closed",
        opened.status == HUD_ACCESS_SUCCESS
        and owner.dashboard_open
        and owner.open_calls == 1
        and owner.close_calls == 0,
        str(opened.as_dict()),
    )

    owner = FakeOwner()
    owner.enabled = True
    owner.dashboard_open = True
    adapter = owner.adapter()
    disabled = adapter.set_enabled(False, "fixture_disable")
    _row(
        rows,
        "states 14-15 disable confirmation",
        disabled.status == HUD_ACCESS_SUCCESS
        and disabled.persistence_succeeded is True
        and disabled.dashboard_action_succeeded is True
        and disabled.tray_refresh_succeeded is True
        and not owner.enabled
        and not owner.dashboard_open,
        str(disabled.as_dict()),
    )

    owner = FakeOwner()
    owner.enabled = True
    owner.dashboard_open = True
    owner.persist_ok = False
    failed = owner.adapter().set_enabled(False, "fixture_disable_persist_fail")
    _row(
        rows,
        "state 16 disable persistence rollback",
        failed.status == HUD_ACCESS_FAILED and owner.enabled and owner.dashboard_open,
        str(failed.as_dict()),
    )

    owner = FakeOwner()
    owner.enabled = True
    owner.dashboard_open = True
    owner.close_ok = False
    partial = owner.adapter().set_enabled(False, "fixture_close_fail")
    _row(
        rows,
        "state 17 close failure remains partial",
        partial.status == HUD_ACCESS_PARTIAL
        and not owner.enabled
        and owner.dashboard_open
        and "close needs retry" in partial.message,
        str(partial.as_dict()),
    )

    owner = FakeOwner()
    owner.enabled = True
    owner.available = False
    owner.reason = "HUD Dashboard is still starting."
    blocked = owner.adapter().open_or_restore_dashboard("fixture_unavailable")
    _row(
        rows,
        "state 10 unavailable is blocked truthfully",
        blocked.status == HUD_ACCESS_BLOCKED and blocked.retryable and "starting" in blocked.message,
        str(blocked.as_dict()),
    )

    owner = FakeOwner()
    owner.source = "missing"
    missing = owner.adapter().query_state()
    owner.source = "malformed"
    malformed = owner.adapter().query_state()
    _row(
        rows,
        "states 18-19 source truth remains observable",
        missing.source == "missing" and malformed.source == "malformed" and not missing.enabled,
        f"missing={missing.as_dict()}; malformed={malformed.as_dict()}",
    )

    with tempfile.TemporaryDirectory(prefix="fam003-hud-state-") as temp_root:
        state_path = Path(temp_root) / "monitoring_hud_state.json"
        previous_override = os.environ.get("NEXUS_MONITORING_HUD_STATE_PATH")
        os.environ["NEXUS_MONITORING_HUD_STATE_PATH"] = str(state_path)
        try:
            missing_state = load_monitoring_hud_state()
            state_path.write_text("{not-valid-json", encoding="utf-8")
            invalid_state = load_monitoring_hud_state()
            persisted = save_monitoring_hud_state(
                feature_enabled=True,
                dashboard_visible=True,
                source="fam003_workstream_validation",
            )
            persisted_state = load_monitoring_hud_state()
            temp_file_absent = not state_path.with_name(f"{state_path.name}.tmp").exists()
        finally:
            if previous_override is None:
                os.environ.pop("NEXUS_MONITORING_HUD_STATE_PATH", None)
            else:
                os.environ["NEXUS_MONITORING_HUD_STATE_PATH"] = previous_override
    _row(
        rows,
        "states 18-19 owner store missing malformed and atomic persistence",
        missing_state.get("source") == "missing"
        and invalid_state.get("source") == "invalid"
        and persisted
        and persisted_state.get("source") == "persisted"
        and persisted_state.get("featureEnabled") is True
        and persisted_state.get("dashboardVisible") is True
        and temp_file_absent,
        (
            f"missing={missing_state.get('source')}; invalid={invalid_state.get('source')}; "
            f"persisted={persisted_state.get('source')}; temp_file_absent={temp_file_absent}"
        ),
    )

    owner = FakeOwner()
    owner.force_mismatch = True
    mismatch = owner.adapter().set_enabled(True, "fixture_mismatch")
    _row(
        rows,
        "state 20 fresh owner truth wins",
        mismatch.status == HUD_ACCESS_FAILED and not mismatch.confirmed_enabled,
        str(mismatch.as_dict()),
    )

    owner = FakeOwner()
    adapter = owner.adapter()
    adapter.begin_shutdown("fixture_shutdown")
    blocked = adapter.set_enabled(True, "fixture_late_enable")
    _row(
        rows,
        "state 23 shutdown blocks new operations",
        blocked.status == HUD_ACCESS_BLOCKED and not owner.enabled,
        str(blocked.as_dict()),
    )

    owner = FakeOwner()
    adapter = owner.adapter()
    nested = {}
    original_persist = owner.persist

    def duplicate_persist(enabled, source):
        if "result" not in nested:
            nested["result"] = adapter.set_enabled(enabled, "fixture_duplicate")
        return original_persist(enabled, source)

    adapter._persist_enabled_callback = duplicate_persist
    outer = adapter.set_enabled(True, "fixture_outer")
    _row(
        rows,
        "state 25 identical request coalesces",
        nested["result"].coalesced and outer.status == HUD_ACCESS_SUCCESS and owner.enabled,
        f"nested={nested['result'].as_dict()}; outer={outer.as_dict()}",
    )

    owner = FakeOwner()
    adapter = owner.adapter()
    opposite = {}
    original_persist = owner.persist

    def opposite_persist(enabled, source):
        if enabled and "result" not in opposite:
            opposite["result"] = adapter.set_enabled(False, "fixture_latest_opposite")
            return True
        return original_persist(enabled, source)

    adapter._persist_enabled_callback = opposite_persist
    stale = adapter.set_enabled(True, "fixture_stale_enable")
    _row(
        rows,
        "state 25 latest opposite generation wins",
        stale.status == HUD_ACCESS_SUPERSEDED
        and opposite["result"].status == HUD_ACCESS_SUCCESS
        and not owner.enabled,
        f"stale={stale.as_dict()}; latest={opposite['result'].as_dict()}",
    )

    owner = FakeOwner()
    adapter = owner.adapter()
    threaded = []
    thread = threading.Thread(target=lambda: threaded.append(adapter.set_enabled(True, "fixture_thread")))
    thread.start()
    thread.join()
    _row(
        rows,
        "state 26 owner-thread guard",
        len(threaded) == 1 and threaded[0].status == HUD_ACCESS_BLOCKED and not owner.enabled,
        str(threaded[0].as_dict()),
    )
    return rows


def _exhaustive_matrix_rows():
    rows = []
    state_results = []
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    fixtures = {entry["id"]: entry for entry in matrix.get("states", [])}

    def add(state_id, name, passed, detail):
        _row(rows, f"state {state_id:02d} {name}", passed, detail)
        fixture = fixtures.get(state_id, {})
        profile = STATE_PROOF_PROFILES.get(state_id)
        if profile is None:
            profile = tuple("MISSING" for _ in STATE_PROOF_FIELDS) + ([],)
        state_result = {
            "stateId": state_id,
            "title": name,
            "fixtureName": fixture.get("name"),
            "fixtureExpectation": fixture.get("expected"),
            **dict(zip(STATE_PROOF_FIELDS, profile[: len(STATE_PROOF_FIELDS)])),
            "actualAdapterResult": detail,
            "automatedEvidence": f"state {state_id:02d} assertion in dev/orin_fam003_hud_access_workstream_validation.py",
            "workstreamVisualEvidence": list(profile[-1]),
            "finalVerdict": "PASS" if passed else "FAIL",
            "evidencePaths": [
                "Review Aids/Evidence/HUD Access 26-State Proof/fam003_hud_access_26_state_results.json",
                "Review Aids/Evidence/HUD Access 26-State Proof/fam003_hud_access_26_state_results.md",
                *[
                    f"Review Aids/Evidence/HUD Settings Visual Proof/{artifact_id}.png"
                    for artifact_id in profile[-1]
                ],
            ],
        }
        state_results.append(state_result)

    owner = FakeOwner()
    add(1, "disabled stable", not owner.adapter().query_state().enabled, str(owner.query()))

    owner = FakeOwner()
    events = []
    observed_before_persist = []
    original_persist = owner.persist

    def probed_enable_persist(enabled, source):
        observed_before_persist.append((owner.enabled, owner.dashboard_open, list(events)))
        return original_persist(enabled, source)

    adapter = owner.adapter(event_logger=events.append)
    adapter._persist_enabled_callback = probed_enable_persist
    enable_result = adapter.set_enabled(True, "matrix_enable")
    add(
        2,
        "enable requested",
        bool(observed_before_persist)
        and observed_before_persist[0][0:2] == (False, False)
        and any("REQUESTED" in event and "operation=enable" in event for event in observed_before_persist[0][2]),
        str(observed_before_persist),
    )
    add(3, "enable succeeds", enable_result.status == HUD_ACCESS_SUCCESS and owner.enabled and owner.dashboard_open, str(enable_result.as_dict()))

    owner = FakeOwner()
    owner.open_ok = False
    state4 = owner.adapter().set_enabled(True, "matrix_launch_fail")
    add(4, "enable persisted launch failed", state4.status == HUD_ACCESS_PARTIAL and owner.enabled and not owner.dashboard_open, str(state4.as_dict()))

    owner = FakeOwner()
    owner.persist_ok = False
    state5 = owner.adapter().set_enabled(True, "matrix_persist_fail")
    add(5, "enable persistence failed", state5.status == HUD_ACCESS_FAILED and not owner.enabled and not owner.dashboard_open, str(state5.as_dict()))

    owner = FakeOwner()
    owner.enabled = True
    state6 = owner.adapter().query_state()
    add(6, "enabled dashboard closed", state6.enabled and not state6.dashboard_open and state6.available, str(state6.as_dict()))

    owner.dashboard_open = True
    state7 = owner.adapter().query_state()
    add(7, "enabled dashboard open", state7.enabled and state7.dashboard_open, str(state7.as_dict()))

    owner = FakeOwner()
    owner.enabled = True
    state8 = owner.adapter().open_or_restore_dashboard("matrix_restore")
    add(8, "enabled hidden or minimized restored", state8.status == HUD_ACCESS_SUCCESS and owner.dashboard_open, str(state8.as_dict()))

    owner = FakeOwner()
    owner.enabled = True
    owner.dashboard_open = True
    state9 = owner.adapter().open_or_restore_dashboard("matrix_already_open")
    add(9, "open while already open", state9.status == HUD_ACCESS_SUCCESS and owner.dashboard_open and owner.close_calls == 0, str(state9.as_dict()))

    owner = FakeOwner()
    owner.enabled = True
    owner.available = False
    owner.reason = "HUD Dashboard is unavailable."
    state10 = owner.adapter().open_or_restore_dashboard("matrix_unavailable")
    add(10, "runtime unavailable", state10.status == HUD_ACCESS_BLOCKED and state10.retryable and owner.open_calls == 0, str(state10.as_dict()))

    owner = FakeOwner()
    owner.tray_ok = False
    state11 = owner.adapter().set_enabled(True, "matrix_tray_fail")
    add(11, "tray refresh failed", state11.status == HUD_ACCESS_PARTIAL and state11.tray_refresh_succeeded is False, str(state11.as_dict()))

    owner = FakeOwner()
    owner.open_ok = False
    adapter = owner.adapter()
    adapter.set_enabled(True, "matrix_retry_seed")
    owner.open_ok = True
    state12 = adapter.retry_last_operation("matrix_retry_success")
    add(12, "retry succeeds", state12.status == HUD_ACCESS_SUCCESS and owner.dashboard_open, str(state12.as_dict()))

    owner = FakeOwner()
    owner.open_ok = False
    adapter = owner.adapter()
    adapter.set_enabled(True, "matrix_retry_fail_seed")
    state13 = adapter.retry_last_operation("matrix_retry_fail")
    add(13, "retry fails", state13.status == HUD_ACCESS_FAILED and state13.retryable and not owner.dashboard_open, str(state13.as_dict()))

    owner = FakeOwner()
    owner.enabled = True
    owner.dashboard_open = True
    events = []
    observed_before_disable_persist = []
    original_persist = owner.persist

    def probed_disable_persist(enabled, source):
        observed_before_disable_persist.append((owner.enabled, owner.dashboard_open, list(events)))
        return original_persist(enabled, source)

    adapter = owner.adapter(event_logger=events.append)
    adapter._persist_enabled_callback = probed_disable_persist
    state15 = adapter.set_enabled(False, "matrix_disable")
    add(
        14,
        "disable requested",
        bool(observed_before_disable_persist)
        and observed_before_disable_persist[0][0:2] == (True, True)
        and any("REQUESTED" in event and "operation=disable" in event for event in observed_before_disable_persist[0][2]),
        str(observed_before_disable_persist),
    )
    add(15, "disable succeeds", state15.status == HUD_ACCESS_SUCCESS and not owner.enabled and not owner.dashboard_open, str(state15.as_dict()))

    owner = FakeOwner()
    owner.enabled = True
    owner.dashboard_open = True
    owner.persist_ok = False
    state16 = owner.adapter().set_enabled(False, "matrix_disable_persist_fail")
    add(16, "disable persistence failed", state16.status == HUD_ACCESS_FAILED and owner.enabled and owner.dashboard_open, str(state16.as_dict()))

    owner = FakeOwner()
    owner.enabled = True
    owner.dashboard_open = True
    owner.close_ok = False
    state17 = owner.adapter().set_enabled(False, "matrix_close_fail")
    add(17, "disable persisted close failed", state17.status == HUD_ACCESS_PARTIAL and not owner.enabled and owner.dashboard_open, str(state17.as_dict()))

    with tempfile.TemporaryDirectory(prefix="fam003-hud-matrix-") as temp_root:
        state_path = Path(temp_root) / "monitoring_hud_state.json"
        previous_override = os.environ.get("NEXUS_MONITORING_HUD_STATE_PATH")
        os.environ["NEXUS_MONITORING_HUD_STATE_PATH"] = str(state_path)
        try:
            state18 = load_monitoring_hud_state()
            state_path.write_text("not-json", encoding="utf-8")
            state19 = load_monitoring_hud_state()
        finally:
            if previous_override is None:
                os.environ.pop("NEXUS_MONITORING_HUD_STATE_PATH", None)
            else:
                os.environ["NEXUS_MONITORING_HUD_STATE_PATH"] = previous_override
    add(18, "state file missing", state18.get("source") == "missing" and state18.get("featureEnabled") is False, str(state18.get("source")))
    add(19, "state file malformed", state19.get("source") == "invalid" and state19.get("featureEnabled") is False, str(state19.get("source")))

    owner = FakeOwner()
    owner.force_mismatch = True
    state20 = owner.adapter().set_enabled(True, "matrix_owner_differs")
    add(20, "runtime differs from request", state20.status == HUD_ACCESS_FAILED and not state20.confirmed_enabled, str(state20.as_dict()))

    owner = FakeOwner()
    owner.enabled = True
    state21 = owner.adapter().query_state()
    add(21, "startup enabled", state21.enabled and not state21.dashboard_open and owner.open_calls == 0, str(state21.as_dict()))

    owner = FakeOwner()
    state22 = owner.adapter().query_state()
    add(22, "startup disabled", not state22.enabled and not state22.dashboard_open and owner.open_calls == 0, str(state22.as_dict()))

    owner = FakeOwner()
    adapter = owner.adapter()
    adapter.begin_shutdown("matrix_shutdown")
    state23 = adapter.set_enabled(True, "matrix_late_request")
    add(23, "shutdown in flight", state23.status == HUD_ACCESS_BLOCKED and not state23.retryable and not owner.enabled, str(state23.as_dict()))

    owner = FakeOwner()
    adapter = owner.adapter()
    before_reopen = adapter.query_state()
    owner.enabled = True
    after_reopen = adapter.query_state()
    add(24, "settings reopened fresh query", not before_reopen.enabled and after_reopen.enabled, f"before={before_reopen.as_dict()}; after={after_reopen.as_dict()}")

    owner = FakeOwner()
    adapter = owner.adapter()
    nested = {}
    original_persist = owner.persist

    def rapid_persist(enabled, source):
        if enabled and "latest" not in nested:
            nested["latest"] = adapter.set_enabled(False, "matrix_latest_disable")
            return True
        return original_persist(enabled, source)

    adapter._persist_enabled_callback = rapid_persist
    stale = adapter.set_enabled(True, "matrix_stale_enable")
    add(25, "rapid enable disable", stale.status == HUD_ACCESS_SUPERSEDED and nested["latest"].status == HUD_ACCESS_SUCCESS and not owner.enabled, f"stale={stale.as_dict()}; latest={nested['latest'].as_dict()}")

    owner = FakeOwner()
    adapter = owner.adapter()
    threaded = []
    thread = threading.Thread(target=lambda: threaded.append(adapter.set_enabled(True, "matrix_thread")))
    thread.start()
    thread.join()
    add(26, "accessibility keyboard focus interaction guard", bool(threaded) and threaded[0].status == HUD_ACCESS_BLOCKED and not owner.enabled, f"thread_guard={threaded[0].as_dict()}; rendered focus proof is routed through fam003_hud_settings_visual_validation")

    return rows, state_results


def _static_rows():
    rows = []
    adapter_source = (ROOT / "desktop" / "monitoring_hud_access.py").read_text(encoding="utf-8")
    renderer_source = (ROOT / "desktop" / "desktop_renderer.py").read_text(encoding="utf-8")
    tray_source = (ROOT / "desktop" / "tray_controller.py").read_text(encoding="utf-8")
    main_source = (ROOT / "desktop" / "orin_desktop_main.py").read_text(encoding="utf-8")
    visual_helper_source = (ROOT / "dev" / "orin_fam003_hud_settings_visual_validation.py").read_text(
        encoding="utf-8"
    )
    aggregate_helper_source = (ROOT / "dev" / "orin_fam003_option_c_workstream_proof_validation.py").read_text(
        encoding="utf-8"
    )
    settings_source = renderer_source.split("class ResidentAccessSettingsDialog", 1)[1].split(
        "class DesktopRuntimeWindow", 1
    )[0]

    public_methods = (
        "def query_state(",
        "def set_enabled(",
        "def open_or_restore_dashboard(",
        "def close_dashboard(",
        "def retry_last_operation(",
    )
    _row(
        rows,
        "public adapter contract",
        all(marker in adapter_source for marker in public_methods),
        ", ".join(public_methods),
    )
    _row(
        rows,
        "Settings has no direct HUD JSON or private runtime mutation",
        "monitoring_hud_state.json" not in settings_source
        and "save_monitoring_hud_state" not in settings_source
        and "_set_monitoring_hud_feature_enabled" not in settings_source
        and "monitoring_hud_access" in settings_source,
        "adapter-only HUD Settings consumer",
    )
    _row(
        rows,
        "one authoritative store",
        "monitoring_hud_state.json" not in adapter_source and "json" not in adapter_source,
        "adapter is storage agnostic",
    )
    _row(
        rows,
        "persistent HUD parent and child",
        '"hud": "hud_dashboard"' in settings_source
        and '"hud_dashboard": "hud_dashboard"' in settings_source
        and "residentAccessHudSettingsContainer" in settings_source,
        "HUD and HUD Dashboard remain registered independent of enabled state",
    )
    _row(
        rows,
        "accepted copy contract",
        "opens HUD Dashboard once as confirmation" in settings_source
        and 'QPushButton("Open HUD Dashboard"' in settings_source
        and 'QPushButton("Open Dashboard"' not in settings_source,
        "one-time disclosure and full action label",
    )
    _row(
        rows,
        "HUD Settings page is actionable and accessible",
        'setAccessibleName("Enable HUD Dashboard")' in settings_source
        and 'setAccessibleName("Open HUD Dashboard")' in settings_source
        and 'setAccessibleName("Retry HUD Dashboard operation")' in settings_source
        and "self.setTabOrder(self.hud_enabled_checkbox, self.hud_open_button)" in settings_source
        and "self.setTabOrder(self.hud_open_button, self.hud_retry_button)" in settings_source
        and 'QPushButton("Open HUD Dashboard"' in settings_source,
        "toggle, open, retry, labels, and tab order are present",
    )
    _row(
        rows,
        "tray action is open-or-restore only",
        'next_visible = True' in tray_source
        and 'return "Close HUD Dashboard"' not in tray_source
        and 'getattr(access, "open_or_restore_dashboard"' in tray_source,
        "no visible close-toggle path",
    )
    _row(
        rows,
        "runtime compatibility paths delegate to adapter",
        "self._monitoring_hud_access_adapter.set_enabled" in renderer_source
        and "self.open_or_restore_monitoring_hud_dashboard" in renderer_source
        and "MonitoringHudAccessAdapter" in main_source,
        "single adapter behavior path",
    )
    _row(
        rows,
        "shutdown generation guard",
        "begin_shutdown" in renderer_source and "MONITORING_HUD_ACCESS_SHUTDOWN_GUARD" not in renderer_source,
        "runtime invokes adapter shutdown guard; adapter owns marker",
    )
    _row(
        rows,
        "Workstream evidence cannot self-promote to H1 LV or UTS",
        '"formalLiveValidation": False' in visual_helper_source
        and '"formalUts": False' in visual_helper_source
        and '"hudAccessWorkstream"' in aggregate_helper_source
        and '"hudSettingsVisual"' in aggregate_helper_source
        and '_assert(result["ok"]' in aggregate_helper_source
        and '"aggregatePolicy"' in aggregate_helper_source,
        "current child helpers are required fail-closed and explicitly non-formal",
    )
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = Path(args.output_dir) if args.output_dir else (
        ROOT / "dev" / "logs" / "fam003_hud_access_workstream_validation" / timestamp
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    exhaustive_rows, state_results = _exhaustive_matrix_rows()
    rows = _scenario_rows() + exhaustive_rows + _static_rows()
    head = _git_value("rev-parse", "HEAD")
    fixture_ids = [entry.get("id") for entry in json.loads(MATRIX_PATH.read_text(encoding="utf-8")).get("states", [])]
    contract_complete = fixture_ids == list(range(1, 27)) and set(STATE_PROOF_PROFILES) == set(range(1, 27))
    for state_result in state_results:
        state_result["head"] = head
        state_result["timestamp"] = timestamp
        state_result["proofRoot"] = str(output_dir)
    status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    if not contract_complete or len(state_results) != 26:
        status = "FAIL"
    state_artifact = {
        "schema": "fam003-hud-access-26-state-results-v2",
        "status": status,
        "owner": "FAM-003",
        "sourceHead": head,
        "timestamp": timestamp,
        "proofRoot": str(output_dir),
        "stateCount": len(state_results),
        "requiredStateIds": list(range(1, 27)),
        "states": state_results,
    }
    state_json_path = output_dir / "fam003_hud_access_26_state_results.json"
    state_json_path.write_text(json.dumps(state_artifact, indent=2) + "\n", encoding="utf-8")
    state_markdown = [
        "# FAM-003 HUD Access Complete 26-State Results",
        "",
        f"Status: `{status}`",
        f"Source HEAD: `{head}`",
        f"Timestamp: `{timestamp}`",
        f"Proof Root: `{output_dir}`",
        "",
    ]
    for state in state_results:
        state_markdown.extend(
            [
                f"## {state['stateId']:02d}. {state['title']}",
                "",
                f"- Fixture: `{state['fixtureName']}` / `{state['fixtureExpectation']}`",
                f"- Entry condition: {state['entryCondition']}",
                f"- Expected adapter behavior: {state['expectedAdapterBehavior']}",
                f"- Actual adapter result: `{state['actualAdapterResult']}`",
                f"- Persistence result: `{state['persistenceResult']}`",
                f"- Global Settings state: {state['globalSettingsState']}",
                f"- Tray state: {state['trayState']}",
                f"- Dashboard state: {state['dashboardState']}",
                f"- USER-facing state: {state['userFacingState']}",
                f"- Retry/rollback: {state['retryOrRollbackResult']}",
                f"- Automated evidence: `{state['automatedEvidence']}`",
                f"- Visual Workstream evidence: `{', '.join(state['workstreamVisualEvidence']) or 'Not applicable with reason: adapter-only state'}`",
                f"- Evidence paths: `{'; '.join(state['evidencePaths'])}`",
                f"- Final verdict: `{state['finalVerdict']}`",
                "",
            ]
        )
    state_md_path = output_dir / "fam003_hud_access_26_state_results.md"
    state_md_path.write_text("\n".join(state_markdown), encoding="utf-8")
    manifest = {
        "schemaVersion": 2,
        "helperStatus": "Workstream-scoped",
        "owner": "FAM-003",
        "status": status,
        "sourceHead": head,
        "timestamp": timestamp,
        "proofRoot": str(output_dir),
        "stateMatrix": str(MATRIX_PATH),
        "stateCount": len(state_results),
        "stateResults": state_results,
        "completeStateArtifactJson": str(state_json_path),
        "completeStateArtifactMarkdown": str(state_md_path),
        "rows": rows,
    }
    (output_dir / "fam003_hud_access_workstream_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    markdown = [
        "# FAM-003 HUD Access Workstream Validation",
        "",
        f"Status: `{status}`",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        detail = str(row["detail"]).replace("|", "/").replace("\n", " ")
        markdown.append(f"| {row['name']} | `{row['status']}` | {detail} |")
    (output_dir / "fam003_hud_access_workstream_report.md").write_text(
        "\n".join(markdown) + "\n",
        encoding="utf-8",
    )
    print(f"FAM-003 HUD access Workstream validation: {status}")
    print(f"Evidence: {output_dir}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
