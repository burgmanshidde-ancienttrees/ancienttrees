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

SYMBOLS IN CI: the dSYMs live only in Hidde's Xcode archives, so the Mac
writes a compact map per store build (scripts/crash_symbols.py, into
data/crash-symbols/) and every machine reads the source line from that.

WHAT A SIGNATURE ASKS OF US (assess(), Hidde 2026-10-16: "check for crashes,
flag them and improve for the next build", and flag one that needs an
immediate update): URGENT when a store build is unusable for someone or the
crash spreads and no server-side fix stops it; act when it bursts with no fix
yet (fix it in the source, the next build carries it); reapply when a crash we
contained server-side fires again; waiting when the fix is in a build that is
not on sale. Fixes are recorded in data/crash-fixes.json.

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
import crash_symbols  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE_BUILDS = os.path.join(ROOT, "data", "store-builds.json")
APP_ID = "6806177833"
BINARY = "AncientTrees"
LOAD = 0x100000000
PAGE = 5  # the payload column is big; a larger select times out

# Signatures already dealt with: a code fix and the first build carrying it,
# and/or a server-side fix that stops it without a build (data/crash-fixes.json).
FIXES = os.path.join(ROOT, "data", "crash-fixes.json")

BURST = 3          # crashes of one signature on a store build ...
BURST_HOURS = 24   # ... inside this many hours is an act item

# URGENT (Hidde, 2026-10-16: flag "when a crash needs an immediate update"):
# the app is unusable for someone (one phone crashing URGENT_SAME_PHONE times
# inside URGENT_PHONE_HOURS, the crash-at-every-launch pattern: Peter's 1.0.2
# crashed 37 times from one phone), or the crash is spreading (URGENT_PHONES
# phones on one signature in 24h). Only when no server-side fix stops it.
URGENT_SAME_PHONE = 3
URGENT_PHONE_HOURS = 6
URGENT_PHONES = 2

FIX_IN_SOURCE = (
    "Fix it in the app source on main, in a .claude/worktrees/ worktree (the "
    "app rules), with a unit test that reproduces it where possible, and merge "
    "so the next archive carries it. Add it to data/crash-fixes.json "
    "(signature, build, fix_commit, first_fixed_build = the next build number) "
    "and log 'For Hidde: next build carries fix for <signature>' in LOG.md. "
    "The night run never archives, uploads or submits; Hidde does.")

CHECK_SERVER_FIRST = (
    "First check whether a server-side fix stops it (a data row the app trips "
    "on, like the empty-tree PATCH of 2026-10-16). If one does, apply it, add "
    "server_remedy and contained_at to its data/crash-fixes.json entry, and "
    "log 'contained, ships with next build': then it is not urgent.")

EXPEDITE = (
    "For Hidde: archive in Xcode (Product, Archive), upload to App Store "
    "Connect, and submit the version with 'Request expedited review' "
    "(developer.apple.com/contact/app-store/?topic=expedite).")


def load_fixes():
    try:
        with open(FIXES, encoding="utf-8") as f:
            return json.load(f).get("fixes") or []
    except (OSError, ValueError):
        return []


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


def _pick(lines):
    """Inlined frames come innermost first; the lines that name our own code
    are what a person needs, so runtime frames are folded away."""
    if not lines:
        return None
    ours = [ln for ln in lines if ".swift:" in ln]
    head = lines[0] if "Swift runtime failure" in lines[0] else None
    picked = ([head] if head else []) + ours[:2]
    return " < ".join(picked or lines[:2])


def symbol(binary, uuid, offset):
    """The source line for a frame: from the stored symbol map
    (data/crash-symbols/, readable in CI), else atos on this Mac's dSYM,
    else None."""
    if not uuid or offset is None:
        return None
    got = crash_symbols.lookup(uuid, offset)
    if got is None and crash_symbols.ensure(uuid):
        got = crash_symbols.lookup(uuid, offset)
    if got:
        return _pick(got.split(" < "))
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
    return _pick([_tidy(ln) for ln in r.stdout.splitlines() if ln.strip()])


def group(diags, symbolicate=True):
    """One row per signature: count, first and last seen, phones, builds."""
    sigs = {}
    for d in diags:
        k = (d["kind"], d["build"], d["exc"], d["uuid"], d["offset"])
        s = sigs.setdefault(k, {
            "kind": d["kind"], "build": d["build"], "version": d["version"],
            "exc": d["exc"], "binary": d["binary"], "uuid": d["uuid"],
            "offset": d["offset"],
            "count": 0, "first": d["at"], "last": d["at"],
            # phone fingerprint -> crash times, in memory only, never printed
            "_phone_times": {}, "times": [], "testflight": d["testflight"]})
        s["count"] += 1
        s["first"] = min(s["first"], d["at"])
        s["last"] = max(s["last"], d["at"])
        s["_phone_times"].setdefault(d["_phone"], []).append(d["at"])
        s["times"].append(d["at"])
    fixes = load_fixes()
    out = []
    for s in sigs.values():
        s["phones"] = len(s["_phone_times"])
        s["frame"] = ("%s+%s" % (s["binary"], hex(s["offset"]))
                      if s["offset"] is not None else "(no %s frame)" % BINARY)
        s["symbol"] = symbol(s["binary"], s["uuid"], s["offset"]) if symbolicate else None
        s["fix"] = next((f for f in fixes if f.get("signature") == s["frame"]
                         and str(f.get("build")) == s["build"]), None)
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


def released(fix, stores):
    """The store build that carries this fix and is on sale, or None."""
    try:
        first = int(fix.get("first_fixed_build"))
    except (TypeError, ValueError):
        return None
    for b, v in stores.items():
        if v.get("state") == "READY_FOR_SALE" and b.isdigit() and int(b) >= first:
            return b
    return None


def fix_label(s, stores):
    f = s.get("fix")
    if not f:
        return ""
    if f.get("first_fixed_build"):
        r = released(f, stores)
        label = ("fixed in build %s, released" % r if r else
                 "fixed in build %s, waiting for release" % f["first_fixed_build"])
    else:
        label = "no code fix yet"
    if f.get("server_remedy"):
        label += "; contained server-side"
    return label


def _max_in_window(times, hours):
    ts = sorted(_when(t) for t in times)
    best, j = 0, 0
    for i, t in enumerate(ts):
        while t - ts[j] > datetime.timedelta(hours=hours):
            j += 1
        best = max(best, i - j + 1)
    return best


def assess(sigs, stores, now=None):
    """What each store-build crash signature asks of us, newest window only.

    level: urgent  needs a new build now (no server-side fix stops it)
           reapply a contained crash fired again: re-apply its server fix
           act     a burst with no fix yet: fix it in the source tonight
           waiting fixed in a build that is not on sale yet, or on sale and
                   this phone is on an old build; nothing to do but wait
    Crashes before a fix's contained_at count as answered."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    out = []
    for s in sigs:
        if s["kind"] != "crash" or not is_store(s["build"], stores):
            continue
        f = s.get("fix") or {}
        cut = now - datetime.timedelta(hours=BURST_HOURS)
        if f.get("contained_at"):
            cut = max(cut, _when(f["contained_at"]))
        recent = {p: [t for t in ts if _when(t) >= cut]
                  for p, ts in s["_phone_times"].items()}
        recent = {p: ts for p, ts in recent.items() if ts}
        n = sum(len(ts) for ts in recent.values())
        phones = len(recent)
        same_phone = max((_max_in_window(ts, URGENT_PHONE_HOURS)
                          for ts in recent.values()), default=0)
        pattern = same_phone >= URGENT_SAME_PHONE or phones >= URGENT_PHONES
        if not (pattern or n >= BURST):
            continue
        if f.get("server_remedy"):
            level = "reapply"
        elif f.get("first_fixed_build"):
            level = "urgent" if pattern and not released(f, stores) else "waiting"
        else:
            level = "urgent" if pattern else "act"
        out.append({"s": s, "level": level, "n": n, "phones": phones,
                    "same_phone": same_phone, "label": fix_label(s, stores)})
    order = {"urgent": 0, "reapply": 1, "act": 2, "waiting": 3}
    out.sort(key=lambda a: (order[a["level"]], -a["n"]))
    return out


def message(a):
    """One sentence a run, or Hidde, can act on."""
    s, f = a["s"], a["s"].get("fix") or {}
    head = ("%s on store build %s (%s): %d crash(es) on %d phone(s) in %dh"
            % (where(s), s["version"], s["build"], a["n"], a["phones"], BURST_HOURS))
    if a["same_phone"] >= URGENT_SAME_PHONE:
        head += ", one phone %d times inside %dh (a crash at every launch)" % (
            a["same_phone"], URGENT_PHONE_HOURS)
    if a["level"] == "urgent":
        if f.get("first_fixed_build"):
            return ("URGENT, needs a new build now: %s. The fix is in build %s, "
                    "which is not on sale. %s" % (head, f["first_fixed_build"], EXPEDITE))
        return ("URGENT, needs a new build now: %s. %s Otherwise: %s Then: %s"
                % (head, CHECK_SERVER_FIRST, FIX_IN_SOURCE, EXPEDITE))
    if a["level"] == "reapply":
        return ("%s. Contained before, and it fired again: %s. Then log "
                "'contained, ships with next build'." % (head, f["server_remedy"]))
    if a["level"] == "act":
        return "%s. %s %s" % (head, CHECK_SERVER_FIRST, FIX_IN_SOURCE)
    return "%s. %s." % (head, a["label"] or "fixed")


_loaded = {}


def load(days=30, symbolicate=True):
    """(signatures, store builds), or (None, reason) when the key is absent."""
    if (days, symbolicate) in _loaded:
        return _loaded[(days, symbolicate)]
    key = load_key()
    if not key:
        return None, "SUPABASE_SERVICE_KEY not set"
    sigs = group(diagnostics(fetch_rows(key, days)), symbolicate)
    _loaded[(days, symbolicate)] = (sigs, store_builds())
    return _loaded[(days, symbolicate)]


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
        if s["fix"]:
            print("\n  %s on build %s: %s (%s)." % (
                s["frame"], s["build"], s["fix"].get("what", ""), fix_label(s, stores)))
    for a in assess(sigs, stores):
        print("\n  %s: %s" % (a["level"].upper(), message(a)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
