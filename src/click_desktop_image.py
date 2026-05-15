from __future__ import annotations

import argparse
import os
from pathlib import Path


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Open the target desktop image.")
    parser.add_argument(
        "--image",
        help="Optional image path. Defaults to the known image name on the desktop.",
    )
    args = parser.parse_args()

    image_path = find_desktop_image(args.image)
    os.startfile(image_path)
    print(f"Opened: {image_path}")


if __name__ == "__main__":
    main()
