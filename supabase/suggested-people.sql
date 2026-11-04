-- Who photographed trees in the places you saved or collected: the second half
-- of "Suggested" under the empty Find people field.
--
-- Hidde, 2026-11-04, on the design page (drafts/design-2026-11-04, section 3):
-- "i like all your proposals please build". The convention is in
-- CONVENTIONS.md, "The empty Find people screen" (2026-11-03): Strava, AllTrails
-- and Instagram fill the space under an empty people search with suggested
-- people. Contacts and Facebook are new personal data (hard list 1), so ours
-- suggests only from what is already public: ambassadors (from the feed) and,
-- through this function, public profiles whose photographs are on the trees
-- of a place.
--
-- WHAT IT RETURNS, and nothing else: per place, the user id, display name,
-- avatar url and how many of that place's trees the person photographed.
-- Never a date, never which trees, never a private sighting: only sightings
-- the site published (status 'published', which is a photograph on the
-- tree's page), only profiles their owner made public, never the caller,
-- never somebody either of the two has blocked. Signed-in only, like names
-- and the follow graph (public-profiles.sql).
--
-- No new table and no new column. The sightings stay behind their own-rows
-- RLS (sightings.sql); this security-definer function is the one door, as
-- public_profile() is.
--
-- `places` is {"utrecht": ["utr_001", ...], "baarn": [...]}: the client knows
-- which trees are in which place from the feed, the server does not.
--
-- Paste into Supabase, SQL editor, Run. Safe to run twice. Until it is run
-- both surfaces show only the ambassadors.

create or replace function public.suggested_photographers(places jsonb)
returns table (place text, user_id uuid, display_name text, avatar_url text, trees int)
language sql
security definer
set search_path = public
stable
as $$
  with wanted as (
    select k.key as place, t.tree_id
    from jsonb_each(coalesce(places, '{}'::jsonb)) k
    cross join lateral jsonb_array_elements_text(
      case when jsonb_typeof(k.value) = 'array' then k.value else '[]'::jsonb end) t(tree_id)
    limit 2000
  )
  select w.place, p.user_id, p.display_name, p.avatar_url,
         count(distinct s.tree_id)::int as trees
  from wanted w
  join public.sightings s on s.tree_id = w.tree_id and s.status = 'published'
  join public.profiles p on p.user_id = s.user_id
  where auth.uid() is not null
    and p.public
    and coalesce(p.display_name, '') <> ''
    and p.user_id <> auth.uid()
    and not exists (select 1 from public.blocks b
                    where (b.blocker = auth.uid() and b.blocked = p.user_id)
                       or (b.blocker = p.user_id and b.blocked = auth.uid()))
  group by w.place, p.user_id, p.display_name, p.avatar_url
  order by trees desc, p.display_name
  limit 30
$$;

revoke all on function public.suggested_photographers(jsonb) from public;
revoke all on function public.suggested_photographers(jsonb) from anon;
grant execute on function public.suggested_photographers(jsonb) to authenticated;
