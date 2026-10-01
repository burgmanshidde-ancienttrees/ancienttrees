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
TWIN_MIN = 10           # a translation whose English twin earns less is group B

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

    groups = {"A": [], "B": [], "C": []}
    kept_thin, a_places, b_sets = [], [], []
    total_pages = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        slug = os.path.basename(path)[:-5]
        d = json.load(open(path))
        trees = [t for t in d.get("trees") or [] if renderable(t)]
        if not trees:
            continue
        n = len(trees)
        has_q = n >= 2
        tslugs = [slugify(t["name"]) for t in trees]
        en = [f"{BASE}/{slug}"] + ([f"{BASE}/{slug}/{QSLUG['en']}"] if has_q else []) + \
             [f"{BASE}/{slug}/{s}" for s in tslugs]
        langs_real = [lang for lang in LANGS if slug in translated[lang]]
        real = []
        for lang in langs_real:
            real += [f"{BASE}/{lang}/{slug}"] + ([f"{BASE}/{lang}/{slug}/{QSLUG[lang]}"] if has_q else []) + \
                    [f"{BASE}/{lang}/{slug}/{s}" for s in tslugs]
        fallback = []
        for lang in LANGS:
            if lang not in langs_real:
                fallback += [f"{BASE}/{lang}/{slug}"] + ([f"{BASE}/{lang}/{slug}/{QSLUG[lang]}"] if has_q else [])
        total_pages += len(en) + len(real) + len(fallback)
        groups["C"] += fallback
        i = imps.get(slug, 0)
        if n <= THIN_MAX:
            if i >= KEEP_IMPRESSIONS:
                kept_thin.append((d.get("city", slug), n, i))
            else:
                groups["A"] += en + real
                a_places.append((d.get("city", slug), d.get("country", ""), n, i))
                continue
        if real and i < TWIN_MIN:
            groups["B"] += real
            b_sets.append((d.get("city", slug), langs_real, i))

    every = sorted(set(groups["A"] + groups["B"] + groups["C"]))
    os.makedirs(os.path.join(ROOT, "drafts"), exist_ok=True)
    json.dump({"generated": "scripts/thin_pages.py", "enabled": False,
               "note": "PROPOSAL. Nothing reads this file until Hidde says yes.",
               "groups": {k: sorted(set(v)) for k, v in groups.items()}},
              open(os.path.join(ROOT, "data", "noindex-proposal.json"), "w"), indent=1, ensure_ascii=False)

    out = []
    out.append("# Noindex proposal\n")
    out.append("Generated by `scripts/thin_pages.py`. Nothing changes until you say yes. Every page stays live and keeps its URL; noindex only asks Google not to list it, and it is undone by deleting the list.\n")
    out.append("| Group | What | Pages |")
    out.append("|---|---|---:|")
    out.append(f"| A | Places with 1 to 3 trees ({len(a_places)} places): city, question and tree pages, and their translations | {len(set(groups['A']))} |")
    out.append(f"| B | Real translations of cities whose English page earns under {TWIN_MIN} impressions in 10 days ({len(b_sets)} cities) | {len(set(groups['B']))} |")
    out.append(f"| C | Fallback language pages: the English text on a /de/, /es/ ... URL | {len(set(groups['C']))} |")
    out.append(f"| | **All three, without double counting** | **{len(every)}** |")
    out.append(f"| | Pages in the site in total (city, question, tree, all languages) | {total_pages} |")
    out.append("")
    out.append(f"Kept indexed although thin, because they earn impressions ({len(kept_thin)}): " +
               ", ".join(f"{c} ({n} trees, {i} impr.)" for c, n, i in sorted(kept_thin, key=lambda x: -x[2])) + "\n")
    out.append("## Group A: places with 1 to 3 trees\n")
    out.append("| Place | Country | Trees | Impr. 10d |")
    out.append("|---|---|---:|---:|")
    for c, k, n, i in sorted(a_places, key=lambda x: (x[1], x[0])):
        out.append(f"| {c} | {k} | {n} | {i} |")
    out.append("\n## Group B: translations of quiet cities\n")
    out.append("| City | Languages | English impr. 10d |")
    out.append("|---|---|---:|")
    for c, ls, i in sorted(b_sets):
        out.append(f"| {c} | {', '.join(ls)} | {i} |")
    open(os.path.join(ROOT, "drafts", "noindex-proposal.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out[:12]))


if __name__ == "__main__":
    main()
