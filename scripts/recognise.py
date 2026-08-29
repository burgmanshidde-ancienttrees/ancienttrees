#!/usr/bin/env python3
"""Which trees cannot be told apart from their neighbours, and the material to fix it.

`how_to_recognise` is the one sentence that answers the question readers have
actually asked us. Of the first four real reports through the contribute form,
three were "I could not tell which tree", and CLAUDE.md's own instruction for
that report is not a pin fix: it is "a recognition line in the story (what the
trunk, bark or setting looks like that the neighbours do not), a trunk photo, or
both". Measured 2026-08-29, the field was on 14 percent of published trees and 9
percent of the trees in cities that actually get search impressions.

    python3 scripts/recognise.py                 # coverage, worst first
    python3 scripts/recognise.py --brief rome     # the material, tree by tree
    python3 scripts/recognise.py --apply lines.json

WHAT THIS SCRIPT DOES NOT DO, on purpose: write the line. A generated line would
be templating, which SEO_GEO_BLUEPRINT.md's P3 forbids outright, and worse, it
would be written from a pattern instead of from the tree. What it does is the
retrieval half, which is free: it puts the species, the measurements, the
setting, the access note and the story in front of a writer in one place, so the
writing pass is judgement and nothing else.

THE RULE FOR THE LINE ITSELF. Every word has to be RE-STATED from what the entry
already holds, never added to it. Species, girth, height, the setting, what the
story already says about the trunk or the crown: all fair. A bark colour nobody
recorded, a lean nobody measured, a hollow nobody mentioned: fabrication under
hard rule 2, and the fact that it sounds like a description rather than a claim
makes it more dangerous rather than less.

And the line answers ONE question, which is not "what is this tree" but "which
of the trees in front of me is it". So it prefers what separates this trunk from
its neighbours over what is impressive about it. A ranked crown of a species
nobody else in the park has beats "a magnificent old oak" every time.

--apply reads {"tree_id": "the line", ...} and writes each one onto its tree,
refusing an id it cannot find and refusing to overwrite a line already there.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cities():
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        if doc.get("trees"):
            out.append((path, doc))
    return out


def demand():
    """Impressions per city slug, read out of DATA.md's newest depth roster.

    The Search Console credentials live in the digest workflow and never in a
    run, so DATA.md is the only place this answer exists. Absent or unreadable,
    everything sorts by tree count instead, which is a worse order and not a
    broken one."""
    try:
        txt = open(os.path.join(ROOT, "DATA.md"), encoding="utf-8").read()
        blk = txt.split("**Depth is allowed on these cities**", 1)[1]
        blk = blk.split("\n\n", 2)[1]
    except Exception:
        return {}
    out = {}
    for line in blk.split("\n"):
        m = re.match(r"\|\s*([a-z0-9\-]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
        if m:
            out[m.group(1)] = int(m.group(3))
    return out


def report():
    imp = demand()
    rows = []
    for path, doc in cities():
        slug = os.path.basename(path)[:-5]
        ts = doc["trees"]
        have = sum(1 for t in ts if t.get("how_to_recognise"))
        nophoto = sum(1 for t in ts
                      if not t.get("how_to_recognise")
                      and not ((t.get("photo") or {}).get("url")
                               and (t.get("photo") or {}).get("status") != "held"))
        rows.append((imp.get(slug, 0), len(ts) - have, nophoto, slug, len(ts), have))
    rows.sort(key=lambda r: (-r[0], -r[1]))
    total = sum(r[4] for r in rows)
    done = sum(r[5] for r in rows)
    print("%d of %d trees carry a recognition line (%d%%)\n" % (done, total, 100 * done // total))
    print("Worst first, by search impressions then by how many are missing. The last")
    print("column is the trees with neither a line NOR a photograph, which are the")
    print("ones a reader standing in the park has nothing at all to match against.\n")
    print("%-22s %7s %7s %7s %9s" % ("city", "imprs", "trees", "missing", "and no photo"))
    for i, m, np, slug, n, have in rows[:40]:
        print("%-22s %7d %7d %7d %9d" % (slug[:22], i, n, m, np))
    print("\n%d trees have neither a line nor a photograph." % sum(r[2] for r in rows))


def brief(slug):
    path = os.path.join(ROOT, "data", "cities", slug + ".json")
    if not os.path.exists(path):
        print("no such city file: %s" % path)
        return 1
    doc = json.load(open(path, encoding="utf-8"))
    print("=== RECOGNITION BRIEF: %s ===" % doc["city"])
    print("Write one sentence per tree, answering which of the trees in front of me")
    print("is it. Re-state only: species, girth, height, setting, access, and what")
    print("the story already says. Invent nothing. Deliver {\"id\": \"line\", ...}\n")
    for t in doc["trees"]:
        if t.get("how_to_recognise"):
            continue
        loc = t.get("location") or {}
        ph = (t.get("photo") or {})
        print("--- %s  %s" % (t["id"], t.get("name")))
        print("    species: %s" % t.get("species"))
        bits = []
        if t.get("girth_cm"):
            bits.append("girth %.2f m" % (t["girth_cm"] / 100.0))
        if t.get("height_m"):
            bits.append("height %s m" % t["height_m"])
        if t.get("age_estimate"):
            bits.append("age %s" % t["age_estimate"])
        if bits:
            print("    %s" % ", ".join(bits))
        print("    where: %s" % (loc.get("address") or "")[:150])
        print("    access: %s" % (t.get("access") or "")[:150])
        print("    photo: %s" % ("yes" if ph.get("url") and ph.get("status") != "held" else "NO"))
        print("    story: %s" % (t.get("story") or "").replace("\n", " "))
        print()
    return 0


def apply(src):
    lines = json.load(open(src, encoding="utf-8"))
    if isinstance(lines, dict) and "lines" in lines:
        lines = lines["lines"]
    wrote = skipped = missing = 0
    seen = set()
    for path, doc in cities():
        touched = False
        for t in doc["trees"]:
            line = lines.get(t["id"])
            if not line:
                continue
            seen.add(t["id"])
            if t.get("how_to_recognise"):
                skipped += 1
                continue
            t["how_to_recognise"] = line.strip()
            wrote += 1
            touched = True
        if touched:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
    for tid in lines:
        if tid not in seen:
            missing += 1
            print("  no such tree: %s" % tid)
    print("%d line(s) written, %d already had one, %d ids not found"
          % (wrote, skipped, missing))
    return 1 if missing else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief")
    ap.add_argument("--apply")
    args = ap.parse_args()
    if args.brief:
        return brief(args.brief)
    if args.apply:
        return apply(args.apply)
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
