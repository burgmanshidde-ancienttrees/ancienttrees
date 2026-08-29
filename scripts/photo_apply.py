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
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "photo-queue.json")
UA = "AncientTrees/1.0 (https://ancienttrees.app)"


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


def measure(url):
    """Width and height of the image we are about to record, read off the bytes.

    Not a nicety. /api/trees.json carries photo.width and photo.height and the
    iOS app decodes them as numbers, so a photo written without them turns the
    field null for every reader at once and the feed contract check refuses the
    whole deploy. That is exactly what happened on 2026-08-29: one approval here
    wrote no dimensions, and the site did not deploy again until somebody read
    the failure. The header is a few kilobytes, so this costs one request.

    Returns (None, None) rather than raising. A photo with no dimensions still
    should not ship, so the caller says so out loud instead of writing silence.
    """
    import struct
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        raw = urllib.request.urlopen(req, timeout=30).read(400_000)
    except Exception:
        return None, None
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", raw[16:24])
        return int(w), int(h)
    i = 2
    while i < len(raw) - 9:
        if raw[i] != 0xFF:
            i += 1
            continue
        marker = raw[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB):
            h, w = struct.unpack(">HH", raw[i + 5:i + 9])
            return int(w), int(h)
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + struct.unpack(">H", raw[i + 2:i + 4])[0]
    return None, None


def photo_block(cand, status, note=None):
    """The photo dict a city file gets, dimensions included, never without."""
    url = full_image(cand)
    w, h = measure(url)
    block = {
        "url": url,
        "license": cand.get("licence"),
        "attribution": credit(cand),
        "status": status,
    }
    if note is not None:
        block["note"] = note
    if w and h:
        block["width"] = w
        block["height"] = h
    else:
        print(f"  WARNING: could not read the size of {url}. The feed carries "
              f"photo.width and photo.height as numbers and a null breaks every "
              f"installed app, so fill them in by hand before pushing.")
    return block


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
        tree["photo"] = photo_block(cand, "approved")
        write_city(path, city)
        print(f"{tree_id}: approved -> {tree['photo']['url']}")
        print(f"          {tree['photo']['license']} / {tree['photo']['attribution']}")
    elif verb == "hold":
        path, city, tree = find_tree(tree_id)
        tree["photo"] = photo_block(cand, "held", note=reason)
        write_city(path, city)
        print(f"{tree_id}: held ({reason})")
    else:
        print(f"{tree_id}: rejected ({reason})")

    json.dump(queue, open(QUEUE, "w"), indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
