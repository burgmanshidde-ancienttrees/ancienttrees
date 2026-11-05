import json, os, sys
sys.path.insert(0, "scripts")
import sightings_publish as sp

SID = "15a3b6f1-3dd9-4ac2-bec5-bbd1c47d7613"
TODAY = "2026-11-05"
SRC = "out/sightings/15a3b6f1-3dd9-4ac2-bec5-bbd1c47d7613.jpg"
LAT, LON = 47.0038375771111, 7.01202241704521
TID = "ltn_001"
NAME = "The Three Atlas Cedars of Préfargier"
FNAME = "ltn_001-the-three-atlas-cedars-of-prefargier.jpg"

w, h = sp.write_image(SRC, os.path.join(sp.PHOTOS, FNAME))

story = (
    "Three Atlas cedars stand together on one lawn in the park of the Préfargier estate, in the "
    "commune of La Tène, canton of Neuchâtel. A reader sent us their photograph and put it in one "
    "line, “3 cèdres de l’Atlas, dans le park du domaine de la maison de santé de Préfargier.”\n\n"
    "The photograph shows why it was worth a picture. Three separate trunks rise a few metres apart "
    "and their crowns have grown into a single dark, broad pyramid, with silvery blue-green needles "
    "at the branch tips, the colour the Atlas cedar, Cedrus atlantica, is known for. It comes from "
    "the Atlas Mountains of Morocco and Algeria. A bench stands under the nearest trunk, and a walker "
    "on the gravel path beside the lawn looks small next to the whole.\n\n"
    "We have found no girth, height or planting date for these three, so this page gives none. "
    "Beside the path a panel in French explains what trees do for mental health, with a QR code for "
    "more. A reader's measurements would be welcome here.\n\n"
    "Walk to the edge of the lawn and the three crowns read as one tree."
)

tree = {
    "id": TID,
    "name": NAME,
    "species": "Atlas Cedar (Cedrus atlantica)",
    "age_estimate": "not documented",
    "age_min": None,
    "age_max": None,
    "age_basis": "source",
    "location": {
        "address": "Parc du domaine de Préfargier, Marin-Epagnier, La Tène, canton of Neuchâtel",
        "latitude": LAT,
        "longitude": LON,
        "neighbourhood": "Préfargier, Marin-Epagnier",
    },
    "story": story,
    "how_to_recognise": "Three Atlas cedars on one open lawn beside a gravel path, their crowns joined into one broad pyramid of blue-green needles, with a bench under the nearest trunk.",
    "verified_sources": [],
    "found_by_reader": {"sighting_id": SID, "date": "2026-11-05"},
    "verify_notes": "2026-11-05: published from a reader's app photograph, note and GPS fix (sighting 15a3b6f1) on Hidde's 2026-10-21 ruling that a good photograph with a GPS fix is not held. Species, location and the grouping of three are the reader's, and the photograph shows three conifers with glaucous blue-green foliage and horizontal tiered branches, consistent with Atlas cedar. No register entry within 100 m and no encyclopaedia article within 300 m; two web searches found no source on the park. Access: the estate is a health-care site (maison de santé), no source states its opening hours, but the cedars stand beside a gravel footpath with a public information panel and a walker in the photograph, so the tree is clearly seen from public ground (rule 10); access says so plainly. No girth, height or age.",
    "access": "Seen from a gravel footpath through the estate's park, where a public information panel stands. We found no opening hours for the grounds, so respect any signs at the entrance.",
    "transport": "At Préfargier near Marin-Epagnier, in the commune of La Tène, canton of Neuchâtel; look up the nearest stop on sbb.ch.",
    "photo": sp.photo_block(
        {"tree_id": TID, "tree_name": NAME, "user_id": "p_2e79bf68318b596d2c9298dc",
         "sighting_id": SID, "taken_at": "2026-11-05"},
        w, h, "three trunks and one crown fill the frame in daylight and colour", TODAY, FNAME),
    "curation_status": "flagged",
    "location_precision": "confirmed",
    "pin_source": {
        "kind": "reader GPS fix",
        "sighting_id": SID,
        "moved_m": 0,
        "date": TODAY,
        "note": "The pin marks where a reader stood to photograph this tree; the photograph was checked to show it.",
    },
}
tree["photo"]["contributor_user_id"] = "p_2e79bf68318b596d2c9298dc"

city = {
    "city": "La Tène",
    "country": "Switzerland",
    "status": "needs_curation",
    "intro": "A trio of Atlas cedars on a lawn in the park of the Préfargier estate, at Marin-Epagnier in the commune of La Tène, canton of Neuchâtel, sent to us by a reader with a photograph. Seen from a public footpath.",
    "meta_description": "Three Atlas cedars at Préfargier in La Tène, canton of Neuchâtel: a reader's photograph, where they stand and how to see them.",
    "hero_tree_id": TID,
    "oldest_tree_id": TID,
    "trees": [tree],
    "question_meta": "Three Atlas cedars grow together at Préfargier, La Tène, canton of Neuchâtel. Where they stand and how to see them.",
    "question_answer": "A reader found three Atlas cedars (Cedrus atlantica) growing together on a lawn in the park of the Préfargier estate at Marin-Epagnier, in La Tène, canton of Neuchâtel. They are visible from a gravel footpath.",
    "question_context": "The grouping, species and place come from a reader's photograph and note. No register or published source lists these trees, and no girth, height or planting date is known.",
    "faq": [
        {"q": "What kind of trees are they?", "a": "Atlas cedars (Cedrus atlantica), three trunks whose crowns have grown into one broad pyramid."},
        {"q": "Where are they?", "a": "On a lawn in the park of the Préfargier estate, Marin-Epagnier, in the commune of La Tène, canton of Neuchâtel."},
        {"q": "How old are they?", "a": "We have found no planting date or measurement for them."},
    ],
}
with open("data/cities/la-tene.json", "w", encoding="utf-8") as fh:
    json.dump(city, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("ok", w, h, len(story.split()))
