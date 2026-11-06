-- FOR HIDDE TO PASTE in the Supabase SQL editor (2026-11-06).
--
-- NEW FROM VISITORS, Discover's second row (Hidde, 2026-11-06: "Ja,
-- goedgekeurd", then "signed out people may see the name but to visit the
-- public profile log in"). The newest photographs visitors sent through the
-- app that went live on one of our trees, newest first: the tree, when it went
-- live, and who sent it.
--
-- WHAT EACH CALLER GETS
-- * Everyone (anon too): the tree id, when it went live, and the display name
--   and avatar ONLY when that profile is public (profiles.public), else null,
--   which the app and the site print as "A visitor". The same rule as
--   tree_notes_for() in tree-notes.sql.
-- * The account id only to a signed-in caller and only for a public profile,
--   so a tap on the name opens the profile; signed out, the tap asks for a
--   sign-in first (CLAUDE.md, Privacy and accounts).
--
-- NEVER OURS: Hidde's and the project's own accounts (data/our-accounts.json,
-- the sha1 of each account id, the list every script reads through
-- scripts/ours.py) are left out; our own photographs are never credited
-- (CLAUDE.md, Reader input). Add a line here when that file grows.
--
-- Reads sightings.status = 'published', which scripts/sightings_publish.py
-- writes (with updated_at) the moment a photograph goes live. Nothing new is
-- stored; no new column; no table grant, a function grant only.

create or replace function public.new_from_visitors(n int default 12)
returns table (
  sighting_id uuid,
  tree_id text,
  published_at timestamptz,
  author_name text,
  author_avatar text,
  author_id uuid
)
language sql
security definer
set search_path = public, extensions
stable
as $$
  select s.id, s.tree_id, s.updated_at,
         case when p.public then p.display_name end,
         case when p.public then p.avatar_url end,
         case when p.public and auth.uid() is not null then s.user_id end
  from public.sightings s
  left join public.profiles p on p.user_id = s.user_id
  where s.status = 'published' and s.tree_id is not null and s.photo is not null
    and encode(digest(s.user_id::text, 'sha1'), 'hex') <> all (array[
      'cc6a542385091392e455911c0d7e351bf0148a4b',
      'ef98f5dbe51e86e6236031d19bdce2364272c6b6',
      'd4e6c578be12fd0916a6277fa7bba4b482405484',
      'a9c1498c827881dd41e3e8cd39edc1a8fbf399f9'
    ])
  order by s.updated_at desc
  limit least(greatest(n, 1), 24)
$$;

revoke all on function public.new_from_visitors(int) from public;
grant execute on function public.new_from_visitors(int) to anon, authenticated;
