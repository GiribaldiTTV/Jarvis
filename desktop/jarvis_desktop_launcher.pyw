# Version 1.3.2 rev 11 launcher

import os
import sys
import time
import threading
import subprocess
import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_SCRIPT = os.path.join(ROOT_DIR, "jarvis_desktop_test.py")
LOG_DIR = os.path.join(ROOT_DIR, "logs")
CRASH_DIR = os.path.join(LOG_DIR, "crash")
STATUS_FILE = os.path.join(LOG_DIR, "diagnostics_status.txt")
DIAGNOSTICS_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_diagnostics.pyw")
VOICE_SCRIPT = os.path.join(ROOT_DIR, "Audio", "jarvis_error_voice.py")

MAX_RECOVERY_ATTEMPTS = 3
RECOVERY_COOLDOWN_SECONDS = 1.2

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CRASH_DIR, exist_ok=True)

RUNTIME_FILE = os.path.join(
    LOG_DIR,
    f"Runtime_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
)

def pythonw():
    exe = sys.executable
    alt = os.path.join(os.path.dirname(exe), "pythonw.exe")
    return alt if os.path.exists(alt) else exe

def runtime(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    with open(RUNTIME_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

def reset_status():
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write("")

def write_status(kind, msg):
    with open(STATUS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{kind}|{msg}\n")

def crash_log(message, attempts, last_code):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(CRASH_DIR, f"Crash_{ts}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("JARVIS CRASH REPORT\n")
        f.write(f"Time: {ts}\n")
        f.write(f"Python: {pythonw()}\n")
        f.write(f"Working Directory: {ROOT_DIR}\n")
        f.write(f"Renderer: {TARGET_SCRIPT}\n")
        f.write(f"Max Recovery Attempts: {MAX_RECOVERY_ATTEMPTS}\n")
        f.write(f"Attempts Used: {attempts}\n")
        f.write(f"Last Exit Code: {last_code}\n")
        f.write(f"Runtime Log: {RUNTIME_FILE}\n")
        f.write(f"Failure Reason: {message}\n")
    runtime(f"Crash log written: {path}")
    return path

def launch_diag():
    runtime("Launching diagnostics UI")
    write_status("TRACE", "Launching diagnostics UI")
    proc = subprocess.Popen([pythonw(), DIAGNOSTICS_SCRIPT])
    runtime(f"Diagnostics PID: {proc.pid}")
    return proc

def transcript_delay_for_word(index, total_words, word):
    delay = 0.24
    if total_words <= 2:
        delay = 0.29
    elif total_words >= 8:
        delay = 0.17

    punctuation_bonus = {
        ".": 0.22,
        ",": 0.10,
        ":": 0.08,
        ";": 0.08,
        "?": 0.18,
        "!": 0.18,
    }

    if index == 0:
        delay += 0.08

    last_char = word[-1] if word else ""
    delay += punctuation_bonus.get(last_char, 0.0)
    return delay

def stream_voice_text(display_text, stop_event):
    words = display_text.split()
    cumulative = ""

    for i, word in enumerate(words):
        if stop_event.is_set():
            return

        cumulative = f"{cumulative} {word}".strip()
        write_status("VOICE_SYNC", cumulative)

        end_time = time.time() + transcript_delay_for_word(i, len(words), word)
        while time.time() < end_time:
            if stop_event.is_set():
                return
            time.sleep(0.01)

def speak(spoken_text, display_text=None):
    if not os.path.exists(VOICE_SCRIPT):
        runtime(f"Voice script missing: {VOICE_SCRIPT}")
        return

    display_text = display_text or spoken_text
    runtime(f"VOICE: {spoken_text}")
    write_status("VOICE_CLEAR", "")

    stop_event = threading.Event()
    worker = threading.Thread(
        target=stream_voice_text,
        args=(display_text, stop_event),
        daemon=True,
    )
    worker.start()

    subprocess.run([pythonw(), VOICE_SCRIPT, "--text", spoken_text])

    stop_event.set()
    worker.join(timeout=0.4)
    write_status("VOICE_FINAL", display_text)

def run_renderer():
    runtime(f"Starting renderer: {TARGET_SCRIPT}")
    proc = subprocess.Popen([pythonw(), TARGET_SCRIPT])
    runtime(f"Renderer PID: {proc.pid}")
    proc.wait()
    runtime(f"Renderer exit code: {proc.returncode}")
    return proc.returncode

def main():
    reset_status()

    runtime("==== Jarvis runtime started ====")
    runtime(f"Python executable: {pythonw()}")
    runtime(f"Working directory: {ROOT_DIR}")
    runtime(f"Renderer target: {TARGET_SCRIPT}")

    diagnostics_opened = False
    recovery_voice_spoken = False
    last_code = None

    for attempt in range(1, MAX_RECOVERY_ATTEMPTS + 1):
        runtime(f"Renderer launch attempt {attempt}/{MAX_RECOVERY_ATTEMPTS}")
        write_status("TRACE", f"Renderer launch attempt {attempt}/{MAX_RECOVERY_ATTEMPTS}"); time.sleep(0.18)

        last_code = run_renderer()

        if last_code == 0:
            runtime("Renderer exited normally")
            write_status("TRACE", "Renderer exited normally")
            return 0

        runtime("Renderer exited unexpectedly")
        write_status("SUMMARY", "Desktop renderer exited unexpectedly")
        write_status("TRACE", f"Renderer exited unexpectedly with code {last_code}")

        if not diagnostics_opened:
            write_status("TRACE", "Initializing diagnostics"); time.sleep(0.18)
            write_status("TRACE", "Scanning runtime environment"); time.sleep(0.18)
            write_status("TRACE", "Checking desktop engine"); time.sleep(0.18)
            launch_diag()
            write_status("STATE", "STARTED")
            speak("Uhm..... Sir, I seem to be malfunctioning.")
            diagnostics_opened = True

        if attempt < MAX_RECOVERY_ATTEMPTS:
            runtime(f"Preparing recovery attempt {attempt}")
            write_status("STATE", "RECOVERING")
            write_status("TRACE", f"Attempting recovery ({attempt}/{MAX_RECOVERY_ATTEMPTS})")
            write_status("TRACE", f"Cooldown before next attempt: {RECOVERY_COOLDOWN_SECONDS:.1f}s")

            if not recovery_voice_spoken:
                speak("Attempting recovery.")
                recovery_voice_spoken = True

            time.sleep(RECOVERY_COOLDOWN_SECONDS)

    runtime("All recovery attempts exhausted")
    write_status("TRACE", "Recovery attempts exhausted")
    write_status("STATE", "COMPLETE")
    speak("Recovery failed.")
    speak("Shutting down.")
    crash_log("Renderer failed after maximum recovery attempts.", MAX_RECOVERY_ATTEMPTS, last_code or -1)

if __name__ == "__main__":
    main()
