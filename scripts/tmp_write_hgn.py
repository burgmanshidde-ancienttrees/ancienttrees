import json

p = "data/research/higashine-verified.json"
d = json.load(open(p))
t = d[0]
t["story"] = (
    "Japan's largest zelkova grows in a primary school playground. "
    "The children of Higashine Elementary are called keyaki-kko, zelkova children, and are taught that catching three falling "
    "leaves before they touch the ground earns a wish. The tree they chase measures 16 metres round at chest height and 24 at "
    "the roots, and forks into two stems five and a half metres up. Of the three great zelkovas of Japan it is the only Special "
    "Natural Monument, a grade above the other two, and the only one still described as robust rather than ageing; a 1980 "
    "ranking of the country's zelkovas gave it the top sumo rank on the east side, East Yokozuna.\n\n"
    "The playground was the main keep of Odajima Castle, built in 1347, and the tree was already substantial when the walls went "
    "up around it. It had a partner: two zelkovas stood here, the mother tree and the father tree, and the father died in 1885. "
    "A storm took a great north-facing bough in 1902, which is why the crown is thin on that side, and the recorded height has "
    "come down from 35 metres at the 1957 designation to 28 now. The base is hollow, with room for about two tatami mats; people "
    "once crawled through it hoping for a child, though it is fenced off today. On the age the experts split: one assessment put "
    "it over a thousand years, a later one over fifteen hundred, and neither has given way."
)
t["best_time"] = {
    "months": [11],
    "kind": "autumn colour",
    "label": "November, when the leaves come down and the schoolchildren chase them",
}
t.pop("verify_notes", None)
json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
open(p, "a").write("\n")
print(len(t["story"].split()), "words")
assert "—" not in t["story"] and "–" not in t["story"]
