// WHAT READERS DID WITH A TREE, counts only, from data/tree-saves.json
// (scripts/tree_saves.py, nightly). Hidde, 2026-10-24, on which tree gets the
// full pin where two collide: "i think photo and likes are the best way."
// Since 2026-11-05 the file also counts "Worth the visit" votes and visible
// notes, which order a place's Highlights (lib/highlights.ts).
// Read here once per build; zero for a tree nobody touched, and zero for every
// tree when the file is missing, so a build never depends on it.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

type Doc = { saves: Record<string, number>; worth: Record<string, number>; notes: Record<string, number> };
let cached: Doc | null = null;

function load(): Doc {
  if (cached) return cached;
  try {
    const doc = JSON.parse(fs.readFileSync(path.join(DATA, "tree-saves.json"), "utf-8"));
    cached = { saves: doc.saves ?? {}, worth: doc.worth ?? {}, notes: doc.notes ?? {} };
  } catch {
    cached = { saves: {}, worth: {}, notes: {} };
  }
  return cached!;
}

/** Readers' Want to go saves of this tree, our own accounts left out. */
export function savesOf(treeId: string): number {
  return load().saves[treeId] ?? 0;
}

/** Readers whose standing vote on this tree is "Worth the visit". */
export function worthOf(treeId: string): number {
  return load().worth[treeId] ?? 0;
}

/** Readers' visible notes on this tree. */
export function notesOf(treeId: string): number {
  return load().notes[treeId] ?? 0;
}
