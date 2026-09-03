import json

p = "data/research/takayama-verified.json"
d = json.load(open(p))
t = d[0]
t["species"] = "Ginkgo (Ginkgo biloba)"
t["story"] = (
    "When this ginkgo drops its last leaf, Hida expects its first snow the next day. "
    "The town treats it as its own herald of winter. It stands between the main hall and the bell-tower gate of Hida Kokubunji, "
    "roughly ten metres round and 27 to 28 metres tall. Sources put its age between 1,200 and 1,300 years, the temple claiming "
    "the higher figure and the prefecture the lower. By the temple's own account the monk Gyoki planted it in 737, when Hida "
    "Kokubunji was founded by decree of Emperor Shomu.\n\n"
    "The other story attached to it is grimmer. A master carpenter raising a seven-storey pagoda here cut his pillars too short. "
    "His daughter Yaegiku saw that bracket blocks would make up the difference, which corrected the mistake and made the pagoda "
    "famous. Afraid she would tell, he killed her, buried her in the grounds and planted a ginkgo over the grave. The tree hangs "
    "aerial roots that look like breasts, which is why it is called Chichi Icho, the breast ginkgo, and why women have come to it "
    "for milk, an easy birth and a healthy child; stone jizo of a parent and child sit at its base. It is a male tree and has "
    "never borne a single nut, a question the temple is asked so often that the answer is in its FAQ. Typhoons and lightning took "
    "pieces of it through the last century. Public money and local donations have kept the rest."
)
t["best_time"] = {
    "months": [11, 12],
    "kind": "autumn colour",
    "label": "late November into early December, when it goes gold and lets the whole crown go at once",
}
t.pop("verify_notes", None)
json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
open(p, "a").write("\n")
print(len(t["story"].split()), "words")
assert "—" not in t["story"] and "–" not in t["story"]
assert "37" not in t["story"]
