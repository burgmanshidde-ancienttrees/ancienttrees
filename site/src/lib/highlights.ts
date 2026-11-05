// WHICH TREES OF A PLACE ARE ITS HIGHLIGHTS (Hidde, 2026-11-05, direction C
// of the city page: a shelf of highlights above the list of every tree).
//
// One rule, decided here and sent as data: the website's city page draws its
// Highlights from this, and the app reads `highlight` on each tree in the feed
// (lib/app-feed.ts), so neither client decides it for itself.
//
// For now a highlight is a photographed tree. Later the rule can pick
// (the oldest, the most saved, the ones with readers' photographs) without
// touching either client.
import { usablePhoto, type TreeLike } from "./images";

export function isHighlight(tree: TreeLike): boolean {
  return Boolean(usablePhoto(tree)?.url);
}
