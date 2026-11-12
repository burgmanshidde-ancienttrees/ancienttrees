-- YOUR OWN TREES ON YOUR PUBLIC PROFILE, AND "APPROVED" ON THE ONES WE TOOK IN.
--
-- Hidde, 2026-11-12: "je hebt de bomen die wij vertonen, onze selectie, en dan
-- heb je alle bomen die iemand zelf kan tonen ... mag van mij uiteindelijk wel
-- te vinden zijn via een profiel", and on the design page the same day: "de
-- approved design is goedgekeurd". CONVENTIONS.md 2026-11-12 ("Your own trees
-- on a public profile") holds the references: iNaturalist (every observation
-- public, location open by default, obscured or private by choice; Research
-- Grade marks the confirmed ones), Strava (map visibility per activity) and
-- Google Maps' "Approved" for a contribution it accepted (our word since
-- 2026-10-09).
--
-- WHAT CHANGES
-- 1. sightings.added: true on a sighting that became one of our trees because
--    this person added it (a city file's found_by_reader.sighting_id). Written
--    by scripts/sightings_link.py on every knock, never by a phone.
-- 2. sightings.hide_location: the person's "hide the exact spot" choice, the
--    iNaturalist geoprivacy switch. Default false, open, as iNaturalist's is.
--    The control that sets it comes with the apps; until then nobody can turn
--    it on and every own tree shows its pin.
-- 3. public_profile() returns two more lists:
--    'approved': ids of our trees that this person added (status published,
--               added). The profile marks those tiles Approved.
--    'own':      the trees this person added that are not in our selection:
--               id, name, species, the shared photograph's path, and the
--               position unless hide_location. No dates, sorted by id, like
--               the other lists.
--
-- A NEW PERSONAL-DATA COLUMN needs Hidde's yes (hard list 1): hide_location
-- is a setting about data we already hold, given the same day ("ja" to the
-- design that carries it). privacycheck.py reads this file; the privacy page
-- says what a public profile shows.
--
-- Paste into Supabase, SQL editor, Run. Safe to run twice.

alter table public.sightings add column if not exists added boolean not null default false;
alter table public.sightings add column if not exists hide_location boolean not null default false;

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
                                           and v.created_at >= s.created_at)), '[]'::json),
    'approved', coalesce((select json_agg(distinct sg.tree_id)
                          from public.sightings sg
                          where sg.user_id = p.user_id and sg.added
                            and sg.status = 'published' and sg.tree_id is not null), '[]'::json),
    -- The shared copy is the only photograph a visitor may load
    -- (shared-sightings.sql). Its path keeps the phone's own spelling of the
    -- id, which is upper case on both apps.
    'own', coalesce((select json_agg(json_build_object(
                        'id', sg.id,
                        'name', sg.name,
                        'species', sg.species,
                        'photo', p.user_id::text || '/' || upper(sg.id::text) || '.jpg',
                        'lat', case when sg.hide_location then null else sg.lat end,
                        'lng', case when sg.hide_location then null else sg.lng end)
                      order by sg.id)
                     from public.sightings sg
                     where sg.user_id = p.user_id and sg.tree_id is null
                       and sg.photo is not null and sg.shared), '[]'::json)
  )
  from public.profiles p
  where p.user_id = uid and p.public
$$;

revoke all on function public.public_profile(uuid) from public;
grant execute on function public.public_profile(uuid) to anon, authenticated;
