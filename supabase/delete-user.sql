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

  -- THE PICTURE IS NOT DELETED HERE, and the first version of this file tried
  -- to, which broke deletion completely for the hour it was live.
  --
  -- Supabase refuses a delete against storage.objects from SQL: "Direct
  -- deletion from storage tables is not allowed. Use the Storage API instead."
  -- That refusal raises, the whole function rolls back, and NOTHING is
  -- deleted, not the saves, not the profile, not even the account. A promise
  -- that quietly does nothing is worse than the orphaned file it was trying to
  -- fix, and only running the test found it (scripts/account_delete_test.py,
  -- 2026-08-27, on the day it was written).
  --
  -- So the avatar is deleted by the CLIENT, through the Storage API, in the
  -- moment before this is called. That is the route Supabase intends, it runs
  -- as the account itself, and if it fails the account still goes: an orphaned
  -- image is a tidy-up job, an account that will not delete is a broken
  -- promise and an App Store rejection.
  --
  -- saves, visited, profiles, follows, blocks and reports all reference
  -- auth.users(id) on delete cascade, so the line below is what takes them,
  -- and adding a table with that foreign key is what keeps this function from
  -- ever needing to know about it.
  delete from auth.users where id = uid;
end;
$$;

revoke all on function public.delete_user() from public;
grant execute on function public.delete_user() to authenticated;
