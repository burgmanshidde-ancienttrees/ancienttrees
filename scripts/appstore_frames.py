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
# HIS WORDS, 2026-08-29, and they are the whole pitch in six.
HERO_LINE = "Trees worth the walk,\nwherever you are."

PANELS = [
    ("1-map", "The remarkable old trees\nnearest to you"),
    ("2-tree", "Why this one is\nworth the walk"),
    ("5-city", "Every old tree\nin a city"),
    ("4-discover", "Browse by city,\ncountry or species"),
    ("3-my-trees", "Collect the ones you\nhave stood in front of"),
    ("6-add", "Add a tree\nnobody has mapped"),
]

CAPTION_TOP = 150          # where the first line sits
CAPTION_SIZE = 92
LINE_GAP = 18
DEVICE_TOP = 620           # below the caption, with air
DEVICE_WIDTH = 1080        # 82 percent, so the ground frames it
BEZEL = 14
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

    f = font("Gabarito-Bold.ttf", CAPTION_SIZE)
    y = CAPTION_TOP
    for line in caption.split("\n"):
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
    frame = Image.new("RGB", (shot.width + BEZEL * 2, shot.height + BEZEL * 2),
                      (0x14, 0x18, 0x0F))
    frame.paste(shot, (BEZEL, BEZEL))
    canvas.paste(rounded(frame, CORNER), (x - BEZEL, DEVICE_TOP - BEZEL),
                 rounded(frame, CORNER))
    return canvas


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

    # A scrim under the words rather than over the whole picture: the top third
    # darkens, the tree keeps its light.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim)
    for y in range(int(H * 0.55)):
        a = int(190 * (1 - y / (H * 0.55)) ** 1.4)
        d.line([(0, y), (W, y)], fill=(10, 14, 8, a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), scrim).convert("RGB")

    draw = ImageDraw.Draw(canvas)
    f = font("Gabarito-Bold.ttf", 104)
    y = 220
    for text in line.split("\n"):
        w = draw.textlength(text, font=f)
        draw.text(((W - w) / 2, y), text, font=f, fill=CREAM)
        y += 104 + 20
    return canvas


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
