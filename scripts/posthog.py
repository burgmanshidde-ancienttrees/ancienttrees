#!/usr/bin/env python3
"""Ask the app's PostHog project a question from this Mac, without waiting
for tomorrow's digest.

Written 2026-10-10. Three trees were collected in the app the day before and
nobody could say which: the tree ids sit in PostHog, and its only read key was
a GitHub secret, which nothing can read back. So the daily digest was the only
way in, once a day. Hidde made a personal key for this machine.

The key lives OUTSIDE the repository, like the Supabase key:
    ~/.ancienttrees-posthog.env   with one line   POSTHOG_READ_KEY=phx_...
(scope Query: Read, project Ancient Trees). POSTHOG_READ_KEY in the
environment works too, which is how a runner would call it.

Our own testing is cut exactly as the digest cuts it (data/app-measure.json,
debug builds), by reusing the digest's own helpers rather than a copy of them.
--all keeps it in.

    python3 scripts/posthog.py --collected          trees collected, 14 days
    python3 scripts/posthog.py --collected 2        ... last 2 days
    python3 scripts/posthog.py --sync               changes that did not reach the account
    python3 scripts/posthog.py --install 3f2a       everything one install did, 14 days
    python3 scripts/posthog.py --day 2026-10-09     every event that day, per install
    python3 scripts/posthog.py --sql "SELECT event, count() FROM events GROUP BY 1"
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daily_digest as dd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.path.expanduser("~/.ancienttrees-posthog.env")


def read_key():
    key = os.environ.get("POSTHOG_READ_KEY")
    if key:
        return key
    try:
        for line in open(ENV, encoding="utf-8"):
            if line.strip().startswith("POSTHOG_READ_KEY="):
                return line.split("=", 1)[1].strip().strip('"\'')
    except OSError:
        pass
    return None


def tree_names():
    names = {}
    for fp in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        try:
            c = json.load(open(fp, encoding="utf-8"))
        except ValueError:
            continue
        for t in c.get("trees", []):
            names[t.get("id")] = "%s, %s" % (t.get("name"), c.get("city"))
    return names


def table(head, rows):
    rows = [[("" if v is None else str(v)) for v in r] for r in rows]
    w = [max(len(h), *(len(r[i]) for r in rows)) if rows else len(h)
         for i, h in enumerate(head)]
    print("  ".join(h.ljust(w[i]) for i, h in enumerate(head)))
    for r in rows:
        print("  ".join(v.ljust(w[i]) for i, v in enumerate(r)))
    if not rows:
        print("(nothing)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--collected", nargs="?", const=14, type=int, metavar="DAYS")
    g.add_argument("--sync", nargs="?", const=14, type=int, metavar="DAYS")
    g.add_argument("--install", metavar="ID_PREFIX")
    g.add_argument("--day", metavar="YYYY-MM-DD")
    g.add_argument("--sql")
    ap.add_argument("--all", action="store_true", help="keep our own testing in")
    a = ap.parse_args()

    key = read_key()
    if not key:
        print("No PostHog key. Put POSTHOG_READ_KEY=phx_... in %s "
              "(PostHog EU > Settings > Personal API keys, scope Query: Read)."
              % ENV)
        return 1
    project, why = dd._ph_project(key)
    if not project:
        print("The key reaches no project: %s" % why)
        return 1
    ours = "" if a.all else dd._ph_ours()[0]
    and_ours = ("AND " + ours) if ours else ""

    def q(sql):
        return dd._posthog(sql, key, project)

    if a.sql:
        for r in q(a.sql):
            print("  ".join(str(v) for v in r))
        return 0

    names = tree_names()
    if a.collected is not None:
        rows = q("""
            SELECT timestamp, properties.tree, substring(distinct_id, 1, 8),
                   properties.build, properties.signed_in, properties.app_version
            FROM events
            WHERE event = 'tree_visited'
                  AND timestamp >= now() - INTERVAL %d DAY %s
            ORDER BY timestamp DESC""" % (a.collected, and_ours))
        table(["when (UTC)", "tree", "install", "build", "signed in", "version"],
              [[str(r[0])[:16].replace("T", " "),
                names.get(r[1], r[1]), r[2], r[3], r[4] or "?", r[5]]
               for r in rows])
    elif a.sync is not None:
        rows = q("""
            SELECT timestamp, event, properties.tree, properties.why,
                   substring(distinct_id, 1, 8), properties.app_version
            FROM events
            WHERE event IN ('sync_failed', 'sync_skipped')
                  AND timestamp >= now() - INTERVAL %d DAY %s
            ORDER BY timestamp DESC""" % (a.sync, and_ours))
        table(["when (UTC)", "event", "tree", "why", "install", "version"],
              [[str(r[0])[:16].replace("T", " "), r[1],
                names.get(r[2], r[2]), r[3], r[4], r[5]] for r in rows])
    elif a.install:
        pre = a.install.replace("'", "")
        rows = q("""
            SELECT timestamp, event, properties.tree, properties.tab,
                   properties.build, properties.signed_in
            FROM events
            WHERE startsWith(distinct_id, '%s')
                  AND timestamp >= now() - INTERVAL 14 DAY
            ORDER BY timestamp""" % pre)
        table(["when (UTC)", "event", "tree", "tab", "build", "signed in"],
              [[str(r[0])[:16].replace("T", " "), r[1],
                names.get(r[2], r[2] or ""), r[3], r[4], r[5] or "?"]
               for r in rows])
    elif a.day:
        day = a.day.replace("'", "")
        rows = q("""
            SELECT substring(distinct_id, 1, 8), any(properties.build),
                   count(), groupUniqArray(event)
            FROM events
            WHERE toDate(timestamp) = toDate('%s') %s
            GROUP BY distinct_id ORDER BY count() DESC""" % (day, and_ours))
        table(["install", "build", "events", "what"],
              [[r[0], r[1], r[2], ", ".join(sorted(r[3]))] for r in rows])
    return 0


if __name__ == "__main__":
    sys.exit(main())
