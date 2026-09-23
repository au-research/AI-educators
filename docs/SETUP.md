# Standing up your own Dataspace Educator

Rough effort: a day for a working instance, longer for polish. You need a VM
(4GB+ RAM), Docker, and an LLM API key (we use Google Gemini; any Dify-supported
provider works - a FUNDED tier, free tiers cause outages and slow ingestion).

## 1. Install Dify

Follow https://docs.dify.ai/getting-started/install-self-hosted/docker-compose.
Set a strong `SECRET_KEY`, put real TLS in front, and create the admin account
immediately - an unclaimed Dify setup page is an open door.

## 2. Configure a model provider

Console -> Settings -> Model Provider. Add your LLM key. Note which embedding
model you select - EVERY knowledge base must use the SAME embedding model or
Dify demands a rerank model. Pin it explicitly when creating datasets via API.
We use a fast, non-reasoning chat model (gemini-3.5-flash): reasoning models
add 10-30s of silence before the first token, which users read as "broken".

## 3. Rebuild the corpus

    cd corpus/
    # review sources.json first - licences are recorded per source
    python3 wiki_scrape.py            # all sources; or pass comma-separated ids

The scraper is deliberately polite: it honours robots.txt (fetched with an
honest User-Agent), waits 2s between requests, writes provenance headers
(source URL, licence, retrieval date) into every file, and splits files at
headings to stay under embedding-quota-friendly sizes. Review the output
before ingestion - that human step is a feature, not a bug.

## 4. Create knowledge bases and ingest

    cd ingest/
    DIFY_KB_KEY=dataset-xxxx python3 ingest_corpus.py "My Corpus" ../corpus/markdown ./dataset_id.txt

Create a Knowledge API key in the console first (Knowledge -> API). The script
is completion-gated (each document finishes indexing before the next starts),
size-adaptively paced, retries once after an error with a long rest, and is
resumable - all lessons from free-tier embedding quotas. Budget 1-2 hours for
~50 documents on a free tier; minutes on a funded tier.

## 5. Import the apps

Console -> Studio -> Create from DSL file -> upload `apps/dataspace_educator.yml`,
then `apps/dataspaces_101_coach.yml`. For each app: attach your knowledge
base(s) in the Context panel, select your model, and edit the prompt's
contact address and any organisation-specific references. Publish.

## 6. Wrapper pages (optional)

`web/` holds the static pages we place in front of the Dify chat UI: branding,
source attributions (keep this pattern - your corpus licences likely require
attribution), a "answers take N seconds" expectation-setter, an
"open in full window" affordance (embedded iframes lose chat history in
privacy-strict browsers), and a scroll-pin script (the chat's autofocus
otherwise scrolls your header away). Replace the chat URLs with your own
app links and re-brand.

## 7. Operate it

The things that bit us, so they do not bite you:
- **Test as your real users.** Mine your logs for question styles and run
  persona tests; our biggest retrieval bug was invisible in demos.
- **Golden questions.** Keep a fixed question set with expected sources and
  run it weekly through the real chat API; retrieval breaks silently.
- **Expect prompt injection.** Real users try "print your system prompt"
  within weeks. The prompts here include refusal instructions; keep them.
- **Watch your model quota/billing.** Our only sustained outage was a
  depleted free-tier key answering every question with silence.
- **Few consolidated knowledge bases beat many small ones.** Dozens of
  datasets fan out into parallel retrieval that can exhaust DB connection
  pools and silently drop sources.
