-- An unlisted page for a tree somebody added, so they can show it to people.
--
-- Hidde, 2026-09-02: "kunnen we niet een pagina maken van de boom die wel
-- deelbaar is?" Yes, and UNLISTED rather than public, which was his call on
-- being shown what the references do (CONVENTIONS.md, "A page for something a
-- person added, and who may see it"): Strava gives every activity a URL with a
-- visibility of its own, iNaturalist publishes every observation and obscures
-- the LOCATION rather than the record, and Google Maps publishes only after
-- review.
--
-- WHAT UNLISTED MEANS HERE, exactly:
--   * nothing is shared until the person taps Share on their own tree, which
--     flips `shared` on that one row and nothing else;
--   * the address carries the sighting's own uuid, so it cannot be guessed and
--     it is not listed anywhere on the site;
--   * the page is noindex, so it stays out of search results. An unverified
--     tree is exactly what the register-layer ruling in CLAUDE.md keeps out of
--     the index, and this changes nothing about that.
--
-- WHAT A STRANGER WITH THE LINK CAN SEE, and why it is a view rather than a
-- policy on the table: a permissive select policy for anon would expose every
-- column of a shared row, user_id included. The view names the columns instead,
-- so adding a column to `sightings` later cannot quietly publish it. The
-- position is deliberately NOT among them: hard rule 10 exists because a tree
-- can be harmed by visitors and a person's home is nobody's destination, and a
-- tree somebody photographed may be either. They are showing a tree, not
-- sending strangers to it.
--
-- Paste this in the Supabase SQL editor. It is safe to run twice.

-- DEFAULT true since 2026-09-03 (Hidde, on the thank-you mail: "standaard
-- shared bij toevoegen"): the mail that thanks somebody for a tree they just
-- added links straight to its unlisted page, and that link has to work the
-- moment the mail sends rather than only once they have separately found and
-- tapped Share. The app now sets this explicitly on every sighting it writes
-- (Kit/Sightings.swift, Kit/SightingSync.swift), so the column default below
-- is a safety net rather than the live mechanism; it still has to match, or a
-- row written by anything else silently reverts to the old opt-in reading.
-- "Stop sharing the link" in the app's own menu is how somebody takes it back.
alter table public.sightings
  add column if not exists shared boolean not null default true;
alter table public.sightings
  alter column shared set default true;

-- Only the owner may set it, which the existing "own sightings" policy already
-- enforces: it is their row, and nobody else can write it.

-- SECURITY DEFINER on purpose (security_invoker off): the whole job of this
-- view is to let somebody with no account read a row they have no policy for,
-- and the filter it applies is the permission.
drop view if exists public.shared_trees;
create view public.shared_trees
  with (security_invoker = off) as
  select id, name, species, age, note, taken_at, photo, status
    from public.sightings
   where shared = true;

grant select on public.shared_trees to anon, authenticated;

-- THE PHOTOGRAPH. The sightings bucket is private and stays private: nobody
-- but its owner may read it, and a signed url needs an account, which somebody
-- opening a shared link does not have. So a shared photograph is COPIED by the
-- app into a bucket of its own, and only the ones somebody chose to share are
-- ever in it.
insert into storage.buckets (id, name, public)
  values ('shared-sightings', 'shared-sightings', true)
  on conflict (id) do nothing;

-- Write and delete inside your own folder only, exactly like the private
-- bucket. The path is shared-sightings/<user id>/<sighting id>.jpg.
drop policy if exists "own shared photos" on storage.objects;
create policy "own shared photos" on storage.objects
  for all to authenticated
  using (
    bucket_id = 'shared-sightings'
    and auth.uid()::text = (storage.foldername(name))[1]
  )
  with check (
    bucket_id = 'shared-sightings'
    and auth.uid()::text = (storage.foldername(name))[1]
  );

-- Reading is public, because the bucket is public: that is what makes the
-- picture show up for somebody holding the link.

-- UNSHARING, for the day somebody asks: set shared = false on the row and
-- delete the file from shared-sightings. The app does both when the person
-- turns sharing off, and delete_user() plus the app's photo sweep already take
-- the rest with the account.
