#!/usr/bin/env bash
# educator_stats.sh v3 - JSON snapshot of Dataspace Educator usage (read-only).
# v3: REDACTION PASS - email addresses and long digit runs (phone-shaped
# strings) are stripped from question and answer text at extraction time,
# so personal contact details users may have typed never reach the
# dashboard. Redaction happens here, server-side, before data leaves.
# v4: test traffic (persona-test, golden-test end users) is excluded from
# every stat via the msgs CTE, so shakedown runs don't inflate usage.
docker exec docker-db_postgres-1 psql -U postgres -d dify -t -A -c "
WITH edu_apps AS (
  -- The five educator apps (v6: all five report here; test users excluded).
  SELECT * FROM (VALUES
    ('bd646117-a39d-44e2-9e3c-eeeab1657e6f'::uuid, 'Educator'),
    ('c0ac4901-1010-4a2e-b101-000000000101'::uuid, '101 Coach'),
    ('c0ac4902-1010-4a2e-b101-000000000201'::uuid, 'Getting-Started'),
    ('c0ac4903-1010-4a2e-b101-000000000301'::uuid, 'Governance'),
    ('c0ac4904-1010-4a2e-b101-000000000401'::uuid, 'Technical')
  ) AS t(app_id, app_label)
),
msgs AS (
  SELECT m.*, ea.app_label FROM messages m
  JOIN edu_apps ea ON ea.app_id = m.app_id
  WHERE (m.from_end_user_id IS NULL
     OR m.from_end_user_id NOT IN (
        SELECT id FROM end_users WHERE session_id IN ('persona-test','golden-test')))
),
fs AS (
  SELECT from_end_user_id u, min(created_at) f
  FROM msgs WHERE from_end_user_id IS NOT NULL GROUP BY 1
),
act AS (
  SELECT DISTINCT date_trunc('week', created_at)::date w, from_end_user_id u
  FROM msgs WHERE from_end_user_id IS NOT NULL
),
red AS (
  SELECT id, created_at, from_end_user_id, app_label,
    regexp_replace(regexp_replace(query,
      '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}', '[email redacted]', 'g'),
      '[0-9]{9,}', '[number redacted]', 'g') AS q_red,
    regexp_replace(regexp_replace(answer,
      '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}', '[email redacted]', 'g'),
      '[0-9]{9,}', '[number redacted]', 'g') AS a_red
  FROM msgs
)
SELECT json_build_object(
  'generated_at', to_char(now(), 'YYYY-MM-DD HH24:MI'),
  'unique_users', (SELECT count(DISTINCT from_end_user_id) FROM msgs),
  'returning_total', (SELECT count(*) FROM (
      SELECT from_end_user_id FROM msgs WHERE from_end_user_id IS NOT NULL
      GROUP BY 1 HAVING count(DISTINCT created_at::date) >= 2) t),
  'total_questions', (SELECT count(*) FROM msgs),
  'answered', (SELECT count(*) FROM msgs WHERE length(trim(answer)) > 0),
  'failed_total', (SELECT count(*) FROM msgs WHERE length(trim(answer)) = 0),
  'failed_api_total', (SELECT count(*) FROM msgs
      WHERE length(trim(answer)) = 0 AND error IS NOT NULL AND length(error) > 0),
  'first_activity', (SELECT to_char(min(created_at), 'YYYY-MM-DD') FROM msgs),
  'avg_latency_s', (SELECT round(avg(provider_response_latency)::numeric, 1)
      FROM msgs WHERE provider_response_latency > 0),
  'daily', (SELECT coalesce(json_agg(t), '[]'::json) FROM (
      SELECT to_char(created_at::date, 'YYYY-MM-DD') AS day,
             count(*) AS questions,
             count(DISTINCT from_end_user_id) AS users
      FROM msgs GROUP BY created_at::date ORDER BY created_at::date) t),
  'weekly', (SELECT coalesce(json_agg(t), '[]'::json) FROM (
      SELECT to_char(a.w, 'YYYY-MM-DD') AS week,
             count(*) FILTER (WHERE date_trunc('week', fs.f)::date = a.w)::int AS new_users,
             count(*) FILTER (WHERE date_trunc('week', fs.f)::date < a.w)::int AS returning_users
      FROM act a JOIN fs ON fs.u = a.u GROUP BY a.w ORDER BY a.w) t),
  'sources', (SELECT coalesce(json_agg(s), '[]'::json) FROM (
      SELECT d.name, sum(seg.hit_count)::int AS hits
      FROM document_segments seg JOIN documents d ON d.id = seg.document_id
      GROUP BY d.name HAVING sum(seg.hit_count) > 0
      ORDER BY sum(seg.hit_count) DESC LIMIT 12) s),
  'failures', (SELECT coalesce(json_agg(f), '[]'::json) FROM (
      SELECT to_char(created_at::date, 'YYYY-MM-DD') AS day, count(*)::int AS count,
             count(*) FILTER (WHERE error IS NOT NULL AND length(error) > 0)::int AS api_errors
      FROM msgs WHERE length(trim(answer)) = 0
      GROUP BY created_at::date ORDER BY created_at::date) f),
  'feedback_up', (SELECT count(*) FROM message_feedbacks WHERE rating = 'like'),
  'feedback_down', (SELECT count(*) FROM message_feedbacks WHERE rating = 'dislike'),
  'per_app', (SELECT coalesce(json_agg(pa), '[]'::json) FROM (
      SELECT ea.app_label AS app,
             count(m.id)::int AS questions,
             count(DISTINCT m.from_end_user_id)::int AS users,
             count(*) FILTER (WHERE length(trim(m.answer)) > 0)::int AS answered,
             round(avg(m.provider_response_latency) FILTER (WHERE m.provider_response_latency > 0)::numeric, 1) AS avg_latency_s,
             to_char(max(m.created_at), 'YYYY-MM-DD') AS last_activity
      FROM edu_apps ea LEFT JOIN msgs m ON m.app_label = ea.app_label
      GROUP BY ea.app_label ORDER BY count(m.id) DESC) pa),
  'recent_feedback', (SELECT coalesce(json_agg(fb), '[]'::json) FROM (
      SELECT mf.rating,
             to_char(mf.created_at, 'YYYY-MM-DD') AS d,
             left(regexp_replace(regexp_replace(m.query,
               '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}', '[email redacted]', 'g'),
               '[0-9]{9,}', '[number redacted]', 'g'), 160) AS q
      FROM message_feedbacks mf JOIN msgs m ON m.id = mf.message_id
      ORDER BY mf.created_at DESC LIMIT 20) fb),
  'recent', (SELECT coalesce(json_agg(r), '[]'::json) FROM (
      SELECT left(id::text, 8) AS id,
             left(q_red, 400) AS q,
             left(a_red, 700) AS a,
             to_char(created_at, 'YYYY-MM-DD') AS d,
             left(coalesce(from_end_user_id::text, 'anon'), 8) AS u,
             app_label AS app
      FROM red ORDER BY created_at DESC LIMIT 150) r)
);"
