"""
Convert a prepped grayscale photo into a self-typing, monochrome ASCII
SVG. Each row wipes in left-to-right, staggered top to bottom (SMIL
clip-path animation), then freezes — no looping.

Usage: python scripts/make_ascii_svg.py [source-prepped.png]
Writes: avi-ascii.svg  (rename as you like, e.g. eric-ascii.svg)
"""
import sys

from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense); leading space = blank

COLS = 100
FONT_W = 6.1
FONT_H = 11
FILL = "#8b949e"  # single light-gray fill, no per-char rainbow


def image_to_ascii(path, cols=COLS):
    img = Image.open(path).convert("L")
    w, h = img.size
    # characters are taller than wide, so compress rows to keep aspect ratio
    aspect_correction = 0.55
    rows = int(h / w * cols * aspect_correction)
    img = img.resize((cols, rows))
    pixels = list(img.getdata())

    ramp_len = len(RAMP)
    chars = []
    for i, p in enumerate(pixels):
        # bright pixel (255, near-white bg) -> low index (space, sparse)
        # dark pixel (0, subject shadow)    -> high index (@, dense)
        idx = int((255 - p) / 255 * (ramp_len - 1))
        chars.append(RAMP[idx])

    grid = [chars[r * cols:(r + 1) * cols] for r in range(rows)]
    return grid


def escape(c):
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(c, c)


def render(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    width = cols * FONT_W
    height = rows * FONT_H

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {width:.0f} {height:.0f}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">'
    )

    row_delay = 0.045
    for r, row_chars in enumerate(grid):
        # collapse leading/trailing blank runs isn't necessary; keep grid simple
        line = "".join(escape(c) for c in row_chars)
        y = (r + 1) * FONT_H - 2
        clip_id = f"clip{r}"
        delay = r * row_delay

        parts.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="0" y="{r*FONT_H}" width="0" height="{FONT_H}">'
            f'<animate attributeName="width" from="0" to="{width:.0f}" '
            f'begin="{delay:.3f}s" dur="0.5s" fill="freeze" calcMode="spline" '
            f'keySplines="0.2 0 0.2 1" />'
            f'</rect></clipPath>'
        )
        parts.append(
            f'<text x="0" y="{y:.1f}" fill="{FILL}" font-size="{FONT_H-1}" '
            f'clip-path="url(#{clip_id})" xml:space="preserve">{line}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    grid = image_to_ascii(path)
    svg = render(grid)
    with open("avi-ascii.svg", "w") as f:
        f.write(svg)
    print(f"Wrote avi-ascii.svg ({len(grid)} rows x {len(grid[0])} cols)")
