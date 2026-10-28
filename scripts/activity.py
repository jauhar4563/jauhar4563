"""Generate cards from GitHub's account-level contribution calendar only.

No repository names, contribution descriptions, or company statistics are requested.
"""
import argparse
import json
import os
import re
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from design import BG, PANEL, CYAN, VIOLET, TEXT, MUTED, ROOT, svg, text

QUERY = """query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def window(today):
    return today - timedelta(days=364), today


def fetch_calendar(login, now):
    start, end = window(now.date())
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is required; no data was written")
    payload = {"query": QUERY, "variables": {
        "login": login, "from": f"{start}T00:00:00Z", "to": now.isoformat().replace("+00:00", "Z")}}
    request = urllib.request.Request("https://api.github.com/graphql", data=json.dumps(payload).encode(), headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-calendar-cards"})
    with urllib.request.urlopen(request, timeout=45) as response:
        result = json.load(response)
    if result.get("errors") or not result.get("data", {}).get("user"):
        raise ValueError("GitHub did not return a complete contribution calendar")
    return result["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def summarize(calendar, today):
    start, end = window(today)
    days = {}
    for week in calendar["weeks"]:
        for item in week["contributionDays"]:
            day = date.fromisoformat(item["date"])
            if start <= day <= end:
                count = item["contributionCount"]
                if isinstance(count, bool) or not isinstance(count, int) or count < 0 or day in days:
                    raise ValueError("Invalid or duplicate contribution day")
                days[day] = count
    expected = {start + timedelta(days=i) for i in range(365)}
    if set(days) != expected:
        raise ValueError("Incomplete calendar; refusing to replace previous cards")
    total = sum(days.values())
    if total != calendar["totalContributions"]:
        raise ValueError("Contribution total does not match daily counts")
    longest = run = 0
    for day in sorted(days):
        run = run + 1 if days[day] > 0 else 0
        longest = max(longest, run)
    cursor = end if days[end] else end - timedelta(days=1)
    current = 0
    while cursor in days and days[cursor] > 0:
        current += 1
        cursor -= timedelta(days=1)
    return {"total": total, "active_days": sum(c > 0 for c in days.values()), "current": current,
            "longest": longest, "start": start.isoformat(), "end": end.isoformat()}


def card(title, eyebrow, summary, metrics, note, mobile=False):
    if mobile:
        body = f'<rect x="1" y="1" width="418" height="278" rx="18" fill="{PANEL}" stroke="#30363D"/>'
        body += '<path d="M20 1H400" stroke="url(#accent)" stroke-width="2"/>'
        body += text(24,32,eyebrow,14,CYAN,600) + text(24,68,title,23,TEXT,700)
        body += text(24,99,summary['start']+' — '+summary['end'],18,MUTED)
        for i, (value, label, color) in enumerate(metrics):
            x = 24+i*193
            body += text(x,166,f'{value:,}',40,color,700)
            body += text(x,197,label.replace(' · days',''),16,TEXT)
        body += text(24,239,'365 UTC days · Details below',17,MUTED)
        body += text(24,262,'Daily refresh / Public contribution calendar',14,MUTED)
        return svg(420,280,title + '. ' + '. '.join(f'{label}: {value}' for value,label,_ in metrics),body)
    body = f'''<rect x="1" y="1" width="718" height="238" rx="18" fill="{PANEL}" stroke="#30363D"/>
<path d="M20 1H700" stroke="url(#accent)" stroke-width="2"/>
{text(28,32,eyebrow,14,CYAN,600)}{text(28,68,title,28,TEXT,700)}
{text(28,96,summary['start']+' — '+summary['end']+' · UTC',18,MUTED)}'''
    for i, (value, label, color) in enumerate(metrics):
        x = 28 + i * 350
        body += text(x, 158, f"{value:,}", 44, color, 700) + text(x, 188, label, 20, TEXT)
    body += text(28, 222, note, 16, MUTED)
    return svg(720, 240, f"{title}. " + ". ".join(f"{label}: {value}" for value, label, _ in metrics) + f". Period: {summary['start']} to {summary['end']} UTC.", body)


def build(output, calendar, today):
    summary = summarize(calendar, today)
    output.mkdir(parents=True, exist_ok=True)
    files = {
        "contributions.svg": card("Showing up. Building things.", "GITHUB / CONTRIBUTIONS", summary,
                                  [(summary["total"], "Contributions", CYAN), (summary["active_days"], "Active days", VIOLET)],
                                  "365-day window · Includes publicly shared private activity"),
        "streak.svg": card("Consistency, one day at a time.", "GITHUB / STREAK", summary,
                           [(summary["current"], "Current streak · days", CYAN), (summary["longest"], "Longest in window · days", VIOLET)],
                           "Current streak allows today to be unfinished · Capped to window"),
    }
    files['contributions-mobile.svg'] = card('Showing up. Building things.', 'GITHUB / CONTRIBUTIONS', summary,
        [(summary['total'], 'Contributions', CYAN), (summary['active_days'], 'Active days', VIOLET)], '', mobile=True)
    files['streak-mobile.svg'] = card('Consistency, one day at a time.', 'GITHUB / STREAK', summary,
        [(summary['current'], 'Current streak · days', CYAN), (summary['longest'], 'Longest in window · days', VIOLET)], '', mobile=True)
    for name, content in files.items():
        (output / name).write_text(content + "\n", encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    accessible = (f"\n**{summary['total']:,} contributions · {summary['active_days']} active days**<br>\n"
                  f"Current streak: **{summary['current']} {'day' if summary['current'] == 1 else 'days'}** · "
                  f"Longest in this window: **{summary['longest']} {'day' if summary['longest'] == 1 else 'days'}**<br>\n"
                  f"Period: {summary['start']} to {summary['end']} (UTC; refreshed daily).\n")
    updated, matches = re.subn(r"(?<=<!-- ACTIVITY:START -->).*?(?=<!-- ACTIVITY:END -->)", accessible, readme, flags=re.S)
    if matches != 1:
        raise ValueError("README must contain exactly one activity marker pair")
    (output / "README.md").write_text(updated, encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input", type=Path, help="Previously fetched GraphQL response for local verification")
    parser.add_argument("--login", default="jauhar4563")
    parser.add_argument("--today", type=date.fromisoformat)
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    today = args.today or now.date()
    if args.today and not args.input:
        parser.error("--today is only valid with --input")
    if args.input:
        raw = json.loads(args.input.read_text())
        calendar = raw["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    else:
        calendar = fetch_calendar(args.login, now)
    print(json.dumps(build(args.output, calendar, today)))


if __name__ == "__main__":
    main()
