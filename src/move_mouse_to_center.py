from __future__ import annotations

import argparse

import pyautogui
import pydirectinput


def main() -> None:
    parser = argparse.ArgumentParser(description="Print mouse position and move it to screen center.")
    parser.add_argument("--duration", type=float, default=0.2)
    args = parser.parse_args()

    x, y = pyautogui.position()
    width, height = pyautogui.size()
    center_x = width // 2
    center_y = height // 2

    print(f"Current mouse position: ({x}, {y})")
    print(f"Screen center: ({center_x}, {center_y})")

    pydirectinput.moveTo(center_x, center_y, duration=args.duration)
    print(f"Moved mouse to: ({center_x}, {center_y})")


if __name__ == "__main__":
    main()
