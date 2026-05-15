from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


DEFAULT_EXE_NAMES = (
    "Warcraft III.exe",
    "Warcraft III Launcher.exe",
    "Frozen Throne.exe",
)

DEFAULT_SEARCH_DIRS = (
    Path("C:/Program Files/Warcraft III"),
    Path("C:/Program Files (x86)/Warcraft III"),
    Path("D:/Games/Warcraft III"),
    Path("D:/Warcraft III"),
)


def find_war3_exe(explicit_path: str | None = None) -> Path:
    if explicit_path:
        path = Path(explicit_path).expanduser()
        if path.exists():
            return path
        raise FileNotFoundError(f"Warcraft III executable not found: {path}")

    env_path = os.getenv("WAR3_EXE")
    if env_path:
        path = Path(env_path).expanduser()
        if path.exists():
            return path
        raise FileNotFoundError(f"WAR3_EXE points to a missing file: {path}")

    for directory in DEFAULT_SEARCH_DIRS:
        for exe_name in DEFAULT_EXE_NAMES:
            path = directory / exe_name
            if path.exists():
                return path

    raise FileNotFoundError(
        "Could not find Warcraft III executable automatically. "
        "Use --exe or set WAR3_EXE."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Warcraft III in windowed mode.")
    parser.add_argument("--exe", help="Path to Warcraft III executable.")
    parser.add_argument(
        "--args",
        nargs=argparse.REMAINDER,
        default=[],
        help="Extra arguments passed to Warcraft III.",
    )
    args = parser.parse_args()

    exe_path = find_war3_exe(args.exe)
    command = [str(exe_path), "-window", *args.args]
    subprocess.Popen(command, cwd=exe_path.parent)
    print(f"Launched Warcraft III windowed: {exe_path}")


if __name__ == "__main__":
    main()
