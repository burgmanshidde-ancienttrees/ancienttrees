#!/usr/bin/env python3
"""Temporary helper: merge a batch of German Munich tree entries into
data/i18n/de/munich.json. Reads a JSON batch file given as argv[1]."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "data", "i18n", "de", "munich.json")

with open(sys.argv[1], encoding="utf-8") as fh:
    batch = json.load(fh)

with open(TARGET, encoding="utf-8") as fh:
    d = json.load(fh)

d.setdefault("trees", {})
d["trees"].update(batch)

# keep tree order stable, matching the English city file
en = json.load(open(os.path.join(ROOT, "data", "cities", "munich.json"), encoding="utf-8"))
order = [t["id"] for t in en["trees"]]
d["trees"] = {i: d["trees"][i] for i in order if i in d["trees"]}

with open(TARGET, "w", encoding="utf-8") as fh:
    json.dump(d, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

print("merged %d, file now holds %d of %d trees" % (len(batch), len(d["trees"]), len(order)))
