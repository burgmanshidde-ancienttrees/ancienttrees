import json, os, sys
sys.path.insert(0, "scripts")
import sightings_publish as sp

SID = "15a3b6f1-3dd9-4ac2-bec5-bbd1c47d7613"
TODAY = "2026-11-05"
SRC = "out/photos/15a3b6f1-3dd9-4ac2-bec5-bbd1c47d7613.jpg"
LAT, LON = 47.0038375771111, 7.01202241704521
TID = "prf_001"
NAME = "The Three Atlas Cedars of Préfargier"
FNAME = "prf_001-the-three-atlas-cedars-of-prefargier.jpg"

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
    "Each trunk is broad and dark, and the lowest limbs sweep out over the grass almost to the "
    "ground, so the group spreads far across the lawn. In the photograph the light is "
    "grey, an autumn day, and the cedars are the darkest thing in the park, against the yellowing "
    "woods behind them.\n\n"
    "We have found no girth, height or planting date for these three, so this page gives none. "
    "If you stand under them with a tape, a measurement would be welcome here.\n\n"
    "Walk to the edge of the lawn and the three crowns read as one tree."
)

tree = {
    "id": TID,
    "name": NAME,
    "species": "Atlas Cedar (Cedrus atlantica)",
    "age_estimate": "not documented",
    "age_min": None,
    "age_max": None,
    "age_basis": None,
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
    "verify_notes": "2026-11-05: published from a reader's app photograph, note and GPS fix (sighting 15a3b6f1) on Hidde's 2026-10-21 ruling that a good photograph with a GPS fix is not held. Species, location and the grouping of three are the reader's, and the photograph shows three conifers with glaucous blue-green foliage and horizontal tiered branches, consistent with Atlas cedar. No register entry within 100 m and no encyclopaedia article within 300 m; two web searches found no source on the park. Access: the estate is a health-care site (maison de santé), no source states its opening hours, but the cedars stand beside a gravel footpath with a walker on it in the photograph, so the tree is clearly seen from public ground (rule 10); access says so plainly. No girth, height or age.",
    "access": "Seen from a gravel footpath along the lawn in the estate's park, where walkers pass. We found no opening hours for the grounds, so respect any signs at the entrance.",
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
    "intro": "La Tène, the commune at the northern end of Lake Neuchâtel whose name was given to a whole period of Celtic Europe, has one place on our map: a lawn in the park of the Préfargier estate at Marin-Epagnier, where three Atlas cedars stand so close that their crowns have grown into one. A reader walked past them, photographed them from the gravel path and sent us the picture with a single line in French. They are seen from that path, where walkers pass.",
    "meta_description": "Three Atlas cedars at Préfargier in La Tène, canton of Neuchâtel: a reader's photograph, where they stand and how to see them.",
    "hero_tree_id": TID,
    "oldest_tree_id": TID,
    "trees": [tree],
    "question_meta": "Three Atlas cedars grow together at Préfargier, La Tène, canton of Neuchâtel. Where they stand and how to see them.",
    "question_answer": "A reader found three Atlas cedars (Cedrus atlantica) growing together on a lawn in the park of the Préfargier estate at Marin-Epagnier, in La Tène, canton of Neuchâtel. They are visible from a gravel footpath.",
    "question_context": "Everything this page says about the cedars comes from one reader's photograph and note, sent through the app on 5 November 2026 with a GPS fix taken where they stood. No tree register we hold lists them, we found no published survey of the Préfargier park that names them, and we have no girth, height or planting date. The photograph is the evidence. It shows three separate trunks a few metres apart on an open lawn, low limbs that sweep almost to the grass, and blue-green needles held in flat tiers, the look of the Atlas cedar, Cedrus atlantica, a conifer from the Atlas Mountains of Morocco and Algeria that is often grown in European parks. Together the three read as one broad dark pyramid against the woods behind. The park belongs to a health-care institution, the maison de santé de Préfargier, and we found no published opening hours for its grounds. The cedars stand beside a gravel footpath, and the reader's photograph shows another walker on it. If you know when they were planted, or have put a tape round one of the trunks, tell us on the page and it goes into this answer.",
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
