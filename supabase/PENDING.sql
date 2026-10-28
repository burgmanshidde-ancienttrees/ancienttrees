-- PENDING, for Hidde to paste in the Supabase SQL editor (2026-10-28). A copy of
-- supabase/profile-at-signup.sql.
--
-- Every account has a profile from the moment it exists.
--
-- Hidde, 2026-10-28, on learning that 16 of the 17 accounts opened since
-- 10-20 had no profile at all (a row was only made when somebody set a name):
-- "public profiles should be created when account is created - for example
-- reddit just gives you a random name untill you change it".
--
-- THE CONVENTION: Reddit gives every new account a generated username
-- (Adjective-Noun-1234) that the person may change; AllTrails, whose
-- Public-first default we follow (public-profiles.sql), shows the name the
-- sign-in provider gave. So: the provider's name when there is one, shortened
-- the way the app already shortens it (Profiles.shortName: "Miguel P."),
-- otherwise a generated tree name ("Mossy Linden 4821"). Edit profile changes
-- it on both surfaces, as before.
--
-- Public or private is still decided by profile_public_default()
-- (public-profiles.sql): accounts opened from 2026-10-20 start public, older
-- ones private. Nothing in this file changes that.
--
-- No new column: display_name already exists (profiles.sql, Hidde's yes of
-- 2026-08-26). Deletion still cascades off auth.users.

create or replace function public.generated_display_name()
returns text
language sql
volatile
as $$
  select initcap((array['mossy','quiet','gnarled','old','tall','shady','sunlit','misty','wild','green',
                        'golden','silver','hollow','rooted','windy','leafy','evergreen','ancient'])
                 [1 + floor(random() * 18)::int])
      || ' ' ||
         (array['Oak','Linden','Beech','Yew','Cedar','Plane','Willow','Olive','Chestnut','Elm',
                'Ash','Fig','Pine','Maple','Ginkgo','Cypress','Baobab','Sequoia'])
                 [1 + floor(random() * 18)::int]
      || ' ' || lpad((floor(random() * 10000))::int::text, 4, '0')
$$;

-- "Miguel Portugal" -> "Miguel P."; one word stays itself; nothing -> null.
create or replace function public.short_provider_name(full_name text)
returns text
language plpgsql
immutable
as $$
declare
  parts text[];
begin
  if full_name is null or btrim(full_name) = '' then
    return null;
  end if;
  parts := regexp_split_to_array(btrim(full_name), '\s+');
  if array_length(parts, 1) = 1 then
    return left(parts[1], 40);
  end if;
  return left(parts[1] || ' ' || left(parts[array_length(parts, 1)], 1) || '.', 40);
end
$$;

create or replace function public.profile_at_signup()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (user_id, display_name)
  values (new.id,
          coalesce(public.short_provider_name(coalesce(new.raw_user_meta_data->>'full_name',
                                                       new.raw_user_meta_data->>'name')),
                   public.generated_display_name()))
  on conflict (user_id) do nothing;
  return new;
end
$$;

drop trigger if exists profile_at_signup on auth.users;
create trigger profile_at_signup after insert on auth.users
  for each row execute function public.profile_at_signup();

-- The accounts that exist without a profile get one now. The insert fires
-- profile_public_default(), so the ones opened before 2026-10-20 stay private.
-- Those older ones get a generated name, never their provider's: signed-in
-- readers can see every name (public-profiles.sql) and search them in the
-- app, and these people signed up when no name of theirs was shown anywhere.
insert into public.profiles (user_id, display_name)
select u.id,
       case when u.created_at >= '2026-10-20'::timestamptz
            then coalesce(public.short_provider_name(coalesce(u.raw_user_meta_data->>'full_name',
                                                              u.raw_user_meta_data->>'name')),
                          public.generated_display_name())
            else public.generated_display_name() end
from auth.users u
where not exists (select 1 from public.profiles p where p.user_id = u.id);
