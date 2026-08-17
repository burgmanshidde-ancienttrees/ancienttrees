#!/usr/bin/env python3
"""Recompute the queue's `score` from travel demand and measured yield.

Hidde, 2026-08-15: "I don't think Wikipedia impression gives a good
representation of English tourist can't we make our top 250 smarter?"

Until today `score` was demand times yield where demand was English Wikipedia
pageviews and yield came from a fame-penalty band. Both halves were tested on
2026-08-15 against the one outcome we actually care about, `impressions_10d`
from the Search Console readback, on the 55 published cities Google has
indexed. Both halves lost.

    English Wikipedia pageviews   rho +0.23   <- the old demand term
    English Wikivoyage pageviews  rho +0.32   <- the new one
    English share of pageviews    rho +0.11   <- the anglophone hypothesis

WHAT CHANGED, and why each change is evidence rather than taste.

1. DEMAND IS TRAVEL INTENT. `travel` (English Wikivoyage pageviews, see
   travel_demand.py) replaces `demand` (English Wikipedia pageviews) as the
   size term. Someone reading a Wikivoyage article is planning a trip.
   Potsdam is famous for a conference; nobody packs a bag for it.

2. THE FAME PENALTY IS GONE. CITY_QUEUE.md was built on "the more famous a
   city is, the worse we do there", derived from ten cities in a digest, and
   it paid out as a band that multiplied contested cities by 1.08 and quiet
   ones by 2.50. On all 111 published cities it does not survive. Split by
   travel demand into thirds, impressions per 100k travel views run 206 / 224
   / 184, which is flat, and clicks run 12 / 23 / 33, which points the other
   way outright. So the predicted yield is now FLAT: we stopped penalising
   fame, and deliberately did not start rewarding it, because the click counts
   are small and half the site is still unindexed.

3. MEASURED YIELD STAYS, because it is the one term that was never a guess.
   A city where Search Console has spoken scores on what it actually earns per
   unit of travel demand, normalised so the median measured city sits at 1.0.

4. PUBLISHED AND NEVER RANKED still scores 0.25, and this is now the SHAKIEST
   rule in the file rather than the firmest. It was written when absence of
   clicks on a live page read as evidence of no demand. Since then we learned
   that 346 pages sit "Discovered - currently not indexed", so London,
   Edinburgh, Portland, Hobart and Quebec City all show zero while never having
   been crawled. That is not evidence of low yield, it is evidence of no crawl.
   Kept at 0.25 for now because demoting a page we cannot see is still the
   safer error, but it should be revisited the moment indexing improves, and
   any city on it deserves a look before it is written off.

WHAT DID NOT CHANGE: `ease` (register supply makes a city cheap to open, and
that is measured at 0.4k tokens per tree against 27k for research), the
four-tree floor, the targets, and every hard rule. This file changes the ORDER
of work and nothing else.

    python3 scripts/rescore.py            # show what would change
    python3 scripts/rescore.py --write    # write score and basis into the queue
"""
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "city-queue.json")

NEVER_RANKED_YIELD = 0.25
PREDICTED_YIELD = 1.0

# Countries Hidde has taken off the list for now. They keep their row, their
# travel demand and their register supply, and they lose their rank, so this is
# a pause rather than a deletion and reversing it is deleting a line here.
#
# India, 2026-08-15: "Let's keep India out of the top 250 for now. It's a huge
# country I don't want to focus on now." Four cities were affected, all
# unpublished, none deep enough to have earned anything: Delhi (rank 33),
# Mumbai (59), Jaipur (72), Agra (91). The travel-demand rescore that morning
# had lifted them, which is what surfaced the question at all.
#
# A run may NOT add or remove a country here on its own. This is a strategy
# call about where the project points, which is Hidde's, and the queue is
# deliberately the one place it cannot be quietly re-derived.
PAUSED_COUNTRIES = {"India"}

# Named exceptions to the wealth tier below, one line per place, each carrying
# the words that put it there. This exists because Hidde named a single place
# rather than a country, 2026-08-17: "En zorg dat alle echt aantrekkelijke
# eilanden in de lijst staan Bali lijkt me erg aantrekkelijk."
#
# Bali is the case where the two readings of his own rich-tourist rule come
# apart. The rule is written as COUNTRY VISITED, and its comment says his India
# decision settles that reading, so Indonesia sitting in the lower-middle tier
# pauses Bali despite 9,950 travel views, which is Dubai and Jerusalem
# territory. Read as VISITOR WEALTH instead, Bali is one of the most obvious
# rich-tourist destinations on earth. He has now named the place, so the place
# is exempt and the country is not: Jakarta, Yogyakarta and Ubud stay paused,
# because he did not name them and widening this on his behalf is exactly what
# the note below forbids.
#
# The same restriction applies here as to the table below. A run may add a place
# ONLY when Hidde has named it, and the quote goes in this comment beside it.
FOCUS_EXCEPTIONS = {"Bali"}

# Hidde, 2026-08-15, immediately after the India pause: "I want to focus on
# cities for rich tourists." The India cut was the specific case; this is the
# rule behind it, and it is deliberately about the COUNTRY VISITED rather than
# the wealth of the visitor, because those two readings give very different
# lists and his own India decision settles which one he meant. Agra and Jaipur
# are visited by affluent Westerners in large numbers and he cut them anyway.
#
# The tier is the World Bank income classification, used because it is a
# published, citable line rather than a list of countries somebody felt good
# about. High income scores full, upper-middle scores half, everything below is
# paused with its row and its data kept.
#
# What this costs, stated plainly because it is not free: it drops real tourist
# cities the product would serve well, Chiang Mai, Marrakech, Mexico City,
# Ho Chi Minh City, Ubud and Bogota among them, several of which sat in the top
# 40 that morning. It is a focus decision, not a claim that those cities are
# bad. Reversing it is editing this table.
UPPER_MIDDLE = {
    "Mexico", "Brazil", "Argentina", "Colombia", "Peru", "South Africa",
    "Thailand", "China", "Malaysia", "Turkey", "Serbia", "Bosnia and Herzegovina",
    "North Macedonia", "Albania", "Montenegro", "Russia", "Cuba", "Ecuador",
}
LOW_AND_LOWER_MIDDLE = {
    "India", "Vietnam", "Indonesia", "Philippines", "Egypt", "Morocco",
    "Cambodia", "Sri Lanka", "Nepal", "Pakistan", "Bangladesh", "Kenya",
    "Tanzania", "Nigeria", "Ukraine", "Bolivia", "Jordan", "Tunisia",
}


def wealth_factor(country):
    """1.0 high income, 0.5 upper-middle, None means paused."""
    if country in PAUSED_COUNTRIES or country in LOW_AND_LOWER_MIDDLE:
        return None
    return 0.5 if country in UPPER_MIDDLE else 1.0


def measured_yield(c):
    """Impressions per 1,000 Wikivoyage views. None when unmeasurable."""
    t = c.get("travel") or 0
    if t < 500:
        # Too little travel demand for a ratio to mean anything: a city on 40
        # views and 2 impressions would otherwise outscore Rome.
        return None
    return (c.get("impressions_10d") or 0) / (t / 1000.0)


def main():
    write = "--write" in sys.argv
    doc = json.load(open(QUEUE, encoding="utf-8"))
    cities = doc["cities"]

    ratios = [measured_yield(c) for c in cities
              if c["status"] == "published" and (c.get("impressions_10d") or 0) > 0]
    ratios = [r for r in ratios if r]
    mid = statistics.median(ratios)
    print("median measured yield: %.2f impressions per 1,000 travel views "
          "(%d cities)" % (mid, len(ratios)))

    before = {c["city"]: c.get("rank") for c in cities}
    paused = []
    for c in cities:
        travel = c.get("travel") or 0
        base = travel / 1000.0
        wealth = wealth_factor(c.get("country", ""))
        if wealth is None and c.get("city") in FOCUS_EXCEPTIONS:
            wealth = 1.0
        if wealth is None:
            # Paused, not deleted: the row, its travel demand and its register
            # supply all stay, so lifting the pause is a one-line edit and no
            # research is lost. A published city is never unranked this way,
            # because retiring a live page is hard rule 3 territory.
            if c["status"] != "published":
                paused.append(c)
                c["score"] = None
                c["basis"] = "paused: outside the focus countries"
                continue
            wealth = 1.0
        base *= wealth
        if c["status"] == "published" and (c.get("impressions_10d") or 0) > 0:
            my = measured_yield(c)
            if my is not None:
                c["score"] = round(base * (my / mid), 2)
                c["basis"] = "measured"
                continue
        if c["status"] == "published":
            c["score"] = round(base * NEVER_RANKED_YIELD, 2)
            c["basis"] = "published, never ranked (may be uncrawled)"
        else:
            c["score"] = round(base * PREDICTED_YIELD, 2)
            c["basis"] = "predicted (travel demand)"
        if not travel:
            c["score"] = None
            c["basis"] = "no travel demand measured"

    ranked = sorted([c for c in cities if c.get("score") is not None],
                    key=lambda c: (-(c["score"] * (c.get("ease") or 1.0)), c["city"]))
    for n, c in enumerate(ranked, 1):
        c["work_score"] = round(c["score"] * (c.get("ease") or 1.0), 2)
        c["rank"] = n
    for c in cities:
        if c.get("score") is None:
            c["rank"] = None

    print("\nBiggest climbers (old rank -> new):")
    moves = [(before.get(c["city"]) - c["rank"], c["city"], c) for c in ranked
             if before.get(c["city"]) and c["rank"]]
    for d, _, c in sorted(moves, key=lambda m: (-m[0], m[1]))[:12]:
        print("  +%-4d %-20s %4d -> %-4d  travel %8s  register %s"
              % (d, c["city"], before[c["city"]], c["rank"],
                 "{:,}".format(c.get("travel") or 0), c.get("register") or 0))
    print("\nBiggest fallers:")
    for d, _, c in sorted(moves, key=lambda m: (m[0], m[1]))[:12]:
        print("  %-5d %-20s %4d -> %-4d  travel %8s  wikipedia %s"
              % (d, c["city"], before[c["city"]], c["rank"],
                 "{:,}".format(c.get("travel") or 0),
                 "{:,}".format(c.get("demand") or 0)))

    if write:
        cities.sort(key=lambda c: (c["rank"] is None, c["rank"] or 0, c["city"]))
        json.dump(doc, open(QUEUE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("\nwrote new score, basis and rank into data/city-queue.json")
    else:
        print("\n(dry run; pass --write to keep it)")


if __name__ == "__main__":
    main()
