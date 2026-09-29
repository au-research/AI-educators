# The educator usage dashboard - and the feedback loop behind it

A single self-contained HTML page, rebuilt daily, that shows how the AI educators
are actually being used - and, more importantly, powers the maintenance loop that
keeps them healthy. This folder contains everything needed to build your own.

## What it shows

- **Headline tiles**: unique users, questions asked, answer rate, returning users,
  average response time, failed answers, user feedback (thumbs), and a
  **retrieval-health score** from automated weekly checks.
- **Per-educator activity**: one row per app (we run five), so new modules'
  uptake is visible from day one.
- **Charts**: daily activity, new-vs-returning users by week.
- **Most-used knowledge sources**: which corpus documents actually earn their
  keep - a direct guide to curation effort.
- **Recent questions** (privacy-redacted) with an unanswered-only filter -
  reading real questions is the single highest-value maintenance habit.
- **Failure tracking**: every unanswered question, split into user-abandoned vs
  API errors. Our only major outage (a depleted free-tier model key) was
  invisible until this existed; it cannot recur silently now.
- Optional extras we run: a weekly AI-written summary of question themes, and a
  nightly classifier pass that flags injection attempts and answers pitched
  wrongly for the user's level.

## The feedback loop (the actual point)

The dashboard is not reporting for its own sake; it drives a cycle:

1. **Observe** - real questions, failures, and flagged responses surface daily.
2. **Triage** - a flagged answer is either fine (honest limits), a prompt gap,
   or a corpus gap.
3. **Fix** - prompt rules are edited, or a reviewed document is added to the
   knowledge base (never auto-ingested: a human reviews everything).
4. **Lock it in** - the fix becomes a **golden question**: a fixed test with an
   expected source, run automatically every week through the real chat
   pipeline. Regressions show up as a red tile, not a user complaint.

In practice this makes the whole maintenance burden roughly an hour a month
plus whatever content you choose to write.

## Privacy by design

- Emails and phone-shaped numbers are redacted **server-side, at extraction** -
  personal details never reach the page.
- Internal test traffic is excluded from every statistic.
- The page carries data baked in at build time: sharing the page shares only
  what you built into it, and rebuilding controls what that is.

## How it works (pipeline)

```
[platform database] --educator_stats.sh--> stats JSON --+
[golden_check.py weekly] --> golden_results.json -------+--build_dashboard.sh--> dashboard.html
[jev_analysis.py nightly, optional] --> jev JSON -------+
```

- `educator_stats.sh` - one SQL query against the Dify database producing all
  statistics as JSON, redaction included. Adapt the app IDs at the top and the
  test-user exclusion to your instance.
- `template.html` - the page, with `__DATA_JSON__` / `__SUMMARY_JSON__` /
  `__GOLDEN_JSON__` / `__JEV_JSON__` placeholders. Plain HTML + vanilla JS,
  no build tooling.
- `build_dashboard.sh` - injects the JSONs into the template. Run it from cron
  daily.
- `golden_check.py` - the weekly retrieval + behaviour checks: fixed questions
  with expected source documents, plus behavioural probes (does the coach still
  refuse to hand over answers? does anything leak under an injection attempt?).
- `jev_analysis.py` - optional nightly classification (we use TypeSafe's Jev)
  for probe detection, topic mix, and answer-quality flags, with email alerts.

## Hosting your copy

The built page is **fully self-contained** - host it on any static web server,
intranet page or document platform. We publish ours as a Claude artifact for
easy access control; the only features that depend on that hosting are the
optional "ask AI about this data" buttons, which you can simply remove.

## Requirements

A Dify-based deployment (or any platform whose message log you can query -
the SQL is the only Dify-specific part), somewhere to run two cron jobs, and
a static place to put an HTML file. That's all.

Questions: skills@ardc.edu.au
