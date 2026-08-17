#!/usr/bin/env python3
"""Download a city's shortlisted photo candidates so a viewing pass can look at
them, and score each one's exposure on the way past.

Two things forced this. Wikimedia rate-limits: measured 2026-08-08, a burst of
29 image fetches took HTTP 429 after twelve, while roughly one request every
three seconds runs clean. Several viewing passes running at once cannot honour
that between them, so the fetching is done ONCE, here, serialised, and the
passes then read local files. And a pass cannot judge what it cannot render:
the rule is to look at the pixels, which means the pixels have to be on disk.

    python3 scripts/photo_fetch.py --zero --out <dir> --per-tree 3
    python3 scripts/photo_fetch.py Ferrara Zurich --out <dir>

It writes <dir>/<city-slug>/<tree_id>-<n>.jpg plus a manifest.json per city
carrying, for each file: the tree, its name and species, the candidate's title,
page url, licence, author, how far the photograph was taken from our pin, and
the photo_light verdict. It judges nothing.
"""
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import photo_gaps as GAPS  # noqa: E402
from geo import km  # noqa: E402


class SL:
    """The ranking and the photo-less-city list both live in photo_gaps.py.
    Two tools for one job is the disease this project keeps catching, so this
    is a thin adapter rather than a second opinion."""
    QUEUE = os.path.join(ROOT, "data", "photo-queue.json")

    @staticmethod
    def cities_without_photos():
        return [c["city"] for c in GAPS.cities()
                if c["photos"] == 0 and c["trees"] >= GAPS.PHOTO_FLOOR]

    @staticmethod
    def live_photo(tree):
        p = tree.get("photo") or {}
        return bool(p.get("url")) and p.get("status") != "held"

    @staticmethod
    def rank(tree, cand):
        score = GAPS.names_match(tree, cand)
        if (cand.get("source") or "") != "last-resort":
            return score
        # A last-resort candidate is here precisely BECAUSE its filename says
        # nothing ("Kontumazgarten 04.jpg"), so names_match scores it zero and
        # every one of them ties. The only evidence such a file carries is
        # where the camera stood, so that is what orders them: 20 metres from
        # the pin is a different bet from 120, and an untitled photograph taken
        # at the trunk is the likeliest thing in an otherwise empty city.
        loc = tree.get("location") or {}
        if cand.get("lat") is None or loc.get("latitude") is None:
            return score
        metres = km((loc["latitude"], loc["longitude"]),
                    (cand["lat"], cand["lng"])) * 1000
        # Capped below a single filename hit (25) on purpose: proximity is the
        # weakest evidence we accept, and an unvetted title standing at the
        # trunk must never outrank a file that actually names the tree.
        return score + max(0.0, 25.0 - metres / 5.0)

try:
    import photo_light as LIGHT
except Exception:
    LIGHT = None

UA = "AncientTreesBot/1.0 (https://ancienttrees.app; photo candidate sweep)"
PAUSE = 3.0  # seconds between fetches; below this Wikimedia starts returning 429


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


FAR_KM = 25


def _within(tree, cand):
    """False only when the candidate's OWN geotag puts it in another city.
    No geotag is not evidence of distance, so those pass and a judge decides."""
    loc = tree.get("location") or {}
    if cand.get("lat") is None or loc.get("latitude") is None:
        return True
    return km((loc["latitude"], loc["longitude"]),
              (cand["lat"], cand["lng"])) <= FAR_KM


def _has_evidence(tree, cand):
    """A last-resort candidate needs a geotag, because that is the only thing
    it has. It was collected precisely BECAUSE its title says nothing, so a
    title match on such a file is coincidence rather than evidence: Melbourne's
    "London Plane of Curtain Square" pulled in a map of Shakespearean London
    theatres, via a category search that read Curtain Square as the Curtain
    Theatre and a name match that read London as a place. Ordinary candidates
    are unaffected; they earned their place by naming the tree."""
    if (cand.get("source") or "") != "last-resort":
        return True
    return cand.get("lat") is not None and (tree.get("location") or {}).get("latitude") is not None


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read()
    with open(dest, "wb") as fh:
        fh.write(data)
    return len(data)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = os.path.join(ROOT, "photo-pass")
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
        args = [a for a in args if a != out]
    per_tree = 3
    if "--per-tree" in sys.argv:
        per_tree = int(sys.argv[sys.argv.index("--per-tree") + 1])
        args = [a for a in args if a != str(per_tree)]
    per_city = 8
    if "--per-city" in sys.argv:
        per_city = int(sys.argv[sys.argv.index("--per-city") + 1])
        args = [a for a in args if a != str(per_city)]

    cities = SL.cities_without_photos() if "--zero" in sys.argv else args
    queue = json.load(open(SL.QUEUE))["trees"]
    trees = {}
    import glob
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f))
        for t in d.get("trees", []):
            trees[t["id"]] = t

    for city in cities:
        rows = []
        for tid, entry in queue.items():
            if (entry.get("city") or "").lower() != city.lower():
                continue
            tree = trees.get(tid)
            if tree is None or SL.live_photo(tree):
                continue
            cands = [c for c in entry.get("candidates", []) if not c.get("judged")]
            # A geotag settles identity in both directions, and the queue is
            # full of the negative case: Hobart's five candidates were all
            # photographed in Brisbane, 1,789 km away, because a name search
            # matched "Creek Street". photo_hunt's own 25 km rule cannot catch
            # these once they are in the file, and a judge asked to look at
            # them spends its attention proving what arithmetic already knows.
            cands = [c for c in cands if _within(tree, c) and _has_evidence(tree, c)]
            cands.sort(key=lambda c: SL.rank(tree, c), reverse=True)
            for c in cands[:per_tree]:
                rows.append((SL.rank(tree, c), tid, tree, c))
        rows.sort(key=lambda r: r[0], reverse=True)
        rows = rows[:per_city]
        if not rows:
            print(f"{city}: nothing to fetch")
            continue

        cdir = os.path.join(out, slug(city))
        os.makedirs(cdir, exist_ok=True)
        manifest = []
        print(f"\n{city}: fetching {len(rows)}")
        for i, (score, tid, tree, c) in enumerate(rows, 1):
            url = c.get("thumb")
            if not url:
                continue
            dest = os.path.join(cdir, f"{tid}-{i}.jpg")
            try:
                size = fetch(url, dest)
            except Exception as e:
                print(f"  {tid}-{i}  FETCH FAILED {e}")
                continue
            verdict = ""
            if LIGHT is not None:
                try:
                    s = LIGHT.score(dest)
                    verdict = LIGHT.verdict(s).split(":")[0][:60]
                except Exception:
                    verdict = ""
            loc = tree.get("location") or {}
            dist = None
            if c.get("lat") is not None and loc.get("latitude") is not None:
                dist = round(km((loc["latitude"], loc["longitude"]),
                                (c["lat"], c["lng"])) * 1000)
            manifest.append({
                "file": os.path.basename(dest),
                "tree_id": tid,
                "tree": tree.get("name"),
                "species": tree.get("species"),
                "where": (loc.get("neighbourhood") or loc.get("address") or "")[:80],
                "candidate_title": c.get("title"),
                "page": c.get("url"),
                "thumb": c.get("thumb"),
                "licence": c.get("licence"),
                "author": c.get("author"),
                "metres_from_pin": dist,
                "rank_score": round(score),
                "exposure": verdict,
                "bytes": size,
            })
            print(f"  {os.path.basename(dest):18s} {str(dist):>6}m  {verdict:22s} "
                  f"{(c.get('title') or '')[:56]}")
            time.sleep(PAUSE)
        with open(os.path.join(cdir, "manifest.json"), "w") as fh:
            json.dump({"city": city, "images": manifest}, fh, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
