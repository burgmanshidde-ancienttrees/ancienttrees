-- Who looks after a place: the ambassadors.
--
-- Hidde, 2026-10-02, the day a stranger put nine photographs on two Paris pages
-- within minutes of installing the app: "email each person that adds trees to
-- become the cities ambassador ... maybe we can even give them special tag if
-- they want - share some responsibility and amplify them", then "ambassador
-- idea is perfect lets implement it in both app and web". That is the explicit
-- yes the accounts rule (DECISIONS.md 2026-08-14) asks for before anything new
-- about a person is stored, and it is recorded here because the rule is.
--
-- THE CONVENTION (CONVENTIONS.md 2026-10-02): komoot's Pioneer is per region,
-- is a badge beside the name on the person's own contributions, and is earned
-- by what they already do. So a row here is one person and one place, and the
-- badge is the whole of it.
--
-- WHAT THIS STORES, exactly: that an account is the ambassador of a place, the
-- place's name as the badge prints it, whether the person said their name may
-- appear on the public page, and since when. No real name, nothing else.
-- Cascades off auth.users, so deleting an account takes the badge with it,
-- which was the condition of opening accounts at all.
--
-- WHO WRITES IT: us, with the service key (scripts/ambassador.py), after the
-- person said yes to Hidde's mail. There is deliberately NO insert or delete
-- policy for signed-in users: an ambassador is invited, never self-declared.
-- The one thing a person may change about their own row is `public`, which is
-- their consent to be named on the website, because that consent is theirs.

create table if not exists public.ambassadors (
  user_id uuid not null references auth.users(id) on delete cascade,
  place_slug text not null check (char_length(place_slug) between 1 and 80),
  -- Denormalised on purpose: the badge prints it, and neither surface should
  -- have to resolve a slug against the catalogue to show a name.
  place_name text not null check (char_length(place_name) between 1 and 80),
  -- Consent to be named on the public city page. Nothing on the website names
  -- a person without it (CLAUDE.md, 2026-08-11); the app shows the badge to
  -- signed-in readers regardless, because a profile is already public there.
  public boolean not null default false,
  since date not null default current_date,
  primary key (user_id, place_slug)
);

alter table public.ambassadors enable row level security;

drop policy if exists "ambassadors are readable" on public.ambassadors;
create policy "ambassadors are readable" on public.ambassadors
  for select using (true);

-- Only your own consent flag, and only that column.
drop policy if exists "own consent is writable" on public.ambassadors;
create policy "own consent is writable" on public.ambassadors
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
revoke update on public.ambassadors from authenticated;
grant update (public) on public.ambassadors to authenticated;
grant select on public.ambassadors to anon, authenticated;
