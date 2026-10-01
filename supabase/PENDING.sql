-- PENDING: one fix to walks.sql, 2026-09-26. The stop check let a stop with no
-- position through (NULL comparison). Paste this; it replaces one function and
-- is safe to run twice. Empty this file again after the rule test passes.
--
-- When a new column or table is written, put its statement here as well, with
-- `if not exists`, so one paste in the SQL editor brings the database level.
-- `python3 scripts/sqlcheck.py` asks the live database what is still missing.

create or replace function public.walk_stops_ok(s jsonb) returns boolean
language sql immutable as $$
  select jsonb_typeof(s) = 'array'
     and jsonb_array_length(s) <= 40
     and not exists (
       select 1 from jsonb_array_elements(s) e
        where jsonb_typeof(e) is distinct from 'object'
           or jsonb_typeof(e -> 'name') is distinct from 'string'
           or jsonb_typeof(e -> 'lat') is distinct from 'number'
           or jsonb_typeof(e -> 'lng') is distinct from 'number'
           or ((e ? 'treeId' and e -> 'treeId' <> 'null'::jsonb)
               = (e ? 'sightingId' and e -> 'sightingId' <> 'null'::jsonb))
     )
$$;

-- 2026-09-26: further photographs when adding a tree, app and website. Paths
-- only, private bucket, never published. Safe to run twice.
alter table public.sightings
  add column if not exists extra_photos text[]
  check (extra_photos is null or cardinality(extra_photos) <= 3);
alter table public.submissions
  add column if not exists extra_photos text[]
  check (extra_photos is null or cardinality(extra_photos) <= 3);

-- PENDING: the ambassadors table, 2026-10-02 (supabase/ambassadors.sql holds
-- the full file with its reasoning; this is the same statements). Paste once;
-- safe to run twice.
create table if not exists public.ambassadors (
  user_id uuid not null references auth.users(id) on delete cascade,
  place_slug text not null check (char_length(place_slug) between 1 and 80),
  place_name text not null check (char_length(place_name) between 1 and 80),
  public boolean not null default false,
  since date not null default current_date,
  primary key (user_id, place_slug)
);
alter table public.ambassadors enable row level security;
drop policy if exists "ambassadors are readable" on public.ambassadors;
create policy "ambassadors are readable" on public.ambassadors for select using (true);
drop policy if exists "own consent is writable" on public.ambassadors;
create policy "own consent is writable" on public.ambassadors
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
revoke update on public.ambassadors from authenticated;
grant update (public) on public.ambassadors to authenticated;
grant select on public.ambassadors to anon, authenticated;
