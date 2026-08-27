-- How many people said a tree was worth the visit, and how many said it was not.
--
-- Hidde, 2026-08-27: "1 person keeps this tree is een hele rare zin, zet gewoon
-- bij thumb hoeveel mensen thumb up of down hebben gedaan verder niet." The
-- sentence went; a number beside each thumb needs this, because the app cannot
-- count votes on its own: submissions has no select policy at all, so a vote is
-- write-only from the client and always has been (own-data.sql says so).
--
-- Same shape as tree_save_counts: SECURITY DEFINER, COUNTS ONLY, no user id, no
-- email, no date. The caller learns that four people liked this tree and
-- nothing about any of them.
--
-- THE UNDO IS THE WHOLE DIFFICULTY. A vote is never deleted: undoing writes a
-- compensating "vote undone: worth it" row, so the rows for one person on one
-- tree are a history, and only the LAST word counts. Counting the raw rows
-- would have given Onder de Linden four votes from one account that currently
-- has none. So: latest row per (tree, person), and an undo is not a vote.
--
-- Two shapes of the tree column, both real. The website writes the bare id
-- ("ams_001"); the app writes "ams_001 (The Rijksmuseum Wingnut)". Everything
-- up to the first space is the id in both.
--
-- Rows with no user_id are older than the account gate of 2026-08-21 (6 of 35
-- on the day this was written) and are left out: without a person there is
-- nothing to take the last word of, and counting them would let one anonymous
-- session vote as many times as it clicked.

create or replace function public.tree_vote_counts()
returns table (tree_id text, up bigint, down bigint)
language sql
security definer
set search_path = public
stable
as $$
  with votes as (
    select distinct on (split_part(tree, ' ', 1), user_id)
           split_part(tree, ' ', 1) as tree_id,
           why
    from public.submissions
    where kind = 'feedback'
      and user_id is not null
      and (why in ('worth it', 'not worth it') or why like 'vote undone%')
    order by split_part(tree, ' ', 1), user_id, created_at desc
  )
  select tree_id,
         count(*) filter (where why = 'worth it')::bigint      as up,
         count(*) filter (where why = 'not worth it')::bigint   as down
  from votes
  group by tree_id
  having count(*) filter (where why in ('worth it', 'not worth it')) >= 1
$$;

revoke all on function public.tree_vote_counts() from public;
grant execute on function public.tree_vote_counts() to anon, authenticated;
