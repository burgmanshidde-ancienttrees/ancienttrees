#!/usr/bin/env python3
"""Put a reader's photograph on the tree's page, once a viewing pass said yes.

The judgement is not here. A viewing pass (the photo-judge agent) looks at
each file in data/sighting-queue.json and returns verdicts; this applies
them, one process, one file at a time, the way photo_verdicts.py does for the
Commons queue and for the same reason: several passes writing the same files
lose each other's work.

    python3 scripts/sightings_publish.py verdicts.json [more.json] [--send]

Input: a JSON array of {sighting_id, verdict, reason, species_seen,
species_match, description_seen, description_match}, verdict one of
approve, hold, reject.

WHO CHECKS: the viewing pass, never the reader (Hidde, 2026-09-11: "i dont
want the user to input the species though they can if they want... i want
you to check the specie if it matches before you put it live. also you
should sort of judge if it matches the description"). A reader may name a
species in the app and it arrives as a hint; nothing requires it. Both
checks below are made against OUR record of the tree, which the queue
carries as tree_species, recognise, why_go, tree_girth_cm, tree_height_m
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
import smtplib
import sys
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


def photo_block(entry, width, height, reason, today):
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
    fname = f"{entry['tree_id']}-{slugify(entry['tree_name'])}.jpg"
    return {
        "url": f"{BASE_URL}/photos/{fname}",
        "license": "Provided by a reader through the Ancient Trees app, all rights reserved",
        "attribution": None,
        "status": "approved",
        "width": width,
        "height": height,
        "source": "contributor",
        "contributor_user_id": entry["user_id"],
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

    AS AN EXTRA (2026-09-12, when trees gained photos[]). The choice used to be
    replace or discard, and both are wrong for the ordinary case: a reader sends
    a good photograph of a tree that already has a good one, and the two answer
    different questions. The Camphor of Munakata Shrine is the worked example,
    a wide shot that shows where it stands and a close-up that shows what it is.
    Scarcity still governs which pictures are worth keeping; what changed is
    that keeping a second one no longer costs the first.
    """
    path = os.path.join(ROOT, "data", "cities", f"{entry['city_slug']}.json")
    city = json.load(open(path, encoding="utf-8"))
    old = None
    for t in city.get("trees", []):
        if t.get("id") == entry["tree_id"]:
            old = t.get("photo") or {}
            if as_extra:
                extras = t.setdefault("photos", [])
                # preflight refuses the same url twice, and an `add` verdict
                # applied on two nights would otherwise produce exactly that.
                urls = {(x or {}).get("url") for x in extras} | {old.get("url")}
                if block["url"] not in urls:
                    extras.append(block)
                break
            if old.get("url") and old.get("url") != block["url"]:
                t["photo_replaced"] = {k: old.get(k) for k in ("url", "license", "attribution", "status")}
            t["photo"] = block
            break
    else:
        raise KeyError(f"{entry['tree_id']} not in {path}")
    save(path, city, indent=2)  # data/cities convention, see preflight's check_city_indent
    # Nothing is replaced by an extra, so nothing may be un-vendored either.
    return None if as_extra else (old or {}).get("url")


def mail_for(entry, reason):
    page = f"{BASE_URL}/{entry['city_slug']}/{slugify(entry['tree_name'])}"
    name = credit_name(entry.get("display_name"))
    subject = "Your photograph is on the tree's page"
    body = (
        f"Hi {name},\n\n"
        f"Your photograph of {entry['tree_name']} in {entry['city']} is now on its page:\n"
        f"{page}\n\n"
        f"Thank you. A photograph taken by somebody who stood in front of the tree is "
        f"worth more to the page than anything we could find ourselves.\n\n"
        f"Is there another tree near you that we should have on the map? Add it in the app "
        f"the same way, or reply to this mail.\n\n"
        f"Hidde\nAncient Trees\n{BASE_URL}\n"
    )
    return subject, body


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
        with smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]), timeout=60) as server:
            server.starttls()
            server.login(creds["SMTP_USER"], creds["SMTP_PASS"])
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
    if not files:
        print(__doc__)
        return 1
    rows = []
    for f in files:
        rows += json.load(open(f, encoding="utf-8"))
    qdoc = load(QUEUE, {"queue": []})
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
            print(f"  {verdict.upper():7} {entry['tree_id']} {entry['tree_name'][:40]}: {reason[:80]}")
            continue
        seen = (r.get("species_seen") or "").strip()
        match = (r.get("species_match") or "").strip().lower()
        if match != "yes" or not seen:
            print(f"  REFUSED {entry['tree_id']} {entry['tree_name'][:40]}: an approval needs "
                  f"species_seen and species_match 'yes' (got {match or 'nothing'!r}); "
                  f"a mismatch or doubt is a hold. Left in the queue.")
            continue
        fits = (r.get("description_seen") or "").strip()
        fit = (r.get("description_match") or "").strip().lower()
        if fit != "yes" or not fits:
            print(f"  REFUSED {entry['tree_id']} {entry['tree_name'][:40]}: an approval needs "
                  f"description_seen and description_match 'yes' (got {fit or 'nothing'!r}); "
                  f"a photograph that does not fit what we wrote about the tree is a hold. "
                  f"Left in the queue.")
            continue
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
        block = photo_block(entry, w, h, reason, today)
        old_url = apply_to_city(entry, block, as_extra=extra)
        dropped = drop_vendored(old_url) if old_url and old_url != block["url"] else 0
        done[sid] = {"outcome": "added" if extra else "published", "date": today,
                     "tree_id": entry["tree_id"], "file": fname, "reason": reason[:300]}
        counts["add" if extra else "approve"] += 1
        published.append(entry)
        print(f"  {'ADDED' if extra else 'PUBLISHED'} {entry['tree_id']} {entry['tree_name'][:40]}: {fname} {w}x{h}"
              f"{f', replaced {old_url}' if old_url else ''}{f' ({dropped} vendored file(s) removed)' if dropped else ''}")
        addr = address_of(entry["user_id"])
        if addr:
            subject, body = mail_for(entry, reason)
            send_mail(addr, subject, body, really, sid)
        else:
            print(f"  mail: no address resolved for {entry['user_id'][:8]} (no service key, or account gone)")
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
