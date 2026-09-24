-- A PHOTOGRAPH ATTACHED TO A TIP, from the website's form.
--
-- Hidde, 2026-09-23: "het gaat er vooral op dat de contribute pagina wel fotos
-- gaat aannemen toch?" He is right, and the gap was embarrassing once looked
-- at: the page's own "What helps most" list asks for "A photo you took
-- yourself" and the form has no file field of any kind, so it asked for
-- something it could not take. The site could set a profile picture and could
-- not accept a photograph of a tree.
--
-- The tree's OWN page is a different case and needs nothing here: that photo
-- goes into sightings, which already exists, because there the tree and its
-- coordinate are known. A tip is about a tree we do not map, so there is no
-- coordinate at all and a browser cannot invent one. The file hangs off the
-- submission instead.
--
-- WHERE THE FILE LIVES: the sightings bucket, at <user id>/<uuid>.jpg, under
-- the folder policy that is already there, so a person can read and delete
-- their own and nobody else's. No new bucket and no new storage policy.
--
-- DELETION. A submission row carries user_id with no cascade, deliberately,
-- because a tip that became a tree must not vanish from the ledger when
-- somebody closes their account. The PHOTOGRAPH is theirs and does go, which
-- is what photo_takedown.py already does for published contributor pictures;
-- this column is what lets it find the unpublished ones too.
alter table public.submissions
  add column if not exists photo text
  check (photo is null or char_length(photo) <= 300);

-- A SECOND photograph, of the sign beside the tree when there is one (Hidde,
-- 2026-09-24). Same bucket and folder as `photo`. Evidence for whoever checks
-- the tip, never published.
alter table public.submissions
  add column if not exists sign_photo text
  check (sign_photo is null or char_length(sign_photo) <= 300);
