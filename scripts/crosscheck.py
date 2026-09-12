#!/usr/bin/env python3
"""Does a feature that reached the website also reach the phone?

Hidde, 2026-09-12, after the multiple-photographs change landed on the web
built and on iOS unbuilt: "remember somewhere to always by default work cross
platform." He has now said a version of this three times. 2026-08-21 set the
both-surfaces rule ("whenever designing these features the same principle
should account for app and web"); 2026-09-11 sharpened it for copy ("zorg dat
dit volgende keer wel gelijk app en web doet") and produced paritycheck.py.
A lesson that appears on three different days is not a rule, it is a missing
check, so this is the third writing turned into one.

WHAT paritycheck.py ALREADY DOES, so this does not repeat it: it catches
user-facing COPY removed from one surface and still standing on the other. It
reads strings. It cannot see a feature, because a feature is not a sentence.

WHAT THIS DOES: it reads the CONTRACT between the two surfaces, which is the
feed. Every feature the website decides and the app shows travels as a field in
/api/trees.json, so a field the website sends that no Swift model reads is a
feature that stopped at the web, and a field the app expects that the website
stopped sending is a feature that broke on the phone. Both are silent today:
Swift's decoder ignores unknown keys, so nothing goes red either way, and the
symptom is a phone quietly missing something the website has.

It is deliberately mechanical and deliberately narrow. It cannot tell that a
strip of thumbnails was drawn on one surface and not the other; it can tell
that the data behind it only travels in one direction, which is where this
class of miss actually starts. Read it as the floor, not the ceiling: the
design-time half stays the one-line answer the both-surfaces rule asks for.

    python3 scripts/crosscheck.py           # exit 1 on a one-sided field
    python3 scripts/crosscheck.py --list    # print both key sets and stop

Needs site/dist/api/trees.json, which is what actually ships. Without a build
it says so and exits 0 rather than guessing, the same way every other script
here behaves when its input is absent.
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "site", "dist", "api", "trees.json")
MODELS = os.path.join(ROOT, "ios", "AncientTrees", "AncientTrees", "Kit", "Models.swift")
ALLOW = os.path.join(ROOT, "data", "cross-surface-allow.json")


def feed_keys():
    """Every key the feed actually puts on a tree and on a photograph.

    Sampled across the whole file rather than off the first row, because most
    of these fields are optional: `photos` sits on one tree in three thousand,
    and a check reading trees[0] would never have seen the field this was
    written for.
    """
    with open(FEED, encoding="utf-8") as fh:
        doc = json.load(fh)
    trees = doc if isinstance(doc, list) else doc.get("trees", [])
    tree_keys, photo_keys = set(), set()
    for t in trees:
        tree_keys |= set(t.keys())
        for p in [t.get("photo")] + list(t.get("photos") or []):
            if isinstance(p, dict):
                photo_keys |= set(p.keys())
    return tree_keys, photo_keys, len(trees)


def coding_keys(src, struct):
    """The wire names one Swift struct decodes.

    The CodingKeys enum is the honest place to read this: a property renamed in
    Swift keeps its wire name here, and a property with no enum entry decodes
    under its own name, which is why the bare `case a, b, c` form counts too.
    """
    start = src.index("struct %s" % struct)
    head = src.index("enum CodingKeys", start)
    end = src.index("}", head)
    out = set()
    for line in src[head:end].splitlines():
        line = line.strip()
        if not line.startswith("case "):
            continue
        for part in line[5:].split(","):
            part = part.strip()
            if not part:
                continue
            out.add(part.split("=")[1].strip().strip('"') if "=" in part else part)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true",
                    help="print what each surface knows about and stop")
    args = ap.parse_args()

    if not os.path.exists(FEED):
        print("crosscheck: no build at site/dist/api/trees.json, so what the "
              "website sends cannot be read. Skipping rather than guessing.")
        return 0
    if not os.path.exists(MODELS):
        print("crosscheck: no ios/ checkout here. Skipping.")
        return 0

    tree_keys, photo_keys, n = feed_keys()
    src = open(MODELS, encoding="utf-8").read()
    app_tree = coding_keys(src, "Tree")
    app_photo = coding_keys(src, "Photo")

    allow = {"web_only": [], "app_only": []}
    if os.path.exists(ALLOW):
        with open(ALLOW, encoding="utf-8") as fh:
            allow.update({k: v for k, v in json.load(fh).items() if k in allow})
    web_only_ok = {e["field"] for e in allow["web_only"]}
    app_only_ok = {e["field"] for e in allow["app_only"]}

    if args.list:
        print("feed tree keys :", " ".join(sorted(tree_keys)))
        print("app  tree keys :", " ".join(sorted(app_tree)))
        print("feed photo keys:", " ".join(sorted(photo_keys)))
        print("app  photo keys:", " ".join(sorted(app_photo)))
        return 0

    problems = []
    for label, sent, read in (("tree", tree_keys, app_tree),
                              ("photo", photo_keys, app_photo)):
        for f in sorted(sent - read - web_only_ok):
            problems.append(
                "%s.%s is sent to every phone and no Swift model reads it, so "
                "whatever it is for exists on the website only. Decode it in "
                "Kit/Models.swift, or record why it is web-only in "
                "data/cross-surface-allow.json." % (label, f))
        for f in sorted(read - sent - app_only_ok):
            problems.append(
                "%s.%s is decoded by the app and the feed sends it on no tree. "
                "Either the website stopped sending it, which breaks the "
                "feature on the phone silently, or the field never existed. "
                "Check site/src/lib/app-feed.ts." % (label, f))

    for p in problems:
        print("  " + p)
    if problems:
        print("crosscheck: %d field(s) live on one surface only" % len(problems))
        return 1
    print("crosscheck: %d trees, every feed field the website sends is read by "
          "the app and every field the app reads is sent" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
