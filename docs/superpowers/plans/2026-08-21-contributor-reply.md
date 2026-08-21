# Contributor Reply Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the loop on reader input: optional email on both contribute forms, a thank-you mail, a three-outcome answer mail that asks questions instead of dismissing, toggling worth-it thumbs with undo on web and app, and the sending machinery with the outreach guardrails.

**Architecture:** The Supabase submissions table gains reply-state columns (email, outcome, reply_text, thanked_at, replied_at). Both clients post to it exactly as today. A new script `scripts/contributor_reply.py` runs from CI (digest + night knocks), sends the two mail kinds over the existing SMTP creds, and records state in the columns so nothing is ever sent twice. Runs compose `reply_text` per submission during Step 0b; the script only transports.

**Tech Stack:** Astro (site, CI-built only, no local Node), SwiftUI (app), Python stdlib (scripts), Supabase REST.

**Spec:** docs/superpowers/specs/2026-08-21-contributor-reply-design.md

## Global Constraints

- No em dashes anywhere, in code comments, copy, mails (hard rule 3).
- The email label copy, verbatim: "Optional. Leave it so we can ask a question if we need to, and tell you what your tip changed. We use it for nothing else."
- Mail 1 body, verbatim from the spec (see Task 7 code).
- No new product dependencies (hard rule 5): the site and app keep posting to Supabase only; mail is sent by scripts, never by the product.
- This repo has no unit-test framework; verification per task is: `python3 -m py_compile` for Python, CI build + smoke test for the site (no local Node), `python3 scripts/appsweep.py` + `appfit.py` + looking at the screens for the app, and dry-run output for the mail script. The per-change eyes rule applies to every user-facing change: look at it rendered, 375px and desktop.
- Commit after every task, push in batches; `git pull --rebase --autostash` before push (night runs share the branch).
- Blocking facts: the Supabase columns exist only after Hidde pastes the SQL (Task 1, FOR HIDDE); CI can only send mail after Hidde adds OUTREACH_* secrets to GitHub Actions (Task 8, FOR HIDDE). Everything else ships and degrades honestly in the meantime.

---

### Task 1: The Supabase columns

**Files:**
- Create: `supabase/contributor-reply.sql`

**Interfaces:**
- Produces: columns `email text`, `outcome text`, `reply_text text`, `thanked_at timestamptz`, `replied_at timestamptz` on `public.submissions`. Tasks 2, 5, 7 rely on these exact names.

- [ ] **Step 1: Write the SQL file**

```sql
-- Contributor reply loop, 2026-08-21.
-- Spec: docs/superpowers/specs/2026-08-21-contributor-reply-design.md
-- Hidde pastes this into the Supabase SQL editor, same routine as saves.sql.
--
-- email       optional, reader-given, used ONLY to reply about their own
--             submission. Never rendered anywhere. Deleted on request.
-- outcome     set by the run that verifies: changed | holds | open_question
-- reply_text  the answer mail's body, composed by the run, sent by
--             scripts/contributor_reply.py after mailcheck passes
-- thanked_at  when the automatic thank-you went out
-- replied_at  when the answer went out
alter table public.submissions add column if not exists email text;
alter table public.submissions add column if not exists outcome text
  check (outcome is null or outcome in ('changed', 'holds', 'open_question'));
alter table public.submissions add column if not exists reply_text text;
alter table public.submissions add column if not exists thanked_at timestamptz;
alter table public.submissions add column if not exists replied_at timestamptz;
```

- [ ] **Step 2: Commit**

```bash
git add supabase/contributor-reply.sql
git commit -m "SQL for the contributor reply columns, for Hidde to paste"
```

- [ ] **Step 3: Record the FOR HIDDE ask** (folded into Task 10's LOG.md entry; nothing to do here beyond remembering it blocks live email capture).

---

### Task 2: Web contribute form: email field and the double-submit fix

**Files:**
- Modify: `site/src/pages/contribute.astro`

**Interfaces:**
- Consumes: the `email` column from Task 1 (posts it only when filled; retries without it if the column does not exist yet, so a submission is never lost to deployment order).

- [ ] **Step 0: Fix the name field's hint.** It says "Optional, and only so we can write back. Never shown on the site.", and "so we can write back" was never true: the form collected no address to write to (found 2026-08-21 when Hidde asked whether we could reach the Toulouse correspondent; we cannot). Change the hint to:

```html
<span class="sg-hint">Optional. Never shown on the site.</span>
```

- [ ] **Step 1: Add the email field** after the name label (line ~60), before the submit button:

```html
    <label>Your email <span class="sg-hint">Optional. Leave it so we can ask a question if we need to, and tell you what your tip changed. We use it for nothing else.</span>
      <input type="email" id="sg-email" placeholder="you@example.com">
    </label>
```

- [ ] **Step 2: Replace the submit handler** (the whole `f.addEventListener('submit', ...)` block) with:

```js
  var btn = f.querySelector('button[type="submit"]');
  var inFlight = false;
  f.addEventListener('submit', function(e) {
    e.preventDefault();
    if (inFlight) return;
    var city = document.getElementById('sg-city').value.trim();
    if (!city) return;
    // One press, one row: the Toulouse correction of 2026-08-20 arrived as
    // three identical rows because nothing stopped the extra presses.
    inFlight = true; btn.disabled = true; btn.textContent = 'Sending...';
    note.textContent = '';
    at.track('suggestion-submit');
    var payload = {
      kind: document.getElementById('sg-kind').value,
      city: city,
      tree: document.getElementById('sg-tree').value.trim(),
      location_hint: document.getElementById('sg-where').value.trim(),
      why: document.getElementById('sg-why').value.trim(),
      name: document.getElementById('sg-name').value.trim(),
      page: document.referrer || null
    };
    var email = document.getElementById('sg-email').value.trim();
    if (email) payload.email = email;
    function post(body) {
      return fetch('${SUPABASE_URL}/rest/v1/submissions', {
        method: 'POST',
        headers: {'apikey': '${SUPABASE_KEY}', 'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
        body: JSON.stringify(body)
      });
    }
    function fail() {
      inFlight = false; btn.disabled = false; btn.textContent = 'Send it in';
      note.textContent = 'That did not go through. Try again in a moment.';
    }
    post(payload).then(function(r) {
      // If the email column does not exist yet the insert 400s; the tree
      // matters more than the address, so retry without it rather than lose it.
      if (!r.ok && payload.email) { delete payload.email; return post(payload); }
      return r;
    }).then(function(r) {
      if (r.ok) {
        f.hidden = true;
        note.textContent = 'Thank you. Everything sent in is verified against independent sources; confirmed trees go live.';
      } else { fail(); }
    }).catch(fail);
  });
```

- [ ] **Step 3: Commit**

```bash
git add site/src/pages/contribute.astro
git commit -m "Contribute form: optional email so we can ask and answer, and one press is one row"
```

(Verification is CI + eyes, batched in Task 10.)

---

### Task 3: Web worth-it control: toggle thumbs, undo, why-chips after a down-vote

**Files:**
- Modify: `site/src/components/WorthIt.astro` (markup comment only if needed; markup itself is unchanged)
- Modify: `site/src/lib/worthit-js.ts` (replace the script body)
- Modify: `site/public/assets/style.css` (one selected-state rule)

**Interfaces:**
- Produces: undo rows in submissions with `why` starting `"vote undone"`. Task 4 (digest) and the Step 0b doc (Task 9) treat these as bookkeeping.

- [ ] **Step 1: Replace the script in `worthit-js.ts`** (everything between the backticks of `WORTHIT_JS`) with:

```js
<script>
(function() {
  function send(box, verdict, reason) {
    var tree = box.dataset.tree, city = box.dataset.city, name = box.dataset.name;
    try {
      fetch('${SUPABASE_URL}/rest/v1/submissions', {
        method: 'POST',
        headers: {'apikey': '${SUPABASE_KEY}', 'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
        body: JSON.stringify({
          kind: 'feedback',
          city: city,
          tree: tree + ' (' + name + ')',
          why: verdict + (reason ? ': ' + reason : ''),
          page: location.pathname
        })
      });
    } catch (e) {}
    try { at.track('worthit-' + verdict); } catch (e) {}
  }
  function show(box, sel, on) {
    var el = box.querySelector(sel);
    if (el) el.hidden = !on;
  }
  // Thumbs are toggle buttons (Hidde, 2026-08-21: "buttons to press and than
  // it selects and than unpress"): press selects and counts, press again
  // undoes, the other thumb switches. They stay visible after a vote; the
  // selected state IS the confirmation.
  function paint(box) {
    var v = localStorage.getItem('at_worthit_' + box.dataset.tree);
    box.querySelectorAll('.worthit-btn').forEach(function(b) {
      var on = v === b.dataset.vote;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    show(box, '.worthit-done', !!v);
  }
  function openWhy(box, heading) {
    var why = box.querySelector('.worthit-why');
    if (!why || localStorage.getItem('at_wrong_' + box.dataset.tree)) return;
    var q = why.querySelector('.worthit-q');
    if (q) q.textContent = heading;
    why.hidden = false;
    var rep = box.querySelector('.worthit-report');
    if (rep) rep.setAttribute('aria-expanded', 'true');
  }
  function reportDone(box) {
    show(box, '.worthit-why', false);
    show(box, '.worthit-report', false);
    show(box, '.worthit-thanks', true);
    show(box, '.worthit-more', true);
  }
  document.querySelectorAll('.worthit').forEach(paint);
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('.worthit-btn, .worthit-chip, .worthit-report');
    if (!btn || btn.classList.contains('worthit-chip-link')) return;
    var box = btn.closest('.worthit');
    if (!box) return;
    var tree = box.dataset.tree;

    if (btn.classList.contains('worthit-report')) {
      var why = box.querySelector('.worthit-why');
      var open = why && why.hidden;
      if (why) {
        var q = why.querySelector('.worthit-q');
        if (q) q.textContent = "What's wrong?";
        why.hidden = !open;
      }
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      return;
    }

    if (btn.classList.contains('worthit-btn')) {
      var vkey = 'at_worthit_' + tree;
      var cur = localStorage.getItem(vkey);
      var vote = btn.dataset.vote;
      if (cur === vote) {
        // Accidental or changed mind: undo writes a compensating row, so the
        // tally nets out without anonymous deletes.
        localStorage.removeItem(vkey);
        send(box, 'vote undone', cur === 'up' ? 'worth it' : 'not worth it');
        paint(box);
        return;
      }
      if (cur) send(box, 'vote undone', cur === 'up' ? 'worth it' : 'not worth it');
      localStorage.setItem(vkey, vote);
      send(box, vote === 'up' ? 'worth it' : 'not worth it', '');
      paint(box);
      // The app-store convention: the vote already counted; the why is an
      // optional follow-up, never an interrogation.
      if (vote === 'down') openWhy(box, 'Care to say why? (optional)');
      return;
    }

    var rkey = 'at_wrong_' + tree;
    if (localStorage.getItem(rkey)) { reportDone(box); return; }
    localStorage.setItem(rkey, btn.dataset.reason);
    send(box, 'report', btn.dataset.reason);
    reportDone(box);
  });
})();
</script>
```

Also update the file's header comment: the thumbs are now toggles with undo and a post-down-vote optional why (Hidde 2026-08-21, revising his 2026-08-16 split knowingly; the split's core survives: the standalone report button stays and voting never requires a reason).

- [ ] **Step 2: Change `.worthit-done` copy** in `WorthIt.astro` from `Thanks, counted.` to `Thanks, counted. Tap again to undo.`

- [ ] **Step 3: Add the selected state** to `site/public/assets/style.css`, next to the existing `.worthit-btn` rules (~line 1104):

```css
.worthit-btn.is-on { border-color: var(--moss); box-shadow: inset 0 0 0 1px var(--moss); }
.worthit-btn[aria-pressed="true"]:hover { border-color: var(--moss); }
```

- [ ] **Step 4: Commit**

```bash
git add site/src/lib/worthit-js.ts site/src/components/WorthIt.astro site/public/assets/style.css
git commit -m "Worth-it thumbs toggle: select, unpress to undo, down-vote offers the why"
```

---

### Task 4: Digest treats undo rows as bookkeeping

**Files:**
- Modify: `scripts/daily_digest.py` (the two submission loops in `product_section`)

**Interfaces:**
- Consumes: `why` starting with `"vote undone"` from Task 3.

- [ ] **Step 1:** In the series loop (the one that starts `rows_, _ = _supa("/rest/v1/submissions?select=id,created_at,kind,city,tree,why", key)`), add directly under the TEST_SUBMISSION_IDS check:

```python
            if (r.get("why") or "").startswith("vote undone"):
                continue  # a cancelled vote is bookkeeping, not feedback
```

- [ ] **Step 2:** In the totals loop's Submissions dedupe block, add the same two lines directly under `allrows = [r for r in allrows if r.get("id") not in TEST_SUBMISSION_IDS]`, as a filter:

```python
                allrows = [r for r in allrows
                           if not (r.get("why") or "").startswith("vote undone")]
```

- [ ] **Step 3: Verify and commit**

```bash
python3 -m py_compile scripts/daily_digest.py
git add scripts/daily_digest.py
git commit -m "Digest: a cancelled vote is bookkeeping, never feedback"
```

---

### Task 5: App contribute form: the same email field

**Files:**
- Modify: `ios/AncientTrees/AncientTrees/Kit/Submissions.swift`
- Modify: `ios/AncientTrees/AncientTrees/Screens/Contribute.swift`

**Interfaces:**
- Consumes: `email` column (Task 1). Same resilience: email is only included when filled; if the insert fails with it, retry without.

- [ ] **Step 1:** In `Submissions.swift`, add to `Draft`:

```swift
        public var email = ""
```

- [ ] **Step 2:** Replace the body-building and send logic in `send(_:from:)`:

```swift
    public static func send(_ d: Draft, from page: String?) async -> Bool {
        var body: [String: Any] = [
            "kind": d.kind.rawValue,
            "city": d.city,
            "tree": d.tree,
            "location_hint": d.locationHint,
            "why": d.why,
            "page": page as Any,
        ]
        if !d.email.isEmpty { body["email"] = d.email }
        if await post(body) { return true }
        // If the email column does not exist yet the insert fails; the tree
        // matters more than the address, so retry without it.
        if body["email"] != nil {
            body.removeValue(forKey: "email")
            return await post(body)
        }
        return false
    }

    private static func post(_ body: [String: Any]) async -> Bool {
        var r = URLRequest(url: url)
        r.httpMethod = "POST"
        r.setValue(key, forHTTPHeaderField: "apikey")
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.setValue("return=minimal", forHTTPHeaderField: "Prefer")
        r.httpBody = try? JSONSerialization.data(withJSONObject: body)
        guard let (_, resp) = try? await URLSession.shared.data(for: r),
              let http = resp as? HTTPURLResponse else { return false }
        return (200..<300).contains(http.statusCode)
    }
```

- [ ] **Step 3:** In `Contribute.swift`, add a new Section between the why-section and the send-button Section:

```swift
                    Section {
                        TextField("Email, if you want to hear back", text: $draft.email)
                            .keyboardType(.emailAddress)
                            .textInputAutocapitalization(.never)
                            .autocorrectionDisabled()
                    } footer: {
                        Text("Optional. Leave it so we can ask a question if we need to, and tell you what your tip changed. We use it for nothing else.")
                    }
```

- [ ] **Step 4: Commit**

```bash
git add ios/AncientTrees/AncientTrees/Kit/Submissions.swift ios/AncientTrees/AncientTrees/Screens/Contribute.swift
git commit -m "App contribute: the same optional email field as the web form"
```

(App build + screens verified in Task 10 via appsweep.)

---

### Task 6: App worth-it control, born as the toggle design

**Files:**
- Create: `ios/AncientTrees/AncientTrees/Kit/WorthIt.swift`
- Modify: `ios/AncientTrees/AncientTrees/Screens/TreeDetail.swift` (insert the view)

**Interfaces:**
- Consumes: `Submission` static url/key from `Submissions.swift`; `Tree` (fields `id`, `city`, `name`); `ContributeView(about:)` for "Something else".
- Produces: the same submission rows as the web control, byte-compatible `why` values, so Step 0b and the digest need nothing app-specific.

- [ ] **Step 1: Write `Kit/WorthIt.swift`**

```swift
// "Worth the visit?" on the app, born with the toggle design the web control
// got the same day (Hidde, 2026-08-21): press selects and counts, press again
// undoes, a down-vote offers the optional why-chips. Same Supabase rows as
// the web control, so the pipeline behind it cannot tell the surfaces apart.
import SwiftUI

struct WorthItView: View {
    let tree: Tree

    @AppStorage private var vote: String
    @State private var whyOpen = false
    @State private var reported: Bool
    @State private var showForm = false

    init(tree: Tree) {
        self.tree = tree
        _vote = AppStorage(wrappedValue: "", "at_worthit_\(tree.id)")
        _reported = State(initialValue:
            UserDefaults.standard.string(forKey: "at_wrong_\(tree.id)") != nil)
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack(spacing: 10) {
                Text("Been here? Worth the visit?")
                    .font(.subheadline.weight(.semibold))
                thumb("up", "hand.thumbsup")
                thumb("down", "hand.thumbsdown")
            }
            if !vote.isEmpty {
                Text("Thanks, counted. Tap again to undo.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            if whyOpen && !reported {
                Text("Care to say why? (optional)")
                    .font(.footnote.weight(.semibold))
                chipRow
            }
        }
        .sheet(isPresented: $showForm) { ContributeView(about: tree) }
    }

    private func thumb(_ dir: String, _ icon: String) -> some View {
        Button {
            if vote == dir {
                send("vote undone", vote == "up" ? "worth it" : "not worth it")
                vote = ""
                whyOpen = false
                return
            }
            if !vote.isEmpty {
                send("vote undone", vote == "up" ? "worth it" : "not worth it")
            }
            vote = dir
            send(dir == "up" ? "worth it" : "not worth it", nil)
            whyOpen = (dir == "down")
        } label: {
            Image(systemName: vote == dir ? icon + ".fill" : icon)
                .frame(minWidth: 44, minHeight: 44)
        }
        .buttonStyle(.bordered)
        .tint(vote == dir ? Color("Moss") : .secondary)
        .accessibilityLabel(dir == "up"
            ? "Yes, \(tree.name) was worth the visit"
            : "No, \(tree.name) was not worth the visit")
        .accessibilityAddTraits(vote == dir ? .isSelected : [])
    }

    private var chipRow: some View {
        FlowChips {
            chip("It's dead or gone", "dead or gone")
            chip("Wrong location", "wrong location")
            chip("Couldn't reach it", "could not reach it")
            Button("Something else") { showForm = true }
                .buttonStyle(.bordered).controlSize(.small)
        }
    }

    private func chip(_ label: String, _ reason: String) -> some View {
        Button(label) {
            UserDefaults.standard.set(reason, forKey: "at_wrong_\(tree.id)")
            reported = true
            whyOpen = false
            send("report", reason)
        }
        .buttonStyle(.bordered).controlSize(.small)
    }

    private func send(_ verdict: String, _ reason: String?) {
        let why = reason.map { "\(verdict): \($0)" } ?? verdict
        Task {
            _ = await Submission.sendFeedback(city: tree.city,
                                              tree: "\(tree.id) (\(tree.name))",
                                              why: why)
        }
    }
}

/// A wrapping HStack for the chips, so they fit a 375 point screen.
struct FlowChips<Content: View>: View {
    @ViewBuilder var content: Content
    var body: some View {
        // Two rows at most at these sizes; a simple wrapping layout.
        ViewThatFits(in: .horizontal) {
            HStack(spacing: 6) { content }
            VStack(alignment: .leading, spacing: 6) { content }
        }
    }
}
```

And add to `Submissions.swift` (kind `feedback` exists in the table but not in the app's Kind enum, which drives the form picker; a raw sender keeps the enum honest):

```swift
    /// The worth-it control's channel: kind 'feedback', same shape as the
    /// web control's rows, so the pipeline cannot tell the surfaces apart.
    public static func sendFeedback(city: String, tree: String, why: String) async -> Bool {
        await post([
            "kind": "feedback",
            "city": city,
            "tree": tree,
            "why": why,
            "page": "app" as Any,
        ])
    }
```

(If `Color("Moss")` is not an asset in Assets.xcassets, check with `grep -r "Moss" ios/AncientTrees/AncientTrees/Assets.xcassets` and match whatever accent tint the app's other controls use instead; the 2026-08-20 sweep fixed the app's tint to moss, so an asset or a shared accent almost certainly exists.)

- [ ] **Step 2:** In `TreeDetail.swift`, insert `WorthItView(tree: tree)` in the detail stack directly after the map card block (find `mapCard` usage in the body's VStack) with the surrounding padding the neighbouring sections use.

- [ ] **Step 3: Commit**

```bash
git add ios/AncientTrees/AncientTrees/Kit/WorthIt.swift ios/AncientTrees/AncientTrees/Kit/Submissions.swift ios/AncientTrees/AncientTrees/Screens/TreeDetail.swift
git commit -m "App gets the worth-it control, born as toggles with undo and the optional why"
```

---

### Task 7: scripts/contributor_reply.py, the transport

**Files:**
- Create: `scripts/contributor_reply.py`

**Interfaces:**
- Consumes: Task 1's columns; `data/outreach-sent.json` (do-not-contact list, daily cap tally); env `SUPABASE_SERVICE_KEY`, `OUTREACH_SMTP_HOST/PORT/USER/PASS/FROM`; `scripts/mailcheck.py` via subprocess.
- Produces: sent thank-yous (`thanked_at` set) and answers (`replied_at` set); appends every send to `data/outreach-sent.json` with `"batch": "contributor-reply"`.

- [ ] **Step 1: Write the script**

```python
#!/usr/bin/env python3
"""Thank contributors and send them the run's answer. The transport half of
the contributor reply loop (spec: docs/superpowers/specs/
2026-08-21-contributor-reply-design.md; Hidde's ruling, 2026-08-21: input is
one of the core features and gets treated with care).

Two mail kinds, both from "Ancient Trees" via the outreach SMTP creds, with
standing approval given in session for exactly these two:

  THANK-YOU  templated, to any submission row with an email and no
             thanked_at. Sent once per address per day however many rows the
             double-submit left.
  ANSWER     the run-composed reply_text, to rows with an email, a
             reply_text, and no replied_at. mailcheck.py gates every one;
             a failing draft is held and printed, never sent.

DRY RUN by default; --send sends. Missing env prints and exits 0, so a CI
step can always call it. State lives in the submissions columns, so a lost
log line can never cause a double send. The do-not-contact list in
data/outreach-sent.json beats everything, and every send is appended there
so the outreach once-only guard knows these addresses too.

Never mailed: privacy-kind rows (a deletion request must not get marketing
warmth; they are printed for the session to handle) and vote-undone
bookkeeping rows.
"""
import datetime
import json
import os
import smtplib
import subprocess
import sys
import tempfile
import urllib.request
from email.message import EmailMessage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
SENT_PATH = os.path.join(ROOT, "data", "outreach-sent.json")
DAILY_CAP = int(os.environ.get("OUTREACH_DAILY_CAP", "50"))

THANKS_SUBJECT = {
    "tree": "Thank you, we received your tree tip",
    "city": "Thank you, we received your tree tip",
    "correction": "Thank you, we received your correction",
    "feedback": "Thank you, we received your report",
}

THANKS_BODY = """Thank you. Your input is very valuable: a real person telling us about a real tree is the best thing this project receives. Together we're building the best database of remarkable trees there is, and the point of it all is getting people outside, standing in front of something old and epic.

We check everything against independent sources, so give us a little time. We'll come back to you with what your input changed. And please feel free to send more: a tree you love, a correction, a photo. They all make the map better.

Ancient Trees
https://ancienttrees.app
"""


def supa(path, key, method="GET", body=None):
    req = urllib.request.Request(SUPA + path, method=method, headers={
        "apikey": key, "Authorization": "Bearer " + key,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(req, data=data, timeout=30) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


def mailcheck_ok(text):
    """Run mailcheck.py on the draft; nonzero exit means hold it."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write("draft\n---\n" + text)
        path = f.name
    try:
        out = subprocess.run([sys.executable,
                              os.path.join(ROOT, "scripts", "mailcheck.py"),
                              path], capture_output=True, text=True, timeout=60)
        return out.returncode == 0, out.stdout.strip()
    finally:
        os.unlink(path)


def main():
    really = "--send" in sys.argv
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        print("contributor_reply: SUPABASE_SERVICE_KEY absent, nothing to do")
        return 0
    creds = {k: os.environ.get("OUTREACH_" + k) for k in
             ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "FROM")}
    if really and not all(creds.values()):
        print("contributor_reply: SMTP env missing (%s); dry run only"
              % ", ".join(k for k, v in creds.items() if not v))
        really = False

    try:
        sent_log = json.load(open(SENT_PATH))
    except Exception:
        sent_log = {"sent": []}
    today = datetime.date.today().isoformat()
    sent_today = sum(1 for s in sent_log["sent"] if s.get("date") == today)
    dnc = {a.lower().strip() for a in sent_log.get("do_not_contact", [])}

    rows = supa("/rest/v1/submissions?select=id,created_at,kind,city,tree,"
                "why,email,outcome,reply_text,thanked_at,replied_at"
                "&email=not.is.null&order=created_at.asc", key)
    rows = [r for r in rows or [] if (r.get("email") or "").strip()]

    jobs = []  # (row, subject, body, column_to_stamp)
    thanked_addrs = set()
    for r in rows:
        addr = r["email"].strip().lower()
        why = (r.get("why") or "")
        if r.get("kind") == "privacy":
            print("PRIVACY row %s from %s: handle in session, never auto-mail"
                  % (r["id"], addr))
            continue
        if why.startswith("vote undone"):
            continue
        if not r.get("thanked_at") and addr not in thanked_addrs:
            subj = THANKS_SUBJECT.get(r.get("kind"), THANKS_SUBJECT["feedback"])
            jobs.append((r, subj, THANKS_BODY, "thanked_at"))
            thanked_addrs.add(addr)
        if r.get("reply_text") and not r.get("replied_at"):
            ok, report = mailcheck_ok(r["reply_text"])
            if not ok:
                print("HOLD reply for row %s: mailcheck says:\n%s"
                      % (r["id"], report))
                continue
            jobs.append((r, "About what you sent us: %s" % (r.get("tree") or
                         r.get("city") or "your tip"), r["reply_text"],
                         "replied_at"))

    server = None
    for r, subject, body, stamp in jobs:
        addr = r["email"].strip()
        low = addr.lower()
        if low in dnc or ("@" + low.split("@")[-1]) in dnc:
            print("SKIP %s: on the do-not-contact list, never overridden" % low)
            continue
        if sent_today >= DAILY_CAP:
            print("HOLD %s: daily cap of %d reached" % (low, DAILY_CAP))
            break
        if not really:
            print("DRY  would send %r to %s (then set %s on row %s)"
                  % (subject, low, stamp, r["id"]))
            continue
        msg = EmailMessage()
        msg["From"] = creds["FROM"]
        msg["To"] = addr
        msg["Subject"] = subject
        msg.set_content(body)
        if server is None:
            server = smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]),
                                  timeout=30)
            server.starttls()
            server.login(creds["SMTP_USER"], creds["SMTP_PASS"])
        server.send_message(msg)
        sent_today += 1
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # Stamp every row of this address needing this stamp, so the
        # double-submit's siblings are covered by the one mail.
        if stamp == "thanked_at":
            supa("/rest/v1/submissions?email=eq.%s&thanked_at=is.null"
                 % urllib.parse.quote(addr), key, "PATCH", {"thanked_at": now})
        else:
            supa("/rest/v1/submissions?id=eq.%s" % r["id"], key, "PATCH",
                 {"replied_at": now})
        sent_log["sent"].append({"date": today, "to": addr,
                                 "outlet": "contributor",
                                 "subject": subject,
                                 "batch": "contributor-reply"})
        json.dump(sent_log, open(SENT_PATH, "w"), ensure_ascii=False, indent=1)
        print("SENT %r to %s" % (subject, low))
    if server:
        server.quit()
    if not jobs:
        print("contributor_reply: nothing waiting")
    return 0


if __name__ == "__main__":
    import urllib.parse  # used in the PATCH by address
    sys.exit(main())
```

Move the `import urllib.parse` to the top imports (it reads clearer there); the code above flags it so it is not forgotten.

- [ ] **Step 2: Verify**

```bash
python3 -m py_compile scripts/contributor_reply.py
python3 scripts/contributor_reply.py
```
Expected without env: `contributor_reply: SUPABASE_SERVICE_KEY absent, nothing to do`, exit 0.

- [ ] **Step 3: Commit**

```bash
git add scripts/contributor_reply.py
git commit -m "contributor_reply.py: the thank-you and the answer, with the outreach guardrails"
```

---

### Task 8: Wire it into CI

**Files:**
- Modify: `.github/workflows/data-digest.yml` (new step before the commit step; extend that step's `git add` with `data/outreach-sent.json`)
- Modify: `.github/workflows/nightly.yml` (same new step before the run step that has SUPABASE_SERVICE_KEY, ~line 144)

**Interfaces:**
- Consumes: `scripts/contributor_reply.py` (Task 7); repo secrets `OUTREACH_SMTP_HOST/PORT/USER/PASS/FROM` (FOR HIDDE, do not exist yet; the script degrades to a printed dry run until they do).

- [ ] **Step 1:** Add to `data-digest.yml`, after "Stock the staging shelf" and before "Commit if there is a new entry":

```yaml
      - name: Thank and answer contributors
        env:
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
          OUTREACH_SMTP_HOST: ${{ secrets.OUTREACH_SMTP_HOST }}
          OUTREACH_SMTP_PORT: ${{ secrets.OUTREACH_SMTP_PORT }}
          OUTREACH_SMTP_USER: ${{ secrets.OUTREACH_SMTP_USER }}
          OUTREACH_SMTP_PASS: ${{ secrets.OUTREACH_SMTP_PASS }}
          OUTREACH_FROM: ${{ secrets.OUTREACH_FROM }}
        run: python3 scripts/contributor_reply.py --send
```

Then read the existing commit step and add `data/outreach-sent.json` to whatever it `git add`s, so a send's log line rides the digest commit.

- [ ] **Step 2:** Add the identical step to `nightly.yml` immediately before the run step at ~line 144, plus its own commit tail because the night run commits separately:

```yaml
      - name: Thank and answer contributors
        env:
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
          OUTREACH_SMTP_HOST: ${{ secrets.OUTREACH_SMTP_HOST }}
          OUTREACH_SMTP_PORT: ${{ secrets.OUTREACH_SMTP_PORT }}
          OUTREACH_SMTP_USER: ${{ secrets.OUTREACH_SMTP_USER }}
          OUTREACH_SMTP_PASS: ${{ secrets.OUTREACH_SMTP_PASS }}
          OUTREACH_FROM: ${{ secrets.OUTREACH_FROM }}
        run: |
          python3 scripts/contributor_reply.py --send
          if ! git diff --quiet data/outreach-sent.json; then
            git config user.name "claude[bot]"
            git config user.email "41898282+claude[bot]@users.noreply.github.com"
            git add data/outreach-sent.json
            git commit -m "Contributor replies sent, log updated"
            git push
          fi
```

(qa.py's `check_no_strategy_in_workflows` allows this: it is mechanics, no phase or strategy words.)

- [ ] **Step 3: Verify and commit**

```bash
python3 - <<'EOF'
import yaml
for p in (".github/workflows/data-digest.yml", ".github/workflows/nightly.yml"):
    yaml.safe_load(open(p))
    print(p, "parses")
EOF
git add .github/workflows/data-digest.yml .github/workflows/nightly.yml
git commit -m "CI thanks and answers contributors at the digest and each knock"
```
(If PyYAML is absent locally, `python3 -c "import yaml"` fails; then verify by pushing and watching the workflow parse on GitHub instead.)

---

### Task 9: Privacy page, and the Step 0b contract for runs

**Files:**
- Modify: `site/src/pages/privacy.astro`
- Modify: `CLAUDE.md` (Step 0b)

- [ ] **Step 1:** Read `privacy.astro` and add one factual paragraph where the page describes what we store:

```html
  <p>If you leave an email address with a submission, we keep it only to reply about that submission: to thank you, ask a question if we need to, and tell you what your tip changed. It is never shown anywhere on the site, never used for anything else, and removed if you ask (choose the privacy option on the <a href="/contribute">contribute form</a>).</p>
```

- [ ] **Step 2:** In `CLAUDE.md` Step 0b, after the numbered submission-handling list, add:

```markdown
**Closing the loop (Hidde, 2026-08-21: input is core and never dismissed).** After verifying a submission, the run records what happened and, when the reader left an email, writes their answer:

- Set `outcome` on the row via the service key: `changed`, `holds`, or `open_question`.
- When `email` is present, compose `reply_text` on the row: one short specific paragraph from the verification record. `changed` says what changed, with the page link. `holds` shows the work and ends in a question back, never "you were wrong": the reader stood there and we did not. `open_question` asks for the specific missing piece (which tree, a photo, a girth). Every reply ends by inviting the answer through /contribute (link prefilled with the tree) and more input generally. `scripts/contributor_reply.py` transports it; the run never sends mail itself.
- Rows whose `why` starts with `vote undone` are bookkeeping: mark them processed, verify nothing, mail nothing.
- A second report on an already-checked tree reopens the question rather than being waved off with the earlier verdict.
- Log the exchange in the tree's `verify_notes`, so the next run continues the thread instead of restarting it.
```

- [ ] **Step 3: Commit**

```bash
git add site/src/pages/privacy.astro CLAUDE.md
git commit -m "Privacy states the email facts; Step 0b closes the loop with outcome and reply_text"
```

---

### Task 10: Push, verify with eyes, log, and the FOR HIDDE list

- [ ] **Step 1: Push everything**

```bash
git pull --rebase --autostash && git push
```

- [ ] **Step 2: Watch CI**

```bash
gh run list -L 3
gh run watch <build-run-id> --exit-status
```
Expected: Build and deploy green, Smoke test green (the 375px fit check covers the new form field and control states).

- [ ] **Step 3: Web eyes pass** (per-change eyes rule). In the browser preview open the deployed site at 375px and desktop:
- `/contribute`: email field renders with its hint; press Send twice fast on an empty-city form does nothing; a filled form disables the button and shows Sending on it.
- Any tree page: thumb press shows the selected state and "Tap again to undo."; second press clears it; down-vote unfolds "Care to say why? (optional)" chips; the standalone "Something's wrong" button still opens the chips with "What's wrong?".
- Screenshot both for the report.

- [ ] **Step 4: App eyes pass**

```bash
python3 scripts/appsweep.py
python3 scripts/appfit.py
```
Look at the tree-detail and contribute screens on the SE-size device: the worth-it control fits 375 points, thumbs are 44 points, chips wrap, email field and footer render. appfit must have nothing new to say.

- [ ] **Step 5: Live round trip (only if Hidde has pasted the SQL by now).** Submit a test through the deployed form with a real email, run `python3 scripts/contributor_reply.py` locally with the service key for a dry run, confirm it lists the thank-you, then delete the test row or mark it in TEST_SUBMISSION_IDS in `scripts/daily_digest.py`.

- [ ] **Step 6: LOG.md entry**, newest first, with the FOR HIDDE block:

```markdown
FOR HIDDE, two pastes and the loop is live:
1. Supabase SQL editor: run supabase/contributor-reply.sql (adds email/outcome/reply columns to submissions).
2. GitHub repo settings, Actions secrets: add OUTREACH_SMTP_HOST, OUTREACH_SMTP_PORT, OUTREACH_SMTP_USER, OUTREACH_SMTP_PASS, OUTREACH_FROM (same values as your local outreach setup). Until then the CI step prints a dry run and sends nothing.
```

- [ ] **Step 7: Final commit and push**

```bash
git add LOG.md
git commit -m "Contributor reply loop: log entry and the FOR HIDDE pastes"
git pull --rebase --autostash && git push
```
