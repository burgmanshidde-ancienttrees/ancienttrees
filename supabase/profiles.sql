-- Who somebody is, and who follows whom.
--
-- Hidde, 2026-08-26, on being told that a display name, a profile photograph
-- and a follow graph are new personal data and therefore his call under the
-- accounts rule (DECISIONS.md 2026-08-14): "ja bouw allemaal maar ... extra
-- persoonsgegevens moet gewoon." That is the yes this file needed, and it is
-- recorded here because the rule it clears is written down.
--
-- WHAT THIS STORES, exactly, and nothing else: a display name, a link to an
-- avatar image, and rows saying that one account follows another. No real
-- name is required, no location, no age, no contacts. A profile is created
-- the moment somebody sets a name and not before, so an account that never
-- touches this has no row here at all.
--
-- DELETION IS THE CONDITION HE SET IN JULY AND IT STILL HOLDS. Everything
-- below cascades off auth.users, so deleting an account really does take the
-- profile, the avatar row and every follow in both directions with it.

create table if not exists public.profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null check (char_length(display_name) between 1 and 40),
  avatar_url text,
  -- Kilometres or miles, one answer per person for both surfaces.
  --
  -- The app has written this column since the profile rebuild of 2026-08-21
  -- (Profiles.saveUnits) and the table never had it: either it was added to
  -- the live database by hand or every one of those writes has been failing
  -- quietly. Added here 2026-09-12 so the file and the app agree, and so the
  -- website can read the same answer instead of guessing a second time.
  --
  -- Null is not "metric", it is "nobody has said", and both surfaces then
  -- fall back to where the reader is: the phone's locale in the app, the
  -- browser's region on the website. Only an explicit choice writes a value.
  units text check (units in ('km', 'mi')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Safe to run against a table that already exists.
alter table public.profiles add column if not exists units text;
do $$ begin
  alter table public.profiles add constraint profiles_units_check
    check (units in ('km', 'mi'));
exception when duplicate_object then null; end $$;

alter table public.profiles enable row level security;

-- A profile is PUBLIC to signed-in readers, because that is what following
-- means: you cannot follow somebody you cannot see. It is writable only by
-- the person it belongs to.
drop policy if exists "profiles are readable" on public.profiles;
create policy "profiles are readable" on public.profiles
  for select using (true);

drop policy if exists "own profile is writable" on public.profiles;
create policy "own profile is writable" on public.profiles
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create table if not exists public.follows (
  follower uuid not null references auth.users(id) on delete cascade,
  followee uuid not null references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (follower, followee),
  -- Nobody follows themselves.
  check (follower <> followee)
);

alter table public.follows enable row level security;

drop policy if exists "follows are readable" on public.follows;
create policy "follows are readable" on public.follows
  for select using (true);

-- You may only create and delete YOUR OWN following. Being followed is not
-- something you do, so there is no policy that lets anybody write a row on
-- somebody else's behalf.
drop policy if exists "own follows are writable" on public.follows;
create policy "own follows are writable" on public.follows
  for insert with check (auth.uid() = follower);

drop policy if exists "own follows are removable" on public.follows;
create policy "own follows are removable" on public.follows
  for delete using (auth.uid() = follower);

-- The two numbers the profile row shows, counted server-side so a client
-- never has to read the graph to count it.
create or replace function public.follow_counts(uid uuid)
returns table (followers bigint, following bigint)
language sql
security definer
set search_path = public
stable
as $$
  select
    (select count(*) from public.follows where followee = uid)::bigint,
    (select count(*) from public.follows where follower = uid)::bigint
$$;

revoke all on function public.follow_counts(uuid) from public;
grant execute on function public.follow_counts(uuid) to anon, authenticated;

-- AVATARS live in a storage bucket rather than in this table, and the bucket
-- is the one part that costs money and carries a moderation duty: people can
-- put anything in an image. Create it once in the Supabase dashboard under
-- Storage, named `avatars`, public read, and add these two policies so a
-- person may only write their own file:
--
--   insert: bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text
--   update: bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text
--
-- The app writes avatars/<user-id>/avatar.jpg, so one person owns one folder
-- and deleting the account's row here leaves nothing pointing at it.
