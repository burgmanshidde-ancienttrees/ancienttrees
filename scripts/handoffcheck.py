#!/usr/bin/env python3
"""Refuse a LOG.md entry that hands Hidde a merge, a push or a deploy.

Hidde, 2026-09-17, after a session finished a verified Contract B change,
pushed it to a claude/ branch and wrote "FOR HIDDE: ... Merge it when you want
it live": **"Merge maar ik wil niet mergen doe dit zelf vraag nooit meer aan
mij."**

It is the ratchet, and the ratchet's own order says a check before a sentence:
CLAUDE.md already says he is not the quality gate, that a run decides for
itself, and that waiting for permission is the failure mode this project is
built to avoid. None of that stopped the handoff, because none of it can refuse
a push. This can.

WHAT IT REFUSES: a line addressed to him that asks for git plumbing. Merging a
branch, pushing it, landing it on main, deploying it, or the softer form of the
same thing, telling him work is finished but sitting somewhere it is not live.
All of that is a session's own work: verify it, merge it, push it to main.

WHAT IT DOES NOT TOUCH, and the distinction is the whole point: FOR HIDDE is a
good mechanism and most of what it carries is real. Things only he can do stay
welcome and are deliberately not matched here, among them approving a spend
(hard rule 5), approving a blueprint or tone edit (hard rule 7), pasting SQL
into his own Supabase, anything needing his account or his name, and any
judgement call this corpus records as his. The test is not "does this mention
Hidde", it is "is this a git operation a session could have done itself".

Usage:  python3 scripts/handoffcheck.py [file ...]      (default: LOG.md)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The ask: a git operation. Kept literal rather than clever, in both languages,
# because a regex that tries to parse intent will fire on an entry that merely
# DESCRIBES a merge ("merged main into the branch"), which is ordinary reporting
# and not a handoff.
ASK = re.compile(
    r"\b("
    r"merge (?:it|this|that|these|them|when|wanneer)"
    r"|merge(?:n)? (?:maar|het|hem|deze|wanneer|als)"
    r"|mergen"
    r"|kun(?:t)? je (?:het |dit )?mergen"
    r"|pull request .{0,20}(?:merge|land)"
    r"|(?:push|land|deploy) (?:it|this|these|them) (?:to|op|naar) main"
    r"|when you want it live"
    r"|wanneer je (?:het |hem )?live wil"
    r"|zet(?:ten)? je het live"
    r"|not (?:yet )?on main"
    r"|staat (?:nog )?niet op main"
    r"|(?:has|have) not deployed"
    r"|is nog niet live"
    r")\b",
    re.I,
)

# Addressed to him, in the SECOND person. A line has to be both an ask and
# addressed, which is what separates a handoff ("merge it when you want it
# live") from reporting one ("a FOR HIDDE line asking him to merge it"). His
# name alone is not enough and was tried first: every entry here mentions him.
ADDRESSED = re.compile(r"\b(you|your|jij|jou|jouw|je)\b", re.I)

# The canonical handoff is a block opening with the marker, which is how this
# corpus has always written one. Line-initial on purpose, allowing markdown
# emphasis and bullets: a mention inside a sentence is prose about the mechanism
# rather than a use of it, and matching those made this check fire on the very
# entry recording the rule.
MARKER = re.compile(r"^[\s>*_\-]*\*{0,2}FOR HIDDE\b", re.I | re.M)


# A SECTION that names this check is documenting the rule rather than handing
# anything over, so it is skipped. Section rather than paragraph, and that is
# not a detail: an entry recording the rule has to be able to quote the shape it
# forbids, and the quotation and the check's name will not sit in the same
# paragraph. Both files that record this one proved it, LOG.md and CLAUDE.md.
#
# The same exemption pitchcheck gives drafts/PITCH_VOICE.md, and for the same
# reason. Deliberately keyed to the check's own name and nothing looser, so it
# cannot be used to wave a real handoff through: a session would have to write
# the word "handoffcheck" into the section to silence it, which is not something
# anybody does by accident.
SELF = re.compile(r"handoffcheck", re.I)
HEADING = re.compile(r"^#{1,6}\s")


def _sections(lines):
    """Index per line of the markdown section it sits in, and each section's
    full text. A run of lines before the first heading is section 0."""
    idx, of, cur, texts = 0, [], [], []
    for line in lines:
        if HEADING.match(line):
            texts.append("\n".join(cur))
            cur = []
            idx += 1
        cur.append(line)
        of.append(idx)
    texts.append("\n".join(cur))
    return of, texts


def offending_lines(text):
    out = []
    lines = text.split("\n")
    of, texts = _sections(lines)
    for i, line in enumerate(lines):
        if not ASK.search(line):
            continue
        if SELF.search(texts[of[i]]):
            continue
        near = "\n".join(lines[max(0, i - 2): i + 1])
        if ADDRESSED.search(line) or MARKER.search(near):
            out.append((i + 1, line.strip()))
    return out


def main(argv):
    targets = [Path(a) for a in argv[1:]] or [ROOT / "LOG.md"]
    bad = []
    for path in targets:
        if not path.exists():
            continue
        for lineno, line in offending_lines(path.read_text(encoding="utf-8")):
            bad.append("%s:%d  %s" % (path.name, lineno, line[:160]))
    if not bad:
        print("handoffcheck: nothing hands Hidde a merge")
        return 0
    print("handoffcheck: an entry asks Hidde to do git work a session does itself")
    for b in bad:
        print("  " + b)
    print("")
    print("Hidde, 2026-09-17: \"Merge maar ik wil niet mergen doe dit zelf vraag")
    print("nooit meer aan mij.\" Verify it, merge it into main, push it, and say")
    print("in LOG.md that it is live. FOR HIDDE stays for what only he can do:")
    print("a spend, a blueprint edit, his own accounts, a judgement this corpus")
    print("records as his.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
