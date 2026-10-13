#!/usr/bin/env python3
"""The trees strangers sent that Hidde has not looked at, as one local page.

Hidde, 2026-10-13: "every daily digest give me the trees to inspect". The
digest (reader_trees_to_inspect() in daily_digest.py) lists them, but DATA.md
is public, so the photographs and the readers' own words cannot go there. This
builds out/inspect/index.html (out/ is never committed) with, per tree: the
photograph, everything the reader filled in, their note word for word, our
verdict and the live page when there is one. A session runs it whenever he asks
for the digest and shows him the page.

    python3 scripts/inspect_readers.py           # build the page, print its path
    python3 scripts/inspect_readers.py --all     # also the ones he already answered

The selection is the digest's: not our own accounts (data/our-accounts.json),
no answer from him yet in data/judgements.json. He answers with
`python3 scripts/judgement.py --feedback <id> "..."`, and the tree leaves both.
"""
import base64
import glob
import html
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.chdir(ROOT)

import inbox  # noqa: E402
import ours  # noqa: E402

KEY = inbox.load_key()
if KEY:
    os.environ["SUPABASE_SERVICE_KEY"] = KEY
import sightings_inbox as si  # noqa: E402

si.KEY = KEY
OUT = os.path.join("out", "inspect")


def tree_url(slug, name):
    s = re.sub(r"^the\s+", "", (name or "").strip(), flags=re.I)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return "https://ancienttrees.app/%s/%s" % (slug, s)


def live_index():
    live = {}
    for path in sorted(glob.glob("data/cities/*.json")):
        try:
            d = json.load(open(path, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        slug = os.path.basename(path)[:-5]
        for t in d.get("trees", []):
            for p in [t.get("photo") or {}] + list(t.get("photos") or []):
                if p.get("sighting_id"):
                    live[str(p["sighting_id"]).lower()] = (slug, t)
    return live


def owners(live=None):
    """sighting id -> the account that sent it. The judgement rows do not carry
    it (their photo field is often a local path), so ask the database, and fall
    back to what the repository knows: a live photograph's contributor and the
    leads file."""
    out = {}
    if KEY:
        try:
            for r in si.supa("/rest/v1/sightings?select=id,user_id") or []:
                out[str(r.get("id")).lower()] = r.get("user_id")
        except Exception:
            pass
    for sid, (_slug, t) in (live or live_index()).items():
        for p in [t.get("photo") or {}] + list(t.get("photos") or []):
            if str(p.get("sighting_id", "")).lower() == sid and p.get("contributor_user_id"):
                out.setdefault(sid, p["contributor_user_id"])
    try:
        for l in json.load(open("data/leads/_sightings.json", encoding="utf-8")).get("leads", []):
            if l.get("sighting_id") and l.get("user_id"):
                out.setdefault(str(l["sighting_id"]).lower(), l["user_id"])
    except (OSError, ValueError, AttributeError):
        pass
    return out


def selection(include_answered=False, live=None):
    """[(sighting id, judgement row, how many sightings of the same tree)],
    strangers only, one row per tree, newest first as judgements.json keeps them.
    A sighting whose sender cannot be established is shown: missing a reader's
    tree is the failure this exists for, showing one of ours is only noise."""
    live = live if live is not None else live_index()
    who = owners(live)
    rows = json.load(open("data/judgements.json", encoding="utf-8")).get("judgements", [])
    by_tree, out = {}, []
    for j in rows:
        sid = str(j.get("id", "")).split(":", 1)[-1].lower()
        uid = who.get(sid) or (str(j.get("photo") or "").split("/")[0]
                               if re.match(r"^[0-9a-f-]{36}/", str(j.get("photo") or "")) else None)
        if uid and ours.is_ours(uid):
            continue
        if j.get("hidde") and not include_answered:
            continue
        if "SUPERSEDED" in (j.get("reason") or ""):
            continue
        key = ((j.get("tree") or sid).lower(), (j.get("city") or "").lower())
        if key in by_tree:
            by_tree[key][2] += 1
            continue
        by_tree[key] = [sid, j, 1]
        out.append(by_tree[key])
    return [tuple(x) for x in out]


def reader_row(sid):
    if not KEY:
        return {}
    try:
        rows = si.supa("/rest/v1/sightings?id=eq.%s&select=*" % sid) or []
    except Exception:
        rows = []
    return rows[0] if rows else {}


def main():
    include = "--all" in sys.argv
    live = live_index()
    picks = selection(include, live)
    os.makedirs(OUT, exist_ok=True)
    cards = []
    for sid, j, _n in picks:
        r = reader_row(sid)
        photo = r.get("photo") or j.get("photo")
        img = ""
        if photo and KEY:
            dest = os.path.join(OUT, sid + ".jpg")
            if si.fetch_photo(photo, dest):
                # Inline, so the page works opened anywhere (a preview pane,
                # a file sent to his phone) without the files beside it.
                with open(dest, "rb") as fh:
                    img = '<img src="data:image/jpeg;base64,%s" alt="">' % base64.b64encode(fh.read()).decode()
        hit = live.get(sid)
        page = ('<a href="%s">%s, live</a>' % (tree_url(hit[0], hit[1].get("name")), html.escape(hit[1].get("id")))
                if hit else "not on the site")
        facts = [
            ("Name they gave", r.get("name") or j.get("tree")),
            ("Species they gave", r.get("species") or j.get("species")),
            ("Age they gave", r.get("age")),
            ("Girth", "%s cm" % r.get("girth_cm") if r.get("girth_cm") else None),
            ("Trunk in hugs", r.get("girth_hugs")),
            ("Photo taken (UTC)", r.get("taken_at")),
            ("Where they stood", "%s, %s" % (r.get("lat"), r.get("lng")) if r.get("lat") else None),
            ("Our verdict", "%s: %s" % (j.get("verdict") or "open", j.get("reason") or "")),
            ("Your answer", j.get("hidde")),
            ("Page", None),
        ]
        dl = "".join("<dt>%s</dt><dd>%s</dd>" % (k, html.escape(str(v))) for k, v in facts if v)
        dl += "<dt>Page</dt><dd>%s</dd>" % page
        note = r.get("note") or j.get("reader_note") or ""
        cards.append(
            '<section><h2>%s</h2><p class="id">%s</p>%s<dl>%s</dl>%s</section>' % (
                html.escape(r.get("name") or j.get("tree") or "unnamed"), html.escape(j.get("id")), img, dl,
                '<h3>Their note, word for word</h3><pre>%s</pre>' % html.escape(note) if note.strip()
                else "<p><em>No note.</em></p>"))
    body = "\n".join(cards) or "<p>Nothing waiting: every tree a stranger sent has your answer.</p>"
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Trees to inspect</title>
<style>
body{font:16px/1.5 -apple-system,system-ui,sans-serif;max-width:760px;margin:0 auto;padding:16px;background:#faf8f3;color:#222}
section{background:#fff;border-radius:12px;padding:16px;margin:0 0 24px;box-shadow:0 1px 3px #0002}
img{width:100%%;border-radius:8px}h2{margin:0}.id{color:#888;font-size:13px;margin:2px 0 12px}
dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px}dt{color:#666}dd{margin:0}
pre{white-space:pre-wrap;font:inherit;background:#f3f0e8;padding:12px;border-radius:8px}
</style></head><body><h1>Trees readers sent, to inspect (%d)</h1>
<p>Answer one with <code>python3 scripts/judgement.py --feedback &lt;id&gt; "..."</code>.</p>
%s</body></html>""" % (len(picks), body)
    path = os.path.join(OUT, "index.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("%d tree(s) to inspect: %s" % (len(picks), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
