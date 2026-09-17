#!/usr/bin/env python3
"""What would translating the rest of the site actually cost? Measure it, do not guess.

Written 2026-09-17 on Hidde's question: "can we make a token cheap full
translation of the website there is a clear need to offer all in different
languages." The answer turns entirely on what "full" means, and the two
readings differ by more than ten times, so this prints both rather than
letting a session pick the flattering one.

  FULL-LOCAL   every city translated into ITS OWN language area's language,
               which is the model Contract J v1.13 already runs on ("a
               language is translated onto the cities of its own language
               area, never onto whichever English page happens to perform
               best"). Affordable.

  FULL-MATRIX  every city in every language. Ten times the cost, and it buys
               a Spanish page about Kyoto that no Spanish speaker searches
               for. Priced here only so nobody has to re-derive why it is
               not the plan.

Token arithmetic is deliberately crude and stated so: characters / 4 for the
input, times 2.2 for the round trip, because the model reads the English and
writes a target text of roughly the same length. It is an order of magnitude,
not an invoice. What it is good enough for is the only question being asked:
does this fit in a subscription, or not.

Fields counted are the ones a reader SEES. notes and verify_notes are
internal and never rendered, so translating them would be paying for nothing.

Usage:
  python3 scripts/transplan.py            # both readings, per language
  python3 scripts/transplan.py --next     # the cheapest untranslated city per language
  python3 scripts/transplan.py --value    # what to translate next, demand per token
  python3 scripts/transplan.py --glossary # how much of the payload is repeated strings
"""
import collections
import glob
import re
import json
import os
import sys

# Languages Contract J v1.13 already ships. Switzerland and Belgium appear
# under more than one language on purpose: both are genuinely multilingual and
# the overlay is per city, so the per-city call is a human one.
SHIPPING = {
    "es": {"Spain", "Mexico", "Argentina", "Chile", "Colombia", "Peru", "Uruguay",
           "Cuba", "Ecuador", "Bolivia", "Venezuela", "Costa Rica", "Guatemala",
           "Panama", "Paraguay"},
    "it": {"Italy", "San Marino", "Switzerland"},
    "nl": {"Netherlands", "Belgium"},
    "de": {"Germany", "Austria", "Switzerland", "Liechtenstein"},
    "pt": {"Portugal", "Brazil"},
    "fr": {"France", "Belgium", "Switzerland", "Luxembourg", "Monaco"},
    "ja": {"Japan"},
}

# Languages the site does NOT have. Adding any of them is a Contract J change
# and therefore needs Hidde's yes and a blueprint version bump (hard rule 7).
# Listed here so the cost of that decision is visible before it is taken.
PROPOSED = {
    "cs": {"Czech Republic"}, "pl": {"Poland"}, "lt": {"Lithuania"},
    "sk": {"Slovakia"}, "hu": {"Hungary"}, "sv": {"Sweden"},
    "da": {"Denmark"}, "no": {"Norway"}, "fi": {"Finland"},
    "el": {"Greece"}, "tr": {"Turkey"}, "ko": {"South Korea"},
    "ro": {"Romania"}, "hr": {"Croatia"},
}

# Countries whose cities need no translation at all.
ENGLISH = {"United States", "United Kingdom", "Australia", "Ireland", "Canada",
           "New Zealand", "Singapore", "South Africa"}

TREE_FIELDS = ["name", "species", "age_estimate", "access", "transport",
               "story", "how_to_recognise"]
CITY_FIELDS = ["title", "meta_description", "intro", "question_title",
               "question_meta", "question_answer", "question_context"]


def tokens(chars):
    """Round-trip tokens for translating this many characters. Crude on purpose."""
    return (chars / 4) * 2.2


def load_cities():
    out = []
    for f in sorted(glob.glob("data/cities/*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        slug = os.path.basename(f)[:-5]
        chars = sum(len(d[k]) for k in CITY_FIELDS if isinstance(d.get(k), str))
        if isinstance(d.get("faq"), list):
            chars += len(json.dumps(d["faq"], ensure_ascii=False))
        trees = d.get("trees") or []
        for t in trees:
            chars += sum(len(t[k]) for k in TREE_FIELDS if isinstance(t.get(k), str))
        out.append({"slug": slug, "country": d.get("country", ""),
                    "trees": len(trees), "chars": chars})
    return out


def done_overlays():
    return {(f.split("/")[2], os.path.basename(f)[:-5])
            for f in glob.glob("data/i18n/*/*.json")}


def plan(cities, done, mapping):
    rows = collections.defaultdict(lambda: {"cities": 0, "trees": 0, "chars": 0})
    for c in cities:
        for lang, countries in mapping.items():
            if c["country"] in countries and (lang, c["slug"]) not in done:
                r = rows[lang]
                r["cities"] += 1
                r["trees"] += c["trees"]
                r["chars"] += c["chars"]
    return rows


def print_table(title, rows):
    print(f"\n{title}")
    print(f"  {'lang':5s} {'cities':>7s} {'trees':>7s} {'chars':>11s} {'~tokens':>11s}")
    tot = {"cities": 0, "trees": 0, "chars": 0}
    for lang in sorted(rows, key=lambda x: -rows[x]["chars"]):
        r = rows[lang]
        for k in tot:
            tot[k] += r[k]
        print(f"  {lang:5s} {r['cities']:7d} {r['trees']:7d} {r['chars']:11,d} "
              f"{tokens(r['chars']):11,.0f}")
    print(f"  {'':5s} {'-'*7} {'-'*7} {'-'*11} {'-'*11}")
    print(f"  {'all':5s} {tot['cities']:7d} {tot['trees']:7d} {tot['chars']:11,d} "
          f"{tokens(tot['chars']):11,.0f}")
    return tot



# Cities whose impressions are Google exact-phrase-operator queries rather than
# people. seolearn.py names them in DATA.md under NOT DEMAND with the standing
# instruction "read their impressions as zero, here and in the queue", and the
# proof that it means translations too is Brussels: 739 English impressions, a
# French overlay built on them, and 1 impression earned. Parsed rather than
# copied, because the list changes every morning.
def not_demand():
    try:
        txt = open("DATA.md", encoding="utf-8").read()
    except OSError:
        return set()
    i = txt.find("NOT DEMAND")
    if i < 0:
        return set()
    block = txt[i:i + 2000].split("\n\n")[0]
    return {m.group(1) for m in re.finditer(r"^\s{2,}([a-z0-9-]+)\s+i\d+", block, re.M)}


# Languages spoken in countries that have more than one. langcheck --next cannot
# see these at all: it offers one language per city, so a city already carrying
# its first language drops out of the queue with its second never considered.
MULTILINGUAL = {
    "Belgium": ["nl", "fr"],
    "Switzerland": ["de", "fr", "it"],
    "Luxembourg": ["fr", "de"],
}


def value(cities, done):
    """Rank by demand per character, not by demand.

    Raw impressions pick the big city every time, and the big city is usually
    the expensive one. What a short window wants is the page that buys the most
    demand per token, which is how a one-tree island beats a thirty-tree
    capital. Impressions are the ENGLISH twin's, which is the precondition
    rung 0b sets rather than a measure of the translated page.
    """
    skip = not_demand()
    imp = {}
    try:
        q = json.load(open("data/city-queue.json", encoding="utf-8"))
        rows = q if isinstance(q, list) else (q.get("cities") or [])
        for r in rows:
            s = r.get("slug") or r.get("city")
            if s:
                imp[s] = r.get("impressions_10d", 0) or 0
    except (OSError, ValueError):
        pass

    out = []
    for c in cities:
        langs = list(MULTILINGUAL.get(c["country"], []))
        for lang, countries in SHIPPING.items():
            if c["country"] in countries and lang not in langs:
                langs.append(lang)
        for lang in langs:
            if (lang, c["slug"]) in done or not c["chars"]:
                continue
            i = imp.get(c["slug"], 0)
            if i < 10:
                continue
            out.append({
                "lang": lang, "slug": c["slug"], "imp": i, "trees": c["trees"],
                "chars": c["chars"], "tok": tokens(c["chars"]),
                "per1k": i / (c["chars"] / 1000),
                "robot": c["slug"] in skip,
                "second": c["country"] in MULTILINGUAL,
            })
    out.sort(key=lambda r: -r["per1k"])

    print("\nTranslate next, ranked by English impressions per 1,000 characters")
    print("of work. Rows marked robot are seolearn NOT DEMAND: their impressions")
    print("are exact-phrase operator queries, so treat them as zero and skip.")
    print(f"\n  {'lang':5s} {'city':24s} {'imp':>5s} {'trees':>6s} {'~tok':>8s} {'imp/1k':>7s}")
    shown = 0
    for r in out:
        if r["robot"]:
            continue
        # A country being multilingual does not make every one of its cities
        # so: Geneva is francophone and Zurich German-speaking, whatever the
        # federal language list says. These rows are a prompt to decide, not
        # a recommendation to act on.
        flag = "  <- judgement call: 2nd language of a multilingual country" if r["second"] else ""
        print(f"  {r['lang']:5s} {r['slug']:24s} {r['imp']:5d} {r['trees']:6d} "
              f"{r['tok']:8,.0f} {r['per1k']:7.1f}{flag}")
        shown += 1
        if shown >= 15:
            break
    skipped = [r for r in out if r["robot"]]
    if skipped:
        print(f"\n  skipped as robot demand: " +
              ", ".join(f"{r['lang']}/{r['slug']} (i{r['imp']})" for r in skipped[:8]))
    return 0


def glossary(cities):
    """How much of the payload is the same string over and over."""
    uniq = collections.defaultdict(collections.Counter)
    for f in sorted(glob.glob("data/cities/*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for t in d.get("trees") or []:
            for k in TREE_FIELDS:
                v = t.get(k)
                if isinstance(v, str) and v.strip():
                    uniq[k][v.strip()] += 1
    print("\nRepetition per field. A field that repeats is a glossary, translated")
    print("once per language and reused, which costs nothing after the first time.")
    print(f"\n  {'field':18s} {'uses':>7s} {'unique':>7s} {'reuse':>6s} {'chars all':>11s} {'chars uniq':>11s}")
    for k in TREE_FIELDS:
        c = uniq[k]
        uses = sum(c.values())
        if not uses:
            continue
        un = len(c)
        ca = sum(len(s) * n for s, n in c.items())
        cu = sum(len(s) for s in c)
        print(f"  {k:18s} {uses:7d} {un:7d} {uses/un:5.1f}x {ca:11,d} {cu:11,d}")


def next_city(cities, done):
    print("\nCheapest untranslated city per language area (smallest payload first,")
    print("so a short window still finishes one rather than half-doing a big one):")
    by = collections.defaultdict(list)
    for c in cities:
        for lang, countries in SHIPPING.items():
            if c["country"] in countries and (lang, c["slug"]) not in done:
                by[lang].append(c)
    for lang in sorted(by):
        c = sorted(by[lang], key=lambda x: x["chars"])[0]
        print(f"  {lang}  {c['slug']:28s} {c['trees']:3d} trees  "
              f"{c['chars']:7,d} chars  ~{tokens(c['chars']):,.0f} tok")


def main():
    if not os.path.isdir("data/cities"):
        print("run me from the repo root")
        return 1
    cities = load_cities()
    done = done_overlays()

    if "--value" in sys.argv:
        return value(cities, done)
    if "--glossary" in sys.argv:
        glossary(cities)
        return 0
    if "--next" in sys.argv:
        next_city(cities, done)
        return 0

    n_en = sum(1 for c in cities if c["country"] in ENGLISH)
    print(f"{len(cities)} published cities, {sum(c['trees'] for c in cities)} trees.")
    print(f"{len(done)} city overlays exist across {len(set(l for l, _ in done))} languages.")
    print(f"{n_en} cities are in English-speaking countries and need nothing.")

    a = print_table("FULL-LOCAL, part 1: the seven languages we already ship, "
                    "cities still untranslated", plan(cities, done, SHIPPING))
    b = print_table("FULL-LOCAL, part 2: languages we do NOT have. Adding any is a "
                    "Contract J change (hard rule 7)", plan(cities, done, PROPOSED))

    print(f"\nFULL-LOCAL total: {a['cities'] + b['cities']} city sets, "
          f"{a['trees'] + b['trees']} trees, "
          f"~{tokens(a['chars'] + b['chars']):,.0f} tokens.")

    every = sum(c["chars"] for c in cities)
    print(f"FULL-MATRIX, every city in all 7 shipping languages, for contrast: "
          f"~{tokens(every * 7):,.0f} tokens.")
    print("\nThe gap between those two lines is the whole decision. The first is a")
    print("few weeks of night runs; the second is the subscription for months, and")
    print("it buys pages nobody searches for.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
