"""Has a reader's app sighting really changed since Hidde last saw it?

The app sends every sighting on the phone back to the server whenever it gets
a session (SightingSync.merge -> pushAll), and every send stamps `updated_at`
with the time of sending. So `updated_at` moves when nothing changed: on
2026-10-27 the Tangier fig's sighting came back on the digest page as new,
and one person's thirteen sightings had all been "saved" in the same minute on
10-25 (Hidde: "is this a bug that the person uploaded it again?").

So the digest never trusts `updated_at` alone. It keeps a fingerprint of what
a reader can actually change (the tree, the name, the note, the photographs,
species, age, sharing) for every sighting Hidde has seen, in
data/sightings-shown.json, and shows a sighting again only when that
fingerprint differs. The file holds sighting ids and hashes, never words.

    python3 scripts/sighting_changes.py --seed   record every shared sighting
                                                 saved before the last look
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(ROOT, "data", "sightings-shown.json")

# What a reader can change about a sighting. `updated_at` is deliberately not
# here: it is the field that lies.
FIELDS = ("tree_id", "name", "note", "photo", "extra_photos", "sign_photo",
          "species", "age", "shared")
SELECT = "id,user_id,status,updated_at," + ",".join(FIELDS)


def fingerprint(row):
    """A short hash of the parts of a sighting a reader can change."""
    blob = json.dumps([row.get(f) for f in FIELDS], sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:16]


def load():
    try:
        return json.load(open(FILE, encoding="utf-8")).get("shown", {})
    except Exception:
        return {}


def save(shown):
    with open(FILE, "w", encoding="utf-8") as fh:
        json.dump({"_note": "Fingerprint of each reader sighting as Hidde last saw it on the digest "
                            "page (scripts/sighting_changes.py). A sighting shows again only when "
                            "this changes; the app's sync moves updated_at without a change.",
                   "shown": dict(sorted(shown.items()))}, fh, indent=1)
        fh.write("\n")


def status(row, shown=None):
    """'new' (never seen), 'changed' (seen, then really changed) or 'same'."""
    shown = load() if shown is None else shown
    before = shown.get(row.get("id"))
    if before is None:
        return "new"
    return "same" if before == fingerprint(row) else "changed"


def seed():
    """One time: every shared sighting saved before Hidde's last look counts as
    seen in its present form. Anything saved after it stays new."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import inbox
    key = inbox.load_key()
    if not key:
        print("sighting_changes: no database key on this Mac, nothing seeded")
        return 1
    try:
        seen_at = json.load(open(os.path.join(ROOT, "data", "digest-seen.json"))).get("seen_at")
    except Exception:
        seen_at = None
    if not seen_at:
        print("sighting_changes: no last look recorded, nothing seeded")
        return 1
    rows = inbox.get("/rest/v1/sightings?select=%s&shared=eq.true" % SELECT, key) or []
    shown = load()
    n = skipped = 0
    for r in rows:
        if (r.get("updated_at") or "")[:19] > seen_at:
            skipped += 1
            continue
        if r["id"] not in shown:
            shown[r["id"]] = fingerprint(r)
            n += 1
    save(shown)
    print("sighting_changes: %d seeded, %d saved after %s left as new" % (n, skipped, seen_at))
    return 0


if __name__ == "__main__":
    if "--seed" in sys.argv:
        sys.exit(seed())
    print(__doc__)
