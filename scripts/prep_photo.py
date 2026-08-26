"""
Prep a photo for ASCII conversion:
  1. remove background (rembg) so only the subject remains
  2. boost local contrast (CLAHE) so a flat face gets real shadows/highlights
  3. composite onto pure white (maps background -> blank end of the ramp)

Usage: python scripts/prep_photo.py source-photo.jpg
Writes: source-prepped.png
"""
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove, new_session

_SESSION = new_session("u2netp")  # small (~4MB) model, avoids OOM on large default model


def prep(path_in, path_out="source-prepped.png"):
    with open(path_in, "rb") as f:
        input_bytes = f.read()

    # 1. remove background -> RGBA with transparent bg
    output_bytes = remove(input_bytes, session=_SESSION)
    rgba = Image.open(__import__("io").BytesIO(output_bytes)).convert("RGBA")

    # 2. composite onto white first (so CLAHE doesn't fight transparency)
    white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, rgba).convert("L")

    # 3. CLAHE contrast boost
    arr = np.array(composited)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    boosted = clahe.apply(arr)

    Image.fromarray(boosted).save(path_out)
    print(f"Wrote {path_out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <photo.jpg>")
        sys.exit(1)
    prep(sys.argv[1])
