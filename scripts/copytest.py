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


# HOW A TEST IS DECIDED, written down rather than judged each time.
#
# A challenger is promoted only if it beats control by this much. 0.25 index
# points on a base of about 0.7 is roughly a third better, which is the size
# this design can actually resolve (see the header). Anything smaller is
# INCONCLUSIVE and the control stays, and inconclusive has to be the ordinary
# outcome: a loop that promotes whatever is ahead on the day promotes noise,
# and it would do it forever without anybody noticing, because each promotion
# looks exactly like a result.
WIN_MARGIN = 0.25


def measure(test):
    """Per arm: how many pages, the index before, the index now, the change.

    The index is clicks over the clicks that arm's positions should have
    earned, so it already carries the position correction. Comparing the
    CHANGE is what removes the city differences: the two arms in this test
    started at 0.80 and 0.61, so comparing levels would hand us a winner on
    day one."""
    rows = {r["city"]: r for r in seolearn.joined()}
    arms = {}
    for city, arm in test["assignment"].items():
        now, was = rows.get(city), test["before"].get(city)
        if not now or not was:
            continue
        a = arms.setdefault(arm, {"n": 0, "bc": 0, "be": 0.0, "ac": 0, "ae": 0.0})
        a["n"] += 1
        a["bc"] += was["clicks"]
        a["be"] += was["impressions"] * was["expected"] / 100
        a["ac"] += now["clicks"]
        a["ae"] += now["impressions"] * now["expected"] / 100
    for a in arms.values():
        a["before"] = a["bc"] / a["be"] if a["be"] else 0.0
        a["after"] = a["ac"] / a["ae"] if a["ae"] else 0.0
        a["delta"] = a["after"] - a["before"]
    return arms


def days_in(test):
    return (datetime.date.today() - datetime.date.fromisoformat(test["started"])).days


def due(test):
    return datetime.date.today() >= datetime.date.fromisoformat(test["review"])


def verdict(test):
    """(winner, margin, why). winner is None when nothing is promoted."""
    arms = measure(test)
    if "control" not in arms or len(arms) < 2:
        return None, 0.0, "not enough arms reporting"
    base = arms["control"]["delta"]
    best, margin = None, 0.0
    for arm, a in arms.items():
        if arm == "control":
            continue
        m = a["delta"] - base
        if best is None or m > margin:
            best, margin = arm, m
    if margin >= WIN_MARGIN:
        return best, margin, "beat control by %+.2f, over the %.2f margin" % (margin, WIN_MARGIN)
    return None, margin, ("best challenger was %+.2f against control, under the %.2f "
                          "margin, so the control stays" % (margin, WIN_MARGIN))


def report(test=None):
    test = test or running()
    if not test:
        return ""
    arms = measure(test)
    if not arms:
        return ""
    total = (datetime.date.fromisoformat(test["review"])
             - datetime.date.fromisoformat(test["started"])).days
    out = ["Copy test: %s (day %d of %d, review %s)"
           % (test["id"], days_in(test), total, test["review"]),
           test["hypothesis"], ""]
    for arm in sorted(arms):
        a = arms[arm]
        out.append("  %-12s n%-3d  before %.2f  now %.2f  change %+.2f"
                   % (arm, a["n"], a["before"], a["after"], a["delta"]))
    if "control" in arms and len(arms) > 1:
        _, margin, why = verdict(test)
        out += ["", "  against control: %+.2f index points (promote at %+.2f)"
                % (margin, WIN_MARGIN)]
    if days_in(test) < 42:
        out += ["", "  TOO EARLY. At about 2 clicks per page per ten days this needs "
                "the full window; a lead now is noise wearing a result's clothes."]
    return "\n".join(out)


def promoted_default(doc, surface):
    """The arm every page wears when no test is running on this surface."""
    return (doc.get("defaults") or {}).get(surface, "control")


def renderable(doc, surface, arms):
    """Whether the site can actually draw these arms.

    A queued test whose arm has no template renders as the control on every
    page, which is the exact silent failure this file already cost a deploy
    over: it would run for eight weeks and report no difference, which is what
    it would report if the idea were wrong. So a test does not start until
    somebody has written its wording into the template, and until then the
    queue says so out loud instead of quietly starting it."""
    known = (doc.get("renderable_arms") or {}).get(surface, ["control"])
    return [a for a in arms if a not in known]


def close(doc, test):
    """Decide, record, and promote a winner into the surface's default."""
    winner, margin, why = verdict(test)
    test["status"] = "closed"
    test["closed"] = datetime.date.today().isoformat()
    test["result"] = {"winner": winner, "margin": round(margin, 3), "why": why,
                      "arms": {k: {kk: round(vv, 3) if isinstance(vv, float) else vv
                                   for kk, vv in v.items()}
                               for k, v in measure(test).items()}}
    lines = ["Copy test %s CLOSED after %d days: %s" % (test["id"], days_in(test), why)]
    if winner:
        doc.setdefault("defaults", {})[test["surface"]] = winner
        lines.append("  %s promoted: every %s now uses it." % (winner, test["surface"]))
    else:
        lines.append("  Nothing promoted. The control stays, which is the ordinary "
                     "outcome and not a failure of the test.")
    return lines


def start_next(doc, surface):
    """Take the next queued test on this surface, if the site can draw it."""
    queue = doc.get("queue") or []
    for i, q in enumerate(queue):
        if q.get("surface") != surface:
            continue
        missing = renderable(doc, surface, q.get("arms", {}))
        if missing:
            return ["  Next queued test %s cannot start: no template for %s. "
                    "A session has to write it into the page first."
                    % (q.get("id"), ", ".join(missing))]
        queue.pop(i)
        doc["queue"] = queue
        save(doc)
        rc = start(q["id"], surface, q["hypothesis"], q["arms"],
                   weeks=q.get("weeks", 8))
        return ["  Started the next queued test: %s" % q["id"]] if rc == 0 else []
    return ["  Nothing queued on %s. The surface rests until one is added." % surface]


def tick():
    """The autonomous step, run daily from the digest.

    Does nothing at all until a test reaches its review date. Then it decides,
    promotes or does not, records the result and starts whatever is queued
    next. Everything it does is reversible by editing data/copy-tests.json."""
    doc = load()
    said = []
    for test in doc.get("tests", []):
        if test.get("status") != "running" or not due(test):
            continue
        said += close(doc, test)
        save(doc)
        said += start_next(doc, test["surface"])
    if said:
        save(doc)
    return said


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
    if args and args[0] == "--tick":
        said = tick()
        print("\n".join(said) if said else "copytest: nothing due")
        return 0
    body = report()
    print(body or "copytest: no test running")
    return 0


if __name__ == "__main__":
    sys.exit(main())
