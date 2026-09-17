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

# THE SIGN-IN SHEET'S VERTICAL RHYTHM, measured off AllTrails' own sheet on
# 2026-09-17 rather than chosen (Hidde: "verticale spacing ziet er beter uit bij
# alltrails let op dat soort dingen onthou dit"). His screenshots are 3x
# captures of a 402pt phone, so each number below is a pixel measurement divided
# by three, and CONVENTIONS.md carries the workings.
#
# Why these are a CHECK and not a note. Spacing is the one class of fault that
# reads as "this looks cheap" while nobody can name what is wrong, so it
# survives every review by eye and every gate that asks whether an element
# EXISTS. Three drifts got through in one afternoon here: an anchor computing a
# 50 point pill among 48s, a rule block at 61 where the reference has 51, and a
# headline left 8 points above a button because hiding the subtitle took its
# margin with it. Each was invisible in a screenshot and obvious in a number.
SHEET_BTN_H = 48.0        # every pill in the sheet, the loud one included
SHEET_BTN_GAP = 16.0      # between two adjacent pills
SHEET_RULE_GAP = 51.0     # across the "or", from the loud pill to the next
SHEET_TITLE_GAP = 32.0    # headline to the loud pill, where no subtitle sits
# Sub-pixel rounding plus a browser's own line-box arithmetic; anything larger
# is a real drift rather than noise.
SHEET_TOL = 3.0

# The width the web's phone checks measure at, and the reason the app measures on
# the smallest phone it supports: the narrowest real screen is the honest one.
PHONE_W = 375

# ZOOM, and it is the one fault on this list that only one platform can have.
#
# Safari on iOS zooms the page in when a focused field carries text under 16px,
# and it does not zoom back out. So a field at 15px is not slightly small, it is
# a page that jumps the moment somebody taps it: Hidde, 2026-09-12, "als je op
# mobile web op zoek klikt zoomt ie raar in", which was the homepage search at
# 15px through a cascade nobody meant.
#
# It lives here rather than in smoke_test.py because this file is where the
# thresholds live, and it is web-only because it is a browser behaviour rather
# than a design bar. The app is native and cannot have it.
#
# Measured as EXECUTED, never as written: the rule that produced the bug never
# said 15 anywhere near the search, it said it 300 lines away and won on
# specificity. Only a computed style can see that.
MIN_INPUT_FONT = 16.0
