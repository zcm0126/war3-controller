from __future__ import annotations

import argparse
import time

import pydirectinput


def double_click(x: int, y: int, delay: float = 0.0) -> None:
    if delay > 0:
        time.sleep(delay)
    pydirectinput.moveTo(x, y, duration=0.1)
    time.sleep(0.1)
    pydirectinput.doubleClick(x=x, y=y, interval=0.1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Double-click a screen position.")
    parser.add_argument("x", type=int, nargs="?", default=960)
    parser.add_argument("y", type=int, nargs="?", default=540)
    parser.add_argument("--delay", type=float, default=0.0)
    args = parser.parse_args()

    double_click(args.x, args.y, args.delay)
    print(f"Double-clicked at ({args.x}, {args.y})")


if __name__ == "__main__":
    main()
