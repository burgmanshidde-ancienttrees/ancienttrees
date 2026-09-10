// Which wording a page is showing, when a copy test is running.
//
// Written 2026-09-10 with scripts/copytest.py, which owns everything else
// about a test: the arms, the matched-pair assignment, the frozen pre-period
// and the reading. This file does one thing, look up the arm for a slug, and
// deliberately holds no rule of its own. That is the 2026-08-25 both-surfaces
// lesson applied here: the ANSWER travels (a slug is in this arm), the RULE
// stays on the server. A second implementation of the assignment in TypeScript
// would drift from the Python one within a week, and a test whose two halves
// disagree about who is in which arm measures nothing at all.
//
// English only, and that is not an oversight. A translated page builds its own
// title through the i18n layer, so an arm applied there would be testing a
// different sentence in a different language against the same control.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

type Test = {
  id: string;
  surface: string;
  status: string;
  assignment: Record<string, string>;
};

let cached: Test[] | null = null;

function tests(): Test[] {
  if (cached) return cached;
  const f = path.join(DATA, "copy-tests.json");
  if (!fs.existsSync(f)) return (cached = []);
  try {
    cached = (JSON.parse(fs.readFileSync(f, "utf-8")).tests ?? []) as Test[];
  } catch {
    // A malformed registry must never take the build down: every page simply
    // renders its control wording, which is what it shipped yesterday.
    cached = [];
  }
  return cached;
}

/** The arm this page is in for the running test on `surface`, or "control".
 *  A city added after a test started is not in the assignment and gets the
 *  control, because an arm somebody joins halfway through is not an arm. */
export function arm(surface: string, slug: string): string {
  for (const t of tests()) {
    if (t.status !== "running" || t.surface !== surface) continue;
    return t.assignment[slug] ?? "control";
  }
  return "control";
}
