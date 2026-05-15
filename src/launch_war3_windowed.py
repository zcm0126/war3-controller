"""
Launch Warcraft III in windowed mode.

Usage:
    python src/launch_war3_windowed.py
    python src/launch_war3_windowed.py --exe "D:\\Games\\Warcraft III\\Warcraft III.exe"

If auto-detection does not find the game, set WAR3_EXE to the full executable
path or pass --exe explicitly.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path
from typing import Iterable, Optional


WINDOWED_ARGS = ("-window",)


def _existing_file(path: Optional[str]) -> Optional[Path]:
    if not path:
        return None

    candidate = Path(path).expanduser()
    if candidate.is_file():
        return candidate

    return None


def _registry_install_paths() -> Iterable[Path]:
    if os.name != "nt":
        return ()

    try:
        import winreg
    except ImportError:
        return ()

    registry_locations = (
        (winreg.HKEY_CURRENT_USER, r"Software\Blizzard Entertainment\Warcraft III"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Blizzard Entertainment\Warcraft III"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Blizzard Entertainment\Warcraft III"),
    )
    value_names = ("Program Path", "InstallPath", "Install Path")

    paths = []
    for hive, key_name in registry_locations:
        try:
            with winreg.OpenKey(hive, key_name) as key:
                for value_name in value_names:
                    try:
                        value, _ = winreg.QueryValueEx(key, value_name)
                    except OSError:
                        continue

                    path = Path(str(value)).expanduser()
                    paths.append(path if path.suffix else path / "Warcraft III.exe")
        except OSError:
            continue

    return paths


def _common_install_paths() -> Iterable[Path]:
    roots = (
        os.environ.get("PROGRAMFILES(X86)"),
        os.environ.get("PROGRAMFILES"),
        r"C:\Program Files (x86)",
        r"C:\Program Files",
    )
    relative_paths = (
        r"Warcraft III\_retail_\x86_64\Warcraft III.exe",
        r"Warcraft III\Warcraft III.exe",
        r"Warcraft III\war3.exe",
        r"Warcraft III\Frozen Throne.exe",
    )

    for root in roots:
        if not root:
            continue
        for relative_path in relative_paths:
            yield Path(root) / relative_path


def find_war3_exe(explicit_path: Optional[str]) -> Optional[Path]:
    search_paths = []
    search_paths.append(_existing_file(explicit_path))
    search_paths.append(_existing_file(os.environ.get("WAR3_EXE")))
    search_paths.extend(_registry_install_paths())
    search_paths.extend(_common_install_paths())

    for path in search_paths:
        if path and path.is_file():
            return path

    return None


def launch_windowed(exe_path: Path) -> subprocess.Popen:
    return subprocess.Popen(
        [str(exe_path), *WINDOWED_ARGS],
        cwd=str(exe_path.parent),
        close_fds=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch Warcraft III in windowed mode.")
    parser.add_argument("--exe", help="Full path to Warcraft III.exe, war3.exe, or Frozen Throne.exe.")
    args = parser.parse_args()

    exe_path = find_war3_exe(args.exe)
    if not exe_path:
        print("Warcraft III executable was not found.")
        print(r'Run again with: python src\launch_war3_windowed.py --exe "D:\Path\To\Warcraft III.exe"')
        print(r'Or set: $env:WAR3_EXE="D:\Path\To\Warcraft III.exe"')
        return 1

    launch_windowed(exe_path)
    print(f"Launched windowed: {exe_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
