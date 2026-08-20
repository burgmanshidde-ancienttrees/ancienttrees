#!/usr/bin/env python3
"""Write a judged photo verdict into the city file and the queue, in one step.

A viewing pass makes a judgement and then has to record it in two places: the
tree's photo block in data/cities/*.json, and the candidate's verdict in
data/photo-queue.json so no image is ever looked at twice. Doing that by hand
is where the mistakes are: an approval written to the city file and not to the
queue means the next pass pays to judge it again, and a rejection written
nowhere means the same street scene comes back every sweep.

    photo_apply.py approve <tree_id> <candidate_url> --reason "crown fills frame"
    photo_apply.py hold    <tree_id> <candidate_url> --reason "may be the other plane"
    photo_apply.py reject  <tree_id> <candidate_url> --reason "street scene, no tree"
    photo_apply.py exhaust <tree_id> --reason "all nine were other cities' trees"

<candidate_url> matches on the Commons page url OR the thumb url, whichever the
pass has to hand. Approve takes the licence and attribution from the queue
entry, so a credit can never drift from the licence it was granted under.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "photo-queue.json")


def find_tree(tree_id):
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f))
        for t in d.get("trees", []):
            if t["id"] == tree_id:
                return f, d, t
    return None, None, None


def full_image(cand):
    """The image the site should render, not the sweep's 960px thumbnail.

    Commons thumb urls carry the sweep's own tracking query and a width bucket;
    img_srcset() picks the width at render time, so what belongs in the file is
    the original. iNaturalist has no such original, so its medium stands."""
    thumb = cand.get("thumb") or ""
    if "upload.wikimedia.org" in thumb and "/thumb/" in thumb:
        base = thumb.split("?")[0]
        parts = base.split("/thumb/", 1)[1].rsplit("/", 1)[0]
        return "https://upload.wikimedia.org/wikipedia/commons/" + parts
    return thumb.split("?")[0] if "inaturalist" not in thumb else thumb


def clean_author(raw):
    """The photographer's NAME, and nothing else they typed into the field.

    Commons' Artist field is free text, and people put a request in it. Catania's
    bunya carries "Ivan Ruggiero\\nI'd appreciate if you could mail me
    (ivanrugg+credit@gmail.com) if you want to use this picture out of the", all
    of which would have been rendered as the credit on a public page. Publishing
    a private email address is the one thing this project never does with a
    person's details, licence or no licence, and it takes the first line only,
    then removes any address or url that survives on it.
    """
    first = (raw or "").strip().splitlines()[0] if (raw or "").strip() else ""
    first = re.sub(r"\S+@\S+", "", first)
    first = re.sub(r"https?://\S+", "", first)
    # iNaturalist hands back a whole sentence: "(c) Skjold Sondergaard, some
    # rights reserved (CC BY)". The licence is recorded in its own field, so
    # repeating it inside the credit is noise, and the (c) belongs to the
    # licence rather than to the name.
    first = re.sub(r"^\(c\)\s*|^©\s*", "", first, flags=re.I)
    first = re.sub(r",?\s*(some|all)\s+rights\s+reserved.*$", "", first, flags=re.I)
    first = re.sub(r"\s*\((?:CC[^)]*|public domain|pd)\)\s*$", "", first, flags=re.I)
    # A username qualified by the wiki it came from is still just the username.
    first = re.sub(r"\s+at\s+\w+\s+Wikipedia\s*$", "", first, flags=re.I)
    # A name does not contain a sentence. If a first line still runs on, keep
    # the part before the first clause break rather than printing an essay.
    first = re.split(r"\s+[-–|,]\s+|\s{2,}", first)[0]
    return first.strip(" .,;:-")[:80]


def write_city(path, city):
    """Write a city file the way every other writer here does: indent 2 and a
    trailing newline.

    This wrote indent=1 and no final newline, which is not what data/cities
    holds, so approving one photograph reformatted the whole file: a one-field
    change arrived as a 724-line diff on Graz. A real edit hidden inside that
    much churn is a review nobody can do.
    """
    with open(path, "w") as fh:
        json.dump(city, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def credit(cand):
    author = clean_author(cand.get("author"))
    if "inaturalist" in (cand.get("source") or ""):
        return f"{author}, via iNaturalist" if author else "via iNaturalist"
    return f"{author}, via Wikimedia Commons" if author else "via Wikimedia Commons"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    verb, tree_id = sys.argv[1], sys.argv[2]
    url = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else None
    reason = ""
    if "--reason" in sys.argv:
        reason = sys.argv[sys.argv.index("--reason") + 1]

    queue = json.load(open(QUEUE))
    entry = queue["trees"].get(tree_id)
    if entry is None:
        print(f"{tree_id}: not in the queue")
        return 1

    if verb == "exhaust":
        entry["exhausted"] = reason or "viewing pass found the source empty"
        json.dump(queue, open(QUEUE, "w"), indent=1, ensure_ascii=False)
        print(f"{tree_id}: marked exhausted ({entry['exhausted']})")
        return 0

    cand = None
    for c in entry.get("candidates", []):
        if url in (c.get("url"), c.get("thumb")) or (url and url in (c.get("thumb") or "")):
            cand = c
            break
    if cand is None:
        print(f"{tree_id}: no candidate matching {url}")
        return 1

    cand["judged"] = verb
    if reason:
        cand["verdict"] = reason

    if verb == "approve":
        path, city, tree = find_tree(tree_id)
        if tree is None:
            print(f"{tree_id}: no such tree in data/cities")
            return 1
        tree["photo"] = {
            "url": full_image(cand),
            "license": cand.get("licence"),
            "attribution": credit(cand),
            "status": "approved",
        }
        write_city(path, city)
        print(f"{tree_id}: approved -> {tree['photo']['url']}")
        print(f"          {tree['photo']['license']} / {tree['photo']['attribution']}")
    elif verb == "hold":
        path, city, tree = find_tree(tree_id)
        tree["photo"] = {
            "url": full_image(cand),
            "license": cand.get("licence"),
            "attribution": credit(cand),
            "status": "held",
            "note": reason,
        }
        write_city(path, city)
        print(f"{tree_id}: held ({reason})")
    else:
        print(f"{tree_id}: rejected ({reason})")

    json.dump(queue, open(QUEUE, "w"), indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
