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
  python3 scripts/langcheck.py
"""
import datetime
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


def main():
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
        print("No language table in DATA.md yet, so there is nothing to compare.")
        print("The digest writes one from its next run; until then this is the baseline:\n")
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

    print("\nBy language, on the rule that a language failing on two cities gets no rollout:")
    for lang, results in sorted(by_lang.items()):
        n, tot = sum(results), len(results)
        call = ("ROLL OUT" if n >= 2 else
                "no verdict yet" if today < VERDICT_DUE else
                "DO NOT EXPAND" if tot >= 2 else "one city only, inconclusive")
        print("  %-3s %d of %d cities past their twin   %s" % (lang, n, tot, call))
    if today < VERDICT_DUE:
        print("\nBefore %s these are early readings, not verdicts. Contract J set four\n"
              "weeks for a reason: Malaga took eleven days to pass and six to show anything."
              % VERDICT_DUE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
