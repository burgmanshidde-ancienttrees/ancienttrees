import re, sys
for n in sys.argv[1:]:
    t = open(f"/tmp/stg{n}.html", errors="ignore").read()
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("&nbsp;", " ").replace("&#39;", "'")
    t = re.sub(r"\s+", " ", t)
    i = t.find("Présentation")
    j = t.find("Territoire Mon quartier")
    print("###", n, len(t))
    print(t[i:j][:2200])
