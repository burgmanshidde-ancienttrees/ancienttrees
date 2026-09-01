#!/usr/bin/env python3
"""Is a language worth investing in? Read the verdict, do not remember it.

Contract J v1.13 wrote the measure down before anything was built, which is
what made the Malaga test worth running: within four weeks of indexing, a
translated set should exceed its English twin's impressions AND beat its
position on the target-language query. This reads that back.

data/language-test.json holds what each English twin earned on 2026-08-22, the
day all 23 overlays went live. That snapshot is the whole point: a week from
now nobody can tell a page that moved from a page that was always fine, and
the number is unrecoverable once the window slides.

Needs no credentials. The daily digest holds the Search Console secrets and
commits its readback into data/city-queue.json every morning, so this runs
anywhere the repo is checked out.

The honest limit, stated because the number will be over-read otherwise:
impressions_10d in the queue is the ENGLISH page's, since the queue is a list
of cities. The per-language readback lives in DATA.md's language table, which
daily_digest.language_lines() started writing the same day. Until a digest has
run since, this reports the baseline and says so rather than inventing a
delta.

Usage:
  python3 scripts/langcheck.py          # the verdict per language
  python3 scripts/langcheck.py --next   # which city to translate next, per language area
"""
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "data", "language-test.json")
DATA_MD = os.path.join(ROOT, "DATA.md")
VERDICT_DUE = datetime.date(2026, 9, 19)  # four weeks after the overlays went live


def latest_language_table():
    """The newest 'language test' table DATA.md carries, as {(lang, city): row}."""
    if not os.path.exists(DATA_MD):
        return {}
    txt = open(DATA_MD, encoding="utf-8").read()
    block = re.search(r"\*\*The language test\*\*.*?\n\n((?:\|.*\n)+)", txt)
    if not block:
        return {}
    out = {}
    for line in block.group(1).splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6 or cells[0] in ("Lang", "---") or set(cells[0]) <= {"-", ":"}:
            continue
        try:
            out[(cells[0], cells[1])] = {
                "clicks": int(cells[2]), "impressions": int(cells[3]),
                "position": float(cells[4]), "en_impressions": int(cells[5])}
        except ValueError:
            continue
    return out


# Which language a city's country reads in. A language goes onto the cities of
# its OWN language area and never onto whichever English page performs best,
# which is Contract J v1.13's measured finding (data/research/language-demand.json:
# local-language demand runs 18 to 53 percent of English, every other language
# 3 to 21). Belgium is deliberately absent: Brussels is French and Antwerp is
# Dutch, so the country cannot answer it and a guess here would be worse than
# the gap.
AREA = {
    "Spain": "es", "Mexico": "es", "Argentina": "es", "Chile": "es",
    "Colombia": "es", "Peru": "es", "Uruguay": "es", "Cuba": "es",
    "Italy": "it",
    "Netherlands": "nl",
    "Germany": "de", "Austria": "de",
    # Switzerland is not one language area and mapping it whole was wrong: it
    # put Geneva, which is francophone and already has a French overlay, at the
    # top of the German list on 2026-09-01. Cities decide it, not the country.
    "Switzerland": None,
    "Portugal": "pt", "Brazil": "pt",
    "France": "fr",
    "Japan": "ja",
}


# Countries that are not one language area are decided per city instead.
CITY_AREA = {"Geneva": "fr", "Lausanne": "fr", "Zurich": "de", "Bern": "de",
             "Basel": "de", "Lugano": "it", "Brussels": "fr", "Antwerp": "nl",
             "Ghent": "nl", "Bruges": "nl"}


def english_impressions():
    """{city slug: (clicks, impressions)} from DATA.md's newest depth roster.

    That table is the only place a run can read per-city Search Console
    numbers: the credentials live in data-digest.yml and never in a night run
    (CLAUDE.md, rule two). It lists every city clearing 10 impressions, so a
    city missing from it is a city under 10, which is exactly the answer this
    needs and not a gap.
    """
    if not os.path.exists(DATA_MD):
        return {}
    txt = open(DATA_MD, encoding="utf-8").read()
    block = re.search(r"\*\*Depth is allowed on these cities\*\*.*?\n\n((?:\|.*\n)+)", txt)
    if not block:
        return {}
    out = {}
    for line in block.group(1).splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        try:
            out[cells[0]] = (int(cells[1]), int(cells[2]))
        except ValueError:
            continue
    return out


def translated():
    """{(lang, slug)} that already have an overlay on disk."""
    root = os.path.join(ROOT, "data", "i18n")
    return {(os.path.basename(os.path.dirname(f)), os.path.basename(f)[:-5])
            for f in glob.glob(os.path.join(root, "*", "*.json"))}


def show_next():
    """The highest-impression untranslated city per language area.

    Exists because the pick was made by FAME on the rollout day and the file
    says to make it by impressions (CLAUDE.md rung 0b). On 2026-08-22 the
    Japanese three were chosen as Tokyo, Kyoto and Osaka; Fukuoka stood at 27
    impressions that morning against Osaka's 24 and Kyoto's 19, was skipped,
    and is now the largest Japanese page on the site with no Japanese version.
    Nobody has to remember that with this printed.
    """
    imps = english_impressions()
    if not imps:
        print("No 'Depth is allowed on these cities' table in DATA.md; cannot rank.")
        return 1
    have = translated()
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        slug = os.path.basename(f)[:-5]
        try:
            city = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        lang = CITY_AREA.get(city.get("city", "")) or AREA.get(city.get("country", ""))
        if not lang or (lang, slug) in have:
            continue
        clicks, impressions = imps.get(slug, (0, 0))
        rows.append((impressions, clicks, lang, slug, len(city.get("trees", []))))
    rows.sort(reverse=True)

    print("Translate next: the untranslated city with the most English impressions,")
    print("per language area. The precondition is the whole rung: a page nobody")
    print("finds in English becomes a page nobody finds in two languages.\n")
    print("| Lang | City | English impressions | Clicks | Trees |")
    print("|---|---|---:|---:|---:|")
    seen = set()
    for impressions, clicks, lang, slug, trees in rows:
        if lang in seen or impressions == 0:
            continue
        seen.add(lang)
        print("| %s | %s | %d | %d | %d |" % (lang, slug, impressions, clicks, trees))

    print("\nThe rest of the queue, biggest first:")
    for impressions, clicks, lang, slug, trees in rows[:15]:
        if impressions == 0:
            continue
        print("  %-3s %-20s %4d impressions  %2d clicks  %2d trees"
              % (lang, slug, impressions, clicks, trees))
    under = [r for r in rows if r[0] == 0]
    print("\n%d more cities in these language areas sit under 10 impressions in\n"
          "English and are not worth translating yet." % len(under))
    return 0


def main():
    if "--next" in sys.argv:
        return show_next()
    if not os.path.exists(BASE):
        print("missing data/language-test.json; the baseline was never taken")
        return 1
    doc = json.load(open(BASE, encoding="utf-8"))
    live = latest_language_table()
    taken = doc.get("taken", "?")
    today = datetime.date.today()

    print("Language test, baseline taken %s, verdict due %s (%d days)"
          % (taken, VERDICT_DUE, (VERDICT_DUE - today).days))
    print("Measure: a translated set should pass its English twin's impressions.\n")

    if not live:
        # Distinguish "the digest has not run" from "the digest ran and wrote
        # nothing", because those need opposite responses and I could not tell
        # them apart for five days. language_lines() was defined, committed,
        # and never called: the patch that was supposed to wire it in targeted
        # a call signature that had already changed. The absence looked
        # exactly like an honest "no impressions yet".
        newest = re.search(r"^## (\d{4}-\d{2}-\d{2}) \(previous UTC day\)", 
                           open(DATA_MD, encoding="utf-8").read(), re.M) if os.path.exists(DATA_MD) else None
        if newest and newest.group(1) > taken:
            print("BROKEN: the digest has run since the baseline (newest entry %s) and wrote"
                  % newest.group(1))
            print("no language table. language_lines() is not reaching DATA.md. Check that")
            print("scripts/daily_digest.py actually CALLS it, not just defines it.\n")
        else:
            print("No language table in DATA.md yet and no digest has run since the baseline.\n")
        print("The baseline, unchanged:\n")
        for r in sorted(doc["baseline"], key=lambda x: -x["en_impressions_10d"]):
            print("  %-3s %-14s %2d trees   English twin %4d impressions"
                  % (r["lang"], r["city"], r["trees"], r["en_impressions_10d"]))
        return 0

    by_lang = {}
    print("| Lang | City | Translated | English twin | Passed? |")
    print("|---|---|---:|---:|---|")
    for r in sorted(doc["baseline"], key=lambda x: -x["en_impressions_10d"]):
        row = live.get((r["lang"], r["city"]))
        got = row["impressions"] if row else 0
        en = row["en_impressions"] if row else r["en_impressions_10d"]
        passed = got > en and en > 0
        by_lang.setdefault(r["lang"], []).append(passed)
        print("| %s | %s | %d | %d | %s |"
              % (r["lang"], r["city"], got, en, "yes" if passed else "not yet"))

    # Absolute impressions sit beside the ratio because a weak twin flatters
    # it: on 2026-09-01 Japanese ran at 99 percent of its English twin and
    # that was 103 impressions against 104, while Spanish at 28 percent
    # delivered 184. A language read on the ratio alone reads backwards.
    totals = {}
    for (lang, _city), row in live.items():
        t = totals.setdefault(lang, [0, 0, 0])
        t[0] += row["clicks"]
        t[1] += row["impressions"]
        t[2] += row["en_impressions"]

    print("\nBy language, on the rule that a language failing on two cities gets no rollout:")
    for lang, results in sorted(by_lang.items()):
        n, tot = sum(results), len(results)
        call = ("ROLL OUT" if n >= 2 else
                "no verdict yet" if today < VERDICT_DUE else
                "DO NOT EXPAND" if tot >= 2 else "one city only, inconclusive")
        c, i, en = totals.get(lang, (0, 0, 0))
        share = ("%d%% of twin" % round(i / en * 100)) if en else "no twin traffic"
        print("  %-3s %d of %d cities past their twin   %4d impressions, %2d clicks, %-15s %s"
              % (lang, n, tot, i, c, share, call))
    if today < VERDICT_DUE:
        print("\nBefore %s these are early readings, not verdicts. Contract J set four\n"
              "weeks for a reason: Malaga took eleven days to pass and six to show anything."
              % VERDICT_DUE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
