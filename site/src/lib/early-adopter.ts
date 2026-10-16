// The early-adopter badge: every account opened before the paid tier goes live.
//
// Hidde, 2026-10-16: "Build it like this on web and app, with the one-time
// sheet. Cutoff: the day the paid tier goes live." Convention: komoot's Pioneer
// pill (CONVENTIONS.md 2026-10-02), the shape our ambassador badge already
// wears, in gold rather than moss so the two never read as the same thing.
// Polarsteps was the reference he named; its badge is not documented anywhere
// we could read (searched 2026-10-16), so the shape is ours, not theirs.
//
// WHO HAS IT is decided by two facts, neither of them the device's (hard rule
// 11): the account's created_at, as /auth/v1/user returns it, and this cutoff.
// Null means the window is still open, so every account has the badge. The
// day the paid tier goes live this becomes that date ("2027-03-01"), and an
// account opened on or after it does not get the badge. The website reads this
// constant at build time; the app reads the same value from /api/version.json
// (early_adopter_until), so the decision travels as data and is written once.
//
// The one-time sheet is remembered on the ACCOUNT, in the auth user's own
// metadata (early_adopter_seen), so a second device does not show it again.
// That flag is not personal data: it records that a sheet was closed.
export const EARLY_ADOPTER_UNTIL: string | null = null;

export function isEarlyAdopter(createdAt: string | undefined, until = EARLY_ADOPTER_UNTIL): boolean {
  if (!createdAt) return false;
  if (!until) return true;
  return createdAt < until;
}
