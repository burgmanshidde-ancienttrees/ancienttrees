-- A profile anybody can open, when its owner says so.
--
-- Hidde, 2026-10-19, after the design page: "ja dit ziet er goed uit", and on
-- the two lists: "die kunnen gewoon gelijk blijven toch?". That is the
-- explicit yes the accounts rule (DECISIONS.md 2026-08-14) asks for before a
-- new personal-data column, and it is recorded here because the rule is.
--
-- THE CONVENTION (CONVENTIONS.md, "A public profile, and the private switch"):
-- Polarsteps and Instagram both carry a "Private account" switch, ON for every
-- new account. Polarsteps' own statement of 2026-09-04 says every profile is
-- private by default, never public. So `public` is false until the person
-- turns the switch off and confirms the sheet that lists what becomes visible.
--
-- WHAT A PUBLIC PROFILE SHOWS: the same page the person sees as their own:
-- name, picture, flag, follow counts, badges, and the two lists (Collected,
-- Want to visit) as tree ids. Never the day a tree was ticked (visited_at),
-- never a private sighting photograph, never an email address.
--
-- HOW: the lists stay behind their own-rows RLS (saves.sql, visited.sql). The
-- one door is public_profile() below, a security-definer function that
-- answers null for a private profile, so no table policy is widened and
-- turning the switch back on closes everything in the same instant.
--
-- Paste into Supabase, SQL editor, Run. Safe to run twice.

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
