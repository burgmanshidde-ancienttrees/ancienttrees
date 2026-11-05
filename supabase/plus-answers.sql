-- The Ancient Trees Plus question.
--
-- Hidde, 2026-11-04: "het ziet er eigenlijk goed uit zo bouw maar", after a
-- session of working out what a paid tier could be (walks for a city trip,
-- offline maps, seasonal alerts, a richer tree log). Nothing is sold: a row on
-- every city page and in the app's settings asks, in three steps, what would
-- make Plus worth paying for (open field first, so nobody copies our list),
-- which one or two of four would come first (shuffled per person, "none of these" last),
-- and whether to tell them when it is here.
--
-- TWO TABLES, because the answer and the hand that goes up are different
-- things:
--
-- plus_answers: ANONYMOUS. No user id, no email, no session, no IP column.
-- What was chosen, the free text, the order the options were shown in (so
-- position bias can be read), the surface, language, city and where the
-- question was opened. Anon and authenticated may insert; nobody but the
-- service key reads. Read by scripts/plus_answers.py.
--
-- plus_waitlist: ONE ROW PER ACCOUNT that pressed "Tell me", so we can mail
-- them when Plus exists. It holds the account id and the time, nothing else
-- (the address stays where it already is, in auth). Signed in only; you may
-- read and delete your own row. Hidde agreed to this in the same session
-- (the "Tell me" step was in the design he approved).
--
-- GRANTS in this file (Supabase stopped granting API access to new tables on
-- 2026-10-30). Paste the whole file into the Supabase SQL editor once; it is
-- safe to run again.

create table if not exists public.plus_answers (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  surface text not null check (surface in ('web', 'app')),
  lang text not null default 'en' check (char_length(lang) <= 5),
  city text not null default '' check (char_length(city) <= 80),
  opened_from text not null default '' check (char_length(opened_from) <= 20),
  -- Up to two (Hidde, 2026-11-05: "max 2 invullen is goed"); "none" stands alone.
  choices text[] not null check (
    cardinality(choices) between 1 and 2
    and choices <@ array['walks', 'offline', 'season', 'log', 'none']::text[]
    and (not ('none' = any(choices)) or cardinality(choices) = 1)
  ),
  idea text not null default '' check (char_length(idea) <= 600),
  shown_order text not null default '' check (char_length(shown_order) <= 60),
  build text not null default '' check (char_length(build) <= 40)
);

alter table public.plus_answers enable row level security;

drop policy if exists "anybody may answer the plus question" on public.plus_answers;
create policy "anybody may answer the plus question" on public.plus_answers
  for insert to anon, authenticated
  with check (created_at > now() - interval '1 hour');

revoke all on public.plus_answers from anon, authenticated;
grant insert on public.plus_answers to anon, authenticated;
grant all on public.plus_answers to service_role;

create table if not exists public.plus_waitlist (
  user_id uuid primary key default auth.uid() references auth.users (id) on delete cascade,
  created_at timestamptz not null default now()
);

alter table public.plus_waitlist enable row level security;

drop policy if exists "you may put yourself on the plus list" on public.plus_waitlist;
create policy "you may put yourself on the plus list" on public.plus_waitlist
  for insert to authenticated
  with check (auth.uid() = user_id);

drop policy if exists "you may see your own place on the plus list" on public.plus_waitlist;
create policy "you may see your own place on the plus list" on public.plus_waitlist
  for select to authenticated
  using (auth.uid() = user_id);

drop policy if exists "you may take yourself off the plus list" on public.plus_waitlist;
create policy "you may take yourself off the plus list" on public.plus_waitlist
  for delete to authenticated
  using (auth.uid() = user_id);

revoke all on public.plus_waitlist from anon, authenticated;
grant select, insert, delete on public.plus_waitlist to authenticated;
grant all on public.plus_waitlist to service_role;
