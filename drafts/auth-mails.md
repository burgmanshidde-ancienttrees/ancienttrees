# The two account mails, ready to paste (2026-09-24)

Hidde's list: "De magic link mail benchmarken en maken, ziet er niet uit" and
"Een eerste mail als je je account aanmaakt benchmarken en maken". Both mails
are sent by Supabase, not by us, so both live in his dashboard. Editing them
needs custom SMTP first, which is the step parked in September as "option A"
(archive/LOG-2026-09.md): the same Gmail app password `OUTREACH_SMTP_*`
already uses, so it is a setting and not a new service.

**Why it is worth ten minutes at a desk, beyond looks:** Supabase's built-in
sender only delivers to the project's own team addresses and a couple of
messages an hour. Until SMTP is set, "Email me a sign-in link" may never have
reached a stranger at all. Custom SMTP fixes that, the look, and unlocks the
six-digit code the app's email sign-in is waiting for, in one go.

## What the references do (benchmark, from memory of their mails, not fetched)

| Product | Subject | Body |
|---|---|---|
| Slack | "Your Slack confirmation code" | Logo, one line, the code large, "expires in 10 minutes", ignore-line |
| Notion | "Your Notion login code" | One line, a link button AND a code, ignore-line |
| Medium | "Sign in to Medium" | One sentence, one button, "link works once, expires", ignore-line |
| AllTrails (welcome) | "Welcome to AllTrails" | Hero photo, one line about what you can do now, one button to explore nearby |
| Strava (welcome) | "Welcome to Strava" | Name, three short things to do first, one primary button |

The pattern is the same everywhere: the subject says exactly what it is, the
action sits in the first screen, the code is readable at a glance, one line
for somebody who did not ask for it. No marketing in a sign-in mail. A welcome
mail is the one place a picture and a single "go outside" nudge belong.

## Steps in the dashboard

1. Supabase, Project Settings, Auth, SMTP Settings: host `smtp.gmail.com`,
   port 465, user and password as in `OUTREACH_SMTP_*`, sender name
   "Ancient Trees".
2. Auth, Email Templates, **Magic Link**: paste template 1.
3. Auth, Email Templates, **Confirm signup**: paste template 2. This mail goes
   to every new account once, so it IS the first mail; no extra sender needed.
4. Say "SMTP staat" and a session flips `Launch.emailSignIn` so the app can
   take the six digits, and checks both surfaces land on one account.

## Template 1: Magic Link

Subject: `Your Ancient Trees sign-in link`

```html
<div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;max-width:480px;margin:0 auto;padding:32px 24px;color:#2b2b24;background:#faf8f2">
  <p style="margin:0 0 24px;font-size:15px;font-weight:600;color:#3A5222">Ancient Trees</p>
  <p style="margin:0 0 20px;font-size:17px;line-height:1.5">Tap the button to sign in.</p>
  <p style="margin:0 0 24px">
    <a href="{{ .ConfirmationURL }}" style="display:inline-block;background:#4A6B2A;color:#ffffff;text-decoration:none;font-size:16px;font-weight:600;padding:14px 28px;border-radius:999px">Sign in</a>
  </p>
  <p style="margin:0 0 8px;font-size:15px;line-height:1.5">In the app, you can type this code instead:</p>
  <p style="margin:0 0 24px;font-size:28px;letter-spacing:6px;font-weight:700;color:#3A5222">{{ .Token }}</p>
  <p style="margin:0;font-size:13px;line-height:1.5;color:#6b6b60">The link and the code work once and expire within the hour. If you did not ask to sign in, you can ignore this mail.</p>
</div>
```

## Template 2: Confirm signup (the first mail)

Subject: `Welcome to Ancient Trees`

```html
<div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;max-width:480px;margin:0 auto;padding:32px 24px;color:#2b2b24;background:#faf8f2">
  <p style="margin:0 0 24px;font-size:15px;font-weight:600;color:#3A5222">Ancient Trees</p>
  <p style="margin:0 0 16px;font-size:20px;line-height:1.35;font-weight:600">Welcome. Your account is almost ready.</p>
  <p style="margin:0 0 24px;font-size:17px;line-height:1.5">Tap the button to confirm your email. After that, the trees you save and the ones you tick off follow you from your phone to your laptop.</p>
  <p style="margin:0 0 28px">
    <a href="{{ .ConfirmationURL }}" style="display:inline-block;background:#4A6B2A;color:#ffffff;text-decoration:none;font-size:16px;font-weight:600;padding:14px 28px;border-radius:999px">Confirm my email</a>
  </p>
  <p style="margin:0 0 8px;font-size:15px;line-height:1.5">Or type this code in the app:</p>
  <p style="margin:0 0 28px;font-size:28px;letter-spacing:6px;font-weight:700;color:#3A5222">{{ .Token }}</p>
  <p style="margin:0 0 24px;font-size:15px;line-height:1.5">Then open the map and see which old trees stand near you.</p>
  <p style="margin:0;font-size:13px;line-height:1.5;color:#6b6b60">If you did not create an account, you can ignore this mail.</p>
</div>
```

Nothing here promises free, forever or always (the forever-promise rule).
