import json

verified = json.load(open('data/research/famous-slovakia-batch1-verified.json'))
by_id = {t['id']: t for t in verified}

targets = {
    'data/leads/kosice.json': 'kos_001',
    'data/leads/sala.json': 'sly_001',
    'data/leads/radava.json': 'rdv_001',
}

for path, tid in targets.items():
    t = by_id[tid]
    d = json.load(open(path))
    lead = d['leads'][0]
    lead['id'] = t['id']
    lead['age_estimate'] = t.get('age_estimate', '')
    lead['age_min'] = t.get('age_min')
    lead['age_max'] = t.get('age_max')
    lead['girth_cm'] = t.get('girth_cm')
    lead['location'] = t['location']
    lead['verified_sources'] = t['verified_sources']
    lead['access'] = t['access']
    lead['transport'] = t['transport']
    lead['location_precision'] = t['location_precision']
    lead['curation_status'] = t['curation_status']
    lead['story'] = t['story']
    lead['how_to_recognise'] = t['how_to_recognise']
    json.dump(d, open(path, 'w'), ensure_ascii=False, indent=2)
    open(path, 'a').write('\n')
    print('folded', tid, 'into', path)
