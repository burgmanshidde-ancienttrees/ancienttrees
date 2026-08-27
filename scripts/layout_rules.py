#!/usr/bin/env python3
"""What counts as a layout fault. One file, both platforms.

Hidde, 2026-08-20: "kun je vervolgens zorgen dat de CI voor app en web dezelfde
kwaliteit nastreven". They did not. The app could measure a four-point drift
(appfit.py, written 2026-08-20) while the website had no idea what a drift was,
and the website had a fit check the app did not judge in CI. Two gates, two
standards, and whichever platform he happened to look at was the one that had
the bug.

So the thresholds live here and nowhere else. scripts/appfit.py reads them for
the app; scripts/smoke_test.py reads them for the site. Changing a number here
changes it on both platforms at once, which is the whole point: a "quality bar"
that is written down twice is two bars.

The three faults, in the vocabulary both checks now print:

  CLIPPED   something starts on the screen and ends past its edge, so the reader
            sees a word cut in half. Horizontal shelves are exempt on both
            platforms, because a shelf is MEANT to run off the edge.

  DRIFT     two things that should share a left edge and are a few points apart.
            A heading at x=20 over a card at x=16 reads as "off" without reading
            as anything nameable, which is why eyes miss it and a number does
            not. Only NEAR misses count: a real inset is deliberate and large.

  SMALL     a control under Apple's 44 by 44 point minimum. Not a matter of
            taste; it is somebody's thumb missing the button three times.

Removing one of these checks needs Hidde, same as every other ratchet check.
"""

# Apple's minimum, from the Human Interface Guidelines, and not ours to soften.
MIN_TAP = 44.0

# A gap this size or smaller between two leading edges is a mistake rather than
# a decision. Real nesting insets are 12 and 16 points in the app, and the web's
# gutter tokens are 1.1rem and 1.75rem, so nothing deliberate lands in this band.
DRIFT_MAX = 11.0

# Frames and DOM rects come back with float noise; anything under this is the
# same edge.
#
# 1.0 since 2026-08-27, and it is the noise floor rather than a softening. The
# tree page's content column measures 402.8 points inside a 402 point screen
# where a city page's measures 402.0, so every full-bleed element on it inherits
# eight tenths of a point that no eye can see and no layout change removes. At
# 0.6 the gate reported that as a clipped control, which kept the whole iOS gate
# red, and a red gate hides real breakage and blinds the app's fresh-eyes review
# as well, because that review takes its screenshots from the newest green run.
#
# What it still catches is unchanged: the faults this was written for are three
# and a half points (the tree page's action bar) and 37 points (the nav bar's
# "Get the app"). Nothing real lives between six tenths of a point and one.
SAME = 1.0

# The width the web's phone checks measure at, and the reason the app measures on
# the smallest phone it supports: the narrowest real screen is the honest one.
PHONE_W = 375
