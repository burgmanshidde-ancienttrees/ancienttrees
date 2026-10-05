"""Read a government tree register straight from its ArcGIS layer into leads.

Written 2026-10-06 (Hidde: "zoek meer van dit soort registers in de us!") after
the Florida Forest Service layer turned 387 champion trees into leads with
coordinates for zero tokens. data/register-sources-us.json lists each layer:
where it points, which place it feeds and how far out, how its fields map, and
what to refuse (a private-ground flag, an unapproved submission, a dead tree).

It writes LEADS, never data/cities, skips anything within 60 m of a tree we
already publish or already list, and keeps the file's own indentation.
Facts only: these layers carry no open licence for republishing as dots.

  python3 scripts/register_import.py                     # every source
  python3 scripts/register_import.py data/register-sources-us.json cook
"""
import json,urllib.request,urllib.parse,math,glob,os,sys,time
def get(u,p):
    u+='?'+urllib.parse.urlencode(p)
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'AncientTrees/1.0'}),timeout=60))
def km(a,b,c,d): return 6371*2*math.asin(math.sqrt(math.sin(math.radians(c-a)/2)**2+math.cos(math.radians(a))*math.cos(math.radians(c))*math.sin(math.radians(d-b)/2)**2))
def feats(layer,where='1=1'):
    out=[];off=0
    while True:
        r=get(layer+'/query',{'where':where,'outFields':'*','outSR':4326,'f':'json','resultOffset':off,'resultRecordCount':1000})
        fs=r.get('features',[]); out+=fs
        if not r.get('exceededTransferLimit') or not fs: break
        off+=len(fs)
    return out
pub=[]; pubn=[]
_STOP={'the','of','tree','trees','a','in','at','and','on','by','park','national','old','big','great','common','american','eastern','western','southern','northern'}
def _toks(x):
    import re as __re
    return {w for w in __re.findall(r'[a-z]+',(x or '').lower()) if w not in _STOP and len(w)>2}
for f in glob.glob('data/cities/*.json'):
    for t in json.load(open(f))['trees']:
        try:
            pub.append((float(t['location']['latitude']),float(t['location']['longitude'])))
            pubn.append((pub[-1][0],pub[-1][1],_toks(t['name']+' '+t.get('species',''))))
        except: pass
def _near_named(lat,lng,words):
    # 2026-10-06: Washington DC's NPS trees were already ours 100 to 300 m from
    # the register's point, under our own names. Within 300 m, two shared name
    # words mean the same tree.
    for a,b,tk in pubn:
        if abs(a-lat)<0.004 and abs(b-lng)<0.005 and km(lat,lng,a,b)<=0.3 and len(words & tk)>=2: return True
    return False
import re as _re
_EMAIL=_re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')
_PHONE=_re.compile(r'\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b')
def _scrub(v):
    # 2026-10-06: Oklahoma's address field carried owners' emails and phone
    # numbers. Personal contact data never leaves the register, whatever field
    # it hides in; preflight's check_register_leads_carry_no_contact_data()
    # refuses a lead that still holds one.
    if not isinstance(v,str): return v
    return _re.sub(r'\s{2,}',' ',_PHONE.sub('',_EMAIL.sub('',v))).strip(' ,;-')

def num(v):
    try: return float(v)
    except: return None
_cfg=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'data/register-sources-us.json'))
SOURCES=_cfg['sources'] if isinstance(_cfg,dict) else _cfg
if len(sys.argv)>2: SOURCES=[x for x in SOURCES if sys.argv[2].lower() in x['name'].lower()]
summary={}
for s in SOURCES:
    fs=feats(s['layer'],s.get('where','1=1'))
    slug=s['place']; cen=s['centre']
    p=f'data/leads/{slug}.json'
    doc=json.load(open(p)) if os.path.exists(p) else {'city':slug,'leads':[],'blocked':[]}
    ind=1
    if os.path.exists(p):
        l2=open(p).read().split('\n')[1]; ind=max(1,len(l2)-len(l2.lstrip()))
    have={(round(l.get('lat') or 0,4),round(l.get('lng') or 0,4)) for l in doc.get('leads',[])+doc.get('blocked',[]) if isinstance(l,dict)}
    add=addb=0
    for f in fs:
        a=f['attributes']; g=f.get('geometry') or {}
        lat=num(g.get('y')) ; lng=num(g.get('x'))
        if s.get('latlng_fields'):
            lat=num(a.get(s['latlng_fields'][0])); lng=num(a.get(s['latlng_fields'][1]))
        if lat is None: continue
        if km(lat,lng,cen[0],cen[1])>s['radius_km']: continue
        if any(km(lat,lng,x,y)<0.06 for x,y in pub): continue
        if _near_named(lat,lng,_toks(' '.join(str(a.get(s['map'].get(k)) or '') for k in ('name','common','sci','loc')))): continue
        if (round(lat,4),round(lng,4)) in have: continue
        m=s['map']; v=lambda k: (_scrub(a.get(m[k])) if m.get(k) else None)
        common=(v('common') or '').strip(); sci=(v('sci') or '').strip()
        circ=num(v('circ')); h=num(v('height'))
        lead={'name':(v('name') or common or sci or 'unnamed').strip(),'species':f"{common} ({sci})" if sci else common,
              'lat':round(lat,6),'lng':round(lng,6),'register_location':(v('loc') or '').strip() if v('loc') else None,
              'girth_cm':round(circ*s.get('circ_to_cm',2.54)) if circ else None,'height_m':round(h*0.3048,1) if h else None,
              'register_status':v('status'),'sources':[s['source_url']],
              'source':s['source_note'],'status':'open'}
        if v('photo'): lead['register_photo']=v('photo')
        blk=None
        for k,bad in (s.get('block_if') or {}).items():
            val=str(a.get(k) or '').strip().lower()
            if val in bad: blk=f"register field {k}={val!r}: not public or not to be listed (hard rule 10)"
        for k in (s.get('block_if_set') or []):
            if str(a.get(k) or '').strip(): blk=blk or f"register field {k}={a.get(k)!r}: marked dead or not found"
        for k,good in (s.get('keep_if') or {}).items():
            val=str(a.get(k) or '').strip().upper()
            if val not in good: blk=blk or f"register field {k}={val!r}: not an approved public entry"
        if blk: doc.setdefault('blocked',[]).append({**lead,'reason':blk}); addb+=1
        else: doc.setdefault('leads',[]).append(lead); add+=1
        have.add((round(lat,4),round(lng,4)))
    open(p,'w').write(json.dumps(doc,indent=ind,ensure_ascii=False)+'\n')
    summary.setdefault(slug,[0,0]); summary[slug][0]+=add; summary[slug][1]+=addb
    print(s['name'],'->',slug,'rows',len(fs),'leads +',add,'blocked +',addb)
    time.sleep(0.5)
print(summary)
