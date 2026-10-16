#!/usr/bin/env python3
"""Symbol maps for the app's store builds, so a night run can name the line.

    python3 scripts/crash_symbols.py            map every store build missing one
    python3 scripts/crash_symbols.py --status   which store builds have a map
    python3 scripts/crash_symbols.py --uuid U   map one binary uuid

THE CATCH this exists for (Hidde, 2026-10-16: "check for crashes, flag them
and improve for the next build"): the night run is on GitHub and the dSYMs live
only in Hidde's Xcode archives (~/Library/Developer/Xcode/Archives, about 24 MB
each), so CI can see that a crash is at AncientTrees+0xb8180 and nothing more.

THE BORING WAY ROUND: on the Mac, take every row start of the dSYM's line table
(dwarfdump --debug-line), ask atos for all of them in one call, and keep only
the rows where atos's answer changes. A crash offset then looks up the nearest
row at or below it and gets exactly what atos would have said, inlined frames
included, with no dSYM in sight. About 0.2 MB gzipped per build, kept in the
repository under data/crash-symbols/<uuid>.json.gz: the map holds function
names and Swift file:line of code that is already public in ios/, and no
person's data, so private_files (for addresses) would add a pull step for no
gain. Only store builds are mapped (data/store-builds.json), not every archive.

crashes.py calls ensure() for each uuid it meets on the Mac, and brief.py names
a store build that still has no map, so a map appears without anyone
remembering to make one. Reading is lookup() and needs nothing but Python.
"""
import argparse
import bisect
import glob
import gzip
import json
import os
import plistlib
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = os.path.join(ROOT, "data", "crash-symbols")
STORE_BUILDS = os.path.join(ROOT, "data", "store-builds.json")
ARCHIVES = os.path.expanduser("~/Library/Developer/Xcode/Archives")
LOAD = 0x100000000


def _tidy(line):
    line = re.sub(r" \(in [^)]+\)", "", line)
    line = line.replace(" (/<compiler-generated>:0)", "")
    return line.replace("|", "/").strip()


_archives = None


def archives():
    """[(build, uuid, dwarf path)] for every archive on this Mac."""
    global _archives
    if _archives is None:
        _archives = _scan()
    return _archives


def _scan():
    out = []
    for arc in glob.glob(os.path.join(ARCHIVES, "*", "*.xcarchive")):
        try:
            with open(os.path.join(arc, "Info.plist"), "rb") as f:
                info = plistlib.load(f)
        except (OSError, ValueError):
            continue
        build = str((info.get("ApplicationProperties") or {}).get("CFBundleVersion") or "")
        dwarf = os.path.join(arc, "dSYMs", "AncientTrees.app.dSYM", "Contents",
                             "Resources", "DWARF", "AncientTrees")
        if not build or not os.path.exists(dwarf):
            continue
        try:
            r = subprocess.run(["dwarfdump", "--uuid", dwarf], capture_output=True,
                               text=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            continue
        for m in re.finditer(r"UUID: ([0-9A-F-]+) \(arm64\)", r.stdout):
            out.append((build, m.group(1), dwarf))
    return out


def _path(uuid):
    return os.path.join(MAPS, "%s.json.gz" % uuid.upper())


def build_map(uuid, dwarf, build):
    """Write data/crash-symbols/<uuid>.json.gz from one dSYM."""
    r = subprocess.run(["dwarfdump", "--debug-line", dwarf], capture_output=True,
                       text=True, timeout=600)
    addrs = set()
    for ln in r.stdout.splitlines():
        if ln.startswith("0x") and "end_sequence" not in ln:
            a = int(ln.split()[0], 16)
            if a >= LOAD:
                addrs.add(a)
    addrs = sorted(addrs)
    r = subprocess.run(["atos", "-arch", "arm64", "-o", dwarf, "-l", hex(LOAD), "-i"],
                       input="\n".join(hex(a) for a in addrs), capture_output=True,
                       text=True, timeout=1800)
    # atos -i prints one or more lines per address (inlined frames) and a
    # blank line between addresses.
    answers = [blk for blk in r.stdout.split("\n\n")]
    if len(answers) < len(addrs):
        # Older atos: one line per address, no blank separators.
        answers = r.stdout.splitlines()
    strings, index, rows, last = [], {}, [], None
    for a, ans in zip(addrs, answers):
        s = " < ".join(_tidy(x) for x in ans.strip().splitlines() if x.strip())
        if s == last:
            continue
        last = s
        if s not in index:
            index[s] = len(strings)
            strings.append(s)
        rows.append([a - LOAD, index[s]])
    os.makedirs(MAPS, exist_ok=True)
    with gzip.open(_path(uuid), "wt", encoding="utf-8") as f:
        json.dump({"uuid": uuid.upper(), "build": build, "strings": strings,
                   "rows": rows}, f, separators=(",", ":"))
    return len(rows)


_cache = {}


def lookup(uuid, offset):
    """What atos would say for this offset, from the stored map, or None."""
    if not uuid or offset is None:
        return None
    uuid = uuid.upper()
    if uuid not in _cache:
        try:
            with gzip.open(_path(uuid), "rt", encoding="utf-8") as f:
                m = json.load(f)
            _cache[uuid] = ([r[0] for r in m["rows"]], [r[1] for r in m["rows"]],
                            m["strings"])
        except (OSError, ValueError, KeyError):
            _cache[uuid] = None
    m = _cache[uuid]
    if not m:
        return None
    i = bisect.bisect_right(m[0], offset) - 1
    return m[2][m[1][i]] if i >= 0 else None


def store_build_numbers():
    try:
        with open(STORE_BUILDS, encoding="utf-8") as f:
            return set(json.load(f))
    except (OSError, ValueError):
        return set()


def missing():
    """[(build, uuid, dwarf)] for store-build archives with no map yet."""
    want, seen, out = store_build_numbers(), set(), []
    for a in archives():
        if a[0] in want and a[1] not in seen and not os.path.exists(_path(a[1])):
            seen.add(a[1])
            out.append(a)
    return out


def ensure(uuid):
    """Map one uuid if this Mac holds its archive; True when a map exists."""
    if not uuid or os.path.exists(_path(uuid)):
        return bool(uuid)
    if not os.path.isdir(ARCHIVES):
        return False
    for build, u, dwarf in archives():
        if u.upper() == uuid.upper():
            build_map(u, dwarf, build)
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--uuid")
    a = ap.parse_args()
    if not os.path.isdir(ARCHIVES):
        print("crash_symbols: no Xcode archives on this machine; nothing to map.")
        return 0
    if a.uuid:
        print("mapped" if ensure(a.uuid) else "no archive holds %s" % a.uuid)
        return 0
    todo = missing()
    if a.status:
        print("%d store-build archive(s) without a symbol map" % len(todo))
        for build, uuid, _ in todo:
            print("  build %s %s" % (build, uuid))
        return 0
    for build, uuid, dwarf in todo:
        n = build_map(uuid, dwarf, build)
        size = os.path.getsize(_path(uuid))
        print("build %s %s: %d rows, %d KB" % (build, uuid, n, size // 1024))
    if not todo:
        print("every store-build archive has a symbol map")
    return 0


if __name__ == "__main__":
    sys.exit(main())
