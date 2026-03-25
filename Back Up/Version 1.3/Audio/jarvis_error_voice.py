import sys
import os
import asyncio
import tempfile
import subprocess
import shutil
import math

import edge_tts
from PySide6.QtCore import QUrl, QEventLoop, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QApplication


DEFAULT_TEXT = "Uhm..... Sir, I seem to be malfunctioning."


def hidden_subprocess_kwargs():
    kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
    }

    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0
        kwargs["startupinfo"] = startupinfo
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    return kwargs


class JarvisErrorSpeaker:
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

        # 25% louder than the previous 0.25
        self.audio_output.setVolume(0.40)

    async def speak(self, text: str):
        fd, source_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        processed_path = None

        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice="en-GB-RyanNeural",
                rate="-10%",
                pitch="-2Hz",
            )
            await communicate.save(source_path)

            if not os.path.exists(source_path):
                print(f"ERROR: audio file was not created: {source_path}")
                return 1

            processed_path = apply_error_effect(source_path)
            playback_path = processed_path if processed_path and os.path.exists(processed_path) else source_path

            loop = QEventLoop()

            def on_media_status_changed(status):
                if status == QMediaPlayer.MediaStatus.EndOfMedia:
                    loop.quit()
                elif status == QMediaPlayer.MediaStatus.InvalidMedia:
                    print("ERROR: Invalid media")
                    loop.quit()

            self.player.mediaStatusChanged.connect(on_media_status_changed)
            self.player.setSource(QUrl.fromLocalFile(playback_path))
            self.player.play()

            QTimer.singleShot(20000, loop.quit)
            loop.exec()

            self.player.stop()
            self.player.setSource(QUrl())
            return 0

        finally:
            for path in (source_path, processed_path):
                if path:
                    try:
                        os.remove(path)
                    except Exception:
                        pass


def parse_args(argv):
    text = None
    i = 1
    positional = []

    while i < len(argv):
        arg = argv[i]

        if arg == "--text" and i + 1 < len(argv):
            text = argv[i + 1]
            i += 2
            continue

        if arg in {"--mode", "--effect"} and i + 1 < len(argv):
            i += 2
            continue

        positional.append(arg)
        i += 1

    if text is None:
        text = os.environ.get("JARVIS_VOICE_TEXT")

    if not text and positional:
        text = " ".join(positional)

    return normalize_line(text or DEFAULT_TEXT)


def normalize_line(text: str) -> str:
    lowered = text.strip().lower()
    mapping = {
        "um..... sir, i seem to be malfunctioning.": "Uhm..... Sir, I seem to be malfunctioning.",
        "uhm..... sir, i seem to be malfunctioning.": "Uhm..... Sir, I seem to be malfunctioning.",
        "attempting restart.": "Attempting restart.",
        "restart failed.": "Restart failed.",
        "attempting fix.": "Attempting fix.",
        "fix failed.": "Fix failed.",
    }
    return mapping.get(lowered, text)


def ffmpeg_exe():
    return shutil.which("ffmpeg") or ""


def ffprobe_exe():
    return shutil.which("ffprobe") or ""


def get_duration_seconds(path):
    exe = ffprobe_exe()
    if not exe:
        return 0.0

    cmd = [
        exe,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path,
    ]

    result = subprocess.run(cmd, **hidden_subprocess_kwargs())

    if result.returncode != 0:
        return 0.0

    try:
        return max(0.0, float(result.stdout.strip()))
    except Exception:
        return 0.0


def seg_filter(level):
    if level == "extreme":
        return (
            "highpass=f=90,"
            "lowpass=f=2850,"
            "acrusher=bits=5:mix=0.95:mode=lin,"
            "chorus=0.86:0.94:80|62:0.42|0.28:0.90|0.94:0.34|0.44,"
            "tremolo=f=15:d=0.68,"
            "aphaser=in_gain=0.68:out_gain=0.88:delay=2.8:decay=0.64:speed=1.8,"
            "aecho=0.88:0.72:28:0.40,"
            "volume=2.25"
        )

    return (
        "highpass=f=100,"
        "lowpass=f=3200,"
        "acrusher=bits=7:mix=0.78:mode=lin,"
        "chorus=0.80:0.90:70|52:0.36|0.24:0.86|0.92:0.30|0.36,"
        "tremolo=f=12:d=0.54,"
        "aphaser=in_gain=0.60:out_gain=0.80:delay=2.2:decay=0.55:speed=1.4,"
        "aecho=0.82:0.55:18:0.30,"
        "acompressor=threshold=-18dB:ratio=2.8:attack=5:release=65,"
        "volume=2.05"
    )


def build_chunked_filter_complex(duration, segment_len=0.40, fade_len=0.050):
    pattern = ["raised","extreme","raised","raised","extreme","raised","extreme","raised"]
    segments = []
    count = max(1, math.ceil(duration / segment_len))

    for i in range(count):
        start = i * segment_len
        end = min(duration, (i + 1) * segment_len)
        if end <= start:
            continue

        level = pattern[i % len(pattern)]
        label = f"s{i}"
        seg_dur = end - start
        chain = seg_filter(level)

        actual_fade = min(fade_len, max(0.010, seg_dur / 4))
        fade_out_start = max(0.0, seg_dur - actual_fade)

        segments.append(
            f"[0:a]atrim=start={start:.3f}:end={end:.3f},"
            f"asetpts=PTS-STARTPTS,{chain},"
            f"afade=t=in:st=0:d={actual_fade:.3f},"
            f"afade=t=out:st={fade_out_start:.3f}:d={actual_fade:.3f}"
            f"[{label}]"
        )

    concat_inputs = "".join(f"[s{i}]" for i in range(len(segments)))
    return ";".join(segments + [f"{concat_inputs}concat=n={len(segments)}:v=0:a=1[outa]"])


def apply_error_effect(source_path):
    exe = ffmpeg_exe()
    if not exe:
        return None

    duration = get_duration_seconds(source_path)
    if duration <= 0:
        return None

    fd, out_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)

    filter_complex = build_chunked_filter_complex(duration)

    cmd = [
        exe,
        "-y",
        "-i", source_path,
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        out_path,
    ]

    result = subprocess.run(cmd, **hidden_subprocess_kwargs())

    if result.returncode != 0 or not os.path.exists(out_path):
        return None

    return out_path


if __name__ == "__main__":
    text = parse_args(sys.argv)
    speaker = JarvisErrorSpeaker()
    sys.exit(asyncio.run(speaker.speak(text)))
