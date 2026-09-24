// Every icon on the site comes from here, and here reads Phosphor's own files.
//
// Hidde, 2026-09-24: "can you never ever draw icons by hand". Until that day
// every glyph on the website was an SVG path somebody typed to look roughly
// like the app's SF Symbol, which is why the two surfaces never matched. The
// files under site/src/icons/phosphor/ are fetched unchanged from
// @phosphor-icons/core 2.1.1 (MIT), and the README there maps each SF Symbol
// the app uses to its Phosphor twin. scripts/iconcheck.py refuses new
// hand-drawn geometry on push.
//
// BOLD is the default weight because it is the one that matches SF Symbols'
// regular weight at UI sizes; Phosphor's own regular reads thin beside the app
// (compared side by side against the app's tree page, 2026-09-24).
//
// A missing icon throws at build time rather than rendering nothing, so the
// answer to "we need a glyph" is always to fetch the file, never to draw one.

const FILES = import.meta.glob("../icons/phosphor/**/*.svg", {
  query: "?raw", import: "default", eager: true,
}) as Record<string, string>;

export type IconWeight = "regular" | "bold" | "fill";

export function icon(name: string, weight: IconWeight = "bold", cls = "ic"): string {
  const path = weight === "regular"
    ? `../icons/phosphor/regular/${name}.svg`
    : `../icons/phosphor/${weight}/${name}-${weight}.svg`;
  const svg = FILES[path];
  if (!svg) {
    throw new Error(`icon ${weight}/${name} is not vendored. Fetch it from `
      + `cdn.jsdelivr.net/npm/@phosphor-icons/core@2.1.1/assets/${weight}/ into `
      + `site/src/icons/phosphor/${weight}/; never draw one (Hidde, 2026-09-24).`);
  }
  return svg.trim().replace("<svg ", `<svg class="${cls}" aria-hidden="true" focusable="false" `);
}
