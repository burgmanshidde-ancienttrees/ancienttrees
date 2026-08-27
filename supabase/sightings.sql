-- The trees somebody added themselves, kept where a lost phone cannot take them.
--
-- Hidde, 2026-08-27, after losing his own trees and photographs in Baarn and
-- then seeing the backup button I built for it: "maar niemand wil een backup my
-- trees knop, je wilt gewoon dat dit automatisch goed gaat." He is right. A
-- button is a thing somebody has to remember on the one day they will not.
--
-- WHAT THIS CHANGES about a rule this project has held since 2026-08-21.
-- Sightings.swift says photographs stay on the phone, and they did, deliberately:
-- no bucket, no table, nothing of anybody's on our side. That was the right
-- default while a sighting was a note to yourself. It stopped being right the
-- moment it turned out that one wipe of one phone takes everything with it, and
-- he asked for the other behaviour by name.
--
-- WHAT IS STORED, exactly: for each tree somebody added, its name, where it is,
-- when they photographed it, and what they typed about it, plus the photograph
-- itself. Nothing more, and none of it is visible to anybody else: these are
-- readable and writable only by the account that made them, and there is no
-- policy anywhere that lets one person read another's. That is the difference
-- between this and the profiles table, and it is why this needs no moderation
-- surface: nobody but you ever sees it.
--
-- DELETION still holds, and is the reason for the cascade below. The row goes
-- with the account; the FILE has to be deleted through the Storage API by the
-- app, the same way the avatar is, because SQL may not touch storage.objects
-- (which is the fault that broke deletion entirely for an hour this morning).

create table if not exists public.sightings (
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  -- The id the phone gave it, so the same sighting on two phones is one row.
  id         uuid not null,
  -- Our tree, when it is one of ours; null when only they have it.
  tree_id    text,
  name       text not null default '' check (char_length(name) <= 120),
  note       text not null default '' check (char_length(note) <= 2000),
  species    text check (char_length(species) <= 120),
  age        text check (char_length(age) <= 60),
  lat        double precision not null,
  lng        double precision not null,
  taken_at   timestamptz not null default now(),
  status     text not null default 'mine',
  -- The file in the sightings bucket, when there is one.
  photo      text,
  updated_at timestamptz not null default now(),
  primary key (user_id, id)
);

alter table public.sightings enable row level security;

drop policy if exists "own sightings" on public.sightings;
create policy "own sightings" on public.sightings
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- The bucket. PRIVATE, unlike avatars: an avatar is meant to be seen by other
-- people and a photograph of a tree you walked to is not. It is served to its
-- owner through a signed request rather than a public url.
insert into storage.buckets (id, name, public)
  values ('sightings', 'sightings', false)
  on conflict (id) do nothing;

-- Read, write and delete your own folder, and nobody else's. The path is
-- sightings/<user id>/<sighting id>.jpg, so the first folder is the account.
drop policy if exists "own sighting photos" on storage.objects;
create policy "own sighting photos" on storage.objects
  for all to authenticated
  using (
    bucket_id = 'sightings'
    and auth.uid()::text = (storage.foldername(name))[1]
  )
  with check (
    bucket_id = 'sightings'
    and auth.uid()::text = (storage.foldername(name))[1]
  );
