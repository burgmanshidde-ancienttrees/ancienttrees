-- Reporting somebody, and blocking them.
--
-- Written 2026-08-27, the day Hidde ruled that the social half ships in 1.0
-- ("sociale deel gaat mee") and then answered the objection to it in one line:
-- "maak gewoon die melden optie, zo moeilijk is het niet toch". He is right
-- that it is small. It is also not optional: from the moment one person can see
-- a name and a photograph another person chose, App Store guideline 1.2 asks
-- for four things, and three of them live here.
--
--   a way to REPORT objectionable content     -> public.reports
--   a way to BLOCK an abusive user            -> public.blocks
--   a published way to REACH US               -> info@ancienttrees.app, on the
--                                                privacy page and in Settings
--   terms nobody can miss                     -> the sign-in sheet's own line
--
-- WHY BLOCKS LIVE ON THE SERVER rather than in the phone's own storage, which
-- would have been half a day less work. A block kept on the device is lost on
-- reinstall, does not follow you to a second phone, and cannot stop the blocked
-- account from following you back. All three are the case a block exists for.
--
-- Deletion still cascades: both tables hang off auth.users, so deleting an
-- account takes its reports and its blocks with it, in both directions.

create table if not exists public.reports (
  id bigint generated always as identity primary key,
  -- WHO REPORTED, kept because a reporter who is themselves abusive is the
  -- other half of moderation, and because a report from nobody cannot be
  -- answered.
  reporter uuid not null references auth.users(id) on delete cascade,
  -- The account being reported. Nothing else identifies it: the name and the
  -- picture are already in profiles and are what will be looked at.
  subject uuid not null references auth.users(id) on delete cascade,
  reason text not null check (char_length(reason) between 1 and 400),
  created_at timestamptz not null default now(),
  -- Set by hand when somebody has actually looked. Apple asks for a timely
  -- response and this column is what makes "timely" answerable.
  handled_at timestamptz,
  check (reporter <> subject)
);

alter table public.reports enable row level security;

-- INSERT ONLY, and only as yourself. Nobody reads reports back through the
-- public key, not even their own: a reporting queue that the reported person
-- can read is a way to find out who reported you.
drop policy if exists "anybody signed in may report" on public.reports;
create policy "anybody signed in may report" on public.reports
  for insert with check (auth.uid() = reporter);

create index if not exists reports_unhandled
  on public.reports (created_at desc) where handled_at is null;

create table if not exists public.blocks (
  blocker uuid not null references auth.users(id) on delete cascade,
  blocked uuid not null references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (blocker, blocked),
  check (blocker <> blocked)
);

alter table public.blocks enable row level security;

-- Your own blocks, and nobody else's. The blocked person must not be able to
-- learn that they were blocked, which is why this is not readable both ways.
drop policy if exists "own blocks are readable" on public.blocks;
create policy "own blocks are readable" on public.blocks
  for select using (auth.uid() = blocker);

drop policy if exists "own blocks are writable" on public.blocks;
create policy "own blocks are writable" on public.blocks
  for all using (auth.uid() = blocker) with check (auth.uid() = blocker);

-- A BLOCK ALSO BREAKS THE FOLLOW, in both directions, because a block that
-- leaves somebody following you is not a block. Done as a trigger rather than
-- in the app so it cannot be forgotten by a second client later.
create or replace function public.break_follows_on_block() returns trigger
language plpgsql security definer as $$
begin
  delete from public.follows
   where (follower = new.blocker and followee = new.blocked)
      or (follower = new.blocked and followee = new.blocker);
  return new;
end;
$$;

drop trigger if exists blocks_break_follows on public.blocks;
create trigger blocks_break_follows
  after insert on public.blocks
  for each row execute function public.break_follows_on_block();
