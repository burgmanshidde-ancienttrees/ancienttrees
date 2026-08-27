-- Where the app's crashes and hangs land.
--
-- Hidde, 2026-08-27: "crash reporting zullen we daar eens mee beginnen dan."
-- The app half is Kit/Diagnostics.swift and it uses MetricKit, which is Apple's
-- own and needs no third party, no SDK and no bill. This is the other end.
--
-- WHAT ARRIVES: one row per crash or hang, at most once a day per phone, only
-- from real devices. It carries the payload Apple assembled, the app version
-- and the OS version, and NOTHING that says who it came from: no user id, no
-- email, no location. That is deliberate rather than sloppy. A crash does not
-- need to know whose it was, and not linking it is what keeps this out of the
-- "data linked to you" half of the App Store privacy label.
--
-- INSERTS ARE ANONYMOUS, and they have to be: an app that crashes before
-- anybody signs in is exactly the app you most want to hear from. The trade is
-- that the publishable key can write here, so anybody who reads the key out of
-- the app can post rubbish. The size cap is in the app and the one below is the
-- backstop; if it is ever abused, the answer is a rate limit at the edge rather
-- than closing the door on signed-out crashes.

create table if not exists public.diagnostics (
  id bigint generated always as identity primary key,
  kind text not null check (kind in ('crash', 'hang')),
  app_version text not null check (char_length(app_version) <= 40),
  os_version text not null check (char_length(os_version) <= 120),
  -- Text rather than jsonb: Apple changes the shape of this payload between
  -- releases, and a row that fails to insert because a field moved tells you
  -- nothing about the crash it was describing.
  payload text not null check (char_length(payload) <= 262144),
  created_at timestamptz not null default now()
);

alter table public.diagnostics enable row level security;

drop policy if exists "anybody may report a crash" on public.diagnostics;
create policy "anybody may report a crash" on public.diagnostics
  for insert with check (true);

-- Nothing reads these back through the app. They are for the service key and
-- for whoever is looking at what broke.

create index if not exists diagnostics_recent on public.diagnostics (created_at desc);
