from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import error as urllib_error
from urllib import request as urllib_request


BOT_LOGIN = "chatgpt-codex-connector[bot]"
BOT_APPROVAL_TEXT = f"{BOT_LOGIN} reacted with thumbs up emoji"


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
    subprocess.run(
        ["schtasks", "/Delete", "/TN", task_name, "/F"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def run_git(repo_root: Path, *args: str, check: bool = True) -> str:
    process = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or process.stdout.strip() or "git command failed")
    return process.stdout.strip()


def branch_phase(branch_record_path: Path) -> str:
    if not branch_record_path.is_file():
        return ""
    text = branch_record_path.read_text(encoding="utf-8")
    match = re.search(r"^- Phase: `([^`]+)`", text, flags=re.M)
    return match.group(1).strip() if match else ""


def fetch_pr_page(repo_full_name: str, pr_number: int) -> str:
    url = f"https://github.com/{repo_full_name}/pull/{pr_number}"
    request = urllib_request.Request(url, headers={"User-Agent": "Codex"})
    with urllib_request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


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
        process = subprocess.run(
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
    bot_approval_label = "present" if status.get("botApproval") else "pending"
    bot_comment_count = int(status.get("botCommentCount") or 0)
    if bot_comment_count:
        bot_comment_label = f"{bot_comment_count} provable bot comment(s)"
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
        "`Release Readiness` is now legal."
        if status.get("merged")
        else "`Release Readiness` is not legal yet."
    )
    remote_head = str(status.get("headSha") or "UNKNOWN")
    local_head = str(status.get("localHeadSha") or "UNKNOWN")
    state_label = str(status.get("prState") or "UNKNOWN").casefold()
    merged_label = "true" if status.get("merged") else "false"
    draft_label = "true" if status.get("draft") else "false"

    return (
        f"PR watcher update for PR #{pr_number}: state={state_label}, merged={merged_label}, "
        f"draft={draft_label}, merge-status {merge_status_label}, remote head {remote_head}, "
        f"local head {local_head}, bot approval {bot_approval_label}, {bot_comment_label}. "
        f"{watcher_blocker} {merge_status_blocker} {merge_verification_blocker} {release_posture}"
    )


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
    payloads = (
        {
            "timestamp": timestamp,
            "type": "event_msg",
            "payload": {
                "type": "agent_message",
                "message": message,
                "phase": "commentary",
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
                "phase": "commentary",
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
    status["threadId"] = args.thread_id
    status["threadRolloutPath"] = str(thread_rollout_path)

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

    current_signature = signature_for(status)
    previous_signature = str(existing_state.get("lastSignature") or "")
    should_emit = current_signature != previous_signature or not str(
        existing_state.get("lastThreadEmitAt") or ""
    ).strip()

    if should_emit:
        message = (
            error_thread_message(args.pr_number, str(status.get("error")))
            if status.get("error")
            else current_thread_message(status)
        )
        emitted_at = append_thread_message(
            thread_id=args.thread_id,
            rollout_path=thread_rollout_path,
            state_db_path=state_db_path,
            message=message,
        )
        status["lastThreadEmitAt"] = emitted_at
        status["lastThreadEmitMessage"] = message
        status["lastThreadEmitSignature"] = current_signature
        append_log(log_path, f"Emitted same-thread update at {emitted_at}")
    else:
        status["lastThreadEmitAt"] = existing_state.get("lastThreadEmitAt", "")
        status["lastThreadEmitMessage"] = existing_state.get("lastThreadEmitMessage", "")
        status["lastThreadEmitSignature"] = existing_state.get(
            "lastThreadEmitSignature", previous_signature
        )

    status["lastSignature"] = current_signature
    save_json(state_path, status)

    if bool(status.get("merged")) or str(status.get("prState") or "").upper() == "CLOSED":
        append_log(log_path, "Stopping watcher because PR is closed or merged.")
        stop_task(args.task_name)

    return 0


if __name__ == "__main__":
    sys.exit(main())
