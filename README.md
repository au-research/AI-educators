# ARDC AI Educators

Everything needed to stand up your own copies of the ARDC's AI learning assistants:
five for the dataspaces domain and four for FAIR data (beta).

### Dataspaces


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

### FAIR data (beta, October 2026)

- **ARDC FAIR Educator** - open Q&A about making research data and software Findable,
  Accessible, Interoperable and Reusable, pitched to the user's role and FAIR maturity level
  (FAIR - Getting started, Practising, Leading), with source-validation banners.
  Live at https://dresa.org.au/fair_ed/
- **FAIR - Getting started, Practising and Leading Coaches** - guided modules that ask the
  learner's role, field and experience, show seven topics with suggested competency targets
  (which the learner can adjust), coach each topic with examples from the learner's own field,
  run a 12-question knowledge check chosen from a bank of 18 by the learner's gap, and end with
  a personal next-steps plan. Live at https://dresa.org.au/fair_start/,
  https://dresa.org.au/fair_practising/ and https://dresa.org.au/fair_leading/

The FAIR tools cover the CARE Principles only in brief, by design: a separate resource on
Indigenous data will be developed and vetted with Indigenous communities. The FAIR corpus
(open-licence sources and compiled concept pages) is still under expert review and will be
published here once that review is complete; the FAIR app files therefore list no knowledge
bases.

Both are configuration for [Dify](https://github.com/langgenius/dify) (open-source LLM
platform) plus a rebuildable knowledge corpus - there is no bespoke ML here, and that
is the point: one part-time non-developer operates the live instances.

## What is in this repository

| Path | Contents |
|---|---|
| `apps/` | Dify app definitions (DSL YAML) for all nine assistants (`dataspace*` and `fair_*`) - import into any Dify instance |
| `corpus/` | `sources.json` (the corpus control file: 44 sources with licence notes) and the polite scraper that rebuilds the corpus from public URLs |
| `ingest/` | Quota-paced, completion-gated ingestion script for loading the corpus into Dify knowledge bases |
| `web/` | The static wrapper pages used on dresa.org.au for all nine (adapt URLs and branding) |
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
(the prompts reference rob.clemens@ardc.edu.au - change this), keep the source-attribution
footer pattern, and check each source's licence still permits your use.

If you redistribute the code or configuration, the Apache-2.0 licence asks you to include
the [NOTICE](NOTICE) file's attribution with it.

## How to acknowledge or cite

If you use or adapt these educators, please acknowledge the ARDC, for example:

> This work builds on the ARDC AI Educators (ARDC skills team, Australian Research Data
> Commons), https://github.com/au-research/AI-educators. The ARDC is enabled by the
> Australian Government's National Collaborative Research Infrastructure Strategy (NCRIS).

In a chat page you build from `web/`, a footer line such as "Based on the ARDC AI Educators"
with a link to this repository is enough. For papers and reports, use the **Cite this
repository** button on GitHub (from [CITATION.cff](CITATION.cff)).

## Using this? Tell us

We would love to hear how you are using or adapting the educators: it helps us show impact
and decide what to improve. Open a ["We're using this" issue](../../issues/new?template=using-this.yml)
(one minute, all optional) or email rob.clemens@ardc.edu.au.

## Provenance

Built by the ARDC skills team (Rob Clemens) with AI-assisted development, September 2026.
Questions: rob.clemens@ardc.edu.au
