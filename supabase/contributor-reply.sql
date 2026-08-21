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
