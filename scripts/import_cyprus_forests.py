#!/usr/bin/env python3
"""Import the Cyprus Department of Forests list of tree natural monuments
outside the state forests into data/registers/cyprus-forests.json.

Source: data.gov.cy, "Μεμονωμένα δέντρα μνημεία της φύσης εκτός των κρατικών
δασών", CC BY 4.0. 81 rows: species (Greek common name), district, village,
girth at chest height (m), height (m), age, proclamation date. No coordinates,
no owners' names, no vitality field.

The age column is the register's round estimate carried forward to about 2012
(rows declared in 1999 end in 13, 2004 in 08 or 58, 2006 in 06 or 56, 2011 in
00 or 50), so `age_years` keeps the number as printed and `age_note` says so.
The species column is a Greek (often Cypriot) common name; `species_en` is our
reading of it, `species_sure` False where the name maps to more than one tree.

Usage: python3 scripts/import_cyprus_forests.py out/tmp/cyprus-trees.csv
"""
import csv
import json
import sys
from datetime import date

SPECIES = {
    # Greek name: (English (Latin), sure)
    "Πλάτανος": ("Oriental Plane (Platanus orientalis)", True),
    "Κυπαρίσσι": ("Mediterranean Cypress (Cupressus sempervirens)", True),
    "Δρυς": ("Oak (Quercus sp.)", False),
    "Καζουαρίνα": ("Casuarina (Casuarina sp.)", False),
    "Λατζιά": ("Oak (Quercus sp.)", False),
    "Περνιά": ("Kermes Oak (Quercus coccifera)", False),
    "Πεύκος": ("Pine (Pinus sp.)", False),
    "Πεύκος της Μάχης": ("Pine (Pinus sp.)", False),
    "Τρέμιθος": ("Atlas Pistachio (Pistacia atlantica)", False),
    "Τρεμιθιά": ("Atlas Pistachio (Pistacia atlantica)", False),
    "Μαχαίριο": (None, False),
    "Δάφνη": ("Bay Laurel (Laurus nobilis)", True),
    "Ελιά": ("Olive (Olea europaea)", True),
    "Κληματαριά": ("Grapevine (Vitis vinifera)", True),
    "Στερατζιά": (None, False),
    "Συκαμινιά": ("Mulberry (Morus sp.)", False),
    "Χαρουπιά": ("Carob (Ceratonia siliqua)", True),
    "Συκομουριά (Τουμπεζιά)": ("Sycamore Fig (Ficus sycomorus)", True),
    "Αόρατος": (None, False),
    "Αμυγδαλιά": ("Almond (Prunus dulcis)", True),
    "Κονναρκά": ("Christ's Thorn Jujube (Ziziphus spina-christi)", False),
}

DISTRICT = {"Λευκωσίας": "Nicosia", "Λεμεσού": "Limassol", "Πάφου": "Paphos",
            "Λάρνακας": "Larnaca", "Αμμοχώστου": "Famagusta"}

VILLAGE = {
    "Νήσου": "Nisou", "Φτερικούδι": "Fterikoudi", "Ψημολόφου": "Psimolofou",
    "Πέρα Πεδί": "Pera Pedi", "Κουκά": "Kouka", "Χούλου": "Choulou",
    "Απλίκι": "Apliki", "Καλοπαναγιώτης": "Kalopanagiotis", "Κάμπος": "Kampos",
    "Κάτω Πύργος": "Kato Pyrgos", "Πολιτικό (Φιλάνι)": "Politiko (Filani)",
    "Αγία Μαύρη (Κοιλάνι)": "Agia Mavri (Koilani)", "Απαισιά": "Apesia",
    "Κολόσσι": "Kolossi", "Λάνια": "Lania", "Λιμνάτης": "Limnatis",
    "Όμοδος": "Omodos", "Πάνω Πλάτρες": "Pano Platres", "Αγγλισίδες": "Anglisides",
    "Αργάκα": "Argaka", "Κρήτου Μαρόττου": "Kritou Marottou",
    "Πόλη Χρυσοχού": "Polis Chrysochous", "Προδρόμι": "Prodromi",
    "Σαλαμιού": "Salamiou", "Σίμου": "Simou", "Στενή": "Steni",
    "Τραχυπέδουλα": "Trachypedoula", "Φοίτη": "Foiti", "Αγία Νάπα": "Ayia Napa",
    "Αγία Ειρήνη": "Agia Eirini", "Μουτουλλάς": "Moutoullas",
    "Άγιος Θεόδωρος": "Agios Theodoros", "Επταγώνεια": "Eptagoneia",
    "Κλωνάρι": "Klonari", "Πάχνα": "Pachna", "Χανδριά": "Chandria",
    "Άγιος Νικόλαος": "Agios Nikolaos", "Λαγουδερά": "Lagoudera",
    "Πάνω Λεύκαρα": "Pano Lefkara", "Περβόλια": "Pervolia",
    "Άγιος Θεράπων": "Agios Therapon", "Άγιος Μάμας": "Agios Mamas",
    "Αυδήμου": "Avdimou", "Βάσα Κοιλανίου": "Vasa Koilaniou",
    "Κάτω Μύλος": "Kato Mylos", "Κάτω Πολεμίδια": "Kato Polemidia",
    "Κισσούσα": "Kissousa", "Κυπερούντα": "Kyperounta", "Ποταμιού": "Potamiou",
    "Σιλίκου": "Silikou", "Σωτήρα": "Sotira", "Γεροσκήπου": "Geroskipou",
    "Γιόλου": "Giolou", "Κελοκέδαρα": "Kelokedara", "Τάλα": "Tala",
    "Φιλούσα Χρυσοχούς": "Filousa Chrysochous",
}


def num(v):
    try:
        return float(str(v).replace(",", ""))
    except ValueError:
        return None


def main():
    rows = []
    with open(sys.argv[1], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            gr = r["Name/Species"].strip()
            en, sure = SPECIES.get(gr, (None, False))
            d, m, y = r["Proclamation_Date"].split("/")
            girth = num(r["Circumference_at_chest_height (m)"])
            rows.append({
                "register_id": f"CY-FD-{int(r['A/A']):02d}",
                "species_el": gr,
                "species": en,
                "species_sure": sure,
                "district": DISTRICT[r["Location/Area"].strip()],
                "village_el": r["Village"].strip(),
                "village": VILLAGE.get(r["Village"].strip()),
                "girth_cm": round(girth * 100) if girth else None,
                "height_m": num(r["Height (m)"]),
                "age_years": int(num(r["Age"])) if num(r["Age"]) else None,
                "proclaimed": f"{y}-{int(m):02d}-{int(d):02d}",
                "latitude": None,
                "longitude": None,
                "location_precision": "village",
                "ground": "unknown",
            })
    out = {
        "source": "Τμήμα Δασών (Department of Forests, Republic of Cyprus): Μεμονωμένα δέντρα μνημεία της φύσης εκτός των κρατικών δασών",
        "endpoint": "https://data.gov.cy/sites/default/files/TreeMonumentsOutsideStateForests.csv",
        "dataset_page": "https://data.gov.cy/el/dataset/memonomena-dentra-mnimeia-tis-fysis-ektos-ton-kratikon-dason",
        "country": "Cyprus",
        "designation": "individual tree declared a natural monument (μνημείο της φύσης) outside the state forests",
        "licence": "CC BY 4.0",
        "licence_proof": "Dataset page, licence block: 'Creative Commons Attribution 4.0 International (CC BY 4.0)'. Read 2026-11-02.",
        "attribution": "Department of Forests, Republic of Cyprus, via data.gov.cy (CC BY 4.0)",
        "fetched": date.today().isoformat(),
        "scope": "81 trees outside the state forests, Republic-controlled districts only (no rows north of the Green Line). The roughly 70 monument trees inside the state forests are not in this file.",
        "caveat": "No coordinates: village only, every pin approximate until a source places the trunk. No owners' names in the source; whether a tree stands on private ground is not stated (ground 'unknown'), so access is checked per tree. Ages are round estimates carried forward to about 2012 (declared 1999 rows end in 13, 2004 in 08/58, 2006 in 06/56, 2011 in 00/50): quote them broadly. Species is a Greek common name; species_sure False where it is ambiguous (Δρυς may be Quercus infectoria subsp. veneris or Q. alnifolia; Τρέμιθος is mostly Pistacia atlantica).",
        "count": len(rows),
        "trees": rows,
    }
    with open("data/registers/cyprus-forests.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(len(rows), "rows;", sum(1 for r in rows if not r["village"]), "villages untransliterated;",
          sum(1 for r in rows if not r["species"]), "species unread")


if __name__ == "__main__":
    main()
