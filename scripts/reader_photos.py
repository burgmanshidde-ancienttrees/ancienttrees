#!/usr/bin/env python3
"""Every photograph a stranger shared through the app, as one local page,
with whether Hidde has seen it.

Hidde, 2026-10-25: "i want to see all photos even from existing trees show me
which i missed and how do we make sure this doesnt happen in the future ...
het is echt kwalijk als ik niet weet van ambassadeurs of fotos of trees". The
inspect page (inspect_readers.py) only ever showed photographs of NEW trees;
a photograph on a tree we already had went live, or was held, without his eyes
on it. This page shows them all, the ones he has not seen first: the image,
the tree and its page, when it came, what we decided, and his answer if any.

    python3 scripts/reader_photos.py            # build the page (unseen first, then the last 30 days)
    python3 scripts/reader_photos.py --all      # every shared photograph ever
    python3 scripts/reader_photos.py --seen     # after he has looked: mark everything the page showed as seen
    python3 scripts/reader_photos.py --count    # one line: how many he has not seen (exit 0 when none)

What he has seen lives in data/photos-seen.json as sighting ids with the date,
never a person. The page goes to out/photos/ and is mirrored beside the digest
in the preview folder as photos.html, served by `preview_start {name: "inspect"}`.
"""
import datetime
import html
import json
import os
import sys

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
from inspect_readers import live_index, tree_url, PREVIEW  # noqa: E402

si.KEY = KEY
OUT = os.path.join("out", "photos")
SEEN = os.path.join("data", "photos-seen.json")
SHOWN = os.path.join("out", "photos", "shown.json")


def load_seen():
    try:
        return json.load(open(SEEN, encoding="utf-8"))
    except Exception:
        return {"_note": "Reader photographs Hidde has looked at on the photo page "
                         "(scripts/reader_photos.py --seen): sighting id -> date. No people.",
                "seen": {}}


def verdicts():
    """Our verdict per sighting id, from the processed file and the judgements."""
    out = {}
    try:
        p = json.load(open("data/sightings-processed.json", encoding="utf-8"))
        if isinstance(p, dict):
            for sid, v in p.items():
                if isinstance(v, dict):
                    out[sid] = (v.get("outcome") or v.get("verdict") or "?", v.get("reason") or v.get("note") or "")
    except Exception:
        pass
    hidde = {}
    for j in json.load(open("data/judgements.json", encoding="utf-8")).get("judgements", []):
        sid = (j.get("id") or "").split(":", 1)[-1]
        if j.get("verdict") and sid not in out:
            out[sid] = (j["verdict"], j.get("reason") or "")
        if j.get("hidde"):
            hidde[sid] = j["hidde"]
    return out, hidde


def rows():
    got = si.supa("/rest/v1/sightings?select=id,user_id,tree_id,name,species,note,photo,lat,lng,taken_at,updated_at"
                  "&shared=eq.true&photo=not.is.null&order=updated_at.desc&limit=1000") or []
    return [r for r in got if not ours.is_ours(r.get("user_id"))]


def main():
    if not KEY:
        print("reader photos: no database key on this Mac, nothing read")
        return 1
    seen = load_seen()
    if "--seen" in sys.argv:
        try:
            shown = json.load(open(SHOWN, encoding="utf-8"))
        except Exception:
            print("reader photos: build the page first; nothing marked")
            return 1
        today = datetime.date.today().isoformat()
        for sid in shown:
            seen["seen"].setdefault(sid, today)
        json.dump(seen, open(SEEN, "w", encoding="utf-8"), indent=1)
        print("reader photos: %d marked seen" % len(shown))
        return 0
    all_rows = rows()
    ours_v, hidde = verdicts()
    # A photograph he already answered on the inspect page is one he has seen.
    for sid in hidde:
        seen["seen"].setdefault(sid, "answered on the inspect page")
    unseen = [r for r in all_rows if r["id"] not in seen["seen"]]
    if "--count" in sys.argv:
        print("reader photos: %d not seen by Hidde" % len(unseen))
        return 0 if not unseen else 1
    since = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    rest = [r for r in all_rows if r["id"] in seen["seen"]
            and ("--all" in sys.argv or (r.get("updated_at") or "") >= since)]
    live = live_index()
    os.makedirs(OUT, exist_ok=True)

    def card(r):
        sid = r["id"]
        img = ""
        dest = os.path.join(OUT, sid + ".jpg")
        if os.path.exists(dest) or si.fetch_photo(r["photo"], dest):
            img = '<img src="%s.jpg" alt="" loading="lazy">' % sid
        hit = live.get(sid)
        page = ('<a href="%s">%s</a>' % (tree_url(hit[0], hit[1].get("name")), html.escape(hit[1].get("name") or ""))
                if hit else "not on any page")
        v = ours_v.get(sid)
        facts = [("Tagged to", "%s (%s)" % (r.get("name") or "-", r.get("tree_id") or "no tree")),
                 ("Sent", (r.get("updated_at") or "")[:16].replace("T", " ")),
                 ("Where they stood", "%.5f, %.5f" % (r["lat"], r["lng"]) if r.get("lat") is not None else None),
                 ("Our verdict", "%s: %s" % v if v else "none yet"),
                 ("Your answer", hidde.get(sid)),
                 ("Seen by you", seen["seen"].get(sid) or "not yet")]
        dl = "".join("<dt>%s</dt><dd>%s</dd>" % (k, html.escape(str(x))) for k, x in facts if x)
        dl += "<dt>On the site</dt><dd>%s</dd>" % page
        note = (r.get("note") or "").strip()
        return '<section class="%s">%s<dl>%s</dl>%s</section>' % (
            "new" if sid not in seen["seen"] else "", img, dl,
            "<h3>Their note, word for word</h3><pre>%s</pre>" % html.escape(note) if note else "")

    body = ("<h2>Not seen by you yet (%d)</h2>" % len(unseen) + ("".join(card(r) for r in unseen) or "<p>None.</p>")
            + "<h2>Seen before, last 30 days (%d)</h2>" % len(rest) + "".join(card(r) for r in rest))
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Readers' photographs</title>
<style>
body{font:16px/1.5 -apple-system,system-ui,sans-serif;max-width:760px;margin:0 auto;padding:16px;background:#faf8f3;color:#222}
section{background:#fff;border-radius:12px;padding:16px;margin:0 0 24px;box-shadow:0 1px 3px #0002}
section.new{border-left:6px solid #3d6b35}
img{display:block;max-width:100%%;max-height:70vh;margin:0 auto 12px;border-radius:8px}
dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px}dt{color:#666}dd{margin:0}
pre{white-space:pre-wrap;font:inherit;background:#f3f0e8;padding:12px;border-radius:8px}
</style></head><body><h1>Readers' photographs</h1>
<p>Every photograph a stranger shared through the app, on new trees and on trees we already had. Once you have looked, the session marks them seen.</p>
%s</body></html>""" % body
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    json.dump([r["id"] for r in unseen + rest], open(SHOWN, "w", encoding="utf-8"))
    if os.path.isdir(PREVIEW):
        import shutil
        shutil.copy(os.path.join(OUT, "index.html"), os.path.join(PREVIEW, "photos.html"))
        for r in unseen + rest:
            src = os.path.join(OUT, r["id"] + ".jpg")
            if os.path.exists(src):
                shutil.copy(src, PREVIEW)
    print("reader photos: %d not seen by Hidde, %d seen in the last 30 days; page out/photos/index.html, "
          "preview http://127.0.0.1:8766/photos.html" % (len(unseen), len(rest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
