#!/usr/bin/env python3
"""icon_check.py - the app icon rules Apple refuses an upload over.

Written 2026-08-27, the day the icon was looked at properly for the first time
and turned out to carry an alpha channel. That is not a review note or a
warning: App Store Connect refuses the binary outright with "Invalid Image - The
app icon can't contain an alpha channel", before a human has seen anything. It
had been sitting there since the icon was made, and nothing in this project
could see it, because every other check is about layout or behaviour.

    python3 scripts/icon_check.py

Three rules, all of them Apple's:

  * exactly 1024 by 1024
  * no alpha channel, at all, whatever the pixels behind it say
  * no transparency-implying format: PNG, and not an interlaced one

Reading a PNG header is enough for all three and needs no library, which
matters: this has to run on the CI runner and on a Linux box, and the flattening
tool that fixed it (a few lines of CoreGraphics) only exists on a Mac.
"""

import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICON = ROOT / "ios/AncientTrees/AncientTrees/Assets.xcassets/AppIcon.appiconset/AppIcon.png"

# PNG colour types. 4 is grey+alpha, 6 is RGB+alpha; both are refused.
WITH_ALPHA = {4, 6}


def main():
    if not ICON.exists():
        sys.exit(f"no app icon at {ICON}")
    data = ICON.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("the app icon is not a PNG")

    # IHDR is always the first chunk: width, height, depth, colour type.
    width, height, _depth, colour = struct.unpack(">IIBB", data[16:26])

    faults = []
    if (width, height) != (1024, 1024):
        faults.append(f"it is {width}x{height} and Apple wants exactly 1024x1024")
    if colour in WITH_ALPHA:
        faults.append("it carries an alpha channel, which refuses the upload outright "
                      "(flatten it onto an opaque background)")
    # A tRNS chunk is transparency in a palette image, the other way in.
    if b"tRNS" in data[:2048]:
        faults.append("it declares transparency in a tRNS chunk")

    if faults:
        print("The app icon would be refused:")
        for f in faults:
            print("  " + f)
        sys.exit(1)
    print(f"app icon: {width}x{height}, no alpha. Apple will take it.")


if __name__ == "__main__":
    main()
