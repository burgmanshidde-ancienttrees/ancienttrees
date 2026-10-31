"""The species dictionary: every kind of tree we know, by every name a reader
might type for it.

Hidde, 2026-10-31: "when adding a tree I often dont know the english name -
some people might even prefer latin names can we make the specie database
smarter and easier to search through on every occasion in the app possible".

The search answered to our English name and the Latin since 2026-10-03, and
only for the species we already map. Somebody standing at a hornbeam who
thinks "haagbeuk" found nothing and typed a name of their own, which splits a
species the way hard rule 9 forbids. This file is the answer as DATA, so web
and app read the same names (CLAUDE.md: a decision travels as data in the
feed, never as a rule implemented twice).

Where the names come from, in order of trust:
  1. our own translations (data/i18n/<lang>/*.json), which a translate pass
     wrote and which the site already publishes;
  2. Wikidata (CC0): the label and the "taxon common name" (P1843) in each of
     our seven languages plus English synonyms.

What is in it:
  - every species we map, keyed by our canonical common name;
  - species we have met in data/leads/ and not mapped yet (`mapped: false`),
    so the chooser can offer "Hornbeam" instead of a name typed by hand;
  - genera, so "eik" offers "Oak (Quercus sp.)", the publish-and-ask answer.

The common name we print never changes here: it stays the one in the city
file (hard rule 9). Everything else is only something to search by.

Usage:
  python3 scripts/species_names.py            # build, asking Wikidata only for what is new
  python3 scripts/species_names.py --refresh  # ask Wikidata again for everything
  python3 scripts/species_names.py --status   # coverage per language
"""
import glob
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "species-names.json"
# Wikidata's raw answer per taxon, so a rebuild asks only for what is new.
CACHE = ROOT / "data" / "research" / "wikidata-species-names.json"
LANGS = ["nl", "de", "es", "it", "fr", "pt", "ja"]
WIKIDATA = "https://query.wikidata.org/sparql"
UA = "AncientTreesSpeciesNames/1.0 (https://ancienttrees.app)"

PAREN = re.compile(r"^(.*?)\s*\((.+)\)\s*$")


def fold(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def split_species(value):
    """'Pedunculate Oak (Quercus robur)' -> ('Pedunculate Oak', 'Quercus robur')."""
    m = PAREN.match(value or "")
    if not m:
        return None, None
    return m.group(1).strip(), m.group(2).strip()


def binomial(latin):
    """The name Wikidata files the taxon under: genus plus epithet, the hybrid
    sign kept, cultivars and ranks below species dropped. None for 'sp.'."""
    words = latin.replace("×", "x").split()
    if len(words) < 2:
        return None
    if words[1].lower() in ("sp.", "sp", "spp.", "spp"):
        return None
    if words[1].lower() == "x" and len(words) >= 3:
        return "%s × %s" % (words[0], words[2])
    if words[1].startswith(("'", "‘", '"')):
        return None
    return "%s %s" % (words[0], words[1])


def walk_species(node, found):
    if isinstance(node, dict):
        v = node.get("species")
        if isinstance(v, str):
            found.append(v)
        for x in node.values():
            walk_species(x, found)
    elif isinstance(node, list):
        for x in node:
            walk_species(x, found)


def gather():
    """Our own names: mapped species from the city files, the rest from leads,
    local names from the translation overlays."""
    mapped = {}  # common -> {latin: count}
    for f in sorted(glob.glob(str(ROOT / "data" / "cities" / "*.json"))):
        for t in json.load(open(f, encoding="utf-8")).get("trees", []):
            common, latin = split_species(t.get("species", ""))
            if common and latin:
                mapped.setdefault(common, {}).setdefault(latin, 0)
                mapped[common][latin] += 1

    mapped_bin = set()
    for latins in mapped.values():
        for latin in latins:
            b = binomial(latin)
            if b:
                mapped_bin.add(fold(b))

    leads = {}  # binomial -> common (our own style, from the lead)
    for f in sorted(glob.glob(str(ROOT / "data" / "leads" / "*.json"))):
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        found = []
        walk_species(data, found)
        for v in found:
            common, latin = split_species(v)
            b = binomial(latin) if latin else None
            if not b or not common or fold(b) in mapped_bin:
                continue
            if not re.match(r"^[A-Z][a-z]+ (× )?[a-z-]+$", b):
                continue  # free text that only looks like a name
            leads.setdefault(b, common)

    local = {}  # latin binomial (folded) -> lang -> set of names
    for lang in LANGS:
        for f in glob.glob(str(ROOT / "data" / "i18n" / lang / "*.json")):
            try:
                data = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            found = []
            walk_species(data, found)
            for v in found:
                name, latin = split_species(v)
                b = binomial(latin) if latin else None
                if name and b:
                    local.setdefault(fold(b), {}).setdefault(lang, set()).add(name)
    return mapped, leads, local


def sparql(names):
    """Labels and common names in our languages for a batch of taxon names."""
    values = " ".join(json.dumps(n) for n in names)
    langs = ", ".join('"%s"' % l for l in ["en"] + LANGS)
    q = """
SELECT ?name ?lang ?label WHERE {
  VALUES ?name { %s }
  ?item wdt:P225 ?name .
  { ?item rdfs:label ?label . }
  UNION { ?item wdt:P1843 ?label . }
  UNION { ?item skos:altLabel ?label . }
  BIND(LANG(?label) AS ?lang)
  FILTER(?lang IN (%s))
}""" % (values, langs)
    url = WIKIDATA + "?" + urllib.parse.urlencode({"query": q, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        rows = json.load(r)["results"]["bindings"]
    out = {}
    for row in rows:
        out.setdefault(row["name"]["value"], {}).setdefault(row["lang"]["value"], set()).add(row["label"]["value"])
    return out


def ask_wikidata(names, cache):
    todo = [n for n in names if n not in cache]
    for i in range(0, len(todo), 60):
        batch = todo[i:i + 60]
        try:
            got = sparql(batch)
        except Exception as e:
            print("wikidata: batch %d failed (%s); kept what we had" % (i // 60, e))
            continue
        for n in batch:
            cache[n] = {l: sorted(v) for l, v in got.get(n, {}).items()}
        print("wikidata: %d of %d" % (min(i + 60, len(todo)), len(todo)))
        time.sleep(1.5)
    return cache


def keep(name, common, latin):
    """A name worth searching by: not the one we print, not the Latin itself,
    and not a Wikidata label that is only the Latin again."""
    f = fold(name)
    if not f or f in (fold(common), fold(latin)):
        return False
    words = latin.split()
    if f.startswith(fold(words[0]) + " "):
        return False  # another Latin spelling of the same taxon
    if len(words) > 1 and words[-1].lower() in f.split():
        return False  # "Gingko biloba": the epithet under another genus spelling
    return len(name) <= 60


def entry(common, latin, wd, local, mapped, genus=False):
    names = {}
    # "Oak (Quercus sp.)" is a genus answer and searches by the genus names.
    b = latin if genus else (binomial(latin) or latin.split()[0])
    for lang in ["en"] + LANGS:
        pool = []
        pool += sorted(local.get(fold(b), {}).get(lang, set()))
        pool += (wd.get(b) or {}).get(lang, [])
        seen, kept = set(), []
        for n in pool:
            # Lower-case labels on Wikidata ("zomereik") read wrong under a
            # title-case common name; the search folds case anyway.
            n = n.strip()
            if keep(n, common, b) and fold(n) not in seen:
                seen.add(fold(n))
                kept.append(n)
        if kept:
            names[lang] = kept[:4]
    e = {"common": common, "latin": latin}
    if genus:
        e["genus"] = True
    elif not mapped:
        e["mapped"] = False
    if names:
        e["names"] = names
    return e


def build(refresh=False):
    mapped, leads, local = gather()
    previous = {}
    if CACHE.exists() and not refresh:
        previous = json.load(open(CACHE, encoding="utf-8"))

    genus_common = {}
    gfile = ROOT / "data" / "genus-names.json"
    if gfile.exists():
        for g, info in json.load(open(gfile, encoding="utf-8")).get("genera", {}).items():
            if info.get("common"):
                genus_common[g] = info["common"]

    mapped_latin = {}
    for common, latins in mapped.items():
        mapped_latin[common] = max(latins.items(), key=lambda kv: kv[1])[0]

    wanted = set()
    for latin in mapped_latin.values():
        if binomial(latin):
            wanted.add(binomial(latin))
    wanted |= set(leads)
    genera = set(genus_common)
    for latin in list(mapped_latin.values()) + list(leads):
        genera.add(latin.split()[0])
    wanted |= genera

    cache = ask_wikidata(sorted(wanted), dict(previous))

    species = []
    for common in sorted(mapped_latin):
        species.append(entry(common, mapped_latin[common], cache, local, True))
    by_common = {e["common"]: e for e in species}
    for b in sorted(leads):
        e = entry(leads[b], b, cache, local, False)
        twin = by_common.get(e["common"])
        if twin:
            # A synonym of a species we map (Platanus x hispanica is our
            # London Plane): its names belong to that row, not to a second one.
            for lang, ns in e.get("names", {}).items():
                have = twin.setdefault("names", {}).setdefault(lang, [])
                for n in ns:
                    if len(have) < 4 and fold(n) not in {fold(h) for h in have}:
                        have.append(n)
            continue
        species.append(e)
        by_common[e["common"]] = e

    gen = []
    for g in sorted(genera):
        common = genus_common.get(g)
        if not common:
            en = (cache.get(g) or {}).get("en", [])
            common = next((n for n in en if keep(n, "", g)), None)
            if not common:
                continue
            common = common[:1].upper() + common[1:]
        gen.append(entry(common, g, cache, local, True, genus=True))

    out = {
        "_note": ("Every name a reader might type for a kind of tree. Written by "
                  "scripts/species_names.py; read by site/src/pages/api/species.json.ts "
                  "(the app's feed) and search-index.json.ts (the website). The common "
                  "name we print stays the city file's; the rest only answers a search."),
        "_licence": "Names from our own translations and from Wikidata (CC0).",
        "species": species,
        "genera": gen,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    CACHE.write_text(json.dumps({k: cache[k] for k in sorted(cache)}, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
    status(out)


def status(out=None):
    out = out or json.load(open(OUT, encoding="utf-8"))
    sp = out["species"]
    m = [e for e in sp if e.get("mapped", True)]
    print("species: %d mapped, %d not mapped yet; genera: %d" % (len(m), len(sp) - len(m), len(out["genera"])))
    for lang in ["en"] + LANGS:
        n = sum(1 for e in m if lang in e.get("names", {}))
        print("  %s: %d of %d mapped species have a name to search by" % (lang, n, len(m)))


if __name__ == "__main__":
    if "--status" in sys.argv:
        status()
    else:
        build(refresh="--refresh" in sys.argv)
