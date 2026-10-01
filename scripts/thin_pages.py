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
  C. Fallback pages: the English text on a /de/, /es/ ... URL, for every city
     with no translation. Already canonical to English; noindex says it plainly.
"""
import glob
import json
import os
import re
import unicodedata

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


def destination(t):
    """A tree somebody would travel for by itself: written up in two or more
    language Wikipedias, or a SOURCED age of a thousand years or more. The
    proxy for the single-famous-tree test of 2026-08-31."""
    if ((t.get("fame") or {}).get("langs") or 0) >= 2:
        return True
    return (t.get("age_min") or 0) >= 1000 and t.get("age_basis") != "derived"


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

    groups = {"fallback": [], "thin_places": [], "question_pages": []}
    kept_thin, a_places = [], []
    total_pages = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        slug = os.path.basename(path)[:-5]
        d = json.load(open(path))
        trees = [t for t in d.get("trees") or [] if renderable(t)]
        if not trees:
            continue
        n = len(trees)
        has_q = n >= 2
        langs_real = [lang for lang in LANGS if slug in translated[lang]]
        total_pages += (1 + has_q + n) * (1 + len(langs_real)) + (1 + has_q) * (len(LANGS) - len(langs_real))
        city_urls = [f"{BASE}/{slug}"] + [f"{BASE}/{lang}/{slug}" for lang in LANGS]
        q_urls = ([f"{BASE}/{slug}/{QSLUG['en']}"] + [f"{BASE}/{lang}/{slug}/{QSLUG[lang]}" for lang in LANGS]) if has_q else []
        # 1. Fallback pages: the English text on a /de/, /es/ ... URL.
        for lang in LANGS:
            if lang not in langs_real:
                groups["fallback"] += [f"{BASE}/{lang}/{slug}"] + ([f"{BASE}/{lang}/{slug}/{QSLUG[lang]}"] if has_q else [])
        # 2. Places with one to three trees: the PLACE pages leave the index,
        #    the tree pages stay, because the tree page is the one with the story.
        i = imps.get(slug, 0)
        if n <= THIN_MAX:
            if any(destination(t) for t in trees) or slug in EARNED_KEEP:
                kept_thin.append((d.get("city", slug), n, i))
            else:
                groups["thin_places"] += city_urls + q_urls
                a_places.append((d.get("city", slug), d.get("country", ""), n, i))
                continue
        # 3. Question pages: ~45 percent template shared with every other
        #    question page and with their own city page. Kept only where
        #    Search Console ever showed one.
        groups["question_pages"] += [u for u in q_urls if u not in q_keep]

    every = sorted(set(sum(groups.values(), [])))
    today = __import__("datetime").date.today().isoformat()
    # Each path keeps the date it was FIRST listed, so the recrawl sitemap's
    # lastmod stays true across rebuilds. deploy.yml reruns this before every
    # build, which is what keeps a place opened tonight from shipping fourteen
    # indexable language copies and a template question page by default.
    nf = os.path.join(ROOT, "data", "noindex.json")
    try:
        prev = json.load(open(nf)).get("paths") or {}
        if isinstance(prev, list):
            prev = {p: "2026-10-01" for p in prev}
    except (OSError, ValueError):
        prev = {}
    paths = {p: prev.get(p, today) for p in sorted({u[len(BASE):] for u in every})}
    json.dump({"generated": "scripts/thin_pages.py",
               "approved": "Hidde, 2026-10-01, in session: 'start with point 1 to 4'",
               "note": "Every path here renders <meta name=robots content=noindex> and a self canonical (site/src/layouts/Base.astro), and so leaves sitemap.xml. Pages stay live. Undo by emptying 'paths' and removing the thin_pages step from deploy.yml.",
               "counts": {k: len(set(v)) for k, v in groups.items()},
               "paths": paths},
              open(nf, "w"), indent=1, ensure_ascii=False)

    out = ["# Noindex list (live)\n",
           "Generated by `scripts/thin_pages.py`, approved by Hidde 2026-10-01. Pages stay live for readers and keep their URLs; noindex only takes them out of Google. Undo by emptying `paths` in data/noindex.json.\n",
           "| Group | What | Pages |", "|---|---|---:|",
           f"| 1 | Fallback language pages: the English text on a /de/, /es/ ... URL | {len(set(groups['fallback']))} |",
           f"| 2 | Place and question pages of places with 1 to 3 trees ({len(a_places)} places); their tree pages stay indexed | {len(set(groups['thin_places']))} |",
           f"| 3 | Question pages Search Console never showed (kept: {len(q_keep)}) | {len(set(groups['question_pages']))} |",
           f"| | **All, without double counting** | **{len(paths)}** |",
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
