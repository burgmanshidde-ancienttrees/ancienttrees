#!/usr/bin/env python3
"""Which pages to take out of Google's index while the site recovers.

Written 2026-10-01. On 09-28 Google stopped showing the site almost entirely:
every country, device and page kept 0 to 2 percent of its impressions while
URL Inspection still says every page is indexed and fetched fine. That is a
sitewide algorithmic demotion, and the September 2026 spam update began on
09-24. The policy that fits a site like ours is scaled content abuse: many
templated pages that each add little.

This prints a PROPOSAL and writes it to drafts/noindex-proposal.md and
data/noindex-proposal.json. It changes nothing on the site. Noindex keeps a
page live for readers and keeps its URL (hard rule 3); it only asks Google not
to list it, and it is undone by deleting the list.

Groups:
  A. Places with one to three trees: their English page, question page and
     tree pages, and any real translations of them. A place that earned real
     impressions (data/city-queue.json, 10 days) is kept indexed.
  B. Real translations of a city whose English page earns almost nothing.
  C. (Until 2026-10-09) Fallback pages: the English text on a /de/, /es/ ... URL,
     for every city with no translation. REMOVED that day on Hidde's "do this":
     they were 8,025 of the 11,526 pages on this list, seven crawled copies of
     every English page, and a noindex does not stop the crawl. The pages are no
     longer built and every URL redirects to its English page
     (site/src/lib/redirect-map.ts), so there is nothing left to noindex.
"""
import glob
import json
import os
import re
import unicodedata

from findable import findable, has_photo, enriched
from enrich import gaps as enrich_gaps

# Only a tree page WITH a photograph stays in Google's index (Hidde, 2026-10-06:
# "laten we voor stap 2 gaan", after the demotion had held flat for eight days
# while the night runs kept adding trees). A page with an AI-drafted story and
# no picture is the scaled-content shape the September 2026 spam update hits,
# however findable the tree is on the ground. findable() still decides what a
# night run may ADD (preflight); this decides only what Google is asked to list.
# The page stays live, and it returns to the index on the next deploy after it
# gains a photograph. False restores the findable rule of 2026-10-04.
INDEX_NEEDS_PHOTO = True

# Finished pages in a proven city RETURN to the index at most this many per
# build (2026-10-09). qa.py's check_index_grows_with_the_trees() refuses a
# deploy adding more than 80 new indexable urls against the live sitemap, and
# that guard is Hidde's; 182 pages qualified the day the enriched rule was
# written. deploy.yml runs this before every build and deploys happen several
# times a day, so the backlog clears in a day or two, most readers first, and
# Google sees each page come back as a change rather than as a burst. A page
# already off the list stays off; the budget counts only pages still on it.
# 40 rather than 60 so that a deploy carrying new photographed trees as well
# stays under the guard.
RETURN_PER_BUILD = 40
# AND THE BUDGET IS URLS AGAINST THE LIVE SITEMAP, NOT TREES (2026-10-09, the
# same afternoon). The first deploy under RETURN_PER_BUILD failed the guard
# twice: 40 returning trees brought their Portuguese, Italian and Dutch copies
# (65 urls), on top of the 68 urls the day's new trees and places had already
# queued up while every deploy was being cancelled by the next push. 133
# against 80, and a guard the next deploy cannot pass is a site that never
# deploys again, because the backlog only grows. So the returns take whatever
# room the guard leaves: everything else that is new is counted first, against
# the sitemap that is live right now, exactly as qa.py will count it, and
# finished pages return into the remainder, most readers first, a tree with
# all its language copies or not at all. With the live sitemap unreadable the
# fixed count above stands, which is also when qa.py skips its check.
GUARD_URLS = 80  # qa.py check_index_grows_with_the_trees(), Hidde's number
GUARD_MARGIN = 10  # pages this script does not enumerate (collections, species)

# THE SPLIT, Hidde 2026-10-08 ("Ok do the split"). The robots meta is read by
# every engine, so the 2026-10-01 noindex also took 11,500 pages out of Bing,
# which never demoted us: Bing's referrals went from 30 to 40 a window to zero
# the day the tag went on, and Bing is the index ChatGPT's search reads. Only
# ONE group was ever Google's objection and nobody else's: the honest tree pages
# that lack a photograph. They now carry <meta name="googlebot" content="noindex">
# (Google reads it, Bing, DuckDuckGo and Yahoo ignore it) and are offered to
# Bing in sitemap-bing.xml, which robots.txt never names so Google never sees
# it. The other groups (fallback pages, which are duplicates in any index; thin
# places; question pages) keep the generic tag. False puts the generic tag back
# on everything; reversing it needs Hidde.
GOOGLE_ONLY_WEAK_TREES = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://ancienttrees.app"
LANGS = ["de", "es", "fr", "it", "ja", "nl", "pt"]
QSLUG = {"en": "oldest-tree", "de": "aeltester-baum", "es": "arbol-mas-antiguo",
         "fr": "arbre-le-plus-vieux", "it": "albero-piu-antico", "ja": "saiko-rei-no-ki",
         "nl": "oudste-boom", "pt": "arvore-mais-antiga"}
THIN_MAX = 3            # a place with this many trees or fewer is group A
KEEP_IMPRESSIONS = 20   # a thin place with this many 10-day impressions stays
# Thin places kept for the impressions they earned BEFORE 09-28. Frozen, because
# every page has read near zero since the demotion and a live threshold would
# quietly push these four onto the list as well.
EARNED_KEEP = {"charleston", "ibiza", "liverpool", "monterey"}
BOT_DEMAND = {"sao-paulo"}  # impressions from a bot query, not readers (handoff 2026-10-01)

TRANSLIT = {"ß": "ss", "ø": "o", "æ": "ae", "œ": "oe", "ł": "l", "đ": "d", "ð": "d",
            "þ": "th", "ħ": "h"}


def slugify(name):
    """site/src/lib/slug.ts slugify(), the one slug rule."""
    s = name.lower().replace("'", "").replace("’", "")
    if s.startswith("the "):
        s = s[4:]
    s = "".join(TRANSLIT.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def renderable(t):
    loc = t.get("location") or {}
    return bool(t.get("story")) and loc.get("latitude") is not None and loc.get("longitude") is not None


def question_evidence():
    """Question pages Search Console ever showed in a digest. Frozen at
    generation time from DATA.md and its archive, so the list does not move
    with the demotion itself (every page reads near zero since 09-28)."""
    seen = set()
    files = [os.path.join(ROOT, "DATA.md")] + glob.glob(os.path.join(ROOT, "archive", "DATA*.md"))
    qs = "|".join(re.escape(v) for v in QSLUG.values())
    for f in files:
        try:
            txt = open(f, encoding="utf-8").read()
        except OSError:
            continue
        for m in re.finditer(r"(/(?:(?:%s)/)?[a-z0-9-]+/(?:%s))\b" % ("|".join(LANGS), qs), txt):
            seen.add(BASE + m.group(1))
    return seen


def roster():
    """Cities that had 10+ impressions the day before the demotion
    (data/depth-roster-frozen.json). Their place pages earned readers, so a
    missing photograph does not take them out (2026-10-06)."""
    try:
        return set(json.load(open(os.path.join(ROOT, "data", "depth-roster-frozen.json")))["cities"])
    except (OSError, ValueError, KeyError):
        return set()


def page_evidence():
    """Tree pages Search Console showed in a digest's top pages before the
    demotion. Frozen like question_evidence(): a page readers found keeps its
    place in the index while it waits for a photograph."""
    seen = set()
    txt = open(os.path.join(ROOT, "DATA.md"), encoding="utf-8").read()
    for line in re.findall(r"Top pages \(10d\): (.*)", txt):
        for path in re.findall(r"(/[a-z0-9/-]+) \(c\d+/i\d+\)", line):
            seen.add(BASE + path)
    return seen


def destination(t):
    """A tree somebody would travel for by itself: written up in two or more
    language Wikipedias, or a SOURCED age of a thousand years or more. The
    proxy for the single-famous-tree test of 2026-08-31."""
    if ((t.get("fame") or {}).get("langs") or 0) >= 2:
        return True
    return (t.get("age_min") or 0) >= 1000 and t.get("age_basis") != "derived"


def live_sitemap():
    """The urls Google is offered right now, or an empty set when the live
    site cannot be read (qa.py skips its burst check in that case too)."""
    import urllib.request
    try:
        with urllib.request.urlopen(f"{BASE}/sitemap.xml", timeout=20) as r:
            return set(re.findall(r"<loc>([^<]+)</loc>", r.read().decode("utf-8", "replace")))
    except Exception as e:
        print(f"deploy guard: live sitemap unreadable ({e.__class__.__name__}), RETURN_PER_BUILD stands")
        return set()


def main():
    imps = {}
    try:
        q = json.load(open(os.path.join(ROOT, "data", "city-queue.json")))
        for c in (q.get("cities", []) if isinstance(q, dict) else q):
            if c.get("slug"):
                imps[c["slug"]] = c.get("impressions_10d") or 0
    except (OSError, ValueError):
        pass
    translated = {lang: {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, "data", "i18n", lang, "*.json"))}
                  for lang in LANGS}
    q_keep = question_evidence()
    on_roster = roster()
    try:
        roster_imps = {k: (v or {}).get("impressions", 0) for k, v in
                       json.load(open(os.path.join(ROOT, "data", "depth-roster-frozen.json")))["cities"].items()}
    except (OSError, ValueError, KeyError, AttributeError):
        roster_imps = {}
    t_keep = page_evidence()

    groups = {"fallback": [], "thin_places": [], "question_pages": [], "weak_trees": []}
    kept_thin, a_places = [], []
    total_pages = 0
    nf = os.path.join(ROOT, "data", "noindex.json")
    try:
        prev = json.load(open(nf)).get("paths") or {}
        if isinstance(prev, list):
            prev = {p: "2026-10-01" for p in prev}
    except (OSError, ValueError):
        prev = {}
    # Finished pages still on the list, in roster order (most readers first);
    # the first RETURN_PER_BUILD leave it this build, the rest wait.
    returning = []
    indexable = set()  # every page this script knows the build will make
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        slug = os.path.basename(path)[:-5]
        d = json.load(open(path))
        trees = [t for t in d.get("trees") or [] if renderable(t)]
        if not trees:
            continue
        tslugs = [slugify(t["name"]) for t in trees]
        n = len(trees)
        has_q = n >= 2
        langs_real = [lang for lang in LANGS if slug in translated[lang]]
        total_pages += (1 + has_q + n) * (1 + len(langs_real))
        city_urls = [f"{BASE}/{slug}"] + [f"{BASE}/{lang}/{slug}" for lang in langs_real]
        q_urls = ([f"{BASE}/{slug}/{QSLUG['en']}"] + [f"{BASE}/{lang}/{slug}/{QSLUG[lang]}" for lang in langs_real]) if has_q else []
        indexable |= set(city_urls) | set(q_urls)
        for ts in tslugs:
            indexable |= {f"{BASE}/{slug}/{ts}"} | {f"{BASE}/{lang}/{slug}/{ts}" for lang in langs_real}
        # 1. Fallback pages: gone since 2026-10-09 (redirects now, see the docstring).
        # 4. Tree pages with neither a photograph nor a confirmed pin (Hidde,
        #    2026-10-01: "zo min mogelijk bomen met geen foto en geen exacte pin").
        #    Recomputed every deploy, so a tree returns to the index the day it
        #    gains either.
        #    Widened 2026-10-04: a pin on a small named site plus a recognition
        #    line counts as findable too (scripts/findable.py, shared with preflight).
        #    Narrowed 2026-10-06: a photograph is required (INDEX_NEEDS_PHOTO).
        #    Widened again 2026-10-09 (Hidde: "do this"): in a PROVEN city a
        #    tree page also stays indexed when the enrichment pass has
        #    finished it (findable.enriched(): findable on the ground, plus the
        #    register record, a measurement and concrete access), because
        #    INDEX_NEEDS_PHOTO alone had taken 2,311 of the 2,822 tree pages in
        #    those cities out of Google, pages it had already been showing, and
        #    a finished page is the opposite of the demoted shape. 182 pages
        #    qualified the day this was written; scripts/enrich.py works
        #    toward the rest, city by city, most readers first.
        for t, ts in zip(trees, tslugs):
            if has_photo(t) if INDEX_NEEDS_PHOTO else findable(t):
                continue
            if INDEX_NEEDS_PHOTO and slug in on_roster and enriched(t, enrich_gaps(t)):
                en_url = f"{BASE}/{slug}/{ts}"
                if en_url[len(BASE):] not in prev:
                    continue  # already back
                returning.append((roster_imps.get(slug, 0), en_url, [f"{BASE}/{lang}/{slug}/{ts}" for lang in langs_real]))
                continue
            urls = [f"{BASE}/{slug}/{ts}"] + [f"{BASE}/{lang}/{slug}/{ts}" for lang in langs_real]
            # A tree page readers found before 09-28 stays while it waits
            # for a photograph, if it is still findable on the ground.
            if INDEX_NEEDS_PHOTO and findable(t):
                urls = [u for u in urls if u not in t_keep]
            groups["weak_trees"] += urls
        # 2. Places with one to three trees: the PLACE pages leave the index,
        #    the tree pages stay, because the tree page is the one with the story.
        i = imps.get(slug, 0)
        if n <= THIN_MAX:
            # A one-tree place page repeats its own tree page (audit 2026-10-01:
            # /aga shared 10 of 37 sentences with /aga/shogun-sugi and both
            # aimed at one query), so only the tree page stays, however famous.
            if slug in EARNED_KEEP or (n >= 2 and any(destination(t) for t in trees)):
                kept_thin.append((d.get("city", slug), n, i))
            else:
                groups["thin_places"] += city_urls + q_urls
                a_places.append((d.get("city", slug), d.get("country", ""), n, i))
                continue
        # 2b. A place where no tree has a photograph leaves the index too
        #     (Hidde, 2026-10-06: keep adding trees for readers, "maar ze
        #     gewoon niet aan google meegeven tot ze fotos krijgen"). Its tree
        #     pages are already out under INDEX_NEEDS_PHOTO; without this a new
        #     place of four photo-less trees would still enter Google as a city
        #     page. Returns with its first photograph.
        #     Not a place on the frozen roster: those pages had readers.
        if INDEX_NEEDS_PHOTO and slug not in on_roster and not any(has_photo(t) for t in trees):
            groups["thin_places"] += city_urls + q_urls
            continue
        # 3. Question pages: ~45 percent template shared with every other
        #    question page and with their own city page. Kept only where
        #    Search Console ever showed one.
        # All of them since the 2026-10-01 audit: every remaining English one
        # answered the same question as its own city page's FAQ, so two pages
        # chased one query.
        groups["question_pages"] += q_urls

    returning.sort(key=lambda r: -r[0])
    take = RETURN_PER_BUILD
    live = live_sitemap()
    if live:
        offlist = set(sum(groups.values(), []))
        candidates = {u for _, en, langs in returning for u in [en] + langs}
        other_new = {u for u in indexable if u not in offlist and u not in candidates and u not in live}
        room = GUARD_URLS - GUARD_MARGIN - len(other_new)
        take, spent = 0, 0
        for _, en, langs in returning:
            cost = len([u for u in [en] + langs if u not in live])
            if spent + cost > room:
                break
            take, spent = take + 1, spent + cost
        print(f"deploy guard: {len(other_new)} other new indexable url(s) against the live sitemap, "
              f"room for {max(room, 0)} returning url(s) under {GUARD_URLS - GUARD_MARGIN}")
    held_back = returning[take:]
    for _, en_url, lang_urls in held_back:
        groups["weak_trees"] += [en_url] + lang_urls
    every = sorted(set(sum(groups.values(), [])))
    today = __import__("datetime").date.today().isoformat()
    # Each path keeps the date it was FIRST listed, so the recrawl sitemap's
    # lastmod stays true across rebuilds. deploy.yml reruns this before every
    # build, which is what keeps a place opened tonight from shipping fourteen
    # indexable language copies and a template question page by default.
    paths = {p: prev.get(p, today) for p in sorted({u[len(BASE):] for u in every})}
    # Google-only: a weak tree page that is on NO other list. A tree page of a
    # thin place is not on the thin_places list (that list holds place and
    # question pages), so in practice this is the whole weak_trees group; the
    # subtraction is what keeps it true if a group ever grows to include one.
    others = {u[len(BASE):] for k, v in groups.items() if k != "weak_trees" for u in v}
    google_only = sorted({u[len(BASE):] for u in groups["weak_trees"]} - others) if GOOGLE_ONLY_WEAK_TREES else []
    if returning:
        print(f"finished pages returning to the index this build: {take} of {len(returning)} "
              f"(RETURN_PER_BUILD {RETURN_PER_BUILD}); {len(held_back)} wait for a later build")
    json.dump({"generated": "scripts/thin_pages.py",
               "approved": "Hidde, 2026-10-01, in session: 'start with point 1 to 4'; the engine split 2026-10-08: 'Ok do the split'",
               "note": "Every path here leaves sitemap.xml and renders a self canonical (site/src/layouts/Base.astro). A path in google_only renders <meta name=googlebot content=noindex>, which only Google reads, and is offered to Bing in sitemap-bing.xml; every other path renders <meta name=robots content=noindex> for every engine. Pages stay live. Undo by emptying 'paths' and removing the thin_pages step from deploy.yml.",
               "counts": {k: len(set(v)) for k, v in groups.items()},
               "google_only": google_only,
               "paths": paths},
              open(nf, "w"), indent=1, ensure_ascii=False)

    out = ["# Noindex list (live)\n",
           "Generated by `scripts/thin_pages.py`, approved by Hidde 2026-10-01. Pages stay live for readers and keep their URLs; noindex only takes them out of Google. Undo by emptying `paths` in data/noindex.json.\n",
           "| Group | What | Pages |", "|---|---|---:|",
           f"| 1 | Fallback language pages (English text on a /de/, /es/ ... URL): removed 2026-10-09, every URL redirects to its English page | {len(set(groups['fallback']))} |",
           f"| 2 | Place and question pages of places with 1 to 3 trees ({len(a_places)} places); their tree pages stay indexed | {len(set(groups['thin_places']))} |",
           f"| 3 | Question pages, which repeat their city page's FAQ | {len(set(groups['question_pages']))} |",
           f"| 4 | Tree pages without a photograph (since 2026-10-06), unless in a proven city and finished: findable + register + measurement + access (since 2026-10-09). Out of GOOGLE only since 2026-10-08: Bing, DuckDuckGo and Yahoo keep them, via sitemap-bing.xml | {len(set(groups['weak_trees']))} |",
           f"| | **All, without double counting** | **{len(paths)}** |",
           f"| | of which Google-only (the googlebot tag) | {len(google_only)} |",
           f"| | Pages in the site (city, question, tree, all languages) | {total_pages} |", "",
           f"Thin places kept indexed ({len(kept_thin)}), a destination tree or real impressions: " +
           ", ".join(c for c, n, i in sorted(kept_thin)) + "\n",
           "## Places whose place pages leave the index\n", "| Place | Country | Trees | Impr. 10d |", "|---|---|---:|---:|"]
    for c, k, n, i in sorted(a_places, key=lambda x: (x[1], x[0])):
        out.append(f"| {c} | {k} | {n} | {i} |")
    open(os.path.join(ROOT, "data", "noindex.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out[:10]))

if __name__ == "__main__":
    main()
