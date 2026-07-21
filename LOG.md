# LOG

What the autonomous runs did, newest first. One entry per run that actually changed something. Hidde reads this to catch up, and says good or bad.

Format, deliberately short:

```
## YYYY-MM-DD HH:MM — what it did in one line
- What changed (files, pages, cities)
- Why, if it was a judgement call
- FOR HIDDE: only when something genuinely needs him. Otherwise leave it out.
```

If an entry has no `FOR HIDDE` line, nothing is waiting on you. That is the normal case.

---

# Open with Hidde

Standing list. Everything else in this file is history; this block is what is actually waiting.

### 1. Make the submission form (7 minutes, only Hidde can, unlocks the flywheel)

At forms.google.com, blank template. Title `Add trees to Ancient Trees`. Seven questions in this order, email **last** (the filter below depends on it):

| # | Question | Type | Required |
|---|---|---|---|
| 1 | Which city? | Short | yes |
| 2 | The tree, or trees | Paragraph | yes |
| 3 | Where does it stand? | Paragraph | yes |
| 4 | Why is it remarkable? | Paragraph | no |
| 5 | How do you know it? | Short | no |
| 6 | Your name, for the credit | Short | no |
| 7 | Your email | Short | no |

Help text on 3: *A street, a park, or a link from Google Maps. This is the single most useful thing you can give us.* On 7: *Only if you would like to hear when your tree goes live.*

Settings: **"Collect email addresses" off**, **"Limit to 1 response" off**, or people are forced to sign in. Confirmation message: *Thank you. Your tree goes into the next research round. If it checks out, it will be on the map within days, with your name on it if you left one.*

Then: Responses tab → green sheet icon → new spreadsheet. Add a second tab, cell A1:

```
=QUERY('Form Responses 1'!A:H, "SELECT A,B,C,D,E,F,G", 1)
```

(adjust the tab name if it differs). This copies everything except the email column. Then File → Share → **Publish to web** → pick **that second tab**, format **CSV**, Publish.

Hand over two links: the form link and the CSV link. They go into `SUBMISSION_FORM_URL` and `SUBMISSIONS_CSV_URL` in `scripts/build_site.py`; every button on the site switches over and runs start reading submissions. The email column stays private.

### 2. Illustrated icons (needs Hidde's eye, do it together)

Map pins should move to the painterly style he asked for, and to leaf shapes so species actually differ. Six of Lisbon's ten trees still share one broadleaf silhouette. Deliberately not started alone: it is taste work.

### 3. Unanswered question

He said "je kan niet de website gratis maken". Everything so far assumes the opposite: the site stays free forever because it is the entire acquisition engine (blueprint P9), and the app is what people pay for. Worth settling, because it changes a lot.

### 4. Later, not now

Analytics once there is traffic, and cookieless to avoid a consent banner. Search Console reading needs his Google credentials; no data worth reading yet.

---

## 2026-07-21 — Working agreement set up

- Added this log, plus a priority ladder and decision boundary in CLAUDE.md, so runs know what to work on and what to leave alone.
- Nothing about the site itself changed.
- FOR HIDDE: the boundary is in CLAUDE.md under "What runs decide alone". If anything in the "ask first" column feels too strict or too loose, move it. That list is the whole steering wheel.
