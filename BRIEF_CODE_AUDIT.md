# Code review of the app and the website, every seven days

Due, not on a weekday (Hidde, 2026-11-04: a weekly run that misses its day must not wait a week). review.yml runs it when the newest `## YYYY-MM-DD code` heading in REVIEW.md is seven or more days old, or there is none, and asks twice a day, so a missed run is caught within hours. The full sweep is due when the newest `code (full)` heading is 28 or more days old; the workflow tells you which this run is.

Hidde, 2026-11-04, after a one-off review of the app found seven bugs, four speed costs and about a thousand lines of dead code that no screenshot could show: "how can we make sure that this kind of analysis is part of our system not me thinking to ask you", and the same afternoon, "should we build a similar thing for web". The daily fresh-eyes review looks at pictures and built pages; this one reads the code behind them.

You review; you never fix. Write only REVIEW.md, data/code-audit.json and one line of LOG.md.

## What to read

- Every review: what changed in the last seven days, plus the files those changes call into or are called from (a bug usually lives where new code meets old).
  - App: `git log --since=7.days --stat -- ios/AncientTrees/AncientTrees` and the diffs.
  - Website: `git log --since=7.days --stat -- site/src` and the diffs. The scripts a visitor runs live as template strings in site/src/lib/*-js.ts and site/src/lib/map*.ts; read them as JavaScript.
- A full sweep (the workflow says FULL SWEEP: yes, when the last one is 28 or more days old): the whole app (ios/AncientTrees/AncientTrees/Screens and Kit) and the website's scripts (site/src/lib/*-js.ts, site/src/lib/map*.ts, site/src/components), largest files first.
- data/code-audit.json first: anything already listed is not reported again, unless it was marked fixed and is back (then it is a regression, say so).
- The corpus that sets the standard: CLAUDE.md (What this is, How to work, Design-time checks, hard rules), PRODUCT_COPY.md. For an interaction, grep CONVENTIONS.md's `^## ` headings and read only the matching entry.

## What to look for

Each finding gets a surface, APP or WEB, and one of five kinds:

- `BUG`: something wrong for a person. App: a crash path (force unwrap on data, index out of range), state out of sync, work done twice at once, a task never cancelled, a change that never reaches the screen, something that breaks offline or signed out. Web: a script that throws for one kind of page or visitor, a listener added twice, a fetch whose failure leaves a control dead, a signed-out or signed-in path that cannot work, a gate that does not go through atCollection.gate.
- `SPEED`: App: work in a SwiftUI body or computed property on every redraw (filtering or sorting the catalogue, big arrays, images decoded on the main thread, network on every appearance, timers nobody needs). Web: work on every scroll, move or keystroke over all trees, a large file loaded on pages that never use it, layout thrash, images without the srcset every image should carry.
- `UX`: an interaction that differs from the convention (AllTrails, Google Maps, Airbnb, komoot, Polarsteps, Apple's own apps), two ways to do one thing, a tap that does something unexpected, or the app and the website doing the same thing differently. Name the convention and its source and describe before and after in one or two sentences so it can be drawn.
- `CUT`: a screen, control, setting, copy or code path nobody needs, or one that only duplicates another.
- `CODE`: dead code, one component written twice, a file grown past the point of reading. Only where it costs something.

Verify every finding by reading the code; leave out what you are not sure of. Three real findings beat fifteen guesses. Speed findings name what runs and how often, not a measurement you did not make. Mechanical faults the gates already catch (qa.py, preflight.py, appfit, the smoke test) are not findings.

## Where it goes

1. data/code-audit.json, one object per finding in `findings`: `{"id": "<SURFACE>-<KIND>-<short-slug>", "surface": "APP|WEB", "kind": "BUG|SPEED|UX|CUT|CODE", "file": "path:line", "summary": "<one sentence>", "fix": "<one sentence>", "first_seen": "YYYY-MM-DD", "status": "open"}`. Never delete a row; a session or run sets `status` to `fixed` (with `fixed_in`, the commit), `not_a_bug` (with `why`, after reading the code) or `declined` (with Hidde's words).
2. REVIEW.md, at the top, under `## YYYY-MM-DD code` (`## YYYY-MM-DD code (full)` on a full sweep; the next due date is read from this heading, so write it even when nothing is found): one line per new finding, its id, file and summary. Nothing new: the heading and "Nothing new in the code."
3. LOG.md, one line at the top of today's entry (create the `## YYYY-MM-DD` heading if there is none), only when there is at least one new UX or CUT finding: `For Hidde: code review, <n> interaction proposal(s) and <m> thing(s) to cut wait for your word (REVIEW.md, <date> code).` Bugs, speed and code need no word from him.
4. Commit those files only, message `Code review: <n> new finding(s)`, and push (`git pull --rebase` and push again when main moved).

## Who acts on it

- BUG and SPEED: the night run, CLAUDE.md rung 2 (bugs) and rung 10 (speed). App work in a .claude/worktrees/ worktree with a unit test where the logic allows; web work verified by build output or a parsed script. Never a visible change; set the row to fixed with the commit.
- UX and CUT: never a run. A session draws the before and after for Hidde and builds only on his yes.
- CODE: rung 10, when nothing above it has work.
