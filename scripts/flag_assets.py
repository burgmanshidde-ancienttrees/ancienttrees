#!/usr/bin/env python3
"""Copy the website's flat square flags (flag-icons 7.2.3, MIT) into the app's
asset catalog as vector imagesets, Flags/<cc>. Re-runnable."""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "site", "public", "flags")
dst = os.path.join(ROOT, "ios", "AncientTrees", "AncientTrees", "Assets.xcassets", "Flags")
os.makedirs(dst, exist_ok=True)
json.dump({"info": {"author": "xcode", "version": 1}, "properties": {"provides-namespace": True}},
          open(os.path.join(dst, "Contents.json"), "w"), indent=2)
n = 0
for f in sorted(os.listdir(src)):
    if not f.endswith(".svg"):
        continue
    cc = f[:-4]
    d = os.path.join(dst, cc + ".imageset")
    os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(src, f), os.path.join(d, f))
    json.dump({"images": [{"filename": f, "idiom": "universal"}],
               "info": {"author": "xcode", "version": 1},
               "properties": {"preserves-vector-representation": True}},
              open(os.path.join(d, "Contents.json"), "w"), indent=2)
    n += 1
shutil.copy(os.path.join(src, "LICENSE.txt"), os.path.join(ROOT, "ios", "AncientTrees", "FLAGS-LICENSE.txt"))
print(n, "flags")
