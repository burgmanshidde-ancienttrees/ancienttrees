-- Where the website's script errors land.
--
-- Hidde, 2026-11-04, the quality line in the daily digest: "I'd rather have
-- some sort of overview and a green, red, or orange light somewhere in the
-- daily digest than more text." The app has MetricKit (diagnostics.sql); the
-- website had nothing, so a script that threw for one kind of visitor stayed
-- invisible until somebody mailed. The page half is
-- site/src/lib/web-errors-js.ts, the reader is scripts/web_errors.py.
--
-- WHAT ARRIVES: one row per distinct script error, at most three per page
-- load, only from ancienttrees.app. The message (300 characters at most), the
-- script file and line, the page path without its query string, a browser
-- family and major version ("Safari 18"), the build and the day. NOTHING that
-- says who it came from: no user id, no account, no session, no full user
-- agent, no query string, and no IP address column. A row cannot point at a
-- person.
--
-- INSERTS ARE ANONYMOUS, as for crashes: a page that breaks before anybody
-- signs in is the page we most want to hear from. Nobody reads rows back
-- through the API except the service key: no select for anon or
-- authenticated. The length checks below are the backstop for rubbish.
--
-- GRANTS in this file (Supabase stopped granting API access to new tables on
-- 2026-10-30): insert for anon and authenticated, everything for service_role.
--
-- Paste the whole file into the Supabase SQL editor once. It is safe to run
-- again.

create table if not exists public.web_errors (
  id bigint generated always as identity primary key,
  day date not null default ((now() at time zone 'utc')::date),
  message text not null check (char_length(message) between 1 and 300),
  source text not null default '' check (char_length(source) <= 200),
  line int check (line is null or (line >= 0 and line < 10000000)),
  path text not null default '/' check (char_length(path) <= 200 and position('?' in path) = 0),
  browser text not null default 'other' check (char_length(browser) <= 40),
  build text not null default '' check (char_length(build) <= 40),
  created_at timestamptz not null default now()
);

alter table public.web_errors enable row level security;

drop policy if exists "anybody may report a page error" on public.web_errors;
create policy "anybody may report a page error" on public.web_errors
  for insert to anon, authenticated
  with check (day between (now() at time zone 'utc')::date - 1
                      and (now() at time zone 'utc')::date + 1);

-- No select, update or delete policy: through the API this table can only be
-- written to, and only by the service key read.
revoke all on public.web_errors from anon, authenticated;
grant insert on public.web_errors to anon, authenticated;
grant all on public.web_errors to service_role;

create index if not exists web_errors_recent on public.web_errors (created_at desc);

-- Kept 90 days. Run this line again whenever you like (or schedule it with
-- pg_cron if that extension is switched on); nothing else deletes rows.
delete from public.web_errors where created_at < now() - interval '90 days';
