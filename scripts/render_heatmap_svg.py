"""
Draw the classic 53-week x 7-day GitHub contribution grid as an
animated SVG: boxes slide in diagonally (staggered by week), then
freeze. Reads data/contributions.json, writes contrib-heatmap.svg.
"""
import json
from datetime import datetime, timedelta

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
FLASH = "#8fe6b8"  # soft light-green highlight each cell flashes before settling on its level color

CELL = 11
GAP = 3
STEP = CELL + GAP
LEFT_PAD = 28
TOP_PAD = 20
MONTH_LABEL_H = 15

# one-shot reveal timing: diagonal cascade (columns sweep faster than rows),
# tuned so the whole ~53x7 grid finishes in ~3.5s
CELL_DUR = 0.5
COL_T = 0.045
ROW_T = 0.11


def load():
    with open("data/contributions.json") as f:
        return json.load(f)


def build_weeks(days):
    """Group flat day list into weeks (columns), each week a list of
    up to 7 days starting Sunday, matching GitHub's own layout."""
    by_date = {d["date"]: d for d in days}
    dates = sorted(by_date.keys())
    first = datetime.strptime(dates[0], "%Y-%m-%d")
    last = datetime.strptime(dates[-1], "%Y-%m-%d")

    # back up to the most recent Sunday on/before `first`
    start = first - timedelta(days=(first.weekday() + 1) % 7)

    weeks = []
    cur = start
    week = []
    while cur <= last:
        key = cur.strftime("%Y-%m-%d")
        week.append(by_date.get(key, {"date": key, "level": 0, "count": 0}))
        if len(week) == 7:
            weeks.append(week)
            week = []
        cur += timedelta(days=1)
    if week:
        while len(week) < 7:
            week.append({"date": "", "level": 0, "count": 0})
        weeks.append(week)
    return weeks


def month_labels(weeks):
    labels = []
    seen = None
    for wi, week in enumerate(weeks):
        for day in week:
            if not day["date"]:
                continue
            m = day["date"][:7]  # YYYY-MM
            if m != seen:
                seen = m
                month_name = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%b")
                labels.append((wi, month_name))
            break
    return labels


def render(data):
    weeks = build_weeks(data["days"])
    n_weeks = len(weeks)
    width = LEFT_PAD + n_weeks * STEP + 10
    height = TOP_PAD + MONTH_LABEL_H + 7 * STEP + 40

    parts = []
    parts.append(
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">'
    )
    parts.append(f'<rect width="{width}" height="{height}" fill="none"/>')

    css_lines = ["  .cell { opacity: 0; transform-box: fill-box; transform-origin: center; }"]
    for lvl, color in enumerate(PALETTE):
        css_lines.append(
            f"  @keyframes reveal{lvl} {{\n"
            f"    0%   {{ opacity: 0; transform: translate(-6px, -6px) scale(0.4); fill: {FLASH}; }}\n"
            f"    35%  {{ opacity: 1; transform: translate(0, 0) scale(1); }}\n"
            f"    100% {{ fill: {color}; }}\n"
            f"  }}"
        )
    parts.append("<style>\n" + "\n".join(css_lines) + "\n</style>")

    # month labels
    for wi, name in month_labels(weeks):
        x = LEFT_PAD + wi * STEP
        parts.append(
            f'<text x="{x}" y="{TOP_PAD}" fill="#8b949e" font-size="10">{name}</text>'
        )

    y0 = TOP_PAD + MONTH_LABEL_H

    for wi, week in enumerate(weeks):
        for di, day in enumerate(week):
            if not day["date"]:
                continue
            x = LEFT_PAD + wi * STEP
            y = y0 + di * STEP
            level = min(day["level"], len(PALETTE) - 1)
            color = PALETTE[level]
            delay = wi * COL_T + di * ROW_T
            title = f'{day["count"]} contributions on {day["date"]}' if day["count"] else f'No contributions on {day["date"]}'
            parts.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="2" ry="2" fill="{color}" '
                f'style="animation: reveal{level} {CELL_DUR}s cubic-bezier(.2,.8,.2,1) forwards; '
                f'animation-delay: {delay:.3f}s">'
                f'<title>{title}</title></rect>'
            )

    # legend
    legend_y = y0 + 7 * STEP + 18
    parts.append(f'<text x="{LEFT_PAD}" y="{legend_y}" fill="#8b949e" font-size="10">Less</text>')
    lx = LEFT_PAD + 32
    for i, color in enumerate(PALETTE):
        parts.append(
            f'<rect x="{lx + i * (CELL + 3)}" y="{legend_y - 9}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>'
        )
    parts.append(
        f'<text x="{lx + len(PALETTE) * (CELL + 3) + 4}" y="{legend_y}" fill="#8b949e" font-size="10">More</text>'
    )

    total = data["total_contributions"]
    streak = data["current_streak"]
    longest = data["longest_streak"]
    stats = f"{total:,} contributions in the last year   \u00b7   current streak {streak}d   \u00b7   longest streak {longest}d"
    parts.append(
        f'<text x="{LEFT_PAD}" y="{legend_y + 20}" fill="#c9d1d9" font-size="11">{stats}</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    data = load()
    svg = render(data)
    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Wrote contrib-heatmap.svg")
