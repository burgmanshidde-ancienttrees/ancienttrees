// The tokens a hand-written question_answer must mention: at least one
// distinctive proper noun from the oldest tree's name, so the title, pin
// and read-more link never point at a different tree than the prose names
// (build_site.py:3346-3358; caught live on Amsterdam and Tokyo).
export const GENERIC_WORDS = new Set([
  "the", "of", "and", "tree", "trees", "oak", "yew", "yews", "ginkgo",
  "olive", "olives", "plane", "planes", "cedar", "cypress", "linden",
  "lime", "ficus", "pine", "elm", "ash", "beech", "chestnut", "wood",
  "grove", "ring", "garden", "gardens", "old", "great", "monumental",
  "king", "queen", "prince", "princess", "royal", "grand", "giant",
  "ancient", "sacred", "holy", "wishing", "guardian",
  "de", "del", "della", "der", "du", "la", "le", "el", "van", "dos",
  "das", "do", "di", "san", "santa",
]);
