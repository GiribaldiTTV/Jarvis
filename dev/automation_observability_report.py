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
    "waiting state",
    "not yet active",
    "no action",
    "remains green",
    "need v1.6.13-prebeta publish",
    "release readiness is not legal yet",
    "pr merge verification pending` remains active",
    "still waiting on merge verification",
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
