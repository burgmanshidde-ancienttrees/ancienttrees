#!/usr/bin/env python3
"""Which of the app's screenshots the night's reviewer looks at.

The website's fresh-eyes reviewer reads HTML, which is cheap. The app's screens
are PNGs, and reading nineteen of them twice over (two phones) every night is
the most expensive thing this project could ask a nightly job to do, on a
subscription that is already the binding constraint.

So it ROTATES, deterministically, by the day of the year: six screens a night,
every screen seen inside four nights, no state kept anywhere and the same answer
whoever asks. The alternative was a table mapping each screen to the source file
that draws it, so the reviewer could look at what changed; that table would be
wrong within a fortnight and nobody would notice.

The smallest phone only. It is the honest one, it is the width the website's own
fit check uses, and the large phone is measured mechanically by appfit anyway.

    python3 scripts/pick_app_screens.py --dir /tmp/appshots
    python3 scripts/pick_app_screens.py --dir /tmp/appshots --count 6 --day 240
"""
import argparse
import datetime
import pathlib
import sys


def pick(root, count, day):
    """Return the chosen PNG paths, in the order they should be looked at."""
    # The artifact keeps appsweep's own folder names, one per phone.
    shots = sorted(p for p in root.rglob("*.png") if "SE" in p.parent.name)
    if not shots:
        # No SE folder: take whatever single phone the artifact does carry
        # rather than reporting nothing, because a reviewer with no pictures
        # writes "nothing found" and that reads like a clean night.
        shots = sorted(root.rglob("*.png"))
    if not shots:
        return []
    start = (day * count) % len(shots)
    return [shots[(start + i) % len(shots)] for i in range(min(count, len(shots)))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="where the artifact was unpacked")
    ap.add_argument("--count", type=int, default=6)
    ap.add_argument("--day", type=int, default=None,
                    help="day of the year; today by default")
    args = ap.parse_args()

    root = pathlib.Path(args.dir)
    if not root.exists():
        print("no screenshots: %s does not exist" % root, file=sys.stderr)
        return 1
    day = args.day if args.day is not None else datetime.date.today().timetuple().tm_yday
    chosen = pick(root, args.count, day)
    if not chosen:
        print("no screenshots under %s" % root, file=sys.stderr)
        return 1
    for p in chosen:
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
