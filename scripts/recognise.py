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


def stuck(limit=40):
    """The trees that would actually defeat somebody standing in front of them.

    Added 2026-09-07, after Hidde tried to collect a cedar in Nara and could not
    tell which one it was: "I don't think we can fix the data, we should design
    the flow of adding a tree in a way that people either get confirmation by
    photo or description, or honesty in not knowing."

    He is right, and this is the list that flow needs. Three conditions have to
    hold at once before a tree is a problem, and the third is the one nothing
    was measuring:

      no recognition line   nothing to read
      no photograph         nothing to compare against
      company               at least one OTHER tree that a government has
                            called remarkable within 25 metres

    The third matters more than it sounds. A tree with neither a line nor a
    picture, standing alone in an empty square, needs nothing: you can see there
    is only one. The same tree in Amsterdam's canal belt, where our pins average
    fifteen registered remarkable trees within a hundred metres, is
    unanswerable. Counting "missing a line" without counting the company is how
    a target list ends up pointing at the wrong cities, which is exactly what
    the first cut of this did.

    Register rows, not all trees: a state body already judged each of these
    remarkable, so they are the lookalikes a visitor would actually hesitate
    between. It undercounts, because the ground holds ordinary old trees too,
    and it undercounts hardest where we hold no register at all (Japan, most of
    Asia). A zero here means no data, never no trees.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import corroborate
    table = corroborate.rows()
    imp = demand()
    out = []
    for path, doc in cities():
        slug = os.path.basename(path)[:-5]
        for t in doc["trees"]:
            if t.get("how_to_recognise"):
                continue
            ph = t.get("photo") or {}
            if ph.get("url") and ph.get("status") != "held":
                continue
            loc = t.get("location") or {}
            if loc.get("latitude") is None:
                continue
            hits = corroborate.nearest(loc["latitude"], loc["longitude"], table,
                                       within=25, limit=20)
            # Our own entry usually sits in the register too, at nearly zero
            # metres, and a tree is not company for itself.
            company = [h for h in hits if h["distance_m"] > 3]
            if not company:
                continue
            out.append((imp.get(slug, 0), len(company), slug, t["id"],
                        t.get("name", ""), t.get("location_precision")))
    out.sort(key=lambda r: (-r[0], -r[1]))
    print("%d trees have nothing to match against AND company within 25 m.\n" % len(out))
    print("Ordered by the city's search impressions, then by how crowded it is.")
    print("A city with no register of ours prints nothing here, which is missing")
    print("data rather than an empty park.\n")
    print("%-16s %6s %7s %-11s %s" % ("city", "imprs", "company", "pin", "tree"))
    for i, c, slug, tid, name, prec in out[:limit]:
        print("%-16s %6d %7d %-11s %s" % (slug[:16], i, c, prec or "?", name[:44]))
    seen = {}
    for i, c, slug, tid, name, prec in out:
        seen[slug] = seen.get(slug, 0) + 1
    top = sorted(seen.items(), key=lambda kv: -kv[1])[:12]
    print("\nBy city: " + ", ".join("%s %d" % (k, v) for k, v in top))


def brief(slug, gaps_only=False):
    path = os.path.join(ROOT, "data", "cities", slug + ".json")
    if not os.path.exists(path):
        print("no such city file: %s" % path)
        return 1
    doc = json.load(open(path, encoding="utf-8"))
    print("=== RECOGNITION BRIEF: %s ===" % doc["city"])
    print("Write ONE sentence per tree, in this shape and no other:")
    print("    You can recognise it by [what you can see]. It stands [where, or beside what].")
    print("It answers a question somebody is asking out loud, 'how do I find it',")
    print("so the reader is the subject. Not a caption, not an inventory.")
    print("Re-state ONLY what is printed below: species, girth, height, setting,")
    print("access, and what the story already says. A bark colour nobody recorded")
    print("is fabrication. Under 240 characters. No em dashes.")
    print("Deliver {\"id\": \"line\", ...}\n")
    for t in doc["trees"]:
        if t.get("how_to_recognise"):
            continue
        # The trees that need it most: no photograph to compare against and a
        # pin that only claims the place. A tree with a good photograph can be
        # matched by eye, and an exact pin can be walked to.
        if gaps_only:
            ph0 = t.get("photo") or {}
            if ph0.get("url") and ph0.get("status") != "held":
                continue
            if t.get("location_precision") == "confirmed":
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


def apply(src, overwrite=False):
    """Write the lines. Refuses to overwrite by default.

    The guard exists because a second pass should never quietly replace a line
    somebody wrote deliberately. --overwrite is for the case it was written
    for: rewriting a batch in a better voice, knowingly, in one go.
    """
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
            if t.get("how_to_recognise") and not overwrite:
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
    ap.add_argument("--stuck", action="store_true",
                    help="trees with no line, no photo and remarkable company nearby")
    ap.add_argument("--brief")
    ap.add_argument("--gaps", action="store_true",
                    help="with --brief: only trees with no photo and a rough pin")
    ap.add_argument("--apply")
    ap.add_argument("--overwrite", action="store_true",
                    help="replace lines that already exist (deliberate rewrites only)")
    args = ap.parse_args()
    if args.stuck:
        stuck()
        return 0
    if args.brief:
        return brief(args.brief, gaps_only=args.gaps)
    if args.apply:
        return apply(args.apply, overwrite=args.overwrite)
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
