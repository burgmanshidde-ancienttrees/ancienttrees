#!/bin/bash
# Refresh the catalogue that ships inside the app.
#
# The bundled copy is the floor, not a cache: a fresh install with no signal
# still has every tree. Run this before a release so the floor is current.
set -e
cd "$(dirname "$0")/AncientTrees/AncientTrees/Data"
for f in trees walks species; do
  curl -sf -m 60 "https://ancienttrees.app/api/$f.json" -o "$f.json"
  printf "%-8s %s\n" "$f" "$(du -h "$f.json" | cut -f1)"
done
python3 -c "import json;d=json.load(open('trees.json'));print('version',d['version'],'|',d['count'],'trees')"
