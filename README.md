# ARDC AI Educators

Everything needed to stand up your own copies of the ARDC's five AI learning assistants
for the dataspaces domain:

- **Dataspace Educator** - open Q&A grounded in curated sources, with role-aware
  answers and source-validation banners on every response.
  Live at https://dresa.org.au/dataspaces_ed/
- **Dataspaces 101 Coach** - a guided five-lesson module with Socratic "resistance"
  (it asks before it tells) and a fixed, deterministically scored knowledge check.
  Live at https://dresa.org.au/dataspaces_101/
- **Getting-Started, Governance and Technical Coaches** - three further guided modules
  on the same coaching pattern, covering first steps, rulebook-building (Sitra-style),
  and technical implementation (RAM, connectors, ODRL, DSP, the Testbed).
  Live under https://dresa.org.au/educators

Both are configuration for [Dify](https://github.com/langgenius/dify) (open-source LLM
platform) plus a rebuildable knowledge corpus - there is no bespoke ML here, and that
is the point: one part-time non-developer operates the live instances.

## What is in this repository

| Path | Contents |
|---|---|
| `apps/` | Dify app definitions (DSL YAML) for both assistants - import into any Dify instance |
| `corpus/` | `sources.json` (the corpus control file: 44 sources with licence notes) and the polite scraper that rebuilds the corpus from public URLs |
| `ingest/` | Quota-paced, completion-gated ingestion script for loading the corpus into Dify knowledge bases |
| `web/` | The static wrapper pages used on dresa.org.au (adapt URLs and branding) |
| `question_bank/` | Reserve multiple-choice questions for the 101 module |
| `docs/SETUP.md` | Step-by-step stand-up guide |
| `dashboard/` | The usage dashboard and feedback-loop kit: stats extraction, page template, weekly golden checks, optional nightly analysis |

## What is deliberately NOT here

- **The corpus content itself.** You rebuild it from the public sources listed in
  `sources.json` - each with its licence recorded - rather than receiving our copies.
  A few entries are summaries or pointers where licences require it; respect those choices.
- **Model API keys, dataset IDs, and anything instance-specific.**
- Internal ARDC materials (original slide decks, planning documents).

## Licence and attribution

Code and configuration: Apache-2.0 (see LICENSE). Documentation: CC BY 4.0.
The corpus sources carry their own licences, recorded per entry in `sources.json`
and in every generated file's provenance header - attribution requirements
(largely CC BY 4.0) apply to what you rebuild.

If you deploy your own instance, please: use your own branding and contact address
(the prompts reference skills@ardc.edu.au - change this), keep the source-attribution
footer pattern, and check each source's licence still permits your use.

## Provenance

Built by the ARDC skills team (Rob Clemens) with AI-assisted development, September 2026.
Questions: skills@ardc.edu.au
