# Continuous copy testing: does the wording actually earn the click.
#
# Written 2026-09-10 on Hidde's "let's test" and, more importantly, "i'd like
# to do continuous testing of copy tbh and make it part of the learning
# cycle". So this is a standing mechanism with a queue of tests, not one
# experiment: a test finishes, a winner is promoted, the next one starts.
#
# WHY NOT A CLASSIC A/B TEST. Google serves one title per URL, so there is no
# per-visitor split and the unit of analysis is the CITY. Measured the day this
# was written: across our 62 pages with real demand the per-city index (CTR
# against the CTR that position normally earns) has a mean of 0.80 and a
# standard deviation of 1.04, so a straight two-arm comparison at 31 pages per
# arm can only see an effect of about 92 percent. Nothing in copywriting does
# that. Two design choices buy the power back:
#
#   DIFFERENCE IN DIFFERENCES. Each city is compared against ITS OWN earlier
#   window, and the control arm absorbs whatever Google did to everybody that
#   month. That removes the between-city variation, which is the half that does
#   not shrink with time.
#
#   MATCHED PAIRS. Cities are sorted by pre-period impressions and paired
#   adjacent, one of each pair to each arm. Impressions drive the noise (a page
#   takes about 2 clicks in ten days, so most of the spread is Poisson), and
#   pairing on them stops one arm inheriting the loud pages by luck.
#
# THE ASSIGNMENT IS FROZEN AT THE START and never recomputed. A city added
# later gets the control, because an arm somebody joins halfway through is not
# an arm. It also means a title never flips between builds, which matters more
# than the statistics: Google re-crawling a page whose title changes every
# night is a worse problem than any test can be worth.
#
# WHAT IT CANNOT SEE, stated so nobody over-reads a result. Google rewrites
# title links a good share of the time, so this measures the title we SET and
# not always the title SHOWN, which dilutes any real effect. And at this volume
# a fortnight is never enough: the review dates below are set eight weeks out
# on purpose.

import datetime
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "data", "copy-tests.json")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seolearn  # noqa: E402  (same directory, and it owns the reading of DATA.md)


def load():
    if not os.path.exists(REGISTRY):
        return {"note": "", "tests": []}
    with open(REGISTRY, encoding="utf-8") as fh:
        return json.load(fh)


def save(doc):
    with open(REGISTRY, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def running(doc=None, surface=None):
    doc = doc or load()
    for t in doc.get("tests", []):
        if t.get("status") != "running":
            continue
        if surface and t.get("surface") != surface:
            continue
        return t
    return None


def has_age_hook(slug):
    """Whether the city title carries an age at all.

    THE AUTHORITY IS site/src/pages/[city].astro, which drops the age below 200
    years because "Oldest 100 Years" sells the page worse than saying nothing.
    This is a screening approximation of that rule and it is allowed to be
    slightly wrong: a page that renders the same title in both arms adds noise
    to both equally, so a mismatch costs power and never correctness."""
    path = os.path.join(ROOT, "data", "cities", slug + ".json")
    if not os.path.exists(path):
        return False
    try:
        trees = json.load(open(path, encoding="utf-8")).get("trees") or []
    except (ValueError, OSError):
        return False
    best = 0
    for t in trees:
        v = t.get("age_max") or t.get("age_min") or 0
        if not v:
            digits = "".join(c for c in str(t.get("age_estimate") or "")
                             .split("-")[-1] if c.isdigit())
            v = int(digits) if digits else 0
        best = max(best, v)
    return best >= 200


def eligible(surface=None):
    """Pages with real demand and an uncontaminated query, loudest first.

    Bot pages are excluded outright: an arm carrying Milan's 350 scraper
    impressions would swamp everything else and measure nothing. For a title
    test, pages whose title would be identical in both arms are excluded too,
    for the reason has_age_hook() gives."""
    rows = [r for r in seolearn.joined() if not r["bot"]]
    if surface == "city title":
        rows = [r for r in rows if has_age_hook(r["city"])]
    return sorted(rows, key=lambda r: -r["impressions"])


def assign(rows, arms, seed):
    """Matched pairs, deterministic in the seed so a rerun gives the same split."""
    names = list(arms)
    out = {}
    for i in range(0, len(rows) - len(names) + 1, len(names)):
        block = rows[i:i + len(names)]
        # Which member of the pair goes to which arm is decided by a hash of
        # the slugs plus the seed: reproducible, and not the alphabet.
        key = hashlib.sha1((seed + "".join(r["city"] for r in block)).encode()).hexdigest()
        order = names if int(key[:8], 16) % 2 == 0 else names[::-1]
        for r, arm in zip(block, order):
            out[r["city"]] = arm
    return out


def start(test_id, surface, hypothesis, arms, weeks=8, seed=None):
    doc = load()
    if any(t["id"] == test_id for t in doc.get("tests", [])):
        print("copytest: %s already registered" % test_id)
        return 1
    if running(doc, surface):
        print("copytest: a test is already running on %s; one at a time, or the "
              "arms confound each other" % surface)
        return 1
    rows = eligible(surface)
    if len(rows) < 20:
        print("copytest: only %d eligible pages, not enough to learn from" % len(rows))
        return 1
    today = datetime.date.today()
    seed = seed or test_id
    test = {
        "id": test_id,
        "surface": surface,
        "status": "running",
        "started": today.isoformat(),
        "review": (today + datetime.timedelta(weeks=weeks)).isoformat(),
        "hypothesis": hypothesis,
        "metric": "index (CTR against expected CTR at the page's position), "
                  "difference in differences against each city's own pre-period",
        "arms": arms,
        "seed": seed,
        # The pre-period, frozen now, because DATA.md's entries age out into
        # archive/ and a test that cannot state its own baseline is not a test.
        "before": {r["city"]: {"clicks": r["clicks"], "impressions": r["impressions"],
                               "expected": r["expected"]} for r in rows},
        "assignment": assign(rows, arms, seed),
    }
    doc.setdefault("tests", []).append(test)
    save(doc)
    counts = {}
    for arm in test["assignment"].values():
        counts[arm] = counts.get(arm, 0) + 1
    print("copytest: started %s on %d pages (%s), review %s"
          % (test_id, len(test["assignment"]),
             ", ".join("%s %d" % kv for kv in sorted(counts.items())), test["review"]))
    return 0


def report(test=None):
    """Where each arm stands, as difference in differences."""
    test = test or running()
    if not test:
        return ""
    rows = {r["city"]: r for r in seolearn.joined()}
    arms = {}
    for city, arm in test["assignment"].items():
        now, was = rows.get(city), test["before"].get(city)
        if not now or not was:
            continue
        a = arms.setdefault(arm, {"n": 0, "bc": 0, "bi": 0, "be": 0.0,
                                  "ac": 0, "ai": 0, "ae": 0.0})
        a["n"] += 1
        a["bc"] += was["clicks"]; a["bi"] += was["impressions"]
        a["be"] += was["impressions"] * was["expected"] / 100
        a["ac"] += now["clicks"]; a["ai"] += now["impressions"]
        a["ae"] += now["impressions"] * now["expected"] / 100
    if not arms:
        return ""
    started = test["started"]
    days = (datetime.date.today() - datetime.date.fromisoformat(started)).days
    out = ["Copy test: %s (day %d of %d, review %s)"
           % (test["id"], days,
              (datetime.date.fromisoformat(test["review"])
               - datetime.date.fromisoformat(started)).days, test["review"]),
           test["hypothesis"], ""]
    base = None
    for arm in sorted(arms):
        a = arms[arm]
        before = a["bc"] / a["be"] if a["be"] else 0
        after = a["ac"] / a["ae"] if a["ae"] else 0
        delta = after - before
        if arm == "control":
            base = delta
        out.append("  %-12s n%-3d  before %.2f  now %.2f  change %+.2f"
                   % (arm, a["n"], before, after, delta))
    if base is not None and len(arms) > 1:
        for arm in sorted(arms):
            if arm == "control":
                continue
            a = arms[arm]
            d = (a["ac"] / a["ae"] if a["ae"] else 0) - (a["bc"] / a["be"] if a["be"] else 0)
            out.append("")
            out.append("  %s against control: %+.2f index points" % (arm, d - base))
    if days < 42:
        out.append("")
        out.append("  TOO EARLY. At about 2 clicks per page per ten days this needs "
                   "the full window; a lead now is noise wearing a result's clothes.")
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    if args and args[0] == "--start-title-test":
        return start(
            test_id="city-title-age-first",
            surface="city title",
            hypothesis="The age is the hook and the count is inventory, so naming "
                       "the oldest tree before the number earns more clicks.",
            arms={
                "control": "Ancient Trees in {city}: {n} to See, Oldest {age} Years",
                "age_first": "Ancient Trees in {city}: Oldest {age} Years, {n} to See",
            },
        )
    body = report()
    print(body or "copytest: no test running")
    return 0


if __name__ == "__main__":
    sys.exit(main())
