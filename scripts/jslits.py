#!/usr/bin/env python3
"""Refuse a stray backtick inside one of the JS-in-TS template literals.

Written 2026-09-23, after one backtick in a CODE COMMENT killed the deploy:

    // (CollectSheet.swift, `from: "app:collect"`), so counting it here

That comment sits inside `export const MY_TREES_JS = ` ... ` `, so the first
backtick ended the literal and everything after it was read as TypeScript. The
build said "Expected a semicolon" on a comment line, which is a confusing way
to be told you closed a string, and the whole site failed to deploy: not just
the feature, everything, including the night runs' work waiting behind it.

It is worth a check rather than care because the trap is invisible while you
write. Backticks are the natural way to quote an identifier in a comment, the
file is full of comments, and nothing on this machine can build the site to
find out. `${...}` is NOT flagged: interpolation is what these literals are
for, and SUPABASE_URL is substituted that way on purpose.

    python3 scripts/jslits.py            # every site/src/lib/*.ts
    python3 scripts/jslits.py <file>...

Exit 1 when it finds one. Runs in scripts/hooks/pre-push, where it costs
about nothing.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPEN = re.compile(r"^\s*export const \w+ = `", re.M)


def check(path):
    out = []
    text = path.read_text(encoding="utf-8")
    for m in OPEN.finditer(text):
        start = m.end()
        end = text.find("`", start)
        if end == -1:
            out.append("%s: `%s` is never closed" % (path, m.group().strip()))
            continue
        # Everything between the opener and the NEXT backtick is what the
        # compiler will treat as the literal. If the author meant more than
        # that, the next backtick is in the wrong place, and the line it sits
        # on is the one to name.
        line = text.count("\n", 0, end) + 1
        rest = text[end + 1:].lstrip()
        if not rest.startswith(";"):
            snippet = text[end - 60:end + 20].split("\n")[-1].strip()
            out.append("%s:%d: a backtick inside the template literal ends it "
                       "early, so everything after is parsed as TypeScript and "
                       "the whole site fails to build: %s" % (path, line, snippet))
            continue
        out += lone_backslashes(path, text[m.end():end],
                                text.count("\n", 0, m.end()) + 1)
    return out


def lone_backslashes(path, body, first_line):
    """A backslash that the template literal eats on its way out.

    The second half of the same trap, and a quieter one. These literals hold
    JavaScript, so `\\n` in the source is what puts `\n` in the emitted string.
    Write one backslash and the literal turns it into a real newline, in the
    middle of a string, and the browser refuses the whole script. Nothing goes
    red: the page builds, renders perfectly, and every function in that script
    is simply missing.

    That is how it happened on 2026-09-23: a patch script wrote `split('\n')`
    into my-trees-js.ts, the account page's whole script died, and the only
    thing that noticed was qa's own node-based parser, in CI, twenty-five
    minutes into a build.

    Measured over all 52 literals on the day it was written: not one lone
    backslash, so this is a rule the codebase already keeps and now cannot
    break by accident.
    """
    out = []
    for n, line in enumerate(body.split("\n"), first_line):
        for m in re.finditer(r"\\+", line):
            if len(m.group()) % 2 == 1:
                out.append("%s:%d: a lone backslash inside the template literal. "
                           "The literal eats it, so what reaches the browser is "
                           "not what is written here and the whole script may "
                           "stop parsing: %s" % (path, n, line.strip()[:70]))
    return out


def astro_literals(path):
    """The same trap, in a .astro page: set:html={`...`}.

    Added 2026-09-24, the day after this file was written, because it only ever
    read site/src/lib/*.ts and a page carries exactly the same construct. A
    backtick in a comment inside contribute.astro's script fragment ended the
    literal, Astro's compiler said "Expected } but found Identifier", and the
    whole site failed to build. The check written to stop that was blind to
    half the places it happens.
    """
    out = []
    text = path.read_text(encoding="utf-8")
    OPEN = "set:html={`"
    i = text.find(OPEN)
    while i >= 0:
        start = i + len(OPEN)
        end = text.find("`", start)
        if end < 0:
            out.append("%s: a set:html template literal is never closed" % path)
            break
        rest = text[end + 1:].lstrip()
        line = text.count("\n", 0, end) + 1
        if not rest.startswith("}"):
            snippet = text[max(0, end - 60):end + 20].split("\n")[-1].strip()
            out.append("%s:%d: a backtick inside a set:html template literal ends "
                       "it early, and Astro then fails to compile the page: %s"
                       % (path, line, snippet))
        else:
            out += lone_backslashes(path, text[start:end],
                                    text.count("\n", 0, start) + 1)
        i = text.find(OPEN, end + 1)
    return out


def main(argv):
    files = [Path(a) for a in argv]
    astro = []
    if not files:
        files = sorted((ROOT / "site" / "src" / "lib").glob("*.ts"))
        astro = sorted((ROOT / "site" / "src").rglob("*.astro"))
    else:
        astro = [f for f in files if f.suffix == ".astro"]
        files = [f for f in files if f.suffix != ".astro"]
    bad = []
    for f in astro:
        if f.exists():
            bad += astro_literals(f)
    for f in files:
        if f.exists():
            bad += check(f)
    for b in bad:
        print(b)
    if not bad:
        print("js literals: %d file(s), no backtick closes one early"
              % (len(files) + len(astro)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
