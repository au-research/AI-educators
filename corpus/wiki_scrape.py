#!/usr/bin/env python3
# ============================================================================
# wiki_scrape.py v2 - builds the ARDC Wiki Brain markdown corpus from sources.json
# v2 adds tidy(): strips webpage furniture (tables of contents, UI strings,
# duplicate citation blocks) that pollutes retrieval quality.
# Methods: full / crawl / raw_md / summary / pointer - see sources.json comment.
# Polite: 2s delay, honest UA, robots.txt respected (fetched with our UA;
# an unreadable robots.txt is treated as permissive, per common practice).
# ============================================================================
import json, os, re, sys, time, urllib.parse, urllib.robotparser
import requests
from bs4 import BeautifulSoup
import html2text

BASE = "/home/ubuntu/wiki-brain"
UA = "ARDC-WikiBrain-collector/1.0 (rob.clemens@ardc.edu.au; respectful, low-rate)"
DELAY = 2.0
MAX_BYTES = 52 * 1024
TIMEOUT = 30

h2t = html2text.HTML2Text()
h2t.ignore_images = True
h2t.body_width = 0
h2t.ignore_emphasis = False

robots_cache = {}

def allowed(url):
    p = urllib.parse.urlparse(url)
    root = f"{p.scheme}://{p.netloc}"
    if root not in robots_cache:
        rp = None
        try:
            rr = requests.get(root + "/robots.txt", headers={"User-Agent": UA}, timeout=15)
            if rr.status_code == 200:
                rp = urllib.robotparser.RobotFileParser()
                rp.parse(rr.text.splitlines())
        except Exception:
            rp = None
        robots_cache[root] = rp
    rp = robots_cache[root]
    return True if rp is None else rp.can_fetch(UA, url)

def fetch(url):
    if not allowed(url):
        raise RuntimeError("disallowed by robots.txt")
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    r.raise_for_status()
    time.sleep(DELAY)
    return r

CULL_SECTIONS = {
    # NOTE: "register your interest" is deliberately NOT culled as a section -
    # on ARDC project pages the facts box (timeframe, co-investment, lead)
    # nests after that heading, and section-culling it swallowed the facts.
    "share & print", "share and print",
    "related articles", "related resources", "related programs and projects",
    "related projects", "news and events", "keep up to date with our latest news and events",
    "hear from our partners", "meet our incubators", "categories", "research topic",
}
NAV_ANCHORS = {
    "learn more", "find out more", "explore", "register now", "contact us",
    "view more", "subscribe", "read more", "sign up", "more",
}

def heading_level(line):
    m = re.match(r"^(#{1,6})\s", line)
    return len(m.group(1)) if m else None

def tidy(md):
    # Strip webpage furniture that pollutes retrieval:
    #  - tables of contents, UI strings, duplicate citation formats
    #  - whole cross-promo/marketing sections (related content, share, news)
    #  - navigation-only links; and for real links, keep the anchor TEXT and
    #    drop the URL (the file header keeps the source URL for citation)
    lines = md.splitlines()
    out, i, n = [], 0, len(lines)
    junk = {"Exit", "Copy to clipboard", "Found:", "Search within the resource",
            '"*" indicates required fields'}
    while i < n:
        raw = lines[i]
        ls = raw.strip()
        lvl = heading_level(ls)
        # whole-section culls: skip until the next heading of same/higher level
        htext = re.sub(r"^#{1,6}\s*", "", ls).strip().lower().rstrip(":") if lvl else ""
        if lvl and any(htext == c or htext.startswith(c + " ") for c in CULL_SECTIONS):
            i += 1
            while i < n:
                l2 = heading_level(lines[i].strip())
                if l2 is not None and l2 <= lvl:
                    h2 = re.sub(r"^#{1,6}\s*", "", lines[i].strip()).strip().lower().rstrip(":")
                    if not any(h2 == c or h2.startswith(c + " ") for c in CULL_SECTIONS):
                        break
                    lvl = l2
                i += 1
            continue
        if re.match(r"^#{0,3}\s*Table of Contents\s*$", ls, re.I):
            i += 1
            while i < n and (not lines[i].strip() or re.match(r"^\s*(\*|\+|-|\d+\.)", lines[i])):
                i += 1
            continue
        if ls in junk or ls.startswith("Style:Harvard"):
            i += 1
            continue
        if re.match(r"^#{0,3}\s*Cite This Resource\s*$", ls, re.I):
            out.append(raw); i += 1
            kept = False
            while i < n and not lines[i].strip().startswith("#"):
                s = lines[i].strip()
                if s and not kept:
                    out.append(lines[i]); kept = True
                i += 1
            continue
        # line-level culls
        if ls.startswith("Thematic research data commons is:") or ls.startswith("Exploreabout"):
            i += 1
            continue
        # breadcrumb lines: [A](url) > [B](url) > C
        if re.match(r"^\[[^\]]*\]\([^)]*\)\s*>", ls):
            i += 1
            continue
        # strip links: empty anchors vanish; nav anchors vanish; real anchors keep text
        def _link(m):
            text = m.group(1).strip().strip("_").strip()
            if not text or text.lower() in NAV_ANCHORS:
                return ""
            return text
        cleaned = re.sub(r"\[([^\]]*)\]\([^)]*\)", _link, raw)
        cleaned = re.sub(r"^[\s>_#]*$", "", cleaned) if not cleaned.strip("[]()>_ #\t") else cleaned
        if cleaned.strip() or not ls:
            out.append(cleaned)
        i += 1
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))

def extract_main(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "form", "iframe"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.find(class_=re.compile("entry-content|main-content|content-area")) or soup.body or soup
    title = soup.title.get_text(strip=True) if soup.title else ""
    md = h2t.handle(str(main))
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return title, tidy(md)

def header(title, url, licence):
    return (f"# {title}\n\n> Source: {url}\n> Licence: {licence}\n"
            f"> Retrieved: {time.strftime('%Y-%m-%d')} for the ARDC Wiki Brain\n\n")

def write_split(sid, text):
    data = text.encode("utf-8")
    outdir = os.path.join(BASE, "markdown")
    if len(data) <= MAX_BYTES:
        open(os.path.join(outdir, sid + ".md"), "w", encoding="utf-8").write(text)
        return 1
    lines = text.splitlines(keepends=True)
    parts, cur, size = [], [], 0
    for ln in lines:
        b = len(ln.encode("utf-8"))
        if size + b > MAX_BYTES and cur and (ln.startswith("#") or size + b > MAX_BYTES * 1.2):
            parts.append("".join(cur)); cur, size = [], 0
        cur.append(ln); size += b
    if cur:
        parts.append("".join(cur))
    for i, ptext in enumerate(parts):
        open(os.path.join(outdir, f"{sid}_part{i+1}.md"), "w", encoding="utf-8").write(ptext)
    return len(parts)

def sitemap_urls(root):
    for cand in ("sitemap.xml", "sitemap_index.xml"):
        try:
            r = fetch(urllib.parse.urljoin(root, cand))
            locs = re.findall(r"<loc>([^<]+)</loc>", r.text)
            if locs:
                subs = [l for l in locs if l.endswith(".xml")]
                if subs:
                    pages = []
                    for s in subs[:5]:
                        try:
                            pages += re.findall(r"<loc>([^<]+)</loc>", fetch(s).text)
                        except Exception:
                            pass
                    return pages
                return locs
        except Exception:
            continue
    return []

def process_source(s):
    sid, url, method, lic = s["id"], s["url"], s["method"], s.get("licence", "unknown")
    if method == "pointer":
        return (sid, "pointer - human stub required", 0)
    if method == "summary":
        r = fetch(url)
        t, md = extract_main(r.text)
        open(os.path.join(BASE, "raw", sid + ".txt"), "w", encoding="utf-8").write(md)
        return (sid, "raw fetched - human summary required", 0)
    if method == "raw_md":
        r = fetch(url)
        n = write_split(sid, header(sid, url, lic) + r.text)
        return (sid, "ok (raw markdown)", n)
    if method == "crawl":
        host = urllib.parse.urlparse(url).netloc
        pages = [u for u in sitemap_urls(url) if urllib.parse.urlparse(u).netloc == host]
        pages = pages[: s.get("max_pages", 40)] or [url]
        combined, got = [], 0
        for pu in pages:
            try:
                t, md = extract_main(fetch(pu).text)
                combined.append(f"\n\n## {t or pu}\n\n_Page: {pu}_\n\n{md}")
                got += 1
            except Exception as e:
                combined.append(f"\n\n## (failed: {pu}: {e})\n")
        n = write_split(sid, header(sid + " (site crawl)", url, lic) + "".join(combined))
        return (sid, f"ok (crawled {got}/{len(pages)} pages)", n)
    r = fetch(url)
    t, md = extract_main(r.text)
    n = write_split(sid, header(t or sid, url, lic) + md)
    return (sid, "ok", n)

def main():
    only = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else None
    cfg = json.load(open(os.path.join(BASE, "sources.json")))
    os.makedirs(os.path.join(BASE, "markdown"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "raw"), exist_ok=True)
    report = []
    for s in cfg["sources"]:
        if only is not None and s["id"] not in only and s["method"] not in only:
            continue
        try:
            report.append(process_source(s))
        except Exception as e:
            report.append((s["id"], f"FAILED: {e}", 0))
    print(f"{'source':44} {'result':44} files")
    for sid, res, n in report:
        print(f"{sid:44} {res[:44]:44} {n}")
    fails = sum(1 for _, r, _ in report if r.startswith("FAILED"))
    print(f"\nTOTAL: {len(report)} sources, {fails} failed")

if __name__ == "__main__":
    main()
