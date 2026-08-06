import json, glob, io, os, urllib.request
from PIL import Image
def thumb(u, w=240):
    if 'upload.wikimedia.org' in u and '/commons/' in u and '/thumb/' not in u:
        a,b=u.split('/commons/'); return f"{a}/commons/thumb/{b}/{w}px-{b.split('/')[-1]}"
    return u
rows=[]
for f in sorted(glob.glob('data/cities/*.json')):
    d=json.load(open(f))
    for t in d['trees']:
        p=t.get('photo') or {}
        if p.get('url'): rows.append((os.path.basename(f)[:-5], d['city'], t['id'], t['name'], p['url']))
print(len(rows),"photos to sample", flush=True)
grey=[]
for i,(slug,city,tid,name,url) in enumerate(rows):
    try:
        req=urllib.request.Request(thumb(url), headers={'User-Agent':'AncientTrees/qa'})
        im=Image.open(io.BytesIO(urllib.request.urlopen(req,timeout=25).read())).convert('RGB')
        im.thumbnail((160,160))
        px=list(im.getdata())
        sat=sum(max(r,g,b)-min(r,g,b) for r,g,b in px)/len(px)
        if sat < 12: grey.append((round(sat,1), slug, tid, name, url))
    except Exception as e:
        print("  fetch failed:", tid, type(e).__name__, flush=True)
print("\n=== near-greyscale (mean saturation < 12) ===")
for g in sorted(grey): print(f"  sat {g[0]:5}  {g[1]:12} {g[2]} {g[3][:40]}")
json.dump([{"slug":g[1],"id":g[2],"name":g[3],"sat":g[0],"url":g[4]} for g in grey],
          open('/tmp/bw.json','w'), indent=1)
