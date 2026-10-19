-- ONE SHARED TREE BY ITS LINK, never the list (privacy audit, 2026-10-19).
-- The shared_trees view answered the public key with every shared sighting at
-- once (86 rows, with notes and exact times), so an "unlisted" link was in
-- fact listed. shared_tree() answers one id, the day only, and the view is
-- closed to the public key. Paste into Supabase, SQL editor, Run.

create or replace function public.shared_tree(tid uuid)
returns json
language sql
security definer
set search_path = public
stable
as $$
  select coalesce(json_agg(json_build_object(
    'id', s.id, 'name', s.name, 'species', s.species, 'age', s.age,
    'note', s.note, 'taken_at', s.taken_at::date, 'photo', s.photo,
    'status', s.status, 'girth_cm', s.girth_cm)), '[]'::json)
  from public.sightings s
  where s.id = tid and s.shared = true
$$;

revoke all on function public.shared_tree(uuid) from public;
grant execute on function public.shared_tree(uuid) to anon, authenticated;

revoke select on public.shared_trees from anon, authenticated;
