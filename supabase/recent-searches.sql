-- Recent searches: the last places, trees and species a signed-in person
-- PICKED from a search field, shown under the empty field on every surface
-- (Hidde approved the design and this table on 2026-11-04: "i like all your
-- proposals please build"; hard list 1, a new account table needs his yes).
--
-- Paste this once into the Supabase SQL editor (dashboard > SQL) and run it.
-- Everything in it is idempotent; running it twice is safe. Until it is
-- pasted, the web and the app get 404 from the REST endpoint and simply draw
-- no Recent section.
--
-- Design notes:
-- * primary key (user_id, kind, key): picking the same thing again only moves
--   it to the top. Clients upsert against exactly this conflict target with
--   searched_at = now().
-- * kind is city | country | species | tree | place; key is the slug, the
--   name, or for a real place "lat,lng"; label and sub are what the row draws.
--   Only results the person picked are stored, never half-typed text.
-- * Clients read the newest five within 90 days; older rows are never shown
--   and are deleted by the client's read (below) or by anyone running the
--   cleanup statement at the bottom.
-- * references auth.users on delete cascade: deleting the account removes
--   every row (account deletion stays end to end).
-- * RLS: a person reads, writes and deletes only their own rows. The anon
--   key can do nothing here, so the grant leaves anon out.

create table if not exists public.recent_searches (
  user_id     uuid not null default auth.uid() references auth.users (id) on delete cascade,
  kind        text not null check (kind in ('city', 'country', 'species', 'tree', 'place')),
  key         text not null,
  label       text not null default '',
  sub         text not null default '',
  searched_at timestamptz not null default now(),
  primary key (user_id, kind, key)
);

create index if not exists recent_searches_newest
  on public.recent_searches (user_id, searched_at desc);

alter table public.recent_searches enable row level security;

drop policy if exists "own recent searches select" on public.recent_searches;
create policy "own recent searches select" on public.recent_searches
  for select using (auth.uid() = user_id);

drop policy if exists "own recent searches insert" on public.recent_searches;
create policy "own recent searches insert" on public.recent_searches
  for insert with check (auth.uid() = user_id);

drop policy if exists "own recent searches update" on public.recent_searches;
create policy "own recent searches update" on public.recent_searches
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own recent searches delete" on public.recent_searches;
create policy "own recent searches delete" on public.recent_searches
  for delete using (auth.uid() = user_id);

-- Supabase no longer grants API access to new tables automatically
-- (2026-10-30): the roles that need it, and only those.
grant select, insert, update, delete on public.recent_searches to authenticated;
grant select, insert, update, delete on public.recent_searches to service_role;

-- Entries older than 90 days are never shown; this removes them for everyone.
delete from public.recent_searches where searched_at < now() - interval '90 days';
