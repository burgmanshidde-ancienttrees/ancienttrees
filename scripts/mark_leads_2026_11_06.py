"""Mark the READY leads the 2026-11-06 write pass looked at: shipped as an id,
or [SKIPPED 2026-11-06 by the write pass: why], so leads.py --ready stops
offering them.

    python3 scripts/mark_leads_2026_11_06.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = "[SKIPPED 2026-11-06 by the write pass: {}] "

MARKS = {
    "new-york": [
        ("Bald cypress, Flushing High School", "skip", "school grounds with no evidence they are open, and six trees rather than one point"),
        ("Bald cypress, 143-66 Sanford Ave", "skip", "residential front yard, hard rule 10"),
        ("Willow oak, 86 Herbert St", "done", "already published as nyc_143 on 2026-11-06"),
        ("Black oak, Queens (Parks id=117)", "skip", "no location text or species detail, unplaceable"),
        ("Swamp white oak SI (id=127)", "skip", "four Parks entries in one row with no description and no single point"),
        ("Canadian burr oak, City Hall Park", "skip", "planted 1967, 17 in, species disputed (forestry says white oak); NYC Parks pages answer a CAPTCHA to curl, so no source text to write from"),
        ("Blue spruce AIDS Memorial Tree", "skip", "donated 2010, 12 in; NYC Parks page behind a CAPTCHA, so no memorial text to write from"),
        ("Weeping willow, Randall's Island", "skip", "31 in, Parks says younger than other Great Trees; Parks page behind a CAPTCHA, no story source"),
        ("Weeping willow, 6th Ave & 15th St", "skip", "inside a community garden fence, open hours not settled"),
        ("Post oak grove, Hunter Island", "skip", "grove with no individual tree coordinate, not one collectible point"),
        ("Pelham Bay littleleaf linden", "skip", "no point in the forestry inventory, grove mostly gone"),
        ("European horse chestnut, Green-Wood stop 1", "skip", "no size, age or story, and the genus line is wrong (horse chestnut is Aesculus)"),
    ],
    "enniskerry": [("Tallest tree in Ireland, River Walk Douglas fir", "done", "shipped as enk_001 (pin approximate at register row 437)")],
    "doneraile": [("Large twin-stem yew", "skip", "no spot in a large park (ancient-yew.org: exact position not known) and no life evidence after 2009; a location that cannot be stated honestly")],
    "inverness": [("Cawdor Castle old yew", "skip", "survival unknown per ancient-yew.org, no girth, nothing to write from")],
    "wales-yews": [("Mamhilad yews (St Illtyd)", "done", "already published as mmh_001 in data/cities/mamhilad.json")],
    "leesburg": [
        ("Norway Maple (Virginia champion)", "skip", "registry point behind houses at 226-229 N King St, no public access shown"),
        ("Red Mulberry 45 ft x 218 in", "done", "shipped as lsb_009"),
    ],
    "wisconsin": [("Quaking Aspen, Plum Lake Hemlock Forest", "skip", "one of about six aspens off an unmarked path, nothing tells it apart")],
    "florence": [
        ("The Monterey Cypress of Largo Fermi", "skip", "not stated whether it stands outside the observatory gate or inside the institute"),
        ("The Hackberry of Terenzano", "done", "shipped as flo_029"),
        ("The Cypress of Via del Bargellino", "skip", "two rural trees, access and life not checked"),
    ],
}


def main():
    for slug, marks in MARKS.items():
        path = os.path.join(ROOT, "data", "leads", slug + ".json")
        raw = open(path, encoding="utf-8").read()
        m = re.match(r"\{\n( +)\"", raw)
        indent = len(m.group(1)) if m else 1
        d = json.loads(raw)
        for name, kind, why in marks:
            hits = [e for e in d.get("leads", []) if isinstance(e, dict) and str(e.get("name", "")).startswith(name)]
            if len(hits) != 1:
                print("!!", slug, name, len(hits), "matches")
                continue
            e = hits[0]
            key = "why" if "why" in e and "reason" not in e else "reason"
            old = e.get(key, "")
            if kind == "done":
                e[key] = why.replace("shipped as", "Shipped as").replace("already published", "Already published") + ". " + old
                e["status"] = "published"
            else:
                e[key] = TAG.format(why) + old
            print(slug, kind, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=indent)
            f.write("\n")


if __name__ == "__main__":
    main()
