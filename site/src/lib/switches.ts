// SWITCHES THE APP FOLLOWS WITHOUT A RELEASE (Hidde, 2026-11-05: "kunnen we
// deze vragenlijst uit de app halen zonder een release"). One file,
// data/app-switches.json: the website reads it here at build time, and
// /api/version.json sends it to the app, which asks on every launch and every
// return (Kit/AppSwitches.swift). Remote Config's shape, without a service:
// a decision travels as data (CLAUDE.md, "Both surfaces by default").
//
// A missing file or key means ON, so a build never hides something by
// accident.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

export type SwitchName = "plus_ask" | "android_review_question";

let cached: Record<string, unknown> | null = null;

function load(): Record<string, unknown> {
  if (cached) return cached;
  try {
    cached = JSON.parse(fs.readFileSync(path.join(DATA, "app-switches.json"), "utf-8"));
  } catch {
    cached = {};
  }
  return cached!;
}

export function switchOn(name: SwitchName): boolean {
  return load()[name] !== false;
}

/** Every switch, for /api/version.json. */
export function switches(): Record<SwitchName, boolean> {
  return { plus_ask: switchOn("plus_ask"), android_review_question: switchOn("android_review_question") };
}
