#!/usr/bin/env python3
"""Post-build QA over site/dist. Runs on every deploy, after the Astro build
(site/, npx astro build; the Python renderer this once followed, build_site.py,
was deleted 2026-08-09 once the Astro cutover ran a clean deploy cycle).

The Astro build validates what it is ABOUT to write (contracts, lengths,
script hygiene, as build-time errors thrown from site/src/lib's ratchet
checks); this script validates what actually landed on disk, the way a
browser will meet it. The split matters: build checks catch what the
generator knows about, this catches what it forgot it was generating.

Checks, all deterministic, no network:
  1. Internal links resolve to a real file (GitHub Pages resolution rules:
     exact file, +.html, or /index.html).
  2. Internal image/script/css sources resolve the same way.
  3. No em dash anywhere in rendered text (hard rule 3).
  4. No banned filler words in rendered text (CLAUDE.md Step 3).
  5. img src urls are http(s) or site-relative, never a Wikimedia File: page.

Exit 1 on any failure, so CI fails the deploy. Run: python3 scripts/qa.py
"""
import argparse
import json
import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"

# Shared with the app since 2026-08-25: scripts/copy_rules.py is read by
# copycheck.py as well, so a word banned here is banned in the app's strings in
# the same commit. It used to live only in this file, which only ever reads
# site/dist.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from copy_rules import BANNED_WORDS  # noqa: E402

# Our own rules are not the reader's business. Hidde, 2026-08-08, on finding the
# parks index explaining its own publish gate to visitors: "Why are you saying
# this logic? That is our logic back to the end user. They just want nice data,
# nice parks with trees. They don't care about our specific rules."
#
# This is the second time the same disease shipped, after the builder-speak rule
# that already bans narrating construction, so it is a check now rather than a
# third note. Three shapes, all of which were live:
#   - the publish gate as copy ("a park earns a page once we have mapped five")
#   - the shortfall as copy ("23 parks hold three or four, not yet enough")
#   - the roadmap as copy ("more species appear as new cities join the map")
# What the reader wants is what IS here and why it is worth their afternoon.
# A count is fine ("9 trees, Madrid"); the threshold behind the count is not.
BUSINESS_RULE_PHRASES = [
    "earns a page", "earn a page", "once we have mapped", "the site has mapped",
    "not yet enough", "enough for a page", "a page of their own",
    "a page of its own", "have enough mapped", "appear as new cities join",
    "qualifies for a page", "publish gate", "we only publish",
]



# Product-copy surfaces (no editorial stories on them) may not make absolute
# promises: the paywall rule bans forever-claims, and "Nothing else, ever"
# still shipped twice before this gate existed. Story prose is exempt because
# "the tree never recovered" is legitimate narrative.
PROMISE_PAGES = {"app.html", "account.html", "contribute.html", "privacy.html",
                 "explore.html", "index.html", "cities.html"}
PROMISE_PATTERNS = [", ever", " forever", "we will never", "we will always",
                    "nothing else, ever", "no ads, ever", "always free"]


class PageScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []      # href/src values
        self.img_srcs = []
        self.text_parts = []
        self._skip_depth = 0  # inside script/style

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip_depth += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script") and a.get("src"):
            (self.img_srcs if tag == "img" else self.links).append(a["src"])
        if tag == "link" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            self.text_parts.append(data)


def resolves(target: Path) -> bool:
    """GitHub Pages resolution: exact file, file + .html, or dir/index.html."""
    if target.is_file():
        return True
    if target.with_suffix(target.suffix + ".html").is_file():
        return True
    if (target / "index.html").is_file():
        return True
    return False


# The only check here that looks at the repository rather than at site/dist,
# and it earns the exception the way every other ratchet check did: the same
# error shipped twice.
#
# A workflow prompt that declares the current phase goes stale invisibly,
# because the corpus gets edited in session and the YAML does not. On
# 2026-08-11 CITY_QUEUE.md was written to kill six competing city orders and
# named "the order embedded in nightly.yml" as one of them; that order was
# still sitting in the prompt, still being executed, on 2026-08-12, six days
# after the phase it encoded had been replaced. Two copies of a course means
# the one nobody edits wins.
#
# So: strategy lives in CLAUDE.md and CITY_QUEUE.md. A workflow prompt may
# carry mechanics (how to claim a pass, which build command matches the tool
# allowlist, what this runner's proxy blocks) and must not carry a phase, a
# priority order or a city work list. The patterns below are the SHAPE of that
# error rather than a word list, so an honest mechanic sentence passes.
STRATEGY_IN_WORKFLOW = [
    "is the current phase", "the current phase is", "the job for the coming runs",
    "phase-1 city", "phase 1 city", "stays closed until", "stay closed until",
    "work stops: no new", "in this order, and photos",
]


def check_no_strategy_in_workflows():
    out = []
    wf = Path(__file__).resolve().parent.parent / ".github" / "workflows"
    if not wf.is_dir():
        return out
    for path in sorted(wf.glob("*.yml")):
        low = path.read_text(encoding="utf-8").lower()
        for pat in STRATEGY_IN_WORKFLOW:
            if pat in low:
                out.append(
                    f".github/workflows/{path.name}: declares strategy ({pat!r}). "
                    "A phase or city order in a workflow prompt goes stale invisibly; "
                    "put it in CLAUDE.md or CITY_QUEUE.md and point at it."
                )
    return out


# The eighth ratchet check, and the same disease as the one above: a second
# copy of something that already has one place to live. data/city-list.json
# carried rank/queue/tier from an older scheme while CITY_QUEUE.md carried the
# real order, and they disagreed hard (Porto 62 against 2, Rome 4 against 12).
# CLAUDE.md Step 0 tells every run to read city-list.json first, so the stale
# order was the one being obeyed. Hidde, 2026-08-12: "kunnen we 1 wachtrij /
# city order maken". The json is inventory now; the order lives in CITY_QUEUE.md
# and is regenerated by scripts/city_queue.py.
def check_auth_corpus_agreement():
    """AUTH_ENABLED and CLAUDE.md's hard rule 1 must tell the same story.

    The mechanism the 2026-08-14 fresh-eyes review demanded after the third
    hard-list exception shipped with stale corpus text: accounts opened in
    production while CLAUDE.md still said "No accounts, logins". A flag and a
    rule that disagree mean either the site or the corpus is lying, and both
    are one commit away from being read as truth by the next run."""
    root = Path(__file__).resolve().parent.parent
    try:
        cfg = (root / "site" / "src" / "lib" / "site-config.ts").read_text(encoding="utf-8")
        corpus = (root / "CLAUDE.md").read_text(encoding="utf-8")
    except OSError as e:
        return [f"auth-consistency check could not read its inputs: {e}"]
    auth_on = "AUTH_ENABLED = true" in cfg
    rule_says_open = "Accounts: OPENED" in corpus
    if auth_on and not rule_says_open:
        return ["site-config.ts has AUTH_ENABLED = true but CLAUDE.md hard rule 1 "
                "does not say accounts are open. Update the rule text (and "
                "DECISIONS.md) in the same change that flips the flag."]
    if not auth_on and rule_says_open:
        return ["CLAUDE.md hard rule 1 says accounts are open but AUTH_ENABLED "
                "is false. One of the two is stale."]
    return []


def check_one_city_order():
    import json as _json
    root = Path(__file__).resolve().parent.parent
    out = []
    path = root / "data" / "city-list.json"
    if path.exists():
        d = _json.loads(path.read_text(encoding="utf-8"))
        rows = d if isinstance(d, list) else d.get("cities", [])
        bad = sorted({k for r in rows if isinstance(r, dict)
                      for k in ("rank", "queue", "tier") if k in r})
        if bad:
            out.append(f"data/city-list.json: carries ordering field(s) {', '.join(bad)}; "
                       "it is generated inventory. Run python3 scripts/city_queue.py")
    # And the rendering must match its source. CITY_QUEUE.md is written from
    # data/city-queue.json; a row edited by hand in the markdown is a second
    # source again, silently, until the next regeneration wipes it.
    src, md = root / "data" / "city-queue.json", root / "CITY_QUEUE.md"
    if src.exists() and md.exists():
        cities = _json.loads(src.read_text(encoding="utf-8"))["cities"]
        want = {c["rank"]: c["city"] for c in cities if c.get("rank")}
        got = {}
        for line in md.read_text(encoding="utf-8").split("\n"):
            m = re.match(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|", line)
            if m:
                got[int(m.group(1))] = m.group(2)
        if got and got != want:
            diff = sorted(set(want.items()) ^ set(got.items()))[:3]
            out.append("CITY_QUEUE.md's table disagrees with data/city-queue.json "
                       f"(e.g. {diff}); the json is the source. "
                       "Run python3 scripts/city_queue.py")
    return out


# A sitemap whose every URL claims to have changed today tells Google nothing,
# and Google discounts lastmod entirely once it proves unreliable. Ours did
# exactly that on every build until 2026-08-13, which is a plausible part of why
# 349 URLs sat at "Discovered - currently not indexed": found, never crawled.
# The fix dates each page from the commit that last touched its source, so this
# check is simply that the dates vary. One distinct date across a thousand pages
# means the git lookup silently fell back (a shallow clone has no history), and
# the deploy would ship the old bug without anyone noticing.
def check_photo_orientation():
    """A photograph we host ourselves must be upright in its PIXELS, with no
    EXIF orientation flag left telling the browser to turn it again.

    Hidde, 2026-08-21, twice in two weeks: "je hebt alle fotos weer 90 graden
    gedraaid erin gezet ... zorg dat het niet nog een keer gebeurt." Both times
    the cause was the same and it is invisible on the desktop: a phone writes
    the picture sideways plus an orientation tag, a rotate tool turns the pixels
    and leaves the tag behind, and the browser then applies the tag on top and
    the tree lies on its side. Preview, Finder and this repo's own image reader
    all honour the tag, so the file looks right everywhere except the one place
    that matters.

    The fix is to rotate the pixels and set the tag to 1, and this is the check
    that proves it stayed done. Only files we serve ourselves are checkable:
    Wikimedia and iNaturalist deliver their thumbnails already upright.
    """
    out = []
    root = Path(__file__).resolve().parent.parent
    photos = root / "site" / "public" / "photos"
    if not photos.is_dir():
        return out
    for f in sorted(photos.glob("*.jpg")) + sorted(photos.glob("*.jpeg")):
        d = f.read_bytes()
        i = d.find(b"Exif\x00\x00")
        if i < 0:
            continue
        tiff = i + 6
        be = d[tiff:tiff + 2] == b"MM"
        end = ">" if be else "<"
        try:
            ifd = tiff + struct.unpack(end + "I", d[tiff + 4:tiff + 8])[0]
            n = struct.unpack(end + "H", d[ifd:ifd + 2])[0]
        except Exception:
            continue
        for k in range(n):
            e = ifd + 2 + k * 12
            try:
                tag = struct.unpack(end + "H", d[e:e + 2])[0]
            except Exception:
                break
            if tag == 0x0112:
                val = struct.unpack(end + "H", d[e + 8:e + 10])[0]
                if val != 1:
                    out.append(
                        "%s carries EXIF orientation %d, so a browser rotates it "
                        "again on top of its pixels. Rotate the pixels upright and "
                        "set the tag to 1." % (f.name, val))
                break
    return out


def check_photo_resolution():
    """A photograph must have the pixels for the box we paint it in.

    Hidde spotted soft thumbnails three times on 2026-08-21 (the country
    mosaic, the species shelf, the map sidebar) and asked for a fix he would
    not have to spot again. The cause is never the markup: a source file can
    simply be smaller than the card. So scripts/photo_res.py measures every
    photograph once and stores width/height beside the url, the homepage
    pickers refuse anything under MIN_CARD for a card, and this check is the
    ratchet that keeps both true.

    It fails on the MISTAKE, never on the gap: a city whose hero is soft while
    a bigger photograph sits in the same city file is a choice we got wrong and
    can fix in one edit. A city whose only photograph is small is an honest gap,
    and blocking a deploy over it would be exactly the kind of gate the mandate
    warns about. The second failure is the data going stale (run photo_res.py;
    the digest runs it daily).
    """
    MIN_CARD, MIN_HERO = 540, 960
    out = []
    root = Path(__file__).resolve().parent.parent
    total = unmeasured = 0
    small_heroes = []
    soft = 0
    for path in sorted((root / "data" / "cities").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        hero_id = doc.get("hero_tree_id")
        for t in doc.get("trees", []):
            p = t.get("photo") or {}
            if not p.get("url"):
                continue
            total += 1
            w = p.get("width") or 0
            if not w:
                unmeasured += 1
            elif w < MIN_CARD:
                soft += 1
        hero = next((t for t in doc.get("trees", [])
                     if hero_id and t.get("id") == hero_id), None)
        hero_w = ((hero or {}).get("photo") or {}).get("width") or 0
        if hero and hero_w and hero_w < MIN_CARD:
            better = max((((t.get("photo") or {}).get("width") or 0)
                          for t in doc.get("trees", [])), default=0)
            if better >= MIN_CARD:
                small_heroes.append("%s: hero %s is %dpx while a %dpx photo sits "
                                    "in the same city" % (doc["city"], hero["name"],
                                                          hero_w, better))
    if small_heroes:
        out.append("%d city hero photo(s) soft while a bigger one is available: %s"
                   % (len(small_heroes), "; ".join(small_heroes[:4])))
    if total and unmeasured > max(10, total // 20):
        out.append("%d of %d photographs have no measured width; run "
                   "`python3 scripts/photo_res.py` (the digest runs it daily)"
                   % (unmeasured, total))
    return out


def check_save_flow_integrity():
    """Two checks born of 2026-08-14's bugs, per the ratchet.

    (1) A modal dialog knocked out of the top layer: .signin-dialog carried
    position:relative, which overrides the UA's position:fixed and parks the
    dialog at the top of the document. CI cannot click, but it can refuse the
    CSS that caused it. (2) A page that renders save hearts without the
    sign-in dialog and its scripts would make the first-save funnel a silent
    no-op; every page with a heart must carry the dialog."""
    out = []
    root = Path(__file__).resolve().parent.parent
    css = (root / "site" / "public" / "assets" / "style.css").read_text(encoding="utf-8")
    m = re.search(r"\.signin-dialog\s*\{([^}]*)\}", css)
    if m and "position:" in m.group(1):
        out.append("style.css: .signin-dialog sets its own position, which knocks a "
                   "modal dialog out of the browser's fixed top-layer placement "
                   "(the 2026-08-14 dialog-at-top-of-page bug)")
    hearts_no_dialog = []
    gated_no_dialog = []
    for page in sorted(DIST.rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        if 'save-btn' in html and 'id="signin-dialog"' not in html:
            hearts_no_dialog.append(str(page.relative_to(DIST)))
        # Feedback is account-gated since 2026-08-21: a worth-it control or
        # the contribute form without the dialog would open nothing on tap,
        # which is the same silent no-op the hearts check exists for.
        if (('worthit-btn' in html or 'id="suggest"' in html)
                and 'id="signin-dialog"' not in html):
            gated_no_dialog.append(str(page.relative_to(DIST)))
    if hearts_no_dialog:
        out.append("%d page(s) render save hearts without the sign-in dialog "
                   "(first-save funnel is a silent no-op there), e.g. %s"
                   % (len(hearts_no_dialog), ", ".join(hearts_no_dialog[:5])))
    if gated_no_dialog:
        out.append("%d page(s) render gated feedback controls (worth-it or the "
                   "contribute form) without the sign-in dialog, e.g. %s"
                   % (len(gated_no_dialog), ", ".join(gated_no_dialog[:5])))
    return out


def check_no_owner_name():
    """The thirteenth ratchet check, from 2026-08-24.

    Hidde: "zet mijn naam er nooit onder altijd die van het bedrijf." It is the
    same rule the blueprint's P5 has carried since 2026-07-28, where the
    site-level entity is the Organization "Ancient Trees" and never a named
    Person, and it is now the second time he has had to say it, which is what
    turns a rule into a check here.

    Nothing rendered has ever carried it: the matches in the repo are all in
    source comments, which is fine and is where the reasoning belongs. This
    exists so that stays true the day somebody writes an about line, a terms
    page or a press quote in a hurry. The reader's own name is a separate rule
    with its own history and is not this check's business.
    """
    out = []
    hits = []
    pattern = re.compile(r"\bHidde\b|\bBurgmans\b", re.I)
    for page in sorted(DIST.rglob("*.html")):
        scan = PageScan()
        scan.feed(page.read_text(encoding="utf-8"))
        if pattern.search(" ".join(scan.text_parts)):
            hits.append(str(page.relative_to(DIST)))
    if hits:
        out.append("%d page(s) render the owner's personal name, which is never "
                   "published: the site's entity is the organisation Ancient "
                   "Trees (blueprint P5). %s"
                   % (len(hits), ", ".join(hits[:5])))
    return out


def check_one_owner_per_event():
    """The twelfth ratchet check, from 2026-08-20.

    Three funnel events were being counted twice, because two click listeners
    each claimed them: the href-matching listener in Base.astro fired
    "app-cta" for any /app link while those same links carried
    data-ev="app-cta", and at.track() calls inside AppModal and the tree
    actions repeated events the data-ev listener already had. Every number in
    DATA.md for app-cta, directions and walks-app before that date is roughly
    double the truth, and nothing could see it.

    So: an event name is either an attribute or a literal at.track() call,
    never both. This catches the duplication that has a name on both sides;
    it cannot catch a listener that matches on something other than the event
    name (the href branch), which is why that branch now tracks exactly the
    one event that has no attribute to hang off."""
    root = Path(__file__).resolve().parent.parent
    src = root / "site" / "src"
    attrs, calls = {}, {}
    for f in sorted(src.rglob("*")):
        if f.suffix not in (".astro", ".ts", ".js") or not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        rel = str(f.relative_to(root))
        for name in re.findall(r'data-ev=["\']([^"\']+)["\']', text):
            attrs.setdefault(name, set()).add(rel)
        # Literal single-argument calls only. at.track('search-' + ctx) builds
        # its name at runtime and has no attribute anywhere to collide with.
        for name in re.findall(r"at\.track\(\s*['\"]([^'\"]+)['\"]\s*[,)]", text):
            calls.setdefault(name, set()).add(rel)
    out = []
    for name in sorted(set(attrs) & set(calls)):
        out.append("event %r is counted twice: data-ev in %s and an at.track() "
                   "call in %s. One owner per event (2026-08-20 double-count)"
                   % (name, ", ".join(sorted(attrs[name])), ", ".join(sorted(calls[name]))))
    return out


def check_one_tree_card():
    """The eleventh ratchet check, from 2026-08-18.

    Hidde asked for one component so that "als we in de toekomst daar
    verbeteringen doorvoeren zorgen dat dat overal gebeurt consistent". Before
    it, a tree rendered two ways: the city page's .tree-card and a smaller
    .entry with a 96px thumb on the park, species and collection pages, and
    every improvement to one missed the other. A component only holds the line
    while nobody hand-rolls a second card next to it, which is exactly what
    happened last time (the 2026-08-14 audit found the same with hearts).

    So: no built page may ship the retired .entry-thumb/.entry-body markup for
    a tree. Cheap, and it fails the moment someone copies the old pattern back
    in rather than adding a prop to TreeCard.astro."""
    out = []
    offenders = []
    for page in sorted(DIST.rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        if "entry-thumb" in html or "entry-body" in html:
            offenders.append(str(page.relative_to(DIST)))
    if offenders:
        out.append("%d page(s) render the retired .entry tree markup instead of "
                   "TreeCard.astro, which is how the two cards drifted apart in the "
                   "first place: %s" % (len(offenders), ", ".join(offenders[:5])))
    return out


def check_species_face_is_chosen():
    """The twelfth ratchet check, from 2026-08-23. This class of error has now
    appeared on two separate days, which is what turns a lesson into a check.

    On 2026-08-21 Hidde said the London Plane and Ginkgo cards were showing the
    wrong pictures, and `face_tree_id` was added to the species schema so a
    person could pin one. It was wired into the homepage shelves by hand and
    nowhere else. Two days later he opened /species and got the Horse Chestnut
    card fronted by a close-up of red survey paint around a wound on a trunk,
    because that page still took the first photograph it happened to find.

    No ranking can catch that. Only a person can see that a picture is of bark
    rather than of a tree, and the pin is how they say so, which makes a page
    that ignores the pin worse than one with no ranking at all.

    So: any page that reads the species collection and draws a card must go
    through speciesFace() or consult face_tree_id itself. Source-level, because
    the built HTML cannot tell you how a url was chosen."""
    out = []
    root = Path(__file__).resolve().parent.parent
    pages = root / "site" / "src" / "pages"
    if not pages.exists():
        return out
    for f in sorted(pages.rglob("*.astro")):
        src = f.read_text(encoding="utf-8")
        draws_species_card = ("speciesCards" in src or "speciesShelf" in src
                              or "pinnedSpeciesPhoto" in src)
        if not draws_species_card:
            continue
        if "speciesFace(" in src or "face_tree_id" in src:
            continue
        out.append("%s draws a species card without speciesFace() or face_tree_id, "
                   "so a person cannot override what it picks. That is how a bark "
                   "close-up came to front the Horse Chestnut page."
                   % f.relative_to(root))
    return out


def check_faces_travel_to_the_app():
    """The thirteenth ratchet check, from 2026-08-25.

    Hidde, on a species card fronted by a photograph of a fountain: "do you save
    the thumbnails between app and web and make sure we use the same ones?" We
    did not. The website ranks the photographs in a set and honours a pin set by
    hand (hero_tree_id, face_tree_id); the app took the FIRST tree it found with
    a picture, because /api/browse.json carried no answer for it to read. So one
    city could wear two faces depending on which screen you were holding, and a
    pin fixed exactly one of them.

    This is the same class of error as the twelfth check above, one surface
    further out: there, a page ignored the pin; here, a whole platform did. The
    fix is that the choice travels as DATA (a tree id in the feed) rather than as
    a rule implemented twice, so this check guards both halves of that.

    Half one: every facet in the feed names its face, and every face it names is
    a live tree with a usable photograph.

    Half two: no Swift screen picks a card face by taking the first tree with a
    photograph. That line is what this whole exercise was about, and it reads so
    naturally that it will be typed again."""
    out = []
    root = Path(__file__).resolve().parent.parent
    browse_path = DIST / "api" / "browse.json"
    trees_path = DIST / "api" / "trees.json"
    if browse_path.exists() and trees_path.exists():
        browse = json.loads(browse_path.read_text(encoding="utf-8"))
        feed = json.loads(trees_path.read_text(encoding="utf-8"))
        trees = feed["trees"] if isinstance(feed, dict) else feed
        photographed = {t["id"] for t in trees if t.get("photo")}
        live = {t["id"] for t in trees}
        # Which trees each facet holds, so "no face" can be told apart from "no
        # photograph anywhere in this facet", which is an honest null.
        members = {}
        for kind in ("collections", "parks", "species"):
            for f in browse.get(kind, []):
                members[(kind, f.get("slug") or f.get("name"))] = set(f.get("trees") or [])
        by_city, by_country = {}, {}
        for t in trees:
            by_city.setdefault(t.get("city_slug"), set()).add(t["id"])
            by_country.setdefault(t.get("country"), set()).add(t["id"])
        for f in browse.get("cities", []):
            members[("cities", f.get("slug"))] = by_city.get(f.get("slug"), set())
        for f in browse.get("countries", []):
            members[("countries", f.get("slug"))] = by_country.get(f.get("name"), set())

        for kind in ("cities", "countries", "species", "parks", "collections"):
            facets = browse.get(kind)
            if facets is None:
                out.append("/api/browse.json carries no %s facet, so the app has "
                           "nothing to read and goes back to guessing" % kind)
                continue
            for f in facets:
                key = f.get("slug") or f.get("name")
                if "face" not in f:
                    out.append("%s facet %s names no face, so the app picks its own "
                               "picture and the two surfaces drift" % (kind, key))
                    continue
                face = f.get("face")
                mine = members.get((kind, key), set())
                if face is None:
                    if mine & photographed:
                        out.append("%s facet %s has a photographed tree and still "
                                   "names no face" % (kind, key))
                elif face not in live:
                    out.append("%s facet %s names face %s, which is not a live tree"
                               % (kind, key, face))
                elif face not in photographed:
                    out.append("%s facet %s names face %s, which has no usable "
                               "photograph" % (kind, key, face))

    ios = root / "ios"
    if ios.exists():
        for f in sorted(ios.rglob("*.swift")):
            src = f.read_text(encoding="utf-8")
            for line_no, line in enumerate(src.splitlines(), 1):
                if "first { $0.photo != nil }" in line or "first { $0.photo != nil &&" in line:
                    out.append("%s:%d picks a card face by taking the first tree with "
                               "a photograph. The face is decided on the server and "
                               "travels in the feed; read catalogue.face(...)"
                               % (f.relative_to(root), line_no))
    return out


def check_sheet_integrity():
    """The tenth ratchet check, from 2026-08-18.

    The phone city page is a Google Maps bottom sheet, and it is three parts
    that only work together: the CSS that makes .panel a fixed, transformed
    sheet, the markup that gives it a grab handle and an inner scroller, and
    the script that sets the transform. On 2026-08-17 the CSS shipped alone.
    With no script the sheet sits at translateY(0) covering the map, and with
    no .sheet-body the overflow:hidden lands on the panel itself, so 114 city
    pages in two languages served no map AND could not be scrolled. Nothing
    failed: the build passed, the smoke test passed, the deploy went green.

    This is the same shape as the hearts-need-the-dialog check above: a set of
    parts that must never separate. So it is enforced the same way, against the
    built pages rather than the templates, because what ships is what matters.

    Widened on 2026-08-18 to every page built on the .split layout, which is
    now /explore as well as the city pages (Hidde: "kunnen we die paginas
    consistent met elkaar houden"). That is the point of keying on the layout
    rather than on a page name: a future page that adopts the split gets the
    same sheet or it does not ship.
    """
    out = []
    root = Path(__file__).resolve().parent.parent
    css = (root / "site" / "public" / "assets" / "style.css").read_text(encoding="utf-8")
    if "[data-detent=" not in css:
        return out  # the sheet layout is not in the stylesheet; nothing to pair
    need = (('id="sheet"', "the id the script looks for"),
            ("sheet-grab", "the drag handle the peek is measured from"),
            ("sheet-body", "the inner scroller, without which the list cannot scroll"),
            ("atSheetFocus", "the sheet script itself"))
    broken = []
    for page in sorted(DIST.rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        # The layout is the trigger, not the page: any page built on .split
        # owes the sheet its parts. panel-head is that layout's own marker and,
        # unlike a class attribute, cannot be missed by an attribute reorder.
        if "panel-head" not in html and 'class="split"' not in html:
            continue
        missing = [why for token, why in need if token not in html]
        if missing:
            broken.append("%s (missing %s)" % (page.relative_to(DIST), "; ".join(missing)))
    if broken:
        out.append("%d page(s) carry the bottom-sheet CSS without all of its parts, "
                   "which serves a city page with the map hidden and the list unscrollable: %s"
                   % (len(broken), ", ".join(broken[:5])))
    return out


# The ninth ratchet check, and the class has now failed twice, which is the
# threshold. On 2026-08-11 a run rendered a submitter's name on a tree page and
# Hidde ruled it out absolutely, on any channel: "privacy technisch echt een no
# go... ookal is het via formulier niet meer doen nooit". On 2026-08-16 the
# Spanish tree template was found still PROMISING it, "y aparecerá en esta
# página con tu nombre", on every photo-less Spanish tree page, while
# /contribute said in English that we never publish a name. The site was
# contradicting itself and offering something we must not deliver.
#
# A promise is worse than the act: it invites people to send a name expecting
# publication. So this greps the built pages rather than the templates, because
# what ships is what matters and a new template would have to be remembered.
# Photo credits are deliberately not caught: "Photo: X (CC BY)" names a
# photographer whose licence obliges the credit, which is a different thing.
NAME_PROMISES = (
    "con tu nombre",
    "con su nombre",
    "with your name",
    "met je naam",
    "met jouw naam",
    "credited by name",
    "we will credit you",
)


def check_no_name_promise(pages):
    out = []
    for page in pages:
        try:
            low = page.read_text(encoding="utf-8").lower()
        except OSError:
            continue
        for pat in NAME_PROMISES:
            if pat in low:
                out.append(
                    f"{page.relative_to(DIST)}: promises to publish a person's name ({pat!r}). "
                    "We never publish a submitter's name, whatever channel it arrived through; "
                    "a photographer's licence credit is the only name on this site."
                )
    return out


def check_tree_count_claims(pages):
    """A rendered "N trees" claim may never overstate what we actually map.

    Added 2026-08-23 with the app overlay, which is the first site-wide count
    this project has published. Hidde asked the right question before it
    shipped ("die aantal trees gaat natuurlijk de hele tijd omhoog dus hoe
    doen we dat"), and the answer is that the overlay generates its number
    from the data and rounds it down. This check exists for the NEXT one:
    the moment somebody types a figure into a page by hand it starts going
    stale, which is exactly the failure check_count_promises() already guards
    one city at a time. The ratchet in CLAUDE.md says the fix ships with the
    check that makes the mistake unshippable, so here it is.

    Deliberately one-sided. Understating is fine and is what rounding down
    produces; only a claim larger than the truth is a lie.
    """
    total = 0
    for f in sorted((ROOT / "data" / "cities").glob("*.json")):
        try:
            city = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for t in city.get("trees", []):
            loc = t.get("location") or {}
            if t.get("story") and loc.get("latitude") is not None and loc.get("longitude") is not None:
                total += 1
    if not total:
        return []
    # Four figures and up only: "10 trees" is a city page counting its own,
    # which check_count_promises() already owns.
    # Only OUR OWN claim about OUR OWN collection, which is rendered in exactly
    # one sentence, by AppModal.astro from roundedTrees(): "Over 1,800 old trees
    # worth the walk", and its Spanish twin. Nothing else on a page is this
    # check's business.
    #
    # The first version scanned every page for any four-digit number followed by
    # "trees" and it was wrong twice in one afternoon. It read the footer's
    # "(c) 2026 Ancient Trees" as a claim of 2,026 trees, on all 3,206 pages.
    # With that fixed it still refused Athens, whose Zappeion story says "most
    # of the original 1857 trees have since been replaced", and Cork, whose
    # story calls the Boole arboretum "around 2,500 trees of some 120 species".
    # Both are true facts about somebody else's planting, and a check cannot
    # tell them from a boast by counting digits.
    #
    # So it guards the thing it can actually guarantee: that the one generated
    # site-wide figure never overstates the map, and that nobody replaces the
    # helper with a number typed by hand. Editorial prose is deliberately out
    # of scope; a story that misdescribes an arboretum is a research error and
    # a reader will tell us.
    pat = re.compile(
        r"\b(\d{1,3}(?:,\d{3})+|\d{3,})\s+(?:old |ancient |remarkable )*trees worth the walk"
        r"|\b(\d{1,3}(?:\.\d{3})+|\d{3,})\s+(?:\u00e1rboles viejos|arboles viejos)", re.I)
    out = []
    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in pat.finditer(text):
            raw = m.group(1) or m.group(2)
            n = int(raw.replace(",", "").replace(".", ""))
            if n > total:
                out.append(
                    f"{page.relative_to(DIST)}: claims {raw} trees, and we map {total}. "
                    "Site-wide counts are generated and rounded DOWN "
                    "(site/src/lib/tree-count.ts); never type one by hand."
                )
    return out


def check_sitemap_dates():
    sm = DIST / "sitemap.xml"
    if not sm.exists():
        return []
    dates = set(re.findall(r"<lastmod>([^<]+)</lastmod>", sm.read_text(encoding="utf-8")))
    if len(dates) > 1:
        return []
    return ["sitemap.xml: every url carries the same lastmod (%s). The dates come "
            "from each page's last source commit, so one date means git history "
            "was unavailable at build time (check fetch-depth on the checkout)."
            % (next(iter(dates), "none"))]


def main():
    global DIST
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=None,
                        help="Override the dist directory (default: site/dist). "
                             "Used during the Astro migration to check site/dist-astro "
                             "without touching behavior against the real dist.")
    args = parser.parse_args()
    if args.dist:
        # Must be absolute: the orphan check below resolves() every link
        # target before comparing it against `pages`, so a relative DIST
        # (exactly what --dist's own help text recommends, e.g. "site/
        # dist-astro") made every one of those comparisons compare a
        # relative Path against an absolute one, silently orphaning every
        # non-excluded page in the build.
        DIST = args.dist.resolve()

    failures = []
    failures += check_auth_corpus_agreement()
    failures += check_photo_orientation()
    failures += check_photo_resolution()
    failures += check_save_flow_integrity()
    failures += check_sheet_integrity()
    failures += check_one_tree_card()
    failures += check_one_owner_per_event()
    failures += check_no_owner_name()
    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        print(f"QA: no pages found under {DIST}, run (cd site && npx astro build) first")
        return 1

    for page in pages:
        rel = page.relative_to(DIST)
        scan = PageScan()
        scan.feed(page.read_text(encoding="utf-8"))
        text = " ".join(scan.text_parts)

        if rel.name == "index.html" and rel.parent.name == "":
            import re as _re
            m = _re.search(r"<title>([^<]*)</title>", page.read_text(encoding="utf-8"))
            if m and not m.group(1).startswith("Ancient Trees"):
                failures.append(f"{rel}: homepage <title> is {m.group(1)!r}; a shelf caption once shadowed it")

        if rel.name in PROMISE_PAGES and rel.parent.name == "":
            import re as _re2
            for pat in PROMISE_PATTERNS:
                # Whole words only. A substring match reads ", every one of them"
                # as the promise ", ever" and fails an honest sentence, which is
                # how this rule blocked a deploy on 2026-08-06.
                if _re2.search(r"%s\b" % _re2.escape(pat), text.lower()):
                    failures.append(f"{rel}: absolute promise {pat!r} in product copy (forever-claims rule)")

        if "—" in text:
            failures.append(f"{rel}: em dash in rendered text (hard rule 3)")
        # A tree with no numeric age (age_min/age_max null, age_estimate with
        # no digit) once made age_token() fall back to the literal string
        # "None", shipping live as "<title>...: None Year Old Tree in City"
        # on three published pages before this check existed (2026-08-09).
        if "None Year" in text:
            failures.append(f"{rel}: literal 'None Year' in rendered text, an undated tree's age fell back to None")
        lower = text.lower()
        for word in BANNED_WORDS:
            if word in lower:
                failures.append(f"{rel}: banned word {word!r} in rendered text")
        for phrase in BUSINESS_RULE_PHRASES:
            if phrase in lower:
                failures.append(
                    f"{rel}: explains our own publishing rule to the reader "
                    f"({phrase!r}). Say what is here and why it is worth the "
                    f"visit; the threshold behind it is ours, not theirs.")

        for src in scan.img_srcs:
            if "/wiki/File:" in src:
                failures.append(f"{rel}: img src is a wiki File: page: {src}")
            # The image standard (Hidde, 2026-07-31): every rendered image is
            # right-sized via img_srcset. A full-resolution original in an img
            # tag means a new render site skipped the helper.
            if "upload.wikimedia.org/wikipedia/commons/" in src and "/thumb/" not in src:
                failures.append(f"{rel}: full-size Wikimedia original in img (use img_srcset): {src[:90]}")
            if re.search(r"(static\.inaturalist\.org|inaturalist-open-data)[^\"]*/original\.", src):
                failures.append(f"{rel}: iNaturalist original in img (use img_srcset): {src[:90]}")
            if not (src.startswith("http") or src.startswith("data:")
                    or not re.match(r"^[a-z]+:", src)):
                failures.append(f"{rel}: img src with unexpected scheme: {src}")

        for url in scan.links + scan.img_srcs:
            if re.match(r"^(https?:|mailto:|data:|tel:)", url):
                continue
            path = url.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue  # pure #anchor
            base = DIST if path.startswith("/") else page.parent
            target = (base / path.lstrip("/")).resolve()
            if not resolves(target):
                failures.append(f"{rel}: dead internal link {url!r}")

    # Orphan check: the machine-testable half of the whole-page rule (Hidde,
    # 2026-08-04). Country pages shipped live with nothing linking to them for
    # three days because "how does anyone reach this" was never asked. A page
    # nobody links to cannot be found by a visitor and is barely crawled.
    linked = set()
    for page in pages:
        scan = PageScan()
        scan.feed(page.read_text(encoding="utf-8"))
        for url in scan.links:
            if re.match(r"^(https?:|mailto:|data:|tel:|#)", url):
                continue
            path = url.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            base = DIST if path.startswith("/") else page.parent
            target = (base / path.lstrip("/")).resolve()
            for cand in (target, target.with_suffix(target.suffix + ".html"),
                         target / "index.html"):
                if cand.is_file():
                    linked.add(cand)
                    break
    # Redirect stubs and the noindexed account prototype are linked on purpose
    # by nothing; the homepage is the root.
    for page in pages:
        if page in linked or page.name == "index.html":
            continue
        text = page.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text or "noindex" in text:
            continue
        failures.append(f"{page.relative_to(DIST)}: orphan, no page on the site links to it")

    failures += check_no_strategy_in_workflows()
    failures += check_one_city_order()
    failures += check_sitemap_dates()
    failures += check_no_name_promise(pages)
    failures += check_tree_count_claims(pages)
    failures += check_species_face_is_chosen()
    failures += check_faces_travel_to_the_app()

    if failures:
        print(f"QA FAILED: {len(failures)} problem(s) in {len(pages)} pages")
        for f in failures[:60]:
            print(f"  - {f}")
        if len(failures) > 60:
            print(f"  ... and {len(failures) - 60} more")
        return 1
    print(f"QA passed: {len(pages)} pages, links resolve, text clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
