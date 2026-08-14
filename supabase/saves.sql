-- The saves table: the save heart's cloud half (Hidde opened the account
-- track 2026-08-14: "just build it - we're continuing with this product").
--
-- Paste this once into the Supabase SQL editor (dashboard > SQL) and run it.
-- Everything in it is idempotent; running it twice is safe.
--
-- Design notes, so the next reader does not have to reverse-engineer:
-- * primary key (user_id, tree_id): one save per tree per account, and the
--   client upserts against exactly this conflict target.
-- * references auth.users on delete cascade: the existing delete_user()
--   function removes the auth.users row, and this FK guarantees the saves
--   go with it, which keeps account deletion truly end-to-end (the gate
--   Hidde set before the account page could be linked).
-- * RLS all the way down: a user sees, writes and deletes only their own
--   rows. The anon key alone can do nothing here.

create table if not exists public.saves (
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  tree_id    text not null,
  name       text not null default '',
  url        text not null default '',
  created_at timestamptz not null default now(),
  primary key (user_id, tree_id)
);

alter table public.saves enable row level security;

drop policy if exists "own saves select" on public.saves;
create policy "own saves select" on public.saves
  for select using (auth.uid() = user_id);

drop policy if exists "own saves insert" on public.saves;
create policy "own saves insert" on public.saves
  for insert with check (auth.uid() = user_id);

drop policy if exists "own saves update" on public.saves;
create policy "own saves update" on public.saves
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own saves delete" on public.saves;
create policy "own saves delete" on public.saves
  for delete using (auth.uid() = user_id);

grant select, insert, update, delete on public.saves to authenticated;
