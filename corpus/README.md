# Corpus recipe

- sources.json: 44 sources with method (full/crawl/raw_md/summary/pointer) and licence per entry. Review before scraping: summary/pointer entries reflect licence limits - keep them.
- wiki_scrape.py: rebuilds markdown/ from the sources. Polite by design (robots-aware, 2s delay, honest UA, provenance headers, heading-splits >52KB).
- Output lands in markdown/ next to this file; REVIEW EVERY FILE before ingesting it into a public-facing assistant.
