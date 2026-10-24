// HOW MANY READERS SAVED A TREE, counts only, from data/tree-saves.json
// (scripts/tree_saves.py, nightly). Hidde, 2026-10-24, on which tree gets the
// full pin where two collide: "i think photo and likes are the best way."
// Read here once per build; zero for a tree nobody has saved, and zero for
// every tree when the file is missing, so a build never depends on it.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

let cached: Record<string, number> | null = null;

function load(): Record<string, number> {
  if (cached) return cached;
  try {
    const doc = JSON.parse(fs.readFileSync(path.join(DATA, "tree-saves.json"), "utf-8"));
    cached = doc.saves ?? {};
  } catch {
    cached = {};
  }
  return cached!;
}

/** Readers' Want to go saves of this tree, our own accounts left out. */
export function savesOf(treeId: string): number {
  return load()[treeId] ?? 0;
}
