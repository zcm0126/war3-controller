from __future__ import annotations

import argparse
import time

import pydirectinput

from double_click_position import double_click
from find_image_position import find_desktop_image, locate_image


def main() -> None:
    parser = argparse.ArgumentParser(description="Find the image icon on screen and double-click it.")
    parser.add_argument(
        "--image",
        help="Optional image path. Defaults to the known image name on the desktop.",
    )
    parser.add_argument("--confidence", type=float, default=0.5)
    parser.add_argument("--min-scale", type=float, default=0.03)
    parser.add_argument("--max-scale", type=float, default=0.2)
    parser.add_argument("--scale-step", type=float, default=0.01)
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()

    image_path = find_desktop_image(args.image)

    pydirectinput.keyDown("win")
    pydirectinput.press("d")
    pydirectinput.keyUp("win")
    time.sleep(args.delay)

    x, y, score, scale = locate_image(
        image_path=image_path,
        min_scale=args.min_scale,
        max_scale=args.max_scale,
        scale_step=args.scale_step,
    )
    if score < args.confidence:
        raise RuntimeError(
            f"Could not find icon confidently. Best score={score:.3f}, scale={scale:.3f}. "
            "Try lowering --confidence or changing --min-scale/--max-scale."
        )

    double_click(x, y)
    print(f"Double-clicked at ({x}, {y}); score={score:.3f}; scale={scale:.3f}")


if __name__ == "__main__":
    main()
