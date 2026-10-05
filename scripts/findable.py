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
