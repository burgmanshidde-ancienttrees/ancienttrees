#!/usr/bin/env python3
"""Wrap the raw App Store screenshots in a caption and a brand ground.

Hidde, 2026-08-29: "volgens mij pakken de meeste apps die appstore screenshot
toch zo aan dat er een achtergrond is en tekst bij staat kun je eens dat
benchmarken en met nieuwe suggestie komen."

WHAT THE REFERENCES ACTUALLY DO, read off their own App Store pages on
2026-08-29 rather than remembered (AllTrails id405075943, komoot id447374873,
PictureThis id1252497129). All three, without exception:

  - a solid BRAND-COLOURED ground, never the white of the screenshot itself
  - a CAPTION AT THE TOP, one or two lines, benefit-first, four to six words
  - the screen INSET below it, and cropped at the bottom rather than shrunk to
    fit, so the picture reads as a phone in use rather than a thumbnail

Where they differ is the inset's edge. AllTrails draws a black device bezel;
komoot and PictureThis let the screen bleed to the panel's sides. We take
AllTrails' side, because our screens are pale and map-heavy and without a
bezel the panel and the screenshot melt into one another.

And the pattern all three share that is worth more than the styling: the FIRST
panel carries a promise rather than a screen. AllTrails opens with "Discover
500,000+ trails" on black, komoot with "Explore 7M+ routes". A gallery is
scrolled, and the first frame is the only one everybody sees.

Usage:
    python3 scripts/appstore_shots.py     # the raw screens, 1320x2868
    python3 scripts/appstore_frames.py    # this, into out/appstore/framed/
"""

import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "out" / "appstore"
OUT = RAW / "framed"
FONTS = ROOT / "ios" / "AncientTrees" / "AncientTrees" / "Fonts"

# App Store Connect's 6.9 inch size, which is what appstore_shots.py writes.
W, H = 1320, 2868

# Brand/Style.swift, the light palette, so the panels and the app agree.
CANOPY = (0x3A, 0x52, 0x22)
CREAM = (0xFA, 0xF7, 0xEF)
INK = (0x26, 0x30, 0x1E)
GOLD = (0xD9, 0xA1, 0x3F)
# The hero heading's gold is the site's own #F0C876 (style.css:709), which is
# lighter than the brand gold because it sits on a photograph.
GOLD_HERO = (0xF0, 0xC8, 0x76)

# THE GROUND IS A CHOICE, so it is a flag rather than a constant (Hidde,
# 2026-08-29: "deze groen is veel te aanwezig, probeer een paar varianten").
# Each is (background, caption colour). The palette is the site's, not new
# paint: cream and ink are what every page already uses, sage and sand are the
# two neutrals sitting between them.
GROUNDS = {
    "canopy": (CANOPY, CREAM),
    "cream":  ((0xFA, 0xF7, 0xEF), INK),
    "ink":    ((0x14, 0x18, 0x0F), CREAM),
    "sage":   ((0xDD, 0xE3, 0xD2), INK),
    "sand":   ((0xE8, 0xDF, 0xCB), INK),
}

# The caption is the reader's, not ours: they are the subject, and there is no
# summary line after it (PRODUCT_COPY.md). Four to six words, like the
# references. The opener is a promise rather than a screen.
# HIS WORDS, 2026-08-29, and they are the whole pitch in six. They are also
# the website's own h1, so the two surfaces say the same thing.
HERO_LINE = "Trees worth the walk,\nwherever you are."

# The opener's photograph, chosen by Hidde on 2026-08-29 out of three he was
# shown. Free Unsplash License, so no visible credit is owed and the name is
# recorded here instead, which is what hard rule 4 asks and what the website's
# own hero lost when build_site.py was deleted.
#
#   Photo: Josh Carter, Unsplash (unsplash.com/@midwestiscool)
#   https://unsplash.com/photos/green-leaf-covering-tree-branch-lD2Ah5thV2U
#
# Put the file at out/appstore/0-hero.jpg. It is not committed: out/ is
# ignored, and a 5 MB photograph in the history buys nothing when the URL is
# written down.
HERO_SOURCE = "https://images.unsplash.com/photo-1529025635398-c8844675ab65?q=85&w=2400&auto=format&fit=crop"

PANELS = [
    # Line one is a verb phrase that stands on its own and line two finishes
    # it, because the two are set in different weights and the bold half has to
    # make sense alone. That is AllTrails' own shape, "Vind routes" over "die
    # je inspireren", and it is why theirs read calmly.
    ("1-map", "Find the old trees\nnearest to you"),
    ("2-tree", "Read what makes it\nworth the walk"),
    ("3-city", "See every old tree\nin a city"),
    ("4-discover", "Browse by city,\ncountry or species"),
    ("5-my-trees", "Collect the trees\nyou have stood in front of"),
    ("6-add", "Add a tree\nnobody has mapped yet"),
]

# Quieter than the first version, measured against AllTrails' own panels: the
# words are smaller, the phone is narrower, and there is more ground around
# both. The canvas itself cannot change, since 1320x2868 is what App Store
# Connect accepts for a 6.9 inch phone and nothing else, so everything that
# makes a panel feel less like a long strip has to happen inside it.
CAPTION_TOP = 170          # where the first line sits
CAPTION_SIZE = 76
LINE_GAP = 14
DEVICE_TOP = 560           # below the caption, with air
DEVICE_WIDTH = 980         # 74 percent, so the ground frames it properly
BEZEL = 20                 # the black between the rail and the screen
RAIL = 10                  # the titanium edge outside it
CORNER = 78


def font(name, size):
    path = FONTS / name
    if not path.exists():
        print(f"missing font {path}", file=sys.stderr)
        return ImageFont.load_default()
    return ImageFont.truetype(str(path), size)


def rounded(img, radius):
    """The screen with iPhone corners, so the bezel can sit around it."""
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0], img.size[1]],
                                           radius=radius, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def panel(raw_path, caption, ground):
    canvas = Image.new("RGB", (W, H), ground[0])
    draw = ImageDraw.Draw(canvas)

    # TWO WEIGHTS, not one (Hidde, 2026-08-29, holding AllTrails' own panels up
    # beside ours: "deze voelt rustiger kun je het meer hierop laten lijken").
    # Theirs read "Vind routes" bold over "die je inspireren" light, and that
    # contrast is most of the calm: one line is the claim and the other is the
    # sentence finishing it, so the eye is given an order to read them in.
    # Ours were both at the same weight, which makes two shouts.
    lines = caption.split("\n")
    y = CAPTION_TOP
    for i, line in enumerate(lines):
        f = font("Gabarito-ExtraBold.ttf" if i == 0 else "Gabarito-Regular.ttf",
                 CAPTION_SIZE)
        w = draw.textlength(line, font=f)
        draw.text(((W - w) / 2, y), line, font=f, fill=ground[1])
        y += CAPTION_SIZE + LINE_GAP

    shot = Image.open(raw_path).convert("RGB")
    scale = DEVICE_WIDTH / shot.width
    shot = shot.resize((DEVICE_WIDTH, int(shot.height * scale)), Image.LANCZOS)

    # Cropped at the bottom rather than shrunk to fit: the references all let
    # the screen run off the panel, which is what makes it read as a phone in
    # somebody's hand rather than a picture of one.
    keep = H - DEVICE_TOP + 40
    if shot.height > keep:
        shot = shot.crop((0, 0, shot.width, keep))

    x = (W - DEVICE_WIDTH) // 2
    device = iphone(shot)
    canvas.paste(device, (x - BEZEL - RAIL, DEVICE_TOP - BEZEL - RAIL), device)
    return canvas


def iphone(shot):
    """The screen inside a phone somebody would recognise.

    Hidde, 2026-08-29: "zou je m wel eens zoals alltrails in een iphone willen
    zetten." Their panels put the screen in a real device rather than in a
    rounded rectangle, and the difference is not decoration: a plain dark
    border reads as a border, and a phone reads as a phone in somebody's hand.

    Three things do that work and nothing else is needed. A rail around the
    bezel, one shade lighter, which is the titanium edge catching light. Corner
    radii that GROW outward, so the rail and the bezel stay concentric the way
    real ones do rather than looking stacked. And the buttons, volume and the
    action button on the left, the side button on the right, because they are
    what the eye actually reads as a telephone.
    """
    w = shot.width + (BEZEL + RAIL) * 2
    h = shot.height + (BEZEL + RAIL) * 2
    body = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)

    # The titanium rail, then the black bezel inside it.
    d.rounded_rectangle([0, 0, w, h], radius=CORNER + BEZEL + RAIL,
                        fill=(0x8A, 0x8F, 0x84))
    d.rounded_rectangle([RAIL, RAIL, w - RAIL, h - RAIL], radius=CORNER + BEZEL,
                        fill=(0x0B, 0x0D, 0x09))
    body.paste(shot, (RAIL + BEZEL, RAIL + BEZEL), rounded(shot, CORNER))

    # The buttons, on the rail itself. Sizes off a real iPhone at this scale:
    # the side button is about twice the length of one volume button.
    btn = (0x6F, 0x74, 0x6A)
    unit = shot.width // 18
    for top, length in ((int(h * 0.16), unit), (int(h * 0.24), unit * 2),
                        (int(h * 0.24) + unit * 2 + unit // 2, unit * 2)):
        d.rounded_rectangle([0, top, RAIL - 1, top + length], radius=RAIL // 2,
                            fill=btn)
    side_top = int(h * 0.22)
    d.rounded_rectangle([w - RAIL + 1, side_top, w, side_top + unit * 3],
                        radius=RAIL // 2, fill=btn)
    return body


def hero(photo_path, line, ground):
    """The opener: a photograph and a promise, no screen at all.

    AllTrails and komoot both do this and it is the frame everybody sees,
    because a gallery is scrolled and the first one is free. The photograph is
    the website's own hero, so somebody arriving from ancienttrees.app meets
    the same picture.
    """
    canvas = Image.new("RGB", (W, H), ground[0])
    photo = Image.open(photo_path).convert("RGB")
    # Fill the panel, cropped from the centre.
    scale = max(W / photo.width, H / photo.height)
    photo = photo.resize((int(photo.width * scale), int(photo.height * scale)),
                         Image.LANCZOS)
    canvas.paste(photo, ((W - photo.width) // 2, (H - photo.height) // 2))

    # THE WORDS SIT LOW, at two thirds (Hidde, 2026-08-29: "kun je de tekst op
    # 2/3 van de pagina zetten ipv boven"). So the scrim moves with them: it
    # darkens UP from the bottom rather than down from the top, which leaves
    # the crown of the tree its light and puts the shade where the sentence is.
    # A scrim that stayed at the top would now be shading nothing.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim)
    reach = int(H * 0.55)
    for i in range(reach):
        y = H - 1 - i
        a = int(200 * (1 - i / reach) ** 1.3)
        d.line([(0, y), (W, y)], fill=(10, 14, 8, a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), scrim).convert("RGB")

    # THE WEBSITE'S OWN HEADING, to its own rule (Hidde, 2026-08-29: "kun je
    # hetzelfde lettertype als op de website gebruiken"). Read off
    # site/public/assets/style.css:708-709 rather than eyeballed: Gabarito at
    # weight 800, letter-spacing -0.02em, line-height 1.08, white with the
    # second half in gold, and a soft shadow under it. The same sentence stands
    # on ancienttrees.app, so the panel and the homepage are one thing.
    draw = ImageDraw.Draw(canvas)
    size = 104
    f = font("Gabarito-ExtraBold.ttf", size)
    tracking = -size * 0.02
    # Two thirds down, measured from the block's own height so both lines sit
    # under the fold rather than the first one landing there.
    lines = line.split("\n")
    y = int(H * 0.66) - int(size * 1.08) * (len(lines) - 1)
    for i, text in enumerate(lines):
        gold = i == 1                       # the site puts the second half in <em>
        w = tracked_width(draw, text, f, tracking)
        draw_tracked(draw, (W - w) / 2, y, text, f, tracking,
                     GOLD_HERO if gold else CREAM)
        y += int(size * 1.08)
    return canvas


def tracked_width(draw, text, f, tracking):
    return sum(draw.textlength(c, font=f) + tracking for c in text) - tracking


def draw_tracked(draw, x, y, text, f, tracking, fill):
    """Letter-spacing, which PIL has no setting for and the site's h1 has.

    Drawn twice: once in the shadow's colour a little lower, once in the
    letter's own, which is what text-shadow does on the page.
    """
    for dx, dy, colour in ((0, 6, (0, 0, 0, 90)), (0, 0, fill)):
        cx = x + dx
        for c in text:
            draw.text((cx, y + dy), c, font=f, fill=colour)
            cx += draw.textlength(c, font=f) + tracking


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    name_of_ground = sys.argv[1] if len(sys.argv) > 1 else "canopy"
    if name_of_ground not in GROUNDS:
        print(f"grounds: {', '.join(GROUNDS)}")
        return
    ground = GROUNDS[name_of_ground]
    out_dir = OUT / name_of_ground
    out_dir.mkdir(parents=True, exist_ok=True)

    photo = RAW / "0-hero.jpg"
    if photo.exists():
        out = out_dir / "0-hero.png"
        hero(photo, HERO_LINE, ground).save(out)
        print(f"  {'0-hero':12} {out.stat().st_size // 1024} KB  \"{HERO_LINE}\"")

    made = 0
    for name, caption in PANELS:
        raw = RAW / f"{name}.png"
        if not raw.exists():
            print(f"  skip {name}: no raw screenshot yet")
            continue
        out = out_dir / f"{name}.png"
        panel(raw, caption, ground).save(out)
        print(f"  {name:12} {out.stat().st_size // 1024} KB  \"{caption.replace(chr(10), ' ')}\"")
        made += 1
    print(f"\n{made} panels in {out_dir}")
    print("LOOK at them before uploading. A caption is marketing, and a wrong "
          "one is a promise the app has to keep.")


if __name__ == "__main__":
    main()
