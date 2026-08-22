#!/usr/bin/env python3
"""Check a translation overlay against Contract J, before it can reach a build.

Written 2026-08-22, when six translation agents started producing overlays in
parallel. Each one reports its own checks as passing. That report is a claim
about a file, not the file, and the difference has cost this project a day
before: a pass reporting success is exactly as cheap to produce as a pass that
did the work.

The build enforces some of this already (tree coverage in getStaticPaths, the
150-250 word bar), but it enforces it by REFUSING TO BUILD, which on a static
site means the whole deploy dies over one long paragraph in one story. This
runs first, names every problem at once, and costs nothing.

Usage:
  python3 scripts/i18ncheck.py                 # every overlay
  python3 scripts/i18ncheck.py it/rome         # one
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, "data", "i18n")
CITIES = os.path.join(ROOT, "data", "cities")

# Japanese does not put spaces between words, so a whitespace token count
# measures nothing there; the bars are expressed in characters instead. These
# three numbers must agree with UNSPACED, introBar and storyBar in
# site/src/lib/i18n.ts. They were written twice once already and disagreed
# within the hour, which is how "ja/tokyo: intro is 1 words" reached a build,
# so if you change one, change both and say so in the commit.
CJK = {"ja", "zh", "ko"}
LIMITS = {"title": 60, "meta_description": 155, "question_title": 60, "question_meta": 155}
REQUIRED = ["city", "title", "meta_description", "intro", "question_title",
            "question_meta", "question_answer", "question_context", "faq", "trees"]
TREE_FIELDS = ["name", "species", "age_estimate", "access", "transport", "story"]


def words(s, lang):
    return len(s) if lang in CJK else len(s.split())


def check(lang, slug):
    p = os.path.join(I18N, lang, slug + ".json")
    en_p = os.path.join(CITIES, slug + ".json")
    out = []
    with open(p, encoding="utf-8") as fh:
        d = json.load(fh)
    with open(en_p, encoding="utf-8") as fh:
        en = json.load(fh)

    for k in REQUIRED:
        if k not in d:
            out.append("missing top-level key: %s" % k)
    for k, lim in LIMITS.items():
        if k in d and len(d[k]) > lim:
            out.append("%s is %d chars, max %d" % (k, len(d[k]), lim))

    lo, hi = (150, 250) if lang in CJK else (60, 100)
    if "intro" in d:
        n = words(d["intro"], lang)
        if not (lo <= n <= hi):
            out.append("intro is %d %s, want %d-%d" % (n, "chars" if lang in CJK else "words", lo, hi))

    # Every tree the English city renders must be translated, or the page
    # silently falls back to English prose and reads as sloppiness.
    en_ids = [t["id"] for t in en.get("trees", [])]
    tr = d.get("trees", {})
    for i in en_ids:
        if i not in tr:
            out.append("no translation for %s" % i)
    for extra in set(tr) - set(en_ids):
        out.append("%s is translated but not in the English city file" % extra)

    slo, shi = (350, 600) if lang in CJK else (150, 250)
    for tid, t in tr.items():
        for f in TREE_FIELDS:
            if not t.get(f):
                out.append("%s: empty or missing %s" % (tid, f))
        if t.get("story"):
            n = words(t["story"], lang)
            if not (slo <= n <= shi):
                out.append("%s: story is %d %s, want %d-%d"
                           % (tid, n, "chars" if lang in CJK else "words", slo, shi))

    # Hard rule 3, and it is worth checking the lookalikes too: an en dash or a
    # horizontal bar reads the same to a person and slips past a naive grep.
    blob = json.dumps(d, ensure_ascii=False)
    for ch, name in [("—", "em dash"), ("–", "en dash"), ("―", "horizontal bar")]:
        if ch in blob:
            out.append("contains a %s (hard rule 3)" % name)
    return out


def main():
    targets = []
    if len(sys.argv) > 1:
        targets = [tuple(a.split("/")) for a in sys.argv[1:]]
    else:
        for lang in sorted(os.listdir(I18N)):
            d = os.path.join(I18N, lang)
            if os.path.isdir(d):
                for f in sorted(os.listdir(d)):
                    if f.endswith(".json"):
                        targets.append((lang, f[:-5]))
    bad = 0
    for lang, slug in targets:
        try:
            probs = check(lang, slug)
        except Exception as e:
            print("%-16s ERROR %s" % ("%s/%s" % (lang, slug), e))
            bad += 1
            continue
        label = "%s/%s" % (lang, slug)
        if probs:
            bad += 1
            print("%-16s %d problem(s)" % (label, len(probs)))
            for x in probs:
                print("    %s" % x)
        else:
            print("%-16s clean" % label)
    print("\n%d overlay(s) checked, %d with problems" % (len(targets), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
