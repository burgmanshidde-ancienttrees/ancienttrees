-- Want to visit, as the server answers it: a save made BEFORE the tree was
-- collected is a fulfilled wish and leaves the list.
--
-- Hidde, 2026-10-19: "remove a tree from want to visit yes, because you
-- visited it". The app did that from build 1.0.4 and the website the same
-- day, but 1.0.3 went to Apple on 10-14 and still keeps the heart, and its
-- sync upserts every heart it holds, so a deleted row comes straight back.
-- A Paris reader collected five saved trees on 2026-11-02 on 1.0.3 and their
-- public profile showed three of them under Want to visit as well (Hidde:
-- "this was my whole point"). So the rule lives here, once, where every
-- build and the website read it: a save older than the collect is not a
-- wish. A heart put on a collected tree afterwards is newer than the collect
-- and stays, as the 10-19 ruling says (the website's heart writes a fresh
-- created_at for that reason; collection-js.ts).
--
-- No new data, no new column: a view over saves and visited. security_invoker
-- keeps both tables' own-rows RLS, so a person reads only their own wishes.
--
-- Paste into Supabase, SQL editor, Run. Safe to run twice.

create or replace view public.wishes with (security_invoker = true) as
  select s.user_id, s.tree_id, s.created_at
  from public.saves s
  where not exists (select 1 from public.visited v
                    where v.user_id = s.user_id and v.tree_id = s.tree_id
                      and v.created_at >= s.created_at);

-- Supabase stopped granting API access to new objects on 2026-10-30.
grant select on public.wishes to authenticated;

-- The public profile's Want to visit reads the same rule.
create or replace function public.public_profile(uid uuid)
returns json
language sql
security definer
set search_path = public
stable
as $$
  select json_build_object(
    'user_id', p.user_id,
    'display_name', p.display_name,
    'avatar_url', p.avatar_url,
    'country', p.country,
    'created_at', (select u.created_at::date from auth.users u where u.id = p.user_id),
    'followers', (select count(*) from public.follows where followee = p.user_id),
    'following', (select count(*) from public.follows where follower = p.user_id),
    'ambassador', coalesce((select json_agg(a.place_name order by a.since)
                            from public.ambassadors a where a.user_id = p.user_id), '[]'::json),
    'visited', coalesce((select json_agg(v.tree_id order by v.tree_id)
                         from public.visited v where v.user_id = p.user_id), '[]'::json),
    'saves', coalesce((select json_agg(s.tree_id order by s.tree_id)
                       from public.saves s where s.user_id = p.user_id
                         and not exists (select 1 from public.visited v
                                         where v.user_id = s.user_id and v.tree_id = s.tree_id
                                           and v.created_at >= s.created_at)), '[]'::json)
  )
  from public.profiles p
  where p.user_id = uid and p.public
$$;
