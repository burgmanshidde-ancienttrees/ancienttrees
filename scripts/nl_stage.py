#!/usr/bin/env python3
"""Stage a Dutch register city so a night run can just write it.

Hidde, 2026-08-22, on the eleven cities left over from his top 25: "prima zet
ze maar klaar". Staging means putting the work where the existing machinery
already looks, rather than in a folder that needs a new instruction to find:

  data/leads/<slug>.json            the shape scripts/leads.py reads, so the
                                    trees show up under `leads.py --ready` and
                                    reach rung 4(a), "write what is already
                                    verified", with no new rule anywhere.
  data/research/<slug>-verified.json  the input BRIEF_WRITING.md documents, so a
                                    write pass can be dispatched straight at it.

Both are generated from the same selection, so they cannot drift apart.

Two things this deliberately does NOT do, because they are judgement and belong
to the writing pass: it does not name the trees properly (it gives a working
title of species plus place) and it does not write a word of prose.

Three things it does enforce, each of which cost a real error today:
  - school grounds are staged as BLOCKED, in the wording data/block-reasons.json
    matches, because CLAUDE.md's school rule is about not sending adult
    strangers where children are and no register field can decide that.
  - a candidate 200 years or older with no register history is marked for a
    check before publishing, because the register carries trees that have been
    gone for thirty years.
  - the id prefix is taken from what is actually published, since Venlo
    generated as Venice's.
"""
import json, os, re, sys, argparse, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nl_candidates as N
from nl_to_research import prefix

SCHOOL = re.compile(r"\bschool\b|lyceum|gymnasium|basisschool|schoolplein|college\b", re.I)


def working_title(t):
    """A title good enough to sort by, honest about being provisional."""
    if t["own_name"]:
        return t["own_name"]
    sp = (t["species"] or t["register_name"] or "Tree").split(" (")[0]
    place = (t["place"] or "").split(",")
    where = place[-1].strip() if len(place) > 1 else (place[0].strip() if place else "")
    where = re.sub(r"\s+", " ", where)[:44]
    return ("%s, %s" % (sp, where)).strip(", ")


def why(t, risky):
    bits = ["LRMB register nr %s (%r)." % (t["nr"], t["register_name"])]
    bits.append("Register planting band %s, so the age is a BAND and must not be sharpened."
                % t["planted_band"])
    bits.append("Register records it as publicly visitable; owner category %s, setting %s."
                % (t["owner_category"], t["setting"]))
    if t["honour_class"] == "ja":
        bits.append("EREKLASSE, the register's top designation, 99 trees nationally.")
    if risky:
        bits.append("CHECK IT IS STILL STANDING before writing: over 200 years old and the "
                    "register gives no history for it, which is the blind spot that let "
                    "Tilburg's Heuvel lime and Alkmaar's thickest beech through today.")
    if t["site_history"]:
        bits.append("Register history of the PLACE, not of the tree, so do not bridge from it: %s"
                    % re.sub(r"\s+", " ", t["site_history"]).strip())
    bits.append("The register is ONE source. A second is wanted; without one the tree still "
                "ships with curation_status flagged.")
    return " ".join(bits)


def stage(city, n=9, km=3.0, write=True):
    trees = N.load(city)
    if not trees:
        return None
    groups = N.cluster(trees, km=km)
    for g in groups:
        g.sort(key=N.score, reverse=True)
    g = max(groups, key=lambda x: (len(x), sum(N.score(t) for t in x)))
    picked = g[:n]

    slug = city.lower().replace(" ", "-").replace("'", "")
    px = prefix(city)

    leads, research, blocked = [], [], 0
    i = 0
    for t in picked:
        risky = N.needs_alive_check(t)
        if SCHOOL.search(t["place"] or ""):
            leads.append({
                "name": working_title(t), "species": t["species"] or t["register_name"],
                "lat": t["latitude"], "lng": t["longitude"], "status": "blocked",
                "why": ("On a primary school playground. Not published: CLAUDE.md's school rule "
                        "keeps this site from sending adult strangers onto school grounds, and "
                        "no register field can settle whether the grounds are genuinely open. "
                        "LRMB nr %s." % t["nr"]),
            })
            blocked += 1
            continue
        i += 1
        leads.append({
            "name": working_title(t), "species": t["species"] or t["register_name"],
            "lat": t["latitude"], "lng": t["longitude"], "status": "lead",
            "why": why(t, risky),
        })
        research.append({
            "id": "%s_%03d" % (px, i),
            "name": None,
            "species": t["species"] or "TO ESTABLISH: register name %r" % t["register_name"],
            "age_estimate": t["age_estimate"], "age_min": t["age_min"], "age_max": t["age_max"],
            "location": {"address": t["place"], "latitude": t["latitude"],
                         "longitude": t["longitude"], "neighbourhood": None},
            "verified_sources": ["https://www.monumentalebomen.nl/"],
            "access": None, "transport": None,
            "photo": {"url": None, "license": None, "attribution": None, "status": "missing"},
            "curation_status": "flagged", "location_precision": "approximate",
            "verify_notes": why(t, risky),
        })

    if write:
        json.dump({"city": city, "country": "Netherlands", "city_slug": slug,
                   "note": ("Staged 2026-08-22 from the Landelijk Register Monumentale Bomen "
                            "(Bomenstichting, attribution required). Publicly visitable single "
                            "trees only, entries the register's own history says are gone already "
                            "removed. Needs only a story per tree; see "
                            "data/research/%s-verified.json for the write-pass input." % slug),
                   "leads": leads}, open("data/leads/%s.json" % slug, "w"),
                  indent=1, ensure_ascii=False)
        json.dump(research, open("data/research/%s-verified.json" % slug, "w"),
                  indent=1, ensure_ascii=False)
    span = max((N.haversine(x["latitude"], x["longitude"], y["latitude"], y["longitude"])
                for x in picked for y in picked), default=0)
    return {"city": city, "slug": slug, "prefix": px, "staged": len(research),
            "blocked": blocked, "span_km": round(span, 1),
            "risky": sum(1 for t in picked if N.needs_alive_check(t))}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cities", nargs="+")
    p.add_argument("--n", type=int, default=9)
    p.add_argument("--km", type=float, default=3.0)
    a = p.parse_args()
    print("%-24s %4s %7s %8s %7s %6s" % ("city", "pfx", "staged", "blocked", "check", "km"))
    tot = 0
    for c in a.cities:
        r = stage(c, n=a.n, km=a.km)
        if not r:
            print("%-24s  no visitable single trees in the register" % c); continue
        tot += r["staged"]
        print("%-24s %4s %7d %8d %7d %6.1f"
              % (r["city"], r["prefix"], r["staged"], r["blocked"], r["risky"], r["span_km"]))
    print("\n%d trees staged across %d cities" % (tot, len(a.cities)))


if __name__ == "__main__":
    main()
