import argparse
import datetime
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import desktop.orin_desktop_main as runtime_main


def _build_logger(log_path: Path):
    log_path.parent.mkdir(parents=True, exist_ok=True)

    def _log(event: str) -> None:
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"[{ts}] {event}\n")
            handle.flush()

    return _log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-log", required=True)
    args = parser.parse_args(argv)

    runtime_log_path = Path(args.runtime_log).resolve()
    runtime_main.RUNTIME_LOG_FILE = str(runtime_log_path)
    runtime_main.runtime_milestone = _build_logger(runtime_log_path)
    sys.argv = [
        "desktop/orin_desktop_main.py",
        "--runtime-log",
        str(runtime_log_path),
    ]
    return runtime_main.main()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
