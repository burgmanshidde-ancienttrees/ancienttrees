-- Letting somebody delete their own profile picture.
--
-- The last row of the deletion test, 2026-08-27. Everything in the database
-- goes when an account is deleted; the avatar file did not, and the reason was
-- not the app and not the function. The avatars bucket has a policy that lets
-- somebody UPLOAD their picture and none that lets them REMOVE it, so the
-- Storage API answered the app's delete with "Access denied" and the file
-- stayed, publicly readable, after its owner had gone.
--
-- Nothing here widens what anybody can reach. The condition is the same one
-- the upload already uses: the first folder of the path is the account's own
-- id, because ProfileEditor writes to avatars/<user id>/avatar.jpg. So an
-- account may delete its own picture and nobody else's.
--
-- UPDATE is here for the same reason and was the other half of the same gap:
-- changing your picture writes over the same path, which is an update rather
-- than an insert, and without this it would fail the second time.

drop policy if exists "own avatar delete" on storage.objects;
create policy "own avatar delete" on storage.objects
  for delete to authenticated
  using (
    bucket_id = 'avatars'
    and auth.uid()::text = (storage.foldername(name))[1]
  );

drop policy if exists "own avatar update" on storage.objects;
create policy "own avatar update" on storage.objects
  for update to authenticated
  using (
    bucket_id = 'avatars'
    and auth.uid()::text = (storage.foldername(name))[1]
  )
  with check (
    bucket_id = 'avatars'
    and auth.uid()::text = (storage.foldername(name))[1]
  );
