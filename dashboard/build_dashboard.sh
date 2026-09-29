#!/usr/bin/env bash
# build_dashboard.sh v3 - regenerates the usage dashboard HTML:
#   __DATA_JSON__    <- fresh stats from educator_stats.sh
#   __SUMMARY_JSON__ <- dashboard/weekly_summary.json if present (written
#                       weekly by the scheduled task), else {} (section hidden)
#   __GOLDEN_JSON__  <- dashboard/golden_results.json if present (written
#                       weekly by golden_check.py), else {} (tile hidden)
set -euo pipefail
BASE=/home/ubuntu/idsa-dify-project
bash "$BASE/scripts/educator_stats.sh" > /tmp/stats.json
python3 - << "PY"
import json, os
stats = json.load(open("/tmp/stats.json"))
def load(p):
    if os.path.exists(p):
        try: return json.load(open(p))
        except Exception: return {}
    return {}
summary = load("/home/ubuntu/idsa-dify-project/dashboard/weekly_summary.json")
golden = load("/home/ubuntu/idsa-dify-project/dashboard/golden_results.json")
jev = load("/home/ubuntu/idsa-dify-project/dashboard/jev_analysis.json")
tpl = open("/home/ubuntu/idsa-dify-project/dashboard/template.html", encoding="utf-8").read()
assert "__DATA_JSON__" in tpl and "__SUMMARY_JSON__" in tpl and "__GOLDEN_JSON__" in tpl and "__JEV_JSON__" in tpl, "placeholder missing from template"
out = tpl.replace("__DATA_JSON__", json.dumps(stats, separators=(",", ":")))
out = out.replace("__SUMMARY_JSON__", json.dumps(summary, separators=(",", ":")))
out = out.replace("__GOLDEN_JSON__", json.dumps(golden, separators=(",", ":")))
out = out.replace("__JEV_JSON__", json.dumps(jev, separators=(",", ":")))
open("/home/ubuntu/idsa-dify-project/dashboard/dashboard_built.html", "w", encoding="utf-8").write(out)
print("dashboard_built.html:", len(out), "bytes; users:", stats["unique_users"], "questions:", stats["total_questions"],
      "summary:", "yes" if summary.get("text") else "none",
      "golden:", ("%s/%s" % (golden.get("passed"), golden.get("total"))) if golden.get("total") else "none")
PY
rm -f /tmp/stats.json
