# Database backup and restore

Since 2026-11-04 (Hidde: "ok lets do option 1"): the free Supabase plan keeps no backup we can restore, so .github/workflows/db-backup.yml makes one. Once a week the whole database (our tables, the accounts, the file index) and every stored file (avatars, readers' photographs) go into one archive, encrypted with Hidde's passphrase and kept 90 days as an artifact of that workflow. It runs daily and only works when the last good backup is six or more days old, so a skipped day is caught the next day.

## Setup, once (Hidde)

1. Supabase dashboard, the Ancient Trees project, **Connect** at the top, tab **Session pooler**, copy the **URI**. Replace `[YOUR-PASSWORD]` in it with the database password (Project Settings, Database; reset it there if nobody has it, then put it in the password manager). The session pooler, not the direct connection: GitHub's machines cannot reach the direct one.
2. Make up a long passphrase for the backups and put it in the password manager as "Ancient Trees backup passphrase". Without it no backup can be opened, by anyone, ever.
3. GitHub, the repository, **Settings**, **Secrets and variables**, **Actions**, **New repository secret**, twice:
   - Name `SUPABASE_DB_URL`, value: the URI from step 1.
   - Name `BACKUP_PASSPHRASE`, value: the passphrase from step 2.
4. GitHub, **Actions**, **Database backup**, **Run workflow**. Green means the first backup exists.

## Restore (a session with Hidde)

1. Actions, Database backup, the run you want, download the artifact `ancienttrees-backup-<date>` and unzip it.
2. `gpg --decrypt ancienttrees-<date>.tar.gz.gpg > backup.tar.gz` (asks for the passphrase), then `tar -xzf backup.tar.gz`.
3. `backup/database.sql` is plain SQL. Restore into a NEW Supabase project first, never over the live one: `psql "<new project's session pooler URI>" -f backup/database.sql`. Compare row counts with the live project before deciding anything.
4. `backup/storage/<bucket>/...` are the files, uploaded back with the Supabase dashboard or the storage API under the same paths. Since 2026-11-13 only one backup in 28 days holds every file (`ancienttrees-backup-<date>`); the weekly ones between hold only the files changed since the backup before (`ancienttrees-backup-<date>-new`), to stay inside the free plan's egress. So unpack the newest full one, then every `-new` after it in date order over the top. The database dump in each is whole.

## The quarterly test

Once a quarter a session does steps 1 to 3 into a scratch Supabase project and checks that the row counts of `profiles`, `saves`, `sightings` and `tree_notes` match the live ones on the backup's date, then deletes the scratch project. A backup nobody has opened is a hope, not a backup.
