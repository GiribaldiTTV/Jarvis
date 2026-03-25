import os
import sys
import time
import ctypes
import subprocess
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_SCRIPT = os.path.join(ROOT_DIR, "jarvis_desktop_test.py")
LOG_DIR = os.path.join(ROOT_DIR, "logs")
CRASH_DIR = os.path.join(LOG_DIR, "crash")
DIAGNOSTICS_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_diagnostics.pyw")
VOICE_SCRIPT_CANDIDATES = [
    os.path.join(ROOT_DIR, "audio", "jarvis_voice.py"),
    os.path.join(ROOT_DIR, "Audio", "jarvis_voice.py"),
    os.path.join(ROOT_DIR, "jarvis_voice.py"),

]
ERROR_VOICE_SCRIPT_CANDIDATES = [
    os.path.join(ROOT_DIR, "audio", "jarvis_error_voice.py"),
    os.path.join(ROOT_DIR, "Audio", "jarvis_error_voice.py"),
    os.path.join(ROOT_DIR, "jarvis_error_voice.py"),

]

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CRASH_DIR, exist_ok=True)

MAX_RECOVERY_ATTEMPTS = 3
RECOVERY_COOLDOWN_SECONDS = 1.2
MUTEX_NAME = "Global\\JARVIS_DESKTOP_LAUNCHER_MUTEX"
VOICE_TIMEOUT_SECONDS = 20
VOICE_LINE_PAUSE_SECONDS = 0.9


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


RUNTIME_LOG_PATH = os.path.join(LOG_DIR, f"runtime_{now_stamp()}.txt")


def write_runtime(level: str, message: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RUNTIME_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] [{level}] {message}\n")


def write_crash_log(summary: str, details: str) -> str:
    crash_path = os.path.join(CRASH_DIR, f"crash_{now_stamp()}.txt")
    with open(crash_path, "w", encoding="utf-8") as f:
        f.write("JARVIS CRASH LOG\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Summary: {summary}\n")
        f.write(f"Target: {TARGET_SCRIPT}\n")
        f.write(f"Runtime log: {RUNTIME_LOG_PATH}\n\n")
        f.write(details)
        f.write("\n")
    write_runtime("ERROR", f"Crash log written: {crash_path}")
    return crash_path


def acquire_mutex():
    kernel32 = ctypes.windll.kernel32
    kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p]
    kernel32.CreateMutexW.restype = ctypes.c_void_p
    kernel32.GetLastError.restype = ctypes.c_ulong

    handle = kernel32.CreateMutexW(None, 0, MUTEX_NAME)
    already_exists = (kernel32.GetLastError() == 183)
    return handle, already_exists


def pythonw_exe() -> str:
    exe = sys.executable
    exe_dir = os.path.dirname(exe)
    preferred = os.path.join(exe_dir, "pythonw.exe")
    if os.path.exists(preferred):
        return preferred
    fallback = os.path.join(exe_dir, "python.exe")
    if os.path.exists(fallback):
        return fallback
    return exe


def no_window_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0


def existing_voice_script(candidates=None) -> str:
    candidates = candidates or VOICE_SCRIPT_CANDIDATES
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return ""


def speak_voice_line(text: str, glitch: bool = False) -> bool:
    voice_script = existing_voice_script(ERROR_VOICE_SCRIPT_CANDIDATES if glitch else VOICE_SCRIPT_CANDIDATES)
    if not voice_script:
        write_runtime("WARN", "No voice script found. Skipping voice line.")
        return False

    voice_exe = pythonw_exe()
    env = os.environ.copy()
    env["JARVIS_VOICE_TEXT"] = text
    env["JARVIS_VOICE_MODE"] = "malfunction" if glitch else "default"
    env["JARVIS_VOICE_EFFECT"] = "glitch" if glitch else "none"

    attempts = [
        ([voice_exe, voice_script, "--text", text, "--mode", "malfunction" if glitch else "default"], "voice --text --mode"),
        ([voice_exe, voice_script, text, "--mode", "malfunction" if glitch else "default"], "voice positional + --mode"),
        ([voice_exe, voice_script, "--text", text, "--effect", "glitch" if glitch else "none"], "voice --text --effect"),
        ([voice_exe, voice_script, text], "voice positional text"),
    ]

    for command, description in attempts:
        try:
            write_runtime("INFO", f"Trying voice line '{text}' using {description}")
            result = subprocess.run(
                command,
                cwd=ROOT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=no_window_flags(),
                timeout=VOICE_TIMEOUT_SECONDS,
                env=env,
            )

            if result.stdout:
                for line in result.stdout.splitlines():
                    if line.strip():
                        write_runtime("VOICE_STDOUT", line)

            if result.stderr:
                for line in result.stderr.splitlines():
                    if line.strip():
                        write_runtime("VOICE_STDERR", line)

            if result.returncode == 0:
                write_runtime("INFO", f"Voice line completed: {text}")
                return True
        except subprocess.TimeoutExpired:
            write_runtime("WARN", f"Voice line timed out: {text}")
        except Exception as e:
            write_runtime("ERROR", f"Voice line failed: {text} | {e}")

    write_runtime("WARN", f"All voice attempts failed for line: {text}")
    return False


def play_failure_sequence() -> None:
    lines = [
        ("Uhm..... Sir, I seem to be malfunctioning.", True),
        ("Attempting restart.", True),
        ("Restart failed.", True),
    ]

    for index, (line, glitch) in enumerate(lines, start=1):
        ok = speak_voice_line(line, glitch=glitch)
        write_runtime("INFO", f"Failure voice step {index}/{len(lines)} success={ok} line={line}")
        time.sleep(VOICE_LINE_PAUSE_SECONDS)


def launch_diagnostics(crash_path: str, summary: str) -> None:
    try:
        play_failure_sequence()

        diag_exe = pythonw_exe()
        if not os.path.exists(DIAGNOSTICS_SCRIPT):
            write_runtime("ERROR", f"Diagnostics script missing: {DIAGNOSTICS_SCRIPT}")
            return

        subprocess.Popen(
            [diag_exe, DIAGNOSTICS_SCRIPT, crash_path, summary],
            cwd=ROOT_DIR,
            close_fds=True,
            creationflags=no_window_flags(),
        )
        write_runtime("INFO", "Diagnostics process launched.")
    except Exception as e:
        write_runtime("ERROR", f"Failed to launch diagnostics process: {e}")


def run_renderer_once(attempt_number: int):
    exe = pythonw_exe()
    write_runtime("INFO", f"Starting desktop renderer process. attempt={attempt_number}")
    write_runtime("INFO", f"Child executable: {exe}")

    proc = subprocess.Popen(
        [exe, TARGET_SCRIPT],
        cwd=ROOT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=no_window_flags(),
    )
    stdout_text, stderr_text = proc.communicate()

    if stdout_text:
        for line in stdout_text.splitlines():
            if line.strip():
                write_runtime("STDOUT", line)

    if stderr_text:
        for line in stderr_text.splitlines():
            if line.strip():
                write_runtime("STDERR", line)

    write_runtime("INFO", f"Desktop renderer exited. exit_code={proc.returncode}")
    return proc.returncode, stdout_text, stderr_text


def main() -> int:
    _, already_exists = acquire_mutex()
    if already_exists:
        return 0

    write_runtime("INFO", "Jarvis Desktop launcher started.")
    write_runtime("INFO", f"Runtime log path: {RUNTIME_LOG_PATH}")
    write_runtime("INFO", f"Launcher executable: {sys.executable}")
    write_runtime("INFO", f"Root directory: {ROOT_DIR}")
    write_runtime("INFO", f"Target script: {TARGET_SCRIPT}")
    write_runtime("INFO", f"Diagnostics script: {DIAGNOSTICS_SCRIPT}")
    write_runtime("INFO", f"Recovery attempts allowed: {MAX_RECOVERY_ATTEMPTS}")

    voice_script = existing_voice_script()
    if voice_script:
        write_runtime("INFO", f"Voice hook ready: {voice_script}")
    else:
        write_runtime("WARN", "Voice hook not armed: jarvis_voice.py was not found in known locations.")

    if not os.path.exists(TARGET_SCRIPT):
        details = f"Missing target script:\n{TARGET_SCRIPT}"
        crash_path = write_crash_log("Target script missing", details)
        launch_diagnostics(crash_path, "Jarvis desktop target script is missing.")
        return 1

    last_stdout = ""
    last_stderr = ""

    for attempt in range(1, MAX_RECOVERY_ATTEMPTS + 1):
        exit_code, stdout_text, stderr_text = run_renderer_once(attempt)
        last_stdout = stdout_text or ""
        last_stderr = stderr_text or ""

        if exit_code == 0:
            write_runtime("INFO", "Desktop renderer exited cleanly.")
            return 0

        if attempt < MAX_RECOVERY_ATTEMPTS:
            write_runtime("WARN", f"Recovery attempt {attempt}/{MAX_RECOVERY_ATTEMPTS}")
            time.sleep(RECOVERY_COOLDOWN_SECONDS)

    details_parts = [
        f"Renderer crashed after {MAX_RECOVERY_ATTEMPTS} attempts.",
        "",
        "--- STDOUT ---",
        last_stdout.strip(),
        "",
        "--- STDERR ---",
        last_stderr.strip(),
    ]
    details = "\n".join(details_parts).strip()

    crash_path = write_crash_log(
        f"Renderer crashed after {MAX_RECOVERY_ATTEMPTS} attempts",
        details,
    )
    launch_diagnostics(crash_path, "Restart attempts exhausted. Diagnostics console standing by.")
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        os.makedirs(CRASH_DIR, exist_ok=True)
        fallback_path = os.path.join(CRASH_DIR, f"launcher_failure_{now_stamp()}.txt")
        with open(fallback_path, "w", encoding="utf-8") as f:
            import traceback
            f.write(traceback.format_exc())
        write_runtime("ERROR", f"Launcher fatal error: {e}")
        raise
