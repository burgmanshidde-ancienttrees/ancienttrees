import json, re, urllib.request, time, subprocess, os

out = subprocess.run(['python3', 'scripts/enrich.py', '--brief', 'caserta'], capture_output=True, text=True).stdout
trees = json.loads(out[out.index('TREES:') + 6:])
ans = []
for t in trees:
    url = [s for s in t['sources'] if 'scheda_' in s][0]
    try:
        h = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=20).read().decode('utf8', 'ignore')
    except Exception as e:
        print(t['id'], 'ERR', e)
        continue
    x = re.sub(r'<[^>]*>', ' ', h)
    g = re.search(r'Circ\. fusto\s*:\s*([\d.,]+)\s*cm', x)
    hh = re.search(r'Altezza\s*:\s*([\d.,]+)', x)
    gps = re.search(r'Coord GPS\s*:\s*([\d.]+),\s*([\d.]+)', x)
    e = {'id': t['id'], 'register_url': url, 'register_name': 'Alberi monumentali della Campania (Regione Campania)'}
    if g:
        e['girth_cm'] = float(g.group(1).replace(',', '.'))
    if hh:
        e['height_m'] = float(hh.group(1).replace(',', '.'))
    if g or hh:
        e['measure_source'] = url
    print(t['id'], e.get('girth_cm'), e.get('height_m'), gps.groups() if gps else None, t['lat'], t['lng'], t['location_precision'])
    ans.append(e)
    time.sleep(1)
os.makedirs('out/enrich', exist_ok=True)
json.dump(ans, open('out/enrich/caserta.answer.json', 'w'), indent=1)
