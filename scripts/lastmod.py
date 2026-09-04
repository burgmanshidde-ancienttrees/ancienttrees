#!/usr/bin/env python3
"""Date every page by when its CONTENT last changed, not when its file did.

Why (2026-09-04). The sitemap's lastmod came from the last git commit that
touched a page's source file. That is right for a page with a file of its
own and wrong for a tree, because a city file holds twenty of them: one
commit on 2026-09-03 re-indented 21 city files without changing a fact, and
another set best_time on 139 trees across 69 files, and between them 2,035 of
the 4,244 URLs in the sitemap told Google they had changed that day. Google
honours lastmod only while it is credible and discounts the whole file when
it is not, which matters on a domain whose crawl is rationed: 655 pages sat
at "Discovered - currently not indexed" the same week. qa.py's existing check
only asks that the dates VARY, so it could not see this.

What this does. For every page whose content lives inside a shared file
(a city page, its question page, each tree page, and the translated versions
of all three) it hashes the part of the data that page is built from, with
keys sorted and whitespace dropped so a re-indent or a re-ordering changes
nothing. `data/lastmod.json` keeps one line per page: the hash and the date
it last changed. Unchanged hash, unchanged date. Changed or new, today.
The build reads the map (site/src/lib/sitemap-integration.ts) and only
falls back to git for pages this script does not cover: species, country and
collection pages have a file each, so git is already right for them.

Seeding. A page not yet in the map takes the date of the last commit that
touched its file, skipping the commits listed in BULK_COMMITS, which are the
ones known to have touched files without changing pages. That is the
conservative direction: a tree whose season peak WAS set on 09-03 reads a
little older than the truth, which understates change rather than shouting
it, and the next real edit corrects it.

Where it runs. deploy.yml runs `--write` before the build so the sitemap
sees today's date on anything that changed; nightly.yml runs `--write` and
commits the map so the record survives. A session that publishes can run it
too; it never needs to, because the build does.

Usage:
  python3 scripts/lastmod.py            # report: changed, new, gone
  python3 scripts/lastmod.py --write    # update data/lastmod.json
"""
import datetime
import glob
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, "data", "lastmod.json")
CITIES = os.path.join(ROOT, "data", "cities")
I18N = os.path.join(ROOT, "data", "i18n")

# Commits that rewrote city files without changing any page. Seeding skips
# them so a page's first recorded date is the last commit that meant it.
BULK_COMMITS = {
    "7f527c8b2d1f2652b3e94ea9acf6314568bd798b",  # 2026-09-03 re-indented 21 city files
    "1a765fb7",                                   # 2026-09-03 best_time backfill, 69 files for 139 trees
}

# Fields on a tree that only its own page renders. Everything else about a
# tree (name, species, photo, age, place, season) also shows on the city
# card and the question page, so a change there dates those pages too.
TREE_ONLY = {"story", "verify_notes", "verified_sources", "curation_status",
             "how_to_recognise", "submitted_by"}


def h(obj):
    s = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


def renderable(t):
    loc = t.get("location") or {}
    return bool(t.get("story")) and loc.get("latitude") is not None and loc.get("longitude") is not None


def city_view(city):
    """What the city page and the question page are built from."""
    top = {k: v for k, v in city.items() if k != "trees"}
    trees = [{k: v for k, v in t.items() if k not in TREE_ONLY}
             for t in city.get("trees", []) if renderable(t)]
    return {"city": top, "trees": trees}


def entries():
    """key -> (hash, source file) for every page this script dates."""
    out = {}
    cities = {}
    for p in sorted(glob.glob(os.path.join(CITIES, "*.json"))):
        slug = os.path.basename(p)[:-5]
        try:
            city = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(city, dict) or not any(renderable(t) for t in city.get("trees", [])):
            continue
        cities[slug] = city
        rel = f"data/cities/{slug}.json"
        cv = h(city_view(city))
        out[f"city:{slug}"] = (cv, rel)
        out[f"q:{slug}"] = (cv, rel)
        for t in city.get("trees", []):
            if renderable(t) and t.get("id"):
                out[f"tree:{t['id']}"] = (h(t), rel)
    if os.path.isdir(I18N):
        for p in sorted(glob.glob(os.path.join(I18N, "*", "*.json"))):
            lang = os.path.basename(os.path.dirname(p))
            slug = os.path.basename(p)[:-5]
            city = cities.get(slug)
            if not city:
                continue
            try:
                ov = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            rel = f"data/i18n/{lang}/{slug}.json"
            ov_top = {k: v for k, v in ov.items() if k != "trees"}
            ov_trees = ov.get("trees") or {}
            cv = h({"overlay": ov_top, "overlay_trees": {
                        k: {kk: vv for kk, vv in v.items() if kk not in TREE_ONLY}
                        for k, v in ov_trees.items() if isinstance(v, dict)},
                    "en": city_view(city)})
            out[f"{lang}:city:{slug}"] = (cv, rel)
            out[f"{lang}:q:{slug}"] = (cv, rel)
            for t in city.get("trees", []):
                if renderable(t) and t.get("id"):
                    out[f"{lang}:tree:{t['id']}"] = (h({"overlay": ov_trees.get(t["id"]), "en": t}), rel)
    return out


def git_dates():
    """file -> date of its last commit, skipping the bulk rewrites."""
    try:
        raw = subprocess.run(
            ["git", "log", "--no-merges", "--format=%x00%H %cs", "--name-only",
             "--", "data/cities", "data/i18n"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except Exception:
        return {}
    dates, cur, skip = {}, None, False
    for line in raw.splitlines():
        if line.startswith("\x00"):
            sha, _, day = line[1:].partition(" ")
            skip = any(sha.startswith(b) for b in BULK_COMMITS)
            cur = day
            continue
        f = line.strip()
        if f and cur and not skip and f not in dates:
            dates[f] = cur
    return dates


def main():
    write = "--write" in sys.argv
    today = datetime.date.today().isoformat()
    try:
        doc = json.load(open(MAP, encoding="utf-8"))
        old = doc.get("entries", {})
    except Exception:
        old = {}
    now = entries()
    gd = None
    new = changed = kept = 0
    fresh = {}
    for key, (hsh, rel) in now.items():
        prev = old.get(key)
        if prev and prev.get("h") == hsh:
            fresh[key] = prev
            kept += 1
        elif prev:
            fresh[key] = {"h": hsh, "d": today}
            changed += 1
        else:
            if gd is None:
                gd = git_dates()
            fresh[key] = {"h": hsh, "d": gd.get(rel, today)}
            new += 1
    gone = len(set(old) - set(now))
    print(f"lastmod: {len(fresh)} pages, {kept} unchanged, {changed} changed, "
          f"{new} new, {gone} gone")
    if write:
        doc = {"_note": "One line per page whose content lives inside a shared "
                        "file: the hash of what the page is built from and the "
                        "date it last changed. Written by scripts/lastmod.py, "
                        "read by site/src/lib/sitemap-integration.ts. Never "
                        "edit by hand; a re-indent or re-order changes nothing "
                        "here, which is the point.",
               "entries": dict(sorted(fresh.items()))}
        with open(MAP, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=0)
            fh.write("\n")
        print(f"wrote {os.path.relpath(MAP, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
