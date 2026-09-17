#!/usr/bin/env python3
"""A sighting records where the PHONE stood, never where we think the tree is.

Written 2026-09-12, the day Hidde asked for it ("sla op waar mensen stonden")
after a photograph he sent from Kyoto could not be placed at all.

What had happened: `claim()` in CollectSheet recorded a sighting of one of our
trees with the TREE's coordinate (`lat: t.lat, lng: t.lng`). So every sighting
that carried a tree id came back reading zero metres from our own pin. That is
not a measurement, it is our own number handed back to us, and it cost two real
things on 2026-09-11. His photograph at the Omiya gate turned out to be a muku
standing beside the Sudajii we map, and nothing could say where it was taken.
And the Sudajii's pin is still `approximate`, while the phone in his hand knew
exactly where he was standing: a reader's GPS fix may correct a pin of ours
that admits it is approximate (CLAUDE.md, 2026-09-08), and that correction was
being thrown away at the moment it was made.

The fix is one argument, which is why it needs a check: it reads as a tidy line
of code either way, no test can see it (the call sits inside a private method
of a SwiftUI view), and the wrong version looks more "correct" to anybody
tidying up, because passing the tree's own coordinate for a tree looks right.

It cannot judge whether a coordinate is any good. It only refuses the one shape
that is always wrong: our own pin stored as if somebody had measured it.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 \
    else pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "ios" / "AncientTrees" / "AncientTrees"

# `record(treeId: ..., lat: t.lat` with anything in between, across lines.
CALL = re.compile(r"\.record\((?:[^()]|\([^()]*\))*?\)", re.S)
OUR_PIN = re.compile(r"\b(?:lat|lng):\s*(?:t|tree|spot|stop)\.(?:lat|lng)\b")


def offenders():
    out = []
    for path in sorted(APP.rglob("*.swift")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for m in CALL.finditer(text):
            call = m.group(0)
            if "treeId" not in call or not OUR_PIN.search(call):
                continue
            line = text[: m.start()].count("\n") + 1
            out.append("%s:%d: a sighting is being recorded at OUR pin "
                       "(%s). Pass the coordinate the phone or the photograph "
                       "gave you; treeId already carries the link to the tree. "
                       "See the comment at this call site."
                       % (path.relative_to(ROOT), line,
                          OUR_PIN.search(call).group(0)))
    return out


def main():
    bad = offenders()
    for line in bad:
        print("standingpoint: " + line)
    if not bad:
        print("standingpoint: sightings record where the phone stood")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
