# Can open data get us to every city in the world?

Measured 2026-07-21, because researching ten trees per city by hand works out at roughly one city a day, which is three months for a hundred cities and decades for the world. The question was whether existing open data can replace the finding, leaving runs to do the writing.

## What was measured

Trees tagged `natural=tree` + `denotation=natural_monument` in OpenStreetMap, counted per city with a bounding box query against the public Overpass API.

| City | Monument-tagged trees |
|---|---|
| Warsaw | 224 |
| Berlin | 90 |
| Vienna | 82 |
| Tokyo | 10 |
| Amsterdam | 4 |

Prague, Paris, London, Rome and New York did not return: the public Overpass instance kept timing out under load, which is a property of the free endpoint, not of the data. Those numbers still need collecting.

Note the wider `denotation` tag is useless on its own: Berlin has 35,848 trees carrying it, because it also covers `avenue` and `urban`, meaning ordinary street trees.

## What it means

**OpenStreetMap is a strong accelerator for part of the world and close to useless for the rest.** Warsaw, Berlin and Vienna are well covered because *Naturdenkmal* and its Polish equivalent are formal legal designations, so there is an official list to map and a mapping culture that does it. Amsterdam returning 4 does not mean Amsterdam has four monumental trees: the Bomenstichting register holds thousands. It means Dutch mappers do not use that tag.

So the honest conclusion is that this **does not** solve world coverage by itself. It solves Central and Eastern Europe cheaply, and leaves everywhere else roughly where it was.

The rest has to come from national registers, one integration at a time: the Netherlands has the Landelijk Register van Monumentale Bomen, Italy the national monumental tree registry (already used for Rome), Poland, France and others have their own. Each is separate work, and there is no universal source. Coverage will stay uneven, and the site should say so rather than imply a uniform map.

## The licence question, which is less of a problem than feared

OSM data is ODbL, and the share-alike clause is real, but it applies to a *Derivative Database*, not to a *Produced Work*. Web pages generated from the data are a Produced Work: they need attribution, which the site already carries for the map tiles, and nothing more. Publishing our own tree database as a database would be the thing that triggers share-alike.

Practical consequences:
- Using OSM to find and place trees, then publishing pages about them, is fine with attribution.
- A paywall on features (routes, offline, the passport) is unaffected, because those are not the database.
- Never publish the tree JSON as a downloadable dataset without checking this properly first.
- This is a reading of the licence by a run, not legal advice. Before anything ships that depends on it, Hidde should be comfortable with it.

## What this suggests architecturally

The bottleneck moves rather than disappears. Even with 224 Warsaw trees handed to us for free, someone still has to write a story for each, and a 150 to 250 word story is the expensive part.

That points at two tiers rather than one, which also answers Hidde's wish to let the ten-per-city limit rise:

- **A data tier.** Every tree we can place from open data: species, location, whatever age the source gives. Cheap, bulk, potentially hundreds per city. Honest about being thin.
- **A story tier.** The ten or so per city that get the full treatment: research, verification against two sources, a written story, a photo. This is what the site is actually good at and what nobody else does.

A city page then leads with the ten that are worth the walk and can show the rest as a map layer underneath. Coverage stops competing with quality, because they stop being the same axis.

## Recommended next steps

1. Finish the survey: get counts for the cities that timed out, and check what the national registers actually offer per country, starting with the Netherlands and Italy where we know registers exist.
2. Decide on the two-tier model before importing anything. It changes the schema, and schema changes get expensive once fifty cities are in.
3. Only then build an import.

Do not start an import on the strength of this document alone. Five cities measured, five that failed, and a licence read by a machine is not a foundation to pour a hundred cities onto.
