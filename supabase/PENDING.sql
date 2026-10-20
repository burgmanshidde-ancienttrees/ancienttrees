-- PENDING since 2026-10-20. Safe to run twice. Explained in profiles.sql.
--
-- "DON'T SHOW" FOR THE FLAG. Until somebody chooses, the app and the website
-- give them the flag of where they appear to be; this column remembers a
-- deliberate "Don't show" so the default never comes back. Until it exists
-- nobody gets a default flag (both surfaces check for it first).
-- Paste into Supabase, SQL editor, Run.

alter table public.profiles add column if not exists flag_hidden boolean not null default false;
