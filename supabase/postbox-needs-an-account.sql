-- THE POSTBOX GETS A LOCK.
--
-- Hidde, 2026-09-23, testing the contribute form: "one thing goes wrong - i
-- can suggest a tree without logging in", then "so the account thing doesnt
-- make sense". Both halves are right, and the second is the sharper one: an
-- anonymous row has no account, so it can never appear on anybody's account
-- page, we can never write back to say what it changed, and the deletion
-- promise has nothing to hang on. It is a tip we can neither answer nor
-- attribute.
--
-- The rule itself is not new. Hidde set it on 2026-08-21, following Google
-- Maps: anyone may see and fill the form, sending needs the account that lets
-- us answer, and a privacy request is the one exception because asking for
-- your own data back can never require making an account first.
--
-- WHAT WAS WRONG is that the rule lived only in JavaScript. The gate is in
-- contribute.astro and it works; the DATABASE accepted anything. Probed on
-- 2026-09-23 with the publishable key and no session: HTTP 201. Ten rows in
-- the table have no account, all of them from before the gate was written, so
-- nobody has walked through the open door. It was still open.
--
-- This is the same shape as the day's other three faults and the reason they
-- are worth counting together: something is asked for, and the thing that was
-- supposed to enforce or read it is not there. A check in the client is a
-- courtesy to the person using it, never a boundary.
--
-- WHAT IT DOES NOT BREAK, checked before writing: every path in the app
-- already guards on account.isSignedIn (Contribute, WorthIt, CollectSheet,
-- PlacePin), and the website's only ungated path is the privacy request,
-- which the second clause allows.

-- FIRST, TAKE AWAY THE POLICY THAT SAYS YES. Added 2026-09-24, after Hidde
-- ran the version below and the anonymous probe still went through with HTTP
-- 201. RLS policies are PERMISSIVE and OR together: one that permits is enough,
-- however many refuse. The open one was made in the Supabase dashboard when
-- this form was built, so it is in no file here and nothing in this repo knows
-- its name.
--
-- So it is dropped by SHAPE rather than by name: every policy on this table
-- that can permit an insert, which is cmd INSERT and cmd ALL. The select policy
-- from own-data.sql is cmd SELECT and is deliberately untouched, because
-- reading your own submissions is what puts them on your account page.
do $$
declare p record;
begin
  for p in
    select policyname
      from pg_policies
     where schemaname = 'public'
       and tablename = 'submissions'
       and cmd in ('INSERT', 'ALL')
  loop
    raise notice 'dropping insert policy %', p.policyname;
    execute format('drop policy %I on public.submissions', p.policyname);
  end loop;
end $$;

drop policy if exists "sending needs an account" on public.submissions;
create policy "sending needs an account" on public.submissions
  for insert
  with check (
    -- Signed in, and stamping your own id rather than somebody else's. The
    -- column defaults to auth.uid(), so an honest client never has to think
    -- about this and a dishonest one cannot post as another account.
    auth.uid() = user_id
    -- Or a privacy request, which may always be anonymous.
    or (kind = 'privacy' and user_id is null)
  );
