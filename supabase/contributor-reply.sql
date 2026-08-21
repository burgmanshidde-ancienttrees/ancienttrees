-- Contributor reply loop, 2026-08-21.
-- Spec: docs/superpowers/specs/2026-08-21-contributor-reply-design.md
-- Hidde pastes this into the Supabase SQL editor, same routine as saves.sql.
--
-- user_id     stamped automatically when a signed-in visitor submits (the
--             form and the vote control send the user's own token since
--             2026-08-21, the Google Maps convention: feedback needs the
--             account, because the account is the reply channel). The reply
--             script resolves the address from here at send time; nothing
--             stores a second copy of the email.
-- email       legacy/fallback only: reader-given, used ONLY to reply about
--             their own submission. Never rendered anywhere. Deleted on
--             request. New forms no longer ask for it.
-- outcome     set by the run that verifies: changed | holds | open_question
-- reply_text  the answer mail's body, composed by the run, sent by
--             scripts/contributor_reply.py after mailcheck passes
-- thanked_at  when the automatic thank-you went out
-- replied_at  when the answer went out
alter table public.submissions add column if not exists user_id uuid default auth.uid();
alter table public.submissions add column if not exists email text;
alter table public.submissions add column if not exists outcome text
  check (outcome is null or outcome in ('changed', 'holds', 'open_question'));
alter table public.submissions add column if not exists reply_text text;
alter table public.submissions add column if not exists thanked_at timestamptz;
alter table public.submissions add column if not exists replied_at timestamptz;
