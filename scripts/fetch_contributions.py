"""
Fetch a GitHub user's public contribution calendar via the same HTML
fragment endpoint the profile page itself uses. No token required.
Writes data/contributions.json with raw days + derived stats.
"""
import json
import os
import re
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME", "EricTeixeir")
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Current GitHub markup: each day is a <td data-date data-level id=...>
    # with NO count in it directly. The count lives in a sibling
    # <tool-tip for="<td id>">N contributions on Month Day.</tool-tip>
    tooltip_by_target = {}
    for tip in soup.select("tool-tip[for]"):
        tooltip_by_target[tip.get("for")] = tip.get_text(strip=True)

    days = []
    cells = soup.select("td.ContributionCalendar-day[data-date]")

    for cell in cells:
        date = cell.get("data-date")
        level = cell.get("data-level")
        if date is None or level is None:
            continue
        count = 0
        label = tooltip_by_target.get(cell.get("id"), "")
        m = re.search(r"([\d,]+)\s+contribution", label)
        if m:
            count = int(m.group(1).replace(",", ""))
        days.append(
            {"date": date, "level": int(level), "count": count}
        )

    if not days:
        print("WARNING: no contribution cells parsed, GitHub markup may have changed", file=sys.stderr)

    total = sum(d["count"] for d in days)

    # current streak (consecutive days with count > 0, ending today)
    days_sorted = sorted(days, key=lambda d: d["date"])
    current_streak = 0
    for d in reversed(days_sorted):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    longest_streak = 0
    running = 0
    for d in days_sorted:
        if d["count"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    best_day = max(days_sorted, key=lambda d: d["count"], default=None)

    out = {
        "username": USERNAME,
        "fetched_at": datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days_sorted,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(out, f, indent=2)

    print(f"Fetched {len(days_sorted)} days, {total} total contributions for {USERNAME}")


if __name__ == "__main__":
    fetch()
