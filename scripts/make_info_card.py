"""
Hand-authored neofetch-style info card, Linux terminal look (no macOS
traffic-light buttons). Each row fades/slides in on a short stagger.
Writes info-card.svg.

Edit the fields below to change the content.
"""
import os

FIELDS = [
    ("os", "Linux + Windows Server"),
    ("role", "Full Stack Developer | Security-focused"),
    ("location", "Maringá, PR - Brasil"),
    ("stack", "Node.js, React, PostgreSQL, Docker, Nginx"),
    ("focus", "Dev + Infra + Observabilidade"),
]

HIGHLIGHTS = [
    "Full Stack development & backend systems",
    "APIs REST, integrações & automação",
    "Infrastructure, Docker & observability",
    "Cybersecurity: Linux hardening, CrowdSec & security practices",
]

WIDTH = 490
LINE_H = 22
PAD_X = 20
PAD_TOP = 24

BG = "#0d1117"
BORDER = "#30363d"
TITLE_BAR = "#161b22"
ACCENT = "#58a6ff"
KEY_COLOR = "#7ee787"
VAL_COLOR = "#c9d1d9"
DIM = "#8b949e"


def row(label, value, y, delay):
    return f"""
<g class="line" style="animation-delay: {delay:.2f}s">
  <text x="{PAD_X}" y="{y}" fill="{KEY_COLOR}" font-size="13" font-weight="600">{label}</text>
  <text x="{PAD_X + 100}" y="{y}" fill="{VAL_COLOR}" font-size="13">{value}</text>
</g>"""


def render():
    rows = list(FIELDS)
    for i, h in enumerate(HIGHLIGHTS):
        rows.append(("highlights" if i == 0 else "", h))

    height = PAD_TOP + 40 + len(rows) * LINE_H + 24

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {WIDTH} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">'
    )
    parts.append(
        f"""
<style>
  .line {{ opacity: 0; transform-box: fill-box; transform-origin: left; animation: fadeSlide 0.35s ease-out forwards; }}
  @keyframes fadeSlide {{
    from {{ opacity: 0; transform: translateX(-8px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
  }}
</style>
"""
    )

    parts.append(
        f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{height-1}" rx="6" '
        f'fill="{BG}" stroke="{BORDER}"/>'
    )
    parts.append(f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="28" rx="6" fill="{TITLE_BAR}"/>')
    parts.append(f'<rect x="0.5" y="20" width="{WIDTH-1}" height="9" fill="{TITLE_BAR}"/>')
    parts.append(f'<line x1="0.5" y1="28.5" x2="{WIDTH-0.5}" y2="28.5" stroke="{BORDER}"/>')
    parts.append(
        f'<text x="14" y="18" fill="{DIM}" font-size="11">eric@linux</text>'
    )
    cx = WIDTH - 20
    parts.append(f'<text x="{cx}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x2715;</text>')
    parts.append(f'<text x="{cx-20}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x25a1;</text>')
    parts.append(f'<text x="{cx-40}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x2212;</text>')
    parts.append(
        f'<text x="{WIDTH/2}" y="18" fill="{DIM}" font-size="11" text-anchor="middle">~ neofetch</text>'
    )

    y = PAD_TOP + 28
    parts.append(
        f'<text x="{PAD_X}" y="{y}" fill="{ACCENT}" font-size="15" font-weight="700">Eric Teixeira</text>'
    )
    y += 6
    parts.append(f'<line x1="{PAD_X}" y1="{y}" x2="{WIDTH-PAD_X}" y2="{y}" stroke="{BORDER}"/>')
    y += LINE_H

    delay = 0.1
    for label, value in rows:
        parts.append(row(label, value, y, delay))
        y += LINE_H
        delay += 0.09

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = render()
    with open("info-card.svg", "w") as f:
        f.write(svg)
    print("Wrote info-card.svg")