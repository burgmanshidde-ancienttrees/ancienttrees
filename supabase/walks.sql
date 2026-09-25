-- Walks you made yourself, on the account from the first one.
--
-- Hidde, 2026-08-24, naming it as one of the things the app is for: "ik wil een
-- nieuwe wandelroute maken incl mijn bomen en kunnen delen." And 2026-09-26,
-- after the audit that found the first attempt (Kit/MyWalks.swift) keeping
-- walks in a file on the phone: "walks you made is for later - but just to be
-- sure already set it up properly." This is his yes under hard rule 1 for a new
-- table holding somebody's data; nothing else about the account rule changes.
--
-- So the server half exists BEFORE any screen does, and the app's store has
-- one place to write the day it is built. A walk that lives on one phone is
-- the exact failure the 2026-09-02 ruling forbids ("alles wat wordt
-- opgeslagen, moet op je account zijn").
--
-- Paste this once into the Supabase SQL editor (dashboard > SQL) and run it.
-- Everything in it is idempotent; running it twice is safe.
-- `python3 scripts/sqlcheck.py` says whether it has reached the live database.
--
-- THE SHAPE, and why:
-- * id is a uuid made by the client (the Swift model already carries one), so
--   a walk saved offline keeps its identity when it reaches the server and an
--   upsert on id is the whole sync. It also becomes the unguessable part of a
--   shared link, the same move as shared_trees.
-- * user_id references auth.users on delete cascade, which is what keeps
--   delete_user() end to end without it having to know this table exists.
-- * stops is jsonb in the Swift model's own keys (treeId, sightingId, lat,
--   lng, name), so the app decodes a row without a mapping layer. A stop is
--   one of OUR trees (treeId) or one only you have (sightingId): exactly one of
--   the two, checked below. There is no foreign key into sightings on purpose:
--   deleting a tree you added must not delete the walk it was part of, and the
--   stop keeps its own name and position so the walk still draws.
-- * shape is the routed line, [[lng, lat], ...], fetched once when the walk is
--   saved. Null means nobody routed it and the map draws the order dashed.
-- * shared defaults to FALSE. Unlike a sighting (where the thank-you mail needs
--   a working link at once), nothing sends a walk anywhere, so sharing is the
--   person's own tap.
-- * RLS all the way down: an account reads and writes its own walks only, and
--   the anon key alone can do nothing to this table.

create table if not exists public.walks (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  name       text not null check (char_length(btrim(name)) between 1 and 80),
  stops      jsonb not null default '[]'::jsonb,
  shape      jsonb,
  km         numeric(6, 2) not null default 0 check (km >= 0),
  minutes    integer not null default 0 check (minutes >= 0),
  shared     boolean not null default false,
  made_at    timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- A stop list the app can always decode: an array of at most 40 objects, each
-- with a name and a position, and exactly one of treeId / sightingId. A check
-- constraint cannot hold a subquery, so it calls an immutable function.
create or replace function public.walk_stops_ok(s jsonb) returns boolean
language sql immutable as $$
  select jsonb_typeof(s) = 'array'
     and jsonb_array_length(s) <= 40
     and not exists (
       select 1 from jsonb_array_elements(s) e
        where jsonb_typeof(e) <> 'object'
           or jsonb_typeof(e -> 'name') <> 'string'
           or jsonb_typeof(e -> 'lat') <> 'number'
           or jsonb_typeof(e -> 'lng') <> 'number'
           or ((e ? 'treeId' and e -> 'treeId' <> 'null'::jsonb)
               = (e ? 'sightingId' and e -> 'sightingId' <> 'null'::jsonb))
     )
$$;

alter table public.walks drop constraint if exists walks_stops_ok;
alter table public.walks add constraint walks_stops_ok check (public.walk_stops_ok(stops));
alter table public.walks drop constraint if exists walks_shape_ok;
alter table public.walks add constraint walks_shape_ok
  check (shape is null or jsonb_typeof(shape) = 'array');

create index if not exists walks_user_made on public.walks (user_id, made_at desc);

-- updated_at is the server's, so two devices editing one walk resolve by the
-- later write rather than by whichever clock was wrong.
create or replace function public.walks_touch() returns trigger
language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

drop trigger if exists walks_touch on public.walks;
create trigger walks_touch before update on public.walks
  for each row execute function public.walks_touch();

alter table public.walks enable row level security;

drop policy if exists "own walks select" on public.walks;
create policy "own walks select" on public.walks
  for select using (auth.uid() = user_id);

drop policy if exists "own walks insert" on public.walks;
create policy "own walks insert" on public.walks
  for insert with check (auth.uid() = user_id);

drop policy if exists "own walks update" on public.walks;
create policy "own walks update" on public.walks
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own walks delete" on public.walks;
create policy "own walks delete" on public.walks
  for delete using (auth.uid() = user_id);

grant select, insert, update, delete on public.walks to authenticated;

-- THE SHARED LINK, ready for the day the button exists. A view rather than an
-- anon policy on the table, for the reason shared-sightings.sql gives: a policy
-- would expose every column of a shared row, user_id included, and a column
-- added later would publish itself. The view names what a stranger may see.
--
-- And hard rule 10 reaches into it. A stop that is one of OUR trees is already
-- public, position and all. A stop that is one of YOURS is a tree nobody has
-- checked, possibly in somebody's garden, and shared_trees deliberately never
-- publishes its position. So here those stops lose lat and lng, and a walk
-- carrying any of them loses its routed line too, because the line runs
-- through the spot. The walk still reads as a list; it just does not lead a
-- stranger to a place we would not publish ourselves.
drop view if exists public.shared_walks;
create view public.shared_walks
  with (security_invoker = off) as
  select w.id,
         w.name,
         w.km,
         w.minutes,
         w.made_at,
         (select coalesce(jsonb_agg(
                   case when e ? 'sightingId' and e -> 'sightingId' <> 'null'::jsonb
                        then e - 'lat' - 'lng'
                        else e end order by n), '[]'::jsonb)
            from jsonb_array_elements(w.stops) with ordinality as t(e, n)) as stops,
         case when exists (select 1 from jsonb_array_elements(w.stops) e
                            where e ? 'sightingId' and e -> 'sightingId' <> 'null'::jsonb)
              then null else w.shape end as shape
    from public.walks w
   where w.shared = true;

grant select on public.shared_walks to anon, authenticated;
