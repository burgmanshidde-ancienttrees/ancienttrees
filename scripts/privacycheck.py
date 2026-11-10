#!/usr/bin/env python3
"""Does the privacy page still name everything we store and everyone who handles it?

    python3 scripts/privacycheck.py          exit 1 and say what is missing
    python3 scripts/privacycheck.py --light  one line for quality.py

Hidde, 2026-11-10, after a compliance audit found the privacy page six weeks
behind the product ("hoe dichten we dit gat - hoe zorgen we dat er om de
zoveel tijd een compliancy check is want ik vraag dit nu random"). The page
still said an account without a name has no profile and a collection is shown
to nobody, while profiles had become public by default. Nobody lied; every
change was made without anybody rereading the page.

So the mechanical half of the answer is this script, run by qa.py on every
push (check_the_privacy_page_names_what_we_store) and read by quality.py:

  1. every file in supabase/ has an entry in data/privacy-map.json, either a
     phrase that appears on site/src/pages/privacy.astro or a one-line reason
     it holds no personal data. A new table without one fails the push, which
     makes the person adding it write the privacy sentence in the same commit;
  2. every service in the map is named on the page;
  3. the parts GDPR article 13 requires are there (who, why, how long, rights,
     the complaint to the Autoriteit Persoonsgegevens, the minimum age).

The human half, whether those sentences are still TRUE, is the weekly
compliance review (BRIEF_COMPLIANCE.md, review.yml)."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "site", "src", "pages", "privacy.astro")
MAP = os.path.join(ROOT, "data", "privacy-map.json")


def _flat(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).lower()


def problems():
    try:
        page = _flat(open(PAGE, encoding="utf-8").read())
        m = json.load(open(MAP, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return ["cannot read %s" % e]
    out = []
    tables = m.get("tables", {})
    for f in sorted(os.listdir(os.path.join(ROOT, "supabase"))):
        if not f.endswith(".sql"):
            continue
        e = tables.get(f)
        if e is None:
            out.append("supabase/%s is not in data/privacy-map.json: say on the privacy "
                       "page what it stores, then map it (or mark it exempt with why)" % f)
        elif not e.get("exempt") and _flat(e.get("phrase", "")) not in page:
            out.append("supabase/%s: the privacy page no longer says \"%s\"" % (f, e.get("phrase")))
    for f in tables:
        if not os.path.exists(os.path.join(ROOT, "supabase", f)):
            out.append("data/privacy-map.json maps supabase/%s, which is gone" % f)
    for name in m.get("services", {}):
        if name.lower() not in page:
            out.append("service %s is not named on the privacy page" % name)
    for phrase, why in m.get("musts", {}).items():
        if phrase.lower() not in page:
            out.append("the privacy page lacks \"%s\" (%s)" % (phrase, why))
    return out


def light():
    p = problems()
    if not p:
        return "green", ""
    return "red", "privacy page misses %d item(s): python3 scripts/privacycheck.py" % len(p)


def main():
    if "--light" in sys.argv:
        print("%s %s" % light())
        return 0
    p = problems()
    for x in p:
        print("privacycheck: " + x)
    if not p:
        print("privacycheck: the privacy page names every table, service and GDPR must")
    return 1 if p else 0


if __name__ == "__main__":
    raise SystemExit(main())
