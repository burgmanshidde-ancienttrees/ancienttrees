#!/usr/bin/env python3
"""Post-build QA over site/dist. Runs on every deploy, after the Astro build
(site/, npx astro build; the Python renderer this once followed, build_site.py,
was deleted 2026-08-09 once the Astro cutover ran a clean deploy cycle).

The Astro build validates what it is ABOUT to write (contracts, lengths,
script hygiene, as build-time errors thrown from site/src/lib's ratchet
checks); this script validates what actually landed on disk, the way a
browser will meet it. The split matters: build checks catch what the
generator knows about, this catches what it forgot it was generating.

Checks, all deterministic, no network:
  1. Internal links resolve to a real file (GitHub Pages resolution rules:
     exact file, +.html, or /index.html).
  2. Internal image/script/css sources resolve the same way.
  3. No em dash anywhere in rendered text (hard rule 3).
  4. No banned filler words in rendered text (CLAUDE.md Step 3).
  5. img src urls are http(s) or site-relative, never a Wikimedia File: page.

Exit 1 on any failure, so CI fails the deploy. Run: python3 scripts/qa.py
"""
import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "site" / "dist"

BANNED_WORDS = ["hidden gem", "must-see", "breathtaking", "nestled"]

# Our own rules are not the reader's business. Hidde, 2026-08-08, on finding the
# parks index explaining its own publish gate to visitors: "Why are you saying
# this logic? That is our logic back to the end user. They just want nice data,
# nice parks with trees. They don't care about our specific rules."
#
# This is the second time the same disease shipped, after the builder-speak rule
# that already bans narrating construction, so it is a check now rather than a
# third note. Three shapes, all of which were live:
#   - the publish gate as copy ("a park earns a page once we have mapped five")
#   - the shortfall as copy ("23 parks hold three or four, not yet enough")
#   - the roadmap as copy ("more species appear as new cities join the map")
# What the reader wants is what IS here and why it is worth their afternoon.
# A count is fine ("9 trees, Madrid"); the threshold behind the count is not.
BUSINESS_RULE_PHRASES = [
    "earns a page", "earn a page", "once we have mapped", "the site has mapped",
    "not yet enough", "enough for a page", "a page of their own",
    "a page of its own", "have enough mapped", "appear as new cities join",
    "qualifies for a page", "publish gate", "we only publish",
]



# Product-copy surfaces (no editorial stories on them) may not make absolute
# promises: the paywall rule bans forever-claims, and "Nothing else, ever"
# still shipped twice before this gate existed. Story prose is exempt because
# "the tree never recovered" is legitimate narrative.
PROMISE_PAGES = {"app.html", "account.html", "contribute.html", "privacy.html",
                 "explore.html", "index.html", "cities.html"}
PROMISE_PATTERNS = [", ever", " forever", "we will never", "we will always",
                    "nothing else, ever", "no ads, ever", "always free"]


class PageScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []      # href/src values
        self.img_srcs = []
        self.text_parts = []
        self._skip_depth = 0  # inside script/style

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip_depth += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script") and a.get("src"):
            (self.img_srcs if tag == "img" else self.links).append(a["src"])
        if tag == "link" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            self.text_parts.append(data)


def resolves(target: Path) -> bool:
    """GitHub Pages resolution: exact file, file + .html, or dir/index.html."""
    if target.is_file():
        return True
    if target.with_suffix(target.suffix + ".html").is_file():
        return True
    if (target / "index.html").is_file():
        return True
    return False


# The only check here that looks at the repository rather than at site/dist,
# and it earns the exception the way every other ratchet check did: the same
# error shipped twice.
#
# A workflow prompt that declares the current phase goes stale invisibly,
# because the corpus gets edited in session and the YAML does not. On
# 2026-08-11 CITY_QUEUE.md was written to kill six competing city orders and
# named "the order embedded in nightly.yml" as one of them; that order was
# still sitting in the prompt, still being executed, on 2026-08-12, six days
# after the phase it encoded had been replaced. Two copies of a course means
# the one nobody edits wins.
#
# So: strategy lives in CLAUDE.md and CITY_QUEUE.md. A workflow prompt may
# carry mechanics (how to claim a pass, which build command matches the tool
# allowlist, what this runner's proxy blocks) and must not carry a phase, a
# priority order or a city work list. The patterns below are the SHAPE of that
# error rather than a word list, so an honest mechanic sentence passes.
STRATEGY_IN_WORKFLOW = [
    "is the current phase", "the current phase is", "the job for the coming runs",
    "phase-1 city", "phase 1 city", "stays closed until", "stay closed until",
    "work stops: no new", "in this order, and photos",
]


def check_no_strategy_in_workflows():
    out = []
    wf = Path(__file__).resolve().parent.parent / ".github" / "workflows"
    if not wf.is_dir():
        return out
    for path in sorted(wf.glob("*.yml")):
        low = path.read_text(encoding="utf-8").lower()
        for pat in STRATEGY_IN_WORKFLOW:
            if pat in low:
                out.append(
                    f".github/workflows/{path.name}: declares strategy ({pat!r}). "
                    "A phase or city order in a workflow prompt goes stale invisibly; "
                    "put it in CLAUDE.md or CITY_QUEUE.md and point at it."
                )
    return out


# The eighth ratchet check, and the same disease as the one above: a second
# copy of something that already has one place to live. data/city-list.json
# carried rank/queue/tier from an older scheme while CITY_QUEUE.md carried the
# real order, and they disagreed hard (Porto 62 against 2, Rome 4 against 12).
# CLAUDE.md Step 0 tells every run to read city-list.json first, so the stale
# order was the one being obeyed. Hidde, 2026-08-12: "kunnen we 1 wachtrij /
# city order maken". The json is inventory now; the order lives in CITY_QUEUE.md
# and is regenerated by scripts/city_queue.py.
def check_one_city_order():
    import json as _json
    root = Path(__file__).resolve().parent.parent
    out = []
    path = root / "data" / "city-list.json"
    if path.exists():
        d = _json.loads(path.read_text(encoding="utf-8"))
        rows = d if isinstance(d, list) else d.get("cities", [])
        bad = sorted({k for r in rows if isinstance(r, dict)
                      for k in ("rank", "queue", "tier") if k in r})
        if bad:
            out.append(f"data/city-list.json: carries ordering field(s) {', '.join(bad)}; "
                       "it is generated inventory. Run python3 scripts/city_queue.py")
    # And the rendering must match its source. CITY_QUEUE.md is written from
    # data/city-queue.json; a row edited by hand in the markdown is a second
    # source again, silently, until the next regeneration wipes it.
    src, md = root / "data" / "city-queue.json", root / "CITY_QUEUE.md"
    if src.exists() and md.exists():
        cities = _json.loads(src.read_text(encoding="utf-8"))["cities"]
        want = {c["rank"]: c["city"] for c in cities if c.get("rank")}
        got = {}
        for line in md.read_text(encoding="utf-8").split("\n"):
            m = re.match(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|", line)
            if m:
                got[int(m.group(1))] = m.group(2)
        if got and got != want:
            diff = sorted(set(want.items()) ^ set(got.items()))[:3]
            out.append("CITY_QUEUE.md's table disagrees with data/city-queue.json "
                       f"(e.g. {diff}); the json is the source. "
                       "Run python3 scripts/city_queue.py")
    return out


def main():
    global DIST
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=None,
                        help="Override the dist directory (default: site/dist). "
                             "Used during the Astro migration to check site/dist-astro "
                             "without touching behavior against the real dist.")
    args = parser.parse_args()
    if args.dist:
        # Must be absolute: the orphan check below resolves() every link
        # target before comparing it against `pages`, so a relative DIST
        # (exactly what --dist's own help text recommends, e.g. "site/
        # dist-astro") made every one of those comparisons compare a
        # relative Path against an absolute one, silently orphaning every
        # non-excluded page in the build.
        DIST = args.dist.resolve()

    failures = []
    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        print(f"QA: no pages found under {DIST}, run (cd site && npx astro build) first")
        return 1

    for page in pages:
        rel = page.relative_to(DIST)
        scan = PageScan()
        scan.feed(page.read_text(encoding="utf-8"))
        text = " ".join(scan.text_parts)

        if rel.name == "index.html" and rel.parent.name == "":
            import re as _re
            m = _re.search(r"<title>([^<]*)</title>", page.read_text(encoding="utf-8"))
            if m and not m.group(1).startswith("Ancient Trees"):
                failures.append(f"{rel}: homepage <title> is {m.group(1)!r}; a shelf caption once shadowed it")

        if rel.name in PROMISE_PAGES and rel.parent.name == "":
            import re as _re2
            for pat in PROMISE_PATTERNS:
                # Whole words only. A substring match reads ", every one of them"
                # as the promise ", ever" and fails an honest sentence, which is
                # how this rule blocked a deploy on 2026-08-06.
                if _re2.search(r"%s\b" % _re2.escape(pat), text.lower()):
                    failures.append(f"{rel}: absolute promise {pat!r} in product copy (forever-claims rule)")

        if "—" in text:
            failures.append(f"{rel}: em dash in rendered text (hard rule 3)")
        # A tree with no numeric age (age_min/age_max null, age_estimate with
        # no digit) once made age_token() fall back to the literal string
        # "None", shipping live as "<title>...: None Year Old Tree in City"
        # on three published pages before this check existed (2026-08-09).
        if "None Year" in text:
            failures.append(f"{rel}: literal 'None Year' in rendered text, an undated tree's age fell back to None")
        lower = text.lower()
        for word in BANNED_WORDS:
            if word in lower:
                failures.append(f"{rel}: banned word {word!r} in rendered text")
        for phrase in BUSINESS_RULE_PHRASES:
            if phrase in lower:
                failures.append(
                    f"{rel}: explains our own publishing rule to the reader "
                    f"({phrase!r}). Say what is here and why it is worth the "
                    f"visit; the threshold behind it is ours, not theirs.")

        for src in scan.img_srcs:
            if "/wiki/File:" in src:
                failures.append(f"{rel}: img src is a wiki File: page: {src}")
            # The image standard (Hidde, 2026-07-31): every rendered image is
            # right-sized via img_srcset. A full-resolution original in an img
            # tag means a new render site skipped the helper.
            if "upload.wikimedia.org/wikipedia/commons/" in src and "/thumb/" not in src:
                failures.append(f"{rel}: full-size Wikimedia original in img (use img_srcset): {src[:90]}")
            if re.search(r"(static\.inaturalist\.org|inaturalist-open-data)[^\"]*/original\.", src):
                failures.append(f"{rel}: iNaturalist original in img (use img_srcset): {src[:90]}")
            if not (src.startswith("http") or src.startswith("data:")
                    or not re.match(r"^[a-z]+:", src)):
                failures.append(f"{rel}: img src with unexpected scheme: {src}")

        for url in scan.links + scan.img_srcs:
            if re.match(r"^(https?:|mailto:|data:|tel:)", url):
                continue
            path = url.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue  # pure #anchor
            base = DIST if path.startswith("/") else page.parent
            target = (base / path.lstrip("/")).resolve()
            if not resolves(target):
                failures.append(f"{rel}: dead internal link {url!r}")

    # Orphan check: the machine-testable half of the whole-page rule (Hidde,
    # 2026-08-04). Country pages shipped live with nothing linking to them for
    # three days because "how does anyone reach this" was never asked. A page
    # nobody links to cannot be found by a visitor and is barely crawled.
    linked = set()
    for page in pages:
        scan = PageScan()
        scan.feed(page.read_text(encoding="utf-8"))
        for url in scan.links:
            if re.match(r"^(https?:|mailto:|data:|tel:|#)", url):
                continue
            path = url.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            base = DIST if path.startswith("/") else page.parent
            target = (base / path.lstrip("/")).resolve()
            for cand in (target, target.with_suffix(target.suffix + ".html"),
                         target / "index.html"):
                if cand.is_file():
                    linked.add(cand)
                    break
    # Redirect stubs and the noindexed account prototype are linked on purpose
    # by nothing; the homepage is the root.
    for page in pages:
        if page in linked or page.name == "index.html":
            continue
        text = page.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text or "noindex" in text:
            continue
        failures.append(f"{page.relative_to(DIST)}: orphan, no page on the site links to it")

    failures += check_no_strategy_in_workflows()
    failures += check_one_city_order()

    if failures:
        print(f"QA FAILED: {len(failures)} problem(s) in {len(pages)} pages")
        for f in failures[:60]:
            print(f"  - {f}")
        if len(failures) > 60:
            print(f"  ... and {len(failures) - 60} more")
        return 1
    print(f"QA passed: {len(pages)} pages, links resolve, text clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
