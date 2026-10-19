-- PENDING since 2026-10-19: the public profile. Paste everything below into
-- Supabase, SQL editor, Run. Safe to run twice. Check afterwards that
-- profiles?select=public answers. The same lines are in public-profiles.sql,
-- which explains every choice.
--
-- Until it runs, nothing breaks: the Private profile switch stays hidden on
-- both surfaces and a profile link says the profile is private.

alter table public.profiles add column if not exists public boolean not null default false;

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
    'created_at', (select u.created_at from auth.users u where u.id = p.user_id),
    'followers', (select count(*) from public.follows where followee = p.user_id),
    'following', (select count(*) from public.follows where follower = p.user_id),
    'ambassador', coalesce((select json_agg(a.place_name order by a.since)
                            from public.ambassadors a where a.user_id = p.user_id), '[]'::json),
    'visited', coalesce((select json_agg(v.tree_id order by v.created_at desc)
                         from public.visited v where v.user_id = p.user_id), '[]'::json),
    'saves', coalesce((select json_agg(s.tree_id order by s.created_at desc)
                       from public.saves s where s.user_id = p.user_id), '[]'::json)
  )
  from public.profiles p
  where p.user_id = uid and p.public
$$;

revoke all on function public.public_profile(uuid) from public;
grant execute on function public.public_profile(uuid) to anon, authenticated;
