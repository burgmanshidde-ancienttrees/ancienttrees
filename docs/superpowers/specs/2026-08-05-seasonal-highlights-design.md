# Seasonal highlights: one living curve per tree

Date: 2026-08-05
Status: approved by Hidde in session, ready for an implementation plan

## The problem

The tree page draws the year as leaf cover. An olive keeps its leaves all twelve
months, so its curve is a straight line, and a straight line says nothing. Hidde's
words: "als het een groen blad heeft, dan is die lijn gewoon recht. Dat zegt ook
niets."

He pointed at PictureThis, which draws a "Hemisphere Trend Curve" that never goes
flat. Reading their screenshots: the southern curve is not a mirror of the
northern one but noisy and irregular, the y axis carries no unit or scale, and the
only botanical annotation is a single badge pinned to the maximum. That is an
observation volume curve, how many people photograph the species per month per
hemisphere, with a phenology label on the peak. We have no such data and will not
fake one.

What we can take is the framing. The chart should answer "when is this tree worth
seeing" instead of stating a botanical fact, because that question never has a
flat answer.

## What the curve means

Per month, how much there is to see on this tree. Derived from the per species
phenology we already hold, plus one judgement per moment.

Baseline per month:

| state | value |
|---|---|
| bare | 0.08 |
| neither bare nor in leaf (turn months) | 0.22 |
| in leaf | 0.38 |

On top of the baseline, each recorded moment (flowers, fruit, colour) adds its
weight to the months it spans:

| judgement | weight | example |
|---|---|---|
| `unseen` | 0.00 | ginkgo flowers |
| `nice` | 0.18 | oak catkins |
| `striking` | 0.35 | olive blossom, acorns |
| `worth the trip` | 0.55 | ginkgo gold, horse chestnut candles |

Two rules turn steps into a wave:

1. **Shoulders.** The month before the first and after the last month of a moment
   receives 40 percent of that moment's weight. A peak rises and falls instead of
   stepping.
2. **Fresh leaves.** The first leaf month that follows a bare month gets an
   automatic +0.15. That spring flush is a real moment and it is recorded nowhere
   in the data.

Values are clamped to 1.0 and are **not normalised per species**. A genuinely
uneventful tree stays low. Normalising would hand every species a full height
peak and the peak would stop meaning anything, which is the same failure as
giving every tree a `best_time`. The vertical axis is therefore fixed at 0 to 1
and never fitted to a species own range.

Worked results against the real files:

```
pedunculate oak   ▂▂▂▆▅▄▄▅██▆▃
ginkgo            ▂▂▂▅▄▄▄▄▄▆█▄    invisible April flowering gone, November gold stands
horse chestnut    ▂▂▂▆█▅▄▅▇▆▃▂
olive             ▅▄▄▅▆▆▅▄▅▆▆▆    blossom in May, harvest in autumn
                  JFMAMJJASOND
```

## Data change

One optional block per file in `data/phenology/[species].json`:

```json
"intensity": { "flowers": "unseen", "fruit": "nice", "colour": "worth the trip" }
```

Absent block, or an absent key inside it, means `nice`. That default is
deliberately the dull one: a species nobody has judged yet gets no false peak.

Allowed values are exactly `unseen`, `nice`, `striking`, `worth the trip`. Any
other value is a build error, in the same way an unknown `best_time.kind` already
is.

All 25 existing files get the block in this change. Every new species file gets it
during its own research, alongside the sources it already needs.

Two files need their data checked before they can be judged: Moreton Bay Fig and
Giant Sequoia both record no flowers, no fruit and no colour, and the fig in fact
carries fruit. Research those two properly rather than declaring them seasonless.

## Page change: the two charts become one

The tree page currently renders two curve charts one directly after the other:
`season_curve()` from `best_time` ("Best time to visit", a single peak) and
`phenology_block()` ("The tree's year", leaf cover). Two charts making the same
promise, stacked. That is a bigger defect than the flat line and it is why the
page reads cluttered.

They merge into one figure:

- one curve across the year, the seasonal highlight score above
- the `best_time` month marked as the peak, with its written label underneath
  ("late November, when the ginkgo turns gold")
- the "at its best right now" chip when the current month is in `best_time.months`
- icon badges for flowers, fruit and colour at their own months, only for moments
  judged `striking` or `worth the trip`, so the chart does not crowd
- the current month marker stays

Where `best_time` names a month that is not the curve's own maximum, the marked
peak follows `best_time`. That field is a per tree judgement written by whoever
researched the tree, and it outranks a score derived from the species.

Nothing is lost, the page gets a block shorter. Where a tree has no `best_time`,
the curve still renders, without a marked peak and without the label line: that is
the normal case for an evergreen with no single best moment.

## Honesty rules

- The footnote states what the chart is: our estimate of when this tree is worth
  seeing, not a measurement, with weeks shifting from year to year.
- A species where nothing rises above `unseen` gets no chart and one plain
  sentence instead, the same honest gap as a missing photo.
- The latitude shift (a month early below 42N, a month late above 56N) and the
  tropical cutoff at 25N are unchanged.
- Build check: a rendered curve whose values are all equal fails the build. This
  bug class cannot return unnoticed, per the QA ratchet in CLAUDE.md.

## What this touches in the corpus

- CLAUDE.md's phenology section describes the calendar as bare / in leaf / flowers
  / fruit / colour. Still true as the source data; the rendering changes from leaf
  cover to seasonal highlight, so that paragraph needs one updated sentence.
- The `best_time` doctrine is untouched. It still names one moment, still drives
  the "at its best right now" badge across the site, and the curve now hosts it
  rather than sitting beside it.
- The scarcity argument behind `best_time` applies to `worth the trip` as well:
  if every species claims it, it stops meaning anything.

## Trio check

- **Product.** Serves the season verb directly, the one that turns "nice" into
  "this weekend".
- **UX.** One glance on a phone, one chart instead of two, honest about being a
  judgement. Must hold at 375px.
- **Tech.** Pure build time derivation from data already on disk. No new
  dependency, one scoring function plus one optional data block, reversible in a
  single commit, and a build check that fails on a flat curve.

## Out of scope

- Observation or popularity data of any kind. We do not have it.
- Per tree curve tuning. The curve stays a species property, shifted by latitude,
  exactly as now.
- Hemisphere pairs. We know where each tree stands, so we draw one curve.
