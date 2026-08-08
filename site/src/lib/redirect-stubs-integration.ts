import fs from "node:fs";
import path from "node:path";
import type { AstroIntegration } from "astro";
import { buildRedirectStubs, renderRedirectStub } from "./redirect-map.ts";

/** Writes every legacy-URL redirect stub straight to dist/ after the build,
 * bypassing Astro's own `redirects` config (see redirect-map.ts for why). */
export default function redirectStubsIntegration(): AstroIntegration {
  return {
    name: "ancienttrees-redirect-stubs",
    hooks: {
      "astro:build:done": async ({ dir, logger }) => {
        const distRoot = fileURLToDir(dir);
        const stubs = buildRedirectStubs();
        for (const stub of stubs) {
          const outFile = path.join(distRoot, stub.outputPath);
          fs.mkdirSync(path.dirname(outFile), { recursive: true });
          fs.writeFileSync(outFile, renderRedirectStub(stub.targetRelative, stub.canonical, stub.title));
        }
        logger.info(`wrote ${stubs.length} redirect stub(s)`);
      },
    },
  };
}

function fileURLToDir(dir: URL): string {
  return dir.protocol === "file:" ? new URL(dir).pathname : String(dir);
}
