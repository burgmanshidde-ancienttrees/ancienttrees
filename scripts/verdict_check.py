#!/usr/bin/env python3
"""Check a viewing pass's verdicts against the images it was actually shown.

    python3 scripts/verdict_check.py out/verdicts/geoB.json out/photo-pass3
    python3 scripts/verdict_check.py out/verdicts/*.json out/photo-pass2

Exit 0 when every row is answerable, 1 when anything is not, and print what.

Why this exists (2026-09-10). A photo-judge pass returns verdicts and the main
session applies them with photo_verdicts.py. Twice in two days a pass reported
work it had not done: one sent an interim summary naming eight approvals whose
tree ids do not exist in data/cities, and one reported six approvals, with
photographers, distances and Wikidata ids, whose verdicts file never reached
disk at all and whose only recoverable row named a different tree, a different
species and a different distance from the one it described.

Nothing shipped either time, because the ids were checked by hand before
applying. That is exactly the kind of safeguard this project has learned not to
trust: a check you have to remember is a check that gets skipped on the run
where it matters. So it is a script, and the rule it enforces is the strict
one: a verdict is only believable about an image the pass was actually handed,
so every (tree_id, url) pair must appear TOGETHER in a manifest. An id that
exists and a url that exists are not enough; the pairing is the claim.

It cannot tell you whether a judgement is any good. It can tell you the pass
was looking at our files.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def manifest_pairs(pass_dir):
    """Every (tree_id, url) the pass was shown, from every manifest under it."""
    pairs, by_tree = set(), {}
    for m in sorted(glob.glob(os.path.join(pass_dir, "*", "manifest.json"))):
        with open(m, encoding="utf-8") as fh:
            city = json.load(fh)
        for img in city.get("images", []):
            for url in (img.get("thumb"), img.get("page")):
                if url:
                    pairs.add((img["tree_id"], url))
            by_tree.setdefault(img["tree_id"], []).append(img.get("file"))
    return pairs, by_tree


def live_ids():
    out = set()
    for p in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        with open(p, encoding="utf-8") as fh:
            for t in json.load(fh).get("trees", []):
                out.add(t["id"])
    return out


def check(verdict_file, pass_dir):
    with open(verdict_file, encoding="utf-8") as fh:
        rows = json.load(fh)
    pairs, by_tree = manifest_pairs(pass_dir)
    ids = live_ids()
    problems = []
    seen_urls = {}
    for i, r in enumerate(rows):
        tid, url = r.get("tree_id"), r.get("page")
        where = f"row {i}"
        if not tid or not url:
            problems.append(f"{where}: missing tree_id or page")
            continue
        if tid not in ids:
            problems.append(f"{where}: {tid} is not a tree in data/cities")
            continue
        if (tid, url) not in pairs:
            if tid not in by_tree:
                problems.append(f"{where}: {tid} was never in this pass's manifests")
            else:
                problems.append(f"{where}: {tid} was shown "
                                f"{len(by_tree[tid])} image(s), and this url is not one of them")
            continue
        # One approval per tree, and never two rows on one image: photo_apply
        # matches the first candidate whose url matches, so a second row on the
        # same url silently overwrites the first verdict.
        if url in seen_urls:
            problems.append(f"{where}: the same url already has a verdict at row {seen_urls[url]}")
        seen_urls[url] = i
    approved = {}
    for i, r in enumerate(rows):
        if r.get("verdict") == "approve":
            if r["tree_id"] in approved:
                problems.append(f"row {i}: {r['tree_id']} is approved twice "
                                f"(also row {approved[r['tree_id']]})")
            approved[r["tree_id"]] = i
    return rows, problems


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 1
    pass_dir, files = args[-1], args[:-1]
    if not os.path.isdir(pass_dir):
        print(f"{pass_dir} is not a directory")
        return 1
    bad = 0
    for f in files:
        rows, problems = check(f, pass_dir)
        name = os.path.basename(f)
        if problems:
            bad += 1
            print(f"{name}: {len(rows)} rows, {len(problems)} PROBLEM(S)")
            for p in problems[:20]:
                print(f"   {p}")
            if len(problems) > 20:
                print(f"   ... and {len(problems) - 20} more")
        else:
            print(f"{name}: {len(rows)} rows, every one about an image this pass was shown")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
