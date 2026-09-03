import os, json, urllib.request

url = "https://caimvxiyrtifilimlkqw.supabase.co/rest/v1/submissions?select=*&order=created_at.asc"
key = os.environ.get("SUPABASE_SERVICE_KEY")
req = urllib.request.Request(url, headers={
    "apikey": key,
    "Authorization": "Bearer " + key,
})
with urllib.request.urlopen(req, timeout=20) as r:
    rows = json.load(r)

processed = set()
try:
    processed = set(json.load(open("data/submissions-processed.json")))
except Exception as e:
    print("no processed file or error:", e)

new = [row for row in rows if row["id"] not in processed]
print("total rows:", len(rows), "processed:", len(processed), "new:", len(new))
for row in new[:20]:
    print(row.get("id"), row.get("kind"), row.get("city"), (row.get("why") or "")[:100])
