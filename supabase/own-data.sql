-- The last two things that lived only on a phone.
--
-- Hidde, 2026-08-27: "ik hoop dat alles mee gaat met je account, likes, bomen
-- etc, niks moet lokaal opgeslagen zijn." Audited the app against that and
-- found two gaps. Everything else already travels: favourites in saves, ticked
-- trees in visited, your own trees and their photographs in sightings, blocked
-- people in blocks, your name and picture in profiles.
--
-- 1. YOUR OWN VOTES. A thumb up or down is written to submissions and can never
--    be read back, because submissions has no select policy at all: it is a
--    postbox. So on a new phone every tree looks unvoted and the same person can
--    say the same thing twice. The policy below lets somebody read THEIR OWN
--    rows and nobody else's, which also means they can see the answer we wrote
--    back to them, which is better than the postbox was.
--
-- 2. KILOMETRES OR MILES. A preference rather than data, and losing it is a
--    small thing, but it is one more thing that does not follow you and it costs
--    a column.

-- Your own submissions, and only ever your own.
drop policy if exists "own submissions are readable" on public.submissions;
create policy "own submissions are readable" on public.submissions
  for select to authenticated
  using (auth.uid() = user_id);

-- Which units somebody reads distances in. Null means they never chose, and the
-- app keeps deciding from the phone's own locale until they do.
alter table public.profiles
  add column if not exists units text
  check (units is null or units in ('km', 'mi'));
