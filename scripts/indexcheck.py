#!/usr/bin/env python3
"""Did the manual Request Indexing submissions do anything?

Hidde submitted ten URLs by hand in Search Console on 2026-08-16, said he
would rather not repeat it, and asked whether it was worth it. That question
has a short shelf life: without a baseline written down on the day, a week
later nobody can tell a page that moved from a page that was always fine. So
data/index-requests.json holds what was submitted and what each URL earned at
the time, and this script reads it back against the impressions the daily
digest writes into data/city-queue.json.

It needs no credentials. The digest holds the Search Console secrets and
commits its readback into the queue every morning, so this runs anywhere the
repo is checked out, which is the same reason passcheck.py reads files rather
than APIs.

The comparison that matters is not "did the submitted cities move" but "did
they move MORE than the ones we did not submit". Google crawls on its own
eventually, and a run that only looked at the ten would credit the requests
for whatever was going to happen anyway. The control group is weak and says so
in its own note: the submitted cities are bigger and in more demand than most
of the control, so a positive result is suggestive rather than proof.

Usage:
  python3 scripts/indexcheck.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUESTS = os.path.join(ROOT, "data", "index-requests.json")
QUEUE = os.path.join(ROOT, "data", "city-queue.json")


def load(path):
    if not os.path.exists(path):
        print("missing: %s" % os.path.relpath(path, ROOT))
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def summarise(label, slugs, by_slug, baseline):
    """One line per group: how many now show impressions, and how many in total.

    Reported as a share rather than a mean, because the mean of a handful of
    small counts moves on one city and reads as a trend when it is one page."""
    rows = [(s, by_slug.get(s)) for s in slugs]
    known = [(s, c) for s, c in rows if c is not None]
    missing = [s for s, c in rows if c is None]
    moved = [(s, c["impressions_10d"], c["clicks_10d"]) for s, c in known
             if (c.get("impressions_10d") or 0) > baseline.get(s, 0)]
    imps = sum((c.get("impressions_10d") or 0) for _, c in known)
    clicks = sum((c.get("clicks_10d") or 0) for _, c in known)
    print("\n%s (%d cities)" % (label, len(known)))
    print("  now showing impressions: %d of %d (%.0f%%)"
          % (len(moved), len(known), 100.0 * len(moved) / len(known) if known else 0))
    print("  impressions across the group: %d      clicks: %d" % (imps, clicks))
    if moved:
        for s, i, c in sorted(moved, key=lambda x: -x[1]):
            print("    %-14s %4d impressions, %d clicks" % (s, i, c))
    if missing:
        print("  not found in the queue: %s" % ", ".join(missing))
    return len(moved), len(known), imps


def main():
    reqs, queue = load(REQUESTS), load(QUEUE)
    if not reqs or not queue:
        return 1
    by_slug = {c.get("slug"): c for c in queue["cities"]}

    for r in reqs["requests"]:
        submitted = [u["slug"] for u in r["urls"]]
        baseline = {u["slug"]: u.get("impressions_at_request", 0) for u in r["urls"]}
        control = r.get("control", [])
        for s in control:
            baseline.setdefault(s, 0)

        print("=" * 66)
        print("Request Indexing, submitted %s by %s" % (r["date"], r.get("by", "?")))
        print("  %s" % r.get("why", ""))
        print("  Baseline window: %s. Queue read: whatever the last digest wrote."
              % r.get("baseline_window", "?"))

        sm, sn, si = summarise("SUBMITTED", submitted, by_slug, baseline)
        cm, cn, ci = summarise("CONTROL, not submitted", control, by_slug, baseline)

        print("\n" + "-" * 66)
        srate = 100.0 * sm / sn if sn else 0
        crate = 100.0 * cm / cn if cn else 0
        print("Submitted: %.0f%% now visible.  Control: %.0f%% now visible." % (srate, crate))
        if sm == 0 and cm == 0:
            print("VERDICT: nothing has moved in either group yet. Google's data lags "
                  "2-3 days and a crawl after a request usually lands within a week, "
                  "so this is expected before roughly %s. Ask again then." % "2026-08-23")
        elif srate > crate + 20:
            print("VERDICT: the submitted cities moved clearly more than the ones left "
                  "alone. The requests did something. Worth knowing that this buys a "
                  "crawl, not a ranking, and it does not scale: the fix that removes "
                  "the need is links, since a linked page gets crawled without asking.")
        elif cm > 0 and srate <= crate + 20:
            print("VERDICT: the control moved about as much as the submitted ten, so "
                  "Google was getting there anyway and the hand work bought little. "
                  "Do not repeat it.")
        else:
            print("VERDICT: partial movement, too early or too small to call. Re-run "
                  "in a few days rather than concluding from this.")
    if reqs.get("caveat"):
        print("\nCaveat carried from the data file:\n  %s" % reqs["caveat"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
