-- Notes from visitors on a tree page (Hidde, 2026-10-24: "negeer mijn regel
-- tegen comments", then "bouw alles"). CONVENTIONS.md, "Notes from visitors on
-- a tree page": one note per person per tree, dated, no replies, no likes, no
-- stars; live for everyone the moment it is written ("zet gewoon live en we
-- kunnen altijd wegmodereren later"); the night run reads every new note
-- (scripts/tree_notes.py) and takes a bad one down by setting hidden.
--
-- Paste this once into the Supabase SQL editor (dashboard > SQL) and run it.
-- Everything in it is idempotent; running it twice is safe.
--
-- Design notes:
-- * primary key (user_id, tree_id): one note per tree per account; the page
--   upserts against exactly this conflict target, so writing again edits.
-- * references auth.users on delete cascade: deleting the account deletes
--   the notes, which keeps account deletion end to end (hard list 1).
-- * RLS: a person reads, writes and deletes only their own rows. Everybody
--   else reads through tree_notes_for(), which hands out the text, the date
--   and the name and picture ONLY when that profile is public
--   (public-profiles.sql, 2026-10-19); a private profile reads "A visitor".
--   No user id leaves the function, so a note never points at an account.
-- * GRANT in the same file (Supabase stopped granting API access
--   automatically on 2026-10-30; CLAUDE.md, Privacy and accounts).

create table if not exists public.tree_notes (
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  tree_id    text not null,
  body       text not null check (char_length(body) between 1 and 1000),
  -- Taken down by a run or by Hidde; the row stays so the person still sees
  -- and can edit or delete their own note.
  hidden     boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, tree_id)
);

create index if not exists tree_notes_tree_id on public.tree_notes (tree_id, created_at desc);

alter table public.tree_notes enable row level security;

drop policy if exists "own notes select" on public.tree_notes;
create policy "own notes select" on public.tree_notes
  for select using (auth.uid() = user_id);

drop policy if exists "own notes insert" on public.tree_notes;
create policy "own notes insert" on public.tree_notes
  for insert with check (auth.uid() = user_id);

drop policy if exists "own notes update" on public.tree_notes;
create policy "own notes update" on public.tree_notes
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own notes delete" on public.tree_notes;
create policy "own notes delete" on public.tree_notes
  for delete using (auth.uid() = user_id);

grant select, insert, update, delete on public.tree_notes to authenticated;
grant select, update on public.tree_notes to service_role;

-- Every note on these trees, newest first, for the tree page (anon and signed
-- in alike). The name and picture only from a public profile.
create or replace function public.tree_notes_for(ids text[])
returns table (
  tree_id text,
  body text,
  created_at timestamptz,
  author_name text,
  author_avatar text
)
language sql
security definer
set search_path = public
stable
as $$
  select n.tree_id, n.body, n.created_at,
         case when p.public then p.display_name end,
         case when p.public then p.avatar_url end
  from public.tree_notes n
  left join public.profiles p on p.user_id = n.user_id
  where n.tree_id = any(ids) and not n.hidden
  order by n.created_at desc
  limit 200
$$;

revoke all on function public.tree_notes_for(text[]) from public;
grant execute on function public.tree_notes_for(text[]) to anon, authenticated;
