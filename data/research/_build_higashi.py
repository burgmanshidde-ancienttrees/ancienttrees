import json

trees = json.load(open('data/research/higashihiroshima-verified.json'))
by_id = {t['id']: t for t in trees}

order = ['hgh_005','hgh_001','hgh_002','hgh_003','hgh_004',
         'hgh_010','hgh_011','hgh_012','hgh_013','hgh_014',
         'hgh_015','hgh_016','hgh_017',
         'hgh_006','hgh_007','hgh_008','hgh_009']

assert set(order) == set(by_id.keys()), set(order) ^ set(by_id.keys())

out_trees = []
for tid in order:
    t = dict(by_id[tid])
    t['photo'] = {"url": None, "license": None, "attribution": None, "status": "missing"}
    t['photos'] = []
    out_trees.append(t)

city = {
    "city": "Higashi-Hiroshima",
    "country": "Japan",
    "status": "published",
    "intro": "Higashi-Hiroshima's seventeen registered giants are spread the way the city itself is: thirty kilometres from sake breweries to coast. A cedar pair shares a mountain-summit temple above Saijo. Five trees crowd one grove that Hiroshima Prefecture declared a natural monument in 1987, above Toyosaka. A lone ginkgo stands two minutes from a train platform at Akitsu. This is not one walk, it is several, and almost none of it has been written about in English before.",
    "meta_description": "Higashi-Hiroshima's oldest tree is a 400-year ginkgo by Renko-ji, two minutes from Akitsu station. That, a mountain cedar pair, and fourteen more.",
    "question_meta": "Higashi-Hiroshima's oldest tree is the Great Ginkgo of Renko-ji, roughly 400 years old and 5.2 metres round, two minutes from Akitsu Station.",
    "question_answer": "The oldest tree in Higashi-Hiroshima is the Great Ginkgo of Renko-ji, estimated at roughly 400 years old and measured at 5.2 to 5.3 metres round, standing in the temple precinct in Akitsu, on the city's southern coast. It is free to visit and a two-minute walk from Akitsu Station on the JR Kure Line.",
    "question_context": "The age is an estimate rather than a measurement, the same honest gap that applies to almost every giant ginkgo in Japan: no register anywhere carries a planting date for this tree, so the figure comes from its size and from local accounts that put it at around four centuries. Its closest rival for the title is the Meoto-sugi, a named husband-and-wife cedar pair on the summit of Mount Fukujo-ji above Saijo's sake breweries, dated only as \"over three hundred years\" in the same 1988 national giant-tree survey that measured the ginkgo. Both readings rest on girth rather than a ring count. What sets the ginkgo apart is how easy it is to reach: most of Higashi-Hiroshima's seventeen registered giants stand in shrine groves reachable only by car, spread across the hills above Toyosaka and Fukutomi, while this one is a short walk from a JR platform on the coast at Akitsu. See all seventeen remarkable trees of Higashi-Hiroshima.",
    "faq": [
        {
            "q": "What is the oldest tree in Higashi-Hiroshima?",
            "a": "The Great Ginkgo of Renko-ji, in Akitsu, estimated at roughly 400 years and 5.2 to 5.3 metres round. Free to visit, a two-minute walk from Akitsu Station."
        },
        {
            "q": "Where is the biggest cluster of old trees?",
            "a": "Uneyama Shrine in Toyosaka-cho, where five separate giants, an oak, a cedar, an umbrella pine, a cypress and a fir, share one grove that Hiroshima Prefecture designated a natural monument in 1987."
        },
        {
            "q": "When should I visit for autumn colour?",
            "a": "November, when the Great Ginkgo of Renko-ji turns gold and the Kurogane Holly at Fukujo-ji reddens with berries."
        },
        {
            "q": "Do I need a car?",
            "a": "For most of these, yes. Only the Renko-ji ginkgo is reachable by train; the rest stand in shrine and temple grounds across Saijo, Toyosaka and Fukutomi that only a road reaches."
        }
    ],
    "hero_tree_id": "hgh_005",
    "oldest_tree_id": "hgh_005",
    "trees": out_trees
}

json.dump(city, open('data/cities/higashi-hiroshima.json', 'w'), ensure_ascii=False, indent=2)
open('data/cities/higashi-hiroshima.json', 'a').write('\n')
print('written', len(out_trees), 'trees')
