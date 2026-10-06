#!/usr/bin/env python3
"""Who to ask to be an ambassador, city by city, cross-referenced with every
mail we ever sent.

Hidde, 2026-10-06: "you make a list of who to approach - and as always cross
reference who we've already contacted", and "it might not be weird to
recontact some that didnt respond because we have an app and ambassador
program now". The ambassadors we have all came out of earlier outreach
(CLAUDE.md, Ambassadors), so the first names to ask are people we already
wrote to.

Reads only files we keep: data/outreach-sent.json (every mail), data/
outreach-replies.json (every answer), data/outreach-contacts*.json (who each
address is and which city), data/ambassadors.json and data/cities. Writes
drafts/ambassador-prospects.md and data/ambassador-prospects.json. Sends
nothing.

Per contact, one status:
  ambassador   already named
  replied      wrote back (the kind is kept: correction, data, referral...)
  recontact    mailed, never answered, not on the do-not-contact list
  new          a contact on file that was never mailed
Cities with nobody on file at all are listed last: those need research.
"""
import glob
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    return json.load(open(os.path.join(ROOT, p), encoding="utf-8"))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def main():
    sent = load("data/outreach-sent.json")
    dnc = [x.lower() for x in sent.get("do_not_contact", [])]
    replies = load("data/outreach-replies.json")["replies"]
    amb = load("data/ambassadors.json")["ambassadors"]
    amb_names = {norm(a.get("display_name", "")) for a in amb}

    contacts = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "outreach-contacts*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for c in (d if isinstance(d, list) else d.get("contacts", [])):
            e = (c.get("email") or "").strip().lower()
            if e and e not in contacts:
                contacts[e] = c

    # From scripts/outreach_threads.py: mail each way in Hidde's own box,
    # which also holds the threads he wrote by hand.
    tp = os.path.join(ROOT, "data", "outreach-threads.json")
    threads = json.load(open(tp)) if os.path.exists(tp) else {}
    mailed = {}
    for m in sent["sent"]:
        e = (m.get("to") or "").strip().lower()
        mailed.setdefault(e, []).append(m)
    # Replies logged without an address still name the person.
    reply_orgs = {norm(r.get("org", "")).split(" ")[0] + " " + norm(r.get("org", "")).split(" ")[1]
                  for r in replies if not r.get("to_address") and len(norm(r.get("org", "")).split()) > 1}
    answered = {}
    for r in replies:
        e = (r.get("to_address") or "").strip().lower()
        answered.setdefault(e, []).append(r.get("kind") or "?")

    cities = {}
    for p in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        d = json.load(open(p, encoding="utf-8"))
        n = len([t for t in d.get("trees") or [] if t.get("story")])
        cities[norm(d.get("city", ""))] = {"slug": os.path.basename(p)[:-5], "city": d.get("city"),
                                           "country": d.get("country"), "trees": n}

    rows = []
    for e in sorted(set(contacts) | set(mailed)):
        if not e or "@" not in e or "burgmans" in e or "hidde" in e:
            continue  # our own test sends
        c = contacts.get(e, {})
        m = mailed.get(e, [])
        # The most descriptive name any record gives this address: thread
        # replies log their outlet as just "reply".
        names = [c.get("org") or ""] + [x.get("outlet") or "" for x in m]
        who = max(names, key=len) or e
        alltext = norm(" ".join(names + [x.get("subject", "") + " " + x.get("resend_reason", "") for x in m]))
        city = c.get("city") or ""
        if any(e == x or (x.startswith("@") and e.endswith(x)) for x in dnc):
            status = "do_not_contact"
        elif any(n and (n in alltext or n.split()[-1] in e) for n in amb_names):
            status = "ambassador"
        elif e in threads and (threads[e]["from_them"] >= 2 or
                               (threads[e]["from_them"] >= 1 and threads[e]["to_them"] >= 4)):
            # A running correspondence is Hidde's own, never a template
            # (2026-10-06: "wolfgang jon etc all have been mailed numerous times").
            status = "in_contact"
        elif e in threads and threads[e]["to_them"] >= 3 and (
                (e in answered and set(answered[e]) != {"auto"}) or any(k and k in alltext for k in reply_orgs)):
            # They answered, from another address or by phone, and the thread
            # ran on: a correspondence all the same.
            status = "in_contact"
        elif e in threads and threads[e]["from_them"] == 0 and threads[e]["to_them"] >= 3:
            status = "mailed_enough"
        elif any("mbassad" in (x.get("batch", "") + x.get("subject", "")) for x in m):
            # Asked already (2026-10-02 onward) and not named yet: a nudge,
            # never a second ask.
            status = "asked"
        elif (e in answered and set(answered[e]) != {"auto"}) or any(
                k and k in alltext for k in reply_orgs):
            # An out-of-office is not an answer from a person.
            status = "replied"
        elif m:
            status = "recontact"
        else:
            status = "new"
        th = threads.get(e, {})
        rows.append({"from_them": th.get("from_them"), "to_them": th.get("to_them"), "email": e, "who": who, "city": city, "country": c.get("country", ""),
                     "type": c.get("type", ""), "status": status,
                     "first_mailed": m[0]["date"] if m else None, "mails": len(m),
                     "reply_kinds": answered.get(e, []), "why": (c.get("why_them") or "")[:200]})

    covered = {norm(r["city"]) for r in rows if r["city"]}
    no_one = sorted((v for k, v in cities.items() if k not in covered and v["trees"] >= 4),
                    key=lambda v: (v["country"] or "", v["city"]))

    json.dump({"generated": "scripts/ambassador_prospects.py", "contacts": rows,
               "cities_without_contact": no_one},
              open(os.path.join(ROOT, "data", "ambassador-prospects.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    order = ["in_contact", "mailed_enough", "asked", "replied", "recontact", "new", "ambassador", "do_not_contact"]
    title = {"in_contact": "In regular contact already: do NOT contact, these threads are personal",
             "mailed_enough": "Mailed three times or more, never answered: leave alone",
             "asked": "Asked to be an ambassador, no answer yet: a short nudge",
             "replied": "Wrote back, never asked to be an ambassador: ask first",
             "recontact": "Mailed, never answered: worth a second mail now there is an app and an ambassador programme",
             "new": "On file, never mailed",
             "ambassador": "Already ambassador",
             "do_not_contact": "Do not contact"}
    out = ["# Ambassador prospects", "",
           "Generated by `scripts/ambassador_prospects.py` from every mail in data/outreach-sent.json. "
           "Re-run it after each batch. Nothing here has been sent.", "",
           "| Status | Contacts |", "|---|---:|"]
    for s in order:
        out.append(f"| {title[s]} | {sum(1 for r in rows if r['status'] == s)} |")
    out.append(f"| Cities of four or more trees with nobody on file | {len(no_one)} |")
    for s in order[2:6]:
        part = sorted((r for r in rows if r["status"] == s), key=lambda r: (r["country"], r["city"], r["who"]))
        out += ["", f"## {title[s]} ({len(part)})", "",
                "| City | Country | Who | Address | First mailed | Answer |", "|---|---|---|---|---|---|"]
        for r in part:
            out.append(f"| {r['city'] or '?'} | {r['country']} | {r['who']} | {r['email']} | "
                       f"{r['first_mailed'] or '-'} | {', '.join(r['reply_kinds']) or '-'} |")
    out += ["", f"## Cities with nobody on file ({len(no_one)}): these need a name found", "",
            "| City | Country | Trees |", "|---|---|---:|"]
    for v in no_one:
        out.append(f"| {v['city']} | {v['country']} | {v['trees']} |")
    open(os.path.join(ROOT, "drafts", "ambassador-prospects.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out[:12]))


if __name__ == "__main__":
    main()
