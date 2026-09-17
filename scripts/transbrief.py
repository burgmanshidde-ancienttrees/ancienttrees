#!/usr/bin/env python3
"""Hand a translation pass only what it has to translate, and merge what comes back.

Written 2026-09-17 on Hidde's "see if there are opportunities to do it faster",
after measuring where a translation pass actually spends its budget. The answer
was not what I expected and the two dead ends are recorded so nobody rebuilds
them:

  A translation memory harvested from the 50 existing overlays saves 2%. The
  repetitive fields (species, access, transport, age_estimate) are short, and
  stories are 85% of the payload and repeat never. The memory is still built
  and passed through, but for CONSISTENCY across cities rather than for tokens:
  one species must read the same in every Dutch page (hard rule 9 restated one
  language down).

  What does pay is the file itself. 43 to 49% of a city JSON is coordinates,
  photo blocks, licences, sources and verify_notes, none of which a translator
  may touch: the overlay is text only. A pass handed the whole file pays for
  all of it on the way in and has to be trusted not to echo any of it back.

So this extracts the translatable fields, enumerates every tree id, and merges
the answer itself. The merge is the half that matters most. `check_overlay_
coverage()` in preflight refuses an overlay missing any tree its English page
holds, and because the site is static that refusal kills the WHOLE deploy
rather than one page; it has already done so twice in one day. A brief that
enumerates the ids and an apply step that verifies them makes that failure
unreachable rather than merely unlikely.

Usage:
  python3 scripts/transbrief.py --brief <lang> <city>   # write the brief
  python3 scripts/transbrief.py --apply <file>          # merge the answer
  python3 scripts/transbrief.py --status                # what is translated
"""
import collections
import glob
import json
import os
import sys

TREE_FIELDS = ["name", "species", "age_estimate", "access", "transport", "story"]
CITY_FIELDS = ["city", "title", "meta_description", "intro", "question_title",
               "question_meta", "question_answer", "question_context"]
MEM_FIELDS = ["species", "access", "transport", "age_estimate"]
LANGS = ["es", "it", "nl", "de", "pt", "fr", "ja"]
OUT = "out/translate"


def english_trees():
    out = {}
    for f in glob.glob("data/cities/*.json"):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for t in d.get("trees") or []:
            if t.get("id"):
                out[t["id"]] = t
    return out


def memory(lang, en=None):
    """EN -> target pairs already settled in this language's overlays."""
    en = en or english_trees()
    mem = collections.defaultdict(dict)
    for f in glob.glob(f"data/i18n/{lang}/*.json"):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for tid, tt in (d.get("trees") or {}).items():
            e = en.get(tid)
            if not e:
                continue
            for k in MEM_FIELDS:
                ev, tv = e.get(k), tt.get(k)
                if isinstance(ev, str) and isinstance(tv, str) and ev.strip() and tv.strip():
                    mem[k][ev.strip()] = tv.strip()
    return mem


def sibling_convention(lang):
    """The strings_note a previous overlay in this language already settled."""
    for f in sorted(glob.glob(f"data/i18n/{lang}/*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if d.get("strings_note"):
            return d["strings_note"], os.path.basename(f)[:-5]
    return None, None


def brief(lang, slug):
    src = f"data/cities/{slug}.json"
    if not os.path.exists(src):
        print(f"no such city: {src}")
        return 1
    if lang not in LANGS:
        print(f"{lang} is not a shipping language. Adding one is a Contract J "
              f"change and needs Hidde (hard rule 7). Shipping: {', '.join(LANGS)}")
        return 1
    if os.path.exists(f"data/i18n/{lang}/{slug}.json"):
        print(f"data/i18n/{lang}/{slug}.json already exists. Refusing to "
              f"overwrite a live translation.")
        return 1

    d = json.load(open(src, encoding="utf-8"))
    en = english_trees()
    mem = memory(lang, en)
    note, from_city = sibling_convention(lang)

    trees = []
    hits = 0
    for t in d.get("trees") or []:
        row = {"id": t["id"]}
        for k in TREE_FIELDS:
            v = t.get(k)
            if isinstance(v, str) and v.strip():
                row[k] = v
        row["_settled"] = {k: mem[k][t[k].strip()] for k in MEM_FIELDS
                           if isinstance(t.get(k), str) and t[k].strip() in mem[k]}
        hits += len(row["_settled"])
        if not row["_settled"]:
            row.pop("_settled")
        trees.append(row)

    out = {
        "_brief": (
            f"Translate this city into {lang}. Return the SAME shape with every "
            f"value translated, as data/i18n/{lang}/{slug}.json, then merge it "
            f"with: python3 scripts/transbrief.py --apply <file>"
        ),
        "_rules": [
            "Text only. Never emit a coordinate, photo, licence, source or id "
            "you were not given; the overlay carries text and nothing else.",
            "Every tree id below must appear in the answer. A short overlay does "
            "not break one page, it stops the whole site deploying.",
            "No em dashes anywhere (hard rule 3).",
            "Stories keep the English bar: 150-250 words, lead with the most "
            "surprising fact, no 'hidden gem', 'must-see', 'breathtaking', "
            "'nestled'. Translate the meaning, not the word order.",
            "species: the target-language common name, the SAME Latin binomial "
            "in parentheses (hard rule 9, one canonical name per species).",
            "_settled shows what this language already calls these things. Reuse "
            "those strings exactly so one species does not get two names.",
            "The question page's own search phrase is fixed per language and is "
            "not yours to invent; it is recorded below.",
        ],
        "lang": lang,
        "slug": slug,
        "question_slug_note": f"URL segment for the question page is fixed in "
                              f"QUESTION_SLUG in site/src/lib/i18n.ts, do not translate it",
        "convention_from": from_city,
        "strings_note": note,
        "city": {k: d[k] for k in CITY_FIELDS if isinstance(d.get(k), str)},
        "faq": d.get("faq") if isinstance(d.get("faq"), list) else [],
        "trees": trees,
    }

    os.makedirs(OUT, exist_ok=True)
    path = f"{OUT}/{lang}-{slug}.json"
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    raw = len(open(src, encoding="utf-8").read())
    got = len(open(path, encoding="utf-8").read())
    print(f"wrote {path}")
    print(f"  {len(trees)} trees, {hits} fields already settled in {lang}")
    print(f"  city file {raw:,} chars -> brief {got:,} chars "
          f"({100 * (1 - got / raw):.0f}% less to read in)")
    return 0


def apply(path):
    a = json.load(open(path, encoding="utf-8"))
    lang, slug = a.get("lang"), a.get("slug")
    if lang not in LANGS or not slug:
        print("answer is missing a valid lang/slug")
        return 1
    src = f"data/cities/{slug}.json"
    d = json.load(open(src, encoding="utf-8"))
    want = [t["id"] for t in d.get("trees") or []]

    got = a.get("trees")
    if isinstance(got, list):
        got = {t["id"]: t for t in got if t.get("id")}
    got = got or {}

    missing = [i for i in want if i not in got]
    if missing:
        print(f"REFUSED: {len(missing)} tree(s) missing from the answer: "
              f"{', '.join(missing[:8])}{' ...' if len(missing) > 8 else ''}")
        print("A short overlay stops the whole site deploying, so this never merges.")
        return 1
    extra = [i for i in got if i not in want]
    if extra:
        print(f"REFUSED: {len(extra)} id(s) not in {slug}: {', '.join(extra[:8])}")
        return 1

    bad = []
    for tid, t in got.items():
        for k, v in t.items():
            if isinstance(v, str) and ("—" in v or "–" in v):
                bad.append(f"{tid}.{k}")
    for k, v in (a.get("city") or {}).items():
        if isinstance(v, str) and ("—" in v or "–" in v):
            bad.append(f"city.{k}")
    if bad:
        print(f"REFUSED: em dash in {len(bad)} field(s) (hard rule 3): "
              f"{', '.join(bad[:6])}")
        return 1

    overlay = {"_note": a.get("_note") or
               f"{lang} overlay for {slug}, written {__import__('datetime').date.today()} "
               f"from data/cities/{slug}.json via scripts/transbrief.py. Text only: "
               f"coordinates, photos, licences, age ranges, best_time and walks stay "
               f"in the English file."}
    for k in CITY_FIELDS:
        v = (a.get("city") or {}).get(k)
        if isinstance(v, str) and v.strip():
            overlay[k] = v
    if a.get("faq"):
        overlay["faq"] = a["faq"]
    if a.get("strings_note"):
        overlay["strings_note"] = a["strings_note"]
    overlay["trees"] = {
        tid: {k: got[tid][k] for k in TREE_FIELDS
              if isinstance(got[tid].get(k), str) and got[tid][k].strip()}
        for tid in want
    }

    os.makedirs(f"data/i18n/{lang}", exist_ok=True)
    dest = f"data/i18n/{lang}/{slug}.json"
    json.dump(overlay, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {dest}: {len(want)} trees, all ids present.")
    print("Now run: python3 scripts/preflight.py && python3 scripts/i18ncheck.py")
    return 0


def status():
    have = collections.defaultdict(set)
    for f in glob.glob("data/i18n/*/*.json"):
        have[f.split("/")[2]].add(os.path.basename(f)[:-5])
    print(f"{'lang':5s} {'cities':>7s}")
    for l in LANGS:
        print(f"{l:5s} {len(have[l]):7d}")
    print(f"{'all':5s} {sum(len(v) for v in have.values()):7d}")
    return 0


def main():
    a = sys.argv[1:]
    if not a or not os.path.isdir("data/cities"):
        print(__doc__)
        return 1
    if a[0] == "--brief" and len(a) >= 3:
        return brief(a[1], a[2])
    if a[0] == "--apply" and len(a) >= 2:
        return apply(a[1])
    if a[0] == "--status":
        return status()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
