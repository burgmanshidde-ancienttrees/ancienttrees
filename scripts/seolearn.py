# What makes a page score, learned by comparing our own pages against each
# other.
#
# Written 2026-09-10 on Hidde's question, "do we have an seo learning mechanism
# built in the runs", and his own answer to it: "see which ones score learn and
# adjust others accordingly."
#
# The honest answer to the question was no. Everything we had was a MEASUREMENT
# loop, not a learning one: the digest reads Search Console and re-ranks
# data/city-queue.json, the depth rule asks whether a city has any impressions,
# langcheck compares a translation against its English twin. Every one of those
# asks "does this page have demand". None of them asks "what do the pages that
# convert have that the others do not", which is the only question whose answer
# transfers to a page that has not been written yet.
#
# The measure is CTR against EXPECTED CTR at the position the page actually
# holds, because a raw CTR comparison is mostly a comparison of positions.
# expected_ctr() lives in daily_digest.py and DATA.md prints it per city as
# "Normal there"; this file reads that column rather than recomputing it, so
# there is one authority for the curve.
#
# WHY IT READS DATA.md AND NOT SEARCH CONSOLE: the GSC credentials live in
# data-digest.yml and weekly-analysis.yml and never in a night run, so DATA.md
# is the only place a run can read the answer. Same reasoning as the depth rule.
#
# THE FIRST THING IT FOUND, and it is why the quoted filter is not optional:
# six pages were taking 16 percent of all measured impressions for queries
# written with quotation marks ('"oldest of its species" owl park', 36
# impressions at position 9, zero clicks). Nobody types that. It is a scraper or
# an SEO tool, and it converts at an index of 0.09 against 0.67 for ordinary
# queries. Left in, it does not merely add noise: it made photo coverage look
# like it did not matter, because the contaminated pages sat in the low-photo
# buckets and dragged them below the no-photo bucket.

import json
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A query somebody typed, or a query a machine constructed. Quotation marks are
# Google's exact-phrase operator: real people almost never reach for it, and no
# page of ours has ever taken a click from one.
BOT_QUERY = re.compile(r'["“”]')

# Below this a page's numbers are noise and a bucket built from them says
# nothing. 40 is deliberately low, because the site is small and a higher floor
# would leave nothing to compare.
MIN_IMPRESSIONS = 40


def newest_entry(path=None):
    """The most recent day's block from DATA.md, as a list of lines."""
    path = path or os.path.join(ROOT, "DATA.md")
    lines = open(path, encoding="utf-8").read().split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith("## 2026")]
    if not starts:
        return []
    first = starts[0]
    second = starts[1] if len(starts) > 1 else len(lines)
    return lines[first:second]


def city_rows(block):
    """The 'Depth is allowed on these cities' table, parsed.

    That table is the only per-page Search Console readback that survives
    outside CI, and it already carries the expected-CTR column."""
    rows = []
    try:
        i = next(j for j, l in enumerate(block)
                 if l.startswith("**Depth is allowed"))
    except StopIteration:
        return rows
    for line in block[i:]:
        if line.startswith("**") and rows:
            break
        if not line.startswith("|") or line.startswith("|---") or "City |" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7:
            continue
        try:
            rows.append({
                "city": cells[0],
                "clicks": int(cells[1]),
                "impressions": int(cells[2]),
                "ctr": float(cells[3].rstrip("%")),
                "position": float(cells[4]),
                "expected": float(cells[5].rstrip("%")),
                "query": cells[6],
            })
        except ValueError:
            continue
    return rows


def page_facts():
    """What each city page actually carries, measured from data/cities."""
    facts = {}
    for path in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        trees = doc.get("trees") or []
        if not trees:
            continue
        shown = sum(1 for t in trees
                    if (t.get("photo") or {}).get("url")
                    and (t.get("photo") or {}).get("status") in ("approved", "found_needs_check"))
        facts[os.path.basename(path)[:-5]] = {
            "trees": len(trees),
            "photos": shown,
            "photo_share": shown / len(trees),
            "confirmed": sum(1 for t in trees if t.get("location_precision") == "confirmed"),
        }
    return facts


def joined():
    """City rows with their page facts attached, and the bot rows marked."""
    facts = page_facts()
    out = []
    for r in city_rows(newest_entry()):
        f = facts.get(r["city"])
        if not f or r["impressions"] < MIN_IMPRESSIONS:
            continue
        r.update(f)
        r["bot"] = bool(BOT_QUERY.search(r["query"]))
        r["index"] = (r["ctr"] / r["expected"]) if r["expected"] else 0.0
        out.append(r)
    return out


def band(rows, label):
    """One bucket's conversion against what its positions should have given us.

    The index is clicks divided by expected clicks: 1.0 means the bucket
    converts exactly as a page at that position normally does, 0.5 means half."""
    if not rows:
        return None
    impressions = sum(r["impressions"] for r in rows)
    clicks = sum(r["clicks"] for r in rows)
    expected = sum(r["impressions"] * r["expected"] / 100 for r in rows)
    return {
        "label": label, "n": len(rows), "impressions": impressions,
        "clicks": clicks, "ctr": 100 * clicks / impressions if impressions else 0,
        "index": clicks / expected if expected else 0,
    }


def report(rows):
    clean = [r for r in rows if not r["bot"]]
    bots = [r for r in rows if r["bot"]]
    lines = []
    add = lines.append

    add("SEO learning pass: %d pages over %d impressions, %d of them clean"
        % (len(rows), MIN_IMPRESSIONS, len(clean)))
    add("Index 1.00 means a page converts exactly as its position normally does.")
    add("")

    if bots:
        bi = sum(r["impressions"] for r in bots)
        total = sum(r["impressions"] for r in rows) or 1
        add("NOT DEMAND: %d pages, %d impressions (%d%% of the sample), %d clicks."
            % (len(bots), bi, round(100 * bi / total), sum(r["clicks"] for r in bots)))
        add("Their biggest query uses Google's exact-phrase operator, so a person "
            "did not type it. Read their impressions as zero, here and in the queue.")
        for r in sorted(bots, key=lambda r: -r["impressions"]):
            add("   %-16s i%-5d c%-3d %s" % (r["city"], r["impressions"], r["clicks"], r["query"][:52]))
        add("")

    def group(title, buckets):
        add(title)
        for label, pred in buckets:
            b = band([r for r in clean if pred(r)], label)
            if b:
                add("   %-22s n%-3d i%-5d c%-4d ctr %4.1f%%  index %.2f"
                    % (b["label"], b["n"], b["impressions"], b["clicks"], b["ctr"], b["index"]))
        add("")

    group("SHARE OF TREES CARRYING A PHOTOGRAPH", [
        ("none", lambda r: r["photo_share"] == 0),
        ("under 20%", lambda r: 0 < r["photo_share"] < 0.2),
        ("20 to 40%", lambda r: 0.2 <= r["photo_share"] < 0.4),
        ("40% and over", lambda r: r["photo_share"] >= 0.4),
    ])
    group("TREES ON THE PAGE", [
        ("4 to 6", lambda r: r["trees"] <= 6),
        ("7 to 15", lambda r: 7 <= r["trees"] <= 15),
        ("16 to 25", lambda r: 16 <= r["trees"] <= 25),
        ("over 25", lambda r: r["trees"] > 25),
    ])

    # The actionable list. A page with real demand, a real query and an index
    # under 0.5 is losing clicks it has already earned the right to, which is
    # worth more than a new page: the impressions exist and are being wasted.
    worst = sorted([r for r in clean if r["index"] < 0.5],
                   key=lambda r: -(r["impressions"] * (r["expected"] / 100) - r["clicks"]))
    if worst:
        add("EARNED AND WASTED, worst first (real queries, converting under half)")
        add("These have the demand already. Fixing one is worth more than a new page.")
        for r in worst[:12]:
            missing = []
            if r["photo_share"] < 0.2:
                missing.append("%d/%d photos" % (r["photos"], r["trees"]))
            lost = r["impressions"] * r["expected"] / 100 - r["clicks"]
            add("   %-16s i%-5d c%-3d p%-5.1f index %.2f  loses ~%.0f clicks/10d  %s"
                % (r["city"], r["impressions"], r["clicks"], r["position"],
                   r["index"], lost, ", ".join(missing) or "-"))
    return "\n".join(lines)


def main():
    rows = joined()
    if not rows:
        print("seolearn: no city table in DATA.md's newest entry, nothing to learn from")
        return 0
    print(report(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
