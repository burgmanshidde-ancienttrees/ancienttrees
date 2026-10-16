#!/usr/bin/env python3
"""What the app's crash reports say, grouped so a person can read them.

    python3 scripts/crashes.py              signatures of the last 30 days
    python3 scripts/crashes.py --days 7     a shorter window
    python3 scripts/crashes.py --raw        skip symbolication, print offsets

Since 1.0 the app posts Apple's MetricKit crash and hang payloads to the
Supabase `diagnostics` table (Kit/Diagnostics.swift, supabase/diagnostics.sql)
and, until 2026-10-16, nothing read them: one reader's 1.0.2 crashed 37 times
from 10-13 to 10-16 and we found out because he mailed. This script is the
reader. daily_digest.py prints its table and health.py turns a burst on a
store build into rung-2 work.

MetricKit only delivers from phones whose owner shares analytics with app
developers, so this is a sample of the crashes, never the count of them.

A SIGNATURE is the build, the exception type and signal, and the topmost
AncientTrees frame of the thread the crash is attributed to (binary uuid plus
offset into its text segment). Symbolicated with atos when this Mac holds the
matching dSYM; in CI there is none and the raw offset is printed instead.

PRIVACY: the payload carries a device model, an OS build and a region format.
They are used here only to estimate how many phones a signature came from and
never printed or written anywhere: DATA.md sits in a public repository, so the
output is counts and builds, nothing else.

STORE BUILDS: which builds reached the App Store is asked of App Store Connect
(appStoreVersions, READY_FOR_SALE or since replaced) and cached in
data/store-builds.json, so health.py can tell a store build from one Hidde ran
from Xcode on a runner that holds no Apple key.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbox import SUPA, load_key  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE_BUILDS = os.path.join(ROOT, "data", "store-builds.json")
APP_ID = "6806177833"
BINARY = "AncientTrees"
LOAD = 0x100000000
PAGE = 5  # the payload column is big; a larger select times out

# Signatures we already understand, keyed by (build, offset of the top frame).
# `remedy` is what to do if it fires again; crashes before `answered` were
# dealt with already and do not count towards a burst.
KNOWN = {
    ("20", 0xb8180): {
        "remedy": (
            "the empty-tree feedback crash (MyVotes.treeId) in 1.0.2, fixed in "
            "1.0.3 build 35. Its data side was fixed on 2026-10-16 by setting "
            "submissions.tree from '' to NULL; firing again means a new general "
            "feedback row holds tree='' again. Re-run that PATCH with the "
            "service key: submissions?kind=eq.feedback&tree=eq. set to "
            "{\"tree\": null}"),
        "answered": "2026-10-16T08:19:00",
    },
}

BURST = 3          # crashes of one signature on a store build ...
BURST_HOURS = 24   # ... inside this many hours is an act item


def _get(path, key, timeout=30):
    req = urllib.request.Request(SUPA + path, headers={
        "apikey": key, "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def fetch_rows(key, days):
    """Every diagnostics row of the last `days` days, five at a time."""
    since = (datetime.datetime.now(datetime.timezone.utc)
             - datetime.timedelta(days=days)).isoformat()
    q = ("/rest/v1/diagnostics?select=id,kind,app_version,created_at,payload"
         "&created_at=gte." + urllib.parse.quote(since) + "&order=id.asc")
    rows, offset = [], 0
    while True:
        page = _get(q + "&limit=%d&offset=%d" % (PAGE, offset), key)
        rows.extend(page)
        if len(page) < PAGE:
            return rows
        offset += PAGE


def _build_of(app_version, meta):
    b = (meta or {}).get("appBuildVersion")
    if b:
        return str(b)
    m = re.search(r"\((\w+)\)", app_version or "")
    return m.group(1) if m else "?"


def _top_frame(diag):
    """The first AncientTrees frame from the top of the attributed thread."""
    stacks = (diag.get("callStackTree") or {}).get("callStacks") or []
    attributed = [s for s in stacks if s.get("threadAttributed")] or stacks[:1]
    for s in attributed:
        frames = list(s.get("callStackRootFrames") or [])
        while frames:
            f = frames[0]
            # A build Hidde runs from Xcode is AncientTrees.debug.dylib.
            if (f.get("binaryName") or "").startswith(BINARY):
                return (f.get("binaryName"), f.get("binaryUUID"),
                        f.get("offsetIntoBinaryTextSegment"))
            frames = list(f.get("subFrames") or [])
    return None, None, None


def diagnostics(rows):
    """One record per crash or hang inside the rows' payloads."""
    out = []
    for r in rows:
        try:
            p = json.loads(r.get("payload") or "{}")
        except ValueError:
            continue
        for kind, field in (("crash", "crashDiagnostics"), ("hang", "hangDiagnostics")):
            for d in p.get(field) or []:
                meta = d.get("diagnosticMetaData") or {}
                binary, uuid, off = _top_frame(d)
                out.append({
                    "kind": kind,
                    "build": _build_of(r.get("app_version"), meta),
                    "version": meta.get("appVersion") or (r.get("app_version") or "?").split(" ")[0],
                    "testflight": bool(meta.get("isTestFlightApp")),
                    "exc": "%s/%s" % (meta.get("exceptionType", "-"), meta.get("signal", "-")),
                    "binary": binary,
                    "uuid": uuid,
                    "offset": off,
                    "at": r.get("created_at"),
                    # In memory only, to count phones; never printed.
                    "_phone": (meta.get("deviceType"), meta.get("osVersion"),
                               meta.get("regionFormat")),
                })
    return out


_dsyms = {}


def _tidy(line):
    """'f() (in AncientTrees) (MyVotes.swift:42)' -> 'f() (MyVotes.swift:42)'."""
    line = re.sub(r" \(in [^)]+\)", "", line)
    line = line.replace(" (/<compiler-generated>:0)", "")
    return line.replace("|", "/").strip()


def symbol(binary, uuid, offset):
    """atos on the matching dSYM, or None when this machine has none.
    Inlined frames come back too, innermost first; the line that names our
    own code is what a person needs, so runtime frames are folded away."""
    if not uuid or offset is None:
        return None
    if uuid not in _dsyms:
        path = None
        try:
            r = subprocess.run(["mdfind", "com_apple_xcode_dsym_uuids == %s" % uuid],
                               capture_output=True, text=True, timeout=20)
            for cand in r.stdout.split("\n"):
                d = os.path.join(cand.strip(), "Contents", "Resources", "DWARF")
                if cand.strip() and os.path.isdir(d) and os.listdir(d):
                    path = os.path.join(d, sorted(os.listdir(d))[0])
                    break
        except (OSError, subprocess.SubprocessError):
            pass
        _dsyms[uuid] = path
    dwarf = _dsyms[uuid]
    if not dwarf:
        return None
    # The app executable loads at 0x100000000; the Xcode debug dylib at 0.
    load = 0 if (binary or "").endswith(".dylib") else LOAD
    try:
        r = subprocess.run(["atos", "-arch", "arm64", "-o", dwarf, "-l", hex(load),
                            "-i", hex(load + offset)],
                           capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    lines = [_tidy(ln) for ln in r.stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    ours = [ln for ln in lines if ".swift:" in ln]
    head = lines[0] if "Swift runtime failure" in lines[0] else None
    picked = ([head] if head else []) + ours[:2]
    return " < ".join(picked or lines[:2])


def group(diags, symbolicate=True):
    """One row per signature: count, first and last seen, phones, builds."""
    sigs = {}
    for d in diags:
        k = (d["kind"], d["build"], d["exc"], d["uuid"], d["offset"])
        s = sigs.setdefault(k, {
            "kind": d["kind"], "build": d["build"], "version": d["version"],
            "exc": d["exc"], "binary": d["binary"], "uuid": d["uuid"],
            "offset": d["offset"],
            "count": 0, "first": d["at"], "last": d["at"], "_phones": set(),
            "times": [], "testflight": d["testflight"]})
        s["count"] += 1
        s["first"] = min(s["first"], d["at"])
        s["last"] = max(s["last"], d["at"])
        s["_phones"].add(d["_phone"])
        s["times"].append(d["at"])
    out = []
    for s in sigs.values():
        s["phones"] = len(s.pop("_phones"))
        s["frame"] = ("%s+%s" % (s["binary"], hex(s["offset"]))
                      if s["offset"] is not None else "(no %s frame)" % BINARY)
        s["symbol"] = symbol(s["binary"], s["uuid"], s["offset"]) if symbolicate else None
        known = KNOWN.get((s["build"], s["offset"]))
        s["known"] = known
        out.append(s)
    out.sort(key=lambda s: (-s["count"], s["last"]))
    return out


def _asc_store_builds():
    from asc_auth import bearer_token
    token = bearer_token()
    url = ("https://api.appstoreconnect.apple.com/v1/apps/%s/appStoreVersions?"
           "fields[appStoreVersions]=versionString,appStoreState,build"
           "&include=build&fields[builds]=version&limit=50" % APP_ID)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    with urllib.request.urlopen(req, timeout=20) as r:
        got = json.load(r)
    builds = {b["id"]: (b.get("attributes") or {}).get("version")
              for b in got.get("included") or [] if b.get("type") == "builds"}
    out = {}
    for v in got.get("data") or []:
        a = v.get("attributes") or {}
        rel = ((v.get("relationships") or {}).get("build") or {}).get("data") or {}
        num = builds.get(rel.get("id"))
        if num:
            out[str(num)] = {"version": a.get("versionString"), "state": a.get("appStoreState")}
    return out


SHIPPED = ("READY_FOR_SALE", "REPLACED_WITH_NEW_VERSION")


def store_builds(refresh=True):
    """{build: {version, state}} for every App Store version. Asks Apple when
    the key is here and caches the answer; otherwise reads the cache."""
    if refresh:
        try:
            got = _asc_store_builds()
            if got:
                with open(STORE_BUILDS, "w", encoding="utf-8") as f:
                    json.dump(got, f, indent=1, sort_keys=True)
                    f.write("\n")
                return got
        except (SystemExit, Exception):
            pass
    try:
        with open(STORE_BUILDS, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def is_store(build, stores):
    return (stores.get(str(build)) or {}).get("state") in SHIPPED


def _when(iso):
    """Supabase's timestamps carry five or six fraction digits, which older
    Pythons refuse; seconds are plenty here."""
    return datetime.datetime.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S").replace(
        tzinfo=datetime.timezone.utc)


def bursts(sigs, stores, now=None):
    """Signatures on a store build that fired BURST times in BURST_HOURS."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    out = []
    for s in sigs:
        if s["kind"] != "crash" or not is_store(s["build"], stores):
            continue
        cut = now - datetime.timedelta(hours=BURST_HOURS)
        if s["known"] and s["known"].get("answered"):
            cut = max(cut, _when(s["known"]["answered"]))
        n = sum(1 for t in s["times"] if _when(t) >= cut)
        if n >= BURST:
            out.append((s, n))
    return out


def load(days=30, symbolicate=True):
    """(signatures, store builds), or (None, reason) when the key is absent."""
    key = load_key()
    if not key:
        return None, "SUPABASE_SERVICE_KEY not set"
    sigs = group(diagnostics(fetch_rows(key, days)), symbolicate)
    return sigs, store_builds()


def where(s):
    return s["symbol"] or s["frame"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--raw", action="store_true")
    a = ap.parse_args()
    sigs, stores = load(a.days, not a.raw)
    if sigs is None:
        print("crashes: %s; nothing read." % stores)
        return 0
    print("Crash and hang signatures, last %d days (a sample: MetricKit only "
          "reports from phones that share analytics)\n" % a.days)
    if not sigs:
        print("  none")
        return 0
    print("| Count | Kind | Build | Store | Exception/signal | Where | Phones | First | Last |")
    print("|---:|---|---|---|---|---|---:|---|---|")
    for s in sigs:
        store = (stores.get(s["build"]) or {}).get("state") or ("TestFlight" if s["testflight"] else "Xcode")
        print("| %d | %s | %s (%s) | %s | %s | %s | %d | %s | %s |" % (
            s["count"], s["kind"], s["version"], s["build"], store, s["exc"],
            where(s), s["phones"], s["first"][:16].replace("T", " "),
            s["last"][:16].replace("T", " ")))
    for s in sigs:
        if s["known"]:
            print("\n  %s on build %s is known: %s" % (s["frame"], s["build"],
                                                       s["known"]["remedy"]))
    for s, n in bursts(sigs, stores):
        print("\n  BURST: %s on store build %s crashed %d times in %dh."
              % (where(s), s["build"], n, BURST_HOURS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
