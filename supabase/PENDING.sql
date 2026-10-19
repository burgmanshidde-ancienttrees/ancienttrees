-- APPLIED 2026-10-19 by Hidde (checked: rpc/public_profile answers, profiles and
-- follows refuse the public key). Nothing pending.
--
-- The public profile. Paste everything below into
-- Supabase, SQL editor, Run. Safe to run twice. The same lines are in
-- public-profiles.sql, which explains every choice.
--
-- Until it runs, nothing breaks: the Public profile switch stays hidden on
-- both surfaces and a profile link says the profile is private.

alter table public.profiles add column if not exists public boolean not null default false;

-- NEW ACCOUNTS START PUBLIC, AllTrails' default; accounts opened before this
-- day stay private, because they signed up when no profile could be seen.
create or replace function public.profile_public_default()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if tg_op = 'INSERT' then
    new.public := coalesce((select u.created_at >= '2026-10-20'::timestamptz
                            from auth.users u where u.id = new.user_id), false);
  end if;
  return new;
end
$$;
drop trigger if exists profile_public_default on public.profiles;
create trigger profile_public_default before insert on public.profiles
  for each row execute function public.profile_public_default();

-- NAMES AND THE FOLLOW GRAPH FOR SIGNED-IN READERS ONLY. Until now the
-- website's public key read every name and who follows whom. A public
-- profile is opened through public_profile() below, never the table.
drop policy if exists "profiles are readable" on public.profiles;
create policy "profiles are readable" on public.profiles
  for select to authenticated using (true);
drop policy if exists "follows are readable" on public.follows;
create policy "follows are readable" on public.follows
  for select to authenticated using (true);

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
    -- The day only, enough for the early-adopter badge.
    'created_at', (select u.created_at::date from auth.users u where u.id = p.user_id),
    'followers', (select count(*) from public.follows where followee = p.user_id),
    'following', (select count(*) from public.follows where follower = p.user_id),
    'ambassador', coalesce((select json_agg(a.place_name order by a.since)
                            from public.ambassadors a where a.user_id = p.user_id), '[]'::json),
    -- NEVER WHERE SOMEBODY IS NOW: no dates, not in the order they happened,
    -- and nothing ticked in the last 24 hours (Polarsteps' live-location
    -- lesson, 2026-09-04). Sorted by tree id, which groups by place.
    'visited', coalesce((select json_agg(v.tree_id order by v.tree_id)
                         from public.visited v where v.user_id = p.user_id
                           and v.created_at < now() - interval '24 hours'), '[]'::json),
    'saves', coalesce((select json_agg(s.tree_id order by s.tree_id)
                       from public.saves s where s.user_id = p.user_id), '[]'::json)
  )
  from public.profiles p
  where p.user_id = uid and p.public
$$;

revoke all on function public.public_profile(uuid) from public;
grant execute on function public.public_profile(uuid) to anon, authenticated;
