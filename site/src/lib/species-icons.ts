// Ported verbatim from SPECIES_ICONS/SPECIES_ARCHETYPES/species_icon(),
// build_site.py:2284-2401. Map pins are drawn, not numbered: a handful of
// species-true silhouettes that read at pin size, falling back to a
// broadleaf crown for anything unmatched. Every tree already carries a
// species, so this gives 100% pin coverage without depending on photos.
import { speciesCommon } from "./species";
import type { Tree } from "./trees";

export const SPECIES_ICONS: Record<string, string> = {
  broadleaf:
    '<path opacity=".45" d="M20 5c-5 0-8 3-9 6-3 .5-5 3-5 6 0 4 3 7 7 7h14c4 0 7-3 7-7 0-3-2-5.5-5-6-1-3-4-6-9-6z"/>' +
    '<path d="M20 8c-4.5 0-7.5 2.5-8.5 5.5C8.5 14 6.5 16 6.5 19c0 3.5 3 6 6.5 6h14c3.5 0 6.5-2.5 6.5-6 0-3-2-5-5-5.5C27.5 10.5 24.5 8 20 8z"/>' +
    '<path d="M18.8 38h2.4l-.7-13h-1z"/>',
  oak:
    '<path opacity=".45" d="M8 20c-2-1-3-3-2.5-5C4 13 5 10 8 9.5 8.5 6.5 11.5 5 14 6c1.5-2.5 6-3.5 8.5-1.5C26 3 30 4.5 30.5 8c3 0 5 2.5 4.5 5.5 1.5 1.5 1.5 4.5-.5 6z"/>' +
    '<path d="M9.5 21.5c-2.5-.5-4-3-3-5.5-1-2 .5-4.5 3-5C10 8.5 12.5 7 15 8c2-2.5 6-2.5 8 0 2.5-1 5.5.5 6 3 2.5.5 4 3 3 5-1 2.5-2.5 4-5 4.5z"/>' +
    '<path d="M17.5 38h5l-1.2-9 4.5-4-1-1.5-4 3-.3-6h-1.5l-.3 6-4-3-1 1.5 4.5 4z"/>' +
    '<ellipse opacity=".45" cx="29" cy="24" rx="1.6" ry="2.2"/>',
  plane:
    '<path opacity=".45" d="M20 3c-6 0-10 3.5-10.5 8-2.5 1-4 3.5-4 6 0 4 3 6.5 6.5 6.5h16c3.5 0 6.5-2.5 6.5-6.5 0-2.5-1.5-5-4-6C30 6.5 26 3 20 3z"/>' +
    '<path d="M20 6c-5 0-8.5 3-9 7-2 .8-3.5 2.7-3.5 5 0 3 2.5 5.5 5.5 5.5h14c3 0 5.5-2.5 5.5-5.5 0-2.3-1.5-4.2-3.5-5-.5-4-4-7-9-7z"/>' +
    '<path d="M19 38h2.2l-.5-14.5h-1.2z"/>' +
    '<path d="M14 23.5l-.3 3.2m0 0a1.8 1.8 0 101.8 1.8 1.8 1.8 0 00-1.8-1.8z"/>' +
    '<path opacity=".45" d="M26.5 23.5l.3 2.2m0 0a1.6 1.6 0 101.6 1.6 1.6 1.6 0 00-1.6-1.6z"/>',
  ginkgo:
    '<path opacity=".45" d="M20 4C11 6 6 13 6.5 21c.3 4 2.5 7 5.5 9l8-9.5L28 30c3-2 5.2-5 5.5-9C34 13 29 6 20 4z"/>' +
    '<path d="M20 7c-7 1.8-11 7.5-10.7 14 .2 3 1.7 5.6 4 7.3L19.5 21l.5-11 .5 11 6.2 7.3c2.3-1.7 3.8-4.3 4-7.3C31 14.5 27 8.8 20 7z"/>' +
    '<path d="M19 38h2l-.4-10h-1.2z"/>',
  cedar:
    '<path d="M8 13h24l-7-5H15z"/>' +
    '<path opacity=".45" d="M6 20h28l-6.5-4.5h-15z"/>' +
    '<path d="M4.5 27h31l-7-4.5H11.5z"/>' +
    '<path d="M19 38h2.4l-.6-11h-1.2z"/>',
  pine:
    '<path opacity=".45" d="M20 3C11 3 5.5 8 5 13.5 8 16 13.5 17.5 20 17.5S32 16 35 13.5C34.5 8 29 3 20 3z"/>' +
    '<path d="M20 5.5c-7.5 0-12.5 4-13 8.5 2.7 2 7.5 3 13 3s10.3-1 13-3c-.5-4.5-5.5-8.5-13-8.5z"/>' +
    '<path d="M18.5 38h3.5c-1-7-1.2-13-.7-21l-1.8-.2c-.8 8-1 14.5-1 21.2z" transform="rotate(-4 20 27)"/>',
  cypress:
    '<path opacity=".45" d="M20 2c-5 5-8 12-8 20 0 6 3 11 8 13 5-2 8-7 8-13 0-8-3-15-8-20z"/>' +
    '<path d="M20 5c-4 4.5-6.3 10.5-6.3 17 0 5 2.4 9.2 6.3 11 3.9-1.8 6.3-6 6.3-11 0-6.5-2.3-12.5-6.3-17z"/>' +
    '<path d="M19.2 38h1.6v-3h-1.6z"/>',
  yew:
    '<path opacity=".45" d="M20 8C10 8 3.5 14 3.5 21c0 5 4 9 10 9h13c6 0 10-4 10-9 0-7-6.5-13-16.5-13z"/>' +
    '<path d="M20 11c-8.5 0-14 5-14 10.5 0 4 3.3 7 8 7h12c4.7 0 8-3 8-7C34 16 28.5 11 20 11z"/>' +
    '<path d="M15 38h2.5l.5-10h-1.5zM22.5 38H25l-1-10h-1.5zM19 38h2v-9h-2z"/>',
  sequoia:
    '<path opacity=".45" d="M20 1c-4 6-6.5 14-6.5 22 0 5 1.5 9 4 11.5h5c2.5-2.5 4-6.5 4-11.5C26.5 15 24 7 20 1z"/>' +
    '<path d="M20 4.5c-3 5-5 11.5-5 18.5 0 4.5 1.3 8 3.2 10h3.6c1.9-2 3.2-5.5 3.2-10 0-7-2-13.5-5-18.5z"/>' +
    '<path d="M16 38h8l-1.5-5h-5z"/>',
  fig:
    '<path opacity=".45" d="M20 4C10.5 4 4 10 4 17c0 5 3.5 8.5 8.5 9h15c5-.5 8.5-4 8.5-9 0-7-6.5-13-16-13z"/>' +
    '<path d="M20 7C11.5 7 6 12 6 17.5c0 4 3 7 7 7.5h14c4-.5 7-3.5 7-7.5C34 12 28.5 7 20 7z"/>' +
    '<path d="M14 38h12c-.5-2.5-1.5-4-3-5.5l-1-7.5h-4l-1 7.5c-1.5 1.5-2.5 3-3 5.5z"/>' +
    '<path opacity=".45" d="M12 38l2-4.5 1.5 1L14.5 38zM28 38l-2-4.5-1.5 1 1 3.5z"/>',
  wingnut:
    '<path opacity=".45" d="M20 4C11 4 5 9.5 5 16c0 4.5 3 8 7.5 8.5h15C32 24 35 20.5 35 16c0-6.5-6-12-15-12z"/>' +
    '<path d="M20 7c-7.5 0-13 4.5-13 10 0 3.5 2.5 6.5 6 7h14c3.5-.5 6-3.5 6-7 0-5.5-5.5-10-13-10z"/>' +
    '<path d="M19 38h2l-.4-14h-1.2z"/>' +
    '<path opacity=".45" d="M12.5 24.5h1.2v3.5a1.4 1.4 0 11-1.2 0zM26.3 24.5h1.2v5a1.4 1.4 0 11-1.2 0z"/>' +
    '<path d="M23 24.5h1.2v7a1.4 1.4 0 11-1.2 0z"/>',
  wisteria:
    '<path d="M8 10c4-4.5 12-6 17-3.5 4 2 7 5.5 7.5 10l-2 .8C29.5 13.5 27 11 24 9.5 20 7.5 13.5 8.5 10 12z"/>' +
    '<path opacity=".45" d="M13 12.5a3.2 5.5 0 103.2 5.5 3.2 5.5 0 00-3.2-5.5z"/>' +
    '<path d="M20 13.5a3.5 6.5 0 103.5 6.5 3.5 6.5 0 00-3.5-6.5z"/>' +
    '<path opacity=".45" d="M27 12a3 5 0 103 5 3 5 0 00-3-5z"/>' +
    '<path d="M8.5 38h2.5c.5-9 .5-18-.5-27l-2 .3c1 9 .8 17.7 0 26.7z"/>',
  rosette:
    '<path d="M18.5 38h3l-1-16h-1z"/>' +
    '<path d="M20 22c-1-6-4.5-10-10-11 4-1.5 8 0 10 3-1-5 1-9 5-11-1 4 .5 8 3 10 2-3.5 6-5 9.5-4-4.5 2.5-7 5.5-7.5 9-.5-.5-5-.5-10 4z" transform="translate(0,1)"/>' +
    '<path opacity=".45" d="M20 23c-3.5-2.5-8-3-11.5-1 3.5 1 6.5 2.5 8.5 5zM20 23c3.5-2.5 8-3 11.5-1-3.5 1-6.5 2.5-8.5 5z"/>',
  pagoda:
    '<path opacity=".45" d="M12 10a6 4.5 0 106 4.5A6 4.5 0 0012 10zM28 10a6 4.5 0 106 4.5 6 4.5 0 00-6-4.5z"/>' +
    '<path d="M20 5a7.5 5.5 0 107.5 5.5A7.5 5.5 0 0020 5z"/>' +
    '<path d="M13 16.5a6.5 5 0 106.5 5 6.5 5 0 00-6.5-5z"/>' +
    '<path opacity=".45" d="M27 16.5a6.5 5 0 106.5 5 6.5 5 0 00-6.5-5z"/>' +
    '<path d="M19 38h2.2l-.5-12h-1.2z"/>',
  olive:
    '<path opacity=".45" d="M13 15a6 5 0 106 5 6 5 0 00-6-5zM26 12a6.5 5.5 0 106.5 5.5A6.5 5.5 0 0026 12z"/>' +
    '<path d="M19 9a6.5 5.5 0 106.5 5.5A6.5 5.5 0 0019 9z"/>' +
    '<path d="M17 38h5c-.5-3.5-1.5-6-3.5-8.5 2-2 2.5-4.5 2-7.5l-2 .3c.4 2.5 0 4.5-1.8 6.2-1.5-2-2.2-4.2-2.2-7h-2c0 3.5 1 6.5 3 9-.3 2.7.5 5 1.5 7.5z"/>',
};

const SPECIES_ARCHETYPES: [string, string[]][] = [
  ["ginkgo", ["ginkgo"]],
  ["plane", ["plane"]],
  ["wingnut", ["wingnut"]],
  ["wisteria", ["wisteria"]],
  ["sequoia", ["sequoia", "redwood"]],
  ["cedar", ["cedar", "bald cypress", "montezuma", "fir", "spruce", "larch"]],
  ["pine", ["pine"]],
  ["yew", ["yew"]],
  ["cypress", ["cypress"]],
  ["fig", ["fig", "ombú", "ombu", "rubber", "banyan", "camphor"]],
  ["olive", ["olive", "elaeagnus"]],
  ["rosette", ["palm", "cycad", "dragon"]],
  ["pagoda", ["pagoda", "locust", "robinia", "acacia", "albizia"]],
  ["oak", ["oak"]],
];

/** Pick the silhouette for a tree. Falls back to a broadleaf crown, which is
 * what most of these city trees actually are. */
export function speciesIcon(tree: Tree): string {
  const name = speciesCommon(tree).toLowerCase();
  for (const [key, needles] of SPECIES_ARCHETYPES) {
    if (needles.some((n) => name.includes(n))) return SPECIES_ICONS[key];
  }
  return SPECIES_ICONS.broadleaf;
}
