// THE FLAG GUESS AS A FILE (Hidde, 2026-10-29: "cant we just auto fill it for
// them from now on?"). Only 3 of 51 profiles had a flag, because the default
// was written only when somebody opened their own account page. signin-js now
// loads this once, at the moment of a sign-in on any page, and writes the
// guess then; the zone table is 10 KB, so no page carries it for nothing.
import { COUNTRY_CORE_JS } from "../lib/countries";

export const prerender = true;

export async function GET() {
  return new Response(COUNTRY_CORE_JS,
                      { headers: { "Content-Type": "text/javascript" } });
}
