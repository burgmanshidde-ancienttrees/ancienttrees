-- profiles.country (2026-10-16): the flag after your name.
--
-- Hidde, 2026-10-16, choosing option 1 of the early-adopter designs: "Ship
-- option 1 with the flag ... Yes to storing a country per account." That is
-- the explicit yes the accounts rule asks for before a new personal-data
-- column (DECISIONS.md 2026-08-14). The same lines are in profiles.sql.
--
-- WHAT THIS STORES: one ISO 3166 two-letter country code, chosen by the
-- person in Edit profile, nothing derived and never filled in for them.
-- Null means nobody said, and then no flag shows. It lives on the profile
-- row, so deleting the account deletes it with everything else.
--
-- Paste into Supabase, SQL editor, Run. Safe to run twice.

alter table public.profiles add column if not exists country text;
do $$ begin
  alter table public.profiles add constraint profiles_country_check
    check (country ~ '^[A-Z]{2}$');
exception when duplicate_object then null; end $$;
