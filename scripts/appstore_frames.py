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
GOLD = (0xD9, 0xA1, 0x3F)

# The caption is the reader's, not ours: they are the subject, and there is no
# summary line after it (PRODUCT_COPY.md). Four to six words, like the
# references. The opener is a promise rather than a screen.
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


def panel(raw_path, caption):
    canvas = Image.new("RGB", (W, H), CANOPY)
    draw = ImageDraw.Draw(canvas)

    f = font("Gabarito-Bold.ttf", CAPTION_SIZE)
    y = CAPTION_TOP
    for line in caption.split("\n"):
        w = draw.textlength(line, font=f)
        draw.text(((W - w) / 2, y), line, font=f, fill=CREAM)
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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    for name, caption in PANELS:
        raw = RAW / f"{name}.png"
        if not raw.exists():
            print(f"  skip {name}: no raw screenshot yet")
            continue
        out = OUT / f"{name}.png"
        panel(raw, caption).save(out)
        print(f"  {name:12} {out.stat().st_size // 1024} KB  \"{caption.replace(chr(10), ' ')}\"")
        made += 1
    print(f"\n{made} panels in {OUT}")
    print("LOOK at them before uploading. A caption is marketing, and a wrong "
          "one is a promise the app has to keep.")


if __name__ == "__main__":
    main()
