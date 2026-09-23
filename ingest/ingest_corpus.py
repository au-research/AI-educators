#!/usr/bin/env python3
# ============================================================================
# ingest_corpus.py - creates ONE consolidated Dify knowledge base and ingests
# every markdown file in a directory, one document at a time.
#
# Usage:
#   DIFY_KB_KEY=dataset-xxxx [DIFY_API_BASE=http://localhost/v1] \
#   [DIFY_EMBEDDING_MODEL=... DIFY_EMBEDDING_PROVIDER=...] \
#     python3 ingest_corpus.py "<dataset name>" <src_dir> <dataset_id_file>
#
# Hard-won rules encoded here (from operating the ARDC Dataspace Educator):
#   - PIN the embedding model when creating datasets via API: if your app
#     attaches datasets with mixed embedding models, Dify demands a rerank
#     model. Set DIFY_EMBEDDING_MODEL/_PROVIDER to match your other datasets.
#   - Completion-gated: each document must finish indexing before the next
#     starts (Dify's queue otherwise bursts per-minute embedding quotas).
#   - Size-adaptive cool-downs between documents, and one automatic
#     delete-and-recreate retry after a 4-minute rest if a document errors
#     (error-state documents reject update-by-file).
#   - Resumable: reruns skip documents already indexed successfully.
#   - Keep files under ~60KB (split at headings) on free embedding tiers.
# ============================================================================
import json, os, sys, time, urllib.request, urllib.parse

NAME, SRC, DATASET_ID_FILE = sys.argv[1], sys.argv[2], sys.argv[3]
KEY = os.environ["DIFY_KB_KEY"]
BASE = os.environ.get("DIFY_API_BASE", "http://localhost/v1")
EMB = {}
if os.environ.get("DIFY_EMBEDDING_MODEL"):
    EMB = {"embedding_model": os.environ["DIFY_EMBEDDING_MODEL"],
           "embedding_model_provider": os.environ.get("DIFY_EMBEDDING_PROVIDER", "")}

def req(path, method="GET", data=None, ctype=None):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Bearer " + KEY)
    if ctype: r.add_header("Content-Type", ctype)
    with urllib.request.urlopen(r, timeout=300) as resp:
        body = resp.read().decode()
        return json.loads(body) if body.strip() else {}

def create_by_file(ds, filepath):
    boundary = "----ic" + str(int(time.time() * 1000))
    name = os.path.basename(filepath)
    rules = {"indexing_technique": "high_quality", "process_rule": {"mode": "automatic"}}
    body = ("--" + boundary + "\r\nContent-Disposition: form-data; name=\"data\"\r\nContent-Type: application/json\r\n\r\n" + json.dumps(rules) + "\r\n").encode()
    body += ("--" + boundary + "\r\nContent-Disposition: form-data; name=\"file\"; filename=\"" + name + "\"\r\nContent-Type: text/markdown\r\n\r\n").encode()
    body += open(filepath, "rb").read() + ("\r\n--" + boundary + "--\r\n").encode()
    return req("/datasets/" + ds + "/document/create-by-file", "POST", body, "multipart/form-data; boundary=" + boundary)

def doc_status(ds, doc_name):
    page = 1
    while page <= 3:
        docs = req("/datasets/" + ds + "/documents?limit=100&page=%d&keyword=%s" % (page, urllib.parse.quote(doc_name)))
        for d in docs.get("data", []):
            if d["name"] == doc_name:
                return d.get("display_status") or d.get("indexing_status"), d["id"]
        if not docs.get("has_more"): break
        page += 1
    return None, None

def wait_done(ds, doc_name, timeout_s=420):
    waited = 0
    while waited < timeout_s:
        time.sleep(20); waited += 20
        st, did = doc_status(ds, doc_name)
        if st in ("available", "completed"): return "available", did
        if st == "error": return "error", did
    return "timeout", None

def main():
    ds_id = None
    if os.path.exists(DATASET_ID_FILE):
        ds_id = open(DATASET_ID_FILE).read().strip() or None
    if not ds_id:
        payload = {"name": NAME, "permission": "only_me", "indexing_technique": "high_quality"}
        payload.update(EMB)
        ds = req("/datasets", "POST", json.dumps(payload).encode(), "application/json")
        ds_id = ds["id"]
        open(DATASET_ID_FILE, "w").write(ds_id)
        print("created dataset %s: %s embedding: %s" % (NAME, ds_id, ds.get("embedding_model")), flush=True)
    else:
        print("using existing dataset %s: %s" % (NAME, ds_id), flush=True)

    have = set()
    page = 1
    while True:
        docs = req("/datasets/" + ds_id + "/documents?limit=100&page=%d" % page)
        for d in docs.get("data", []):
            st = d.get("display_status") or d.get("indexing_status")
            if st in ("available", "completed"):
                have.add(d["name"])
        if not docs.get("has_more"): break
        page += 1
    files = sorted(f for f in os.listdir(SRC) if f.endswith(".md"))
    todo = [f for f in files if f not in have]
    print("%s: %d files; already ingested: %d; to do: %d" % (NAME, len(files), len(have), len(todo)), flush=True)

    done = failed = 0
    for idx, f in enumerate(todo):
        path = os.path.join(SRC, f)
        size = os.path.getsize(path)
        ok = False
        for attempt in (1, 2):
            try:
                create_by_file(ds_id, path)
                result, did = wait_done(ds_id, f)
                if result == "available":
                    ok = True; break
                print("attempt %d %s for %s" % (attempt, result.upper(), f), flush=True)
                if did:
                    try: req("/datasets/" + ds_id + "/documents/" + did, "DELETE")
                    except Exception: pass
                if attempt == 1:
                    time.sleep(240)
            except Exception as e:
                print("attempt %d EXCEPTION for %s: %s" % (attempt, f, str(e)[:120]), flush=True)
                if attempt == 1:
                    time.sleep(240)
        if ok:
            done += 1
            print("OK %s (%d/%d)" % (f, done, len(todo)), flush=True)
        else:
            failed += 1
            print("GAVE-UP %s" % f, flush=True)
        if idx < len(todo) - 1:
            cool = 30 if size < 15000 else (90 if size < 35000 else 180)
            time.sleep(cool)
    print("RESULT %s: %d ingested, %d failed of %d" % (NAME, done, failed, len(todo)), flush=True)

if __name__ == "__main__":
    main()
