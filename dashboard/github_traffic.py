#!/usr/bin/env python3
"""github_traffic.py - DRESA (Oct 2026): GitHub statistics for the public AI-educators repository,
for the educator usage dashboard. Install on the educator VM as
/home/ubuntu/idsa-dify-project/scripts/github_traffic.py; cron runs it daily (19:00 UTC).

What it does, in plain English:
  1. Reads a read-only GitHub token from .github_traffic.key (mode 600; never printed).
  2. Asks GitHub for the repository's page views and clones (per day, last 14 days), the top
     10 sites that sent visitors, the top 10 pages viewed, stars, forks, watchers and the number
     of "We're using this" issues (label "adopter").
  3. GitHub forgets anything older than 14 days, so each day's figures are merged into
     dashboard/github_history.json, which keeps growing: that is our long-term record.
  4. Writes dashboard/github_traffic.json, which build_dashboard.sh bakes into the page.
  No token yet -> writes {} and the dashboard simply hides the GitHub card.
"""
import datetime, json, os, urllib.request

BASE = "/home/ubuntu/idsa-dify-project"
KEY = BASE + "/.github_traffic.key"
HIST = BASE + "/dashboard/github_history.json"
OUT = BASE + "/dashboard/github_traffic.json"
REPO = "au-research/AI-educators"

def save(path, data):
    tmp = path + ".tmp"
    json.dump(data, open(tmp, "w"), indent=1)
    os.replace(tmp, path)          # swap in whole, so the dashboard never reads a half-written file

if not os.path.exists(KEY):
    save(OUT, {}); print("no token yet: GitHub card hidden"); raise SystemExit

TOKEN = open(KEY).read().strip()

def get(path):
    req = urllib.request.Request("https://api.github.com/repos/" + REPO + path, headers={
        "Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "ardc-educator-dashboard"})
    return json.load(urllib.request.urlopen(req, timeout=30))

try:
    repo = get("")
    views = get("/traffic/views")
    clones = get("/traffic/clones")
    refs = get("/traffic/popular/referrers")
    paths = get("/traffic/popular/paths")
    adopters = get("/issues?state=all&labels=adopter&per_page=100")
except Exception as e:  # keep yesterday's card, but say why it is stale
    old = json.load(open(OUT)) if os.path.exists(OUT) else {}
    old["error"] = "GitHub refused or was unreachable: %s (check the token in .github_traffic.key)" % type(e).__name__
    save(OUT, old); print(old["error"]); raise SystemExit(1)

# Merge today's 14-day window into the long-term history (newer figures replace older ones for a day)
hist = json.load(open(HIST)) if os.path.exists(HIST) else {"views": {}, "clones": {}}
for kind, data in (("views", views), ("clones", clones)):
    for d in data.get(kind, []):
        hist[kind][d["timestamp"][:10]] = {"count": d["count"], "uniques": d["uniques"]}
save(HIST, hist)

def total(kind, key, since=None):
    return sum(v[key] for day, v in hist[kind].items() if since is None or day >= since)

since14 = (datetime.date.today() - datetime.timedelta(days=13)).isoformat()
all_days = sorted(set(hist["views"]) | set(hist["clones"]))
out = {
    "updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "tracking_since": all_days[0] if all_days else None,
    "views_14": views.get("count", 0), "visitors_14": views.get("uniques", 0),
    "clones_14": clones.get("count", 0), "cloners_14": clones.get("uniques", 0),
    "views_all": total("views", "count"), "clones_all": total("clones", "count"),
    "stars": repo.get("stargazers_count", 0), "forks": repo.get("forks_count", 0),
    "watchers": repo.get("subscribers_count", 0), "adopters": len(adopters),
    "daily": [{"d": d, "v": hist["views"].get(d, {}).get("count", 0), "c": hist["clones"].get(d, {}).get("count", 0)}
              for d in all_days[-60:]],
    "referrers": [{"name": r["referrer"], "count": r["count"], "uniques": r["uniques"]} for r in refs],
    "paths": [{"path": p["path"], "title": p["title"], "count": p["count"], "uniques": p["uniques"]} for p in paths],
}
save(OUT, out)
print("GitHub: %d views (%d visitors) and %d clones (%d cloners) in 14 days; history since %s"
      % (out["views_14"], out["visitors_14"], out["clones_14"], out["cloners_14"], out["tracking_since"]))
