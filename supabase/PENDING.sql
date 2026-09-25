-- PENDING: one fix to walks.sql, 2026-09-26. The stop check let a stop with no
-- position through (NULL comparison). Paste this; it replaces one function and
-- is safe to run twice. Empty this file again after the rule test passes.
--
-- When a new column or table is written, put its statement here as well, with
-- `if not exists`, so one paste in the SQL editor brings the database level.
-- `python3 scripts/sqlcheck.py` asks the live database what is still missing.

create or replace function public.walk_stops_ok(s jsonb) returns boolean
language sql immutable as $$
  select jsonb_typeof(s) = 'array'
     and jsonb_array_length(s) <= 40
     and not exists (
       select 1 from jsonb_array_elements(s) e
        where jsonb_typeof(e) is distinct from 'object'
           or jsonb_typeof(e -> 'name') is distinct from 'string'
           or jsonb_typeof(e -> 'lat') is distinct from 'number'
           or jsonb_typeof(e -> 'lng') is distinct from 'number'
           or ((e ? 'treeId' and e -> 'treeId' <> 'null'::jsonb)
               = (e ? 'sightingId' and e -> 'sightingId' <> 'null'::jsonb))
     )
$$;
