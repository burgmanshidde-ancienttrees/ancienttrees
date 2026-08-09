// Ported from check_count_promises(), build_site.py:2915-2975.
//
// A city that grows past ten must stop promising ten. Florence went to
// fifteen with three separate sentences still saying ten, one of them a FAQ
// answer counting which six of the ten were free. The title is generated
// and corrects itself; hand-written copy does not, and nothing was watching
// it until this check existed. It caught four more live count lies (NYC,
// Venice, Lyon, Den Bosch) after being widened - this is an active check,
// not a dead one, and CLAUDE.md's ratchet says removing it needs Hidde.
const NUMBER_WORDS: Record<string, number> = Object.fromEntries(
  "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty"
    .split(" ")
    .map((w, n) => [w, n]),
);
// Digits count too, not only spelled-out words. Paris's copy said "15 more"
// and "23 more" rather than "fifteen more"/"twenty-three more" (twenty-three
// has no entry above anyway), and a word-only pattern let both go stale
// unnoticed until a fresh-eyes review caught them by eye (build_site.py,
// origin/main 0fc4993, REVIEW.md 2026-08-08).
const N = `\\d+|${Object.keys(NUMBER_WORDS).join("|")}`;

const SUMMARY = new Set(["meta_description", "question_meta"]);
const ALL_COPY = new Set(["intro", "meta_description", "question_meta", "question_answer", "question_context", "faq"]);

interface PromisePattern {
  rx: RegExp;
  allowed: (n: number) => Set<number>;
  scope: Set<string>;
}

// Three shapes, each deliberately narrow. A page counts other things all the
// time ("the two trees frame two kinds of longevity", "only four trees in
// the whole city carry the designation"), so only a phrase that can just
// about only mean "this is how many trees this page has" is allowed to fail
// a build.
const PROMISE: PromisePattern[] = [
  // "Naples's ten most remarkable trees"
  { rx: new RegExp(`\\b(${N})\\s+(?:most|remarkable)\\b`, "gi"), allowed: (n) => new Set([n]), scope: ALL_COPY },
  // "its story, and nine more". One or two trees are named before it. Only
  // in the two summary fields: in body prose "five more planted by the
  // residents" is Bath counting the five planes inside a single entry.
  { rx: new RegExp(`\\b(${N})\\s+more\\b`, "gi"), allowed: (n) => new Set([n + 1, n + 2]), scope: SUMMARY },
  // "six of the ten trees on this list", "none of these ten need a ticket"
  { rx: new RegExp(`\\bof the\\s+(${N})\\s+trees?\\b`, "gi"), allowed: (n) => new Set([n]), scope: ALL_COPY },
  {
    rx: new RegExp(`\\b(?:these|the)\\s+(${N})\\s+(?:are|is|need|needs|were|was|stand|stands|remain|listed|below)\\b`, "gi"),
    allowed: (n) => new Set([n]),
    scope: ALL_COPY,
  },
  // "All sixteen are free to see", "All sixteen trees on this list". Vienna
  // grew to nineteen with both of these live in the intro and FAQ while the
  // meta fields were caught: the second time this class slipped in one day,
  // so per the ratchet it becomes pattern rather than vigilance. Anchored on
  // trees/are/stand/need so "all five trunks" inside an entry stays legal.
  {
    rx: new RegExp(`\\ball\\s+(${N})\\s+(?:trees?|are|stand|need|needs|remain)\\b`, "gi"),
    allowed: (n) => new Set([n]),
    scope: ALL_COPY,
  },
];

interface CountPromiseCity {
  trees?: unknown[];
  intro?: string;
  meta_description?: string;
  question_meta?: string;
  question_answer?: string;
  question_context?: string;
  faq?: { q: string; a: string }[];
}

export function checkCountPromises(cityData: CountPromiseCity, canonical: string): void {
  const n = (cityData.trees ?? []).length;
  const fields: [string, string][] = (
    ["intro", "meta_description", "question_meta", "question_answer", "question_context"] as const
  ).map((k) => [k, cityData[k] ?? ""]);
  for (const f of cityData.faq ?? []) {
    fields.push(["faq", f.q ?? ""], ["faq", f.a ?? ""]);
  }
  for (const [key, text] of fields) {
    if (!text) continue;
    for (const { rx, allowed, scope } of PROMISE) {
      if (!scope.has(key)) continue;
      rx.lastIndex = 0;
      let m: RegExpExecArray | null;
      while ((m = rx.exec(text))) {
        const word = m[1].toLowerCase();
        const claims = allowed(/^\d+$/.test(word) ? parseInt(word, 10) : NUMBER_WORDS[word]);
        const minClaim = Math.min(...claims);
        if (minClaim < 4 || claims.has(n)) continue;
        const claimsStr = [...claims].sort((a, b) => a - b).join("/");
        throw new Error(
          `${canonical}: copy still promises ${claimsStr} trees but the city has ${n} (${JSON.stringify(m[0])})`,
        );
      }
    }
  }
}
