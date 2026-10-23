#!/usr/bin/env python3
"""Put a reader's photograph on the tree's page, once a viewing pass said yes.

The judgement is not here. A viewing pass (the photo-judge agent) looks at
each file in data/sighting-queue.json and returns verdicts; this applies
them, one process, one file at a time, the way photo_verdicts.py does for the
Commons queue and for the same reason: several passes writing the same files
lose each other's work.

    python3 scripts/sightings_publish.py verdicts.json [more.json] [--send]
    python3 scripts/sightings_publish.py --vouched [--send]
    python3 scripts/sightings_publish.py --pins    (only the pin catch-up below)

PINS (2026-10-05): every accepted photograph moves its tree's pin to the
photograph's GPS fix when our pin says approximate; see move_pin().

Input: a JSON array of {sighting_id, verdict, reason, species_seen,
species_match, description_seen, description_match}, verdict one of
approve, hold, reject.

WHO CHECKS: the viewing pass, never the reader (Hidde, 2026-09-11: "i dont
want the user to input the species though they can if they want... i want
you to check the specie if it matches before you put it live. also you
should sort of judge if it matches the description"). A reader may name a
species in the app and it arrives as a hint; nothing requires it. Both
checks below are made against OUR record of the tree, which the queue
carries as tree_species, recognise, tree_girth_cm, tree_height_m
and story.

THE PHOTOGRAPH MUST FIT THE DESCRIPTION, as well as the species. A big
camphor is still the wrong photograph for "the oldest and largest tree in
the park" if the one in frame is a modest one beside a path. So an approval
also says what in the photograph matches what we wrote (`description_seen`:
the size, the shape, the setting, the thing the recognition line points at)
and `description_match`: yes, no, unsure. Only "yes" publishes.

THE SPECIES IS COMPARED BEFORE ANYTHING SHIPS (Hidde, 2026-09-11: "heb je
soort vergelijker als vaste stap ingebouwd"). An approval must say what the
viewing pass SAW in the photograph (`species_seen`: leaf, bark, crown, in a
few words) and whether that matches the tree's recorded species
(`species_match`: yes, no, unsure). Only "yes" publishes. The case that made
it a gate rather than a habit: on 2026-09-11 a night run approved a photograph
for the Sudajii of Omiya Gate whose pale, smooth trunk is not a Castanopsis,
because it judged light and composition and never asked what tree it was
looking at. A reader picks from a list of nearby trees, and picking the wrong
one is the ordinary mistake, not a rare one. An approval missing either
field is refused and stays in the queue. Every verdict is recorded in
data/sightings-processed.json so a photograph is never judged twice; a hold
is a verdict too (two similar trees stand nearby, the picture cannot settle
which), and stays a hold until somebody knows more.

The verdicts are approve, add, hold and reject. ADD (2026-09-12) publishes the
photograph BESIDE the one the tree already has rather than in place of it, for
the case the other two get wrong: a good picture of a tree that already has a
good picture, answering a different question. A wide shot says where a tree
stands and a close-up says what it is, and until trees could carry more than
one the only ways to handle the second were to displace the first or to throw
it away. It takes the same two checks an approval does, because an extra ships
on a page exactly as the lead does.

An approval does five things, in this order, and stops at the first that
fails:
  1. Opens the file, applies the phone's EXIF orientation to the PIXELS and
     drops the tag (qa.py refuses a self-hosted file with orientation != 1,
     because a browser would turn the tree on its side), resizes to LONG on
     the long edge, writes site/public/photos/<tree_id>-<slug>.jpg.
  2. Writes the tree's photo block: our own url, a gift licence in the form
     images.ts already prints as a name alone, the DISPLAY NAME as the credit
     (never the email), width and height (the app feed refuses a null), and
     source "contributor" with contributor_user_id, both, because preflight
     refuses one without the other and photo_takedown.py keeps the deletion
     promise through that id.
  3. Removes the vendored copies of the photograph it replaces, so qa's
     orphan check does not find dead weight in site/public/photos.
  4. Records the outcome.
  5. Writes the reader a short mail, through mailcheck, saying the photograph
     is on the page and asking for the next tree. DRY unless --send; the
     night run passes --send with the outreach credentials it already holds.

Needs Pillow for step 1 (pip install pillow; the night run installs it).
Needs SUPABASE_SERVICE_KEY to resolve the reader's address for step 5, and
the OUTREACH_* credentials to send; absent either, the mail is printed.
"""
import datetime
import json
import os
import re
import unicodedata
import smtplib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people  # noqa: E402  account ids as codes in public files (2026-10-19)
import ours  # noqa: E402

import mailer
from email.message import EmailMessage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
QUEUE = os.path.join(ROOT, "data", "sighting-queue.json")
PROCESSED = os.path.join(ROOT, "data", "sightings-processed.json")
MANIFEST = os.path.join(ROOT, "data", "photo-manifest.json")
PHOTOS = os.path.join(ROOT, "site", "public", "photos")
SENT_PATH = os.path.join(ROOT, "data", "outreach-sent.json")
BASE_URL = "https://ancienttrees.app"
LONG = 1600
FALLBACK_NAME = "a reader of Ancient Trees"
# A reader's fix further than this from our own approximate pin is not taken
# on trust: either the pin is badly wrong or the reader picked the wrong tree,
# and telling those apart needs somebody to look. Printed, never applied.
READER_PIN_MAX_M = 300


# NO LEAD IS SPELT "none" BY THE QUEUE (2026-10-09). sightings_inbox.py's
# tree_index() writes photo_status "none" for a tree whose photo block carries
# no url, and this file tested current_photo against (None, "", "missing"),
# so a vouched photograph for a tree with NO picture at all was judged to
# have one and went in as an extra. That is how Hidde's overrule on the City
# Hall Maple (2026-10-05) ran and still left rey_003 reading "missing": the
# photograph sat in photos[] under a lead that did not exist. One test, read
# by the vouched path and by the inbox's ranking.
NO_LEAD = (None, "", "missing", "none")


def has_lead(status):
    return status not in NO_LEAD


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s or "tree"


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default


def save(path, doc, indent=1):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=indent)
        fh.write("\n")


def credit_name(display_name):
    name = (display_name or "").strip()
    return name if name else FALLBACK_NAME


def photo_block(entry, width, height, reason, today, fname=None):
    """The photo dict the tree gets. Pure, so it can be tested without a file."""
    # NO NAME ON IT (Hidde, 2026-09-04: "laten we niet mensen hun naam noemen,
    # laten we alleen hun fotos gebruiken als ze goed zijn, het kan mensen
    # afschrikken als hun naam erbij staat"). This retires the credit half of
    # the 2026-09-02 decision, and it moves in the same direction as the rule
    # that has stood since 2026-08-11: a person who sends us something is not
    # published. A named photographer who ASKED to be credited is a different
    # case and keeps their name (images.ts, isAGift): they were written to,
    # they answered, and the name is the whole of what they get.
    #
    # The account id stays, because the takedown sweep needs it and it is not
    # a name.
    # THE URL FOLLOWS THE FILE (2026-10-02). An extra is written to disk under a
    # name carrying the sighting id so it cannot overwrite the lead, and this
    # block used to rebuild the url from the stem alone, so the extra's url was
    # the lead's url, apply_to_city's duplicate check dropped it, and the file
    # sat in site/public/photos with nothing pointing at it until QA failed
    # the deploy and a run deleted it. That lost the Paris Turkey Oak close-up
    # a reader sent on 2026-10-01, the first add verdict ever applied.
    fname = fname or f"{entry['tree_id']}-{slugify(entry['tree_name'])}.jpg"
    return {
        "url": f"{BASE_URL}/photos/{fname}",
        "license": "Provided by a reader through the Ancient Trees app, all rights reserved",
        "attribution": None,
        "status": "approved",
        "width": width,
        "height": height,
        "source": "contributor",
        "contributor_user_id": people.ref(entry["user_id"]),
        "sighting_id": entry["sighting_id"],
        "note": (f"Photographed by a reader and sent through the app "
                 f"({(entry.get('taken_at') or '')[:10] or 'date unknown'}); a viewing pass "
                 f"approved it on {today}: {reason.strip() or 'meets the Cadiz standard'}. "
                 f"Not an open licence: ask before reuse elsewhere. No name is printed "
                 f"beside it (2026-09-04). Comes off the page when the account is "
                 f"deleted (scripts/photo_takedown.py)."),
    }


def write_image(src, dest):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise RuntimeError(
            "Pillow is not installed, and a reader's photograph must be rotated "
            "upright before it ships (qa refuses a self-hosted file whose EXIF "
            "tag would turn it again). Run: pip install pillow")
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB",):
        im = im.convert("RGB")
    w, h = im.size
    scale = LONG / max(w, h)
    if scale < 1:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    im.save(dest, "JPEG", quality=86, optimize=True)  # no exif written: tag is gone
    return im.size


def drop_vendored(old_url):
    """Delete our vendored copies of the photograph being replaced."""
    if not old_url:
        return 0
    man = load(MANIFEST, {"photos": {}})
    rec = man.get("photos", {}).get(old_url)
    removed = 0
    if rec:
        for w in rec.get("widths", []):
            p = os.path.join(PHOTOS, f"{rec['base']}-{w}.jpg")
            if os.path.exists(p):
                os.remove(p)
                removed += 1
        del man["photos"][old_url]
        save(MANIFEST, man)
    elif "/photos/" in old_url and old_url.startswith(BASE_URL):
        p = os.path.join(PHOTOS, old_url.rsplit("/", 1)[-1])
        if os.path.exists(p):
            os.remove(p)
            removed += 1
    return removed


def apply_to_city(entry, block, as_extra=False):
    """Put the photograph on the tree, as the lead or beside it.

    BESIDE THE ONE IT HAD (since 2026-10-23 as the lead, the old lead moving
    into the strip; see READER FIRST below). AS AN EXTRA (2026-09-12, when trees gained photos[]). The choice used to be
    replace or discard, and both are wrong for the ordinary case: a reader sends
    a good photograph of a tree that already has a good one, and the two answer
    different questions. The Camphor of Munakata Shrine is the worked example,
    a wide shot that shows where it stands and a close-up that shows what it is.
    Scarcity still governs which pictures are worth keeping; what changed is
    that keeping a second one no longer costs the first.
    """
    path = os.path.join(ROOT, "data", "cities", f"{entry['city_slug']}.json")
    city = json.load(open(path, encoding="utf-8"))
    old, promoted = None, []
    for t in city.get("trees", []):
        if t.get("id") == entry["tree_id"]:
            old = t.get("photo") or {}
            if as_extra:
                extras = t.setdefault("photos", [])
                # preflight refuses the same url twice, and an `add` verdict
                # applied on two nights would otherwise produce exactly that.
                urls = {(x or {}).get("url") for x in extras} | {old.get("url")}
                if block["url"] not in urls:
                    # READER FIRST (Hidde, 2026-10-23: "if google appreciates
                    # them as lead better then make them lead"): the reader's
                    # photograph leads, the one it had moves into the strip.
                    # unique_photo() in thin_pages.py reads the lead only.
                    if old.get("url"):
                        extras.insert(0, old)
                    t["photo"] = block
                break
            if old.get("url") and old.get("url") != block["url"]:
                t["photo_replaced"] = {k: old.get(k) for k in ("url", "license", "attribution", "status")}
            # PROMOTION (2026-10-09): the same photograph may already sit in
            # photos[] as an extra (the has_lead bug above put one there under
            # no lead at all). Becoming the lead takes it out of the strip,
            # and its separately named file with it, or the page would show
            # the picture twice.
            kept = []
            for x in t.get("photos") or []:
                if (x or {}).get("sighting_id") == entry["sighting_id"] or (x or {}).get("url") == block["url"]:
                    promoted.append(x.get("url"))
                else:
                    kept.append(x)
            if t.get("photos") is not None:
                if kept:
                    t["photos"] = kept
                else:
                    del t["photos"]
            t["photo"] = block
            break
    else:
        raise KeyError(f"{entry['tree_id']} not in {path}")
    save(path, city, indent=2)  # data/cities convention, see preflight's check_city_indent
    for url in promoted:
        if url and url != block["url"]:
            drop_vendored(url)
    # Nothing is replaced by an extra, so nothing may be un-vendored either.
    return None if as_extra else (old or {}).get("url")


def metres(lat1, lon1, lat2, lon2):
    import math
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(a))


def move_pin(tree, lat, lon, sighting_id, taken_at, today):
    """The reader's GPS fix becomes the pin, when ours admits it is approximate.

    Hidde, 2026-10-05, on the Reykjavik reader whose three photographs stood
    11, 20 and 92 metres from our pins: "verbeter de pins en doe dit standaard
    vanaf nu". The rule itself is CLAUDE.md's of 2026-09-08: a reader's fix
    beats a pin of ours that says approximate, and never one that says
    confirmed. Our own field says which kind it is, so this is arithmetic.

    It runs only for a photograph a viewing pass (or Hidde) has already
    accepted as THIS tree, which is what turns a coordinate into evidence: the
    pin then marks a spot somebody stood and photographed the tree from. The
    fix is the photograph's own location (LibraryPicker reads it off the asset;
    the camera takes it at the shutter), not where the phone was at upload.

    Pure on the tree dict, so it can be tested without a file. Returns a line
    for the log, or None when nothing moved.
    """
    if lat is None or lon is None:
        return None
    if tree.get("location_precision") != "approximate":
        return None
    loc = tree.setdefault("location", {})
    if loc.get("latitude") is None or loc.get("longitude") is None:
        return None
    d = metres(loc["latitude"], loc["longitude"], lat, lon)
    if d > READER_PIN_MAX_M:
        return (f"NOT MOVED {tree.get('id')}: the reader stood {round(d)} m from our pin, "
                f"over {READER_PIN_MAX_M} m; look before trusting it")
    loc["latitude"], loc["longitude"] = round(lat, 6), round(lon, 6)
    tree["location_precision"] = "confirmed"
    tree["pin_source"] = {
        "kind": "reader GPS fix",
        "sighting_id": sighting_id,
        "moved_m": round(d),
        "date": today,
        "note": ("The pin marks where a reader stood to photograph this tree; the "
                 "photograph was checked to show it (CLAUDE.md 2026-09-08, made "
                 "automatic 2026-10-05)."),
    }
    return f"PIN {tree.get('id')}: moved {round(d)} m to the reader's fix, now confirmed"


def pin_from_reader(city_slug, tree_id, lat, lon, sighting_id, taken_at, today):
    """move_pin on the tree in its city file, saved only when it moved."""
    path = os.path.join(ROOT, "data", "cities", f"{city_slug}.json")
    if not os.path.exists(path):
        return None
    city = json.load(open(path, encoding="utf-8"))
    for t in city.get("trees", []):
        if t.get("id") == tree_id:
            line = move_pin(t, lat, lon, sighting_id, taken_at, today)
            if line and line.startswith("PIN "):
                save(path, city, indent=2)
            return line
    return None


def catch_up_pins(done, today):
    """Every photograph already published whose tree still has a rough pin.

    Runs on every call, so a fix recorded before this existed, or one whose
    move was refused once over the distance cap and has since been looked at,
    is picked up without anybody remembering it. Coordinates come from the
    processed record (written since 2026-10-05) or, for older ones, from
    Supabase when the service key is present.
    """
    lines = []
    want = {}
    for sid, rec in done.items():
        if rec.get("outcome") not in ("published", "added") or not rec.get("tree_id"):
            continue
        if rec.get("pin_checked"):
            continue
        want[sid] = rec
    if not want:
        return lines
    trees = {}
    import glob
    for path in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        slug = os.path.basename(path)[:-5]
        for t in (load(path, {}).get("trees") or []):
            trees[t.get("id")] = (slug, t.get("location_precision"))
    missing = [sid for sid, rec in want.items()
               if rec.get("lat") is None and trees.get(rec["tree_id"], (None, None))[1] == "approximate"]
    fetched = supa_coordinates(missing) if missing else {}
    for sid, rec in want.items():
        slug, prec = trees.get(rec["tree_id"], (None, None))
        if slug is None:
            continue
        if prec != "approximate":
            rec["pin_checked"] = today
            continue
        lat, lon, taken = rec.get("lat"), rec.get("lon"), rec.get("taken_at")
        if lat is None and sid in fetched:
            lat, lon, taken = fetched[sid]
            rec["lat"], rec["lon"], rec["taken_at"] = lat, lon, taken
        if lat is None:
            continue  # no coordinate known yet; try again next run
        line = pin_from_reader(slug, rec["tree_id"], lat, lon, sid, taken, today)
        if line:
            lines.append(line)
        rec["pin_checked"] = today
    return lines


def supa_coordinates(sighting_ids):
    """{sighting_id: (lat, lng, taken_at)} from Supabase, {} without the key."""
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key or not sighting_ids:
        return {}
    import urllib.request
    out = {}
    for i in range(0, len(sighting_ids), 50):
        ids = ",".join(sighting_ids[i:i + 50])
        req = urllib.request.Request(
            f"{SUPA}/rest/v1/sightings?select=id,lat,lng,taken_at&id=in.({ids})",
            headers={"apikey": key, "Authorization": f"Bearer {key}"})
        try:
            rows = json.load(urllib.request.urlopen(req, timeout=20))
        except Exception as e:
            print(f"  pins: could not read coordinates ({e.__class__.__name__})")
            return out
        for r in rows:
            if r.get("lat") is not None and r.get("lng") is not None:
                out[str(r["id"]).lower()] = (r["lat"], r["lng"], r.get("taken_at"))
    return out


TRANSLIT = {"ß": "ss", "ø": "o", "æ": "ae", "œ": "oe", "ł": "l", "đ": "d", "ð": "d", "þ": "th", "ħ": "h"}


def page_slug(name):
    """slugify() in site/src/lib/slug.ts, the one rule the pages are built
    with. Not this file's slugify(), which names photo files and keeps "the"."""
    s = name.lower().replace("'", "").replace("’", "")
    if s.startswith("the "):
        s = s[4:]
    s = "".join(TRANSLIT.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def page_url(t):
    """The tree's live page, from its name as published today (names change)."""
    path = os.path.join(ROOT, "data", "cities", f"{t['city_slug']}.json")
    name = t["tree_name"]
    if os.path.exists(path):
        for x in json.load(open(path, encoding="utf-8")).get("trees", []):
            if x.get("id") == t.get("tree_id"):
                name = x.get("name") or name
    return f"{BASE_URL}/{t['city_slug']}/{page_slug(name)}"


def mail_for(trees, first, display_name=None):
    """One mail for every photograph of one reader that went live since the
    last. `first` is their first mail from us: it carries the one ask, and a
    later mail is a thank-you only (the tree ask goes once per thread,
    HIS_VOICE.md 2026-10-20). Signed Ancient Trees, never as Hidde."""
    name = (display_name or "").strip()
    hi = f"Hi {name}," if name else "Hi,"
    pages = [(t["tree_name"], t["city"], page_url(t)) for t in trees]
    if len(pages) == 1:
        tree, city, page = pages[0]
        subject = f"Your photo is on the page of {tree}"
        said = f"Thanks for your photo of {tree} in {city}. It's on the tree's page now:\n{page}\n"
    else:
        subject = "Your photos are on the trees' pages"
        said = "Thanks for your photos. They're on the trees' pages now:\n" + "".join(
            f"{tree}, {city}\n{page}\n" for tree, city, page in pages)
    ask = ("\nIf you know another old tree that should be on the map, "
           "you can add it in the app the same way.\n") if first else ""
    return subject, f"{hi}\n\n{said}{ask}\nThanks again,\nAncient Trees\n"


# AT MOST ONE MAIL PER READER PER MAIL_GAP_DAYS (Hidde, 2026-10-23: "eerste
# live foto meteen een mail, daarna hooguit één per 30 dagen, gebundeld").
# Codes and tree ids only, never an address: this repository is public.
MAILED = os.path.join(ROOT, "data", "photo-live-mailed.json")
MAIL_GAP_DAYS = 30


def queue_mail(entry, today):
    doc = load(MAILED, {"readers": {}})
    r = doc["readers"].setdefault(entry["user_id"], {"last": None, "pending": [], "sent": []})
    if any(p["sighting_id"] == entry["sighting_id"] for p in r["pending"] + r["sent"]):
        return
    r["pending"].append({k: entry.get(k) for k in
                         ("sighting_id", "tree_id", "tree_name", "city", "city_slug", "display_name")}
                        | {"live": today})
    save(MAILED, doc)


def flush_mail(really, today):
    """Send what is due: a first mail at once, a bundle once the gap has passed."""
    doc = load(MAILED, {"readers": {}})
    for ref, r in doc["readers"].items():
        if not r["pending"] or ours.is_ours(ref):
            continue
        if r["last"]:
            waited = (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(r["last"])).days
            if waited < MAIL_GAP_DAYS:
                print(f"  mail {ref}: {len(r['pending'])} photo(s) wait, last mail {waited} day(s) ago")
                continue
        addr = address_of(people.uid(ref))
        if not addr:
            print(f"  mail {ref}: no address resolved (no service key, or account gone)")
            continue
        subject, body = mail_for(r["pending"], first=not r["last"],
                                 display_name=r["pending"][-1].get("display_name"))
        if send_mail(addr, subject, body, really, r["pending"][0]["sighting_id"]):
            r["sent"] += [{"sighting_id": p["sighting_id"], "tree_id": p["tree_id"], "mailed": today}
                          for p in r["pending"]]
            r["pending"], r["last"] = [], today
    save(MAILED, doc)


def mailcheck_ok(text):
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        # The header declares who this goes to, which exempts it from the
        # App Store line (mailcheck's check_app_link): they sent the
        # photograph from inside the app. Everything above --- is header and
        # never reaches the reader.
        f.write("draft\naudience: app user\n---\n" + text)
        path = f.name
    try:
        out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "mailcheck.py"), path],
                             capture_output=True, text=True, timeout=60)
        return out.returncode == 0, out.stdout.strip()
    finally:
        os.unlink(path)


def address_of(user_id):
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        return None
    import urllib.request
    req = urllib.request.Request(f"{SUPA}/auth/v1/admin/users/{user_id}",
                                 headers={"apikey": key, "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return (json.loads(r.read()) or {}).get("email")
    except Exception:
        return None


# WHAT THE READER SEES ON THEIR OWN PHOTOGRAPH, written back onto their row.
# Their app and the website's My trees print "Your photo, waiting for a look"
# while the row says mine or sent, and "Your photo is on the tree's page" once
# it says published (Sightings.Sighting.photoState, my-trees-js). Without this
# the state could never change, because nothing else ever touches a sighting
# row after the phone writes it. Nothing is written on a dry run, like the mail.
# NO MAIL WHEN A PHOTOGRAPH GOES LIVE (Hidde, 2026-10-02: "do we still send
# emails to people when trees are live - i think we shouldnt"). The first
# stranger to send photographs through the app did so from a Sign in with
# Apple relay address, minutes after installing; a mail from us into that
# inbox is the one thing about the exchange they did not ask for. The app
# already shows the status on their own tree, which is where the answer
# belongs. The mail code stays for the day he wants it back.
# Asked again 2026-10-21 for photos on existing trees, he said yes and then
# withdrew it: "denk je niet dat mensen daar op een gegeven moment klaar mee
# zijn", "doe maar niet". Mail fatigue outweighs the thanks.
# 2026-10-23 he answered the fatigue himself: the first photograph mails at
# once, later ones wait and go together, at most one mail per 30 days
# (flush_mail). On since the same day, when he approved the text
# (drafts/photo-live-mail.md): "Ja, de tekst is goed, zet de mail aan."
MAIL_WHEN_LIVE = True
VERDICT_STATUS = {"approve": "published", "add": "published",
                  "reject": "declined", "hold": "checking"}


def mark_status(sighting_id, verdict, really):
    status = VERDICT_STATUS.get(verdict)
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not status or not really or not key or str(sighting_id).startswith("tip-"):
        return
    import urllib.request
    body = json.dumps({"status": status,
                       "updated_at": datetime.datetime.utcnow().isoformat() + "Z"}).encode()
    req = urllib.request.Request(f"{SUPA}/rest/v1/sightings?id=eq.{sighting_id}", data=body,
                                 method="PATCH",
                                 headers={"apikey": key, "Authorization": "Bearer " + key,
                                          "Content-Type": "application/json",
                                          "Prefer": "return=minimal"})
    try:
        urllib.request.urlopen(req, timeout=30).close()
    except Exception as e:
        print(f"  {sighting_id}: status not written back ({e.__class__.__name__})")


def send_mail(addr, subject, body, really, sighting_id):
    sent_log = load(SENT_PATH, {"sent": []})
    dnc = {a.lower().strip() for a in sent_log.get("do_not_contact", [])}
    if addr.lower() in dnc or any(addr.lower().endswith(d) for d in dnc if d.startswith("@")):
        print(f"  mail to {addr}: on the do-not-contact list, not sent")
        return False
    ok, why = mailcheck_ok(body)
    if not ok:
        print(f"  mail to {addr}: held by mailcheck\n{why}")
        return False
    creds = {k: os.environ.get(f"OUTREACH_{k}") for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "FROM")}
    if not really or not all(creds.values()):
        print(f"  mail to {addr} (dry run{'' if all(creds.values()) else ', no credentials'}):\n"
              f"    {subject}\n" + "\n".join("    " + l for l in body.splitlines()))
        return False
    if "burgmans.hidde" in creds["FROM"].lower():
        print("  REFUSED: mail would go out under a personal address")
        return False
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = creds["FROM"], addr, subject
    msg.set_content(body)
    try:
        with mailer.connect(creds, timeout=60) as server:
            server.send_message(msg)
    except Exception as e:
        print(f"  mail to {addr}: transport failed ({e.__class__.__name__})")
        return False
    sent_log.setdefault("sent", []).append({
        "date": datetime.date.today().isoformat(), "to": addr, "outlet": "reader (app)",
        "subject": subject, "batch": "sighting-published", "sighting_id": sighting_id})
    save(SENT_PATH, sent_log)
    print(f"  SENT {addr}: {subject}")
    return True


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    really = "--send" in sys.argv
    # The mail step in nightly.yml, which holds the SMTP secrets and pulls the
    # do-not-contact list; publishing only queues (queue_mail).
    if "--flush-mail" in sys.argv:
        if MAIL_WHEN_LIVE:
            flush_mail(really, datetime.date.today().isoformat())
        return 0
    qdoc = load(QUEUE, {"queue": []})
    rows = []
    # --vouched: the photographs of a reader Hidde vouches for go live as they
    # are (data/sightings-vouched.json; 2026-10-05, "ook zijn semi slechte
    # foto's beter dan geen"). Lead when the tree has none, extra beside it
    # when it has; his word stands in for the species and description look.
    if "--vouched" in sys.argv:
        for e in qdoc.get("queue", []):
            if not e.get("vouched"):
                continue
            rows.append({"sighting_id": e["sighting_id"],
                         "verdict": "add" if has_lead(e.get("current_photo")) else "approve",
                         "reason": f"Vouched for by Hidde: {e['vouched']}",
                         "species_seen": "vouched", "species_match": "vouched",
                         "description_seen": "vouched", "description_match": "vouched"})
        print(f"sightings publish: {len(rows)} vouched photograph(s) in the queue")
    elif not files and "--pins" not in sys.argv:
        print(__doc__)
        return 1
    for f in files:
        rows += json.load(open(f, encoding="utf-8"))
    queue = {e["sighting_id"]: e for e in qdoc.get("queue", [])}
    processed = load(PROCESSED, {"done": {}})
    done = processed.setdefault("done", {})
    today = datetime.date.today().isoformat()
    counts = {"approve": 0, "add": 0, "hold": 0, "reject": 0}
    published = []
    for r in rows:
        sid, verdict, reason = r.get("sighting_id"), r.get("verdict"), (r.get("reason") or "")
        if verdict not in counts:
            print(f"  {sid}: unknown verdict {verdict!r}, skipped")
            continue
        entry = queue.get(sid)
        if not entry:
            print(f"  {sid}: not in the queue, skipped (run sightings_inbox.py first)")
            continue
        if verdict not in ("approve", "add"):
            done[sid] = {"outcome": "held" if verdict == "hold" else "rejected",
                         "date": today, "tree_id": entry["tree_id"], "reason": reason[:300]}
            counts[verdict] += 1
            mark_status(sid, verdict, really)
            print(f"  {verdict.upper():7} {entry['tree_id']} {entry['tree_name'][:40]}: {reason[:80]}")
            continue
        seen = (r.get("species_seen") or "").strip()
        match = (r.get("species_match") or "").strip().lower()
        vouch = match == "vouched" and bool(entry.get("vouched"))
        if not vouch and (match != "yes" or not seen):
            print(f"  REFUSED {entry['tree_id']} {entry['tree_name'][:40]}: an approval needs "
                  f"species_seen and species_match 'yes' (got {match or 'nothing'!r}); "
                  f"a mismatch or doubt is a hold. Left in the queue.")
            continue
        fits = (r.get("description_seen") or "").strip()
        fit = (r.get("description_match") or "").strip().lower()
        if not vouch and (fit != "yes" or not fits):
            print(f"  REFUSED {entry['tree_id']} {entry['tree_name'][:40]}: an approval needs "
                  f"description_seen and description_match 'yes' (got {fit or 'nothing'!r}); "
                  f"a photograph that does not fit what we wrote about the tree is a hold. "
                  f"Left in the queue.")
            continue
        if not vouch:
            reason = f"{reason.strip()} Species seen: {seen}. Fits the description: {fits}.".strip()
        src = os.path.join(ROOT, entry["file"])
        if not os.path.exists(src):
            print(f"  {sid}: file missing at {entry['file']}, run sightings_inbox.py again")
            continue
        # An extra needs a name of its own or it would overwrite the lead's file.
        extra = verdict == "add"
        stem = f"{entry['tree_id']}-{slugify(entry['tree_name'])}"
        fname = f"{stem}-{entry['sighting_id'][:8]}.jpg" if extra else f"{stem}.jpg"
        try:
            w, h = write_image(src, os.path.join(PHOTOS, fname))
        except Exception as e:
            print(f"  {sid}: could not write the image ({e.__class__.__name__}: {str(e)[:80]})")
            continue
        block = photo_block(entry, w, h, reason, today, fname=fname)
        old_url = apply_to_city(entry, block, as_extra=extra)
        dropped = drop_vendored(old_url) if old_url and old_url != block["url"] else 0
        done[sid] = {"outcome": "added" if extra else "published", "date": today,
                     "tree_id": entry["tree_id"], "file": fname, "reason": reason[:300],
                     "lat": entry.get("latitude"), "lon": entry.get("longitude")}
        pin = pin_from_reader(entry["city_slug"], entry["tree_id"], entry.get("latitude"),
                              entry.get("longitude"), sid, entry.get("taken_at"), today)
        done[sid]["pin_checked"] = today
        if pin:
            print(f"  {pin}")
        counts["add" if extra else "approve"] += 1
        mark_status(sid, verdict, really)
        published.append(entry)
        print(f"  {'ADDED' if extra else 'PUBLISHED'} {entry['tree_id']} {entry['tree_name'][:40]}: {fname} {w}x{h}"
              f"{f', replaced {old_url}' if old_url else ''}{f' ({dropped} vendored file(s) removed)' if dropped else ''}")
        if MAIL_WHEN_LIVE and really:
            queue_mail(entry, today)
        else:
            print("  mail: off, a photograph going live sends no mail yet (MAIL_WHEN_LIVE)")
    # And any photograph published earlier whose tree still has a rough pin.
    for line in catch_up_pins(done, today):
        print(f"  {line}")
    # Judged entries leave the queue; the rest wait for the next pass.
    qdoc["queue"] = [e for e in qdoc.get("queue", []) if e["sighting_id"] not in done]
    save(QUEUE, qdoc)
    save(PROCESSED, processed)
    print(f"sightings publish: {counts['approve']} published, {counts['add']} added "
          f"beside an existing photograph, {counts['hold']} held, "
          f"{counts['reject']} rejected, {len(qdoc['queue'])} still waiting")
    if published:
        print("Now: python3 scripts/preflight.py, then commit data/cities, site/public/photos, "
              "data/photo-manifest.json, data/sighting-queue.json and data/sightings-processed.json together.")
        # Their words go on the page too (Hidde, 2026-10-22: "zonde om die
        # niet te gebruiken"): the notes these readers wrote that no story
        # quotes yet, printed here so the session that published the photo
        # writes the quote in the same commit.
        import subprocess
        for tid in sorted({e["tree_id"] for e in published}):
            subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "reader_words.py"),
                            "--tree", tid])
    return 0


if __name__ == "__main__":
    sys.exit(main())
