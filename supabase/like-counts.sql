-- How many people have saved each tree, as one public number.
--
-- Hidde, 2026-08-26: "aantal likes tellen en terug geven, pas van 1 tellen."
--
-- The saves table is row-level-secured per user, which is right and is also
-- why the app cannot count it: a reader may only see their own rows, so a
-- count from the client is always their own saves and nothing else. This is
-- the ordinary answer to that, a SECURITY DEFINER function that returns
-- COUNTS ONLY. No user id, no email, no date, nothing that says who: the
-- caller learns that eleven people saved this tree and nothing about any of
-- them, which keeps it inside the rule that no personal data is ever exposed.
--
-- "Pas van 1 tellen" is honoured here rather than in the app: a tree nobody
-- has saved is simply not in the result, so there is no zero to render and no
-- decision for the caller to make.

create or replace function public.tree_save_counts()
returns table (tree_id text, saves bigint)
language sql
security definer
set search_path = public
stable
as $$
  select tree_id, count(*)::bigint as saves
  from public.saves
  group by tree_id
  having count(*) >= 1
$$;

revoke all on function public.tree_save_counts() from public;
grant execute on function public.tree_save_counts() to anon, authenticated;
