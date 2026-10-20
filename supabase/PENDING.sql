-- APPLIED 2026-10-20 by Hidde (checked: profiles.flag_hidden answers, false
-- for every row). Nothing pending.
--
-- "DON'T SHOW" FOR THE FLAG. Until somebody chooses, the app and the website
-- give them the flag of where they appear to be; this column remembers a
-- deliberate "Don't show" so the default never comes back.

alter table public.profiles add column if not exists flag_hidden boolean not null default false;
