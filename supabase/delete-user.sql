-- Deleting an account, all the way down, including the picture.
--
-- REPLACES the delete_user() that has been in the database since the account
-- track opened. That one removed the auth.users row and let the foreign keys
-- take the rest, which is right and is not everything: an avatar lives in
-- storage rather than in a table, and storage.objects does not cascade off
-- auth.users. It is set to a null owner instead, so the file stays in the
-- bucket, still publicly readable at its old address, after the person who
-- uploaded it has deleted their account.
--
-- Found 2026-08-27 while writing the end-to-end deletion test Hidde asked for.
-- It is the one part of "we delete everything" that was not true, and it is the
-- part a person would care most about, because it is their face.
--
-- Everything else still travels by cascade and is listed here so the promise
-- can be checked rather than trusted: saves, visited, profiles, follows in both
-- directions, blocks in both directions, and reports both made and received.

create or replace function public.delete_user() returns void
language plpgsql security definer set search_path = public as $$
declare
  uid uuid := auth.uid();
begin
  if uid is null then
    raise exception 'delete_user() called without a signed-in account';
  end if;

  -- THE PICTURE FIRST, because it is the only thing here that a cascade
  -- cannot reach. ProfileEditor uploads to avatars/<user id>/avatar.jpg, so
  -- the first folder of the path is the account's own id.
  delete from storage.objects
   where bucket_id = 'avatars'
     and (storage.foldername(name))[1] = uid::text;

  -- Then the account. saves, visited, profiles, follows, blocks and reports
  -- all reference auth.users(id) on delete cascade, so this line is what takes
  -- them, and adding a table with that foreign key is what keeps this function
  -- from needing to know about it.
  delete from auth.users where id = uid;
end;
$$;

revoke all on function public.delete_user() from public;
grant execute on function public.delete_user() to authenticated;
