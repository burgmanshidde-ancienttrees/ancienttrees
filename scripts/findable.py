"""Can somebody standing there find this tree? One answer, read by every check.

Hidde, 2026-10-01: "zo min mogelijk bomen met geen foto en geen exacte pin",
the Google-recovery rule that keeps a tree with neither out of the index and
refuses a new one. Widened by him on 2026-10-04 ("voer dat door"), sitewide,
after being shown that the question underneath it is findability, not
precision: a pin on a SMALL NAMED SITE plus a line saying which tree it is
finds the trunk as surely as a surveyed coordinate. The Three Sisters at the
gate of Magnolia Cemetery are the worked case: two oaks at one entrance,
unmissable once you are standing there, refused by the old rule because the
pin was not "confirmed".

So a tree is findable when it has ANY of:
  1. a usable photograph (not held),
  2. location_precision "confirmed",
  3. location_site {"name": ..., "radius_m": <= SITE_MAX_M} AND a
     how_to_recognise line.
A site is a place you take in at one glance: a churchyard, a cemetery gate, a
square, a cloister, a courtyard, a library lawn. A park, a wood, a campus or a
garden you walk through is not, whatever radius somebody writes down; that is
the verify pass's judgement and BRIEF_RESEARCH.md says so.

preflight.py (refusing a new tree) and thin_pages.py (noindex) both import
this, so the two cannot drift apart the way two copies of one rule always have
here. Removing or loosening it needs Hidde.
"""

SITE_MAX_M = 50

# ADDING is not INDEXING (Hidde, 2026-10-05: "the night runs should keep on
# adding trees", "we just should be considerate about what to add to google",
# "the google situation is grim anyway right - why not make the product
# better?"). Since 2026-10-01 a tree that is not findable was refused outright,
# and with the shelf dry that left the night runs nothing to add: 20 of 41 runs
# from 09-30 to 10-05 shipped no tree with 110 of 120 minutes unspent. A tree on
# the map serves the product whether or not Google sees its page, and
# thin_pages.py already keeps every tree that is not findable out of the index,
# recomputed every deploy, so it enters Google the day it gains a photo or a
# pin. So preflight no longer refuses it. True brings the refusal back.
ADD_NEEDS_FINDABLE = False


def has_photo(tree):
    ph = tree.get("photo") or {}
    return bool(ph.get("url")) and ph.get("status") != "held"


def on_a_small_site(tree):
    site = tree.get("location_site") or {}
    try:
        r = float(site.get("radius_m"))
    except (TypeError, ValueError):
        return False
    return bool((site.get("name") or "").strip()) and 0 < r <= SITE_MAX_M \
        and bool((tree.get("how_to_recognise") or "").strip())


def findable(tree):
    return has_photo(tree) or tree.get("location_precision") == "confirmed" \
        or on_a_small_site(tree)


# INDEXED again by being FINISHED, on top of a photograph (2026-10-09, Hidde:
# "do this", on being shown that INDEX_NEEDS_PHOTO had taken 2,311 of the 2,822
# tree pages in the proven cities out of Google, pages Google had already been
# showing). A tree page in a proven city (data/depth-roster-frozen.json) returns
# to the index when the enrichment pass has finished it: the tree is findable
# on the ground AND the page carries a measurement, the official register or
# authority record, and concrete visiting facts. That is Google's own
# description of a page worth indexing ("a substantial, complete description",
# "beyond the obvious") and it is what distinguishes the page from the
# AI-drafted-story-alone shape that was demoted. scripts/enrich.py says which
# of the three a tree still lacks (its gaps()); thin_pages.py reads this.
# Outside the proven cities a photograph is still the only way in.
ENRICHED_NEEDS = ("register", "measurement", "access")


def enriched(tree, gaps):
    """gaps: the tree's open gaps from scripts/enrich.py gaps()."""
    return findable(tree) and not (set(ENRICHED_NEEDS) & set(gaps))


# NO NEW TREE UNLESS ITS PAGE IS RICH OR A READER ADDED IT (Hidde, 2026-10-09:
# "Let's not add any more trees unless rich page and or added by user right?").
# Rich is enriched() above, the same rule that returns a page to the index, so
# a tree that may ship is by construction a tree Google may see. A reader's
# tree is the exception because a person who stood there is the validation
# this whole project is walking toward (CLAUDE.md, "What validates a tree");
# it still meets the ordinary bar, and thin_pages.py decides its indexing.
# Trees live that day are in data/rich-baseline.json and stay (hard rule 3).
# preflight's check_a_new_tree_is_rich_or_a_readers() reads this; False
# switches it off and needs Hidde.
ADD_NEEDS_RICH = True


def reader_added(tree):
    """A tree that came through a reader: a sighting id on it or on its
    photograph, or a contributor's photograph (source + contributor_user_id,
    the pair sightings_publish.py writes)."""
    import json as _json
    blob = _json.dumps(tree)
    return '"sighting_id"' in blob or '"contributor_user_id"' in blob
