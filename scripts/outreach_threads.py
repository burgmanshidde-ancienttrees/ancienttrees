#!/usr/bin/env python3
"""How much mail has gone each way with every ambassador prospect, from Hidde's
mailbox. Read-only Gmail SEARCH on addresses already in our outreach files;
no message is opened. Writes data/outreach-threads.json, which
scripts/ambassador_prospects.py reads (Hidde, 2026-10-06: "check my inbox
against people ive had regular contact with dont contact them").

    source ~/.ancienttrees-mail.env && python3 scripts/outreach_threads.py
"""
import imaplib, json, os, time
d=json.load(open('data/ambassador-prospects.json'))
addrs=[c['email'] for c in d['contacts'] if c['status'] in ('asked','replied','recontact')]
P='data/outreach-threads.json'
out=json.load(open(P)) if os.path.exists(P) else {}
def conn():
    M=imaplib.IMAP4_SSL(os.environ.get('OUTREACH_IMAP_HOST','imap.gmail.com'))
    M.login(os.environ['OUTREACH_SMTP_USER'],os.environ['OUTREACH_SMTP_PASS'])
    box=[b.decode().split(' "/" ')[-1] for b in M.list()[1] if b'\\All' in b][0]
    M.select(box, readonly=True); return M
M=conn()
def n(q):
    global M
    for i in range(3):
        try: return len(M.search(None,'X-GM-RAW',f'"{q}"')[1][0].split())
        except Exception:
            time.sleep(2); M=conn()
    return -1
for a in addrs:
    if a in out: continue
    out[a]={'from_them':n(f'from:{a} after:2026/08/08'),'to_them':n(f'to:{a} after:2026/08/08')}
    json.dump(out,open(P,'w'),indent=1)
print(len(out),'addresses checked')
