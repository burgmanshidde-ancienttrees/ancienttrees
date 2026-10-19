-- A profile anybody can open, when its owner says so.
--
-- Hidde, 2026-10-19, after the design page: "ja dit ziet er goed uit", and on
-- the two lists: "die kunnen gewoon gelijk blijven toch?". That is the
-- explicit yes the accounts rule (DECISIONS.md 2026-08-14) asks for before a
-- new personal-data column, and it is recorded here because the rule is.
--
-- THE CONVENTION (CONVENTIONS.md, "A public profile, and the private switch"):
-- AllTrails starts every new account Public; Polarsteps starts it private.
-- Hidde chose AllTrails (2026-10-19, "ok"), with one difference: accounts
-- opened before the profile existed stay private, because AllTrails was
-- criticised for opening people up without telling them. The switch is the
-- way out on both surfaces.
--
-- WHAT WAS CHECKED FOR LEAKS (2026-10-19, Hidde: "kijk nog eens kritisch"):
-- the website's public key read every display name and the whole follow
-- graph; both are signed-in only from here. The lists carry no dates, no
-- time order and nothing from the last 24 hours, so a profile never says
-- where somebody is now. What remains visible on a public profile, by
-- design: the places somebody collects trees in, which is roughly where
-- they live or travel, the same as AllTrails' location field.
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
