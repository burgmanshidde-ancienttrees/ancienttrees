"""A small copy of every shared photograph, for the tiles.

    python3 scripts/shared_thumbs.py          make what is missing, drop orphans
    python3 scripts/shared_thumbs.py --dry    say what it would do

WHY (Hidde, 2026-11-13: "fix maar", after Supabase mailed that the org passed
the free plan's 5 GB of egress a month). The copies in the public bucket
shared-sightings average about 900 KB, and a profile's grid of tiles loaded
each one whole to show it 200 pixels wide. He did not want the photographs
themselves made smaller ("dit is wel jammer, kan het ook zonder dit"), so the
full copy stays exactly as it is and opens on the tree's own shared page; the
tiles load this copy instead: 600 px on the long edge, JPEG 80, about 60 KB.

Where: the public bucket shared-thumbs, at the same path as the original
(<account id>/<sighting id>.jpg). A separate bucket, never a folder inside
shared-sightings: sightings_link.py deletes every folder there that is not a
living account's.

Never outlives its original: a thumb whose original is gone (the person
unshared it, or their account went and sightings_link.py took the copy down)
is deleted on the same run, so this script runs right after that one in
nightly.yml. Downloads only originals that have no thumb yet: the first run
reads them all once, then only what is new.

A tile whose thumb is not made yet (shared since the last knock) falls back to
the full copy, so nothing ever shows empty. Needs SUPABASE_SERVICE_KEY and
Pillow. Prints counts only.
"""
import io
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

URL = "https://caimvxiyrtifilimlkqw.supabase.co"
SRC = "shared-sightings"
DST = "shared-thumbs"
EDGE = 600
KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")


def call(path, body=None, method=None, headers=None, raw=False):
    data = body if raw else (json.dumps(body).encode() if body is not None else None)
    h = {"apikey": KEY, "Authorization": "Bearer " + KEY}
    if not raw:
        h["Content-Type"] = "application/json"
    h.update(headers or {})
    r = urllib.request.Request(URL + path, data=data, method=method or ("POST" if data else "GET"), headers=h)
    with urllib.request.urlopen(r, timeout=60) as resp:
        out = resp.read()
    return out


def files(bucket):
    """Every object path, one folder level deep (<account id>/<file>)."""
    out = set()
    for folder in json.loads(call(f"/storage/v1/object/list/{bucket}", {"prefix": "", "limit": 1000})):
        if folder.get("id"):
            continue
        offset = 0
        while True:
            rows = json.loads(call(f"/storage/v1/object/list/{bucket}",
                                   {"prefix": folder["name"] + "/", "limit": 1000, "offset": offset}))
            out |= {folder["name"] + "/" + r["name"] for r in rows if r.get("id")}
            if len(rows) < 1000:
                break
            offset += 1000
    return out


def ensure_bucket(dry):
    try:
        call(f"/storage/v1/bucket/{DST}")
        return True
    except urllib.error.HTTPError as e:
        if e.code not in (400, 404):
            raise
    if dry:
        print(f"shared_thumbs: bucket {DST} would be made (dry)")
        return False
    call("/storage/v1/bucket", {"id": DST, "name": DST, "public": True,
                                "file_size_limit": 1_000_000, "allowed_mime_types": ["image/jpeg"]})
    print(f"shared_thumbs: bucket {DST} made, public")
    return True


def thumb(data):
    from PIL import Image, ImageOps
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    img.thumbnail((EDGE, EDGE))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=80, optimize=True)
    return buf.getvalue()


def main():
    dry = "--dry" in sys.argv
    if not KEY:
        sys.exit("shared_thumbs: no SUPABASE_SERVICE_KEY")
    have_bucket = ensure_bucket(dry)
    originals = files(SRC)
    thumbs = files(DST) if have_bucket else set()
    orphans = sorted(thumbs - originals)
    missing = sorted(originals - thumbs)
    if orphans and not dry:
        call(f"/storage/v1/object/{DST}", {"prefixes": orphans}, "DELETE")
    made = read = 0
    for path in missing:
        if dry:
            continue
        q = urllib.parse.quote(path)
        try:
            data = call(f"/storage/v1/object/authenticated/{SRC}/{q}")
            small = thumb(data)
        except Exception as e:
            print(f"shared_thumbs: one original unreadable ({e.__class__.__name__})")
            continue
        read += len(data)
        call(f"/storage/v1/object/{DST}/{q}", small, "POST", raw=True,
             headers={"Content-Type": "image/jpeg", "x-upsert": "true", "cache-control": "max-age=604800"})
        made += 1
    print(f"shared_thumbs: {len(originals)} shared, {made} thumb(s) made "
          f"({read / 1e6:.1f} MB read), {len(orphans)} orphan(s) {'would go' if dry else 'removed'}"
          + (f", {len(missing)} would be made (dry)" if dry else ""))


if __name__ == "__main__":
    main()
