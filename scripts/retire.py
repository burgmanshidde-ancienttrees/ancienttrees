#!/usr/bin/env python3
"""Retire published trees in one step, including everything a retirement leaves behind.

Written 2026-10-10. A night run retired 45 Dutch trees the national register
marks Dood/geveld, by hand: out of data/cities, into data/leads, slugs into
REMOVED_TREE_SLUGS. Preflight said 0 problems, and the deploy then went red for
two and a half hours, one error per build, on what the hand edit left behind:
two park pages still promising the old counts, a city FAQ saying 37 of 39, a
story pointing at a felled neighbour, and a vendored photograph nothing pointed
at any more. All of it is mechanical to find, so this does the finding.

Usage:
  python3 scripts/retire.py <city-slug> <tree-id>... --reason "why"
      moves each tree to data/leads/<city>.json (--to blocked for the blocked
      list) with removed/removed_reason, adds its slug to REMOVED_TREE_SLUGS so
      the URL keeps resolving, deletes its files in site/public/photos and
      rebuilds data/photo-manifest.json, then prints what still needs a hand.
  python3 scripts/retire.py <city-slug> <tree-id>...
      for trees already retired by hand: reads them back from the leads file
      and does everything except the move.
  --dry-run   change nothing, print what would happen.

What it changes is reversible and mechanical. What it PRINTS is the copy a
person has to rewrite: park and city count promises that no longer hold, every
place the old count still appears, and every mention of a retired tree in the
rest of the city. Then run python3 scripts/preflight.py, which refuses the
park counts and the orphan photographs before a push.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import park_groups
import preflight
from thin_pages import slugify
import vendor_photos

REDIRECT_MAP = os.path.join("site", "src", "lib", "redirect-map.ts")
PHOTOS = os.path.join("site", "public", "photos")
CITY_COPY = ("intro", "meta_description", "question_meta", "question_answer", "question_context")


def load(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    m = re.search(r"^( +)\S", raw, re.M)
    return json.loads(raw), (len(m.group(1)) if m else 1)


def save(path, doc, indent):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=indent, ensure_ascii=False)
        fh.write("\n")


def count_words(n):
    """The ways copy can write n: digits, and the word when there is one."""
    out = [str(n)]
    if 0 <= n < len(preflight.WORDS):
        out.append(preflight.WORDS[n])
    return out


def find_count(text, n):
    hits = []
    for w in count_words(n):
        # Not inside a longer number either: "5.39 metres round" is no 39.
        for m in re.finditer(r"(?<![\w.,-])%s(?![\w-]|[.,]\d)" % re.escape(w), text, re.I):
            hits.append(text[max(0, m.start() - 40):m.end() + 40].replace("\n", " "))
    return hits


GENERIC = {"the", "of", "at", "by", "in", "on", "and", "tree", "trees", "old", "great",
           "giant", "ancient", "little", "big", "twin", "twins", "pair", "trio",
           # place nouns: the proper name beside them is the needle, not these
           "statue", "courtyard", "church", "chapel", "park", "garden", "gardens",
           "street", "square", "gate", "castle", "house", "lane", "road", "bridge",
           "canal", "pond", "lake", "hospital", "school", "station", "monument"}


def name_needles(tree, remaining):
    """What a mention of this tree looks like elsewhere: its id, its name
    without the article, and the PLACE in its name. The place matters most,
    because a neighbour's story names the place rather than the tree: Arnhem's
    lime story said "a common lime beside the Watermuseum" about The
    Watermuseum Lime. The place is what follows "of/at/by" ("the Boogjes
    Courtyard"), or failing that the proper words before the species ("Wagnerlaan
    Poplar"); never a colour or a shape ("White Horse Chestnut"). A place word a
    remaining tree also stands at (Zijpendaal, with three trees at its gate) is
    dropped, since every mention of it is about them."""
    name = re.sub(r"^the\s+", "", tree.get("name") or "", flags=re.I).strip()
    needles = [tree["id"]]
    if len(name.split()) >= 2:
        needles.append(name)
    species = set(re.findall(r"[a-z]+", (tree.get("species") or "").split("(")[0].lower()))
    shared = " ".join(
        "%s %s %s" % (t.get("name") or "", (t.get("location") or {}).get("neighbourhood") or "",
                      (t.get("location") or {}).get("address") or "")
        for t in remaining).lower()
    m = re.search(r"\b(?:of|at|by|in|on)\s+(?:the\s+)?(.+)$", name, re.I)
    place = m.group(1) if m else name
    if m and len(place.split()) >= 2 and place.lower() not in shared:
        needles.append(place)
    for w in re.findall(r"[^\W\d_][\w'-]+", place):
        lw = w.lower()
        if len(w) < 5 or lw in GENERIC or lw in species or not w[0].isupper():
            continue
        if re.search(r"(?<!\w)%s(?!\w)" % re.escape(lw), shared):
            continue
        needles.append(w)
    return needles


def insert_redirects(entries, reason, dry):
    with open(REDIRECT_MAP, encoding="utf-8") as fh:
        src = fh.read()
    head = "const REMOVED_TREE_SLUGS: [string, string][] = [\n"
    if head not in src:
        raise SystemExit("%s: cannot find REMOVED_TREE_SLUGS" % REDIRECT_MAP)
    new = [e for e in entries if '["%s", "%s"]' % e not in src]
    if not new:
        return []
    block = "  // %s, scripts/retire.py: %s\n" % (datetime.date.today().isoformat(), reason[:90].replace("\n", " "))
    block += "".join('  ["%s", "%s"],\n' % e for e in new)
    if not dry:
        with open(REDIRECT_MAP, "w", encoding="utf-8") as fh:
            fh.write(src.replace(head, head + block, 1))
    return new


def remove_photos(retired_ids, retired_trees, dry):
    """Files of the retired trees that no published tree still points at."""
    still = set()
    for path in glob.glob(os.path.join("data", "cities", "*.json")):
        for t in load(path)[0].get("trees", []):
            for shot in [t.get("photo") or {}] + list(t.get("photos") or []):
                u = (shot or {}).get("url") or ""
                if "/photos/" in u:
                    still.add(u.rsplit("/", 1)[-1])
    gone = set()
    for f in os.listdir(PHOTOS) if os.path.isdir(PHOTOS) else []:
        if any(f.startswith(i + "-") for i in retired_ids):
            gone.add(f)
    for t in retired_trees:
        for shot in [t.get("photo") or {}] + list(t.get("photos") or []):
            u = (shot or {}).get("url") or ""
            if "/photos/" in u and os.path.exists(os.path.join(PHOTOS, u.rsplit("/", 1)[-1])):
                gone.add(u.rsplit("/", 1)[-1])
    gone -= still
    if not dry:
        for f in gone:
            os.remove(os.path.join(PHOTOS, f))
        if gone:
            vendor_photos.write_manifest()
    return sorted(gone)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("city")
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--reason", help="why; required when a tree is still in data/cities")
    ap.add_argument("--to", choices=("leads", "blocked"), default="leads")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    dry = a.dry_run

    city_path = os.path.join("data", "cities", a.city + ".json")
    leads_path = os.path.join("data", "leads", a.city + ".json")
    city, city_indent = load(city_path)
    leads, leads_indent = load(leads_path) if os.path.exists(leads_path) else ({"leads": [], "blocked": []}, 1)
    in_leads = {t.get("id"): t for kind in ("leads", "blocked") for t in leads.get(kind) or []}

    before_trees = list(city["trees"])
    retired, moving = [], []
    for i in a.ids:
        t = next((t for t in city["trees"] if t.get("id") == i), None)
        if t:
            moving.append(t)
        elif i in in_leads:
            retired.append(in_leads[i])   # retired by hand already
        else:
            raise SystemExit("%s is neither in %s nor in %s" % (i, city_path, leads_path))
    if moving and not a.reason:
        raise SystemExit("--reason is required to move %s out of %s"
                         % (", ".join(t["id"] for t in moving), city_path))

    today = datetime.date.today().isoformat()
    for t in moving:
        city["trees"].remove(t)
        rec = dict(t, removed=today, removed_reason=a.reason)
        leads.setdefault(a.to, []).append(rec)
        retired.append(t)
    if moving and not dry:
        save(city_path, city, city_indent)
        save(leads_path, leads, leads_indent)
    # Count the "before" from the city as it stood plus anything retired by hand.
    before_trees += [t for t in retired if t not in before_trees]
    retired_ids = {t["id"] for t in retired}
    after_trees = [t for t in before_trees if t["id"] not in retired_ids]
    verb = "would" if dry else "did"

    print("%s: %d trees retired (%s), %d remain" % (a.city, len(retired), ", ".join(sorted(retired_ids)), len(after_trees)))
    if moving:
        print("  %s move %d to %s [%s]" % (verb, len(moving), leads_path, a.to))

    added = insert_redirects([(a.city, slugify(t.get("name") or "")) for t in retired], a.reason or "retired", dry)
    for e in added:
        print("  %s add %s/%s to REMOVED_TREE_SLUGS" % (verb, *e))
    clash = {slugify(t.get("name") or "") for t in after_trees} & {slugify(t.get("name") or "") for t in retired}
    for s in sorted(clash):
        print("  CHECK a remaining tree has the slug %s, which now redirects" % s)

    for f in remove_photos(retired_ids, retired, dry):
        print("  %s delete site/public/photos/%s" % (verb, f))

    todo = []

    # Parks whose count moved. City copy quotes a park's count too ("Thirteen
    # of these twenty stand inside that garden"), so those numbers are looked
    # for there as well.
    park_moves = []
    old_parks = park_groups.city_parks({"trees": before_trees})
    new_parks = park_groups.city_parks({"trees": after_trees})
    for path, intro in park_groups.park_intros(a.city):
        park = intro.get("park")
        o, n = len(old_parks.get(park, [])), len(new_parks.get(park, []))
        if o == n:
            continue
        label = os.path.relpath(path)
        park_moves.append((park, o))
        print("\n  park %s: %d -> %d trees" % (park, o, n))
        if park_groups.page_allowed(o, intro) and not park_groups.page_allowed(n, intro):
            todo.append("%s: the park page DISAPPEARS (below Contract H's gate), and its URL "
                        "with it. Hard rule 3: find a tree or redirect /parks/%s." % (label, intro.get("slug")))
        todo += preflight.park_promise_problems(intro, n, label)
        for key in ("title", "meta_description", "intro"):
            for hit in find_count(intro.get(key) or "", o):
                todo.append("%s %s still says the old count %d: ...%s..." % (label, key, o, hit))

    # The city's own copy.
    o, n = len(before_trees), len(after_trees)
    todo += preflight.check_city(city_path) if not dry else []
    fields = [(k, city.get(k) or "") for k in CITY_COPY]
    fields += [("faq", (f.get("q") or "") + " " + (f.get("a") or "")) for f in city.get("faq") or []]
    for key, text in fields:
        for hit in find_count(text, o):
            todo.append("%s %s still says the old count %d: ...%s..." % (city_path, key, o, hit))
    for park, po in park_moves:
        for key, text in fields:
            for hit in find_count(text, po):
                todo.append("%s %s may quote %s's old count %d: ...%s..." % (city_path, key, park, po, hit))
    for path in sorted(glob.glob(os.path.join("data", "i18n", "*", a.city + ".json"))):
        ov = load(path)[0]
        text = json.dumps({k: v for k, v in ov.items() if k != "trees" and not k.startswith("_")},
                          ensure_ascii=False)
        for hit in find_count(text, o)[:3]:
            todo.append("%s still says the old count %d: ...%s..." % (path, o, hit))
        stale = sorted(retired_ids & set((ov.get("trees") or {}).keys()))
        if stale:
            todo.append("%s carries translations of %s (harmless, nothing renders them)" % (path, ", ".join(stale)))

    # Mentions of the retired trees anywhere else in the city.
    needles = [(t["id"], nd) for t in retired for nd in name_needles(t, after_trees)]
    texts = [("%s %s" % (city_path, k), v) for k, v in fields]
    for t in after_trees:
        for k in ("story", "how_to_recognise", "recognise", "access", "transport"):
            if t.get(k):
                texts.append(("%s %s %s" % (city_path, t["id"], k), str(t[k])))
    for path, intro in park_groups.park_intros(a.city):
        texts += [("%s %s" % (os.path.relpath(path), k), intro.get(k) or "") for k in ("title", "meta_description", "intro")]
    for where, text in texts:
        for rid, nd in needles:
            if re.search(r"(?<!\w)%s(?!\w)" % re.escape(nd), text, re.I):
                todo.append("%s mentions %s (%r)" % (where, rid, nd))

    # Other files that point at a tree by id.
    for path in sorted(glob.glob(os.path.join("data", "collections", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        for rid in sorted(retired_ids):
            if '"%s"' % rid in src:
                todo.append("%s names %s as an entry" % (path, rid))

    print()
    if todo:
        print("STILL TO DO BY HAND (%d), then python3 scripts/preflight.py:" % len(todo))
        for line in todo:
            print("  " + line)
    else:
        print("nothing else names the retired trees; run python3 scripts/preflight.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
