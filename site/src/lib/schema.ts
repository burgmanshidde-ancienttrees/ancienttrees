// Ported from breadcrumb_schema()/ld_script(), build_site.py:1160-1196, and
// the site-level WebSite+Organization graph (build_site.py:986-987, P5:
// Organization not a named Person, per the owner-privacy rule).
export const BASE_URL = "https://ancienttrees.app";

export const SITE_SCHEMA = [
  { "@type": "WebSite", name: "Ancient Trees", url: BASE_URL },
  { "@type": "Organization", name: "Ancient Trees", url: BASE_URL },
];

export type Crumb = [name: string, url: string | null];

/** Google requires every ListItem to carry an "item". Crumbs without a page
 * of their own (a country not yet published, or the current page itself)
 * fall back to the page's own canonical URL for the LAST crumb only,
 * exactly as Google's docs prescribe (an intermediate crumb doing the same
 * once wrongly claimed the country WAS the tree page). */
export function breadcrumbSchema(items: Crumb[], pageUrl?: string) {
  const elements = items.map(([name, url], i) => {
    const position = i + 1;
    const el: Record<string, unknown> = { "@type": "ListItem", position, name };
    if (url) {
      el.item = url;
    } else if (position === items.length && pageUrl) {
      el.item = pageUrl;
    }
    return el;
  });
  return { "@type": "BreadcrumbList", itemListElement: elements };
}

export function ldScript(graph: unknown[]): string {
  const payload = { "@context": "https://schema.org", "@graph": graph };
  return `<script type="application/ld+json">${JSON.stringify(payload)}</script>`;
}
