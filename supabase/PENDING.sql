-- ONE STATEMENT PENDING, at the foot: submissions.sign_photo (2026-09-24).
-- Emptied earlier on 2026-09-24 after Hidde pasted the last batch
-- (sightings.girth_hugs, submissions.photo, sightings.sign_photo); all three
-- were confirmed against the live REST API the same hour.
--
-- When a new column or table is written, put its statement here as well, with
-- `if not exists`, so one paste in the SQL editor brings the database level.
-- `python3 scripts/sqlcheck.py` asks the live database what is still missing.

-- PENDING 2026-09-24: the sign photograph on the website's form. The app's
-- add-a-tree flow stores it on sightings.sign_photo (live); a tip sent from
-- /contribute hangs its files off the SUBMISSION instead (see
-- supabase/submission-photos.sql), so it needs the same column there. Until
-- this is pasted, the form drops the key and retries, so the tip still lands.
alter table public.submissions
  add column if not exists sign_photo text
  check (sign_photo is null or char_length(sign_photo) <= 300);
