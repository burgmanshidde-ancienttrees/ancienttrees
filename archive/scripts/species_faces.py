#!/usr/bin/env python3
"""Every species card face, in one list, so a viewing pass can judge them.

Hidde, 2026-08-23, on the Horse Chestnut card: he would not use that photo as a
thumbnail. It was a close-up of red survey paint around a wound on a trunk, and
it was fronting the species page because /species took the first photograph it
found. Sampling three faces that day found two that fail the Cadiz standard: a
bark close-up and a woodland footpath with no tree in it.

No script can judge this. A ranking knows pixels and aspect ratio; only a person
can see that a picture is of bark, of a path, or of the parked cars. So the
useful thing a script can do is make LOOKING cheap, which is what
photo_gaps.py --shortlist does for photo-less trees.

    python3 scripts/species_faces.py              every face, biggest species first
    python3 scripts/species_faces.py --unpinned   only the ones nobody has chosen
    python3 scripts/species_faces.py --urls       bare urls, one per line, to fetch

Pin a good one by setting `face_tree_id` on data/species/<slug>.json. A pin
always wins over the ranking, and scripts/qa.py fails the build if a page that
draws species cards ignores it.
"""
import argparse, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_CARD_PX = 540


def usable(t):
    p = t.get("photo") or {}
    if not (p.get("url") and p.get("license") and p.get("attribution")):
        return None
    if p.get("status") not in ("approved", "found_needs_check"):
        return None
    if "/wiki/File:" in p["url"]:
        return None
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unpinned", action="store_true")
    ap.add_argument("--urls", action="store_true")
    a = ap.parse_args()

    intros = {}
    for f in glob.glob(os.path.join(ROOT, "data", "species", "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        intros[d["common_name"]] = d

    members = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        c = json.load(open(f, encoding="utf-8"))
        for t in c.get("trees", []):
            members.setdefault(t.get("species") or "", []).append((c["city"], t))

    rows = []
    for common, intro in intros.items():
        ms = [m for sp, lst in members.items() if sp.split(" (")[0].strip() == common for m in lst]
        if not ms:
            continue
        pin = intro.get("face_tree_id")
        chosen = None
        if pin:
            hit = next((m for m in ms if m[1]["id"] == pin), None)
            if hit and usable(hit[1]):
                chosen = (hit[0], hit[1], usable(hit[1]), "PINNED")
        if not chosen:
            ranked = []
            for city, t in ms:
                p = usable(t)
                if not p:
                    continue
                w, h = p.get("width") or 0, p.get("height") or 0
                ranked.append(((w == 0 or w >= MIN_CARD_PX), (w >= h if w and h else False), w,
                               city, t, p))
            ranked.sort(key=lambda r: (r[0], r[1], r[2]), reverse=True)
            if ranked:
                r = ranked[0]
                chosen = (r[3], r[4], r[5], "guessed")
        if chosen and not (a.unpinned and chosen[3] == "PINNED"):
            rows.append((len(ms), common, chosen))

    # A pin that points at a tree with no usable photograph is a silent no-op:
    # the card quietly falls back to the ranking and nobody learns that a
    # person's choice is being ignored. Found 2026-08-23, when Pin Oak was
    # pinned to apd_008, a tree published that same morning with no photo.
    dangling = []
    for common, intro in intros.items():
        pin = intro.get("face_tree_id")
        if not pin:
            continue
        hit = None
        for _, lst in members.items():
            for city, t in lst:
                if t["id"] == pin:
                    hit = (city, t)
        if hit is None:
            dangling.append((common, pin, "no tree with that id"))
        elif not usable(hit[1]):
            dangling.append((common, pin, "%s, %s has no usable photo" % (hit[0], pin)))

    rows.sort(reverse=True)
    if a.urls:
        for _, _, ch in rows:
            print(ch[2]["url"])
        return 0

    print("%-26s %5s %-8s %-13s %s" % ("species", "trees", "how", "city", "photo"))
    for n, common, (city, t, p, how) in rows:
        print("%-26s %5d %-8s %-13s %s" % (common[:26], n, how, city[:13],
                                           os.path.basename(p["url"])[:52]))
    pinned = sum(1 for _, _, ch in rows if ch[3] == "PINNED")
    print("\n%d species show a photo, %d pinned by hand, %d still guessed."
          % (len(rows), pinned, len(rows) - pinned))
    print("Judge them against the Cadiz standard: the TREE is the subject, crown and")
    print("trunk both readable, daylight, colour, and it survives a centre crop.")
    if dangling:
        print("\n%d pin(s) do nothing, so the card is still guessing:" % len(dangling))
        for common, pin, reason in dangling:
            print("  %-24s face_tree_id %-10s %s" % (common[:24], pin, reason))
    return 0


if __name__ == "__main__":
    sys.exit(main())
