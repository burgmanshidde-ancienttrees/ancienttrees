#!/usr/bin/env python3
"""What outreach actually produced, per recipient type and per country.

Joins data/outreach-sent.json with data/outreach-replies.json. Exists because
until 2026-08-22 the reply rate was a feeling: replies lived as loose files in
drafts/ and the only way to count them was to read filenames.

    python3 scripts/outreach_stats.py
"""
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    sent = json.load(open(os.path.join(ROOT, "data", "outreach-sent.json")))["sent"]
    reps = json.load(open(os.path.join(ROOT, "data", "outreach-replies.json")))["replies"]
    contacts = {}
    import glob
    for f in glob.glob(os.path.join(ROOT, "data", "outreach-contacts*.json")):
        for c in json.load(open(f)):
            e = (c.get("email") or "").lower().strip()
            if e:
                contacts.setdefault(e, c)
    return sent, reps, contacts


def main():
    sent, reps, contacts = load()
    replied = {(r.get("to_address") or "").lower() for r in reps if r.get("to_address")}
    # human replies only: an out-of-office proves nothing about interest
    human = {(r.get("to_address") or "").lower() for r in reps
             if r.get("to_address") and r.get("kind") != "auto"}

    per_type = collections.defaultdict(lambda: [0, 0])
    per_country = collections.defaultdict(lambda: [0, 0])
    per_batch = collections.defaultdict(lambda: [0, 0])
    seen = set()
    for s in sent:
        a = s["to"].lower()
        if a in seen:
            continue
        seen.add(a)
        c = contacts.get(a, {})
        t = c.get("type", "unknown")
        country = c.get("country", "unknown")
        for bucket, key in ((per_type, t), (per_country, country),
                            (per_batch, s.get("batch", "?"))):
            bucket[key][0] += 1
            if a in human:
                bucket[key][1] += 1

    def table(title, bucket, minimum=1):
        print(f"\n{title}")
        print(f"  {'':26} {'mailed':>6} {'replied':>8} {'rate':>6}")
        for k, (n, r) in sorted(bucket.items(), key=lambda kv: -kv[1][1]):
            if n < minimum:
                continue
            print(f"  {str(k)[:26]:26} {n:6} {r:8} {(100*r/n if n else 0):5.0f}%")

    total = len(seen)
    print(f"outreach: {total} addresses mailed, {len(human)} human replies, "
          f"{len(replied)-len(human)} automatic")
    table("By recipient type", per_type)
    table("By country", per_country, minimum=2)
    table("By batch", per_batch)

    kinds = collections.Counter(r.get("kind") for r in reps if r.get("kind") != "auto")
    print("\nWhat the replies were")
    for k, n in kinds.most_common():
        print(f"  {str(k)[:26]:26} {n:6}")

    owed = [r for r in reps if r.get("needs_reply")]
    if owed:
        print(f"\nOWED A REPLY BY US ({len(owed)}):")
        for r in owed:
            print(f"  - {r['org']} ({r.get('date') or 'date unknown'})"
                  f"{'  draft: ' + r['draft'] if r.get('draft') else '  NO DRAFT YET'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
