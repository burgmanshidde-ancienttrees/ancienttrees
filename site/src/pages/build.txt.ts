// WHICH COMMIT THE LIVE SITE IS.
//
// Written 2026-09-23, after finding the site was four days behind main and
// nothing anywhere could say so. The cause is ordinary GitHub behaviour and
// not a bug here: a push made with GITHUB_TOKEN never triggers another
// workflow, and the night runs push with exactly that, so deploy.yml fires
// only when a person pushes from a laptop. Between 19 and 23 September nobody
// did, and every tree, translation and blueprint change from those four days
// sat in main while ancienttrees.app served the 19th.
//
// Nothing could see it. /api/version.json hashes the CONTENT of the feeds, so
// it answers "has the data changed" for a phone and cannot answer "is what you
// are serving current", which is a different question: a day with no new trees
// produces the same hash whether it deployed or not. health.py now reads this
// file instead, and `git rev-list <sha>..origin/main` turns it into a number.
//
// Plain text on purpose: no schema, nothing the app decodes, nothing that can
// break a feed contract by existing.
export const prerender = true;

export async function GET() {
  const sha = process.env.GITHUB_SHA || "local";
  return new Response(`${sha}\n${new Date().toISOString()}\n`,
                      { headers: { "Content-Type": "text/plain" } });
}
