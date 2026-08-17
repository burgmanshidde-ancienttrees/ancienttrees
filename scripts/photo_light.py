#!/usr/bin/env python3
"""Score a photograph's exposure before anyone spends eyes on it.

Hidde, 2026-08-13, on the Weichselboom photograph that had just gone live:
"deze foto heeft wel echt slechte belichting bijna zwart wit - kun je een
betere vinden en kun je belichting beoordeling meenemen in je foto keuze."
He is right that it is a real criterion and right that it was missing: the
Cadiz standard says "taken in daylight, properly exposed and in colour", and
until now the only thing enforcing that was somebody remembering to look.

Colour and exposure are measurable, so they should not cost a viewing pass.
This prints four numbers per image and one verdict:

    brightness  mean luma, 0-255
    contrast    standard deviation of luma; very low reads as flat or hazy
    colour      mean saturation, 0-1; a backlit silhouette drops toward 0 and
                reads as almost black and white, which is exactly the
                complaint above
    blown       share of pixels at the top of the range; a bright sky behind a
                dark subject blows out and takes the subject's colour with it

    python3 scripts/photo_light.py photo.jpg
    python3 scripts/photo_light.py https://upload.wikimedia.org/...jpg

What it CANNOT do is say whether the tree is the subject, whether the crown is
readable, or whether the photograph is of the right tree at all. Those still
need a viewing pass. This only takes the obviously bad ones off its plate, and
a rejection here is cheap in a way that a rejection after downloading and
looking is not.

macOS only, deliberately: it shells out to sips, which is already on this
machine, rather than adding an image library to a project whose stack is
deliberately boring. CI cannot fetch images anyway (the runner's proxy blocks
upload.wikimedia.org), so a check that only works in a session is a check that
works exactly where the viewing pass happens.
"""
import os
import struct
import subprocess
import sys
import tempfile
import urllib.request

UA = "AncientTreesBot/1.0 (https://ancienttrees.app; photo exposure check)"

# Thresholds, set from the photographs already on the site rather than from
# theory. The Weichselboom (the complaint that produced this file) scores
# colour 0.06 with 12% blown; Trento's plane, the best photograph we have,
# scores colour 0.30 with 2% blown.
FLAT_CONTRAST = 28
GREY_COLOUR = 0.10
DIM_BRIGHTNESS = 60
BLOWN_SHARE = 0.10
# A night shot under street lighting is monochromatic in the OPPOSITE direction
# to a black-and-white one: sodium lamps wash the whole frame in a single
# intense orange, so saturation goes UP while brightness stays down. The colour
# test only ever looked for too little colour, so Delft's Sint Agathaplein "by
# night" scored a clean OK, and only a viewing pass noticed there was no tree in
# it. Measured 2026-08-17: that frame reads 0.83 saturation at brightness 68,
# against 0.38 at 94 for Ferrara's bagolaro and 0.18 at 136 for Nuremberg's lime,
# both broad daylight. Never a night shot is already the Cadiz standard; this
# makes it a number rather than something somebody has to notice.
LAMPLIT_COLOUR = 0.62
LAMPLIT_BRIGHTNESS = 90


def _bmp_pixels(path, size=64):
    """A small BMP of the image, as (r, g, b) triples.

    sips writes a bottom-up 24-bit BMP with 4-byte aligned rows; that is a
    dozen lines to parse and needs nothing but the standard library."""
    with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as fh:
        tmp = fh.name
    try:
        subprocess.run(["sips", "-s", "format", "bmp", "-Z", str(size), path,
                        "--out", tmp],
                       check=True, capture_output=True)
        data = open(tmp, "rb").read()
    finally:
        os.unlink(tmp)
    if data[:2] != b"BM":
        raise ValueError("not a BMP")
    offset = struct.unpack_from("<I", data, 10)[0]
    w, h = struct.unpack_from("<ii", data, 18)
    bits = struct.unpack_from("<H", data, 28)[0]
    if bits != 24:
        raise ValueError("expected 24-bit BMP, got %d" % bits)
    row_bytes = (w * 3 + 3) // 4 * 4
    out = []
    for row in range(abs(h)):
        start = offset + row * row_bytes
        for col in range(w):
            b, g, r = data[start + col * 3: start + col * 3 + 3]
            out.append((r, g, b))
    return out


def score(path):
    px = _bmp_pixels(path)
    n = len(px)
    lumas, sats = [], []
    blown = dark = 0
    for r, g, b in px:
        y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        lumas.append(y)
        hi, lo = max(r, g, b), min(r, g, b)
        sats.append(0.0 if hi == 0 else (hi - lo) / hi)
        if y > 245:
            blown += 1
        if y < 12:
            dark += 1
    mean = sum(lumas) / n
    var = sum((y - mean) ** 2 for y in lumas) / n
    return {
        "brightness": round(mean, 1),
        "contrast": round(var ** 0.5, 1),
        "colour": round(sum(sats) / n, 3),
        "blown": round(blown / n, 3),
        "dark": round(dark / n, 3),
    }


def verdict(s):
    """One line a viewing pass can act on without opening the image."""
    bad = []
    if s["colour"] < GREY_COLOUR:
        bad.append("almost colourless, reads as black and white")
    if s["blown"] > BLOWN_SHARE and s["colour"] < 0.18:
        bad.append("backlit: the sky is blown out and the subject is a silhouette")
    if s["brightness"] < DIM_BRIGHTNESS:
        bad.append("underexposed")
    if s["colour"] > LAMPLIT_COLOUR and s["brightness"] < LAMPLIT_BRIGHTNESS:
        bad.append("shot after dark under artificial light")
    if s["contrast"] < FLAT_CONTRAST:
        bad.append("flat, no separation between subject and background")
    if bad:
        return "POOR: " + "; ".join(bad)
    if s["colour"] < 0.16 or s["blown"] > BLOWN_SHARE:
        return "WEAK: usable, but the light is working against it"
    return "OK: daylight, colour, subject separated"


def fetch(url):
    with tempfile.NamedTemporaryFile(suffix=".img", delete=False) as fh:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        fh.write(urllib.request.urlopen(req, timeout=30).read())
        return fh.name


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip().splitlines()[0])
        print("usage: photo_light.py <file-or-url> [...]")
        return 1
    worst = 0
    for a in args:
        tmp = None
        try:
            path = fetch(a) if a.startswith("http") else a
            tmp = path if a.startswith("http") else None
            s = score(path)
            v = verdict(s)
        except Exception as e:                      # a bad image is not a crash
            print("%-58s could not read: %s" % (a[-58:], e))
            continue
        finally:
            if tmp:
                os.unlink(tmp)
        print("%-58s brightness %5.1f  contrast %5.1f  colour %.3f  blown %.3f"
              % (a[-58:], s["brightness"], s["contrast"], s["colour"], s["blown"]))
        print("    %s" % v)
        worst = max(worst, 2 if v.startswith("POOR") else 1 if v.startswith("WEAK") else 0)
    return worst


if __name__ == "__main__":
    sys.exit(main())
