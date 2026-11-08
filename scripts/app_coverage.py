"""Which named app controls does any UI test touch, and signed in or out?

Reads every accessibilityIdentifier("...") in the app source (by file), and
every quoted identifier in the UI tests, and prints per screen file which
identifiers no test names at all. Rough on purpose: an identifier built at run
time ("tile-\\(id)") cannot be matched and is listed as dynamic.

    python3 scripts/app_coverage.py
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "ios/AncientTrees/AncientTrees")
TESTS = os.path.join(ROOT, "ios/AncientTrees/AncientTreesUITests")
IDENT = re.compile(r'accessibilityIdentifier\(\s*"([^"]+)"')
ID_ARG = re.compile(r'\bid:\s*"([^"]+)"')

tests_text = {}
for f in glob.glob(os.path.join(TESTS, "*.swift")):
    tests_text[os.path.basename(f)] = open(f, encoding="utf-8").read()

def touched(ident):
    hits = []
    for name, text in tests_text.items():
        if '"%s"' % ident in text:
            hits.append(name.replace(".swift", ""))
    return hits

signed_in_files = {n for n, t in tests_text.items() if "-signed-in" in t}

rows = []
for f in sorted(glob.glob(os.path.join(APP, "**/*.swift"), recursive=True)):
    text = open(f, encoding="utf-8").read()
    ids = sorted(set(IDENT.findall(text)) | set(ID_ARG.findall(text)))
    if not ids:
        continue
    rel = os.path.relpath(f, APP)
    static = [i for i in ids if "\\(" not in i]
    dynamic = [i for i in ids if "\\(" in i]
    covered, bare, signed_in = [], [], []
    for i in static:
        h = touched(i)
        if h:
            covered.append(i)
            if any(x + ".swift" in signed_in_files for x in h):
                signed_in.append(i)
        else:
            bare.append(i)
    rows.append((rel, len(static), len(covered), len(signed_in), bare, dynamic))

tot = sum(r[1] for r in rows)
cov = sum(r[2] for r in rows)
sin = sum(r[3] for r in rows)
print("named controls: %d; named by some UI test: %d; in a test file that signs in: %d" % (tot, cov, sin))
print()
print("| File | Named | In a test | In a signed-in test | Never named by a test |")
print("|---|---:|---:|---:|---|")
for rel, n, c, s, bare, dyn in sorted(rows, key=lambda r: -(r[1] - r[2])):
    extra = (" (+%d built at run time)" % len(dyn)) if dyn else ""
    print("| %s | %d | %d | %d | %s%s |" % (rel, n, c, s, ", ".join(bare[:12]) + (" ..." if len(bare) > 12 else ""), extra))
