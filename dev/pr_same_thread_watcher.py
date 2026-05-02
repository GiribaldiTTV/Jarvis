from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import uuid
from shutil import which
from datetime import datetime, timezone
from pathlib import Path
from urllib import error as urllib_error
from urllib import request as urllib_request


BOT_LOGIN = "chatgpt-codex-connector[bot]"
BOT_APPROVAL_TEXT = f"{BOT_LOGIN} reacted with thumbs up emoji"
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    return utc_now().isoformat().replace("+00:00", "Z")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def append_log(path: Path, message: str) -> None:
    ensure_parent(path)
    timestamp = utc_now().strftime("%Y-%m-%d %H:%M:%S")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def _subprocess_run(args: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    if CREATE_NO_WINDOW:
        kwargs.setdefault("creationflags", CREATE_NO_WINDOW)
    return subprocess.run(args, **kwargs)


def load_state(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def save_json(path: Path, payload: dict[str, object]) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def set_text(path: Path, value: str) -> None:
    ensure_parent(path)
    path.write_text(value, encoding="utf-8")


def stop_task(task_name: str) -> None:
    _subprocess_run(
        ["schtasks", "/Delete", "/TN", task_name, "/F"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def run_git(repo_root: Path, *args: str, check: bool = True) -> str:
    process = _subprocess_run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or process.stdout.strip() or "git command failed")
    return process.stdout.strip()


def git_is_ancestor(repo_root: Path, ancestor_sha: str, descendant_sha: str) -> bool:
    if not ancestor_sha or not descendant_sha:
        return False
    process = _subprocess_run(
        ["git", "merge-base", "--is-ancestor", ancestor_sha, descendant_sha],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return process.returncode == 0


def branch_phase(branch_record_path: Path) -> str:
    if not branch_record_path.is_file():
        return ""
    text = branch_record_path.read_text(encoding="utf-8")
    match = re.search(r"^- Phase: `([^`]+)`", text, flags=re.M)
    return match.group(1).strip() if match else ""


def _record_value(text: str, label: str) -> str:
    patterns = (
        rf"^- {re.escape(label)}:\s*`([^`]+)`\s*$",
        rf"^- {re.escape(label)}:\s*(.+?)\s*$",
        rf"^{re.escape(label)}:\s*`([^`]+)`\s*$",
        rf"^{re.escape(label)}:\s*(.+?)\s*$",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.M)
        if match:
            return match.group(1).strip().strip("`")
    return ""


def _record_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        flags=re.M,
    )
    return match.group(1).strip() if match else ""


def branch_record_snapshot(branch_record_path: Path) -> dict[str, str]:
    if not branch_record_path.is_file():
        return {}
    text = branch_record_path.read_text(encoding="utf-8")
    identity = _record_section(text, "Branch Identity")
    active_seam = _record_section(text, "Active Seam")
    next_legal_section = _record_section(text, "Next Legal Phase")
    next_legal_match = re.search(r"`([^`]+)`", next_legal_section)
    next_legal_phase = (
        _record_value(next_legal_section, "Next Legal Phase")
        or (next_legal_match.group(1).strip() if next_legal_match else next_legal_section.strip())
    )
    return {
        "branchRecordPath": str(branch_record_path),
        "branchRecordBranch": _record_value(identity, "Branch"),
        "branchRecordWorkstream": _record_value(identity, "Workstream"),
        "branchRecordClass": _record_value(identity, "Branch Class"),
        "branchRecordPhase": _record_value(_record_section(text, "Current Phase"), "Phase"),
        "branchRecordNextLegalPhase": next_legal_phase,
        "branchRecordActiveSeam": _record_value(active_seam, "Active seam"),
        "branchRecordNextActiveSeam": _record_value(active_seam, "Next active seam"),
        "branchRecordBotReviewStatus": _record_value(_record_section(text, "PR Bot Review Signal"), "Bot Review Signal Status"),
        "branchRecordBotReviewHead": _record_value(_record_section(text, "PR Bot Review Signal"), "Bot Review Signal Head SHA"),
    }


def fetch_pr_page(repo_full_name: str, pr_number: int) -> str:
    url = f"https://github.com/{repo_full_name}/pull/{pr_number}"
    request = urllib_request.Request(url, headers={"User-Agent": "Codex"})
    with urllib_request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def fetch_github_json(url: str) -> object:
    request = urllib_request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Codex PR watcher",
        },
    )
    with urllib_request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8", "replace"))


def _is_bot_user(item: object) -> bool:
    if not isinstance(item, dict):
        return False
    user = item.get("user") or {}
    if not isinstance(user, dict):
        return False
    login = str(user.get("login") or "")
    return login.casefold() == BOT_LOGIN.casefold()


def fetch_rest_bot_signal(
    repo_full_name: str,
    pr_number: int,
    head_sha: str,
) -> tuple[bool, int, str]:
    api_root = f"https://api.github.com/repos/{repo_full_name}"
    bot_approval = False
    bot_comment_count = 0
    errors: list[str] = []

    try:
        reactions = fetch_github_json(f"{api_root}/issues/{pr_number}/reactions")
        if isinstance(reactions, list):
            bot_approval = any(
                _is_bot_user(reaction) and str(reaction.get("content") or "") == "+1"
                for reaction in reactions
                if isinstance(reaction, dict)
            )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"reaction lookup failed: {exc}")

    # Issue comments are not commit-scoped; treat bot issue comments as current PR feedback.
    try:
        issue_comments = fetch_github_json(f"{api_root}/issues/{pr_number}/comments")
        if isinstance(issue_comments, list):
            bot_comment_count += sum(
                1 for comment in issue_comments if _is_bot_user(comment)
            )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"issue-comment lookup failed: {exc}")

    for url in (
        f"{api_root}/pulls/{pr_number}/reviews",
        f"{api_root}/pulls/{pr_number}/comments",
    ):
        try:
            items = fetch_github_json(url)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{url.rsplit('/', 1)[-1]} lookup failed: {exc}")
            continue
        if not isinstance(items, list):
            continue
        for item in items:
            if not _is_bot_user(item):
                continue
            commit_id = str(item.get("commit_id") or "")
            if head_sha and commit_id and commit_id != head_sha:
                continue
            bot_comment_count += 1

    return bot_approval, bot_comment_count, "; ".join(errors)


def fetch_rest_pr_status(
    repo_full_name: str,
    pr_number: int,
) -> tuple[dict[str, object], str]:
    try:
        detail = fetch_github_json(f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}")
    except (OSError, json.JSONDecodeError) as exc:
        return {}, f"PR detail lookup failed: {exc}"
    if not isinstance(detail, dict):
        return {}, "PR detail lookup returned an unexpected payload"

    head = detail.get("head") or {}
    base = detail.get("base") or {}
    return {
        "repo": repo_full_name,
        "prNumber": pr_number,
        "prUrl": str(detail.get("html_url") or f"https://github.com/{repo_full_name}/pull/{pr_number}"),
        "prState": str(detail.get("state") or "UNKNOWN").upper(),
        "merged": bool(detail.get("merged")),
        "draft": bool(detail.get("draft")),
        "headRef": str(head.get("ref") or ""),
        "baseRef": str(base.get("ref") or "main"),
        "headSha": str(head.get("sha") or ""),
        "title": str(detail.get("title") or ""),
        "createdTime": str(detail.get("created_at") or ""),
        "mergedTime": str(detail.get("merged_at") or ""),
        "closedTime": str(detail.get("closed_at") or ""),
    }, ""


def _json_string_field(html: str, key: str) -> str:
    match = re.search(rf'"{re.escape(key)}":"((?:[^"\\]|\\.)*)"', html)
    if not match:
        return ""
    return bytes(match.group(1), "utf-8").decode("unicode_escape")


def parse_pr_page(html: str, repo_full_name: str, pr_number: int) -> dict[str, object]:
    state = _json_string_field(html, "state") or "UNKNOWN"
    head_branch = _json_string_field(html, "headBranch")
    base_branch = _json_string_field(html, "baseBranch") or "main"
    head_sha = _json_string_field(html, "headSha")
    title = _json_string_field(html, "title")
    merged_time = _json_string_field(html, "mergedTime")
    closed_time = _json_string_field(html, "closedTime")
    created_time = _json_string_field(html, "createdTime")
    bot_approval = BOT_APPROVAL_TEXT in html

    bot_comment_patterns = (
        rf"{re.escape(BOT_LOGIN)}.{{0,300}}commented",
        rf"commented.{{0,300}}{re.escape(BOT_LOGIN)}",
        rf"{re.escape(BOT_LOGIN)}.{{0,300}}reviewed",
        rf"reviewed.{{0,300}}{re.escape(BOT_LOGIN)}",
    )
    bot_comment_count = 0
    for pattern in bot_comment_patterns:
        bot_comment_count += len(re.findall(pattern, html, flags=re.I | re.S))

    merged = bool(merged_time)
    closed = state == "CLOSED" or bool(closed_time) or merged
    draft = "draft" in title.casefold() or bool(re.search(r">\s*Draft\s*<", html, flags=re.I))

    return {
        "repo": repo_full_name,
        "prNumber": pr_number,
        "prUrl": f"https://github.com/{repo_full_name}/pull/{pr_number}",
        "prState": "CLOSED" if closed else state,
        "merged": merged,
        "draft": draft,
        "headRef": head_branch,
        "baseRef": base_branch,
        "headSha": head_sha,
        "title": title,
        "createdTime": created_time,
        "mergedTime": merged_time,
        "closedTime": closed_time,
        "botApproval": bot_approval,
        "botCommentCount": bot_comment_count,
    }


def compute_local_merge(repo_root: Path, base_branch: str) -> tuple[bool | None, str]:
    try:
        run_git(repo_root, "fetch", "origin", base_branch, "--prune")
        process = _subprocess_run(
            ["git", "merge-tree", "--write-tree", "--quiet", f"origin/{base_branch}", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - defensive runtime path
        return None, str(exc)
    return process.returncode == 0, ""


def current_thread_message(status: dict[str, object]) -> str:
    pr_number = status["prNumber"]
    merge_status_green = status.get("mergeable") is True
    merge_status_label = "green" if merge_status_green else "not green"
    recorded_bot_status = str(status.get("branchRecordBotReviewStatus") or "").strip()
    recorded_bot_resolved = recorded_bot_status.casefold() in {"approved", "comment addressed"}
    bot_signal_resolved = bool(status.get("botApproval")) or recorded_bot_resolved
    if status.get("botApproval"):
        bot_approval_label = "present"
    elif recorded_bot_status:
        bot_approval_label = recorded_bot_status
    else:
        bot_approval_label = "pending"
    bot_comment_count = int(status.get("botCommentCount") or 0)
    if bot_comment_count:
        bot_comment_label = f"{bot_comment_count} provable bot comment(s)"
    elif recorded_bot_status.casefold() == "comment addressed":
        bot_comment_label = "comment addressed in branch record"
    else:
        bot_comment_label = "no provable bot comments"

    merge_status_blocker = "`PR Merge Status Unproven` is clear." if merge_status_green else "`PR Merge Status Unproven` remains active."
    watcher_blocker = "`PR Watcher Provisioning Unproven` is clear."
    merge_verification_blocker = (
        "`PR Merge Verification Pending` is clear."
        if status.get("merged")
        else "`PR Merge Verification Pending` remains active."
    )
    release_posture = (
        "Merge verification is complete; run Release Readiness source-of-truth validation "
        "before claiming release legality."
        if status.get("merged")
        else "`Release Readiness` is not legal yet."
    )
    remote_head = str(status.get("headSha") or "UNKNOWN")
    local_head = str(status.get("localHeadSha") or "UNKNOWN")
    state_label = str(status.get("prState") or "UNKNOWN").casefold()
    merged_label = "true" if status.get("merged") else "false"
    draft_label = "true" if status.get("draft") else "false"
    pr_url = str(status.get("prUrl") or "")
    merged_at = str(status.get("mergedTime") or "")
    workstream = str(status.get("branchRecordWorkstream") or "Unknown Workstream")
    branch_name = str(status.get("branchRecordBranch") or status.get("localBranch") or "Unknown Branch")
    branch_class = str(status.get("branchRecordClass") or "implementation validation")
    branch_phase_value = str(status.get("branchRecordPhase") or status.get("phase") or "PR Readiness")
    active_seam = str(status.get("branchRecordActiveSeam") or "PR Readiness PR2 - Merge Verification Watch")
    next_legal_phase = str(status.get("branchRecordNextLegalPhase") or "Release Readiness")
    thread_id = str(status.get("threadId") or "UNKNOWN")
    last_run = str(status.get("lastRunLocal") or "UNKNOWN")
    merge_watch_active = "pr2" in active_seam.casefold() or "merge verification" in active_seam.casefold()
    bot_comment_count = int(status.get("botCommentCount") or 0)
    blockers_list: list[str] = []
    if status.get("merged"):
        blockers_list.append("None for PR merge verification")
    else:
        if bot_comment_count > 0 and not recorded_bot_resolved:
            blockers_list.append("PR Validation Pending")
        elif not bot_signal_resolved:
            blockers_list.append("Bot Review Signal Pending")
        if merge_status_label != "green":
            blockers_list.append("PR Merge Status Unproven")
        if merge_watch_active or not blockers_list:
            blockers_list.append("PR Merge Verification Pending")
    blockers = "; ".join(blockers_list)
    completion_status = "Green" if status.get("merged") else "Red"
    if status.get("merged"):
        continue_decision = "Stop watcher and proceed to Release Readiness validation from updated main"
    elif merge_watch_active:
        continue_decision = "Continue; remain in PR Readiness PR2 until merge verification clears"
    elif "PR Merge Verification Pending" in blockers_list and len(blockers_list) == 1:
        continue_decision = "Continue into PR Readiness PR2 merge-watch with Release Readiness still blocked"
    else:
        continue_decision = "Stop; remain in PR Readiness PR1 until live PR blockers clear"
    repair_status = str(status.get("lastRepairAttemptStatus") or "").strip().casefold()
    repair_summary = str(status.get("lastRepairWorkerSummary") or "").strip()
    repair_summary = repair_summary.splitlines()[0].strip() if repair_summary else ""
    repair_clause = ""
    if repair_status == "succeeded":
        repair_clause = (
            f" Auto-repair worker completed for the current PR comment. {repair_summary}"
            if repair_summary
            else " Auto-repair worker completed for the current PR comment."
        )
    elif repair_status == "failed":
        repair_clause = (
            f" Auto-repair worker failed for the current PR comment: {repair_summary}"
            if repair_summary
            else " Auto-repair worker failed for the current PR comment."
        )

    lines = [
        f"PR watcher source-of-truth update for PR #{pr_number}",
        "",
        "Governed State:",
        f"- Workstream: {workstream}",
        f"- Branch: {branch_name}",
        f"- Branch Class: {branch_class}",
        f"- Current Phase: {branch_phase_value}",
        f"- Active Seam: {active_seam}",
        f"- Next Legal Phase: {next_legal_phase}",
        f"- Completion Status: {completion_status}",
        f"- Blockers: {blockers}",
        f"- Continue Decision: {continue_decision}",
        "",
        "Live PR Truth:",
        f"- PR URL: {pr_url or f'PR #{pr_number}'}",
        f"- State: {state_label}",
        f"- Merged: {merged_label}",
        f"- Draft: {draft_label}",
        f"- Merge Status: {merge_status_label}",
        f"- Remote Head: {remote_head}",
        f"- Local Head: {local_head}",
        f"- Bot Approval: {bot_approval_label}",
        f"- Bot Comments: {bot_comment_label}",
    ]
    if merged_at:
        lines.append(f"- Merged At: {merged_at}")

    lines.extend(
        [
            "",
            "Watcher Proof:",
            f"- Reporting Thread: {thread_id}",
            f"- Last Watcher Run: {last_run}",
            f"- {watcher_blocker}",
            f"- {merge_status_blocker}",
            f"- {merge_verification_blocker}",
            f"- {release_posture}",
        ]
    )
    if repair_clause:
        lines.append(f"- {repair_clause.strip()}")

    if status.get("merged"):
        release_seam = f"Release Readiness RR1 - {workstream} Release Validation"
        lines.extend(
            [
                "",
                "Copy/Paste Codex Prompt:",
                "```text",
                "Project Context:",
                "Mode: Release Readiness",
                "Phase: Release Readiness",
                f"Workstream: {workstream}",
                "Branch: main",
                f"Branch Class: {branch_class}",
                "",
                "Load:",
                "Docs/Main.md",
                "",
                "Active Seam:",
                release_seam,
                "",
                "Context:",
                (
                    f"PR #{pr_number} merged into main"
                    + (f" at `{merged_at}`" if merged_at else "")
                    + f". The same-thread watcher verified merged state from `{branch_name}` "
                    f"at `{last_run}`, cleared `PR Merge Verification Pending`, emitted the "
                    "thread update, and retired its watcher host."
                ),
                "",
                "Task:",
                "Run Release Readiness validation from updated main.",
                "",
                "Scope:",
                f"- Validate PR #{pr_number} merge truth.",
                "- Validate same-thread watcher merge-verification proof.",
                "- Validate watcher shutdown/deletion proof.",
                "- Validate merged-main canon and branch-record posture.",
                "- Validate pending release posture and selected-next truth remain preserved.",
                "- Identify release blockers or bounded repair candidates.",
                "",
                "Return:",
                "- governed state markers",
                "- validation commands and results",
                "- merge verification findings",
                "- watcher lifecycle findings",
                "- release readiness findings",
                "- repair candidates, if any",
                "- rollback path",
                "- continue/stop decision",
                "```",
            ]
        )
    else:
        if merge_watch_active or "PR Merge Verification Pending" in blockers_list:
            next_prompt_basis = (
                "- No Release Readiness prompt is legal yet.\n"
                "- Keep PR Readiness PR2 active until this watcher reports `merged=true`."
            )
        else:
            next_prompt_basis = (
                "- No Release Readiness prompt is legal yet.\n"
                "- Keep PR Readiness PR1 active until live PR validation blockers clear."
            )
        lines.extend(
            [
                "",
                "Next Prompt Basis:",
                *next_prompt_basis.splitlines(),
            ]
        )

    return "\n".join(lines)


def error_thread_message(pr_number: int, message: str) -> str:
    return (
        f"PR watcher update for PR #{pr_number}: live PR inspection failed with `{message}`. "
        "`PR Watcher Provisioning Unproven` is clear because the same-thread watcher is running, "
        "but `PR State Unknown` and `PR Merge Verification Pending` remain active. "
        "`Release Readiness` is not legal yet."
    )


def append_thread_message(
    *,
    thread_id: str,
    rollout_path: Path,
    state_db_path: Path,
    message: str,
) -> str:
    timestamp = utc_now_iso()
    started_at = int(utc_now().timestamp())
    completed_at = int(utc_now().timestamp())
    turn_id = str(uuid.uuid4())
    payloads = (
        {
            "timestamp": timestamp,
            "type": "event_msg",
            "payload": {
                "type": "task_started",
                "turn_id": turn_id,
                "started_at": started_at,
                "model_context_window": 258400,
                "collaboration_mode_kind": "default",
            },
        },
        {
            "timestamp": timestamp,
            "type": "event_msg",
            "payload": {
                "type": "agent_message",
                "message": message,
                "phase": "final_answer",
                "memory_citation": None,
            },
        },
        {
            "timestamp": timestamp,
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": message}],
                "phase": "final_answer",
            },
        },
        {
            "timestamp": timestamp,
            "type": "event_msg",
            "payload": {
                "type": "task_complete",
                "turn_id": turn_id,
                "last_agent_message": message,
                "completed_at": completed_at,
                "duration_ms": 0,
            },
        },
    )
    ensure_parent(rollout_path)
    with rollout_path.open("a", encoding="utf-8") as handle:
        for record in payloads:
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")

    if state_db_path.is_file():
        try:
            connection = sqlite3.connect(state_db_path)
            connection.execute(
                "UPDATE threads SET updated_at = ? WHERE id = ?",
                (int(utc_now().timestamp()), thread_id),
            )
            connection.commit()
        except sqlite3.Error:
            pass
        finally:
            try:
                connection.close()
            except Exception:
                pass
    return timestamp


def _assistant_messages_from_record(record: object) -> list[str]:
    if not isinstance(record, dict):
        return []
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return []

    messages: list[str] = []
    if payload.get("type") == "agent_message":
        message = payload.get("message")
        if isinstance(message, str):
            messages.append(message)
    if payload.get("type") == "task_complete":
        message = payload.get("last_agent_message")
        if isinstance(message, str):
            messages.append(message)
    if payload.get("type") == "message" and payload.get("role") == "assistant":
        for item in payload.get("content") or []:
            if isinstance(item, dict) and item.get("type") == "output_text":
                text = item.get("text")
                if isinstance(text, str):
                    messages.append(text)
    return messages


def transcript_has_assistant_message(rollout_path: Path, message: str) -> bool:
    if not rollout_path.is_file():
        return False
    try:
        lines = rollout_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return False
    for line in reversed(lines[-400:]):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if any(candidate == message for candidate in _assistant_messages_from_record(record)):
            return True
    return False


def wait_for_assistant_transcript_message(
    rollout_path: Path,
    message: str,
    *,
    attempts: int = 6,
    delay_seconds: float = 0.5,
) -> bool:
    for attempt in range(max(1, attempts)):
        if transcript_has_assistant_message(rollout_path, message):
            return True
        if attempt < attempts - 1:
            time.sleep(delay_seconds)
    return False


def touch_codex_thread_state(state_db_path: Path, thread_id: str) -> tuple[bool, str]:
    if not state_db_path.is_file():
        return False, f"Codex thread state database '{state_db_path}' is missing"
    connection = None
    try:
        connection = sqlite3.connect(state_db_path)
        cursor = connection.execute(
            "UPDATE threads SET updated_at = ? WHERE id = ?",
            (int(utc_now().timestamp()), thread_id),
        )
        connection.commit()
        if cursor.rowcount == 0:
            return False, f"Codex thread '{thread_id}' was not found in '{state_db_path}'"
    except sqlite3.Error as exc:
        return False, f"failed to refresh Codex thread state for '{thread_id}': {exc}"
    finally:
        try:
            if connection is not None:
                connection.close()
        except Exception:
            pass
    return True, f"Codex thread state refreshed for '{thread_id}'"


def record_visible_delivery(
    *,
    automation_db_path: Path,
    automation_id: str,
    thread_id: str,
    thread_title: str,
    source_cwd: Path,
    inbox_title: str,
    message: str,
) -> tuple[bool, str]:
    if not automation_db_path.is_file():
        return False, f"Codex automation database '{automation_db_path}' is missing"
    now_ms = int(utc_now().timestamp() * 1000)
    connection = None
    try:
        connection = sqlite3.connect(automation_db_path)
        existing_run_created_at = connection.execute(
            "SELECT created_at FROM automation_runs WHERE thread_id = ?",
            (thread_id,),
        ).fetchone()
        run_created_at = (
            int(existing_run_created_at[0]) if existing_run_created_at else now_ms
        )
        connection.execute(
            """
            INSERT INTO automation_runs (
                thread_id, automation_id, status, read_at, thread_title, source_cwd,
                inbox_title, inbox_summary, created_at, updated_at,
                archived_user_message, archived_assistant_message, archived_reason
            ) VALUES (?, ?, 'PENDING_REVIEW', NULL, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL)
            ON CONFLICT(thread_id) DO UPDATE SET
                automation_id = excluded.automation_id,
                status = 'PENDING_REVIEW',
                read_at = NULL,
                thread_title = excluded.thread_title,
                source_cwd = excluded.source_cwd,
                inbox_title = excluded.inbox_title,
                inbox_summary = excluded.inbox_summary,
                updated_at = excluded.updated_at
            """,
            (
                thread_id,
                automation_id,
                thread_title,
                str(source_cwd),
                inbox_title,
                message,
                run_created_at,
                now_ms,
            ),
        )
        inbox_id = f"{automation_id}:{thread_id}"
        existing_inbox_created_at = connection.execute(
            "SELECT created_at FROM inbox_items WHERE id = ?",
            (inbox_id,),
        ).fetchone()
        inbox_created_at = (
            int(existing_inbox_created_at[0]) if existing_inbox_created_at else now_ms
        )
        connection.execute(
            """
            INSERT INTO inbox_items (id, title, description, thread_id, read_at, created_at)
            VALUES (?, ?, ?, ?, NULL, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                description = excluded.description,
                thread_id = excluded.thread_id,
                read_at = NULL
            """,
            (
                inbox_id,
                inbox_title,
                message,
                thread_id,
                inbox_created_at,
            ),
        )
        connection.commit()
    except sqlite3.Error as exc:
        return False, f"failed to record visible watcher delivery in Codex app state: {exc}"
    finally:
        try:
            if connection is not None:
                connection.close()
        except Exception:
            pass
    return True, f"Codex automation run and inbox delivery recorded for '{thread_id}'"


def deliver_thread_update(
    *,
    codex_exe: Path | None,
    repo_root: Path,
    thread_id: str,
    rollout_path: Path,
    state_db_path: Path,
    automation_db_path: Path,
    automation_id: str,
    thread_title: str,
    inbox_title: str,
    message: str,
    output_path: Path,
) -> tuple[str, str, bool, str]:
    attempts: list[str] = []
    emitted_at = ""
    used_codex_resume = False
    used_fallback = False

    if codex_exe is not None:
        try:
            emitted_at = emit_via_codex_resume(
                codex_exe=codex_exe,
                repo_root=repo_root,
                thread_id=thread_id,
                message=message,
                output_path=output_path,
            )
            used_codex_resume = True
            attempts.append("codex_resume command returned")
        except Exception as exc:
            attempts.append(f"codex_resume failed: {exc}")

    transcript_proven = wait_for_assistant_transcript_message(rollout_path, message)
    if not transcript_proven:
        emitted_at = append_thread_message(
            thread_id=thread_id,
            rollout_path=rollout_path,
            state_db_path=state_db_path,
            message=message,
        )
        used_fallback = True
        attempts.append("verified transcript fallback appended assistant message")
        transcript_proven = wait_for_assistant_transcript_message(
            rollout_path,
            message,
            attempts=3,
            delay_seconds=0.25,
        )

    thread_state_ok, thread_state_message = touch_codex_thread_state(state_db_path, thread_id)
    visible_delivery_ok, visible_delivery_message = record_visible_delivery(
        automation_db_path=automation_db_path,
        automation_id=automation_id,
        thread_id=thread_id,
        thread_title=thread_title,
        source_cwd=repo_root,
        inbox_title=inbox_title,
        message=message,
    )
    attempts.extend(
        [
            f"assistant transcript proof={'present' if transcript_proven else 'missing'}",
            thread_state_message,
            visible_delivery_message,
        ]
    )

    emit_method = "rollout_fallback"
    if used_codex_resume and used_fallback:
        emit_method = "codex_resume+verified_fallback"
    elif used_codex_resume:
        emit_method = "codex_resume"

    delivery_proven = transcript_proven and thread_state_ok and visible_delivery_ok
    return emitted_at or utc_now_iso(), emit_method, delivery_proven, "; ".join(attempts)


def find_codex_exe(explicit_path: str) -> Path | None:
    candidates = []
    if explicit_path:
        candidates.append(Path(explicit_path))
    if which("codex"):
        candidates.append(Path(which("codex") or ""))
    candidates.append(Path.home() / "codex-debug" / "codex.exe")

    for candidate in candidates:
        if candidate and candidate.is_file():
            return candidate
    return None


def emit_via_codex_resume(
    *,
    codex_exe: Path,
    repo_root: Path,
    thread_id: str,
    message: str,
    output_path: Path,
) -> str:
    ensure_parent(output_path)
    prompt = f"Post exactly the following PR watcher update to the user and nothing else:\n\n{message}"
    process = _subprocess_run(
        [
            str(codex_exe),
            "exec",
            "resume",
            thread_id,
            prompt,
            "--dangerously-bypass-approvals-and-sandbox",
            "-o",
            str(output_path),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        stderr = process.stderr.strip()
        stdout = process.stdout.strip()
        raise RuntimeError(stderr or stdout or f"codex resume failed with exit code {process.returncode}")
    return utc_now_iso()


def build_comment_repair_worker_prompt(
    *,
    repo_full_name: str,
    pr_number: int,
    branch_record_path: Path,
) -> str:
    return (
        f"You are operating on the current checked-out branch for {repo_full_name} PR #{pr_number}.\n"
        "Goal: address actionable unresolved review feedback from chatgpt-codex-connector[bot] on this PR only.\n"
        "Use the GitHub connector/tools available in this environment.\n\n"
        "Required workflow:\n"
        "1. Inspect the live unresolved review threads/comments for this PR.\n"
        "2. If there are no unresolved actionable bot review comments, make no code changes and say so clearly.\n"
        "3. If there are actionable unresolved bot review comments, implement the minimum fix on this same branch only.\n"
        "4. Run the minimum relevant validation.\n"
        "5. Commit and push the fix.\n"
        "6. Reply to each addressed top-level bot review comment with a concise resolution note naming the new commit SHA.\n"
        "7. Resolve each addressed review thread.\n"
        f"8. Update {branch_record_path} so the bot-review state truth reflects `Comment addressed` for the current head when applicable.\n"
        "9. Do not merge the PR. Do not widen scope. Do not create a new branch.\n\n"
        "Respond with a short final summary only."
    )


def run_comment_repair_worker(
    *,
    codex_exe: Path,
    repo_root: Path,
    repo_full_name: str,
    pr_number: int,
    branch_record_path: Path,
    output_path: Path,
) -> tuple[bool, str]:
    ensure_parent(output_path)
    prompt = build_comment_repair_worker_prompt(
        repo_full_name=repo_full_name,
        pr_number=pr_number,
        branch_record_path=branch_record_path,
    )
    process = _subprocess_run(
        [
            str(codex_exe),
            "exec",
            "-",
            "--dangerously-bypass-approvals-and-sandbox",
            "-C",
            str(repo_root),
            "-o",
            str(output_path),
        ],
        cwd=repo_root,
        input=prompt,
        capture_output=True,
        text=True,
        check=False,
    )
    summary = ""
    if output_path.is_file():
        try:
            summary = output_path.read_text(encoding="utf-8").strip()
        except OSError:
            summary = ""
    if not summary:
        summary = process.stderr.strip() or process.stdout.strip()
    if not summary:
        summary = f"codex exec exited with code {process.returncode}"
    return process.returncode == 0, summary


def _normalize_id(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return normalized or "watcher-host"


def ensure_visible_thread_host(
    *,
    automation_db_path: Path,
    automation_id: str,
    automation_name: str,
    repo_root: Path,
    thread_id: str,
    thread_title: str,
    inbox_title: str,
    inbox_summary: str,
) -> tuple[bool, str]:
    ensure_parent(automation_db_path)
    now_ms = int(utc_now().timestamp() * 1000)
    automation_dir = Path.home() / ".codex" / "automations" / automation_id
    automation_toml = automation_dir / "automation.toml"
    automation_prompt = (
        "Host a visible Codex thread for the local PR watcher so status-change updates from the "
        "scheduled watcher surface in the app."
    )
    ensure_parent(automation_toml)
    created_at = now_ms
    if automation_toml.is_file():
        try:
            existing_text = automation_toml.read_text(encoding="utf-8")
            existing_created_at = re.search(r"^created_at = (\d+)$", existing_text, flags=re.M)
            if existing_created_at:
                created_at = int(existing_created_at.group(1))
        except (OSError, ValueError):
            created_at = now_ms
    # Always rewrite the host config so a stale target_thread_id cannot survive retargeting.
    automation_toml.write_text(
        "\n".join(
            [
                "version = 1",
                f'id = "{automation_id}"',
                'kind = "heartbeat"',
                f'name = "{automation_name}"',
                f'prompt = "{automation_prompt}"',
                'status = "ACTIVE"',
                'rrule = "FREQ=MINUTELY;INTERVAL=1"',
                'target_thread_id = "' + thread_id + '"',
                f"created_at = {created_at}",
                f"updated_at = {now_ms}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    connection = None
    try:
        connection = sqlite3.connect(automation_db_path)
        connection.execute(
            """
            INSERT INTO automations (
                id, name, prompt, status, next_run_at, last_run_at, cwds, rrule, model,
                reasoning_effort, created_at, updated_at
            ) VALUES (?, ?, ?, 'ACTIVE', NULL, ?, ?, 'FREQ=MINUTELY;INTERVAL=1', ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                prompt = excluded.prompt,
                status = 'ACTIVE',
                cwds = excluded.cwds,
                rrule = excluded.rrule,
                model = excluded.model,
                reasoning_effort = excluded.reasoning_effort,
                updated_at = excluded.updated_at
            """,
            (
                automation_id,
                automation_name,
                automation_prompt,
                now_ms,
                json.dumps([str(repo_root)]),
                "gpt-5.4-mini",
                "low",
                now_ms,
                now_ms,
            ),
        )
        existing_created_at = connection.execute(
            "SELECT created_at FROM automation_runs WHERE thread_id = ?",
            (thread_id,),
        ).fetchone()
        created_at = int(existing_created_at[0]) if existing_created_at else now_ms
        connection.execute(
            """
            INSERT INTO automation_runs (
                thread_id, automation_id, status, read_at, thread_title, source_cwd,
                inbox_title, inbox_summary, created_at, updated_at,
                archived_user_message, archived_assistant_message, archived_reason
            ) VALUES (?, ?, 'PENDING_REVIEW', NULL, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL)
            ON CONFLICT(thread_id) DO UPDATE SET
                automation_id = excluded.automation_id,
                status = 'PENDING_REVIEW',
                read_at = NULL,
                thread_title = excluded.thread_title,
                source_cwd = excluded.source_cwd,
                inbox_title = excluded.inbox_title,
                inbox_summary = excluded.inbox_summary,
                updated_at = excluded.updated_at
            """,
            (
                thread_id,
                automation_id,
                thread_title,
                str(repo_root),
                inbox_title,
                inbox_summary,
                created_at,
                now_ms,
            ),
        )
        inbox_id = f"{automation_id}:{thread_id}"
        existing_inbox_created_at = connection.execute(
            "SELECT created_at FROM inbox_items WHERE id = ?",
            (inbox_id,),
        ).fetchone()
        inbox_created_at = (
            int(existing_inbox_created_at[0]) if existing_inbox_created_at else now_ms
        )
        connection.execute(
            """
            INSERT INTO inbox_items (id, title, description, thread_id, read_at, created_at)
            VALUES (?, ?, ?, ?, NULL, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                description = excluded.description,
                thread_id = excluded.thread_id,
                read_at = NULL
            """,
            (
                inbox_id,
                inbox_title,
                inbox_summary,
                thread_id,
                inbox_created_at,
            ),
        )
        connection.commit()
    except sqlite3.Error as exc:
        return False, f"failed to register visible watcher host in Codex app state: {exc}"
    finally:
        try:
            connection.close()
        except Exception:
            pass
    return True, f"visible watcher host '{automation_name}' is registered for thread '{thread_id}'"


def retire_visible_thread_host(
    *,
    automation_db_path: Path,
    automation_id: str,
) -> tuple[bool, str]:
    now_ms = int(utc_now().timestamp() * 1000)
    automation_dir = Path.home() / ".codex" / "automations" / automation_id
    automation_toml = automation_dir / "automation.toml"
    connection = None
    try:
        if automation_toml.is_file():
            automation_toml.unlink()
        try:
            automation_dir.rmdir()
        except OSError:
            pass

        if automation_db_path.is_file():
            connection = sqlite3.connect(automation_db_path)
            connection.execute("DELETE FROM automations WHERE id = ?", (automation_id,))
            connection.execute(
                """
                UPDATE automation_runs
                SET status = 'COMPLETED', updated_at = ?
                WHERE automation_id = ?
                """,
                (now_ms, automation_id),
            )
            connection.commit()
    except (OSError, sqlite3.Error) as exc:
        return False, f"failed to retire visible watcher host '{automation_id}': {exc}"
    finally:
        try:
            if connection is not None:
                connection.close()
        except Exception:
            pass
    return True, f"visible watcher host '{automation_id}' retired"


def signature_for(status: dict[str, object]) -> str:
    fields = {
        "prState": status.get("prState"),
        "merged": status.get("merged"),
        "draft": status.get("draft"),
        "mergeable": status.get("mergeable"),
        "mergeableState": status.get("mergeableState"),
        "headSha": status.get("headSha"),
        "localHeadSha": status.get("localHeadSha"),
        "botApproval": status.get("botApproval"),
        "botCommentCount": status.get("botCommentCount"),
        "error": status.get("error"),
        "lastRepairAttemptStatus": status.get("lastRepairAttemptStatus"),
        "lastRepairAttemptKey": status.get("lastRepairAttemptKey"),
    }
    return json.dumps(fields, sort_keys=True, separators=(",", ":"))


def build_status(
    *,
    repo_full_name: str,
    pr_number: int,
    repo_root: Path,
) -> dict[str, object]:
    html = fetch_pr_page(repo_full_name, pr_number)
    pr_status = parse_pr_page(html, repo_full_name, pr_number)
    rest_status, rest_status_error = fetch_rest_pr_status(repo_full_name, pr_number)
    if rest_status:
        pr_status.update(rest_status)
    rest_approval, rest_comment_count, rest_signal_error = fetch_rest_bot_signal(
        repo_full_name,
        pr_number,
        str(pr_status.get("headSha") or ""),
    )
    pr_status["botApproval"] = bool(pr_status.get("botApproval")) or rest_approval
    pr_status["botCommentCount"] = max(
        int(pr_status.get("botCommentCount") or 0),
        rest_comment_count,
    )
    pr_status["botSignalError"] = rest_signal_error
    pr_status["prStatusError"] = rest_status_error
    local_head = run_git(repo_root, "rev-parse", "HEAD")
    local_branch = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    mergeable, merge_error = compute_local_merge(repo_root, str(pr_status.get("baseRef") or "main"))

    pr_status["localHeadSha"] = local_head
    pr_status["localBranch"] = local_branch
    pr_status["mergeable"] = mergeable
    pr_status["mergeableState"] = (
        "CLEAN" if mergeable is True else "DIRTY" if mergeable is False else "UNKNOWN"
    )
    pr_status["mergeableError"] = merge_error
    pr_status["lastRunLocal"] = utc_now_iso()
    pr_status["phase"] = ""
    pr_status["error"] = ""
    return pr_status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-full-name", required=True)
    parser.add_argument("--pr-number", type=int, required=True)
    parser.add_argument("--task-name", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--branch-record", required=True)
    parser.add_argument("--state-path", required=True)
    parser.add_argument("--latest-path", required=True)
    parser.add_argument("--log-path", required=True)
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--thread-rollout-path", required=True)
    parser.add_argument("--state-db-path", required=True)
    parser.add_argument("--required-phase", default="PR Readiness")
    parser.add_argument("--codex-exe", default="")
    parser.add_argument("--resume-output-path", default="")
    parser.add_argument("--automation-db-path", default=str(Path.home() / ".codex" / "sqlite" / "codex-dev.db"))
    parser.add_argument("--ui-automation-id", default="")
    parser.add_argument("--ui-automation-name", default="")
    parser.add_argument("--ui-thread-title", default="")
    parser.add_argument("--ui-inbox-title", default="")
    parser.add_argument("--force-emit", action="store_true")
    parser.add_argument("--override-thread-message", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root)
    branch_record_path = Path(args.branch_record)
    state_path = Path(args.state_path)
    latest_path = Path(args.latest_path)
    log_path = Path(args.log_path)
    thread_rollout_path = Path(args.thread_rollout_path)
    state_db_path = Path(args.state_db_path)
    automation_db_path = Path(args.automation_db_path)
    codex_exe = find_codex_exe(args.codex_exe)
    resume_output_path = (
        Path(args.resume_output_path)
        if args.resume_output_path
        else latest_path.with_name(f"{latest_path.stem}-resume.txt")
    )

    phase = branch_phase(branch_record_path)
    if phase != args.required_phase:
        message = f"Watcher stopped because branch phase is '{phase}'."
        set_text(latest_path, message)
        append_log(log_path, message)
        stop_task(args.task_name)
        return 0

    existing_state = load_state(state_path)
    status: dict[str, object]
    try:
        status = build_status(
            repo_full_name=args.repo_full_name,
            pr_number=args.pr_number,
            repo_root=repo_root,
        )
    except Exception as exc:  # pragma: no cover - runtime fallback behavior
        status = {
            "prNumber": args.pr_number,
            "phase": phase,
            "lastRunLocal": utc_now_iso(),
            "localHeadSha": "",
            "headSha": "",
            "prState": "UNKNOWN",
            "merged": False,
            "draft": False,
            "mergeable": None,
            "mergeableState": "UNKNOWN",
            "botApproval": False,
            "botCommentCount": 0,
            "error": str(exc),
        }
        try:
            status["localHeadSha"] = run_git(repo_root, "rev-parse", "HEAD")
            status["headSha"] = status["localHeadSha"]
        except Exception:
            pass

    status["phase"] = phase
    status.update(branch_record_snapshot(branch_record_path))
    status["threadId"] = args.thread_id
    status["threadRolloutPath"] = str(thread_rollout_path)
    status["lastRepairAttemptKey"] = existing_state.get("lastRepairAttemptKey", "")
    status["lastRepairAttemptAt"] = existing_state.get("lastRepairAttemptAt", "")
    status["lastRepairAttemptStatus"] = existing_state.get("lastRepairAttemptStatus", "")
    status["lastRepairWorkerSummary"] = existing_state.get("lastRepairWorkerSummary", "")
    status["lastRepairWorkerOutputPath"] = existing_state.get("lastRepairWorkerOutputPath", "")

    line = (
        f"PR #{args.pr_number} state={status.get('prState')} merged={status.get('merged')} "
        f"draft={status.get('draft')} mergeable={status.get('mergeable')} "
        f"mergeable_state={status.get('mergeableState')} headSha={status.get('headSha')} "
        f"localHeadSha={status.get('localHeadSha')} botApproval={status.get('botApproval')} "
        f"botComments={status.get('botCommentCount')}"
    )
    if status.get("error"):
        line = f"{line} error={status.get('error')}"
    set_text(latest_path, line)
    append_log(log_path, line)

    automation_id = args.ui_automation_id.strip() or _normalize_id(f"local-pr-{args.pr_number}-watch-host")
    automation_name = args.ui_automation_name.strip() or f"PR #{args.pr_number} Watch Host"
    thread_title = args.ui_thread_title.strip() or automation_name
    inbox_title = args.ui_inbox_title.strip() or f"PR #{args.pr_number} watcher update"
    visible_thread_ok, visible_thread_message = ensure_visible_thread_host(
        automation_db_path=automation_db_path,
        automation_id=automation_id,
        automation_name=automation_name,
        repo_root=repo_root,
        thread_id=args.thread_id,
        thread_title=thread_title,
        inbox_title=inbox_title,
        inbox_summary=line,
    )
    append_log(log_path, visible_thread_message)
    status["visibleThreadRegistered"] = visible_thread_ok
    status["visibleThreadAutomationId"] = automation_id
    status["visibleThreadAutomationName"] = automation_name

    repair_triggered = False
    repair_output_path = latest_path.with_name(f"{latest_path.stem}-worker.txt")
    bot_comment_count = int(status.get("botCommentCount") or 0)
    recorded_bot_status = str(status.get("branchRecordBotReviewStatus") or "").strip().casefold()
    recorded_bot_head = str(status.get("branchRecordBotReviewHead") or "").strip()
    current_head = str(status.get("localHeadSha") or status.get("headSha") or "").strip()
    recorded_comment_addressed = (
        recorded_bot_status in {"approved", "comment addressed"}
        and (
            recorded_bot_head == current_head
            or git_is_ancestor(repo_root, recorded_bot_head, current_head)
        )
    )
    repair_key = f"{status.get('headSha') or ''}:{bot_comment_count}"
    if (
        codex_exe is not None
        and not bool(status.get("merged"))
        and str(status.get("prState") or "").upper() != "CLOSED"
        and bot_comment_count > 0
        and not recorded_comment_addressed
        and repair_key
        and (
            repair_key != str(existing_state.get("lastRepairAttemptKey") or "")
            or str(existing_state.get("lastRepairAttemptStatus") or "").strip().casefold()
            == "failed"
        )
    ):
        repair_triggered = True
        append_log(
            log_path,
            f"Triggering bounded comment-repair worker for PR #{args.pr_number} with key {repair_key}.",
        )
        status["lastRepairAttemptKey"] = repair_key
        status["lastRepairAttemptAt"] = utc_now_iso()
        repair_ok, repair_summary = run_comment_repair_worker(
            codex_exe=codex_exe,
            repo_root=repo_root,
            repo_full_name=args.repo_full_name,
            pr_number=args.pr_number,
            branch_record_path=branch_record_path,
            output_path=repair_output_path,
        )
        status["lastRepairAttemptStatus"] = "succeeded" if repair_ok else "failed"
        status["lastRepairWorkerSummary"] = repair_summary
        status["lastRepairWorkerOutputPath"] = str(repair_output_path)
        append_log(
            log_path,
            (
                f"Comment-repair worker {'completed' if repair_ok else 'failed'} for PR "
                f"#{args.pr_number}: {repair_summary}"
            ),
        )
        try:
            refreshed_status = build_status(
                repo_full_name=args.repo_full_name,
                pr_number=args.pr_number,
                repo_root=repo_root,
            )
            refreshed_status["phase"] = phase
            refreshed_status.update(branch_record_snapshot(branch_record_path))
            refreshed_status["threadId"] = args.thread_id
            refreshed_status["threadRolloutPath"] = str(thread_rollout_path)
            refreshed_status["lastRepairAttemptKey"] = status["lastRepairAttemptKey"]
            refreshed_status["lastRepairAttemptAt"] = status["lastRepairAttemptAt"]
            refreshed_status["lastRepairAttemptStatus"] = status["lastRepairAttemptStatus"]
            refreshed_status["lastRepairWorkerSummary"] = status["lastRepairWorkerSummary"]
            refreshed_status["lastRepairWorkerOutputPath"] = status["lastRepairWorkerOutputPath"]
            status = refreshed_status
        except Exception as exc:  # pragma: no cover - defensive runtime path
            append_log(log_path, f"Post-repair status refresh failed: {exc}")

    current_signature = signature_for(status)
    previous_signature = str(existing_state.get("lastSignature") or "")
    should_emit = (
        repair_triggered
        or args.force_emit
        or current_signature != previous_signature
        or not str(existing_state.get("lastThreadEmitAt") or "").strip()
        or not bool(existing_state.get("lastThreadDeliveryProven"))
    )

    if should_emit:
        message = args.override_thread_message or (
            error_thread_message(args.pr_number, str(status.get("error")))
            if status.get("error")
            else current_thread_message(status)
        )
        emitted_at, emit_method, delivery_proven, delivery_proof = deliver_thread_update(
            codex_exe=codex_exe,
            repo_root=repo_root,
            thread_id=args.thread_id,
            rollout_path=thread_rollout_path,
            state_db_path=state_db_path,
            automation_db_path=automation_db_path,
            automation_id=automation_id,
            thread_title=thread_title,
            inbox_title=inbox_title,
            message=message,
            output_path=resume_output_path,
        )
        status["lastThreadEmitAt"] = emitted_at
        status["lastThreadEmitMessage"] = message
        status["lastThreadEmitSignature"] = current_signature
        status["lastThreadEmitMethod"] = emit_method
        status["lastThreadDeliveryProven"] = delivery_proven
        status["lastThreadDeliveryProof"] = delivery_proof
        append_log(
            log_path,
            (
                f"Emitted same-thread update at {emitted_at} via {emit_method}; "
                f"delivery_proven={delivery_proven}; {delivery_proof}"
            ),
        )
    else:
        status["lastThreadEmitAt"] = existing_state.get("lastThreadEmitAt", "")
        status["lastThreadEmitMessage"] = existing_state.get("lastThreadEmitMessage", "")
        status["lastThreadEmitSignature"] = existing_state.get(
            "lastThreadEmitSignature", previous_signature
        )
        status["lastThreadEmitMethod"] = existing_state.get("lastThreadEmitMethod", "")
        status["lastThreadDeliveryProven"] = existing_state.get(
            "lastThreadDeliveryProven",
            False,
        )
        status["lastThreadDeliveryProof"] = existing_state.get("lastThreadDeliveryProof", "")

    status["lastSignature"] = current_signature
    save_json(state_path, status)

    if bool(status.get("merged")) or str(status.get("prState") or "").upper() == "CLOSED":
        if not bool(status.get("lastThreadDeliveryProven")):
            message = (
                "Watcher is not stopping because final thread delivery proof is missing; "
                "it will retry on the next scheduled run."
            )
            append_log(log_path, message)
            status["visibleThreadHostRetired"] = False
            status["visibleThreadHostRetireMessage"] = message
            save_json(state_path, status)
            return 0
        append_log(log_path, "Stopping watcher because PR is closed or merged.")
        retired, retire_message = retire_visible_thread_host(
            automation_db_path=automation_db_path,
            automation_id=automation_id,
        )
        append_log(log_path, retire_message)
        status["visibleThreadHostRetired"] = retired
        status["visibleThreadHostRetireMessage"] = retire_message
        save_json(state_path, status)
        stop_task(args.task_name)

    return 0


if __name__ == "__main__":
    sys.exit(main())
