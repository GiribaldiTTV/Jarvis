from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path


CODEX_HOME = Path.home() / ".codex"
AUTOMATION_DB = CODEX_HOME / "sqlite" / "codex-dev.db"
AUTOMATION_DIR = CODEX_HOME / "automations"
REPO_ROOT = Path(__file__).resolve().parents[1]
BLOCKER_WORDS = (
    "block",
    "blocked",
    "blocker",
    "failed",
    "failure",
    "missing",
    "should retire",
    "unavailable",
    "unproven",
)
GREEN_WORDS = (
    "green",
    "no action",
    "no drift",
    "remains green",
    "waiting state",
)
EXPECTED_WAITING_MARKERS = (
    "waiting phase",
    "waiting state",
    "waiting on hardening",
    "waiting on phase transition",
    "waiting for pr or release readiness",
    "not yet active",
    "no action",
    "pr and release readiness are not active yet",
    "pr readiness not active",
    "release readiness not active",
    "no merge or release-publication follow-through",
    "remains green",
    "need v1.6.13-prebeta publish",
    "release readiness is not legal yet",
    "pr merge verification pending` remains active",
    "still waiting on merge verification",
    "merge verification still pending",
    "merge watch still pending",
    "watcher still pending",
    "pr #107 has not merged yet",
    "watch for merged=true",
)


@dataclass(frozen=True)
class Finding:
    severity: str
    automation_id: str
    title: str
    detail: str


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def ms_to_iso(value: int | None) -> str:
    if value is None:
        return ""
    return dt.datetime.fromtimestamp(value / 1000, tz=dt.timezone.utc).isoformat()


def parse_kv_toml(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r'^([A-Za-z0-9_-]+)\s*=\s*"?(.*?)"?$', line.strip())
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def expected_interval_seconds(rrule: str) -> int:
    interval_match = re.search(r"(?:^|;)INTERVAL=(\d+)(?:;|$)", rrule)
    interval = int(interval_match.group(1)) if interval_match else 1
    if "FREQ=MINUTELY" in rrule:
        return interval * 60
    if "FREQ=HOURLY" in rrule:
        return interval * 60 * 60
    if "FREQ=DAILY" in rrule:
        return interval * 24 * 60 * 60
    return 24 * 60 * 60


def freshness_limit_seconds(rrule: str) -> int:
    interval = expected_interval_seconds(rrule)
    # Give the app scheduler one missed window plus a small floor before calling it stale.
    return max(interval * 2, interval + 30 * 60)


def load_active_automations(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return connection.execute(
        """
        SELECT id, name, status, rrule, last_run_at, next_run_at, cwds
        FROM automations
        ORDER BY id
        """
    ).fetchall()


def latest_run(connection: sqlite3.Connection, automation_id: str) -> sqlite3.Row | None:
    return connection.execute(
        """
        SELECT automation_id, status, thread_id, inbox_title, inbox_summary, updated_at, created_at
        FROM automation_runs
        WHERE automation_id = ?
        ORDER BY updated_at DESC
        LIMIT 1
        """,
        (automation_id,),
    ).fetchone()


def latest_inbox_item(connection: sqlite3.Connection, automation_id: str) -> sqlite3.Row | None:
    return connection.execute(
        """
        SELECT id, title, description, thread_id, created_at, read_at
        FROM inbox_items
        WHERE id LIKE ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (f"{automation_id}:%",),
    ).fetchone()


def read_repo_text(relative_path: str) -> str:
    path = REPO_ROOT / relative_path
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def pr99_heartbeat_missing_is_historical() -> bool:
    record = read_repo_text("Docs/branch_records/feature_automation_planning.md")
    required_markers = (
        "historical PR99-specific proof",
        "not a standing active automation",
        "missing live PR99 TOML/script files after retirement are not automation drift by themselves",
    )
    return all(marker in record for marker in required_markers)


def fb049_active_phase_truth_is_aligned() -> bool:
    record = read_repo_text("Docs/branch_records/feature_fb_049_runtime_branch_readiness.md")
    backlog = read_repo_text("Docs/feature_backlog.md")
    roadmap = read_repo_text("Docs/prebeta_roadmap.md")
    workstream_record_markers = (
        "Phase: `Workstream`",
        "Current Workstream Seam: `Workstream WS1 - Pre-Settled Incoming-Launch Conflict Truthful Exit Proof`",
        "Next Active Seam: `Hardening H1 - Pre-Settled Incoming-Launch Conflict Hardening`",
        "Completion Status: `Green`",
    )
    workstream_surface_markers = (
        "Current Workstream State: WS1 complete and green",
        "Current Workstream State: `WS1 complete and green`",
    )
    hardening_record_markers = (
        "Phase: `Hardening`",
        "Current Hardening Seam: `Hardening H1 - Pre-Settled Incoming-Launch Conflict Validation`",
        "Active seam: `Hardening H1 - Pre-Settled Incoming-Launch Conflict Validation`",
        "Next Active Seam: `Live Validation LV1 - Pre-Settled Incoming-Launch Conflict Live Validation`",
    )
    hardening_surface_markers = (
        "Current Hardening State: Active on `Hardening H1 - Pre-Settled Incoming-Launch Conflict Validation`",
        "Current Hardening State: `Active on Hardening H1 - Pre-Settled Incoming-Launch Conflict Validation`",
    )
    live_validation_record_markers = (
        "Phase: `Live Validation`",
        "Current Live Validation Seam: `Live Validation LV1 - Pre-Settled Incoming-Launch Conflict Live Validation`",
        "Active seam: `Live Validation LV1 - Pre-Settled Incoming-Launch Conflict Live Validation`",
        "User-Facing Shortcut Validation: `PASS`",
        "User Test Summary Results: `WAIVED`",
        "Next Active Seam: `PR Readiness PR1 - FB-049 Runtime Branch PR Validation`",
    )
    live_validation_surface_markers = (
        "Current Live Validation State: Green on `Live Validation LV1 - Pre-Settled Incoming-Launch Conflict Live Validation`",
        "Current Live Validation State: `Green on Live Validation LV1 - Pre-Settled Incoming-Launch Conflict Live Validation`",
    )
    pr_readiness_pr1_record_markers = (
        "Phase: `PR Readiness`",
        "Current PR Readiness Seam: `PR Readiness PR1 - FB-049 Runtime Branch PR Validation`",
        "Active seam: `PR Readiness PR1 - FB-049 Runtime Branch PR Validation`",
        "Live PR Number: `107`",
        "Same-Thread Watcher: `pr107-same-thread-merge-watch`",
        "Next active seam: `PR Readiness PR2 - FB-049 Runtime Branch Merge Verification Watch`",
    )
    pr_readiness_pr1_surface_markers = (
        "Current PR Readiness State: Active on `PR Readiness PR1 - FB-049 Runtime Branch PR Validation` for PR #107",
        "Current PR Readiness State: `Active on PR Readiness PR1 - FB-049 Runtime Branch PR Validation for PR #107`",
    )
    pr_readiness_pr2_record_markers = (
        "Phase: `PR Readiness`",
        "Current PR Readiness Seam: `PR Readiness PR2 - FB-049 Runtime Branch Merge Verification Watch`",
        "Active seam: `PR Readiness PR2 - FB-049 Runtime Branch Merge Verification Watch`",
        "Previous seam: `PR Readiness PR1 - FB-049 Runtime Branch PR Validation`",
        "Live PR Number: `107`",
        "Same-Thread Watcher: `pr107-same-thread-merge-watch`",
        "PR2 Merge Watch Posture: `PR Merge Verification Pending`",
    )
    pr_readiness_pr2_surface_markers = (
        "Current PR Readiness State: PR1 is historical green for PR #107 live-surface validation; active on `PR Readiness PR2 - FB-049 Runtime Branch Merge Verification Watch`",
        "Current PR Readiness State: `PR1 is historical green for PR #107 live-surface validation`; active on `PR Readiness PR2 - FB-049 Runtime Branch Merge Verification Watch`",
    )
    stale_markers = (
        "Current Workstream State: Not started",
        "Current Workstream State: `Not started`",
        "active in Branch Readiness on `feature/fb-049-runtime-branch-readiness`",
    )
    workstream_aligned = (
        all(marker in record for marker in workstream_record_markers)
        and workstream_surface_markers[0] in backlog
        and workstream_surface_markers[1] in roadmap
    )
    hardening_aligned = (
        all(marker in record for marker in hardening_record_markers)
        and hardening_surface_markers[0] in backlog
        and hardening_surface_markers[1] in roadmap
    )
    live_validation_aligned = (
        all(marker in record for marker in live_validation_record_markers)
        and live_validation_surface_markers[0] in backlog
        and live_validation_surface_markers[1] in roadmap
    )
    pr_readiness_pr1_aligned = (
        all(marker in record for marker in pr_readiness_pr1_record_markers)
        and pr_readiness_pr1_surface_markers[0] in backlog
        and pr_readiness_pr1_surface_markers[1] in roadmap
    )
    pr_readiness_pr2_aligned = (
        all(marker in record for marker in pr_readiness_pr2_record_markers)
        and pr_readiness_pr2_surface_markers[0] in backlog
        and pr_readiness_pr2_surface_markers[1] in roadmap
    )
    return (
        (
            workstream_aligned
            or hardening_aligned
            or live_validation_aligned
            or pr_readiness_pr1_aligned
            or pr_readiness_pr2_aligned
        )
        and not any(marker in backlog or marker in roadmap for marker in stale_markers)
    )


def pr107_merge_watch_pending_is_expected() -> bool:
    record = read_repo_text("Docs/branch_records/feature_fb_049_runtime_branch_readiness.md")
    backlog = read_repo_text("Docs/feature_backlog.md")
    roadmap = read_repo_text("Docs/prebeta_roadmap.md")
    record_markers = (
        "Current PR Readiness Seam: `PR Readiness PR2 - FB-049 Runtime Branch Merge Verification Watch`",
        "Same-Thread Watcher: `pr107-same-thread-merge-watch`",
        "PR2 Merge Watch Posture: `PR Merge Verification Pending`",
        "Stop Basis: `PR Merge Verification Pending`",
        "Stop Condition: `PR #107 is not watcher-verified as merged.`",
    )
    surface_markers = (
        "Current PR Readiness State: PR1 is historical green for PR #107 live-surface validation; active on `PR Readiness PR2 - FB-049 Runtime Branch Merge Verification Watch`",
        "Current PR Readiness State: `PR1 is historical green for PR #107 live-surface validation`; active on `PR Readiness PR2 - FB-049 Runtime Branch Merge Verification Watch`",
    )
    return (
        all(marker in record for marker in record_markers)
        and surface_markers[0] in backlog
        and surface_markers[1] in roadmap
    )


def pr107_merge_handoff_failure_is_carried() -> bool:
    record = read_repo_text("Docs/branch_records/feature_fb_049_runtime_branch_readiness.md")
    backlog = read_repo_text("Docs/feature_backlog.md")
    roadmap = read_repo_text("Docs/prebeta_roadmap.md")
    workstream = read_repo_text("Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md")
    required_markers = (
        "PR Watcher Merge Handoff Missing",
        "PR #107 merged",
        "watcher handoff failure",
        "feature/fb-030-voice-audio-runtime-branch-readiness",
    )
    return all(
        marker in surface
        for marker, surface in (
            (required_markers[0], record),
            (required_markers[1], record),
            (required_markers[2], backlog),
            (required_markers[2], roadmap),
            (required_markers[3], workstream),
        )
    )


def classify_pending_review(title: str, summary: str) -> str:
    text = f"{title}\n{summary}".casefold()
    if (
        title.casefold().startswith("pr #")
        and "watcher update" in title.casefold()
        and "mergeable_state=clean" in text
        and "merged=false" in text
        and "botcomments=0" in text
    ):
        return "REVIEW_INFO"
    if (
        "live toml for ws1 pr99-heartbeat-watch is absent" in text
        and pr99_heartbeat_missing_is_historical()
    ):
        return "REVIEW_INFO"
    if (
        (
            "phase drift found on fb-049 branch" in text
            or "fb-049 branch still in workstream" in text
            or "fb-049 remains in workstream posture" in text
            or "fb-049 remains in hardening wait state" in text
            or "fb-049 still in hardening" in text
            or "branch remains in workstream" in text
            or "release window sentinel still waiting" in text
            or "phase has not reached pr or release readiness" in text
            or "phase has not reached pr readiness" in text
        )
        and fb049_active_phase_truth_is_aligned()
    ):
        return "REVIEW_INFO"
    if (
        (
            "live pr #107 watcher needs explicit contract" in text
            or "fb-049 admission gate cleared" in text
            or "fb-049 merge watch still pending" in text
            or "pr readiness watcher still pending" in text
            or "pr #107 merge verification still pending" in text
            or "pr #107 has not merged yet" in text
        )
        and pr107_merge_watch_pending_is_expected()
    ):
        return "REVIEW_INFO"
    if (
        (
            "fb-049 pr readiness remains blocked" in text
            or "pr #107 merge verification still pending" in text
            or "fb-049 still waiting on merge verification" in text
        )
        and pr107_merge_handoff_failure_is_carried()
    ):
        return "REVIEW_INFO"
    if any(marker in text for marker in EXPECTED_WAITING_MARKERS):
        return "REVIEW_INFO"
    if any(word in text for word in BLOCKER_WORDS):
        return "BLOCKER_CANDIDATE"
    if any(word in text for word in GREEN_WORDS):
        return "REVIEW_INFO"
    return "REVIEW_REQUIRED"


def automation_toml_map() -> dict[str, Path]:
    result: dict[str, Path] = {}
    if not AUTOMATION_DIR.is_dir():
        return result
    for child in AUTOMATION_DIR.iterdir():
        if not child.is_dir():
            continue
        toml = child / "automation.toml"
        values = parse_kv_toml(toml)
        automation_id = values.get("id") or child.name
        if toml.is_file():
            result[automation_id] = toml
    return result


def memory_tail(automation_id: str, line_count: int = 4) -> list[str]:
    path = AUTOMATION_DIR / automation_id / "memory.md"
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()[-line_count:]


def build_report() -> tuple[dict[str, object], list[Finding]]:
    findings: list[Finding] = []
    now = utc_now()
    if not AUTOMATION_DB.is_file():
        findings.append(
            Finding(
                "BLOCKER",
                "codex-automation-db",
                "Codex automation database missing",
                str(AUTOMATION_DB),
            )
        )
        return {
            "generated_at": now.isoformat(),
            "automation_db": str(AUTOMATION_DB),
            "automation_dir": str(AUTOMATION_DIR),
            "automations": [],
            "finding_counts": {
                severity: sum(1 for finding in findings if finding.severity == severity)
                for severity in ("BLOCKER", "BLOCKER_CANDIDATE", "REVIEW_REQUIRED", "REVIEW_INFO")
            },
        }, findings

    tomls = automation_toml_map()
    rows: list[dict[str, object]] = []
    with sqlite3.connect(AUTOMATION_DB) as connection:
        connection.row_factory = sqlite3.Row
        automations = load_active_automations(connection)
        active_ids = {str(row["id"]) for row in automations}

        for row in automations:
            automation_id = str(row["id"])
            status = str(row["status"] or "")
            rrule = str(row["rrule"] or "")
            run = latest_run(connection, automation_id)
            inbox_item = latest_inbox_item(connection, automation_id)
            run_updated_at = int(run["updated_at"]) if run and run["updated_at"] else None
            last_run_at = int(row["last_run_at"]) if row["last_run_at"] else None
            newest_proof_ms = max(value for value in (run_updated_at, last_run_at) if value) if (run_updated_at or last_run_at) else None
            age_seconds = (
                (now - dt.datetime.fromtimestamp(newest_proof_ms / 1000, tz=dt.timezone.utc)).total_seconds()
                if newest_proof_ms
                else None
            )
            toml_path = tomls.get(automation_id)
            latest_title = str(run["inbox_title"] or "") if run else ""
            latest_summary = str(run["inbox_summary"] or "") if run else ""
            latest_status = str(run["status"] or "") if run else ""
            next_run_at = int(row["next_run_at"]) if row["next_run_at"] else None

            if status == "ACTIVE" and not toml_path:
                findings.append(
                    Finding(
                        "BLOCKER_CANDIDATE",
                        automation_id,
                        "Active automation has no TOML backing record",
                        "Codex DB reports ACTIVE but no automation.toml exists under $CODEX_HOME/automations.",
                    )
                )
            if status == "ACTIVE" and not newest_proof_ms:
                first_run_grace_active = (
                    next_run_at is not None
                    and (
                        dt.datetime.fromtimestamp(next_run_at / 1000, tz=dt.timezone.utc) - now
                    ).total_seconds()
                    > -10 * 60
                )
                if first_run_grace_active:
                    findings.append(
                        Finding(
                            "REVIEW_INFO",
                            automation_id,
                            "Active automation awaiting first run proof",
                            "No scheduler last_run_at or automation_runs row exists yet, but the first scheduled run remains inside the initial grace window.",
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            "BLOCKER_CANDIDATE",
                            automation_id,
                            "Active automation has no run proof",
                            "No scheduler last_run_at and no automation_runs row were found.",
                        )
                    )
            if status == "ACTIVE" and age_seconds is not None and age_seconds > freshness_limit_seconds(rrule):
                findings.append(
                    Finding(
                        "REVIEW_REQUIRED",
                        automation_id,
                        "Automation run proof is stale",
                        f"Newest proof is {int(age_seconds)} seconds old for rrule {rrule!r}.",
                    )
                )
            if latest_status == "PENDING_REVIEW":
                findings.append(
                    Finding(
                        classify_pending_review(latest_title, latest_summary),
                        automation_id,
                        latest_title or "Pending automation review",
                        latest_summary or "Latest automation run is pending review.",
                    )
                )

            rows.append(
                {
                    "id": automation_id,
                    "name": row["name"],
                    "status": status,
                    "rrule": rrule,
                    "toml": str(toml_path) if toml_path else "",
                    "last_run_at": ms_to_iso(last_run_at),
                    "next_run_at": ms_to_iso(row["next_run_at"]),
                    "latest_run_status": latest_status,
                    "latest_inbox_title": latest_title,
                    "latest_summary": latest_summary,
                    "latest_thread_id": str(run["thread_id"] or "") if run else "",
                    "latest_updated_at": ms_to_iso(run_updated_at),
                    "latest_inbox_item_title": str(inbox_item["title"] or "") if inbox_item else "",
                    "latest_inbox_item_description": str(inbox_item["description"] or "") if inbox_item else "",
                    "memory_tail": memory_tail(automation_id),
                }
            )

        for automation_id, toml_path in sorted(tomls.items()):
            if automation_id not in active_ids:
                rows.append(
                    {
                        "id": automation_id,
                        "name": parse_kv_toml(toml_path).get("name", automation_id),
                        "status": "TOML_ONLY",
                        "rrule": parse_kv_toml(toml_path).get("rrule", ""),
                        "toml": str(toml_path),
                        "last_run_at": "",
                        "next_run_at": "",
                        "latest_run_status": "",
                        "latest_inbox_title": "",
                        "latest_summary": "",
                        "latest_thread_id": "",
                        "latest_updated_at": "",
                        "memory_tail": memory_tail(automation_id),
                    }
                )

    report = {
        "generated_at": now.isoformat(),
        "automation_db": str(AUTOMATION_DB),
        "automation_dir": str(AUTOMATION_DIR),
        "automations": rows,
        "finding_counts": {
            severity: sum(1 for finding in findings if finding.severity == severity)
            for severity in ("BLOCKER", "BLOCKER_CANDIDATE", "REVIEW_REQUIRED", "REVIEW_INFO")
        },
    }
    return report, findings


def render_text(report: dict[str, object], findings: list[Finding]) -> str:
    lines = [
        "Automation Observability Source-of-Truth Report",
        f"Generated: {report['generated_at']}",
        f"Automation DB: {report['automation_db']}",
        f"Automation Dir: {report['automation_dir']}",
        "",
        "Findings:",
    ]
    if not findings:
        lines.append("- None")
    for finding in findings:
        lines.append(
            f"- [{finding.severity}] {finding.automation_id}: {finding.title} - {finding.detail}"
        )

    lines.extend(["", "Automation Rows:"])
    for row in report["automations"]:  # type: ignore[index]
        lines.append(
            (
                f"- {row['id']} | status={row['status']} | latest={row['latest_run_status'] or 'none'} "
                f"| title={row['latest_inbox_title'] or 'none'} | updated={row['latest_updated_at'] or 'none'}"
            )
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero when blocker or review-required findings are present",
    )
    args = parser.parse_args()

    report, findings = build_report()
    if args.json:
        payload = {
            **report,
            "findings": [finding.__dict__ for finding in findings],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_text(report, findings))

    if args.strict and any(
        finding.severity in {"BLOCKER", "BLOCKER_CANDIDATE", "REVIEW_REQUIRED"}
        for finding in findings
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
