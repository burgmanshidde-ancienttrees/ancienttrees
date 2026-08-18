-- The visited table: the personal tree log's cloud half.
--
-- Hidde's paywall copy (DECISIONS.md 2026-08-18) sells "Personal Tree Log &
-- Badges: tick off trees you've stood in front of ... as your tree journal
-- grows", and a journal that lives in one browser's localStorage is not a
-- journal. Ticking off has been local-only since it shipped, so a new phone,
-- a cleared browser or seven days of Safari inactivity wiped it silently. That
-- is the one failure a collection cannot survive, and it is the reason this
-- table exists before the app does.
--
-- Paste this once into the Supabase SQL editor (dashboard > SQL) and run it.
-- Everything in it is idempotent; running it twice is safe.
--
-- Deliberately the same shape as saves.sql, for the same reasons:
-- * primary key (user_id, tree_id): one visit record per tree per account,
--   and the client upserts against exactly this conflict target.
-- * references auth.users on delete cascade: delete_user() removes the
--   auth.users row and this FK guarantees the log goes with it, which is what
--   keeps account deletion genuinely end to end.
-- * RLS all the way down: a user reads and writes only their own rows, and
--   the anon key alone can do nothing here.
--
-- visited_at is the day they stood in front of it, not the day they tapped:
-- the app will let someone log a tree they saw last week, and a badge that
-- counts "this autumn" needs the real date rather than the entry date.

create table if not exists public.visited (
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  tree_id    text not null,
  visited_at date not null default current_date,
  created_at timestamptz not null default now(),
  primary key (user_id, tree_id)
);

alter table public.visited enable row level security;

drop policy if exists "own visited select" on public.visited;
create policy "own visited select" on public.visited
  for select using (auth.uid() = user_id);

drop policy if exists "own visited insert" on public.visited;
create policy "own visited insert" on public.visited
  for insert with check (auth.uid() = user_id);

drop policy if exists "own visited update" on public.visited;
create policy "own visited update" on public.visited
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own visited delete" on public.visited;
create policy "own visited delete" on public.visited
  for delete using (auth.uid() = user_id);

grant select, insert, update, delete on public.visited to authenticated;
