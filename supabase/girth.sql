-- Girth as a data point somebody can send us, on both surfaces.
--
-- Hidde, 2026-09-11: "we zouden girth toevoegen als data punt". It is the one
-- measurement that unlocks the rest: girth plus a species gives a derived age
-- (CLAUDE.md, Step 2), and it feeds /collections/thickest-trees. About half
-- our trees carry none, and a reader with a tape, or two arms, is standing in
-- front of the trunk.
--
-- WHAT IS STORED: one whole number, the trunk's circumference in centimetres,
-- on a row that already exists. It is a fact about a tree, not about a
-- person, so it adds no personal data and changes nothing about deletion: the
-- sightings row still cascades with the account, and a submission row is
-- still what it was.
--
-- The range is a sanity check, not a judgement: under 10 cm is a typo, and
-- the widest trunk on earth (the Tule tree) is about 42 m round.
--
-- Safe to run twice.

alter table public.sightings
  add column if not exists girth_cm integer
  check (girth_cm is null or girth_cm between 10 and 5000);

alter table public.submissions
  add column if not exists girth_cm integer
  check (girth_cm is null or girth_cm between 10 and 5000);

-- The unlisted page for a tree somebody added shows it too, so the view is
-- rebuilt with the column appended. Same definition as shared-sightings.sql
-- otherwise, including SECURITY DEFINER and the grant.
drop view if exists public.shared_trees;
create view public.shared_trees
  with (security_invoker = off) as
  select id, name, species, age, note, taken_at, photo, status, girth_cm
    from public.sightings
   where shared = true;

grant select on public.shared_trees to anon, authenticated;
