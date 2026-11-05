#!/usr/bin/env python3
"""What people answered to the Ancient Trees Plus question.

    python3 scripts/plus_answers.py          the ranking, every idea word for word,
                                             and how many asked to be told

The question sits under the ambassador on every city page (web,
site/src/components/PlusAsk.astro) and in the app's city sheet and Settings
(Screens/PlusAsk.swift). Hidde, 2026-11-04. Tables: supabase/plus-answers.sql.
Read with the service key (SUPABASE_SERVICE_KEY, or
~/.ancienttrees-supabase.env, as inbox.py).

HOW TO READ IT (the rules agreed before it went live, 2026-11-04):
  - It is a RANKING, not a rate. Only people who opened the question answer,
    so nothing here is a share of all visitors.
  - "Tell me" is the number that counts: a raised hand, not an opinion.
  - The options were shuffled per person; the position each winner was shown
    in is printed so a first-place bias can be seen.
  - The ideas are printed whole, never summed up (Hidde, 2026-10-25).
  - Decide before it runs what each outcome means; it ends at 100 answers or
    six weeks, whichever comes first.

PRIVACY: plus_answers holds no account, session or IP. plus_waitlist holds
account ids only; this prints their count, never who.
"""
import collections
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbox import SUPA, load_key  # noqa: E402

LABELS = {
    "walks": "Recommended tree walks for a city trip",
    "offline": "Download offline maps",
    "season": "Seasonal alerts when trees are at their best",
    "log": "A richer log of every tree you've collected",
    "none": "None of these",
}


def get(key, path):
    req = urllib.request.Request(SUPA + path, headers={"apikey": key, "Authorization": "Bearer " + key,
                                                       "Prefer": "count=exact"})
    with urllib.request.urlopen(req, timeout=30) as r:
        total = r.headers.get("Content-Range", "*/0").split("/")[-1]
        return json.load(r), total


def main():
    key = load_key()
    if not key:
        print("No service key (SUPABASE_SERVICE_KEY or ~/.ancienttrees-supabase.env).")
        return 1
    try:
        rows, _ = get(key, "/rest/v1/plus_answers?select=created_at,surface,lang,city,opened_from,choices,idea,shown_order"
                           "&order=created_at.asc&limit=5000")
        _, listed = get(key, "/rest/v1/plus_waitlist?select=created_at&limit=1")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("The plus tables are not there yet: paste supabase/plus-answers.sql into the Supabase SQL editor.")
            return 0
        raise
    answered = [r for r in rows if r.get("choices")]
    print(f"Plus question: {len(answered)} answers, {listed} asked to be told when it is here.\n")
    if not answered:
        return 0
    # Up to two per person (2026-11-05), so a column can add up to more than
    # the number of people; "Picked by" is people, not a share of the votes.
    count = collections.Counter(c for r in answered for c in r["choices"])
    first = collections.Counter()
    for r in answered:
        order = (r.get("shown_order") or "").split(",")
        if order and order[0] in r["choices"]:
            first[order[0]] += 1
    print("| Choice | Picked by | Of which it was shown first |")
    print("|---|---:|---:|")
    for k, n in count.most_common():
        print(f"| {LABELS.get(k, k)} | {n} | {first.get(k, 0)} |")
    by = collections.Counter(f"{r['surface']} / {r.get('opened_from') or '?'}" for r in answered)
    print("\nWhere it was opened: " + ", ".join(f"{k} {n}" for k, n in by.most_common()))
    ideas = [r for r in rows if (r.get("idea") or "").strip()]
    if ideas:
        print("\nTheir own words (the open question, word for word):\n")
        for r in ideas:
            print(f"- {r['created_at'][:10]} {r['surface']} {r.get('city') or ''} ({r.get('lang')}): {r['idea'].strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
