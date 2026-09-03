import json

p = "data/research/ofunato-verified.json"
d = json.load(open(p))
t = d[0]
t["story"] = (
    "The 2011 tsunami put this poplar half under seawater and it stayed standing. "
    "It is not an old tree, and its age is not the point. The proprietor's mother planted it in the backyard of a shop and home "
    "in Okirai shortly after the Showa Sanriku tsunami of 1933, which makes it about ninety; a local paper reckoned in 2018 that "
    "an ordinary poplar manages around sixty years and that this one had already passed eighty. It came through the Chile "
    "earthquake tsunami of 1960 as well. Around 1992 the neighbours discussed felling it because they were worried about "
    "lightning, and nothing happened, for want of a budget.\n\n"
    "Okirai took the worst tsunami damage anywhere in Sanriku-cho on 11 March 2011 and was very nearly erased. The water rose to "
    "roughly half the tree's 25 metres. Afterwards people began calling it the Do-konjo Poplar, which comes out in English as "
    "something close to gutsy. The better known survivor of this coast, the lone pine at Rikuzentakata, died of the salt and "
    "stands today as a treated replica of itself; this one is simply still alive. When the landowner handed the ground to Ofunato "
    "City he made keeping the tree a condition of the gift, and the city built a public plaza around it, opened in 2018, with "
    "benches and a gazebo. It is a registered site on the national 3.11 memorial route. No source we found names which poplar it "
    "is, so if you know, tell us."
)
t.pop("verify_notes", None)
json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
open(p, "a").write("\n")
print(len(t["story"].split()), "words")
assert "—" not in t["story"] and "–" not in t["story"]
