#!/usr/bin/env python3
"""Spell-check the English a reader actually sees.

Hidde, 2026-09-24: "hoe zorgen we dat je nooit meer spelfouten maakt als je
copy live zet - dat is toch niet zo veel gevraagd van een llm - hoe verbeteren
we dit proces het gaat non stop fout."

WHAT THIS CAN AND CANNOT DO, said plainly because the answer to his question is
two things and only one of them is a script. This catches a MISSPELLED WORD:
neglish, wil lbe, recieve. It cannot catch "ask a question if we need one",
which is five correctly spelled words in the wrong idiom and is the mistake
that prompted him. That half is a reading pass, and it runs weekly from
review.yml.

WHERE IT LOOKS: the string tables a reader meets, and the app's own literals.
Not the tree stories, which are prose written against TONE_OF_VOICE.md and
full of proper nouns; not the corpus, which is notes to ourselves.

IT NEVER RUNS IN CI, deliberately. The dictionary is /usr/share/dict/words,
which is on this Mac and would be an apt-get on a runner, and a check that
adds a minute to every build is a check that gets removed. It is in the
pre-push hook, where it costs under a second, and it prints one line and exits
0 when there is no dictionary, so nothing is ever blocked by its absence.

    python3 scripts/spellcheck.py           # the tables and the app
    python3 scripts/spellcheck.py --list    # every unknown word, to seed the allow file

Words that are not misspellings (place names, species, our own nouns) live in
data/spelling-allow.txt, one per line.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICTS = ["/usr/share/dict/words", "/usr/share/dict/american-english",
         "/usr/share/dict/british-english"]
ALLOW = ROOT / "data" / "spelling-allow.txt"

# (path, the declaration whose block holds the ENGLISH strings). The other
# seven languages in these files are not misspelt English; reading them was the
# first version's whole 779-word noise problem.
SOURCES = [
    ("site/src/lib/signin-strings.ts", "  en: {"),
    ("site/src/lib/i18n.ts", "const EN: UIStrings = {"),
]
SWIFT_DIRS = ["ios/AncientTrees/AncientTrees/Screens", "ios/AncientTrees/AncientTrees/Kit"]

# A string literal in a TS table, and the English ones only: the other seven
# languages are not misspelt English, they are other languages.
# Both quotes, because a TS table uses single ones for any string that holds
# markup. Reading only double-quoted ones made the check report `href` and
# `const`, which is a check reporting our own code back at us.
TABLE_STR = re.compile(r'"((?:[^"\\\n]|\\.){4,})"' + r"|'((?:[^'\\\n]|\\.){4,})'")
SWIFT_STR = re.compile(r'(?:Text|Label|Button|navigationTitle|confirmationDialog)\(\s*"((?:[^"\\]|\\.){4,})"')


def dictionary():
    for d in DICTS:
        if os.path.exists(d):
            with open(d, encoding="utf-8", errors="ignore") as fh:
                return {w.strip().lower() for w in fh if w.strip()}
    return None


def allowed():
    if not ALLOW.exists():
        return set()
    out = set()
    for line in ALLOW.read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip().lower()
        if line:
            out.add(line)
    return out


def english_block(text, opener):
    """The one declaration that holds the English, by its own first line.

    Named per file rather than guessed, because the two files are shaped
    differently: one is a Record keyed by language, the other a single const
    that ui() falls back to.
    """
    i = text.find(opener)
    if i < 0:
        return ""
    depth, j = 0, text.index("{", i)
    for k in range(j, len(text)):
        if text[k] == "{":
            depth += 1
        elif text[k] == "}":
            depth -= 1
            if depth == 0:
                return text[j:k]
    return text[j:]


def strings_from(path, opener):
    block = english_block((ROOT / path).read_text(encoding="utf-8"), opener)
    return [m.group(1) or m.group(2) for m in TABLE_STR.finditer(block)]


def forms(w):
    """The plain forms of a word, because the system list has no inflections.

    /usr/share/dict/words holds "answer" and not "answered", "city" and not
    "cities". Without this every ordinary sentence is a page of false alarms,
    and a check that cries wolf is a check somebody bypasses in a week.
    """
    w = w.lower().replace("\u2019", "'")
    out = {w, w.replace("'s", ""), w.replace("'", "")}
    for suf, adds in (("s", [""]), ("es", [""]), ("ies", ["y"]),
                      ("ed", ["", "e"]), ("d", [""]),
                      ("ing", ["", "e"]), ("er", ["", "e"]), ("est", ["", "e"]),
                      ("ly", [""]), ("'s", [""])):
        if w.endswith(suf) and len(w) > len(suf) + 1:
            stem = w[:-len(suf)]
            for a in adds:
                out.add(stem + a)
            # dropped, running: the doubled consonant goes back to one.
            if len(stem) > 2 and stem[-1] == stem[-2]:
                out.add(stem[:-1])
    return out


def words(s):
    # Strip html, entities, urls, placeholders and code-ish tokens before
    # looking at anything: a check that flags `href` teaches nobody anything.
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&[a-z]+;", " ", s)
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"\$\{[^}]*\}|%s|%\d+\$?@|\\[nut]", " ", s)
    s = s.replace("\\u2019", "'").replace("’", "'")
    out = []
    for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", s):
        w = w.strip("'-")
        # camelCase and ALLCAPS are identifiers, not prose.
        if not w or w.isupper() or re.search(r"[a-z][A-Z]", w):
            continue
        out.append(w)
    return out


def main(argv):
    d = dictionary()
    if d is None:
        print("spellcheck: no system dictionary here, nothing checked")
        return 0
    ok = d | allowed()
    found = {}
    for rel, opener in SOURCES:
        if not (ROOT / rel).exists():
            continue
        for s in strings_from(rel, opener):
            for w in words(s):
                if w.lower() in ok:
                    continue
                # "trees" for "tree" and "walked" for "walk": the dictionary is
                # a word list rather than a stemmer, so try the obvious forms
                # before calling anything a mistake.
                if forms(w) & ok:
                    continue
                found.setdefault(w, []).append(rel)
    for rel in SWIFT_DIRS:
        for f in sorted((ROOT / rel).rglob("*.swift")):
            for m in SWIFT_STR.finditer(f.read_text(encoding="utf-8")):
                for w in words(m.group(1)):
                    if w.lower() in ok or forms(w) & ok:
                        continue
                    found.setdefault(w, []).append(str(f.relative_to(ROOT)))

    if "--list" in argv:
        for w in sorted(found, key=str.lower):
            print(w)
        return 0
    if not found:
        print("spellcheck: every word a reader sees is a word")
        return 0
    print("spellcheck: %d word(s) not in the dictionary or the allow file:" % len(found))
    for w in sorted(found, key=str.lower):
        where = sorted(set(found[w]))[0]
        print("  %-24s %s" % (w, where))
    print("A real name or a species belongs in data/spelling-allow.txt.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
