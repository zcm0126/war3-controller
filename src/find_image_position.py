from __future__ import annotations

import argparse
import time
from pathlib import Path

import cv2
import numpy as np
import pyautogui
import pydirectinput


DEFAULT_IMAGE_STEM = "0f759659ac3f68595545e795dd861aa3"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp")


def find_desktop_image(image: str | None = None) -> Path:
    if image:
        path = Path(image).expanduser()
        if path.exists():
            return path
        raise FileNotFoundError(f"File not found: {path}")

    desktop = Path.home() / "Desktop"
    for extension in IMAGE_EXTENSIONS:
        path = desktop / f"{DEFAULT_IMAGE_STEM}{extension}"
        if path.exists():
            return path

    names = ", ".join(f"{DEFAULT_IMAGE_STEM}{ext}" for ext in IMAGE_EXTENSIONS)
    raise FileNotFoundError(f"Could not find image on desktop. Checked: {names}")


def locate_image(
    image_path: Path,
    min_scale: float,
    max_scale: float,
    scale_step: float,
) -> tuple[int, int, float, float]:
    screenshot = np.array(pyautogui.screenshot())
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    template = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise RuntimeError(f"Could not read image: {image_path}")

    best_score = -1.0
    best_center = (0, 0)
    best_scale = 0.0
    screen_h, screen_w = screenshot.shape[:2]
    template_h, template_w = template.shape[:2]

    scale = max_scale
    while scale >= min_scale:
        width = int(template_w * scale)
        height = int(template_h * scale)
        scale -= scale_step

        if width < 8 or height < 8 or width > screen_w or height > screen_h:
            continue

        resized = cv2.resize(template, (width, height), interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        _, score, _, top_left = cv2.minMaxLoc(result)

        if score > best_score:
            best_score = score
            best_scale = scale + scale_step
            best_center = (top_left[0] + width // 2, top_left[1] + height // 2)

    return best_center[0], best_center[1], best_score, best_scale


def main() -> None:
    parser = argparse.ArgumentParser(description="Find an image position on screen.")
    parser.add_argument("--image", help="Image path. Defaults to the known desktop image.")
    parser.add_argument("--confidence", type=float, default=0.5)
    parser.add_argument("--min-scale", type=float, default=0.03)
    parser.add_argument("--max-scale", type=float, default=0.2)
    parser.add_argument("--scale-step", type=float, default=0.01)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--no-show-desktop", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    image_path = find_desktop_image(args.image)
    if not args.no_show_desktop:
        pydirectinput.keyDown("win")
        # pydirectinput.press("d")
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
            f"Could not find image confidently. Best score={score:.3f}, scale={scale:.3f}. "
            f"Try: --confidence {max(score - 0.02, 0.1):.2f}"
        )

    if args.verbose:
        print(f"x={x} y={y} score={score:.3f} scale={scale:.3f}")
    else:
        print(f"{x} {y}")


if __name__ == "__main__":
    main()
