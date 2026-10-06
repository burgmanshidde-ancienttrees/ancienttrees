-- Private working files: outreach logs, contacts and mail drafts.
--
-- Hidde, 2026-10-06, on finding that the public GitHub repository carried
-- 600+ email addresses of people we wrote to, their replies and the waitlist:
-- "What about supabase", then "Yes". That is the explicit yes the accounts
-- rule asks for before personal data gets a new home.
--
-- WHAT THIS STORES: data/outreach-*.json and drafts/ (OUTREACH.md, mail
-- batches), byte for byte, one row per file, keyed by its path. They
-- hold the addresses of organisations and people we mailed and what they
-- answered. Nothing a reader of the site ever sees.
--
-- WHO READS IT: only the service key (scripts/private_store.py, on Hidde's Mac
-- and in the night runs). RLS is on and there is no policy at all, so the
-- public anon key and signed-in readers get nothing.

create table if not exists public.private_files (
  path text primary key check (char_length(path) between 1 and 300),
  content text not null,
  updated_at timestamptz not null default now()
);

alter table public.private_files enable row level security;
revoke all on public.private_files from anon, authenticated;
