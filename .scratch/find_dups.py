import json
from collections import Counter

for f, label in [("data/leads/brussels.json", "brussels"), ("data/leads/genoa.json", "genoa")]:
    d = json.load(open(f))
    leads = d["leads"]
    names = [l.get("name") for l in leads]
    c = Counter(names)
    dups = [n for n, cnt in c.items() if cnt > 1]
    print(label, "dups:", dups)
    for n in dups:
        matching = [l for l in leads if l.get("name") == n]
        for m in matching:
            print("  ", json.dumps(m, ensure_ascii=False)[:250])
