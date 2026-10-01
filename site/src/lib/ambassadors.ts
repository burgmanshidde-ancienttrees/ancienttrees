// Who looks after a place, for the one line the city page may print.
//
// Reads data/ambassadors.json, which scripts/ambassador.py writes from the
// ambassadors table (and, for people who have no app account, from Hidde's own
// word). The website prints a NAME only where `public` is true and a
// display_name is present: that flag is the person's consent to be named, and
// the site names nobody without it (CLAUDE.md, 2026-08-11). Everything else in
// the file is for the app and for the sync, not for a page.
import fs from "node:fs";
import path from "node:path";

export interface Ambassador {
  user_id: string | null;
  place_slug: string;
  place_name: string;
  public: boolean;
  since: string | null;
  display_name?: string;
}

let cache: Ambassador[] | null = null;

function all(): Ambassador[] {
  if (cache) return cache;
  const file = path.join(process.cwd(), "../data/ambassadors.json");
  try {
    const doc = JSON.parse(fs.readFileSync(file, "utf-8"));
    cache = (doc.ambassadors ?? []) as Ambassador[];
  } catch {
    cache = [];
  }
  return cache;
}

/** The people who may be NAMED on this place's page, in the order they were
 *  granted. Empty for almost every place, which is the point: a line that is
 *  rare means something. */
export function namedAmbassadorsFor(slug: string): Ambassador[] {
  return all().filter((a) => a.place_slug === slug && a.public && a.display_name);
}
