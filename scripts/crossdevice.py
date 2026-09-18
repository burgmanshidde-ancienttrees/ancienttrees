#!/usr/bin/env python3
"""Every place either surface keeps something, with a verdict on whether it travels.

Hidde, 2026-09-11, on finding a photograph he took in the app missing from his
own tree on the website: "alles moet cross device beschikbaar zijn wat onder je
account hangt. Check of dit voor alles geldt."

The check for it cannot be "does this sync", which no script can tell. What it
CAN do is refuse a new store that nobody has thought about, which is the same
move conventioncheck.py makes: it cannot judge the answer, only whether anybody
looked. So every key the app writes to UserDefaults and every key the website
writes to localStorage has to be named in data/cross-device.json with one of two
verdicts and a reason:

    account   it hangs under the account and MUST be on the server; the entry
              says which table carries it.
    device    it belongs to this device and staying here is correct (a
              remembered map style, a queue waiting to be sent, a cache).

Adding a store means adding a line. Getting the verdict wrong is still possible;
forgetting the question is not.

AND, since 2026-09-18, an `account` store that is also written to the device
has to answer a second question in `off`: what takes it off a phone nobody is
signed in to. That is the hole this register had, and it was not hypothetical.
`at_worthit_`, `at_wrong_` and `at_wrong_detail_` were all correctly ruled
`account` here, and all three were written to UserDefaults anyway, read by the
views as the truth, and cleared by nothing at all. A signed-out phone went on
showing the last person's votes for weeks with this check green, because the
register asked whether anybody had ruled and never whether the code obeyed.

`off` is prose, not a symbol, and "nothing, because ..." is a legitimate answer
(a display preference is not somebody's data). The point is the same one
conventioncheck.py makes: a script cannot judge the answer, only whether
anybody was made to write one down. Hidde, 2026-09-18: "stop saving stuff
locally anywhere please make sure this happens nowhere always account related."

    python3 scripts/crossdevice.py          # check
    python3 scripts/crossdevice.py --list   # what is registered, by verdict
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(ROOT, "data", "cross-device.json")
SWIFT = os.path.join(ROOT, "ios", "AncientTrees", "AncientTrees")
WEB = os.path.join(ROOT, "site", "src")

# A key written with an id in it ("at_worthit_\(tree.id)") is one store, not one
# per tree, so it registers under its prefix.
INTERP = re.compile(r'\\\(.*')

SWIFT_PATTERNS = [
    re.compile(r'forKey:\s*"([^"]+)"'),
    re.compile(r'AppStorage\((?:wrappedValue:[^,]+,\s*)?"([^"]+)"'),
    re.compile(r'(?:let|var)\s+\w*[Kk]ey\w*\s*(?::\s*String\s*)?=\s*"([^"]+)"'),
]
WEB_PATTERN = re.compile(r'(?:localStorage|sessionStorage)\.\w+Item\(\s*[\'"]([^\'"]+)[\'"]')


def walk(root, suffixes):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "dist")]
        for f in files:
            if f.endswith(suffixes):
                yield os.path.join(base, f)


def found():
    """key -> the files that write it."""
    out = {}
    for path in walk(SWIFT, (".swift",)):
        if "Tests" in path:
            continue
        text = open(path, encoding="utf-8", errors="ignore").read()
        for pattern in SWIFT_PATTERNS:
            for key in pattern.findall(text):
                key = INTERP.sub("", key)
                if not key:
                    continue
                out.setdefault(key, set()).add(os.path.relpath(path, ROOT))
    for path in walk(WEB, (".ts", ".astro", ".js")):
        text = open(path, encoding="utf-8", errors="ignore").read()
        for key in WEB_PATTERN.findall(text):
            out.setdefault(key, set()).add(os.path.relpath(path, ROOT))
    return out


def main():
    register = json.load(open(REGISTER, encoding="utf-8"))
    known = register["stores"]
    stores = found()

    if "--list" in sys.argv:
        for verdict in ("account", "device", "not a store"):
            names = sorted(k for k, v in known.items() if v["verdict"] == verdict)
            print(f"\n{verdict} ({len(names)})")
            for n in names:
                print(f"  {n}: {known[n]['why']}")
        return 0

    missing = sorted(k for k in stores if k not in known)
    stale = sorted(k for k in known if k not in stores and not known[k].get("keep"))
    # An account store the code writes to the device, with nobody named to take
    # it off again when the account goes.
    unswept = sorted(k for k in stores
                     if k in known
                     and known[k]["verdict"] == "account"
                     and not known[k].get("off"))

    for key in missing:
        where = ", ".join(sorted(stores[key]))
        print(f"FAIL  {key}  (written in {where})")
        print("      Not in data/cross-device.json. Say whether it hangs under "
              "the account (and which table carries it) or belongs to the device.")
    for key in stale:
        print(f"NOTE  {key} is registered and nothing writes it any more.")
    for key in unswept:
        where = ", ".join(sorted(stores[key]))
        print(f"FAIL  {key}  (written in {where})")
        print("      Ruled 'account' and written to the device with no \"off\". "
              "Say what takes it off a phone nobody is signed in to, or say "
              "\"nothing, because ...\".")

    if missing or unswept:
        print(f"\n{len(missing)} unregistered store(s), {len(unswept)} "
              "account store(s) nothing is named to clear. A store nobody has "
              "ruled on is a store that does not travel; an account store "
              "nobody clears is the last person's data on this phone.")
        return 1
    print(f"cross-device: {len(stores)} stores, all ruled on "
          f"({sum(1 for k in stores if known[k]['verdict'] == 'account')} account, "
          f"{sum(1 for k in stores if known[k]['verdict'] == 'device')} device).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
