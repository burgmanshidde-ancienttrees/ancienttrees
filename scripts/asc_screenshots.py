#!/usr/bin/env python3
"""Replace the iPhone screenshots of the version in PREPARE_FOR_SUBMISSION.

Reads the framed panels appstore_frames.py wrote (one folder per ground; the
6.9-inch files at the top, the 6.5-inch copies in 6.5-inch/) and puts them, in
file-name order, into the primary locale's APP_IPHONE_67 and APP_IPHONE_65
sets, deleting whatever those sets held. Other locales without their own set
show the primary's, which is how Connect already behaves. Nothing here submits.

    python3 scripts/asc_screenshots.py <framed-dir>            # dry run
    python3 scripts/asc_screenshots.py <framed-dir> --apply

Written 2026-10-14 for 1.0.3, when the seven panels were otherwise a drag and
drop per size per release.
"""
import glob
import hashlib
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from asc_auth import bearer_token  # noqa: E402

APP = "6806177833"
API = "https://api.appstoreconnect.apple.com/v1"
PRIMARY = "en-GB"
TOK = bearer_token(1200)


def call(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url if url.startswith("http") else API + url, data=data, method=method,
                                 headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{method} {url} -> {e.code}\n{e.read().decode()[:800]}")


def upload(set_id, path):
    data = open(path, "rb").read()
    made = call("POST", "/appScreenshots", {"data": {
        "type": "appScreenshots",
        "attributes": {"fileName": os.path.basename(path), "fileSize": len(data)},
        "relationships": {"appScreenshotSet": {"data": {"type": "appScreenshotSets", "id": set_id}}}}})
    shot = made["data"]
    for op in shot["attributes"]["uploadOperations"]:
        chunk = data[op["offset"]:op["offset"] + op["length"]]
        headers = {h["name"]: h["value"] for h in op.get("requestHeaders", [])}
        req = urllib.request.Request(op["url"], data=chunk, method=op["method"], headers=headers)
        urllib.request.urlopen(req, timeout=120).read()
    call("PATCH", f"/appScreenshots/{shot['id']}", {"data": {
        "type": "appScreenshots", "id": shot["id"],
        "attributes": {"uploaded": True, "sourceFileChecksum": hashlib.md5(data).hexdigest()}}})
    return shot["id"]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    framed, apply = args[0], "--apply" in sys.argv
    sizes = {"APP_IPHONE_67": sorted(glob.glob(os.path.join(framed, "*.png"))),
             "APP_IPHONE_65": sorted(glob.glob(os.path.join(framed, "6.5-inch", "*.png")))}
    for k, v in sizes.items():
        print(k, [os.path.basename(p) for p in v])
        if not v:
            raise SystemExit(f"no panels for {k}")
    v = [x for x in call("GET", f"/apps/{APP}/appStoreVersions?limit=5")["data"]
         if x["attributes"]["appStoreState"] == "PREPARE_FOR_SUBMISSION"]
    if not v:
        raise SystemExit("no version in PREPARE_FOR_SUBMISSION")
    loc = [l for l in call("GET", f"/appStoreVersions/{v[0]['id']}/appStoreVersionLocalizations")["data"]
           if l["attributes"]["locale"] == PRIMARY][0]
    sets = {s["attributes"]["screenshotDisplayType"]: s["id"]
            for s in call("GET", f"/appStoreVersionLocalizations/{loc['id']}/appScreenshotSets")["data"]}
    for kind, files in sizes.items():
        sid = sets.get(kind)
        old = call("GET", f"/appScreenshotSets/{sid}/appScreenshots")["data"] if sid else []
        print(f"{kind}: replace {len(old)} with {len(files)}")
        if not apply:
            continue
        if not sid:
            sid = call("POST", "/appScreenshotSets", {"data": {
                "type": "appScreenshotSets", "attributes": {"screenshotDisplayType": kind},
                "relationships": {"appStoreVersionLocalization": {"data": {
                    "type": "appStoreVersionLocalizations", "id": loc["id"]}}}}})["data"]["id"]
        for o in old:
            call("DELETE", f"/appScreenshots/{o['id']}")
        ids = [upload(sid, f) for f in files]
        call("PATCH", f"/appScreenshotSets/{sid}/relationships/appScreenshots",
             {"data": [{"type": "appScreenshots", "id": i} for i in ids]})
        print(f"  uploaded {len(ids)}")
    print("applied" if apply else "dry run; add --apply to write")


if __name__ == "__main__":
    main()
