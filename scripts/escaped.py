#!/usr/bin/env python3
"""Bugs a PERSON found that no test caught, and the test that catches them now.

Hidde, 2026-11-08, after a day of finding them himself (Discover's ambassador
seat that ignored his tap, pins that blinked after a fresh install) and asking
how a professional tester would judge this: the measure every team keeps is
the escaped defect, a bug that got past the tests to a person. Each one is a
lesson about the tests, and it is only learned when a test that would have
caught it exists. So:

  - a bug found by Hidde or a reader goes in data/code-audit.json as a BUG row
    with `found_by`, which makes it an open bug in the digest's quality line
    and rung-2 work (health.py), like the code review's own findings;
  - it is closed only with `test` (the test that now catches it) or
    `no_test_reason` (why no machine can), checked by qa.py
    (`check_an_escaped_bug_has_a_test()`);
  - `--report` says how many bugs people found against how many the tests
    found, over a window: the number that should fall.

    python3 scripts/escaped.py --add APP "Discover's ambassador seat ignores a tap" \\
        --file ios/AncientTrees/AncientTrees/Screens/Home.swift:851 [--found-by hidde]
    python3 scripts/escaped.py --test <id> AncientTreesUITests/AmbassadorAskWalk
    python3 scripts/escaped.py --fixed <id> <commit> [--no-test "why no machine can"]
    python3 scripts/escaped.py --report [--days 30]
"""
import argparse
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "code-audit.json")
PEOPLE = ("hidde", "reader")


def load():
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


def save(d):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write("\n")


def row(d, rid):
    for r in d.get("findings", []):
        if r.get("id") == rid:
            return r
    sys.exit("no row %s in data/code-audit.json" % rid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", nargs=2, metavar=("SURFACE", "SUMMARY"))
    ap.add_argument("--file", default="")
    ap.add_argument("--found-by", default="hidde", choices=PEOPLE + ("test", "review"))
    ap.add_argument("--test", nargs=2, metavar=("ID", "TEST"))
    ap.add_argument("--fixed", nargs=2, metavar=("ID", "COMMIT"))
    ap.add_argument("--no-test", metavar="WHY")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()
    today = datetime.date.today().isoformat()
    d = load()
    rows = d.setdefault("findings", [])

    if a.add:
        surface, summary = a.add[0].upper(), a.add[1]
        if surface not in ("APP", "WEB"):
            sys.exit("surface is APP or WEB")
        slug = re.sub(r"[^a-z0-9]+", "-", summary.lower()).strip("-")[:40]
        rid = "ESC-%s-%s" % (today, slug)
        rows.append({"id": rid, "surface": surface, "kind": "BUG", "file": a.file,
                     "summary": summary, "first_seen": today, "status": "open",
                     "found_by": a.found_by})
        save(d)
        print("added %s (open bug, found by %s)" % (rid, a.found_by))
        return 0

    if a.test:
        r = row(d, a.test[0])
        r["test"] = a.test[1]
        save(d)
        print("%s is now caught by %s" % (r["id"], a.test[1]))
        return 0

    if a.fixed:
        r = row(d, a.fixed[0])
        if r.get("found_by") in PEOPLE and not r.get("test") and not a.no_test:
            sys.exit("%s was found by a person: name the test that catches it now "
                     "(--test) or say why no machine can (--no-test \"why\")" % r["id"])
        if a.no_test:
            r["no_test_reason"] = a.no_test
        r["status"] = "fixed"
        r["fixed_in"] = a.fixed[1]
        save(d)
        print("%s fixed in %s" % (r["id"], a.fixed[1]))
        return 0

    if a.report:
        since = (datetime.date.today() - datetime.timedelta(days=a.days)).isoformat()
        recent = [r for r in rows if r.get("kind") == "BUG" and r.get("first_seen", "") >= since]
        by_people = [r for r in recent if r.get("found_by") in PEOPLE]
        by_tests = [r for r in recent if r.get("found_by") in ("test", "review")
                    or (r.get("kind") == "BUG" and not r.get("found_by"))]
        bare = [r for r in by_people if not r.get("test") and not r.get("no_test_reason")]
        print("last %d days: %d bug(s) found by people, %d by tests and reviews; "
              "%d found by people still without a test" % (a.days, len(by_people), len(by_tests), len(bare)))
        for r in by_people:
            print("  %s  %s  %s  test: %s" % (r["first_seen"], r["status"], r["summary"],
                                             r.get("test") or r.get("no_test_reason") or "NONE YET"))
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
