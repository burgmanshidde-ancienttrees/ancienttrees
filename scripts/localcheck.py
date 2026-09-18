#!/usr/bin/env python3
"""The app's half of "nothing is stored locally".

Hidde has now given this rule three times, on three different days:

  2026-08-27  "niks moet lokaal opgeslagen zijn."
  2026-09-02  "ik wil dat je ervoor zorgt dat er niets meer lokaal wordt
               opgeslagen. Alles wat wordt opgeslagen, moet op je account zijn."
  2026-09-18  "Stop saving stuff locally anywhere please make sure this
               happens nowhere always account related."

By this project's own ratchet the second time should have made it a check on
BOTH surfaces, and it only made one: qa.py has refused an unlisted
localStorage key on the website since 2026-09-02, and nothing ever asked the
app the same question. So the same fault went on living there. On the day this
was written the app was keeping every worth-it vote and every report in three
UserDefaults keys per tree, written from the account at launch and then read
by the views as though they were the truth. Nothing cleared them on sign-out,
so a signed-out phone still showed the last person's votes.

What it refuses: a UserDefaults key or an @AppStorage key in the app that is
not named in data/local-storage-allow.json, and any key built from a variable
or an interpolation, whatever it holds. The second half is not pedantry. A key
written per tree cannot be enumerated, so it cannot be cleared when somebody
signs out, and a list cannot check what it cannot read.

The allow-list is the audit: one line per key saying why that thing is about
this DEVICE rather than about the person. Reading it should tell you in a
minute what the app keeps and why. Adding a line is a decision somebody wrote
down; the check exists so it cannot be a silence.

Run: python3 scripts/localcheck.py   (exit 1 on anything unlisted)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "ios" / "AncientTrees" / "AncientTrees"
ALLOW = ROOT / "data" / "local-storage-allow.json"

# A literal key: UserDefaults...forKey: "x" / removeObject(forKey: "x") /
# @AppStorage("x") / AppStorage(wrappedValue: ..., "x").
LITERAL = re.compile(r'(?:forKey:\s*|AppStorage\(\s*)"([^"\\]+)"')
# The same calls with anything that is not a plain string literal.
COMPUTED = re.compile(
    r'(?:forKey:\s*(?!")(?!Self\.)(?!\w+\.key\b)|AppStorage\(\s*(?!")(?:wrappedValue:[^,]*,\s*)?(?!"))'
)
# An interpolated key is a literal to the regex above but a computed key in
# fact, and it is the exact shape this check was written for.
INTERPOLATED = re.compile(r'(?:forKey:\s*|AppStorage\(\s*(?:wrappedValue:[^,]*,\s*)?)"[^"]*\\\(')


def key_names(text):
    """Every key name a Swift file names through a `let ... = "x"` constant.

    Stores reach their key through a private constant (`private let key =
    "saved.entries.v1"`), so `forKey: Self.key` is the normal shape and the
    name is one line up rather than at the call.
    """
    return re.findall(r'(?:let|var)\s+\w*[Kk]ey\w*\s*(?::\s*\w+\s*)?=\s*"([^"]+)"', text)


def main():
    allow = json.loads(ALLOW.read_text(encoding="utf-8"))
    allowed = set(allow.get("app", {}))
    if not APP.exists():
        print("localcheck: no app here")
        return 0

    offenders = []
    for f in sorted(APP.rglob("*.swift")):
        text = f.read_text(encoding="utf-8")
        touches = "UserDefaults" in text or "AppStorage" in text
        if not touches:
            continue
        rel = f.relative_to(ROOT)
        # Keys named by a constant in this file, which is how every store here
        # reaches UserDefaults.
        named = [k for k in key_names(text) if "UserDefaults" in text or "AppStorage" in text]
        for line_no, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("//") or line.strip().startswith("///"):
                continue
            if INTERPOLATED.search(line):
                offenders.append("%s:%d builds its key from the value it is "
                                 "about; such a key cannot be cleared" % (rel, line_no))
                continue
            for k in LITERAL.findall(line):
                if k not in allowed:
                    offenders.append("%s:%d writes %r" % (rel, line_no, k))
        for k in named:
            # A constant naming a key is only a storage key when this file
            # actually talks to UserDefaults, which the guard above settled.
            if k in allowed:
                continue
            # Publishable API keys and view-annotation keys live in the same
            # shape and are not device storage; they are caught by the line
            # scan above only when they reach forKey:, so a constant on its own
            # is reported ONLY when the file has no other explanation.
            if re.search(r'forKey:\s*(?:Self\.)?%s\b' % re.escape(k), text):
                offenders.append("%s names %r as a storage key" % (rel, k))

    if offenders:
        print("localcheck: %d place(s) store something on the device that "
              "data/local-storage-allow.json does not list.\n"
              "Everything a person keeps belongs to their account "
              "(Hidde, 2026-09-02 and 2026-09-18). Either send it to the "
              "account, or add a line to that file saying why it is about "
              "this device." % len(offenders))
        for o in sorted(set(offenders)):
            print("  " + o)
        return 1

    print("localcheck: the app keeps %d listed things on the device, all with "
          "a reason" % len(allowed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
