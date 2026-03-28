import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
LAUNCHER_SCRIPT = Path(__file__).with_name("jarvis_desktop_launcher.pyw")
LIVE_LOG_DIR = ROOT_DIR / "logs"
HISTORY_FILENAME = "jarvis_history_v1.jsonl"

HISTORICAL_CONTEXT_MATCH_LINE = (
    "Historical context (prior finalized runs only): "
    "matching failure fingerprint observed in 1 prior run(s)."
)
HISTORICAL_CONTEXT_STABILITY_LINE = (
    "Historical context (prior finalized runs only): "
    "recent recorded failure history stability = stable."
)
HISTORICAL_ADVISORY_LINE = (
    "Advisory (historical, non-authoritative): "
    "this finalized failure fingerprint has appeared in 1 prior finalized failed run(s)."
)

HEALTHY_RENDERER_SCRIPT = """import sys
from pathlib import Path

runtime_log = ""
for index, arg in enumerate(sys.argv):
    if arg == "--runtime-log" and index + 1 < len(sys.argv):
        runtime_log = sys.argv[index + 1]
        break

if runtime_log:
    Path(runtime_log).parent.mkdir(parents=True, exist_ok=True)
    with open(runtime_log, "a", encoding="utf-8") as handle:
        handle.write("[00:00:00] RENDERER_MAIN|STARTUP_READY\\n")

raise SystemExit(0)
"""

FAILURE_RENDERER_SCRIPT = """import sys
from pathlib import Path

runtime_log = ""
for index, arg in enumerate(sys.argv):
    if arg == "--runtime-log" and index + 1 < len(sys.argv):
        runtime_log = sys.argv[index + 1]
        break

if runtime_log:
    Path(runtime_log).parent.mkdir(parents=True, exist_ok=True)
    with open(runtime_log, "a", encoding="utf-8") as handle:
        handle.write("[00:00:00] RENDERER_MAIN|STARTUP_READY\\n")

raise RuntimeError("Synthetic renderer failure")
"""


class HarnessAssertionError(RuntimeError):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="Contained historical-memory harness runner.")
    parser.add_argument(
        "--workspace-root",
        default="",
        help="Base directory for contained workspaces. Defaults to a temporary directory outside the live logs tree.",
    )
    return parser.parse_args()


def is_relative_to(path, parent):
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def assert_true(condition, message):
    if not condition:
        raise HarnessAssertionError(message)


def resolve_workspace_root(raw_value):
    if raw_value:
        workspace_root = Path(raw_value).resolve()
        workspace_root.mkdir(parents=True, exist_ok=True)
    else:
        workspace_root = Path(tempfile.mkdtemp(prefix="jarvis_fb014_rev1b_")).resolve()

    assert_true(
        not is_relative_to(workspace_root, LIVE_LOG_DIR),
        f"Contained workspace root must not be inside the live logs tree: {workspace_root}",
    )
    return workspace_root


def snapshot_live_log_tree():
    if not LIVE_LOG_DIR.exists():
        return {}

    snapshot = {}
    for path in LIVE_LOG_DIR.rglob("*"):
        if path.is_file():
            stat = path.stat()
            snapshot[str(path.resolve())] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def prepare_workspace(workspace_root, scenario_name):
    scenario_root = workspace_root / scenario_name
    if scenario_root.exists():
        shutil.rmtree(scenario_root)
    scenario_root.mkdir(parents=True)
    return scenario_root


def create_renderer_script(path, script_text):
    write_text(path, script_text)


def parse_history_file(path):
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines, [json.loads(line) for line in lines]


def collect_single_file(directory, pattern, required):
    matches = sorted(directory.glob(pattern))
    if required:
        assert_true(len(matches) == 1, f"Expected exactly one {pattern} in {directory}, found {len(matches)}.")
        return matches[0]
    assert_true(len(matches) <= 1, f"Expected at most one {pattern} in {directory}, found {len(matches)}.")
    return matches[0] if matches else None


def run_launcher_scenario(scenario_root, renderer_script, seed_history_lines=None):
    log_root = scenario_root / "logs"
    log_root.mkdir(parents=True, exist_ok=True)
    if seed_history_lines:
        write_text(log_root / HISTORY_FILENAME, "\n".join(seed_history_lines) + "\n")

    live_log_snapshot_before = snapshot_live_log_tree()

    env = os.environ.copy()
    env["JARVIS_HARNESS_LOG_ROOT"] = str(log_root)
    env["JARVIS_HARNESS_TARGET_SCRIPT"] = str(renderer_script)
    env["JARVIS_HARNESS_DISABLE_DIAGNOSTICS"] = "1"
    env["JARVIS_HARNESS_DISABLE_VOICE"] = "1"

    result = subprocess.run(
        [sys.executable, str(LAUNCHER_SCRIPT)],
        cwd=str(scenario_root),
        env=env,
        capture_output=True,
        text=True,
    )

    live_log_snapshot_after = snapshot_live_log_tree()
    assert_true(
        live_log_snapshot_before == live_log_snapshot_after,
        "Contained scenario wrote to or modified the live production logs tree.",
    )

    runtime_file = collect_single_file(log_root, "Runtime_*.txt", required=True)
    crash_dir = log_root / "crash"
    crash_file = collect_single_file(crash_dir, "Crash_*.txt", required=False) if crash_dir.exists() else None
    history_path = log_root / HISTORY_FILENAME
    assert_true(history_path.exists(), f"Missing history file for scenario: {history_path}")

    history_lines, history_records = parse_history_file(history_path)
    runtime_text = runtime_file.read_text(encoding="utf-8")
    crash_text = crash_file.read_text(encoding="utf-8") if crash_file else ""

    lingering_paths = {
        "diagnostics_status": log_root / "diagnostics_status.txt",
        "diagnostics_stop": log_root / "diagnostics_stop.signal",
        "startup_abort": log_root / "renderer_startup_abort.signal",
    }

    return {
        "scenario_root": scenario_root,
        "log_root": log_root,
        "renderer_script": renderer_script,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "runtime_file": runtime_file,
        "runtime_text": runtime_text,
        "crash_file": crash_file,
        "crash_text": crash_text,
        "history_path": history_path,
        "history_lines": history_lines,
        "history_records": history_records,
        "lingering_paths": lingering_paths,
    }


def assert_no_lingering_artifacts(result):
    for label, path in result["lingering_paths"].items():
        assert_true(not path.exists(), f"Lingering {label} artifact detected: {path}")


def assert_no_historical_output(text):
    assert_true("Historical context (prior finalized runs only):" not in text, "Unexpected historical context output present.")
    assert_true("Advisory (historical, non-authoritative):" not in text, "Unexpected historical advisory output present.")


def validate_healthy(result):
    assert_true(result["returncode"] == 0, "Healthy scenario launcher exit code was not 0.")
    assert_true(result["crash_file"] is None, "Healthy scenario should not produce a crash log.")
    assert_true(len(result["history_records"]) == 1, "Healthy scenario should write exactly one history record.")
    record = result["history_records"][0]
    assert_true(record["final_outcome"] == "SUCCESS", "Healthy scenario history final_outcome must be SUCCESS.")
    assert_true(record["final_classification"] == "NORMAL_EXIT_COMPLETE", "Healthy scenario final_classification must be NORMAL_EXIT_COMPLETE.")
    assert_true(record["attempt_count"] == 1, "Healthy scenario attempt_count must be 1.")
    assert_true("STATUS|SUCCESS|LAUNCHER_RUNTIME|NORMAL_EXIT_COMPLETE" in result["runtime_text"], "Healthy scenario missing NORMAL_EXIT_COMPLETE runtime marker.")
    assert_no_historical_output(result["runtime_text"])
    assert_no_lingering_artifacts(result)


def validate_failed_no_history(result):
    assert_true(result["returncode"] == 0, "Failed scenario launcher exit code was not 0.")
    assert_true(result["crash_file"] is not None, "Failed scenario should produce a crash log.")
    assert_true(len(result["history_records"]) == 1, "Failed scenario with no prior history should end with exactly one history record.")
    record = result["history_records"][0]
    assert_true(record["final_outcome"] == "FAILURE", "Failed scenario final_outcome must be FAILURE.")
    assert_true(
        record["final_classification"] == "CONSECUTIVE_IDENTICAL_CRASH_THRESHOLD_REACHED",
        "Failed scenario final_classification must reflect the repeated identical crash threshold.",
    )
    assert_true(record["attempt_pattern"] == "repeated identical crash", "Failed scenario attempt_pattern drifted from repeated identical crash.")
    assert_true(bool(record["failure_fingerprint"]), "Failed scenario must record a non-empty failure_fingerprint.")
    assert_true("STATUS|SUCCESS|LAUNCHER_RUNTIME|FAILURE_FLOW_COMPLETE" in result["runtime_text"], "Failed scenario missing FAILURE_FLOW_COMPLETE marker.")
    assert_no_historical_output(result["runtime_text"])
    assert_no_historical_output(result["crash_text"])
    assert_no_lingering_artifacts(result)


def validate_failed_matching_prior(result):
    assert_true(result["returncode"] == 0, "Matching-prior scenario launcher exit code was not 0.")
    assert_true(result["crash_file"] is not None, "Matching-prior scenario should produce a crash log.")
    assert_true(len(result["history_records"]) == 2, "Matching-prior scenario should end with two history records.")
    record = result["history_records"][-1]
    assert_true(record["final_outcome"] == "FAILURE", "Matching-prior scenario final_outcome must be FAILURE.")
    assert_true(
        record["final_classification"] == "CONSECUTIVE_IDENTICAL_CRASH_THRESHOLD_REACHED",
        "Matching-prior scenario final_classification must reflect the repeated identical crash threshold.",
    )
    assert_true(record["attempt_pattern"] == "repeated identical crash", "Matching-prior scenario attempt_pattern drifted from repeated identical crash.")
    assert_true(HISTORICAL_CONTEXT_MATCH_LINE in result["runtime_text"], "Matching-prior scenario missing historical recurrence context line.")
    assert_true(HISTORICAL_CONTEXT_STABILITY_LINE in result["runtime_text"], "Matching-prior scenario missing historical stability context line.")
    assert_true(HISTORICAL_ADVISORY_LINE in result["runtime_text"], "Matching-prior scenario missing historical advisory line.")
    assert_no_historical_output(result["crash_text"])
    assert_no_lingering_artifacts(result)


def print_result_summary(name, result):
    print(f"{name}: PASS")
    print(f"  workspace: {result['scenario_root']}")
    print(f"  runtime:   {result['runtime_file']}")
    if result["crash_file"] is not None:
        print(f"  crash:     {result['crash_file']}")
    print(f"  history:   {result['history_path']}")


def main():
    args = parse_args()
    workspace_root = resolve_workspace_root(args.workspace_root)

    healthy_root = prepare_workspace(workspace_root, "healthy_run")
    healthy_renderer = healthy_root / "renderer_ready.py"
    create_renderer_script(healthy_renderer, HEALTHY_RENDERER_SCRIPT)
    healthy_result = run_launcher_scenario(healthy_root, healthy_renderer)
    validate_healthy(healthy_result)
    print_result_summary("healthy_run", healthy_result)

    failed_no_history_root = prepare_workspace(workspace_root, "failed_no_prior_history")
    failed_renderer = failed_no_history_root / "renderer_failure.py"
    create_renderer_script(failed_renderer, FAILURE_RENDERER_SCRIPT)
    failed_no_history_result = run_launcher_scenario(failed_no_history_root, failed_renderer)
    validate_failed_no_history(failed_no_history_result)
    print_result_summary("failed_no_prior_history", failed_no_history_result)

    failed_matching_prior_root = prepare_workspace(workspace_root, "failed_matching_prior_history")
    matching_renderer = failed_matching_prior_root / "renderer_failure.py"
    create_renderer_script(matching_renderer, FAILURE_RENDERER_SCRIPT)
    failed_matching_prior_result = run_launcher_scenario(
        failed_matching_prior_root,
        matching_renderer,
        seed_history_lines=failed_no_history_result["history_lines"],
    )
    validate_failed_matching_prior(failed_matching_prior_result)
    print_result_summary("failed_matching_prior_history", failed_matching_prior_result)

    print(f"Workspace root: {workspace_root}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except HarnessAssertionError as exc:
        print(f"FB-014 harness failure: {exc}", file=sys.stderr)
        raise SystemExit(1)
